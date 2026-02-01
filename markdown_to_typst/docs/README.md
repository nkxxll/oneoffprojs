---
title: "Markdown to PDF Converter"
author: "Documentation"
date: "2026-02-01"
---

# Overview

This script converts Markdown files to PDF using Pandoc with Typst as the typesetting engine. It provides a clean, professional output with customizable templates.

# Requirements

- [Pandoc](https://pandoc.org/) (version 3.0+)
- [Typst](https://typst.app/) (installed and available in PATH)

# Usage

```bash
./convert.sh input.md [output.pdf]
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `input.md` | Path to the Markdown source file | Yes |
| `output.pdf` | Path for the generated PDF (defaults to input name with `.pdf` extension) | No |

## Examples

Convert a single file:

```bash
./convert.sh docs/README.md
```

Specify custom output path:

```bash
./convert.sh docs/README.md output/documentation.pdf
```

# How It Works

1. **Input Validation**: The script checks that an input file is provided
2. **Template Setup**: Creates the `templates/` directory and default template if they don't exist
3. **Conversion Pipeline**: 
   - Pandoc reads the Markdown file
   - Converts to Typst format using the template
   - Typst compiles the result to PDF

# Template System

The script uses a Typst template located at `templates/template.typ`. On first run, a default template is created with:

- **Page Layout**: A4 with 25mm horizontal and 30mm vertical margins
- **Typography**: Linux Libertine font at 11pt, justified paragraphs
- **Headings**: Numbered sections (1.1, 1.2, etc.)
- **Title Block**: Centered title, author, and date from YAML frontmatter

## Customizing the Template

Edit `templates/template.typ` to customize:

- Fonts and text sizes
- Page margins and numbering
- Header/footer content
- Color schemes

# YAML Frontmatter

Add metadata to your Markdown files:

```yaml
---
title: "Your Document Title"
author: "Author Name"
date: "2026-02-01"
---
```

This metadata is passed to the template and rendered in the title block.
