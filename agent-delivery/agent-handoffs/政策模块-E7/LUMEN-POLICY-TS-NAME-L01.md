# LUMEN-POLICY-TS-NAME-L01 · 时序任务传递产业中文名

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只把 `industry_name` 放到执行体顶层。未改任务号，未加新接口。 |

## 修改

`PolicyAnalysisAdapterImpl.buildExecuteBody`：创建参数里的 `industry_name` / `industryName` 写入 Python body 顶层。`params` 里原来就有这份字段。`taskName` 仍等于任务号。

## 测试

本地 Maven 按本次要求跳过。本机 Maven 3.6 也跑不了 3.14 编译插件。

线上（`http://10.50.69.111:30892`）：

- Java `dev` `e313d12`，流水线 2843，`deploy:topic-async-service` 成功。
- Python `dev` `85bd5a5`，流水线 2844。`deploy:entan-api` 原是手动，已点运行并成功。
- 创建 `POLICY-20261024-007`，`user_id=agent-ts-online`，`industry_vid=chain:INB170401`，`industry_name=高性能与前沿新材料`。
- 结果 `match_object` = `高性能与前沿新材料`。`taskName` = `POLICY-20261024-007`。
- `headline.latest_year_publish_count` = 2，没有 `M_POLICY_TIMESERIES`。2020 年 2 条，2019 年 0 条，增长率空。5 条政策 `status` 都是 1、无到期日，有效占比 100。

## 页面还差一段

当前页面创建参数仍只传 `industry_vid`。不改前端时，从页面点「开始分析」结果里的匹配对象还会是链码。卡片文案仍是「政策密度指数」，要等 `LUMEN-POLICY-TS-FE-L01`。

## CI

- Java：`e5c6d3b..e313d12` `origin/dev`
- Python：`daa6677..85bd5a5` `origin/dev`
- 部署命名空间：`zhipu-tts`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 25000 |
| model_used | grok-4.7 |
| cost_warn | green |
| 说明 | source: session_estimate。 |
