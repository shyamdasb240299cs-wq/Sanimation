"""Build film.blend from the exported data (run once on the authoring machine):
   blender -b --python build.py
Creates: per-set collections (three.js Y-up world under a rotated root), Poly Haven material upgrades,
Poly Haven set dressing (collision-checked), character/sprite/puff/blob pools, lights, camera, compositor (ink, DOF, bloom, grade)."""
import bpy, json, os, math, base64, glob
import numpy as np
from mathutils import Matrix, Vector

KIT = os.path.dirname(os.path.abspath(__file__))
DATA, ASSETS = os.path.join(KIT, 'data'), os.path.join(KIT, 'assets')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 1080, 1920, 30
try: sc.view_settings.view_transform = 'AgX'
except Exception as e: print('view transform', e)
sc.view_settings.look = 'AgX - Medium High Contrast'
bpy.context.preferences.filepaths.save_version = 0

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [a]  # sRGB -> linear

# ---------------- root: three.js Y-up world ----------------
ROOT = bpy.data.objects.new('Y_UP', None); ROOT.rotation_euler = (math.pi / 2, 0, 0); sc.collection.objects.link(ROOT)
def to_mat(e):  # three.js column-major 16 -> Matrix
    return Matrix([[e[0], e[4], e[8], e[12]], [e[1], e[5], e[9], e[13]], [e[2], e[6], e[10], e[14]], [e[3], e[7], e[11], e[15]]])

# ---------------- images ----------------
IMG = {}
def img(path, colorspace='sRGB'):
    if path in IMG: return IMG[path]
    im = bpy.data.images.load(path, check_existing=True); im.colorspace_settings.name = colorspace; IMG[path] = im; return im

# ---------------- Poly Haven material upgrades (by painted-texture kind) ----------------
PH = {'wood': ('wood_floor', 'detail', 0.55), 'tiles': ('large_floor_tiles_02', 'detail', 0.45), 'wall': ('painted_plaster_wall', 'detail', 0.6),
      'concrete': ('concrete_floor_02', 'detail', 0.5), 'asphalt': ('asphalt_02', 'detail', 0.35), 'sand': ('coast_sand_01', 'detail', 0.3),
      'grass': ('leafy_grass', 'replace', 0.25), 'carpet': ('quatrefoil_jacquard_fabric', 'detail', 1.2), 'fabric': ('quatrefoil_jacquard_fabric', 'detail', 1.6),
      'brick': ('red_brick_03', 'detail', 0.6), 'shingles': ('roof_tiles_14', 'detail', 0.5), 'siding': ('exterior_wall_cladding', 'detail', 0.45),
      'factoryFloor': ('hangar_concrete_floor', 'detail', 0.25), 'brushed': ('metal_plate', 'detail', 0.6)}
PH_MEAN = {}
def ph_mean(k):
    if k not in PH_MEAN:
        im = img(os.path.join(ASSETS, 'tex', k, 'diff.jpg')); px = np.empty(len(im.pixels), np.float32); im.pixels.foreach_get(px)
        PH_MEAN[k] = float(np.clip((px.reshape(-1, 4)[:, :3] @ np.array([0.2126, 0.7152, 0.0722], np.float32)).mean(), 0.05, 1))
    return PH_MEAN[k]

