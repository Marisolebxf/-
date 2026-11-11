# POL-L2-DS11-VIZ-GAPFILL-L02 · 政策分析评价 Tab1 七可视化块缺项表灌数

- 任务：`POL-L2-DS11-VIZ-GAPFILL-L02`
- 日期：2026-11-12
- 执行：`agent:data-agent` · 监管：`human:淮政玮`
- ponytail: full
- 上游（列清单唯一真源）：`sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02-DATA.md`（严格照抄 §2/§4/§5，不自行发挥）
- 行内容种子对照：`lumen-ui-science-pc/src/mock/modules/policySeed.ts`（evaluationMetrics / policyPortraitSummaries / geographicDistributionData / implementationByRegionData / topicHeatmapData / topicSentimentSummary / bubbleChartData，语义对齐）
- 先例脚本：`seed_gapfill_policy_eval_viz.py`（L01，--check/--apply 双模式同构）

## 1. 范围与实现

| 项 | 内容 |
|---|---|
| 库 | `gkxlumenx_gapfill`（D19：建库建表显式 `CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci`） |
| 脚本 | `lumen-algo-py/scripts/seed_gapfill_policy_eval_viz2.py`（新增） |
| SQL | `lumen-algo-py/scripts/mysql/gapfill_policy_eval_viz2.sql`（--check 覆写，已生成） |

七张新表，全部 demo 复刻保留块（无 SRS 序号），`gap_item` 用「`DS11-VIZ ` + 块名」。每行 `is_mock=1`、`fill_method=manual`、`gapfill_batch_id='POL-L2-DS11-VIZ-GAPFILL-L02'`、`generated_at` 脚本生成、`metric_id=NULL`（禁抄任何 `M_POLICY_*`，DATA §5）。唯一性用表级 UNIQUE KEY 落实 DATA §4 各表约定。

## 2. 七表列摘要与行数

| 表 | gap_item | 关键列（拣行键加粗） | 行数 |
|---|---|---|---|
| `gapfill_policy_eval_viz_metric` | `DS11-VIZ 评估指标体系卡` | **dim_key** / dim_label / score_value / weight_pct / pending_ref | 5 |
| `gapfill_policy_eval_viz_portrait` | `DS11-VIZ 三联画像` | **portrait_type**（政策/企业/人才闭集） / title / subtitle / summary_text / kpi_label / kpi_value / kpi_unit / tags_text / detail_overview / detail_metrics_text / detail_highlights_text | 3 |
| `gapfill_policy_eval_viz_geo` | `DS11-VIZ 地理分布图` | **region_name** / policy_count / lng / lat / sample_policies_text | 10 |
| `gapfill_policy_eval_viz_region_impl` | `DS11-VIZ 分地区落实率` | **region_name** / implement_rate / funded_rate / declared_rate / delayed_count | 8 |
| `gapfill_policy_eval_viz_topic_heat` | `DS11-VIZ 话题热力图` | **topic_name + stat_month**（YYYY-MM） / heat_value | 96 |
| `gapfill_policy_eval_viz_topic_sentiment` | `DS11-VIZ 情感分布` | **scope_kind + topic_name** / positive_pct / neutral_pct / negative_pct / sample_size | 6 |
| `gapfill_policy_eval_viz_bubble` | `DS11-VIZ 产业影响力气泡图` | **bubble_name** / category / influence_value / attention_value / funding_amount / growth_rate | 8 |

合计 **136 行**。语义要点：

- metric 表恰 5 维（覆盖广度/深度力度/协同程度/实施效果/创新引领），权重合计 100，`pending_ref='QPOL-02'`（PE-B01 权重未确认）；**不灌总分行**（总分归 `gapfill_policy_sim_score` 页头卡读面）。
- sentiment 表总体恰 1 行（`sample_size=12840` 为占比口径留证）+ 5 分话题行，三列占比合计均为 100；分话题行 `sample_size` 留空（FE 未消费）。
- geo 表不灌政策流向连线、地图文件、geojson；不灌「全国」兜底行。
- 不落前端渲染常量（色阶阈值、轴范围、visualMap、类别配色均为前端行为）。

## 3. 命令与自检证据

```text
python scripts/seed_gapfill_policy_eval_viz2.py --check
```

--check JSON 原文（2026-11-12 实跑）：

```json
{"mode": "check", "ok": true, "db": "gkxlumenx_gapfill", "rows": {"gapfill_policy_eval_viz_metric": 5, "gapfill_policy_eval_viz_portrait": 3, "gapfill_policy_eval_viz_geo": 10, "gapfill_policy_eval_viz_region_impl": 8, "gapfill_policy_eval_viz_topic_heat": 96, "gapfill_policy_eval_viz_topic_sentiment": 6, "gapfill_policy_eval_viz_bubble": 8}, "sql": "E:\\zhipu\\gkx-lumen\\repos\\lumen-algo-py\\scripts\\mysql\\gapfill_policy_eval_viz2.sql"}
```

