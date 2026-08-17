# SVC · ODS 表级清单（国内机构要素库）

```yaml
---
doc_id: SVC-SOURCE-INVENTORY
element: SVC
role: source
status: draft
version: "2026-08-14"
updated: 2026-08-14
task: DATA-SVC-STORAGE-S2-L01
---
```

> **真源**：权威 `third-party-source/doc/` xlsx；日常读 `doc/md-extract/`。  
> Sheet：`版权人才、企业机构、政策数据汇总表` → **国内机构要素库**。  
> CSV：`doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv`  
> **Demo 实例**：与 ENT **共用** `demo_gkxlumenx_ods`（核对/补齐，**禁止**再建 `dwd_org_base_info` / `svc_org_base`）。  
> **禁止**：以 `gkx-mysql-raw` / L01 现网 `SHOW CREATE` 当建表真源；默认写正式 `gkxlumenx_ods`。

## 真源入口

| 用途 | 路径 |
|---|---|
| 权威 | `agent-delivery/data/third-party-source/doc/版权人才、企业机构、政策数据汇总表.xlsx` |
| 优先读 · MD | `…/doc/md-extract/版权人才、企业机构、政策数据汇总表.md`（sheet「国内机构要素库」） |
| 日常建表 · CSV | `…/doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv` |
| ENT 同源清单 | [`../../ENT/sources/inventory.md`](../../ENT/sources/inventory.md) |
| 核对脚本 | `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/run_svc_ods_reconcile.py` |

## 与 ENT 边界

| 类别 | 说明 |
|---|---|
| **与 ENT 共用（本域依赖）** | 下表全部 33 张约定 ODS（供应方名常带 `dwd_*`，落库角色仍是 ODS）。机构主体权威在 ENT；SVC **只读键 + 本域圈定/关系** |
| **本域独有（ODS）** | **无**。不另建机构主表 / 平行 `svc_org_base` |
| **本域独有（项目 DWD，非本清单）** | 圈定结果 / 关系 / 本域切片 → **S3** `stores/`；规则受 **Q-SVC-010** 阻断，不得标 live |

## 表级清单（md-extract · 33 表）

> 字段数 = CSV 约定英文字段数；Demo 另有 `_demo_id` 物理主键（与 ENT `llm_ods` 一致）。  
> **S2 核对（2026-08-14）**：`demo_gkxlumenx_ods` 上 33/33 表齐全；文档列差集 **0**（含 `industry*`）。