def tex_node(nt, t, colorspace='sRGB', path=None):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = img(path or os.path.join(DATA, 'tex', t['id'] + '.png'), colorspace); n.name = 'tex_' + t['id']
    n.extension = 'REPEAT' if t.get('wrap') else 'EXTEND'
    if t['rep'] != [1, 1] or t['off'] != [0, 0]:
        uv = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (t['rep'][0], t['rep'][1], 1); mp.inputs['Location'].default_value = (t['off'][0], t['off'][1], 0)
        nt.links.new(uv.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
    return n

def ph_nodes(nt, kind):
    name, mode, scale = PH[kind]; d = os.path.join(ASSETS, 'tex', name)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    out = {}
    for key, cs in (('diff', 'sRGB'), ('nor', 'Non-Color'), ('rough', 'Non-Color')):
        p = os.path.join(d, key + '.jpg')
        if not os.path.exists(p): continue
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = img(p, cs); n.projection = 'BOX'; n.projection_blend = 0.25; nt.links.new(mp.outputs['Vector'], n.inputs['Vector']); out[key] = n
    return name, mode, out

MATS = {}
def build_mat(mt):
    key = mt['id']
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    col = hexc(mt['color'])
    if mt['shader']:  # painted ocean -> real water
        bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.inputs['Base Color'].default_value = (0.02, 0.18, 0.24, 1); bs.inputs['Roughness'].default_value = 0.06; bs.inputs['IOR'].default_value = 1.33
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.name = 'water_noise'; nz.noise_dimensions = '4D'; nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 6
        tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; nt.links.new(nz.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
        nt.links.new(bs.outputs['BSDF'], out.inputs['Surface']); m['kind'] = 'water'; MATS[key] = m; return m
    alpha_src = None
    if mt['basic']:  # unlit (glows, screens, signs)
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0
        if mt['map']:
            t = tex_node(nt, mt['map']); mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1
            mul.inputs['A'].default_value = col; nt.links.new(t.outputs['Color'], mul.inputs['B']); nt.links.new(mul.outputs['Result'], em.inputs['Color']); alpha_src = t
        else: em.inputs['Color'].default_value = col
        shader = em
    else:
        bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = mt['rough']; bs.inputs['Metallic'].default_value = mt['metal']
        base = None
        if mt['map']:
            t = tex_node(nt, mt['map']); alpha_src = t; base = t.outputs['Color']
        kind = mt['name'][3:] if mt['name'].startswith('ph:') else None
        if kind in PH:
            name, mode, P = ph_nodes(nt, kind)
            if mode == 'replace' and 'diff' in P: base = P['diff'].outputs['Color']
            elif 'diff' in P and base is not None:
                bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(P['diff'].outputs['Color'], bw.inputs['Color'])
                mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Max'].default_value = ph_mean(name) * 2; mr.inputs['To Min'].default_value = 0.0; mr.inputs['To Max'].default_value = 2.0; mr.clamp = False
                nt.links.new(bw.outputs['Val'], mr.inputs['Value'])
                cl = nt.nodes.new('ShaderNodeClamp'); cl.inputs['Min'].default_value = 0.78; cl.inputs['Max'].default_value = 1.22; nt.links.new(mr.outputs['Result'], cl.inputs['Value'])
                mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 0.35
                nt.links.new(base, mx.inputs['A']); nt.links.new(cl.outputs['Result'], mx.inputs['B']); base = mx.outputs['Result']
            if 'nor' in P:
                nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.065 if kind == 'sand' else 0.22; nt.links.new(P['nor'].outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
            if 'rough' in P:
                rr = nt.nodes.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = max(0.05, mt['rough'] * 0.7); rr.inputs['To Max'].default_value = min(1, mt['rough'] * 1.25 + 0.05)
                nt.links.new(P['rough'].outputs['Color'], rr.inputs['Value']); nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
        if base is not None:
            mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1; mul.inputs['A'].default_value = col
            nt.links.new(base, mul.inputs['B']); nt.links.new(mul.outputs['Result'], bs.inputs['Base Color'])
        else: bs.inputs['Base Color'].default_value = col
        e = hexc(mt['emissive'])
        if mt['ei'] > 0 and sum(e[:3]) > 0:
            if mt['emap']: te = tex_node(nt, mt['emap']); nt.links.new(te.outputs['Color'], bs.inputs['Emission Color'])
            else: bs.inputs['Emission Color'].default_value = e
            bs.inputs['Emission Strength'].default_value = mt['ei']
        shader = bs
    op = mt['opacity'] if mt['transparent'] else 1.0
    if op < 0.999 or (alpha_src is not None and (mt['transparent'] or mt['alphaTest'] > 0)):
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
        if alpha_src is not None:
            ma = nt.nodes.new('ShaderNodeMath'); ma.operation = 'MULTIPLY'; ma.inputs[1].default_value = op; nt.links.new(alpha_src.outputs['Alpha'], ma.inputs[0]); nt.links.new(ma.outputs['Value'], mix.inputs['Fac'])
        else: mix.inputs['Fac'].default_value = op
        nt.links.new(tr.outputs['BSDF'], mix.inputs[1]); nt.links.new(shader.outputs[0], mix.inputs[2]); shader = mix
        m.surface_render_method = 'BLENDED' if op < 0.999 else 'DITHERED'
        if op < 0.6: m.use_transparent_shadow = True
    if mt.get('name') == 'hero_hand_skin':
        em=nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value=col; em.inputs['Strength'].default_value=.75
        mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.28
        nt.links.new(em.outputs[0],mix.inputs[1]);nt.links.new(shader.outputs[0],mix.inputs[2]);shader=mix
    nt.links.new(shader.outputs[0], out.inputs['Surface'])
    MATS[key] = m; return m

# ---------------- geometry ----------------
MESHES = {}
def b64(s, dt): return np.frombuffer(base64.b64decode(s), dt) if s else None
def build_mesh(gid, groups, nmat):
    k = (gid, tuple(map(tuple, groups)), nmat)
    if k in MESHES: return MESHES[k]
    G = json.load(open(os.path.join(DATA, 'geo', gid + '.json')))
    pos = b64(G['pos'], np.float32).reshape(-1, 3); nor = b64(G['nor'], np.float32); uv = b64(G['uv'], np.float32)
    idx = b64(G['idx'], np.uint32) if G['idx'] else np.arange(len(pos), dtype=np.uint32)
    tris = idx.reshape(-1, 3); nt = len(tris)
    me = bpy.data.meshes.new(gid); me.vertices.add(len(pos)); me.vertices.foreach_set('co', pos.ravel())
    me.loops.add(nt * 3); me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32))
    me.polygons.add(nt); me.polygons.foreach_set('loop_start', np.arange(0, nt * 3, 3, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(nt, 3, np.int32))
    if groups and nmat > 1:
        mi = np.zeros(nt, np.int32)
        for st, cnt, m_i in groups: mi[st // 3:(st + cnt) // 3] = min(m_i, nmat - 1)
        me.polygons.foreach_set('material_index', mi)
    if uv is not None:
        uvl = me.uv_layers.new(name='UVMap'); uvl.data.foreach_set('uv', uv.reshape(-1, 2)[tris.ravel()].ravel())
    me.update()
    me.polygons.foreach_set('use_smooth', np.ones(nt, bool))
    if nor is not None:
        try: me.normals_split_custom_set_from_vertices(nor.reshape(-1, 3))
        except Exception as e: print('normals', gid, e)
    MESHES[k] = me; return me

SETS = {}
for f in sorted(glob.glob(os.path.join(DATA, 'sets', '*.json'))):
    name = os.path.basename(f)[:-5]; S = json.load(open(f))
    coll = bpy.data.collections.new('set_' + name); sc.collection.children.link(coll)
    for r in S['meshes']:
        me = build_mesh(r['geo'], r['groups'], len(r['mats']))
        ob = bpy.data.objects.new(r['id'], me)
        for mt in r['mats']: ob.data.materials.append(build_mat(mt)) if len(ob.data.materials) < len(r['mats']) else None
        ob.parent = ROOT; ob.matrix_parent_inverse = Matrix.Identity(4); ob.matrix_basis = to_mat(r['m'])
        ob.visible_shadow = r['cast']; ob.hide_render = not r['vis']; ob['base_vis'] = r['vis']; ob['base_m'] = r['m']
        if r['noink']: ob['noink'] = 1
        coll.objects.link(ob)
    SETS[name] = S; coll['cols'] = json.dumps(S['cols'])
    print('built set', name, len(S['meshes']))

# ---------------- Poly Haven set dressing (collision-checked against colliders, actors, cameras) ----------------
DRESS = {  # three.js coords [x, y, z], rotation about up (rad), uniform scale
 'apartment': [('potted_plant_04', (-0.55, 0.92, -2.92), 0, 1.0), ('ceramic_vase_01', (-2.62, 0.93, 1.45), 0, 1.0), ('tea_set_01', (-2.55, 0.93, 1.8), 0.4, 0.9),
               ('book_encyclopedia_set_01', (1.05, 2.06, -2.86), 0, 0.9), ('alarm_clock_01', (2.25, 0.76, -2.45), -0.6, 1.0), ('wall_clock', (-0.3, 2.25, -2.99), 0, 1.0)],
 'penthouse': [('Chandelier_01', (-1.0, 3.95, 0.6), 0, 1.0), ('potted_plant_01', (-7.2, 0, -5.3), 0, 1.4), ('potted_plant_02', (7.3, 0, 5.3), 0.5, 1.3),
               ('mid_century_lounge_chair', (-6.4, 0, 2.6), 1.2, 1.0), ('tea_set_01', (-1.2, 0.36, 0.25), 0, 1.0), ('ceramic_vase_01', (-6.15, 0.79, -3.6), 0, 1.2), ('book_encyclopedia_set_01', (6.9, 1.16, -0.2), 0, 1.0)],
 'hq': [('ArmChair_01', (-4.6, 0, 2.8), 2.6, 1.0), ('ArmChair_01', (-3.0, 0, 3.6), 3.4, 1.0), ('potted_plant_01', (-6.3, 0, 4.4), 0, 1.3), ('hanging_picture_frame_02', (2.5, 1.9, 4.88), math.pi, 1.4),
        ('ceramic_vase_01', (40, 0.79, -1.3), 0, 1.4), ('office_notepads', (39.45, 0.79, 2.2), 0, 1.0), ('security_camera_01', (78.3, 3.2, -14), 0.8, 1.0),
        ('potted_plant_02', (78.6, 0, 2.0), 0, 1.0), ('potted_plant_02', (78.6, 0, -18), 0, 1.0), ('fire_alarm', (81.95, 1.5, -6.5), -math.pi / 2, 1.0)],
 'city': [('metal_trash_can', (6.6, 0.16, -50), 0, 1.0), ('fire_hydrant', (6.55, 0.16, -60), 0, 1.0), ('utility_box_01', (9.6, 0.16, -64), -math.pi / 2, 1.0),
          ('modular_street_seating', (9.3, 0.16, -71), -math.pi / 2, 1.0), ('concrete_road_barrier', (-120, 4, -800), 0.4, 1.4), ('concrete_road_barrier', (-125, 4, -796), 0.4, 1.4)],
 'suburb': [('fire_hydrant', (4.6, 0, 1.7), 0, 1.0), ('jacaranda_tree', (-19, 0, -3.5), 0, 1.0), ('jacaranda_tree', (33, 0, -3.5), 1.5, 1.0), ('shrub_01', (-8, 0, -5), 0, 1.6), ('shrub_02', (8.5, 0, -5.5), 0, 1.6), ('shrub_04', (-34, 0, -5), 0, 1.6)],
 'factory': [('steel_frame_shelves_01', (-29.5, 0, -30), math.pi / 2, 1.3), ('steel_frame_shelves_01', (-29.5, 0, -36), math.pi / 2, 1.3), ('Barrel_01', (12, 0, -6), 0, 1.0), ('Barrel_01', (12.8, 0, -6.4), 1, 1.0),
             ('cardboard_box_01', (-12.5, 0, -12), 0.3, 1.5), ('cardboard_box_01', (-12.3, 0.45, -12.1), 0.9, 1.4), ('WetFloorSign_01', (-10.5, 0, -5.5), 0.5, 1.0), ('tool_cart', (-12, 0, -8.5), 0.8, 1.0), ('industrial_storage_cart', (10, 0, -20), 0, 1.0)],
 'mission': [('binder_notebook', (-5.5, 0.81, -8.0), 0.3, 1.0), ('office_notepads', (4.2, 1.16, -4.5), 0, 1.0), ('potted_plant_02', (-10.3, 0, 6.2), 0, 1.2), ('potted_plant_02', (10.3, 0, 6.2), 0, 1.2)],
 'xroom': [('stationery_supplies', (-3.2, 0.8, -3.0), 0, 1.0), ('office_notepads', (3.4, 0.8, 0.6), 0, 1.0)],
 'ocean': [('island_tree_01', (594, 0.45, -9), 0, 1.0), ('island_tree_02', (607, 0.45, -11), 1, 1.0), ('island_tree_03', (588, 0.45, -4), 2, 1.0), ('Ukulele_01', (601.2, 0.47, -1.2), 1.2, 1.0),
           ('lifebuoy', (597.0, 0.47, -1.8), 0, 1.0), ('sand_rocks_small_01', (604, 0.45, 3), 0, 1.0), ('coast_rocks_01', (612, 0.2, 10), 0.5, 1.0)],
}

# Extra curated CC0 dressing: all coordinates in the original Y-up set space.
EXTRA_DRESS = {
'apartment': [('desk_lamp_arm_01',(2.15,.76,-2.76),0,.65),('stationery_supplies',(1.05,.76,-2.72),0,.6),('croissant',(-2.6,.93,.3),.3,.9)],
'penthouse': [('modern_ceiling_lamp_01',(-4,3.8,1),0,1),('modern_arm_chair_01',(6.8,0,3.9),-1.7,1),('side_table_01',(5.8,0,4.2),0,1),('potted_plant_04',(-6.1,.79,-3.0),0,1),('book_encyclopedia_set_01',(-6.3,.79,-3.6),0,.8)],
'hq': [('classic_laptop',(.35,.80,-2.5),0,.85),('desk_lamp_arm_01',(-1.1,.80,-2.5),0,.8),('clipboard',(40.45,.80,0),0,.9),('binder_notebook',(39.55,.80,-3),.2,1),('stationery_supplies',(40,.80,4.9),0,.7),('wall_clock',(34.15,2.5,-3),1.57,1),('hanging_picture_frame_01',(81.96,1.9,-20),-1.57,1.3)],
'factory': [('flood_lights',(14,0,-18),-1.2,1),('hanging_industrial_lamp',(-7,5.5,-10),0,1),('mounted_fluorescent_lights',(-15,5.2,-24),0,1),('clipboard',(-12,1.05,-8.5),.3,1),('cardboard_box_01',(11,0,-23),0,1.5)],
'mission': [('classic_laptop',(-6.5,.81,-8),0,.8),('desk_lamp_arm_01',(5.5,1.16,-4.5),0,.7),('clipboard',(4.8,1.16,-4.5),.2,1)],
'xroom': [('potted_plant_04',(-4.6,.8,.6),0,1),('classic_laptop',(4.4,.8,.7),0,.8),('desk_lamp_arm_01',(-4.5,.8,-3.3),0,.8),('binder_notebook',(-3.7,.8,.7),.3,.8)],
'city': [('street_lamp_01',(7,.16,-57),0,1),('planter_box_01',(9,.16,-76),0,1),('metal_trash_can',(-7,.16,-62),0,1)],
'suburb': [('tree_small_02',(-12,0,-4.5),0,1),('planter_box_01',(12,0,-3.5),0,1),('grass_medium_01',(-8,0,-4),0,1.1)],
'ocean': [('outdoor_table_chair_set_01',(610,.45,-5),0,1),('sand_rocks_small_01',(610,.45,5),0,1),('coast_rocks_01',(615,.15,14),0,.5)],
}
for setname, entries in EXTRA_DRESS.items(): DRESS.setdefault(setname, []).extend(entries)
EXTRA2 = {  # second dressing pass (more CC0 props); every placement is collision-checked below
'apartment': [('calathea_orbifolia_01',(2.65,0,-1.35),0,1),('ceramic_vase_02',(-2.62,.93,.95),0,1)],
'penthouse': [('pachira_aquatica_01',(-7.3,0,.6),0,1.2),('side_table_tall_01',(-4.8,0,.55),0,1),('ceramic_vase_03',(7.1,1.16,-2.5),0,1),('anthurium_botany_01',(-4.8,1.0,.55),0,1)],
'hq': [('pachira_aquatica_01',(6.2,0,4.3),0,1.2),('korean_fire_extinguisher_01',(78.15,.25,-26),1.57,1),('anthurium_botany_01',(45.2,0,6.6),0,1.2),('caged_hanging_light',(80,3.35,-30),0,1)],
'city': [('concrete_road_barrier_02',(-118,4,-806),.3,1.4),('utility_box_02',(-9.6,.16,-30),1.57,1),('planter_box_02',(-9.0,.16,-46),1.57,1),('planter_box_03',(9.0,.16,-86),-1.57,1)],
'suburb': [('garden_gnome',(-4.0,0,-2.5),.4,1.2),('wooden_picnic_table',(-22,0,-5),.2,1),('modular_electricity_poles',(45,0,12.3),1.57,1),('fern_02',(4.6,0,-6.0),0,1.2),('shrub_03',(-4.6,0,-6.3),0,1.4)],
'factory': [('Barrel_02',(13.2,0,-7.3),.5,1),('metal_toolbox',(-11.2,0,-9.4),.4,1),('hand_truck',(11.4,0,-9.2),-.6,1),('korean_fire_extinguisher_01',(-29.6,.25,-12),1.57,1),('security_light',(-31.5,6,-20),1.57,1)],
'mission': [('calathea_orbifolia_01',(-10.2,0,-12.1),0,1.3),('fern_02',(10.2,0,-12.1),0,1.3)],
'xroom': [('pachira_aquatica_01',(6.3,0,-6.3),0,1.1)],
'ocean': [('Lantern_01',(600.2,.97,-1.9),0,.8),('wooden_lantern_01',(598.0,.45,.8),0,1),('plastic_monobloc_chair_01',(603.6,.45,-3.0),-.6,1),('fern_02',(596,.45,-6),0,1.4)],
}
for setname, entries in EXTRA2.items(): DRESS.setdefault(setname, []).extend(entries)

def bbox_three(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs if o.type == 'MESH' for c in o.bound_box]
    if not pts: return None
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    return (min(xs), max(xs), min(zs), max(zs), -max(ys), -min(ys))  # Blender (x, y, z) -> three (x, y=z, z=-y)
OCC = {}
for fpath in sorted(glob.glob(os.path.join(DATA, 'frames', 'f*.json')))[::3]:
    F = json.load(open(fpath)); o = OCC.setdefault(F['set'], {'act': [], 'cam': []})
    o['act'] += [c['p'] for c in F['cards']]; o['cam'].append(F['cam']['m'][12:15])
report = []
for sname, items in DRESS.items():
    coll = bpy.data.collections.get('set_' + sname)
    for (asset, p, ry, s) in items:
        path = os.path.join(ASSETS, 'models', asset, asset + '.gltf')
        if not os.path.exists(path): report.append(f'{sname}: missing {asset}'); continue
        before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path); new = [o for o in bpy.data.objects if o not in before]
        rootn = [o for o in new if o.parent is None]
        for o in rootn: o.location = (p[0], -p[2], p[1]); o.rotation_euler = (0, 0, ry); o.scale = (s, s, s)
        bpy.context.view_layer.update(); bb = bbox_three(new); ok = True
        if bb:
            x0, x1, y0, y1, z0, z1 = bb; O = OCC.get(sname, {'act': [], 'cam': []})
            if y0 < 2.15 and any(x0 - 0.25 < a[0] < x1 + 0.25 and z0 - 0.25 < a[2] < z1 + 0.25 for a in O['act']): ok = False; report.append(f'{sname}: {asset} overlaps an actor path -> removed')
            elif any(x0 - 0.3 < c[0] < x1 + 0.3 and y0 - 0.3 < c[1] < y1 + 0.3 and z0 - 0.3 < c[2] < z1 + 0.3 for c in O['cam']): ok = False; report.append(f'{sname}: {asset} intersects a camera path -> removed')
        for o in new:
            for c in list(o.users_collection): c.objects.unlink(o)
            if ok: coll.objects.link(o)
            else: bpy.data.objects.remove(o)
        if ok:
            report.append(f'{sname}: placed {asset}')
            for o in rootn:
                o['asset_id'] = asset; o['asset_set'] = sname
                o['rest_rot'] = list(o.rotation_euler)
            for o in new:
                if o.type != 'MESH': continue
                for m in o.data.materials:
                    if m: m['downloaded_cc0'] = True

print('\n'.join(report)); open(os.path.join(KIT, 'dressing_report.txt'), 'w').write('\n'.join(report))

# Downloaded assets retain their shapes and textures, with calmer microdetail and richer color.
for m in bpy.data.materials:
    if not m.get('downloaded_cc0') or not m.node_tree: continue
    nt=m.node_tree
    for n in list(nt.nodes):
        if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value *= .3
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Coat Weight'].default_value = .12
            n.inputs['Coat Roughness'].default_value = .3
            socket=n.inputs['Base Color']
            if socket.is_linked:
                src=socket.links[0].from_socket
                hsv=nt.nodes.new('ShaderNodeHueSaturation');hsv.inputs['Saturation'].default_value=1.14
                nt.links.new(src,hsv.inputs['Color']);nt.links.new(hsv.outputs['Color'],socket)
# ---------------- pools: character cards, sprites, puffs, blobs ----------------
pools = bpy.data.collections.new('pools'); sc.collection.children.link(pools)
for aov in ('card',):
    if aov not in sc.view_layers[0].aovs: a = sc.view_layers[0].aovs.add(); a.name = aov; a.type = 'VALUE'
def plane(name, w, h, y0):
    me = bpy.data.meshes.new(name); v = [(-w / 2, y0, 0), (w / 2, y0, 0), (w / 2, y0 + h, 0), (-w / 2, y0 + h, 0)]
    me.from_pydata(v, [], [(0, 1, 2, 3)]); uv = me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = c
    return me
def card_mat(name, lit_capable=True):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); m.surface_render_method = 'DITHERED'
    out = nt.nodes.new('ShaderNodeOutputMaterial'); t = nt.nodes.new('ShaderNodeTexImage'); t.name = 'img'; t.extension = 'CLIP'
    tint = nt.nodes.new('ShaderNodeRGB'); tint.name = 'tint'; tint.outputs[0].default_value = (1, 1, 1, 1)
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1
    nt.links.new(t.outputs['Color'], mul.inputs['A']); nt.links.new(tint.outputs[0], mul.inputs['B'])
    em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(mul.outputs['Result'], em.inputs['Color'])
    ems = nt.nodes.new('ShaderNodeValue'); ems.name = 'emit'; ems.outputs[0].default_value = 1.0; nt.links.new(ems.outputs[0], em.inputs['Strength'])
    df = nt.nodes.new('ShaderNodeBsdfDiffuse'); nt.links.new(mul.outputs['Result'], df.inputs['Color'])
    up = nt.nodes.new('ShaderNodeCombineXYZ'); up.inputs['Z'].default_value = 1.0; nt.links.new(up.outputs[0], df.inputs['Normal'])
    dk = nt.nodes.new('ShaderNodeValue'); dk.name = 'diffk'; dk.outputs[0].default_value = 0.0
    dm = nt.nodes.new('ShaderNodeMixShader'); dm.name = 'litmix'; dm.inputs['Fac'].default_value = 0.0
    add = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(em.outputs[0], add.inputs[0]); nt.links.new(df.outputs[0], add.inputs[1])
    nt.links.new(em.outputs[0], dm.inputs[1]); nt.links.new(add.outputs[0], dm.inputs[2])
    sc_ = nt.nodes.new('ShaderNodeMath'); sc_.operation = 'MULTIPLY'; nt.links.new(dk.outputs[0], sc_.inputs[0]); sc_.inputs[1].default_value = 1.0
    # diffuse weight: scale diffuse colour by diffk
    mul2 = nt.nodes.new('ShaderNodeMix'); mul2.data_type = 'RGBA'; mul2.blend_type = 'MULTIPLY'; mul2.inputs['Factor'].default_value = 1
    nt.links.new(mul.outputs['Result'], mul2.inputs['A']); cmb = nt.nodes.new('ShaderNodeCombineColor'); [nt.links.new(sc_.outputs[0], cmb.inputs[i]) for i in range(3)]
    nt.links.new(cmb.outputs[0], mul2.inputs['B']); nt.links.new(mul2.outputs['Result'], df.inputs['Color'])
    op = nt.nodes.new('ShaderNodeValue'); op.name = 'opacity'; op.outputs[0].default_value = 1.0
    am = nt.nodes.new('ShaderNodeMath'); am.operation = 'MULTIPLY'; nt.links.new(t.outputs['Alpha'], am.inputs[0]); nt.links.new(op.outputs[0], am.inputs[1])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); fin = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(am.outputs[0], fin.inputs['Fac']); nt.links.new(tr.outputs[0], fin.inputs[1]); nt.links.new(dm.outputs[0], fin.inputs[2])
    ao = nt.nodes.new('ShaderNodeOutputAOV'); ao.aov_name = 'card'; ao.inputs['Value'].default_value = 1.0
    nt.links.new(fin.outputs[0], out.inputs['Surface']); return m
