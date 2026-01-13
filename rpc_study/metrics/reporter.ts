import * as fs from "fs";
import { MetricPoint } from "./tracker.js";

export class MetricsReporter {
  constructor(private outputFile?: string) {}

  toCSV(data: MetricPoint[]): string {
    const header =
      "timestamp,operation,bytes_sent,bytes_received,latency_ms\n";
    const rows = data
      .map(
        (m) =>
          `${m.timestamp},${m.operation},${m.bytesSent},${m.bytesReceived},${m.latencyMs}`
      )
      .join("\n");
    return header + rows;
  }

  toJSON(data: MetricPoint[]): string {
    return JSON.stringify(data, null, 2);
  }

  writeSummary(
    stats: Record<string, any>,
    data: MetricPoint[],
    format: "csv" | "json" = "csv"
  ) {
    let content = "";

    // Summary section
    content += "=== METRICS SUMMARY ===\n";
    for (const [op, stat] of Object.entries(stats)) {
      if (stat) {
        content += `\n${op}:\n`;
        content += `  Count: ${stat.count}\n`;
        content += `  Latency: min=${stat.latency.min.toFixed(2)}ms, max=${stat.latency.max.toFixed(2)}ms, avg=${stat.latency.avg.toFixed(2)}ms\n`;
        content += `  Bytes Sent: ${stat.bytesSent.total}\n`;
        content += `  Bytes Received: ${stat.bytesReceived.total}\n`;
      }
    }

    content += "\n=== DETAILED DATA ===\n";
    content +=
      format === "csv"
        ? this.toCSV(data)
        : this.toJSON(data).substring(0, 500) + "...";

    if (this.outputFile) {
      fs.writeFileSync(this.outputFile, content);
    } else {
      console.log(content);
    }
  }
}
