# Plan for Handling Errors and Validation in ICS.ts with Effect

## Overview
This plan outlines how to handle all possible errors related to date conversions and implement comprehensive event validation in `src/ICS.ts` using Effect's error handling capabilities. The current code has TODOs for error handling in `getStart`, `getEnd`, and validation in `validateIcsEvent`.

## Current Issues
- `getStart` and `getEnd` functions create `new Date()` without checking for invalid date strings
- No validation of date relationships (e.g., end before start)
- No validation of duration values
- `validateIcsEvent` is not implemented
- Date parsing can result in "Invalid Date" objects without proper error handling

## Error Handling Strategy

### 1. Date Parsing Errors
- **Problem**: `new Date(string)` doesn't throw but can create Invalid Date objects
- **Solution**: Use `Effect.try` to wrap date creation and check validity with `isNaN(date.getTime())`
- **Error Types**: Define custom error types for invalid dates

### 2. Required Field Validation
- **Problem**: EventParams.start is required but could be invalid
- **Solution**: Validate that start date is valid in `getStart`

### 3. Optional Field Validation
- **Problem**: event.end and event.duration are optional but when provided must be valid
- **Solution**: In `getEnd`, validate end date if provided, validate duration if provided

### 4. Logical Validation
- **Problem**: End date could be before start date
- **Solution**: Add validation to ensure end >= start when both are provided

### 5. Duration Validation
- **Problem**: Duration could be negative or unreasonably large
- **Solution**: Validate duration is positive and reasonable (e.g., not exceeding 24 hours for events)

## Implementation Plan

### Custom Error Types
Define error classes/schemata for different validation failures:
- `InvalidStartDateError`
- `InvalidEndDateError` 
- `InvalidDurationError`
- `EndBeforeStartError`
- `MissingEndOrDurationError` (though current logic defaults to 1h)

### Updated getStart Function
```typescript
const getStart = (event: EventParams) =>
  Effect.gen(function* () {
    const date = yield* Effect.try({
      try: () => new Date(event.start),
      catch: () => new InvalidStartDateError(event.start)
    });
    
    if (isNaN(date.getTime())) {
      return yield* new InvalidStartDateError(event.start);
    }
    
    return date;
  });
```

### Updated getEnd Function  
```typescript
const getEnd = (event: EventParams) =>
  Effect.gen(function* () {
    const start = yield* getStart(event);
    
    if (event.end && event.duration) {
      // Both provided - validate both but prefer duration for calculation
      const endDate = yield* Effect.try({
        try: () => new Date(event.end),
        catch: () => new InvalidEndDateError(event.end)
      });
      
      if (isNaN(endDate.getTime())) {
        return yield* new InvalidEndDateError(event.end);
      }
      
      if (event.duration <= 0) {
        return yield* new InvalidDurationError(event.duration);
      }
      
      // Use duration for calculation but warn if it doesn't match end
      const calculatedEnd = new Date(start.getTime() + event.duration);
      if (Math.abs(calculatedEnd.getTime() - endDate.getTime()) > 1000) { // Allow 1s tolerance
        yield* Effect.logWarning("Duration and end time don't match, using duration");
      }
      
      return calculatedEnd;
    }
    
    if (event.duration && !event.end) {
      if (event.duration <= 0) {
        return yield* new InvalidDurationError(event.duration);
      }
      
      return new Date(start.getTime() + event.duration);
    }
    
    if (event.end && !event.duration) {
      const endDate = yield* Effect.try({
        try: () => new Date(event.end),
        catch: () => new InvalidEndDateError(event.end)
      });
      
      if (isNaN(endDate.getTime())) {
        return yield* new InvalidEndDateError(event.end);
      }
      
      if (endDate <= start) {
        return yield* new EndBeforeStartError(start, endDate);
      }
      
      return endDate;
    }
    
    // Neither provided - default to 1 hour
    yield* Effect.log("No duration or end given, choosing default 1h!");
    return new Date(start.getTime() + Duration.toMillis(Duration.hours(1)));
  });
```

### validateIcsEvent Implementation
```typescript
export const validateIcsEvent = (event: EventParams) => 
  Effect.gen(function* () {
    // First validate the schema structure (though TypeScript handles this at compile time)
    // We could add runtime schema validation if needed
    
    // Validate start date
    yield* getStart(event);
    
    // Validate end/date logic without calculating (to avoid duplicate work)
    if (event.end) {
      const endDate = yield* Effect.try({
        try: () => new Date(event.end),
        catch: () => new InvalidEndDateError(event.end)
      });
      
      if (isNaN(endDate.getTime())) {
        return yield* new InvalidEndDateError(event.end);
      }
    }
    
    if (event.duration !== undefined) {
      if (typeof event.duration !== 'number' || event.duration <= 0) {
        return yield* new InvalidDurationError(event.duration);
      }
    }
    
    // Validate title is not empty
    if (!event.title || event.title.trim().length === 0) {
      return yield* new InvalidTitleError(event.title);
    }
    
    // Success - return the validated event
    return event;
  });
```

### Updated generateIcsString Function
The main function should handle validation errors:
```typescript
export const generateIcsString = (events: readonly EventParams[]) =>
  Effect.gen(function* () {
    // Validate all events first
    for (const event of events) {
      yield* validateIcsEvent(event);
    }
    
    const lines: string[] = [
      "BEGIN:VCALENDAR", 
      "VERSION:2.0",
      "PRODID:-//effect-ts//ics-generator//EN",
    ];

    for (const event of events) {
      const s = yield* getStart(event);
      const e = yield* getEnd(event);
      const uid = Bun.randomUUIDv7();
      lines.push("BEGIN:VEVENT");
      lines.push(`UID:${uid}`);
      lines.push(`SUMMARY:${event.title}`);
      if (event.description) lines.push(`DESCRIPTION:${event.description}`);
      if (event.location) lines.push(`LOCATION:${event.location}`);
      lines.push(`DTSTART:${formatDate(s)}`);
      lines.push(`DTEND:${formatDate(e)}`);
      lines.push("END:VEVENT");
    }

    lines.push("END:VCALENDAR");
    return lines.join("\r\n");
  });
```

## Error Type Definitions
Add to Models.ts or a new errors.ts file:
```typescript
export class InvalidStartDateError extends Data.TaggedError("InvalidStartDateError")<{
  readonly dateString: string;
}> {}

export class InvalidEndDateError extends Data.TaggedError("InvalidEndDateError")<{
  readonly dateString: string;
}> {}

export class InvalidDurationError extends Data.TaggedError("InvalidDurationError")<{
  readonly duration: number;
}> {}

export class EndBeforeStartError extends Data.TaggedError("EndBeforeStartError")<{
  readonly start: Date;
  readonly end: Date;
}> {}

export class InvalidTitleError extends Data.TaggedError("InvalidTitleError")<{
  readonly title: string;
}> {}
```

## Testing Considerations
- Test invalid date strings
- Test negative durations  
- Test end before start
- Test missing required fields
- Test valid cases
- Test edge cases like leap years, timezone handling

## Future Improvements
- Add timezone support
- Add recurrence rule validation
- Add attendee validation
- Add custom property validation
