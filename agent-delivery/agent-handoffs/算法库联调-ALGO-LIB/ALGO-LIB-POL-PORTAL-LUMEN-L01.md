# ALGO-LIB-POL-PORTAL-LUMEN-L01 · 政策扶持十条计算迁入 lumen-algo-py

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-10-24 淮政玮：本单不依赖 `SYSINT-ADS-02-L01`，可以跑。同仓 ADS-02 改的是三要素 WBS，不改本单这几个文件。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 计算从已签收的 demo `portal_gap_rows` 原样移植。没有新公式，没有改指标种子。自检 `tests/test_policy_portal_gaps.py`。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 按已签收 demo 函数移植，未用压缩代替源码。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用 |
| 图 diff | 未改存储流图。读的仍是 DWD `policy_base_info`、`industry_chain_node`、`policy_industry_rel` |
| 会签态 | 未改图 |
| 说明 | 缺表（errno 1146）时节点两行降级为空，政策行照常算。 |

## 范围与实现

`GET /internal/policy/indicators?kind=all` 的 `data.portal_gaps` 有十条，key 与 demo 一致。`kind` 不是 `all` 时不附这组。

口径登记在 `vendor/entan-py/conf/settings_policy.yaml` 的 `portal_gaps`，并写入 `polan/common/config.py` 的默认值：密度分母 `natural_month`；重点城市为深圳市、广州市、北京市、上海市、杭州市、南京市、天津市、重庆市、合肥市、青岛市。相近指标标量与这十行的 value 相同则该行清空，不写入 `filled_from`。源行没有时该条 `value` 为空并带原因。

Java `PolicyFacadeServiceImpl.copyMap` 按 key 原样拷贝，成功包络里的 `portal_gaps` 会随 `unwrapIndicators` 上去。本单没有改 `lumen-svc-platform`。Feign 失败走 `honestEmptyIndicators`，那条路径本来就没有 `portal_gaps`，不另开 Java 单。

## 偏离

无。没有调用 demo 服务。没有改 `PORTAL-CMS-政策扶持.md`。排名仍留给 `SYSINT-03-04B-L01`，本单不删 `portal_gaps`。

## 产物清单

- `repos/lumen-algo-py/vendor/entan-py/polan/basic/indicators.py`（`portal_gap_rows`）
- `repos/lumen-algo-py/vendor/entan-py/polan/eval/intensity.py`（`reject_portal_gap_rehang`）
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `repos/lumen-algo-py/vendor/entan-py/conf/settings_policy.yaml`
- `repos/lumen-algo-py/vendor/entan-py/polan/common/config.py`
- `repos/lumen-algo-py/tests/test_policy_portal_gaps.py`

## 验收证据

`python -m pytest tests/test_policy_portal_gaps.py -q`：11 passed。覆盖十条 key、相近 ID 不填、自然月序列、省/市/深圳/节点，以及 `kind=all` 在缺节点表时仍返回十条。

未对运行中的 Python / Java 做线上联调。代码在本地工作区，未提交。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 算法在 Python，Java 不写算法 | ✅ |
| 调用链仍是前端 → Java → `/internal/policy/indicators` | ✅ |
| 不调用 demo-* 服务 | ✅ |
| 不改 Nebula、不新造桶 | ✅ |
| 未把 mock 写成已接入；无行则空并写原因 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |

## 开放项

- `SYSINT-03-04B-L01` 补省级/城市力度排名。前序本单 handoff 已在，状态到 `integration` 后可领。不得把 `portal_gaps` 删成空。
- 正式 ADS 未灌通。本接口读 DWD 政策行；库空或未登记口径时十条为空。
