import bpy
import os
import math

class VesselMotionProperties(bpy.types.PropertyGroup):
    """Stores user-defined vessel motion settings"""
    frame_count: bpy.props.IntProperty(name="Frame Count", default=400, min=1, max=5000)
    motion_speed: bpy.props.FloatProperty(name="Motion Speed", default=1.0, min=0.5, max=5.0)
    surge: bpy.props.FloatProperty(name="Surge", default=0.2, min=0.0, max=5.0)
    sway: bpy.props.FloatProperty(name="Sway", default=0.15, min=0.0, max=5.0)
    heave: bpy.props.FloatProperty(name="Heave", default=0.1, min=0.0, max=5.0)
    roll: bpy.props.FloatProperty(name="Roll", default=5.0, min=0.0, max=30.0)
    pitch: bpy.props.FloatProperty(name="Pitch", default=3.0, min=0.0, max=30.0)
    yaw: bpy.props.FloatProperty(name="Yaw", default=2.0, min=0.0, max=30.0)
    
    keyframe_step: bpy.props.IntProperty(name="Keyframe Step", default=1, min=1, max=50, description="Set the step interval between keyframes")
    
    preset: bpy.props.EnumProperty(
        name="Preset",
        description="Select a motion preset",
        items=[
            ('default', "Default", "Default Settings"),
            ('calm', "Calm Sea", "Minimal motion"),
            ('medium', "Medium Sea", "Moderate motion"),
            ('heavy', "Heavy Sea", "Strong motion")
        ],
        default='default',
        update=lambda self, context: self.update_preset()
    )

    def update_preset(self):
        presets = {
            'default': {'surge': 0.2, 'sway': 0.15, 'heave': 0.1, 'roll': 5.0, 'pitch': 3.0, 'yaw': 2.0},
            'calm': {'surge': 0.05, 'sway': 0.05, 'heave': 0.05, 'roll': 1.0, 'pitch': 1.0, 'yaw': 1.0},
            'medium': {'surge': 0.3, 'sway': 0.25, 'heave': 0.2, 'roll': 10.0, 'pitch': 8.0, 'yaw': 5.0},
            'heavy': {'surge': 0.5, 'sway': 0.4, 'heave': 0.35, 'roll': 20.0, 'pitch': 15.0, 'yaw': 10.0},
        }
        preset_values = presets.get(self.preset, presets['default'])
        for attr, value in preset_values.items():
            setattr(self, attr, value)

class GenerateAndApplyMotionOperator(bpy.types.Operator):
    """Generate and Apply Vessel Motion to Selected Object"""
    bl_idname = "wm.generate_apply_motion"
    bl_label = "Generate & Apply Motion"
    
    def execute(self, context):
        obj = bpy.context.active_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        props = context.scene.vessel_motion_props
        frame_count = props.frame_count
        speed = props.motion_speed
        surge = props.surge
        sway = props.sway
        heave = props.heave
        roll = props.roll
        pitch = props.pitch
        yaw = props.yaw
        keyframe_step = props.keyframe_step
        
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = frame_count
        
        for i in range(0, frame_count, keyframe_step):
            radians = (i / 100) * (math.pi * 2) * speed
            
            obj.location = (
                surge * 10.0 * (math.sin(radians)),
                sway * 10.0 * (math.sin(radians * 0.8)),
                heave * 10.0 * (math.sin(radians * 1.2))
            )
            obj.keyframe_insert(data_path="location", frame=i+1)
            
            obj.rotation_euler = (
                roll * 0.0174533 * (math.sin(radians)),
                pitch * 0.0174533 * (math.sin(radians * 0.8)),
                yaw * 0.0174533 * (math.sin(radians * 0.5))
            )
            obj.keyframe_insert(data_path="rotation_euler", frame=i+1)
        
        return {'FINISHED'}

class VesselMotionPanel(bpy.types.Panel):
    """Creates a Panel in the N-panel"""
    bl_label = "Vessel Motion Generator"
    bl_idname = "PT_VesselMotionGenerator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vessel Motion'

    def draw(self, context):
        layout = self.layout
        props = context.scene.vessel_motion_props
        
        layout.prop(props, "frame_count")
        layout.prop(props, "motion_speed")
        layout.prop(props, "preset")
        layout.separator()
        layout.prop(props, "surge")
        layout.prop(props, "sway")
        layout.prop(props, "heave")
        layout.prop(props, "roll")
        layout.prop(props, "pitch")
        layout.prop(props, "yaw")
        layout.separator()
        layout.prop(props, "keyframe_step")
        layout.operator("wm.generate_apply_motion", text="Generate & Apply Motion")

class AboutPanel(bpy.types.Panel):
    """Creates an About Panel in the N-panel"""
    bl_label = "About Vessel Motion Generator v1.1"
    bl_idname = "PT_AboutVesselMotionImporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vessel Motion'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Created by: Raymond / Broomstick")
        layout.label(text="Usage:")
        layout.label(text="1. Set parameters")
        layout.label(text="2. Select Object")
        layout.label(text="3. Press Generate/Apply button")
        layout.operator("wm.url_open", text="More Info").url = "https://broomstick.no"

# Registering classes
def register():
    bpy.utils.register_class(VesselMotionProperties)
    bpy.utils.register_class(GenerateAndApplyMotionOperator)
    bpy.utils.register_class(VesselMotionPanel)
    bpy.utils.register_class(AboutPanel)
    bpy.types.Scene.vessel_motion_props = bpy.props.PointerProperty(type=VesselMotionProperties)

def unregister():
    bpy.utils.unregister_class(VesselMotionProperties)
    bpy.utils.unregister_class(GenerateAndApplyMotionOperator)
    bpy.utils.unregister_class(VesselMotionPanel)
    bpy.utils.unregister_class(AboutPanel)
    del bpy.types.Scene.vessel_motion_props

if __name__ == "__main__":
    register()
