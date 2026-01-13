// Common LSP types and utilities
export interface Position {
  line: number;
  character: number;
}

export interface Range {
  start: Position;
  end: Position;
}

export interface Location {
  uri: string;
  range: Range;
}

export interface Hover {
  contents: string;
}

export interface CompletionItem {
  label: string;
  kind: number;
  detail?: string;
}

export interface Diagnostic {
  range: Range;
  message: string;
  severity: number; // 1=error, 2=warning, 3=info, 4=hint
}
