"""Run with Python 3 or blender -b --python validate_kit.py. Read-only portable-data check."""
from pathlib import Path
import json, struct
ROOT=Path(__file__).resolve().parent
errors=[]; sets={}; files=set(); shots={}; used_cards=set()
for p in (ROOT/'data/sets').glob('*.json'):
    S=json.loads(p.read_text()); sets[p.stem]={m['id'] for m in S['meshes']}
    for m in S['meshes']:
        files.add(ROOT/'data/geo'/(m['geo']+'.json'))
        for mt in m['mats']:
            for t in [mt.get('map'),mt.get('emap')]:
                if t: files.add(ROOT/'data/tex'/(t['id']+'.png'))
for f in range(3995):
    p=ROOT/'data/frames'/f'f{f:04d}.json'
    if not p.exists(): errors.append(str(p));continue
    F=json.loads(p.read_text());shots[F['shot']]=shots.get(F['shot'],0)+1
    if F['f']!=f: errors.append(f'wrong frame id {f}')
    for d in F['dyn']+F['geos']:
        if d['id'] not in sets[F['set']]:errors.append(f'{f}: unknown mesh {d["id"]}')
    for c in F['cards']:files.add(ROOT/'data/cards'/c['img']);used_cards.add(c['img'])
    for c in F['sprites']:files.add(ROOT/'data/sprites'/c['img'])
    for c in F['texs']:files.add(ROOT/'data/tex'/c['img'])
for p in files:
    if not p.is_file() or not p.stat().st_size:errors.append(str(p))
for p in (ROOT/'assets/models').glob('*/*.gltf'):
    g=json.loads(p.read_text())
    for x in g.get('buffers',[])+g.get('images',[]):
        uri=x.get('uri','')
        if uri and not uri.startswith('data:') and not (p.parent/uri).is_file():errors.append(str(p.parent/uri))
if errors:raise RuntimeError('\n'.join(errors[:40])+f'\n{len(errors)} validation failures')
print(f'PASS: 3995 frames, {len(shots)} shots, {len(sets)} sets, {len(files)} referenced files, {len(used_cards)} character images; all glTF dependencies present.')
