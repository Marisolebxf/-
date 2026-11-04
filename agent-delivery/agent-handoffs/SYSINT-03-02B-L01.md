# SYSINT-03-02B-L01 · 产业全景指标与图谱数字

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | COVER-CHAIN 已 done（7 注册 + 1 缺口）；2026-10-24 起李伟不再监管本线 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 01B 门面模式与 `/internal/v1/chain` 前缀；不改 metric_engine / 不动 CMS / 不写图谱 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | COVER-CHAIN 8/8 行与契约 §1.1/§1.3 原文对照 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。新增只读门面 `/internal/v1/chain/portal/{catalog,metrics}` |
| 会签态 | 技术方案 draft |
| 说明 | 节点/边不进 CMS；读图不在本叶（WBS-03-06） |

## 范围与实现

门户专题全景指标门面（`panorama` / `overview` 两 page_key）：

1. **9 行已注册**（契约 7 ID，其中企业/机构数在两个 page_key 复用）：全部带 `metric_id`。全球/全国区域数两行 COVER 裁定空态（`data_source=empty` + reason）；其余 serve 行 D4 mock 占位 + 口径 note。
2. **1 个缺口行**（深圳各区计数）：`metric_id=null`；计数器件 `M_CHAIN_SZ_REGION_COUNT` 只进 `rejected_metric_ids`（计数器语义≠分区分布面，承接方式待母单 D10）。
3. `industry_code` 透传（选链=接口过滤）；`nearby_metrics` 只用于拒绝改挂。

不改 `PORTAL-CMS-专题全景.md`、不改种子/矩阵、不调 demo-*、不动 `metric_engine.py` 现有计算。

## 偏离

- serve 行 value 暂为 null（D4 mock；`COMPUTE_IDS` 真算灌数未接）。理由：与 01B 同批，真算接线属数据侧阶段。
- 现网已有 `chain_read.enterprise_stats`（sync 读面）未并入本门面——那是 R-1 复用面（VIZ-API 范围），本叶不重复实现。

## 产物清单

| 仓 | 路径 |
|---|---|
| lumen-algo-py | `lumen_common/algorithms/chain/portal_metrics.py` |
| lumen-algo-py | `lumen_algo_service/views/chain.py`（`/portal/catalog` `/portal/metrics`） |
| lumen-algo-py | `tests/test_portal_chain_metrics.py` |
| gkx-orchestration | 本 handoff |

## 测试结果

`python -m pytest tests/test_portal_chain_metrics.py tests/test_portal_ent_metrics.py -q` → **14 passed**。

覆盖：catalog 9+1；serve 带-ID；全球/全国空态；`SZ_REGION_COUNT` 不填区级缺口；page_key 过滤；HTTP 批量往返。

未做线上联调；代码停本地，待监管人验收后 commit/push。

## 遗留风险

- 区级分布面是否立项走 `M_CHAIN_SZ_REGION_COUNT` 计数器：等母单 D10。
- 全球/全国两行页面字样（「库内覆盖区域数」）待拍板，未拍前只空态不造数。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 算法在 Python | ✅ |
| 调用链 Feign `/internal/*` | ✅ 路径已留 |
| 不调用 demo-* | ✅ |
| 缺口不手填 / 不顶替 | ✅ 测例 |
| D9 metric_id | ✅ |
| 非展示系统 / 非 VIZ 复用面 | ✅ 独立 `/portal/*` 路由 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 约 60000（估） |
| model_used | composer |
| actual_cost | 约 0.35 |
| cost_warn | green |
