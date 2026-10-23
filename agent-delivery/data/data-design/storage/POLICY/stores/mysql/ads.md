# POLICY · ADS（契约面）

```yaml
---
doc_id: POLICY-STORE-MYSQL-ADS
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-10-23
engine: mysql
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> Java **只读**本层。DDL 细列见旧稿 v1 §3。库：`demo_gkxlumenx_ads`。`calc_batch_id` 前缀 `mock_` 区分 Mock。

## 表总览（as-built 16 张）

| 群 | 张数 | 产出模块 |
|---|---|---|
| 指标表 | 9 | `basic/indicators.py` · `eval/*` |
| 图镜像 | 2 | `graph/entity.py` |
| NER 结果 | 1 | `graph/entity.py` |
| 文本智能处理 | 3 | `text/*` |
| 产业关联镜像 | 1 | `industry_enrich.py`（自 DWD 同名表按政策同步） |

> 旧口径「九张指标表」只覆盖第一群。指标 / 图 / 文本的写入图见 [`../../etl/pipeline-dwd-to-ads.md`](../../etl/pipeline-dwd-to-ads.md)。`policy_industry_rel` 不在那 12 步里。

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

节点/边键与四类边语义见 [`../nebula.md`](../nebula.md)。

## NER 结果（1 张）

| 表 | 用途 | 关键列 |
|---|---|---|
| `policy_entity` | 政策核心实体抽取结果，图谱构建的上游 | `policy_id` · `entity_type` · `entity_name` · `attributes` json · `source_field` · `confidence` · `model_version` |

`entity_type` as-built 取值：`policy` / `level` / `type` / `org` / `region` / `time` / `keyword` / `industry` / `enterprise` / `talent` / `service`。`source_field` 记录该实体从 DWD 哪一列抽出，是 D9 血缘的字段级落点。

## 文本智能处理（3 张）

| 表 | 用途 | 关键列 |
|---|---|---|
| `policy_text_parse` | D1 政策文本解析：摘要 + 结构化要素 + 自动标签 | `policy_id` · `title` · `summary` · `structured_elements` json · `auto_tags` json · `model_version` |
| `policy_match` | D2 政策匹配推送：主体 ↔ 政策的匹配打分与理由 | `subject_type` · `subject_id` · `subject_name` · `policy_id` · `policy_title` · `match_score` · `match_reasons` json · `rank_no` |
| `policy_simulate` | D3 政策效果推演仿真：基线 vs 仿真值与曲线 | `scenario_id` · `scope_type` · `scope_code` · `params` json · `baseline_value` · `simulated_value` · `delta_rate` · `curve` json · `explanation` |

三张表均带 `model_version` + `calc_batch_id`，规则基线产物按 D9 须在 UI 标注模型版本。`policy_simulate` 目前只存**单轮**结果；多轮对比快照是 `OPEN-POLICY-DISP-05` 缺口，不要往本表塞。

## 产业关联镜像（1 张）

| 表 | 用途 | 关键列 |
|---|---|---|
| `policy_industry_rel` | DWD 同名表的只读镜像。列与 `demo_gkxlumenx_dwd.policy_industry_rel` 相同 | `id` · `policy_id` · `industry_name` · `industry_link_code` · `is_deleted` · `create_time` · `update_time` |

抽取写完 DWD 后，按 `policy_id` 删除 ADS 中该政策的行，再插入 DWD 当前行（含已逻辑删除行，`id` 不变）。Java 读本表。算法增量与图谱仍读 DWD。有效行：`is_deleted=0`。

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
