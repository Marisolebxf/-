# Wireframe-CHAIN-TOPIC-DIAGNOSIS｜产业运行诊断

> **版本**：v1.4-bottleneck-bid-vocab  
> **状态**：核心产品包 Wireframe；`ready_for_v1: true`  
> **体验 Owner**：高颖  
> **screen_tier**：`medium_1440_1920`  
> **边界**：本文件为产业运行诊断唯一结构基线；父包 `F-CHAIN-04/05/06` 仅溯源。  
> **修订**：瓶颈补齐 `.5.1`/`.5.2` 原文词汇面（时序数据、四核心指标、环节健康度、卡脖子/归因建议）。

## 1. Frame 清单

| Frame | 路由 / 宿主 | 目标 | 故事 |
| --- | --- | --- | --- |
| `F-DIAG-01` | `/industry-center/diagnosis` | 工作区壳、对象上下文、Tab | 全部 |
| `F-DIAG-02` | `?tab=cycle` | 周期配置 / 过程 / 结果 | `US-CHAIN-DIAG-01/02` |
| `F-DIAG-03` | `?tab=key-link` | 关键环节配置 / 过程 / 结果 | `US-CHAIN-DIAG-03/04` |
| `F-DIAG-04` | `?tab=bottleneck` | 瓶颈配置 / 过程 / 结果 | `US-CHAIN-DIAG-05/06` |
| `F-DIAG-05` | `?tab=records` | 诊断记录 | `US-CHAIN-DIAG-07` |

## 2. 统一骨架与状态机

- 壳层（对齐企业评估）：页标题「产业运行诊断」+ 对象上下文条 + 一级 Tab（产业周期 / 关键环节 / 瓶颈堵点 / 诊断记录）。
- 工作态：`no_object+config` → `config` → `processing`（页内可视化 Steps）→ `result`；记录态独立。
- **无分析对象时**：Tab 与各配置区参数仍完整展示；「生成分析」禁用并提示先选对象（同企业评估「先显配置、后绑对象」）。
- 三业务 Tab 共享兼容产业 ID；关键/瓶颈共享兼容链 ID；配置与结果焦点隔离；周期不消费链 ID。
- 点击「生成分析」才创建任务并进入可视化过程；结果须显式「查看分析结果」；**禁止自动跳转结果页**。
- 周期过程 Steps 使用 §4.1 Bid 词汇表；非可操作联网控制台。

## 3. F-DIAG-01 工作区壳与对象上下文

```text
┌─ 产业运行诊断 ───────────────────────────────────────────────────┐
│ 分析对象：{摘要} | 空态引导 + [打开对比篮]                          │
│ Tabs: 产业周期 | 关键环节 | 瓶颈堵点 | 诊断记录  ← 无对象时也显示   │
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
│ 参数卡片：市场规模 | 增长率 | 利润率 | 技术成熟度                     │
│ 模型/数据版本                                      [生成分析]      │
├─ 共享任务过程壳（生成后）──────────────────────────────────────────┤
│ Steps：见 §4.1 Bid 词汇阶段（只读进度）                              │
│ V1 降级条：当前为固定可回放检索快照 · 待正式联网检索与模型接通        │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 回溯—诊断—预测 | 当前阶段 | 阶段评分 | 驱动因素 | 拐点 | 决策摘要   │
│ 检索来源与快照 | [查看配置] [生成报告]                              │
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
| `industry_id` | 单选产业 | — |
| 四参数 | 可调；提交时冻结快照 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 过程 Steps | 必须使用 §4.1 词汇；只读，非联网控制台 | — |
| 检索快照 / V1 降级 | 未接通时固定可回放 + 待接通说明；禁止完成态假话 | `gap_ref: GAP-CHAIN-DIAG-API` |
| 回溯—诊断—预测 / 驱动 / 拐点 | 不可变结果 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |

禁止：未点按钮自动建任务；「已完成实时全网检索」；可操作联网控制台；静默刷新过期结果。

评审挂点：
- `CHAIN-DIAG-F02-CYCLE-TITLE`（requirement_trace）
- `CHAIN-DIAG-F02-CYCLE-STAGE`（missing_metric_entry）
- `CHAIN-DIAG-F02-PROCESS-STAGES`（requirement_trace）
- `CHAIN-DIAG-F02-RETRIEVAL-SNAPSHOT`（requirement_trace）
- `CHAIN-DIAG-F02-DECISION-BRIEF`（requirement_trace）

## 5. F-DIAG-03 关键环节配置与结果

```text
┌─ 产业运行诊断 / 关键环节 · 配置 ──────────────────────────────────┐
│ 注册因子只读：附加值率 | 技术壁垒 | 市场集中度 | 权重/阈值状态       │
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
| 代表企业 | 共享企业抽屉 | — |

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
│ 五维只读：技术 | 人才 | 市场需求 | 资本 | 政策 | 权重/阈值状态       │
│ 模型/数据版本（只读确认）                              [生成分析]  │
├─ 共享任务过程壳（生成后）──────────────────────────────────────────┤
│ Steps：见 §6.1 Bid 词汇阶段（只读进度）                              │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ .5.1 四核心指标 | 各产业环节健康度 | 五维健康矩阵 | 时序说明         │
│ 卡脖子/瓶颈标记 | 成因 | 影响 | 改进建议 | 趋势预警 | [报告交接]   │
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
| `.5.1` 四核心指标 | 技术成熟度、人才供给量、融资事件、政策覆盖率须可见 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 各环节健康度 | 须按产业环节评分；禁止只给链级总分 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |
| 时序说明 | V1 可固定可回放序列 + 降级说明 | — |
| 卡脖子 / 归因 | 自动标记 + 成因 + 改进建议（政策/项目设计）；证据绑定 | `metric_gap_ref: GAP-CHAIN-DIAG-METRICS` |

禁止：前端自定维度/阈值；无依据解决路径；业务模式展示未标注 Mock 结论；过程删除 Bid 能力词。

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
│ 列表：任务摘要 → [查看进度] [查看结果] [复制配置新建]               │
└────────────────────────────────────────────────────────────────────┘
```

禁止：复制共享任务中心内部阶段实现；跨模块历史混排而不标注类型。

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

共 **17** 个唯一宿主。

## 12. 自检

1. 每 Frame 有路由、故事、字段、状态、禁止行为。  
2. 统计值均有 `metric_gap_ref` 或后续正式 metric_id。  
3. 「资本」口径与五维只读可见（不得用「资金」替代维名）。  
4. BusinessMode 全 absent。  
5. 排除项明确。  
