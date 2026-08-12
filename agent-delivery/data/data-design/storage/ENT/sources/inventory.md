# 企业维 ODS 表级清单

> **状态**：S2 初填 · 2026-08-12 · `DATA-ENT-STORAGE-S2-L01`  
> **三方 ODS 唯一真源（OPEN-ENT-FLOW-05 · 关闭）**：  
> 权威：`agent-delivery/data/third-party-source/doc/`（xlsx）  
> **优先读取**：`…/doc/md-extract/`（自 Excel 抽取 · md/csv；冲突或过期时以 xlsx 重抽）  
> 企业主文件：`版权人才、企业机构、政策数据汇总表.xlsx` → **先读** `md-extract/版权人才、企业机构、政策数据汇总表.md`  
> **GDF 施工镜像**（非真源）：`data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml`  
> **Mapping 施工**：`…/09-企业维-ODS到DWD-Mapping说明-v3.md`（须对齐 `doc/`）  
> **禁止**：以 `gkx-mysql-raw` live as-built 或 Wave A 漂移稿覆盖 `doc/`（见 [`README.md`](./README.md)）

## 目标库约定

| 层 | 库名（约定） | 说明 |
|---|---|---|
| ODS（贴源 / Demo Mock 写入面） | `gkxlumenx_ods`（正式）；Demo 目标 `demo_gkxlumenx_ods` 或同构前缀（见 etl/pipeline-demo-mock 命名表） | 表名 / 字段 = **`doc/` 承诺** |
| 现网探测（对账 only） | live `gkx`（见 `third-party-source/gkx-mysql-raw/`） | **禁止**作 ODS 设计真源 |

## P0 表级清单（Wave A · 国内机构主数据等）

| ODS 表（约定名） | 在线约定文档入口 | 用途（一句话） | 落入项目 DWD | Demo | 与现网差异备注 |
|---|---|---|---|---|---|
| dwd_org_base_info | doc/版权人才…xlsx · 国内机构要素库 | 企业/机构主数据 | enterprise_base 等 | 是 | live 常作 `dwd_org_reg_info`；**以承诺名为准** |
| dwd_org_shareholder_info | 同上 | 股东 | enterprise 关联 / 详情 | 是 | |
| dwd_org_executive_info | 同上 | 高管 | enterprise_executive | 是 | |
| dwd_org_org_product_info | 同上 | 经营/产品活动 | enterprise_extra 等 | 是 | |
| dwd_org_annual_financial_info | 同上 | 年报财务 | enterprise_finance_history | 是 | |
| dwd_org_important_news_info | 同上 | 重点资讯 | enterprise_news | 是 | |
| dwd_org_stock_base | 同上 | 上市基本信息 | enterprise_base.is_listed / extra | 是 | |
| dwd_org_stock_finance_info | 同上 | 上市财务指标 | finance_history | 是 | |
| dwd_org_heis_info | 同上 | 高校机构 | 契约待补则先贴源 | 是 | live 或作 hels；承诺拼写 heis |
| dwd_research_institute_base_info | 同上 | 科研机构 | 待补契约 | 是 | |
| dwd_special_hongkong_company | 同上 | 香港企业 | 待补 | 是 | |
| dwd_special_taiwan_company | 同上 | 台湾企业 | 待补 | 是 | |
| dwd_special_aomen_company | 同上 | 澳门企业 | 待补 | 是 | |

## 招投标 / 产业链 / 风险（摘要 · 全表见 Wave A yaml）

| ODS 表（约定名） | 用途 | 落入 | Demo |
|---|---|---|---|
| dwd_bid_*_out（承诺四张出库表） | 招投标 | enterprise_bid | 是 |
| dwd_org_industry_tags / dwd_industry_chain_info 等 | 产业链归属 | enterprise_industry_chain | 是 |
| 风险承诺子集（见 Mapping §risk） | 司法/经营异常等 | risk_* | 是 |

完整 P0/P1 表名以 **`doc/md-extract/`（优先读）/ `doc/` xlsx（权威）** 为准；Wave A yaml 仅为施工速查镜像。本表不重复粘贴全量，避免双源漂移。

## 明确排除（本波不贴 / 不作 Demo ODS）

见 Wave A `exclude`：`dwd_company*`、`company_*`、`ods_*`、`*_bak_*`、`hycy_*` 等。
