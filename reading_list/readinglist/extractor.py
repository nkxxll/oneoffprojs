import sys
from dataclasses import dataclass

import trafilatura

from readinglist.newsletter import is_excluded_domain


@dataclass
class BlogContent:
    url: str
    title: str
    text: str | None
    description: str = ""
    error: str | None = None


def extract_blog_content(
    url: str, link_title: str, description: str = ""
) -> BlogContent:
    if is_excluded_domain(url):
        return BlogContent(
            url=url,
            title=link_title,
            text=description,
            description=description,
        )

    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return BlogContent(
                url=url,
                title=link_title,
                text=None,
                description=description,
                error="Failed to fetch",
            )

        text = trafilatura.extract(downloaded)
        if text is None or len(text.strip()) < 50:
            return BlogContent(
                url=url,
                title=link_title,
                text=None,
                description=description,
                error="No content extracted",
            )

        metadata = trafilatura.extract_metadata(downloaded)
        title = metadata.title if metadata and metadata.title else link_title

        return BlogContent(url=url, title=title, text=text, description=description)
    except Exception as e:
        return BlogContent(
            url=url, title=link_title, text=None, description=description, error=str(e)
        )


def extract_all_blogs(blog_links: list[tuple[str, str, str]]) -> list[BlogContent]:
    results = []
    for link_title, url, description in blog_links:
        print(f"Extracting: {url}", file=sys.stderr)
        content = extract_blog_content(url, link_title, description)
        results.append(content)
        if content.error:
            print(f"  Error: {content.error}", file=sys.stderr)
        else:
            print(f"  OK: {len(content.text or '')} chars", file=sys.stderr)
    return results
