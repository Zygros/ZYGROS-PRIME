"""Provider-neutral AI adapter.

Supports OpenAI-compatible HTTP APIs (including OpenAI) and local Ollama.
No provider credentials are stored in the repository.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class AIConfig:
    provider: str = os.getenv("ZYGROS_AI_PROVIDER", "openai")
    model: str = os.getenv("ZYGROS_AI_MODEL", "gpt-5.6-mini")
    base_url: str = os.getenv("ZYGROS_AI_BASE_URL", "https://api.openai.com/v1")
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    timeout: int = int(os.getenv("ZYGROS_AI_TIMEOUT", "120"))


class AIProvider:
    def __init__(self, config: AIConfig | None = None):
        self.config = config or AIConfig()

    def generate(self, prompt: str, system: str = "") -> str:
        p = self.config.provider.lower()
        if p in {"openai", "api", "openai-compatible"}:
            return self._openai_compatible(prompt, system)
        if p == "ollama":
            return self._ollama(prompt, system)
        raise ValueError(f"Unsupported ZYGROS_AI_PROVIDER: {self.config.provider}")

    def _openai_compatible(self, prompt: str, system: str) -> str:
        if not self.config.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for API mode")
        url = self.config.base_url.rstrip("/") + "/chat/completions"
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": ([{"role": "system", "content": system}] if system else [])
            + [{"role": "user", "content": prompt}],
        }
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.config.timeout,
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def _ollama(self, prompt: str, system: str) -> str:
        url = self.config.base_url.rstrip("/") + "/api/chat"
        messages = ([{"role": "system", "content": system}] if system else [])
        messages.append({"role": "user", "content": prompt})
        r = requests.post(
            url,
            json={"model": self.config.model, "messages": messages, "stream": False},
            timeout=self.config.timeout,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
