"""Rigged cartoon hand: one continuous skin mesh + a bone rig, posed by joint angles.

make_rigged_hand(name, collection, skin_hex, sleeve_hex, pose) -> root empty (unparented).
Local frame = Three.js-style: +Y 'up the surface', +Z toward the camera, contact surface is z=0.
  'thumbprint' : relaxed open right hand turned on its side; the thumb's pad rests on the glass at the origin,
                 the four fingers curl loosely above the glass (no clenched fist).
  'flat'       : open right hand, palm down; the centre of the palm's underside touches the surface at the origin.
                 Fingers point along +Y, the wrist/sleeve toward -Y.
The hand is posed with real bones (3 per finger, 3 for the thumb) and smooth, distance-based skin weights,
so knuckles fold naturally. Nails and the sleeve are bone-parented and follow the pose. The contact point is
measured from the posed (evaluated) mesh, so the hand never floats above or sinks into the surface."""
import bpy, math
from mathutils import Vector, Matrix, Euler
import numpy as np
from continuous_hands import _Surface, _material, _nail, _apply

# rest design: right hand, back of hand +Z, palm -Z, fingers +Y, wrist at y=0
FINGERS = [('index', -.0295, .071, .0100), ('middle', -.0095, .079, .0106), ('ring', .0105, .073, .0100), ('little', .0295, .057, .0086)]
THUMB_BASE, THUMB_DIR, THUMB_LEN, THUMB_R = Vector((-.024, .018, -.004)), Vector((-.62, .78, 0)).normalized(), (.034, .030, .027), .0138
KNUCKLE_Y = .084

def _segs(L): return (L * .45, L * .30, L * .25)

def _skin_surface():
    s = _Surface()
    s.palm([(-.030, 0, 0, .020, .0150), (0.000, 0, 0, .026, .0160), (.020, -.002, 0, .036, .0170), (.045, 0, 0, .0425, .0170),
            (.068, .001, -.001, .0425, .0155), (.082, .001, -.002, .0370, .0125), (.089, .001, -.002, .0240, .0085), (.092, .001, -.002, .0060, .0030)])
    for _, x, L, r in FINGERS:
        a, b, c = _segs(L); y0 = KNUCKLE_Y
        s.tube([(x, y0 - .012, -.002, r * 1.08), (x, y0, -.002, r * 1.05), (x, y0 + a, -.002, r * .98), (x, y0 + a + b, -.002, r * .92), (x, y0 + L - r * .4, -.002, r * .86), (x, y0 + L, -.002, r * .45)], radial=22, flatten=.86)
        s.ellipsoid((x, y0 + L - r * .55, -.002), (r * .86, r * .95, r * .80))   # round fingertip
    p = THUMB_BASE.copy(); pts = [(p.x - THUMB_DIR.x * .010, p.y - THUMB_DIR.y * .010, p.z, THUMB_R * 1.05)]
    for i, l in enumerate(THUMB_LEN):
        p = p + THUMB_DIR * l; pts.append((p.x, p.y, p.z, THUMB_R * (1.0 - .08 * i)))
    tip = p - THUMB_DIR * (THUMB_R * .5); pts[-1] = (tip.x, tip.y, tip.z, THUMB_R * .5)
    s.tube(pts, radial=26, flatten=.82)
    s.ellipsoid((p.x - THUMB_DIR.x * THUMB_R * .6, p.y - THUMB_DIR.y * THUMB_R * .6, p.z), (THUMB_R * .92, THUMB_R * .92, THUMB_R * .82))
    s.ellipsoid((-.020, .028, -.006), (.017, .025, .0135), -.55)   # thenar mound
    return s

def _bones():
    B = [('palm', Vector((0, -.020, 0)), Vector((0, .070, 0)), None)]
    for n, x, L, r in FINGERS:
        y = KNUCKLE_Y; par = 'palm'
        for i, l in enumerate(_segs(L)):
            B.append((f'{n}_{i}', Vector((x, y, -.002)), Vector((x, y + l, -.002)), par)); par = f'{n}_{i}'; y += l
    p = THUMB_BASE.copy(); par = 'palm'
    for i, l in enumerate(THUMB_LEN):
        B.append((f'thumb_{i}', p.copy(), p + THUMB_DIR * l, par)); par = f'thumb_{i}'; p = p + THUMB_DIR * l
    return B

