import { McpSchema, McpServer } from "@effect/ai"
import { FileSystem } from "@effect/platform"
import { BunContext, BunSink, BunStream } from "@effect/platform-bun"
import type { PlatformError } from "@effect/platform/Error"
import { Effect, Layer, Logger, Schema } from "effect"
import { ICSToolImplLayer, ICSToolkitLayer } from "./Tools.js"

// TODO this could be the place where we store the state of the mcp server with the ics calendar events
const Readme = McpServer.resource({
  uri: "file:///README.md",
  name: "README",
  description: "README Markdown file that explains usage of the mcp tools",
  mimeType: "text/x-markdown",
  audience: ["assistant", "user"],
  content: Effect.succeed(`# ICS Event Planner MCP
## ValidateEvent
Validates the date and information for an Event.
## CreateCalendar
Is able to create an ICS Calendar File
`)
})

const timestamp = McpSchema.param("timestamp", Schema.NumberFromString)

const CalendarFiles = McpServer.resource`file://calendars/${timestamp}.ics`({
  name: "Calendars",
  description: "This is a directory with all the created calendars named with the timestamp of their creation.",
  mimeType: "text/calendar",
  audience: ["assistant", "user"],
  content(
    _uri: string,
    timestamp: number
  ) {
    return Effect.gen(function*() {
      const fs = yield* FileSystem.FileSystem
      const path = `calendars/${timestamp}.ics`
      const content = yield* fs.readFileString(path)
      return content
    }).pipe(
      Effect.catchTag("SystemError", (e: PlatformError) => Effect.fail(`Calendar file not found: ${e.cause}`))
    )
  }
})

const EventPrompt = McpServer.prompt({
  name: "Event",
  description: "Enter an event through this template",
  parameters: Schema.Struct({
    start: Schema.String,
    end: Schema.String,
    day: Schema.String
  }),
  completion: {
    start: () => Effect.succeed([]),
    end: () => Effect.succeed([]),
    day: () => Effect.succeed([":today", ":tomorrow", ":nextweek"])
  },
  content: ({ day, end, start }) =>
    Effect.succeed(
      `Book an event with the start at ${start}, the end at ${end} and day ${day} use the EventCreator tool.`
    )
})

// Merge all the resources and prompts into a single server layer
export const ServerLayer = Layer.mergeAll(
  Readme,
  EventPrompt,
  CalendarFiles,
  ICSToolkitLayer.pipe(Layer.provide(ICSToolImplLayer))
).pipe(
  Layer.provide(BunContext.layer),
  Layer.provide(
    McpServer.layerStdio({
      name: "ICS mcp",
      version: "1.0.0",
      stdin: BunStream.stdin,
      stdout: BunSink.stdout
    })
  ),
  Layer.provide(Logger.add(Logger.prettyLogger({ stderr: true })))
)
