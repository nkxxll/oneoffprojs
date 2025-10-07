#!/usr/bin/env bash
set -e

# Run from script directory
cd "$(dirname "$0")"

PYTHON="uv run"
ICSGEN="./main.py"

# Helper function to run a single test
run_test() {
  local name="$1"
  local cmd="$2"
  local expected="$3"

  echo "Running: $name"
  output=$($PYTHON $ICSGEN $cmd --dry)

  if echo "$output" | grep -q "$expected"; then
    echo "✅ $name passed"
  else
    echo "❌ $name failed"
    echo "Expected to find: $expected"
    echo "Got output:"
    echo "$output"
    echo
    exit 1
  fi
}

# 1️⃣ Test simple event (today 9:00 → today 10:00)
run_test "Basic event" "9:00 Read_paper 10:00" "SUMMARY:Read_paper"

# 2️⃣ Test event with location
run_test "With location" ":tomorrow-8:00 Team_sync Office :tomorrow-9:00" "LOCATION:Office"

# 3️⃣ Test event with description
run_test "With description" "9:00 Coffee_break 9:30 --desc Short_break" "DESCRIPTION:Short_break"

# 4️⃣ Test ISO format
run_test "ISO time" "2025-10-08T10:00 Meeting 2025-10-08T11:00" "SUMMARY:Meeting"

# 5️⃣ Test now+15m parsing
run_test "Relative now+15m" "now+15m Quick_task now+45m" "SUMMARY:Quick_task"

echo
echo "🎉 All tests passed!"
