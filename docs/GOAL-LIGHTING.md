# Goal-driven lighting in Blender 5.3

Lighting Workflow 0.3.0 tunes explicitly named lights against measured scene-linear targets at the active camera and frame of a saved project. The Windows Blender 5.3.0 build used for acceptance was `02f0899d78e3`. Use the separate [blenderctl v0.64.0 distribution](https://github.com/tsist/blenderctl/releases/tag/v0.64.0) with production release `1.0.0`.

Run this example from the blenderctl distribution. Replace the names and power limits with those in your project. The file's active camera and saved frame must show the named measurement objects.

```powershell
$source = (Resolve-Path -LiteralPath './shot.blend').Path
$request = @{
  schema_version = '1.0'
  command = 'production.run'
  params = @{
    file = $source
    expected_sha256 = (Get-FileHash -LiteralPath $source).Hash.ToLowerInvariant()
    release = '1.0.0'
    domain = 'lighting'
    context = @{ scene = 'Scene'; view_layer = 'ViewLayer' }
    request = @{
      scene = 'Scene'
      view_layer = 'ViewLayer'
      lights = @(@{ name = 'Key'; max_energy = 500 }, @{ name = 'Fill'; max_energy = 250 })
      exposure = @(@{
        subject = 'Subject'
        stops = 0.4
        tolerance_stops = 0.10
        protect = @(@{ object = 'Background'; tolerance_stops = 0.10 })
      })
      key_fill = @(@{
        key = @('Key')
        fill = @('Fill')
        region = @{ object = 'Subject' }
        ratio = 2.0
        tolerance_stops = 0.10
      })
      sampling = @{ width = 224; samples = 64; threads = 2 }
    }
  }
}
$request | ConvertTo-Json -Depth 10 | Set-Content './light-goals.json' -Encoding utf8
./blenderctl.ps1 --blender '<absolute-path-to-blender.exe>' request './light-goals.json'
```

- Combine relative exposure, protected object drift, and key-to-fill measurements with `brightness` limits if required. A brightness entry contains `roi = @(left, top, right, bottom)` in normalized image coordinates and scene-linear luminance `min` and `max`. Measure the baseline before selecting those limits.
- The default adjusts power of named eligible static lights. To add a local AREA fill, supply name, position, aim, size, and permitted power bounds under `add_lights`, with `allow_add_lights = $true`. To change a named emitter's receiver links, supply `light_links` with `allow_link_changes = $true`.
- Cycles CPU measures the constraints at the declared sample count. Read `production-report.json` for baseline and measured values, tolerances, before and after powers, and protection status. An unsatisfied request reports the conflict and preserves the source without promoting a candidate. Use `apply = $false` to assess a proposal without saving.
- For an applied request, keep the candidate path and SHA-256. Review the final render separately in your production engine at the actual exposure and output settings.
