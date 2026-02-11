from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import AgentConfig
from .ollama_client import OllamaClient
import logging

from .retrieval import extract_urls, gather_documents
from .storage import Storage
from .subagents import DocsAgent, WebAgent, SynthesisAgent, TaskContext, SourceGatheringAgent


class Orchestrator:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.ollama = OllamaClient(
            base_url=cfg.ollama_base_url,
            model=cfg.ollama_model,
            timeout_sec=cfg.request_timeout_sec,
        )

    def run(self, query: str, run_name: str | None = None) -> Path:
        log = logging.getLogger(__name__)
        if run_name is None:
            stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            safe = "_".join(query.strip().split())[:48] or "research"
            run_name = f"{safe}_{stamp}"

        log.info("Run name: %s", run_name)
        storage = Storage.create(self.cfg.output_dir, run_name)

        query_urls = extract_urls(query)
        base_sources = _merge_sources(self.cfg.sources, query_urls)
        log.info("Base sources: %d", len(base_sources))

        docs = gather_documents(
            sources=base_sources,
            cache_dir=self.cfg.output_dir / ".cache",
            timeout_sec=self.cfg.request_timeout_sec,
            max_chars=self.cfg.max_chunk_chars,
            github_token=self.cfg.github_token,
            skip_github=self.cfg.skip_github,
        )
        log.info("Initial documents: %d", len(docs))

        ctx = TaskContext(
            query=query,
            docs=docs,
            model=self.cfg.ollama_model,
            storage=storage,
            ollama=self.ollama,
            max_context_chunks=self.cfg.max_context_chunks,
        )

        source_agent = SourceGatheringAgent()
        source_notes, additional_sources = source_agent.gather_sources(
            ctx, limit=self.cfg.max_additional_sources
        )
        storage.write_markdown(
            "subagent_source_gathering.md",
            source_notes,
            metadata={
                "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "model": self.cfg.ollama_model,
                "agent": source_agent.name,
            },
        )

        merged_sources = _merge_sources(base_sources, additional_sources)
        log.info("Merged sources: %d", len(merged_sources))
        docs = gather_documents(
            sources=merged_sources,
            cache_dir=self.cfg.output_dir / ".cache",
            timeout_sec=self.cfg.request_timeout_sec,
            max_chars=self.cfg.max_chunk_chars,
            github_token=self.cfg.github_token,
            skip_github=self.cfg.skip_github,
        )
        ctx.docs = docs
        log.info("Total documents after merge: %d", len(docs))

        storage.write_sources(merged_sources, self.cfg.ollama_model)

        subagents = [DocsAgent(), WebAgent(), SynthesisAgent()]
        for agent in subagents:
            output = agent.run(ctx)
            storage.write_markdown(
                f"subagent_{agent.name}.md",
                output,
                metadata={
                    "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                    "model": self.cfg.ollama_model,
                    "agent": agent.name,
                },
            )

        # The synthesis output is the summary
        synthesis_path = storage.run_dir / "subagent_synthesis.md"
        summary_content = synthesis_path.read_text(errors="ignore")
        storage.write_markdown(
            "summary.md",
            summary_content,
            metadata={
                "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "model": self.cfg.ollama_model,
            },
        )

        return storage.run_dir


def _merge_sources(existing: list[str], new: list[str]) -> list[str]:
    merged: list[str] = []
    seen = set()
    for src in existing + new:
        if not src or src in seen:
            continue
        seen.add(src)
        merged.append(src)
    return merged
