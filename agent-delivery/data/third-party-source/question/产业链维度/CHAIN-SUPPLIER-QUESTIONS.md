# 产业链库 — 给三方供应方的问题清单

```yaml
---
doc_id: CHAIN-SUPPLIER-QUESTIONS
element: CHAIN
role: source
status: draft
version: "2026-09-02"
updated: 2026-09-02
owner: human:李伟
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。图谱 hang 需要稳定码（链 `chain:{INB*}` / 环节 `segment:{INB*}`），不要用名称猜点。  
> **抽样**：2026-09-02 live `gkx`，`is_deleted=0`：`dwd_industry_chain_info` **1273**；`dwd_org_industry_tags` **19029**；`dwd_industry_chain_news_info` **12291**。入站 **无** `dwd_org_industry_chain_dtl` / `dwd_org_industry_chain_pat_dtl`。  
> **映射对照**：[`data-design/产业链/ODS-DWD-字段对照与缺失明细.md`](../../../data-design/产业链/ODS-DWD-字段对照与缺失明细.md)（`position` 入站缺失已登记）。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 DWD/ADS（`industry_chain*` / `chain_overview` / Nebula 边表）；`related_entities`；甲方口径 QC01–QC11 / Q053（编码已冻结 INB，本清单只核字段交付）；请对方替我们 COUNT / 打分 / hang 图。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

跨维已有题、**不在本表重复开号**（sidecar `q_id` 指向企业维）：

| 跟哪题 | 入站列 | 本批卡住的 CHAIN metric |
|--------|--------|-------------------------|
| `ENT-P0-2` | `dwd_org_industry_tags.industry_code`（JSON 数组串，非标量 INB） | `M_CHAIN_ENTERPRISE_POWER`, `M_CHAIN_ACADEMIC_POWER`, `M_CHAIN_COMPETITIVENESS_INDEX`, `M_CHAIN_CYCLE_STAGE`（链上主体筛选） |
| `ENT-P2-1` | `credit_code` / 机构主键 | 同上（tags 现网 credit 非空，仍跟企业主档 1:1 规则） |
| `ENT-P0-6` | 专利受让人名称→机构码 | `M_CHAIN_ACADEMIC_COOP_SCORE`, `M_CHAIN_HOTSPOT_SCORE`, `M_CHAIN_ENTERPRISE_POWER`（专利维；链–专利表另见 CHAIN-P1-1） |

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| CHAIN-P0-1 | P0 | `dwd_industry_chain_info`（缺 `position`/`chain_stage`） | 现网无上游/中游/下游列，仅有 `level` 0–7。请交付：① 官方位置列与合法值；或 ② `level`↔环节位置对照表（表名 + 样例 3 行）。无码无法做下游环节 / 完整度分段。随口径修订。 | `M_CHAIN_DOWNSTREAM_COUNT`, `M_CHAIN_HIGH_VALUE_RATIO`, `M_CHAIN_COMPLETENESS_SCORE`, `M_CHAIN_BREAK_RISK_COUNT` | 2026-09-02 |
| CHAIN-P0-2 | P0 | （缺表）`dwd_org_industry_chain_dtl` | 入站无此表；现网企业↔链在 `dwd_org_industry_tags`。请确认：① 是否以 tags 为官方交付；② 主键（`dwd_id`/`id`/`credit_code`+链码）；③ 一行多链 JSON 拆法与空值。随口径修订。 | `M_CHAIN_ENTERPRISE_COUNT`, `M_CHAIN_ENTERPRISE_NEW_COUNT`, `M_CHAIN_INSTITUTION_COUNT`, `M_CHAIN_CONCENTRATION_INDEX`, `M_CHAIN_GLOBAL_REGION_COUNT`, `M_CHAIN_BOTTLENECK_COUNT`, `M_CHAIN_HOTSPOT_COUNT`, `M_CHAIN_HOTSPOT_SCORE` | 2026-09-02 |
| CHAIN-P0-3 | P0 | `dwd_industry_chain_info.industry_code` / `industry_link_code` / `id` | 现网 1273 行码均为 `INB*`。请确认：链根 VID=`chain:{industry_code}`（level=0）、环节 VID=`segment:{industry_link_code}`；`id` 是否可作稳定替代主键；不与其他域撞号。不要用名称猜点。随口径修订。 | `M_CHAIN_EDGE_COUNT`, `M_CHAIN_DOWNSTREAM_COUNT`, `M_CHAIN_COMPLETENESS_SCORE`, `M_CHAIN_ENTERPRISE_POWER`, `M_CHAIN_ACADEMIC_POWER`, `M_CHAIN_COMPETITIVENESS_INDEX` | 2026-09-02 |
| CHAIN-P0-4 | P0 | `dwd_industry_chain_news_info`（缺 `heat_score`） | 现网无热度列。请交付 `heat_score`（或另表：表名 + 样例 3 行）、空值与更新频率。随口径修订。 | `M_CHAIN_HOT_NEWS_COUNT`, `M_CHAIN_HOTSPOT_COUNT`, `M_CHAIN_HOTSPOT_SCORE`, `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT` | 2026-09-02 |
| CHAIN-P1-1 | P1 | （缺表）`dwd_org_industry_chain_pat_dtl` | 无链–专利明细表，仅有通用 `dwd_patent*`。请交付关联表（链码/环节码 + 专利主键 + 样例 3 行）；若否，书面确认只用名称匹配（机构码缺口跟 ENT-P0-6）。随口径修订。 | `M_CHAIN_ACADEMIC_COOP_SCORE`, `M_CHAIN_HOTSPOT_SCORE`, `M_CHAIN_ENTERPRISE_POWER` | 2026-09-02 |
| CHAIN-P1-2 | P1 | `dwd_industry_chain_news_info.industry_code` | 值为 JSON 数组串（如 `["INB1309"]`），偶见 `INA*`。请确认正式语义、拆行规则、合法枚举、空值约定。随口径修订。 | `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT`, `M_CHAIN_HOTSPOT_COUNT`, `M_CHAIN_HOT_NEWS_COUNT` | 2026-09-02 |
| CHAIN-P2-1 | P2 | `dwd_industry_chain_info.is_deleted` / 过滤约定 | 我方默认 `is_deleted=0`。请书面过滤规则；历史行 / `insert_remark` 是否排除。随口径修订。 | `M_CHAIN_EDGE_COUNT`, `M_CHAIN_COMPLETENESS_SCORE` | 2026-09-02 |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。 -->

---

# 分析日志（新的在上）

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
  - 项目算法表 `dwd.industry_bottleneck`（算法判定）：不向供应方要；`BOTTLENECK_*` 只追企业↔链原料（挂 P0-2）
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
