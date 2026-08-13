# UX-SPEC-CHAIN-TOPIC-PANORAMA｜产业链全景图谱

> 版本：1.6-condition-task  
> 状态：ready_for_v1  
> 四件套版本：1.6-condition-task  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 变更：0 级产业 / 1 级链 / 可选数据截至；默认预跑秒开，改条件后开始分析套过程壳（`DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813`）。本页无查看报告。

## 1. 权威输入与边界

本 UX-SPEC 只深化同目录 IA、TRACE、USM、Wireframe，并遵守：

- 两份 P0 Bid：展示系统与专题服务系统 `1.1.1.2.4.2.2.1/.1/.2`；算法库 `1.1.1.1.1.1.1.2.15/.3.1`；
- `Design.md`、`UX-UE 通用交互组件规范.md`、`data-lineage-policy.md`；
- 全系统角色权限体系、权限点清单、架构基线；
- `cfg_metric-CHAIN-seed.yaml`、决策 Q056/Q062；
- TRACE `source_manifest` 中逐项 disposition。

边界：

- 不改变产品范围、不修改 Demo；既有页面只作后续偏差审计对象。
- 全景图谱默认预跑秒开；改条件后创建系统任务与报告，不把整页换成诊断过程向导。
- 算法 Bid 的输入、服务和输出用于页面数据合同；模板配置、人工导入、SDK、后台维护与导出按钮不进入本页。
- 无 URL 对象时系统补默认推荐产业 + 第一条可用 1 级链 + 最新数据截至（`source=default`）；分析对象只选产业；所属产业链再选 1 级链；数据截至可选择。用户清空后 `source=cleared` 保持空态。禁止打开对比篮作为换对象主路径；禁止对象 Modal。
- 门户产业总览和门户产业链全景不在本包修改。
- 权限沿用企业分析解释方式：产品角色与 L0–L4 persona 分离，服务端失败关闭；前端不从 Mock 用户推断敏感字段。

## 2. 四件套同步核对

| 核对项 | 产品结论 | UX 落点 | 结论 |
| --- | --- | --- | --- |
| 原始需求 | 展示 Bid 结构/下钻/演进 + 算法 Bid 全景模型/服务 | F-PAN-02/03 | 已补齐算法真源 |
| 对象入口 | 无 URL 对象→默认推荐产业+首条 1 级链秒开；分析对象只选产业；所属链再选；改条件走开始分析 | F-PAN-01/F-PAN-02 | `DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813` |
| 对比篮 | 可选分发进入，不创建任务；**不**承担本页换对象 | PAN-J02 | 已收窄 |
| 结构 | 完整正式链、稳定 LTR、服务返回关系 | F-PAN-02 | 已定义 |
| 深度下钻 | 产业链→复合环节子结构（可选/可递归）→叶子环节→微观实体/属性 | F-PAN-02/03 | Bid 直接需求，不以普通选中态或 Tab 切换替代 |
| 详情 | 关联企业/主流技术路线/市场规模三组 | F-PAN-03 | 严格对齐展示 Bid 叶子原文 |
| 市场规模 | `M_CHAIN_MARKET_SIZE` + Q056 | F-PAN-03 | 空值固定文案，不伪造 |
| 演进 | Q062 同 chain 固定快照、五类差异、Pending | F-PAN-02/03 | 不宣称实时 |
| readiness | 现有矩阵只适用门户总览 | §9 | 不复制 D1–D4 |
| 架构 | 前端→网关→Java→服务 | §10 | 不直连 Python/图数据库 |
| 响应式 | 1920/1680 Panel；1440 Drawer≥480 | §8 | 对齐 Design |
| 导航 | route 稳定选择全景图谱，保留产业总览 | 全局 | 不丢选中、不转技术链 |

## 3. 用户旅程与任务流

### PAN-J01｜直接进入并确认对象

