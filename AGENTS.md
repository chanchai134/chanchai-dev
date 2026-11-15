# AGENTS.md

## Purpose

This repository contains Chanchai Charnataparporn's comprehensive CV. The published artifact is a static HTML document with a six-page A4 print layout. There is no application server, package manager, build step, or test framework.

## Canonical files

- `chanchai.html` is the canonical, human-editable source and contains the **Print / Save as PDF** button.
- `README.md` documents viewing, printing, updating, and reviewing the CV.
- `.gitignore` excludes private Word resumes, Excel work logs, and generated PDFs.

PDFs are on-demand exports only; they are not repository artifacts. Never add `chanchai.pdf` or any other PDF to Git. PDF creation must go through the **Print / Save as PDF** button in the HTML, not through a generated file committed alongside the source.

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
- Preserve the **Print / Save as PDF** button and its `window.print()` behavior.

## Editing workflow

1. Check `git status`, the current branch, and `origin` before changing files.
2. Read the relevant HTML and identify the intended content or layout change.
3. Edit `chanchai.html`; keep unrelated content and styling unchanged.
4. Inspect every page in a real browser, including print media. Check for horizontal overflow, content beyond the page, overlapping footers, broken grids, and accidental blank pages.
5. Review the final diff and stage only the intended files with explicit `git add` commands.
6. Stop for the repository owner's review. Do not commit or push.

## On-demand PDF export

The repository owner can open `chanchai.html` and click **Print / Save as PDF**. Use these browser settings:

- A4 portrait
- 100% scale
- Zero margins
- Background graphics enabled
- Browser headers and footers disabled

Generated PDFs must remain outside Git. Do not create a repository PDF through DevTools, a script, or another build process. If the owner explicitly asks for a PDF verification copy, use the HTML print-button workflow and save it outside the repository; never stage it.

## Verification requirements

A content or layout change requires a real-browser print-layout check before staging.

- Confirm the expected page count; currently six pages.
- Confirm the print layout uses A4 portrait and the intended page breaks.
- Inspect all pages for clipping, overlap, blank pages, broken columns, and unreadably dense content.
- Confirm section endings and page-number markers are present and no content is truncated.
- Check that no PDF or private Office document is staged.
- Run `git diff --check` and review `git diff --stat` plus the actual diff.
- After staging, review `git status --short`, `git diff --cached --stat`, and `git diff --cached`.

If content overflows, rebalance sections or add a deliberate page rather than clipping content or shrinking the entire document excessively.

## Git staging and ownership

- Stage intended files explicitly; do not use `git add .` as a substitute for reviewing what will be published.
- Do not stage ignored source documents or generated PDFs with `git add -f`.
- Do not run `git commit` or `git push`. The repository owner performs both after reviewing the staged changes.
- Do not amend, reset, rebase, force-push, or otherwise rewrite Git history.
- Do not create releases, enable GitHub Pages, or change repository visibility.
- After staging, report the staged files and checks performed, then stop. Do not claim the changes were committed or published.

Update this file and `README.md` whenever the maintenance, export, or staging workflow changes.
