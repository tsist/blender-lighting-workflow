# 当前范围与证据

公开包基线：Lighting Workflow0.2.1、匹配CLI0.57.0、打光技能0.2.0。原本机验证使用Windows、Blender5.2.1 LTS/build9e2066aef7ef；其他版本/平台须分别实测。插件补丁修复禁用受管对象冷重开的检查/模板变换读取；CLI/Schema、艺术规范和目录架构保持，路径与证据导航为公开适配。

先设置BLENDERCTL_ROOT为明确匹配checkout，实际入口为该checkout的blenderctl.ps1；执行显式全局--blender与独立--jobs-dir。插件来源在checkout的tools/lighting_workflow_addon，host合同为tools/blenderctl/lighting_workflow_contract.py和lighting_interface.py。公共说明见 所选checkout的`docs/USAGE.md`、`docs/VALIDATION.md`、`docs/SKILLS.md`。不从独立安装的技能目录猜CLI位置。

saved-file create/patch/restore、原生灯/World、可选地板、三锚定、双引擎预览、原生控光、受管板与链接、版本化实际状态模板、跨工程有界批量已在本机对应范围验证。一个Scene一个活动方案。GUI布局/选方案与共享后台operator已验；原生参数编辑/Text快照/恢复全部鼠标交互未跑，Text检查快照不保证可重放manifest。

本机15项core、21项template加别名/边界检查、51项只读交叉审核和独立公共技能执行通过。official quick_validate因现有解释器缺PyYAML记not_run；基本结构/链接/字节校验和实际技能演练分别记录，不冒充官方校验器通过。历史实现身份与最终身份分列，不用新SHA替旧证据改名。

0.2.1共用rigid reader从persisted basis/parentinverse/evaluated parent读实际刚体变换，无可见性切换副作用；不支持的对象自身约束/Action/physics/curve parenting拒绝。三锚定1/8/16帧、禁用对象迁移/独立重开和15core/21template补丁回归通过。补丁实现身份6736923e…与四案例/24运动图原0.2.0身份3864a989…分开，未声称原正式图已按补丁重渲。

原用户确认产品中性及新增角色/室内/室外预览方向达到及格；正式四类共8PNG、5编辑工程，主线程看图，不能声称用户逐张确认正式像素。运动有24图与1/8/16帧锚定/非目标独立验证，非完整连续视频/复杂动画保证。公开摘要不捆用户资产、私有blend、原图和原审计JSON。

Eevee反光补光有明确VOLUME探针/匹配烘焙前置，插件不自动创建/烘焙/重烘焙；单有板对象不证明贡献。Sky原生日轮为Cycles-only，NPR采用引擎专用材质输入，照明工具随后保护。详细边界查 [advanced-controls](advanced-controls.md)。旧M1工程仍可编辑/恢复，缺原saved_expectation的旧恢复报告要从源重新运行。

本机代表案例不包含完整角色绑定、灯光动画编排、IES/Gobo、体积雾、任意资产/缓存、跨平台或固定提速承诺。私人访谈、WM和Wiki不公开，也不继承原用户对新任务的授权。宿主有自己的知识库时回读实际原文与适用范围；能力缺失不臆称检索或写入。新结论使用当前项目已有知识/审计流程，不在技能目录另建长期知识库。
