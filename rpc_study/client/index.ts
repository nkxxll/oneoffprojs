import { spawn, ChildProcessWithoutNullStreams } from "child_process";
import { createConnection } from "vscode-languageserver/node.js";
import * as rpc from "vscode-jsonrpc/node.js";
import { MetricsTracker } from "../metrics/tracker.js";
import {
  MetricsReadableWrapper,
  MetricsWritableWrapper,
} from "../metrics/stream-wrapper.js";
import { TrafficAnalyzer } from "../metrics/traffic-analyzer.js";

export class LSPClient {
  private connection: rpc.MessageConnection;
  private childProcess: ChildProcessWithoutNullStreams;
  private metrics: MetricsTracker;
  private trafficAnalyzer: TrafficAnalyzer;
  private readWrapper: MetricsReadableWrapper;
  private writeWrapper: MetricsWritableWrapper;

  constructor(serverPath: string, private verbose = false) {
    this.metrics = new MetricsTracker();
    this.trafficAnalyzer = new TrafficAnalyzer();

    // Spawn the server process
    this.childProcess = spawn("node", [serverPath], {
      stdio: ["pipe", "pipe", "pipe"],
    });

    // Forward server stderr to our stderr
    this.childProcess.stderr.on("data", (data) => {
      if (this.verbose) {
        process.stderr.write(`[server] ${data}`);
      }
    });

    // Wrap streams for metrics
    this.readWrapper = new MetricsReadableWrapper("client-in");
    this.writeWrapper = new MetricsWritableWrapper("client-out");

    // Pipe server stdout through read wrapper (server -> client)
    this.childProcess.stdout.pipe(this.readWrapper);
    // Pipe write wrapper to server stdin (client -> server)
    this.writeWrapper.pipe(this.childProcess.stdin);

    // Create JSON-RPC connection using wrapped streams
    this.connection = rpc.createMessageConnection(
      new rpc.StreamMessageReader(this.readWrapper),
      new rpc.StreamMessageWriter(this.writeWrapper)
    );

    this.connection.listen();
  }

  private async sendRequest(method: string, params: any): Promise<any> {
    return this.connection.sendRequest(method, params);
  }

  private sendNotification(method: string, params: any): void {
    this.connection.sendNotification(method, params);
  }

  async initialize(): Promise<any> {
    const startTime = Date.now();
    const params = {
      processId: process.pid,
      rootPath: null,
      rootUri: null,
      capabilities: {},
    };
    const bytesSent = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params,
    }).length;
    const result = await this.sendRequest("initialize", params);
    const latency = Date.now() - startTime;

    const bytesReceived = JSON.stringify(result).length;
    this.trafficAnalyzer.recordMessageType("initialize", bytesSent, bytesReceived);
    this.metrics.record({
      timestamp: startTime,
      operation: "initialize",
      bytesSent,
      bytesReceived,
      latencyMs: latency,
    });

    // Send initialized notification
    this.sendNotification("initialized", {});

    return result;
  }

  async hover(uri: string, line: number, character: number): Promise<any> {
    const startTime = Date.now();
    const params = {
      textDocument: { uri },
      position: { line, character },
    };
    const bytesSent = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "textDocument/hover",
      params,
    }).length;
    const result = await this.sendRequest("textDocument/hover", params);
    const latency = Date.now() - startTime;

    const bytesReceived = JSON.stringify(result).length;
    this.trafficAnalyzer.recordMessageType("textDocument/hover", bytesSent, bytesReceived);
    this.metrics.record({
      timestamp: startTime,
      operation: "textDocument/hover",
      bytesSent,
      bytesReceived,
      latencyMs: latency,
    });

    return result;
  }

  async completion(uri: string, line: number, character: number): Promise<any> {
    const startTime = Date.now();
    const params = {
      textDocument: { uri },
      position: { line, character },
    };
    const bytesSent = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "textDocument/completion",
      params,
    }).length;
    const result = await this.sendRequest("textDocument/completion", params);
    const latency = Date.now() - startTime;

    const bytesReceived = JSON.stringify(result).length;
    this.trafficAnalyzer.recordMessageType("textDocument/completion", bytesSent, bytesReceived);
    this.metrics.record({
      timestamp: startTime,
      operation: "textDocument/completion",
      bytesSent,
      bytesReceived,
      latencyMs: latency,
    });

    return result;
  }

  async diagnostic(uri: string): Promise<any> {
    const startTime = Date.now();
    const params = {
      textDocument: { uri },
    };
    const bytesSent = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "textDocument/diagnostic",
      params,
    }).length;
    const result = await this.sendRequest("textDocument/diagnostic", params);
    const latency = Date.now() - startTime;

    const bytesReceived = JSON.stringify(result).length;
    this.trafficAnalyzer.recordMessageType("textDocument/diagnostic", bytesSent, bytesReceived);
    this.metrics.record({
      timestamp: startTime,
      operation: "textDocument/diagnostic",
      bytesSent,
      bytesReceived,
      latencyMs: latency,
    });

    return result;
  }

  async close(): Promise<void> {
    this.connection.dispose();
    this.childProcess.kill();
  }

  getMetrics() {
    return this.metrics;
  }

  getTrafficAnalyzer() {
    return this.trafficAnalyzer;
  }

  getWireMetrics() {
    this.trafficAnalyzer.setInMetrics(this.readWrapper.getMetrics());
    this.trafficAnalyzer.setOutMetrics(this.writeWrapper.getMetrics());

    return {
      bytesReceived: this.readWrapper.getMetrics().totalBytes,
      bytesSent: this.writeWrapper.getMetrics().totalBytes,
      messagesReceived: this.readWrapper.getMetrics().messageCount,
      messagesSent: this.writeWrapper.getMetrics().messageCount,
    };
  }

  printTrafficSummary(): void {
    const wire = this.getWireMetrics();
    const estimated = this.metrics.getStats();

    console.log("\n=== CLIENT TRAFFIC ANALYSIS ===");
    console.log(this.trafficAnalyzer.getSummary());

    console.log("\n=== WIRE BYTES (Actual) ===");
    console.log(`Actual bytes received from server: ${wire.bytesReceived}`);
    console.log(`Actual bytes sent to server: ${wire.bytesSent}`);
    console.log(`Total wire traffic: ${wire.bytesReceived + wire.bytesSent} bytes`);

    if (estimated) {
      console.log("\n=== ESTIMATED vs ACTUAL ===");
      console.log(`Estimated bytes sent: ${estimated.bytesSent.total}`);
      console.log(`Actual bytes sent: ${wire.bytesSent}`);
      console.log(`Difference: ${wire.bytesSent - estimated.bytesSent.total} bytes (wire overhead)`);
    }
  }
}
