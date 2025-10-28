import { useState } from "react";
import type { TestRunResult } from "./types";
import { render } from "@opentui/react";

interface TestResultsDisplayProps {
  results: TestRunResult[];
}

export function TestResultsDisplay({ results }: TestResultsDisplayProps) {
  const [runStates, setRunStates] = useState<Record<number, boolean>>({});
  const [testStates, setTestStates] = useState<Record<string, boolean>>({});

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
      {results.map((run, runIndex) => {
        const isRunOpen = runStates[runIndex] ?? false;
        return (
          <box
            border
            key={runIndex}
            title={`Test Run: ${run.name} - ${isRunOpen ? "Expanded" : "Collapsed"}`}
          >
            <text
              onMouseDown={() =>
                setRunStates((prev) => ({
                  ...prev,
                  [runIndex]: !prev[runIndex],
                }))
              }
            >
              {isRunOpen ? "v" : ">"} Test Run: {run.name}
            </text>
            {isRunOpen && (
              <box border padding={1}>
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
                  const key = `${runIndex}-${testIndex}`;
                  const isTestOpen = testStates[key] ?? false;
                  return (
                    <box
                      key={testIndex}
                      onMouseDown={() =>
                        setTestStates((prev) => ({
                          ...prev,
                          [key]: !prev[key],
                        }))
                      }
                    >
                      <text>
                        {summary} - {isTestOpen ? "Expanded" : "Collapsed"}
                      </text>
                      {isTestOpen && (
                        <box border padding={1}>
                          <text>
                            <b>Request:</b>
                          </text>
                          <text>{JSON.stringify(test.message, null, 2)}</text>
                          <text>
                            <b>Response</b>:
                          </text>
                          {test.response ? (
                            <text>
                              {JSON.stringify(test.response, null, 2)}
                            </text>
                          ) : (
                            <text>No response received</text>
                          )}
                          {test.fixture && !test.matched && (
                            <>
                              <text>
                                <b>Expected</b>:
                              </text>
                              <text>
                                {JSON.stringify(test.fixture, null, 2)}
                              </text>
                            </>
                          )}
                        </box>
                      )}
                    </box>
                  );
                })}
              </box>
            )}
          </box>
        );
      })}
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
