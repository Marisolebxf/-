# 产业链域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v2.3（2026-11-03：round2 答复落稿——node.chain_id 改所属 L1 链、parent_node_id 补直接父级、边表改真父子 1,055 条、stage_code 定 NULL；详见 `23-核对签收与答复.md` round2 节。v2.2=round1 答复；基线对齐 10-19 清单）  
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

### 3.0 三方 `dwd_industry_chain_info` → DWD 定稿

三方列里的值不在列名位置。下表是 2026-11-02 用「谐波减速器」对三方原列和 demo ODS 核对后的结果，作为本包定稿。GDF 贴源原样镜像进 `gkxlumenx_ods`。Mapping 读三方列，按下表写入，不按列注释改读，也不先重排成 demo ODS 再映射。

| 列 | 三方里实际存的 | demo ODS 重排后 |
|---|---|---|
| `industry_link_code` | 父级码 `INB1204010102` | 己码 `INB120401010202` |
| `industry_link_name` | 父名「减速器」 | 己名「谐波减速器」 |
| `industry_code` | 己码 `INB120401010202` | 根码 `INB1204` |
| `industry_name` | 己名「谐波减速器」 | 根名「机器人」 |
| `level` | `0`（这列没有层级） | `4` |
| `parent_name` | 层级数字 `4` | 父名「减速器」 |
| `parent_code` | 根链中文名「机器人」 | 父码 `INB1204010102` |

分表只看三方 `parent_name` 转成的整数：`0` 或 `1` 写入 `industry_chain`；`2` 至 `7` 写入 `industry_chain_node`。同一源行只进一张表。

**写入 `industry_chain`（`parent_name` 为 0 或 1）**

| 源字段 | 目标字段 | 写入 |
|---|---|---|
| `industry_code` | `chain_id` | 原值 |
| `industry_code` | `chain_code` | 与 `chain_id` 相同 |
| `industry_name` | `chain_name` | 原值 |
| `parent_name` | `chain_level` | 整数。`0` 或 `1` |
| `parent_name` | `chain_tier` | `L0` 或 `L1`，与 `chain_level` 同一个数 |
| `industry_link_code` | `parent_chain_id` | `chain_level=0` 写 NULL；`chain_level=1` 写原值 |
| `industry_code` | `industry_id` | `chain_level=0` 时写 `industry_code` |
| `industry_link_code` | `industry_id` | `chain_level=1` 时写 `industry_link_code` |
| — | `status` | `active` |
| — | `future_industry_flag` | 写 `0`。现网 demo 53 行全是 `0` |
| `industry_link_name` | — | 不写入 |
| `parent_code` | — | 不写入 |
| `level` | — | 不写入 |
| `node_company_count` | — | 不写入 |
| — | `chain_short_name` / `chain_category` / `description` | 不写入 |

**写入 `industry_chain_node`（`parent_name` 为 2 至 7）**

| 源字段 | 目标字段 | 写入 |
|---|---|---|
| `industry_code` | `node_id` | 原值 |
| `industry_code` | `node_code` | 与 `node_id` 相同 |
| `industry_name` | `node_name` | 原值 |
| `parent_name` | `node_level` | 整数。`2` 至 `7` |
| `industry_link_code` | `chain_id` | **v2.3 修正（round2 问 1 拍板）**：填**所属 L1 链**的码（53 个之一），不是直接父级码。取法：`industry_link_code` 指向的祖先层级=1 时取该码；层级≥2 则沿父级继续向上，直到层级=1。例：`INB130301010101`（硅材料）→ 向上经 `INB1303010101`→`INB130301`→ **`INB130301`（半导体材料 L1）**。验收：1,220 行 `chain_id` 必须全部命中 `industry_chain`（53 行），命中率 100% |
| `industry_link_code` | `parent_node_id` | **v2.3 修正（round2 问 1 拍板）**：填直接父级的码；父级为 L1 链时（`node_level=2`，共 165 行）写 NULL——此时归属已由 `chain_id` 表达。验收：L3~L7 共 1,055 行有父指针，且每行可在 `industry_chain_node` 命中 |
| `industry_code` 末两位 | `sort_no` | 转整数。例：`INB120401010202` → `2` |
| `industry_code` 末两位 | `stage_code` | **v2.3.1 徐滕强拍板（2026-11-03）：维持三等分派生**——末两位 `1`–`4` 写 `upstream`；`5`–`8` 写 `midstream`；`9` 及以上写 `downstream`。依据：假定供应方同级排序按供应流向排列（假定成立则字段可用）；GDF round2 问 4 的 958/185/77 分布为该规则结果。**风险已书面告知**：若供应方排序实为其他含义，此字段需按确认结果重算并刷新（登记客户决策清单 🟡 待供应方确认） |
| `industry_name` | `description` | 与 `node_name` 相同 |
| — | `status` | `active` |
| `industry_link_name` | — | 不写入 |
| `parent_code` | — | 不写入 |
| `level` | — | 不写入 |
| `node_company_count` | — | 不写入 |
| — | `node_type` / `importance_level` / `node_path` | 不写入。现网另有 22 行 `node_type` 已有值，不是这张源表加工出来的 |

