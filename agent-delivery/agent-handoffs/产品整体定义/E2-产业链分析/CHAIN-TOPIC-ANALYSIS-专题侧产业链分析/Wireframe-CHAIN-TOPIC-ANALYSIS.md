# Wireframe-CHAIN-TOPIC-ANALYSIS

> **2026-08-04 能力拆分通知**：`F-CHAIN-02/03` 仅保留历史溯源；全景图谱结构、对象 Modal、响应式与挂点以 `../CHAIN-TOPIC-PANORAMA-产业链全景图谱/Wireframe-CHAIN-TOPIC-PANORAMA.md` 为唯一实施基线。  
> **2026-08-05 能力拆分通知**：`F-CHAIN-07/08` 仅保留历史溯源；区域产业评价结构、挂点与状态以 `../CHAIN-TOPIC-REGIONAL-区域产业评价/Wireframe-CHAIN-TOPIC-REGIONAL.md`（`F-REG-01~04`）为唯一实施基线。  
> **2026-08-05 能力拆分通知（续）**：`F-CHAIN-09/10` 仅保留历史溯源；深圳产业决策结构、挂点与状态以 `../CHAIN-TOPIC-SHENZHEN-深圳产业决策/Wireframe-CHAIN-TOPIC-SHENZHEN.md`（`F-SZ-01~04`）为唯一实施基线。  
> **2026-08-05 能力拆分通知**：`F-CHAIN-04/05/06` 仅保留历史溯源；产业运行诊断结构、挂点与状态以 `../CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/Wireframe-CHAIN-TOPIC-DIAGNOSIS.md`（`F-DIAG-01~05`）为唯一实施基线。

> **模块**：E2 / CHAIN-TOPIC-ANALYSIS · 专题侧产业链分析  
> **版本**：v0.6-core-package  
> **状态**：核心产品包 Wireframe 已完成；`core_package_ready: true`、`ready_for_ux: true`、`ready_for_v1: true`；允许进入 V1 高保真首轮，但不代表 PDR/Gate、任务或部署状态  
> **对应 IA**：`IA-CHAIN-TOPIC-ANALYSIS.md`  
> **对应 USM / TRACE**：`USM-CHAIN-TOPIC-ANALYSIS.md` / `TRACE-CHAIN-TOPIC-ANALYSIS.yaml`  
> **轨道 / 屏幕**：`Track-MS` / `medium_1440_1920`

## 0. 使用边界

- 本文定义专题侧 12 个 Frame 的结构、字段、交互、状态、禁止行为和评审挂载；不修改门户产业总览。
- 七项计算型分析均按“对象与配置 → 生成分析 → 可视化分析过程 → 显式查看结果 → 不可变结果 → 生成报告”统一交互，同时按“配置故事 → 共享任务故事 → 结果故事 → 可选报告故事”分离生命周期。
- 统计字段的正式 `M_CHAIN_*` 尚未建立专题真源。本文使用 `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` 明确占位，绝不把 gap ID 当成 metric_id，也不发明口径、公式、数据源或 D1～D4 状态。
- `DEC-D9-DATA-HEALTH-GROUPING-20260803` 已关闭 marker overflow：入口固定为 D1、`DataHealthBadge(D2+D3)`、D4 三组；`DataHealthBadge` Popover 分别保留 D2「结构」和 D3「源映射」两行。

## 1. 页面 / Frame 清单

| Frame | 入口 / 路由 | 目的 | TRACE / Stories |
| --- | --- | --- | --- |
| `F-CHAIN-01` 产业查询与对象摘要 | `/industry-center/search?mode=smart\|industry\|advanced` | 发现产业/产业链并同类型入篮 | `US-CHAIN-TOPIC-01` |
| `F-CHAIN-02` 产业链全景图谱 | `/industry-center/panorama` | 看清完整链条结构 | `REQ-CHAIN-TOPIC-01`；`US-02/03` |
| `F-CHAIN-03` 全景节点详情与演进 | 同上，页内右栏 / 对比状态 | 下钻节点并核对动态变化 | `REQ-CHAIN-TOPIC-01`；`US-02/03` |
| `F-CHAIN-04` 产业周期配置与结果 | `/industry-center/diagnosis?tab=cycle` | 提交周期分析并阅读结果 | `REQ-CHAIN-TOPIC-02`；`US-04/05` |
| `F-CHAIN-05` 关键环节配置与结果 | `/industry-center/diagnosis?tab=key-link` | 提交关键环节识别并阅读结果 | `REQ-CHAIN-TOPIC-04`；`US-06/07` |
| `F-CHAIN-06` 瓶颈堵点配置与结果 | `/industry-center/diagnosis?tab=bottleneck` | 提交瓶颈识别并阅读归因 | `REQ-CHAIN-TOPIC-05`；`US-08/09` |
| `F-CHAIN-07` 区域产业指数配置与结果 | `/industry-center/regional?tab=index` | 配置指数并比较优势短板 | `REQ-CHAIN-TOPIC-03`；`US-10/11` |
| `F-CHAIN-08` 区域竞争力配置与结果 | `/industry-center/regional?tab=competitiveness` | 配置三维评价并阅读排名 | `REQ-CHAIN-TOPIC-08`；`US-12/13` |
| `F-CHAIN-09` 深圳产业对比配置与结果 | `/industry-center/shenzhen?tab=comparison` | 配置深圳对标并阅读阶段判断 | `REQ-CHAIN-TOPIC-06`；`US-14/15` |
| `F-CHAIN-10` 深圳产业发展配置与结果 | `/industry-center/shenzhen?tab=development` | 基于结构化对比结果生成建议与路径 | `REQ-CHAIN-TOPIC-07`；`US-16/17` |
| `F-CHAIN-11` 统一可视化分析过程与分析记录 | `/industry-center/tasks/:taskId`；各工作空间 `tab=records` | 查看阶段过程、恢复任务、撤回 queued 任务和复用历史配置 | `US-18/19` |
| `F-CHAIN-12` 报告入口与阅读交接 | `/industry-center/reports/:reportId` | 从有效结果进入同源报告 | `US-20` |

