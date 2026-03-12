bl_info = {
    "name": "Batch FBX Folder to Blender Collections",
    "author": "Tassel",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import, 3D View > Sidebar (N) > Batch FBX",
    "description": "Import all FBX files from a folder into per-file Collections named after the FBX filename.",
    "category": "Import-Export",
}

import bpy
import os
from bpy.types import Operator, Panel
from bpy.props import StringProperty, BoolProperty


def import_fbx_to_collections(folder_path: str, recursive: bool = False, unlink_from_other_collections: bool = True):
    if not folder_path or not os.path.isdir(folder_path):
        raise ValueError("Ugyldig mappebane")

    # Samle fbx-filer
    fbx_files = []
    if recursive:
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f.lower().endswith(".fbx"):
                    fbx_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(folder_path):
            if f.lower().endswith(".fbx"):
                fbx_files.append(os.path.join(folder_path, f))

    fbx_files.sort()
    if not fbx_files:
        print("Ingen .fbx-filer funnet i:", folder_path)
        return 0, 0

    scene_root = bpy.context.scene.collection

    total_objs = 0
    for fbx_path in fbx_files:
        base_name = os.path.splitext(os.path.basename(fbx_path))[0]

        # Lag/hent collection
        coll = bpy.data.collections.get(base_name)
        if coll is None:
            coll = bpy.data.collections.new(base_name)
            scene_root.children.link(coll)
        else:
            # Sørg for at den er linket til scenen (i tilfelle den finnes men ikke er i scene tree)
            if coll.name not in [c.name for c in scene_root.children]:
                scene_root.children.link(coll)

        before = set(bpy.data.objects)

        # Importer
        bpy.ops.import_scene.fbx(filepath=fbx_path)

        after = set(bpy.data.objects)
        new_objs = list(after - before)

        # Link nye objekter til riktig collection
        for obj in new_objs:
            if obj.name not in coll.objects:
                coll.objects.link(obj)

            if unlink_from_other_collections:
                for c in list(obj.users_collection):
                    if c != coll:
                        try:
                            c.objects.unlink(obj)
                        except RuntimeError:
                            pass

        total_objs += len(new_objs)
        print(f"Imported '{fbx_path}' -> Collection '{base_name}' ({len(new_objs)} objects)")

    return len(fbx_files), total_objs


class BATCHFBX_OT_folder_to_collections(Operator):
    bl_idname = "batchfbx.folder_to_collections"
    bl_label = "Batch FBX Folder to Blender Collections"
    bl_options = {"REGISTER", "UNDO"}

    directory: StringProperty(
        name="Folder",
        description="Velg mappe med FBX-filer",
        subtype="DIR_PATH",
    )
    recursive: BoolProperty(
        name="Recursive (inkl. undermapper)",
        default=False,
    )
    unlink_from_other_collections: BoolProperty(
        name="Unlink fra andre Collections",
        description="Flytt objekter inn i target-collection (fjern link fra andre collections)",
        default=True,
    )

    def execute(self, context):
        folder = self.directory
        try:
            num_files, num_objs = import_fbx_to_collections(
                folder_path=folder,
                recursive=self.recursive,
                unlink_from_other_collections=self.unlink_from_other_collections,
            )
        except Exception as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}

        self.report({"INFO"}, f"Imported {num_files} FBX files, {num_objs} objects.")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class BATCHFBX_PT_panel(Panel):
    bl_label = "Batch FBX Folder to Collections"
    bl_idname = "BATCHFBX_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Batch FBX"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Import all FBX in a folder:")
        op = layout.operator(BATCHFBX_OT_folder_to_collections.bl_idname, text="Batch FBX Folder to Collections")
        # Defaultverdier (kan endres i redo-panelet etter kjøring)
        op.recursive = False
        op.unlink_from_other_collections = True


def menu_func_import(self, context):
    self.layout.separator()
    self.layout.operator(
        BATCHFBX_OT_folder_to_collections.bl_idname,
        text="Batch FBX Folder to Blender Collections"
    )


classes = (
    BATCHFBX_OT_folder_to_collections,
    BATCHFBX_PT_panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
  
