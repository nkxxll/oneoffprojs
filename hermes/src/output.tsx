import { render } from "@opentui/react";
import type { TestRunResult } from "./types";

interface TestResultsDisplayProps {
  results: TestRunResult[];
}

export function TestResultsDisplay({ results }: TestResultsDisplayProps) {
  let totalTests = 0;
  let passedTests = 0;

  // aua
  for (const run of results) {
    if (!run) continue;
    for (const test of run.tests) {
      if (!test) continue;
      totalTests++;
      if (test.response) {
        if (test.fixture) {
          if (test.matched) passedTests++;
        } else {
          passedTests++;
        }
      }
    }
  }

  return (
    <scrollbox>
      {results.map((run, runIndex) => (
        <box key={runIndex} title={`Test Run: ${run.name}`} border padding={1}>
          {run.tests.map((test, testIndex) => {
            if (!test) return null;
            let status = "FAIL";
            if (test.response) {
              if (test.fixture) {
                status = test.matched
                  ? "PASS (fixture)"
                  : "FAIL (fixture mismatch)";
              } else {
                status = "PASS (new)";
              }
            }
            const summary = `${status}: ${test.type}`;
            return (
              <box key={testIndex} title={summary} border padding={1}>
                <text>
                  <b>Request:</b>
                </text>
                <text>{JSON.stringify(test.message, null, 2)}</text>
                <text>
                  <b>Response</b>:
                </text>
                {test.response ? (
                  <text>{JSON.stringify(test.response, null, 2)}</text>
                ) : (
                  <text>No response received</text>
                )}
                {test.fixture && !test.matched && (
                  <>
                    <text>
                      <b>Expected</b>:
                    </text>
                    <text>{JSON.stringify(test.fixture, null, 2)}</text>
                  </>
                )}
              </box>
            );
          })}
        </box>
      ))}
      <box padding={1}>
        <text>
          <b>Summary</b>
        </text>
        <text>Total tests: {totalTests}</text>
        <text>Passed: {passedTests}</text>
        <text>Failed: {totalTests - passedTests}</text>
      </box>
    </scrollbox>
  );
}

export async function displayResults(results: TestRunResult[]) {
  await render(<TestResultsDisplay results={results} />);
}
