# Chanchai Charnataparporn — CV

A comprehensive backend software engineer CV built as a self-contained HTML document with a six-page A4 print layout. A PDF can be exported on demand through the document's **Print / Save as PDF** button; no PDF is stored in this repository. A Node.js AWS Lambda function streams the same HTML through your existing API Gateway, and GitHub Actions updates its code through the AWS CLI.

## Files

| File | Purpose |
| --- | --- |
| `chanchai.html` | Editable CV source with embedded CSS, print layout, and PDF export button |
| `index.cjs` | Dependency-free Node.js handler that streams the HTML from disk |
| `.github/workflows/deploy-lambda.yml` | Two-file ZIP and AWS CLI code update using GitHub OIDC |
| `AGENTS.md` | Maintenance and staging instructions for coding agents |
| `.gitignore` | Exclusions for private sources and generated files |

The CV covers professional experience, technical skills, platform engineering, selected projects, education, certifications, and academic awards. The HTML and Lambda handler have no external runtime dependencies.

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

## AWS Lambda deployment

The Node.js 24 Lambda uses `awslambda.streamifyResponse`, `awslambda.HttpResponseStream.from`, `fs.createReadStream`, and `stream/promises.pipeline` to stream `chanchai.html` from disk without buffering it in memory. It returns status 200 and only the header `Content-Type: text/html; charset=utf-8`. Request events are ignored because this function serves only static CV content.

The existing Lambda runs Node.js 24 with handler `index.handler`. Your existing API Gateway and its permissions remain separate. For response streaming, its REST API Lambda proxy integration must use response transfer mode `STREAM`.

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
