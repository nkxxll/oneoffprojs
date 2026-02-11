from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import base64
import hashlib
import re
import urllib.parse

import logging

from githubkit import GitHub, TokenAuthStrategy
from pypdf import PdfReader
from trafilatura import extract, fetch_url as trafi_fetch
from urlextract import URLExtract


@dataclass
class DocumentChunk:
    source: str
    chunk_id: str
    content: str
    kind: str


def is_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
        return parsed.scheme in {"http", "https"}
    except Exception:
        return False


def is_github_repo_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
        if parsed.netloc.lower() != "github.com":
            return False
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        return len(parts) >= 2
    except Exception:
        return False


def _parse_github_repo(value: str) -> tuple[str, str, str | None]:
    parsed = urllib.parse.urlparse(value)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    branch: str | None = None
    if len(parts) >= 4 and parts[2] == "tree":
        branch = parts[3]
    return owner, repo, branch


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:12]


def _clean_whitespace(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_urls(text: str) -> list[str]:
    extractor = URLExtract()
    return [url.rstrip(").,]}>\"'") for url in extractor.find_urls(text)]


def chunk_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for para in paragraphs:
        if length + len(para) + 2 > max_chars and current:
            chunks.append("\n\n".join(current))
            current = []
            length = 0
        current.append(para)
        length += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def load_local_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".rst"}:
        return path.read_text(errors="ignore")
    if suffix in {".html", ".htm"}:
        html = path.read_text(errors="ignore")
        extracted = extract(html)
        return extracted or html
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    return path.read_text(errors="ignore")


def fetch_url(url: str, cache_dir: Path, timeout_sec: float) -> str:
    log = logging.getLogger(__name__)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = _hash(url)
    cache_path = cache_dir / f"{cache_key}.txt"
    if cache_path.exists():
        return cache_path.read_text(errors="ignore")

    try:
        downloaded = trafi_fetch(url)
    except Exception as exc:  # pragma: no cover - network failure
        log.warning("Failed to fetch URL: %s (%s)", url, exc)
        downloaded = None
    if downloaded is None:
        text = ""
    else:
        extracted = extract(downloaded)
        text = extracted or downloaded

    text = _clean_whitespace(text)
    cache_path.write_text(text)
    return text


def build_chunks(
    source: str,
    content: str,
    kind: str,
    max_chars: int,
) -> list[DocumentChunk]:
    cleaned = _clean_whitespace(content)
    chunks = chunk_text(cleaned, max_chars)
    return [
        DocumentChunk(source=source, chunk_id=f"{kind}-{idx}", content=chunk, kind=kind)
        for idx, chunk in enumerate(chunks)
    ]


def _allowed_github_path(path: str) -> bool:
    lowered = path.lower()
    skip_prefixes = (
        "node_modules/",
        "vendor/",
        "dist/",
        "build/",
        ".git/",
        ".github/",
    )
    if any(lowered.startswith(prefix) for prefix in skip_prefixes):
        return False
    allowed_ext = {
        ".md",
        ".txt",
        ".rst",
        ".py",
        ".js",
        ".ts",
        ".go",
        ".rs",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
        ".html",
        ".htm",
        ".css",
        ".sh",
        ".bat",
        ".ps1",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".scala",
        ".sql",
    }
    return Path(path).suffix.lower() in allowed_ext


