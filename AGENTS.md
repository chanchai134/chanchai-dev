# AGENTS.md

## Purpose

This repository contains Chanchai Charnataparporn's comprehensive CV. The published artifact is a static HTML document with a six-page A4 print layout. A dependency-free Node.js AWS Lambda handler streams the same HTML through the owner's existing API Gateway. GitHub Actions packages two files into a ZIP and updates the existing Lambda with the AWS CLI. There is no local application server, package manager, application build step, SAM template, or CI test suite.

## Canonical files

- `chanchai.html` is the canonical, human-editable source and contains the **Print / Save as PDF** button.
- `index.cjs` streams that exact HTML with the native Node.js Lambda response-streaming API.
- `.github/workflows/deploy-lambda.yml` assumes an AWS role through GitHub OIDC, packs `index.cjs` and `chanchai.html` into a ZIP, and runs `aws lambda update-function-code --publish`.
- `README.md` documents viewing, printing, updating, deployment configuration, and reviewing the CV.
- `.gitignore` excludes private sources and generated files.

PDFs are on-demand exports only; they are not repository artifacts. Never add `chanchai.pdf` or any other PDF to Git. PDF creation must go through the **Print / Save as PDF** button in the HTML, not through a generated file committed alongside the source.

## Content rules

- Preserve factual accuracy. Do not invent employers, dates, titles, credentials, technologies, responsibilities, or quantified outcomes.
- Use the longer, more detailed version when reconciling duplicate resume content.
- Do not remove historical detail merely to force the CV onto one page. This is deliberately a multi-page CV.
- Preserve working links and credential IDs exactly unless the user supplies replacements.
- Do not publish raw resumes, timesheets, work logs, addresses, or other private source material without explicit user approval. The origin repository is public at the time this guide was written.
- The existing API Gateway exposes the public CV. Package only the public HTML and handler in `cv-lambda.zip`; never include private source documents.
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
5. Do not add CI tests for this deployment. For handler changes, check JavaScript syntax with `node --check index.cjs` if needed. For workflow changes, lint the GitHub Actions YAML when a linter is available.
6. Review the final diff and stage only the intended files with explicit `git add` commands.
7. Stop for the repository owner's review. Do not commit, push, or trigger a deployment.

## On-demand PDF export

The repository owner can open `chanchai.html` and click **Print / Save as PDF**. Use these browser settings:

- A4 portrait
- 100% scale
- Zero margins
- Background graphics enabled
- Browser headers and footers disabled

Generated PDFs must remain outside Git. Do not create a repository PDF through DevTools, a script, or another build process. If the owner explicitly asks for a PDF verification copy, use the HTML print-button workflow and save it outside the repository; never stage it.

## AWS Lambda and continuous deployment

- Keep the Lambda dependency-free and stream `chanchai.html` from disk with `createReadStream` and `pipeline`; never read the whole document into memory or add a second canonical HTML copy.
- Export the handler with `awslambda.streamifyResponse` and wrap the writable stream using `awslambda.HttpResponseStream.from`. `awslambda` is a Lambda runtime global, not an npm dependency.
- Return status 200 and only the header `Content-Type: text/html; charset=utf-8`. Do not add method handling, extra headers, or buffered response objects; the gateway owns HTTP behavior.
- The workflow packs exactly `index.cjs` and `chanchai.html` at the root of `cv-lambda.zip` with `zip -j -X`, then calls `aws lambda update-function-code --zip-file fileb://cv-lambda.zip --publish` and `aws lambda wait function-updated`.
- The Node.js 24 Lambda and API Gateway already exist and are not provisioned by this repository. Do not add SAM, CloudFormation, Function URLs, artifact buckets, or gateway resources to this deployment.
- The gateway's REST API Lambda proxy integration should use response transfer mode `STREAM`.
- GitHub OIDC supplies short-lived credentials. Never add long-lived AWS access keys to workflow files or documentation.
- Use exactly three repository secrets: `AWS_REGION`, `FUNCTION_ARN`, and `AWS_DEPLOY_ROLE_ARN`. `FUNCTION_ARN` is the full ARN of the existing Lambda. Do not reintroduce GitHub variables or other deployment configuration.
- Reference secrets directly where needed; do not map them into `env` variables or echo them in workflow steps.
- The deployment role needs `lambda:UpdateFunctionCode`, `lambda:PublishVersion`, and `lambda:GetFunctionConfiguration` for the waiter.
- Do not add CI tests, a test job, SAM validation/build, or a gateway smoke test to this workflow. The owner deliberately wants a minimal package-and-upload pipeline.
- Pushing the workflow to `main` enables automatic deployment for subsequent changes. The repository owner performs that push and any manual workflow dispatch.

## Verification requirements

A content or layout change requires a real-browser print-layout check before staging.

- Confirm the expected page count; currently six pages.
- Confirm the print layout uses A4 portrait and the intended page breaks.
- Inspect all pages for clipping, overlap, blank pages, broken columns, and unreadably dense content.
- Confirm section endings and page-number markers are present and no content is truncated.
- Check that no PDF, private Office document, AWS credential, ZIP archive, test file, or SAM/build directory is staged.
- Do not add or run a CI test suite for this deployment.
- Lint the GitHub Actions YAML when a linter is available and verify the ZIP contains only `chanchai.html` and `index.cjs`.
- Run `git diff --check` and review `git diff --stat` plus the actual diff.
- After staging, review `git status --short`, `git diff --cached --stat`, and `git diff --cached`.

If content overflows, rebalance sections or add a deliberate page rather than clipping content or shrinking the entire document excessively.

## Git staging and ownership

- Stage intended files explicitly; do not use `git add .` as a substitute for reviewing what will be published.
- Do not stage ignored source documents or generated PDFs with `git add -f`.
- Do not run `git commit` or `git push`. The repository owner performs both after reviewing the staged changes.
- Do not amend, reset, rebase, force-push, or otherwise rewrite Git history.
- Do not create releases, enable GitHub Pages, change repository visibility, edit GitHub/AWS secrets, assume deployment roles, or trigger GitHub Actions deployments.
- Remember that pushing deployment-related files to `main` deploys to AWS. The owner controls that side effect by reviewing and pushing.
- After staging, report the staged files and checks performed, then stop. Do not claim the changes were committed, published, or deployed.

Update this file and `README.md` whenever the maintenance, export, or staging workflow changes.
