import { Schema, Data } from "effect";

export const EventParams = {
  start: Schema.String,
  end: Schema.optional(Schema.String),
  duration: Schema.optional(Schema.Number), // unix mills :D
  title: Schema.String,
  description: Schema.optional(Schema.String),
  location: Schema.optional(Schema.String),
};

// Note: this creates the structure I need to generate the type later !but! EventParams is and cannot be a struct
const EventParamsSchema = Schema.Struct(EventParams);

export type EventParams = Schema.Schema.Type<typeof EventParamsSchema>;

export const CalendarParams = {
  calendarList: Schema.Array(EventParamsSchema)
};

const CalendarParamsSchema = Schema.Struct(CalendarParams);

export type CalendarParams = Schema.Schema.Type<typeof CalendarParamsSchema>;

// Custom error types for validation
export class InvalidStartDateError extends Data.TaggedError("InvalidStartDateError")<{
  readonly dateString: string;
}> {}

export class InvalidEndDateError extends Data.TaggedError("InvalidEndDateError")<{
  readonly dateString: string;
}> {}

export class InvalidDurationError extends Data.TaggedError("InvalidDurationError")<{
  readonly duration: number;
}> {}

export class EndBeforeStartError extends Data.TaggedError("EndBeforeStartError")<{
  readonly start: Date;
  readonly end: Date;
}> {}

export class InvalidTitleError extends Data.TaggedError("InvalidTitleError")<{
  readonly title: string;
}> {}