POSES = {  # bone: (x curl [neg = toward palm], z spread) in degrees
    'point': {'index_0': (-4, 2), 'index_1': (-6, 0), 'index_2': (-4, 0), 'middle_0': (-70, 0), 'middle_1': (-85, 0), 'middle_2': (-55, 0),
              'ring_0': (-72, -3), 'ring_1': (-88, 0), 'ring_2': (-55, 0), 'little_0': (-74, -6), 'little_1': (-88, 0), 'little_2': (-55, 0),
              'thumb_0': (-30, 22), 'thumb_1': (-25, 0), 'thumb_2': (-15, 0)},
    'thumbprint': {'index_0': (-22, 7), 'index_1': (-30, 0), 'index_2': (-18, 0), 'middle_0': (-28, 0), 'middle_1': (-36, 0), 'middle_2': (-22, 0),
                   'ring_0': (-34, -5), 'ring_1': (-40, 0), 'ring_2': (-24, 0), 'little_0': (-40, -11), 'little_1': (-44, 0), 'little_2': (-26, 0),
                   'thumb_0': (-10, -6), 'thumb_1': (-6, 0), 'thumb_2': (-8, 0)},
    'flat': {'index_0': (-6, 7), 'index_1': (-8, 0), 'index_2': (-6, 0), 'middle_0': (-6, 0), 'middle_1': (-9, 0), 'middle_2': (-6, 0),
             'ring_0': (-7, -5), 'ring_1': (-10, 0), 'ring_2': (-7, 0), 'little_0': (-8, -11), 'little_1': (-11, 0), 'little_2': (-8, 0),
             'thumb_0': (-14, 8), 'thumb_1': (-8, 0), 'thumb_2': (-6, 0)},
}
ORIENT = {'point': Euler((math.radians(-28), 0, 0), 'XYZ'), 'thumbprint': Euler((0, math.radians(-36), math.radians(-30)), 'XYZ'), 'flat': Euler((0, 0, 0), 'XYZ')}

def _seg_dist(P, a, b):
    ab = b - a; t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-12), 0, 1); return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)

