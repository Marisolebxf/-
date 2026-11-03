# POL-L2-DS11-VIZ-TEMPLATE-L01 · 222 报告模板定制与批量导出 · 模板选用表建表与灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| 状态流转 | task-claim → in_progress → integration（note：代码已落盘，待签收） |
| 说明 | 派单授权提交脚本与 handoff 并推送 origin/dev |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `seed_gapfill_policy_eval_viz.py` 的 `--check`/`--apply` 幂等模式，未另起框架。未用 YAGNI 跳过 D16 追溯列 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS11-VIZ-DATA.md` 第 5 节与 `sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 第 5.4、9 节。范围只有 222 一张模板选用表。219、220 两张表由 `POL-L2-DS11-VIZ-GAPFILL-L01` 已建已灌，本单不碰。221 不建表。未写 ODS、DWD、ADS、供应方库，未改 D4，未新造 `metric_id`，未碰 `gapfill_policy_eval_shell`。

库目标是 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_template`，列逐列照 DATA 第 5 节（`template_name`/`report_period`/`analysis_dim`/`chart_kind` + 追溯列）。唯一键四列 `template_name + report_period + analysis_dim + chart_kind`（派单口径，即 DATA「同一模板多组合分多行」的机器化）。

### 模板选用行（10 行 / 6 模板）

一行是一条模板选用：一个模板名 + 该行允许的一个汇报周期、一个分析维度、一个图表类型。同一模板多种组合分成多行（DATA 第 5 节：不把多值用分隔符写进同一格；派单口径：唯一键按模板名，同模板多组合行即多行满足）。

| 模板名 | 周期 | 维度 | 图表 |
|---|---|---|---|
| 政策效果综合月报 | 月度 | 政策面 | 趋势 |
| 政策效果综合月报 | 月度 | 政策面 | 柱状 |
| 区域政策对比季报 | 季度 | 产业面 | 柱状 |
| 区域政策对比季报 | 季度 | 产业面 | 热力 |
| 资金投向跟踪季报 | 季度 | 资金面 | 柱状 |
| 资金投向跟踪季报 | 季度 | 资金面 | 趋势 |
| 年度政策全景报告 | 年度 | 政策面 | 趋势 |
| 年度政策全景报告 | 年度 | 产业面 | 关系网 |
| 政策要素关联年报 | 年度 | 政策面 | 弦线 |
| 产业链政策观察季报 | 季度 | 产业面 | 趋势 |

闭集（派单口径）：周期 月度/季度/年度（DATA 第 5 节明确周期不是闭集、由灌数单定合理值；不迁 demo 的近 1 年/近 3 年/近 5 年）；维度 政策面/资金面/产业面；图表 趋势/柱状/热力/弦线/关系网（五行全覆盖）。未收饼图、散点（ARCH 3.1 明确不迁）。

### 追溯列

每行 `is_mock=1`、`metric_id` 留空、`gap_item=222 报告模板定制与批量导出`、`fill_method=manual`、`gapfill_batch_id=POL-L2-DS11-VIZ-TEMPLATE-L01`、`generated_at` 取执行时刻。按 DATA 规定不设 `fill_model`，不设模板正文/编号/文件地址/对象键/PDF/Excel/操作日志列。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 维度值用 政策面/资金面/产业面，非 DATA 第 5 节列举的 时间/区域/类别/地区/行业/目标群体 | 派单明文给定闭集与分析维度示例 | 按派单口径执行 |
| `chart_kind` 每行单值，未做逗号多值 | DATA 第 5 节明确「不把多个图表类型用分隔符写进同一格」；派单「可多值逗号分隔」与真源冲突，取真源 | 每行单值，同模板多图表类型拆多行 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_template.py`（`--check` 不连库自检并覆写 SQL；`--apply` 连库建表+灌数，先 DELETE 再 INSERT 幂等）
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_template.sql`（DDL + 10 行 INSERT）
- 本 handoff

未改 `/display/v1/policy/**`、未改 Java、未改 D4、未新造 `metric_id`、未写 nGQL、未碰 `gapfill_policy_eval_shell` 与 219/220 两张表。

## 验收证据

- `--check`（2026-11-03，退出码 0）：`{"mode":"check","ok":true,"rows":{"gapfill_policy_eval_template":10,"templates":6,"periods":3,"dims":3,"chart_kinds":5}}`
- `--apply`：**未连库，待有权限会话执行**。本会话无 `LUMEN_ALGO_MYSQL_PASSWORD`（进程环境变量、编排仓 `.env`、lumen-algo-py `.env*` 均无），脚本按设计返回 `{"mode":"apply","connected":false,"reason":"no password"}` 退出码 2，未伪造行数
- 待执行命令（在 `repos/lumen-algo-py`，PowerShell，不用 `&&`）：

```
$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_eval_template.py --apply
```

自检在 `--check` 里（不连库），锁住：唯一键四列无重复；行数 8–12；周期/维度非空且在闭集（月度/季度/年度、政策面/资金面/产业面）；图表类型都在闭集（趋势/柱状/热力/弦线/关系网）；每行 `is_mock=1`、`metric_id` 空、`fill_method=manual`；SQL 只出现 `gkxlumenx_gapfill.gapfill_policy_eval_template` 一张 INSERT 目标表，不出现 shell/trend/partition/scheme 表名、`fill_model`、ODS/DWD/ADS、`M_POLICY_`。

## 架构合规自检

- ✅ D16：只写 `gkxlumenx_gapfill` 下 `gapfill_` 前缀表，行上带规定追溯列；未写 ODS、DWD、ADS、供应方库
- ✅ D18 可实现：接口不直接返回 mock，模板选用入表由 `gkxlumen-element` 只读
- ✅ 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- ✅ 未新造 `metric_id`
- ✅ 未碰 `gapfill_policy_eval_shell`（壳表只服务 224、225）
- ✅ 调用链：本单只灌库，不改 Java/展示/算法接口
- ✅ 图谱：未写 nGQL

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 60000 |
| model_used | glm-5.3 |
| actual_cost | 0.20 |
| cost_warn | green |

数字是估算。

## CI/CD

- 分支：`lumen-algo-py` `dev`（commit 见下方两仓提交）
- 库：**未连库**。`gkxlumenx_gapfill.gapfill_policy_eval_template` 待有权限会话 `--apply` 后建立
- pipeline：本单不跟发布
- 部署：无

## 未做的事

- 未连库执行 `--apply`（密码缺失，待有权限会话补跑）
- 未把任务标成 done；状态已在 integration，待签收
- 未改读取接口。读表是 `gkxlumen-element` 的事（`GET shells` 按模板读）
- 未改架构稿、DATA、说明书、注册表
- 未碰 219/220 两张表与 `gapfill_policy_eval_shell`、`gapfill_policy_eval_scheme`
