import { displayResults } from "./output.js";
import { loadFixture, compareFixture } from "./fixtures.js";

export async function runTests(config, args) {
  const results = [];

  for (let runIndex = 0; runIndex < config.testRuns.length; runIndex++) {
    const testRun = config.testRuns[runIndex];
    if (args.verbose) console.log(`Running test run: ${testRun.name}`);

    const runResults = await runTestRun(
      config.cmd,
      config.args,
      testRun.tests,
      testRun.name,
      args,
    );
    results.push({ name: testRun.name, tests: runResults });
  }

  await displayResults(results, args);
}

async function runTestRun(cmd, args, tests, runName, options) {
  const testArgs = args || [];
  const process = Bun.spawn([cmd, ...testArgs], {
    stdin: "pipe",
    stdout: "pipe",
    stderr: "inherit",
  });
  const responses = [];

  // Send messages
  for (const test of tests) {
    if (options.verbose)
      console.log(`Sending: ${JSON.stringify(test.message)}`);
    process.stdin.write(JSON.stringify(test.message) + "\n");
  }
  process.stdin.end();

  // Read stdout
  const reader = process.stdout.getReader();
  let buffer = "";
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      let trim = line.trim();
      if (trim) {
        try {
          const response = JSON.parse(trim);
          responses.push(response);
        } catch (e) {
          console.error(`Failed to parse response: ${line}`);
        }
      }
    }
  }

  // Wait for exit
  const exitCode = await process.exited;
  if (exitCode !== 0) {
    throw new Error(`Process exited with code ${exitCode}`);
  }

  // Process results
  const runResults = [];
  for (let i = 0; i < tests.length; i++) {
    const fixture = await loadFixture(runName, i);
    const response = responses[i] || null;
    const matched =
      fixture && response ? compareFixture(response, fixture) : false;
    runResults.push({
      ...tests[i],
      response,
      fixture,
      matched,
    });
  }
  return runResults;
}
