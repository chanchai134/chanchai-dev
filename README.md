# Chanchai Charnataparporn — CV

A comprehensive backend software engineer CV built as a self-contained HTML document with a six-page A4 print layout. A PDF can be exported on demand through the document's **Print / Save as PDF** button; no PDF is stored in this repository.

## Files

| File | Purpose |
| --- | --- |
| `chanchai.html` | Editable CV source with embedded CSS, print layout, and PDF export button |
| `README.md` | Viewing, printing, updating, and review instructions |
| `AGENTS.md` | Maintenance, verification, and staging instructions for coding agents |
| `.gitignore` | Exclusions for private source documents and generated PDFs |

The CV covers professional experience, technical skills, platform engineering, selected projects, education, certifications, and academic awards. It uses no external assets, packages, or build tools.

## Open the CV

Open `chanchai.html` in Chrome, Edge, or another modern browser. Contact, profile, project, and credential links are clickable.

## Export a PDF

The **Print / Save as PDF** button in `chanchai.html` is the only PDF export path for this repository.

1. Open `chanchai.html` in Chrome or Edge.
2. Click **Print / Save as PDF** at the top of the document.
3. In the browser's print dialog, use these settings:
   - Destination: **Save as PDF**
   - Paper size: **A4**
   - Orientation: **Portrait**
   - Margins: **None**
   - Scale: **Default / 100%**
   - Background graphics: **Enabled**
   - Browser headers and footers: **Disabled**
4. Save the PDF wherever you want to keep or share it. Generated PDFs are ignored and must not be committed.

The stylesheet defines A4 dimensions and explicit page breaks. Do not use “Fit to page,” since it can change the intended layout.

## Update the CV

Edit `chanchai.html` and check every page in the browser's print preview. When a PDF is needed, export a fresh copy with **Print / Save as PDF**. Do not add the exported PDF to Git.

Each page is an explicit `<section class="page">`. When adding or removing pages, update page numbering and the print instructions as well.

## Review and publish changes

Agents may modify files and stage intended changes with explicit `git add` commands. Agents must not commit or push; the repository owner reviews, commits, and pushes.

Before committing, review the staged work:

```bash
git status --short
git diff --cached
```

## Source-document privacy

The original Word resumes and Excel timesheet are private source material and are intentionally excluded by `.gitignore`. They are not required to view, print, or maintain the published CV. Do not commit them without an explicit decision to make them public.

## Repository

https://github.com/chanchai134/chanchai-dev
