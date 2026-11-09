# 10 · DWD / ADS MySQL DDL（金融）

> **状态：草稿，未签收。** 金融域目前在 `agent-delivery/data/data-design/storage/` 下**没有** `FIN/` 目录，所以按 `mysql-ddl-convention.md` §1「一张表只有一份带注释的 CREATE，真源在 storage」的要求，真源**尚未存在**。本目录是成包期的临时落点（OPEN-FIN-01）。

## 文件

| 文件 | 内容 | 生成方式 |
|---|---|---|
| [fin-dwd-draft.md](fin-dwd-draft.md) | 11 张 `gkxlumenx_dwd.fin_*` 建表草稿 | `script/gen_fin_pack.py` 生成（与 09 §3 同源） |
| [fin-ads-draft.md](fin-ads-draft.md) | 4 张 `gkxlumenx_ads.ads_fin_*` 建表草稿 | 手写，口径见 `12` |

## 本期必须存在的表

| 层 | 表 |
|---|---|
| DWD（Wave B） | `fin_corp_basic`、`fin_security`、`fin_industrial_fund`、`fin_industrial_fund_gp`、`fin_industrial_fund_lp`、`fin_industrial_fund_strategy`、`fin_industrial_fund_inv_summary`、`fin_bond`、`fin_industry_class_his`、`fin_main_biz_composition`、`fin_valuation_daily` |
| ADS（②） | `ads_fin_industrial_fund_summary`、`ads_fin_bond_issue_summary`、`ads_fin_listed_company_snapshot`、`ads_fin_main_biz_latest` |

## 状态与未做

| 项 | 状态 |
|---|---|
| 上述 15 张表 | 草稿。`demo_gkxlumenx_*`、线上 lumen 库均**未建** |
| `gkx-gdf-ddl-signoff` | **未跑**。该自检要求「线上 demo 库与 lumen 库都已有这些表，且与 dwd.md / ads.md 一致」，本包做不到，也不应在此之前宣称通过 |
| 入 `storage/FIN/stores/mysql/` | 待架构师另开叶（OPEN-FIN-01） |
| 字符集 | 已按 `utf8mb4_0900_ai_ci`；字符列未单独写 COLLATE（继承表级） |

## 禁止

- 把供应方 `dwd_*` 当项目 DWD 建表。
- 为「表清单好看」灌假数据。
- 在 `demo_gkxlumenx_*` 建这些表。