CARD_ME = plane('card', 2.25 * 0.6, 2.25, -2.25 * 0.025); SPR_ME = plane('sprite', 1, 1, -0.5)
for i in range(32):
    o = bpy.data.objects.new(f'card_{i:02d}', CARD_ME.copy()); o.data.materials.append(card_mat(f'cardmat_{i:02d}')); o.parent = ROOT; o.hide_render = True; pools.objects.link(o)
for i in range(140):
    o = bpy.data.objects.new(f'spr_{i:03d}', SPR_ME.copy()); o.data.materials.append(card_mat(f'sprmat_{i:03d}')); o.parent = ROOT; o.hide_render = True; o.visible_shadow = False; pools.objects.link(o)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1); ico = bpy.context.object.data; bpy.data.objects.remove(bpy.context.object)
def simple_mat(name, color, emit=0.0, rough=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = color; b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = color; b.inputs['Emission Strength'].default_value = emit
    return m
PUFF = simple_mat('puff', (0.92, 0.9, 0.88, 1)); PUFFD = simple_mat('puff_dark', (0.12, 0.1, 0.11, 1)); FIRE = simple_mat('fire', (1.0, 0.45, 0.08, 1), emit=12.0)
for _m in (PUFF, PUFFD, FIRE): _m.use_fake_user = True
for i in range(70):
    if i == 0: ico.materials.append(PUFF)
    o = bpy.data.objects.new(f'puff_{i:02d}', ico); o.parent = ROOT; o.hide_render = True; pools.objects.link(o)
    o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = PUFF
BLOB = bpy.data.materials.new('blob'); BLOB.use_nodes = True; nt = BLOB.node_tree; nt.nodes.clear(); BLOB.surface_render_method = 'BLENDED'
o_ = nt.nodes.new('ShaderNodeOutputMaterial'); gt = nt.nodes.new('ShaderNodeTexGradient'); gt.gradient_type = 'SPHERICAL'; tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (2, 2, 2); mp.inputs['Location'].default_value = (0, 0, 0)
nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], gt.inputs['Vector'])
mf = nt.nodes.new('ShaderNodeMath'); mf.operation = 'MULTIPLY'; mf.inputs[1].default_value = 0.45; nt.links.new(gt.outputs['Fac'], mf.inputs[0])
tr = nt.nodes.new('ShaderNodeBsdfTransparent'); dk = nt.nodes.new('ShaderNodeBsdfDiffuse'); dk.inputs['Color'].default_value = (0.02, 0.015, 0.03, 1)
mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(mf.outputs[0], mx.inputs['Fac']); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(dk.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o_.inputs['Surface'])
blob_me = plane('blob', 1, 1, -0.5)
for i in range(32):
    o = bpy.data.objects.new(f'blob_{i:02d}', blob_me); o.data.materials.append(BLOB) if i == 0 else None; o.parent = ROOT; o.hide_render = True; o.visible_shadow = False; pools.objects.link(o)

