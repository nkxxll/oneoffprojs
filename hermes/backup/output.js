import { run, update, view, init } from "../backup/tui/index.jsex.js";

export async function displayResults(results) {
  let totalTests = 0;
  let passedTests = 0;

  const initialItems = [];

  for (let runIndex = 0; runIndex < results.length; runIndex++) {
    const run = results[runIndex];
    for (let testIndex = 0; testIndex < run.tests.length; testIndex++) {
      const test = run.tests[testIndex];
      totalTests++;
      let status = "FAIL";
      if (test.response) {
        if (test.fixture) {
          status = test.matched ? "PASS (fixture)" : "FAIL (fixture mismatch)";
        } else {
          status = "PASS (new)";
        }
        if (test.matched || !test.fixture) passedTests++;
      }

      const foldedContent = `Test Run: ${run.name} - ${status}: ${test.type}`;

      let content = `Test Run: ${run.name}\n${status}: ${test.type}\n`;
      content += `Request: ${JSON.stringify(test.message, null, 2)}\n`;
      if (test.response) {
        content += `Response: ${JSON.stringify(test.response, null, 2)}\n`;
        if (test.fixture && !test.matched) {
          content += `Expected: ${JSON.stringify(test.fixture, null, 2)}\n`;
        }
      } else {
        content += "Response: No response received\n";
      }

      initialItems.push({
        runName: run.name,
        testIndex,
        test,
        content,
        foldedContent,
      });
    }
  }

  const [initialModel] = init(initialItems);
  run(initialModel, update, view);
  // everything here will not happen
}
