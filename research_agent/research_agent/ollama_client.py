from __future__ import annotations

from typing import Iterable

import ollama


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout_sec: float = 120.0):
        self.model = model
        self.client = ollama.Client(host=base_url, timeout=timeout_sec)

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> str:
        options = {"temperature": temperature}
        if max_tokens is not None:
            options["num_predict"] = max_tokens

        if stream:
            parts: list[str] = []
            for chunk in self.client.chat(model=self.model, messages=messages, options=options, stream=True):
                msg = chunk.get("message", {}).get("content")
                if msg:
                    parts.append(msg)
            return "".join(parts).strip()

        response = self.client.chat(model=self.model, messages=messages, options=options)
        return response.get("message", {}).get("content", "").strip()