1. 用户点击左侧“产业链全景图谱”，该项保持 selected。
2. 无 URL 有效对象且非 `source=cleared`：系统补默认推荐产业（与产业查询推荐目录同源），`replace` 写入 `object_type=industry&object_id=…&source=default`，直入工作区；**不**打开对比篮或 Modal。
3. F-PAN-01 页内 Select 预填该产业；旁显示 Tag「推荐示例」；轻提示「当前为推荐示例产业，可在分析对象中更换」；提示可关闭。所属产业链只读「按全链路展开，无需再选子链」。
4. 用户在 Select 确认其他 `industry` 或 `industry_chain` 后进入工作区：产业全链路、链单链；**无所属链二次确认步**；`source=select`。清空则空态 + 红校验，不写回默认。
5. 校验失败时保留对象身份与原因，错误贴近当前步骤并提供重试。
6. URL 已带有效对象且 `source≠default`（查询 / 篮分发 / Select）时，跳过推荐提示，直入加载。

### PAN-J02｜从对比篮发起（可选深链，非换对象）

1. 用户在系统篮的产业分组选中一个兼容对象并选择“产业链全景图谱”。
2. `industry` 与 `industry_chain` 均直接进入工作区；之后换对象改页内 Select，不必再回篮。
3. 前一弹层关闭后再进页，不出现双遮罩；不创建 `task_id`。

### PAN-J03｜浏览与下钻

1. 用户用结构控制、工具栏或结构列表阅读完整链。
2. click / Enter 选择节点，F-PAN-03 以 `chain_id + node_id + snapshot_id` 读取详情；复合环节返回 `child_nodes/child_edges` 时可继续下钻子结构，叶子环节进入三类详情。
3. 在关联企业、主流技术路线、市场规模三类分组查看有据主体和属性；切换分组只刷新详情 body。
4. “查看企业”在当前页打开共享企业画像抽屉；卡片、抽屉和企业对比篮共用企业主记录及稳定 ID。关闭不重载图谱，焦点回触发项。

### PAN-J04｜核对固定快照演进

1. 用户切换双快照或时间轴；先校验同一 chain 与 schema 兼容。
2. 系统按稳定空间基线显示五类差异并标 Pending。
3. 用户暂停、选择变化项，在详情查看前后快照和证据。
4. 不兼容、无变化或无证据时保留最近有效视图，不生成伪差异。

## 4. Frame 与承载映射

| Frame | 入口 | 宿主 | 出口 | 上下文保持 |
| --- | --- | --- | --- | --- |
| F-PAN-01 | 进页即见；换对象 | 页内 Select + 所属产业链只读 | 确认即加载 F-PAN-02；去产业查询 | 取消清空保留 `source=cleared` |
| F-PAN-02 | 默认推荐 / Select / 对比篮分发 / 产业查询确认后的 industry 或 chain | `/industry-center/panorama` | 节点到 F-PAN-03；Select 换对象 | URL、Select、`source`、服务请求对象一致 |
| F-PAN-03 | 节点/变化选择 | 1920/1680 Panel；1440 Drawer | 关闭回图谱；企业在当前页打开共享企业画像抽屉 | 错误与关闭不改变图谱坐标、时间状态、模式 |

跨模块：去产业查询携带 `return_context=panorama`；产业查询进全景仅带 `object_type/object_id`；共享企业画像抽屉接收 `enterprise_id/enterprise_code/source_chain_id/source_node_id`，且必须与卡片和企业篮同源；关闭不改变当前对象。

## 5. 交互与状态转换

### 5.1 对象入口（页内 Select）