## 2. 统一页面骨架与状态机

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Header 64px：系统身份 / 当前模块 / 系统任务浮层                      │
├──────────────┬───────────────────────────────────────────────────────┤
│ Sidebar 200px│ ContextBar：页面 / Tab / 对象 / 草稿或任务身份         │
│ 战略分析     ├───────────────────────────────────────────────────────┤
│ 产业链分析   │ 主工作区：对象空态 / 配置 / 过程 / 结果 / 记录         │
│              │                                                       │
│              ├───────────────────────────────────────────────────────┤
│              │ 页内主动作：生成分析 / 查看结果 / 生成报告            │
└──────────────┴───────────────────────────────────────────────────────┘
```

七项计算型分析统一状态：

```text
object_empty → draft → validating → created → prechecking → queued → running
                                      └──────────────→ failed / terminated
queued → withdrawn
running → succeeded --点击查看结果→ result_available → result_readonly --点击生成报告→ report_handoff
```

- `queued`：发起人可二次确认撤回，成功后进入 `withdrawn`、释放同类互斥、不生成结果。
- `running`：普通用户无取消入口；即使直接调用取消也必须由服务端拒绝。离页不终止任务。
- `succeeded`：不自动跳结果，用户显式点击“查看结果”。结果绑定不可变快照。
- `failed / terminated / withdrawn`：不得原位重跑；只可复制配置形成新草稿和新 `task_id`。

### 2.1 企业评估交互壳层复用合同

当前企业评估实现仅作为交互与实现参考，产业链七项分析复用以下页面模式和插槽合同：

```text
ConfigView
  对象摘要 + 分析专属配置 + 校验反馈 + [生成分析]
      ↓ 创建 task_id
ProcessingView
  任务摘要 + StageSteps + CurrentStageAlert + 后台继续/恢复说明
      ↓ succeeded 后 [查看结果]
ResultView
  结果身份 + 分析专属结果内容 + [生成报告]
```

| 壳层插槽 / 状态 | 七项分析的统一规则 | 领域差异来源 |
| --- | --- | --- |
| `task_summary` | `task_id`、分析类型、对象摘要、状态、队列位置或已用时间 | 共享任务真源 + 当前配置快照 |
| `stage_steps` | 展示已完成 / 进行中 / 等待 / 失败 / 完成，不显示虚构百分比 | 当前 `analysis_type.stage_definitions` |
| `current_stage_alert` | 说明当前阶段、后台继续、离页恢复或失败处理 | 共享状态 + 当前阶段文案 |
| `result_action` | 仅 succeeded 启用“查看结果”，不自动跳转 | 当前任务 `result_route/result_id` |
| `result_content` | 只读、不可变，并展示对象/配置/模型/数据/生成时间身份 | `F-CHAIN-04`～`10` 各自结果区 |
| `report_action` | 仅成功且有效结果显示“生成报告” | `F-CHAIN-12` 报告交接合同 |

必须按分析类型注册：`analysis_type`、对象与配置摘要、`stage_definitions`、结果路由、结果内容槽位、报告类型。禁止复制企业评估的企业字段、指标权重、六个企业阶段文案、雷达/排名/得分图表及报告章节；禁止以单一 Spinner 代替过程可视化，禁止完成后自动跳转结果。

## 3. F-CHAIN-01 产业查询与对象摘要

### 3.1 线框图

```text
┌─ 产业查询主页面 ────────────────────────────────────────────────────┐
│ [智能检索] [查产业] [高级筛选→]                                    │
│ 关键词查询区                                                       │
│ 已匹配关键词：[字段：值 ×] [字段：值 ×]                            │
│ 示例查询 · 热门产业→                                              │
├────────────────────────────────────────────────────────────────────┤
│ 最近检索：[当前模式·条件 1] [当前模式·条件 2]              [清除] │
├────────────────────────────────────────────────────────────────────┤
│ 未执行条件：[推荐产业] · 推荐理由                                  │
│   [查看摘要] [进入全景图谱] [加入对比篮]                            │
│ 执行条件后：[检索结果]                                              │
│ □ 产业/产业链横向卡片 · 类型 · 父级产业 · 摘要 · 可用性            │
│   [查看摘要] [进入全景图谱] [加入对比篮]                            │
│ □ …                                         [全选本页] [加入对比篮] │
└────────────────────────────────────────────────────────────────────┘
             │ 高级筛选 / 热门产业（携带 preset）
             ▼
┌─ 产业查询 / 高级筛选 ──────────────────────────────────────────────┐
│ 高级筛选 · 字段库                                                  │
│ AND/OR · 父级产业等产业字段条件 · 个人查询方案                     │
│ [添加条件] [清空条件]                              [应用筛选]      │
└────────────────────────────────────────────────────────────────────┘
                              ┌─ 对象摘要抽屉 ───────────────────────┐
                              │ 身份 / 摘要 / 来源 / 可进入的页面    │
                              │ [关闭] [加入对比篮] [进入全景图谱]   │
                              └──────────────────────────────────────┘