# ---------------- camera, lights ----------------
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); cam.parent = ROOT; sc.collection.objects.link(cam); sc.camera = cam
cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 24.0; cam.data.clip_start = 0.05; cam.data.clip_end = 6000
sun = bpy.data.objects.new('SUN', bpy.data.lights.new('SUN', 'SUN')); sc.collection.objects.link(sun); sun.data.angle = math.radians(5.0)
for i in range(4):
    l = bpy.data.objects.new(f'prac_{i}', bpy.data.lights.new(f'prac_{i}', 'POINT')); l.parent = ROOT; l.data.shadow_soft_size = 0.25; sc.collection.objects.link(l); l.hide_render = True
# world: HDRI with rotation + strength set per frame
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
wo = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground'); bg.name = 'bg'; env = nt.nodes.new('ShaderNodeTexEnvironment'); env.name = 'env'
tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.name = 'envrot'
nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector']); nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs[0], wo.inputs['Surface'])
for h in glob.glob(os.path.join(ASSETS, 'hdri', '*.hdr')): img(h, 'Linear Rec.709')
# HDRI sun azimuth (brightest pixel) so the sky's sun can be rotated to match the key light
hdri_az = {}
for h in glob.glob(os.path.join(ASSETS, 'hdri', '*.hdr')):
    im = IMG[h]; W_, H_ = im.size; px = np.empty(W_ * H_ * 4, np.float32); im.pixels.foreach_get(px); lum = px.reshape(H_, W_, 4)[:, :, :3].sum(2)
    y, x = np.unravel_index(np.argmax(lum), lum.shape); hdri_az[os.path.basename(h)] = (x / W_) * 2 * math.pi
