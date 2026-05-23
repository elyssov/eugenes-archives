#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add "en" to a work's languages list in works.json / universes.json.

Used when adding an English version to a RU-only work. The catalog
already carries English base fields (title, subtitle, description,
author with no suffix), so we only need to flip the languages array.

Usage:  python tools/sync_en_catalog.py <work-id> [<work-id> ...]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGS = ['works.json', 'universes.json']
LANG_ORDER = ['en', 'ru', 'vi']


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def sync(work_id):
    manifest_path = os.path.join(ROOT, 'works', work_id, 'manifest_en.json')
    if not os.path.isfile(manifest_path):
        print('  ! no manifest_en.json for %s -- skipped' % work_id)
        return False

    for catalog in CATALOGS:
        cpath = os.path.join(ROOT, catalog)
        if not os.path.isfile(cpath):
            continue
        data = load(cpath)
        for i, entry in enumerate(data):
            if entry.get('id') != work_id:
                continue
            langs = entry.get('languages', [])
            if 'en' not in langs:
                langs = langs + ['en']
            entry['languages'] = [l for l in LANG_ORDER if l in langs]
            data[i] = entry
            save(cpath, data)
            print('  + %s now lists en in %s' % (work_id, catalog))
            return True
    print('  ! %s not found in any catalog' % work_id)
    return False


if __name__ == '__main__':
    ids = sys.argv[1:]
    if not ids:
        print(__doc__)
        sys.exit(1)
    ok = 0
    for wid in ids:
        if sync(wid):
            ok += 1
    print('Done: %d/%d synced.' % (ok, len(ids)))
