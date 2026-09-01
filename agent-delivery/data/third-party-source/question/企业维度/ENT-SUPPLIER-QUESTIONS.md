# 企业库 — 给三方供应方的问题清单

```yaml
---
doc_id: ENT-SUPPLIER-QUESTIONS
element: ENT
role: source
status: draft
version: "2026-09-01"
updated: 2026-09-01
owner: human:徐滕强
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。聚类来自 COVER-STAT 细稿现网探针（2026-08-27～31 live `gkx`），本叶未再探库。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 DWD/ADS（`enterprise_*` / `region_id` 派生列名）；`related_entities`；甲方口径 Q-*（Q010 / Q017 / Q038 / Q048 / Q068 / QC01 / Q-E32-01 等）；产业链目录 `dwd_industry_chain_info` 叶子码（CHAIN 切片，李伟）；CMS 明星名单；请对方替我们 COUNT。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| ENT-P0-1 | P0 | `dwd_org_base_info`（缺行政区划码列） | 现网仅有城市中文名（如 `city='深圳市'` 约 17562/40020），**无**稳定行政区划码（建议 6 位 adcode / 国标区划码）。请交付主档上的码列，或 `org_id`↔区划码对照表（表名 + 样例 3 行）。不要只用中文市名。随口径修订。 | `M_ENT_SZ_COUNT`, `M_ENT_REGIONAL_COUNT`, `M_ENT_SZ_CHAIN_POSITION`, `M_ENT_SZ_LIST_TOPIC`, `M_ENT_REGIONAL_COUNT_TOPIC` | 2026-09-01 |
| ENT-P0-2 | P0 | `dwd_org_industry_tags`（产业/环节码） | 企业上链码能否对上 `INB*`（链根如 `INB1701`、叶子如 `INB17010102`）？现网项目侧 `node_id` 空、`chain_code` 曾见 `IC-*` 非 INB。请确认：码列名、合法枚举、空值约定；`org_id` 与主档如何 JOIN。随口径修订。 | `M_ENT_DOMAIN_COVERAGE_COUNT`, `M_ENT_DOMAIN_COVERAGE_BREADTH`, `M_ENT_CHAIN_COMPLETENESS`, `M_ENT_DOMAIN_DIST_TOPIC`, `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`, `M_ENT_CHAIN_STAGE_COVERAGE` | 2026-09-01 |
| ENT-P0-3 | P0 | （缺表）供应商–客户边 | 入站 **无** 企业供应关系表。`dwd_org_shareholder_info`（股东）、`dwd_org_invest_info`（投资）、`dwd_org_sc_info`（证照）、产业链标签 **都不是** 供应商边。请交付：表名 + 主键 + `org_id`/`related_org_id`/`relation_type` 样例 3 行；`relation_type` 合法值（至少含 supplier）。随口径修订。 | `M_ENT_SUPPLIER_COUNT` | 2026-09-01 |
| ENT-P0-4 | P0 | `dwd_org_annual_financial_info.development_employee` | 现网 517597 行 **全部 SQL NULL**，有效 >0 为 0（空置率 100%）。请确认：空值约定；后续批次能否给出研发人员人数；主键（`org_id`+年）。国外 `dwd_foreign_org_annual_financial_info.rd_staff` 同期 18193 行亦全空。随口径修订。 | `M_ENT_RESEARCHER_COUNT` | 2026-09-01 |
| ENT-P0-5 | P0 | `dwd_org_annual_financial_info.arch_development_am` / `operating_revenue` | 研发经费、营业收入样例行全 NULL（上市财务表不采用）。请确认列是否正式交付、空值约定、年主键。禁止把临床试验表 `dwd_rd` 当企业 R&D 经费。随口径修订。 | `M_ENT_AVG_RD_INVESTMENT`, `M_ENT_RD_INVESTMENT_RATIO` | 2026-09-01 |
| ENT-P0-6 | P0 | `dwd_patent_assignees.name` / `dwd_patent.first_current_assignee_name` | 受让人目前是名称，需映射到机构 `org_id`。请确认能否配统一社会信用代码 / 组织机构代码；第一专利权人是否稳定等于 `sequence=1` 或主表 `first_current_assignee_name`。随口径修订。 | `M_ENT_PATENT_TOTAL`, `M_ENT_PATENT_GRANT_COUNT`, `M_ENT_KEY_TOTAL` | 2026-09-01 |
| ENT-P0-7 | P0 | `dwd_org_tech_tag`（标签码） | 现网多为中文名称（如「高新技术企业」2807 行），**无**稳定 `tag_code`（我方需要 `high_tech` / `foreign` / `sme` / `listed` / `little_giant` / `little_giant_pro`）。请交付码列或名称↔码对照（表名 + 样例 3 行）；认定起止日是否另有列。随口径修订。 | `M_ENT_HIGH_TECH_COUNT`, `M_ENT_TYPE_COUNT` | 2026-09-01 |
| ENT-P1-1 | P1 | `dwd_patent_legal.status` | 现网主值是「授权」不是「有效」。请给合法值清单；「授权」与「有效」是否同一状态、如何区分失效。随口径修订。 | `M_ENT_PATENT_VALID_COUNT`, `M_ENT_PATENT_GRANT_COUNT` | 2026-09-01 |
| ENT-P1-2 | P1 | `dwd_org_important_news_info`（整表） | 2026-08 行数在 0～19983 间晃过。请书面过滤规则（`is_deleted` 等）、主键、日期列名、与 `org_id` 关联键；后续批次行数是否稳定。随口径修订。 | `M_ENT_BASE_97_4`, `M_ENT_DEV_HISTORY` | 2026-09-01 |
| ENT-P1-3 | P1 | `dwd_forg_base_info`（整表） | 国外企业主档现网 **0 行**。请确认是否交付、主键、`incorporation_date` 空值约定。随口径修订。 | `M_ENT_NEW_COUNT_Y` | 2026-09-01 |
| ENT-P2-1 | P2 | `dwd_org_base_info.org_id` / 信用代码 | 请确认机构主键与统一社会信用代码 1:1、空值与历史码规则。跨表 JOIN 稀疏时我方 drop 对不上的行。随口径修订。 | `M_ENT_TOTAL_COUNT`, `M_ENT_NEW_COUNT_Y` | 2026-09-01 |

<!-- 一行一列聚类。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。二次指标 / CMS-only 不另开题。 -->

---

# 分析日志（新的在上）

## 2026-09-01

- 本批算法类型：STAT 为主 / COMPUTE 二次跳过 / GRAPH 0 / MODEL 跳过（五维分等） / third_party 0 / UNKNOWN 0 / **MIXED 跳过**
- 本批范围：`metrics/calc-logic/ENT/` COVER-STAT 细稿（约 80 叶）；**STAT/COMPUTE 原料列**。禁止超 `DATA-SUPPLIER-Q-ENT-L01`。
- D1 快照：本会话 MCP `metric-registry` 不可用；不打开 seed/矩阵 YAML。草案仍出题并标「随口径修订」。禁止改 D3 改绿。
- 入站抽样：沿用细稿 live `gkx` 探针（2026-08-27 `dwd_patent*` / 标签；2026-08-28 主档深圳行；2026-08-31 年报研发人员）。**本叶未再探库。**
- 跳过、不进对外清单：
  - 二次（`<- metric:`）：`M_ENT_CITY_AVG_TECH_POWER`、`M_ENT_TECH_RANK`、`M_ENT_COMPETITIVENESS_RANK`、`M_ENT_SHORTBOARD_COUNT`、`M_ENT_CITY_DENSITY`、`M_ENT_ATTRACT_SCORE`、`M_ENT_CULTIVATE_SCORE`、`M_ENT_RECOMMEND_COUNT`、全部 `M_ENT_KEYPANO_*`（除根 `M_ENT_KEY_TOTAL` 挂专利映射进 P0-6）、`M_ENT_TYPE_DIST_TOPIC`
  - CMS-only：`M_ENT_STAR_ENTERPRISE_COUNT`
  - MIXED / MODEL 分：`M_ENT_TECH_SCORE`、`M_ENT_BUSINESS_SCORE`、`M_ENT_INDUSTRY_MATCH_SCORE`、`M_ENT_PAINPOINT_SEVERITY`、`M_ENT_CLUSTER_INDEX` 等（先拆类型再问）
  - 项目自建缺口（无独立目标表 / 缺项目列）：不问供应方
  - 产业链目录叶子 / `dwd_industry_chain_info.position`：CHAIN 切片
  - 甲方 Q010/Q016/Q017/Q038/Q048/Q068/QC01/Q-E32-01：不改写
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| ENT-P0-1 | 主档缺区划码 | `city='深圳市'` 17562；无 adcode | 加码列或对照表 + 3 行 |
| ENT-P0-2 | `dwd_org_industry_tags` | node/INB 对不上；IC-* | INB 码列、JOIN 键、空值 |
| ENT-P0-3 | 缺供应边表 | 股东/投资/证照对象错 | 表名 + relation_type 样例 |
| ENT-P0-4 | `development_employee` | 100% NULL（517597） | 能否补人数；国外 rd_staff 同 |
| ENT-P0-5 | `arch_development_am` / `operating_revenue` | 样例全 NULL | 正式交付与空值；非 `dwd_rd` |
| ENT-P0-6 | 专利受让人名称 | 86028 / 70000 行；无信用代码 | 稳定码 + 第一权利人规则 |
| ENT-P0-7 | `dwd_org_tech_tag` | 名称无码；六类不全 | tag_code 或对照表 |
| ENT-P1-1 | `dwd_patent_legal.status` | 主值「授权」非「有效」 | 合法枚举 |
| ENT-P1-2 | 重点资讯表 | 行数 0～19983 晃 | 过滤规则与主键 |
| ENT-P1-3 | `dwd_forg_base_info` | 0 行 | 是否交付、注册日 |
| ENT-P2-1 | `org_id` / 信用代码 | 跨表 JOIN 稀疏 | 1:1 与空值规则 |

- 声明：草案口径标「随口径修订」。一列一题，未按 80 指标拆题。
- sidecar：本批 upsert 卡住的 STAT 原料指标（同一 q_id 可多指标；跳过二次/CMS/MIXED）。清单见 `source-gap-index.yaml`。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 ENT-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |

---

## 抽样备注（项目侧，不发给对方也可）

- 深圳过滤目标是 `region_id LIKE '4403%'`，那是**项目**派生列；供应方只需给稳定区划码原料。
- 六类类型禁止用 `org_size` / `enterprise_type` / `is_listed` 冒充；只问标签码。
- 图谱 hang、项目 DWD 灌数、GDF Mapping **不问**供应方。
