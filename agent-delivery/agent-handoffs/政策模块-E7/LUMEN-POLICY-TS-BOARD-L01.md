# LUMEN-POLICY-TS-BOARD-L01 · 时序结果板四张卡

> 口径：[`LUMEN-POLICY-TS-CALIBER-L01.md`](./LUMEN-POLICY-TS-CALIBER-L01.md) 与总控 §0。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控。lock 24h。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改在线结果板和 Job 读中文名。未改 `indicators.run()`，未加标题过滤。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单测无大日志。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 未改图。仍只读 ADS 关联 + DWD 政策主表。 |
| 会签态 | `approved` |

## 修改内容

- `headline` 不再放 `M_POLICY_TIMESERIES`。末年发布条数改键 `latest_year_publish_count`。无跨度时为 `null`。
- 年序列 `density_trend` 仍是各年 `publish_count`。
- 增长率仍走 `growth_rate`：上一年为 0 或没有则为 `null`。
- `is_valid` 改为仅 `status` 为 `1` 或 `"1"`，且到期日空或未过今天。空状态不再算有效。
- `job._run_timeseries_board` 在 `match_object` 之前读 `industry_name`（body 或 `params`）。没有中文名时仍用 VID。
- 单测注入 `load_fn` 空列表。带 `industry_vid` 的聚合会合并库内关联行，不注入就会把现网 2 条算进夹具。

## 测试结果

`lumen-algo-py`：`pytest tests/test_timeseries_board.py tests/test_policy_job.py` → 20 passed。

## 留给前端（段 D）

现页面仍把 `headline.M_POLICY_TIMESERIES` 标成「政策密度指数」。该键已去掉。`policyTimeseriesResult.ts` 在密度为空时还会回退到 `M_POLICY_PEAK_YEAR_PUBLISH`（峰值年条数）。段 D 必须改读 `latest_year_publish_count`，并停掉这个回退。

## 遗留风险

- 未部署。已发布页在段 D 发版前仍显示旧标签；数值在只发算法、不发前端时，密度卡会空或落到峰值。
- 关联错配不在本叶过滤。见 `LUMEN-POLICY-TS-REL-L01`。

## CI/CD

- 分支：`lumen-algo-py` `dev`，提交见本叶收尾
- pipeline：随 push
- 部署：本叶不点部署

## 涉及文件

- `vendor/entan-py/polan/timeseries_board.py`
- `vendor/entan-py/polan/job.py`
- `tests/test_timeseries_board.py`
- `tests/test_policy_job.py`

## 架构合规

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 不改 `indicators.run()` | ✅ |
| 不按标题滤关联 | ✅ |
| Java 不写算法 | ✅ 本叶未改 Java |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | grok-4.7 |
| cost_warn | green |
| 说明 | source: session_estimate。无 Console 分离值，未按价表计 actual_cost。 |
