import { McpServer, Toolkit } from "@effect/ai";
import { Tool } from "@effect/ai";
import { Effect, Schema } from "effect";
import { EventParams } from "./Models.js";

const createEvent = (
  params: { readonly description?: string | undefined } & {
    readonly start: string;
  } & { readonly end?: string | undefined } & {
    readonly duration?: string | undefined;
  } & { readonly title: string } & { readonly location?: string | undefined },
) =>
  Effect.gen(function* () {
    return "hey ho this needs to be implemented";
  });

const CreateEvent = Tool.make("CreateEvent", {
  description: "Create an ICS file with the start time and the end time",
  parameters: EventParams,
  success: Schema.String,
}).annotate(Tool.Idempotent, true);

const CreateCalendar = Tool.make("CreateCalendar", {
  description: "Create an ICS file with the start time and the end time",
  success: Schema.String,
}).annotate(Tool.Readonly, true);

const ICSToolkit = Toolkit.make(CreateEvent, CreateCalendar);

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit);

export const ICSToolImplLayer = ICSToolkit.toLayer({
  CreateEvent: (params) => createEvent(params),
  CreateCalendar: () => Effect.succeed(`not implemented yet`),
});
