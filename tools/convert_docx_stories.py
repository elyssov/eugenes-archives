#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert DOCX fiction stories to archive format."""

import os
import sys
import json
import re
import docx

# Add parent to path so we can import reparse_all
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reparse_all import split_and_write

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = r"C:\Users\elyss\Downloads\SciFi"

STORIES = [
    {
        "id": "kukla",
        "filename": "kukla-b53402.docx",
        "title_ru": "Кукла",
        "category": "short",
        "genre": "Тёмное фэнтези",
    },
    {
        "id": "zhivaya-dusha",
        "filename": "zhivaya_dusha-b53403.docx",
        "title_ru": "Живая душа",
        "category": "short",
        "genre": "Паранормальный детектив",
    },
    {
        "id": "serv",
        "filename": "serv-b110109.docx",
        "title_ru": "Серв",
        "category": "short",
        "genre": "Социальная фантастика",
    },
    {
        "id": "igra",
        "filename": "igra-b53404.docx",
        "title_ru": "Игра",
        "category": "novella",
        "genre": "Survival horror",
    },
    {
        "id": "kipyatok",
        "filename": "o_polze_kipyatka_v_skorlupe_i_netradicionnykh_metodakh_rybnoj_lovli-b53407.docx",
        "title_ru": "О пользе кипятка в скорлупе",
        "category": "short",
        "genre": "Городское фэнтези",
    },
    {
        "id": "sneg",
        "filename": "sneg-b110111.docx",
        "title_ru": "Снег",
        "category": "short",
        "genre": "Военная мистика",
    },
]


def docx_to_md(filepath):
    """Extract text from DOCX and convert to markdown."""
    doc = docx.Document(filepath)
    lines = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            lines.append("")
            continue

        style_name = para.style.name if para.style else ""

        # Detect headings by style
        if "Heading" in style_name or "heading" in style_name:
            level = 1
            m = re.search(r'(\d)', style_name)
            if m:
                level = int(m.group(1))
            lines.append(f"{'#' * level} {text}")
        elif "Title" in style_name or "title" in style_name:
            lines.append(f"# {text}")
        else:
            # Process inline formatting from runs
            formatted = process_runs(para.runs)
            lines.append(formatted)

    return "\n".join(lines)


def process_runs(runs):
    """Convert paragraph runs to markdown with inline formatting."""
    parts = []
    for run in runs:
        text = run.text
        if not text:
            continue
        if run.bold and run.italic:
            text = f"***{text}***"
        elif run.bold:
            text = f"**{text}**"
        elif run.italic:
            text = f"*{text}*"
        parts.append(text)
    return "".join(parts)


def ensure_h2_title(md_text, title):
    """Ensure the story starts with a ## title for the parser.

    Single-chapter stories need exactly one ## header at the top.
    Convert any # headers to ##, or prepend ## title if none exists.
    """
    lines = md_text.split("\n")
    result = []
    has_h2 = False
    found_first_heading = False

    for line in lines:
        stripped = line.strip()
        # Convert # Heading to ## Heading (but not ## or ### etc.)
        if stripped.startswith("# ") and not stripped.startswith("## "):
            if not found_first_heading:
                result.append(f"## {stripped[2:]}")
                has_h2 = True
                found_first_heading = True
            else:
                # Subsequent # headings become ### (sub-sections within the single chapter)
                result.append(f"### {stripped[2:]}")
        elif stripped.startswith("## ") and not stripped.startswith("### "):
            has_h2 = True
            found_first_heading = True
            result.append(line)
        else:
            result.append(line)

    md_text = "\n".join(result)

    # If no heading was found at all, prepend one
    if not has_h2:
        md_text = f"## {title}\n\n{md_text}"

    return md_text


def process_story(story):
    """Process a single story: DOCX -> MD -> HTML + manifest."""
    work_id = story["id"]
    docx_path = os.path.join(DOWNLOADS, story["filename"])

    if not os.path.exists(docx_path):
        print(f"  ERROR: {docx_path} not found!")
        return False

    # Create directories
    work_dir = os.path.join(BASE, "works", work_id)
    ru_dir = os.path.join(work_dir, "ru")
    os.makedirs(ru_dir, exist_ok=True)

    # Extract DOCX to MD
    print(f"  Extracting DOCX...")
    md_text = docx_to_md(docx_path)

    # Clean up excessive blank lines
    md_text = re.sub(r"\n{3,}", "\n\n", md_text)

    # Remove metadata block (Название, Автор, Ссылка lines at top)
    md_text = re.sub(
        r"^\s*\*\*Название:\*\*.*\n\*\*Автор\(-ы\):\*\*.*\n\*\*Ссылка:\*\*.*\n*",
        "",
        md_text,
    )

    # Convert dialogue dashes: "- " at start of line to em-dash "— "
    # This prevents the MD parser from treating dialogue as list items
    md_text = re.sub(r"^(\s*)- ", r"\1" + "\u2014 ", md_text, flags=re.MULTILINE)

    # Ensure each paragraph is separated by a blank line
    # (some DOCX exports have consecutive non-empty lines that should be separate paragraphs)
    new_lines = []
    prev_was_text = False
    for line in md_text.split("\n"):
        stripped = line.strip()
        is_text = stripped != "" and not stripped.startswith("#")
        if is_text and prev_was_text:
            new_lines.append("")  # insert blank line between paragraphs
        new_lines.append(line)
        prev_was_text = is_text
    md_text = "\n".join(new_lines)

    # Clean up excessive blank lines again after paragraph separation
    md_text = re.sub(r"\n{3,}", "\n\n", md_text)

    # Ensure proper ## title
    md_text = ensure_h2_title(md_text, story["title_ru"])

    # Save source MD
    source_path = os.path.join(work_dir, "source_ru.md")
    with open(source_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    print(f"  Saved {source_path}")

    # Run parser
    n = split_and_write(work_id, "ru", source_path)
    print(f"  Generated {n} section(s)")

    # Create manifest
    manifest_path = os.path.join(work_dir, "manifest_ru.json")
    # Read back what split_and_write created to get chapters
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Enrich manifest with full metadata
    manifest.update({
        "id": work_id,
        "title": story["title_ru"],
        "author": "Евгений Лисовский",
        "date": "2020-2024",
        "category": story["category"],
        "genre": story["genre"],
        "lang": "ru",
        "original_lang": "ru",
    })

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"  Manifest: {manifest_path}")

    return True


if __name__ == "__main__":
    for story in STORIES:
        print(f"\n=== {story['id']}: {story['title_ru']} ===")
        process_story(story)

    print("\n--- Done! ---")
