import { Tool } from "@effect/ai/McpSchema";

export const ICSTool = Tool.make("EventCreator", {
    description: "Create an ICS file with the start time and the end time",
    parameters: {
        start: Schema.Number,
        end: Schema.Number,
    },
    success: Schema.String,
}).annotate(Tool.Idempotent, true);

