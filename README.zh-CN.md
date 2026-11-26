# Lighting Workflow 打光工作流

[English](README.md)

通过可审查的保存文件 CLI 工作单元，创建、编辑、检查和恢复可编辑的 Blender 灯光方案。

**灯光插件 0.3.0、Blender 5.3.0、打光技能 1.1.0，GPL-3.0-or-later。** 按主体曝光、背景保护、主辅光比和画面亮度协调调灯。配合独立的 blenderctl v0.64.0 分发及生产包 1.0.0，参见[生产请求示例](docs/GOAL-LIGHTING.md)。

此前版本的受管灯组验收见[发布说明](docs/RELEASE_NOTES.md)。

## 功能和边界

- 受管原生灯、柔光箱/条光、常量/HDRI/天空World、反光/遮光板、照明接收与阴影投射INCLUDE/EXCLUDE链接。
- create/patch/restore、源/材质/已有相机保护、字段手改冲突、独立候选和第二进程重开。
- 导出当前实际状态的版本模板，显式对象绑定、目标尺寸适配、native或scale_squared功率策略；SUN不随目标尺寸平方缩放。
- 有界顺序批量、逐项结果、部分失败、取消检查点和带SHA/源码/运行身份约束的恢复。
- 世界/目标/相机锚定，多相机与简单运动采样；精简Blender面板提供受管方案管理和原生参数编辑。

本机代表输入覆盖产品、卡通/NPR角色、室内、室外，分别验证Cycles/Eevee。技术验证、主线程看图和用户反馈各自记录，不能相互替代，详见[验收范围](docs/VALIDATION.md)。

**Eevee反光板间接补光须明确配置VOLUME探针并按场景烘焙，插件不会自动创建/烘焙/重烘焙。** 已验夹具中只打开raytracing没有有效补光。Sky原生日轮仅Cycles。NPR使用引擎专用材质输入，打光插件随后保护它们。

## 安装与入口

在 Blender 的 **Preferences → Extensions → Install from Disk** 安装 0.3.0 插件 ZIP，随后启用 Lighting Workflow。SHA-256 随版本发布。

本仓随附 CLI 快照 0.57.0，服务以下受管灯组命令。另需Python **3.12+**与Blender；本仓不捆绑二进制。保留原`tools/`目录和全部runtime Python模块的原字节，以保持打光实现身份；其他CLI领域仍有各自依赖和契约，不因随源码打包就变成本发布已验范围。

从checkout运行PowerShell：

```powershell
$env:BLENDERCTL_ROOT = (Get-Location).Path
$env:BLENDER_PATH = '<实际blender.exe绝对路径>'
$env:BLENDERCTL_PYTHON = '<实际python.exe绝对路径>'
./blenderctl.ps1 --version
./blenderctl.ps1 lighting describe
./blenderctl.ps1 lighting describe --operation run --schema
./blenderctl.ps1 --blender $env:BLENDER_PATH --jobs-dir (Join-Path $env:BLENDERCTL_ROOT 'runtime/lighting-jobs') --timeout 900 --compact request '<请求JSON绝对路径>'
```

`BLENDERCTL_ROOT`标识选择的checkout，调用该checkout的launcher；它不是隐式切换任意CLI版本的授权。原portable布局之外显式提供 **`--blender`**。全局参数在子命令前，输入为绝对路径和真实SHA；最终读取`ok/error`、逐项状态、保护、重开和实际渲染报告，磁盘完整报告是权威。

五个执行入口为`lighting.run/inspect/template-save/template-edit/batch`。详见[用法与JSON示例](docs/USAGE.md)、[技能安装](docs/SKILLS.md)及实时describe。安装技能后由宿主在下一轮/目录刷新时发现；技能不会安装Blender或自动配置CLI。

## 公开内容

本仓公开插件/runtime源码、Schema、可移植技能说明和发布工具。不公开用户生产资产、私有`.blend`、原案例PNG、原审计JSON、个人配置、WM或私人Wiki。

公开说明摘要来自有边界的本机验证，不代表公开CI已运行Blender或Linux验收。0.3.0 的画面目标用 Cycles CPU 测量，详见[发布说明](docs/RELEASE_NOTES.md)及[许可范围](docs/LICENSING.md)。
