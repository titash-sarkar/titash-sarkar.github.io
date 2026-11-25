# Personal site guide

This repository contains the public, static version of Titash Sarkar's personal site.

## Intent

The site is a home for a long-running personal inquiry: **what is intelligence made of?** It follows that question through information, memory, language, evolution, mathematics, physics, philosophy, and the history of life.

It is neither a résumé nor a catalogue of opinions. It should feel like a clear trail of thought: serious about big questions, curious without pretending to have resolved them, and willing to begin with the fundamentals.

Professional work in AI belongs on the site because it is part of Titash's life and career. It should not be presented as the reason for, proof of, or substitute for the personal inquiry into intelligence. The two stories may meet, but they remain distinct.

## Design

The design is quiet, editorial, and spacious. It should feel closer to a well-kept notebook than a product landing page.

- Use the paper, ink, green, and muted palette defined in `site.css`.
- Use serif type for ideas, titles, and reading; use sans-serif type for navigation, labels, and supporting details.
- Let generous whitespace, careful typography, and a small number of visual elements do the work.
- Keep pages responsive and readable on a phone.
- Avoid gradients, stock imagery, decorative animation, dense card grids, badges, dashboards, and generic "personal brand" styling.
- Make visual changes in `site.css` so published pages retain a coherent identity.

## Structure

- `index.html` is the homepage.
- `site.css` is the single shared stylesheet for every published page.
- `blog_md/` contains Markdown sources for posts.
- `blog_html/` contains generated, published HTML posts.
- `scripts/build_post.py` converts a Markdown post into its matching HTML page.

## Writing and publishing posts

Draft unfinished work in the separate `blog-wip` repository. When a post is ready to publish here:

1. Add or copy its Markdown source to `blog_md/`.
2. Give it front matter with at least a `title`:

   ```md
   ---
   title: Post title
   date: Month DD, YYYY
   description: A short page description.
   ---
   ```

3. Build the public page:

   ```bash
   python3 scripts/build_post.py blog_md/post-name.md blog_html/post-name.html
   ```

4. Add the generated page to the writing list in `index.html`.

Do not edit generated files in `blog_html/` by hand. Change the Markdown source, then rebuild it.

## Content voice

Write in a plain, slightly wry tone, with clarity, intellectual honesty, and an interest in first principles. Keep claims proportionate to the evidence. Prefer concrete language to generic professional language, and leave room for uncertainty when a question is genuinely open.

Keep the tone editorial: thoughtful, precise, and personal without sounding like a manifesto or a polished pitch. Use flamboyance judiciously. Vivid metaphors and dramatic phrasing should clarify an idea or reflect a genuine personal response; avoid stacking grand claims, neat oppositions, and slogan-like lines.

Each post should make one idea easier to see. Begin with the question or intuition that motivated it, then work toward a precise explanation. The goal is understanding, rather than performance or authority.


## Some other blogs for reference
- https://leimao.github.io/
- https://lilianweng.github.io/
- https://karpathy.github.io/
- https://sebastianraschka.com/
- https://lucumr.pocoo.org/