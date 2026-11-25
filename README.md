# Personal Site
This is a minimalist personal site hosted on GitHub Pages.

## Publishing a post

Write the draft as Markdown in `blog-wip`, then convert the finished draft into a page here:

```bash
python3 scripts/build_post.py /Users/titashsarkar/titash/git/blog-wip/my-post.md blog_html/my-post.html
```

Each draft starts with front matter. The standard converter creates a page using the dark notebook template in `scripts/templates/notebook.html`. Use `--layout article` for the older shared `site.css` article layout.

```md
---
title: The Monty Hall problem
date: April 18, 2025
description: Why switching doors gives you a better chance of winning.
---

# The first question

Write the post here. The converter supports headings, paragraphs, lists, links,
bold and italic text, quotes, horizontal rules, inline code, and fenced code blocks.
```

## Notebook pages

The dark notebook template is the standard output for Markdown pages. Build with:

```bash
python3 scripts/build_post.py blog_md/notebook.md blog_html/notebook.html
```

The template maps component tags to presentation classes. `hero` becomes the page header, `section` becomes a ruled section, `group` becomes a responsive card grid with a group label, `essay` becomes a card, and `quote` becomes a highlighted closing quote. Add a `class="..."` attribute only for a one-off variation; class names are appended to the component's default classes.

```md
---
title: A Notebook of Rational Inquiry
description: A notebook about intelligence and perception.
eyebrow: A field notebook
hero_image: ../delete/Exploring Ideas Toward Intelligence.png
hero_alt: A visual exploration of ideas converging toward intelligence.
footer: © 2026 · A Notebook of Rational Inquiry
---

:::hero
## A Working Approximation

Introductory paragraphs go here. Use **bold** for the blue serif highlight.
:::

:::section title="Following ideas past their boundaries."
:::group title="Mathematics"
:::essay symbol="π ≈ 3.14159…" title="Why π Shows Up Everywhere"
A circle's ratio turning up in probability, physics and prime numbers.
:::
:::
:::

:::quote cite="Dostoevsky"
*dubito, ergo cogito, ergo sum*
:::
```

Component tags accept `class="extra-class"` for an additional CSS class, for example `:::section title="About" class="narrow"`. Essay tags also accept `href="relative/path.html"` to make a card a link and `status="Coming soon"` to show a small status line. The Markdown tags choose the component; the template assigns its standard class automatically. The standard `scripts/build_post.py` command uses this notebook layout. Pass `--layout article` only when you need the older shared `site.css` article layout.
