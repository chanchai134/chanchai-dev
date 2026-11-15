# AGENTS.md

## Purpose

This repository contains Chanchai Charnataparporn's comprehensive CV. The published artifacts are a static HTML document and its generated A4 PDF. There is no application server, package manager, build step, or test framework.

## Canonical files

- `chanchai.html` is the canonical, human-editable source.
- `chanchai.pdf` is the generated, ready-to-share artifact and is intentionally tracked.
- `README.md` documents viewing, printing, and updating the CV.
- `.gitignore` excludes private Word resumes and Excel work logs.

Keep the HTML and PDF synchronized. Never edit the PDF independently to make a content change; change the HTML and regenerate it.

## Content rules

- Preserve factual accuracy. Do not invent employers, dates, titles, credentials, technologies, responsibilities, or quantified outcomes.
- Use the longer, more detailed version when reconciling duplicate resume content.
- Do not remove historical detail merely to force the CV onto one page. This is deliberately a multi-page CV.
- Preserve working links and credential IDs exactly unless the user supplies replacements.
- Do not publish raw resumes, timesheets, work logs, addresses, or other private source material without explicit user approval. The origin repository is public at the time this guide was written.
- If the user asks for a content refresh, inspect current local sources rather than guessing from old summaries.

## HTML and print architecture

- The document is self-contained HTML with embedded CSS and system fonts; avoid adding runtime dependencies or remote assets.
- Each printed page is an explicit `<section class="page" id="page-N">` inside `<main class="cv">`.
- The current layout has six A4 pages. Update this guide, the print-bar text, and every `Page N of 6` footer if the page count intentionally changes.
- `.page` has fixed `210mm × 297mm` dimensions. `@page` selects A4 portrait with zero margins.
- Page footers are absolutely positioned. Content must remain above them.
- The screen-only print bar is hidden in print media.
- Preserve `break-after: page` / `page-break-after: always` behavior and avoid breaking individual jobs, project cards, or bullet items where practical.

## Editing workflow

1. Check `git status`, the current branch, and `origin` before changing files.
2. Read the relevant HTML and identify the intended content or layout change.
3. Edit `chanchai.html`; keep unrelated content and styling unchanged.
4. Inspect every page in a real browser, including print media. Check for horizontal overflow, content beyond the page, overlapping footers, broken grids, and accidental blank pages.
5. Regenerate `chanchai.pdf` from the updated HTML.
6. Verify the PDF and review the final diff before committing.

## PDF generation

Preferred browser settings:

- A4 portrait
- 100% scale
- Zero margins
- Background graphics enabled
- Browser headers and footers disabled

Browser DevTools Protocol can generate a deterministic PDF with `Page.printToPDF` using:

- `printBackground: true`
- `displayHeaderFooter: false`
- `preferCSSPageSize: true`
- `scale: 1`
- All four margins set to `0`

Alternatively, follow the manual Chrome/Edge instructions in `README.md`.

## Verification requirements

A content or layout change is not complete until the generated PDF has been checked.

- Confirm the expected page count; currently six pages.
- Confirm every page is A4 portrait, approximately `594.96 × 841.92` PDF points.
- Extract text and confirm section endings and page-number markers are present. Empty or truncated pages are failures.
- Render all pages to images and inspect them for clipping, overlap, blank pages, broken columns, and unreadably dense content.
- Check that `chanchai.html` and `chanchai.pdf` represent the same content.
- Run `git diff --check` and review `git diff --stat` plus the actual diff.

If content overflows, rebalance sections or add a deliberate page rather than clipping content or shrinking the entire document excessively.

## Git and publishing

- Stage intended files explicitly; do not use `git add .` as a substitute for reviewing what will be published.
- Do not commit ignored source documents with `git add -f`.
- Do not rewrite published history or force-push unless the user explicitly requests it.
- Use a focused conventional commit message, such as `docs: update CV experience` or `fix: correct CV print layout`.
- Push the current branch to its configured upstream. Do not create releases, enable GitHub Pages, or change repository visibility unless requested.
- After pushing, fetch or query the remote and verify that the remote branch points to the new local commit before reporting success.

Update this file and `README.md` whenever the maintenance or verification workflow changes.
