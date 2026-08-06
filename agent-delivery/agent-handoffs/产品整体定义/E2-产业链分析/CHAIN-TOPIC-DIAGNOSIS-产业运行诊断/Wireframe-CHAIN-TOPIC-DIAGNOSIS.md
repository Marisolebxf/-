# Wireframe-CHAIN-TOPIC-DIAGNOSIS｜产业运行诊断

> **版本**：v1.12-hide-cycle-score-kpis  
> **状态**：核心产品包 Wireframe；`ready_for_v1: true`  
> **体验 Owner**：高颖  
> **screen_tier**：`medium_1440_1920`  
> **边界**：本文件为产业运行诊断唯一结构基线；父包 `F-CHAIN-04/05/06` 仅溯源。  
> **修订**：周期结果顶栏去掉「阶段评分 / 技术成熟度」数值卡；保留当前阶段与阶段判定；评分仍见于回溯/预测曲线与对标表。`DEC-CHAIN-DIAG-HIDE-CYCLE-SCORE-KPIS-20260806`。

## 1. Frame 清单

| Frame | 路由 / 宿主 | 目标 | 故事 |
| --- | --- | --- | --- |
| `F-DIAG-01` | `/industry-center/diagnosis` | 工作区壳、对象上下文、Tab | 全部 |
| `F-DIAG-02` | `?tab=cycle` | 周期配置 / 过程 / 结果 | `US-CHAIN-DIAG-01/02` |
| `F-DIAG-03` | `?tab=key-link` | 关键环节配置 / 过程 / 结果 | `US-CHAIN-DIAG-03/04` |
| `F-DIAG-04` | `?tab=bottleneck` | 瓶颈配置 / 过程 / 结果 | `US-CHAIN-DIAG-05/06` |
| `F-DIAG-05` | `?tab=records` | 诊断记录 | `US-CHAIN-DIAG-07` |

## 2. 统一骨架与状态机

- 壳层（对齐企业评估）：页标题「产业运行诊断」（`ReviewOnly`，业务态不展示页标题，与企业评估一致）+ 对象上下文条 + 一级 Tab（产业周期 / 关键环节 / 瓶颈堵点 / 诊断记录，业务态保留）。
- **一级 Tab 视觉**：与企业评估同构——`global-workbench-tabs` + `enterprise-center-primary-tabs`（底边 3px 主色下划线、无卡片底）；禁止自绘 Arco Tabs 卡片条样式。
- 工作态：`no_object+config` → `config` → `processing`（页内可视化 Steps）→ `result`；记录态独立。
- **可视化过程壳（对齐企业评估）**：上卡「诊断生成中」+ 状态 Tag + Descriptions（任务 ID / 诊断类型 / 对象数量·单位按对象类型 / 已用时间）；下卡「可视化分析过程」+ Steps（vertical label）+ 当前阶段 Alert + 右下操作（查看诊断记录 / 查看分析结果）。Bid 降级说明进评审态。
- **无分析对象时**：Tab 与各配置区参数仍完整展示；「生成分析」禁用并提示先选对象（同企业评估「先显配置、后绑对象」）。
- 三业务 Tab 共享兼容产业 ID；关键/瓶颈共享兼容链 ID；配置与结果焦点隔离；周期不消费链 ID。
- **本次分析上下文（方案 A，三 Tab 结构一致、字段按需）**：配置区顶部固定「分析对象」（只读，与顶栏同源）+「所属产业链」。周期为「本分析不依赖产业链」只读占位，并增加业务可见「分析时间范围」；关键/瓶颈为必填确认 Select（无时间范围）。
- **业务 / 评审分层**：业务模式不展示页标题、「本次分析上下文」标题、「顶栏同源 / 正式口径待闭合 / 固定演示」、结果顶「演示数据」Alert 等交付说明；此类文案进评审模式（`ReviewOnly`）。业务态仍保留一级 Tab、身份字段（周期含时间范围）与结果正文。
- **配置底栏**：三 Tab 统一「重置参数」+「生成分析」；不在参数区标题旁另设「恢复推荐值」。
- 点击「生成分析」才创建任务并进入可视化过程；结果须显式「查看分析结果」；**禁止自动跳转结果页**。
- 周期过程 Steps 使用 §4.1 Bid 词汇表；非可操作联网控制台。

## 3. F-DIAG-01 工作区壳与对象上下文

