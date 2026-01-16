#!/bin/bash

# Snapshot Testing Script for qtaks
# Uses diff to compare current output with fixture
# Prompts to update fixture if output differs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$SCRIPT_DIR/test"
BINARY="$SCRIPT_DIR/qtaks"
FIXTURE_FILE="$TEST_DIR/test.out.fixture"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== qtaks Snapshot Test ===${NC}"
echo "Binary: $BINARY"
echo "Test directory: $TEST_DIR"
echo ""

# Check if binary exists
if [ ! -f "$BINARY" ]; then
    echo -e "${RED}Error: qtaks binary not found at $BINARY${NC}"
    echo "Please build the project first:"
    echo "  jai qtaks.jai -output_path:. -output_executable_name:qtaks"
    exit 1
fi

# Generate current output
echo -e "${YELLOW}Generating current output...${NC}"
OUTPUT=$("$BINARY" -path "$TEST_DIR" 2>&1)

echo ""

# Check if fixture exists
if [ ! -f "$FIXTURE_FILE" ]; then
    echo -e "${YELLOW}No fixture found. Creating first fixture...${NC}"
    echo "$OUTPUT" > "$FIXTURE_FILE"
    echo -e "${GREEN}Fixture created at: $FIXTURE_FILE${NC}"
    echo "Run the test again to verify output."
    exit 0
fi

# Compare outputs using diff
echo -e "${YELLOW}Comparing with fixture...${NC}"
echo ""

if diff -u <(cat "$FIXTURE_FILE") <(echo "$OUTPUT") > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Test passed! Output matches fixture.${NC}"
    exit 0
else
    echo -e "${RED}✗ Test failed! Output differs from fixture.${NC}"
    echo ""
    echo -e "${YELLOW}Diff (showing changes):${NC}"
    echo "---"
    
    diff -u --color=always <(cat "$FIXTURE_FILE") <(echo "$OUTPUT") || true
    
    echo "---"
    echo ""
    read -p "Do you want to update the fixture? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$OUTPUT" > "$FIXTURE_FILE"
        echo -e "${GREEN}✓ Fixture updated at: $FIXTURE_FILE${NC}"
        exit 0
    else
        echo -e "${YELLOW}Fixture not updated. Test failed.${NC}"
        exit 1
    fi
fi
