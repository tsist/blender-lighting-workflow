# License and distribution scope

The Lighting Workflow extension, compatible project CLI snapshot, schemas, public lighting skill, documentation and release tooling are distributed under **GPL-3.0-or-later**; see [LICENSE](../LICENSE). The extension retains its original SPDX declaration. The matching CLI snapshot comes from the same project's licensed distribution; keeping its runtime modules intact preserves execution identity and does not change ownership or the requirements of optional facilities.

External runtimes are not bundled: Python3.12+ uses the Python Software Foundation license; Blender/bpy/bmesh/mathutils and its native components retain their distribution's GPL and component notices. Optional CLI domains may rely on NumPy, OpenUSD/pxr, native import/export modules or other separately supplied packages. Consult each actual runtime/component license before redistribution. Host agent tools, external image providers and persistent memory are separately configured and authorized.

User production models, private `.blend` files, textures, original acceptance images and audit reports are not distributed and are not relicensed by this public summary. No production asset permission is inferred from technical validation. Source-only original fixture recipes, if supplied, are for bounded reproducibility; they do not authorize publishing third-party assets.

The archive contains no Blender/Python binary or third-party library implementation. Presence of optional domain source is not a promise that every optional dependency is included, installed, licensed for a user's chosen downstream distribution, or validated by the lighting release.
