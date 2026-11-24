# 能力范围与协作边界

本文件说明当前工作区灯光工作流的适用范围、场景前置条件与跨部门协作分工。实时查看当前宿主、已验发行号与全部动作清单，运行：

```powershell
& './blenderctl.ps1' discover --product lighting --actions
```

## 当前可直接使用的能力

- **工作副本生命周期**：围绕明确保存的 `.blend` 与 SHA256 执行 `lighting inspect` 及 `lighting run`（`create`、`patch`、`restore`），每次编辑均输出独立候选并经另起进程冷重开复核，原工程、模型、材质与既有相机保持完好。
- **原生灯具与环境**：支持 `AREA`、`POINT`、`SPOT`、`SUN` 全套原生参数、柔光箱与条光、常量 World、程序天空与外部 HDRI（带资源 SHA256 闭环校验），并支持可选棚拍背景地板。
- **锚定与运动镜头**：支持 `world`、`target`、`camera` 三类锚定，可在指定帧号上建灯与多帧出图核验。
- **高阶控光**：支持原生照明链接（`receivers`）与阴影链接（`blockers`）的 `INCLUDE` / `EXCLUDE` 模式，以及受管反光板（`reflector`）和黑遮光板（`flag`）。
- **双引擎对照预览**：支持在同一工作流内输出 Cycles 与 EEVEE Next 实拍 PNG 预览并各自解码核验。
- **面板交接与内嵌快照**：支持通过 `lighting rig-handoff` 对已保存工程执行选方案、选单灯、选整组、编辑单灯属性（`shape`、`angle_deg`、`hide_render`、`hide_viewport`）以及读写工程内嵌快照。
- **模板与批量**：支持导出当前实际状态为版本化模板、递增修订模板、按功率策略跨镜迁移，以及 1 至 8 项、合计最多 24 图的有界顺序批量与安全断点续跑。

## 使用前置与约定

- **单场景单活动灯组**：一个 Scene 同一时刻保持一个活动受管灯组。需要换一套全新布光方案时，先对当前灯组执行 `restore` 还原原灯与 World，再创建新方案。
- **显式保存再交接**：用户在打开的 Blender 窗口里做了手调后，先保存持久 `.blend` 快照，再通过 `lighting inspect`、`lighting run` 或 `lighting rig-handoff` 接手，确保后台读到最新状态。
- **外部资源声明**：静态贴图与 HDRI 在 `resources` 中声明绝对路径与 SHA256；涉及动态 UDIM、序列帧贴图或模拟缓存时，按对应专项契约先做好前置准备。
- **EEVEE Next 反光补光前置**：需要白色反光板在 EEVEE Next 下贡献间接补光时，提前在场景中配置并烘焙 `VOLUME` 光照探针，灯位或控光板调整后重新烘焙并保存。
- **跨引擎太阳统一**：需要双引擎保持一致的直射太阳光时，将程序天空的 `sun_disc` 设为 `false`，用原生 `SUN` 灯具承担太阳主光。

## 与其他部门的协作分工

- **相机与镜头表**：构图调整、景别切换和镜头起止帧排定，交由 [blender-camera-workflow](https://github.com/tsist/blender-camera-workflow/blob/main/skills/blender-camera-workflow/SKILL.md) 统筹。
- **材质与着色修改**：排查后确认发灰、塑料感或高光异常源自材质节点或贴图，以及为三渲二分别配置 Cycles / EEVEE 专属着色器时，交由 [blender-material-authoring](https://github.com/tsist/blender-material-workflow/blob/main/skills/blender-material-authoring/SKILL.md) 或 [blender-toon-workflow](https://github.com/tsist/blender-toon-workflow/blob/main/skills/blender-toon-workflow/SKILL.md) 处理，再把定稿副本交回布光。
- **批量镜头渲染与后期合成**：多镜头动画序列渲染交由 [blender-render-batch](https://github.com/tsist/blender-render-batch/blob/main/skills/blender-render-batch/SKILL.md)；辉光、景深、调色与后期深度补光交由 [blender-compositing](https://github.com/tsist/blender-compositing-workflow/blob/main/skills/blender-compositing/SKILL.md)。
- **正式资产入库**：带灯光或独立道具通过审看需要归档入库时，交由 [blender-asset-manager](https://github.com/tsist/blenderctl/blob/main/skills/blender-asset-manager/SKILL.md) 执行命名校验、目录编目与发布事务。
- **超范围特性**：涉及完整灯光关键帧动画编排、IES/Gobo 投射纹理或复杂体积雾制作时，先在工作副本上用 Blender 原生节点与动画工具配合实现，再由灯光环节统一核验最终画面。
