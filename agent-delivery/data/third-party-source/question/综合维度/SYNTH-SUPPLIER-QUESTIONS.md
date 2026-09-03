# 综合分析 — 给三方供应方的问题清单

```yaml
---
doc_id: SYNTH-SUPPLIER-QUESTIONS
element: SYNTH
role: source
status: draft
version: "2026-09-03"
updated: 2026-09-03
owner: human:徐滕强
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问综合域**独有**入站 `dwd_*`（协同边、资金/空间原料、图谱 API 落表）。  
> **跨维不重问**：企业主档区划码 / 上链 INB / 专利受让人码 / 年报研发 / 标签码 → 见 [ENT-SUPPLIER-QUESTIONS.md](../企业维度/ENT-SUPPLIER-QUESTIONS.md)；政策列 → POLICY；产业链目录叶子 → CHAIN。  
> **科研机构（综合五维入参）**：挂三方机构库类型码 + 稳定 ID（本文件 SYNTH-P0-5 / ENT-P2-1），**不等 ORG-P0-1、不甩久新科研机构专题**。人才专题 `M_TALENT_*` 本期不向久新开口；协同边人才端只问三方库主键是否在边上。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：[`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 DWD/ADS、`related_entities`、甲方 Q-SYNTH-* / Q-SYNTH-C-* / Q-SYNTH-E-* / Q-SYNTH-V-*（权重、公式、分母）、请对方算指数/中心度。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| SYNTH-P0-1 | P0 | `dwd_org_base_info_zh_project_rel`（`org_id`×`project_id`） | 合作项目边：同一 `project_id` 是否稳定出现 **≥2 个** `org_id`？`org_id` 须能 JOIN 三方机构库 `dwd_org_base_info.org_id`（稳定码不重问，见 ENT-P2-1）。圈定高校/科研院所用类型码见 SYNTH-P0-5，**不等 ORG-P0-1**。请给过滤规则（默认 `is_deleted=0`）+ 多样例 3 行。`dwd_zh_project.funded_institution` 现为**名称**，不能当边。随口径修订。 | `M_SYNTH_COLLAB_RELATION_INPUT`, `M_SYNTH_COLLAB_COMPLETENESS`, `M_SYNTH_COLLAB_CENTRALITY`, `M_SYNTH_COLLAB_DENSITY`, `M_SYNTH_COLLAB_INDEX` | 2026-09-02 |
| SYNTH-P0-2 | P0 | `dwd_zh_project.participating_institution` | JSON 参与机构是否含统一社会信用代码 / `org_id`，还是只有名称？空值约定？请给 Schema + 1 条样例。随口径修订。 | `M_SYNTH_COLLAB_RELATION_INPUT`, `M_SYNTH_COLLAB_COMPLETENESS` | 2026-09-01 |
| SYNTH-P0-3 | P0 | （缺表）人才流动边 | 入站 **无** 人才在机构间流动/任职变迁边。本叶只要：有无 `dwd_*` 边表（两端为三方库稳定码 + 事件日）。人才专题不向久新开口。请给表名 + 3 行，或书面「不交付」。随口径修订。 | `M_SYNTH_COLLAB_RELATION_INPUT`, `M_SYNTH_COLLAB_CENTRALITY`, `M_SYNTH_COLLAB_DENSITY` | 2026-09-02 |
| SYNTH-P0-4 | P0 | `dwd_patent_assignees`（同一 `patent_id` 多权利人） | 联合专利边：同一专利是否保证 ≥2 个机构权利人行？机构码仍走企业维 ENT-P0-6，**本叶不重问信用代码**。请确认能否按 `patent_id` 抽出机构–机构边（不要个人发明人冒充机构）。随口径修订。 | `M_SYNTH_COLLAB_RELATION_INPUT`, `M_SYNTH_COLLAB_OUTPUT_CORR` | 2026-09-01 |
| SYNTH-P0-5 | P0 | `dwd_org_base_info`（主体类型码列） | 七要素「科研机构」维：请给出能圈定**高校/科研院所**的类型码列（或对照表）+ 合法枚举 + 样例 3 行（`org_id` + 类型码）。不要只用名称。若现网 `org_type` 仅为工商组织形式，请书面指出另列。主键/信用代码复用 ENT-P2-1。**不等 ORG-P0-1**。随口径修订。 | `M_SYNTH_ELEM_TYPE_SCORE`, `M_SYNTH_ELEM_TYPE_INDEX`, `M_SYNTH_ELEM_LEVEL_SCORE`, `M_SYNTH_ELEM_INDICATOR` | 2026-09-02 |
| SYNTH-P1-1 | P1 | `dwd_zh_project.funded_amount` / （缺区域资金表） | 七要素「资金」入参：现表是**项目经费**（万元），不是区域资金存量/结构。请确认有无区域财政、产业基金、风险投资等 `dwd_*`（主键 + 区划码 + 年）。没有则书面「只有项目经费」。随口径修订。 | `M_SYNTH_ELEM_TYPE_SCORE`, `M_SYNTH_ELEM_TYPE_INDEX`, `M_SYNTH_ELEM_LEVEL_SCORE`, `M_SYNTH_ELEM_INDICATOR` | 2026-09-01 |
| SYNTH-P1-2 | P1 | （缺表）空间 / 载体 | 七要素「空间」：入站未见园区/载体/孵化器独立 `dwd_*`（主档经纬度是企业点位，不够结构维）。请给表名 + 主键 + 区划码样例 3 行，或书面不交付。随口径修订。 | `M_SYNTH_ELEM_TYPE_SCORE`, `M_SYNTH_ELEM_LEVEL_INDEX`, `M_SYNTH_ELEM_INDICATOR` | 2026-09-01 |
| SYNTH-P1-3 | P1 | `M_SYNTH_GRAPHAPI_116_1` 落表 | third_party：产业全要素图谱 API 的**点/边快照**是否落在某张入站 `dwd_*`？请给表名 + 主键 + 更新频率。若只提供接口、无表，书面说明，我方自建图，不请对方 hang。随口径修订。 | `M_SYNTH_GRAPHAPI_116_1` | 2026-09-01 |
| SYNTH-P1-4 | P1 | （缺表）展示侧图谱分析/算法结果 | third_party：模式识别、预测、分类聚类、推荐、路径、中心性、社群等结果是否落某张入站 `dwd_*`？kit 仅 `pending_ods`。请给表名 + 主键 + 更新频率；若只接口、无表，书面说明。**不要**与 GRAPHAPI-116（P1-3）混成一张表，除非对方书面确认同一快照。不请对方 hang。随口径修订。 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_005`, `M_SYNTH_DS_21_GRAPH_ANALYSIS_006`, `M_SYNTH_DS_21_GRAPH_ANALYSIS_007`, `M_SYNTH_DS_21_GRAPH_ANALYSIS_008`, `M_SYNTH_DS_23_GRAPH_ALGO_001`, `M_SYNTH_DS_23_GRAPH_ALGO_002`, `M_SYNTH_DS_23_GRAPH_ALGO_006`, `M_SYNTH_DS_23_GRAPH_ALGO_007`, `M_SYNTH_DS_23_GRAPH_ALGO_008`, `M_SYNTH_DS_23_GRAPH_ALGO_009`, `M_SYNTH_DS_23_GRAPH_ALGO_011`, `M_SYNTH_DS_23_GRAPH_ALGO_012`, `M_SYNTH_DS_23_GRAPH_ALGO_013`, `M_SYNTH_DS_23_GRAPH_ALGO_014` | 2026-09-03 |
| SYNTH-P2-1 | P2 | `dwd_rel_project_scholar.scholar_id` | 项目–学者边已有。请确认 `scholar_id` 与**三方人才库**主键是否同一套、空值规则。本期不向久新开口。随口径修订。 | `M_SYNTH_COLLAB_RELATION_INPUT` | 2026-09-02 |

<!-- MIXED seq 182–191 本波不进。二次 RANK 不进。权重/公式甲方题不进。 -->

---

# 分析日志（新的在上）

## 2026-09-03

- 任务：`DATA-SUPPLIER-Q-SYNTH-L01`（`in_progress`；`supervised_by=human:徐滕强`）。监管人指示「synth继续做」。
- 本批算法类型：third_party 14（DS-21×4 + DS-23×10） / MODEL 5（`ELEM_DOMAIN_INDEX` / `ELEM_INDEX` / `VIT_*` 三指数分项） / MIXED 跳过（182–191 + `ELEM_CONTRIB`） / 二次 RANK 跳过 / 甲方权重跳过
- 本批指标：cap=19（硬顶 20）。游标=无 sidecar 或问法应变的 `M_SYNTH_*`。已有 as_of 且问法未变的 12 条协同/要素/GRAPHAPI **跳过**。
- D1 快照（本批抽样）：DS-21/23 均为 `draft`；`ELEM_DOMAIN_INDEX` / `ELEM_INDEX` / `VIT_INDEX` = `missing`；`VIT_INDICATOR` / `VIT_DIM_SCORE` = `draft`。草案仍出题。禁止改 D3。
- 入站：kit `source_tables` 均为 `pending_ods` / pending 专题库，**未再探库**。不编造表名。
- 问题表：新开 **SYNTH-P1-4**（展示侧图谱分析/算法结果落表；与 P1-3 GRAPHAPI-116 分开）。
- 不新开题：
  - `M_SYNTH_ELEM_DOMAIN_INDEX` → 产业/技术码复用 ENT-P0-2
  - `M_SYNTH_ELEM_INDEX` → 合成甲方题；入参缺口复用 P0-5 / P1-1 / P1-2
  - `M_SYNTH_VIT_INDEX` / `DIM_SCORE` / `INDICATOR` → 四维原料跨 ENT/POLICY，综合不另开列
- sidecar：upsert 本批 19 keys（14×P1-4 + 2 要素复用 + 3 活力跨维）。`source_gap_indexed` SYNTH 累计 31。
- 声明：随口径修订。叶不标 `done`。

## 2026-09-02

- 任务：`DATA-SUPPLIER-Q-SYNTH-L01`（`in_progress`；`supervised_by=human:徐滕强`）。PM 指示：七要素「科研机构」维与协同边改挂三方机构库，不等 ORG-P0-1。
- 本批：不扫新 cap；只改挂已有综合题。
- 拟改已写入现行：新开 **SYNTH-P0-5**（`dwd_org_base_info` 类型码）；修订 P0-1 / P0-3 / P2-1 文案（JOIN 机构库、人才端不甩久新）。
- 不重问：ENT-P2-1 主键/信用代码；不把甲方 Q-SVC-008/010 改写成综合题（只问「哪一列能圈定高校/科研院所」）。
- 未探库。sidecar：本批更新协同边摘要 + 要素题点名 P0-5（`q_id` 资金/空间仍 P1-1/P1-2；`M_SYNTH_ELEM_TYPE_SCORE` 主号改 **SYNTH-P0-5**）。
- 声明：随口径修订。叶不标 `done`。

## 2026-09-01

- 本批算法类型：STAT 2（RELATION_INPUT；WEIGHT 跳过甲方） / COMPUTE 0 / GRAPH 若干（协同中心度/密度/贡献路径） / MODEL 活力+要素+协同指数 / third_party 1（GRAPHAPI-116） / MIXED 10 **跳过** / UNKNOWN 0
- 本批指标：注册表 `M_SYNTH_*` 46 条（rejudge SYNTH.md）；细稿仅 `M_SYNTH_VIT_RANK` / `M_SYNTH_ELEM_RANK`（二次，不向供应方要列）
- D1 快照：MCP `metric-registry` 本会话不可用；多数 draft / missing（METRIC-OPEN）。草案仍出题。禁止改 D3。
- 入站依据：`gkx_schema_ddl.sql` 表结构 + METRIC-OPEN 缺口（`pending_ods_joint_patent/cooperation_project/talent_flow`、资金/空间）。**本叶未再探库行数。**
- **跨维依赖（不重问）**：
  - ENT-P0-1 区划码 → 活力/要素区域对比
  - ENT-P0-2 上链 INB → 要素领域（CHAIN 目录仍归李伟）
  - ENT-P0-6 / P1-1 专利码与法律状态 → 科技维入参、联合专利边只问「多权利人」
  - POLICY 现行待回复 → 政策维入参
  - ENT-P2-1 机构主键/信用代码（本叶 P0-1 JOIN、P0-5 不重问）
  - ~~TALENT/ORG 久新 → 人才结构、科研机构主档~~（2026-09-02 废止：科研机构改挂 SYNTH-P0-5；人才专题不开口）
  - SVC → 服务机构规模（侯佳伟切片）
- 跳过、不进对外清单：
  - MIXED：`M_SYNTH_182_1` … `M_SYNTH_191_1`
  - 二次 RANK：`M_SYNTH_VIT_RANK`、`M_SYNTH_ELEM_RANK`（`<- metric:` 指数）
  - 甲方权重/公式：`M_SYNTH_VIT_WEIGHT`、`M_SYNTH_ELEM_WEIGHT`；Q-SYNTH-01/02/E-01/C-01/C-02
  - 展示侧 DS-21/DS-23 无入站 `dwd_*` 的 GRAPH/MODEL（模式识别/最短路/社群等）：不编造表名
  - 项目 ADS 指数结果表
- 问题表：

| Q-id | 入站表.列 | 现象 | 请对方确认 |
|------|-----------|------|------------|
| SYNTH-P0-1 | 项目–机构关联 | 有 `org_id`×`project_id`；资助机构列是名称 | 一项目多机构样例 |
| SYNTH-P0-2 | `participating_institution` | JSON，未知是否含码 | Schema / 信用代码 |
| SYNTH-P0-3 | 人才流动 | DDL 无此边表 | 有无表或书面不交付 |
| SYNTH-P0-4 | 专利多权利人 | 总量映射已在 ENT | 能否抽机构–机构联合边 |
| SYNTH-P1-1 | 项目经费 vs 区域资金 | 仅 `funded_amount` | 有无区域资金 `dwd_*` |
| SYNTH-P1-2 | 空间载体 | DDL 未见园区表 | 有无表 |
| SYNTH-P1-3 | GRAPHAPI | kit pending_cosign | 落哪张 `dwd_*` 或无表 |
| SYNTH-P2-1 | `scholar_id` | 有项目–学者边 | 与人才主键是否同一套 |

- 声明：草案口径标「随口径修订」。未把 46 条拆成 46 题。
- sidecar：upsert 卡住的协同/要素/GRAPHAPI metric_id；活力指数 MODEL 不另开题（跨维引用 ENT/POLICY）。2026-09-02 起科研机构维不再引用久新/ORG-P0-1。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 SYNTH-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |

---

## 抽样备注（项目侧，不发给对方也可）

- 协同图 VID 用机构 `org_id`（三方机构库）/ 学者 `scholar_id`（三方人才库主键是否在边上，见 P2-1）；不等久新科研机构专题。
- `dwd_rel_project_patent` 是项目↔专利，不是机构↔机构联合专利边。
- `dwd_en_paper_funding` 是论文资助，不当区域资金要素。
- 指数合成、四维权重、完整度分母 = 甲方/算法卡，不写进供应方题。
