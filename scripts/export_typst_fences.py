from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FENCE_RE = re.compile(r"```typst[^\n]*\n(.*?)\n```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*_\[\]()]", "", value)
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()


def title_for(text: str, position: int, index: int) -> str:
    headings = list(HEADING_RE.finditer(text[:position]))
    if headings:
        return headings[-1].group(2).strip()
    return f"diagram-{index:02d}"


def compile_svg(code: str, page_dir: Path, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "diagram.typ"
        src.write_text(code.strip() + "\n", encoding="utf-8")
        subprocess.run(
            ["typst", "compile", "--format", "svg", str(src), str(out)],
            cwd=page_dir,
            check=True,
        )


def main() -> None:
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        matches = list(FENCE_RE.finditer(text))
        if not matches:
            continue

        out_dir = page.parent / page.stem
        out_dir.mkdir(exist_ok=True)
        index = 0
        names: dict[str, int] = {}

        def replace(match: re.Match[str]) -> str:
            nonlocal index
            index += 1
            title = title_for(text, match.start(), index)
            slug = slugify(title) or f"diagram-{index:02d}"
            names[slug] = names.get(slug, 0) + 1
            name = f"{slug}-{names[slug]}.svg" if names[slug] > 1 else f"{slug}.svg"
            svg = out_dir / name
            compile_svg(match.group(1), page.parent, svg)
            return (
                '<figure class="typst-diagram">\n'
                f'  <img src="{page.stem}/{name}" alt="{title}">\n'
                "</figure>"
            )

        page.write_text(FENCE_RE.sub(replace, text), encoding="utf-8")


if __name__ == "__main__":
    main()