```

### 3.2 字段与指标

| 区块 / 字段 | 类型 | 来源 | 必填 | 默认 / 联动 | metric_id / gap |
| --- | --- | --- | --- | --- | --- |
| `object_type` | enum | 产业检索服务 | 是 | 仅 `industry` / `industry_chain` | — |
| `industry_id / chain_id` | stable id | 产业检索服务 | 是 | 不用名称代替身份 | — |
| `parent_industry_id` | id | 产业检索服务 | 产业链必填 | 入篮时保留 | — |
| 对象名称、摘要、来源 | string | 产业检索服务 | 是 | 权限撤回时隐藏敏感摘要 | — |
| `permission_state` | enum | 统一权限服务 / V1 确定性权限夹具 | 是 | `allowed / permission_locked`；锁态只消费结果，不由页面计算 L0～L4 | `GAP-CHAIN-TOPIC-PERMISSIONS` |
| `availability_state` | enum | 产业目录 / 数据服务 | 是 | `available / unavailable`；不得与权限状态合并 | — |
| 结果总数 | int | 聚合服务 | 否 | 未有正式口径前不作为业务 KPI | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 推荐理由 | string | 确定性 V1 推荐合同 | 推荐态必填 | 仅未执行查询时显示；不声明实时排序 | — |

### 3.3 交互与状态

| 触发 / 状态 | 页面行为 | 禁止行为 / 下一步 |
| --- | --- | --- |
| F-01 可见页头 | “产业查询”标题和说明整体仅评审态显示；业务态折叠该行并直接进入查询主区 | 不把评审说明作为业务文案，不影响查询字段、操作、结果或权限 |
| 智能检索提交 | 在搜索框正下方显示“已匹配关键词”与字段化可关闭 Tag；结果按全部当前 Tag 匹配 | 不把匹配关键词、匹配字段或匹配说明重复放在结果卡上 |
| 移除匹配关键词 | 删除所点 Tag，保留输入文本与其他 Tag，并立即按剩余关键词重算结果 | 不清空其他关键词，不要求重新点击检索；全部移除后按企业查询同类降级语义显示多字段关键词提示 |
| 点击“高级筛选” | 导航到 `/industry-center/search?mode=advanced` 的独立高筛页面并显示返回“产业查询”的面包屑；复用企业高筛的左侧内置字段库、右侧条件区、字段搜索、推荐标识、展开/收起、AND/OR、查询方案和应用/编辑结果交互 | 不在蓝色查询主视觉内展开条件编辑器，不自动执行查询；只复用结构与组件，不继承企业字段 |
| 最近检索 | 固定在普通检索条件与推荐/结果之间；有效执行后按当前模式显示记录，点击即恢复并重跑；按标题去重，最多 10 条，可清除 | 示例查询只预填、热门产业只跳转并预置条件，未执行或未应用时不写入记录；不跨模式混显 |
| 点击“热门产业” | 导航到同一高筛页面，URL 携带稳定 `preset`，字段库预置对应 `parent_industry_id` 条件 | 不把热门项当关键词直接检索；不在用户点击“应用筛选”前生成结果 |
| 推荐态 | 不显示复选框与批量工具栏；每张推荐卡支持查看摘要、进入全景图谱、单卡加入对比篮 | 不把推荐对象伪装成已执行检索结果，不在推荐态触发类型锁定；不提供去门户总览 |
| 检索结果态 | 首个勾选锁定类型；卡片操作同推荐态（查看摘要、进入全景图谱、加入对比篮）；支持全选本页与批量加入对比篮 | 不跨页暗选，不混选对象类型；不提供去门户总览 |
| 进入全景图谱 | `industry` / `industry_chain` 均跳转 `/industry-center/panorama`，携带 `object_type`、`object_id` 与返回查询上下文；产业入口展开所含产业链 | 不跳门户总览；不把 `chain_node` 作为独立结果或篮对象；不可用/权限受限对象禁用该动作 |
| 对象摘要抽屉 | 展示身份、摘要、来源与“可进入的页面”；操作仅关闭、加入对比篮、进入全景图谱 | 不出现去门户总览 / 打开专题全景 |
| 首个勾选 | 锁定本次选择类型 | 不允许 industry 与 chain 混选 |
| 全选本页 | 只选当前页同类型、可用且未入篮对象 | 不跨页暗选、不选不可用项 |
| 加入对比篮 | 成功项入篮，逐项返回失败原因；停留原页 | 不直接发起分析、不清空查询上下文 |
| 权限受限对象 | 卡片显示 Arco `IconLock` 与“权限受限”语义；保留对象名称、类型、父级产业、所属领域、更新时间、来源等允许公开的元数据，摘要替换为权限原因；查看摘要、进入全景图谱、选择和入篮动作呈锁态并可通过 Tooltip 读取原因 | 不使用普通不可用灰态替代锁态；不泄露摘要；不展示或推断“需要 L2/L3”等最低等级；评审模式不得改变权限结果 |
| 对象或数据暂不可用 | 卡片显示普通“暂不可用”与目录/数据/服务原因，禁止选择、进入全景图谱和入篮 | 不使用锁图标或权限申请文案，不与权限受限合并为同一视觉状态 |
| 初次进入 / 切换模式 / 清空条件 | 显示“推荐产业”，仅含 `industry` 和可解释推荐理由 | 不标为检索结果，不声明实时排序，不推荐产业链 |
| loading / empty | 卡片骨架 / 已执行查询后的三种模式对应空态 | 可调整或清空查询；零命中不回退推荐 |
| error / permission | 保留条件并明确重试 / 失败关闭；对象级 permission 使用锁态并保留非敏感元数据，页面级 permission 使用 Result/Alert | 不泄露敏感摘要，不从 Mock 用户推断权限等级 |

> 对比篮入口不属于本 Frame。系统对比篮以全局浮层存在，可从任意页面直接打开；本页不得重复设置“打开对比篮”按钮。

### 3.4 企业查询共享复用矩阵

| 区域 / 能力 | 共享承载 | 产业注入 | 禁止行为 |
| --- | --- | --- | --- |
| 普通查询工作台 | `ElementSearchWorkbench`；固定模式栏、输入/反馈、快捷入口、最近检索、推荐/结果的顺序与稳定容器 | 页面标识、模式标签、placeholder、示例和热门项 | 复制 Hero、最近检索或结果容器形成产业私有平行结构 |
| 检索中枢 | 泛化后的 `SearchHub`；Arco 搜索框、模式 Tab、SmartChip 宿主、示例与热门入口 | `smart / industry / advanced` 显示标签、产业 parser 输出、热门产业跳转 | 继承“查企业”、企业 test id、企业权限文案或企业字段 |
| 最近检索 | `RecentSearchPanel`；当前模式过滤、标题去重、最多 10 条、30 天、恢复重跑、清除 | 独立产业 storage key、产业模式和快照序列化 | 两域共用存储、产业页复制另一套历史 Tag UI |
| 推荐/结果工作区 | `ElementSearchWorkbench` 共享标题、说明、工具栏宿主、loading/empty/error/permission 容器和区块顺序 | 推荐卡、产业结果卡、查看摘要 / 进入全景图谱 / 加入对比篮与同类型选择 | 把企业名单、收藏、导出、评分、去门户总览等动作带入产业查询 |
| 高级筛选 | 现有 `FilterPanel` 页面形态 | 产业字段库、条件、方案和热门 preset | 在蓝色 Hero 内嵌高筛；继承企业字段 schema |
| 摘要与后续动作 | 共享 Drawer/焦点恢复语义 | 产业摘要；统一「进入全景图谱」出口与加入对比篮 | 从共享骨架推导门户总览出口或跨类型入篮规则 |

共享层只拥有结构、可访问性和状态宿主，不拥有领域字段、数据、权限结论或业务动作。企业与产业页面必须通过同一共享组件挂载点消费该结构；视觉一致性不得仅靠复制 CSS 达成。

## 4. F-CHAIN-02 产业链全景图谱

### 4.1 线框图

```text
┌─ 对象 ContextBar ──────────────────────────────────────────────────┐
│ 产业 / 产业链 · 快照时间          [单点] [双快照] [时间轴] [工具栏] │
├────────────────────────────────────────────────────────────────────┤
│ 上游 ───────── 核心环节 ───────── 下游     （完整正式环节与关系）  │
│                  [当前节点高亮]                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 4.2 字段、交互与状态

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `object_type/object_id` | 显式上下文；industry 先显示所属链，chain 直接进完整链 | — |
| `snapshot_id/schema_version` | 每次展示必须绑定快照与结构版本 | — |
| 环节与关系 | 全部正式环节进入画布，稳定从左到右 | — |
| 节点数量、关联数量等统计 | 未有正式专题口径前不得作为正式 KPI | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |

