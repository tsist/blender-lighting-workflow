---
name: blender-lighting
description: 使用 Lighting Workflow 插件与公共 Blender CLI 创建、编辑、诊断和恢复可编辑灯光方案，分析参考、比较双引擎实际输出并迭代。适用于照明制作；材质或合成需求与现有专项工具协作，资产编目另用资产技能。
metadata:
  version: "0.2.0"
---

# Blender 打光

公开副本保留技能0.2.0的照明规则，仅适配checkout、证据导航和当前插件0.2.1支持基线。先将 `BLENDERCTL_ROOT` 指向匹配的blender-lighting-workflow源码checkout绝对路径，调用该checkout的 `blenderctl.ps1`；正式执行显式提供全局 `--blender` 与独立 `--jobs-dir`。另需实际Blender；可用 `BLENDERCTL_PYTHON` 显式选择launcher的Python3.12+。技能安装不配置CLI或二进制，宿主通常从下一轮/目录刷新发现。公共入口见 所选checkout的`docs/USAGE.md`、`docs/VALIDATION.md`本机验收范围。

把打光意图转成可编辑方案，保留用户手改与源工程，依据实际图像判断质量。当前为开发候选，能力与证据读取 [当前范围](references/scope.md)，不能将预设或技术通过视为审美保证。

先从 `blenderctl.ps1 lighting describe` 发现领域接口；需要字段时用 `--operation run|inspect|manifest|template|target|template-save|template-edit|batch --schema` 或 `--section lights|world|patches|boards`。复杂任务使用 UTF-8 JSON `--compact request`；异步任务沿原 job ID 有界 `job wait --wait-seconds 30`，完整磁盘报告为权威。通用入口、身份和作业规则用所选checkout的docs/USAGE.md及宿主现有blender-cli（如有）。

明确目标主体、场景、相机、观察尺度与参考效果。自然语言或参考图提取光向、源尺寸、反射形状、明暗层次、色温/色彩与情绪；不能只凭“高级感”机械套三点光，也不承诺单图精确反求灯位。选择少量有差异的方向并说明取舍。

使用明确保存的 `.blend`；承接GUI工作先保存持久快照。检查实际Scene/View Layer、相机、原灯、World、单位/世界bbox、材质/发光物及共享引用。模型、产品材质与已有相机默认保护；缺相机可创建，构图修改须在任务中明确。产品重打可禁用原灯但保留恢复状态；室内外通常保留实际光源，再组织补光。

通过 `lighting.inspect` 确认受管状态；通过 `lighting.run` 的create/patch/restore完成工作。节点、光位、参数和依赖以当前合同为准。位置与灯具尺寸按目标bbox最长边归一；energy是原生功率，目标缩放时必须有意识选功率，不能把500W预设无条件用在小产品。锚定world/target/camera显式声明，默认world。

patch前读取最新快照；非冲突手改保留，同字段冲突先报告而非旧方案覆写。读取report中的protection、verification、source_unchanged、candidate SHA、error与recovery。恢复也要验证原World/曝光/原灯可见性和非目标，不以点击成功代替恢复。

需要复用时用 `lighting.template-save` 导出当前可表征的实际状态；`template-edit` 以完整 `edits.content` 生成严格递增版本并记录父SHA，不覆写旧文件。`run` 的 manifest 与 template+target 二选一；迁移时显式选择 `native` 或 `scale_squared` 功率策略，SUN不按尺寸平方改变。目标按顺序映射，受管板自动映射，其他链接对象用 `bindings` 明确映射；缺映射报错。模板不会迁移任意节点改造、灯具roll或分离的render/viewport可见性，遇到拒绝先说明原因。

`lighting.batch` 最多8项、合计24预览，顺序执行并为每项保存候选。部分失败返回失败退出码且保留成功项；从带SHA的父报告恢复时，成功项重新独立重开、核图SHA，失败项可复用已有检查点。取消必须等待本作业终态；不能边运行边恢复。恢复保持原保存期望，不能用损坏候选重新建立基线。旧M1报告没有原期望时从源重新运行；旧M1工程仍可正常编辑/恢复。

首轮默认最多3方向；选定后每轮最多2次有依据的自主修正，再携对比与原因请用户决定。观察塑形、主次、视线、轮廓、阴影落点及材质身份；金属依靠环境反射形状，不把暗区一概补亮。固定相机、曝光、引擎、seed和采样做逐灯或参数对照，保存可编辑候选和明确差异。

Cycles和Eevee分别渲染、看图并记录差异。5.2官方文档给两者光链接接口，但存在细分限制，需目标案例验证；ShaderToRGB是Eevee路线、Toon BSDF是Cycles路线。NPR材质/合成需求在该次任务范围明确后协调现有工具，分别留照明与着色改动对照。

高级控光与已验差异查 [控光和引擎边界](references/advanced-controls.md)。特别注意：Eevee反光板的间接补光需要匹配场景的光照探针与烘焙，单开raytracing不能保证；板或灯变化后重新烘焙并保存。当前插件不自动创建/烘焙探针。Sky的Sun Disc仅Cycles，双引擎直接太阳用原生SUN，Sky显式sun_disc=false；Eevee World太阳提取是另一个机制。摄影/NPR诊断查 [照明判断](references/lighting-principles.md)。

快速预览通常768–1024px，正式静帧约2048px，画质按案例；外部资源声明SHA，缺失报告，不默默替换HDRI。基础灯具/常量World或程序化天空可不依赖外部HDRI。资源闭包、独立重开、真实解码与用户质量反馈各自记录。

交付可编辑blend、PNG、方案参数、精简报告和资源/恢复引用。计量公共调用、代理往返、机器墙钟及恢复成本；少调用不自动等于更快。本机四类代表案例、NPR与运动样本已有公开验收摘要；原案例认可不保证新场景质量。新增规模、运动域、引擎/平台等只在匹配实测证据齐备后声明通过，安装与公开发布遵循当前用户授权。
