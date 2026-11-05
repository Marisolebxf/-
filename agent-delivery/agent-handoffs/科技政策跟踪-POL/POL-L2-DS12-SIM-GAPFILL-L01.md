# POL-L2-DS12-SIM-GAPFILL-L01 · 科技政策推演结果表与参与意见表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 注册表已由淮政玮认领并处于 `in_progress`。本会话不改 task-registry，不把任务标成 done |
| 说明 | 执行角色 `agent:data-agent`。只提交 `lumen-algo-py` 本地 commit，不 push |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `seed_gapfill_policy_eval_viz.py` 的两表 `--check` / `--apply`。未另起框架。未用 YAGNI 跳过 D16 列 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS12-SIM-DATA.md` 第 2、8、11 节。库只允许 `gkxlumenx_gapfill`。两张表不合并。不灌文本解析，不为 237 建表，不为 240 建表，不灌 PDF / Word / 文件路径。不改 D4，不新造 `metric_id`。`metric_id` 写 NULL。

### 结果表 `gapfill_policy_sim_result`（20 行）

| 行种类 | 行数 | `gap_item` | 拣行 |
|---|---|---|---|
| 多维评估 | 4 | `235 多维度效果评估` | `policy_id` 为 NULL。经济 78.2500、社会 71.5000、环境 66.0000、创新 74.7500，各有一句说明 |
| 重点 | 4 | `238 政策重点可视化展示` | `policy_id=18363390`。四组各一行：政策目标、支持领域、实施路径、资金安排 |
| 影响范围 | 3 | `239 政策影响范围分析` | 同一 `policy_id`。受益对象、影响区域、影响行业各一行。每行有 `time_change_text` 与 `region_text` |
| 路径环节 | 5 | `241 政策实施路径预测` | 同一 `policy_id`。政策发布、申报受理、评审评估、资金拨付、效果评估各一行 |
| 解读段落 | 4 | `242 政策解读报告生成` | 同一 `policy_id`。政策背景、主要内容、预期效果、实施建议。正文只在 `body_text` |

`18363390` 与预测表新出台预测的一个业务键相同，来源是 `scripts/seed_gapfill_policy_cmp.py`。`18407696` 只有预测行，本表不挂重点、影响范围、路径、解读。按该 `policy_id` 查询时这些区为空。

### 意见表 `gapfill_policy_sim_stakeholder`（3 行）

行种类只有 `参与意见`。请求种类是利益攸关方，不是 `row_kind`，也不另开列。不设 `policy_id`。

| 主体 `actor_role` | 渠道 `channel_name` | `opinion_at` |
|---|---|---|
| 决策者 | 在线问卷 | 2026-01-15 10:00:00 |
| 评估者 | 意见征集 | 2026-02-20 14:30:00 |
| 利益攸关方 | 专家评审 | 2026-03-18 09:15:00 |

主体闭集是决策者、评估者、利益攸关方。三种都出现。渠道闭集是在线问卷、意见征集、专家评审。`gap_item` 固定 `236 利益攸关方参与评估`。`opinion_at` 与 `generated_at` 分列。生成的 SQL 与行数据不用「利益低关方」；脚本把这个错写放进 SQL 禁止表。

每行 `is_mock=1`，`fill_method=manual`，`metric_id` 为 NULL，`gapfill_batch_id=POL-L2-DS12-SIM-GAPFILL-L01`，`generated_at=2026-11-06 01:00:00`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| `--apply` 未连上库 | 本会话环境没有 `LUMEN_ALGO_MYSQL_PASSWORD`。不改连接信息，不把口令写入 git | SQL 已落盘。有口令后同一条 `--apply` 可建表灌数 |
| 重点等只挂 `18363390` | 派单要求与 233 相同的一个 `policy_id`。233 有两行，本表取其中一行 | `18407696` 的重点、影响范围、路径、解读为空 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sim_result.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_sim_result.sql`
- 本 handoff（只在编排仓工作区，未提交）

本地 commit：`eb5e7d640f9a3f7b9bedc6e3545286fa645baf77`。未 push。

## 验收证据

在 `repos/lumen-algo-py` 执行：

```
python scripts/seed_gapfill_policy_sim_result.py --check
```

退出码 0：

```
{"mode": "check", "ok": true, "db": "gkxlumenx_gapfill", "rows": {"gapfill_policy_sim_result": 20, "gapfill_policy_sim_stakeholder": 3}, "sql": "E:\\zhipu\\gkx-lumen\\repos\\lumen-algo-py\\scripts\\mysql\\gapfill_policy_sim_result.sql"}
```

```
python scripts/seed_gapfill_policy_sim_result.py --apply
```

退出码 2：

```
{"mode": "apply", "connected": false, "reason": "no password"}
```

`--check` 锁住：结果表五种闭集与上表行数；多维评估四维各一行且 `policy_id` 为空、得分不是 0 占位；重点四组；影响范围三类且时间变化、区域原文都有值；路径五环节、解读四段各自唯一；意见表 3 行、三种主体、三种渠道、`row_kind=参与意见`、`gap_item` 三行都是 `236 利益攸关方参与评估`；意见表 DDL 无 `policy_id`；`18363390` 出现在预测脚本中；SQL 不出现文本解析、文件路径、`gkxlumenx_ads`、`M_POLICY_`、错写「利益低关方」。

## 架构合规自检

- D16：两张表都在 `gkxlumenx_gapfill`，行上带各自追溯列，`metric_id` 留空
- 未写 ODS、DWD、ADS、供应方库，未改 `policy_text_parse`
- 237 不灌，240 不建表，242 只有正文
- 未调用 `polan.text.parse.run`、`polan.text.simulate.run`
- 未改 D4，未新造 `metric_id`，未把 `M_POLICY_SIMULATE` 写入这两张表
- 未把布局推荐、评价页方案、受众反馈拷进这两张表

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 40000 |
| model_used | grok-4.7 |
| actual_cost | 0.20 |
| cost_warn | green |

估算。本会话不回写注册表。与 EST 灌数单同一会话，数字按单分列，不是两倍实测。

## CI/CD

- 分支：`lumen-algo-py` `dev`，本地超前 `origin/dev` 2、落后 14。未 pull，未 push
- commit：`eb5e7d640f9a3f7b9bedc6e3545286fa645baf77`
- pipeline：未推送，无
- 部署：无

## 未做的事

- 未把任务标成 done
- 未改同仓他人未提交文件：`k8s/README.md`、`scripts/mysql/gapfill_policy_eval_template.sql`

## 总控推送

2026-11-06 三仓都落地后推 `lumen-algo-py` `origin/dev`。提交 `eb5e7d640f9a3f7b9bedc6e3545286fa645baf77` 已在远端。`--apply` 仍未执行，两张表未灌进库。
