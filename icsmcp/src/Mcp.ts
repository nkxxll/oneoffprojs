import { McpServer } from "@effect/ai";
import { BunSink, BunStream } from "@effect/platform-bun";
import { Effect, Layer, Logger, Schema } from "effect";
import { ICSToolImplLayer, ICSToolkitLayer } from "./Tools.js";

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
`),
});

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


const EventPrompt = McpServer.prompt({
  name: "Event",
  description: "Enter an event through this template",
  parameters: Schema.Struct({
    start: Schema.String,
    end: Schema.String,
    day: Schema.String,
  }),
  completion: {
    start: () => Effect.succeed([]),
    end: () => Effect.succeed([]),
    day: () => Effect.succeed([":today", ":tomorrow", ":nextweek"]),
  },
  content: ({ start, end, day }) =>
    Effect.succeed(
      `Book an event with the start at ${start}, the end at ${end} and day ${day} use the EventCreator tool.`,
    ),
});

// Merge all the resources and prompts into a single server layer
export const ServerLayer = Layer.mergeAll(
  Readme,
  EventPrompt,
  ICSToolkitLayer.pipe(Layer.provide(ICSToolImplLayer)),
).pipe(
  Layer.provide(
    McpServer.layerStdio({
      name: "ICS mcp",
      version: "1.0.0",
      stdin: BunStream.stdin,
      stdout: BunSink.stdout,
    }),
  ),
  Layer.provide(Logger.add(Logger.prettyLogger({ stderr: true }))),
);