```text
┌─ 产业运行诊断 ───────────────────────────────────────────────────┐
│ 分析对象：{摘要} | 空态引导 + [打开对比篮]                          │
│ Tabs（global-workbench-tabs）: 产业周期 | 关键环节 | 瓶颈堵点 | 诊断记录 │
│ （配置页参数区始终可预览）                                         │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 |
| --- | --- |
| 对象摘要 | 来自共享篮；空态引导打开对比篮，**不隐藏**下方配置 |
| Tab | `cycle` / `key-link` / `bottleneck` / `records`；写入 URL；无对象时仍可切换预览配置 |

状态：`no_object` / `object_ready` / `permission_locked` / `unavailable`。  
禁止：无对象时隐藏 Tab/配置；页内私有对象 Select；模块自建浮层篮；工作区自建「更换对象」平行入口（以对比篮为准）。

评审挂点：`CHAIN-DIAG-F01-OBJECT-CONTEXT`（requirement_trace；BusinessMode absent）。

## 4. F-DIAG-02 产业周期配置与结果

```text
┌─ 产业运行诊断 / 周期分析 · 配置 ──────────────────────────────────┐
│ 本次分析上下文：分析对象（只读）| 所属产业链＝不依赖 | 分析时间范围 │
│ 参数表：市场规模 | 增长率 | 利润率 | 技术成熟度                       │
│ 模型/数据版本                                      [生成分析]      │
├─ 共享任务过程壳（对齐企业评估 · 生成后）────────────────────────────┤
│ 上卡：诊断生成中 | 状态Tag | 任务ID/类型/对象数量/已用时间           │
│ 下卡：可视化分析过程 | Steps（§4.1）| 当前阶段 Alert | 右下操作     │
│ V1 降级条（评审态）：固定可回放检索快照 · 待正式联网检索与模型接通   │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 回溯—诊断—预测 | 当前阶段 | 阶段判定 | 驱动因素 | 拐点 | 决策摘要   │
│ 趋势图（ECharts）：历史实线 + 预测虚线 + 95% 置信带（演示）         │
│ 轴标签预测年可标 2027E；图例：历史 / 预测 / 置信区间 / 潜在拐点     │
│ 潜在拐点：预测段空心菱形轻量标注（非已确认事件）+ 右侧列表完整叙述   │
│ 下方保留 backtrace 四张阶段卡；方法依据文案进 ReviewOnly              │
│ 检索来源与快照：三列可回放事件短列表（历史/市场/动态，各约 3–4 条）   │
│ 事件可点 → 页内详情抽屉；源链接 Demo 禁用（正式由服务端返回）         │
│ 事件字段：日期 · 标题 · 一行摘要 · 来源标签；底栏命中条数+来源池     │
│ 顶栏总结（对齐企业评估）：{类型}结果 | 元信息 | [按此配置新建分析]   │
│ 底栏报告卡：诊断报告 | [生成 / 查看报告]                            │
└────────────────────────────────────────────────────────────────────┘
```

### 4.1 周期过程阶段文案（验收必现）

| 顺序 | 阶段文案（须可见） | Bid 原文锚点 |
| --- | --- | --- |
| 1 | 任务提交与参数冻结 | 用户输入/调整关键产业参数 |
| 2 | 整合产业参数与联网检索的历史与市场数据 | 实时网络搜索 / 联网检索历史与市场数据 |
| 3 | 大语言模型推理与周期阶段判断（诊断） | 大语言模型生成周期阶段判断 |
| 4 | 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点 | 全网检索最新产业动态；驱动因素与拐点；推理与归纳 |
| 5 | 结果可信性校验与分析报告组装 | 趋势预测报告 / 分析报告 |

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| `industry_id` | 单选产业（顶栏 + 本次分析上下文只读回显） | — |
| 所属产业链 | 周期不消费；只读占位「本分析不依赖产业链」 | — |
| 分析时间范围 | 业务可见；置于本次分析上下文；可调；提交后写入参数快照并在结果顶栏回显；**不**放在评审态「本次分析配置」 | — |
| 四参数 | 可调；提交时冻结快照 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 权重阈值版本 / 模型版本 / 数据截至 | 仅评审态「本次分析配置」；业务态不展示 | — |
| 过程 Steps | 必须使用 §4.1 词汇；只读，非联网控制台 | — |
| 检索快照 / V1 降级 | 未接通时固定可回放 + 待接通说明；禁止完成态假话 | `gap_ref: GAP-CHAIN-DIAG-API` |
| 检索事件短列表 | 三列卡内各 3–4 条演示事件（date/title/summary/sourceLabel）；点击打开页内详情抽屉（含快照摘录）；「打开源链接」Demo 禁用并说明待服务端返回；禁止假外链 / 实时检索完成态 | `gap_ref: GAP-CHAIN-DIAG-API` |
| 回溯—诊断—预测 / 驱动 / 拐点 | 不可变结果；结果 KPI 条仅「当前阶段 / 阶段判定」，**不**挂「阶段评分 / 技术成熟度」数值卡（曲线纵轴与对标表可保留评分） | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 趋势预测图 | ECharts 折线：历史实线（backtrace）+ 预测虚线（forecast，衔接年重合）+ 包住预测线的 95% 置信带（演示，`ciLow`/`ciHigh`）；禁止柱状条伪趋势；置信带勿做成单向楔形 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 潜在拐点标注 | 拐点绑定预测轴年份；图上 scatter 空心菱形轻量标注（上行绿 / 风险橙）+ 右侧列表完整叙述；禁止做成已确认实心事件点 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 预测方法说明 | 业务态可不展示长口径；评审态 `ReviewOnly` 展示演示方法依据 | `gap_ref: GAP-CHAIN-DIAG-SEMANTICS` |
| 多产业周期对比 | 主对象仍单选；表为**系统对标**结果（非对比篮多选）；标题旁注「系统对标（演示）」；对标产业产生方式见 `QC10`（确认前不开放自选对标） | `pending_ref: QC10` |

禁止：未点按钮自动建任务；「已完成实时全网检索」；可操作联网控制台；静默刷新过期结果；用柱状高度冒充趋势/预测；把对比表误当作多产业分析对象。

评审挂点：
- `CHAIN-DIAG-F02-CYCLE-TITLE`（requirement_trace）
- `CHAIN-DIAG-F02-CYCLE-STAGE`（missing_metric_entry）
- `CHAIN-DIAG-F02-PROCESS-STAGES`（requirement_trace）
- `CHAIN-DIAG-F02-RETRIEVAL-SNAPSHOT`（requirement_trace）
- `CHAIN-DIAG-F02-DECISION-BRIEF`（requirement_trace）
- `CHAIN-DIAG-F02-CYCLE-COMPARISON`（pending_decision / QC10）

## 5. F-DIAG-03 关键环节配置与结果

```text
┌─ 产业运行诊断 / 关键环节 · 配置 ──────────────────────────────────┐
│ 本次分析上下文：分析对象（只读）| 所属产业链（必填确认）             │
│ 注册因子只读表：附加值率 | 技术壁垒 | 市场集中度 | 权重/阈值状态     │
│ 模型/数据版本（只读确认）                              [生成分析]  │
├─ 共享任务过程壳（生成后）──────────────────────────────────────────┤
│ Steps：见 §5.1 Bid 词汇阶段（只读进度）                              │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 全链路结构化图谱（研发→设计→制造→销售→服务）                         │
│ 功能边界 | 衔接逻辑 | 高端化指数 | 关键标注                           │
│ 竞争格局 | 代表企业 | 技术趋势 | [生成报告交接]                      │
└────────────────────────────────────────────────────────────────────┘
```

### 5.1 关键环节过程阶段文案（验收必现）

| 顺序 | 阶段文案（须可见） | Bid 原文锚点 |
| --- | --- | --- |
| 1 | 任务提交与产业链对象冻结 | 提交识别任务 |
| 2 | 全链路环节结构化拆解（研发/设计/制造/销售/服务） | `.4.1` 标准化环节 / 结构化图谱 |
| 3 | 基于附加值率、技术壁垒、市场集中度计算高端化指数 | `.4.2` 指标与高端化指数 |
| 4 | 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 | `.4.2` 标注与分析 |
| 5 | 结果可信性校验与分析报告组装 | 技术趋势报告 / 分析报告 |

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| `industry_chain_id` | 单选产业链 | — |
| 注册因子 | 只读确认；不可编辑正式权重 | `gap_ref: GAP-CHAIN-DIAG-SEMANTICS` |
| 过程 Steps | 必须使用 §5.1 词汇 | — |
| 结构化图谱 | 全链五环节可读结构（图谱或等价链式结构）；须可见功能边界与衔接逻辑 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 高端化指数 + 关键标注 | 指数须显式标注；不可截断为仅关键列表 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 竞争格局 / 代表企业 / 技术趋势 | 结果面必现；报告经 ENT-EXPORT 交接 | — |
| 代表企业 | 与全景「关联企业」同构卡片（名称/经营状态/资质/产业方向 + 查看企业 + 加入/移出企业篮）；画像用共享 `ElementProfile`；加入系统企业篮 | — |

禁止：伪可编辑权重；补造无证据关键标注；跳转企业分析页；只展示关键节点而隐藏全链。

评审挂点：
- `CHAIN-DIAG-F03-KEY-TITLE`（requirement_trace）
- `CHAIN-DIAG-F03-KEY-COUNT`（missing_metric_entry）
- `CHAIN-DIAG-F03-PROCESS-STAGES`（requirement_trace）
- `CHAIN-DIAG-F03-FACTOR-READONLY`（pending_decision）
- `CHAIN-DIAG-F03-HIGH-END-INDEX`（missing_metric_entry）

## 6. F-DIAG-04 瓶颈堵点配置与结果

```text
┌─ 产业运行诊断 / 瓶颈堵点 ─────────────────────────────────────────┐
│ 本次分析上下文：分析对象（只读）| 所属产业链（必填确认）             │
│ 五维只读表：技术 | 人才 | 市场需求 | 资本 | 政策 | 权重/阈值状态     │
│ 模型/数据版本（只读确认）                              [生成分析]  │
├─ 共享任务过程壳（生成后）──────────────────────────────────────────┤
│ Steps：见 §6.1 Bid 词汇阶段（只读进度）                              │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 顶栏：{分析对象} · 产业瓶颈堵点识别结果                              │
│ 主工区：全链路环节健康图谱（五节点+有向边，非全景）                   │
│ 节点=研发/设计/制造/销售/服务；显式健康度；卡脖子/薄弱点位标注       │
│ 点选节点 → 右侧详情：健康度 + 成因/影响/改进建议/趋势预警           │
│ 左图谱容器高度与右详情等高对齐（以右侧内容高度为准）                 │
│ 顶栏 KPI：瓶颈数 / 最高严重度 / 类型分布 / 卡脖子环节数（= choke 计数）│
├─ 诊断报告 SectionPanel ─────────────────────────────────────────────┤
│ [生成 / 查看报告] · 政策/项目设计正式出口                            │
└────────────────────────────────────────────────────────────────────┘
```

### 6.1 瓶颈过程阶段文案（验收必现）

| 顺序 | 阶段文案（须可见） | Bid 原文锚点 |
| --- | --- | --- |
| 1 | 任务提交与产业链对象冻结 | 提交识别任务 |
| 2 | 整合各环节技术/人才/资本/政策等时序数据 | `.2.2.5` 时序数据 |
| 3 | 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度 | `.5.1` 四指标与健康度 |
| 4 | 瓶颈智能识别与卡脖子环节归因/改进建议生成 | `.5.2` 智能识别与建议 |
| 5 | 结果可信性校验与靶向方案/报告组装 | 靶向方案 / 分析报告 |

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| `industry_chain_id` | 单选产业链 | — |
| 五维 | 文案必须「资本」（展示 Bid 原文）；算法「资金」不拆第六维 | TRACE `dimension_alias_note` |
| 过程 Steps | 必须使用 §6.1 词汇 | — |
| 全链路环节健康图谱 | 默认五环节结构化图谱为主工区；节点显式健康度与稳健/关注/薄弱/卡脖子点位；窄屏可降级链式；禁止报告长文主区；禁止全景通图高亮 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| `.5.1` 四核心指标 | 技术成熟度、人才供给量、融资事件、政策覆盖率须在过程 Steps 可见；不在结果页做链级对齐表复述；不随点选变化则禁止放右侧详情 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 各环节健康度 | 须按产业环节在图谱节点评分；禁止只给链级总分；禁止截断为仅瓶颈列表 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 卡脖子环节数（顶栏） | 与图谱节点「卡脖子」点位同词同计数；禁止用「断链风险」借词 | `metric_id: M_CHAIN_CHOKE_LINK_COUNT` |
| 图谱/详情等高 | 左图谱与右详情为关联主体；左侧高度按右侧对齐 | — |
| 时序说明 | V1 可固定可回放序列 + 降级说明；长说明进 `ReviewOnly` | — |
| 卡脖子 / 归因 | 节点自动标记 + 点选后成因/改进建议（政策/项目设计）；证据绑定 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |

禁止：前端自定维度/阈值；无依据解决路径；业务模式展示未标注 Mock 结论；过程删除 Bid 能力词；主区以纸质报告体替代图谱；跳转全景冒充。

评审挂点：
- `CHAIN-DIAG-F04-BOTTLENECK-TITLE`（requirement_trace）
- `CHAIN-DIAG-F04-BOTTLENECK-COUNT`（missing_metric_entry）
- `CHAIN-DIAG-F04-PROCESS-STAGES`（requirement_trace）
- `CHAIN-DIAG-F04-LINK-HEALTH`（missing_metric_entry）
- `CHAIN-DIAG-F04-DIMENSION-READONLY`（pending_decision）

## 7. F-DIAG-05 诊断记录

```text
┌─ 诊断记录 ────────────────────────────────────────────────────────┐
│ 过滤：对象 / 类型(周期|关键环节|瓶颈) / 状态 / 时间                    │
│ 列表：任务摘要（含 objectSummary）→ [查看进度] [查看结果] [复制配置] │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 动作 | 规则 |
| --- | --- |
| 查看结果 | 进入对应 Tab 不可变结果；**须恢复任务快照分析对象**；禁止因对比篮为空显示「未选分析对象」 |
| 查看进度 | 过程壳元信息取自任务快照 |
| 复制配置新建 | 回到配置草稿；不复制任务中心内部阶段实现 |

