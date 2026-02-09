from dataclasses import dataclass
import sys

CANDIDATE_TAGS = [
    "programming",
    "rust",
    "go",
    "python",
    "javascript",
    "typescript",
    "web",
    "ai",
    "machine-learning",
    "databases",
    "security",
    "devops",
    "career",
    "software-engineering",
    "systems",
    "performance",
    "testing",
    "architecture",
    "open-source",
    "tools",
    "linux",
    "networking",
    "distributed-systems",
    "compilers",
    "algorithms",
]

SIMILARITY_THRESHOLD = 0.3
MAX_TAGS = 3


@dataclass
class TaggedBlog:
    url: str
    title: str
    tags: list[str]
    description: str = ""


class Tagger:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        import numpy as np
        from sentence_transformers import SentenceTransformer

        print(f"Loading model: {model_name}", file=sys.stderr)
        self.model = SentenceTransformer(model_name)
        self.np = np
        self.tags = CANDIDATE_TAGS
        self.tag_embeddings = self.model.encode(self.tags, convert_to_numpy=True)

    def assign_tags(self, text: str) -> list[str]:
        text_embedding = self.model.encode([text], convert_to_numpy=True)[0]
        similarities = self.np.dot(self.tag_embeddings, text_embedding) / (
            self.np.linalg.norm(self.tag_embeddings, axis=1) * self.np.linalg.norm(text_embedding)
        )
        tag_scores = list(zip(self.tags, similarities))
        tag_scores.sort(key=lambda x: x[1], reverse=True)
        selected = [tag for tag, score in tag_scores if score >= SIMILARITY_THRESHOLD][:MAX_TAGS]
        return selected if selected else [tag_scores[0][0]]


def tag_blogs(blogs: list[tuple[str, str, str, str]], tagger: Tagger) -> list[TaggedBlog]:
    results = []
    for url, title, text, description in blogs:
        tags = tagger.assign_tags(text)
        results.append(TaggedBlog(url=url, title=title, tags=tags, description=description))
        print(f"Tagged '{title}': {tags}", file=sys.stderr)
    return results
