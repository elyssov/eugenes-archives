#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert DOCX fiction stories to MD source files and run parser."""

import docx
import os
import json
import sys
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'tools'))
from reparse_all import split_and_write


def docx_to_md(docx_path, chapter_names_as_headers=None):
    """Convert DOCX to markdown string.

    chapter_names_as_headers: list of standalone line texts that should become ## headers
    """
    doc = docx.Document(docx_path)
    lines = []
    skip_metadata = True

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        style_name = p.style.name if p.style else 'Normal'

        # Skip first few metadata lines (Название, Автор, Ссылка, blank)
        if skip_metadata:
            if i < 4:
                continue
            skip_metadata = False

        # Convert Heading styles to ## (for parser compatibility)
        if 'Heading' in style_name:
            lines.append('')
            lines.append(f'## {text}')
            lines.append('')
            continue

        # Check for standalone chapter name lines
        if chapter_names_as_headers and text in chapter_names_as_headers:
            lines.append('')
            lines.append(f'## {text}')
            lines.append('')
            continue

        # Handle bold/italic runs
        if p.runs:
            parts = []
            for run in p.runs:
                t = run.text
                if not t:
                    continue
                if run.bold and run.italic:
                    t = f'***{t}***'
                elif run.bold:
                    t = f'**{t}**'
                elif run.italic:
                    t = f'*{t}*'
                parts.append(t)
            rich_text = ''.join(parts)
            # Clean up adjacent formatting markers
            rich_text = re.sub(r'\*\*\*\*\*\*', '', rich_text)  # empty bold+italic
            rich_text = re.sub(r'\*\*\*\*', '', rich_text)  # adjacent bold markers
            rich_text = re.sub(r'\*\*\s*\*\*', ' ', rich_text)  # bold space bold
            rich_text = re.sub(r'\*\s*\*', ' ', rich_text)  # italic space italic
            lines.append(rich_text)
        else:
            lines.append(text)

    # Clean up: remove excessive blank lines
    result = '\n'.join(lines)
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    return result.strip() + '\n'


def create_manifest(work_id, title, category, genre, chapters_data):
    """Create manifest_ru.json for a work."""
    manifest = {
        "id": work_id,
        "title": title,
        "author": "Евгений Лисовский",
        "date": "2020-2024",
        "category": category,
        "genre": genre,
        "lang": "ru",
        "chapters": chapters_data
    }
    mpath = os.path.join(BASE, 'works', work_id, 'manifest_ru.json')
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return mpath


STORIES = [
    {
        'id': 'vechnyj-gorod',
        'filename': 'vechnyj_gorod_probuzhdenie-b53484.docx',
        'title_ru': 'Вечный Город: Пробуждение',
        'category': 'short',
        'genre': 'Эпик-фэнтези',
    },
    {
        'id': 'blagoslovennaya-eres',
        'filename': 'blagoslovennaya_eres-b53469.docx',
        'title_ru': 'Благословенная ересь',
        'category': 'novella',
        'genre': 'Warhammer 40K фанфикшн',
    },
    {
        'id': 'jeloustoun',
        'filename': 'jeloustoun_nazvanie_rabochee-b115630.docx',
        'title_ru': 'Йеллоустоун',
        'category': 'novella',
        'genre': 'Катастрофа',
    },
    {
        'id': 'kogda-gasnet-zvezda',
        'filename': 'kogda_gasnet_zvezda-b53545.docx',
        'title_ru': 'Когда гаснет звезда',
        'category': 'novella',
        'genre': 'Hard SF',
    },
    {
        'id': 'arkhivy-shpenglera',
        'filename': 'arkhivy_fon_shpenglera_kaschej-b53467.docx',
        'title_ru': 'Архивы фон Шпенглера: Кащей',
        'category': 'novel',
        'genre': 'Городское фэнтези / уютный хоррор',
        'chapter_names': ['Три месяца спустя'],
    },
    {
        'id': 'khroniki-zolotogo-dola',
        'filename': 'khroniki_zolotogo_dola_zhiznennoe_prostranstvo-b53538.docx',
        'title_ru': 'Хроники Золотого Дола',
        'category': 'novel',
        'genre': 'Фантастика',
    },
]


if __name__ == '__main__':
    src_dir = 'C:/Users/elyss/Downloads/SciFi'

    for story in STORIES:
        work_id = story['id']
        docx_path = os.path.join(src_dir, story['filename'])
        work_dir = os.path.join(BASE, 'works', work_id)
        os.makedirs(work_dir, exist_ok=True)

        print(f'\n=== {work_id} ===')

        # Convert DOCX to MD
        chapter_names = story.get('chapter_names', None)
        md_content = docx_to_md(docx_path, chapter_names)

        source_path = os.path.join(work_dir, 'source_ru.md')
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f'  MD written: {source_path} ({len(md_content)} chars)')

        # Run parser
        n_sections = split_and_write(work_id, 'ru', source_path)
        print(f'  Parsed: {n_sections} sections')

        # Read back chapters from manifest to get chapter data
        mpath = os.path.join(work_dir, 'manifest_ru.json')
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # Enhance manifest with full metadata
        manifest['title'] = story['title_ru']
        manifest['author'] = 'Евгений Лисовский'
        manifest['date'] = '2020-2024'
        manifest['category'] = story['category']
        manifest['genre'] = story['genre']

        with open(mpath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'  Manifest: {mpath}')

    print('\nDone!')
