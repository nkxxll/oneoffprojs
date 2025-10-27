interface Test {
    type: string;
    testIndex: number;
    message: object;
    response: object;
    fixture: object;
}

interface Item {
    runName: string;
    test: Test;
    content: string;
    folded: boolean;
    foldedContent: string;
}
