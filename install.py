#!/usr/bin/env python3
"""Link argstack skills into one agent's skills directory. Python 3.9+."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
BUNDLED = {p.parent.name: p.parent for p in sorted((ROOT/'skills').glob('*/SKILL.md'))}
EXTERNAL = json.loads((ROOT/'external-skills.json').read_text())


def resolve_external(name):
    item = EXTERNAL[name]
    cache = Path(os.environ.get('XDG_CACHE_HOME') or Path.home()/'.cache')/'argstack'/item['sha256']/name
    path = cache/'SKILL.md'
    if not path.exists():
        with urllib.request.urlopen(item['source'], timeout=30) as response:
            data = response.read(1024*1024)
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise SystemExit(f'{name}: upstream integrity check failed')
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=cache, delete=False) as handle:
            handle.write(data)
        os.replace(handle.name, path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit(f'{name}: existing cached file differs; no link created')
    return cache.resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*', help='skills to install (default: all bundled)')
    parser.add_argument('--all', action='store_true', help='include the pinned upstream-only skill')
    parser.add_argument('--list', action='store_true', help='show catalog; no changes')
    parser.add_argument('--target', type=Path, help='agent skills directory')
    args = parser.parse_args()
    if args.list:
        print('\n'.join([*BUNDLED, *(f'{name} (upstream)' for name in EXTERNAL)])); return
    if args.target is None: parser.error('pass --target to choose a skills directory')
    if args.all and args.names: parser.error('choose named skills or --all')
    names = list(dict.fromkeys(args.names or [*BUNDLED, *(EXTERNAL if args.all else ())]))
    unknown = set(names) - BUNDLED.keys() - EXTERNAL.keys()
    if unknown: parser.error('unknown skills: '+', '.join(sorted(unknown)))
    target = args.target.expanduser().resolve()
    sources = {name:BUNDLED[name] if name in BUNDLED else resolve_external(name) for name in names}
    todo = []
    for name, src in sources.items():
        link = target/name
        if os.path.lexists(link):
            if link.is_symlink() and link.resolve() == src: continue
            raise SystemExit(f'Existing skill at {link}; no links changed.')
        todo.append((link,src))
    target.mkdir(parents=True,exist_ok=True)
    created = []
    try:
        for link,src in todo:
            link.symlink_to(src,target_is_directory=True); created.append(link)
    except OSError:
        for link in reversed(created): link.unlink()
        raise
    print(f'{len(names)} skills ready; {len(created)} new links in {target}')
if __name__=='__main__':main()
