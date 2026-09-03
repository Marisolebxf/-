# DATA-ENT-DWD-ALIGN-DDL-L01 · 两库按清单 ALTER ADD

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

对 `gkxlumenx_dwd` 与 `demo_gkxlumenx_dwd` **缺哪列 ADD 哪列**；旧同义列不 DROP；live `gkx` 未改。

正式库已 ADD：extra 七列、财务 `main_business_revenue`/`total_profit`/`total_fixed_assets`、`news.original_url`、`bid.project_no`、专利宽列、`patent_history` 三列、`executive.data_source`。

demo 已 ADD：base 正式宽列（未加 `id`）、bid/invest 正式列名、`executive.gender`、`extra.data_source`、财务 `net_profit`+KPI、news `summary` 等、专利现网同义列。

## 产物清单

- 两库 information_schema 抽检：`stock_noun` / `project_no` / `original_url` / `net_profit` / `patent_invention_count` / `gender`+`data_source` 均在
- 本 handoff

## 验收证据

- 2026-09-03 `gkxlumenx-dwd-public` 先读后写再改回只读
- 抽检 SQL 见上；未 DROP 任何同义列
- live `gkx` 零 DDL

## 偏离

- demo 表未补技术主键 `id`（四类表「id 忽略」）
- 未把 `inv_external_id` ADD 进正式库（Q-WP3-27）
- extra 七列已在正式库，`reg_info` 补读留给现有 ETL 模块后续小补，本叶不改 Java、不改 ES 键名

## 测试结果

- 抽检列两库都在
- 连接已改回 read-only

## 遗留风险

- ALTER 后旧行新列为 NULL，等 GDF Wave B 洗
- 未触发 ES / 未洗数

## CI/CD

- 分支：orchestration `origin/dev`（文档/handoff）
- pipeline：`cicd: skip`
- K8s：不适用

## Cost 回填

见下节。

## 成本

- actual_tokens：18000
- model_used：cursor-grok-4.6
- actual_cost：0.10
- cost_warn：green

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 / 算法只在 Python | ✅ 只 ALTER DWD |
| 图谱 Nebula | ✅ 未写图 |
| 可观测性 | ✅ 无新服务 |
| CI/CD | ✅ 只推 `origin/dev` |
| demo2 只读 merge | ✅ 未 merge lumen |
| D12 | ✅ 未调 demo 服务；demo DWD 同套 ADD |
| GDF 不写 ES/nGQL | ✅ |
| Java 企业 API | ✅ 零改 |

## 涉及文件

- `13-现网DDL差集`（拟 ALTER 已执行）
- 本 handoff
