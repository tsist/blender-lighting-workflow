# CLI usage and contracts

Use this checkout's `blenderctl.ps1`, Python3.12+ and a separately installed Blender. Set `BLENDERCTL_ROOT` to the absolute checkout, `BLENDER_PATH` to the executable and, if discovery needs it, `BLENDERCTL_PYTHON` to a chosen interpreter. Global `--blender`, `--jobs-dir`, `--timeout`, `--async` and `--compact` options precede subcommands. A launcher on other platforms needs its own verification; Python source availability is not a platform acceptance claim.

```powershell
$lightingCli = Join-Path $env:BLENDERCTL_ROOT 'blenderctl.ps1'
& $lightingCli lighting describe
& $lightingCli lighting describe --operation template --schema
& $lightingCli lighting describe --section boards
& $lightingCli --blender $env:BLENDER_PATH --jobs-dir '<new-absolute-jobs-directory>' --timeout 900 --compact request '<absolute-request.json>'
```

## Five operations

| JSON command | Direct CLI | Behavior |
| --- | --- | --- |
| `lighting.run` | `lighting run` | Create/patch/restore manifest, or hashed template+target; candidate/reopen/optional previews |
| `lighting.inspect` | `lighting inspect` | Read a saved snapshot's actual rig/light/board/link state |
| `lighting.template-save` | `lighting template-save` | Export representable live state, not the old creation recipe |
| `lighting.template-edit` | `lighting template-edit` | Full `edits.content`, strictly increasing revision and parent SHA; old file untouched |
| `lighting.batch` | `lighting batch` |1–8 independent items, at most24 preview outputs, sequential rendering |

The eight lighting schemas in [schemas](cli/schemas/) cover run, inspect, manifest, template, target, template-save, template-edit and batch. Describe returns the runtime's exact schema. Example requests below contain placeholders; replace every absolute path/name and hash with actual inputs.

## First saved-file create

Save GUI edits to a clear persistent `.blend` snapshot first. The CLI cannot observe unsaved GUI changes. A simple schema-valid JSON request is:

```json
{
  "schema_version": "1.0",
  "command": "lighting.run",
  "params": {
    "file": "<absolute-source.blend>",
    "expected_sha256": "<source-sha256-lowercase-64hex>",
    "resources": [],
    "manifest": {
      "version": "1.0", "scene": "Scene", "view_layer": "ViewLayer",
      "rig_id": "studio", "action": "create", "targets": ["Product"],
      "mode": "relight", "anchor": "world",
      "lights": [{
        "id": "key", "role": "key", "type": "AREA",
        "location": [1, -1.5, 1.5], "aim": [0, 0, 0],
        "energy": 200, "color": [1, 0.9, 0.8], "size": 0.8,
        "shape": "DISK", "normalize": true
      }],
      "world": {"kind": "constant", "color": [0.05, 0.05, 0.05], "strength": 0.1}
    }
  }
}
```

`resources: []` is valid only when the actual input has no unpacked external dependencies. Declare each actual static file as `{ "file": "<absolute-resource>", "expected_sha256": "<hash>" }`; packed HDRI export creates owned byte-verified resource files. Dynamic UDIM/sequence/cache contracts need the existing dedicated facilities and are not silently closed by this example.

Positions and light/board sizes are normalized to the target's evaluated maximum world-bbox extent. Energy uses native Blender units;200W is an illustrative input, not an artistic default. Use `adapt` to preserve actual existing lights and add managed supplementation, and name `keep_lights` when relighting requires explicit exceptions. One Scene supports one active rig; restore before creating another. Models, materials and existing cameras are protected. World/exposure changes are explicit; absent cameras may be created.

To inspect the resulting saved candidate, point `lighting.inspect` at its **new** SHA, not the original source hash. A patch uses the latest snapshot and `patches:[{"id":"key","values":{"energy":160}}]`; a restore uses the same Scene/View Layer/rig with `action:"restore"`. Structural hand edits are not silently overwritten.

## Templates and versions

Template-save params require `file`, `expected_sha256`, `resources`, `scene`, `rig_id`, `template_id`, `revision`. The job saves a new template descriptor. Template-edit params are:

```json
{
  "template": {"file": "<absolute-template.json>", "expected_sha256": "<hash>"},
  "revision": 2,
  "edits": {"content": {"<replace-with-complete-template-JSON>": "not-a-patch"}}
}
```

That last content placeholder must be replaced by the complete schema-valid template. Keep the template_id; the new revision must exceed the old. The host records `parent_sha256` and writes a new file.

For a template run, replace `manifest` with hashed `template` and `target`:

```json
{
  "template": {"file": "<absolute-template.json>", "expected_sha256": "<hash>"},
  "target": {
    "scene": "Scene", "view_layer": "ViewLayer", "rig_id": "migrated",
    "targets": ["DestinationProduct"], "mode": "relight", "anchor": "world",
    "power_policy": "scale_squared", "bindings": {"ExternalReceiver": "ChosenReceiver"}
  }
}
```

Source/destination targets map by ordered index, owned boards by ID. Only include actually needed external bindings; unused/conflicting/missing bindings fail, including coincidental same names. `native` preserves power; `scale_squared` scales non-SUN energy by target extent ratio squared. Neither ensures the same art on different shapes. World templates copy representable managed structures only; they do not clone arbitrary scene nodes/settings. Roll/nonunit light scale, split viewport/render visibility or other unrepresentable changes fail.

## Preview, batch and recovery

Preview schema supports `CYCLES`/`BLENDER_EEVEE`, explicit device, width/height each16–2048, samples1–256, up to24 frames/cameras individually; the actual Cartesian render total per run and entire batch is limited to24. Batch has at most8 items. Cycles device/backend is explicitly chosen; Eevee renders through GRAPHICS. A sample preview object:

```json
{"engines":["CYCLES","BLENDER_EEVEE"],"device":{"backend":"CPU"},"width":768,"height":768,"samples":64,"frames":[1],"cameras":["Camera"],"denoise":true}
```

Batch params are `{ "version":"1.0", "items":[{"id":"first","params":{...complete-lighting-run-params...}}] }`; use UTF-8 JSON and unique IDs. Partial results retain per-item failures and successes but return failure/nonzero status. Compact output may summarize the envelope as failed; inspect its per-item results and hashed full report to distinguish partial completion.

For `--async`, retain the job ID, then use the same jobs directory with `job wait <id> --wait-seconds 30`. This is a bounded wait; submission is not completion. Cancel only the owned job, wait for its terminal state, then resume using the original request plus `resume:{file,expected_sha256}` for the authoritative report. Preserve upstream jobs/resources. Recovery verifies source/resource hashes, runtime/implementation identity, candidate SHA and original saved expectations. Do not manufacture a new expectation from a suspect candidate. Earlier reports without saved expectations require a new source run; old M1 projects can still be edited/restored.

See [engine support and verification limits](VALIDATION.md). A successful report is not an artistic approval or an automatic Eevee probe bake.
