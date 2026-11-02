# 产业链域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v2.2（2026-11-02：round1 核对 20 题答复落稿——链树列语义按真源实测重写 §3.1~3.4；答复全文见 `23-核对签收与答复.md`。基线对齐 10-19 三方承诺清单；变更史见 CHANGELOG）  
> **日期**：2026-11-02（v2.0 = 2026-10-20；v1.0 = 2026-09-01）  
> **范围**：GDF 三方承诺表（产业链要素库）→ 项目 DWD（`gkxlumenx_dwd.industry_chain_*`）字段级映射  
> **配套**：`产业链-DWD表设计-业务需求驱动(v5).md`（DDL 真源）· `storage/CHAIN/stores/mysql/dwd-chain.md`（入口）  
> **目标库**：`gkxlumenx_dwd`（MySQL）  
> **交付对象**：GDF 三方 ETL 团队  
> **GDF 派单包**：`data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v2/`（现行；v1 已历史）  
> **本期目的**：把 **链树 + 企业挂接** 洗进项目 DWD，后续 STAT 指标只读 DWD/ADS，不扫 ODS。

---


> **【GDF-CHAIN-WORKPACK-v2.0 · 2026-10-20】** 基线对齐 10-19 三方承诺清单：四表全在册、行数不变；live 实证 `dwd_industry_chain_info` 含 `parent_name` 列（新增 §3.1 使用）；10-19 Excel 纪要所列 `t_id`/`id`/`code_company_count` **live 库中不存在，不作源**。其余规则全部继承 v1.0。

## 0. 本期边界（指标前置）

STAT 第一波（企业数/分布/深圳/链总数/营收融资专利产品等）依赖：

| 需要的项目 DWD | 本包是否洗 | 说明 |
|---|---|---|
| `industry_chain` / `node` / `node_rel` | **洗** | 链树 |
| `industry_chain_entity_rel`（`entity_type=enterprise`） | **洗** | `entity_id=org_id` |
| `enterprise_base` / 年报 / 融资 / 专利 / 产品 | **不洗** | 认企业包 Mapping；本包只 JOIN 已有 `enterprise_base` |
| `industry_chain_news_event` | **不洗、闲置** | 禁止再灌本表 |
| `industry_analysis_*` | **不洗** | 李伟 09-01：B2 不同构写入项目 DWD；Wave A 可贴源 |
| 市调 / 投融资链表 / 历程 / 抽取 / 模型五表 | **不洗** | 无源或走 ENT/CMS/算法 |

禁止：指标 SQL 读供应方 `gkx.dwd_*`；把 Demo `gdf_sim` 合成键写成生产主键；用 `dwd_org_industry_chain_dtl` 冒充关单（承诺 Sheet 现表是 `dwd_org_industry_tags`）。

---

## 1. 映射分类

| 类型 | 说明 |
|---|---|
| **直接** | 源列写入目标列（可截断/类型转换） |
| **派生** | 由 `level` / 码前缀等规则生成，不另找源列 |
| **拆行** | JSON/多值列炸成多行后再映射 |
| **关联** | 必须 JOIN 项目 DWD 他表；对不上 **丢弃**，禁止编键 |

### 1.1 Q053（已冻结）

平台 `chain_id` / `node_id` / `industry_id` = 供应方 **INB 原文**。禁止把资讯侧 `IC*` 写入这些主键。

### 1.2 企业挂接键

`industry_chain_entity_rel.entity_id` = **`enterprise_base.org_id`**（与 STAT 口径、ENT hang 一致）。  
源只有 `credit_code` 时：`credit_code` = `enterprise_base.enterprise_code` → 取 `org_id`。对不上 **drop**，禁止把信用代码当成 `org_id`，禁止自造 `p:{credit}:…`。

v5 文案里企业权威键曾写 `enterprise_code`：本 Mapping **覆盖为生产写入 `org_id`**；信用代码可进 `ext.credit_code`。

### 1.3 与企业包的表重叠

企业包 Wave A 已列产业链四表。本包 **CHAIN 洗数以本 Mapping 为准**；企业包不得再把 `dwd_industry_chain_info` 洗进 `enterprise_*`。挂接辅表 `enterprise_industry_chain` 仍由企业域/hang 作业写，须与本包 `entity_rel` 同键（`org_id` + INB `node_id`）。

---

## 2. 源表 → 目标表总览

### 2.1 本期洗（P0）

