# SYSINT-03-03B-L01 · 专题服务指标与主数据

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | COVER-SVC 已 done：11 注册件覆盖 13 行 + T1/T2 趋势翻案 + 4 归属行，0 物理缺口 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 svcan 既有 `compute_metric`（M_SVC_PT_* / M_SVC_ORG_TECH_SCORE）；不引新依赖；不改权重 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | COVER-SVC 18/18 物理行与契约 §1.1–§1.5 原文对照 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。新增只读门面 `/internal/v1/svcan/portal/{catalog,metrics}` |
| 会签态 | 技术方案 draft |
| 说明 | `svc_business_domain` 正文走 CMSOPS 写侧（03A-JAVA），本叶只指标；名称/领导人走主数据不覆盖 |

## 范围与实现

门户专题服务指标门面（`global` / `industry` / `region` / `tech` / `shenzhen`）：

1. **14 行已注册**（11 件 ID）：全部带 `metric_id`。趋势两行按 COVER T1/T2 挂总量件 ID + `trend_of` 指向序列面，**不新立趋势 ID**；技术力两行（前 30 / 名次分数）同用 `M_SVC_ORG_TECH_SCORE`，前 30 走降序截断，权重 Q-SVCCHAIN-01 未拍板不改。
2. **0 物理缺口行**（T1/T2 翻案后契约无剩余缺口格）；catalog 携带 4 项待拍决策注记。
3. `tech_limit` 可调（默认 30）；`nearby_metrics` 只用于拒绝改挂。

不改契约、不改种子/矩阵、不调 demo-*、不动 svcan 既有 10 个 `/portal/*` 端点。

## 偏离

- serve 行 value 大多为 null（D4 mock）；`M_SVC_ORG_TECH_SCORE` 两行真实调用 svcan compute（临时权重，诚实标注）。
- 历年趋势的序列数值本体（64 有值年 / 47 有值年）在 gkx 面可算，本门面未展开 series——接 ADS/真库后按 `trend_of` 补 series 字段即可，契约形状不变。

## 产物清单

| 仓 | 路径 |
|---|---|
| lumen-algo-py | `lumen_common/algorithms/svcan/portal_metrics.py` |
| lumen-algo-py | `lumen_algo_service/views/svcan.py`（`/portal/catalog` `/portal/metrics`） |
| lumen-algo-py | `tests/test_portal_svc_metrics.py` |
| gkx-orchestration | 本 handoff |

## 测试结果

`pytest tests/test_portal_svc_metrics.py tests/test_portal_chain_metrics.py tests/test_portal_ent_metrics.py -q` → **22 passed**（58.7s）。

覆盖：catalog 14+0；趋势不新立 ID（T1/T2）；技术力单 ID 双行 + 截 30；page_key 过滤；邻近不填空态；HTTP 往返。01B/02B 回归同绿。

未做线上联调；代码停本地，待监管人验收后 commit/push。

## 遗留风险

- Q-SVCCHAIN-01（权重/名单）、SVC-P0-3（供方成员表）、Q-SVCCHAIN-07（海外边界）未拍：对应行按现有口径出数带注，不升绿。
- 技术力榜真实调用 svcan compute 在无 DB 环境会走 mock fallback（`data_source=mock`），诚实不造假。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 算法在 Python | ✅ |
| 调用链 Feign `/internal/*` | ✅ |
| 不调用 demo-* | ✅ |
| 缺口不手填 / 不顶替 | ✅ 测例 |
| D9 metric_id | ✅ |
| 不覆盖法定名称 / 不另做重点名单 | ✅ catalog 注记 + 单 ID 承接 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 约 70000（估） |
| model_used | composer |
| actual_cost | 约 0.4 |
| cost_warn | green |
