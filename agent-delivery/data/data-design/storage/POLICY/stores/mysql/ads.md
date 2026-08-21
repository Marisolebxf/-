# POLICY · ADS（契约面）

```yaml
---
doc_id: POLICY-STORE-MYSQL-ADS
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: mysql
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> Java **只读**本层。DDL 细列见旧稿 v1 §3。库：`demo_gkxlumenx_ads`。`calc_batch_id` 前缀 `mock_` 区分 Mock。

## 指标表（v1 九张，搬树不改列语义）

| 表 | 用途 |
|---|---|
| `policy_level_dist` | 层级/总数/时效 |
| `policy_type_dist` | 类型分布 |
| `policy_timeseries` | 发布时序 |
| `policy_national_dist` | 分省 |
| `policy_sz_dist` | 深圳分区 |
| `policy_focus` | 焦点/机遇/关联 |
| `policy_intensity` | 力度/产业覆盖 |
| `policy_effect` | 效果/短板/布局 |
| `policy_metric_timeseries` | 三维/通用时序 |

## 图镜像（现网 as-built · 读兜底）

| 表 | 用途 |
|---|---|
| `policy_graph_node` | 点镜像；Nebula 失败时 `/v1/policy/graph` 可读 |
| `policy_graph_edge` | 边镜像 |

## 展示窗口消费（DS-10/11/12）

对照 [`../../windows/display-ds10-12.md`](../../windows/display-ds10-12.md)。KPI 不另建表。  
原型 `policyData.js` **不是**本层真源。

| metric / 页 | 表 |
|---|---|
| `M_POLICY_TOTAL_COUNT` / `LEVEL_DIST` / `VALIDITY_RATE` | `policy_level_dist` |
| `M_POLICY_TYPE_DIST` | `policy_type_dist`（QPOL-01 类别：科创/行业/园区/招商/人才） |
| `M_POLICY_TIMESERIES` | `policy_timeseries` |
| `M_POLICY_NATIONAL_DIST` / `SZ_DIST` | 对应两表 |
| `M_POLICY_FOCUS_*` / `OPPORTUNITY_*` / `RELATION_DEGREE` | `policy_focus` + 图 |
| `M_POLICY_INTENSITY_*` / `SUPPORT_STRENGTH` / `INDUSTRY_COVERAGE` | `policy_intensity` |
| `M_POLICY_EFFECT_*` / `SHORTBOARD_*` / `LAYOUT_*` / `IMPLEMENTATION_EFFECT` | `policy_effect` |
| `M_POLICY_INDUSTRY_FIT` 等三维 | `policy_metric_timeseries` |

舆情热力、浏览量、仿真多轮快照、条款树：**缺表**，见 OPEN-POLICY-DISP-*，禁止把 fixture 计数写入上表冒充 live。
