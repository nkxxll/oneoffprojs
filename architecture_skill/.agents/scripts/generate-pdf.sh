#!/bin/bash

# Combines architecture documentation markdown files into a single PDF
# Usage: ./generate-pdf.sh <docs-directory> [output.pdf]
# Example: ./generate-pdf.sh docs/architecture architecture-documentation.pdf

set -e

DOCS_DIR="${1:?Usage: $0 <docs-directory> [output.pdf]}"
OUTPUT="${2:-$DOCS_DIR/architecture-documentation.pdf}"
COMBINED="$DOCS_DIR/architecture-combined.md"
SCRIPT_DIR="$(dirname "$0")"
TEMPLATE_DIR="$SCRIPT_DIR/templates"
TEMPLATE="$TEMPLATE_DIR/typst-template.typ"

# Check for pandoc
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is required but not installed."
    echo "Install with: brew install pandoc"
    exit 1
fi

# Check for typst
if ! command -v typst &> /dev/null; then
    echo "Error: typst is required but not installed."
    echo "Install with: brew install typst"
    exit 1
fi

# Create template directory if needed
mkdir -p "$TEMPLATE_DIR"

# Create Typst template if it doesn't exist
if [ ! -f "$TEMPLATE" ]; then
    cat > "$TEMPLATE" << 'EOF'
// Define horizontalrule for Pandoc's Typst output
#let horizontalrule = line(length: 100%, stroke: 0.5pt + luma(180))

#let project(title: "", authors: (), date: none, body) = {
  set document(author: authors, title: title)
  set page(
    margin: (left: 25mm, right: 25mm, top: 25mm, bottom: 25mm),
    numbering: "1 / 1",
    number-align: center,
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: luma(100))
        #title
        #h(1fr)
        #if date != none { date }
        #line(length: 100%, stroke: 0.5pt + luma(180))
      ]
    },
  )
  set text(font: "Libertinus Serif", lang: "en", size: 10.5pt)
  set heading(numbering: "1.1")
  
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(1em)
    block(text(weight: 700, 1.2em, it))
    v(0.5em)
  }
  
  show heading.where(level: 2): it => {
    v(0.8em)
    block(text(weight: 600, 1.1em, it))
    v(0.3em)
  }
  
  show raw.where(block: true): it => {
    set text(size: 9pt)
    block(
      fill: luma(245),
      stroke: 0.5pt + luma(200),
      inset: 10pt,
      radius: 3pt,
      width: 100%,
      it
    )
  }
  
  show raw.where(block: false): it => {
    box(
      fill: luma(240),
      inset: (x: 3pt, y: 0pt),
      outset: (y: 3pt),
      radius: 2pt,
      text(size: 9pt, it)
    )
  }
  
  // Title block
  align(center)[
    #v(2em)
    #block(text(weight: 700, 1.75em, title))
    #v(1em, weak: true)
    #if authors != () and authors.len() > 0 {
      let author-text = if type(authors) == str { authors } else { authors.join(", ") }
      text(0.95em, author-text)
      v(0.5em)
    }
    #if date != none {
      text(0.9em, style: "italic", date)
    }
    #v(3em, weak: true)
  ]
  
  // Table of contents
  outline(
    title: [Contents],
    indent: 1.5em,
    depth: 3,
  )
  pagebreak()

  // Main body
  set par(justify: true, leading: 0.65em)
  body
}

#show: project.with(
  title: "$title$",
  authors: ($for(author)$"$author$"$sep$, $endfor$),
  date: "$date$",
)

$body$
EOF
    echo "Created Typst template at $TEMPLATE"
fi

# Find and combine markdown files in correct order
echo "Combining documentation files..."

# Start with empty combined file
> "$COMBINED"

# Add title metadata
cat >> "$COMBINED" << EOF
---
title: "Architecture Documentation"
date: "$(date +%Y-%m-%d)"
---

EOF

# Function to strip YAML frontmatter from a file
strip_frontmatter() {
    awk '
        BEGIN { in_frontmatter = 0; frontmatter_count = 0 }
        /^---[[:space:]]*$/ {
            frontmatter_count++
            if (frontmatter_count <= 2) {
                in_frontmatter = !in_frontmatter
                next
            }
        }
        !in_frontmatter { print }
    ' "$1"
}

# Add top-level docs in order (use .md files, not .template.md)
for f in "$DOCS_DIR"/0*.md; do
    if [[ -f "$f" && ! "$f" == *.template.md && ! "$f" == *-combined.md ]]; then
        echo "  Adding: $(basename "$f")"
        strip_frontmatter "$f" >> "$COMBINED"
        echo -e "\n\n" >> "$COMBINED"
    fi
done

# Add module docs if they exist
if [ -d "$DOCS_DIR/modules" ]; then
    for f in "$DOCS_DIR/modules"/*.md; do
        if [[ -f "$f" && ! "$f" == *.template.md ]]; then
            echo "  Adding: modules/$(basename "$f")"
            strip_frontmatter "$f" >> "$COMBINED"
            echo -e "\n\n" >> "$COMBINED"
        fi
    done
fi

echo "Converting to PDF..."

# Convert using pandoc + typst
pandoc "$COMBINED" \
    --to=typst \
    --template="$TEMPLATE" \
    --pdf-engine=typst \
    --resource-path="$DOCS_DIR:$DOCS_DIR/modules" \
    -o "$OUTPUT"

echo "Generated: $OUTPUT"