| # | 源表（`gkxlumenx_ods`，同名贴源） | 目标表 | 类型 |
|---|---|---|---|
| 1 | `dwd_industry_chain_info`（层级 0+1，按 `parent_name`/码长判定；v2.2） | `industry_chain` | 直接+派生 |
| 2 | `dwd_industry_chain_info`（层级 2~7，按 `parent_name`/码长判定；v2.2） | `industry_chain_node` | 直接+派生 |
| 3 | `dwd_industry_chain_info`（父子） | `industry_chain_node_rel` | 派生（无独立边表） |
| 4 | `dwd_org_industry_tags` | `industry_chain_entity_rel` | 拆行+关联 |

### 2.1.1 可执行拆分

| 作业 | 输入 | 输出 | 当前可执行性 |
|---|---|---|---|
| `CHAIN-B1-TREE` | `dwd_industry_chain_info` | `industry_chain` / `industry_chain_node` / `industry_chain_node_rel` | **可执行** |
| `CHAIN-B3-ENTITY-REL` | `dwd_org_industry_tags` + `enterprise_base` | `industry_chain_entity_rel` | **条件可执行**；`enterprise_base` 未就绪时只阻塞本作业 |

`CHAIN-B2-INDANA`（六表同构入项目 DWD）**本期不执行、禁止写入**。B3 阻塞不得连带阻塞 B1。

### 2.2 本期只贴源、不洗（mirror_only）

| 源表 | 原因 |
|---|---|
| `dwd_org_industry_product_tags` | 产品 STAT 走 `enterprise_industry_product.product_name`，不进链 `entity_rel` 产品行 |
| `dwd_industry_chain_news_info` | 合规交付、无利用价值；禁止灌 `industry_chain_news_event` |
| 六张 `dwd_industry_analysis_*` | 李伟：不写入项目 `industry_analysis_*`；可 Wave A 贴 ODS |

### 2.3 明确不纳入本包

| 对象 | 原因 |
|---|---|
| `dwd_org_industry_chain_dtl` | 承诺产业链 Sheet **未检出**此表名；不以 ENT 旧路径关单 |
| `dwd_org_financing_info` → `industry_chain_investment_event` | 融资 STAT 走 ENT `enterprise_financing` × 挂接 |
| `dwd_org_important_news_info` | 企业包 → `enterprise_news`；**不当 CHAIN A4**（淮政玮 09-01） |
| 市调/历程/互动量/抽取/模型 | 无 ODS 或非 GDF 本包 |

---

## 3. 逐表字段

公共治理列（`id` / `source_*` / `etl_batch_id` / `data_version` / `valid_*` / `is_deleted` / `created_time` / `updated_time` / `ext`）按 v5 §3.3 系统生成，下表不重复。过滤：`is_deleted = 0`。

### 3.1 `dwd_industry_chain_info` → `industry_chain`（**v2.2 重写**：列语义按真源实测修正，round2 问 1~6 答复落稿）

> **真源列语义（2026-11-02 实测 1,273 行）**：`industry_code` = 自身 INB 码、全唯一、码长 7→21 与层级 0→7 一一对应；`industry_link_code`/`industry_link_name` = **直接父级**的码/名（12 根链为空串）；`parent_code` = 所属**根链中文名**；`parent_name` = **层级序号 0..7**；`level` 列全 0 **无效禁用**。分层判定用 `parent_name`（或码长），不用 `level`。

**行过滤**：层级 ∈ {0, 1}（按 `parent_name` ∈ {0,1} 或码长 ∈ {7,9} 判定）。层级 ≥2 不进本表。

| 源字段 | 目标字段 | 类型 | 转换 |
|---|---|---|---|
| `industry_code` | `chain_id` | 直接 | INB 原文，全唯一（round2 问 4 拍板，废止 `industry_link_code` 主键用法） |
| `industry_code` | `chain_code` | 直接 | 与 `chain_id` 同值 |
| `industry_name` | `chain_name` | 直接 | 自身名（round2 问 6 拍板；`industry_link_name` 是父名，不映射） |
| `industry_code` | `industry_id` | 派生 | L0：=自身码；L1：=所属根链码（= `industry_link_code`，即直接父级，如 `INB130301`→`INB1303`） |
| `industry_link_code` | `parent_chain_id` | 直接 | L0 为空串→NULL；L1=根链码。**不跳级**（round2 问 5 拍板） |
| `parent_name` | （层级判定 + 校验） | 派生 | 层级序号 0..7；只用于行过滤与校验，不落库 |
| `level` | — | **禁用** | 全 0，无区分度；禁止按 `level∈{0,1}` 分表（v2.0 旧规则废止） |
| （层级） | `chain_level` | 派生 | 0/1（= `parent_name` 数值） |
| （层级） | `chain_tier` | 派生 | `L0`/`L1` |
| — | `future_industry_flag` | 派生 | **按簇表派生（round2 问 17 拍板，弃 INB13 前缀）**：`industry_id` ∈ `gkxlumenx_dim.industry_cluster_map`（`cluster_group='fut'`，政策版 `sz-10+5-2026`）→ 1，否则 0。当前 fut 成员 6 条根链：机器人/具身智能/软件与信息服务/人工智能/低空经济/合成生物 |
| — | `status` | 派生 | `active` |
| `parent_code` | — | 不映射 | 是根链中文名，非码；根链归属已由 `industry_id` 表达 |
| `node_company_count` | — | 不映射 | 企业数走 ADS |
| — | `chain_short_name` / `chain_category` / `description` | 不映射 | 介绍正文 CMS |

