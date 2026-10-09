# 控光、模板与双引擎边界

核验2026-10-09，本机Blender5.2.1 LTS/build9e2066aef7ef，当前支持Lighting Workflow0.2.1；原光学/四案例证据为0.2.0，补丁仅有单列的变换读取/迁移回归。原本机证据以 所选checkout的`docs/VALIDATION.md`公开验收摘要 为导航，私人原审计不随包分发。字段以公共 `lighting describe --schema` 为准，以下是选择与验收规则。

Area shape=RECTANGLE和size/size_y用于柔光箱/条光。normalize显式控制功率语义，spread_deg控制扩散范围；diffuse/specular_factor属于艺术分量控制，偏离真实摄影时说明。create支持原生参数；patch只支持合同列出的可合并字段，不能凭参数名猜patch支持。

receivers/blockers是对象名列表，receivers_mode/blockers_mode为INCLUDE或EXCLUDE。创建独立私有链接集合，清空数组取消对应链接。mode-only patch须先有非空集合。混合成员模式、外部消费者或集合结构变化拒绝；同字段手改按三方冲突处理。只点名一个blocker的INCLUDE也意味着其他对象不投该灯的阴影，不是“保留默认并加一个”。链接接收与阴影投射分别看图。

boards是受管实网格：reflector白面、flag黑面，位置/尺寸按目标bbox最长边归一，rotation_deg为世界欧拉角。板位置、颜色、粗糙度、尺寸和enabled可patch；拓扑/节点改造显式拒绝。Cycles真实多次反射可产生补光。Eevee无匹配烘焙探针的夹具中即使raytracing=true，白板ROI没有有效补光，记录为limited。加入原生VOLUME探针并分别对off/on状态烘焙后，同灯/曝光ROI从.003002到.081541；保存重开不再烘焙，像素差为0。该前置配置不是插件自动能力，也不是任意场景保证。黑flag阴影双引擎通过。

Sky使用显式sun_rotation_deg/sun_elevation_deg/sun_disc；scattering模型支持这些太阳参数，旧sky.rotation_deg无效并被拒绝。HDRI rotation_deg仍表示映射绕Z旋转。太阳盘与EeveeWorld.sun_threshold能量提取不同；需要native SUN为唯一直接太阳时，使用明确保存的sun_threshold=0输入并保留World，当前插件未公开该阈值控制。预设/模板不得默默把其他World设置恢复到默认。

HDRI声明绝对路径与SHA；packed导出为owned资源文件并核字节。不捆绑大型资源库。实验用128×64或64×32浮点EXR只证明方向/强度与持久性，不能当生产HDRI质量案例。

模板保存live位置/方向/尺寸、功率/色彩、板、链接模式与可表达World；不把旧recipe当手改后的实际方案。目标按source target索引映射，受管板按id重命名，其他名称要求bindings；别名冲突拒绝。normalize会拒绝未知字段和无法闭合的资源。scale_squared只显式缩放非SUN功率，遵守同形状、同距离比例的实验条件；迁移后仍检查相机和实际反射。

批量部分失败保留pass/fail与每项报告。恢复报告、源码和Blender运行身份变化会CONFLICT，候选SHA变化也拒绝。强制取消后的pending子报告必须是原批job/items/id/lighting-report.json；不存在尚未保存的检查点时重新提交源批次。不得手改报告SHA来伪装重验。

官方机制与本机RNA/像素验证范围见 所选checkout的`docs/VALIDATION.md`公开验收摘要。完整字段读取所选checkout的live describe及docs/cli/schemas；文档支持、技术验证、实际图像与用户反馈分开。原私人Wiki/审计不随包分发。
