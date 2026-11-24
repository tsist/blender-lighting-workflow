# 高级控光与双引擎对策

本手册汇总 Lighting Workflow 的高阶控光参数、双引擎实测差异、`lighting rig-handoff` 现场灯组交接以及模板批量迁移做法。需要核对完整字段与取值范围时，运行 `& './blenderctl.ps1' lighting describe --operation <动作> --schema` 实时查阅。

## 原生灯具参数与补丁字段

创建灯组（`action: "create"`）支持全套原生灯光参数，微调（`action: "patch"`）对应 `lighting describe --section patches` 列出的可合并字段：

- **柔光箱与条光**：选 `type: "AREA"` 配 `shape: "RECTANGLE"`，通过 `size` 和 `size_y` 拉出长条高光或大面柔光。
- **光束收拢与功率语义**：用 `spread_deg` 收窄面光扩散角，用 `normalize` 显式开关面积归一化功率。
- **分量调节**：`diffuse_factor` 与 `specular_factor` 用于艺术化控制漫反射与高光比例；调离默认值时在交付说明里标明意图。
- **聚光与太阳**：`SPOT` 用 `spot_size_deg` 和 `spot_blend` 控光锥与羽化；`SUN` 用 `angle_deg` 控太阳角直径与阴影软硬。

修改前先跑 `lighting inspect` 读最新快照。与手调互不重叠的字段会自动保留；同一字段若存在手调差异，先读报告中的 `conflict` 提示，确认后再通过 `conflict: "overwrite"` 或保留手调推进。

## 照明链接与阴影链接

通过灯具字段 `receivers` / `blockers`（对象名数组）与 `receivers_mode` / `blockers_mode`（`INCLUDE` 或 `EXCLUDE`），可以精准指定某盏灯照亮谁、谁投下它的阴影：

- 插件会为受管灯具创建独立的私有链接集合；把对象数组清空即可解除对应链接。
- 单独修改 `receivers_mode` 或 `blockers_mode` 时，先确保对应对象列表已有成员。
- **留意 `INCLUDE` 的语义**：在 `blockers` 里设 `INCLUDE` 并填入一个对象时，表示只有该对象投射此灯阴影，场景里其余对象同步退出投射范围。每次改完光链接或阴影链接，都出图分别核对受光面和投影。
- 保持链接集合的归属干净；若外部集合结构或混合成员被手动改乱，先在源工程理清归属再重新提交。

## 受管反光板与黑遮光板

在清单的 `boards` 中声明实网格控光板，支持白板（`kind: "reflector"`）和黑旗（`kind: "flag"`）：

- `location` 和 `size` 按目标边界框最长边归一，`rotation_deg` 采用世界欧拉角。
- 后续可用 `board_patches` 微调位置、旋转、尺寸、颜色、粗糙度和开关（`enabled`），保持原有板面网格与材质节点完整。
- **双引擎表现差异**：
  - **黑遮光板（`flag`）**：在 Cycles 与 EEVEE Next 下均可直接遮挡光线、切出干净阴影。
  - **白色反光板（`reflector`）**：Cycles 依靠多次光线弹射直接形成自然补光。EEVEE Next 下单靠打开光追（`use_raytracing: true`）还出不来有效漫反射补光，需要提前在场景中配置原生 `VOLUME` 光照探针并完成烘焙；每次挪动灯具或反光板后重新烘焙并保存工程，冷重开后补光效果就会稳定保持。

## 天空与环境 HDRI

通过清单里的 `world` 配置环境照明：

- **常量环境（`constant`）**：配 `color` 和 `strength`，适合干净棚拍与零外部依赖的快速预览。
- **程序天空（`sky`）**：显式填写 `sky_type`、`sun_rotation_deg`、`sun_elevation_deg` 和 `sun_disc`。Cycles 支持程序天空自带的日轮显示；为了在 Cycles 与 EEVEE Next 下获得一致的太阳方向与直射光，将 `sun_disc` 设为 `false`，另配一盏原生 `SUN` 负责直射太阳。若需屏蔽 EEVEE World 的太阳提取影响，请在输入源工程中把 World 的 `sun_threshold` 明确设为 `0` 并使用 `adapt` 模式保留该 World。
- **环境贴图（`hdri`）**：填写 `file`、`strength` 和绕 Z 轴旋转的 `rotation_deg`，同时把该 HDRI 的绝对路径与 SHA256 写进请求的 `resources` 数组。已打包进工程的外部资源会按受管资源核验字节；生产静帧一律使用完整动态范围的正式 HDRI。

