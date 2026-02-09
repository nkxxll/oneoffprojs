# Reading List Generator - Plan

## Goal
Given a newsletter URL, generate an Obsidian-formatted reading list with categorized blog links.

## Output Format
```markdown
# <newsletter name>

<newsletter introduction>

## <blog one>

<link to blog one>
[[<blog one>]]

- tag1
- tag2
- tag3

## <blog two>
...
```

## Architecture

```
main.py              # CLI entry point
├── newsletter.py    # fetch newsletter, extract blog links
├── extractor.py     # fetch & extract blog text via trafilatura
├── tagger.py        # embedding + tag assignment
└── formatter.py     # generate obsidian markdown output
```

## Pipeline

### 1. Fetch & Parse Newsletter (`newsletter.py`)
- Fetch HTML from newsletter URL using `requests`
- Parse with `BeautifulSoup4`
- Extract newsletter title and introduction text
- Extract external blog links (filter out internal substack links, social media, images, etc.)

### 2. Extract Blog Content (`extractor.py`)
- For each external blog link, fetch the page
- Use `trafilatura` to extract clean article text
- Handle failures gracefully (timeouts, 404s, paywalls)

### 3. Semantic Tagging (`tagger.py`)
- Load a sentence-transformer model (e.g., `all-MiniLM-L6-v2`)
- Define a set of candidate tags (e.g., programming, rust, go, web, ai, databases, security, devops, career, etc.)
- Pre-compute embeddings for candidate tags
- For each blog's extracted text:
  - Generate embedding
  - Compute cosine similarity against all tag embeddings
  - Assign up to 3 tags above similarity threshold (e.g., 0.3)

### 4. Generate Obsidian Markdown (`formatter.py`)
- Format output with newsletter title as H1
- Include newsletter intro
- For each blog: H2 title, link, note placeholder `[[title]]`, and tag list

## Dependencies

```toml
dependencies = [
    "beautifulsoup4>=4.14.3",
    "requests>=2.32.5",
    "trafilatura>=2.0.0",
    "sentence-transformers>=3.0.0",
]
```

## Usage (planned)

```bash
uv run main.py "https://registerspill.thorstenball.com/p/joy-and-curiosity-71"
```
