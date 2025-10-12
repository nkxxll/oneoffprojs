import { McpServer, Toolkit } from "@effect/ai";
import { Tool } from "@effect/ai";
import { Effect, Schema } from "effect";
import { CalendarParams, EventParams } from "./Models.js";
import { generateIcsString } from "./ICS.js";

const validateEvent = (params: EventParams) =>
  Effect.gen(function* () {
    return JSON.stringify(params);
  });

// yes this is just a wrapper that does nothing but if in the future there has
// to be some validation logic or so I want that to be handled here
const createCalendar = (params: CalendarParams) =>
  generateIcsString(params.calendarList);

const ValidateEvent = Tool.make("ValidateEvent", {
  description: "Create an ICS file with the start time and the end time",
  parameters: EventParams,
  success: Schema.String,
}).annotate(Tool.Idempotent, true);

const CreateCalendar = Tool.make("CreateCalendar", {
  parameters: CalendarParams,
  description: "Create an ICS file with the start time and the end time",
  success: Schema.String,
}).annotate(Tool.Readonly, true);

const ICSToolkit = Toolkit.make(ValidateEvent, CreateCalendar);

export const ICSToolkitLayer = McpServer.toolkit(ICSToolkit);

export const ICSToolImplLayer = ICSToolkit.toLayer({
  ValidateEvent: (params) => validateEvent(params),
  CreateCalendar: (params) => createCalendar(params),
});
