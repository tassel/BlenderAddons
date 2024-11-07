import bpy
import webbrowser

# Define the color buttons for materials with RGBA (alpha is set to 1.0)
COLOR_MATERIALS = {
    "Yellow_1": (1, 0.964, 0, 1),           # Yellow
    "Yellow_2": (0.866, 0.639, 0, 1),       # Yellow2
    "Green_1": (0, 1, 0, 1),                # Green
    "Green_": (0, 0.306, 0.067, 1),         # Dark Green
    "Grey_1": (0.235, 0.235, 0.235, 1),     # Grey
    "Grey_2": (0.604, 0.604, 0.604, 1),     # Light Grey
    "Red": (1, 0, 0, 1),                    # Red
    "Blue": (0, 0, 1, 1),                   # Blue
    "Orange": (0.811, 0.365, 0, 1),         # Orange
    "White": (1, 1, 1, 1),                  # White
    "Black": (0, 0, 0, 1),                  # Black
    "Purple": (0.333, 0.063, 0.200, 1),     # Purple
    "Physx": (0.031, 0.239, 0.541, 1),      # Physx Blue
}

# Panel class
class MaterialColorPanel(bpy.types.Panel):
    bl_label = "Material ColorBar"
    bl_idname = "VIEW3D_PT_ColorBar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Color'

    def draw(self, context):
        layout = self.layout

        # Create a row for the color buttons
        row = layout.row()

        row.label(text="       Assign Material Color To Object:")

        # Create a button for each color in COLOR_MATERIALS
        for color_name, color_rgb in COLOR_MATERIALS.items():
            row = layout.row(align=True)
            row.template_node_socket(color=color_rgb)
            operator = row.operator("object.set_material_color", text=f"[ {color_name.replace('_', ' ')} ]")
            operator.color = color_rgb  # Pass color to the operator
            operator.material_name = f"ColorSelector_{color_name}"

        layout.operator("object.select_by_material_color", text="Select by Color")

        # About dialog window at the bottom
        row = layout.row(align=True)
        row.operator("object.about_material_color_tool", text="About", icon='INFO')


# Operator for the "About" dialog popup
class AboutMaterialColorToolOperator(bpy.types.Operator):
    bl_idname = "object.about_material_color_tool"
    bl_label = "About Material ColorBar"
    bl_options = {'REGISTER', 'INTERNAL'}

    def invoke(self, context, event):
        # This method shows the dialog using invoke_props_dialog
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.label(text="About Material Color Tool:")
        layout.label(text="This tool helps to quickly assign predefined")
        layout.label(text="materials with specific colors to objects.")
        layout.label(text="It's designed to streamline scene setup.")
        
        row = layout.row()
        row.operator("wm.url_open", text="Open homme3d.com").url = "https://www.homme3d.com"

    def execute(self, context):
        return {'FINISHED'}


# Operator to set material color
class SetMaterialColorOperator(bpy.types.Operator):
    bl_idname = "object.set_material_color"
    bl_label = "Set Material Color"
    
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=4,  # RGBA color (we include Alpha as well)
        min=0.0,
        max=1.0,
        default=(1, 1, 1, 1),  # Default to white (RGBA)
    )
    material_name: bpy.props.StringProperty()  # Name of the material

    def execute(self, context):
        # Check if the material already exists, else create it
        material = bpy.data.materials.get(self.material_name)
        if material is None:
            material = bpy.data.materials.new(name=self.material_name)
            material.use_nodes = True
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = self.color  # Set the color

        # Apply the material to all selected objects
        for obj in context.selected_objects:
            if obj.type == 'MESH':  # Only apply material to mesh objects
                obj.data.materials.clear()
                obj.data.materials.append(material)
        
        return {'FINISHED'}


# Operator to select objects by material color
class SelectByMaterialColorOperator(bpy.types.Operator):
    bl_idname = "object.select_by_material_color"
    bl_label = "Select by Material Color"

    def execute(self, context):
        # Get the color of the active object’s material
        if context.selected_objects:
            active_obj = context.view_layer.objects.active
            if active_obj and active_obj.type == 'MESH' and active_obj.data.materials:
                active_material = active_obj.data.materials[0]
                color = active_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value[:3]  # Extract RGB

                # Select all objects with the same material color
                for obj in context.scene.objects:
                    if obj.type == 'MESH' and obj != active_obj:
                        if obj.data.materials and obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value[:3] == color:
                            obj.select_set(True)
                        else:
                            obj.select_set(False)

        return {'FINISHED'}


# Operator to open URL in browser
class WM_OT_OpenURL(bpy.types.Operator):
    """Open homme3d.com in the default web browser"""
    bl_idname = "wm.url_open"
    bl_label = "Open URL"
    url: bpy.props.StringProperty()

    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}


# Register the classes
def register():
    bpy.utils.register_class(MaterialColorPanel)
    bpy.utils.register_class(SetMaterialColorOperator)
    bpy.utils.register_class(SelectByMaterialColorOperator)
    bpy.utils.register_class(AboutMaterialColorToolOperator)
    bpy.utils.register_class(WM_OT_OpenURL)

def unregister():
    bpy.utils.unregister_class(MaterialColorPanel)
    bpy.utils.unregister_class(SetMaterialColorOperator)
    bpy.utils.unregister_class(SelectByMaterialColorOperator)
    bpy.utils.unregister_class(AboutMaterialColorToolOperator)
    bpy.utils.unregister_class(WM_OT_OpenURL)

if __name__ == "__main__":
    register()