## 使用 `lighting rig-handoff` 接续已存灯组

当需要在已保存工作副本上直接复用插件面板操作（无需整套重写清单）时，调用 `blenderctl.ps1 lighting rig-handoff --params <参数JSON> --output <新工程路径>`：

1. 先运行 `blenderctl.ps1 discover --product lighting` 获取当前已验的 `edition` 值，连同 `file`、`expected_sha256`、`context`（`scene`、`view_layer`、`frame`）、`rig_id` 和可选 `resources` 写入参数 JSON。
2. 按需选择六项操作之一：
   - `choose-rig`：切换当前场景的活动受管灯组。
   - `choose-light`：传入 `light_id`，在指定视图层物体模式下选中该单灯并设为活动对象。
   - `select-group`：在指定视图层选中整个受管灯组，方便进窗口后批量互动微调。
   - `edit-light`：传入 `light_id` 与 `values`（可含 `shape`、`angle_deg`、`hide_render`、`hide_viewport`），直接改写灯具属性。
   - `save-snapshot`：把当前灯组实际状态写入工程内嵌的文本数据块（`LW_Snapshot_*`）。
   - `read-snapshot`：传入准确的文本块名，独立只读取出快照内容（此操作无需 `--output`）。

除 `read-snapshot` 外，其余操作都会把结果写到 `--output` 指定的新绝对路径 `.blend`，原工程保持不变。

## 模板保存、修订与跨镜迁移

主镜布光验收通过后，用模板把实际灯光状态沉淀下来，快速铺到同场景的其余镜头：

- **保存模板（`lighting template-save`）**：读取保存工程中真实的灯具位置、朝向、尺寸、功率、色彩、控光板、光链接和可表达的 World 状态，导出新的版本化模板文件。遇到手调拆开了视口与渲染显隐，或改了自定义节点与灯具滚转角时，先在工作副本上把灯具理顺为模板可表达状态再导出。
- **修订模板（`lighting template-edit`）**：通过 `edits.content` 提交完整模板 JSON，并填入严格递增的 `revision`。工具会记录 `parent_sha256` 并写出新文件，旧版模板完整留存。
- **迁移套用（`lighting run --template ... --target ...`）**：与 `--manifest` 二选一。在 `target` JSON 里指定新场景、视图层、新 `rig_id`、新目标对象列表 `targets`、`mode`、`anchor` 与 `power_policy`：
  - 目标对象按索引顺序映射，受管控光板按 `id` 自动对应，其余出现在光链接里的外部对象通过 `bindings` 一一映射并避免别名冲突。
  - `power_policy: "native"` 保持原瓦数；`power_policy: "scale_squared"` 按新旧目标尺寸比的平方缩放非 `SUN` 灯具功率（`SUN` 功率不变），适合同形体、同距离比例的跨尺度复用。套用后仍需按新相机出图检查反射与暗部。

## 批量执行与断点续跑

使用 `lighting batch --manifest <批量清单>` 顺序渲染多个镜头或灯光方案：

- 单批支持 1 至 8 项，全批预览图合计上限 24 张，顺序执行并逐项存盘独立候选与报告。
- 部分条目失败时，整批返回失败退出码，同时保留已成功条目的候选文件与报告。
- 需要断点续跑时，先确认原作业已彻底进入终态，再把原批量报告路径与 SHA256 填进 `--resume` 与 `--resume-sha256` 重新提交。工具会核对源码、运行环境、请求签名、原保存预期与候选 SHA256；成功项经独立重开和图片 SHA256 复验后直接复用，失败或未完成项从原安全检查点继续。若原工程或候选文件已被外部改动，直接从干净源工程重新提交新批次。