def fetch_github_repo(
    url: str,
    cache_dir: Path,
    timeout_sec: float,
    max_file_bytes: int = 300_000,
    github_token: str | None = None,
) -> list[tuple[str, str]]:
    owner, repo, branch = _parse_github_repo(url)
    if github_token:
        gh = GitHub(auth=TokenAuthStrategy(github_token), timeout=timeout_sec)
    else:
        gh = GitHub(timeout=timeout_sec)
    if branch is None:
        repo_meta = gh.rest.repos.get(owner=owner, repo=repo).parsed_data
        branch = repo_meta.default_branch or "main"

    tree = gh.rest.git.get_tree(owner=owner, repo=repo, tree_sha=branch, recursive="1").parsed_data
    entries = tree.tree or []

    cache_dir.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str]] = []
    for entry in entries:
        if entry.type != "blob":
            continue
        path = entry.path or ""
        if not path or not _allowed_github_path(path):
            continue
        size = entry.size
        if isinstance(size, int) and size > max_file_bytes:
            continue
        source_id = f"{url}::{path}"
        cache_key = _hash(source_id)
        cache_path = cache_dir / f"github_{cache_key}.txt"
        if cache_path.exists():
            content = cache_path.read_text(errors="ignore")
        else:
            content_resp = gh.rest.repos.get_content(owner=owner, repo=repo, path=path, ref=branch).parsed_data
            if not hasattr(content_resp, "content") or content_resp.content is None:
                continue
            decoded = base64.b64decode(content_resp.content)
            content = decoded.decode("utf-8", errors="ignore")
            content = _clean_whitespace(content)
            cache_path.write_text(content)
        results.append((source_id, content))
    return results


def fetch_github_readme(
    url: str,
    cache_dir: Path,
    timeout_sec: float,
) -> list[tuple[str, str]]:
    owner, repo, branch = _parse_github_repo(url)
    branches = [b for b in [branch, "main", "master"] if b]
    readme_names = ["README.md", "Readme.md", "readme.md", "README"]

    cache_dir.mkdir(parents=True, exist_ok=True)
    for br in branches:
        for name in readme_names:
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{br}/{name}"
            cache_key = _hash(raw_url)
            cache_path = cache_dir / f"github_readme_{cache_key}.txt"
            if cache_path.exists():
                content = cache_path.read_text(errors="ignore")
            else:
                try:
                    downloaded = trafi_fetch(raw_url)
                except Exception as exc:  # pragma: no cover - network failure
                    logging.getLogger(__name__).warning(
                        "Failed to fetch GitHub README: %s (%s)", raw_url, exc
                    )
                    downloaded = None
                if downloaded is None:
                    continue
                content = _clean_whitespace(downloaded)
                if not content:
                    continue
                cache_path.write_text(content)
            return [(f"{url}::{name}", content)]
    return []


def gather_documents(
    sources: list[str],
    cache_dir: Path,
    timeout_sec: float,
    max_chars: int,
    github_token: str | None = None,
    skip_github: bool = False,
) -> list[DocumentChunk]:
    log = logging.getLogger(__name__)
    docs: list[DocumentChunk] = []
    for source in sources:
        if is_github_repo_url(source):
            repo_cache = cache_dir / "github"
            if skip_github:
                log.info("Skipping GitHub repo fetch; reading README only: %s", source)
                files = fetch_github_readme(
                    source,
                    cache_dir=repo_cache,
                    timeout_sec=timeout_sec,
                )
            else:
                log.info("Fetching GitHub repo: %s", source)
                files = fetch_github_repo(
                    source,
                    cache_dir=repo_cache,
                    timeout_sec=timeout_sec,
                    github_token=github_token,
                )
            for file_source, content in files:
                docs.extend(build_chunks(file_source, content, "web", max_chars))
        elif is_url(source):
            log.info("Fetching URL: %s", source)
            content = fetch_url(source, cache_dir=cache_dir, timeout_sec=timeout_sec)
            docs.extend(build_chunks(source, content, "web", max_chars))
        else:
            path = Path(source).expanduser().resolve()
            if path.is_dir():
                log.info("Loading local directory: %s", path)
                for child in sorted(path.rglob("*")):
                    if child.is_file():
                        content = load_local_file(child)
                        docs.extend(build_chunks(str(child), content, "local", max_chars))
            elif path.is_file():
                log.info("Loading local file: %s", path)
                content = load_local_file(path)
                docs.extend(build_chunks(str(path), content, "local", max_chars))
    return docs
