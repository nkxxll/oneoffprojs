import { Duration, Effect } from "effect";
import { type EventParams } from "./Models.js";

const formatDate = (date: Date): string =>
  date.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

// TODO: handle the errors
const getStart = (event: EventParams) =>
  Effect.gen(function* () {
    return new Date(event.start);
  });
// TODO: handle the errors
const getEnd = (event: EventParams) =>
  Effect.gen(function* () {
    if (!event.duration && !event.end) {
      yield* Effect.log("No duration or end given choosing default 1h!");
      const s = yield* getStart(event);
      return new Date(
        s.setTime(s.getTime() + Duration.toMillis(Duration.hours(1))),
      );
    } else if (event.duration && !event.end) {
      const s = yield* getStart(event);
      return new Date(s.setTime(s.getTime() + event.duration!));
    }
    return new Date(event.end!);
  });

export const generateIcsString = (events: readonly EventParams[]) =>
  Effect.gen(function* () {
    const lines: string[] = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//effect-ts//ics-generator//EN",
    ];

    for (const event of events) {
      const s = yield* getStart(event);
      const e = yield* getEnd(event);
      const uid = Bun.randomUUIDv7();
      lines.push("BEGIN:VEVENT");
      lines.push(`UID:${uid}`);
      lines.push(`SUMMARY:${event.title}`);
      if (event.description) lines.push(`DESCRIPTION:${event.description}`);
      if (event.location) lines.push(`LOCATION:${event.location}`);
      lines.push(`DTSTART:${formatDate(s)}`);
      lines.push(`DTEND:${formatDate(e)}`);
      lines.push("END:VEVENT");
    }

    lines.push("END:VCALENDAR");
    return lines.join("\r\n");
  });
