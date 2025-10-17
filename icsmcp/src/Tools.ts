import { McpServer, Toolkit } from "@effect/ai";
import { Tool } from "@effect/ai";
import { Effect, Schema } from "effect";
import { CalendarParams, EventParams } from "./Models.js";
import { validateIcsEvent, generateIcsString } from "./ICS.js";

const validateEvent = (params: EventParams) =>
  Effect.gen(function* () {
    const validatedEvent = yield* validateIcsEvent(params);
    return {
      type: "text",
      text: JSON.stringify(validatedEvent),
    };
  });

// yes this is just a wrapper that does nothing but if in the future there has
// to be some validation logic or so I want that to be handled here
const createCalendar = (params: CalendarParams) =>
  generateIcsString(params.calendarList);

const ValidateEvent = Tool.make("ValidateEvent", {
  description: "Validate an ICS event",
  parameters: EventParams,
  success: Schema.Struct({
    type: Schema.String,
    text: Schema.String,
  }),
  failure: Schema.Struct({
    type: Schema.Literal("error"),
    error: Schema.Struct({
      message: Schema.String,
      code: Schema.String,
    }),
  }),
}).annotate(Tool.Idempotent, true);

const CreateCalendar = Tool.make("CreateCalendar", {
  parameters: CalendarParams,
  description: "Create an ICS file with the start time and the end time",
  success: Schema.Struct({
    type: Schema.Literal("resource"),
    resource: Schema.Struct({
      uri: Schema.String,
      mimeType: Schema.String,
      text: Schema.String,
    }),
  }),
  failure: Schema.Struct({
    type: Schema.Literal("error"),
    error: Schema.Struct({
      message: Schema.String,
      code: Schema.String,
    }),
  }),
}).annotate(Tool.Readonly, true);

const ICSToolkit = Toolkit.make(ValidateEvent, CreateCalendar);

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit);

export const ICSToolImplLayer = ICSToolkit.toLayer({
  ValidateEvent: (params) =>
    validateEvent(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid start date: ${e.dateString}`,
              code: "INVALID_START_DATE",
            },
          } as const),
        InvalidEndDateError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid end date: ${e.dateString}`,
              code: "INVALID_END_DATE",
            },
          } as const),
        InvalidDurationError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid duration: ${e.duration}ms`,
              code: "INVALID_DURATION",
            },
          } as const),
        InvalidTitleError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid title: ${e.title}`,
              code: "INVALID_TITLE",
            },
          } as const),
      }),
    ),
  CreateCalendar: (params) =>
    createCalendar(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid start date: ${e.dateString}`,
              code: "INVALID_START_DATE",
            },
          } as const),
        InvalidEndDateError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid end date: ${e.dateString}`,
              code: "INVALID_END_DATE",
            },
          } as const),
        InvalidDurationError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid duration: ${e.duration}ms`,
              code: "INVALID_DURATION",
            },
          } as const),
        EndBeforeStartError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `End date ${e.end.toISOString()} is before start date ${e.start.toISOString()}`,
              code: "END_BEFORE_START",
            },
          } as const),
        InvalidTitleError: (e) =>
          Effect.fail({
            type: "error" as const,
            error: {
              message: `Invalid title: ${e.title}`,
              code: "INVALID_TITLE",
            },
          } as const),
      }),
    ),
});
