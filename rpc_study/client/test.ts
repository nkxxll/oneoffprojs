import { LSPClient } from "./index.js";

const serverPath = "./dist/server/index.js";

async function runTests() {
  console.log("🚀 Starting LSP E2E tests...\n");

  const client = new LSPClient(serverPath, true);

  try {
    await new Promise((r) => setTimeout(r, 100));

    // Test 1: Initialize
    console.log("\n📋 Test 1: Initialize");
    const initResult = await client.initialize();
    console.log("✓ Server initialized");

    await new Promise((r) => setTimeout(r, 100));

    // Test 2: Hover
    console.log("\n🖱️  Test 2: Hover request");
    const hoverResult = await client.hover("file:///test.ts", 0, 9);
    console.log("✓ Hover response:", hoverResult);

    await new Promise((r) => setTimeout(r, 100));

    // Test 3: Completion
    console.log("\n⚡ Test 3: Completion request");
    const completionResult = await client.completion("file:///test.ts", 2, 0);
    console.log("✓ Completion items:", completionResult?.length, "items");

    await new Promise((r) => setTimeout(r, 100));

    // Test 4: Diagnostics
    console.log("\n🔍 Test 4: Diagnostics request");
    const diagnosticsResult = await client.diagnostic("file:///test.ts");
    console.log("✓ Diagnostics:", diagnosticsResult?.length, "issues");

    // Print metrics
    await new Promise((r) => setTimeout(r, 200));
    console.log("\n📊 CLIENT METRICS:");
    const metrics = client.getMetrics().getData();
    for (const metric of metrics) {
      console.log(
        `  [${metric.operation}] ${metric.bytesSent} bytes sent | ${metric.bytesReceived} bytes received | ${metric.latencyMs}ms`
      );
    }

    // Summary stats
    const operations = new Set(metrics.map((m) => m.operation));
    console.log("\n📈 SUMMARY STATS:");
    for (const op of operations) {
      const stats = client.getMetrics().getStats(op);
      if (stats) {
        console.log(`  ${op}:`);
        console.log(
          `    Latency: min=${stats.latency.min}ms, max=${stats.latency.max}ms, avg=${stats.latency.avg.toFixed(2)}ms`
        );
        console.log(`    Bytes Sent: ${stats.bytesSent.total}`);
        console.log(`    Bytes Received: ${stats.bytesReceived.total}`);
      }
    }

    // Print wire traffic analysis
    client.printTrafficSummary();

    console.log("\n✅ All tests passed!\n");
  } catch (error) {
    console.error("❌ Test failed:", error);
    process.exit(1);
  } finally {
    client.close();
    await new Promise((r) => setTimeout(r, 500));
    process.exit(0);
  }
}

runTests();
