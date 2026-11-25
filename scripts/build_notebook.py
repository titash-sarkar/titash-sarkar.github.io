#!/usr/bin/env python3
"""Build a component-based notebook page from tagged Markdown.

Usage: python3 scripts/build_notebook.py source.md output.html
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shlex
from pathlib import Path
from urllib.parse import quote

from build_post import parse_front_matter, render_markdown

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path(__file__).with_name("templates") / "notebook.html"
COMPONENTS = {"hero", "prose", "section", "group", "essay", "quote"}
CLASS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


def attrs_for(tag: str) -> tuple[str, dict[str, str]]:
    parts = shlex.split(tag)
    name = parts[0]
    attrs: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"Expected key=value in component tag: {part}")
        key, value = part.split("=", 1)
        attrs[key] = value
    return name, attrs


def extra_class(attrs: dict[str, str]) -> str:
    value = attrs.get("class", "").strip()
    if not value:
        return ""
    classes = value.split()
    if not all(CLASS_RE.fullmatch(item) for item in classes):
        raise ValueError(f"Invalid class name: {value}")
    return " " + " ".join(classes)


def render_components(markdown: str, metadata: dict[str, str]) -> str:
    lines = markdown.splitlines()

    def parse(index: int, nested: bool = False) -> tuple[str, int]:
        output: list[str] = []
        prose: list[str] = []

        def flush() -> None:
            if prose:
                output.append(render_markdown("\n".join(prose)))
                prose.clear()

        while index < len(lines):
            line = lines[index]
            if line.strip() == ":::" and nested:
                flush()
                return "\n".join(output), index + 1
            opening = re.fullmatch(r":::([A-Za-z]+)(?:\s+(.*))?", line.strip())
            if not opening:
                prose.append(line)
                index += 1
                continue
            flush()
            tag, raw_attrs = opening.groups()
            if tag not in COMPONENTS:
                raise ValueError(f"Unknown component '{tag}' on line {index + 1}")
            _, attrs = attrs_for(tag + (" " + raw_attrs if raw_attrs else ""))
            inner, index = parse(index + 1, nested=True)
            extra = extra_class(attrs)
            if tag == "hero":
                image = metadata.get("hero_image", "")
                image_html = ""
                if image:
                    src = quote(image, safe="/:#?&=%")
                    alt = html.escape(metadata.get("hero_alt", ""), quote=True)
                    image_html = f'<img class="hero-image" src="{src}" alt="{alt}" />'
                body_title = html.escape(metadata["title"])
                eyebrow = html.escape(metadata.get("eyebrow", ""))
                eyebrow_html = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
                output.append(f'<header class="hero{extra}">{eyebrow_html}<h1 class="site-title">{body_title}</h1>{image_html}<div class="prose">{inner}</div></header>')
            elif tag == "prose":
                output.append(f'<div class="prose{extra}">{inner}</div>')
            elif tag == "section":
                title = html.escape(attrs.get("title", ""))
                heading = f'<h2 class="section-title">{title}</h2>' if title else ""
                output.append(f'<section class="page-section{extra}">{heading}{inner}</section>')
            elif tag == "group":
                title = html.escape(attrs.get("title", ""))
                heading = f'<h3 class="group">{title}</h3>' if title else ""
                output.append(f'<div class="essays{extra}">{heading}{inner}</div>')
            elif tag == "essay":
                title = html.escape(attrs.get("title", ""))
                symbol = html.escape(attrs.get("symbol", ""))
                href = attrs.get("href", "")
                if href and (href.startswith("//") or href.lower().startswith(("javascript:", "data:"))):
                    raise ValueError("Essay links must use a relative path or an http(s) URL.")
                href_attr = f' href="{html.escape(href, quote=True)}"' if href else ""
                element = "a" if href else "article"
                heading = f'<h4>{title}</h4>' if title else ""
                symbol_html = f'<div class="sym">{symbol}</div>' if symbol else ""
                status = html.escape(attrs.get("status", ""))
                status_html = f'<span class="coming-soon">{status}</span>' if status else ""
                output.append(f'<{element} class="essay{extra}"{href_attr}>{symbol_html}{heading}{inner}{status_html}</{element}>')
            elif tag == "quote":
                cite = html.escape(attrs.get("cite", ""))
                cite_html = f'<cite>{cite}</cite>' if cite else ""
                output.append(f'<blockquote class="quote{extra}">{inner}{cite_html}</blockquote>')
        flush()
        if nested:
            raise ValueError("Unclosed component block; expected :::")
        return "\n".join(output), index

    rendered, _ = parse(0)
    return rendered


def build(metadata: dict[str, str], content: str, output_parent: Path = ROOT) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    metadata = dict(metadata)
    image = metadata.get("hero_image", "")
    if image:
        image_path = (ROOT / image).resolve()
        metadata["hero_image"] = Path(os.path.relpath(image_path, output_parent.resolve())).as_posix()
    rendered_content = render_components(content, metadata)
    if not re.search(r"^:::hero(?:\s|$)", content, re.MULTILINE):
        image = metadata.get("hero_image", "")
        image_html = ""
        if image:
            src = quote(image, safe="/:#?&=%")
            alt = html.escape(metadata.get("hero_alt", ""), quote=True)
            image_html = f'<img class="hero-image" src="{src}" alt="{alt}" />'
        rendered_content = (
            f'<header class="hero"><h1 class="site-title">{html.escape(metadata["title"])}</h1>'
            f'{image_html}<div class="prose">{rendered_content}</div></header>'
        )
    replacements = {
        "{{TITLE}}": html.escape(metadata["title"]),
        "{{DESCRIPTION}}": html.escape(metadata.get("description", metadata["title"]), quote=True),
        "{{CONTENT}}": rendered_content,
        "{{FOOTER}}": html.escape(metadata.get("footer", "A notebook of rational inquiry")),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a notebook page from tagged Markdown.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    metadata, content = parse_front_matter(args.source.read_text(encoding="utf-8"))
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(metadata, content, output.parent), encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
