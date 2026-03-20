# Super Simple PBR Material Library — Blender Addon

Super simple one-click material assignment tool for Blender.
Built to speed up asset preparation for real-time engines and web 3D pipelines when hust want to assign "basic" mats.

All materials use **Principled BSDF** and export correctly via **glTF 2.0** to Three.js, Babylon.js, Unity, Unreal Engine, PlayCanvas, and React Three Fiber.

![Blender](https://img.shields.io/badge/Blender-3.0%2B-orange?logo=blender&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.4-blue)

---

## Materials

| Category | Materials |
|---|---|
| Water | Freshwater, Seawater, Pool Water |
| Metal | Chrome, Steel (Polished / Matte), Aluminum, Titanium, Iron, Gold, Copper, Brass, Diamondplate, Rust |
| Glass | Clear, Frosted, Thick, Mirror, Blue, Green, Red, Amber, Smoke, Ice Blue |
| Emissive | Warm White, Yellow, Orange, Red, Cool White, Cyan, Ice Blue, Green |
| Neon | Neon Blue, Neon Purple |
| Paint | White, Light Gray, Dark Gray, Black, Red, Orange, Yellow, Brown, Green, Blue, Light Blue, Purple |

---

<img width="243" height="832" alt="image" src="https://github.com/user-attachments/assets/a4f7a43c-e4fd-4175-b169-33b72c2f9db4" />

## Installation

1. Download `pbr_material_library_EN.py`
2. In Blender: `Edit > Preferences > Add-ons > Install`
3. Select the file and enable the addon
4. Open the N-panel in the 3D Viewport (`N` key) → **PBR Lib** tab

## Usage

1. Select one or more mesh objects
2. Click any material button to assign
3. Export via `File > Export > glTF 2.0 (.glb)`

---

## Compatibility

Tested on Blender **3.x** and **4.x** — handles API differences for `blend_method`, `shadow_method`, `Transmission Weight`, and `Emission Color` automatically.
