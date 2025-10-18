import { McpServer, Toolkit } from "@effect/ai";
import { Tool } from "@effect/ai";
import { Effect, Schema } from "effect";
import { CalendarParams, EventParams } from "./Models.js";
import { validateIcsEvent, generateIcsString } from "./ICS.js";

const validateEvent = (params: EventParams) =>
  Effect.gen(function* () {
    const validatedEvent = yield* validateIcsEvent(params);
    return JSON.stringify(validatedEvent);
  });

// yes this is just a wrapper that does nothing but if in the future there has
// to be some validation logic or so I want that to be handled here
const createCalendar = (params: CalendarParams) =>
  Effect.gen(function* () {
    const content = yield* generateIcsString(params.calendarList);
    return `Please create a file named calendar.ics with the following content:\n\n${content}`;
  });

const ValidateEvent = Tool.make("ValidateEvent", {
  description: "Validate an ICS event",
  parameters: EventParams,
  success: Schema.String,
  failure: Schema.String,
}).annotate(Tool.Idempotent, true);

const CreateCalendar = Tool.make("CreateCalendar", {
  parameters: CalendarParams,
  description: "Create an ICS file with the start time and the end time",
  success: Schema.String,
  failure: Schema.String,
}).annotate(Tool.Readonly, true);

const ICSToolkit = Toolkit.make(ValidateEvent, CreateCalendar);

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit);

export const ICSToolImplLayer = ICSToolkit.toLayer({
  ValidateEvent: (params) =>
    validateEvent(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) =>
          Effect.fail(`Invalid start date: ${e.dateString}`),
        InvalidEndDateError: (e) =>
          Effect.fail(`Invalid end date: ${e.dateString}`),
        InvalidDurationError: (e) =>
          Effect.fail(`Invalid duration: ${e.duration}ms`),
        InvalidTitleError: (e) =>
          Effect.fail(`Invalid title: ${e.title}`),
      }),
    ),
  CreateCalendar: (params) =>
    createCalendar(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) =>
          Effect.fail(`Invalid start date: ${e.dateString}`),
        InvalidEndDateError: (e) =>
          Effect.fail(`Invalid end date: ${e.dateString}`),
        InvalidDurationError: (e) =>
          Effect.fail(`Invalid duration: ${e.duration}ms`),
        EndBeforeStartError: (e) =>
          Effect.fail(`End date ${e.end.toISOString()} is before start date ${e.start.toISOString()}`),
        InvalidTitleError: (e) =>
          Effect.fail(`Invalid title: ${e.title}`),
      }),
    ),
});
