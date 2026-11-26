# Release 0.3.0

Goal-driven lighting combines named-light adjustments with exposure, background protection, key-to-fill ratio and image luminance targets in Blender 5.3.0. Added local fill and receiver changes require explicit permission. Cycles CPU measurement and candidate protection were tested on Windows with build `02f0899d78e3`. See the [production request guide](GOAL-LIGHTING.md).

# Release 0.2.2

The Windows Blender 5.3.0 build 02f0899d78e3 ran the repository's procedural fixture through a managed key and fill rig, World and disabled flag, then independently reopened the result and produced one decoded 128 × 128 image each in Cycles and EEVEE. Source bytes remained identical. Version 0.2.2 records this qualification in the extension and CLI discovery.

# Release 0.2.1

First standalone public release of Lighting Workflow0.2.1, with compatible blenderctl0.57.0 runtime and lighting skill0.2.0. CLI/schema and skill versions remain unchanged. The original0.2.0 was the locally accepted case baseline, not the extension distributed by this release.

## Cold-reopen transform fix

Installation/cold-reopen validation discovered that `matrix_world` can expose an identity cache for disabled managed lights/boards.0.2.1 fixes both inspection and template export through a shared rigid-transform reader using persisted basis, parent inverse and evaluated parent transforms. It does not toggle visibility or modify hidden-state flags. Unsupported own constraints, Action, physics and curve parenting fail explicitly.

Targeted regression passed world/target/camera anchors at frames1/8/16, disabled-object migration and independent reopening, plus15 core/21 template checks. This is a real patch for a runtime defect, not a repository architecture change, submodule introduction or blanket version upgrade.

Final implementation identity: `6736923ee41f64392c3217336d9d34849bc0ad5e5b1269604574d5568d28dbb8`.

Extension ZIP SHA-256: `8a58c16659a3b7db86160fa2a6bb5a1fc2eb7349f360aae2f53292e4b679eee3`.

Includes managed lights/Worlds, native controls, reflector/flag boards, receiver/blocker linking, actual-state versioned templates, target adaptation, bounded cross-file batches, cancellation and checkpoint recovery. World/target/camera anchoring and representative multi-camera/simple motion were locally exercised.

Public export keeps the final patched runtime bytes and original directory layout intact. The original0.2.0 extension and `3864a9897c563093b98e4c0c91e87817371d8fd194a4e3e3dcc93499726e272a` identity remain historical local evidence. Portable launcher/export checks are packaging work, not retroactive scene rendering. The public skill keeps its lighting rules and version0.2.0, adapting environment/path/evidence navigation and the supported plugin baseline.

The public summary reports the original0.2.0 four representative cases/eight formal static PNGs,24 motion samples,15 core checks,21 template checks plus alias/boundary checks, exact ZIP/skill execution and51 cross-review checks. Those images were not relabeled or claimed rerendered under0.2.1. Original private scenes/images/audit reports are excluded. See [VALIDATION](VALIDATION.md) for the separately recorded patch regression and engine/UI/platform/resource/efficiency boundaries.

Eevee reflector indirect fill still needs explicit VOLUME probe setup and matching bake; the extension does not perform it. Native Sky Sun Disc is Cycles-only. Existing M1 projects remain compatible, but old recovery reports without saved expectations require new source runs. No full animation, arbitrary asset, universal speedup or public Linux/Blender CI promise is added.

Source, extension and skill distribution are [GPL-3.0-or-later](LICENSING.md). This release does not modify or republish an unrelated repository, global agent configuration or external runtime.
