"""Render frames of 'Elon for a Day' from film.blend + data/ (resumable).
   blender -b film.blend --python render_frames.py -- --start 0 --end 3994 --engine CYCLES --samples 96 --out frames
Skips frames that already exist, so re-running continues where it stopped."""
import bpy, json, os, sys, math, time, base64, hashlib
import numpy as np
from mathutils import Matrix, Vector, Quaternion, Euler

KIT = os.path.dirname(os.path.abspath(bpy.data.filepath)); DATA = os.path.join(KIT, 'data'); ASSETS = os.path.join(KIT, 'assets')
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
A = {'start': 0, 'end': 3994, 'engine': 'CYCLES', 'samples': 96, 'out': os.path.join(KIT, 'frames'), 'step': 1, 'res': 100, 'only': ''}
for i in range(0, len(argv) - 1, 2): A[argv[i].lstrip('-')] = argv[i + 1]
for k in ('start', 'end', 'samples', 'step', 'res'): A[k] = int(A[k])
DATA = os.path.abspath(A.get('data', DATA))
os.makedirs(A['out'], exist_ok=True)
sc = bpy.context.scene; sc.render.resolution_percentage = A['res']
if A.get('view'):
    sc.view_settings.view_transform = A['view']
    if A['view'] == 'AgX': sc.view_settings.look = 'AgX - Medium High Contrast'
if A['engine'].upper() == 'CYCLES':
    sc.render.engine = 'CYCLES'; sc.cycles.samples = A['samples']
    pr = bpy.context.preferences.addons['cycles'].preferences; dev = None
    for t in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI', 'METAL'):
        try:
            pr.compute_device_type = t; pr.get_devices()
            if any(d.type == t for d in pr.devices): dev = t; break
        except Exception: pass
    if dev:
        for d in pr.devices: d.use = d.type in (dev, 'CPU') if dev != 'OPTIX' else d.type == 'OPTIX'
        sc.cycles.device = 'GPU'; sc.cycles.denoiser = 'OPTIX' if dev == 'OPTIX' else 'OPENIMAGEDENOISE'
    if not dev:
        sc.cycles.device = 'CPU'
        if A.get('require-gpu') == '1': raise RuntimeError('No supported GPU found. Select OptiX/CUDA and update the NVIDIA driver before the full render.')
    print('Cycles device:', dev or 'CPU')
else:
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = A['samples'] if A['samples'] < 64 else 24

def hexc(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c]
def to_mat(e): return Matrix([[e[0], e[4], e[8], e[12]], [e[1], e[5], e[9], e[13]], [e[2], e[6], e[10], e[14]], [e[3], e[7], e[11], e[15]]])
def b2v(p): return Vector((p[0], -p[2], p[1]))  # three.js world -> Blender world
IMGS = {}
def load(path):
    im = IMGS.get(path)
    if im is None:
        im = bpy.data.images.load(path, check_existing=True); IMGS[path] = im
    return im
def trim_images(keep=24):
    # free character/sprite/screen images that are no longer shown (each card image is ~10 MB in RAM)
    for k in list(IMGS):
        if '/hdri/' in k: continue
        im = IMGS[k]
        if im.users == 0: bpy.data.images.remove(im); IMGS.pop(k)

OBJ = {o.name: o for o in bpy.data.objects}
SETC = {c.name[4:]: c for c in bpy.data.collections if c.name.startswith('set_')}
CARDS = sorted([o for o in bpy.data.objects if o.name.startswith('card_')], key=lambda o: o.name)
SPRS = sorted([o for o in bpy.data.objects if o.name.startswith('spr_')], key=lambda o: o.name)
PUFFS = sorted([o for o in bpy.data.objects if o.name.startswith('puff_')], key=lambda o: o.name)
BLOBS = sorted([o for o in bpy.data.objects if o.name.startswith('blob_')], key=lambda o: o.name)
PRAC = [OBJ[f'prac_{i}'] for i in range(4)]
CAM, SUN, ROOT = OBJ['CAM'], OBJ['SUN'], OBJ['Y_UP']
FILL = OBJ.get('FILL')
if FILL is None:
    FILL = bpy.data.objects.new('FILL', bpy.data.lights.new('FILL', 'AREA')); sc.collection.objects.link(FILL); FILL.parent = CAM
    FILL.data.shape = 'DISK'; FILL.data.size = 6.0; FILL.location = (0, 0.6, 1.2); FILL.data.use_shadow = False
    FILL.visible_camera = False; FILL.visible_glossy = False