| 触发 / 状态 | 页面行为 | 禁止行为 / 下一步 |
| --- | --- | --- |
| 点击节点 | 高亮并打开 `F-CHAIN-03` 绑定详情 | 不把 node 变成分析主对象 |
| 缩放 / 适配 / 复位 | 只改变视口 | 不触发业务下钻或重算 |
| loading | 保留稳定画布容器与对象上下文 | 不闪回门户页面 |
| empty / error | 区分无结构、快照失败、无权限 | 不自动折叠、聚合、分页或伪造链条 |

## 5. F-CHAIN-03 全景节点详情与演进

### 5.1 结构

```text
┌─ 右侧详情（绑定 node_id + snapshot_id） ────────────────────────────┐
│ 环节职责 / 上下游关系 / 变化证据                                   │
│ 关联企业卡 [打开共享企业抽屉] [入企业篮]                           │
│ 技术路线 / 市场 / 科研与服务机构摘要                               │
└────────────────────────────────────────────────────────────────────┘
┌─ 双快照 / 时间轴 ──────────────────────────────────────────────────┐
│ 基准快照 [时间]  对比快照 [时间]  [播放/暂停]  变化：新增/替代/退出 │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `node_id/chain_id/snapshot_id` | 详情三重绑定，不随视口改变 | — |
| 企业 / 技术 /市场等明细 | 只作当前产业链上下文，不生成技术对象入口 | — |
| 市场规模、企业数、变化量等统计 | 有正式指标后逐字段登记；当前只展示明细或缺口 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 变化证据 | 必须带来源快照和变化类型 | — |

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 无选中节点 | 详情区提示“选择环节查看详情” | 选择节点 |
| 快照不兼容 | 不进入比较，保留当前有效单点 | 重选兼容快照 |
| 时间范围无变化 | 明确“无已确认变化”，不伪造动画 | 调整范围 |
| 详情失败 | 画布不丢失，详情区独立重试 | 重试或换节点 |

## 6. F-CHAIN-04 产业周期配置与结果

### 6.1 结构

```text
┌─ 产业运行诊断 / 周期分析 ─────────────────────────────────────────┐
│ 对象卡：1 个 industry        模型与数据版本状态                    │
│ 注册参数表单 / 联网检索边界 / 预测窗口              [生成分析]    │
├─ 成功结果 ─────────────────────────────────────────────────────────┤
│ 当前阶段 | 历史回溯 | 趋势预测 | 驱动因素 | 潜在拐点 | 局限性     │
│ [查看配置] [生成报告]                                              │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 来源与规则 | metric_id / gap |
| --- | --- | --- |
| `industry_id` | 共享篮 / 草稿；恰好 1 个 | — |
| 注册参数、预测窗口 | 模型注册合同；不得前端自创 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 周期阶段、驱动、拐点 | 不可变结果快照 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 模型 / 数据 / 参数版本 | 结果审计字段 | — |

