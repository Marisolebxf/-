# 产业链库 — 给三方供应方的问题清单

```yaml
---
doc_id: CHAIN-SUPPLIER-QUESTIONS
element: CHAIN
role: source
status: draft
version: "2026-09-03"
updated: 2026-09-03
owner: human:李伟
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。图谱 hang 用稳定 INB 码按**我方 VID**（`chain:{chain_id}` / `node:{chain_id}:{node_id}`，见 Q053 + `gkx-platform-business-keys.md`），不要用名称猜点。  
> **抽样**：2026-09-02 live `gkx`，`is_deleted=0`：`dwd_industry_chain_info` **1273**；`dwd_org_industry_tags` **19029**。`dwd_industry_chain_news_info` 曾抽样 12291，**项目已定不再使用该表**。入站 **无** `dwd_org_industry_chain_dtl` / `dwd_org_industry_chain_pat_dtl`。  
> **映射对照**：[`data-design/产业链/ODS-DWD-字段对照与缺失明细.md`](../../../data-design/产业链/ODS-DWD-字段对照与缺失明细.md)（`position` 入站缺失已登记）。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **项目已定（2026-09-03 `human:李伟`）**：① 弃用入站表名 `dwd_org_industry_chain_dtl`（已无此表）；企业↔链官方源 = **`dwd_org_industry_tags`**。kit/细稿仍写 `dtl` 的，对内改指向 tags，**不再问供应方要回这张表**。② **VID/主键不问供应方**：对齐 [`DEC-CHAIN-Q053`](../../../data-design/产业链/DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md) + [`gkx-platform-business-keys.md`](../../gkx-platform-business-keys.md)——链根 `chain:{industry_code}`（level=0）；节点 `node:{chain_id}:{industry_link_code}`；**禁止**供应方自增 `id` 作 VID。旧稿 `segment:` 前缀不以本清单对外题为准。③ **入站过滤**：默认 **`is_deleted=0`**（对齐 [`SUPPLIER-WORK-CONSTRAINTS`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)）；不问对方书面重申。④ 弃用入站表名 **`dwd_org_industry_chain_pat_dtl`**（已无此表）；链–专利走通用 `dwd_patent*` + 企业/tags 间接关联，机构码跟 **ENT-P0-6**，**不再问供应方要回链专利明细表**。⑤ **不再使用** `dwd_industry_chain_news_info`；资讯热度 / 资讯产业码 **不对供应方出题**。  
> **不要问对方**：项目 DWD/ADS（`industry_chain*` / `chain_overview` / Nebula 边表）；`related_entities`；甲方口径 QC01–QC11 / Q053（编码已冻结 INB）；我方 VID 拼法；`is_deleted` 默认过滤（团队已定 `=0`）；请对方替我们 COUNT / 打分 / hang 图；**已弃用的 `dwd_org_industry_chain_dtl` / `dwd_org_industry_chain_pat_dtl` / `dwd_industry_chain_news_info`**。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

跨维已有题、**不在本表重复开号**（sidecar `q_id` 指向企业维）：

| 跟哪题 | 入站列 | 本批卡住的 CHAIN metric |
|--------|--------|-------------------------|
| `ENT-P0-2` | `dwd_org_industry_tags.industry_code`（JSON 数组串，非标量 INB） | `M_CHAIN_ENTERPRISE_POWER`, `M_CHAIN_ACADEMIC_POWER`, `M_CHAIN_COMPETITIVENESS_INDEX`, `M_CHAIN_CYCLE_STAGE`；以及原挂 CHAIN-P0-2、改挂本列的企业↔链原料指标（见已关闭） |
| `ENT-P2-1` | `credit_code` / 机构主键 | 同上（tags 现网 credit 非空，仍跟企业主档 1:1 规则） |
| `ENT-P0-6` | 专利受让人名称→机构码 | `M_CHAIN_ACADEMIC_COOP_SCORE`, `M_CHAIN_HOTSPOT_SCORE`, `M_CHAIN_ENTERPRISE_POWER`（专利维；`pat_dtl` 已弃用；资讯表已弃用，热点资讯侧不再对供应方出题） |

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| CHAIN-P0-1 | P0 | `dwd_industry_chain_info`（缺环节位置列） | **现状**：现网仅有树深 `level`（0–7），**没有**上/中/下游位置列；`level`≠环节位置，我方不能自行对照。**请交付其一**：① 官方位置列（列名 + 合法值，如上游/中游/下游或等价码）+ 样例 3 行（`industry_link_code` + 位置原值）；或 ② 独立对照表（表名 + 键列 + 位置列 + 样例 3 行）。**不要**：用产业名称猜位置；不要只回「看 level」。随口径修订。 | `M_CHAIN_DOWNSTREAM_COUNT`, `M_CHAIN_HIGH_VALUE_RATIO`, `M_CHAIN_COMPLETENESS_SCORE`, `M_CHAIN_BREAK_RISK_COUNT` | 2026-09-02 |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。 -->

---

# 已关闭（不对供应方发）

| Q-id | 关闭日 | 裁定 | 后续 |
|------|--------|------|------|
| CHAIN-P0-2 | 2026-09-03 | `human:李伟`：**弃用** `dwd_org_industry_chain_dtl`（入站已无此表）。企业↔链官方源 = `dwd_org_industry_tags`。 | kit/细稿/映射凡写 `← ods: dwd_org_industry_chain_dtl` 改为 tags；JSON 产业码拆行缺口跟 **ENT-P0-2**，不新开 CHAIN 题。原挂本号的 metric sidecar 改挂 `ENT-P0-2`。 |
| CHAIN-P0-3 | 2026-09-03 | `human:李伟`：VID/主键为**项目约定**（不问供应方）。对齐 Q053 + `gkx-platform-business-keys`：链根 `chain:{industry_code}`（level=0→`chain_id`）；节点 `node:{chain_id}:{industry_link_code}`；**禁止**自增 `id`/`pk_id` 作生产键或 VID。现网码 `INB*` 已满足形态。旧稿 `segment:` 作废（对本清单）。 | 曾改挂 P2-1 的 `M_CHAIN_EDGE_COUNT`：P2-1 同日关闭后自 sidecar **移除**（VID+过滤均已项目侧定）；其余曾列本号的指标继续跟 P0-1 / ENT-P0-2 等各自缺口。 |
| CHAIN-P2-1 | 2026-09-03 | `human:李伟`：入站默认 **`is_deleted=0`**（对齐 `SUPPLIER-WORK-CONSTRAINTS`），不问供应方书面重申；不另追 `insert_remark` 排除规则。 | `M_CHAIN_EDGE_COUNT` 自 sidecar 移除；`M_CHAIN_COMPLETENESS_SCORE` 仍跟 **CHAIN-P0-1**（位置列缺口）。ETL/探针统一 `WHERE is_deleted=0`。 |
| CHAIN-P1-1 | 2026-09-03 | `human:李伟`：**弃用** `dwd_org_industry_chain_pat_dtl`（入站已无此表）。链–专利不另要直连表；走通用 `dwd_patent*` + 企业 + tags。 | kit/细稿凡写 `← ods: dwd_org_industry_chain_pat_dtl` 改为通用专利表；机构码缺口跟 **ENT-P0-6**。原挂本号的 `M_CHAIN_ACADEMIC_COOP_SCORE` sidecar 改挂 `ENT-P0-6`。 |
| CHAIN-P0-4 | 2026-09-03 | `human:李伟`：**不再使用** `dwd_industry_chain_news_info`。资讯热度字段不对供应方要。 | 热门资讯 / 资讯热度原料指标自 sidecar **移除**；`M_CHAIN_HOTSPOT_SCORE` 专利密度侧改挂 **ENT-P0-6**。kit/细稿凡写资讯 ODS 的对内改源，不新开 CHAIN 题。 |
| CHAIN-P1-2 | 2026-09-03 | `human:李伟`：**不再使用** `dwd_industry_chain_news_info`。资讯 `industry_code` / `INA*` 不对供应方问。 | `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT` 自 sidecar **移除**（资讯源已弃用）。 |

---

# 分析日志（新的在上）

## 2026-09-03

- 裁定：`human:李伟` **不再使用** `dwd_industry_chain_news_info`，关闭 **CHAIN-P0-4**、**CHAIN-P1-2**。
- 现行表：删除上述两行；不对供应方要资讯热度 / 资讯产业码。
- sidecar：移除 `M_CHAIN_HOT_NEWS_COUNT`、`M_CHAIN_DEVELOPMENT_MILESTONE_COUNT`；`M_CHAIN_HOTSPOT_SCORE` 改挂 `ENT-P0-6`（专利密度仍跟受让人机构码）。
- 文案：现行待回复「问什么」按「现状 / 请交付 / 不要」重写（P0-1 仍开）。
- 裁定：`human:李伟` 关闭 **CHAIN-P1-1** — 弃用 `dwd_org_industry_chain_pat_dtl`；链–专利走通用 `dwd_patent*` + 企业 + tags，机构码跟 ENT-P0-6。
- 现行表：删除 CHAIN-P1-1 行；不向供应方要回该表。
- sidecar：`M_CHAIN_ACADEMIC_COOP_SCORE` 由 `CHAIN-P1-1` 改挂 `ENT-P0-6`，`as_of=2026-09-03`。
- 裁定：`human:李伟` 关闭 **CHAIN-P2-1** — 入站默认 `is_deleted=0`（`SUPPLIER-WORK-CONSTRAINTS`），不问对方书面过滤规则。
- 现行表：删除 CHAIN-P2-1 行。
- sidecar：移除 `M_CHAIN_EDGE_COUNT`（VID+过滤均已项目侧定，无未决供应方缺口）；`COMPLETENESS_SCORE` 仍挂 P0-1。
- 裁定：`human:李伟` 关闭 **CHAIN-P0-3** — VID/主键项目侧已定（Q053 + platform-business-keys），不问供应方确认拼法；禁自增 `id` 作 VID；旧稿 `segment:` 不以本清单为准。
- 现行表：删除 CHAIN-P0-3 行。
- sidecar：`M_CHAIN_EDGE_COUNT` 曾由 `CHAIN-P0-3` 改挂 `CHAIN-P2-1`；同日 P2-1 关闭后移除该条。
- 裁定：`human:李伟` 关闭 **CHAIN-P0-2** — 弃用 `dwd_org_industry_chain_dtl`，官方源 `dwd_org_industry_tags`。
- 现行表：删除 CHAIN-P0-2 行；不向供应方要回该表。
- sidecar：原 `q_id=CHAIN-P0-2` 的 7 条改挂 `ENT-P0-2`，`as_of=2026-09-03`，summary 写明「dtl 已弃用，原料=tags；JSON 码跟 ENT-P0-2」。
- 声明：不对供应方发「请恢复 dtl / pat_dtl / 资讯表」/「请确认我方 VID 拼法」/「请书面确认 is_deleted」类问题。

## 2026-09-02

- 本批算法类型：STAT 7 / COMPUTE 1 / GRAPH 3 / MODEL 9 / third_party 0 / UNKNOWN 0 / **MIXED 0（本波跳过）**
- 本批指标（禁止超 `DATA-SUPPLIER-Q-CHAIN-L01` 当日 cap 20）：
  - STAT：`M_CHAIN_ENTERPRISE_COUNT`, `M_CHAIN_ENTERPRISE_NEW_COUNT`, `M_CHAIN_INSTITUTION_COUNT`, `M_CHAIN_HOT_NEWS_COUNT`, `M_CHAIN_HIGH_VALUE_RATIO`, `M_CHAIN_GLOBAL_REGION_COUNT`, `M_CHAIN_BOTTLENECK_COUNT`
  - COMPUTE：`M_CHAIN_CONCENTRATION_INDEX`
  - GRAPH：`M_CHAIN_DOWNSTREAM_COUNT`, `M_CHAIN_EDGE_COUNT`, `M_CHAIN_BREAK_RISK_COUNT`
  - MODEL：`M_CHAIN_ENTERPRISE_POWER`, `M_CHAIN_ACADEMIC_POWER`, `M_CHAIN_COMPETITIVENESS_INDEX`, `M_CHAIN_CYCLE_STAGE`, `M_CHAIN_COMPLETENESS_SCORE`, `M_CHAIN_HOTSPOT_COUNT`, `M_CHAIN_HOTSPOT_SCORE`, `M_CHAIN_ACADEMIC_COOP_SCORE`, `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT`
- D1 快照（本批 MCP `metric-get`/`metric-query`，禁止改矩阵）：aligned 约 5（企业能力/学术生态/竞争力/周期/热点等）/ draft 或 matrix 缺失若干；草案仍出题并标「随口径修订」
- 入站抽样：live `gkx` / `is_deleted=0` / 2026-09-02
  - `dwd_industry_chain_info`：**1273**；`industry_code` 抽样全为 `INB*`（如 `INB1303`）；`level` 0–7；**无** `position` / `node_stage` / `chain_stage`
  - `dwd_org_industry_tags`：**19029**；`industry_code` 样例为 JSON 数组串（如 `['INB1333','INB1502']`）；`credit_code` / `company_name` 非空率 100%（本批）
  - `dwd_industry_chain_news_info`：**12291**；`industry_code` 亦为 JSON 数组串；**无** `heat_score` / `heat`
  - **表不存在**：`dwd_org_industry_chain_dtl`、`dwd_org_industry_chain_pat_dtl`（kit 仍写这两张名）
- kit / 细稿：多数 STAT 写 `dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl` 或项目 ADS；MODEL 入参落在 `dwd_industry_chain_info` + `dwd_org_industry_tags` + 年报/专利通用表。项目 ADS / Nebula **不编成供应方题**。
- 跳过、不进对外清单（本批）：
  - `MIXED`：本波不做
  - `pending_ods` + `pending_cosign` 且入参键不清：`M_CHAIN_BASE_95_1`, `M_CHAIN_CHOKE_LINK_COUNT`, `M_CHAIN_DEEP_117_1`…`129_1`, `M_CHAIN_GRAPH_102_1` / `103_1`, `M_CHAIN_GLOBAL_CASE_MATCH` → **记 blocked：等唐绍祖入参清单**，不问公式
  - 项目算法表 `dwd.industry_bottleneck`（算法判定）：不向供应方要；`BOTTLENECK_*` 只追企业↔链原料（原挂 P0-2；2026-09-03 起跟 ENT-P0-2 / tags）
  - 甲方 QC01–QC11 / Q053：不改写（INB 已冻结，本批只问字段是否交付）
  - 二次 / CMS-only：本批未见独立二次根需另开
- 跨维复用、不新开 CHAIN Q：见文首表（ENT-P0-2 / ENT-P2-1 / ENT-P0-6）
- 问题表（2026-09-02 \human:李伟\ 点头后已落盘「现行待回复」）：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| CHAIN-P0-1 | 缺 \position\/\chain_stage\ | 仅 \level\ 0–7 | 位置列或 level 对照表 |
| CHAIN-P0-2 | 缺 \dwd_org_industry_chain_dtl\ | 企业↔链在 tags | tags 是否官方；主键；JSON 拆法 |
| CHAIN-P0-3 | \industry_code\/\industry_link_code\/\id\ | 全 INB*；去重 1273 | chain:/segment: VID 规则 |
| CHAIN-P0-4 | 缺 \heat_score\ | 资讯 16 列无 heat | 热度列或另表 |
| CHAIN-P1-1 | 缺 \dwd_org_industry_chain_pat_dtl\ | 仅通用专利表 | 链–专利表或书面确认名称匹配 |
| CHAIN-P1-2 | 资讯 \industry_code\ | JSON 数组；偶见 INA | 语义/拆行/枚举 |
| CHAIN-P2-1 | \is_deleted\ | 默认 \=0\ | 书面过滤规则 |

- 声明：草案口径标「随口径修订」。监管人 \human:李伟\。GRAPH 只问 INB/稳定码。
- sidecar：本批 upsert **20** 条（16 条挂 CHAIN-P0/P1/P2；4 条 \q_id\ 指向 ENT-P0-2）。清单见 \source-gap-index.yaml\。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
