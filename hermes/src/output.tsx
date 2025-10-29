import { useRef, useState } from "react";
import type { TestRunResult } from "./types";
import { render, useKeyboard } from "@opentui/react";
import { saveFixture } from "./fixtures";
import { getConstantValue } from "typescript";

interface TestResultsDisplayProps {
  results: TestRunResult[];
}

export function TestResultsDisplay({ results }: TestResultsDisplayProps) {
  const scroll = useRef(undefined);
  const initialRunStates = results.length > 0 ? { 0: true } : {};
  const [runStates, setRunStates] =
    useState<Record<number, boolean>>(initialRunStates);
  const [testStates, setTestStates] = useState<Record<string, boolean>>({});
  const [selected, setSelected] = useState({ runIndex: 0, testIndex: 0 });
  useKeyboard(async (key) => {
    if (key.name === "j" && key.shift) {
      // jump to next run
      let { runIndex } = selected;
      if (runIndex < results.length - 1) {
        runIndex++;
      }
      setSelected({ runIndex, testIndex: 0 });
      setRunStates((prev) => ({ ...prev, [runIndex]: true }));
    } else if (key.name === "k" && key.shift) {
      // jump to previous run
      let { runIndex } = selected;
      if (runIndex > 0) {
        runIndex--;
      }
      setSelected({ runIndex, testIndex: 0 });
      setRunStates((prev) => ({ ...prev, [runIndex]: true }));
    } else if (key.name === "j") {
      // move down
      let { runIndex, testIndex } = selected;
      const currentRun = results[runIndex];
      if (testIndex < currentRun.tests.length - 1) {
        testIndex++;
      } else if (runIndex < results.length - 1) {
        runIndex++;
        testIndex = 0;
      }
      setSelected({ runIndex, testIndex });
      setRunStates((prev) => ({ ...prev, [runIndex]: true }));
    } else if (key.name === "k") {
      // move up
      let { runIndex, testIndex } = selected;
      if (testIndex > 0) {
        testIndex--;
      } else if (runIndex > 0) {
        runIndex--;
        testIndex = results[runIndex].tests.length - 1;
      }
      setSelected({ runIndex, testIndex });
      setRunStates((prev) => ({ ...prev, [runIndex]: true }));
    } else if (key.name === "l") {
      const keyStr = `${selected.runIndex}-${selected.testIndex}`;
      setTestStates((prev) => ({ ...prev, [keyStr]: !prev[keyStr] }));
    } else if (key.name === "s") {
      const currentRun = results[selected.runIndex];
      const currentTest = currentRun.tests[selected.testIndex];
      await saveFixture(
        currentRun.name,
        selected.testIndex,
        currentTest.response,
      );
    } else if (key.name === "q") {
      process.exit(0);
    }
  });

  let totalTests = 0;
  let passedTests = 0;

  // aua
  for (const run of results) {
    if (!run) continue;
    for (const test of run.tests) {
      if (!test) continue;
      totalTests++;
      if (test.type === "notifications/initialized") {
        if (!test.response) passedTests++;
      } else if (test.response) {
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
                  if (test.type === "notifications/initialized") {
                    if (!test.response) {
                      status = "PASS (notification)";
                    }
                  } else if (test.response) {
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
                  const isSelected =
                    runIndex === selected.runIndex &&
                    testIndex === selected.testIndex;
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
                        {isSelected ? ">" : " "} {summary} -{" "}
                        {isTestOpen ? "Expanded" : "Collapsed"}
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
                            <text>
                              {test.type === "notifications/initialized"
                                ? "No response (expected for notification)"
                                : "No response received"}
                            </text>
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
