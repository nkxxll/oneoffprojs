import { Readable, Writable, Transform } from "stream";

export interface StreamMetrics {
  totalBytes: number;
  messageCount: number;
  bytesByMessage: number[];
}

export class MetricsReadableWrapper extends Transform {
  public metrics: StreamMetrics = {
    totalBytes: 0,
    messageCount: 0,
    bytesByMessage: [],
  };

  constructor(private label: string = "read") {
    super();
  }

  _transform(
    chunk: Buffer,
    encoding: BufferEncoding,
    callback: (error?: Error | null, data?: Buffer) => void
  ): void {
    const bytes = chunk.length;
    this.metrics.totalBytes += bytes;
    this.metrics.messageCount++;
    this.metrics.bytesByMessage.push(bytes);
    callback(null, chunk);
  }

  getMetrics(): StreamMetrics {
    return { ...this.metrics };
  }
}

export class MetricsWritableWrapper extends Transform {
  public metrics: StreamMetrics = {
    totalBytes: 0,
    messageCount: 0,
    bytesByMessage: [],
  };

  constructor(private label: string = "write") {
    super();
  }

  _transform(
    chunk: Buffer,
    encoding: BufferEncoding,
    callback: (error?: Error | null, data?: Buffer) => void
  ): void {
    const bytes = chunk.length;
    this.metrics.totalBytes += bytes;
    this.metrics.messageCount++;
    this.metrics.bytesByMessage.push(bytes);
    callback(null, chunk);
  }

  getMetrics(): StreamMetrics {
    return { ...this.metrics };
  }
}

export function wrapReadStream(
  stream: NodeJS.ReadableStream,
  label: string = "read"
): { wrapped: MetricsReadableWrapper; original: NodeJS.ReadableStream } {
  const wrapper = new MetricsReadableWrapper(label);
  (stream as Readable).pipe(wrapper);
  return { wrapped: wrapper, original: stream };
}

export function wrapWriteStream(
  stream: NodeJS.WritableStream,
  label: string = "write"
): { wrapped: MetricsWritableWrapper; original: NodeJS.WritableStream } {
  const wrapper = new MetricsWritableWrapper(label);
  wrapper.pipe(stream as Writable);
  return { wrapped: wrapper, original: stream };
}
