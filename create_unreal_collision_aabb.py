
# install:
#   in Blender, Edit menu -> Preferences -> Install
#   choose this py file
#   then enable this python file in the list "Add Mesh: Create Unreal Collision AABB"

# typical usage:
#   select objects to bound with a box, then shift+A to get the add menu, go to Mesh sub menu, then choose "Create Unreal Collision AABB"
#   the created box will be located under a collection with the name "Collision_" + the name of the first selected object, the collection will be
#     created if it doesn't exist
#   all created boxes get the prefix "UBX_" so on import into Unreal they will be treated as collision
#   if needed, it is safe to rotate the box after creation

# exporting:
#   select all the cosmetic geometry and all the collision boxes
#   choose to export fbx with the selected objects option checked

bl_info = {
    "name": "Create Unreal Collision AABB",
    "author": "Bob Parkinson Jr.",
    "version": (1,15),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Create Unreal Collision AABB",
    "description": "Create a mesh AABB that encompasses all selected objects",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh",
}

import bpy
import bmesh
from bpy.props import BoolProperty, FloatVectorProperty
import mathutils
from bpy_extras import object_utils

def get_box_info(width, height, depth):
    verts = [(+1.0, +1.0, -1.0),
             (+1.0, -1.0, -1.0),
             (-1.0, -1.0, -1.0),
             (-1.0, +1.0, -1.0),
             (+1.0, +1.0, +1.0),
             (+1.0, -1.0, +1.0),
             (-1.0, -1.0, +1.0),
             (-1.0, +1.0, +1.0),
             ]

    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7),
            ]

    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces

def update_collection(context, name):
    scene = context.scene

    coll = bpy.data.collections.get(name)

    # if it doesn't exist create it
    if coll is None:
        coll = bpy.data.collections.new(name)

    # if it is not linked to scene colleciton treelink it
    if not scene.user_of_id(coll):
        context.collection.children.link(coll)

    return coll

class CreateAABB(bpy.types.Operator, object_utils.AddObjectHelper):
    """Create a mesh AABB that encompasses all selected objects"""
    bl_idname = "mesh.boundbox_add"
    bl_label = "Create Unreal Collision AABB"
    bl_description = "Create a mesh AABB that encompasses all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    view_align : BoolProperty(name="Align to View", default=False,)
    location : FloatVectorProperty(name="Location", subtype='TRANSLATION',)
    rotation : FloatVectorProperty(name="Rotation", subtype='EULER',)

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        minx, miny, minz = (999999.0,) * 3
        maxx, maxy, maxz = (-999999.0,) * 3
        base_name = ""
        for obj in context.selected_objects:
            if base_name == "":
                base_name = obj.name
                dot_index = base_name.find('.')
                if dot_index >= 0:
                    base_name = base_name[0:dot_index]

            for v in obj.bound_box:
                v_world = obj.matrix_world @ mathutils.Vector((v[0], v[1], v[2]))

                if v_world[0] < minx:
                    minx = v_world[0]
                if v_world[0] > maxx:
                    maxx = v_world[0]

                if v_world[1] < miny:
                    miny = v_world[1]
                if v_world[1] > maxy:
                    maxy = v_world[1]

                if v_world[2] < minz:
                    minz = v_world[2]
                if v_world[2] > maxz:
                    maxz = v_world[2]

        verts, faces = get_box_info((maxx - minx) / 2, (maxz - minz) / 2, (maxy - miny) / 2)

        mesh_name = ""
        coll = None
        if base_name == "":
            mesh_name = "UBX_AABB"
        else:
            coll = update_collection(context, "Collision_" + base_name)
            mesh_base_name = "UBX_" + base_name
            dot_index = mesh_base_name.find('.')
            if dot_index >= 0:
              mesh_base_name = mesh_base_name[0:dot_index]
            mesh_name = mesh_base_name + "_0"
            counter = 0
            while bpy.context.scene.objects.get(mesh_name):
                mesh_name = mesh_base_name + "_" + str(counter)
                counter = counter + 1

        mesh = bpy.data.meshes.new(mesh_name)

        bm = bmesh.new()
        for v_co in verts:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()
        self.location[0] = minx + ((maxx - minx) / 2)
        self.location[1] = miny + ((maxy - miny) / 2)
        self.location[2] = minz + ((maxz - minz) / 2)
        bbox = object_utils.object_data_add(context, mesh, operator=self)
        bbox.display_type = 'WIRE'
        bbox.hide_render = True

        if coll != None:
            try:
                bpy.context.scene.collection.objects.unlink(bbox)
            except:
                pass
            try:
                coll.objects.link(bbox)
            except:
                pass

        return {'FINISHED'}

def menu_boundbox(self, context):
    self.layout.operator(CreateAABB.bl_idname, text=CreateAABB.bl_label, icon="PLUGIN")

def register():
    bpy.utils.register_class(CreateAABB)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_boundbox)

def unregister():
    bpy.utils.unregister_class(CreateAABB)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_boundbox)

if __name__ == "__main__":
    register()
