import bpy
import webbrowser

class MeshSizeAnalyzer(bpy.types.Panel):
    bl_label = "Mesh Size Analyzer"
    bl_idname = "OBJECT_PT_mesh_size_analyzer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Analysis'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Main functionality for setting the threshold and refreshing the list
        layout.label(text="Mesh Analysis")
        layout.prop(scene, "heavy_obj_threshold", text="Poly Threshold")
        layout.operator("object.find_heavy_objects", text="Refresh List")
        
        # Collapsible list of heavy objects
        box = layout.box()
        box.label(text="Heavy Objects")
        if 'heavy_objects' in scene and scene['heavy_objects']:
            col = box.column(align=True)
            for entry in scene['heavy_objects']:
                obj_name = entry["name"]
                poly_count = entry["poly_count"]
                
                # Determine if this object is currently selected
                obj = bpy.context.scene.objects.get(obj_name)
                text_color = 'ORANGE' if obj and obj.select_get() else 'NONE'
                
                row = col.row(align=True)
                op = row.operator("object.select_heavy_object", text=obj_name, icon='DOT')
                op.obj_name = obj_name
                op.use_custom_color = (text_color == 'ORANGE')  # Flag to color the text
                row.label(text=f"   {poly_count} polys/tris")
        else:
            box.label(text="No heavy objects found")
        
        # "About" Rollout with Company Info
        about_box = layout.box()
        about_box.label(text="About Mesh Size Analyzer:")
        about_box.label(text="This tool helps identify objects with high poly/tris counts.")
        about_box.label(text="It’s designed to optimize scene performance.")
        
        # Company URL
        row = about_box.row()
        row.operator("wm.url_open", text="My Webpage").url = "https://www.homme3d.com"


class OBJECT_OT_FindHeavyObjects(bpy.types.Operator):
    bl_idname = "object.find_heavy_objects"
    bl_label = "Find Heavy Objects"
    
    def execute(self, context):
        threshold = context.scene.heavy_obj_threshold
        heavy_objects = []

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                # Ensure the object's mesh data is up-to-date
                obj_eval = obj.evaluated_get(context.evaluated_depsgraph_get())
                mesh = obj_eval.to_mesh()
                poly_count = len(mesh.polygons)
                
                # Free the evaluated mesh
                obj_eval.to_mesh_clear()

                # Check if it meets the threshold
                if poly_count >= threshold:
                    heavy_objects.append({"name": obj.name, "poly_count": poly_count})

        # Sort by poly count descending
        heavy_objects.sort(key=lambda x: x["poly_count"], reverse=True)
        
        # Store in scene custom property for UI display
        context.scene['heavy_objects'] = heavy_objects
        return {'FINISHED'}


class OBJECT_OT_SelectHeavyObject(bpy.types.Operator):
    bl_idname = "object.select_heavy_object"
    bl_label = "Select Heavy Object"
    obj_name: bpy.props.StringProperty()
    use_custom_color: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=self.obj_name, icon='DOT')
        
    def execute(self, context):
        # Select the object in the scene
        obj = bpy.context.scene.objects.get(self.obj_name)
        if obj:
            # Deselect all other objects
            bpy.ops.object.select_all(action='DESELECT')
            # Select and activate the clicked object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
        return {'FINISHED'}


class WM_OT_OpenURL(bpy.types.Operator):
    """Open a URL in the default web browser"""
    bl_idname = "wm.url_open"
    bl_label = "Open URL"
    url: bpy.props.StringProperty()

    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MeshSizeAnalyzer)
    bpy.utils.register_class(OBJECT_OT_FindHeavyObjects)
    bpy.utils.register_class(OBJECT_OT_SelectHeavyObject)
    bpy.utils.register_class(WM_OT_OpenURL)
    bpy.types.Scene.heavy_obj_threshold = bpy.props.IntProperty(
        name="Poly Threshold - objects with polys/tris greater than:", 
        default=50000, 
        min=0, 
        description="Minimum number of polys/tris to be considered heavy"
    )

def unregister():
    bpy.utils.unregister_class(MeshSizeAnalyzer)
    bpy.utils.unregister_class(OBJECT_OT_FindHeavyObjects)
    bpy.utils.unregister_class(OBJECT_OT_SelectHeavyObject)
    bpy.utils.unregister_class(WM_OT_OpenURL)
    del bpy.types.Scene.heavy_obj_threshold

if __name__ == "__main__":
    register()