w['hdri_az'] = json.dumps(hdri_az)

# ---------------- render settings ----------------
vl = sc.view_layers[0]
for p_ in ('use_pass_z', 'use_pass_normal', 'use_pass_mist'): setattr(vl, p_, True)
sc.render.engine = 'BLENDER_EEVEE'; e = sc.eevee; e.taa_render_samples = 24; e.use_raytracing = True; e.use_shadows = True
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
sc.render.film_transparent = False
c = sc.cycles; c.samples = 96; c.use_adaptive_sampling = True; c.adaptive_threshold = 0.02; c.use_denoising = True; c.max_bounces = 5; c.diffuse_bounces = 3; c.glossy_bounces = 3; c.transmission_bounces = 4; c.transparent_max_bounces = 16; c.caustics_reflective = False; c.caustics_refractive = False

# ---------------- compositor: ink (normal+depth edges, cards masked), DOF, bloom, grade, vignette, flash/fade ----------------
ng = bpy.data.node_groups.new('Post', 'CompositorNodeTree'); sc.compositing_node_group = ng; N = ng.nodes; Lk = ng.links.new
rl = N.new('CompositorNodeRLayers'); go = N.new('NodeGroupOutput'); ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
def node(t, name=None, **inp):
    n = N.new(t)
    if name: n.name = name
    for k, v in inp.items(): n.inputs[k].default_value = v
    return n
