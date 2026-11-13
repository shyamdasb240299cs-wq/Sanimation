"""Rejoin asset files that were split to fit GitHub's 100 MB file limit (e.g. jacaranda_tree.bin.part00..02).
Run once: blender -b --python rejoin_parts.py   (or: python rejoin_parts.py). Safe to re-run."""
import os, glob
ROOT = os.path.dirname(os.path.abspath(__file__))
done = 0
for first in glob.glob(os.path.join(ROOT, 'assets', '**', '*.part00'), recursive=True):
    target = first[:-len('.part00')]
    parts = sorted(glob.glob(target + '.part[0-9][0-9]'))
    if os.path.exists(target) and os.path.getsize(target) == sum(os.path.getsize(p) for p in parts):
        continue
    with open(target + '.tmp', 'wb') as out:
        for p in parts:
            with open(p, 'rb') as f: out.write(f.read())
    os.replace(target + '.tmp', target); done += 1
    print('rejoined', os.path.relpath(target, ROOT), len(parts), 'parts')
print('rejoin_parts: OK,', done, 'file(s) rebuilt')
