import os
from typing import List, Dict

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class AICore:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history: List[Dict[str, str]] = [{"role":"system","content":system_prompt}]
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if OpenAI else None

    def ask(self, user_text: str) -> str:
        self.history.append({"role":"user","content":user_text})
        if not self.client:
            return "[AICore] OpenAI client not available. Set OPENAI_API_KEY."
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.history,
                temperature=0.5,
                max_tokens=800
            )
            out = resp.choices[0].message.content
            self.history.append({"role":"assistant","content":out})
            return out
        except Exception as e:
            return f"[AICore Error] {e}"
