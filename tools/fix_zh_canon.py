# -*- coding: utf-8 -*-
"""Канон транслитерации после правки Юджина (12.06.2026):
  Lyssovsky / Лисовский  → 李索夫斯基 (не 利索夫斯基, не 叶夫根尼·利索夫斯基)
  Aeliss                  → 艾丽丝   (не 艾莉丝)
  Lissovskaya            → 李索夫斯卡娅 (соответствие)
Применить к universes.json и works.json в полях с _zh-суффиксом.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    ('叶夫根尼·利索夫斯基', '李索夫斯基'),
    ('利索夫斯基',          '李索夫斯基'),
    ('利索夫斯卡娅',        '李索夫斯卡娅'),
    ('艾莉丝',              '艾丽丝'),
    ('利索夫斯卡',          '李索夫斯卡'),  # safety, prefix
]

def fix_str(s):
    if not isinstance(s, str):
        return s, 0
    n = 0
    for src, dst in REPLACEMENTS:
        if src in s:
            n += s.count(src)
            s = s.replace(src, dst)
    return s, n

def fix_dict(d):
    total = 0
    for k, v in list(d.items()):
        if isinstance(v, str) and k.endswith('_zh') or k == 'zh':
            new_v, n = fix_str(v)
            if n:
                d[k] = new_v
                total += n
    return total

def main():
    for fname in ('universes.json', 'works.json'):
        path = os.path.join(ROOT, fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        n = 0
        for entry in data:
            n += fix_dict(entry)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'{fname}: {n} замен')

    # И в скриптах-источниках — чтобы при следующем прогоне держался канон.
    for fname in ('tools/add_zh_universes.py', 'tools/add_zh_works.py'):
        path = os.path.join(ROOT, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        n = 0
        for src, dst in REPLACEMENTS:
            n += content.count(src)
            content = content.replace(src, dst)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname}: {n} замен')

if __name__ == '__main__':
    main()
