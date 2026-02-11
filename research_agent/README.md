# Research Agent (Ollama)

A Python research agent that runs on your old machine, uses a locally hosted Ollama model (qwen3:14b), and writes all research artifacts to Markdown files.

## Quick Start
1. Edit `config.toml` to point at your sources and Ollama endpoint.
2. Run a research task:

```bash
python -m research_agent "Your research question" --config config.toml
```

Or explicitly:

```bash
python -m research_agent run "Your research question" --config config.toml
```

Skip GitHub repo crawling (README-only):

```bash
python -m research_agent "Your research question" --config config.toml --skip-github
```

Outputs are written to `research/<run_name>/`.

## Remote Execution Options
- **SSH (simple)**

```bash
ssh <old-machine> "python -m research_agent 'Your query' --config config.toml"
```

- **HTTP Job Server (optional)**

```bash
python -m service.server --host 0.0.0.0 --port 8080 --jobs .job_queue
```

Submit a job:

```bash
curl -X POST http://<old-machine>:8080/jobs \
  -H 'Content-Type: application/json' \
  -d '{"query":"Your research question","config":"config.toml"}'
```

Check status:

```bash
curl http://<old-machine>:8080/jobs/<job_id>
```

## Output Structure
Each run creates:
- `summary.md`
- `sources.md`
- `subagent_source_gathering.md`
- `subagent_docs.md`
- `subagent_web.md`
- `subagent_synthesis.md`

## Notes
- Web sources are mandatory; include URLs in `sources`.
- GitHub repo URLs are supported (e.g., `https://github.com/org/repo` or `/tree/<branch>`).
- URLs embedded in the query are merged with `sources`.
- A source-gathering pass runs first and can add more URLs from initial sources.
- Citations are optional and can be added later.
- No embeddings are used yet; the architecture supports adding them later.

## GitHub OAuth (Optional)
If you hit GitHub rate limits or need private repos, run:

```bash
python -m research_agent auth-github --config config.toml
```

This uses the GitHub device flow and stores `github_client_id` and `github_token` in `config.toml`.
