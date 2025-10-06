import argparse
import logging
import sys
from pathlib import Path

import fitz  # PyMuPDF

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)  # Set minimum level to INFO

# Create a handler that writes to stderr
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)

# Optional: add a simple formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(handler)


def extract_annotations(pdf_path: Path) -> str:
    """Extract all text annotations and notes from a PDF into Markdown."""
    doc = fitz.open(pdf_path)
    md_output = []

    for page_number, page in enumerate(doc.pages(), start=1):
        current = {"page": page_number, "annotations": []}
        annots = page.annots()
        if not annots:
            continue

        for annot in annots:
            sub_type_num, sub_type_text = annot.type
            info = annot.info
            note = info.get("content", "").strip() if info else ""
            text = ""

            logger.info(f"This is the type num: {sub_type_num}; text: {sub_type_text}")
            # Extract highlighted / underlined text
            if sub_type_text in ("Highlight", "Underline", "Squiggly"):
                quads = annot.vertices
                logger.info(f"this is the quad: {quads}")
                if quads:
                    logger.info("we found quads")
                    # Group vertices into 4s (each quad)
                    for i in range(0, len(quads), 4):
                        rect = fitz.Quad(quads[i : i + 4]).rect
                        text += page.get_text("text", clip=rect).strip() + " "
                    text = text.strip()

            # For text notes (sticky notes), there's no highlighted region
            elif sub_type_text == "Text":
                note = note or None
                text = None

            if text or note:
                if text:
                    current["annotations"].append(
                        f"**Text ({sub_type_text}):** {text}\n"
                    )
                if note:
                    current["annotations"].append(
                        f"**Note ({sub_type_text}):** {note}\n"
                    )
                current["annotations"].append("")  # blank line between annotations

        # only add annotation if there is something on that page
        if len(current["annotations"]) > 0:
            md_output.append(f"## Page {current['page']}\n")
            for a in current["annotations"]:
                md_output.append(a)

    return "\n".join(md_output)


def main():
    parser = argparse.ArgumentParser(
        description="Extract PDF annotations into Markdown."
    )
    parser.add_argument("pdf_path", type=Path, help="Path to annotated PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output Markdown file path", default=None
    )
    args = parser.parse_args()

    md_content = extract_annotations(args.pdf_path)

    if not md_content.strip():
        print("No annotations found.")
        return

    if args.output:
        args.output.write_text(md_content, encoding="utf-8")
        print(f"✅ Extracted annotations saved to {args.output}")
    else:
        print(md_content)


if __name__ == "__main__":
    logger.info("Program started...")
    main()
    logger.info("Program finished!")
