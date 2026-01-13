import * as vscode from "vscode";
import * as path from "path";
import { LanguageClient, LanguageClientOptions, ServerOptions } from "vscode-languageclient/node";

let client: LanguageClient;

export async function activate(context: vscode.ExtensionContext) {
  console.log("RPC Study Language Server activating...");

  // Path to the language server
  const serverModule = context.asAbsolutePath(path.join("dist", "server", "index.js"));

  const serverOptions: ServerOptions = {
    run: { module: serverModule },
    debug: { module: serverModule, options: { execArgv: ["--nolazy", "--inspect=6009"] } },
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: "file", language: "typescript" },
      { scheme: "file", language: "javascript" },
    ],
    synchronize: {
      fileEvents: vscode.workspace.createFileSystemWatcher("**/*.{ts,js}"),
    },
  };

  client = new LanguageClient("rpc-study-lsp", "RPC Study Language Server", serverOptions, clientOptions);

  client.start();
  context.subscriptions.push(client);

  console.log("RPC Study Language Server started successfully");
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
