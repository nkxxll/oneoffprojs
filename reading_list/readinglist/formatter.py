from readinglist.tagger import TaggedBlog

# Character mappings from non-ASCII to ASCII equivalents (using hex escapes)
ASCII_REPLACEMENTS = {
    "\u2013": "-", "\u2014": "--", "\u2212": "-",  # en-dash, em-dash, minus
    "\u2192": "->", "\u2190": "<-", "\u2194": "<->",  # arrows
    "\u201f": '"', "\u201b": "'", "\uff02": '"',  # quotes
    "\u2018": "'", "\u2019": "'", "\u201a": "'",  # single quotes
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u2e42": '"',  # double quotes
    "\u2026": "...", "\u2022": "*", "\u00b0": "deg",  # ellipsis, bullet, degree
    "\u00d7": "x", "\u00f7": "/", "\u00a7": "sec", "\u00b6": "para",  # symbols
    "\u2020": "*", "\u2021": "**",  # daggers
    "\u00c9": "E", "\u00e9": "e", "\u00c8": "E", "\u00e8": "e",  # E accents
    "\u00ca": "E", "\u00ea": "e", "\u00cb": "E", "\u00eb": "e",
    "\u00c1": "A", "\u00e1": "a", "\u00c0": "A", "\u00e0": "a",  # A accents
    "\u00c2": "A", "\u00e2": "a", "\u00c4": "A", "\u00e4": "a",
    "\u00c3": "A", "\u00e3": "a", "\u00c5": "A", "\u00e5": "a",
    "\u00da": "U", "\u00fa": "u", "\u00d9": "U", "\u00f9": "u",  # U accents
    "\u00db": "U", "\u00fb": "u", "\u00dc": "U", "\u00fc": "u",
    "\u00d3": "O", "\u00f3": "o", "\u00d2": "O", "\u00f2": "o",  # O accents
    "\u00d4": "O", "\u00f4": "o", "\u00d6": "O", "\u00f6": "o",
    "\u00d5": "O", "\u00f5": "o", "\u00d8": "O", "\u00f8": "o",
    "\u00cd": "I", "\u00ed": "i", "\u00cc": "I", "\u00ec": "i",  # I accents
    "\u00ce": "I", "\u00ee": "i", "\u00cf": "I", "\u00ef": "i",
    "\u00e7": "c", "\u00c7": "C", "\u010d": "c", "\u010c": "C",  # c cedilla, caron
    "\u00f1": "n", "\u00d1": "N", "\u0161": "s", "\u0160": "S",  # n tilde, s caron
    "\u017e": "z", "\u017d": "Z", "\u017a": "z", "\u0179": "Z",  # z caron, acute
    "\u0111": "d", "\u0110": "D", "\u0142": "l", "\u0141": "L",  # d stroke, l stroke
    "\u00e6": "ae", "\u00c6": "AE", "\u0153": "oe", "\u0152": "OE",  # ligatures
    "\u00df": "ss", "\u1e9e": "SS",  # eszett
}


def asciify(text: str) -> str:
    """Convert non-ASCII characters to ASCII equivalents."""
    for char, replacement in ASCII_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text


def format_obsidian_markdown(
    newsletter_title: str,
    newsletter_intro: str,
    tagged_blogs: list[TaggedBlog],
) -> str:
    lines = [f"# {newsletter_title}", ""]

    if newsletter_intro:
        lines.append(newsletter_intro)
        lines.append("")

    for blog in tagged_blogs:
        lines.append(f"## {blog.title}")
        lines.append("")
        if blog.description:
            lines.append(f"> {blog.description}")
            lines.append("")
        lines.append(blog.url)
        lines.append(f"[[{blog.title}]]")
        lines.append("")
        for tag in blog.tags:
            lines.append(f"- {tag}")
        lines.append("")

    return asciify("\n".join(lines))