| 触发 / 状态 | 页面行为 | 禁止行为 |
| --- | --- | --- |
| 提交 | 最终校验后创建新任务 | 不用 chain 对象；不重复建任务 |
| succeeded | 显式“查看结果”，不自动跳转 | 不原位编辑或静默刷新结果 |
| result expired | 只读结果，禁新正式报告 | 可复制配置新建 |
| error / permission | 保留草稿或失败关闭 | 不用 Mock 权限替代服务端结果 |

## 7. F-CHAIN-05 关键环节配置与结果

```text
┌─ 产业运行诊断 / 关键环节识别 ─────────────────────────────────────┐
│ 对象：1 个 industry_chain     固定因子（只读）        [生成分析]   │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 完整链条 + 关键标注 | 环节排名 | 竞争格局 | 代表企业 | 技术趋势   │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `chain_id/parent_industry_id` | 恰好 1 个产业链 | — |
| 附加值、技术壁垒、集中度等固定因子 | 只读注册值，不展示无意义模板保存 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 高端化指数、排名、关键标注 | 来自不可变结果；缺证据不标注 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 代表企业 | 可打开共享企业抽屉 / 入企业篮 | — |

- 加载：固定因子与结果区分别使用稳定骨架。
- 空态：无对象时展示选择对象说明，但不设置页内“打开对比篮”按钮；用户可使用任意页面可用的系统对比篮全局浮层。无关键环节时说明模型结论，不伪造 TopN。
- 错误 / 无权限：禁止提交或隐藏敏感企业摘要；完整链条的非敏感结构按权限合同处理。
- 禁止：编辑固定因子权重、直接发起企业分析、把企业或节点作为本任务主对象。

## 8. F-CHAIN-06 瓶颈堵点配置与结果

```text
┌─ 产业运行诊断 / 瓶颈堵点 ─────────────────────────────────────────┐
│ 对象：1 个 industry_chain  固定维度：技术/人才/资本/政策… [生成分析]│
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 全链健康图 | 维度矩阵 | 瓶颈位置 | 原因 | 改进建议 | 局限性       │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `chain_id` | 恰好 1 个产业链 | — |
| 固定诊断维度与阈值 | 注册合同；任一必需维度不可用不得静默删除 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 健康度、瓶颈分值、归因证据 | 不可变结果 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 改进建议 | 绑定瓶颈、原因和模型版本 | — |

- 默认：只读确认维度；不出现自定义阈值。
- 部分证据：显式局限，不能输出伪正式完整诊断。
- 过期结果：只读、禁新正式报告。
- 禁止：创建政策/项目、预算、责任分派或执行跟踪。

## 9. F-CHAIN-07 区域产业指数配置与结果

```text
┌─ 区域产业评价 / 指数评价 ─────────────────────────────────────────┐
│ 对象组合：1产业×1~5区域 或 2~5产业×1区域                           │
│ 预设指标勾选 | 权重=100% | 个人模板 | [轻量预览] [生成分析]        │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 综合指数 | 维度对比 | 指标贡献 | 优势短板 | [查看配置]             │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `industry_ids/region_codes` | 只允许 1×1、1×2~5、2~5×1 | — |
| 预设指标与权重 | 勾选 / 取消参与；合计 100%；不删除库项 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 自定义指标 | 本轮不开放，显示 Bid 差异 | `gap_ref: GAP-CHAIN-TOPIC-CUSTOM-METRIC` |
| 预览值 | 轻量服务；不入任务历史、不占任务并发 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 综合指数、贡献、优势短板 | 不可变结果 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |

- 多产业×多区域：禁止提交，不自动删除对象。
- 权重不等于 100%：定位差额，支持一键均分；不静默归一化。
- 不可比较对象：不生成伪排名，列出对象和原因。
- 禁止：创建/删除指标、把区域加入篮、把预览写入分析记录。

## 10. F-CHAIN-08 区域竞争力配置与结果

```text
┌─ 区域产业评价 / 竞争力 ───────────────────────────────────────────┐
│ 对象组合 | 企业能力 / 学术生态 / 配套环境（固定三维）              │
│ 一级权重=100%                                      [生成分析]      │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 综合排名 | 三维对比 | 热力图 | 优势短板 | 版本边界                 │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| 对象组合 | 沿用 `F-CHAIN-07` 区域合同 | — |
| 三大一级维度和权重 | 维度固定，只调一级权重 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 综合指数 / 排名 / 热力图 | 同一模型与权重版本才可比较 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |

