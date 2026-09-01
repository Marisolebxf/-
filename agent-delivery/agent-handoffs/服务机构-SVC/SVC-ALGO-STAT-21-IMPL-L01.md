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
| 说明 | 复用 `svcseed.py` 同一批 `_write_metrics`；不新建 science/svcan 工厂；不改 seed/矩阵 YAML。50892 专题产品页本叶不改。 |

## 范围与实现

T2：年报缺行**内存**补人数/营收（不写 ODS 宽表）→ ADS 卡面三列 → 同一批写官方 ID。仍写旧 A1–A6 ID，避免 50100 断读。

| 序号 | ID | 本叶写入 |
|------|-----|----------|
| 1 | `M_SVC_ORG_TOTAL` | fact = 圈定 COUNT=3525 |
| 2 | `M_SVC_ORG_NEW_COUNT` | series 工商成立年 |
| 6 | `M_SVC_PT_GLOBAL_TOTAL` | fact + 存量 series |
| 7 | `M_SVC_PT_GLOBAL_TYPE_DIST` | dist 高校/院所/企业 |
| 8 | `M_SVC_PT_REGION_ORG` | region_dist 省级 |
| 9 | `M_SVC_PT_GLOBAL_SCALE_DIST` | 卡面 `employees_number` 四档 |
| 10 | `M_SVC_PT_KEYORG_SCALE` | 不另灌；读卡面三列 |
| 11 | `M_SVC_PT_SZ_TOTAL` | fact+series 深圳 **1355** |
| 12 | `M_SVC_PT_SZ_TYPE_DIST` | 深圳三类 |
| 13 | `M_SVC_PT_SZ_REGION_ORG` | 深圳 `area` |
| 21 | `M_SVC_SZ_COMPARE_METRIC` | 仅 `shenzhen_org_count`=1355 |

未做：3/4/5/14–20、MODEL/GRAPH、metrics seed/矩阵、**50892 `lumen-ui-topic`**。

## 联调（2026-09-01 · human:侯佳伟 确认灌数成功）

| 项 | 结果 |
|----|------|
| 50100 灌数 | `replace` 成功；`last_run=2026-09-01 11:40:20`；7.6s；无 error |
| 卡面 | `svc_org_card`=3525 |
| 深圳 | `sz_scale.org_count`=1355（与第 11/21 条锁口一致） |
| 深圳各区 | 南山 341 … 盐田 11 |
| `svc_metric_fact` | 6 行（旧 2 + 官方 4 fact） |
| 年报 1364 | 已修：不再 INSERT ODS 年报宽表 |

## 50897 / 50892

| 入口 | 本叶 |
|------|------|
| **50897** 算法库联调台 | 已更新：基础指标页叠 STAT-21 T2 官方 ID；`/entan/v1/svc/indicators` 增加 `org_total` / `pt_*` / `sz_compare` |
| **50892** 专题产品 | **暂停、未改、无回退**（工作区干净） |

50897 仓：`lumen-ui-algo-apiview`。不迁 run-pipeline。挂起条不造数。

## 产物

- `${GKX_ROOT}/repos/demo-algo-ent-analysis/entan/svcseed.py`
- `${GKX_ROOT}/repos/demo-algo-ent-analysis/api/svc_routes.py`
- `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/mysql/svc_ddl_demo_empty.sql`
- `${GKX_ROOT}/repos/lumen-ui-algo-apiview/src/catalog/svc.json`
- `agent-delivery/data/data-design/storage/SVC/stores/mysql/ddl-demo-empty.sql`

## 测试结果

- `py -3 -m entan.svcseed --check`：通过
- `node --test scripts/catalog.test.mjs`（apiview）：20 pass
- 50100 `/internal/svc/status` + `/v1/svc/indicators`：现网已出数

## 架构合规

| 铁律 | |
|------|--|
| 算法只在 Python | ✅ |
| 调用链 前端→Java→Python `/internal/*` | ✅ 50897 仍走 `/entan/v1/svc/*`；不直连 Python |
| Nebula | ✅ 本叶不写图 |
| D12 | ✅ 不调 demo 当 lumen 生产写路径；50897 只读 Java |
| 不改 seed/矩阵 YAML | ✅ 进度表保持 D1=草案 D4=Mock |

## 偏离

task.repo = `demo-algo-science`，实现落在 `demo-algo-ent-analysis`。as-built = 扩 F-SEED。

## 遗留

- 年报缺行人数是 Demo 造数，指标表不得改绿
- 高校/院所主体表空则类型图 0/0/N
- 50897 新字段须等 `demo-algo-ent-analysis` deploy 绿后点「执行」才出图
- 本会话 `task-registry` MCP 未挂载，状态请 coordinator 推 `integration`（note：联调通过）

## 开放项

无。挂起条仍不进本叶。50892 产品复刻另叶。

## CI/CD

- `demo-algo-ent-analysis` `7b3179c` 已 push（1364）；本收口另含 `svc_routes` indicators 扩展
- `lumen-ui-algo-apiview` `origin/dev`（catalog）
- 50892：无 commit

## Cost

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 180000 |
| `model_used` | `claude-sonnet-4.5`（registry 合法枚举；本会话 Cursor Grok 4.6，按 Sonnet 价表） |
| `actual_cost` | 0.97 |
| `cost_warn` | green |
| 口径 | algorithm-agent 80/20；`180000×0.8×3/1e6 + 180000×0.2×15/1e6 = 0.972`；`source: session_estimate` |
