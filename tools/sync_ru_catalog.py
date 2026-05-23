#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync a work's Russian metadata into the catalog (works.json / universes.json).

For the given work id, reads works/<id>/manifest_ru.json and:
  - adds "ru" to the catalog entry's "languages" list (kept in en, ru, vi order),
  - sets title_ru / subtitle_ru / description_ru / author_ru from the manifest,
  - inserts the *_ru keys right after their base counterparts.

The manifest_ru.json is the single source of truth for the Russian title,
subtitle and description, so translations live in exactly one place.

Usage:  python tools/sync_ru_catalog.py <work-id> [<work-id> ...]
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


def insert_after(entry, anchor, key, value):
    """Return a new dict with key=value placed right after `anchor`."""
    out = {}
    for k, v in entry.items():
        if k == key:
            continue
        out[k] = v
        if k == anchor:
            out[key] = value
    if key not in out:
        out[key] = value
    return out


def sync(work_id):
    manifest_path = os.path.join(ROOT, 'works', work_id, 'manifest_ru.json')
    if not os.path.isfile(manifest_path):
        print('  ! no manifest_ru.json for %s -- skipped' % work_id)
        return False
    m = load(manifest_path)

    for catalog in CATALOGS:
        cpath = os.path.join(ROOT, catalog)
        if not os.path.isfile(cpath):
            continue
        data = load(cpath)
        for i, entry in enumerate(data):
            if entry.get('id') != work_id:
                continue
            langs = entry.get('languages', [])
            if 'ru' not in langs:
                langs = langs + ['ru']
            entry['languages'] = [l for l in LANG_ORDER if l in langs]
            for field in ('title', 'subtitle', 'description', 'author'):
                if not m.get(field):
                    continue
                anchor = field  # always insert ru right after the base field
                entry = insert_after(entry, anchor, field + '_ru', m[field])
            data[i] = entry
            save(cpath, data)
            print('  + %s synced into %s' % (work_id, catalog))
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
