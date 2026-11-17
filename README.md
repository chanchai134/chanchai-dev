# Chanchai Charnataparporn — CV

A senior software engineer CV sourced from `base.md` and presented as a self-contained HTML document with a two-page A4 print layout and no CV page footers. A PDF can be exported on demand through the browser's print menu; no PDF is stored in this repository. A Node.js AWS Lambda function serves the same HTML through your existing API Gateway HTTP API, and GitHub Actions updates its code through the AWS CLI.

## Files

| File | Purpose |
| --- | --- |
| `base.md` | Canonical CV content and wording |
| `chanchai.html` | Presentation source with embedded CSS and a two-page print layout; its content mirrors `base.md` |
| `index.cjs` | Dependency-free Node.js handler that returns the HTML as a string |
| `.github/workflows/deploy-lambda.yml` | Two-file ZIP and AWS CLI code update using GitHub OIDC |
| `AGENTS.md` | Content-mapping, maintenance, and staging instructions for coding agents |
| `.gitignore` | Exclusions for private sources and generated files |

The CV contains the professional summary, education and certificates, and experience from `base.md`. Literal `TODO` entries remain visible until the source is updated. The HTML and Lambda handler have no external runtime dependencies.

## Open the CV

Open `chanchai.html` in Chrome, Edge, or another modern browser. Contact, profile, project, and credential links are clickable.

## Export a PDF

Use the browser's built-in print menu to export a PDF. The HTML contains no in-document print controls.

1. Open `chanchai.html` in Chrome or Edge.
2. Open the browser menu and choose **Print**.
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

Edit wording in `base.md` first, then mirror it into `chanchai.html` without rephrasing or adding content. Edit `chanchai.html` directly only for presentation changes. There is no generator or build step; the two files are synchronized manually.

Apply these source mappings exactly:

- `left text -> right text`: render a flex row with `justify-content: space-between`, preserving both text sides and hiding the `->` marker.
- `<br>`: render a normal HTML line break.
- `### text1, text2, text3`: render each comma-separated value as a separate `<span class="tag">...</span>` in source order, without the `###` marker or commas.
- Markdown links: preserve the exact label and URL as a clickable link.

Preserve all other wording and literal `TODO` entries exactly. Check every page in a real browser with print media enabled. When a PDF is needed, export a fresh copy through the browser's print menu and do not add it to Git.

Each page is an explicit `<section class="page">`. The current two-page layout places profile/education plus the Experience heading and complete first role on page 1, and the four remaining roles on page 2, with compact headers and no CV name/page-number footers. Keep the Experience heading and first role together on page 1, without duplicating the heading on page 2. When adding or removing pages, update this guide and `AGENTS.md`. Keep browser headers and footers disabled during PDF export. Changing `base.md` alone does not change the published document or trigger deployment; the updated content must also be mirrored into `chanchai.html`. The deployment package still contains only `chanchai.html` and `index.cjs`.

## AWS Lambda deployment

The Node.js 24 Lambda uses `fs/promises.readFile` to read `chanchai.html` from disk as a UTF-8 string and returns a standard Lambda proxy response. The response contains `statusCode: 200`, the HTML string in `body`, and only the header `Content-Type: text/html; charset=utf-8`. Request events are ignored because this function serves only static CV content.

The existing Lambda runs Node.js 24 with handler `index.handler`. Your existing API Gateway HTTP API and its permissions remain separate. Its Lambda proxy integration uses standard buffered responses; no response streaming configuration is required.

The workflow has no CI test or SAM build. It simply:

1. Assumes your deployment role through GitHub OIDC.
2. Packs `index.cjs` and `chanchai.html` at the ZIP root.
3. Runs `aws lambda update-function-code --publish`.
4. Waits for the code update to finish.

Set these three repository secrets under **Settings → Secrets and variables → Actions**:

| Secret | Value |
| --- | --- |
| `AWS_REGION` | Lambda region, such as `ap-southeast-1` |
| `FUNCTION_ARN` | Full ARN of the existing Lambda function |
| `AWS_DEPLOY_ROLE_ARN` | IAM role trusted by this repository's GitHub OIDC identity |

The deployment role needs `lambda:UpdateFunctionCode` and `lambda:PublishVersion` on that function, plus `lambda:GetFunctionConfiguration` for the AWS waiter. No AWS access keys, S3 bucket, SAM, CloudFormation, or GitHub variables are used.

Pushes to `main` deploy when `chanchai.html`, `index.cjs`, or the workflow changes. Manual deployment is available through **Actions → Deploy CV to AWS Lambda**.

After a successful deployment, the live CV is available at **https://chanchai.dev/**.

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
