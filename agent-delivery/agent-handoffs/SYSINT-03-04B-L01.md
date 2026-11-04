# SYSINT-03-04B-L01 · 政策扶持力度排名

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | `ALGO-LIB-POL-PORTAL-LUMEN-L01` 已有 handoff 且为 integration。不等签收。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 排名只聚合已有评分。没有新 metric_id。十条计算未改语义。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 按契约「按省、按市聚合该评分」实现，未用压缩代替。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。计算在 Python `/internal/policy/indicators` |
| 会签态 | 技术方案 §2.2 为 `draft` |
| 说明 | 无分则空，不用力度指数顶排名。 |

## 范围与实现

`kind=all` 增加 `intensity_rank`。只取 `policy_intensity` 里 `metric_id=M_POLICY_INTENSITY_SCORE` 且 `scope_type=policy` 的分，用政策 `region` 归到省、市，名次按平均分。每行仍带这个评分 ID，没有省级排名 ID、城市排名 ID。

`M_POLICY_INTENSITY_INDEX` 不进排名。没有可聚合的分时 `province` / `city` 为空，并写原因。`portal_intensity.mock` 默认 `false`。打开且没有分时才给带 `mock` 的示例名次。

`portal_gaps` 十条仍在，本单不把序列删成空。

## 偏离

无。没有改契约，没有改种子。

## 产物清单

- `vendor/entan-py/polan/basic/indicators.py`（`portal_intensity_ranks`）
- `vendor/entan-py/api/policy_routes.py`
- `vendor/entan-py/conf/settings_policy.yaml`
- `vendor/entan-py/polan/common/config.py`
- `tests/test_policy_portal_gaps.py`

## 验收证据

`python -m pytest tests/test_policy_portal_gaps.py -q`：13 passed（2026-11-04 复跑 17 passed，后续 policy 提交带来的同文件增量用例一并全绿）。覆盖：指数行不进排名；无分时空列表；有分时省、市名次带 `M_POLICY_INTENSITY_SCORE`；有排名时十条 key 仍在。

【2026-11-04 线上联调补充（本由 algorithm-agent 代 04B 收尾）】
- 代码早已随后续 policy 提交上 dev（`intensity_rank` 在 `vendor/entan-py/polan/basic/indicators.py:637` + `policy_routes.py:605`）；note「未提交」为 2026-10-24 过期信息。
- dev 网关实测 `GET http://10.50.69.111:30895/policy/topic/v1/policy/indicators?kind=all`（HTTP 200，448KB）：
  - `intensity_rank`：`metric_id=M_POLICY_INTENSITY_SCORE`、`mock=false`、province/city 各 0 行 + reason「没有 M_POLICY_INTENSITY_SCORE 可聚合的政策行」——源表无评分行为空并写明原因 ✅（DoD-3）
  - `portal_gaps` 十条 key 齐、`reason` 全带；national 20008/series 348、node_coverage 99.1、sz_node_coverage 0.0（事实如实，不补 0 不造数）✅（DoD-2）
  - DoD-1 聚合只挂 `M_POLICY_INTENSITY_SCORE` ✅；未改 `PORTAL-CMS-政策扶持.md`、未调 demo-* ✅

## 架构合规自检

| 项 | 结果 |
|---|---|
| 算法在 Python | ✅ |
| 不调用 demo-* | ✅ |
| 不新注册排名 ID，不改 QPOL-02 | ✅ |
| 无行则空并写原因 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |
