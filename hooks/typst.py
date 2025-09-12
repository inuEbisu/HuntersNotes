import os
import re
import subprocess
import tempfile

FENCE_RE = re.compile(r"```typst[^\n]*\n(.*?)\n```", re.DOTALL)


def compile_typst_to_svg(code: str, cwd: str) -> str:
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "snippet.typ")
        out = os.path.join(td, "snippet.svg")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)
        subprocess.run(
            ["typst", "compile", "--format", "svg", src, out],
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        with open(out, "r", encoding="utf-8") as f:
            return f.read()


def on_page_markdown(markdown, page, config, files):
    page_dir = os.path.dirname(page.file.abs_src_path)

    def repl(m):
        code = m.group(1).strip()
        try:
            svg = compile_typst_to_svg(code, cwd=page_dir)
            return f'<figure class="typst-diagram">{svg}</figure>'
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode("utf-8", "ignore")
            return f'{m.group(0)}\n\n<div class="admonition danger"><p class="admonition-title">Compilation failed</p><pre><code>{err}</code></pre></div>'

    return FENCE_RE.sub(repl, markdown)