| 触发 | 前置 | 结果 | 禁止 |
| --- | --- | --- | --- |
| 页面无 URL 对象且非 cleared | shell_ready | default_recommend_workspace（`source=default`） | 自动开篮、对象 Modal、静默不可更换默认、Skeleton 假链 |
| 在 Select 更换 | workspace | ready（全链路或单链）；`source=select` | 打开对比篮 / Modal |
| 清空 Select | workspace | no_object_shell（`source=cleared`） | 静默写回默认推荐 |
| 选 industry | object_list | ready（全链路） | 所属链二次确认、静默改写为默认 chain 身份 |
| 选 chain | object_list | ready | 丢失 parent industry |
| 篮分发 / 查询进入 | ready | workspace_loading；非 default | 本页再强制开篮 |
| 关闭推荐提示 | default_recommend_workspace | 同工作区，会话内不再显示提示条 | 清除当前对象 |
| 去产业查询 | workspace | search_redirect | 预置假对象冒充用户选择 |

默认推荐态必须可见「推荐示例」标识；更换路径是 Select，不是全局圆点。

### 5.2 图谱与节点

- 工作区外框使用 16px 内边距。
- 视口工具栏必须复用 `SharedMapChrome`，定位于图谱左上；页面不得自定义工具项、图标、文案或视觉样式。
- 时间状态标识位于工具栏下方 16px；演进图例定位于图谱左下并使用单列布局，五类变化分别使用不同系统语义色。
- Q062 状态入口为 ReviewMode 可聚焦按钮，click/Enter/Space 打开 Popover，内容固定包含开放项编号、缺口、当前处理、责任人和关闭条件；BusinessMode absent。
- BusinessMode 产品文案使用“数据截至 / 当前状态 / 状态对比 / 查看时间 / 基准时间 / 对比时间 / 演进时间轴”，不得出现“快照”或 schema 版本；底层 `snapshot_id/schema_version` 不改名。

| 操作 | 外围响应 | 内核响应 | 不改变 |
| --- | --- | --- | --- |
| 节点 click / Enter | 请求详情、同步标题 | 唯一高亮节点 | 主对象、快照、布局基线 |
| 边 hover | Tooltip 来源摘要 | 高亮边 | 选中节点 |
| zoom/pan | 更新视口状态 | 缩放/平移 | 业务数据与详情 |
| fit/reset | 恢复可读视野 | 重算视口 | 模式与 ContextBar |
| fullscreen | 保留工具栏、图例、退出 | 响应尺寸 | 焦点返回点 |
| 结构列表 | 停止播放、回到当前状态、隐藏演进控制和变化标识 | 与当前结构同一 selection | 主对象与详情分组 |

### 5.3 快照模式

- Segmented：当前状态（默认）/ 状态对比 / 演进时间轴。
- 双快照校验通过前保持当前单点；两个快照必须同 `chain_id` 且 schema 兼容。
- 时间轴位于图谱下方，提供播放、暂停、上一步、下一步；切换对象前先停止播放。顶部只保留模式与快照控制。
- 新快照不存在当前节点时，详情显示“该快照中不存在”，不自动换节点。
- `prefers-reduced-motion` 下禁用连续补间，改为步进。
- 结构列表不支持动态演进；进入后不保留状态对比或时间轴上下文，切回图谱后由当前状态重新开始。

### 5.4 详情与字段

