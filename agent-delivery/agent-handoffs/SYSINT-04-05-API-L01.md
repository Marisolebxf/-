# SYSINT-04-05-API-L01 · 门户政策扶持读接口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | `SYSINT-03-04B-L01` 与 `SYSINT-03-04C-L01` 均已有 handoff 且为 integration。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 一个读接口拼已有指标透传和时间线，没有第二套计算。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 字段沿用 04B / 04C，未用压缩代替契约。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。浏览器到 Java；指标再进 Python `/internal/policy/indicators`；时间线停在 Java |
| 会签态 | 技术方案 §2.2 为 `draft` |
| 说明 | 时间线按 04C 派单不调 Python。 |

## 范围与实现

`GET /topic/v1/policy/portal`

| 字段 | 来源 |
|---|---|
| `indicators` | Python `kind=all` 原样上送，含 `portal_gaps` 与 `intensity_rank` |
| `latest` | 时间线 `scope=latest` 的 `items`，五个字段 |
| `shenzhen_latest` | 时间线 `scope=shenzhen` 的 `items` |

排名 ID 只有 `M_POLICY_INTENSITY_SCORE`。无政策记录时两个列表为空。时间线 mock 默认关。不调用 demo 服务。

## 偏离

无。

## 产物清单

- `PolicyFacadeController` `/portal`
- `PolicyFacadeService` / `PolicyFacadeServiceImpl.portal`
- `PolicyFacadeServiceImplTest.portalPassesScoreRankAndKeepsEmptyTimeline`

## 验收证据

单测：Python 只被以 `kind=all` 调用；排名 ID 为 `M_POLICY_INTENSITY_SCORE`；mock 关时两个时间线为空。本机没有 JDK，测试没有跑起来。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 计算只走 lumen-algo-py `/internal/policy/indicators` | ✅ |
| Java 不写算法 | ✅ |
| 不调用 demo-* | ✅ |
| 时间线五个字段，无记录为空列表 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |
