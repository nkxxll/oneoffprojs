interface Config {
    cmd: string;
    args?: string;
    test_runs: RawTestRun[];
}

interface RawTestRun {
    name?: string;
    tests: RawTest[];
}

interface RawTest {
    type: 'initialize' | 'notifications/initialized' | 'list/tools' | 'tools/call';
    params?: any;
    tool?: string;
    args?: any;
}

export interface ProcessedConfig {
    cmd: string;
    args: string | undefined;
    testRuns: ProcessedTestRun[];
}

interface ProcessedTestRun {
    name: string;
    tests: ProcessedTest[];
}

interface ProcessedTest {
    type: string;
    params?: any;
    tool?: string;
    args?: any;
    message: Message;
}

interface Message {
    jsonrpc: string;
    id?: number;
    method: string;
    params?: any;
}

interface TestResult extends ProcessedTest {
    response: any;
    fixture: any;
    matched: boolean;
}

interface TestRunResult {
    name: string;
    tests: TestResult[];
}

export interface Args {
    help: boolean;
    verbose: boolean;
    quiet: boolean;
}

interface Test {
    type: string;
    testIndex: number;
    message: object;
    response: object;
    fixture: object;
}

interface Item {
    runName: string;
    testIndex: number;
    test: Test;
    content: string;
    foldedContent: string;
}
