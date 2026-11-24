---
name: blender-lighting
description: 使用 Lighting Workflow 插件与公共 blenderctl 保留中性基线灯、分析参考光向光比与色温、搭建主光辅光轮廓光与环境 HDRI、对比双引擎画面并用模板批量套用到同场景多镜头。接到资产或镜头的成片布光、灯组微调、跨镜复用或还原灯组任务时使用。
metadata:
  version: "1.0.0"
---

# Blender 灯光制作

本技能负责把布光意图做成可编辑、可还原、可跨镜复用的 Blender 灯光方案，属于 [镜头与灯光部门](https://github.com/tsist/blender-ai-workflow/blob/main/skills/blender-work-methodology/references/departments/camera-lighting.md)。留住材质审看时的中性基线灯当参照，再搭成片主灯组与单镜补光，用实拍画面把关造型、光比与情绪。

## 怎么做

### 1. 摸清工程现场，留住中性基线灯

先拿到已保存的 `.blend` 工程并算出小写 SHA256，再用只读命令摸清场景名、View Layer、目标对象边界框、已有相机、原灯具与 World 设置。在独立工作副本上新建成片灯组，源工程和中性基线灯完整留着对照，方便随时分辨问题出在材质还是灯光。

```powershell
$ctl   = './blenderctl.ps1'
$batch = 'work/audit/<batch>/'
$jobs  = Join-Path $batch 'jobs'
New-Item -ItemType Directory -Path $jobs -Force | Out-Null

$src = '<PROJECT_ROOT>/work\tea\shot01-camera.blend'
$sha = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash.ToLowerInvariant()

# 实时查看最新动作、发行号与字段说明
& $ctl discover --product lighting
& $ctl lighting describe
& $ctl --jobs-dir $jobs scene inspect $src --expected-sha256 $sha
& $ctl --jobs-dir $jobs lighting inspect $src --expected-sha256 $sha --resources $resJson --scene Scene
```

- **资产或产品重打**：在清单一律选 `mode: "relight"`。插件会收起原有灯具并记下恢复状态，画面干净又随时能退回。
- **室内外实景补光**：选 `mode: "adapt"` 并把要保留的窗光、实景灯名写进 `keep_lights`。顺着场景原有光源方向补光，空间才自然。

### 2. 拆解视觉参考，定下光向、光比与色温

动手摆灯前先用一句话写明画面目标，再把参考图拆成可验证的要素：主光方向、光源角尺寸（决定阴影软硬）、主辅光比、冷暖色温、主体与背景的轮廓分离，以及金属或玻璃上的反射形状。

首轮选出两到三个有实质差异的方向，用小图预览快速对比。方向定了再做精修，省去盲目调参的时间。判断要点见 [照明分析与画面判断](references/lighting-principles.md)。

### 3. 搭建主光、辅光、轮廓光与环境

先用 `lighting describe --section lights`、`--section world` 和 `--section boards` 核对最新字段，写好 UTF-8 JSON 清单，通过 `lighting run` 的 `action: "create"` 搭起完整灯组。

- **主光（Key）定造型**：按参考方向安放主灯，调节光源尺寸与距离控制阴影软硬。柔光箱和长条高光用原生 `AREA` 配 `shape: "RECTANGLE"` 及 `size`、`size_y`。
- **辅光（Fill）控光比**：给暗部留出层次与质感，让明暗有呼吸感，再按需要补上白色反光板（`reflector`）或黑色遮光板（`flag`）。
- **轮廓光（Rim）提分离**：从侧后方勾出主体边缘，需要单独照亮或避开特定对象时，用 `receivers` / `blockers` 与 `INCLUDE` / `EXCLUDE` 做光链接和阴影链接。
- **环境与天空**：`world.kind` 可选 `constant`、`sky` 或 `hdri`。用到外部 HDRI 时，在 `resources` 中声明绝对路径与 SHA256，确保冷重开后依赖完整。
- **尺度与锚定**：灯位与灯具尺寸按目标边界框最长边归一，`energy` 则是原生功率。换不同尺寸的主体时，按实际体量重新选定功率。`anchor` 默认挂在 `world`，需要随主体或相机联动时显式设为 `target` 或 `camera`。

### 4. 对比 Cycles 与 EEVEE Next 光追实拍画面

在 `lighting run` 的 `preview` 里同时指定 Cycles 与 EEVEE Next，保持同一相机、同一帧、同一曝光与色彩管理出图对比。快速迭代用 768–1024px，定稿静帧出 2048px；长作业通过 `job wait --wait-seconds 30` 分段等待。

- **看图核对**：逐张打开实拍 PNG，对照中性基线图检查立体感、阴影落点、眼神光、金属反射形状和暗部细节。
- **跨引擎统一太阳**：在程序天空中显式设 `sun_disc: false`，另加一盏原生 `SUN` 负责直射太阳光，让双引擎的太阳角度与阴影保持一致。
- **EEVEE Next 反光板补光**：场景里用到白色反光板产生间接补光时，先给场景放好并烘焙原生 `VOLUME` 光照探针；灯位或反光板挪动后重新烘焙并保存。更多引擎细则见 [高级控光与双引擎对策](references/advanced-controls.md)。

### 5. 迭代微调、接续手调与安全还原

- **有依据地迭代**：先跑 `lighting inspect` 读最新快照，再用 `lighting run` 的 `action: "patch"` 做小步修改。每轮只动一个主变量（如主光角度、光比或环境强度），出图对照有明显改善再往下走；每轮最多做两步自主精修，带着前后对比图请用户拍板。
- **保护现场手调**：同字段遇到手调冲突时，先看报告里的 `conflict` 提示，核对差异后再决定保留手调或显式覆盖。
- **用 `rig-handoff` 接手已存灯组**：需要对已保存工程选定受管灯组、单灯微调属性或读写内嵌快照时，运行 `lighting rig-handoff`（先用 `discover --product lighting` 查当前 `edition`）：
  - `choose-rig` / `choose-light` / `select-group`：在指定视图层切换当前方案或选中整组灯光。
  - `edit-light`：直接微调单灯的 `shape`、`angle_deg`、`hide_render`、`hide_viewport`。
  - `save-snapshot` / `read-snapshot`：把当前灯组写进工程内嵌文本快照，或按文本名独立读回核对。
- **退回布光前状态**：需要换一套全新灯光或还原旧场景时，运行 `lighting run` 的 `action: "restore"`，并在独立重开后核对原 World、曝光和原灯可见性。

### 6. 保存灯组模板，批量套用到同场景多镜头

主镜头灯光通过审看后，把当前实际状态导成版本化模板，快速复用到同场景其余镜头，保证整场戏气氛统一。

1. **导出模板**：运行 `lighting template-save`，从已保存工程里导出实际灯位、功率、色温、控光板、光链接和可表达的 World。
2. **迭代模板**：需要修改模板参数时，运行 `lighting template-edit` 生成更高 `revision` 的新文件，旧模板原样留作回溯。
3. **跨镜套用与批量出图**：单镜套用跑 `lighting run --template <模板> --template-sha256 <SHA> --target <目标JSON>`；多镜批量跑 `lighting batch`（每批最多 8 项、合计最多 24 张预览，按顺序逐项存盘）。
   - `power_policy` 显式选 `native`（同尺度直接复用）或 `scale_squared`（按主体尺度比平方缩放非 `SUN` 灯功率，`SUN` 保持原值）。
   - 外部链接对象在 `bindings` 里明确映射，套用后照常出图复核机位反射与暗部。
   - 批量中途中断或部分失败时，等作业进入终态，带上原报告路径与 SHA256 运行 `--resume` 续跑。

## 交给下游

打包交付给渲染、合成或剪辑部门时，交齐下面五样东西：

- **可编辑灯光工程副本**：保存好的 `.blend` 绝对路径与 SHA256（源工程与中性基线灯保持完好）。
- **依赖与报告**：`lighting-report.json`、外部 HDRI 路径与 SHA256 清单，以及已保存的模板文件或内嵌快照名。
- **双组对照图**：同机位、同曝光的中性基线灯 vs 成片布光对照图，以及 Cycles 与 EEVEE Next 实拍预览图。
- **冷重开核验结论**：确认独立重开无丢贴图、原模型/材质/相机均未受改动。

**返修分工**：构图遮挡或运镜问题回相机环节调；受光死黑、高光爆掉或眼神光缺失留在灯光环节修；换了多套灯光金属依然发灰像塑料，退回 UV 与材质部门查粗糙度与金属度贴图。

## 例子：给茶具主镜搭暖调侧逆光并套用到两个特写镜头

接到任务：「给 `work/tea/shot01-camera.blend` 里的紫砂壶主镜做清晨暖调侧逆光，定稿后同步到 `shot02-close.blend` 和 `shot03-pour.blend`。」

1. **查现场留基线**：建批次目录 `work/audit/<batch>/`，算出 `shot01-camera.blend` 的 SHA256，运行 `lighting inspect` 确认场景名为 `Scene`、目标对象为 `Teapot_Main`，同时留住材质审看阶段的中性基线灯图当标尺。
2. **拆参考建灯组**：写好 `manifest-create.json`，设 `mode: "relight"`、`anchor: "target"`，搭起 45° 侧后方暖色长条主光（`AREA` + `RECTANGLE`）、正面低强度冷调柔光辅灯、右侧低位黑旗控高光溢出，再挂一张声明了 SHA256 的清晨室内 HDRI。
3. **跑双引擎对比**：提交 `lighting run` 生成工作副本和 Cycles / EEVEE Next 1024px 预览图。打开对比发现壶嘴侧高光略硬、壶腹暗部偏闷，记录差异。
4. **微调与留快照**：提交一次 `action: "patch"` 拉大主光尺寸、微抬辅光并调整黑旗角度，再渲图确认体积与釉面高光到位。接着用 `lighting rig-handoff` 执行 `save-snapshot` 在工程里留一份快照。
5. **存模板并批量套用**：运行 `lighting template-save` 导出 `tea-morning-r1.json`。写一份包含 `shot02-close.blend` 与 `shot03-pour.blend` 的 `batch-manifest.json`（设 `power_policy: "native"` 并配好 `bindings`），运行 `lighting batch` 顺序生成两个特写镜头的灯光副本与 2048px 实拍图。
6. **冷重开与交接**：核对三份报告的冷重开结果与图档无误，把三个灯光副本、模板文件、HDRI 清单以及基线/成片对照图交给用户审看，确认后送渲染与合成部门。

## 参考

- [照明分析与画面判断](references/lighting-principles.md)
- [高级控光与双引擎对策](references/advanced-controls.md)
- [能力范围与协作边界](references/scope.md)
- [命令契约、Schema 与源码索引](references/sources.md)

维护：唯一维护源是 `./.agents/skills/blender-lighting/`，改完按项目流程同步各镜像。
