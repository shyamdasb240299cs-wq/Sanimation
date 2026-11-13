"""Continuous, stylised anatomical hands for the polished film.

All positions are Three.js coordinates: +Y up, +Z towards the viewer. Parent the
returned empty to the film's Y_UP object. A grip is sized for a phone centred at
(0, 0, 0), measuring 0.075 x 0.155 x 0.009 m, with its screen facing +Z.
A press has its thumb-pad contact at the origin and its wrist down and right.

create_hand(name, collection, skin_srgbhex, sleeve_srgbhex, pose='grip') returns
an empty containing ONE continuous, closed skin mesh, five shaped nail plates,
and a sleeve. The skin is a voxel union of carefully tapered surface lofts; it
has no separated knuckle balls, finger capsules, or interphalangeal seams.
It needs no armature. Animate the returned empty for a small grip/press motion.
"""
import math
import bpy
import bmesh
from mathutils import Vector


def _linear_hex(value):
    value = value.lstrip('#')
    rgb = [int(value[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb) + (1.0,)


def _material(name, colour, roughness=.48, subsurface=.035, coat=.12):
    mat = bpy.data.materials.get(name)
    if mat:
        if not any(n.bl_idname == 'ShaderNodeOutputAOV' and n.aov_name == 'card' for n in mat.node_tree.nodes):
            aov=mat.node_tree.nodes.new('ShaderNodeOutputAOV');aov.aov_name='card';aov.inputs['Value'].default_value=.78
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    base=_linear_hex(colour)
    reviewed=name.startswith('Continuous skin ') or name.startswith('Natural warm nail')
    shader.inputs['Base Color'].default_value = tuple(v*.34 for v in base[:3])+(1,) if reviewed else base
    if reviewed: mat['reviewed_reflectance']=True
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Subsurface Weight'].default_value = subsurface
    shader.inputs['Coat Weight'].default_value = coat
    shader.inputs['Coat Roughness'].default_value = .38
    shader.inputs['Specular IOR Level'].default_value = .22
    mat.diffuse_color = _linear_hex(colour)
    aov=mat.node_tree.nodes.new('ShaderNodeOutputAOV')
    aov.aov_name='card'
    aov.inputs['Value'].default_value=.78
    return mat


def _catmull(points, per_segment=7):
    """Smooth centreline with separate radius and dorsal-width channels."""
    result = []
    for i in range(len(points) - 1):
        a, b, c, d = [points[max(0, min(len(points)-1, j))] for j in (i-1, i, i+1, i+2)]
        for step in range(per_segment):
            t = step / float(per_segment)
            result.append(tuple(.5 * ((2*b[k]) + (-a[k]+c[k])*t + (2*a[k]-5*b[k]+4*c[k]-d[k])*t*t + (-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in range(len(b))))
    result.append(points[-1])
    return result


class _Surface:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def tube(self, control, radial=20, flatten=.88):
        """Closed continuous finger with an elliptical, tapering section."""
        path = _catmull(control)
        start = len(self.vertices)
        for j, p in enumerate(path):
            centre = Vector(p[:3])
            before = Vector(path[max(j-1, 0)][:3])
            after = Vector(path[min(j+1, len(path)-1)][:3])
            tangent = (after-before).normalized()
            # A stable dorsal direction keeps the fingers softly flattened.
            dorsal = Vector((0, 0, 1))
            dorsal -= tangent * dorsal.dot(tangent)
            if dorsal.length < .05:
                dorsal = Vector((0, 1, 0)) - tangent * tangent.y
            dorsal.normalize()
            side = tangent.cross(dorsal).normalized()
            for k in range(radial):
                angle = 2 * math.pi * k / radial
                self.vertices.append(tuple(centre + side * (p[3] * math.cos(angle)) + dorsal * (p[3] * flatten * math.sin(angle))))
        for j in range(len(path)-1):
            for k in range(radial):
                a = start+j*radial+k
                b = start+j*radial+(k+1)%radial
                self.faces.append((a,b,b+radial,a+radial))
        lo = len(self.vertices)
        self.vertices.append(tuple(path[0][:3]))
        hi = len(self.vertices)
        self.vertices.append(tuple(path[-1][:3]))
        for k in range(radial):
            self.faces.append((lo,start+(k+1)%radial,start+k))
            a = start+(len(path)-1)*radial+k
            b = start+(len(path)-1)*radial+(k+1)%radial
            self.faces.append((hi,a,b))

    def palm(self, rows, radial=40):
        """Palm/wrist loft: (y, centre-x, centre-z, half-width, half-depth)."""
        smooth = _catmull(rows, 5)
        start = len(self.vertices)
        for y, x, z, width, depth in smooth:
            for k in range(radial):
                a = 2*math.pi*k/radial
                self.vertices.append((x+width*math.cos(a), y, z+depth*math.sin(a)))
        for j in range(len(smooth)-1):
            for k in range(radial):
                a = start+j*radial+k
                b = start+j*radial+(k+1)%radial
                self.faces.append((a,a+radial,b+radial,b))
        for end, rev in ((0,True),(len(smooth)-1,False)):
            y,x,z,w,d = smooth[end]
            cap = len(self.vertices)
            self.vertices.append((x,y,z))
            for k in range(radial):
                a,b=start+end*radial+k,start+end*radial+(k+1)%radial
                self.faces.append((cap,b,a) if rev else (cap,a,b))

    def ellipsoid(self, centre, scale, rotation=0):
        start = len(self.vertices)
        rings, sides = 22, 36
        cr,sr=math.cos(rotation),math.sin(rotation)
        for j in range(rings+1):
            phi=math.pi*j/rings
            for k in range(sides):
                theta=2*math.pi*k/sides
                x=scale[0]*math.sin(phi)*math.cos(theta)
                y=scale[1]*math.sin(phi)*math.sin(theta)
                z=scale[2]*math.cos(phi)
                self.vertices.append((centre[0]+cr*x-sr*y,centre[1]+sr*x+cr*y,centre[2]+z))
        for j in range(rings):
            for k in range(sides):
                a=start+j*sides+k
                b=start+j*sides+(k+1)%sides
                self.faces.append((a,b,b+sides,a+sides))

    def object(self, name, collection, parent, material):
        mesh=bpy.data.meshes.new(name+'_mesh')
        mesh.from_pydata(self.vertices,[],self.faces)
        mesh.update()
        # Recalculate before the voxel union, so every contributing volume has
        # outward normals despite independently authored loft directions.
        bm=bmesh.new();bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
        bm.to_mesh(mesh);bm.free()
        obj=bpy.data.objects.new(name,mesh)
        collection.objects.link(obj)
        obj.parent=parent
        obj.data.materials.append(material)
        for polygon in mesh.polygons:
            polygon.use_smooth=True
        return obj


def _apply(obj, modifier):
    with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj], selected_editable_objects=[obj]):
        bpy.ops.object.modifier_apply(modifier=modifier.name)


def _nail(name, collection, parent, centre, tangent, width, length, material, dorsal=(0,0,1)):
    """A thin domed, rounded-square plate; natural ivory/pink, never emissive."""
    up=Vector(dorsal).normalized()
    axis=Vector(tangent)
    axis-=up*axis.dot(up)
    axis.normalize()
    side=axis.cross(up).normalized()
    surface=_Surface()
    rings,sides=5,32
    surface.vertices.append(tuple(Vector(centre)+up*.00035))
    for j in range(1,rings+1):
        r=j/rings
        for k in range(sides):
            a=2*math.pi*k/sides
            # Superellipse subtly squares the tip without corners.
            c,s=math.cos(a),math.sin(a)
            u=math.copysign(abs(c)**.78,c)*width*.5*r
            v=math.copysign(abs(s)**.78,s)*length*.5*r
            dome=.00035*(1-r*r)-.00035*(u/(width*.5))**2
            surface.vertices.append(tuple(Vector(centre)+side*u+axis*v+up*dome))
    for k in range(sides):
        surface.faces.append((0,1+k,1+(k+1)%sides))
    for j in range(rings-1):
        for k in range(sides):
            a=1+j*sides+k;b=1+j*sides+(k+1)%sides
            surface.faces.append((a,a+sides,b+sides,b))
    obj=surface.object(name,collection,parent,material)
    solid=obj.modifiers.new('Natural nail plate thickness','SOLIDIFY')
    solid.thickness=.00022
    solid.offset=-1
    bevel=obj.modifiers.new('Soft nail perimeter','BEVEL')
    bevel.width=.00016
    bevel.segments=3
    return obj


def _components(mesh):
    adjacency=[[] for _ in mesh.vertices]
    for edge in mesh.edges:
        a,b=edge.vertices
        adjacency[a].append(b);adjacency[b].append(a)
    unseen=set(range(len(mesh.vertices)));count=0
    while unseen:
        count+=1;stack=[unseen.pop()]
        while stack:
            for neighbour in adjacency[stack.pop()]:
                if neighbour in unseen:
                    unseen.remove(neighbour);stack.append(neighbour)
    bm=bmesh.new();bm.from_mesh(mesh)
    nonmanifold=sum(not edge.is_manifold for edge in bm.edges)
    bm.free()
    return count,nonmanifold


def create_hand(name, collection, skin_srgbhex, sleeve_srgbhex, pose='grip'):
    """Return an unparented root empty; caller supplies position and Y_UP parent.

    Grip: phone local origin at its centre. Press: thumb's pad contact is the
    local origin. Use uniform scale to match a differently sized device.
    The root stores mesh name, connected-component count, and manifold QA.
    """
    if pose not in ('grip','press','edge','flat'):
        raise ValueError("Hand pose must be 'grip', 'press', 'edge' or 'flat'")
    root=bpy.data.objects.new(name,None)
    collection.objects.link(root)
    root.empty_display_type='PLAIN_AXES'
    root.empty_display_size=.025
    root['hand_pose']=pose
    root['coordinate_system']='Three.js Y-up; screen/camera +Z'
    skin=_material('Continuous skin '+skin_srgbhex,skin_srgbhex)
    cuff=_material('Continuous sleeve '+sleeve_srgbhex,sleeve_srgbhex,.68,0,.025)
    # A natural translucent pink/ivory nail, distinct from shiny white dots.
    nailmat=_material('Natural warm nail plates','#E8BC9D',.37,.012,.12)
    surface=_Surface()
    nails=[]
    if pose=='grip':
        surface.palm([
            (-.130,.008,-.023,.0125,.0090),
            (-.104,.007,-.023,.0135,.0100),
            (-.079,.006,-.024,.0180,.0110),
            (-.059,.005,-.024,.0260,.0140),
            (-.028,.005,-.024,.0310,.0155),
            (.003,.006,-.025,.0290,.0140),
            (.025,.007,-.025,.0240,.0115),
            (.037,.010,-.026,.0160,.0090),
            (.040,.011,-.026,.0070,.0060)])
        # Roots lie inside the palm. Pads turn around the device edge and rest
        # gently on the front bezel. Length/radius varies by finger.
        fingers=[('Index',.032,.0058,.032),('Middle',.010,.0063,.029),('Ring',-.012,.0059,.031),('Little',-.034,.0049,.035)]
        for label,y,r,tipx in fingers:
            path=[(.027,y,-.026,r*1.10),(.041,y-.001,-.023,r*1.08),(.050,y-.004,-.012,r),(.049,y-.008,.002,r*.94),(.041,y-.010,.010,r*.86),(tipx,y-.010,.011,r*.67),(tipx-.003,y-.010,.0105,r*.28)]
            surface.tube(path)
            nails.append((label,(tipx+.0013,y-.010,.011+r*.70),(-1,0,-.05),r*1.26,r*1.63,(0,0,1)))
        thumb=[(-.010,-.043,-.026,.0105),(-.026,-.056,-.021,.0100),(-.040,-.061,-.008,.0088),(-.043,-.055,.004,.0080),(-.034,-.045,.011,.0068),(-.027,-.041,.0115,.0048),(-.025,-.040,.0105,.0019)]
        surface.tube(thumb,radial=24,flatten=.83)
        nails.append(('Thumb',(-.031,-.043,.0167),(.8,.6,0),.0101,.0122,(0,0,1)))
        sleeve=_Surface()
        sleeve.palm([(-.190,.008,-.023,.0170,.0125),(-.155,.008,-.023,.0160,.012),(-.132,.008,-.023,.0154,.0118),(-.124,.008,-.023,.0150,.0115)])
    elif pose=='edge':
        # THUMBPRINT (relaxed open hand). Origin = thumb-pad contact on the glass (z=0, +z toward camera).
        # The hand stands edge-on like a handshake: palm faces -x, wrist below (-y). The short, broad thumb
        # lies along the glass with its pad on the scanner; the four fingers curl loosely upward beside it,
        # stacked away from the glass (index nearest the camera), never clenched into a fist.
        surface.palm([
            (-.118,.074,.040,.0150,.0230),
            (-.100,.072,.040,.0165,.0270),
            (-.080,.069,.039,.0175,.0310),
            (-.058,.067,.038,.0178,.0330),
            (-.038,.066,.038,.0170,.0320),
            (-.026,.066,.038,.0150,.0280),
            (-.020,.066,.038,.0110,.0200),
            (-.017,.066,.038,.0040,.0060)])
        fingers=[('Index',.062,.0098),('Middle',.044,.0102),('Ring',.028,.0096),('Little',.015,.0082)]
        for label,z,r in fingers:
            path=[(.068,-.030,z,r*1.10),(.068,-.004,z,r*1.04),(.064,.020,z,r),(.054,.038,z-.002,r*.94),(.043,.043,z-.003,r*.84),(.037,.041,z-.003,r*.38)]
            surface.tube(path,radial=20)
            nails.append((label,(.039,.044,z-.003+r*.15),(-1,0,0),r*1.2,r*1.4,(0,1,0)))
        surface.ellipsoid((.054,-.064,.022),(.0175,.0260,.0150),.55)      # thenar mound
        thumb=[(.058,-.070,.020,.0145),(.042,-.050,.014,.0138),(.026,-.031,.0105,.0126),(.012,-.014,.0086,.0110),(.003,-.003,.0076,.0098),(-.002,.006,.0073,.0060)]
        surface.tube(thumb,radial=28,flatten=.78)
        surface.ellipsoid((.000,-.001,.0070),(.0098,.0118,.0070),-.6)     # broad flattened pad on the glass
        nails.append(('Thumb',(.0005,.0005,.0150),(-.55,.83,0),.0120,.0130,(0,0,1)))
        sleeve=_Surface()
        sleeve.palm([(-.260,.074,.040,.0200,.0330),(-.200,.074,.040,.0195,.0320),(-.150,.074,.040,.0185,.0300),(-.125,.074,.040,.0180,.0290)])
    elif pose=='flat':
        # OPEN HAND, palm down. Origin = centre of the palm's underside (z=0 is the surface it presses).
        # Fingers point along +y, wrist/sleeve toward -y, thumb splays to -x (a right hand seen from above).
        surface.palm([
            (-.125,.000,.014,.0150,.0110),
            (-.100,.000,.014,.0175,.0118),
            (-.078,.000,.013,.0300,.0135),
            (-.050,.000,.0125,.0390,.0125),
            (-.020,.000,.0122,.0410,.0122),
            (.008,.000,.0120,.0395,.0115),
            (.020,.000,.0118,.0340,.0090),
            (.026,.000,.0118,.0200,.0050),
            (.028,.000,.0118,.0040,.0015)])
        fingers=[('Index',-.028,.0108,.070),('Middle',-.008,.0112,.077),('Ring',.012,.0106,.071),('Little',.031,.0090,.056)]
        for label,x,r,L in fingers:
            path=[(x,.004,.0122,r*1.12),(x*1.04,.004+L*.40,.0118,r),(x*1.08,.004+L*.75,.0098,r*.93),(x*1.10,.004+L*.97,.0072,r*.82),(x*1.10,.006+L,.0066,r*.36)]
            surface.tube(path,radial=20)
            nails.append((label,(x*1.10,.004+L*.93,.0072+r*.78),(0,1,0),r*1.22,r*1.5,(0,0,1)))
        surface.ellipsoid((-.034,-.050,.0115),(.0200,.0270,.0120),-.45)   # thenar
        thumb=[(-.034,-.058,.0122,.0150),(-.050,-.038,.0116,.0138),(-.062,-.018,.0106,.0124),(-.068,.000,.0096,.0110),(-.070,.012,.0092,.0090),(-.070,.018,.0090,.0040)]
        surface.tube(thumb,radial=24,flatten=.85)
        nails.append(('Thumb',(-.070,.008,.0092+.0092),(-.1,1,0),.0118,.0130,(0,0,1)))
        sleeve=_Surface()
        sleeve.tube([(0,-.230,.014,.0190),(0,-.185,.014,.0182),(0,-.150,.014,.0172),(0,-.135,.014,.0165)],radial=32,flatten=.82)
    else:
        # A true opposed thumb: it grows from the SIDE thenar mound, bends
        # across the palm at the MCP joint, then turns its broad distal pad
        # toward the glass. Visible thumb length is only about 39 mm against
        # a 75 mm palm. The fist is close to the screen, never a long pointer.
        # Palm and wrist share the SAME loft, so there is no union collar or
        # cap seam around the wrist. The diagonal row centres follow the arm.
        surface.palm([
            (-.170,.101,.025,.0125,.0100),
            (-.145,.090,.025,.0130,.0105),
            (-.120,.077,.027,.0148,.0120),
            (-.102,.067,.029,.0180,.0130),
            (-.090,.060,.030,.0230,.0140),
            (-.073,.050,.030,.0280,.0145),
            (-.053,.041,.030,.0290,.0150),
            (-.036,.033,.030,.0250,.0130),
            (-.025,.029,.030,.0175,.0090),
            (-.021,.029,.030,.0100,.0060),
            (-.019,.029,.030,.0030,.0020)])
        surface.ellipsoid((.019,-.044,.023),(.0185,.0220,.0140),.38)
        thumb=[(.025,-.050,.030,.0120),(.014,-.039,.028,.0112),(.002,-.028,.023,.0102),(-.006,-.018,.0155,.0088),(-.004,-.009,.0092,.0076),(0,-.001,.0067,.0065),(.001,.004,.0063,.0034)]
        surface.tube(thumb,radial=28,flatten=.90)
        # The contact pad reaches the screen plane at local (0,0,0).
        surface.ellipsoid((0,0,.0065),(.0067,.0083,.0065),-.18)
        # Distal thumbnail follows the tilted dorsal surface almost to the
        # fingertip. It is neither a white dot nor a plate halfway up a digit.
        nails.append(('Thumb',(-.0018,-.0045,.0146),(.18,.98,-.28),.0104,.0112,(0,.28,.96)))
        # Closed fist: fingertips tuck fully into the palm; only thumb extends.
        curls=[('Index',.020,-.035,.0069),('Middle',.034,-.030,.0072),('Ring',.047,-.033,.0067),('Little',.058,-.041,.0058)]
        for label,x,y,r in curls:
            path=[(x+.005,y-.018,.030,r*1.12),(x+.002,y-.006,.036,r*1.12),(x,y+.001,.032,r),(x-.001,y-.003,.022,r),(x+.001,y-.014,.020,r*.88),(x+.003,y-.021,.026,r*.55)]
            surface.tube(path)
            nails.append((label,(x,y-.012,.0138),(0,-1,0),r*1.16,r*1.35,(0,0,-1)))
        sleeve=_Surface()
        sleeve.tube([(.129,-.222,.025,.0180),(.112,-.190,.025,.0170),(.099,-.165,.025,.0156),(.095,-.156,.025,.0154)],radial=32,flatten=.83)
    skinobj=surface.object(name+'_ContinuousSkin',collection,root,skin)
    remesh=skinobj.modifiers.new('Continuous anatomical union','REMESH')
    remesh.mode='VOXEL'
    remesh.voxel_size=.00072
    remesh.use_smooth_shade=True
    _apply(skinobj,remesh)
    smoothing=skinobj.modifiers.new('Soft connective tissue','SMOOTH')
    smoothing.factor=.40
    smoothing.iterations=6
    _apply(skinobj,smoothing)
    for p in skinobj.data.polygons:
        p.use_smooth=True
    count,nonmanifold=_components(skinobj.data)
    root['skin_object']=skinobj.name
    root['skin_connected_components']=count
    root['skin_nonmanifold_edges']=nonmanifold
    root['skin_vertices']=len(skinobj.data.vertices)
    if count != 1 or nonmanifold:
        raise RuntimeError('%s: hand union failed (%d components, %d non-manifold edges)'%(name,count,nonmanifold))
    # Actual topology is already manifold. The final surface subdivision gives
    # smooth silhouettes at 1080x1920 with no finger-ball join marks.
    subdivision=skinobj.modifiers.new('Polished continuous silhouette','SUBSURF')
    subdivision.subdivision_type='CATMULL_CLARK'
    subdivision.levels=1
    subdivision.render_levels=1
    for label,centre,tangent,width,length,dorsal in nails:
        _nail(name+'_'+label+'Nail',collection,root,centre,tangent,width,length,nailmat,dorsal)
    cuffobj=sleeve.object(name+'_Sleeve',collection,root,cuff)
    bevel=cuffobj.modifiers.new('Soft fabric edge','BEVEL')
    bevel.width=.0009;bevel.segments=3
    root['nail_count']=len(nails)
    root['cuff_max_y']=max(v.co.y for v in cuffobj.data.vertices)
    return root