- 二级 Tabs：关联企业 / 主流技术路线 / 市场规模，只刷新详情 body。主流技术路线使用路径卡表达“前置投入 → 技术/工艺步骤 → 产出/应用”，不以技术实体列表冒充。
- 下钻状态包含 `chain_id / node_id / snapshot_id / active_subject_group / active_entity_id?`；节点、时间或对象变化时校验身份，旧响应不得覆盖当前详情。
- 关闭企业实体抽屉后焦点返回原企业条目，并恢复原主体分组；关闭 1440 环节 Drawer 后焦点返回原图谱节点。两者都不得重置图谱坐标。
- 右侧详情布局和样式复用产业链总览；概要只出现一次。人才科研、服务供应只是算法模型的多源输入/可查主体范围，无独立展示需求时不生成本页 Tab。
- 关联企业卡仅由可解析的企业主记录生成；“查看企业”打开共享企业画像抽屉，不跳转空画像；加入企业篮复用同一 `enterprise_id/enterprise_code`。无法解析企业主记录时不显示虚构卡片或可点击详情入口。
- 复合环节仅在服务返回 `child_nodes/child_edges` 时显示“下钻内部结构”；返回上级恢复进入前的复合节点选中、高亮、详情和视口。
- 进入子结构后，下钻面包屑、子结构名称与“返回上一级”组成画布上方的独立行，与图谱/结构列表保持 16px 间距；禁止绝对定位覆盖内容。
- 左侧工作区外层只承担布局，不显示背景、边框或圆角；下钻路径行、实际图谱/结构列表和时间轴是直接子区域，实际内容只保留一层可见容器。
- 节点概要不重复列出上游环节、下游环节和证据来源；上下游由图谱/子结构表达，证据保留在关系详情与追溯层。摘要、下钻动作、属性区使用 16px 垂直间距。
- 环节状态在图谱、结构列表和详情中共用同一彩色映射：瓶颈关注为橙色、关键环节为蓝色、稳健环节为青色；断点单独使用红色虚线。结构列表状态 Tag 按文本自适应宽度，不撑满卡片。企业“在营”使用深青色、演进“新增”使用绿色，三者不得共用同一颜色。文本始终保留，不只依赖颜色。
- 演进状态条紧随详情面包屑，位于概要和分组列表之前；变化类型只在状态条显示一次，不在概要重复。该顺序不得因列表长度改变。
- 各分组独立 loading/empty/error，不让整 Drawer 闪烁。
- 市场规模宿主绑定 `M_CHAIN_MARKET_SIZE`；值为 null，固定显示“暂无正式数据源”，不得显示 0、Mock 数字或估算。
- 无权字段保留标签和原因，敏感值不进 DOM；服务端返回最终授权结果。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| 对象加载 | Select 目录；推荐示例态保留上下文与图谱 | 局部重试 |
| 对象校验失败 | 当前步骤 Error + 恢复确认按钮 | 修正后重试 |
| 图谱加载 | ContextBar/工具栏保留，固定高度 Skeleton | 原位替换 |
| 图谱空 | “当前产业链暂无正式结构” | 更换对象；无 Demo 链 |
| 图谱错误 | Result error + retry | 同请求重试 |
| 图谱无权 | 页面壳、对象、模式位置和申请/更换动作保留 | 不渲染节点摘要 |
| 详情加载/错误 | Drawer 先开，body Skeleton / Alert | 重试或换节点 |
| 分组无数据 | 分组局部 Empty | 切换其他分组 |
| 市场无源 | 字段空值文案 + Q056 评审追溯 | 等待正式源，不可手填 |
| 快照不兼容 | 日期控件就地错误 + Message | 保留最近单点并重选 |
| 范围无变化 | Info “该范围无已确认变化” | 调整快照 |
| 网络恢复 | 保留最近成功快照并标其时间 | 用户显式重试，不冒充最新 |

## 7. 组件、键盘与无障碍

| 场景 | 组件 | Keyboard / Focus | ARIA |
| --- | --- | --- | --- |
| 对象选择 | 页内 Arco Select（复用 `industryObjectSelect`）+ 只读所属产业链 | Select 可搜索；清空保持空态 | 分析对象 aria-label；错误关联尚未选择 |
| 模式 | Segmented / RadioGroup | 左右键切换；焦点不跳画布 | radiogroup / aria-checked |
| 工具栏 | 系统 `SharedMapChrome` | Tab、Enter/Space；全屏退出回原按钮 | 每个按钮动作型 aria-label |
| 图谱 | 专业图谱内核 + 可访问节点层 | 方向键同层移动、Enter 选中、Esc 清除 | 节点名称含阶段/状态 |
| 结构列表 | Arco Table/List | 键盘定位、Enter 同步选中 | 与图谱 selection 关联 |
| 详情 | Arco Drawer/Tabs/Descriptions/List | Drawer 标题首焦点；Esc 关闭回节点 | loading/error live region |
| 变化图例 / 状态 Tag | 系统图例容器 + 同源语义色 | 可聚焦、可切换高亮 | 新增绿、退出红、关系变化蓝、主体变化紫、技术替代橙；文本始终保留 |

