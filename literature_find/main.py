import argparse
from pathlib import Path

import pypdf


def search_pdf(pdf_path: Path, search_terms: set[str]) -> dict[str, list[int]]:
    """Search for terms in a PDF and return matches with page numbers."""
    matches: dict[str, list[int]] = {term: [] for term in search_terms}

    try:
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text().lower()
                for term in search_terms:
                    if term.lower() in text:
                        matches[term].append(page_num)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return matches


def search_directory(directory: Path, search_terms: set[str]) -> None:
    """Search all PDFs in a directory for the given terms."""
    pdf_files = list(directory.rglob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return

    print(f"Searching {len(pdf_files)} PDF file(s) for: {', '.join(search_terms)}\n")

    for pdf_path in pdf_files:
        matches = search_pdf(pdf_path, search_terms)
        found_terms = {term: pages for term, pages in matches.items() if pages}

        if found_terms:
            print(f"📄 {pdf_path.relative_to(directory)}")
            for term, pages in found_terms.items():
                print(f"   '{term}' found on page(s): {', '.join(map(str, pages))}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Search for words in PDF files")
    parser.add_argument("directory", type=Path, help="Directory to search")
    parser.add_argument("words", nargs="+", help="Word(s) to search for")
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"Error: {args.directory} is not a valid directory")
        return 1

    search_directory(args.directory, set(args.words))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