# normal edges
fn = node('CompositorNodeFilter', Type='Sobel'); Lk(rl.outputs['Normal'], fn.inputs['Image'])
bwn = node('CompositorNodeRGBToBW'); Lk(fn.outputs['Image'], bwn.inputs['Image'])
# depth edges on log-depth
lg = node('ShaderNodeMath'); lg.operation = 'LOGARITHM'; lg.inputs[1].default_value = math.e; Lk(rl.outputs['Depth'], lg.inputs[0])
lgc = node('CompositorNodeCombineColor'); [Lk(lg.outputs[0], lgc.inputs[i]) for i in range(3)]
fd = node('CompositorNodeFilter', Type='Sobel'); Lk(lgc.outputs['Image'], fd.inputs['Image']); bwd = node('CompositorNodeRGBToBW'); Lk(fd.outputs['Image'], bwd.inputs['Image'])
md = node('ShaderNodeMath'); md.operation = 'MULTIPLY'; md.inputs[1].default_value = 6.0; Lk(bwd.outputs['Val'], md.inputs[0])
mn = node('ShaderNodeMath'); mn.operation = 'MULTIPLY'; mn.inputs[1].default_value = 0.9; Lk(bwn.outputs['Val'], mn.inputs[0])
mx_ = node('ShaderNodeMath'); mx_.operation = 'MAXIMUM'; Lk(md.outputs[0], mx_.inputs[0]); Lk(mn.outputs[0], mx_.inputs[1])
th = node('ShaderNodeMapRange'); th.inputs['From Min'].default_value = 0.35; th.inputs['From Max'].default_value = 0.9; th.clamp = True; Lk(mx_.outputs[0], th.inputs['Value'])
# fade ink with distance (far city stays clean)
dfade = node('ShaderNodeMapRange'); dfade.inputs['From Min'].default_value = 60; dfade.inputs['From Max'].default_value = 400; dfade.inputs['To Min'].default_value = 1; dfade.inputs['To Max'].default_value = 0.15; dfade.clamp = True; Lk(rl.outputs['Depth'], dfade.inputs['Value'])
e1 = node('ShaderNodeMath'); e1.operation = 'MULTIPLY'; Lk(th.outputs['Result'], e1.inputs[0]); Lk(dfade.outputs['Result'], e1.inputs[1])
inv = node('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; Lk(rl.outputs['card'], inv.inputs[1])
e2 = node('ShaderNodeMath', 'inkamt'); e2.operation = 'MULTIPLY'; Lk(e1.outputs[0], e2.inputs[0]); Lk(inv.outputs[0], e2.inputs[1])
e3 = node('ShaderNodeMath', 'inkstrength'); e3.operation = 'MULTIPLY'; e3.inputs[1].default_value = 0.85; Lk(e2.outputs[0], e3.inputs[0])
ink = node('ShaderNodeMix', 'ink'); ink.data_type = 'RGBA'; ink.inputs['B'].default_value = (0.012, 0.008, 0.016, 1); Lk(e3.outputs[0], ink.inputs['Factor']); Lk(rl.outputs['Image'], ink.inputs['A'])
# aerial fog by mist
fog = node('ShaderNodeMix', 'fog'); fog.data_type = 'RGBA'; Lk(rl.outputs['Mist'], fog.inputs['Factor']); Lk(ink.outputs['Result'], fog.inputs['A']); fog.inputs['B'].default_value = (0.8, 0.85, 0.9, 1)
# lens: defocus on depth
dof = node('CompositorNodeDefocus', 'dof'); dof.use_zbuffer = True; dof.blur_max = 40; dof.f_stop = 128
Lk(fog.outputs['Result'], dof.inputs['Image']); Lk(rl.outputs['Depth'], dof.inputs['Z'])
glare = node('CompositorNodeGlare', 'bloom', Type='Bloom'); glare.inputs['Threshold'].default_value = 0.9; glare.inputs['Strength'].default_value = 0.4
Lk(dof.outputs['Image'], glare.inputs['Image'])
hs = node('CompositorNodeHueSat', 'sat'); Lk(glare.outputs['Image'], hs.inputs['Image'])
cb = node('CompositorNodeColorBalance', 'grade'); Lk(hs.outputs['Image'], cb.inputs['Image'])
el = node('CompositorNodeEllipseMask'); el.inputs['Size'].default_value = (0.95, 0.85); blr = node('CompositorNodeBlur'); blr.inputs['Size'].default_value = (300, 300); Lk(el.outputs['Mask'], blr.inputs['Image'])
vg = node('ShaderNodeMix', 'vignette'); vg.data_type = 'RGBA'; vg.blend_type = 'MULTIPLY'; vg.inputs['Factor'].default_value = 0.35; Lk(cb.outputs['Image'], vg.inputs['A'])
vgc = node('CompositorNodeCombineColor'); [Lk(blr.outputs['Image'], vgc.inputs[i]) for i in range(3)]; Lk(vgc.outputs['Image'], vg.inputs['B'])
fl = node('ShaderNodeMix', 'flash'); fl.data_type = 'RGBA'; fl.inputs['Factor'].default_value = 0; fl.inputs['B'].default_value = (1, 1, 1, 1); Lk(vg.outputs['Result'], fl.inputs['A'])
fd2 = node('ShaderNodeMix', 'fade'); fd2.data_type = 'RGBA'; fd2.inputs['Factor'].default_value = 0; fd2.inputs['B'].default_value = (0, 0, 0, 1); Lk(fl.outputs['Result'], fd2.inputs['A'])
Lk(fd2.outputs['Result'], go.inputs[0])

# Blender-only continuous replacement hands use the exported motion markers.
import sys
if KIT not in sys.path: sys.path.insert(0, KIT)
from install_hands import install_hands
install_hands(KIT)
# Set portable paths explicitly even on the first save.
for im in bpy.data.images:
    if im.filepath and not im.packed_file:
        absolute = bpy.path.abspath(im.filepath)
        im.filepath = '//' + os.path.relpath(absolute, KIT)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(KIT, 'film.blend'), relative_remap=True)
print('SAVED film.blend')
