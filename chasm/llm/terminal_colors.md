# Plan to Use Terminal Colors in Chasm TUI

## Problem
The TUI app "chasm" currently uses hardcoded colors like "black" for backgrounds and named colors like "green", "red" for foregrounds. These do not respect the user's terminal color scheme, leading to poor visibility or aesthetics on terminals with different themes (e.g., light backgrounds).

## Goal
Modify the code to use the terminal's default colors instead of hardcoded ones, ensuring the app adapts to the user's terminal theme.

## Analysis
- **Library**: @opentui/react uses named colors (e.g., "red", "green") which map to ANSI color codes internally.
- **Hardcoded Colors Found**:
  - Backgrounds: "black" in Toast.tsx and CommandPalette.tsx
  - Foregrounds: "green", "yellow", "red", "blue" in StatusView.tsx and DiffView.tsx
- **Terminal Colors**: Refers to using the terminal's default foreground/background colors, which vary by theme.

## Solution Approach
1. **Remove Hardcoded Backgrounds**: Eliminate `backgroundColor: "black"` from components to use the terminal's default background.
2. **Keep Foreground Colors**: Named colors like "green" are acceptable as they correspond to standard ANSI colors, which terminals adjust.
3. **Theme Detection (Future)**: If needed, detect light/dark theme using environment variables like `COLORFGBG` and adjust colors accordingly.

## Steps
1. **Update Toast.tsx**: Remove `backgroundColor: "black"` from the box style.
2. **Update CommandPalette.tsx**: Remove `backgroundColor: "black"` from the box styles in file selector and message boxes.
3. **Verify Other Components**: Ensure StatusView.tsx and DiffView.tsx use appropriate named colors.
4. **Test**: Run the app in different terminal themes to ensure visibility.

## Potential Enhancements
- Add support for custom color schemes via environment variables.
- Use ANSI escape codes directly if @opentui supports them for finer control.
- Detect color support and fall back to monochrome if needed.

## Risks
- Removing backgrounds might make text less readable if terminal has poor contrast.
- @opentui may not handle unset backgrounds as expected; test thoroughly.
