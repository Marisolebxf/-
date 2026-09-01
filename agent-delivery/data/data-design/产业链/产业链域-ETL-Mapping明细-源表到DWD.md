# 产业链域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v1.0  
> **日期**：2026-09-01  
> **范围**：GDF 三方承诺表（产业链要素库）→ 项目 DWD（`gkxlumenx_dwd.industry_chain_*`）字段级映射  
> **配套**：`产业链-DWD表设计-业务需求驱动(v5).md`（DDL 真源）· `storage/CHAIN/stores/mysql/dwd-chain.md`（入口）  
> **目标库**：`gkxlumenx_dwd`（MySQL）  
> **交付对象**：GDF 三方 ETL 团队  
> **GDF 派单包**：`data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v1/`  
> **本期目的**：把 **链树 + 企业挂接** 洗进项目 DWD，后续 STAT 指标只读 DWD/ADS，不扫 ODS。

---

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
| 1 | `dwd_industry_chain_info`（`level`∈{0,1}） | `industry_chain` | 直接+派生 |
| 2 | `dwd_industry_chain_info`（`level`≥2） | `industry_chain_node` | 直接+派生 |
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

### 3.1 `dwd_industry_chain_info` → `industry_chain`

**行过滤**：`level IN (0, 1)`（数值 0/1）。`level`≥2 **不**进本表。

| 源字段 | 目标字段 | 类型 | 转换 |
|---|---|---|---|
| `industry_link_code` | `chain_id` | 直接 | INB 原文；空行丢弃 |
| `industry_link_code` | `chain_code` | 直接 | 与 `chain_id` 同值（Wave1） |
| `industry_code` | `industry_id` | 派生 | L0：`industry_id = chain_id`。L1：取所属 L0 的 INB（优先 `industry_code` 若已是 L0 INB，否则沿 `parent_code` 升到 `level=0`） |
| `industry_link_name`（空则 `industry_name`） | `chain_name` | 直接 | |
| `parent_code` | `parent_chain_id` | 直接 | L0 写 NULL |
| `level` | `chain_level` | 直接 | 0/1 |
| `level` | `chain_tier` | 派生 | 0→`L0`；1→`L1` |
| — | `future_industry_flag` | 派生 | `industry_id` 前缀 `INB13`→1，否则 0（团队临时默认，可配置） |
| — | `status` | 派生 | `active` |
| `node_company_count` | — | 不映射 | 企业数走 ADS |
| — | `chain_short_name` / `chain_category` / `description` | 不映射 | 介绍正文 CMS |

**UK**：`chain_id` Upsert。

### 3.2 `dwd_industry_chain_info` → `industry_chain_node`

**行过滤**：`level >= 2`。

| 源字段 | 目标字段 | 类型 | 转换 |
|---|---|---|---|
| `industry_link_code` | `node_id` / `node_code` | 直接 | INB 原文 |
| `parent_code` | `chain_id` | 关联 | 必须能在 `industry_chain.chain_id` 找到（通常为 L1）；找不到则沿祖先升到 L1，仍没有则 **drop** |
| `parent_code` | `parent_node_id` | 直接 | 父级亦为节点（level≥2）时填写；父为 L1 链则 NULL |
| `industry_link_name` | `node_name` | 直接 | |
| `industry_link_name` | `description` | 直接 | 可与名称相同；门户节点简介读本列 |
| `level` | `node_level` | 直接 | |
| `industry_link_code` 末段 | `sort_no` | 派生 | 可解析数字则用，否则按同 `chain_id` 稳定排序 |
| — | `stage_code` | 派生 | 可选：同链按 `sort_no` 三等分 `upstream`/`midstream`/`downstream`；无把握则 NULL，禁止乱填 |
| — | `status` | 派生 | `active` |
| — | `node_type` / `importance_level` / `node_path` | 不映射 | |
| `node_company_count` | — | 不映射 | ADS |

**UK**：`(chain_id, node_id)` Upsert。

### 3.3 → `industry_chain_node_rel`

无 ODS 边表。只生成 **树父子边**（不要 Demo 那种按 sort 相邻伪造 upstream，除非另拍）。

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

### 3.4 `dwd_org_industry_tags` → `industry_chain_entity_rel`

**拆行**：`industry_link_code`（及如有的 `industry_code`）若为 JSON 数组 / 分隔多值，炸成一行一码。空码丢弃。

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

`node_scope_key` = `COALESCE(node_id, '__CHAIN__')`。

依赖：**Wave B 本作业启动前** `gkxlumenx_dwd.enterprise_base` 已有对应企业（企业包 Mapping 3.1）。对账输出 drop 行数（无 org_id / 无 INB）。

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
| OPEN-CHAIN-MAP-01 | `stage_code` 三等分是否保留 | 可空 |
| OPEN-CHAIN-MAP-02 | `future_industry_flag` 前缀规则 | 临时 INB13 |
| OPEN-CHAIN-MAP-03 | 产品 tags → entity_rel product | 本期不洗 |
| OPEN-CHAIN-MAP-06 | 分析 `industry_code` → INB `chain_id` | 挡后续按链资讯；本期 B2 不洗 |
| OPEN-CHAIN-FLOW-01 | 正式 DAG 名 | 产线回写 |

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