- 自定义导航、Tab、图谱按钮均补 2px 主蓝 focus-visible。
- 变化不用颜色作为唯一编码；复杂图谱必须有结构列表替代路径。
- 无权 disabled 控件的原因可被键盘读取，但不可触发受限动作。

## 8. 响应式行为

| 宽度 | 布局 | 收缩 / 滚动 | 固定 |
| --- | --- | --- | --- |
| 1920 | Sidebar 200；控制 + 图谱 + 480–560 Panel | 页面不横滚；图谱内平移 | Header、Sidebar、ContextBar、工具栏 |
| 1680 | Sidebar 可展开；控制压缩；Panel 480 | 详情 body 滚动；对象名最多两行 | 同上 |
| 1440 | Sidebar 默认 64；控制可折叠；图谱全宽；详情 Drawer min 480 | Drawer 覆盖不重排坐标 | ContextBar、图谱工具栏 |

图谱与详情区域使用首屏剩余高度；时间轴模式下，图谱主动让出时间轴及其上方 16px 间距所需高度，保证时间轴位于首屏内。双状态图谱容器宽度小于 1100px 时自动切换为上下排列，恢复宽度后回到左右排列，不改变选择、时间状态或视口操作能力。

专题系统不提供 `<1440` 移动重排。任何宽度都不隐藏更换对象、快照、模式、退出全屏和 Drawer 关闭。长链不缩至不可读。

## 9. 内部评审投影

| Frame | mount_id | payload | 业务模式 |
| --- | --- | --- | --- |
| F-PAN-01 | `CHAIN-PAN-F01-OBJECT-MODAL-TITLE` | 页内 Select 产品解释与解耦决策 | absent |
| F-PAN-02 | `CHAIN-PAN-F02-PANORAMA-TITLE` | 展示 Bid + 算法 Bid + 当前落点 | absent |
| F-PAN-03 | `CHAIN-PAN-F03-EVOLUTION-TITLE` | 下钻/演进需求 + Q062 | absent |
| F-PAN-03 | `CHAIN-PAN-F03-MARKET-SIZE-PENDING` | `M_CHAIN_MARKET_SIZE` + Q056 | absent |

`cfg_metric-CHAIN-seed.yaml` 已登记指标语义；现有 readiness 矩阵仅适用 `CHAIN-PORTAL-OVERVIEW`，因此本专题 `metric_readiness_projection: []`，不自填或复制 D1–D4。市场规模挂点是开放项追溯，不伪装成 readiness 图标。

## 10. Demo 实施交接

建议页面包：

- `IndustryPanoramaPage`：路由、导航 key、F-PAN-01 页内 Select、Frame 编排；
- `industryObjectSelect`：与周期分析共用对象目录（无二次选链）；
- `PanoramaGraphCanvas`：图谱内核、可访问节点层、结构列表；
- `PanoramaNodeDetail`：Panel/Drawer 与三类直接要求详情；
- `PanoramaEvolutionControls`：固定快照、差异图例与 reduced motion；
- 共享依赖：`industryObjectSelect`、企业详情、Arco 基础组件、ReviewTrace。对比篮仅可选分发，不作为本页对象选择器。

状态模型至少包含：`entrySource/objectCandidate/resolvedChain/snapshotMode/baseSnapshot/compareSnapshot/selectedNode/viewport/detailState/permissionState/serviceEvidence`。

服务约束：

- 调用链为前端 → 网关 → Java 聚合 → `/topic/v1/{element}/graph|metrics|analysis`；
- 前端禁止直连 Python、MySQL、NebulaGraph 或在本地构建关系/差异；
- 正式 OpenAPI 未冻结前，V1 用固定可回放响应并显式 Pending；不宣称 production/live。

