import { Hover, CompletionItem, Diagnostic, Position, Range } from "../shared/types.js";

// Static test document for MVP
const TEST_DOCUMENT = `function hello(name: string): string {
  return "Hello, " + name;
}

const greeting = hello("World");
console.log(greeting);
`;

export class LSPHandlers {
  private documents: Map<string, string> = new Map();

  constructor() {
    this.documents.set("file:///test.ts", TEST_DOCUMENT);
  }

  initialize() {
    return {
      capabilities: {
        hoverProvider: true,
        completionProvider: true,
        diagnosticProvider: true,
      },
    };
  }

  didOpen(uri: string, text: string) {
    this.documents.set(uri, text);
  }

  didChange(uri: string, text: string) {
    this.documents.set(uri, text);
  }

  hover(uri: string, position: Position): Hover | null {
    // Dummy hover response
    return {
      contents: "Function: hello(name: string): string",
    };
  }

  completion(uri: string, position: Position): CompletionItem[] {
    // Dummy completions
    return [
      { label: "console", kind: 2, detail: "Built-in console object" },
      { label: "function", kind: 1 },
      { label: "const", kind: 1 },
    ];
  }

  diagnostics(uri: string): Diagnostic[] {
    // Return fixed set of diagnostics for testing
    return [
      {
        range: { start: { line: 0, character: 0 }, end: { line: 0, character: 8 } },
        message: "Unused variable 'greeting'",
        severity: 2, // warning
      },
    ];
  }
}
