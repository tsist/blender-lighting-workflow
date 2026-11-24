# 命令契约、Schema 与源码索引

本文件集中列出当前工作区灯光工作流的实时查询命令、JSON Schema 与源码位置，需要核对字段约束或排查行为时按路径直读。

## 实时目录与自省命令

```powershell
$ctl = './blenderctl.ps1'

# 查看当前宿主、发行号、支持状态与全部动作
& $ctl discover --product lighting
& $ctl discover --product lighting --actions

# 查看领域摘要、各动作完整 JSON Schema 与分节字段
& $ctl lighting describe
& $ctl lighting describe --operation manifest --schema
& $ctl lighting describe --operation template --schema
& $ctl lighting describe --operation target --schema
& $ctl lighting describe --operation batch --schema
& $ctl lighting describe --section lights
& $ctl lighting describe --section world
& $ctl lighting describe --section patches
& $ctl lighting describe --section boards

# 查看各子命令参数帮助
& $ctl lighting --help
& $ctl lighting inspect --help
& $ctl lighting run --help
& $ctl lighting template-save --help
& $ctl lighting template-edit --help
& $ctl lighting batch --help
& $ctl lighting rig-handoff --help
```

## JSON Schema 文件

- **布光清单（create / patch / restore）**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-manifest.schema.json`
- **检查请求**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-inspect-request.schema.json`
- **运行请求**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-run-request.schema.json`
- **模板结构**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-template.schema.json`
- **模板保存请求**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-template-save-request.schema.json`
- **模板修订请求**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-template-edit-request.schema.json`
- **跨镜目标映射**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-target.schema.json`
- **批量请求**：`<PROJECT_ROOT>/docs/cli/schemas/lighting-batch-request.schema.json`

## 通用 CLI 文档

- **安装与快速开始**：`<PROJECT_ROOT>/docs/cli/安装与快速开始.md`
- **公共命令总契约**：`<PROJECT_ROOT>/docs/cli/命令契约.md`
- **通用请求总 Schema**：`<PROJECT_ROOT>/docs/cli/schemas/request.schema.json`

## 插件与 CLI 实现位置

- **Lighting Workflow 插件源码**：
  - `tools/lighting_workflow_addon/contract.py`（核心字段与校验规则）
  - `tools/lighting_workflow_addon/core.py`（创建、补丁、检查与还原逻辑）
  - `tools/lighting_workflow_addon/advanced.py`（光链接、控光板与世界环境处理）
  - `tools/lighting_workflow_addon/templates.py`（实际状态导出、修订与实例化迁移）
  - `tools/lighting_workflow_addon/ui.py`（面板与内嵌快照操作）
- **公共 CLI 封装与验证**：
  - `tools/blenderctl/lighting_interface.py`（CLI 子命令入口与参数解析）
  - `tools/blenderctl/lighting_workflow_contract.py`（请求归一化与合同检查）
  - `tools/blenderctl/lighting_workflow.py`（工作单元执行、资源闭环与双引擎预览）
  - `tools/blenderctl/lighting_batch.py`（有界批量与断点续跑）
  - `tools/blenderctl/lighting_verifier.py`（独立进程冷重开验证器）
