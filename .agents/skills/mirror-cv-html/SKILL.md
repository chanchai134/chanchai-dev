---
name: mirror-cv-html
description: Use when syncing base.md to chanchai.html statically.
---

# Mirror CV Markdown to HTML

Mirror this repository's canonical CV content from `base.md` into the existing presentation in `chanchai.html`. This is a synchronization task, not a resume-writing task. Keep the workflow manual: there is no generator, package manager, build step, or second canonical HTML copy.

Do not use Computer Use, browser automation, browser rendering, screenshots, or print-preview automation for this procedure. Perform only static checks against the source files and HTML. The repository owner handles all browser and print verification personally.

## Start with the live files

1. Run `git status --short --branch`, confirm the current branch, and inspect `origin`.
2. Read `AGENTS.md`, `base.md`, and `chanchai.html`. Treat `AGENTS.md` as the repository-wide authority alongside this skill.
3. Preserve owner changes already in progress:
   - `git diff -- base.md chanchai.html`
   - `git diff --cached -- base.md chanchai.html`
   - Do not reset, unstage, or overwrite unrelated edits.
4. Decide whether the request changes content, presentation, or both. For wording changes, edit `base.md` first. For presentation-only changes, leave `base.md` unchanged and prove that all rendered content still matches it.

## Build the expected content model from the source

Parse `base.md` independently of the old HTML before editing. Locate source constructs by their markers and surrounding sections, not fixed line numbers; blank lines can change. Record the identity, role, contact rows, section headings, paragraphs, two-sided rows, job metadata, bullets, tags, links, and literal placeholders in source order.

Do not fill missing fields from older CVs or other career sources. Do not silently rephrase, correct capitalization, normalize dashes, or change dates, URLs, credential IDs, or punctuation. HTML escaping is allowed only when it produces the same visible text. Keep every `TODO` visible until the owner changes it in `base.md`.

## Apply these source mappings exactly

| `base.md` construct | Required `chanchai.html` rendering |
| --- | --- |
| First `#` name | `<h1 id="person-name">` inside `.hero` |
| Role line below the name | `<div class="role" id="person-role">` |
| Labeled contact fields | `.contact-item` elements inside the existing `.contact-row` groups; make the email a `mailto:` link and preserve every other supplied label and destination |
| `# Professional Summary` and following paragraph | A section headed by `.section-title`, with the paragraph in `.summary` |
| `# Education and certificates` | A section using the shared `.bullets` list; each entry retains a normal circular bullet |
| `left text -> right text` | `.split-line` with `.split-left` and `.split-right`; keep `display: flex` and `justify-content: space-between` in the stylesheet. Omit the `->` marker and preserve both text sides |
| `- ## job title -> duration` | A sibling `<article class="job">` containing `.job-head.split-line`, `h3.job-title.split-left`, and `.split-right` for the duration |
| Indented company/product/detail lines | One `<p class="job-meta">` per visible metadata line |
| `<br>` at the end of job metadata | Close the current `.job-meta` paragraph and put the next metadata line in its own `.job-meta` paragraph. Do not emit the marker or add an empty trailing paragraph |
| Indented `- ` responsibility | An `<li>` in that job's `<ul class="bullets">`, in source order |
| `- ### tag1, tag2` | One `<span class="tag">` per trimmed comma-separated value inside `.tags`, preserving exact spelling and source order; omit `###` and commas |
| `[label](url)` | `<a href="url">label</a>` with the exact label and destination |
| Bare `TODO` beneath a role | A normal paragraph containing exactly `TODO` |

Do not invent additional Markdown transformations. Keep inline links inside their original fields; do not append them elsewhere in the document.

## Preserve the current presentation architecture

- Keep one `<main class="cv">` containing `.hero`, the summary and education sections, and one Experience section. Put every role directly in that Experience section as a sibling `<article class="job">`.
- Keep `.cv` at `210mm` wide with automatic height and compact padding on screen and print. The screen sheet may have one continuous shadow, but no page gaps or fixed page heights.
- Give all roles identical unboxed typography, structure, and spacing. Do not introduce `.job-card`, role-card borders, shaded panels, `.remaining-jobs`, or different styling for roles containing `TODO`.
- Do not add explicit `.page` sections, a repeated continuation header, CV name/page-number footers, a second Experience heading, print buttons, runtime dependencies, or remote assets.
- Keep `@page { size: A4 portrait; margin: 0; }`. In print media, remove the screen shadow and use `box-decoration-break: clone` on `.cv` so document padding repeats at automatic page breaks.
- Let Chrome paginate naturally to use available page space. Never use `break-inside: avoid` on `.job`, wrap roles in an unbreakable group, or force an entire role onto a later page. A role may continue on the next page without repeating its title or the Experience heading.
- Keep individual bullets and education entries intact where practical with `.bullets li { break-inside: avoid; }`. Use `.job-head { break-after: avoid; }` to discourage an orphaned job heading, but do not use that as a reason to push a whole role forward.

## Edit only the necessary blocks

Reuse the existing CSS and DOM components. Change source-driven text in the corresponding HTML field, and change presentation in CSS or classes rather than altering source wording. Keep unrelated styling, deployment files, and documentation unchanged unless the presentation architecture or maintenance workflow actually changes. When it does, update both `README.md` and `AGENTS.md`, including this skill if its procedure becomes stale.

## Check content statically against the source

Compare the final HTML source with an expected content model derived independently from `base.md`; do not compare against another hand-written copy of the wording. Inspect HTML elements and attributes directly, without opening a browser. Check all of the following:

- Identity, role, contacts, headings, summary, education entries, all role titles/durations, metadata, bullets, tags, and placeholders match exactly after HTML unescaping.
- Every `->` row retains both text sides and uses `.split-line`, `.split-left`, and `.split-right` with the required flex CSS.
- Every source `<br>` produces the required metadata paragraph boundary without an empty paragraph.
- Every tag appears once, in source order, with exact capitalization. Confirm newly inserted tags stay in their intended positions.
- Every anchor label and literal `href` attribute matches the source in document order. Include the generated email `mailto:` link at its actual contact-row position.
- Visible text contains no `->`, `<br>`, or `###` rendering markers, retains the exact source count of `TODO`, and contains no legacy CV section or wording.
- The static CSS retains the continuous document, shared unboxed role treatment, and automatic print-pagination rules above.

If a mismatch is only in the HTML, mirror the canonical source rather than improvising wording. If a static checker reports an empty field or implausible count, debug its parser before changing the CV. Do not claim visual or print verification: the owner performs those checks personally. Do not create a PDF.

## Review and stage

1. Run `git diff --check` and inspect `git diff --stat` plus the actual diff.
2. Stage only intended files with explicit paths, normally `git add -- base.md chanchai.html`; add changed guides or this skill separately when applicable. Never use `git add .` as a substitute for review.
3. Review `git status --short`, `git diff --cached --stat`, and `git diff --cached`. Ensure no PDF, private Office source, credential, ZIP, test suite, or SAM/build directory is staged.
4. Report the staged files, static source/HTML comparison result, and any remaining placeholder content. State that browser and print verification are left to the owner. Stop for owner review. Do not commit, push, or deploy.
