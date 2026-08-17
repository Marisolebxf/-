# DEMO-SVC-SEED-ODS-L01 · 产业服务链 A — Demo ODS/本域表核对与建表

> 日期：2026-08-17  
> Task：`DEMO-SVC-SEED-ODS-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 S2 reconcile + DDL 草稿 APPLY；未新建第二套主表；未写正式库 |

## 范围与实现

- **Demo ODS**：`run_svc_ods_reconcile.py --self-check` + `--check` → **aligned=true**（33 表、缺列 0、复用 ENT）
- **本域 DWD/ADS**：对 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` APPLY `storage/SVC/etl/demo_gkxlumenx_dwd_svc_tables.sql`；补齐 `svc_org_profile_card`
- **新增脚本**：`repos/demo-algo-ent-analysis/scripts/apply_svc_demo_ddl.py`
- **非范围**：MOCK 种子行（`DEMO-SVC-SEED-MOCK-L01`）；正式库；Q-SVC-010 关闭

## 偏离说明

无。ADS 其余 `svc_metric_*` 等契约表仍按 ads.md draft，本叶以 DDL 草稿骨架 + 已存在旁路表为准；灌数样例留给 MOCK 叶。

## 产物清单

| 产物 | 路径 |
|------|------|
| ODS 核对报告 | `repos/demo-algo-ent-analysis/out/svc_seed_ods_check.json` |
| DDL APPLY 报告 | `repos/demo-algo-ent-analysis/out/svc_seed_ddl_apply.json` |
| APPLY 脚本 | `repos/demo-algo-ent-analysis/scripts/apply_svc_demo_ddl.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-SEED-ODS-L01.md` |

## 验收证据

- [x] ODS `aligned=true`（missing_tables/columns 空）
- [x] live：`demo_gkxlumenx_dwd.service_org*` 五表；`demo_gkxlumenx_ads.svc_org_profile_card` + `svc_rec_ranking`（及库内已有其它 svc_*）
- [x] 零写正式 `gkxlumenx_*`
- [x] MySQL：`111.198.38.90:34306` · Demo 库名

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A 本叶结构 |
| 2 | 调用链 | ✅ N/A |
| 3 | Nebula | ✅ N/A |
| 6 | demo 不污染正式 | ✅ 仅 demo_* |
| 8 | ADS | ✅ Demo ADS 骨架可建 |
| D12 | 不写正式 ODS 当真源 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 联调确认

联调通过：Demo ODS 对齐 + 本域 DWD/ADS 表可连；下游 B/C 可读空表。下一叶：`DEMO-SVC-SEED-MOCK-L01`。
