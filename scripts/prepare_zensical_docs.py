from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_DOCS = ROOT / "generated" / "zensical-docs"
OUT_CONFIG = ROOT / "zensical.generated.toml"
SOURCE_CONFIG = ROOT / "zensical.toml"
GENERATED_DOCS_DIR = "generated/zensical-docs"
SITE_STATS = DOCS / "assets" / "site-stats.json"
SITE_STATS_RE = re.compile(
    r"(<span\b(?=[^>]*\bdata-site-stat=[\"'](?P<key>[^\"']+)[\"'])[^>]*>)"
    r".*?"
    r"(</span>)"
)

META_KEYS = (
    "git_revision_date_localized",
    "git_revision_date_localized_raw_date",
    "git_revision_date_localized_raw_datetime",
    "git_revision_date_localized_raw_iso_date",
    "git_revision_date_localized_raw_iso_datetime",
    "git_revision_date_localized_hash",
    "git_creation_date_localized",
    "git_creation_date_localized_raw_date",
    "git_creation_date_localized_raw_datetime",
    "git_creation_date_localized_raw_iso_date",
    "git_creation_date_localized_raw_iso_datetime",
    "git_creation_date_localized_hash",
    "git_site_revision_date_localized",
    "git_site_revision_date_localized_raw_date",
    "git_site_revision_date_localized_raw_datetime",
    "git_site_revision_date_localized_raw_iso_date",
    "git_site_revision_date_localized_raw_iso_datetime",
    "git_site_revision_date_localized_hash",
)


@dataclass(frozen=True)
class GitDate:
    commit: str
    iso_datetime: str

    @property
    def iso_date(self) -> str:
        return self.iso_datetime[:10]

    @property
    def display(self) -> str:
        return self.iso_date


def run_git_log(path: Path | None = None) -> list[GitDate]:
    command = [
        "git",
        "log",
        "--follow",
        "--format=%H%x00%cI",
    ]
    if path is not None:
        command.extend(["--", str(path.relative_to(ROOT))])
    else:
        command.extend(["--", "docs"])

    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "unknown git error"
        raise RuntimeError(f"failed to read git history: {message}")

    dates: list[GitDate] = []
    for line in result.stdout.splitlines():
        commit, _, iso_datetime = line.partition("\0")
        if commit and iso_datetime:
            dates.append(GitDate(commit=commit, iso_datetime=iso_datetime))
    return dates


def fallback_date() -> GitDate:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return GitDate(commit="", iso_datetime=now.isoformat().replace("+00:00", "Z"))


def quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def metadata_for(path: Path, site_revision: GitDate) -> dict[str, str]:
    history = run_git_log(path)
    revision = history[0] if history else fallback_date()
    creation = history[-1] if history else revision

    return {
        "git_revision_date_localized": revision.display,
        "git_revision_date_localized_raw_date": revision.display,
        "git_revision_date_localized_raw_datetime": revision.iso_datetime,
        "git_revision_date_localized_raw_iso_date": revision.iso_date,
        "git_revision_date_localized_raw_iso_datetime": revision.iso_datetime,
        "git_revision_date_localized_hash": revision.commit,
        "git_creation_date_localized": creation.display,
        "git_creation_date_localized_raw_date": creation.display,
        "git_creation_date_localized_raw_datetime": creation.iso_datetime,
        "git_creation_date_localized_raw_iso_date": creation.iso_date,
        "git_creation_date_localized_raw_iso_datetime": creation.iso_datetime,
        "git_creation_date_localized_hash": creation.commit,
        "git_site_revision_date_localized": site_revision.display,
        "git_site_revision_date_localized_raw_date": site_revision.display,
        "git_site_revision_date_localized_raw_datetime": site_revision.iso_datetime,
        "git_site_revision_date_localized_raw_iso_date": site_revision.iso_date,
        "git_site_revision_date_localized_raw_iso_datetime": site_revision.iso_datetime,
        "git_site_revision_date_localized_hash": site_revision.commit,
    }


def split_front_matter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        return [], text

    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "".join(lines[index + 1 :])
            return lines[1:index], body
    return [], text


def inject_front_matter(path: Path, values: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(text)
    generated_keys = {f"{key}:" for key in META_KEYS}

    kept = [
        line
        for line in front_matter
        if line.split("#", 1)[0].strip().split(" ", 1)[0] not in generated_keys
    ]
    if kept and kept[-1].strip():
        kept.append("\n")

    generated = [f"{key}: {quote(values[key])}\n" for key in META_KEYS]
    path.write_text("---\n" + "".join(kept + generated) + "---\n" + body, encoding="utf-8")


def load_site_stats() -> dict[str, str]:
    if not SITE_STATS.exists():
        return {}

    values = json.loads(SITE_STATS.read_text(encoding="utf-8"))
    return {
        key: f"{value:,}" if isinstance(value, int) else str(value)
        for key, value in values.items()
    }


def inject_site_stats(path: Path, stats: dict[str, str]) -> None:
    if not stats:
        return

    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        key = match.group("key")
        value = stats.get(key)
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}{match.group(3)}"

    updated = SITE_STATS_RE.sub(replace, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def write_generated_config() -> None:
    text = SOURCE_CONFIG.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    in_project = False
    inserted = False
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_project and not inserted:
                output.append(f'docs_dir = "{GENERATED_DOCS_DIR}"\n')
                inserted = True
            in_project = stripped == "[project]"

        if in_project and stripped.startswith("docs_dir"):
            if not inserted:
                output.append(f'docs_dir = "{GENERATED_DOCS_DIR}"\n')
                inserted = True
            continue

        output.append(line)

    if in_project and not inserted:
        output.append(f'docs_dir = "{GENERATED_DOCS_DIR}"\n')
    elif not inserted:
        raise RuntimeError("could not find [project] section in zensical.toml")

    OUT_CONFIG.write_text("".join(output), encoding="utf-8")


def main() -> None:
    if OUT_DOCS.exists():
        shutil.rmtree(OUT_DOCS)
    shutil.copytree(DOCS, OUT_DOCS)

    site_history = run_git_log()
    site_revision = site_history[0] if site_history else fallback_date()
    site_stats = load_site_stats()

    for source_path in sorted(DOCS.rglob("*.md")):
        target_path = OUT_DOCS / source_path.relative_to(DOCS)
        inject_front_matter(target_path, metadata_for(source_path, site_revision))
        inject_site_stats(target_path, site_stats)

    write_generated_config()
    print(f"Prepared {OUT_DOCS.relative_to(ROOT)} and {OUT_CONFIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
