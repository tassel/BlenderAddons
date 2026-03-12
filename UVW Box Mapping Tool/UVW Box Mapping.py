bl_info = {
    "name": "UVW Box Mapping Tool",
    "author": "Broomstick",
    "version": (1, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > UVW Box Map",
    "description": "Simulates 3ds Max-style UVW Box Mapping with tiling",
    "category": "BRS Tools",
}

import bpy
import bmesh
from bpy.props import FloatProperty
from bpy.types import Operator, Panel, PropertyGroup


class UVWBoxSettings(PropertyGroup):
    scale_x: FloatProperty(name="Tiling X", default=1.0, min=0.001)
    scale_y: FloatProperty(name="Tiling Y", default=1.0, min=0.001)
    scale_z: FloatProperty(name="Tiling Z", default=1.0, min=0.001)


class UVWBoxMapOperator(Operator):
    bl_idname = "uv.uvw_box_map"
    bl_label = "Apply UVW Box Mapping"
    bl_description = "Apply box projection UVs using face normals"

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        settings = context.scene.uvw_box_settings

        # Ensure we're in EDIT mode
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.verify()
        bm.faces.ensure_lookup_table()

        for face in bm.faces:
            normal = face.normal.normalized()
            axis = max(range(3), key=lambda i: abs(normal[i]))
            for loop in face.loops:
                co = loop.vert.co
                uv = loop[uv_layer].uv

                if axis == 0:  # X projection
                    uv.x = co.y / settings.scale_y
                    uv.y = co.z / settings.scale_z
                elif axis == 1:  # Y projection
                    uv.x = co.x / settings.scale_x
                    uv.y = co.z / settings.scale_z
                else:  # Z projection
                    uv.x = co.x / settings.scale_x
                    uv.y = co.y / settings.scale_y

        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}


class UVWBoxMapPanel(Panel):
    bl_label = "UVW Box Map"
    bl_idname = "VIEW3D_PT_uvw_box_map"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BRS Tools"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.uvw_box_settings

        layout.prop(settings, "scale_x")
        layout.prop(settings, "scale_y")
        layout.prop(settings, "scale_z")
        layout.operator("uv.uvw_box_map")


classes = (
    UVWBoxSettings,
    UVWBoxMapOperator,
    UVWBoxMapPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.uvw_box_settings = bpy.props.PointerProperty(type=UVWBoxSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.uvw_box_settings


if __name__ == "__main__":
    register()