禁止：复制共享任务中心内部阶段实现；跨模块历史混排而不标注类型；从记录打开结果后丢失分析对象名称。

评审挂点：`CHAIN-DIAG-F05-RECORDS`（requirement_trace）。

## 8. 响应式

- 1920 / 1680：参数卡片 4 列；五维可 5 列；结果图表并排。  
- 1440：参数/五维可折行；结果上下堆叠。  
- 不声明专题小屏 `small_reflow`。

## 9. 状态覆盖（每业务 Frame）

`empty_object` / `loading` / `config_invalid` / `permission_locked` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `partial_evidence_gap` / `error_retry`。

## 10. 模块排除

全景图谱、区域评价、深圳决策、门户总览、技术链、模型训练控制台、可操作联网检索控制台、页内 PDF 引擎、正式可编辑权重阈值。

## 11. review_trace_contract

| mount_id | frame_id | marker_type | BusinessMode |
| --- | --- | --- | --- |
| CHAIN-DIAG-F01-OBJECT-CONTEXT | F-DIAG-01 | requirement_trace | absent |
| CHAIN-DIAG-F02-CYCLE-TITLE | F-DIAG-02 | requirement_trace | absent |
| CHAIN-DIAG-F02-CYCLE-STAGE | F-DIAG-02 | missing_metric_entry | absent |
| CHAIN-DIAG-F02-PROCESS-STAGES | F-DIAG-02 | requirement_trace | absent |
| CHAIN-DIAG-F02-RETRIEVAL-SNAPSHOT | F-DIAG-02 | requirement_trace | absent |
| CHAIN-DIAG-F02-DECISION-BRIEF | F-DIAG-02 | requirement_trace | absent |
| CHAIN-DIAG-F02-CYCLE-COMPARISON | F-DIAG-02 | pending_decision | absent |
| CHAIN-DIAG-F03-KEY-TITLE | F-DIAG-03 | requirement_trace | absent |
| CHAIN-DIAG-F03-KEY-COUNT | F-DIAG-03 | missing_metric_entry | absent |
| CHAIN-DIAG-F03-PROCESS-STAGES | F-DIAG-03 | requirement_trace | absent |
| CHAIN-DIAG-F03-HIGH-END-INDEX | F-DIAG-03 | missing_metric_entry | absent |
| CHAIN-DIAG-F03-FACTOR-READONLY | F-DIAG-03 | pending_decision | absent |
| CHAIN-DIAG-F04-BOTTLENECK-TITLE | F-DIAG-04 | requirement_trace | absent |
| CHAIN-DIAG-F04-BOTTLENECK-COUNT | F-DIAG-04 | missing_metric_entry | absent |
| CHAIN-DIAG-F04-PROCESS-STAGES | F-DIAG-04 | requirement_trace | absent |
| CHAIN-DIAG-F04-LINK-HEALTH | F-DIAG-04 | missing_metric_entry | absent |
| CHAIN-DIAG-F04-DIMENSION-READONLY | F-DIAG-04 | pending_decision | absent |
| CHAIN-DIAG-F05-RECORDS | F-DIAG-05 | requirement_trace | absent |

共 **18** 个唯一宿主。

## 12. 自检

1. 每 Frame 有路由、故事、字段、状态、禁止行为。  
2. 统计值均有 `metric_gap_ref` 或后续正式 metric_id。  
3. 「资本」口径与五维只读可见（不得用「资金」替代维名）。  
4. BusinessMode 全 absent。  
5. 排除项明确。  
