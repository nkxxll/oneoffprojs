import { Duration, Effect } from "effect"
import {
  EndBeforeStartError,
  type EventParams,
  InvalidDurationError,
  InvalidEndDateError,
  InvalidStartDateError,
  InvalidTitleError
} from "./Models.js"

const formatDate = (date: Date): string => date.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z"

const _parseDate = (dateString: string, error: InvalidStartDateError | InvalidEndDateError) =>
  Effect.gen(function*() {
    const date = yield* Effect.try({
      try: () => new Date(dateString),
      catch: () => error
    })
    if (isNaN(date.getTime())) {
      return yield* Effect.fail(error)
    }
    return date
  })

const _validateDuration = (duration: number) => {
  if (typeof duration !== "number" || duration <= 0) {
    return Effect.fail(new InvalidDurationError({ duration }))
  }
  return Effect.succeed(duration)
}

const getStart = (event: EventParams) => _parseDate(event.start, new InvalidStartDateError({ dateString: event.start }))

const getEnd = (event: EventParams) =>
  Effect.gen(function*() {
    const start = yield* getStart(event)

    if (event.end && event.duration) {
      const endDate = yield* _parseDate(event.end, new InvalidEndDateError({ dateString: event.end }))
      yield* _validateDuration(event.duration)

      // Use duration for calculation but warn if it doesn't match end
      const calculatedEnd = new Date(start.getTime() + event.duration)
      if (Math.abs(calculatedEnd.getTime() - endDate.getTime()) > 1000) { // Allow 1s tolerance
        yield* Effect.logWarning(
          "Duration and end time don't match, using duration"
        )
      }

      return calculatedEnd
    }

    if (event.duration && !event.end) {
      yield* _validateDuration(event.duration)
      return new Date(start.getTime() + event.duration)
    }

    if (event.end && !event.duration) {
      const endDate = yield* _parseDate(event.end, new InvalidEndDateError({ dateString: event.end }))
      if (endDate <= start) {
        return yield* Effect.fail(
          new EndBeforeStartError({ start, end: endDate })
        )
      }
      return endDate
    }

    // Neither provided - default to 1 hour
    yield* Effect.log("No duration or end given, choosing default 1h!")
    return new Date(start.getTime() + Duration.toMillis(Duration.hours(1)))
  })

export const validateIcsEvent = (event: EventParams) =>
  Effect.gen(function*() {
    yield* getStart(event)

    if (event.end) {
      yield* _parseDate(event.end, new InvalidEndDateError({ dateString: event.end }))
    }

    if (event.duration !== undefined) {
      yield* _validateDuration(event.duration)
    }

    if (!event.title || event.title.trim().length === 0) {
      return yield* Effect.fail(new InvalidTitleError({ title: event.title }))
    }

    return event
  })

export const generateIcsString = (events: ReadonlyArray<EventParams>) =>
  Effect.gen(function*() {
    // Validate all events first
    for (const event of events) {
      yield* validateIcsEvent(event)
    }

    const lines: Array<string> = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//effect-ts//ics-generator//EN"
    ]

    for (const event of events) {
      const s = yield* getStart(event)
      const e = yield* getEnd(event)
      const uid = crypto.randomUUID()
      lines.push("BEGIN:VEVENT")
      lines.push(`UID:${uid}`)
      lines.push(`SUMMARY:${event.title}`)
      if (event.description) lines.push(`DESCRIPTION:${event.description}`)
      if (event.location) lines.push(`LOCATION:${event.location}`)
      lines.push(`DTSTART:${formatDate(s)}`)
      lines.push(`DTEND:${formatDate(e)}`)
      lines.push("END:VEVENT")
    }

    lines.push("END:VCALENDAR")
    const content = lines.join("\r\n")
    return content
  })