def make_rigged_hand(name, collection, skin_hex, sleeve_hex, pose='thumbprint'):
    if pose not in POSES: raise ValueError(pose)
    root = bpy.data.objects.new(name, None); collection.objects.link(root); root.empty_display_size = .03; root['hand_pose'] = pose; root['rigged'] = 1
    orient = bpy.data.objects.new(name + '_orient', None); collection.objects.link(orient); orient.parent = root
    skin = _material('Continuous skin ' + skin_hex, skin_hex); cuff = _material('Continuous sleeve ' + sleeve_hex, sleeve_hex, .68, 0, .025); nailmat = _material('Natural warm nail plates', '#E8BC9D', .37, .012, .12)
    # --- skin: one closed, manifold mesh ---
    ob = _skin_surface().object(name + '_Skin', collection, orient, skin)
    rm = ob.modifiers.new('union', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = .0010; rm.use_smooth_shade = True; _apply(ob, rm)
    sm = ob.modifiers.new('soften', 'SMOOTH'); sm.factor = .4; sm.iterations = 5; _apply(ob, sm)
    for p in ob.data.polygons: p.use_smooth = True
    # --- armature ---
    arm = bpy.data.armatures.new(name + '_rig'); rig = bpy.data.objects.new(name + '_Rig', arm); collection.objects.link(rig); rig.parent = orient
    with bpy.context.temp_override(active_object=rig, object=rig, selected_objects=[rig], selected_editable_objects=[rig]):
        bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode='EDIT')
        for bn, h, t, par in _bones():
            e = arm.edit_bones.new(bn); e.head, e.tail = h, t; e.roll = 0
            if par: e.parent = arm.edit_bones[par]; e.use_connect = False
        bpy.ops.object.mode_set(mode='OBJECT')
    ob.parent = rig
    # --- smooth distance-based skin weights (palm uses a sheet of segments) ---
    V = np.array([v.co[:] for v in ob.data.vertices]); bones = _bones(); D = []
    for bn, h, t, _ in bones:
        if bn == 'palm':
            d = np.min([_seg_dist(V, np.array([x, -.03, 0]), np.array([x, .078, 0])) for x in (-.032, -.016, 0, .016, .032)], axis=0)
        else: d = _seg_dist(V, np.array(h[:]), np.array(t[:]))
        D.append(d)
    D = np.array(D); W = 1.0 / (D + .0025) ** 6
    top = np.argsort(-W, axis=0)[:3]; mask = np.zeros_like(W, bool); np.put_along_axis(mask, top, True, axis=0); W = np.where(mask, W, 0); W /= W.sum(0)
    for bi, (bn, *_ ) in enumerate(bones):
        g = ob.vertex_groups.new(name=bn); idx = np.nonzero(W[bi] > .01)[0]
        for i in idx: g.add([int(i)], float(W[bi, i]), 'REPLACE')
    md = ob.modifiers.new('rig', 'ARMATURE'); md.object = rig
    sub = ob.modifiers.new('silhouette', 'SUBSURF'); sub.levels = 0; sub.render_levels = 1
    # --- nails + sleeve, bone-parented so they follow the fold ---
    def bone_child(o, bone):
        Mb = arm.bones[bone].matrix_local.copy(); Mb.translation = arm.bones[bone].tail_local
        o.parent = rig; o.parent_type = 'BONE'; o.parent_bone = bone; o.matrix_parent_inverse = Mb.inverted(); o.matrix_basis = Matrix.Identity(4)
    for n, x, L, r in FINGERS:
        nl = _nail(name + '_' + n + 'Nail', collection, orient, (x, KNUCKLE_Y + L - r * .75, -.002 + r * .80), (0, 1, 0), r * 1.25, r * 1.45, nailmat, (0, 0, 1))
        bone_child(nl, f'{n}_2')
    tp = THUMB_BASE + THUMB_DIR * (sum(THUMB_LEN) - THUMB_R * .8)
    nl = _nail(name + '_ThumbNail', collection, orient, (tp.x, tp.y, tp.z + THUMB_R * .76), tuple(THUMB_DIR), THUMB_R * 1.15, THUMB_R * 1.3, nailmat, (0, 0, 1)); bone_child(nl, 'thumb_2')
    sl = _Surface(); sl.palm([(-.200, 0, 0, .0230, .0190), (-.120, 0, 0, .0225, .0185), (-.045, 0, 0, .0215, .0175), (-.020, 0, 0, .0210, .0170)])
    slo = sl.object(name + '_Sleeve', collection, orient, cuff); bv = slo.modifiers.new('edge', 'BEVEL'); bv.width = .0012; bv.segments = 3
    bone_child(slo, 'palm')
    # --- pose ---
    for bn, (cx, sz) in POSES[pose].items():
        pb = rig.pose.bones[bn]; pb.rotation_mode = 'XYZ'; pb.rotation_euler = (math.radians(cx), 0, math.radians(sz))
    orient.rotation_euler = ORIENT[pose]
    # --- contact alignment from the evaluated (posed) skin ---
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    M = root.matrix_world.inverted() @ ob.matrix_world; P = np.array([(M @ v.co)[:] for v in ev.data.vertices])
    if pose in ('thumbprint', 'point'):
        gi = ob.vertex_groups['thumb_2' if pose == 'thumbprint' else 'index_2'].index; tw = np.array([max([g.weight for g in v.groups if g.group == gi] or [0]) for v in ob.data.vertices])
        cand = P[tw > .5] if (tw > .5).sum() > 20 else P
    else:
        gi = ob.vertex_groups['palm'].index; tw = np.array([max([g.weight for g in v.groups if g.group == gi] or [0]) for v in ob.data.vertices])
        cand = P[tw > .6]
    zmin = cand[:, 2].min(); pad = cand[cand[:, 2] < zmin + .0025]; c = pad.mean(0)
    orient.location = (-c[0], -c[1], -zmin)
    root['skin_object'] = ob.name; root['rig_object'] = rig.name; root['skin_vertices'] = len(ob.data.vertices)
    return root

# sprite-driven hands: key -> (skin, sleeve, pose). 'grip' uses the continuous phone-grip hand; others are rigged.
PRESS_SPECS={'thumb':('#edbd94','#6c7d88','thumbprint'),'fist':('#edbd94','#9c3044','flat'),'click':('#edbd94','#9c3044','flat'),
             'tap':('#edc8ac','#239ca6','point'),'hold':('#edc8ac','#239ca6','grip')}
def make_press_hand(key,coll):
    import bpy
    skin,sleeve,pose=PRESS_SPECS[key]
    if pose=='grip':
        from continuous_hands import create_hand
        root=create_hand('hand_press_'+key,coll,skin,sleeve,pose='grip')
    else:
        from rig_hands import make_rigged_hand
        root=make_rigged_hand('hand_press_'+key,coll,skin,sleeve,pose=pose)
    root.parent=bpy.data.objects['Y_UP'];root['sprite_key']=key;root['hand_pose']=pose
    for child in root.children_recursive:child.hide_render=True
    return root
