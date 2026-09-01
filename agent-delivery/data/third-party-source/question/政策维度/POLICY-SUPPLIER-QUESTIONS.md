# 政策库 — 给三方供应方的问题清单

```yaml
---
doc_id: POLICY-SUPPLIER-QUESTIONS
element: POLICY
role: source
status: draft
version: "2026-09-01"
updated: 2026-09-01
owner: human:淮政玮
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。政策图谱 hang 必须对上产业链已有 VID（`chain:{chain_id}` / `segment:{node_id}`，如 `INB1701`）。  
> **抽样**：2026-09-01 Demo 贴源 `demo_gkxlumenx_ods.dwd_policy_base`，`is_deleted=0`，**47050** 行（与供应库 `gkx.dwd_policy_base` 同构镜像；验收仍以 live `gkx` 为准）。本叶未再探库。  
> **DDL 真源**：[`data-design/storage/POLICY/sources/ods-ddl.md`](../../../data-design/storage/POLICY/sources/ods-ddl.md)。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 DWD `policy_base_info.related_entities`（我方 `ods_to_dwd` 拼的，供应库无此列）；政策类型展示归类 **QPOL-01** 及权重/阈值 **QPOL-02**、关联判定 **QPOL-03**（甲方口径）；图谱 C 回写供应库（C 不写入站表）。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| POLICY-P0-1 | P0 | `dwd_policy_base.theme` / `keywords` / `quote_policy` / `ministry` | 未抽取时大量是字符串 `"NULL"` 不是 SQL NULL（theme 95.7%、keywords 99.2%、quote_policy 96.7%、ministry ~94%）。请确认空值约定，后续批次能否统一为 SQL NULL。随口径修订。 | `M_POLICY_TEXT_PARSE`, `M_POLICY_FOCUS_INDEX`, `M_POLICY_DEEP_166_1`, `M_POLICY_OPPORTUNITY_COUNT` | 2026-09-01 |
| POLICY-P0-2 | P0 | `dwd_policy_base.theme` | DDL COMMENT 是背景/指导思想提炼；实测非空值是标签 JSON 数组（如 `["监督管理"]`），不是产业名、也不是指导思想正文。请确认正式语义、合法枚举/码表、是否另有目标产业字段或另表。随口径修订。 | `M_POLICY_FOCUS_INDEX`, `M_POLICY_DEEP_166_1`, `M_POLICY_OPPORTUNITY_COUNT`, `M_POLICY_SHORTBOARD_COUNT`, `M_POLICY_DEEP_169_1`, `M_POLICY_DEEP_170_1` | 2026-09-01 |
| POLICY-P0-3 | P0 | `dwd_policy_base`（缺产业码列） | 现有字段对不上产业链 `chain_id` / `node_id`（`INB*`）。请交付其一：政策行上增加产业/环节编码列（建议 `INB1701` / `INB17010102`）；或政策 `id` ↔ 产业链码对照表（表名 + 样例 3 行）。没有码无法上图。随口径修订。 | `M_POLICY_INDUSTRY_COVERAGE`, `M_POLICY_INDUSTRY_FIT`, `M_POLICY_GRAPH_106_1`, `M_POLICY_MATCH`, `M_POLICY_RELATION_DEGREE` | 2026-09-01 |
| POLICY-P0-4 | P0 | `dwd_policy_base.policy_support` | JSON 数组键实测为 `condition` / `support_way` / `support_object` / `support_behavior`。请提供完整 JSON Schema、枚举、空值规则；`support_object` 是否会给到统一社会信用代码或组织机构代码（当前只有角色词）；有没有目标产业编码（抽样没有）。随口径修订。 | `M_POLICY_SUPPORT_STRENGTH`, `M_POLICY_INTENSITY_SCORE`, `M_POLICY_INTENSITY_INDEX`, `M_POLICY_DEEP_167_1`, `M_POLICY_IMPLEMENTATION_EFFECT` | 2026-09-01 |
| POLICY-P1-1 | P1 | `dwd_policy_base` 或另表（政策↔主体） | 政策 ↔ 企业 / 科研机构 / 服务机构是否有稳定 ID？在 `dwd_policy_base` 还是另表？请给**表名 + 3 条样例**（政策 `id` + 对方主键）。入站 DDL **无** `pedigree` / `related_entities`。随口径修订。 | `M_POLICY_GRAPH_106_1`, `M_POLICY_GRAPH_107_1`, `M_POLICY_RELATION_DEGREE`, `M_POLICY_IMPLEMENTATION_EFFECT` | 2026-09-01 |
| POLICY-P1-2 | P1 | `dwd_policy_base.quote_policy` | 约 96% 为 `"NULL"`。有值时是标题、文号，还是被引政策的稳定 `id`？图谱引用边需要对方 `id`，不要只给标题。随口径修订。 | `M_POLICY_GRAPH_107_1`, `M_POLICY_DEEP_170_1`, `M_POLICY_RELATION_DEGREE` | 2026-09-01 |
| POLICY-P1-3 | P1 | `dwd_policy_base.ministry` | 约 94% 空。空是否表示未抽取？有值时能否配组织机构代码，而不只是名称？随口径修订。 | `M_POLICY_DEEP_170_1`, `M_POLICY_OPPORTUNITY_COUNT` | 2026-09-01 |
| POLICY-P1-4 | P1 | `dwd_policy_base.type` / `rank` / `status` | 请给合法值清单。`rank` 是否严格为国家级 / 省级 / 市级 / 区县级？`status` 是否只有有效 / 失效？**不问**该用哪一列当展示「类型」（那是甲方 QPOL-01）。随口径修订。 | `M_POLICY_TYPE_DIST`, `M_POLICY_LEVEL_DIST`, `M_POLICY_VALIDITY_RATE`, `M_POLICY_EFFECT_SCORE`, `M_POLICY_DEEP_168_1`, `M_POLICY_SUPPORT_STRENGTH` | 2026-09-01 |
| POLICY-P2-1 | P2 | `dwd_policy_base.id` | 当前最长 8 字符，我方图 VID 为 `pol:{id}`（space `vid_length=80`）。请确认不会超过 80 字符，也不会与国际表 `dwd_global_policy_base.id` 撞号。随口径修订。 | `M_POLICY_TOTAL_COUNT`, `M_POLICY_BASE_100_1`, `M_POLICY_GRAPH_106_1` | 2026-09-01 |
| POLICY-P2-2 | P2 | `dwd_policy_base.is_deleted` / `is_history` / `insert_remark` | 当前行过滤规则请书面写清（我方默认 `is_deleted=0`）。随口径修订。 | `M_POLICY_TOTAL_COUNT`, `M_POLICY_BASE_100_1`, `M_POLICY_TIMESERIES` | 2026-09-01 |
| POLICY-P2-3 | P2 | `dwd_global_policy_base`（整表） | 国际表无 `status` / `expire_date` / `rank`。国内国际如何区分有效政策？随口径修订。 | `M_POLICY_VALIDITY_RATE`, `M_POLICY_TOTAL_COUNT`, `M_POLICY_EFFECT_SCORE` | 2026-09-01 |

<!-- 一行一列聚类。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。二次指标 / CMS-only 不另开题。 -->

---

# 分析日志（新的在上）

## 2026-09-01

- 本批算法类型：STAT 12 / COMPUTE 1 / GRAPH 4 / MODEL 18 / third_party 0 / UNKNOWN 0 / MIXED 0
- 本批指标（禁止超 DATA-SUPPLIER-Q-POLICY-L01 `/goal` 清单）：
  - STAT：`M_POLICY_BASE_100_1`, `M_POLICY_INDUSTRY_COVERAGE`, `M_POLICY_LAYOUT_REC_COUNT`, `M_POLICY_LEVEL_DIST`, `M_POLICY_NATIONAL_DIST`, `M_POLICY_OPPORTUNITY_COUNT`, `M_POLICY_SHORTBOARD_COUNT`, `M_POLICY_SZ_DIST`, `M_POLICY_TIMESERIES`, `M_POLICY_TOTAL_COUNT`, `M_POLICY_TYPE_DIST`, `M_POLICY_VALIDITY_RATE`
  - COMPUTE：`M_POLICY_SUPPORT_STRENGTH`
  - GRAPH：`M_POLICY_DS_11_POLICY_EVAL_015`, `M_POLICY_GRAPH_106_1`, `M_POLICY_GRAPH_107_1`, `M_POLICY_RELATION_DEGREE`
  - MODEL：`M_POLICY_DEEP_166_1` … `M_POLICY_DEEP_171_1`, `M_POLICY_DS_07_POLICY_GUARD_001`, `M_POLICY_DS_07_POLICY_GUARD_008`, `M_POLICY_DS_11_POLICY_EVAL_012`, `M_POLICY_EFFECT_SCORE`, `M_POLICY_FOCUS_INDEX`, `M_POLICY_IMPLEMENTATION_EFFECT`, `M_POLICY_INDUSTRY_FIT`, `M_POLICY_INTENSITY_INDEX`, `M_POLICY_INTENSITY_SCORE`, `M_POLICY_MATCH`, `M_POLICY_SIMULATE`, `M_POLICY_TEXT_PARSE`
- D1 快照：aligned 0 / draft 0（本批 matrix parsed=0，D1/D4 均为 null，属预期；草案仍出题并标「随口径修订」。MCP 只读，禁止改矩阵）
- 入站抽样：Demo 贴源 `demo_gkxlumenx_ods.dwd_policy_base` / `is_deleted=0` / **47050** 行；与供应库 `gkx.dwd_policy_base` 同构；验收 live `gkx`。本叶未再探库。
- kit 回看：多数算法库叶 `source_tables=pending_ods` + `formula=pending_cosign`；已落地细稿的 MODEL 入参集中在 `dwd_policy_base`（id / theme / keywords / policy_support / quote_policy / ministry / type / rank / status / expire_date）+ 产业锚点 `dwd_industry_chain_info`（我方链，不向供应方要）。项目 DWD 名 `pedigree` / `allfactors` / `maelements` / `topic_type` **不是**入站列，不编成供应方题。
- 跳过、不进对外清单：
  - 二次：`M_POLICY_LAYOUT_REC_COUNT`（← 机遇+短板）、`M_POLICY_DEEP_171_1`（← 同上）、`M_POLICY_DS_07_POLICY_GUARD_001`（← 焦点+布局）、`M_POLICY_DS_07_POLICY_GUARD_008`（← 力度+效果）、`M_POLICY_DS_11_POLICY_EVAL_012`（← 文本解析摘要）
  - CMS-only / 无入站 `dwd_*`：`M_POLICY_SIMULATE`、`M_POLICY_DS_11_POLICY_EVAL_015`（均 `ads.policy_simulate`）
  - 入站列已在 DDL、本批抽样未另见缺口、不新开题：`M_POLICY_TIMESERIES`（`publish_date`/`publish_year`）、`M_POLICY_NATIONAL_DIST` / `M_POLICY_SZ_DIST`（`province`/`city`/`district`）——过滤规则仍挂 P2-2
- 未把甲方 QPOL-01/02/03/05/07 改写成供应方题。
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| POLICY-P0-1 | `theme`/`keywords`/`quote_policy`/`ministry` | 字符串 `"NULL"` 占比 95.7% / 99.2% / 96.7% / ~94% | 空值约定能否统一 SQL NULL |
| POLICY-P0-2 | `theme` | 非空为标签 JSON，如 `["科技创新","产业发展"]` | 正式语义、枚举、是否另有产业字段 |
| POLICY-P0-3 | （缺列） | 无 `INB*`；名称对不上 `chain:`/`segment:` VID | 加码列或对照表 + 3 行样例 |
| POLICY-P0-4 | `policy_support` | JSON 数组；`support_object` 仅角色词 | Schema / 枚举 / 是否有信用代码与产业码 |
| POLICY-P1-1 | 政策↔主体 | DDL 无 pedigree；无主体主键 | 表名 + 政策 id + 对方主键 3 行 |
| POLICY-P1-2 | `quote_policy` | 96% `"NULL"`；有值像标题/文号 | 是否被引政策稳定 `id` |
| POLICY-P1-3 | `ministry` | ~94% 空 | 空=未抽取？能否配组织机构代码 |
| POLICY-P1-4 | `type`/`rank`/`status` | 枚举未书面闭集 | 合法值清单（不问 QPOL-01） |
| POLICY-P2-1 | `id` | 最长 8 字符 | 不超 80、不与国际表撞号 |
| POLICY-P2-2 | `is_deleted` 等 | 我方默认 `is_deleted=0` | 书面过滤规则 |
| POLICY-P2-3 | `dwd_global_policy_base` | 无 status/expire_date/rank | 国际如何判有效 |

- 声明：草案口径标「随口径修订」。现稿 11 条抽样结论保留，Q-id 改为 `POLICY-P0-1`…`POLICY-P2-3`。缺列才补问法（P1-1 写明无 pedigree），未另开文件、未拆成 35 题。
- sidecar：本批 upsert 25 条卡住的 metric_id（同一 q_id 可多指标；跳过二次/CMS-only 与无抽样缺口的 STAT 三列）。清单见 `source-gap-index.yaml`。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 POLICY-P0-3） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |

---

## 抽样备注（项目侧，不发给对方也可）

- 产业 hang 输入槽：我方 DWD `related_entities.industry` ← `ods_to_dwd` 抄 `theme` 或 `policy_support` 内「目标产业」；`theme` 为 `"NULL"` 时槽内就是 `["NULL"]`。**不向供应方问 `related_entities`，也不请对方 hang 回写。**
- 图谱 C（`POLICY_RE_SUPPORT` 等）只 **读** 该槽做 `FETCH`，**不回写**供应库、也不回写 DWD。
- 对照产业链已存在点：`chain:INB1701`（新一代信息技术）、`segment:INB17010102`（晶圆制造）。
- kit 里的 `dwd.policy_base_info.*` / `ads.policy_*` 是项目侧，不是供应方工作面。
