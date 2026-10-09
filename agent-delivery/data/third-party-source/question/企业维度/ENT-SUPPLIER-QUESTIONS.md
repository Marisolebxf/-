# 企业库 — 给三方供应方的问题清单

```yaml
---
doc_id: ENT-SUPPLIER-QUESTIONS
element: ENT
role: source
status: draft
version: "2026-09-10"
updated: 2026-09-10
owner: human:徐滕强
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。聚类来自 COVER-STAT 细稿现网探针（2026-08-27～31 live `gkx`），本叶未再探库。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 DWD/ADS（`enterprise_*` / `region_id` 派生列名）；`related_entities`；甲方口径 Q-*；产业链目录叶子码（CHAIN）；CMS 明星名单；请对方 COUNT。  
> **2026-09-03 精简尺（收窄）**：只关「缺 `org_id` / 信用代码、但同一行已有**企业名称**、项目侧可后关联主体」这一类。缺稳定区划码 / 产业 INB / 标签码、空列、空表、无边、交付不稳、脏到不能用，**仍问**。  
> **ENT-P0-2 纠偏（2026-09-10）**：勿把项目 DWD `enterprise_industry_chain.node_id` 空 / `chain_code=IC-*` 写成入站缺列；入站问的是 tags 码列与拆行规则。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| ENT-P0-1 | P0 | `dwd_org_base_info`（缺行政区划码列） | 【缺稳定码】现网仅城市中文名（如 `city='深圳市'` 约 17562/40020）。市级名可后对照市码，**不够**区县/`4403%` 过滤。请交付主档码列（建议 6 位 adcode）或 `org_id`↔区划码对照（表名 + 样例 3 行）。随口径修订。 | `M_ENT_SZ_COUNT`, `M_ENT_REGIONAL_COUNT`, `M_ENT_SZ_CHAIN_POSITION`, `M_ENT_SZ_LIST_TOPIC`, `M_ENT_REGIONAL_COUNT_TOPIC` | 2026-09-03 |
| ENT-P0-2 | P0 | `dwd_org_industry_tags.industry_code` / `industry_link_code` | 【确认码列与拆行】企业↔链官方源=本表（`dtl` 已弃用）。现网码值多为列表字面量（如 `['INB1333','INB1502']`），不是一行一码。请书面确认：① 链码/环节码官方列名；② 是否均为目录 `INB*`（与 `dwd_industry_chain_info` 同源）；③ 多码拆行规则与空值；④ 与主档 JOIN 键；⑤ 样例 3 行（主键+码原值）。**不要**用产业中文名当节点。**不问**我方 DWD `node_id`/`IC-*`（项目灌数问题）。随口径修订。 | `M_ENT_DOMAIN_COVERAGE_COUNT`, `M_ENT_DOMAIN_COVERAGE_BREADTH`, `M_ENT_CHAIN_COMPLETENESS`, `M_ENT_DOMAIN_DIST_TOPIC`, `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`, `M_ENT_CHAIN_STAGE_COVERAGE` | 2026-09-10 |
| ENT-P0-3 | P0 | （缺已确认边）供应商–客户 | 【无边】入站 **无已确认** 供应关系表。股东/投资/产业标签不是供应边。候选 `dwd_org_sc_info`（live≈1716，两端企业+信用代码，`type` 仅 1/2）。请书面确认：是否供应关系表；`type` 1/2 谁供谁客；样例 3 行。未确认不洗不造。随口径修订。 | `M_ENT_SUPPLIER_COUNT` | 2026-09-03 |
| ENT-P0-4 | P0 | `dwd_org_annual_financial_info.development_employee` | 【空列】现网 517597 行 **全部 SQL NULL**，有效 >0 为 0。请确认空值约定、后续批次能否给出研发人员人数、主键（`org_id`+年）。国外 `dwd_foreign_org_annual_financial_info.rd_staff` 同期亦全空。随口径修订。 | `M_ENT_RESEARCHER_COUNT` | 2026-09-03 |
| ENT-P0-5 | P0 | `dwd_org_annual_financial_info.arch_development_am` / `operating_revenue` | 【空列】研发经费、营业收入样例行全 NULL。请确认列是否正式交付、空值约定、年主键。禁止把 `dwd_rd` 当企业 R&D 经费。随口径修订。 | `M_ENT_AVG_RD_INVESTMENT`, `M_ENT_RD_INVESTMENT_RATIO` | 2026-09-03 |
| ENT-P0-7 | P0 | `dwd_org_tech_tag`（标签码） | 【缺稳定码】现网多为中文名（如「高新技术企业」2807 行），**无** `tag_code`。六类要 `high_tech` / `foreign` / `sme` / `listed` / `little_giant` / `little_giant_pro`。名称对照只能盖住已出现的词，盖不住缺失类。请给码列或名称↔码对照 + 认定起止日。随口径修订。 | `M_ENT_HIGH_TECH_COUNT`, `M_ENT_TYPE_COUNT` | 2026-09-03 |
| ENT-P1-1 | P1 | `dwd_patent_legal.status` | 【口径枚举】列有值，主值是「授权」不是「有效」。请给合法值清单；二者是否同一状态、如何区分失效。随口径修订。 | `M_ENT_PATENT_VALID_COUNT`, `M_ENT_PATENT_GRANT_COUNT` | 2026-09-03 |
| ENT-P1-2 | P1 | `dwd_org_important_news_info`（整表） | 【交付不稳】2026-08 行数在 0～19983 间晃过，有空窗。请书面过滤规则、主键、日期列、与 `org_id` 关联键；后续批次是否稳定。随口径修订。 | `M_ENT_BASE_97_4`, `M_ENT_DEV_HISTORY` | 2026-09-03 |
| ENT-P1-3 | P1 | `dwd_forg_base_info`（整表） | 【空表】国外企业主档现网 **0 行**。请确认是否交付、主键、`incorporation_date` 空值约定。随口径修订。 | `M_ENT_NEW_COUNT_Y` | 2026-09-03 |
| ENT-P1-4 | P1 | `dwd_org_executive_info.executives_name` | 【质量不可用】列义应是单人姓名。现网至少 53 行顶满 255，内容是股东名单+出资+占比，不是姓名。请确认官方语义、最大长度、脏行是错灌还是允许拼串。项目 DWD 加宽不问供应方。随口径修订。 | —（无独立 metric_id） | 2026-09-03 |
| ENT-P2-1 | P2 | `dwd_org_base_info.org_id` / 信用代码 | 【主键规则】请确认机构主键与统一社会信用代码 1:1、空值与历史码。跨表 JOIN 稀疏时会 drop。**不是**再要一遍「有企业名请补 org_id」（那类见已关的 P0-6）。随口径修订。 | `M_ENT_TOTAL_COUNT`, `M_ENT_NEW_COUNT_Y` | 2026-09-03 |

<!-- 一行一列聚类。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。二次指标 / CMS-only 不另开题。 -->

---

# 分析日志（新的在上）

## 2026-09-10（纠偏 ENT-P0-2 问法）

- 问题：旧稿写「现网 `node_id` 空、`chain_code` 曾见 `IC-*`」，易被读成入站 tags 缺列。
- 事实拆分：
  - `node_id` / `IC-*`：项目 DWD `enterprise_industry_chain` 样例/未按 INB 灌数（COVER-STAT 2026-08-27～28 探针）；**不问供应方**。
  - 入站真缺口：`dwd_org_industry_tags` 的 `industry_code` / `industry_link_code` 现网多为 `INB*` 列表字面量，缺书面拆行、空值、与主档 JOIN、与目录表对齐规则。
- 现行表：重写 ENT-P0-2「问什么」；Q-id 不改号。sidecar ENT 挂本题的 summary 同步改成「tags JSON/列表码需确认拆行」。

## 2026-09-03（回捞：只关名称→主体）

- 监管人反馈：上一刀把码缺口 / 交付不稳 / 脏列也关了，问题被卡丢。
- 尺子收窄：只关「缺 `org_id` 但已有**企业名称**」→ **仅关 ENT-P0-6**（专利受让人有名）。
- 现行 **11** 行（原 12 − P0-6）。Q-id 不重编号。问什么加类型标：空列 / 空表 / 无边 / 缺稳定码 / 交付不稳 / 口径枚举 / 质量不可用 / 主键规则。
- **回捞**：P0-1 区划码、P0-2 INB、P0-7 标签码、P1-1 授权/有效枚举、P1-2 资讯晃、P1-4 高管脏串、P2-1 跨表主键规则。
- sidecar：回捞题改回缺口摘要；P0-6 仍写「有名关联主体，不问供应方」。
- 未改 seed / D3；未探库；未动综合 / 其他维。

## 2026-09-03（精简：过窄，已被回捞取代）

- 当时按「有名/中文标签可后关联」关了 8 题，现行只留 4。监管人随后指出卡丢。以本节之上「回捞」为准。

## 2026-09-03

- 订正（监管人确认，不新开题）：
  - ENT-P0-3：已提交稿把 `dwd_org_sc_info` 写成「证照、都不是供应边」。改为**候选供应关系表**，先问对方认不认 `type` 1/2；未确认不洗不造。
  - ENT-P1-4：现行「问什么」去掉「我方 DWD 加宽」。加宽仍只写抽样备注，不问供应方改项目表。
- sidecar：`M_ENT_SUPPLIER_COUNT` summary 同步 P0-3；无独立 metric 的 P1-4 仍不 upsert。
- 声明：未改 seed / D3；未探库。

---

## 2026-09-02

- 来源：demo 企业灌数 `apply_ods_to_dwd` → `enterprise_executive` 报 `DataError 1406 Data too long for column 'executive_name' at row 406`（trace 见当日联调）。
- 入站：`demo_gkxlumenx_ods.dwd_org_executive_info.executives_name` `varchar(255)`；`MAX(CHAR_LENGTH)=255`；`CHAR_LENGTH>128` 共 **53** 行。样例前缀是「CZGA EDUCATION HOLDING LIMITED…（万元）…%%…股权投资基金」，不是人名。职务列 `executives_position` 最长 28，未超。
- 项目侧对照（**不问供应方改我方表**）：`demo_gkxlumenx_dwd.enterprise_executive.executive_name` `varchar(128)`；正式库 `gkxlumenx_dwd` 同列 `varchar(100)`。
- 结论：**应扩展项目 DWD 列宽对齐入站（至少 255，或按对方官方长度）**，截断只是 STRICT 临时挡 1406，不能当终态。同时要对方书面确认该列到底是姓名还是被错灌的股东串。
- 问题表：

| Q-id | 入站表.列 | 现象 | 请对方确认 |
|------|-----------|------|------------|
| ENT-P1-4 | `dwd_org_executive_info.executives_name` | 53 行顶满 255；内容含万元/占比 | 语义、官方长度、脏行是否错灌 |

- sidecar：无独立 metric_id，本条不 upsert `source-gap-index.yaml`。
- 声明：项目 DWD 加宽走 GDF/DDL，不写进发给对方的问句正文。

---

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
| ENT-P0-2 | `dwd_org_industry_tags.industry_code` / `industry_link_code` | 码多为 `INB*` 列表字面量，非一行一码（旧稿误写项目 DWD `node_id`/`IC-*`，2026-09-10 已纠） | 列名、拆行、空值、与主档 JOIN、与目录 INB 对齐 |
| ENT-P0-3 | 缺已确认供应边 | 股东/投资不是边；`dwd_org_sc_info` 候选 | 是否供应表；type 1/2 |
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
- `executives_name`（ENT-P1-4）：入站已是 255 且有顶格脏串。项目侧 `enterprise_executive.executive_name` **应加宽对齐入站**（至少 255），禁止把截断当终态；加宽本身不问供应方。
