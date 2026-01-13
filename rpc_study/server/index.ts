import * as rpc from "vscode-languageserver";
import {
  TextDocumentSyncKind,
  InitializeResult,
  DidChangeTextDocumentParams,
  DidOpenTextDocumentParams,
  HoverParams,
  CompletionParams,
  CompletionItemKind,
} from "vscode-languageserver";
import { LSPHandlers } from "./handlers.js";
import { MetricsTracker } from "../metrics/tracker.js";
import {
  MetricsReadableWrapper,
  MetricsWritableWrapper,
} from "../metrics/stream-wrapper.js";
import { TrafficAnalyzer } from "../metrics/traffic-analyzer.js";

const handlers = new LSPHandlers();
const metrics = new MetricsTracker();
const trafficAnalyzer = new TrafficAnalyzer();

// Wrap stdin/stdout to capture actual wire bytes
const readWrapper = new MetricsReadableWrapper("server-in");
const writeWrapper = new MetricsWritableWrapper("server-out");

// Pipe stdin through our wrapper
process.stdin.pipe(readWrapper);
// Pipe our wrapper to stdout
writeWrapper.pipe(process.stdout);

// Create the language server connection using wrapped streams
const connection = rpc.createConnection(
  new (rpc as any).StreamMessageReader(readWrapper),
  new (rpc as any).StreamMessageWriter(writeWrapper)
);

connection.onInitialize((): InitializeResult => {
  console.error("[LSP] Initializing Language Server");
  trafficAnalyzer.recordMessageType("initialize", 0, 0);
  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Full,
      hoverProvider: true,
      completionProvider: {
        resolveProvider: false,
      },
      diagnosticProvider: {
        interFileDependencies: false,
        workspaceDiagnostics: false,
      },
    },
  };
});

connection.onDidOpenTextDocument((params: DidOpenTextDocumentParams) => {
  const startTime = Date.now();
  const { uri, text } = params.textDocument;
  handlers.didOpen(uri, text);
  const requestBytes = JSON.stringify(params).length;
  trafficAnalyzer.recordMessageType("textDocument/didOpen", requestBytes, 0);
  metrics.record({
    timestamp: startTime,
    operation: "textDocument/didOpen",
    bytesSent: text.length,
    bytesReceived: 0,
    latencyMs: Date.now() - startTime,
  });
});

connection.onDidChangeTextDocument((params: DidChangeTextDocumentParams) => {
  const startTime = Date.now();
  const { uri } = params.textDocument;
  const text = params.contentChanges[0]?.text || "";
  handlers.didChange(uri, text);
  const requestBytes = JSON.stringify(params).length;
  trafficAnalyzer.recordMessageType("textDocument/didChange", requestBytes, 0);
  metrics.record({
    timestamp: startTime,
    operation: "textDocument/didChange",
    bytesSent: text.length,
    bytesReceived: 0,
    latencyMs: Date.now() - startTime,
  });
});

connection.onHover((params: HoverParams) => {
  const startTime = Date.now();
  const { uri } = params.textDocument;
  const { line, character } = params.position;
  const result = handlers.hover(uri, { line, character });
  const requestBytes = JSON.stringify(params).length;
  const responseBytes = JSON.stringify(result).length;
  trafficAnalyzer.recordMessageType("textDocument/hover", requestBytes, responseBytes);
  metrics.record({
    timestamp: startTime,
    operation: "textDocument/hover",
    bytesSent: 0,
    bytesReceived: responseBytes,
    latencyMs: Date.now() - startTime,
  });
  return result;
});

connection.onCompletion((params: CompletionParams) => {
  const startTime = Date.now();
  const { uri } = params.textDocument;
  const { line, character } = params.position;
  const handlerResult = handlers.completion(uri, { line, character });

  // Convert to proper LSP CompletionItem format
  const result = handlerResult.map((item) => ({
    label: item.label,
    kind: item.kind as CompletionItemKind,
    detail: item.detail,
  }));

  const requestBytes = JSON.stringify(params).length;
  const responseBytes = JSON.stringify(result).length;
  trafficAnalyzer.recordMessageType("textDocument/completion", requestBytes, responseBytes);
  metrics.record({
    timestamp: startTime,
    operation: "textDocument/completion",
    bytesSent: 0,
    bytesReceived: responseBytes,
    latencyMs: Date.now() - startTime,
  });
  return result;
});

connection.onRequest("textDocument/diagnostic", (params: any) => {
  const startTime = Date.now();
  const { uri } = params.textDocument;
  const result = handlers.diagnostics(uri);
  const requestBytes = JSON.stringify(params).length;
  const responseBytes = JSON.stringify(result).length;
  trafficAnalyzer.recordMessageType("textDocument/diagnostic", requestBytes, responseBytes);
  metrics.record({
    timestamp: startTime,
    operation: "textDocument/diagnostic",
    bytesSent: 0,
    bytesReceived: responseBytes,
    latencyMs: Date.now() - startTime,
  });
  return result;
});

process.on("exit", () => {
  // Update traffic analyzer with final stream metrics
  trafficAnalyzer.setInMetrics(readWrapper.getMetrics());
  trafficAnalyzer.setOutMetrics(writeWrapper.getMetrics());

  console.error("\n=== SERVER METRICS ===");
  const data = metrics.getData();
  console.error(`Total requests: ${data.length}`);

  const operations = new Set(data.map((m) => m.operation));
  for (const op of operations) {
    const stats = metrics.getStats(op);
    if (stats) {
      console.error(`\n${op}:`);
      console.error(`  Count: ${stats.count}`);
      console.error(
        `  Latency: min=${stats.latency.min}ms, max=${stats.latency.max}ms, avg=${stats.latency.avg.toFixed(2)}ms`
      );
      console.error(`  Bytes Sent: ${stats.bytesSent.total}`);
      console.error(`  Bytes Received: ${stats.bytesReceived.total}`);
    }
  }

  // Print traffic analysis
  console.error("\n" + trafficAnalyzer.getSummary());

  // Print wire bytes comparison
  const inMetrics = readWrapper.getMetrics();
  const outMetrics = writeWrapper.getMetrics();
  console.error("\n=== WIRE BYTES (Actual) ===");
  console.error(`Actual bytes read from stdin: ${inMetrics.totalBytes}`);
  console.error(`Actual bytes written to stdout: ${outMetrics.totalBytes}`);
  console.error(`Total wire traffic: ${inMetrics.totalBytes + outMetrics.totalBytes} bytes`);
});

// Start the server. This will also start listening on stdin.
connection.listen();
