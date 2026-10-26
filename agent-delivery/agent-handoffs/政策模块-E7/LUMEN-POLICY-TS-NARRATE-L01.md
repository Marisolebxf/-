# LUMEN-POLICY-TS-NARRATE-L01 · 时序结果板之后的模型润色

> 设计：`05.6.1-政策时序分析.md` §5，FUNC-DESIGN §4.1.2。本叶只改时序 Job，不改区域对比和深圳三维。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 由 human:淮政玮 名下改由 algorithm-agent 执行。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 润色单独模块，接在 `build_timeseries_board` 返回之后。未改 `indicators.run()`，未改年序列和 headline 公式。 |

## 修改内容

- 新增 `polan/insight_narrate.py`。规则层先补「发布连续性」的 `pending_ref=QPOL-07`，并在 `key_nodes` 非空时追加「节点分布」草稿（`tone=flat`）。
- 模型只替换已有标题的 `text`。多出来的标题（增长率空时的「最近环比」）丢掉，不进结果。
- 无 Key：`narration.status=skipped`。超时、异常、坏 JSON、数字不在事实包、连续性丢掉「有发布年数 / 跨度年数」、出现「政策密度指数」或因果句：只退回该卡草稿。整单仍成功。
- 客户端本步 `timeout_sec=8`、`max_retries=0`、`temperature=0.1`。不改公共客户端默认值，不用 `web_search`。
- 失败不写 `honesty.degraded`，不改 `headline`、年序列、`key_nodes`、`policy_count`、`honesty.fabricated`。不写 `result_snapshot_id`。
- `job._run_timeseries_board` 在结果板成功后调用 `narrate_board`。测试注入 `_narrate_client`。Java 不传该字段。

## 测试结果

`lumen-algo-py`：`pytest tests/test_policy_narrate.py tests/test_timeseries_board.py tests/test_policy_job.py` → 28 passed。

## CI/CD

- 分支：`lumen-algo-py` `dev`，提交 `a58429e`
- 部署：本叶不点部署

## 遗留

- 已推 `origin/dev`，未点部署。线上 014 仍是润色上线前的结果。
- 05.6.1 第 6 步仍标未上线，等本叶发布后再改 as-built。
- 区域对比、深圳三维不在本叶。

## 涉及文件

- `vendor/entan-py/polan/insight_narrate.py`
- `vendor/entan-py/polan/job.py`
- `tests/test_policy_narrate.py`

## 架构合规

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 前端 → Java → `/internal/*` | ✅ Java 不调模型，只存 `result_payload` |
| 不改 `indicators.run()` | ✅ |
| 不改 Java `totalNodes` | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 60000 |
| model_used | grok-4.7 |
| actual_cost | 0.12 |
| cost_warn | green |
| 说明 | source: session_estimate。无 Console 的 in/out 分离值。 |
