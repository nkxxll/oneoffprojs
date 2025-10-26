import { saveFixture } from './fixtures.js';
import { run, update, view, init } from './tui/index.js';

export async function displayResults(results, args) {
  let totalTests = 0;
  let passedTests = 0;

  const newFixtures = [];

  const initialItems = [];

  for (let runIndex = 0; runIndex < results.length; runIndex++) {
    const run = results[runIndex];
    for (let testIndex = 0; testIndex < run.tests.length; testIndex++) {
      const test = run.tests[testIndex];
      totalTests++;
      let status = 'FAIL';
      if (test.response) {
        if (test.fixture) {
          status = test.matched ? 'PASS (fixture)' : 'FAIL (fixture mismatch)';
        } else {
          status = 'PASS (new)';
          newFixtures.push({ runIndex, testIndex, runName: run.name, response: test.response });
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
        content += 'Response: No response received\n';
      }

      initialItems.push({
        id: `${runIndex}-${testIndex}`,
        content,
        foldedContent
      });
    }
  }

  const [initialModel] = init(initialItems);
  run(initialModel, update, view);

  // After TUI exits, handle fixtures
  for (const item of newFixtures) {
    await saveFixture(item.runName, item.testIndex, item.response);
  }

  console.log(`\nSummary: ${passedTests}/${totalTests} tests passed`);
}
