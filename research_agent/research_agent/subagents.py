from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import logging

from .ollama_client import OllamaClient
from .retrieval import DocumentChunk, extract_urls, is_url, is_github_repo_url
from .storage import Storage


@dataclass
class TaskContext:
    query: str
    docs: list[DocumentChunk]
    model: str
    storage: Storage
    ollama: OllamaClient
    max_context_chunks: int


class SubAgent:
    name = "base"

    def run(self, ctx: TaskContext) -> str:
        raise NotImplementedError


class DocsAgent(SubAgent):
    name = "docs"

    def run(self, ctx: TaskContext) -> str:
        logging.getLogger(__name__).info("DocsAgent: %d chunks", len(ctx.docs))
        doc_chunks = [d for d in ctx.docs if d.kind == "local"]
        return _summarize_chunks(
            ctx,
            doc_chunks,
            prompt_title="Local documentation summary",
        )


class WebAgent(SubAgent):
    name = "web"

    def run(self, ctx: TaskContext) -> str:
        logging.getLogger(__name__).info("WebAgent: %d chunks", len(ctx.docs))
        doc_chunks = [d for d in ctx.docs if d.kind == "web"]
        return _summarize_chunks(
            ctx,
            doc_chunks,
            prompt_title="Web documentation summary",
        )


class SynthesisAgent(SubAgent):
    name = "synthesis"

    def run(self, ctx: TaskContext) -> str:
        logging.getLogger(__name__).info("SynthesisAgent: reading subagent outputs")
        inputs = []
        for name in ("docs", "web"):
            agent_path = ctx.storage.run_dir / f"subagent_{name}.md"
            if agent_path.exists():
                inputs.append(agent_path.read_text(errors="ignore"))

        combined = "\n\n".join(inputs)
        if not combined.strip():
            combined = "No prior subagent notes were found."

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a research synthesis agent. Consolidate findings into a clear,"
                    " structured report with key insights, risks, and next steps."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Research question: {ctx.query}\n\n"
                    "Inputs from subagents:\n"
                    f"{combined}\n\n"
                    "Deliverable: a concise Markdown report with headings, bullets, and clear takeaways."
                ),
            },
        ]
        return ctx.ollama.chat(messages, temperature=0.2, max_tokens=1400)


def _summarize_chunks(
    ctx: TaskContext,
    chunks: list[DocumentChunk],
    prompt_title: str,
) -> str:
    if not chunks:
        return f"No sources found for {prompt_title.lower()}."

    selected = chunks[: ctx.max_context_chunks]
    sources = "\n".join(
        f"- [{chunk.kind}] {chunk.source} ({chunk.chunk_id})" for chunk in selected
    )
    content = "\n\n".join(
        f"Source: {chunk.source}\nChunk: {chunk.chunk_id}\n\n{chunk.content}"
        for chunk in selected
    )
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a research subagent. Produce a focused summary."
                f" Title: {prompt_title}."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Research question: {ctx.query}\n\n"
                f"Available sources:\n{sources}\n\n"
                "Extract the most relevant points, mention any uncertainty, and format as Markdown."
                " If sources are weak or unrelated, say so.\n\n"
                f"Sources content:\n{content}"
            ),
        },
    ]
    return ctx.ollama.chat(messages, temperature=0.3, max_tokens=1200)


class SourceGatheringAgent(SubAgent):
    name = "source_gathering"

    def gather_sources(self, ctx: TaskContext, limit: int) -> tuple[str, list[str]]:
        logging.getLogger(__name__).info("SourceGatheringAgent: scanning %d docs", len(ctx.docs))
        found: list[str] = []
        for chunk in ctx.docs:
            urls = extract_urls(chunk.content)
            for url in urls:
                if is_url(url) or is_github_repo_url(url):
                    found.append(url)

        unique = []
        seen = set()
        for url in found:
            if url in seen:
                continue
            seen.add(url)
            unique.append(url)
            if len(unique) >= limit:
                break

        if unique:
            content = "\n".join(f"- {url}" for url in unique)
        else:
            content = "No additional sources found."
        return content, unique