**UK**：`chain_id` Upsert。**行数验收线：53（L0 12 + L1 41）**——超出即分层判定错误。

### 3.2 `dwd_industry_chain_info` → `industry_chain_node`（**v2.2 重写**）

**行过滤**：层级 ∈ {2..7}（按 `parent_name` ∈ {2..7} 或码长 ≥ 11 判定）。

| 源字段 | 目标字段 | 类型 | 转换 |
|---|---|---|---|
| `industry_code` | `node_id` / `node_code` | 直接 | INB 原文，全唯一 |
| `industry_link_code` | `chain_id` | 关联 | 自身**直接父级**码；父为 L1 链（层级=2）时即链表 `chain_id`；**v2.2 修正**：不再「沿祖先升到 L1 跳级归属」，L2~L7 的 `chain_id` = 直接父级码（父必在链表或节点表），沿 `parent_node_id`/`parent_chain_id` 上溯可达根链 |
| `industry_link_code` | `parent_node_id` | 直接 | **直接父级**码（round2 问 5 拍板，补齐父子指针）；父为 L1 链时（层级=2）置 NULL——此时归属由 `chain_id` 表达 |
| `industry_name` | `node_name` | 直接 | 自身名；`description` 同源可填（门户节点简介） |
| `parent_name` | （层级判定） | 派生 | `node_level` = `parent_name` 数值（2..7） |
| `industry_code` | `sort_no` | 派生 | **同 `chain_id` 内按 `industry_code` 升序序号（1,2,3…）**（round2 问 16 拍板，废止「末段解析数字」） |
| （排序） | `stage_code` | 派生 | **采用**（round2 问 18 拍板，不置 NULL）：同链按 `sort_no` 三等分 `upstream`/`midstream`/`downstream`，余数归 upstream |
| — | `status` | 派生 | `active` |
| — | `node_type` / `importance_level` / `node_path` | 不映射 | |
| `node_company_count` | — | 不映射 | ADS |

**UK**：`(chain_id, node_id)` Upsert。**行数验收线：1,220**。

### 3.3 → `industry_chain_node_rel`（v2.2 启用：节点表已带 `parent_node_id`，父子边随之生成）

只生成**树父子边**（相邻伪造 upstream 边仍禁止）。父为 L1 链的边不写（归属在 `node.chain_id`）。

| 目标字段 | 规则 |
|---|---|
| `relation_id` | `node-rel:{chain_id}:{source}:{target}`（≤64） |
| `chain_id` | 子节点的 `chain_id` |
| `source_node_id` | 父节点 `node_id`（仅当父也在 `industry_chain_node`） |
| `target_node_id` | 子 `node_id` |
| `relation_type` | `parent_child` |
| `relation_direction` | `directed` |
| `confidence` | 1.0 |
| `relation_weight` / `evidence_ref` | NULL |

父不在节点表（父是 L1 链）→ **不写边**，归属已在 `node.chain_id`。

### 3.4 `dwd_org_industry_tags` → `industry_chain_entity_rel`（v2.2 修订：解析格式与脏值钉死，命中率待重测）

**拆行**：挂点列（`industry_link_code` / `industry_code`）为**单引号列表字面量**（`['INB1333']`，非标准 JSON）——按此格式解析炸行（round1 附注确认）。空列表 `[]`（真源占 24.9%）整行丢弃进治理清单。**脏值处置（round2 问 19 拍板）**：中文路径名列表（如 `['原材料','中药材种植',…]`，1 行）、异常 `credit_code`（日期串 1 行、全角括号 1 行）→ 不洗、进治理清单（带证据）。禁止截断码位猜 INB。

