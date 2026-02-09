from dataclasses import dataclass
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


@dataclass
class NewsletterData:
    title: str
    intro: str
    blog_links: list[tuple[str, str, str]]  # (title, url, description)


EXCLUDED_DOMAINS = {
    "twitter.com",
    "x.com",
    "facebook.com",
    "linkedin.com",
    "instagram.com",
    "youtube.com",
}

EXCLUDED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}


def is_excluded_domain(url: str) -> bool:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return any(excluded in domain for excluded in EXCLUDED_DOMAINS)


def is_external_link(url: str, newsletter_domain: str) -> bool:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    domain = parsed.netloc.lower()
    if newsletter_domain in domain:
        return False
    path = parsed.path.lower()
    for ext in EXCLUDED_EXTENSIONS:
        if path.endswith(ext):
            return False
    return True


def fetch_newsletter(url: str) -> NewsletterData:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return parse_newsletter(soup, url)


def parse_newsletter(soup: BeautifulSoup, url: str) -> NewsletterData:
    newsletter_domain = urlparse(url).netloc
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Newsletter"
    title = title.split(" - ")[0].strip()

    intro = ""
    post_body = soup.find("div", class_="body")
    if post_body:
        first_p = post_body.find("p")
        if first_p:
            assert type(first_p) is not int, "the type of first p is int this should not happen"
            intro = first_p.get_text(strip=True)

    blog_links: list[tuple[str, str, str]] = []
    seen_urls: set[str] = set()

    if post_body:
        for p_tag in post_body.find_all("p"):
            for a_tag in p_tag.find_all("a", href=True):
                href = a_tag["href"]
                if not is_external_link(href, newsletter_domain):
                    continue
                if href in seen_urls:
                    continue
                seen_urls.add(href)
                link_text = a_tag.get_text(strip=True)
                if not link_text:
                    continue
                description = p_tag.get_text(strip=True)
                blog_links.append((link_text, href, description))

    return NewsletterData(title=title, intro=intro, blog_links=blog_links)
