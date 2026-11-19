# Lighting Workflow

[简体中文](README.zh-CN.md)

A Blender extension and companion agent skill for creating, editing, inspecting and restoring editable lighting plans through protected saved-file CLI work units.

**Lighting Workflow 0.2.2 · compatible blenderctl snapshot 0.57.0 · lighting skill 0.2.0 · GPL-3.0-or-later.** The Windows Blender 5.3.0 compatibility check covered managed rig creation, cold reopen and static Cycles and EEVEE previews. The previous Blender 5.2.1 qualification is recorded in the release notes.

The0.2.1 patch fixes cold-reopen transforms of disabled managed lights/boards in inspection and template export. Original four-case image evidence remains the0.2.0 baseline; it is not relabeled with the patch identity. See [release notes](docs/RELEASE_NOTES.md).

## Capabilities

- Managed native lights, softbox/strip shapes, constant/HDRI/Sky Worlds, reflector/flag boards, receiver and shadow linking with INCLUDE/EXCLUDE.
- Explicit create/patch/restore, independent candidates, source/material/camera protection, field-level manual-edit conflicts and fresh-process reopening.
- Actual-state versioned templates, explicit external-object bindings, target-size adaptation and native or scale-squared power policies; SUN energy does not scale with target extent.
- Bounded sequential batches, per-item results, partial failure, cancellation checkpoints and hash/implementation/runtime-bound recovery.
- World/target/camera anchors, multiple cameras and sampled simple motion. A small Blender sidebar supports inspecting and selecting managed rigs and editing native controls.

The local representative set covers product, cartoon/NPR character, room and outdoor scenes in Cycles and Eevee. Technical verification and user approval are distinct; see [validation and limits](docs/VALIDATION.md).

**Eevee reflector indirect fill requires an explicitly configured VOLUME light probe and matching bake. The extension does not create, bake or rebake probes.** Ray tracing alone is insufficient in the verified fixture. Sky's native Sun Disc is Cycles-only. NPR uses engine-specific material inputs; the lighting extension subsequently protects them.

## Install and run

Install the 0.2.2 extension ZIP through Blender **Preferences → Extensions → Install from Disk** and enable Lighting Workflow. The release includes SHA-256 checksums.

Clone or unpack this repository for the compatible CLI. Python **3.12+** and a separately installed Blender are required; neither is bundled. This checkout keeps the original `tools/` layout and all runtime Python modules byte-for-byte to preserve lighting implementation identity. Optional domains retain their separate dependencies and verification scope; packaging their modules does not certify them.

From the checkout in PowerShell:

```powershell
$env:BLENDERCTL_ROOT = (Get-Location).Path
$env:BLENDER_PATH = '<absolute-path-to-blender.exe>'
$env:BLENDERCTL_PYTHON = '<absolute-path-to-python.exe>'
./blenderctl.ps1 --version
./blenderctl.ps1 lighting describe
./blenderctl.ps1 lighting describe --operation run --schema
./blenderctl.ps1 --blender $env:BLENDER_PATH --jobs-dir (Join-Path $env:BLENDERCTL_ROOT 'runtime/lighting-jobs') --timeout 900 --compact request '<absolute-path-to-request.json>'
```

`BLENDERCTL_ROOT` identifies the selected checkout; call that checkout's launcher explicitly. Outside the original portable runtime layout, pass the real **`--blender`** executable. All global options precede subcommands. Requests use absolute source/resource paths and expected SHA-256 hashes. Read final `ok/error`, per-item results, protection, independent reopen and render records; the disk report remains authoritative.

The five execution commands are `lighting.run`, `lighting.inspect`, `lighting.template-save`, `lighting.template-edit` and `lighting.batch`. See [usage and JSON examples](docs/USAGE.md), [skill installation](docs/SKILLS.md) and live `lighting describe`. Installed agent skills become discoverable on the host's next turn/catalog refresh; installing a skill does not install Blender or configure this CLI.

## Distributed scope

This public repository contains extension/runtime source, schemas, portable skill documentation and release tooling. It excludes Blender binaries, user production assets, private `.blend` files, original rendered case images, production audit JSON, personal configuration, working-memory records and private Wiki.

Original bounded local validation is summarized publicly; it is not a claim that public CI rendered Blender scenes or validated Linux. The patch adds the documented transform-reading correction without changing the CLI0.57.0/schema version, artistic methods or repository/runtime architecture. See [release notes](docs/RELEASE_NOTES.md) and [license scope](docs/LICENSING.md).
