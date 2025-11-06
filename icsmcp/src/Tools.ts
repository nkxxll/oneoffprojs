import { McpServer, Tool, Toolkit } from "@effect/ai"
import { FileSystem } from "@effect/platform"
import { BunContext } from "@effect/platform-bun"
import type { PlatformError } from "@effect/platform/Error"
import { Config, Effect, Schema } from "effect"
import { generateIcsString, validateIcsEvent } from "./ICS.js"
import { CalendarParams, EventParams } from "./Models.js"

const validateEvent = (params: EventParams) =>
  Effect.gen(function*() {
    const validatedEvent = yield* validateIcsEvent(params)
    return JSON.stringify(validatedEvent)
  }).pipe(
    Effect.catchTags({
      InvalidStartDateError: (e) => Effect.fail(`Invalid start date: ${e.dateString}`),
      InvalidEndDateError: (e) => Effect.fail(`Invalid end date: ${e.dateString}`),
      InvalidDurationError: (e) => Effect.fail(`Invalid duration: ${e.duration}ms`),
      InvalidTitleError: (e) => Effect.fail(`Invalid title: ${e.title}`)
    })
  )

const createCalendar = (params: CalendarParams) =>
  Effect.gen(function*() {
    const fs = yield* FileSystem.FileSystem
    const home = yield* Config.string("HOME")
    const calendarDir = `${home}/git/oneoffprojs/icsmcp/calendars`
    yield* fs.makeDirectory(calendarDir, { recursive: true })
    const timestamp = Date.now()
    const filename = `${calendarDir}/${timestamp}.ics`
    const content = yield* generateIcsString(params.calendarList)
    yield* fs.writeFileString(filename, content)
    return `Your calendar can be found in: file:///calendars/${timestamp}.ics`
  }).pipe(
    Effect.provide(BunContext.layer),
    Effect.catchTags({
      InvalidStartDateError: (e) => Effect.fail(`Invalid start date: ${e.dateString}`),
      InvalidEndDateError: (e) => Effect.fail(`Invalid end date: ${e.dateString}`),
      InvalidDurationError: (e) => Effect.fail(`Invalid duration: ${e.duration}ms`),
      EndBeforeStartError: (e) =>
        Effect.fail(
          `End date ${e.end.toISOString()} is before start date ${e.start.toISOString()}`
        ),
      InvalidTitleError: (e) => Effect.fail(`Invalid title: ${e.title || "no cause"}`),
      SystemError: (e: PlatformError) => Effect.fail(`Platform error occured while saving the file: ${e.message}`),
      BadArgument: (error) => Effect.fail(`Bad argument error ${error.message}`)
    })
  )

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
})

const ICSToolkit = Toolkit.make(ValidateEvent, CreateCalendar)

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit)

export const ICSToolImplLayer = ICSToolkit.toLayer({
  ValidateEvent: (params) => validateEvent(params),
  CreateCalendar: (params) => createCalendar(params)
})
