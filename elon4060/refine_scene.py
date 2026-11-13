"""Apply the reviewed hand revision and colour response without reimporting the sets."""
import bpy,os,sys,json,math
from mathutils import Matrix
KIT=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,KIT)
from continuous_hands import create_hand
sc=bpy.context.scene
bpy.context.preferences.filepaths.save_version=0
from rig_hands import make_press_hand, PRESS_SPECS
_pool=bpy.data.collections.get('pools')
for root in [o for o in bpy.data.objects if o.get('sprite_key')]:
    for child in list(root.children_recursive):bpy.data.objects.remove(child,do_unlink=True)
    bpy.data.objects.remove(root,do_unlink=True)
for key in PRESS_SPECS: make_press_hand(key,_pool)
# Bright film lights need restrained hand reflectance to retain sculpted anatomy.
for m in bpy.data.materials:
    if not m.node_tree or not (m.name.startswith('Continuous skin ') or m.name.startswith('Natural warm nail')):continue
    if m.get('reviewed_reflectance'):continue
    bs=m.node_tree.nodes.get('Principled BSDF')
    if bs:
        v=bs.inputs['Base Color'].default_value
        bs.inputs['Base Color'].default_value=(v[0]*.34,v[1]*.34,v[2]*.34,1)
        bs.inputs['Specular IOR Level'].default_value=.22
        m['reviewed_reflectance']=True
# Preserve the painted sand design, with the CC0 normal supplying subdued relief.
S=json.load(open(os.path.join(KIT,'data/sets/ocean.json')))
for r in S['meshes']:
 for mt in r['mats']:
    if mt.get('name')!='ph:sand':continue
    m=bpy.data.materials[mt['id']];nt=m.node_tree
    # Locate existing base-colour multiplier, and replace its photographic source with painted tex.
    tex=nt.nodes.get('tex_'+mt['map']['id'])
    for n in nt.nodes:
        if n.type=='BSDF_PRINCIPLED' and tex:
            source=n.inputs['Base Color'].links[0].from_node
            if source.type=='MIX':nt.links.new(tex.outputs['Color'],source.inputs['B'])
        if n.type=='NORMAL_MAP':n.inputs['Strength'].default_value=.065
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(KIT,'film.blend'))
print('Saved reviewed hand and lighting revision')
