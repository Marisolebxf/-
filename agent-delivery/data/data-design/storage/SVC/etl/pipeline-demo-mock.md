# SVC · Demo / 约定 ODS 全链路（模拟 GDF）

> **口径**：对齐 ENT / CHAIN `pipeline-demo-mock.md`；机构主体复用 ENT，**不复制**主表。  
> **A 退出门**：`DEMO-SVC-A-RECLOSE-L01`（2026-08-18 live 重跑）  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: SVC-ETL-DEMO-MOCK
element: SVC
role: etl
status: as-built
version: "2026-08-18"
updated: "2026-08-18"
engine: multi
a_reclose: DEMO-SVC-A-RECLOSE-L01
---
```

## 1. 意图

Demo 灌数基于 **ETL 调度模拟 GDF**。ODS 结构以 **`third-party-source/doc/`** 为准（优先 `md-extract/` **国内机构要素库**），不以现网 as-built / L01 实查为准。落 `demo_*`。圈定结果一律 `pending_client_confirm`（**Q-SVC-010 不伪闭合**）。

## 2. 主路径

```text
约定文档(md-extract 国内机构要素库)
  → 复用/核对 demo_gkxlumenx_ods（与 ENT 同实例；禁第二套 dwd_org_base_info）
  → ENT 机构 DWD（既有 demo 行）
  → SVC 圈定 MOCK（待核验）
  → demo_* SVC DWD / ADS
  →（后续工厂）ES / Nebula / MinIO
```

可选旁路：[`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md)（不得冒充全链路验收）。

## 3. 命名表

| 角色 | 开发默认 | 禁止作 Demo 默认 |
|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` |
| MySQL DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` |
| MySQL ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` |
| MySQL DIM | `demo_gkxlumenx_dim` | `gkxlumenx_dim` |
| MinIO | `demo_**` 桶；本域前缀建议 `svc/{task_id}/` | 正式桶当 Demo 默认 |
| Nebula | 挂 **`demo_gkx_chain`**（决策 #7） | `demo_gkx_svc` 当第二张图；正式 space 当 Demo 默认 |

**铁律**：结构共用 `stores/*`；**实例隔离**。只写 `demo_gkxlumenx_*`。

## 4. 建表 / 核对脚本（A 已 live）

仓根：`${GKX_ROOT}/repos/demo-algo-ent-analysis`。环境：`GKX_ROOT` + `ENTAN_MYSQL_*`（拒非 `demo_` 库名）。

| 项 | 路径 |
|---|---|
| ODS 核对/补列 | `scripts/run_svc_ods_reconcile.py` |
| 本域 DWD/ADS DDL | `scripts/apply_svc_demo_ddl.py` ← SQL [`demo_gkxlumenx_dwd_svc_tables.sql`](./demo_gkxlumenx_dwd_svc_tables.sql) |
| MOCK 种子 | `scripts/seed_svc_demo_mock.py` |
| ODS 结构真源 | `doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv` |
| 表清单 | [`../sources/inventory.md`](../sources/inventory.md) |
| seeds | [`../seeds/README.md`](../seeds/README.md) |

```text
# 仓根：repos/demo-algo-ent-analysis
py -3 scripts/run_svc_ods_reconcile.py --self-check
py -3 scripts/run_svc_ods_reconcile.py --check --json-out out/svc_a_reclose_ods.json
# 缺列才：py -3 scripts/run_svc_ods_reconcile.py --apply
py -3 scripts/apply_svc_demo_ddl.py
# 仅当旧同名表缺 SVC 列：py -3 scripts/apply_svc_demo_ddl.py --rebuild-mismatch
py -3 scripts/seed_svc_demo_mock.py
```

### 2026-08-18 重跑证据（`DEMO-SVC-A-RECLOSE-L01`）

| 项 | 结果 |
|---|---|
| 入口 | `111.198.38.90:34306` · 用户 `gkxlumenx` · **仅** `demo_*` |
| ODS | `aligned=true` · 文档 33 表 · missing_tables/columns 空 · `dwd_org_base_info` 100 行 · `industry*` 9 列 |
| DWD/ADS DDL | `service_org*` 五表 + `svc_org_profile_card` / `svc_rec_ranking` 等 live；**未** `--rebuild-mismatch` |
| MOCK | batch `svc-mock-20260818` · DWD/ADS 各 24 户 · `verification_status=pending_client_confirm` · ranking ATTRACT 8 + CULTIVATE 8 |
| 正式库 | 探测到 schema 存在；**本叶零写入** `gkxlumenx_*` |

本机旁路产物（gitignore `out/`）：`svc_a_reclose_ods.json` · `svc_a_reclose_ddl.json` · `svc_a_reclose_seed.json` · `svc_a_reclose_verify.json`。

## 5. 仍开放（不挡 A 退出门，挡工厂「模拟 GDF」齐套）

| ID | 说明 |
|---|---|
| OPEN-SVC-FLOW-01 | 模拟 GDF 的 DAG/作业名未登记；本叶不编造 |
| OPEN-SVC-FLOW-03 | MinIO 本域前缀与现网桶参数待与平台稿对齐 |
| OPEN-SVC-FLOW-04 | ES / Nebula 同步 SLA |
| Q-SVC-010 | 圈定不得标 live；MOCK 保持待核验 |

## 6. 禁止

- 以现网三方 as-built、L01 `SHOW CREATE`、或未对齐 `doc/` 的草稿当 Demo ODS 真源  
- 复制 `dwd_org_base_info` 到 SVC 名下 / 平行 `svc_org_base`  
- 写正式 `gkxlumenx_*`  
- 第二套表结构 / 直写 ADS 冒充全链路  
- 把 Demo 临时准入口径写成正式契约  
- 用旧 `DEMO-SVC-SEED-*` `integration` 单独给 C 开闸（必须经本退出门）  
