from pathlib import Path
root=Path(__file__).resolve().parent.parent/'frames'
bad=[]
for f in range(3755):
 p=root/f'f{f:04d}.jpg'
 if not p.exists() or p.stat().st_size<3:bad.append(f);continue
 with p.open('rb') as fp:
  fp.seek(-2,2)
  if fp.read()!=b'\xff\xd9':bad.append(f)
if bad:raise SystemExit('Missing/incomplete frames: '+','.join(map(str,bad[:40]))+f' ({len(bad)} total)')
print('All 3755 JPEGs present and complete.')
