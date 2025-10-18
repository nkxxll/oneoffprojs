# Plan to Fix Response Types in Tools.ts and ICS.ts

## Overview

The MCP server SDK currently only supports text content types, so the tool success and failure schemas are set to `Schema.String`. The implementations need to be updated to return plain strings instead of structured response objects. For the `CreateCalendar` tool, the response should be a text message instructing the client to create a file with the ICS content.

## Current Issues

1. `generateIcsString` in `ICS.ts` returns a resource response object with `{ type: "resource", resource: {...} }`
2. `createCalendar` in `Tools.ts` passes through this resource object
3. The tool implementations expect text responses, but some are returning resource objects
4. The error handling in both the validate and the create calendar tool in `Tools.ts` returns an
   error object which should now be only a string with the message.

## Planned Changes

### 1. Update `generateIcsString` in `ICS.ts`

- **Change return type**: Instead of returning a resource response object, return the ICS content string directly
- **Remove `createIcsFileResponse`**: No longer needed since we're returning text instead of resources
- **Keep validation logic**: The event validation remains the same

**Before:**

```typescript
export const generateIcsString = (events: readonly EventParams[]) =>
  Effect.gen(function* () {
    // ... validation and generation ...
    const content = lines.join("\r\n");
    const response = createIcsFileResponse(content);
    return response;
  });
```

**After:**

```typescript
export const generateIcsString = (events: readonly EventParams[]) =>
  Effect.gen(function* () {
    // ... validation and generation ...
    const content = lines.join("\r\n");
    return content;
  });
```

### 2. Update `createCalendar` in `Tools.ts`

- **Change return type**: Instead of returning the resource object, return a text message containing the ICS content
- **Add instruction message**: Include text telling the client to create a file with the content

**Before:**

```typescript
const createCalendar = (params: CalendarParams) =>
  generateIcsString(params.calendarList);
```

**After:**

```typescript
const createCalendar = (params: CalendarParams) =>
  Effect.gen(function* () {
    const content = yield* generateIcsString(params.calendarList);
    return `Please create a file named calendar.ics with the following content:\n\n${content}`;
  });
```

### 3. Update `ValidateEvent` response in `Tools.ts`

- **Keep current JSON response**: The validation tool already returns a text response with JSON
- **Optional enhancement**: Consider adding a more user-friendly message prefix, but the current JSON.stringify is functional

**Current (no change needed):**

```typescript
const validateEvent = (params: EventParams) =>
  Effect.gen(function* () {
    const validatedEvent = yield* validateIcsEvent(params);
    return JSON.stringify(validatedEvent);
  });
```

### 4. Ensure Tool Implementations Match Schemas

- **Schemas are correct**: Both tools already have `success: Schema.String, failure: Schema.String`
- **Implementation alignment**: The `ICSToolImplLayer` will now correctly return string values that match the schemas
- **Error handling**: Keep the existing error transformation logic in the implementation layer but
  return `Effect.success` with the message string

## Testing Considerations

- Verify that `CreateCalendar` returns a properly formatted text message with the ICS content
- Ensure `ValidateEvent` still returns valid JSON for validated events
- Test error cases to ensure failure responses are still strings
- Confirm that the client can parse and use the text responses appropriately

## Migration Notes

- This change maintains backward compatibility for the tool schemas
- The client will need to handle text responses differently than resource objects
- For `CreateCalendar`, clients should extract the ICS content from the text message and create the file manually
