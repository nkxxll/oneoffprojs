# Research Agent Implementation Plan (Ollama + Qwen3:14b)

## Goals
- Build a Python research agent that uses locally hosted Ollama models (qwen3:14b) on an old machine.
- Support subagents that can gather information from documentation and other sources.
- Persist all research artifacts as Markdown files.

## Assumptions
- The "old machine" hosts both the Ollama server and the research agent runtime.
- The old machine is reachable for task submission (e.g., via SSH or an HTTP job API).
- Model `qwen3:14b` is already pulled and available on that Ollama instance.
- The agent will run on that old machine and gather up the research in a specific directory named after the research topic.
- Documentation sources include local folders, local Markdown/HTML/PDF files, and web URLs accessible from the old machine.

## Architecture Overview
- **Remote Runtime**: Agent runs on the old machine as a long-lived service or job runner.
- **Core Orchestrator**: Coordinates tasks, assigns subagents, aggregates outputs.
- **Subagents**: Independent workers with scoped responsibilities (e.g., docs crawl, web search, summarization).
- **Retriever Layer**: Fetches and chunks data from sources (local files, URLs).
- **LLM Client**: Calls Ollama’s HTTP API with `qwen3:14b` (local to old machine).
- **Storage Layer**: Writes research outputs and intermediate notes to Markdown files on the old machine.
- **Configuration**: Single config file (TOML) for endpoints, model, and paths.
  - Include `run_mode` (service vs. one-shot) and `job_queue` settings if needed.

## Implementation Steps
1. **Define Project Structure**
   - `research_agent/` package with modules: `orchestrator.py`, `subagents.py`, `retrieval.py`, `ollama_client.py`, `storage.py`, `config.py`.
   - `docs/` for user-facing docs.
   - `research/` for output Markdown files.
   - `runner/` or `service/` for remote job handling (SSH-triggered CLI or HTTP API).

2. **Add Configuration System**
   - Use a `config.toml` (or `config.yaml`) for:
     - `ollama_base_url`
     - `ollama_model`
     - `output_dir`
     - `sources` (paths and URLs)
   - Provide defaults and validation with a small schema.

3. **Implement Ollama Client**
   - Minimal HTTP client for Ollama `/api/chat`.
   - Support system/user messages, temperature, max tokens, and streaming.
   - Provide retries and timeouts.

4. **Implement Retrieval Layer**
   - Local file loader (Markdown, text, HTML, PDF).
   - URL fetcher with caching to disk.
   - Chunking (by tokens or paragraph) and metadata tagging.
   - Optional embedding index for faster retrieval (if required later).

5. **Implement Subagent Framework**
   - Base `SubAgent` class with `run(task, context)`.
   - Standard subagents:
     - `DocsAgent`: reads and summarizes documentation.
     - `WebAgent`: fetches URLs and extracts relevant content.
     - `SynthesisAgent`: consolidates into final notes.
   - The orchestrator spawns subagents based on task type.

6. **Implement Orchestrator**
   - Accepts a user query and routes to subagents.
   - Maintains a task queue.
   - Aggregates partial outputs and emits final report.
   - Writes each subagent’s output to Markdown with timestamped filenames.

7. **Markdown Storage**
   - Each run creates a folder with:
     - `summary.md`
     - `sources.md`
     - `subagent_<name>.md`
   - Include metadata block at top with date, model, and source list.

8. **Remote Execution Interface**
   - **Option A (simpler)**: SSH-triggered CLI on the old machine:
     - `ssh <old-machine> "python -m research_agent 'query' --config config.toml"`
   - **Option B (robust)**: Lightweight HTTP API on the old machine:
     - POST `/jobs` with query/config, return a job id.
     - GET `/jobs/<id>` for status and output paths.

9. **Testing & Validation**
   - Unit tests for config loading, Ollama client, retrieval, and storage.
   - Integration test with a local Ollama endpoint.

## Milestones
- **M1**: Remote execution path (SSH CLI or HTTP API), Ollama client, and Markdown storage.
- **M2**: Retrieval layer (local files + URLs).
- **M3**: Subagent framework and orchestrator.
- **M4**: Polishing, tests, and documentation.

## Decisions
- Web sources are mandatory. Research tasks will include documentation and GitHub repositories, so the WebAgent is required.
- Citations are a nice-to-have, not a must-have. Implementable but optional in early versions.
- No embeddings/NLP tools for now. Keep the architecture modular so retrieval augmentation can be added later.