| # | 约定表名 | 字段数 | 共用/独有 | 本域用途（一句话） |
|---|---|---|---|---|
| 1 | `dwd_org_base_info` | 37 | ENT 共用 | 机构主体；含 `industry*`（Q-SVC-009） |
| 2 | `dwd_org_shareholder_info` | 10 | ENT 共用 | 股东 |
| 3 | `dwd_org_executive_info` | 8 | ENT 共用 | 高管 |
| 4 | `dwd_org_org_product_info` | 9 | ENT 共用 | 经营/产品；`main_activities` 可作圈定临时特征（待核验） |
| 5 | `dwd_org_annual_financial_info` | 19 | ENT 共用 | 年报财务 |
| 6 | `dwd_org_important_news_info` | 10 | ENT 共用 | 重点资讯 |
| 7 | `dwd_org_stock_base` | 11 | ENT 共用 | 上市基本 |
| 8 | `dwd_org_stock_finance_info` | 20 | ENT 共用 | 上市财务 |
| 9 | `dwd_org_tech_tag` | 5 | ENT 共用 | 技术/资质标签 |
| 10 | `dwd_org_financing_info` | 12 | ENT 共用 | 融资 |
| 11 | `dwd_org_invest_info` | 11 | ENT 共用 | 对外投资 |
| 12 | `dwd_org_subsidiary_info` | 9 | ENT 共用 | 子公司 |
| 13 | `dwd_org_recruit_info` | 11 | ENT 共用 | 招聘 |
| 14 | `dwd_org_changerecord_info` | 10 | ENT 共用 | 变更记录 |
| 15 | `dwd_org_merger_acquisition_info` | 11 | ENT 共用 | 并购 |
| 16 | `dwd_org_company_abnormal` | 13 | ENT 共用 | 经营异常 |
| 17 | `dwd_org_company_punish` | 22 | ENT 共用 | 行政处罚 |
| 18 | `dwd_org_company_illegal` | 14 | ENT 共用 | 严重违法 |
| 19 | `dwd_org_opt_judicial_case` | 15 | ENT 共用 | 司法案件 |
| 20 | `dwd_org_bankruptcy_public_cases` | 14 | ENT 共用 | 破产公开 |
| 21 | `dwd_org_bankruptcy_public_cases_list` | 12 | ENT 共用 | 破产公开明细 |
| 22 | `dwd_org_risk_shixin` | 26 | ENT 共用 | 失信 |
| 23 | `dwd_org_risk_zhixing` | 19 | ENT 共用 | 执行 |
| 24 | `dwd_org_risk_tax_punish` | 26 | ENT 共用 | 税务处罚 |
| 25 | `dwd_org_heis_info` | 20 | ENT 共用 | 高校机构 |
| 26 | `dwd_research_institute_base_info` | 20 | ENT 共用 | 科研机构 |
| 27 | `dwd_special_hongkong_company` | 19 | ENT 共用 | 香港企业 |
| 28 | `dwd_special_taiwan_company` | 36 | ENT 共用 | 台湾企业 |
| 29 | `dwd_special_aomen_company` | 19 | ENT 共用 | 澳门企业 |
| 30 | `dwd_bid_base_out` | 56 | ENT 共用 | 招投标主 |
| 31 | `dwd_bid_win_candidate_out` | 15 | ENT 共用 | 中标候选人 |
| 32 | `dwd_bid_purchase_agency_out` | 10 | ENT 共用 | 采购代理 |
| 33 | `dwd_bid_target_item_out` | 18 | ENT 共用 | 标的物 |

## `dwd_org_base_info` · industry*（Q-SVC-009）

文档承诺列（建表认文档；live 三方缺列不得反向删文档列）：

| 英文字段 | 中文（文档） |
|---|---|
| `industry` | 国民经济行业分类 |
| `industry_l1_name` / `industry_l1_code` | 一级行业 |
| `industry_l2_name` / `industry_l2_code` | 二级行业 |
| `industry_l3_name` / `industry_l3_code` | 三级行业 |
| `industry_l4_name` / `industry_l4_code` | 四级行业 |

**S2 证据**：`demo_gkxlumenx_ods.dwd_org_base_info` 上述 9 列均已存在（`SHOW CREATE` 见 etl 快照 / `out/svc_demo_ods_show_create.sql`）。

## 建表 / 核对入口

| 项 | 值 |
|---|---|
| 复用 ENT 主路径 | `scripts/run_llm_ods.py`（`entan/llm_ods/` · 国内机构要素库） |
| **本域核对/补列** | `scripts/run_svc_ods_reconcile.py`（`--check` / `--apply`；**不** DROP 重建主表） |
| 自检 | `py -3 scripts/run_svc_ods_reconcile.py --self-check` |
| DDL 快照（摘要） | [`../etl/demo_gkxlumenx_ods_svc_org_show_create.sql`](../etl/demo_gkxlumenx_ods_svc_org_show_create.sql) |

## 开放项（不伪闭合）

| ID | 说明 | 状态 |
|---|---|---|
| Q-SVC-009 / OPEN-SVC-FLOW-08 | 文档 `industry*` vs 三方 live；Demo 已按文档对齐 | 供方对账另轨；不挡 S2 |
| Q-SVC-010 / OPEN-SVC-FLOW-10 | 服务机构准入主路径 | **阻断级**；圈定结果不得标 live |
| OPEN-SVC-FLOW-06 | Demo 核对/补齐 | **本单关闭（核对差集 0）** |
