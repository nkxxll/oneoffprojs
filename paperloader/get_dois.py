#!/usr/bin/env python3
"""
Fetch DOIs for paper titles using CrossRef API.
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Optional


def get_doi(title: str, timeout: int = 5) -> Optional[str]:
    """
    Query CrossRef API to find DOI for a given paper title.

    Args:
        title: Paper title to search for
        timeout: Request timeout in seconds

    Returns:
        DOI string if found, None otherwise
    """
    try:
        # CrossRef API endpoint
        url = "https://api.crossref.org/v1/works"
        params = {"query": title, "rows": 1, "select": "DOI,title"}

        full_url = f"{url}?{urllib.parse.urlencode(params)}"

        # Add User-Agent header as requested by CrossRef
        req = urllib.request.Request(
            full_url, headers={"User-Agent": "paperloader/1.0"}
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read())

        if data.get("message", {}).get("items"):
            item = data["message"]["items"][0]
            # Check if the title matches reasonably well
            result_title = item.get("title", [""])[0].lower()
            query_title = title.lower()

            # Simple matching: check if most words overlap
            query_words = set(query_title.split())
            result_words = set(result_title.split())
            overlap = len(query_words & result_words) / max(len(query_words), 1)

            if overlap > 0.5:  # At least 50% word overlap
                return item.get("DOI")

    except Exception as e:
        print(f"Error fetching DOI for '{title}': {e}", file=sys.stderr)

    return None


def main():
    if len(sys.argv) == 2:
        papers = sys.argv[1]
    else:
        papers = "papers.json"

    # Load titles from papers.json
    with open(papers) as f:
        titles = json.load(f)

    dois = []
    total = len(titles)

    print(f"Fetching DOIs for {total} papers...", file=sys.stderr)

    for i, title in enumerate(titles, 1):
        print(f"[{i}/{total}] {title[:60]}...", file=sys.stderr)
        doi = get_doi(title)

        if doi:
            dois.append({"title": title, "doi": doi})
            print(f"  Found: {doi}", file=sys.stderr)
        else:
            dois.append({"title": title, "doi": None})
            print(f"  Not found", file=sys.stderr)

        # Be nice to the API - small delay between requests
        time.sleep(0.5)

    # Output results as JSON
    output = {"total": total, "found": sum(1 for d in dois if d["doi"]), "papers": dois}

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
