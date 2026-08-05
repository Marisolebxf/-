# Wireframe-CHAIN-TOPIC-REGIONAL｜区域产业评价

> **版本**：v1.0-package-split  
> **状态**：核心产品包 Wireframe；`ready_for_v1: true`  
> **体验 Owner**：高颖  
> **screen_tier**：`medium_1440_1920`  
> **边界**：本文件为区域产业评价唯一结构基线；父包 `F-CHAIN-07/08` 仅溯源。

## 1. Frame 清单

| Frame | 路由 / 宿主 | 目标 | 故事 |
| --- | --- | --- | --- |
| `F-REG-01` | `/industry-center/regional` | 工作区壳、对象上下文、Tab | 全部 |
| `F-REG-02` | `?tab=index` | 指数配置 / 结果 | `US-CHAIN-REG-01/02` |
| `F-REG-03` | `?tab=competitiveness` | 竞争力配置 / 结果 | `US-CHAIN-REG-03/04` |
| `F-REG-04` | `?tab=records` | 分析记录 | `US-CHAIN-REG-05` |

## 2. 统一骨架与状态机

- 壳层：页标题「区域产业评价」+ 对象上下文条 + 一级 Tab（指数 / 竞争力 / 分析记录）。
- 工作态：`no_object` → `config` → `task_created` / `processing`（共享壳）→ `result`；记录态独立。
- 两业务 Tab 共享兼容产业对象；区域、指标、权重、预览、结果焦点隔离。
- 点击「生成分析」才创建任务；结果须显式「查看分析结果」；禁止自动跳转。

## 3. F-REG-01 工作区壳与对象上下文

```text
┌─ 区域产业评价 ───────────────────────────────────────────────────┐
│ 分析对象：{产业摘要} | [打开对比篮]                                 │
│ Tabs: 区域产业指数评价 | 区域产业竞争力评价 | 分析记录              │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 |
| --- | --- |
| 产业对象摘要 | 来自共享篮兼容产业；无效时空态文案引导打开对比篮 |
| Tab | `index` / `competitiveness` / `records`；写入 URL |

状态：`no_object` / `object_ready` / `permission_locked` / `unavailable`。  
禁止：页内私有产业 Select；区域入篮；模块自建浮层篮。

评审挂点：`CHAIN-REG-F01-OBJECT-CONTEXT`（requirement_trace；BusinessMode absent）。

## 4. F-REG-02 区域产业指数配置与结果

```text
┌─ 区域产业评价 / 指数评价 ─────────────────────────────────────────┐
│ 模式：单产业×多区域 | 多产业×单区域                                  │
│ 区域选择（1~5 或 1）| 预设指标勾选 | 权重=100% | 个人模板            │
│ [轻量预览] [生成分析]                                               │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 综合指数 | 维度对比 | 指标贡献 | 优势短板 | [查看配置] [生成报告]   │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| `industry_ids` / `region_codes` | 仅 1×1、1×2~5、2~5×1 | — |
| 预设指标与权重 | 勾选；合计 100%；不删库项 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |
| 自定义指标 | 本轮不开放，显式差异 | `gap_ref: GAP-CHAIN-REG-CUSTOM-METRIC` |
| 预览值 | 不入任务历史、不占并发 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |
| 综合指数 / 贡献 / 优势短板 | 不可变结果 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |

禁止：多产业×多区域；静默归一化权重；预览写入分析记录；区域入篮；创建/删除指标。

评审挂点：
- `CHAIN-REG-F02-INDEX-TITLE`（requirement_trace）
- `CHAIN-REG-F02-INDEX-METRICS`（missing_metric_entry）
- `CHAIN-REG-F02-CUSTOM-METRIC-GAP`（pending_decision）
- `CHAIN-REG-F02-PREVIEW`（requirement_trace）

## 5. F-REG-03 区域竞争力配置与结果

```text
┌─ 区域产业评价 / 竞争力 ───────────────────────────────────────────┐
│ 对象组合（同指数合同）| 企业能力 / 学术生态 / 配套环境（固定）      │
│ 一级权重=100% | [一键均分]                          [生成分析]      │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 综合排名 | 三维对比 | 热力图 | 优势短板 | 版本边界 | [生成报告]     │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| 对象组合 | 同 F-REG-02 | — |
| 三大一级维度和权重 | 维度固定，只调一级权重 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |
| 综合指数 / 排名 / 热力图 | 同模型与权重版本才可比较 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |

禁止：新增/删除一级维度；降成两维；人工覆盖排名；跨版本混排。

评审挂点：
- `CHAIN-REG-F03-COMPETITIVENESS-TITLE`（requirement_trace）
- `CHAIN-REG-F03-COMPETITIVENESS-METRICS`（missing_metric_entry）
- `CHAIN-REG-F03-VERSION-BOUNDARY`（requirement_trace）

## 6. F-REG-04 分析记录

```text
┌─ 分析记录 ────────────────────────────────────────────────────────┐
│ 过滤：对象 / 类型(指数|竞争力) / 状态 / 时间                        │
│ 列表：任务摘要 → [查看进度] [查看结果] [复制配置新建]               │
└────────────────────────────────────────────────────────────────────┘
```

禁止：复制共享任务中心内部阶段实现；跨模块历史混排而不标注类型。

评审挂点：`CHAIN-REG-F04-RECORDS`（requirement_trace）。

## 7. 响应式

- 1920 / 1680：配置区单列主宽；结果图表并排。  
- 1440：结果区图表上下堆叠；权重控件保持可编辑。  
- 不声明专题小屏 `small_reflow`。

## 8. 状态覆盖（每业务 Frame）

`empty_object` / `loading` / `config_invalid` / `permission_locked` / `previewing` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `incomparable` / `partial_metric_gap` / `error_retry`。

## 9. 模块排除

全景图谱、诊断三项、深圳两项、门户总览、技术链、区域入篮、指标库后台维护、模型训练、页内 PDF 引擎。

## 10. review_trace_contract

| mount_id | frame_id | marker_type | BusinessMode |
| --- | --- | --- | --- |
| CHAIN-REG-F01-OBJECT-CONTEXT | F-REG-01 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-TITLE | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-METRICS | F-REG-02 | missing_metric_entry | absent |
| CHAIN-REG-F02-CUSTOM-METRIC-GAP | F-REG-02 | pending_decision | absent |
| CHAIN-REG-F02-PREVIEW | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F03-COMPETITIVENESS-TITLE | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F03-COMPETITIVENESS-METRICS | F-REG-03 | missing_metric_entry | absent |
| CHAIN-REG-F03-VERSION-BOUNDARY | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F04-RECORDS | F-REG-04 | requirement_trace | absent |

共 **9** 个唯一宿主。

## 11. 自检

1. 每 Frame 有路由、故事、字段、状态、禁止行为。  
2. 统计值均有 `metric_gap_ref` 或后续正式 metric_id，无伪口径。  
3. 自定义指标 Gap 可见。  
4. BusinessMode 全 absent。  
5. 排除项明确。  
