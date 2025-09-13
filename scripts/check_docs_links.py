#!/usr/bin/env python3
import os, re, sys
from pathlib import Path

ROOT = Path('/home/yanchao/simplex-engine')
DOCS = ROOT / 'docs'

link_re = re.compile(r"\[.*?\]\(([^)]+)\)")

broken = []
checked = 0

for md in DOCS.rglob('*.md'):
    try:
        text = md.read_text()
    except Exception as e:
        print(f"ERROR reading {md}: {e}")
        continue
    for m in link_re.finditer(text):
        raw = m.group(1).strip()
        # ignore external
        if raw.startswith('http://') or raw.startswith('https://') or raw.startswith('mailto:'):
            continue
        if raw.startswith('#'):
            continue
        # strip title part like 'file.md" "title' (rare) and query
        if '"' in raw:
            raw = raw.split('"')[0].strip()
        if '?' in raw:
            raw = raw.split('?')[0]
        # split anchor
        path_part = raw.split('#')[0]
        if not path_part:
            continue
        # handle absolute-like starting with / -> relative to repo root
        if path_part.startswith('/'):
            target = ROOT / path_part.lstrip('/')
        else:
            target = (md.parent / path_part).resolve()
        checked += 1
        ok = False
        if target.exists():
            ok = True
        else:
            # try adding README.md if target is directory or target refers to directory path
            if (target / 'README.md').exists():
                ok = True
            elif target.with_suffix('.md').exists():
                ok = True
            else:
                ok = False
        if not ok:
            broken.append((str(md.relative_to(ROOT)), path_part, str(target.relative_to(ROOT))))

# Print results
if broken:
    print('Broken links found:')
    for src, link, resolved in broken:
        print(f'- {src} -> {link} (resolved: {resolved})')
    print(f'\nChecked {checked} links; {len(broken)} broken.')
    sys.exit(2)
else:
    print(f'No broken links found across docs (checked {checked} links).')
    sys.exit(0)
