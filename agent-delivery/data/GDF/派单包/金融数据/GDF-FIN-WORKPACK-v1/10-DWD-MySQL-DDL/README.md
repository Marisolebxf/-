# 10 · DWD / ADS MySQL DDL（金融）

> **状态：DDL 绿（2026-11-09）。** 结构真源 = `agent-delivery/data/data-design/storage/FIN/stores/mysql/dwd.md` + `ads.md`（`GDF-FIN-STORAGE-DDL-L01` 已签收）；本目录两份 draft 是同步副本（每表一个 sql 围栏），改列须两边同改。  
> **自检**：`python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --dimension fin` → **通过**（包 ↔ storage ↔ `demo_gkxlumenx_*` ↔ `gkxlumenx_*`，15 表）。  
> **提醒**：DDL 绿 ≠ `SYSINT-06-04-L01` 跑通；跑通仍须 GDF 导入 / 回传后 Java 只读 ADS。

## 文件

| 文件 | 内容 | 生成方式 |
|---|---|---|
| [fin-dwd-draft.md](fin-dwd-draft.md) | 11 张 `gkxlumenx_dwd.fin_*` 建表 | `script/gen_fin_pack.py` 生成（与 09 §3 同源） |
| [fin-ads-draft.md](fin-ads-draft.md) | 4 张 `gkxlumenx_ads.ads_fin_*` 建表 | 手写，口径见 `12` |

## 本期必须存在的表

| 层 | 表 |
|---|---|
| DWD（Wave B） | `fin_corp_basic`、`fin_security`、`fin_industrial_fund`、`fin_industrial_fund_gp`、`fin_industrial_fund_lp`、`fin_industrial_fund_strategy`、`fin_industrial_fund_inv_summary`、`fin_bond`、`fin_industry_class_his`、`fin_main_biz_composition`、`fin_valuation_daily` |
| ADS（②） | `ads_fin_industrial_fund_summary`、`ads_fin_bond_issue_summary`、`ads_fin_listed_company_snapshot`、`ads_fin_main_biz_latest` |

## 状态

| 项 | 状态 |
|---|---|
| 上述 15 张表 | demo + lumen 已建且与 md 一致（DDL 自检通过） |
| `gkx-gdf-ddl-signoff` | **通过**（`--dimension fin`） |
| 入 `storage/FIN/stores/mysql/` | 已入（15 张） |
| 字符集 | `utf8mb4_0900_ai_ci`；字符列未单独写 COLLATE（继承表级） |
| 跑通 | **未关**：归 `SYSINT-06-04-L01` |

## 禁止

- 把供应方 `dwd_*` 当项目 DWD 建表。
- 为「表清单好看」灌假数据。
- 在 `demo_gkxlumenx_*` 当产线目标写作业（自检可核 demo；产线作业只写 `gkxlumenx_*`）。
