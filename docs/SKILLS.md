# Agent skill installation

The public [blender-lighting skill](../skills/blender-lighting/SKILL.md) version 1.1.0 includes the Blender 5.3 goal-driven workflow and the existing managed-rig methods. The [production request guide](GOAL-LIGHTING.md) identifies the separate compatible blenderctl distribution.

Choose the host's actual skill directory explicitly. For Codex this is normally a `skills` directory beneath its configured home; other agents have their own conventions. Installation copies only the skill, not Blender or a CLI environment. Existing directories must be reviewed/migrated deliberately, not silently overwritten.

```powershell
$lightingSkillSource = Join-Path $env:BLENDERCTL_ROOT 'skills/blender-lighting'
$lightingSkillDestination = Join-Path '<absolute-agent-skill-root>' 'blender-lighting'
if (Test-Path -LiteralPath $lightingSkillDestination) { throw 'Skill already exists; compare and migrate explicitly.' }
Copy-Item -LiteralPath $lightingSkillSource -Destination $lightingSkillDestination -Recurse
```

After installation, start the next agent turn or refresh/restart the host's skill catalog as required. No claim is made that the skill becomes callable within an already-running turn. Set `BLENDERCTL_ROOT` to this matching source checkout and pass the actual Blender executable via `--blender`. If necessary, set `BLENDERCTL_PYTHON` to Python3.12+ for the checkout launcher.

The lighting skill uses this repo's public docs and live CLI schema for contracts; companion modeling/material/CLI knowledge may come from the host's existing tools. It does not configure external providers, persistent memory, account permissions or resource libraries. Knowledge of a native Blender feature is not evidence that its effect has been verified in a new scene.
