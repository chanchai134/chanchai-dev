#!/usr/bin/env python3
"""Deterministically mirror base.md into <main class="cv"> in chanchai.html.

Default mode is a read-only parity check. Use --write to update the HTML.
Only Python's standard library is required; no browser is opened.
"""

from __future__ import annotations

import argparse
import difflib
import html
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

CONTACT_LABELS = (
    "Phone",
    "Email",
    "Date of Birth",
    "Web",
    "GitHub",
    "LinkedIn",
)
SUMMARY_HEADING = "# Professional Summary"
EDUCATION_HEADING = "# Education and certificates"
PROJECTS_HEADING = "# Individual Projects"
EXPERIENCE_HEADING = "# Experience"
CONTACT_PATTERN = re.compile(
    r"(?<!\S)(" + "|".join(re.escape(label) for label in CONTACT_LABELS) + r"):"
)


class SyncError(ValueError):
    """A source or template cannot be synchronized safely."""


@dataclass(frozen=True)
class Contact:
    label: str
    value: str


@dataclass(frozen=True)
class SplitRow:
    left: str
    right: str


@dataclass(frozen=True)
class Job:
    title: str
    duration: str
    # Entries are (kind, value), where kind is metadata, bullet, tags, or placeholder.
    entries: tuple[tuple[str, str | tuple[str, ...]], ...]


@dataclass(frozen=True)
class Project:
    title: str
    # Entries are (kind, value), where kind is metadata, bullet, tags, or placeholder.
    entries: tuple[tuple[str, str | tuple[str, ...]], ...]


@dataclass(frozen=True)
class CV:
    name: str
    role: str
    contact_rows: tuple[tuple[Contact, ...], ...]
    summary: tuple[str, ...]
    education: tuple[SplitRow, ...]
    projects: tuple[Project, ...]
    jobs: tuple[Job, ...]


def fail(line_number: int, message: str) -> None:
    raise SyncError(f"base.md:{line_number}: {message}")


def required_field(value: str, line_number: int, field: str) -> str:
    if not value:
        fail(line_number, f"{field} must not be empty")
    if value != value.strip():
        fail(line_number, f"{field} has unexpected surrounding whitespace")
    return value


def split_row(value: str, line_number: int) -> SplitRow:
    if value.count(" -> ") != 1:
        fail(line_number, "expected exactly one ' -> ' separator")
    left, right = value.split(" -> ")
    return SplitRow(
        required_field(left, line_number, "left-hand text"),
        required_field(right, line_number, "right-hand text"),
    )


def parse_contact_line(line: str, line_number: int) -> tuple[Contact, ...]:
    matches = list(CONTACT_PATTERN.finditer(line))
    if not matches or matches[0].start() != 0:
        fail(line_number, "expected labeled contact fields")
    contacts = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        value = line[match.end() : end].strip()
        if not value:
            fail(line_number, f"{match.group(1)} value must not be empty")
        contacts.append(Contact(match.group(1), value))
    return tuple(contacts)


