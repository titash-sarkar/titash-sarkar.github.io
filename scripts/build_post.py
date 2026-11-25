#!/usr/bin/env python3
"""Convert a Markdown draft into a themed HTML page for this site.

Usage:
    python3 scripts/build_post.py /path/to/draft.md blog/my-post.html
    python3 scripts/build_post.py /path/to/draft.md blog/my-post.html --layout article
"""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def parse_front_matter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        raise ValueError("A post must begin with YAML-style front matter delimited by ---. ")

    end = markdown.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Front matter must end with a line containing ---. ")

    metadata: dict[str, str] = {}
    for line in markdown[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front-matter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"')

    if "title" not in metadata:
        raise ValueError("Front matter requires a title.")
    return metadata, markdown[end + 5 :].strip()


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*|__([^_]+)__", lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)", lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    return text


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    quote: list[str] = []
    in_code = False
    code: list[str] = []

    def close_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    def close_quote() -> None:
        nonlocal quote
        if quote:
            output.append(f"<blockquote>{inline(' '.join(quote))}</blockquote>")
            quote = []

    for line in lines:
        if line.startswith("```"):
            close_paragraph()
            close_list()
            close_quote()
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
                code = []
            in_code = not in_code
            continue

        if in_code:
            code.append(line)
            continue

        if not line.strip():
            close_paragraph()
            close_list()
            close_quote()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            close_paragraph()
            close_list()
            close_quote()
            level = len(heading.group(1)) + 1  # The document title is already the h1.
            output.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            continue

        if re.match(r"^\s*(---|\*\*\*|___)\s*$", line):
            close_paragraph()
            close_list()
            close_quote()
            output.append("<hr />")
            continue

        if line.startswith("> "):
            close_paragraph()
            close_list()
            quote.append(line[2:])
            continue

        unordered = re.match(r"^[-*+]\s+(.+)$", line)
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if unordered or ordered:
            close_paragraph()
            close_quote()
            wanted = "ul" if unordered else "ol"
            if list_type and list_type != wanted:
                close_list()
            if not list_type:
                output.append(f"<{wanted}>")
                list_type = wanted
            output.append(f"<li>{inline((unordered or ordered).group(1))}</li>")
            continue

        close_list()
        close_quote()
        paragraph.append(line.strip())

    if in_code:
        raise ValueError("Unclosed code fence.")
    close_paragraph()
    close_list()
    close_quote()
    return "\n      ".join(output)


def build_page(metadata: dict[str, str], article_html: str, stylesheet_href: str, home_href: str) -> str:
    title = html.escape(metadata["title"])
    description = html.escape(metadata.get("description", title), quote=True)
    date = html.escape(metadata.get("date", ""))
    date_html = f'\n        <p class="article-date">{date}</p>' if date else ""

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{description}" />
  <title>{title} — Titash Sarkar</title>
  <link rel="stylesheet" href="{stylesheet_href}" />
</head>
<body>
  <main class="article-page">
    <a href="{home_href}" class="back-link">&larr; Back to home</a>
    <header class="article-header">
      <h1>{title}</h1>{date_html}
    </header>
    <article class="article-body">
      {article_html}
    </article>
  </main>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a site article from Markdown.")
    parser.add_argument("source", type=Path, help="Markdown draft with front matter")
    parser.add_argument("output", type=Path, help="HTML file to create")
    parser.add_argument(
        "--layout", choices=("notebook", "article"), default="notebook",
        help="Page layout (default: notebook).",
    )
    args = parser.parse_args()

    metadata, markdown = parse_front_matter(args.source.read_text(encoding="utf-8"))
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.layout == "notebook":
        from build_notebook import build as build_notebook_page
        page = build_notebook_page(metadata, markdown, output.parent)
    else:
        relative_css = Path(os.path.relpath(ROOT / "site.css", output.parent)).as_posix()
        relative_home = Path(os.path.relpath(ROOT / "index.html", output.parent)).as_posix()
        page = build_page(metadata, render_markdown(markdown), relative_css, relative_home)
    output.write_text(page, encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
