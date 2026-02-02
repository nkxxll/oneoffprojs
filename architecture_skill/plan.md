# Architecture Documentation Skill - Implementation Plan

## Overview

Create a Claude Code skill that generates hierarchical architecture documentation (broad → specific) with Mermaid diagrams, then converts those diagrams to SVG files in a second pass.

---

## Skill Structure

```
.agents/skills/documenting-architecture/
├── SKILL.md                    # Main instructions
├── reference/
│   ├── diagram-types.md        # Mermaid diagram templates (C4, flowchart, sequence, etc.)
│   └── documentation-template.md # Output format templates
└── scripts/
    └── convert-mermaid-to-svg.sh  # Converts mermaid code blocks to SVG files
```

---

## Phase 1: Architecture Documentation Generation

### Step 1: Project Discovery
1. Read project structure (directories, key files)
2. Identify entry points, config files, package manifests
3. Detect language/framework stack

### Step 2: Hierarchical Documentation (Broad → Specific)

**Level 1 - System Overview** (`docs/architecture/00-system-overview.md`)
- High-level purpose and goals
- External dependencies and integrations
- System context diagram (C4 Level 1)

**Level 2 - Container/Component View** (`docs/architecture/01-components.md`)
- Major components/modules
- Data stores, APIs, services
- Container diagram (C4 Level 2)
- Component interaction diagram

**Level 3 - Module Deep Dives** (`docs/architecture/modules/<module-name>.md`)
- Per-module documentation
- Key classes/functions
- Sequence diagrams for important flows
- Dependency graphs

**Level 4 - Data Flow & Patterns** (`docs/architecture/02-data-flow.md`)
- Request/response flows
- Data transformation pipelines
- State management patterns

### Step 3: Embed Mermaid Diagrams
Each doc file includes mermaid code blocks:
```markdown
## System Context

```mermaid
C4Context
    title System Context Diagram
    Person(user, "User")
    System(app, "Application")
    System_Ext(ext, "External API")
    Rel(user, app, "Uses")
    Rel(app, ext, "Calls")
`` `
```

---

## Phase 2: Mermaid → SVG Conversion

### Conversion Script (`scripts/convert-mermaid-to-svg.sh`)

**Dependencies:** `@mermaid-js/mermaid-cli` (mmdc)

**Algorithm:**
1. Find all `.md` files in `docs/architecture/`
2. For each file:
  - `mv file.md file.template.md`
  - `mmdc -i file.template.md -o file.md`


**Script outline:**
```bash
#!/bin/bash
# convert-mermaid-to-svg.sh

# Check if mmdc is available
if ! command -v mmdc &> /dev/null && ! npx -y @mermaid-js/mermaid-cli --version &> /dev/null; then
    echo "Error: mermaid-cli (mmdc) is not installed."
    echo "Install it with: npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

ARCH_DIR="${1:-docs/architecture}"

# Find all markdown files (excluding .template.md)
find "$ARCH_DIR" -name "*.md" ! -name "*.template.md" | while read -r mdfile; do
    template="${mdfile%.md}.template.md"
    mv "$mdfile" "$template"
    npx -y @mermaid-js/mermaid-cli -i "$template" -o "$mdfile"
done
```

This leverages mmdc's built-in markdown processing which:
- Detects mermaid code blocks in markdown
- Renders each to SVG (saved alongside the output file)
- Replaces code blocks with image references automatically

---

## SKILL.md Content Outline

```yaml
---
name: documenting-architecture
description: "Generates hierarchical architecture documentation with Mermaid diagrams. Use when asked to document architecture, create system diagrams, or explain codebase structure."
---
```

### Instructions Include:
1. **Workflow**: Discovery → Generate docs (broad→specific) → Convert diagrams
2. **Output structure**: Where files go, naming conventions
3. **Diagram guidelines**: Which diagram types for which level
4. **Conversion command**: How to run the SVG conversion script

---

## Implementation Checklist

- [ ] Create `SKILL.md` with frontmatter and instructions
- [ ] Create `reference/diagram-types.md` with Mermaid templates
- [ ] Create `reference/documentation-template.md` with doc structure
- [ ] Create `scripts/convert-mermaid-to-svg.sh` for conversion
- [ ] Test on a sample project
- [ ] Document prerequisites (mermaid-cli installation)

---

## Prerequisites for Users

```bash
# Install mermaid CLI globally
npm install -g @mermaid-js/mermaid-cli

# Or use npx (no install needed)
npx @mermaid-js/mermaid-cli -i input.mmd -o output.svg
```

---

## Example Workflow

1. User loads skill: "document the architecture of this project"
2. Agent runs Phase 1:
   - Analyzes codebase
   - Creates `docs/architecture/` with markdown files
   - Embeds mermaid diagrams in code blocks
3. User (or agent) runs Phase 2:
   - `./scripts/convert-mermaid-to-svg.sh docs/architecture`
   - Mermaid blocks replaced with SVG image links
4. Result: Complete architecture docs with rendered diagrams
