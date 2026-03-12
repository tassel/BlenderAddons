import bpy

bl_info = {
    "name": "Animation Tools",
    "blender": (2, 80, 0),
    "category": "Animation",
}

class BRS_OT_GoToFrame(bpy.types.Operator):
    """Go to a specific frame"""
    bl_idname = "brs_anim.goto_frame"
    bl_label = "Go To Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    frame: bpy.props.IntProperty(default=1)
    
    def execute(self, context):
        context.scene.frame_set(self.frame)
        return {'FINISHED'}

class BRS_OT_ChangeFrame(bpy.types.Operator):
    """Change Frame"""
    bl_idname = "brs_anim.change_frame"
    bl_label = "Change Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    step: bpy.props.IntProperty()
    
    def execute(self, context):
        context.scene.frame_set(context.scene.frame_current + self.step)
        return {'FINISHED'}

class BRS_OT_KeyframeSet(bpy.types.Operator):
    """Set Keyframe"""
    bl_idname = "brs_anim.keyframe_set"
    bl_label = "Set Keyframe"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        items=[
            ('LOC', "Position", "Keyframe Location"),
            ('ROT', "Rotation", "Keyframe Rotation"),
            ('SCALE', "Scale", "Keyframe Scale"),
            ('PRS', "PRS", "Keyframe Position, Rotation, and Scale")
        ]
    )
    
    def execute(self, context):
        for obj in context.selected_objects:
            if self.mode == 'LOC' or self.mode == 'PRS':
                obj.keyframe_insert(data_path="location")
            if self.mode == 'ROT' or self.mode == 'PRS':
                obj.keyframe_insert(data_path="rotation_euler")
            if self.mode == 'SCALE' or self.mode == 'PRS':
                obj.keyframe_insert(data_path="scale")
        return {'FINISHED'}

class BRS_OT_DeleteKeyframes(bpy.types.Operator):
    """Delete Keyframes and Refresh Timeline"""
    bl_idname = "brs_anim.delete_keyframes"
    bl_label = "Delete Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        items=[
            ('LOC', "Position", "Delete Location Keyframes"),
            ('ROT', "Rotation", "Delete Rotation Keyframes"),
            ('SCALE', "Scale", "Delete Scale Keyframes"),
            ('PRS', "PRS", "Delete Position, Rotation, and Scale Keyframes")
        ]
    )
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                if self.mode in ['LOC', 'PRS']:
                    obj.keyframe_delete(data_path="location")
                if self.mode in ['ROT', 'PRS']:
                    obj.keyframe_delete(data_path="rotation_euler")
                if self.mode in ['SCALE', 'PRS']:
                    obj.keyframe_delete(data_path="scale")
        
        # Refresh animation timeline
        context.view_layer.update()
        return {'FINISHED'}

class BRS_OT_PlayStop(bpy.types.Operator):
    """Toggle Play/Stop Animation"""
    bl_idname = "brs_anim.play_stop"
    bl_label = "Play/Stop Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel()
        else:
            bpy.ops.screen.animation_play()
        return {'FINISHED'}

class BRS_PT_AnimationPanel(bpy.types.Panel):
    """Creates a Panel in the UI"""
    bl_label = "Brs's Animation Tools"
    bl_idname = "BRS_PT_AnimationPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("brs_anim.goto_frame", text="Go To Start").frame = 1
        row.operator("brs_anim.play_stop", text="Play/Stop")
        row.operator("brs_anim.goto_frame", text="Go To End").frame = context.scene.frame_end
        
        row = layout.row()
        row.operator("brs_anim.change_frame", text="< Prev").step = -1
        row.operator("brs_anim.change_frame", text="Next >").step = 1
    
        layout.label(text="Jump n't Keys Forward & Backwards:")
        row = layout.row()
        for step in [5, 25, 50, 75, 100]:
            row.operator("brs_anim.change_frame", text=f"+{step}").step = step
            
        row = layout.row()
        for step in [5, 25, 50, 75, 100]:
            row.operator("brs_anim.change_frame", text=f"-{step}").step = -step
        
        layout.label(text="Set Keys:")
        row = layout.row()
        row.operator("brs_anim.keyframe_set", text="POS", icon='KEY_HLT').mode = 'LOC'
        row.operator("brs_anim.keyframe_set", text="ROT", icon='ORIENTATION_GIMBAL').mode = 'ROT'
        row.operator("brs_anim.keyframe_set", text="SCALE", icon='FULLSCREEN_ENTER').mode = 'SCALE'
        row.operator("brs_anim.keyframe_set", text="PRS", icon='MODIFIER').mode = 'PRS'
        
        layout.label(text="Delete Keys:")
        row = layout.row()
        row.operator("brs_anim.delete_keyframes", text="POS", icon='KEY_HLT').mode = 'LOC'
        row.operator("brs_anim.delete_keyframes", text="ROT", icon='ORIENTATION_GIMBAL').mode = 'ROT'
        row.operator("brs_anim.delete_keyframes", text="SCALE", icon='FULLSCREEN_ENTER').mode = 'SCALE'
        row.operator("brs_anim.delete_keyframes", text="ALL", icon='MODIFIER').mode = 'PRS'    

classes = [
    BRS_OT_GoToFrame,
    BRS_OT_ChangeFrame,
    BRS_OT_KeyframeSet,
    BRS_OT_DeleteKeyframes,
    BRS_OT_PlayStop,
    BRS_PT_AnimationPanel
]

def register():
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(cls)
            except RuntimeError:
                pass
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(cls)
            except RuntimeError:
                pass

if __name__ == "__main__":
    unregister()
    register()
  