def parse_base(source: str) -> CV:
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) < 2:
        fail(1, "expected a name and role")
    if not lines[0].startswith("# ") or lines[0].startswith("## "):
        fail(1, "expected '# <name>'")
    name = required_field(lines[0][2:], 1, "name")
    role = required_field(lines[1], 2, "role")

    index = 2
    contact_rows = []
    while index < len(lines) and lines[index] != SUMMARY_HEADING:
        line = lines[index]
        if line.startswith("# "):
            fail(index + 1, f"expected '{SUMMARY_HEADING}'")
        if line.strip():
            contact_rows.append(parse_contact_line(line, index + 1))
        index += 1
    if index == len(lines):
        fail(len(lines), f"missing '{SUMMARY_HEADING}'")
    if not contact_rows:
        fail(index + 1, "at least one contact row is required")
    index += 1

    summary = []
    while index < len(lines) and lines[index] != EDUCATION_HEADING:
        line = lines[index]
        if line.startswith("# "):
            fail(index + 1, f"expected '{EDUCATION_HEADING}'")
        if line.strip():
            summary.append(required_field(line, index + 1, "summary paragraph"))
        index += 1
    if index == len(lines):
        fail(len(lines), f"missing '{EDUCATION_HEADING}'")
    if not summary:
        fail(index + 1, "professional summary must not be empty")
    index += 1

    education = []
    while index < len(lines) and lines[index] != EXPERIENCE_HEADING:
        line = lines[index]
        if line.startswith("# "):
            fail(index + 1, f"expected '{EXPERIENCE_HEADING}'")
        if line.strip():
            if not line.startswith(" - "):
                fail(index + 1, "expected an education entry beginning with ' - '")
            education.append(split_row(line[3:], index + 1))
        index += 1
    if index == len(lines):
        fail(len(lines), f"missing '{EXPERIENCE_HEADING}'")
    if not education:
        fail(index + 1, "at least one education entry is required")
    # Don't increment index here - we're pointing at EXPERIENCE_HEADING
    
    # Skip EXPERIENCE_HEADING
    index += 1

    jobs = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("# "):
            # Found a new section (e.g., "# Individual Projects"), stop parsing jobs
            break
        if not line.startswith(" - ## "):
            fail(index + 1, "expected a role beginning with ' - ## '")
        title_row = split_row(line[6:], index + 1)
        index += 1
        entries = []
        while index < len(lines) and not lines[index].startswith(" - ## "):
            line = lines[index]
            if not line.strip():
                index += 1
                continue
            if line.startswith("# "):
                # Found a new section (e.g., "# Individual Projects"), exit inner loop
                # Outer loop will handle it
                break
            if not line.startswith("   ") or line.startswith("    "):
                fail(index + 1, "role content must use exactly three leading spaces")
            body = line[3:]
            if body.startswith("- ### "):
                raw_tags = body[6:]
                tags = tuple(tag.strip() for tag in raw_tags.split(","))
                if not raw_tags or any(not tag for tag in tags):
                    fail(index + 1, "tag lists must contain non-empty comma-separated values")
                entries.append(("tags", tags))
            elif body.startswith("- "):
                bullet = required_field(body[2:], index + 1, "bullet")
                entries.append(("bullet", bullet))
            elif body == "TODO":
                entries.append(("placeholder", body))
            else:
                if "<br>" in body:
                    if body.count("<br>") != 1 or not body.endswith("<br>"):
                        fail(index + 1, "<br> is supported only once at the end of metadata")
                    body = body[:-4]
                metadata = required_field(body, index + 1, "metadata")
                entries.append(("metadata", metadata))
            index += 1
        jobs.append(Job(title_row.left, title_row.right, tuple(entries)))
    if not jobs:
        fail(len(lines), "at least one experience role is required")
    
    # Parse projects (optional, after jobs)
    projects = []
    if index < len(lines) and lines[index] == PROJECTS_HEADING:
        index += 1  # Skip PROJECTS_HEADING
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue
            if line.startswith("# "):
                # No more sections after projects expected
                fail(index + 1, "additional sections after projects are not supported")
            if not line.startswith(" - ## "):
                fail(index + 1, "expected a project beginning with ' - ## '")
            title = required_field(line[6:], index + 1, "project title")
            index += 1
            entries = []
            while index < len(lines) and not lines[index].startswith(" - ## "):
                line = lines[index]
                if not line.strip():
                    index += 1
                    continue
                if line.startswith("# "):
                    fail(index + 1, "additional sections are not supported")
                if not line.startswith("   ") or line.startswith("    "):
                    fail(index + 1, "project content must use exactly three leading spaces")
                body = line[3:]
                if body.startswith("- ### "):
                    raw_tags = body[6:]
                    tags = tuple(tag.strip() for tag in raw_tags.split(","))
                    if not raw_tags or any(not tag for tag in tags):
                        fail(index + 1, "tag lists must contain non-empty comma-separated values")
                    entries.append(("tags", tags))
                elif body.startswith("- "):
                    bullet = required_field(body[2:], index + 1, "bullet")
                    entries.append(("bullet", bullet))
                elif body == "TODO":
                    entries.append(("placeholder", body))
                else:
                    if "<br>" in body:
                        if body.count("<br>") != 1 or not body.endswith("<br>"):
                            fail(index + 1, "<br> is supported only once at the end of metadata")
                        body = body[:-4]
                    metadata = required_field(body, index + 1, "metadata")
                    entries.append(("metadata", metadata))
                index += 1
            projects.append(Project(title, tuple(entries)))

    return CV(
        name=name,
        role=role,
        contact_rows=tuple(contact_rows),
        summary=tuple(summary),
        education=tuple(education),
        projects=tuple(projects),
        jobs=tuple(jobs),
    )


def markdown_links(text: str) -> list[tuple[int, int, str, str]]:
    """Return (start, end, label, destination) for supported inline links."""
    links = []
    position = 0
    while position < len(text):
        start = text.find("[", position)
        if start < 0:
            break
        if "]" in text[position:start]:
            raise SyncError("unmatched closing bracket outside a Markdown link")
        label_end = text.find("](", start + 1)
        if label_end < 0:
            raise SyncError("unclosed Markdown link label")
        label = text[start + 1 : label_end]
        if not label:
            raise SyncError("Markdown link labels must not be empty")
        if "[" in label or "]" in label:
            raise SyncError("nested or unmatched brackets in Markdown link labels are not supported")
        destination_start = label_end + 2
        destination_end = destination_start
        depth = 1
        while destination_end < len(text) and depth:
            character = text[destination_end]
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    break
            destination_end += 1
        if destination_end == len(text) or depth != 0:
            raise SyncError("unclosed Markdown link destination")
        destination = text[destination_start:destination_end]
        if not destination or destination != destination.strip():
            raise SyncError("Markdown link destinations must be non-empty and have no surrounding whitespace")
        if any(ord(character) <= 0x20 for character in destination):
            raise SyncError("Markdown link destinations must not contain whitespace")
        links.append((start, destination_end + 1, label, destination))
        position = destination_end + 1
    if "]" in text[position:]:
        raise SyncError("unmatched closing bracket outside a Markdown link")
    return links


