bl_info = {
    "name": "Quick Batch Rename Objects and Materials",
    "author": "Tassel",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Batch Rename",
    "description": "Batch rename selected objects and all materials with prefix/suffix options",
    "category": "Tassel Tools",
}

import bpy

class BatchRenamerProperties(bpy.types.PropertyGroup):
    remove_prefix: bpy.props.StringProperty(name="Remove Prefix", default="")
    add_prefix: bpy.props.StringProperty(name="Add Prefix", default="")
    add_suffix: bpy.props.StringProperty(name="Add Suffix", default="")
    rename_objects: bpy.props.BoolProperty(name="Rename Objects", default=True)
    rename_materials: bpy.props.BoolProperty(name="Rename Materials", default=True)

class OBJECT_OT_batch_rename(bpy.types.Operator):
    bl_idname = "object.batch_rename"
    bl_label = "Batch Rename"
    bl_description = "Batch rename selected objects and all materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.batch_renamer_props

        if props.rename_objects:
            for obj in context.selected_objects:
                old_name = obj.name
                new_name = old_name

                if props.remove_prefix and new_name.startswith(props.remove_prefix):
                    new_name = new_name[len(props.remove_prefix):]
                if props.add_prefix:
                    new_name = props.add_prefix + new_name
                if props.add_suffix:
                    new_name = new_name + props.add_suffix

                if new_name != old_name:
                    obj.name = new_name
                    self.report({'INFO'}, f"Renamed Object: {old_name} → {new_name}")

        if props.rename_materials:
            for mat in bpy.data.materials:
                old_name = mat.name
                new_name = old_name

                if props.remove_prefix and new_name.startswith(props.remove_prefix):
                    new_name = new_name[len(props.remove_prefix):]
                if props.add_prefix:
                    new_name = props.add_prefix + new_name
                if props.add_suffix:
                    new_name = new_name + props.add_suffix

                if new_name != old_name:
                    mat.name = new_name
                    self.report({'INFO'}, f"Renamed Material: {old_name} → {new_name}")

        return {'FINISHED'}

class VIEW3D_PT_batch_rename(bpy.types.Panel):
    bl_label = "Batch Rename"
    bl_category = "BRS Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        props = context.scene.batch_renamer_props

        layout.prop(props, "remove_prefix")
        layout.prop(props, "add_prefix")
        layout.prop(props, "add_suffix")

        layout.separator()
        layout.prop(props, "rename_objects")
        layout.prop(props, "rename_materials")

        layout.separator()
        layout.operator("object.batch_rename", icon='FILE_TICK')

classes = (
    BatchRenamerProperties,
    OBJECT_OT_batch_rename,
    VIEW3D_PT_batch_rename,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        try:
            register_class(cls)
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {e}")
    bpy.types.Scene.batch_renamer_props = bpy.props.PointerProperty(type=BatchRenamerProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        try:
            unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {e}")
    if hasattr(bpy.types.Scene, "batch_renamer_props"):
        del bpy.types.Scene.batch_renamer_props

if __name__ == "__main__":
    unregister()
    register()
  