码长必须等于 `7 + 2 × parent_name`。对不上的行进治理清单，不改用别的列分表。

公共治理列（`id` / `source_*` / `etl_batch_id` / `data_version` / `valid_*` / `is_deleted` / `created_time` / `updated_time` / `ext`）按 v5 §3.3 系统生成，下表不重复。过滤：`is_deleted = 0`。

### 3.1 `industry_chain`

字段对应以 §3.0 为准。`parent_name` → `chain_level`。唯一键 `chain_id`。验收行数 **53**（`chain_level=0` 的 12 行 + `chain_level=1` 的 41 行）。

### 3.2 `industry_chain_node`

字段对应以 §3.0 为准。`parent_name` → `node_level`。**v2.3：`chain_id`=所属 L1 链（沿父级向上追溯，命中率 100% 验收）；`parent_node_id`=直接父级码（L2 共 165 行父为链，写 NULL）**。唯一键 `(chain_id, node_id)`。验收行数 **1,220**。

### 3.3 → `industry_chain_node_rel`（**v2.3 重写（round2 问 3 拍板）**：真父子边，废弃「兄弟相邻」方案）

> **v2.2 的「同链按 sort_no 相邻写 upstream 边（913 行）」作废**——那是同父兄弟间的并列边，不是上下游，且违反旧版 09「禁止按 sort 相邻伪造 upstream」的既有禁令。v2.3 恢复真源显式父子关系。

**生成规则**：逐节点看 `industry_link_code`（直接父级）——父级是**节点**（层级≥2）→ 生成一条父子边；父级是 **L1 链**（层级=1，即全部 L2 共 165 行）→ 不生成（归属已由节点表 `chain_id` 表达）。**验收行数：1,055**（420+388+142+80+25，即 L3~L7 各层行数之和）。

| 目标字段 | 规则 |
|---|---|
| `relation_id` | `node-rel:{chain_id}:{父 node_id}:{子 node_id}`。超过 64 字符时改为这段文字的 SHA-256 前 64 位 |
| `chain_id` | 子节点的所属 L1 链（与节点表新 `chain_id` 同值） |
| `source_node_id` | **父节点** `node_id`（=子行 `parent_node_id`） |
| `target_node_id` | **子节点** `node_id` |
| `relation_type` | `parent_child` |
| `relation_direction` | `directed` |
| `confidence` | `1.0`（真源显式父子，非推导） |
| `relation_weight` / `evidence_ref` | NULL |

**验收（B1 出数后三查）**：① 边表 1,055 行；② 每行 `source_node_id` 在节点表命中且 `node_level` = 子行减 1；③ 沿 `parent_node_id` 从任一 L7 节点上溯，终点必为某 L2 节点（其 `chain_id` 即所属链）——树完整可还原。

### 3.4 `dwd_org_industry_tags` → `industry_chain_entity_rel`（v2.3.1 修订：解析格式与脏值钉死；业务口径=全量全国）

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

**业务口径（round2 问 7，2026-11-03 徐滕强拍板）：全量全国，不存在「只做广东」**。不得以样例匹配率定业务范围（PoC 阶段样例匹配不上属正常现象）。执行规则不变：`credit_code` JOIN `enterprise_base` 命中才写 `org_id`，对不上不伪造；**未命中行进治理清单**（带 credit_code/company_name/挂点证据），待企业主档覆盖扩展后二次挂接——丢弃≠放弃，不因此缩小业务范围。命中率数字（round1 双方的 85%/15%/2%）均为样例期数字，不作范围依据。

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
| OPEN-CHAIN-MAP-01 | `stage_code` | **已定（2026-11-03 徐滕强）：维持三等分派生**（1-4/5-8/9+）；排序含义登记 🟡 待供应方确认，确认后如不符再重算刷新 |
| OPEN-CHAIN-MAP-02 | `future_industry_flag` | **已定（2026-11-02 对照 demo）：链树作业写 0** |
| OPEN-CHAIN-MAP-03 | 产品 tags → entity_rel product | 本期不洗 |
| OPEN-CHAIN-MAP-06 | 分析 `industry_code` → INB `chain_id` | 挡后续按链资讯；本期 B2 不洗 |
| OPEN-CHAIN-MAP-07 | 链上企业挂接口径 | **已定（2026-11-03 徐滕强）：全量全国**；未命中行进治理清单待二次挂接，命中率随 Wave A 对账回执（仅作数据现状参考，不作范围依据） |
| OPEN-CHAIN-FLOW-01 | 正式 DAG 名 | 产线回写 |
| OPEN-CHAIN-FLOW-02 | 正式图空间名 + 上图/rebuild 契约 + 点数稳定判定 | **已定（2026-11-02 二次确认）**：空间 `gkx_chain`；契约见 `12`§5 |

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

