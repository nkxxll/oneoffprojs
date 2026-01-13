import { StreamMetrics } from "./stream-wrapper.js";

export interface TrafficMetrics {
  totalBytesIn: number;
  totalBytesOut: number;
  messagesIn: number;
  messagesOut: number;
  byMessageType: Map<string, { bytes: number; count: number }>;
  headerBytes: number;
  bodyBytes: number;
  overheadRatio: number;
}

export interface TrafficSummary {
  direction: "in" | "out";
  totalBytes: number;
  messageCount: number;
  avgBytesPerMessage: number;
}

export class TrafficAnalyzer {
  private inMetrics: StreamMetrics | null = null;
  private outMetrics: StreamMetrics | null = null;
  private messageTypeStats: Map<string, { bytesIn: number; bytesOut: number; count: number }> = new Map();

  setInMetrics(metrics: StreamMetrics): void {
    this.inMetrics = metrics;
  }

  setOutMetrics(metrics: StreamMetrics): void {
    this.outMetrics = metrics;
  }

  recordMessageType(type: string, bytesIn: number, bytesOut: number): void {
    const existing = this.messageTypeStats.get(type) || { bytesIn: 0, bytesOut: 0, count: 0 };
    existing.bytesIn += bytesIn;
    existing.bytesOut += bytesOut;
    existing.count++;
    this.messageTypeStats.set(type, existing);
  }

  estimateHeaderOverhead(messageCount: number): number {
    // LSP headers are typically: "Content-Length: XXX\r\n\r\n"
    // Average header is ~25 bytes per message
    return messageCount * 25;
  }

  getTrafficMetrics(): TrafficMetrics {
    const totalBytesIn = this.inMetrics?.totalBytes || 0;
    const totalBytesOut = this.outMetrics?.totalBytes || 0;
    const messagesIn = this.inMetrics?.messageCount || 0;
    const messagesOut = this.outMetrics?.messageCount || 0;

    const headerBytes = this.estimateHeaderOverhead(messagesIn + messagesOut);
    const bodyBytes = totalBytesIn + totalBytesOut - headerBytes;

    return {
      totalBytesIn,
      totalBytesOut,
      messagesIn,
      messagesOut,
      byMessageType: new Map(
        Array.from(this.messageTypeStats.entries()).map(([k, v]) => [
          k,
          { bytes: v.bytesIn + v.bytesOut, count: v.count },
        ])
      ),
      headerBytes: Math.max(0, headerBytes),
      bodyBytes: Math.max(0, bodyBytes),
      overheadRatio: bodyBytes > 0 ? headerBytes / bodyBytes : 0,
    };
  }

  getSummary(): string {
    const metrics = this.getTrafficMetrics();
    const lines: string[] = [
      "=== TRAFFIC ANALYSIS ===",
      `Total bytes received: ${metrics.totalBytesIn.toLocaleString()} bytes`,
      `Total bytes sent: ${metrics.totalBytesOut.toLocaleString()} bytes`,
      `Total overhead (headers): ~${metrics.headerBytes.toLocaleString()} bytes`,
      `Messages exchanged: ${metrics.messagesIn + metrics.messagesOut}`,
      "",
      "Per-operation breakdown:",
    ];

    for (const [type, stats] of this.messageTypeStats.entries()) {
      lines.push(`  ${type}: ${stats.bytesIn}↓ ${stats.bytesOut}↑ (${stats.count} messages)`);
    }

    lines.push("");
    lines.push(`Overhead ratio: ${(metrics.overheadRatio * 100).toFixed(1)}% (header bytes / body bytes)`);

    return lines.join("\n");
  }

  getInSummary(): TrafficSummary | null {
    if (!this.inMetrics) return null;
    return {
      direction: "in",
      totalBytes: this.inMetrics.totalBytes,
      messageCount: this.inMetrics.messageCount,
      avgBytesPerMessage:
        this.inMetrics.messageCount > 0
          ? this.inMetrics.totalBytes / this.inMetrics.messageCount
          : 0,
    };
  }

  getOutSummary(): TrafficSummary | null {
    if (!this.outMetrics) return null;
    return {
      direction: "out",
      totalBytes: this.outMetrics.totalBytes,
      messageCount: this.outMetrics.messageCount,
      avgBytesPerMessage:
        this.outMetrics.messageCount > 0
          ? this.outMetrics.totalBytes / this.outMetrics.messageCount
          : 0,
    };
  }
}
