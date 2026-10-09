# Validation and limits

The original local acceptance used **Windows, Blender5.2.1 LTS/build9e2066aef7ef, CLI0.57.0 and Lighting Workflow0.2.0**, with an RTX5080 Laptop OptiX device for Cycles production rendering. These are local results, not public CI or cross-platform certification.

## Recorded evidence

| Work | Original bounded result |
| --- | --- |
| Core | 15 native lifecycle/compatibility checks passed |
| Templates | 21 actual-state/migration checks; four alias negatives and native SUN endpoint check passed |
| Host/API | Original saved expectation rejection, partial failure/reuse and strong-supervisor cancellation/resume passed |
| Public advanced workflow | Four candidates/eight dual-engine images, plus template migration/two images passed |
| Exact extension archive | Native manifest check, isolated import/register/create/template export/board patch/restore/unregister passed |
| Skill exercise | Independent public-CLI version edit/migration and decoded CPU Cycles output passed;64px preview is operational evidence only |
| Cross-review | 51 schema/API/package/skill/evidence checks passed, with a declared abbreviated per-job support advisory |
| Static representative cases | Product, cartoon/NPR character, room and outdoor: eight PNGs, longest edge2048; five editable projects because the character has separate engine-specific material inputs |
| Motion | 24 images across world/target/camera anchoring and multi-camera samples; fresh-process matrix/non-target checks at frames1/8/16 |

The product direction and the three new preview directions received user acceptance as passable. Formal static outputs followed those directions and were reviewed by the primary agent; this does not claim the user directly inspected every final pixel file. Motion technical/image review is separate from that preview feedback. Original audit reports, user assets and case files remain private and are not uploaded by this repository.

## Engine differences

- Native receiver/blocker linking and flag shadows passed Cycles/Eevee fixtures and public operations. Linking is an artistic mechanism with specific semantics; including one blocker excludes other objects from casting that emitter's shadows.
- Cycles reflector indirect fill passed an optical fixture. Eevee with ray tracing alone had no effective fill in the matched fixture. Explicit native VOLUME setup and separately matching off/on bakes changed the ROI from0.003002 to0.081541; reopening preserved the result without rebaking. **The extension does not create/bake/rebake probes.** Reevaluate and rebake after scene/light/board changes.
- Synthetic float EXR fixtures verified HDRI rotation, strength and persistence in both engines. These small fixtures are not production-quality HDRI assets.
- Sky without native Sun Disc passed both engines. Native Sky Sun Disc is documented Cycles-only and was not independently pixel-validated here. Eevee World Sun extraction is a distinct mechanism; the contract does not expose `sun_threshold`. Explicit SUN lighting uses preserved input World state when this distinction matters.
- NPR character inputs use Cycles Toon BSDF and Eevee ShaderToRGB/ColorRamp respectively, with matching geometry/palette/camera. These input material changes are not made by the lighting extension and do not promise matching pixels or correct arbitrary render passes.

Single-job `support` is abbreviated: consult this table and [advanced controls](../skills/blender-lighting/references/advanced-controls.md), including probe/bake prerequisites, before interpreting a successful object-creation report as effective illumination.

## Reliability and scope

Source/resource SHA checks, candidate guards, fresh-process reopening and original saved expectations are distinct from visual acceptance. Non-conflicting field edits are retained; conflicting fields and unsupported structural changes fail. Recovery requires the original request, report hash, implementation/runtime identity and saved candidate hash. Reports predating original saved expectations require a new run from source; old M1 projects remain editable/restorable. No recovery is promised before a checkpoint was saved.

The implementation identity for the original0.2.0 formal-case snapshot is:

`3864a9897c563093b98e4c0c91e87817371d8fd194a4e3e3dcc93499726e272a`

Earlier public-operation evidence used a separately recorded `55fc939d…` source revision; its reports were not relabeled with the0.2.0 identity. Four-case formal images and24 motion images remain historical0.2.0 evidence. Public0.2.1 includes the targeted patch below; neither its new identity nor packaging checks retroactively certify those images under patched code.

### 0.2.1 cold-reopen patch

Installation/cold-reopen checks exposed a native `matrix_world` cache returning identity for disabled managed lights/boards. Inspection and template export now use a common rigid-transform reader from persisted basis, parent inverse and evaluated parent. It does not toggle visibility. Unsupported own constraints/action/physics and curve parenting are rejected rather than silently estimated.

Patch regression passed world/target/camera anchors at frames1/8/16, disabled migration with fresh reopening, and the15 core/21 template checks. This is targeted runtime evidence, not a rerender of the entire original acceptance set. CLI0.57.0 and schema versions remain unchanged.

Final0.2.1 implementation identity: `6736923ee41f64392c3217336d9d34849bc0ad5e5b1269604574d5568d28dbb8`.

Release extension ZIP SHA-256: `8a58c16659a3b7db86160fa2a6bb5a1fc2eb7349f360aae2f53292e4b679eee3`. The original0.2.0 ZIP is retained privately as historical evidence and is not this release's extension.

GUI rendered layout, rig-selection operation and shared headless operator lifecycle passed. Full GUI mouse interaction was not run. The official skill `quick_validate` was **not_run** because PyYAML was absent from the existing checked interpreters; structure/link/archive checks and independent skill execution passed separately.

Motion covers representative sampled frames, not continuous-video proof, full character binding, complex animation or lighting animation choreography. Native IES/Gobo, fog, other Blender versions, Linux/macOS and arbitrary asset/caches are not certified by these cases.

## Performance observations

Formal eight-image machine task wall time was235.001s; the24-image motion task was165.729s. In one matched small workload, two sequential calls became one batch call, client wall time10.749→10.063s and compact output8937→5742bytes. Fixed run order, caches and temperature were not randomized. These measurements exclude initial research/fixture development and do not prove a universal rendering speedup.

Public CI/source checks, when present, check the stated export/host invariants only. No Blender rendering or Linux functional validation is inferred from them. Reproduce on a chosen matching Blender, use fresh source snapshots/jobs, inspect actual rendered images and record your own limitations.
