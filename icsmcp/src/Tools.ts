import { McpServer, Tool, Toolkit } from "@effect/ai"
import { Effect, Schema } from "effect"
import { generateIcsString, validateIcsEvent } from "./ICS.js"
import { CalendarParams, EventParams } from "./Models.js"

/** NOTE: elicit takes a schema that has to have a decode and an encode capability
 * the decoding has to return a plain object this is indicated by the signature/type template:
 * ```js
 * <S extends Schema.Codec<any, Record<string, unknown>, any, any>>
 * ```
 * Schema.Struct({ age: Schema.Number, name: Schema.String }) e.g. creates a plain object when decoded
 * Schema.Record({ key: Schema.Literal("age"), value: Schema.Number }) is the same as a struct with age
 * what you can do with a record is give a type for the key like Schema.Number and a schema for the value like
 * { start: number, end: number ... } for an event then you can get a
 * { 1: { start... }, 2: <event 2>, 3: <event 3> }
 */
// todo: just don't know how to use this thing yet
// const CalendarType = McpServer.elicit({
//   message: `Please provide the calendar type you are using: "apple" | "other" (default "apple")`,
//   schema: Schema.Struct({
//     calendar_type: Schema.Union(
//       Schema.Literal("apple"),
//       Schema.Literal("other"),
//     ),
//   }),
// });

const validateEvent = (params: EventParams) =>
  Effect.gen(function*() {
    const validatedEvent = yield* validateIcsEvent(params)
    return JSON.stringify(validatedEvent)
  })

// yes this is just a wrapper that does nothing but if in the future there has
// to be some validation logic or so I want that to be handled here
const createCalendar = (params: CalendarParams) =>
  Effect.gen(function*() {
    const content = yield* generateIcsString(params.calendarList)
    return `Please create a file named calendar.ics with the following content:\n\n${content}`
  })

const ValidateEvent = Tool.make("ValidateEvent", {
  description: "Validate an ICS event",
  parameters: EventParams,
  success: Schema.String,
  failure: Schema.String
}).annotate(Tool.Idempotent, true)

const CreateCalendar = Tool.make("CreateCalendar", {
  parameters: CalendarParams,
  description: "Create an ICS file with the start time and the end time",
  success: Schema.String,
  failure: Schema.String
}).annotate(Tool.Readonly, true)

const ICSToolkit = Toolkit.make(ValidateEvent, CreateCalendar)

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit)

export const ICSToolImplLayer = ICSToolkit.toLayer({
  ValidateEvent: (params) =>
    validateEvent(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) => Effect.fail(`Invalid start date: ${e.dateString}`),
        InvalidEndDateError: (e) => Effect.fail(`Invalid end date: ${e.dateString}`),
        InvalidDurationError: (e) => Effect.fail(`Invalid duration: ${e.duration}ms`),
        InvalidTitleError: (e) => Effect.fail(`Invalid title: ${e.title}`)
      })
    ),
  CreateCalendar: (params) =>
    createCalendar(params).pipe(
      Effect.catchTags({
        InvalidStartDateError: (e) => Effect.fail(`Invalid start date: ${e.dateString}`),
        InvalidEndDateError: (e) => Effect.fail(`Invalid end date: ${e.dateString}`),
        InvalidDurationError: (e) => Effect.fail(`Invalid duration: ${e.duration}ms`),
        EndBeforeStartError: (e) =>
          Effect.fail(
            `End date ${e.end.toISOString()} is before start date ${e.start.toISOString()}`
          ),
        InvalidTitleError: (e) => Effect.fail(`Invalid title: ${e.title}`)
      })
    )
})
