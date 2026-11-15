# Chanchai Charnataparporn — CV

A comprehensive backend software engineer CV built as a self-contained HTML document, with a matching six-page A4 PDF.

## Files

| File | Purpose |
| --- | --- |
| `chanchai.html` | Editable CV source with embedded CSS and print layout |
| `chanchai.pdf` | Ready-to-share, six-page A4 PDF generated from the HTML |
| `AGENTS.md` | Maintenance and verification instructions for coding agents |

The CV covers professional experience, technical skills, platform engineering, selected projects, education, certifications, and academic awards. It uses no external assets, packages, or build tools.

## Open the CV

Open `chanchai.html` in Chrome, Edge, or another modern browser. Contact, profile, project, and credential links are clickable.

For the finished document, open [chanchai.pdf](chanchai.pdf).

## Print or regenerate the PDF

1. Open `chanchai.html` in Chrome or Edge.
2. Select **Print / Save as PDF**, or press `Ctrl+P`.
3. Use these settings:
   - Destination: **Save as PDF**
   - Paper size: **A4**
   - Orientation: **Portrait**
   - Margins: **None**
   - Scale: **Default / 100%**
   - Background graphics: **Enabled**
   - Browser headers and footers: **Disabled**
4. Save over `chanchai.pdf` when the HTML has changed.

The stylesheet defines A4 dimensions and explicit page breaks. Do not use “Fit to page,” since it can change the intended layout.

## Update the CV

Edit `chanchai.html`, check every page in print preview, and regenerate `chanchai.pdf`. Keep the HTML and PDF in the same commit so they remain synchronized.

Each page is an explicit `<section class="page">`. When adding or removing pages, update page numbering and the print instructions as well.

## Source-document privacy

The original Word resumes and Excel timesheet are private source material and are intentionally excluded by `.gitignore`. They are not required to view, print, or maintain the published CV. Do not commit them without an explicit decision to make them public.

## Repository

https://github.com/chanchai134/chanchai-dev