最小实施核对：无 URL 对象→推荐示例产业+首条 1 级链秒开且非开篮/非 Modal、页内 Select「请选择产业」、所属产业链 Select、数据截至 Select、改条件出「开始分析」套过程壳、本页无查看报告、清空不写回默认、查询「进入全景」直达、完整链不折叠、断点与瓶颈语义分离、三类直接要求详情、主流技术路线呈现为有向路径、Q056 空值、Q062 固定状态、16px 容器内边距、左上系统工具栏、左下五色中文图例、图谱下方时间轴、1440 Drawer≥480、导航稳定选中、业务模式无评审标识。

明确排除：静默不可更换的默认对象、任务过程、报告、导出、技术链跳转、门户总览改动、图谱编辑、企业子图、节点/关系/企业数量 KPI、复制门户 readiness。

## 11. 缺口与阻断项

| Gap | blocks_v1 | 阻断阶段 | V1 处理 | Owner / 关闭条件 |
| --- | --- | --- | --- | --- |
| `GAP-CHAIN-PANORAMA-APPROVAL` | false | pdr、v1_final、v2_lumen、production | 按本五件套确定性布局实现，不宣称冻结 | 郭万迎；补结构化批准 |
| `GAP-CHAIN-PANORAMA-READINESS` | false | pdr、v1_final、v2_lumen、production | Q056 空值；不设其他数量 KPI；不复制门户矩阵 | 何老师；建立本专题 D1–D4 行与正式市场源 |
| `GAP-CHAIN-PANORAMA-SNAPSHOT-API` | false | pdr、v1_final、v2_lumen、production | Q062 固定双快照、五类差异、Pending | 唐绍祖+徐滕强；冻结快照/差异 API |
| `GAP-CHAIN-PANORAMA-COMPARE-BASKET` | false | v1_final、v2_lumen、production | 本页 Select 换对象；篮仅可选分发 | 高颖；共享包冻结 |

