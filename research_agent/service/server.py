from __future__ import annotations

import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from research_agent.config import load_config
from research_agent.orchestrator import Orchestrator


class JobStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create(self, payload: dict) -> str:
        job_id = uuid.uuid4().hex
        path = self.base_dir / f"{job_id}.json"
        payload = {
            "id": job_id,
            "status": "queued",
            "output_dir": None,
            "error": None,
            **payload,
        }
        path.write_text(json.dumps(payload, indent=2))
        return job_id

    def update(self, job_id: str, **fields: object) -> None:
        path = self.base_dir / f"{job_id}.json"
        data = json.loads(path.read_text())
        data.update(fields)
        path.write_text(json.dumps(data, indent=2))

    def get(self, job_id: str) -> dict:
        path = self.base_dir / f"{job_id}.json"
        return json.loads(path.read_text())


class Handler(BaseHTTPRequestHandler):
    server_version = "ResearchAgentServer/0.1"

    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/jobs":
            self._send(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        payload = json.loads(raw.decode("utf-8"))
        query = payload.get("query")
        config_path = payload.get("config", "config.toml")
        run_name = payload.get("run_name")

        if not query:
            self._send(400, {"error": "Missing 'query'"})
            return

        cfg = load_config(config_path)
        job_id = self.server.job_store.create({"query": query, "config": config_path})

        def _run_job() -> None:
            self.server.job_store.update(job_id, status="running")
            try:
                orchestrator = Orchestrator(cfg)
                output_dir = orchestrator.run(query, run_name=run_name)
                self.server.job_store.update(job_id, status="completed", output_dir=str(output_dir))
            except Exception as exc:  # pragma: no cover - safety net
                self.server.job_store.update(job_id, status="failed", error=str(exc))

        thread = threading.Thread(target=_run_job, daemon=True)
        thread.start()

        self._send(202, {"id": job_id, "status": "queued"})

    def do_GET(self) -> None:  # noqa: N802
        if not self.path.startswith("/jobs/"):
            self._send(404, {"error": "Not found"})
            return

        job_id = self.path.split("/jobs/")[-1]
        try:
            data = self.server.job_store.get(job_id)
        except FileNotFoundError:
            self._send(404, {"error": "Job not found"})
            return

        self._send(200, data)


class ResearchAgentServer(HTTPServer):
    def __init__(self, host: str, port: int, job_store: JobStore):
        super().__init__((host, port), Handler)
        self.job_store = job_store


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Research agent job server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--jobs", default=".job_queue")
    args = parser.parse_args()

    server = ResearchAgentServer(args.host, args.port, JobStore(Path(args.jobs)))
    print(f"Server listening on {args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
