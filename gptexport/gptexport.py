"""Export ChatGPT shared conversations to Markdown."""

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone


def fetch_share_html(url: str) -> str:
    share_id = url.rstrip("/").split("/")[-1]
    share_url = f"https://chatgpt.com/share/{share_id}"
    req = urllib.request.Request(
        share_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def parse_turbo_stream(html: str) -> list:
    pattern = r'streamController\.enqueue\("(.+?)"\);'
    matches = re.findall(pattern, html)
    if not matches:
        raise ValueError("Could not find conversation data in page")
    raw = matches[0]
    # The JS string uses \uXXXX escapes for UTF-8 byte sequences.
    # Decode unicode_escape to Latin-1 chars, then re-encode as Latin-1
    # bytes and decode as UTF-8 to get proper characters.
    unescaped = raw.encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
    return json.loads(unescaped)


def deref(val, data: list):
    """Dereference a single turbo-stream value."""
    if isinstance(val, int):
        if val == -5:
            return None
        if 0 <= val < len(data):
            return data[val]
    return val


def resolve_keys(obj: dict, data: list) -> dict:
    """Convert _XX keys to their semantic names by looking up data[XX]."""
    resolved = {}
    for key, value in obj.items():
        if key.startswith("_") and key[1:].isdigit():
            idx = int(key[1:])
            if 0 <= idx < len(data) and isinstance(data[idx], str):
                resolved[data[idx]] = value
            else:
                resolved[key] = value
        else:
            resolved[key] = value
    return resolved


def extract_conversation(data: list) -> tuple[str, float, list[dict]]:
    """Extract title, create_time, and messages from turbo-stream data."""
    title = None
    create_time = None
    for i, item in enumerate(data):
        if item == "title" and i + 1 < len(data):
            candidate = data[i + 1]
            if isinstance(candidate, str) and candidate not in (
                "title",
                "mapping",
            ):
                title = candidate
                break

    for i, item in enumerate(data):
        if item == "create_time" and i + 1 < len(data):
            candidate = data[i + 1]
            if isinstance(candidate, (int, float)) and candidate > 1_000_000_000:
                create_time = candidate
                break

    # Find linear_conversation array
    lin_conv = None
    for i, item in enumerate(data):
        if item == "linear_conversation" and i + 1 < len(data):
            ref = data[i + 1]
            arr = deref(ref, data) if isinstance(ref, int) else ref
            if isinstance(arr, list) and len(arr) > 2:
                lin_conv = arr
                break

    if lin_conv is None:
        raise ValueError("Could not find linear_conversation in data")

    messages = []
    for node_ref in lin_conv:
        node = data[node_ref] if isinstance(node_ref, int) else node_ref
        if not isinstance(node, dict):
            continue

        node_r = resolve_keys(node, data)

        msg_ref = node_r.get("message")
        if msg_ref is None:
            continue
        msg = data[msg_ref] if isinstance(msg_ref, int) else msg_ref
        if not isinstance(msg, dict):
            continue

        msg_r = resolve_keys(msg, data)

        # Extract author role
        author_ref = msg_r.get("author")
        if author_ref is None:
            continue
        author = data[author_ref] if isinstance(author_ref, int) else author_ref
        if not isinstance(author, dict):
            continue
        author_r = resolve_keys(author, data)
        role = deref(author_r.get("role"), data)
        if isinstance(role, int):
            role = deref(role, data)

        if role not in ("user", "assistant"):
            continue

        # Extract content
        content_ref = msg_r.get("content")
        if content_ref is None:
            continue
        content = data[content_ref] if isinstance(content_ref, int) else content_ref
        if not isinstance(content, dict):
            continue
        content_r = resolve_keys(content, data)

        # Check content type
        ctype_ref = content_r.get("content_type")
        if ctype_ref is not None:
            ctype = deref(ctype_ref, data)
            if isinstance(ctype, int):
                ctype = deref(ctype, data)
            if ctype != "text":
                continue

        # Get parts
        parts_ref = content_r.get("parts")
        if parts_ref is None:
            continue
        parts = data[parts_ref] if isinstance(parts_ref, int) else parts_ref
        if not isinstance(parts, list):
            continue

        text_parts = []
        for p in parts:
            pv = data[p] if isinstance(p, int) and 0 <= p < len(data) else p
            if isinstance(pv, str) and pv.strip():
                text_parts.append(pv)

        if text_parts:
            content_text = "\n\n".join(text_parts)
            content_text = re.sub(r"\s*citeturn\d+\w+\d*", "", content_text)
            messages.append({"role": role, "content": content_text})

    return title or "Untitled Conversation", create_time, messages


def format_markdown(
    title: str, create_time: float | None, messages: list[dict], url: str
) -> str:
    lines = []
    lines.append(f"# {title}\n")

    if create_time:
        dt = datetime.fromtimestamp(create_time, tz=timezone.utc)
        lines.append(f"**Date:** {dt.strftime('%Y-%m-%d')}")
    lines.append(f"**Source:** [chatgpt.com]({url})\n")
    lines.append("---\n")

    for msg in messages:
        sender = "You" if msg["role"] == "user" else "ChatGPT"
        lines.append(f"### **{sender}**\n")
        lines.append(msg["content"])
        lines.append("\n---\n")

    return "\n".join(lines).strip() + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: gptexport <share-url> [output.md]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    html = fetch_share_html(url)
    data = parse_turbo_stream(html)
    title, create_time, messages = extract_conversation(data)
    markdown = format_markdown(title, create_time, messages, url)

    if output_path:
        with open(output_path, "w") as f:
            f.write(markdown)
        print(f"Saved to {output_path}", file=sys.stderr)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