上述缺口均有安全、确定且可见的 V1 处理，故不阻断 V1 高保真首轮；仍阻断所列后续阶段，不能据此宣称 PDR、V1-FINAL、V2 或生产就绪。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-PANORAMA
  version: "1.5-object-uncouple-basket"
  status: ready_for_v1
  source_four_pack:
    - IA-CHAIN-TOPIC-PANORAMA.md
    - TRACE-CHAIN-TOPIC-PANORAMA.yaml
    - USM-CHAIN-TOPIC-PANORAMA.md
    - Wireframe-CHAIN-TOPIC-PANORAMA.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  source_inventory_complete: true
  original_requirement_sources:
    - 展示Bid#1.1.1.2.4.2.2.1
    - 算法Bid#1.1.1.1.1.1.1.3.1
  permission_contract:
    product_role_is_not_permission_persona: true
    mock_user_permission_inference: prohibited
    final_authorization: server_fail_closed
    unauthorized_sensitive_value: do_not_render
  journeys:
    - {journey_id: PAN-J01-DIRECT, role: ROLE-PAN-PARK, story_refs: [US-CHAIN-PANORAMA-01], primary_flow: [open_menu, apply_default_recommend, show_recommend_hint, change_via_page_select, confirm_object, load_workspace], abnormal_flows: [default_unavailable_fallback, industry_no_published_chain, permission_denied, dismiss_hint, clear_select_empty]}
    - {journey_id: PAN-J02-BASKET, role: ROLE-PAN-GOV, story_refs: [US-CHAIN-PANORAMA-01, US-CHAIN-PANORAMA-02], primary_flow: [select_one_object, choose_panorama, load_workspace_fulllink_or_chain], abnormal_flows: [multiple_objects, invalid_object]}
    - {journey_id: PAN-J03-EXPLORE, role: ROLE-PAN-PARK, story_refs: [US-CHAIN-PANORAMA-02, US-CHAIN-PANORAMA-03], primary_flow: [read_full_chain, select_node, read_evidence, return_to_canvas], abnormal_flows: [graph_error, detail_error, sensitive_denied, market_source_missing]}
    - {journey_id: PAN-J04-EVOLUTION, role: ROLE-PAN-GOV, story_refs: [US-CHAIN-PANORAMA-04], primary_flow: [choose_fixed_snapshots, validate, inspect_change, read_evidence], abnormal_flows: [incompatible_snapshots, no_change, no_evidence]}
  frame_specs:
    - {frame_id: F-PAN-01, route_or_host: /industry-center/panorama#object-context, source_refs: [US-CHAIN-PANORAMA-01], states: [default, loading, empty, error, permission], interactions: [page_select, clear_keep_empty, go_to_search]}
    - {frame_id: F-PAN-02, route_or_host: /industry-center/panorama, source_refs: [US-CHAIN-PANORAMA-01, US-CHAIN-PANORAMA-02, US-CHAIN-PANORAMA-04], states: [default, default_recommend_workspace, loading, empty, error, permission, single, dual, timeline], interactions: [dismiss_recommend_hint, change_via_compare_basket, open_compare_basket, go_to_search, zoom, pan, fit, reset, fullscreen, select_node, structure_list, change_mode]}
    - {frame_id: F-PAN-03, route_or_host: /industry-center/panorama#detail, source_refs: [US-CHAIN-PANORAMA-03, US-CHAIN-PANORAMA-04], states: [default, loading, empty, error, permission, market_source_missing, incompatible_snapshot, no_change], interactions: [switch_detail_tab, retry, open_enterprise_drawer, close]}
  feedback_rules:
    - {trigger: direct_entry_without_object, response: apply_default_recommend_and_show_hint, recovery: change_via_compare_basket_or_go_to_search}
    - {trigger: industry_selected, response: full_link_expand_direct, recovery: change_object_if_no_published_chain}
    - {trigger: graph_load_failed, response: preserve_context_and_show_retry, recovery: retry_or_change_object}
    - {trigger: market_source_missing, response: show_empty_value_and_q056_copy, recovery: wait_for_registered_formal_source}
    - {trigger: incompatible_snapshots, response: retain_last_valid_single_view, recovery: choose_compatible_snapshots}
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, reduced_motion, alternative_structure_list]
  metric_readiness_projection: []
  metric_readiness_projection_reason: no_matrix_rows_applicable_to_CHAIN_TOPIC_PANORAMA
  review_mounts:
    - {mount_id: CHAIN-PAN-F01-OBJECT-MODAL-TITLE, frame_id: F-PAN-01, business_mode: absent}
    - {mount_id: CHAIN-PAN-F02-PANORAMA-TITLE, frame_id: F-PAN-02, business_mode: absent}
    - {mount_id: CHAIN-PAN-F03-EVOLUTION-TITLE, frame_id: F-PAN-03, business_mode: absent}
    - {mount_id: CHAIN-PAN-F03-MARKET-SIZE-PENDING, frame_id: F-PAN-03, business_mode: absent}
  gaps:
    - {id: GAP-CHAIN-PANORAMA-APPROVAL, summary: stable_layout_approval_provenance_incomplete, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_five_pack_contract, owner: "human:郭万迎", deadline: before_pdr, return_to: approval}
    - {id: GAP-CHAIN-PANORAMA-READINESS, summary: semantic_registry_exists_but_topic_readiness_rows_and_market_source_missing, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: q056_empty_and_no_other_numeric_kpis, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-PANORAMA-SNAPSHOT-API, summary: snapshot_and_diff_openapi_not_frozen, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: q062_fixed_replayable_snapshots_with_pending, owner: "human:唐绍祖+徐滕强", deadline: before_pdr, return_to: architecture}
    - {id: GAP-CHAIN-PANORAMA-COMPARE-BASKET, summary: shared_compare_basket_package_not_frozen, blocks_v1: false, blocks_stages: [v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_single_object_handoff, owner: "human:高颖", deadline: before_v1_final, return_to: architecture}
```
