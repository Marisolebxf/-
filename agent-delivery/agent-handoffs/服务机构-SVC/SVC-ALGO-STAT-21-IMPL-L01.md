# SVC-ALGO-STAT-21-IMPL-L01 · 已确认 STAT 的 Demo T2 实现

> 只认分析叶收口 + 文首 T0–T2。仓登记是 `demo-algo-science`，现网工厂在 `demo-algo-ent-analysis/entan/svcseed.py`（F-SEED 直写 Demo ADS）。本叶扩这个工厂，不在 science 仓另起一套。

## 任务认领

| 字段 | 值 |
|------|-----|
| task-id | `SVC-ALGO-STAT-21-IMPL-L01` |
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `pull` |
| lock | 24h |
| 依赖 | `SVC-ALGO-STAT-21-L01` = done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `svcseed.py` 同一批 `_write_metrics`；不新建 science/svcan 工厂；不改 seed/矩阵 YAML。 |

## 范围与实现

T2 顺序：ODS 年报补 `employees_number` / `operating_revenue`（不加列）→ ADS 卡面加同名三列 + `org_size` → 投影 → 同一批写指标。

| 序号 | ID | 本叶写入 |
|------|-----|----------|
| 1 | `M_SVC_ORG_TOTAL` | fact = 圈定 COUNT |
| 2 | `M_SVC_ORG_NEW_COUNT` | series 工商成立年新增 |
| 6 | `M_SVC_PT_GLOBAL_TOTAL` | fact + 存量累加 series；ext 仅国内 |
| 7 | `M_SVC_PT_GLOBAL_TYPE_DIST` | dist 高校/科研院所/企业（∩ 主体表，无表则 0/0/N） |
| 8 | `M_SVC_PT_REGION_ORG` | region_dist 省级 |
| 9 | `M_SVC_PT_GLOBAL_SCALE_DIST` | dist 四档扫卡面 `employees_number`（禁 `org_size`） |
| 10 | `M_SVC_PT_KEYORG_SCALE` | 不另灌；读卡面三列 |
| 11 | `M_SVC_PT_SZ_TOTAL` | fact+series 深圳 |
| 12 | `M_SVC_PT_SZ_TYPE_DIST` | 深圳三类 |
| 13 | `M_SVC_PT_SZ_REGION_ORG` | 深圳 `area` |
| 21 | `M_SVC_SZ_COMPARE_METRIC` | **仅** `shenzhen_org_count` |

仍写旧 A1–A6 ID（`M_SVC_ORG_CNT` 等），避免 50100 断读。

未做：3/4/5/14–20、MODEL/GRAPH、`lumen-algo-py`、前端、metrics seed/矩阵。

## 产物

- `${GKX_ROOT}/repos/demo-algo-ent-analysis/entan/svcseed.py`
- `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/mysql/svc_ddl_demo_empty.sql`
- `agent-delivery/data/data-design/storage/SVC/stores/mysql/ddl-demo-empty.sql`

灌数：`py -3 -m entan.svcseed replace`（只写 `demo_gkxlumenx_*`）。

## 测试结果

- `py -3 -m entan.svcseed --check`：通过（分档边界 + 三类归属）
- 未在本窗对 88.43 跑 `replace`（会 TRUNCATE 再灌；需监管人点一次）

## 架构合规

| 铁律 | |
|------|--|
| 算法只在 Python | ✅ |
| 调用链 前端→Java→Python `/internal/*` | ✅ 本叶只改工厂；`/internal/svc/run-pipeline` 已有 |
| Nebula | ✅ 不写图 |
| 可观测 | N/A 工厂批处理沿用 logger |
| D12 不调 demo 当 lumen 生产 | ✅ 只写 demo ADS |
| 不改 seed/矩阵 YAML | ✅ |

## 偏离

task.repo = `demo-algo-science`，实现落在 `demo-algo-ent-analysis`：science 仓无 `svcan` / `svc_org_card`。as-built = 扩 F-SEED。

## 遗留

- 高校/院所主体表现网若仍空，类型图允许 0/0/N
- 年报空行用确定性 Demo 补数（hash 人数），不是三方 live
- 需跑一次 `replace` 才进 50100
- 自测页走已有 `LUMEN-UI-ALGO-APIVIEW-SVC-L01`，本叶不另开

## 开放项

无。挂起条仍不进本叶。