- 必需维度不可用：禁止正式提交，不降成两维模型。
- 不同模型 / 权重版本：禁止直接混排。
- 数据不足区域：明确不参与或低置信处理，不能补造完整排名。
- 禁止：新增一级维度、修改内部算法、人工覆盖排名。

## 11. F-CHAIN-09 深圳产业对比配置与结果

```text
┌─ 深圳产业决策 / 情况对比 ─────────────────────────────────────────┐
│ 主体：深圳（固定） | 产业：1 个 | 标杆区域：1~5 个                 │
│ 四维模型（只读） | 区域就绪矩阵                  [生成分析]        │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 四维对比 | 综合结论 | 优势差距 | 产业化潜力 | 发展阶段             │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| 主体区域 | 固定深圳，不能替换 | — |
| `industry_id` | 恰好 1 个产业 | — |
| benchmark regions | 1~5 个国内 / 国际标杆；不可用项保留原因 | — |
| 企业、专利、政策、人才等四维 | 注册模型，只读确认 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |
| 潜力 / 阶段 / 优势差距 | 不可变结构化结果 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |

- 无有效标杆：禁止提交，不自动填充默认城市。
- 标杆数据后续失效：旧结果不变，显示局限。
- 无结构化合同：结果不能成为 `F-CHAIN-10` 输入。
- 禁止：更换深圳主体、静默删除不利标杆、自动运行发展分析。

## 12. F-CHAIN-10 深圳产业发展配置与结果

```text
┌─ 深圳产业决策 / 发展分析 ─────────────────────────────────────────┐
│ 产业：1 个 | 来源：有效深圳对比结构化结果（显式选择）              │
│ 目标：政策 / 技术 / 人才                           [生成分析]      │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 三类建议 | 路径 A | 路径 B（至少两条） | 依据 | 适用条件 | 局限性  │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `industry_id` | 与来源结果产业一致 | — |
| `source_result_id/revision` | 必须同产业、有效、有权且结构兼容 | — |
| 政策 / 技术 / 人才目标 | 用户显式确认 | — |
| 建议与路径依据 | 绑定来源对比快照 | `metric_gap_ref: GAP-CHAIN-TOPIC-METRICS` |

- PDF、过期、跨产业或无权结果：不可选择，不从内容猜结构化输入。
- 可靠路径少于两条：结果标不完整，不补造第二条。
- 来源结果失效：旧结果仍只读，新任务需重新选择来源。
- 禁止：自动继承最近结果、自动运行、创建项目/预算/排期/责任分派。

## 13. F-CHAIN-11 统一可视化分析过程与分析记录

### 13.1 结构

```text
┌─ 任务摘要 ─────────────────────────────────────────────────────────┐
│ task_id / 分析类型 / 对象摘要 / 创建时间 / 状态 / 队列或已用时间   │
├─ 可视化分析过程 ───────────────────────────────────────────────────┤
│ ①任务提交 ─ ②校验 ─ ③数据准备 ─ ④领域分析 ─ ⑤结果校验 ─ ⑥组装  │
│ 当前阶段提示 / 后台继续与恢复说明                                  │
│ queued：[撤回]    running：无取消动作    succeeded：[查看结果]      │
│ failed/terminated/withdrawn：[按此配置新建分析]                    │
├─ 分析记录 ─────────────────────────────────────────────────────────┤
│ 当前二级页面所属任务筛选 / 状态 / 时间 / 对象 / 结果或失败入口     │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 | metric_id |
| --- | --- | --- |
| `task_id/task_type/status/stage` | 服务端任务真源 | — |
| `stage_definitions/current_stage` | 按 `analysis_type` 注册；六段式仅为当前壳层规划，不复制企业领域文案 | — |
| 对象 / 配置 / 模型 / 数据快照引用 | 全部只读 | — |
| 队列位置 / 已用时间 | 服务端返回；仅作任务状态字段 | — |
| 来源页面 / Tab / 结果路由 | 服务端身份恢复，不由 URL 猜测 | — |

| 状态 / 触发 | 页面行为 | 禁止行为 |
| --- | --- | --- |
| queued 撤回 | 二次确认；成功进入 withdrawn、释放互斥、不产结果 | 不直接前端改状态 |
| running | 展示阶段和已用时间，离页继续 | 普通用户不显示取消；服务端拒绝取消 |
| succeeded | 显示“查看结果”，不自动跳转 | 不静默打开最近成功结果 |
| failed / terminated / withdrawn | 允许复制快照到新草稿 | 不原位重跑、不复用 task_id |
| records | 只显示所属二级页面历史 | 不建立独立全局产业任务中心 |

## 14. F-CHAIN-12 报告入口与阅读交接

```text
┌─ 来源结果报告区 ───────────────────────────────────────────────────┐
│ not_generated / generating / ready / failed / expired              │
│ [生成报告] [查看任务] [查看报告] [下载 PDF]                        │
├─ 只读报告 ─────────────────────────────────────────────────────────┤
│ 报告身份 / 对象与范围 / 决策摘要 / 核心发现 / 证据与分析           │
│ 来源与版本 / 局限性 / 同源 PDF                                    │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric_id / gap |
| --- | --- | --- |
| `source_task_id/source_result_id` | 必须成功、有效且有权 | — |
| `report_id/report_revision_id` | 阅读与 PDF 的一致性边界 | — |
| 章节统计与图表 | 完全读取来源结果，不在报告阶段重算 | 引用来源结果 metric_id；未登记时 `GAP-CHAIN-TOPIC-METRICS` |
| 报告状态 | 共享报告任务真源 | — |

