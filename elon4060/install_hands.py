"""Install continuous Blender hands, driven by the original exported motion markers."""
import bpy, json, os
from mathutils import Matrix
from continuous_hands import create_hand

def install_hands(kit):
    sc=bpy.context.scene
    for path in sorted(__import__('glob').glob(os.path.join(kit,'data','sets','*.json'))):
        name=os.path.basename(path)[:-5];S=json.load(open(path));rs=S['meshes'];coll=bpy.data.collections['set_'+name]
        for i,r in enumerate(rs):
            if not all(abs(a-b)<1e-6 for a,b in zip(r['m'][12:15],[.006,-.03,-.022])):continue
            if abs(r['m'][5]-1.15)>1e-5 or abs(r['m'][10]-.5)>1e-5:continue
            ids=[q['id'] for q in rs[i:i+21]]
            skin=r['mats'][0]['color'];sleeve=rs[i+19]['mats'][0]['color']
            root=create_hand('hand_grip_'+r['id'],coll,skin,sleeve,pose='grip')
            root.parent=bpy.data.objects['Y_UP'];root['motion_marker']=r['id'];root['source_set']=name
            root['legacy_ids']=json.dumps(ids);root['hand_pose']='grip'
            for n in ids:
                ob=bpy.data.objects.get(n)
                if ob:ob['hand_legacy']=1;ob.hide_render=True
            for child in root.children_recursive:child.hide_render=True
            if name=='apartment' and not sc.get('tablet_surface_id'):
                sc['tablet_surface_id']=rs[i-1]['id']
    coll=bpy.data.collections.get('pools')
    for key,sleeve in [('thumb','#6c7d88'),('fist','#9c3044'),('click','#9c3044')]:
        from rig_hands import make_rigged_hand
        root=make_rigged_hand('hand_press_'+key,coll,'#edbd94',sleeve,pose='thumbprint' if key=='thumb' else 'flat')
        root.parent=bpy.data.objects['Y_UP'];root['sprite_key']=key;root['hand_pose']='press'
        for child in root.children_recursive:child.hide_render=True
    sc['continuous_hands_version']='v2'
    print('Installed continuous Blender hands; tablet screen',sc.get('tablet_surface_id'))
