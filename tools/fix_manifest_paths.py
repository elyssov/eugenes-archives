#!/usr/bin/env python3
"""Repair manifest_*.json files whose chapter.file paths don't match disk reality.

Walks every works/<id>/manifest_*.json, checks each chapter's file path,
and if the file doesn't exist where the manifest claims, searches a few
plausible alternative paths (works/<id>/<lang>/<fname>, etc.) and rewrites
the manifest with the correct path. Idempotent.
"""

import os
import json
import glob

ROOT = r'C:\Projects\eugenes-archives'


def find_chapter_file(work_id, lang, fname):
    candidates = [
        os.path.join('works', work_id, lang, fname),
        os.path.join('works', work_id, fname),
        os.path.join(work_id, lang, fname),
        os.path.join(work_id, fname),
        fname,
    ]
    for c in candidates:
        if os.path.exists(os.path.join(ROOT, c)):
            return c.replace(os.sep, '/')
    return None


def main():
    pattern = os.path.join(ROOT, 'works', '*', 'manifest_*.json')
    for mf in glob.glob(pattern):
        with open(mf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        work_id = data.get('id') or os.path.basename(os.path.dirname(mf))
        lang = data.get('lang', '')
        changed = False
        for ch in data.get('chapters', []):
            fp = ch.get('file', '')
            full = os.path.join(ROOT, fp.replace('/', os.sep))
            if os.path.exists(full):
                continue
            fname = os.path.basename(fp)
            fixed = find_chapter_file(work_id, lang, fname)
            if fixed:
                rel = os.path.relpath(mf, ROOT)
                print(f'  {rel}: {fp}  ->  {fixed}')
                ch['file'] = fixed
                changed = True
            else:
                rel = os.path.relpath(mf, ROOT)
                print(f'  !! MISSING: {rel} : {fp}  (no candidate found)')
        if changed:
            with open(mf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'  SAVED')
    print('Done.')


if __name__ == '__main__':
    main()
