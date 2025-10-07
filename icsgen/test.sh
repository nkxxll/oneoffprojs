#!/usr/bin/env bash
set -e

# Run from script directory
cd "$(dirname "$0")"

PYTHON="uv run"
ICSGEN="./main.py"
FIXTURES_DIR="./fixtures"

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

# Helper function to run a file creation test
run_file_creation_test() {
    local name="$1"
    local cmd="$2"

    echo "Running: $name"
    output=$($PYTHON $ICSGEN $cmd)

    # Get the output path from the success message
    # "✅ ICS file written to /tmp/some-uuid.ics"
    path=$(echo "$output" | grep "ICS file written to" | sed 's/.* to //')

    if [[ -f "$path" ]]; then
        echo "✅ $name passed"
        rm "$path" # cleanup
    else
        echo "❌ $name failed"
        echo "Expected to find file at: $path"
        echo "Got output:"
        echo "$output"
        echo
        exit 1
    fi
}

echo "===================="
echo " Running icsgen tests"
echo "===================="

# 1️⃣ Test simple event (today 9:00 → today 10:00)
run_test "Basic event" "9:00 Read_paper 10:00" "SUMMARY:Read_paper"

# 2️⃣ Test event with location
run_test "With location" ":tomorrow-8:00 Team_sync Office :tomorrow-9:00" "LOCATION:Office"

# 3️⃣ Test event with description
run_test "With description" "9:00 Coffee_break 9:30 --desc Short_break" "DESCRIPTION:Short_break"

# 4️⃣ Test ISO format
run_test "ISO time" "2025-10-08T10:00 Meeting 2025-10-08T11:00" "SUMMARY:Meeting"
run_test "ISO time" "2025-10-08T10:00 Meeting 2025-10-08T11:00" "DTSTART:20251008T100000"

# 5️⃣ Test now+15m parsing
run_test "Relative now+15m" "now+15m Quick_task now+45m" "SUMMARY:Quick_task"

# 6️⃣ Test multiple events mode
if [[ ! -f "$FIXTURES_DIR/tasks.txt" ]]; then
    echo "❌ Missing fixture file: $FIXTURES_DIR/tasks.txt"
    echo "Please create it with lines like:"
    echo ":tomorrow-8:00 \"Morning run\" Park :tomorrow-9:00"
    echo "2025-10-07T09:00 \"Team meeting\" Office 2025-10-07T10:00"
    exit 1
fi

run_test "Multi-event file" "-m $FIXTURES_DIR/tasks.txt" "BEGIN:VEVENT"

# 7️⃣ Test default output (temp file)
run_file_creation_test "Default output" "9:00 Test_event 10:00 --no-open"

# 8️⃣ Test -o flag
echo "Running: -o flag"
rm -f my_event.ics # ensure it doesn't exist
$PYTHON $ICSGEN 9:00 Test_event 10:00 -o my_event.ics --no-open > /dev/null
if [[ -f "my_event.ics" ]]; then
    echo "✅ -o flag test passed"
    rm my_event.ics
else
    echo "❌ -o flag test failed"
    exit 1
fi

echo
echo "🎉 All tests passed!"
