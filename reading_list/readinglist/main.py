import argparse
import sys

from readinglist.extractor import extract_all_blogs
from readinglist.formatter import format_obsidian_markdown
from readinglist.newsletter import fetch_newsletter
from readinglist.tagger import Tagger, tag_blogs


def log(message: str) -> None:
    print(message, file=sys.stderr)


# https://registerspill.thorstenball.com/p/joy-and-curiosity-71
JOY_AND_CURIOSITY_URL = "https://registerspill.thorstenball.com/p/joy-and-curiosity-{}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate Obsidian reading list from newsletter"
    )
    parser.add_argument(
        "issue",
        nargs="?",
        type=str,
        help="Issue number for Joy and Curiosity newsletter",
    )
    parser.add_argument("--url", help="Custom newsletter URL (overrides issue number)")
    args = parser.parse_args()

    if args.url:
        url = args.url
    elif args.issue:
        url = JOY_AND_CURIOSITY_URL.format(args.issue)
    else:
        parser.error("Either issue number or --url is required")
    log(f"Fetching newsletter: {url}")

    newsletter = fetch_newsletter(url)
    log(f"Title: {newsletter.title}")
    log(f"Found {len(newsletter.blog_links)} external blog links")

    blog_contents = extract_all_blogs(newsletter.blog_links)

    successful_blogs = [
        (b.url, b.title, b.text, b.description)
        for b in blog_contents
        if b.text is not None
    ]
    log(f"\nSuccessfully extracted {len(successful_blogs)} blogs")

    if not successful_blogs:
        log("No blog content to tag. Exiting.")
        exit(1)

    tagger = Tagger()
    tagged_blogs = tag_blogs(successful_blogs, tagger)

    output = format_obsidian_markdown(newsletter.title, newsletter.intro, tagged_blogs)
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
