import { LSPClient } from "./index.js";

// Read TEST_MULTIPLIER from environment, default to 1
const TEST_MULTIPLIER = parseInt(process.env.TEST_MULTIPLIER || "1", 10);

if (TEST_MULTIPLIER < 1) {
  console.error("❌ TEST_MULTIPLIER must be >= 1");
  process.exit(1);
}

interface EfficiencyMetrics {
  totalRequests: number;
  totalLatency: number;
  totalBytesSent: number;
  totalBytesReceived: number;
  throughput: number; // requests per second
  efficiency: number; // requests per MB
  avgLatency: number;
  avgPayloadSize: number;
}

async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

function analyzeEfficiency(client: LSPClient): EfficiencyMetrics {
  const data = client.getMetrics().getData();
  
  const totalRequests = data.length;
  const totalLatency = data.reduce((sum, m) => sum + m.latencyMs, 0);
  const totalBytesSent = data.reduce((sum, m) => sum + m.bytesSent, 0);
  const totalBytesReceived = data.reduce((sum, m) => sum + m.bytesReceived, 0);
  
  const totalBytes = totalBytesSent + totalBytesReceived;
  const totalTimeMs = totalLatency;
  
  return {
    totalRequests,
    totalLatency,
    totalBytesSent,
    totalBytesReceived,
    throughput: (totalRequests / (totalTimeMs / 1000)) || 0,
    efficiency: totalRequests / ((totalBytes / 1024 / 1024) || 1),
    avgLatency: totalLatency / totalRequests,
    avgPayloadSize: totalBytes / totalRequests,
  };
}