脚本内置校验：唯一键不重、权重合计 100、分值域 0–100、月份格式 YYYY-MM、sentiment 三列合计 100、总体行样本量必填、经纬度中国范围、禁词扫描（fill_model / M_POLICY_ / ODS / DWD / ADS / 总分 / 全国 等）、七表建表语句逐张核对 CHARSET/COLLATE。

## 4. 灌数命令与执行结果（--apply 已执行 ✅ 2026-11-12 主会话）

`--apply` 连库执行同一份语句（建库建表 + 灌行），不整表删除，可重复执行：

```powershell
$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_eval_viz2.py --apply
# 预期输出：{"mode":"apply","connected":true,"ok":true,"db":"gkxlumenx_gapfill","batch":"POL-L2-DS11-VIZ-GAPFILL-L02","rows":{...七表行数同 --check...}}
```

**实跑结果（2026-11-12 04:0x，库 10.50.11.76:3306，密码经编排仓 .env 注入，不进 git）**：

```json
{"mode": "apply", "connected": true, "ok": true, "db": "gkxlumenx_gapfill", "batch": "POL-L2-DS11-VIZ-GAPFILL-L02", "rows": {"gapfill_policy_eval_viz_metric": 5, "gapfill_policy_eval_viz_portrait": 3, "gapfill_policy_eval_viz_geo": 10, "gapfill_policy_eval_viz_region_impl": 8, "gapfill_policy_eval_viz_topic_heat": 96, "gapfill_policy_eval_viz_topic_sentiment": 6, "gapfill_policy_eval_viz_bubble": 8}}
```

**独立 SELECT 复核（与 --apply 分离的独立连接）**：七表行数 5/3/10/8/96/6/8（TOTAL 136）一致；`metric` 表血缘列断言 `is_mock=1 AND metric_id IS NULL AND pending_ref='QPOL-02'` 命中 5/5；`information_schema` 确认七表 collation 均 `utf8mb4_general_ci`（D19 7/7）。复核临时脚本已删。

> **首轮 --apply 曾失败（errno 1046 No database selected），已根修**：脚本连库 `database=None`（库可能尚不存在），但语句列表无 `USE`，建表/INSERT 落空。修法 = `CREATE DATABASE` 后补 `USE \`gkxlumenx_gapfill\`` 一行，同时自检断言语句计数 `1+7+rows` → `2+7+rows`。修后 --check 绿、--apply 绿、独立复核绿。

## 5. 架构合规自检

| 铁律 | 结果 |
|---|---|
| D16 只写 `gkxlumenx_gapfill`、`gapfill_` 前缀 | ✅ 七表均在 gapfill 库，不写 ODS/DWD/ADS/供应方库 |
| D18 行灌 `gapfill_` 表，接口不直返写死 mock | ✅ 灌的是表行，读方后续 Java 只读 |
| D19 显式 utf8mb4 / utf8mb4_general_ci | ✅ 建库 + 七张 CREATE TABLE 均显式声明 |
| metric_id 留空、不新造、不改 D4 | ✅ 全行 `metric_id=NULL`，`is_mock=1` |
| 不污染既有表（trend/partition/shell/scheme/sim_score） | ✅ 只 INSERT 七张新表，无 DELETE/TRUNCATE |
| 不碰 task-registry MCP、不 commit/push | ✅ 产物停本地，registry 与提交由主会话收口 |

## 6. 偏离说明

- **~~--apply 未执行~~ → 已由主会话执行**：子会话会话内无 `LUMEN_ALGO_MYSQL_PASSWORD` 停在 --check；主会话经编排仓 `.env` 注入密码后执行 --apply 成功（见 §4 实跑结果与独立复核）。首轮 1046 根修记录见 §4。
- **行内容非逐字复制种子**：数值与文本语义对齐 `policySeed.ts`（维度五元组、画像三段、地理十城、落实率八城、热力 8×12 满矩阵、情感总体+五话题、气泡八产业），多值文本列（tags/metrics/highlights/代表政策）按 DATA 列约束用顿号/分号并入单行，属 DATA §4 规定形状。
- **generated_at 为运行时生成**（先例 L01 为写死常量）：DATA §2 规定「行写入时间，由灌数单填写」，脚本生成更贴语义；同一次运行内各行一致。
- 其余列级定义、gap_item 固定值、唯一性约束均按 DATA 定稿，无偏离。

## 7. 新增文件清单

| 文件 | 说明 |
|---|---|
| `lumen-algo-py/scripts/seed_gapfill_policy_eval_viz2.py` | 灌数脚本（--check/--apply） |
| `lumen-algo-py/scripts/mysql/gapfill_policy_eval_viz2.sql` | 覆写产出的可执行 SQL |
| `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02.md` | 本 handoff |

## 8. cost（占位）

完工总控回填。
