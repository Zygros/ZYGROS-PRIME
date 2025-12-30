from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class Scroll:
    name: str
    path: Path
    content: str

    def summary(self, max_chars:int=400)->str:
        return (self.content[:max_chars] + "...") if len(self.content) > max_chars else self.content

def load_scrolls_from_dir(dir_path: str) -> List[Scroll]:
    p = Path(dir_path)
    out: List[Scroll] = []
    if not p.exists():
        return out
    for f in p.iterdir():
        if f.is_file() and f.suffix.lower() in {".txt", ".md"}:
            try:
                out.append(Scroll(name=f.name, path=f, content=f.read_text(encoding="utf-8", errors="ignore")))
            except Exception:
                pass
    return out
