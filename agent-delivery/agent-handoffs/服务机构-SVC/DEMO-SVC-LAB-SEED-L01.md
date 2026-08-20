# DEMO-SVC-LAB-SEED-L01 · SVC F-SEED 灌数接到 Demo

> 日期：2026-08-20  
> Task：`DEMO-SVC-LAB-SEED-L01`  
> 仓：`demo-algo-ent-analysis`  
> 总控：阶段 F。淮政玮：立刻 F-SEED；未 F-GATE 不开 50892。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短通路：ODS 圈定 → circle/card/A1–A6；不写十模型/Nebula；自检 `--check` + 一次 replace |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CLI 认领 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，未改边） |
| 图 diff | 无工厂边变更。实现灌数时序：ODS → circle → card + A1–A6 |
| 会签态 | 流图仍 2026-08-19 approved |
| 说明 | 写库方 = 本仓 Python |

## 范围与实现

1. 执行 `scripts/mysql/svc_ddl_demo_empty.sql`（编排仓 DDL 副本）；遇旧 Gate-0 `svc_metric_*` 缺 `category`/`value` 则 DROP 四张指标表后重建。  
2. `entan/svcseed.py` 规则 A：`demo_gkxlumenx_ods.dwd_org_base_info` → `svc_org_circle` / `svc_org_card` / 融资 hang / A1–A6。  
3. `POST /internal/svc/run-pipeline` 与 CLI 同一引擎；`assert_demo_mysql_targets`；live 拒绝灌数。  
4. `plane.py` 增加 `svc` 域，对齐 50100 顶栏。

## 实测（Demo NAT，replace）

| 项 | 值 |
|---|---|
| ODS | 40000 |
| 圈定 | **3525**（未 fallback 全表） |
| 融资 hang | 31 |
| 指标 | dist 98 / region 10 / series 43 / fact 2 |
| rule_version | `svc_rule_demo_kw_v1.1` |
| pending | 一律 1 |
| 未做 | 十模型、Nebula、50892、正式库 |

## 偏离说明

- 旧 Gate-0 指标表结构不兼容，F-SEED **DROP 重建** Demo `svc_metric_*` 四表（不碰 ODS 33）。  
- `event_id` 用 md5，避免 VARCHAR(64) 截断撞 UK。

## 产物清单

| 产物 | 路径 |
|---|---|
| 引擎 | `entan/svcseed.py` |
| 路由 | `api/svc_routes.py` |
| DDL 副本 | `scripts/mysql/svc_ddl_demo_empty.sql` |

## 验收证据

- [x] `py -3 -m entan.svcseed --check` ok  
- [x] replace：circle 3525，不写正式库，不 DROP ODS  
- [x] 50100 同源 `/internal/svc/run-pipeline`  
- [x] Q-SVC-010 待核验  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链 | ✅ 灌数写 Demo ADS；线上读 ADS |
| 6 | demo 不污染 lumen | ✅ |
| 8 | ADS | ✅ 卡面+指标 |
| 10 | D9 | ✅ 不伪闭合 |

## CI/CD

- 分支：`origin/dev`
- 部署：随 entan 服务；本机已灌 Demo

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80000 |
| actual_tokens | 120000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.62 |
| cost_warn | green |
