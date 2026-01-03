#!/bin/bash
# Test script for asciify
# Version: 1.0.0
# Author: Niklas

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASCIIFY="$SCRIPT_DIR/asciify.sh"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

passed=0
failed=0

# Test function
test_asciify() {
    local input="$1"
    local expected="$2"
    local description="$3"
    
    local result=$(echo "$input" | "$ASCIIFY")
    
    if [ "$result" = "$expected" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((passed++))
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Input:    $input"
        echo "  Expected: $expected"
        echo "  Got:      $result"
        ((failed++))
    fi
}

echo "Running asciify tests..."
echo ""

# Test cases
test_asciify "example – to -" "example - to -" "En dash conversion"
test_asciify "em — dash" "em -- dash" "Em dash conversion"
test_asciify "arrow →" "arrow ->" "Right arrow conversion"
test_asciify "arrow ←" "arrow <-" "Left arrow conversion"
test_asciify "double arrow ↔" "double arrow <->" "Bidirectional arrow"
test_asciify $'"smart quotes"' '"smart quotes"' "Smart double quotes"
test_asciify $'\'smart single\'' "'smart single'" "Smart single quotes"
test_asciify "ellipsis…" "ellipsis..." "Ellipsis"
test_asciify "5 × 3" "5 x 3" "Multiplication sign"
test_asciify "10 ÷ 2" "10 / 2" "Division sign"
test_asciify "25°C" "25degC" "Degree symbol"
test_asciify "bullet • point" "bullet * point" "Bullet point"
test_asciify "section § law" "section sec law" "Section symbol"
test_asciify "paragraph ¶ text" "paragraph para text" "Paragraph symbol"

# French/European accented characters
test_asciify "café" "cafe" "French e acute"
test_asciify "très" "tres" "French e grave"
test_asciify "Château" "Chateau" "French e circumflex"
test_asciify "naïve" "naive" "French i diaeresis"
test_asciify "à bientôt" "a bientot" "French a grave and o circumflex"
test_asciify "résumé" "resume" "Multiple accents"
test_asciify "Zürich" "Zurich" "German umlaut"
test_asciify "naïfs" "naifs" "Multiple i and f"
test_asciify "garçon" "garcon" "French c cedilla"
test_asciify "señor" "senor" "Spanish n tilde"
test_asciify "Łódź" "Lodz" "Polish l stroke"
test_asciify "Königsberg" "Konigsberg" "German o umlaut"
test_asciify "français" "francais" "French a cedilla combo"
test_asciify "coeleste" "coeleste" "Latin e ligature replaced"
test_asciify "Ångström" "Angstrom" "Swedish a ring"

echo ""
echo "=============================="
echo -e "Tests passed: ${GREEN}$passed${NC}"
echo -e "Tests failed: ${RED}$failed${NC}"
echo "=============================="

exit $failed
