"""
Super Simple PBR Material Library – Blender Addon
=================================================
Creates and assigns glTF-compatible PBR materials to selected objects.
All materials use Principled BSDF, which exports correctly to
Three.js, Unreal Engine and Unity via glTF 2.0 etc.

Installation:
  Edit > Preferences > Add-ons > Install > select this file > enable

Panel:
  3D Viewport > N-panel (press N) > tab "PBR Lib"
"""

bl_info = {
    "name": "Super Simple PBR MatLib",
    "author": "Tassel / LaBaN",
    "version": (1, 4),
    "blender": (3, 0, 0),
    "location": "View3D > N-Panel > PBR Lib",
    "description": "Assign glTF-compatible PBR materials to selected objects",
    "category": "Material",
}

import bpy


# ---------------------------------------------------------------------------
# Material definitions
# All values tuned for correct glTF export via Principled BSDF.
#
# Extra keys:
#   emission_color    - (R, G, B, 1.0)  enables emissive
#   emission_strength - float, default 1.0
# ---------------------------------------------------------------------------
MATERIAL_DEFS = {

    # WATER
    "Freshwater": {
        "category": "Water",
        "base_color": (0.08, 0.38, 0.72, 1.0),
        "metallic": 0.0, "roughness": 0.02,
        "transmission": 0.97, "ior": 1.333, "alpha": 0.25,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Seawater": {
        "category": "Water",
        "base_color": (0.03, 0.18, 0.32, 1.0),
        "metallic": 0.0, "roughness": 0.10,
        "transmission": 0.80, "ior": 1.338, "alpha": 0.50,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Pool_Water": {
        "category": "Water",
        "base_color": (0.08, 0.70, 0.82, 1.0),
        "metallic": 0.0, "roughness": 0.01,
        "transmission": 0.93, "ior": 1.333, "alpha": 0.35,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },

    # METAL
    "Chrome": {
        "category": "Metal",
        "base_color": (0.92, 0.92, 0.96, 1.0),
        "metallic": 1.0, "roughness": 0.04,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Aluminum": {
        "category": "Metal",
        "base_color": (0.74, 0.76, 0.78, 1.0),
        "metallic": 1.0, "roughness": 0.28,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Diamondplate": {
        "category": "Metal",
        "base_color": (0.55, 0.58, 0.62, 1.0),
        "metallic": 1.0, "roughness": 0.42,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Steel_Polished": {
        "category": "Metal",
        "base_color": (0.80, 0.80, 0.82, 1.0),
        "metallic": 1.0, "roughness": 0.08,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Steel_Matte": {
        "category": "Metal",
        "base_color": (0.62, 0.63, 0.65, 1.0),
        "metallic": 1.0, "roughness": 0.45,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Rust": {
        "category": "Metal",
        "base_color": (0.48, 0.18, 0.06, 1.0),
        "metallic": 0.4, "roughness": 0.85,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Gold": {
        "category": "Metal",
        "base_color": (1.00, 0.77, 0.18, 1.0),
        "metallic": 1.0, "roughness": 0.10,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Copper": {
        "category": "Metal",
        "base_color": (0.95, 0.48, 0.24, 1.0),
        "metallic": 1.0, "roughness": 0.15,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Brass": {
        "category": "Metal",
        "base_color": (0.88, 0.70, 0.25, 1.0),
        "metallic": 1.0, "roughness": 0.22,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Titanium": {
        "category": "Metal",
        "base_color": (0.55, 0.55, 0.58, 1.0),
        "metallic": 1.0, "roughness": 0.18,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },
    "Iron": {
        "category": "Metal",
        "base_color": (0.30, 0.30, 0.32, 1.0),
        "metallic": 1.0, "roughness": 0.60,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
    },

    # GLASS
    "Glass_Clear": {
        "category": "Glass",
        "base_color": (0.95, 0.97, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.0,
        "transmission": 1.0, "ior": 1.52, "alpha": 0.05,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Frosted": {
        "category": "Glass",
        "base_color": (0.90, 0.92, 0.95, 1.0),
        "metallic": 0.0, "roughness": 0.35,
        "transmission": 0.92, "ior": 1.52, "alpha": 0.30,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Thick": {
        "category": "Glass",
        "base_color": (0.75, 0.90, 0.82, 1.0),
        "metallic": 0.0, "roughness": 0.02,
        "transmission": 0.95, "ior": 1.55, "alpha": 0.40,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Mirror": {
        "category": "Glass",
        "base_color": (0.88, 0.90, 0.92, 1.0),
        "metallic": 0.85, "roughness": 0.02,
        "transmission": 0.15, "ior": 1.52, "alpha": 0.85,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Blue": {
        "category": "Glass",
        "base_color": (0.10, 0.35, 0.85, 1.0),
        "metallic": 0.0, "roughness": 0.04,
        "transmission": 0.90, "ior": 1.52, "alpha": 0.25,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Green": {
        "category": "Glass",
        "base_color": (0.10, 0.70, 0.30, 1.0),
        "metallic": 0.0, "roughness": 0.04,
        "transmission": 0.90, "ior": 1.52, "alpha": 0.25,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Red": {
        "category": "Glass",
        "base_color": (0.85, 0.08, 0.06, 1.0),
        "metallic": 0.0, "roughness": 0.04,
        "transmission": 0.88, "ior": 1.52, "alpha": 0.28,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Amber": {
        "category": "Glass",
        "base_color": (0.92, 0.55, 0.05, 1.0),
        "metallic": 0.0, "roughness": 0.03,
        "transmission": 0.88, "ior": 1.52, "alpha": 0.30,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_Smoke": {
        "category": "Glass",
        "base_color": (0.12, 0.12, 0.14, 1.0),
        "metallic": 0.0, "roughness": 0.05,
        "transmission": 0.75, "ior": 1.52, "alpha": 0.45,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },
    "Glass_IceBlue": {
        "category": "Glass",
        "base_color": (0.72, 0.90, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.18,
        "transmission": 0.92, "ior": 1.309, "alpha": 0.20,
        "blend_mode": "BLEND", "shadow_mode": "NONE",
    },

    # EMISSIVE - WARM TONES
    "Emit_Warm_White": {
        "category": "Emissive",
        "base_color": (1.00, 0.96, 0.88, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (1.00, 0.96, 0.88, 1.0),
        "emission_strength": 3.0,
    },
    "Emit_Yellow": {
        "category": "Emissive",
        "base_color": (1.00, 0.85, 0.10, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (1.00, 0.85, 0.10, 1.0),
        "emission_strength": 4.0,
    },
    "Emit_Orange": {
        "category": "Emissive",
        "base_color": (1.00, 0.42, 0.02, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (1.00, 0.42, 0.02, 1.0),
        "emission_strength": 4.0,
    },
    "Emit_Red": {
        "category": "Emissive",
        "base_color": (1.00, 0.06, 0.04, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (1.00, 0.06, 0.04, 1.0),
        "emission_strength": 4.0,
    },

    # EMISSIVE - COOL TONES
    "Emit_Cool_White": {
        "category": "Emissive",
        "base_color": (0.88, 0.95, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.88, 0.95, 1.00, 1.0),
        "emission_strength": 3.0,
    },
    "Emit_Cyan": {
        "category": "Emissive",
        "base_color": (0.02, 0.88, 0.92, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.02, 0.88, 0.92, 1.0),
        "emission_strength": 5.0,
    },
    "Emit_Ice_Blue": {
        "category": "Emissive",
        "base_color": (0.30, 0.65, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.30, 0.65, 1.00, 1.0),
        "emission_strength": 4.0,
    },
    "Emit_Green": {
        "category": "Emissive",
        "base_color": (0.05, 0.92, 0.28, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.05, 0.92, 0.28, 1.0),
        "emission_strength": 4.5,
    },

    # EMISSIVE - NEON
    "Neon_Blue": {
        "category": "Emissive",
        "base_color": (0.05, 0.30, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.05, 0.30, 1.00, 1.0),
        "emission_strength": 10.0,
    },
    "Neon_Purple": {
        "category": "Emissive",
        "base_color": (0.62, 0.05, 1.00, 1.0),
        "metallic": 0.0, "roughness": 0.5,
        "transmission": 0.0, "ior": 1.5, "alpha": 1.0,
        "blend_mode": "OPAQUE", "shadow_mode": "OPAQUE",
        "emission_color": (0.62, 0.05, 1.00, 1.0),
        "emission_strength": 10.0,
    },

    # PAINT
    "Paint_White":       {"category":"Paint","base_color":(0.95,0.95,0.95,1.0),"metallic":0.0,"roughness":0.30,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_LightGray":   {"category":"Paint","base_color":(0.70,0.70,0.70,1.0),"metallic":0.0,"roughness":0.35,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_DarkGray":    {"category":"Paint","base_color":(0.28,0.28,0.28,1.0),"metallic":0.0,"roughness":0.40,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Black":       {"category":"Paint","base_color":(0.02,0.02,0.02,1.0),"metallic":0.0,"roughness":0.40,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Red":         {"category":"Paint","base_color":(0.80,0.05,0.05,1.0),"metallic":0.0,"roughness":0.32,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Orange":      {"category":"Paint","base_color":(0.90,0.38,0.02,1.0),"metallic":0.0,"roughness":0.32,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Yellow":      {"category":"Paint","base_color":(0.95,0.80,0.02,1.0),"metallic":0.0,"roughness":0.30,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Green":       {"category":"Paint","base_color":(0.05,0.55,0.12,1.0),"metallic":0.0,"roughness":0.30,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Blue":        {"category":"Paint","base_color":(0.05,0.22,0.78,1.0),"metallic":0.0,"roughness":0.30,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_LightBlue":   {"category":"Paint","base_color":(0.30,0.65,0.95,1.0),"metallic":0.0,"roughness":0.28,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Brown":       {"category":"Paint","base_color":(0.38,0.18,0.06,1.0),"metallic":0.0,"roughness":0.45,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
    "Paint_Purple":      {"category":"Paint","base_color":(0.45,0.08,0.70,1.0),"metallic":0.0,"roughness":0.30,"transmission":0.0,"ior":1.5,"alpha":1.0,"blend_mode":"OPAQUE","shadow_mode":"OPAQUE"},
}


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _try_set(inputs, name, value):
    """Sets input value if it exists - Blender version-safe."""
    if name in inputs:
        inputs[name].default_value = value


def build_material(name, defs):
    """
    Gets existing material or creates new one.
    Sets up Principled BSDF correctly for glTF 2.0 export.
    """
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True

    # Blender 3.x vs 4.x transparency API
    blend = defs.get("blend_mode", "OPAQUE")
    if hasattr(mat, "blend_method"):
        mat.blend_method = blend
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "BLENDED" if blend == "BLEND" else "DITHERED"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = defs.get("shadow_mode", "OPAQUE")

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Principled BSDF
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    _try_set(bsdf.inputs, "Base Color", defs["base_color"])
    _try_set(bsdf.inputs, "Metallic",   defs["metallic"])
    _try_set(bsdf.inputs, "Roughness",  defs["roughness"])
    _try_set(bsdf.inputs, "IOR",        defs["ior"])
    _try_set(bsdf.inputs, "Alpha",      defs["alpha"])

    if defs["transmission"] > 0:
        # Blender 4.x = "Transmission Weight", Blender 3.x = "Transmission"
        _try_set(bsdf.inputs, "Transmission Weight", defs["transmission"])
        _try_set(bsdf.inputs, "Transmission",         defs["transmission"])

    # Emission
    ec = defs.get("emission_color")
    es = defs.get("emission_strength", 1.0)
    if ec:
        _try_set(bsdf.inputs, "Emission Color",    ec)   # Blender 4.x
        _try_set(bsdf.inputs, "Emission",          ec)   # Blender 3.x
        _try_set(bsdf.inputs, "Emission Strength", es)

    # Material Output
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (320, 0)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    return mat


def assign_material_to_selected(material_name):
    defs = MATERIAL_DEFS[material_name]
    mat  = build_material(material_name, defs)

    targets = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    if not targets:
        return False, "No mesh objects selected!"

    for obj in targets:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    return True, f"'{material_name}' assigned to {len(targets)} object(s)"


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class PBRL_OT_AssignMaterial(bpy.types.Operator):
    bl_idname      = "pbrl.assign_material"
    bl_label       = "Assign PBR Material"
    bl_description = "Create and assign a PBR material to selected objects"
    bl_options     = {"REGISTER", "UNDO"}

    material_name: bpy.props.StringProperty()

    def execute(self, context):
        ok, msg = assign_material_to_selected(self.material_name)
        self.report({"INFO"} if ok else {"WARNING"}, msg)
        return {"FINISHED"} if ok else {"CANCELLED"}


class PBRL_OT_ClearMaterials(bpy.types.Operator):
    bl_idname      = "pbrl.clear_materials"
    bl_label       = "Clear Materials"
    bl_description = "Remove all materials from selected objects"
    bl_options     = {"REGISTER", "UNDO"}

    def execute(self, context):
        targets = [o for o in context.selected_objects if o.type == "MESH"]
        for obj in targets:
            obj.data.materials.clear()
        self.report({"INFO"}, f"Cleared materials from {len(targets)} object(s)")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

class PBRL_PT_MainPanel(bpy.types.Panel):
    bl_label       = "Super Simple PBR Material Library"
    bl_idname      = "PBRL_PT_main"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "PBR Lib"

    def _btn(self, parent, mat_name, label):
        op = parent.operator("pbrl.assign_material", text=label)
        op.material_name = mat_name

    def _section(self, layout, title, icon):
        layout.separator(factor=0.5)
        box = layout.box()
        box.label(text=title, icon=icon)
        return box

    def draw(self, context):
        layout = self.layout

        # Status
        box = layout.box()
        sel = [o for o in context.selected_objects if o.type == "MESH"]
        if sel:
            box.label(text=f"Selected: {len(sel)} mesh object(s)", icon="CHECKMARK")
        else:
            box.label(text="Select one or more objects", icon="ERROR")

        # WATER
        box = self._section(layout, "Water", "MATFLUID")
        row = box.row(align=True)
        self._btn(row, "Freshwater", "Freshwater")
        self._btn(row, "Seawater",   "Seawater")
        self._btn(row, "Pool_Water", "Pool Water")

        # METAL
        box = self._section(layout, "Metal", "MATSPHERE")
        row = box.row(align=True)
        self._btn(row, "Chrome",         "Chrome")
        self._btn(row, "Steel_Polished", "Steel Polished")
        self._btn(row, "Steel_Matte",    "Steel Matte")
        row = box.row(align=True)
        self._btn(row, "Aluminum",  "Aluminum")
        self._btn(row, "Titanium",  "Titanium")
        self._btn(row, "Iron",      "Iron")
        row = box.row(align=True)
        self._btn(row, "Gold",   "Gold")
        self._btn(row, "Copper", "Copper")
        self._btn(row, "Brass",  "Brass")
        row = box.row(align=True)
        self._btn(row, "Diamondplate", "Diamondplate")
        self._btn(row, "Rust",         "Rust")

        # GLASS
        box = self._section(layout, "Glass", "SHADING_RENDERED")
        row = box.row(align=True)
        self._btn(row, "Glass_Clear",   "Clear")
        self._btn(row, "Glass_Frosted", "Frosted")
        self._btn(row, "Glass_Thick",   "Thick")
        self._btn(row, "Glass_Mirror",  "Mirror")
        row = box.row(align=True)
        self._btn(row, "Glass_Blue",  "Blue")
        self._btn(row, "Glass_Green", "Green")
        self._btn(row, "Glass_Red",   "Red")
        self._btn(row, "Glass_Amber", "Amber")
        row = box.row(align=True)
        self._btn(row, "Glass_Smoke",   "Smoke")
        self._btn(row, "Glass_IceBlue", "Ice Blue")

        # EMISSIVE
        box = self._section(layout, "Emissive + Neon", "LIGHT_SUN")

        box.label(text="Warm tones:")
        row = box.row(align=True)
        self._btn(row, "Emit_Warm_White", "Warm White")
        self._btn(row, "Emit_Yellow",     "Yellow")
        self._btn(row, "Emit_Orange",     "Orange")
        self._btn(row, "Emit_Red",        "Red")

        box.label(text="Cool tones:")
        row = box.row(align=True)
        self._btn(row, "Emit_Cool_White", "Cool White")
        self._btn(row, "Emit_Cyan",       "Cyan")
        self._btn(row, "Emit_Ice_Blue",   "Ice Blue")
        self._btn(row, "Emit_Green",      "Green")

        box.label(text="Neon:")
        row = box.row(align=True)
        self._btn(row, "Neon_Blue",   "Neon Blue")
        self._btn(row, "Neon_Purple", "Neon Purple")

        # PAINT
        box = self._section(layout, "Paint", "MATPLANE")
        row = box.row(align=True)
        self._btn(row, "Paint_White",     "White")
        self._btn(row, "Paint_LightGray", "Light Gray")
        self._btn(row, "Paint_DarkGray",  "Dark Gray")
        self._btn(row, "Paint_Black",     "Black")
        row = box.row(align=True)
        self._btn(row, "Paint_Red",    "Red")
        self._btn(row, "Paint_Orange", "Orange")
        self._btn(row, "Paint_Yellow", "Yellow")
        self._btn(row, "Paint_Brown",  "Brown")
        row = box.row(align=True)
        self._btn(row, "Paint_Green",     "Green")
        self._btn(row, "Paint_Blue",      "Blue")
        self._btn(row, "Paint_LightBlue", "Light Blue")
        self._btn(row, "Paint_Purple",    "Purple")

        # TOOLS + EXPORT
        layout.separator()
        box = layout.box()
        box.label(text="Tools", icon="TOOL_SETTINGS")
        box.operator("pbrl.clear_materials", icon="X")

        layout.separator(factor=0.5)
        box = layout.box()
        box.label(text="Export to Three.js / glTF:", icon="EXPORT")
        col = box.column(align=True)
        col.label(text="File > Export > glTF 2.0 (.glb)")
        col.label(text="Materials + Normals + UVs")

        # ABOUT - collapsible rollout at the bottom
        layout.separator(factor=0.5)
        box = layout.box()
        row = box.row()
        row.prop(
            context.scene, "pbrl_about_expanded",
            icon="TRIA_DOWN" if context.scene.pbrl_about_expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False,
        )
        row.label(text="About", icon="INFO")

        if context.scene.pbrl_about_expanded:
            col = box.column(align=True)
            col.scale_y = 0.85
            col.label(text="Super Simple PBR MatLib 1.4")
            col.separator(factor=0.8)
            col.label(text="Super simple one-click PBR material")
            col.label(text="assignment tool for Blender. Built to")
            col.label(text="speed up asset preparation for real-")
            col.label(text="time engines and web 3D pipelines.")
            col.separator(factor=1.5)
            col.label(text="───────────────────")
            col.label(text="All materials use Principled BSDF and")
            col.label(text="export correctly via glTF 2.0 to:")
            col.separator(factor=0.8)
            col.label(text="Three.js, Babylon.js, Unity, Godot,")
            col.label(text="Unreal Engine, PlayCanvas, R3F Etc.")
            col.separator(factor=1.5)
            col.label(text="───────────────────")
            col.label(text="Material categories:")
            col.separator(factor=0.8)
            col.label(text="Water, Metal, Glass,")
            col.label(text="Emissive, Neon, Paint")
            col.separator(factor=1.5)
            col.label(text="───────────────────")
            col.label(text="Select mesh objects, click a material")
            col.label(text="button to assign. That's it.")


# ---------------------------------------------------------------------------
# Scene property for the About rollout toggle
# ---------------------------------------------------------------------------

def register_props():
    bpy.types.Scene.pbrl_about_expanded = bpy.props.BoolProperty(
        name="Show About",
        default=False,
    )


def unregister_props():
    del bpy.types.Scene.pbrl_about_expanded


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

CLASSES = [
    PBRL_OT_AssignMaterial,
    PBRL_OT_ClearMaterials,
    PBRL_PT_MainPanel,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    register_props()


def unregister():
    unregister_props()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
