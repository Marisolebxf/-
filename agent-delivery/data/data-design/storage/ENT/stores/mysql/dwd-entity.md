# MySQL DWD · 企业实体（工商）

```yaml
---
doc_id: ENT-STORE-DWD-ENTITY
element: ENT
role: store-mysql
status: draft
version: "2026-09-03"
updated: "2026-09-03"
engine: mysql
as_built_source: data-design/企业/DWD表结构设计-企业工商表-MySQL-v3.1.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **地位**：项目侧 DWD **工商/实体** as-built 入口（storage 树）。  
> **DDL 真源**：[`DWD表结构设计-企业工商表-MySQL-v3.1.md`](../../../企业/DWD表结构设计-企业工商表-MySQL-v3.1.md)（**禁止**在本文件粘贴整份 DDL）。  
> **库名**：正式 `gkxlumenx_dwd`；Demo 实例见 [`../../etl/pipeline-demo-mock.md`](../../etl/pipeline-demo-mock.md)（目标 `demo_gkxlumenx_dwd`）。  
> **结构评审**：`status=draft`；流图会签 **不算** 本文件 approved。

## 1. 边界

| 含 | 不含 |
|---|---|
| `enterprise_*` 工商/实体明细（见下表） | 指标预聚合 → [`dwd-aggregate.md`](./dwd-aggregate.md) |
| | `risk_*` → [`dwd-risk.md`](./dwd-risk.md) |
| | ADS 算法结果 → [`ads.md`](./ads.md) |

统一约定：主键 `id bigint AUTO_INCREMENT`；企业关联键优先 `org_id`（与工商 v3.1 / 风险域 collation 对齐）。

## 2. 表清单（as-built · 2026-09-03 ALIGN）

> 列名真源：工商 v3.1 + `agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-DWD-ALIGN-四类分类表.md`。demo 与正式库同一套 ADD。

| # | 表名 | 用途（一句话） | 关键键 |
|---:|---|---|---|
| 1 | `enterprise_base` | 企业主数据 | `org_id` UK 语义；`enterprise_code` |
| 2 | `enterprise_extra` | 详情低频扩展 | `org_id` |
| 3 | `enterprise_executive` | 高管 | `org_id` |
| 4 | `enterprise_bid` | 招投标 | `org_id` |
| 5 | `enterprise_news` | 资讯 | `org_id` |
| 6 | `enterprise_finance_history` | 财务历史（Q-WP3-22：`net_profit` 升为设计列） | `org_id` |
| 7 | `enterprise_financing` | 融资事件 | `org_id`；字段契约 `finance_round/amount/...` |
| 8 | `enterprise_industry_chain` | 产业链归属 / **企业上链** | `org_id` + INB `chain_code`/`node_id`（见 §5） |
| 9 | `enterprise_tag` | 企业标签 | `org_id` |
| 10 | `enterprise_invest` | 对外投资 | `org_id` |
| 11 | `enterprise_supply_chain` | 供应链 | `org_id` |
| 12 | `enterprise_cooperation` | 合作 | `org_id` |
| 13 | `enterprise_innovation_carrier` | 创新载体 | `org_id` |
| 14 | `enterprise_parent_subsidiary` | 母子公司 | `org_id` |
| 15 | `enterprise_history_name` | 曾用名 | `org_id` |
| 16 | `enterprise_patent_detail` | 专利明细 | `org_id` + `patent_id` |
| 17 | `enterprise_patent_history` | 专利历史快照 | `org_id` |
| 18 | `enterprise_fund_project` | 基金项目 | `org_id` |
| 19 | `enterprise_chain_patent` | 链专利（空表可有） | `org_id` |
| 20 | `enterprise_industry_product` | 产业产品（空表可有） | `org_id` |
| 21 | `enterprise_recruit` | 招聘（2026-08-12 新增） | `org_id`；UK 见工商 v3.1 §7 |
| 22 | `enterprise_patent_org_rel` | 专利-企业角色关系（v3） | `(patent_id, org_id, party_role, party_sequence)` |
| 23 | `enterprise_shareholder` | 股东（2026-09-02 新增，Q-WP3-17） | `org_id` + `shareholder_name`；**不上图、不灌 ES**；禁止写进 `enterprise_supply_chain` |

**国外机构**（`enterprise_forg_*` 六表）：见工商 v3.1 §6；Mapping 明细 §2.5 / §3.15。不在上表国内计数内。

行数/索引/纠偏记录以工商 v3.1 §1–2 为准（含 `enterprise_industry_chain.org_id` NULL 债、删除 `enterprise_base2`）。

## 3. 读写

| 写 | 读 |
|---|---|
| GDF / Demo ETL 模拟 GDF；过渡 mockgen 直写 DWD（非 ODS 主路径） | ETL→ADS/ES/Nebula；算法按需；**Java 禁扫** |

## 4. 禁止

- 本文件复制大段 CREATE TABLE  
- 以三方 `gkx-mysql-raw` 倒逼本层字段  
- 未评审即标 `approved`

## 5. 上链（Demo · `ENT-CHAIN-HANG-MOCK-L01`）

企业挂到产业链 **INB 节点**（不是行业分析抽边、不是图边 LLM）。本表字段复用 v3.1：`org_id` + `chain_code`/`chain_name` + `node_id`/`node_name`，**不另开列名**。

| 项 | 口径 |
|---|---|
| 企业键 | **`org_id`**（`enterprise_base`）；禁止亿集 vid |
| 信用代码 | ODS/`enterprise_code` = `credit_code`；对不上 org_id → **drop**，禁止乱编 |
| 链侧对称表 | CHAIN `industry_chain_entity_rel`（`entity_type=enterprise`，`entity_id=org_id`，`belongs_to`） |
| 过程全文 | [`../../../CHAIN/etl/pipeline-ent-hang.md`](../../../CHAIN/etl/pipeline-ent-hang.md) |
| 脚本 | `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/run_ent_chain_hang.py` |

历史债：正式库本表 `org_id` 可空（工商 v3.1 §1）。Demo `--apply` 只写能对齐的行。ENT `gdf_sim.map_industry_chain` 仍可能写入 `node_id` 空的 domain 占位；上链脚本对已对齐 `org_id` **覆盖为 INB**。
