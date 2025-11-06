# Plan for Code Improvements

This plan outlines the steps to refactor and improve the ICS generation tool based on the initial code review.

## 1. Refactor `src/Tools.ts`

### Objective: Remove hardcoded paths and improve portability.

-   **Task 1.3: Remove Misleading Comment**
    -   Delete the comment `// yes this is just a wrapper that does nothing...` from the `createCalendar` function to accurately reflect its purpose.

## 2. Refactor `src/ICS.ts`

### Objective: Reduce code duplication by creating helper functions.

-   **Task 2.1: Create a Date Parsing Helper**
    -   Create a new internal helper function, e.g., `_parseDate(dateString, errorConstructor)`.
    -   This function will take a date string and an error constructor.
    -   It will handle the `new Date()` creation, check for `isNaN`, and return a `Effect.fail` with the appropriate error (`InvalidStartDateError` or `InvalidEndDateError`) on failure.

-   **Task 2.2: Integrate Date Parsing Helper**
    -   Update `getStart` and `getEnd` to use the new `_parseDate` helper function, removing the duplicated date parsing and validation logic.

-   **Task 2.3: Consolidate Duration Validation**
    -   Create a small helper `_validateDuration(duration)` that checks if the duration is a positive number and returns an `InvalidDurationError` otherwise.
    -   Update `getEnd` and `validateIcsEvent` to use this helper, removing duplicated checks.
