export interface KairosConfig {
  host: string;
  user: string;
  keyPath: string;
  // Add other config fields as needed
}

export type TimewCommand =
  | { type: "start"; args: { tag: string; startTime?: string } }
  | { type: "stop"; args?: { stopTime: string } }
  | { type: "summary" }
  | { type: "track"; args: { start: string; end: string; tag: string } }
  | { type: "inspect" }
  | {
  type: "modify";
  args: { id: string; tag?: string; start?: string; end?: string };
  };

export interface CommandResult {
  success: boolean;
  output: string;
}