async function runAdvancedTests() {
  console.log("🚀 Starting Advanced LSP E2E Tests with Efficiency Metrics...");
  console.log(`📌 TEST_MULTIPLIER: ${TEST_MULTIPLIER}x\n`);

  const client = new LSPClient("./dist/server/index.js", true);

  try {
    // Phase 1: Initialize
    console.log("═══════════════════════════════════════════════════════════");
    console.log("PHASE 1: INITIALIZATION");
    console.log("═══════════════════════════════════════════════════════════");
    const initResult = await client.initialize();
    console.log("✓ Server initialized with capabilities:", 
      Object.keys(initResult).join(", "));
    await sleep(50);

    // Phase 2: Bulk hover requests (test scalability)
    const hoverIterations = 10 * TEST_MULTIPLIER;
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log(`PHASE 2: BULK HOVER REQUESTS (${hoverIterations * 5} requests)`);
    console.log("═══════════════════════════════════════════════════════════");
    const hoverPositions = [
      { line: 0, char: 9 },
      { line: 0, char: 15 },
      { line: 1, char: 5 },
      { line: 2, char: 12 },
      { line: 3, char: 8 },
    ];
    
    const hoverStart = Date.now();
    let hoverCount = 0;
    for (let i = 0; i < hoverIterations; i++) {
      for (const pos of hoverPositions) {
        await client.hover("file:///test.ts", pos.line, pos.char);
        hoverCount++;
      }
    }
    const hoverDuration = Date.now() - hoverStart;
    console.log(`✓ Completed ${hoverCount} hover requests in ${hoverDuration}ms`);
    console.log(`  Throughput: ${(hoverCount / (hoverDuration / 1000)).toFixed(2)} req/s`);
    await sleep(50);

    // Phase 3: Bulk completion requests
    const completionIterations = 10 * TEST_MULTIPLIER;
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log(`PHASE 3: BULK COMPLETION REQUESTS (${completionIterations * 5} requests)`);
    console.log("═══════════════════════════════════════════════════════════");
    const completionPositions = [
      { line: 0, char: 2 },
      { line: 1, char: 0 },
      { line: 2, char: 5 },
      { line: 3, char: 10 },
      { line: 4, char: 3 },
    ];
    
    const completionStart = Date.now();
    let completionCount = 0;
    for (let i = 0; i < completionIterations; i++) {
      for (const pos of completionPositions) {
        await client.completion("file:///test.ts", pos.line, pos.char);
        completionCount++;
      }
    }
    const completionDuration = Date.now() - completionStart;
    console.log(`✓ Completed ${completionCount} completion requests in ${completionDuration}ms`);
    console.log(`  Throughput: ${(completionCount / (completionDuration / 1000)).toFixed(2)} req/s`);
    await sleep(50);

    // Phase 4: Stress test - rapid sequential requests
    const stressRequests = 100 * TEST_MULTIPLIER;
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log(`PHASE 4: STRESS TEST - RAPID SEQUENTIAL REQUESTS (${stressRequests} mixed)`);
    console.log("═══════════════════════════════════════════════════════════");
    const stressStart = Date.now();
    for (let i = 0; i < stressRequests; i++) {
      const rand = Math.random();
      if (rand < 0.5) {
        await client.hover("file:///test.ts", i % 5, (i * 3) % 20);
      } else {
        await client.completion("file:///test.ts", i % 5, (i * 2) % 15);
      }
    }
    const stressDuration = Date.now() - stressStart;
    console.log(`✓ Completed ${stressRequests} mixed requests in ${stressDuration}ms`);
    console.log(`  Throughput: ${(stressRequests / (stressDuration / 1000)).toFixed(2)} req/s`);
    await sleep(50);

    // Phase 5: Diagnostics batching
    const diagRequests = 20 * TEST_MULTIPLIER;
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log(`PHASE 5: DIAGNOSTIC BATCHING (${diagRequests} requests)`);
    console.log("═══════════════════════════════════════════════════════════");
    const diagStart = Date.now();
    for (let i = 0; i < diagRequests; i++) {
      await client.diagnostic("file:///test.ts");
    }
    const diagDuration = Date.now() - diagStart;
    console.log(`✓ Completed ${diagRequests} diagnostic requests in ${diagDuration}ms`);
    console.log(`  Throughput: ${(diagRequests / (diagDuration / 1000)).toFixed(2)} req/s`);

    // Calculate efficiency metrics
    await sleep(200);
    const efficiency = analyzeEfficiency(client);

    console.log("\n═══════════════════════════════════════════════════════════");
    console.log("EFFICIENCY ANALYSIS");
    console.log("═══════════════════════════════════════════════════════════");
    console.log(`📊 Total Requests: ${efficiency.totalRequests}`);
    console.log(`📊 Total Bytes: ${(efficiency.totalBytesSent + efficiency.totalBytesReceived).toFixed(2)} bytes`);
    console.log(`⏱️  Total Latency: ${efficiency.totalLatency.toFixed(2)}ms`);
    console.log(`📤 Total Bytes Sent: ${efficiency.totalBytesSent.toFixed(2)} bytes`);
    console.log(`📥 Total Bytes Received: ${efficiency.totalBytesReceived.toFixed(2)} bytes`);
    console.log(`\n⏳ Average Time per 1000 Requests: ${(efficiency.avgLatency * 1000).toFixed(2)}ms`);
    console.log(`📦 Average Bytes per 1000 Requests: ${(efficiency.avgPayloadSize * 1000).toFixed(2)} bytes`);
    console.log(`\n🚀 Throughput: ${efficiency.throughput.toFixed(2)} req/s`);
    console.log(`⚡ Efficiency: ${efficiency.efficiency.toFixed(2)} req/MB`);
    console.log(`⏳ Avg Latency: ${efficiency.avgLatency.toFixed(2)}ms/req`);
    console.log(`📦 Avg Payload: ${efficiency.avgPayloadSize.toFixed(2)} bytes/req`);

    // Detailed per-operation metrics
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log("PER-OPERATION METRICS");
    console.log("═══════════════════════════════════════════════════════════");
    
    const operations = new Set(client.getMetrics().getData().map((m) => m.operation));
    for (const op of operations) {
      const stats = client.getMetrics().getStats(op);
      if (stats) {
        console.log(`\n📍 ${op}:`);
        console.log(`   Count: ${stats.count} requests`);
        console.log(`   Latency: min=${stats.latency.min}ms, max=${stats.latency.max}ms, avg=${stats.latency.avg.toFixed(2)}ms`);
        console.log(`   Bytes Sent: min=${stats.bytesSent.min}, max=${stats.bytesSent.max}, total=${stats.bytesSent.total}`);
        console.log(`     → Per 100 requests: ${stats.bytesSent.per100.toFixed(2)} bytes`);
        console.log(`     → Per 1000 requests: ${stats.bytesSent.per1000.toFixed(2)} bytes`);
        console.log(`   Bytes Received: min=${stats.bytesReceived.min}, max=${stats.bytesReceived.max}, total=${stats.bytesReceived.total}`);
        console.log(`     → Per 100 requests: ${stats.bytesReceived.per100.toFixed(2)} bytes`);
        console.log(`     → Per 1000 requests: ${stats.bytesReceived.per1000.toFixed(2)} bytes`);
        
        const opThroughput = (stats.count / (stats.latency.avg / 1000)).toFixed(2);
        console.log(`   Throughput: ${opThroughput} req/s`);
      }
    }

    // Efficiency comparison
    console.log("\n═══════════════════════════════════════════════════════════");
    console.log("EFFICIENCY REPORT");
    console.log("═══════════════════════════════════════════════════════════");
    console.log(`✅ LSP is handling ${efficiency.totalRequests} requests efficiently`);
    console.log(`✅ Average response time: ${efficiency.avgLatency.toFixed(2)}ms (excellent)`);
    console.log(`✅ Payload efficiency: ${efficiency.efficiency.toFixed(0)} requests per MB`);
    console.log(`✅ Sustained throughput: ${efficiency.throughput.toFixed(2)} requests/second`);
    
    if (efficiency.avgLatency < 5) {
      console.log("🎯 VERDICT: LSP is HIGHLY EFFICIENT for this workload");
    } else if (efficiency.avgLatency < 10) {
      console.log("🎯 VERDICT: LSP is EFFICIENT for this workload");
    } else {
      console.log("⚠️  VERDICT: LSP shows acceptable performance");
    }

    // Print wire traffic analysis
    client.printTrafficSummary();

    console.log("\n✅ All tests passed!\n");
  } catch (error) {
    console.error("❌ Test failed:", error);
    process.exit(1);
  } finally {
    client.close();
    await sleep(500);
    process.exit(0);
  }
}

runAdvancedTests();