sc.view_settings.exposure = 0.12
def _getmat(name, col, emit=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = col; b.inputs['Roughness'].default_value = 1.0
    if emit: b.inputs['Emission Color'].default_value = col; b.inputs['Emission Strength'].default_value = emit
    return m
MAT_PUFF, MAT_PUFFD, MAT_FIRE = _getmat('puff', (0.92, 0.9, 0.88, 1)), _getmat('puff_dark', (0.12, 0.1, 0.11, 1)), _getmat('fire', (1.0, 0.45, 0.08, 1), 12.0)
TEXNODES = {}
for m in bpy.data.materials:
    if m.node_tree:
        for n in m.node_tree.nodes:
            if n.name.startswith('tex_'): TEXNODES.setdefault(n.name[4:], []).append(n)
WATER = [m.node_tree.nodes['water_noise'] for m in bpy.data.materials if m.get('kind') == 'water']
W = sc.world.node_tree.nodes; HDRI_AZ = json.loads(sc.world['hdri_az'])
P = sc.compositing_node_group.nodes
# light preset (identified by sky colour) -> HDRI and world strength
SKY = {'#7fb2e6': ('kloofendal_48d_partly_cloudy_puresky', 0.55), '#3f7fd2': ('kloofendal_48d_partly_cloudy_puresky', 0.6), '#6c78c0': ('qwantani_late_afternoon_puresky', 0.6),
       '#6ea2dc': ('kloofendal_48d_partly_cloudy_puresky', 0.5), '#070b1e': ('qwantani_night_puresky', 1.2), '#0d0a1c': (None, 0.25), '#2a0c12': (None, 0.25),
       '#5a62b4': ('qwantani_sunset_puresky', 0.65), '#2f8ae0': ('kloofendal_48d_partly_cloudy_puresky', 0.65), '#03040c': ('qwantani_night_puresky', 0.4), '#0d1324': (None, 0.3)}

GRIP_HANDS = [o for o in bpy.data.objects if o.get('motion_marker')]
PRESS_HANDS = {o['sprite_key']:o for o in bpy.data.objects if o.get('sprite_key')}
PALM_LOCAL = Matrix.Translation(Vector((.006,-.03,-.022))) @ Matrix.Diagonal((1,1.15,.5,1))
PALM_INV = PALM_LOCAL.inverted()
def hand_visible(root, visible):
    for child in root.children_recursive: child.hide_render = not visible
DRESS_ROOTS = [o for o in bpy.data.objects if o.get('asset_id')]
state = {'set': None, 'touched': set()}
def reset_obj(o):
    o.matrix_basis = to_mat(o['base_m']); o.hide_render = not o['base_vis']
def apply_frame(F):
    s = F['set']
    if s != state['set']:
        for lc in sc.view_layers[0].layer_collection.children:
            if lc.name.startswith('set_'): lc.exclude = lc.name[4:] != s
        for n in state['touched']: reset_obj(OBJ[n])
        state['touched'] = set(); state['set'] = s
    cur = {d['id'] for d in F['dyn']}
    for n in state['touched'] - cur: reset_obj(OBJ[n])
    for d in F['dyn']:
        o = OBJ.get(d['id'])
        if o: o.matrix_basis = to_mat(d['m']); o.hide_render = not d['v']
    state['touched'] = cur
    for g in F['geos']:  # vertex-animated geometry (receipt)
        o = OBJ.get(g['id']); me = o.data
        pos = np.frombuffer(base64.b64decode(g['pos']), np.float32)
        if len(pos) == len(me.vertices) * 3: me.vertices.foreach_set('co', pos); me.update()
    for t in F['texs']:
        for n in TEXNODES.get(t['id'], []): n.image = load(os.path.join(DATA, 'tex', t['img']))
    # Continuous Blender skin follows the same device motion as its exported marker.
    for root in GRIP_HANDS:
        marker = OBJ[root['motion_marker']]
        visible = root['source_set'] == s and not marker.hide_render
        root.matrix_basis = marker.matrix_basis @ PALM_INV
        hand_visible(root, visible)
        for legacy in json.loads(root['legacy_ids']): OBJ[legacy].hide_render = True
    for root in PRESS_HANDS.values(): hand_visible(root, False)
    # camera
    CAM.matrix_basis = to_mat(F['cam']['m']); CAM.data.lens = (CAM.data.sensor_height / 2) / math.tan(math.radians(F['cam']['fov']) / 2)
    # sun + sky
    L = F['L']; d = b2v(F['sun']['dir']).normalized()
    SUN.rotation_mode = 'QUATERNION'; SUN.rotation_quaternion = d.to_track_quat('Z', 'Y'); SUN.data.energy = F['sun']['i'] * 0.82; SUN.data.color = hexc(F['sun']['c'])
    hd, st = SKY.get(L['skyTop'], ('kloofendal_48d_partly_cloudy_puresky', 0.5))
    if hd:
        W['env'].image = load(os.path.join(ASSETS, 'hdri', hd + '.hdr')); W['bg'].inputs['Strength'].default_value = st * L.get('envI', 1)
        u = HDRI_AZ.get(hd + '.hdr', 0) / (2 * math.pi); az = math.atan2(d.y, -d.x); W['envrot'].inputs['Rotation'].default_value = (0, 0, az - 2 * math.pi * (u - 0.5))
        sc.world.node_tree.links.new(W['env'].outputs['Color'], W['bg'].inputs['Color'])
    else:
        for l in list(sc.world.node_tree.links):
            if l.to_node == W['bg'] and l.to_socket.name == 'Color': sc.world.node_tree.links.remove(l)
        W['bg'].inputs['Color'].default_value = (*hexc(L['envTop']), 1); W['bg'].inputs['Strength'].default_value = st
    amb = (L.get('envI', 1) * 0.7 + L.get('hemi', 0.3)) * (1.0 if L['skyTop'] in ('#7fb2e6', '#6ea2dc', '#0d1324', '#0d0a1c', '#2a0c12') else 0.45)
    FILL.data.energy = 1050 * amb; FILL.data.color = hexc(L.get('envHor', '#ffffff'))
    for i, l in enumerate(PRAC):
        if i < len(F['prac']):
            p = F['prac'][i]; l.hide_render = False; l.location = Vector((p['p'][0], p['p'][1], p['p'][2])); l.data.energy = p['i'] * 4 * math.pi * 0.8; l.data.color = hexc(p['c'])
            l.data.use_custom_distance = True; l.data.cutoff_distance = p['d']
        else: l.hide_render = True
    # characters (cards) + contact shadows
    el = math.radians(L['el']); diffk = 0.5 * math.pi / (F['sun']['i'] * max(0.15, math.sin(el)) + 1.0)
    bi = 0
    for i, o in enumerate(CARDS):
        if i >= len(F['cards']): o.hide_render = True; continue
        c = F['cards'][i]; o.hide_render = False; nt = o.active_material.node_tree
        nt.nodes['img'].image = load(os.path.join(DATA, 'cards', c['img']))
        o.matrix_basis = Matrix.Translation(Vector(c['p'])) @ Euler((0, c['ry'], c['rz']), 'XYZ').to_matrix().to_4x4() @ Matrix.Diagonal((c['s'], c['s'], c['s'], 1))
        nt.nodes['tint'].outputs[0].default_value = (*[.45+.55*v for v in hexc(c['tint'])], 1); nt.nodes['opacity'].outputs[0].default_value = c['alpha']
        nt.nodes['litmix'].inputs['Fac'].default_value = 0.14 if c['lit'] else 0.0; nt.nodes['emit'].outputs[0].default_value = 0.92 if c['lit'] else 1.0; nt.nodes['diffk'].outputs[0].default_value = diffk * 0.65
        o.visible_shadow = c['cast']
        if c['blob'] and bi < len(BLOBS):
            b = BLOBS[bi]; bi += 1; b.hide_render = False
            b.matrix_basis = Matrix.Translation(Vector(c['blob']['p'])) @ Euler((-math.pi / 2, 0, 0), 'XYZ').to_matrix().to_4x4() @ Matrix.Diagonal((c['blob']['s'][0] * 1.1, c['blob']['s'][1] * 1.1, 1, 1))
    for b in BLOBS[bi:]: b.hide_render = True
    # sprites (UI, particles) and 3D puffs / fire
    si = pi_ = 0; camp = Vector(F['cam']['m'][12:15])
    for s in F['sprites']:
        key=s.get('key','')
        if key in PRESS_HANDS:
            root=PRESS_HANDS[key];hand_visible(root,True)
            if key=='thumb' and F['shot']=='tablet':
                surface=OBJ[sc['tablet_surface_id']].matrix_basis
                reach=max(0,min(1,(F['f']-660)/20));reach=1-(1-reach)**3
                press=max(0,min(1,(F['f']-680)/3))*max(0,min(1,(700-F['f'])/3))
                k=1-reach
                root.matrix_basis=surface @ Matrix.Translation(Vector((.002+.07*k,-.05-.11*k,.0004+.06*k-.0012*press))) @ Euler((0,0,math.radians(-38)),'XYZ').to_matrix().to_4x4() @ Matrix.Diagonal((.78,.78,.78,1))
            elif key=='fist':
                reach=max(0,min(1,(F['f']-2124)/18));reach=1-(1-reach)**3
                press=max(0,min(1,(F['f']-2140)/2))*max(0,min(1,(2154-F['f'])/2));press=press*press*(3-2*press)
                root.matrix_basis=Matrix.Translation(Vector((-1.3,1.12+.26*(1-reach)-.04*press,3.7))) @ Euler((-math.pi/2,0,-.25),'XYZ').to_matrix().to_4x4()
            elif key=='click':
                reach=max(0,min(1,(F['f']-2462)/14));reach=1-(1-reach)**3
                root.matrix_basis=Matrix.Translation(Vector((.08,.825+.18*(1-reach),-.45))) @ Euler((-math.pi/2,0,-.25),'XYZ').to_matrix().to_4x4()
            elif key=='tap':  # preview sprite was offset for drawing; the 3D fingertip goes exactly on the button
                q=s['q'];Q=Quaternion((q[3],q[0],q[1],q[2]));R=Q.to_matrix()
                tip=Vector(s['p'])-R@Vector((.2*.09,0,0))+R@Vector((0,.26*.09,0))
                root.matrix_basis=Matrix.Translation(tip) @ Q.to_matrix().to_4x4()
            else:
                q=s['q'];root.matrix_basis=Matrix.Translation(Vector(s['p'])) @ Quaternion((q[3],q[0],q[1],q[2])).to_matrix().to_4x4()
            continue
        if s.get('kind') in ('puff', 'fire') and pi_ < len(PUFFS):
            o = PUFFS[pi_]; pi_ += 1; o.hide_render = False; r = s['s'][1] * 0.42
            o.matrix_basis = Matrix.Translation(Vector(s['p'])) @ Matrix.Diagonal((r, r * 0.85, r, 1))
            o.material_slots[0].material = MAT_FIRE if s['kind'] == 'fire' else (MAT_PUFFD if s.get('dark') else MAT_PUFF); continue
        if si >= len(SPRS): continue
        o = SPRS[si]; si += 1; o.hide_render = False; nt = o.active_material.node_tree
        nt.nodes['img'].image = load(os.path.join(DATA, 'sprites', s['img'])); nt.nodes['tint'].outputs[0].default_value = (*hexc(s['tint']), 1); nt.nodes['opacity'].outputs[0].default_value = s['alpha']
        nt.nodes['litmix'].inputs['Fac'].default_value = 0.0; nt.nodes['emit'].outputs[0].default_value = 1.0
        p, sx, sy = Vector(s['p']), s['s'][0], s['s'][1]
        if s.get('over'):  # overlay: slide toward the camera along the view ray so it is never occluded
            k = 0.6 / max(0.61, (p - camp).length); p = camp + (p - camp) * k; sx *= k; sy *= k
        q = s['q']; o.matrix_basis = Matrix.Translation(p) @ Quaternion((q[3], q[0], q[1], q[2])).to_matrix().to_4x4() @ Matrix.Diagonal((sx, sy, 1, 1))
    for o in SPRS[si:]: o.hide_render = True
    for o in PUFFS[pi_:]: o.hide_render = True
    # Small deterministic breeze on downloaded foliage; no cumulative transforms.
    for o in DRESS_ROOTS:
        if o['asset_set'] != F['set']: continue
        name=o['asset_id'];rest=o['rest_rot']
        if any(k in name for k in ('tree','shrub','plant','grass')):
            phase=sum(ord(k) for k in o.name)*.17
            amount=.008 if F['set'] in ('ocean','suburb','city') else .002
            o.rotation_euler=(rest[0]+amount*math.sin(F['f']/30*1.3+phase),rest[1]+amount*.6*math.cos(F['f']/30+phase),rest[2])
    # post: fog, lens, bloom, grade, vignette, flash/fade
    fog = F['fog']; sc.world.mist_settings.start = fog['near']; sc.world.mist_settings.depth = max(1, fog['far'] - fog['near']); sc.world.mist_settings.falloff = 'LINEAR'
    P['fog'].inputs['B'].default_value = (*hexc(fog['c']), 1); P['fog'].inputs['Factor'].default_value = 0.85
    D = F['D']; s_ = max(0.2, D['focus']); f_mm = CAM.data.lens; cinf = D.get('cinf', 0) * sc.render.resolution_x / 1080
    CAM.data.dof.use_dof = False; CAM.data.dof.focus_distance = s_
    P['dof'].f_stop = 128 if cinf < 0.5 else max(0.5, min(128, f_mm * f_mm * sc.render.resolution_x / (cinf * 13.5 * (s_ * 1000 - f_mm))))
    P['dof'].blur_max = max(4, cinf * 2.2)
    P['bloom'].inputs['Strength'].default_value = L.get('bloom', 0.45) * 0.38; P['bloom'].inputs['Threshold'].default_value = L.get('bloomTh', 0.88)
    P['sat'].inputs['Saturation'].default_value = min(1.24, L.get('sat', 1.06) * 1.07)
    gain, lift = hexc(L.get('gain', '#ffffff')), hexc(L.get('lift', '#000000'))
    cb = P['grade']; cb.inputs[8].default_value = (*gain, 1); cb.inputs[4].default_value = (lift[0] + 1, lift[1] + 1, lift[2] + 1, 1) if False else cb.inputs[4].default_value
    P['vignette'].inputs['Factor'].default_value = L.get('vig', 0.22) * 0.85
    po = F['post']; P['flash'].inputs['Factor'].default_value = po['flash']; P['flash'].inputs['B'].default_value = (*hexc(po.get('flashCol', '#ffffff')), 1); P['fade'].inputs['Factor'].default_value = po['fade']
    for n in WATER: n.inputs['W'].default_value = F['f'] / 30 * 0.15

only = set(int(x) for x in A['only'].split(',') if x) if A['only'] else None
frames = sorted(only) if only else list(range(A['start'], A['end'] + 1, A['step']))
# Separate render revisions and resolutions: never silently mix old and new frames.
def content_hash(path):
    digest=hashlib.sha256()
    with open(path,'rb') as fp:
        for block in iter(lambda:fp.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()
def data_hash(root):
    digest=hashlib.sha256()
    for folder,dirs,names in os.walk(root):
        dirs.sort()
        for name in sorted(names):
            path=os.path.join(folder,name)
            digest.update(os.path.relpath(path,root).replace(os.sep,'/').encode())
            digest.update(content_hash(path).encode())
    return digest.hexdigest()
manifest_path = os.path.join(A['out'], 'render-settings.json')
signature = {'revision': 'polished-v2', 'engine': A['engine'], 'samples': A['samples'], 'view': sc.view_settings.view_transform, 'resolution_percent': A['res'],
             'renderer_sha256': hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
             'blend_sha256': content_hash(bpy.data.filepath), 'data_sha256': data_hash(DATA)}
# Use content version plus file size, not filesystem timestamps (copying machines may change them).
if os.path.exists(manifest_path):
    previous = json.load(open(manifest_path))
    if previous != signature: raise RuntimeError('This output folder contains another render configuration. Choose a new --out folder to prevent mixed frames.')
elif any(n.startswith('f') and n.endswith('.jpg') for n in os.listdir(A['out'])):
    raise RuntimeError('Unversioned frames already exist here. Choose an empty output folder.')
with open(manifest_path, 'w') as mf: json.dump(signature, mf, indent=2)
t0 = time.time(); n = 0
for f in frames:
    out = os.path.join(A['out'], f'f{f:04d}.jpg')
    if os.path.exists(out) and os.path.getsize(out) > 2:
        with open(out, 'rb') as check:
            check.seek(-2, 2)
            if check.read() == b'\xff\xd9': continue
    F = json.load(open(os.path.join(DATA, 'frames', f'f{f:04d}.json')))
    apply_frame(F); sc.frame_set(f); sc.render.filepath = out; bpy.ops.render.render(write_still=True); n += 1
    for o in CARDS + SPRS:
        if o.hide_render: o.active_material.node_tree.nodes['img'].image = None
    trim_images()
    print(f'frame {f} done  ({(time.time() - t0) / n:.2f} s/frame avg)', flush=True)
print('ALL DONE', n, 'frames rendered')
