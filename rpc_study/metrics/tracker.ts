export interface MetricPoint {
  timestamp: number;
  operation: string;
  bytesSent: number;
  bytesReceived: number;
  latencyMs: number;
}

export class MetricsTracker {
  private data: MetricPoint[] = [];

  record(metric: MetricPoint) {
    this.data.push(metric);
  }

  getData(): MetricPoint[] {
    return this.data;
  }

  getStats(operation?: string) {
    const filtered = operation
      ? this.data.filter((m) => m.operation === operation)
      : this.data;

    if (filtered.length === 0) return null;

    const latencies = filtered.map((m) => m.latencyMs);
    const bytesSents = filtered.map((m) => m.bytesSent);
    const bytesRecvs = filtered.map((m) => m.bytesReceived);

    const totalBytesSent = bytesSents.reduce((a, b) => a + b, 0);
    const totalBytesRecv = bytesRecvs.reduce((a, b) => a + b, 0);
    const count = filtered.length;

    return {
      count,
      latency: {
        min: Math.min(...latencies),
        max: Math.max(...latencies),
        avg: latencies.reduce((a, b) => a + b, 0) / latencies.length,
      },
      bytesSent: {
        min: Math.min(...bytesSents),
        max: Math.max(...bytesSents),
        total: totalBytesSent,
        per100: (totalBytesSent / count) * 100,
        per1000: (totalBytesSent / count) * 1000,
      },
      bytesReceived: {
        min: Math.min(...bytesRecvs),
        max: Math.max(...bytesRecvs),
        total: totalBytesRecv,
        per100: (totalBytesRecv / count) * 100,
        per1000: (totalBytesRecv / count) * 1000,
      },
    };
  }
}
