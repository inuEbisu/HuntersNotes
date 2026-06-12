from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "assets" / "site-stats.json"

FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FENCE_RE = re.compile(r"```[^\n]*\n(.*?)\n```", re.DOTALL)
CJK_RE = re.compile(r"[\u3400-\u9fff]")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-_'][A-Za-z0-9]+)*")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)|<img\b", re.IGNORECASE)


def strip_markdown(text: str) -> str:
    text = FRONT_MATTER_RE.sub("", text)
    text = FENCE_RE.sub("", text)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"[#>*_~\-|=]", " ", text)
    return text


def count_code_lines(text: str) -> int:
    total = 0
    for match in FENCE_RE.finditer(text):
        total += sum(1 for line in match.group(1).splitlines() if line.strip())
    return total


def main() -> None:
    stats = {"pages": 0, "words": 0, "codes": 0, "images": 0}

    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        prose = strip_markdown(text)

        stats["pages"] += 1
        stats["words"] += len(CJK_RE.findall(prose)) + len(WORD_RE.findall(prose))
        stats["codes"] += count_code_lines(text)
        stats["images"] += len(IMAGE_RE.findall(text))

    OUT.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
