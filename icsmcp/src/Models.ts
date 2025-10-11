import { Schema } from "effect";

export const Event = Schema.Struct({
  start: Schema.String,
  end: Schema.optional(Schema.String),
  duration: Schema.optional(Schema.String),
  title: Schema.String,
  description: Schema.optional(Schema.String),
  location: Schema.optional(Schema.String),
});

export type Event = Schema.Schema.Type<typeof Event>;

export const EventParams = {
  start: Schema.String,
  end: Schema.optional(Schema.String),
  duration: Schema.optional(Schema.String),
  title: Schema.String,
  description: Schema.optional(Schema.String),
  location: Schema.optional(Schema.String),
};

export type EventParams = typeof EventParams