**挂点**：

1. 码 = 某 `industry_chain_node.node_id` → 填 `node_id`，`chain_id` 取该节点。
2. 否则码 = 某 `industry_chain.chain_id` → `node_id` NULL（链级），`node_scope_key='__CHAIN__'`。
3. 否则 **drop**（含全部 `IC*`）。禁止截断码位猜 INB。

**企业键**：

| 源字段 | 目标字段 | 类型 | 转换 |
|---|---|---|---|
| `credit_code` | （关联） | 关联 | JOIN `enterprise_base.enterprise_code`；无匹配 drop |
| （关联结果） | `entity_id` | 关联 | `org_id` |
| — | `entity_type` | 派生 | `enterprise` |
| — | `relation_type` | 派生 | `belongs_to` |
| — | `role_type` | 派生 | `participant` |
| — | `is_primary` | 派生 | 1 |
| — | `relation_id` | 派生 | `er:{node_or_chain}:{org_id}`（≤64） |
| `company_name` | `ext.company_name` | 直接 | 不进独立列 |
| `credit_code` | `ext.credit_code` | 直接 | |

**全国/广东口径（round2 问 7）——待命中率重测后定**：round1 双方数字均不采信（GDF 真源抽样 15%；我方 ODS 残缺仅约 1,000 行）。流程：我方补灌 ODS 至真源全量 228 万（`CHAIN-ODS-SYNC-L01`）→ 真源全量重测 `credit_code`→`enterprise_base` 命中率 → round2 补充答复。本问不阻塞 Wave A 与 `CHAIN-B1-TREE`。

依赖：`enterprise_base` 就绪后运行（企业包 Mapping 3.1）。对账输出 drop 行数（无 org_id / 无 INB）。

### 3.5 行业分析六表（本期不写入项目 DWD）

`human:李伟` 2026-09-01：**禁止** `CHAIN-B2-INDANA`（不得把 `dwd_industry_analysis_*` 同构写入 `gkxlumenx_dwd.industry_analysis_*`）。不得借此灌 `industry_chain_news_event`。Wave A 可贴源到 `gkxlumenx_ods`，字段矩阵不进本期 Wave B。

资讯按链聚合仍受 **OPEN-CHAIN-MAP-06** 约束；未对照 INB 禁止猜码。

---

## 4. ETL 顺序

```text
1. Wave A 贴源（链四表 P0 wash 源；分析六表 mirror_only）
2. 建 industry_chain* 四张（不要求建 industry_analysis_*）
3. CHAIN-B1-TREE 洗链树
4. enterprise_base 就绪后运行 CHAIN-B3-ENTITY-REL
5. 禁止 CHAIN-B2-INDANA；禁止 INSERT industry_chain_news_event
```

---

## 5. 抽样与诚实

链树四表：INB、`entity_id`→`org_id`。  
分析六表：本期不洗 DWD，不做 DWD 抽样。

---

## 6. 开放项

| ID | 项 | 状态 |
|---|---|---|
| OPEN-CHAIN-MAP-01 | `stage_code` 三等分是否保留 | **已定（round2 问 18）：采用，同链按 sort_no 三等分** |
| OPEN-CHAIN-MAP-02 | `future_industry_flag` 规则 | **已定（round2 问 17）：按簇表 fut 组派生，弃 INB13 前缀** |
| OPEN-CHAIN-MAP-03 | 产品 tags → entity_rel product | 本期不洗 |
| OPEN-CHAIN-MAP-06 | 分析 `industry_code` → INB `chain_id` | 挡后续按链资讯；本期 B2 不洗 |
| OPEN-CHAIN-MAP-07 | 链上企业全国/广东口径 | **待 ODS 补灌后命中率重测（round2 问 7）** |
| OPEN-CHAIN-FLOW-01 | 正式 DAG 名 | 产线回写 |
| OPEN-CHAIN-FLOW-02 | 正式图空间名 + 上图/rebuild 契约 + 点数稳定判定 | 架构师确认中，round2 随 `12` 补（round2 问 8~13） |

---

## 7. 资讯口径（2026-09-01 淮政玮）

| 角色 | 表 |
|---|---|
| ODS（可贴源） | `dwd_industry_analysis_*` 六张 |
| 项目 DWD 六表 | **本期不写**（李伟：B2 不执行） |
| 闲置 | `industry_chain_news_event`（不洗） |
| 企业维（非链 A4） | `enterprise_news` |
| 废 | `dwd_industry_chain_news_info` |

A5/A6：六表无热度/情感，继续挂起。

