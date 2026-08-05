# Wireframe-CHAIN-TOPIC-SHENZHEN｜深圳产业决策

> **版本**：v1.0-package-split  
> **状态**：`ready_for_v1: true`  
> **screen_tier**：`medium_1440_1920`  
> **边界**：本文件为深圳产业决策唯一结构基线；父包 `F-CHAIN-09/10` 仅溯源。

## 1. Frame 清单

| Frame | 路由 | 目标 | 故事 |
| --- | --- | --- | --- |
| `F-SZ-01` | `/industry-center/shenzhen` | 壳、对象上下文、Tab | 全部 |
| `F-SZ-02` | `?tab=comparison` | 对比配置/结果 | `US-CHAIN-SZ-01/02` |
| `F-SZ-03` | `?tab=development` | 发展配置/结果 | `US-CHAIN-SZ-03/04` |
| `F-SZ-04` | `?tab=records` | 分析记录 | `US-CHAIN-SZ-05` |

## 2. 统一骨架

- 标题「深圳产业决策」+ 产业对象上下文 + Tab（情况对比 / 发展分析 / 分析记录）。
- 状态：`no_object` → `config` → `task_created`/`processing` → `result`。
- 显式「生成分析」建任务；显式「查看分析结果」；禁止自动跳转与自动跑发展分析。

## 3. F-SZ-01 工作区壳

```text
┌─ 深圳产业决策 ───────────────────────────────────────────────────┐
│ 分析对象：{产业} | 主体：深圳（固定） | [打开对比篮]               │
│ Tabs: 情况分析对比 | 发展分析 | 分析记录                            │
└────────────────────────────────────────────────────────────────────┘
```

禁止：更换主体为非深圳；页内私有产业 Select；模块私有篮。

挂点：`CHAIN-SZ-F01-OBJECT-CONTEXT`（requirement_trace；BusinessMode absent）。

## 4. F-SZ-02 情况对比

```text
┌─ 深圳产业决策 / 情况对比 ─────────────────────────────────────────┐
│ 主体：深圳（固定） | 产业：1 | 标杆区域：1~5 | 四维模型（只读）    │
│ 区域就绪矩阵                                      [生成分析]        │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 四维对比 | 综合结论 | 优势差距 | 产业化潜力 | 发展阶段 | [生成报告]│
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 | gap |
| --- | --- | --- |
| 主体 | 固定深圳 | — |
| `industry_id` | 恰好 1 | — |
| benchmarks | 1～5；不可用保留原因 | — |
| 企业/专利/政策/人才 | 只读确认 | `GAP-CHAIN-SZ-METRICS` |
| 潜力/阶段/优势差距 | 不可变 | `GAP-CHAIN-SZ-METRICS` |

禁止：静默删不利标杆；无结构化合同时冒充可喂给发展分析。

挂点：`CHAIN-SZ-F02-COMPARE-TITLE`、`CHAIN-SZ-F02-COMPARE-METRICS`、`CHAIN-SZ-F02-BENCHMARK-READY`。

## 5. F-SZ-03 发展分析

```text
┌─ 深圳产业决策 / 发展分析 ─────────────────────────────────────────┐
│ 产业：1 | 来源：有效深圳对比结构化结果（显式选择）                  │
│ 目标：政策 / 技术 / 人才                            [生成分析]      │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ 三类建议 | 路径A | 路径B（≥2） | 依据 | 适用条件 | 局限性 | 报告   │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 | gap |
| --- | --- | --- |
| `source_result_id` | 同产业、有效、有权、结构兼容 | — |
| 目标三维 | 用户显式确认 | — |
| 建议与路径 | 绑定来源快照；路径≥2 | `GAP-CHAIN-SZ-METRICS` |
| 全球案例 | 本轮不宣称交付 | `GAP-CHAIN-SZ-CASE-LIBRARY` |

禁止：PDF 作输入；自动继承最近对比；项目/预算/排期/责任分派 UI。

挂点：`CHAIN-SZ-F03-DEV-TITLE`、`CHAIN-SZ-F03-DEV-EVIDENCE`、`CHAIN-SZ-F03-SOURCE-RESULT`、`CHAIN-SZ-F03-CASE-GAP`。

## 6. F-SZ-04 分析记录

过滤：对象 / 类型(对比|发展) / 状态 / 时间。  
动作：查看进度 / 查看结果 / 复制配置新建。  
挂点：`CHAIN-SZ-F04-RECORDS`。

## 7. 响应式

1920/1680 图表并排；1440 可上下堆叠；不声明专题小屏。

## 8. 状态覆盖

`empty_object` / `loading` / `config_invalid` / `permission_locked` / `no_benchmark` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `source_invalid` / `incomplete_paths` / `stale_benchmark_note` / `error_retry`。

## 9. 排除

全景/诊断/区域评价、门户总览、技术链深圳页、执行跟踪工具、页内 PDF 引擎回灌。

## 10. review_trace_contract

| mount_id | frame_id | marker_type |
| --- | --- | --- |
| CHAIN-SZ-F01-OBJECT-CONTEXT | F-SZ-01 | requirement_trace |
| CHAIN-SZ-F02-COMPARE-TITLE | F-SZ-02 | requirement_trace |
| CHAIN-SZ-F02-COMPARE-METRICS | F-SZ-02 | missing_metric_entry |
| CHAIN-SZ-F02-BENCHMARK-READY | F-SZ-02 | requirement_trace |
| CHAIN-SZ-F03-DEV-TITLE | F-SZ-03 | requirement_trace |
| CHAIN-SZ-F03-DEV-EVIDENCE | F-SZ-03 | missing_metric_entry |
| CHAIN-SZ-F03-SOURCE-RESULT | F-SZ-03 | requirement_trace |
| CHAIN-SZ-F03-CASE-GAP | F-SZ-03 | pending_decision |
| CHAIN-SZ-F04-RECORDS | F-SZ-04 | requirement_trace |

共 **9** 个唯一宿主；BusinessMode 全 absent。

## 11. 自检

Frame/故事/禁止行为齐全；发展输入链显式；Gap 可见。  
