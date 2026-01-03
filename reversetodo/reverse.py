#!/usr/bin/env python3
import sys

sections = []
current = []

for line in sys.stdin:
    if line.startswith("="):
        if current:
            sections.append("".join(current))
            current = []
    current.append(line)

if current:
    sections.append("".join(current))

# reverse section order
for section in reversed(sections):
    sys.stdout.write(section)
