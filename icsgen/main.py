#!/usr/bin/env python3
"""
icsgen — Simple ICS calendar event generator with minimal dependencies.

Usage examples:
  icsgen 9:00 "Read paper" :tomorrow-10:00
  icsgen :tomorrow-8:00 "Team sync" Office :tomorrow-9:00
  icsgen 2025-10-08T10:00 "Call with client" 2025-10-08T11:00
  icsgen now+15m "Coffee break" now+45m
  icsgen -m tasks.txt -o schedule.ics
"""

import argparse
import re
from datetime import datetime, timedelta
from uuid import uuid4
from pathlib import Path
import sys


# ------------------ Time Parsing ------------------ #
def parse_time(t: str) -> datetime:
    """Parse multiple natural time formats into datetime."""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    # :tomorrow-8:00
    if t.startswith(":tomorrow-"):
        hh, mm = map(int, t.split("-")[1].split(":"))
        return datetime.combine(tomorrow.date(), datetime.min.time()) + timedelta(hours=hh, minutes=mm)

    # :today-8:00
    if t.startswith(":today-"):
        hh, mm = map(int, t.split("-")[1].split(":"))
        return datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=hh, minutes=mm)

    # HH:MM → today
    if re.match(r"^\d{1,2}:\d{2}$", t):
        hh, mm = map(int, t.split(":"))
        return datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=hh, minutes=mm)

    # DD.MMTHH:MM
    if re.match(r"^\d{1,2}\.\d{1,2}T\d{1,2}:\d{2}$", t):
        day, month, timepart = re.split(r"[\.T]", t)
        hh, mm = map(int, timepart.split(":"))
        return datetime(now.year, int(month), int(day), hh, mm)

    # DD.MM.YYYTHH:MM
    if re.match(r"^\d{1,2}\.\d{1,2}\.\d{4}T\d{1,2}:\d{2}$", t):
        day, month, year, timepart = re.split(r"[\.T]", t)
        hh, mm = map(int, timepart.split(":"))
        return datetime(int(year), int(month), int(day), hh, mm)

    # ISO 8601
    try:
        return datetime.fromisoformat(t)
    except ValueError:
        pass

    # now+1h or now+30m
    if t.startswith("now+"):
        match = re.match(r"now\+(\d+)([hm])", t)
        if match:
            num, unit = match.groups()
            delta = timedelta(hours=int(num)) if unit == "h" else timedelta(minutes=int(num))
            return now + delta

    # timestamp
    if t.isdigit():
        return datetime.fromtimestamp(int(t))

    raise ValueError(f"Unrecognized time format: {t}")


# ------------------ ICS Generation ------------------ #
def fmt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def make_event(summary, start, end, location=None, desc=None):
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uuid4()}",
        f"DTSTAMP:{fmt(datetime.utcnow())}Z",
        f"DTSTART:{fmt(start)}",
        f"DTEND:{fmt(end)}",
        f"SUMMARY:{summary}",
    ]
    if location:
        lines.append(f"LOCATION:{location}")
    if desc:
        lines.append(f"DESCRIPTION:{desc}")
    lines.append("END:VEVENT")
    return "\n".join(lines)


def make_calendar(events):
    return "\n".join(["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//icsgen//EN", *events, "END:VCALENDAR"])


# ------------------ CLI ------------------ #
def main():
    parser = argparse.ArgumentParser(description="Generate ICS calendar events easily.")
    parser.add_argument("args", nargs="*", help="Positional args: <start> <summary> [<location>] <end>")
    parser.add_argument("-o", "--output", default="event.ics", help="Output ICS file name (default: event.ics)")
    parser.add_argument("-d", "--desc", help="Optional event description")
    parser.add_argument("-m", "--multi", help="Read multiple events from a file (one per line)")
    parser.add_argument("--dry", action="store_true", help="Print output to stdout instead of writing file")

    opts = parser.parse_args()

    events = []

    if opts.multi:
        lines = Path(opts.multi).read_text().splitlines()
        for line in lines:
            if not line.strip():
                continue
            parts = re.findall(r'".+?"|\S+', line)
            parts = [p.strip('"') for p in parts]
            if len(parts) < 3:
                print(f"Skipping malformed line: {line}")
                continue

            start = parse_time(parts[0])
            summary = parts[1]
            if len(parts) == 3:
                end = parse_time(parts[2])
                location = None
            else:
                location = parts[2]
                end = parse_time(parts[3])

            events.append(make_event(summary, start, end, location))
    else:
        args = opts.args
        if len(args) < 3:
            parser.error("You must provide at least <start> <summary> <end>.")

        start = parse_time(args[0])
        summary = args[1]
        if len(args) == 3:
            end = parse_time(args[2])
            location = None
        else:
            location = args[2]
            end = parse_time(args[3])

        events.append(make_event(summary, start, end, location, opts.desc))

    ics_content = make_calendar(events)

    if opts.dry:
        print(ics_content)
    else:
        Path(opts.output).write_text(ics_content)
        print(f"✅ ICS file written to {Path(opts.output).resolve()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