def inline_html(text: str) -> str:
    if "<br>" in text:
        raise SyncError("inline <br> is supported only at the end of job metadata")
    output = []
    position = 0
    for start, end, label, destination in markdown_links(text):
        output.append(html.escape(text[position:start]))
        output.append(
            f'<a href="{html.escape(destination, quote=True)}">{html.escape(label)}</a>'
        )
        position = end
    output.append(html.escape(text[position:]))
    return "".join(output)


def contact_html(contact: Contact) -> str:
    if contact.label == "Email" and "[" not in contact.value:
        escaped = html.escape(contact.value)
        return f'<a href="mailto:{escaped}">{escaped}</a>'
    return inline_html(contact.value)


def render_main(cv: CV) -> str:
    lines = [
        '  <main class="cv">',
        '    <header class="hero">',
        f'      <h1 id="person-name">{html.escape(cv.name)}</h1>',
        f'      <div class="role" id="person-role">{html.escape(cv.role)}</div>',
    ]
    for row in cv.contact_rows:
        lines.append('      <div class="contact-row">')
        for contact in row:
            lines.append(
                '        <span class="contact-item">'
                f'<span class="contact-label">{html.escape(contact.label)}:</span> '
                f'{contact_html(contact)}</span>'
            )
        lines.append("      </div>")
    lines.extend(
        [
            "    </header>",
            "",
            '    <section class="section" aria-labelledby="summary-title">',
            '      <h2 class="section-title" id="summary-title">Professional Summary</h2>',
        ]
    )
    for paragraph in cv.summary:
        lines.append(f'      <p class="summary">{inline_html(paragraph)}</p>')
    lines.extend(
        [
            "    </section>",
            "",
            '    <section class="section" aria-labelledby="education-title">',
            '      <h2 class="section-title" id="education-title">Education and certificates</h2>',
            '      <ul class="bullets credentials">',
        ]
    )
    for row in cv.education:
        lines.extend(
            [
                '        <li class="credential split-line">',
                f'          <span class="split-left">{inline_html(row.left)}</span>',
                f'          <span class="split-right">{inline_html(row.right)}</span>',
                "        </li>",
            ]
        )
    lines.extend(
        [
            "      </ul>",
            "    </section>",
            "",
        ]
    )
    
    lines.extend(
        [
            '    <section class="section" aria-labelledby="experience-title">',
            '      <h2 class="section-title" id="experience-title">Experience</h2>',
        ]
    )
    for job in cv.jobs:
        lines.extend(
            [
                '      <article class="job">',
                '        <div class="job-head split-line">',
                f'          <h3 class="job-title split-left">{inline_html(job.title)}</h3>',
                f'          <div class="split-right">{inline_html(job.duration)}</div>',
                "        </div>",
            ]
        )
        index = 0
        while index < len(job.entries):
            kind, value = job.entries[index]
            if kind == "metadata":
                lines.append(f'        <p class="job-meta">{inline_html(str(value))}</p>')
            elif kind == "placeholder":
                lines.append(f"        <p>{html.escape(str(value))}</p>")
            elif kind == "tags":
                if not isinstance(value, tuple):
                    raise SyncError("tag entries must contain a tuple of tag values")
                lines.append('        <div class="tags">')
                for tag in value:
                    lines.append(f'          <span class="tag">{inline_html(tag)}</span>')
                lines.append("        </div>")
            elif kind == "bullet":
                lines.append('        <ul class="bullets">')
                while index < len(job.entries) and job.entries[index][0] == "bullet":
                    lines.append(f"          <li>{inline_html(str(job.entries[index][1]))}</li>")
                    index += 1
                lines.append("        </ul>")
                continue
            else:
                raise SyncError(f"unsupported rendered entry kind: {kind}")
            index += 1
        lines.append("      </article>")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.extend(["    </section>", ""])
    
    # Render projects section if there are any
    if cv.projects:
        lines.extend(
            [
                '    <section class="section" aria-labelledby="projects-title">',
                '      <h2 class="section-title" id="projects-title">Individual Projects</h2>',
            ]
        )
        for project in cv.projects:
            lines.extend(
                [
                    '      <article class="job">',
                    '        <div class="job-head split-line">',
                    f'          <h3 class="job-title split-left">{inline_html(project.title)}</h3>',
                    '        </div>',
                ]
            )
            index = 0
            while index < len(project.entries):
                kind, value = project.entries[index]
                if kind == "metadata":
                    lines.append(f'        <p class="job-meta">{inline_html(str(value))}</p>')
                elif kind == "placeholder":
                    lines.append(f"        <p>{html.escape(str(value))}</p>")
                elif kind == "tags":
                    if not isinstance(value, tuple):
                        raise SyncError("tag entries must contain a tuple of tag values")
                    lines.append('        <div class="tags">')
                    for tag in value:
                        lines.append(f'          <span class="tag">{inline_html(tag)}</span>')
                    lines.append("        </div>")
                elif kind == "bullet":
                    lines.append('        <ul class="bullets">')
                    while index < len(project.entries) and project.entries[index][0] == "bullet":
                        lines.append(f"          <li>{inline_html(str(project.entries[index][1]))}</li>")
                        index += 1
                    lines.append("        </ul>")
                    continue
                else:
                    raise SyncError(f"unsupported rendered entry kind: {kind}")
                index += 1
            lines.append("      </article>")
            lines.append("")
        if lines[-1] == "":
            lines.pop()
        lines.append("    </section>")
        lines.append("")
    
    lines.extend(["  </main>"])
    return "\n".join(lines) + "\n"


