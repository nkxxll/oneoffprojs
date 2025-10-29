import { loadFixture, compareFixture, saveFixture } from "./fixtures.ts";
import type {
  ProcessedConfig,
  Args,
  ProcessedTest,
  TestResult,
  TestRunResult,
} from "./types";

export async function runTests(
  config: ProcessedConfig,
  args: Args,
): Promise<TestRunResult[]> {
  const results: TestRunResult[] = [];

  for (const testRun of config.testRuns) {
    if (!testRun) continue;
    if (args.verbose) console.log(`Running test run: ${testRun.name}`);

    const runResults: TestResult[] = await runTestRun(
      config.cmd,
      config.args,
      testRun.tests,
      testRun.name,
      args,
    );
    results.push({ name: testRun.name, tests: runResults });
  }

  return results;
}

async function runTestRun(
  cmd: string,
  args: string | undefined,
  tests: ProcessedTest[],
  runName: string,
  options: Args,
): Promise<TestResult[]> {
  if (!cmd) throw new Error("Command is required");
  const testArgs = args?.split(" ") || [];
  const process = Bun.spawn([cmd, ...testArgs], {
    stdin: "pipe",
    stdout: "pipe",
    stderr: "inherit",
  });
  const responsesMap = new Map<number, any>();

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
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trim = line.trim();
      if (trim) {
        try {
          const response = JSON.parse(trim);
          if (response.id !== undefined) {
            responsesMap.set(response.id, response);
          }
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
    const test = tests[i];
    if (!test) continue;
    const fixture = await loadFixture(runName, i);
    const response = test.message.id !== undefined ? responsesMap.get(test.message.id) || null : null;
    const matched =
      fixture && response ? compareFixture(response, fixture) : false;

    // Save fixture if we have a response but no fixture
    if (response && !fixture) {
      await saveFixture(runName, i, response);
    }

    runResults.push({
      type: test.type,
      params: test.params,
      tool: test.tool,
      args: test.args,
      message: test.message,
      response,
      fixture,
      matched,
    });
  }
  return runResults;
}
