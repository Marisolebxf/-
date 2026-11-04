# SYSINT-03-01B-L01 · 企业发展指标区块

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | COVER-ENT 已 done；按门户契约接线，非展示系统 SYSINT-05 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 01C 的 `/internal/enterprise` 前缀；门面 + 空态铁律，不新依赖；ADS 真算未灌数前 value 诚实为 null/mock |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | COVER 12+7 行与契约 §1 原文对照，未用摘要代替 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。计算在 Python `/internal/enterprise/portal/*` |
| 会签态 | 技术方案 draft |
| 说明 | 指标不进 CMS；与 CMSOPS 写侧 / VIZ 读侧路由不重叠 |

## 范围与实现

门户企业发展四页（`overview` / `key-pano` / `star` / `shenzhen`）指标区块门面：

1. **12 个已注册 `metric_id`**：响应一律带 `metric_id`。其中 COVER 裁定空态 3 个（科研人数 / 明星名单计数 / 研发投入占比）`value=null` + reason；其余 `serve` 行 D4 仍 mock，本叶先出空值占位与口径 note，不把相邻指标写入 value。
2. **7 个契约缺口行**：`metric_id=null`、`value=null`；`M_ENT_NEW_COUNT_Y` / `M_ENT_STAR_PATENT_COUNT` 等只进 `rejected_metric_ids`，禁止顶替。
3. 领域摘要复用既有 `compute_metric(M_ENT_KEYPANO_DOMAIN_SUMMARY)`。

不改 `PORTAL-CMS-企业发展.md`，不改 metric 种子，不调 demo-*，不把手填数写进 CMS。

## 偏离

- ADS / gkx 真算复算脚本（`metrics/repro/M_ENT_*.py`）**尚未**接到本门面的 `value` 填充；本叶先闭合「走指标服务 + 空态铁律」。真算灌数可另开叶或本叶续作。
- registry 原记仓 `lumen-algo-py`；实现落该仓。门户 Java 读侧（`PORTAL-ENT-DEV-SRS-API`）仍走 topic-py 汇总表，**未**在本叶改 Feign 切到本门面——对接留给 api-agent 联调。

## 产物清单

| 仓 | 路径 |
|---|---|
| lumen-algo-py | `lumen_common/algorithms/entan/portal_metrics.py` |
| lumen-algo-py | `lumen_algo_service/views/enterprise.py`（`/portal/catalog` `/portal/metrics`） |
| lumen-algo-py | `tests/test_portal_ent_metrics.py` |
| gkx-orchestration | 本 handoff |

## 验收证据

`python -m pytest tests/test_portal_ent_metrics.py -q` → **8 passed**。

覆盖：catalog 12+7；已注册带 `metric_id`；空态三 ID；`NEW_COUNT_Y` 不填总数趋势；专利邻近 ID 拒绝；科研人数空态；`page_key=overview` 过滤。

未做线上联调；代码在 `lumen-algo-py` 工作区，**待监管人验收后再 commit/push**。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 算法在 Python | ✅ |
| 调用链 Feign `/internal/*` | ✅ 路径已留；Java 接线未做 |
| 不调用 demo-* | ✅ |
| 缺口不手填 / 不顶替 | ✅ 测例 |
| D9 metric_id | ✅ 已注册行带 ID |
| 非展示系统 SYSINT-05 | ✅ 门户 CMS 指标叶 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 约 90000（估） |
| model_used | composer |
| actual_cost | 约 0.5 |
| cost_warn | green |