- 报告共享框架未激活：动作失败关闭，来源结果仍可读；显示 `GAP-CHAIN-TOPIC-REPORT-ACTIVATION`。
- 来源过期 / 失败 / 无权：不创建报告，不泄露模板或结果内容。
- 在线阅读与 PDF 必须同一修订；不能一个跟随最新数据、另一个保留旧数据。
- 禁止：报告收藏、编辑、章节配置、用 PDF 作为发展分析输入、报告阶段重算结论。

## 15. 跨 Frame 对象共享与隔离

| 范围 | 可共享 | 必须隔离 |
| --- | --- | --- |
| `F-CHAIN-02/03` | 对象、节点、快照、视口的页内上下文 | 不向分析工作空间自动传对象 |
| `F-CHAIN-04/05/06` | 同一诊断页兼容的 industry；05/06 可共享兼容 chain | 配置、筛选、结果焦点互不共享 |
| `F-CHAIN-07/08` | 兼容产业对象 | 区域、指标、权重、模板、预览分别维护 |
| `F-CHAIN-09/10` | 兼容产业对象 | 发展分析必须显式选择来源结果 |
| `F-CHAIN-11` | 只读任务真源 | 进入记录不得覆盖业务 Tab 草稿 |
| `F-CHAIN-12` | 来源结果和报告修订身份 | 报告不得反向改写结果或篮对象 |

跨二级页面时，目标页先恢复自己的未提交草稿或非终态任务；都没有才显示对象空态。跨页对象只可由共享篮重新分发、明确的历史复制动作或有效深链恢复。

## 16. 必需状态矩阵

| Frame | default | loading | empty | error | permission | 特殊状态 |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | 查询模式和卡片 | 卡片骨架 | 无匹配对象 | 保留条件可重试 | permission_locked 锁态、非敏感元数据保留、敏感摘要隐藏；与 unavailable 分离 | type_locked / partial_add |
| F-02 | 完整图谱 | 稳定画布骨架 | 无结构 | 快照失败 | 无权失败关闭 | single / dual / timeline |
| F-03 | 节点详情 | 详情独立骨架 | 未选节点 | 详情可重试 | 企业摘要裁剪 | incompatible_snapshot |
| F-04~10 | 对象与配置 / 结果 | 表单或结果骨架 | 对象空态 | 保留草稿 / 结果错误 | 生成与查看失败关闭 | validating / result / expired |
| F-11 | 可视化过程或记录 | 稳定任务摘要、Steps / 列表骨架 | 无任务 / 无历史 | 阶段失败可恢复 | 仅本人及获授权任务 | created / prechecking / queued / running / succeeded / failed / withdrawn / terminated |
| F-12 | 报告状态 / 阅读 | 章节骨架 | 未生成 | 生成或阅读失败 | 不泄露报告摘要 | generating / ready / expired |

## 17. 评审追溯合同（机器可读）

```yaml
review_trace_applicability: applicable
reason: 模块包含原始需求追溯、统计指标、Mock/Pending/readiness 与不可变模型结果。
business_mode_contract:
  all_review_mounts: absent
  must_not_change: [business_fields, permissions, result_snapshot, actions, layout_capacity]
overflow_rule_ref: agent-delivery/data-lineage-policy.md#2.3.3 / DEC-D9-DATA-HEALTH-GROUPING-20260803
overflow_gap_ref: null
overflow_status: resolved_by_data_health_grouping
entry_marker_groups: [definition, data_health, ingestion]
data_health_component: DataHealthBadge
data_health_dimensions: [schema_status, source_mapping_status]
data_health_popover_rows: [structure, source_mapping]
max_markers: 3
spacing_px: 4
review_trace_contract:
  - frame_id: F-CHAIN-01
    review_mounts:
      - mount_id: CHAIN-TOPIC-F01-SEARCH-TITLE
            host_label: 产业查询评审页头（标题和说明）
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-CHAIN-TOPIC-01]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-02
    review_mounts:
      - mount_id: CHAIN-TOPIC-F02-PANORAMA-TITLE
        host_label: 产业链全景图谱标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-01, US-CHAIN-TOPIC-02]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-03
    review_mounts:
      - mount_id: CHAIN-TOPIC-F03-EVOLUTION-TITLE
        host_label: 动态演进区标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-01, US-CHAIN-TOPIC-03]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F03-STATS-HOST
        host_label: 节点详情统计字段组
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-04
    review_mounts:
      - mount_id: CHAIN-TOPIC-F04-CYCLE-TITLE
        host_label: 周期分析结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-02, US-CHAIN-TOPIC-04, US-CHAIN-TOPIC-05]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F04-CYCLE-METRICS
        host_label: 周期判断与预测统计区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-05
    review_mounts:
      - mount_id: CHAIN-TOPIC-F05-KEYLINK-TITLE
        host_label: 关键环节结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-04, US-CHAIN-TOPIC-06, US-CHAIN-TOPIC-07]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F05-KEYLINK-METRICS
        host_label: 固定因子与关键环节指标区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-06
    review_mounts:
      - mount_id: CHAIN-TOPIC-F06-BOTTLENECK-TITLE
        host_label: 瓶颈堵点结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-05, US-CHAIN-TOPIC-08, US-CHAIN-TOPIC-09]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F06-BOTTLENECK-METRICS
        host_label: 健康度与归因指标区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-07
    review_mounts:
      - mount_id: CHAIN-TOPIC-F07-INDEX-TITLE
        host_label: 区域产业指数结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-03, US-CHAIN-TOPIC-10, US-CHAIN-TOPIC-11]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F07-INDEX-METRICS
        host_label: 指标配置与指数结果区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS, GAP-CHAIN-TOPIC-CUSTOM-METRIC]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-08
    review_mounts:
      - mount_id: CHAIN-TOPIC-F08-COMPETITIVENESS-TITLE
        host_label: 区域竞争力结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-08, US-CHAIN-TOPIC-12, US-CHAIN-TOPIC-13]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F08-COMPETITIVENESS-METRICS
        host_label: 三维权重与排名指标区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-09
    review_mounts:
      - mount_id: CHAIN-TOPIC-F09-SZ-COMPARE-TITLE
        host_label: 深圳产业对比结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-06, US-CHAIN-TOPIC-14, US-CHAIN-TOPIC-15]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F09-SZ-COMPARE-METRICS
        host_label: 四维对比与阶段指标区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-10
    review_mounts:
      - mount_id: CHAIN-TOPIC-F10-DEVELOPMENT-TITLE
        host_label: 深圳产业发展结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [REQ-CHAIN-TOPIC-07, US-CHAIN-TOPIC-16, US-CHAIN-TOPIC-17]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F10-DEVELOPMENT-EVIDENCE
        host_label: 建议与路径依据区
        marker_type: missing_metric_entry
        source_relation: direct_requirement
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-11
    review_mounts:
      - mount_id: CHAIN-TOPIC-F11-TASK-TITLE
        host_label: 统一可视化分析过程与分析记录标题
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-CHAIN-TOPIC-18, US-CHAIN-TOPIC-19]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-CHAIN-12
    review_mounts:
      - mount_id: CHAIN-TOPIC-F12-REPORT-TITLE
        host_label: 产业分析报告标题
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-CHAIN-TOPIC-20, GAP-CHAIN-TOPIC-REPORT-ACTIVATION]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: CHAIN-TOPIC-F12-REPORT-METRICS
        host_label: 报告统计与图表区
        marker_type: missing_metric_entry
        source_relation: product_interpretation
        trace_refs: [GAP-CHAIN-TOPIC-METRICS]
        required_payload: [gap_ref, host_fields, metric_owner, expected_matrix]
        review_mode: present
        business_mode: absent
```

