# Batch FBX Folder to Blender Collections

Batch import all FBX files from a selected folder and automatically organize them into Blender Collections named after each FBX file.
---
## What This Add-on Does

This add-on allows you to:

- Select a folder containing `.fbx` files
- Automatically import **all FBX files**
- Create a **separate Collection per FBX**
- Name each Collection after the FBX filename
- Optionally:
  - Include subfolders (recursive import)
  - Unlink imported objects from other collections (clean structure)

Perfect for asset libraries, kitbash folders, scan data, or large FBX dumps.

---
## Where to Find It in Blender

After installation and activation:

### Option 1 – N-Panel (Sidebar)

1. Open the **3D Viewport**
2. Press **N**
3. Go to the **"Batch FBX"** tab
4. Click:

   **Batch FBX Folder to Collections**

---

### Option 2 – File Menu

Go to:

File → Import → Batch FBX Folder to Blender Collections

---

## HOW IT WORKS

For each `.fbx` file in the selected folder:

1. Blender imports the file
2. A new Collection is created with the same name as the FBX file
3. All newly imported objects are moved into that Collection
4. (Optional) Objects are unlinked from other collections to keep the scene clean

### Example

Folder structure:\
MyFolder/\
├── Tree.fbx\
├── Rock.fbxv
└── House.fbx

Result in Blender:
Scene Collection\
├── Tree\
├── Rock\
└── House


Each Collection contains only the objects from its corresponding FBX file.

---

## INSTALLATION

   - Go to **Edit → Preferences → Add-ons**
   - Click **Install**
   - Select the zip file
   - Enable the add-on

---

## OPERATOR OPTIONS

When running the tool, you can configure:

### Recursive (Include Subfolders)
Imports FBX files from subdirectories as well.

### Unlink from Other Collections
Moves imported objects exclusively into their target Collection for a cleaner scene hierarchy.

---

## COMPATIBLE WITH

- Blender 2.80+
- Blender 3.x
- Blender 4.x

---

## USE CASES

- Asset library importing
- Game development pipelines
- Scan data processing
- Modular kit organization
- Cleaning up large FBX dumps

---

## LICENSE

Free to use and modify.
