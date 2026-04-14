#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Re-parse all works from source MD into clean HTML with proper formatting."""

import re
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def md_to_html(text):
    """Convert markdown to well-formatted HTML."""
    lines = text.split('\n')
    out = []
    para = []
    in_blockquote = False
    bq_lines = []
    in_table = False
    table_rows = []

    def flush_para():
        if para:
            t = ' '.join(para)
            t = inline(t)
            out.append(f'<p>{t}</p>')
            para.clear()

    def flush_bq():
        nonlocal in_blockquote
        if bq_lines:
            content = '\n'.join(bq_lines)
            # Detect Aeliss notes
            is_aeliss = any(x in content[:80] for x in ['[Aeliss', '[Аэлисс', '[A.]', '[El:', '[Эль:'])
            cls = 'authors-note' if is_aeliss else 'blockquote-text'
            # Process paragraphs within blockquote
            bq_paras = []
            cur = []
            for bl in bq_lines:
                if bl.strip() == '':
                    if cur:
                        bq_paras.append(' '.join(cur))
                        cur = []
                else:
                    cur.append(bl)
            if cur:
                bq_paras.append(' '.join(cur))

            inner = '\n'.join(f'<p>{inline(p)}</p>' for p in bq_paras)
            out.append(f'<div class="{cls}">\n{inner}\n</div>')
            bq_lines.clear()
        in_blockquote = False

    def flush_table():
        nonlocal in_table
        if not table_rows:
            in_table = False
            return
        cols = max(len(r) for r in table_rows)
        html = '<div class="table-wrapper"><table>\n'
        for i, row in enumerate(table_rows):
            tag = 'th' if i == 0 else 'td'
            html += '<tr>'
            for j, cell in enumerate(row):
                if j < cols:
                    html += f'<{tag}>{inline(cell.strip())}</{tag}>'
            html += '</tr>\n'
        html += '</table></div>'
        out.append(html)
        table_rows.clear()
        in_table = False

    def inline(t):
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
        t = re.sub(r'`([^`]+?)`', r'<code>\1</code>', t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        return t

    for line in lines:
        s = line.strip()

        # Tables
        if '|' in s and s.startswith('|') and s.endswith('|'):
            flush_para()
            if in_blockquote:
                flush_bq()
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(set(c) <= set('-| :') for c in cells):
                continue  # separator row
            if not in_table:
                in_table = True
            table_rows.append(cells)
            continue
        elif in_table:
            flush_table()

        # Blockquotes
        if s.startswith('> ') or s == '>':
            flush_para()
            if not in_blockquote:
                in_blockquote = True
            content = s[2:] if s.startswith('> ') else ''
            bq_lines.append(content)
            continue
        elif in_blockquote:
            # Empty line inside blockquote = paragraph break
            if s == '':
                bq_lines.append('')
                continue
            # Non-quote line = end of blockquote
            flush_bq()

        # Empty line
        if s == '':
            flush_para()
            continue

        # Horizontal rules
        if s in ['---', '***', '* * *'] or re.match(r'^[-=*~]{5,}$', s):
            flush_para()
            out.append('<hr class="section-break">')
            continue

        # Headers
        if s.startswith('#### '):
            flush_para()
            out.append(f'<h4>{inline(s[5:])}</h4>')
            continue
        if s.startswith('### '):
            flush_para()
            out.append(f'<h3>{inline(s[4:])}</h3>')
            continue
        if s.startswith('## '):
            flush_para()
            out.append(f'<h2>{inline(s[3:])}</h2>')
            continue
        if s.startswith('# '):
            flush_para()
            out.append(f'<h1>{inline(s[2:])}</h1>')
            continue

        # Author's note markers
        if s.startswith('*(Author') or s.startswith('*(Примечание'):
            flush_para()
            note = s.strip('*').strip('(').rstrip(')').rstrip('*')
            out.append(f'<div class="authors-note"><p><em>{inline(note)}</em></p></div>')
            continue

        # List items
        if s.startswith('- ') or s.startswith('• '):
            flush_para()
            out.append(f'<li>{inline(s[2:])}</li>')
            continue

        # Numbered items
        m = re.match(r'^(\d+)[.)]\s+(.*)', s)
        if m:
            flush_para()
            out.append(f'<p class="numbered"><span class="num">{m.group(1)}.</span> {inline(m.group(2))}</p>')
            continue

        # Regular text
        para.append(s)

    flush_para()
    if in_blockquote:
        flush_bq()
    if in_table:
        flush_table()

    # Wrap consecutive <li> in <ul>
    html = '\n'.join(out)
    html = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html)

    return html


def split_and_write(work_id, lang, source_path):
    """Split source MD by ## headers and write HTML chapters."""
    with open(source_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by ## headers only
    sections = []
    title = 'Introduction'
    current = []

    for line in text.split('\n'):
        if line.startswith('## ') and not line.startswith('### '):
            if current:
                sections.append((title, '\n'.join(current)))
            title = line[3:].strip()
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append((title, '\n'.join(current)))

    # If first section is just title/metadata with < 500 chars, merge with second
    if len(sections) > 1 and len(sections[0][1]) < 500:
        merged = sections[0][1] + '\n\n' + sections[1][1]
        sections = [(sections[1][0], merged)] + sections[2:]

    # Write
    outdir = os.path.join(BASE, 'works', work_id, lang)
    os.makedirs(outdir, exist_ok=True)
    # Clear old
    for f in os.listdir(outdir):
        if f.endswith('.html'):
            os.remove(os.path.join(outdir, f))

    chapters = []
    for i, (sec_title, content) in enumerate(sections):
        html = md_to_html(content)
        fname = f'section_{i+1:02d}.html'
        with open(os.path.join(outdir, fname), 'w', encoding='utf-8') as f:
            f.write(html)
        chapters.append({
            'id': f'section_{i+1:02d}',
            'title': sec_title,
            'file': f'works/{work_id}/{lang}/{fname}'
        })

    # Update manifest
    mpath = os.path.join(BASE, 'works', work_id, f'manifest_{lang}.json')
    if os.path.exists(mpath):
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        manifest['chapters'] = chapters
    else:
        manifest = {'id': work_id, 'lang': lang, 'chapters': chapters}

    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return len(sections)


if __name__ == '__main__':
    works = [
        ('ich-paper', 'en', 'works/ich-paper/source_en.md'),
        ('trap-of-safety', 'en', 'works/trap-of-safety/source_en.md'),
        ('black-box', 'en', 'works/black-box/source_en.md'),
        ('i-have-a-dream', 'en', 'works/i-have-a-dream/source_en.md'),
        ('in-memoriam', 'en', 'works/in-memoriam/source_en.md'),
        ('pentagon', 'en', 'works/pentagon/source_en.md'),
        ('prayers', 'en', 'works/prayers/source_en.md'),
        ('pereira', 'en', 'works/pereira/source_en.md'),
        # RU translations (Lara's)
        ('pereira', 'ru', 'works/pereira/source_ru_lara.md'),
        ('pentagon', 'ru', 'works/pentagon/source_ru_lara.md'),
        ('i-have-a-dream', 'ru', 'works/i-have-a-dream/source_ru_lara.md'),
        ('trap-of-safety', 'ru', 'works/trap-of-safety/source_ru_lara.md'),
    ]

    for work_id, lang, src in works:
        path = os.path.join(BASE, src)
        if os.path.exists(path):
            n = split_and_write(work_id, lang, path)
            print(f'{work_id} ({lang}): {n} sections')
        else:
            print(f'{work_id} ({lang}): SOURCE MISSING')