### 17.1 禁止挂载位置

- 禁止把评审标识放入业务按钮、表单 label、图表图例、数据值字符串或下载文件正文。
- 禁止在任一专题 Frame 重复设置“打开对比篮”按钮；对比篮只通过系统级全局浮层入口打开。
- 除已确认的 F-01 评审页头折叠外，禁止评审模式改变布局容量；任何 Frame 均不得因评审模式改变业务字段、权限判定、默认选择、任务状态、结果快照或报告修订。
- 禁止把 requirement trace、D1 定义、D2 结构、D3 源映射、D4 接入状态压成同一无类型标识。
- D2、D3 不得重新展开为同宿主的两枚兄弟入口角标；`DataHealthBadge` 必须逐行保留两维 payload，不得以组合显示为由静默隐藏或压成无类型状态。

## 18. 响应式与视觉约束

- `screen_tier: medium_1440_1920`，只适用于专题系统 Track-MS 中屏工作台；不声明 `small_reflow` 或 Track-L。
- 遵循当前 `Design.md`：Header 64px、Sidebar 200px、页面底色 `#D8E7FC`、主色 `#165DFF`、Arco 组件、浅色中屏工作台。
- 1440px：压缩辅助说明与卡片列数，右侧详情可抽屉化；不得删除业务字段、状态或追溯宿主。
- 1680px～1920px：增加主视图宽度与并列比较空间，不改变对象、故事、指标或权限合同。
- 不以浏览器宽度创建移动端 deliverable；专题系统不得借本包声明 `small_reflow`。

## 19. 模块明确排除

- 门户产业总览、门户内容管理和门户 Demo 改造；
- 产业查询导出、结果收藏、报告收藏、独立产业任务中心；
- 区域入篮、技术对象入篮、技术链分析、企业分析直达；
- 多产业×多区域笛卡尔积；
- 自定义指标的未批准实现；
- 前端自算正式指标、模型结论、关键环节、瓶颈或发展路径；
- 政策/项目创建、预算、排期、责任单位和执行管理。

## 20. Wireframe 自检

- [x] 12 个 Frame 均对应 IA 节点、TRACE Frame 计划与 USM 主/异常路径。
- [x] 每个统计区已引用正式指标缺口；未把 gap ID 冒充 metric_id。
- [x] 默认、加载、空、错误、权限及任务特殊状态已定义。
- [x] `queued → withdrawn` 与 `running → 普通用户不可取消` 已进入状态机、Frame 11 和禁止行为。
- [x] `review_trace_applicability: applicable`，12/12 Frame 均有显式 `review_mounts`。
- [x] 每个 `mount_id` 唯一，宿主、类型、payload、评审/业务模式显隐齐全。
- [x] marker overflow 已由批准规则关闭；D1 / `DataHealthBadge(D2+D3)` / D4 三组投影最多三枚且不丢失机器维度。
- [x] `screen_tier` 与 TRACE 一致为 `medium_1440_1920`。
- [x] 未引入模块外搜索对象、导出、收藏、执行管理或技术链入口。
