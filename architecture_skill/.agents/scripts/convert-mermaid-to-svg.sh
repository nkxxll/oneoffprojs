#!/bin/bash
# convert-mermaid-to-svg.sh
# Converts Mermaid code blocks in markdown files to SVG images

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if mmdc is available
check_mmdc() {
    if command -v mmdc &> /dev/null; then
        MMDC_CMD="mmdc"
        return 0
    else
        echo -e "${RED}Error: mermaid-cli (mmdc) is not installed.${NC}"
        echo "Install it with: npm install -g @mermaid-js/mermaid-cli"
        exit 1
    fi
}

# Print usage
usage() {
    echo "Usage: $0 [DIRECTORY]"
    echo ""
    echo "Converts Mermaid code blocks in markdown files to SVG images."
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY    Directory containing markdown files (default: docs/architecture)"
    echo ""
    echo "The script will:"
    echo "  1. Find all .md files (excluding .template.md)"
    echo "  2. Rename each to .template.md"
    echo "  3. Process with mmdc to convert Mermaid blocks to SVG"
    echo "  4. Save the result back to the original .md filename"
    echo ""
    echo "Prerequisites:"
    echo "  npm install -g @mermaid-js/mermaid-cli"
}

# Main function
main() {
    # Handle help flag
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
        exit 0
    fi

    ARCH_DIR="${1:-docs/architecture}"

    # Check if directory exists
    if [[ ! -d "$ARCH_DIR" ]]; then
        echo -e "${RED}Error: Directory '$ARCH_DIR' does not exist.${NC}"
        exit 1
    fi

    # Check for mmdc
    check_mmdc

    echo -e "${GREEN}Converting Mermaid diagrams in: $ARCH_DIR${NC}"
    echo "Using: $MMDC_CMD"
    echo ""

    # Count files
    file_count=0
    
    # Find all markdown files (excluding .template.md)
    while IFS= read -r -d '' mdfile; do
        # Skip if no files found
        [[ -z "$mdfile" ]] && continue
        
        template="${mdfile%.md}.template.md"
        
        echo -e "${YELLOW}Processing: $mdfile${NC}"
        
        # Rename to template
        mv "$mdfile" "$template"
        
        # Convert with mmdc
        # mmdc processes markdown, finds mermaid blocks, renders to SVG,
        # and replaces code blocks with image references
        if $MMDC_CMD -i "$template" -o "$mdfile" 2>/dev/null; then
            echo -e "  ${GREEN}✓ Converted successfully${NC}"
            ((file_count++))
        else
            echo -e "  ${RED}✗ Conversion failed, restoring original${NC}"
            mv "$template" "$mdfile"
        fi
        
    done < <(find "$ARCH_DIR" -name "*.md" ! -name "*.template.md" -print0)

    echo ""
    if [[ $file_count -gt 0 ]]; then
        echo -e "${GREEN}Done! Converted $file_count file(s).${NC}"
        echo "Original files preserved as .template.md"
    else
        echo -e "${YELLOW}No markdown files found to convert.${NC}"
    fi
}

main "$@"
