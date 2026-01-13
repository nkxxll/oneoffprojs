# LSP Integration & Traffic Measurement Plan

## Current State
✅ Project already uses `vscode-languageserver` and `vscode-languageclient`
✅ Basic LSP protocol implemented with stdin/stdout communication
✅ Metrics tracking infrastructure exists (MetricsTracker)
⚠️ Traffic measurement is approximate (JSON stringification estimates)

---

## Architecture Overview

### Server Side (`server/index.ts`)
**Current Implementation:**
- Uses `vscode-languageserver` to create connection via stdin/stdout
- `StreamMessageReader` reads from `process.stdin`
- `StreamMessageWriter` writes to `process.stdout`
- Handlers registered for LSP events (initialize, hover, completion, etc.)
- Records metrics post-operation (latency calculated locally)

**Issues:**
1. Byte counting is estimated via `JSON.stringify(data).length`
2. Doesn't capture actual wire protocol bytes (LSP uses JSON-RPC with headers/delimiters)
3. Estimates don't include JSON-RPC envelope, Content-Length header, CRLF delimiters

### Client Side (`client/index.ts`)
**Current Implementation:**
- Uses `vscode-languageclient` to spawn server process
- Creates LanguageClient with ServerOptions pointing to spawned process
- Sends requests and tracks metrics

**Issues:**
- Manual byte estimation for JSON-RPC messages
- Doesn't hook into actual network I/O
- No way to measure actual wire protocol overhead

---

## Proposed Enhancement Plan

### Phase 1: Accurate Byte Counting (HIGH PRIORITY)

#### 1a. Intercept Streams at Protocol Level

**Server-side stream interception:**
```typescript
// server/index.ts - Add stream wrapping BEFORE creating connection
const readStream = wrapStreamWithMetrics(process.stdin, 'read');
const writeStream = wrapStreamWithMetrics(process.stdout, 'write');

const connection = rpc.createConnection(
  new StreamMessageReader(readStream),
  new StreamMessageWriter(writeStream)
);
```

**Create `metrics/stream-wrapper.ts`:**
- Wrap readable/writable streams
- Hook into 'data' events to count actual bytes
- Differentiate between request direction (client→server vs server→client)
- Accumulate byte counts with optional per-message breakdown

#### 1b. Client-side Stream Interception

**Problem:** `vscode-languageclient` uses internal pipes to communicate with spawned process.

**Solution:** Hook into child process stdio streams:
```typescript
// client/index.ts modification
const child = spawn('node', [serverPath]);
const readStream = wrapStreamWithMetrics(child.stdout, 'server-response');
const writeStream = wrapStreamWithMetrics(child.stdin, 'client-request');
```

Then pass these wrapped streams to client via `StreamInfo`:
```typescript
serverOptions: {
  run: { transport: TransportKind.Pipe, ... },
  // OR use raw node.js child process with stream wrapping
}
```

---

### Phase 2: Wire Protocol Measurement

#### 2a. LSP Message Structure
LSP (JSON-RPC 2.0 over headers) format:
```
Content-Length: 123\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}
```

**Bytes to count:**
- Header: `Content-Length: XXX\r\n\r\n` (~20-30 bytes per message)
- Body: JSON-RPC message

#### 2b. Enhanced Metrics Collection

**Create `metrics/traffic-analyzer.ts`:**
```typescript
interface TrafficMetrics {
  totalBytesIn: number;
  totalBytesOut: number;
  messagesIn: number;
  messagesOut: number;
  byMessageType: Map<string, { bytes: number; count: number }>;
  overheadRatio: number; // (header bytes / body bytes)
}
```

---

### Phase 3: Integration Strategy

#### Server Implementation
1. ✅ Keep existing handler structure in `handlers.ts`
2. ✅ Keep connection setup in `server/index.ts`
3. ✨ **NEW:** Wrap streams before creating connection
4. ✨ **NEW:** Track incoming/outgoing bytes in wrapper
5. ✅ Keep existing per-request metrics recording
6. ✨ **NEW:** On exit, output total traffic summary

#### Client Implementation
1. ✅ Keep existing `LSPClient` class structure
2. ✨ **NEW:** Option to track actual stream bytes (separate from request-level metrics)
3. ✨ **NEW:** Compare JSON-stringify estimates vs actual wire bytes
4. ✅ Keep per-operation metrics
5. ✨ **NEW:** Report overhead analysis

---

## Implementation Checklist

### New Files to Create
- [ ] `metrics/stream-wrapper.ts` - Stream interception utility
- [ ] `metrics/traffic-analyzer.ts` - Wire protocol analysis
- [ ] `types/stream-metrics.ts` - Type definitions for stream metrics

### Files to Modify
- [ ] `server/index.ts` - Integrate stream wrapper
- [ ] `client/index.ts` - Hook into child process streams
- [ ] `metrics/tracker.ts` - Add traffic-level tracking
- [ ] Package.json - (no new deps needed)

### Testing Strategy
- [ ] Verify stream wrapper doesn't break protocol
- [ ] Compare wire bytes vs JSON estimates
- [ ] Test with various message sizes
- [ ] Output sample measurement report

---

## Key Design Decisions

### Why Stream Wrapping?
- **Pro:** Capture actual wire protocol bytes
- **Pro:** Works without modifying vscode-languageserver/client internals
- **Pro:** Easy to enable/disable with env vars
- **Con:** Requires understanding stream interfaces

### Why Separate Traffic vs Request Metrics?
- **Separation of concerns:** Request metrics = business logic timing
- **Traffic metrics** = protocol overhead analysis
- Allows comparing estimated vs actual bytes

### Measurement Points
1. **Per-message:** Bytes in/out per LSP message
2. **Per-operation:** Aggregated across all messages in single operation
3. **Total session:** Cumulative traffic across all operations

---

## Expected Output Example

```
=== TRAFFIC ANALYSIS ===
Total bytes received: 2,456 bytes
Total bytes sent: 1,892 bytes
Total overhead (headers): ~245 bytes
Messages exchanged: 24

Per-operation breakdown:
  initialize: 456↓ 234↑
  textDocument/hover: 89↓ 142↑ (3 messages)
  textDocument/completion: 156↓ 298↑ (2 messages)
  textDocument/diagnostic: 234↓ 456↑ (1 message)

Overhead ratio: 12% (header bytes / total bytes)
```

---

## Next Steps
1. Create stream wrapper utility
2. Integrate into server
3. Integrate into client
4. Test and validate
5. Compare estimates vs actual
6. Generate traffic report