def find_main_span(template: str) -> tuple[int, int]:
    """Locate the single top-level CV block with explicit string offsets."""
    opening = '  <main class="cv">'
    start = template.find(opening)
    if start < 0 or template.find(opening, start + len(opening)) >= 0:
        raise SyncError(
            'chanchai.html must contain exactly one two-space-indented <main class="cv"> block'
        )
    closing = '  </main>'
    cursor = start + len(opening)
    close_start = -1
    while cursor < len(template):
        position = template.find(closing, cursor)
        if position < 0:
            break
        if position == 0 or template[position - 1] in "\r\n":
            close_start = position
            break
        cursor = position + len(closing)
    if close_start < 0:
        raise SyncError('chanchai.html has no closing </main> for <main class="cv">')
    end = close_start + len(closing)
    if template.startswith("\r\n", end):
        end += 2
    elif end < len(template) and template[end] in "\r\n":
        end += 1
    elif end < len(template):
        raise SyncError('the CV </main> closing tag must be on its own line')
    if template.find('  <main class="cv">', end) >= 0:
        raise SyncError('chanchai.html must contain only one CV main block')
    return start, end


def normalized_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def render_document(base_text: str, template_text: str) -> str:
    start, end = find_main_span(template_text)
    existing_main = template_text[start:end]
    if existing_main.endswith("\r\n"):
        newline = "\r\n"
    elif existing_main.endswith("\r"):
        newline = "\r"
    else:
        newline = "\n"
    generated_main = render_main(parse_base(base_text)).replace("\n", newline)
    # Preserve the entire HTML/CSS shell byte-for-byte outside the main block.
    return template_text[:start] + generated_main + template_text[end:]


def atomic_write(path: Path, content: str) -> None:
    file_mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as temporary:
            temporary.write(content.encode("utf-8"))
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_name, file_mode)
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[4]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root, help="repository root")
    parser.add_argument("--base", type=Path, help="override base.md path")
    parser.add_argument("--html", dest="html_path", type=Path, help="override chanchai.html path")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true", help="update HTML if it differs")
    action.add_argument("--check", action="store_true", help="read-only parity check (default)")
    parser.add_argument("--diff", action="store_true", help="show a unified diff when out of sync")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_path = args.base or args.root / "base.md"
    html_path = args.html_path or args.root / "chanchai.html"
    try:
        base_text = base_path.read_bytes().decode("utf-8-sig")
        current = html_path.read_bytes().decode("utf-8-sig")
        expected = render_document(base_text, current)
        if args.write:
            if current == expected:
                print(f"UNCHANGED: {html_path} already matches {base_path}")
            else:
                atomic_write(html_path, expected)
                print(f"WROTE: {html_path} now matches {base_path}")
            return 0
        if current == expected:
            print(f"IN SYNC: {html_path} matches {base_path}")
            return 0
        print(
            f"OUT OF SYNC: {html_path} does not match the deterministic rendering of {base_path}",
            file=sys.stderr,
        )
        if args.diff:
            diff = difflib.unified_diff(
                normalized_newlines(current).splitlines(),
                normalized_newlines(expected).splitlines(),
                fromfile=str(html_path),
                tofile=f"{html_path} (expected)",
                lineterm="",
            )
            print("\n".join(diff))
        print("Run with --write to update the HTML.", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, SyncError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
