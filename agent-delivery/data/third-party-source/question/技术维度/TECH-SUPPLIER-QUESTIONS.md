# 技术链 — 给久新的入站缺口问题清单

```yaml
---
doc_id: TECH-SUPPLIER-QUESTIONS
element: TECH
role: source
status: draft
version: "2026-09-04"
updated: 2026-09-04
owner: human:郭万迎
audience: 久新（书面回复） / PM 转发
---
```

> **对接：久新**（技术链专题 `TECH`）。  
> **用途**：只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> **合同说明**：智树专题五维合同包不含技术链分析专题交付；**但我方交付仍会用到技术指标/数据项**，故按对外口径继续列入口缺口（监管人 2026-09-04 确认）。产业链/综合已问过的同类列见「兄弟域同列」。  
> **方法**：见 [../README.md](../README.md)。供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：[`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。2026-09-04 监管人确认升现行。MODEL×3 不进对外表。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 | 兄弟域同列 |
|------|--------|-----------|--------|------------------|------------|------------|
| TECH-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出**技术点/技术主题**入站表名、主键列与稳定码列（技术点稳定 ID，不要只用中文名）及样例 3 行 + 空值规则。随口径修订。 | 本批对外 36 条（39−3 MODEL） | 2026-09-04 | |
| TECH-P0-2 | P0 | （缺列：技术领域稳定码未给出） | 请给出技术点/话题归属的**技术领域稳定码**（或 `technology_id`↔领域码对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充。随口径修订。 | `M_TECH_TOPIC_HEAT`, `M_TECH_DEEP_133_1`, `M_TECH_DEEP_134_1`, `M_TECH_DEEP_140_1` | 2026-09-04 | |
| TECH-P1-1 | P1 | （缺列：指数/成熟度/热度值列未给出） | 请说明各指数/成熟度/热度/路径分析结果落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），样例 3 行；不问公式。随口径修订。 | 32 条 third_party | 2026-09-04 | |
| TECH-P1-2 | P1 | （缺列：STAT 原料键未给出） | 请给出支撑「技术热度查询 / 投资额 / 产出规模 / 论文·专利计数」的最少入站 `dwd_*` 表.列（金额列、计数关联键、日期列），样例各 1 行；不请对方聚合。随口径修订。 | `M_TECH_HEAT_QUERY`, `M_TECH_INVEST_AMOUNT`, `M_TECH_OUTPUT_SCALE`, `M_TECH_PAPER_PATENT_CNT` | 2026-09-04 | `ENT-P0-6`（专利权利人稳定码；论文侧若另表仍须本叶点名） |
| TECH-P1-3 | P1 | （缺表：技术点↔机构/专利边） | 请给出技术点稳定码与机构稳定码（或专利主键）相连的入站边表/对照表 + 样例 3 行；不请对方 hang 图。随口径修订。 | `M_TECH_ENTITY_REL`, `M_TECH_EDGE_STRENGTH`, `M_TECH_REL_STRENGTH`, `M_TECH_GRAPH_104_1`, `M_TECH_GRAPH_105_1`, `M_TECH_GRAPH_STRUCT` | 2026-09-04 | |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id，metric_id 并列。MIXED 本波不进本表。 -->

---

# 分析日志（新的在上）

## 2026-09-04

- 任务：`DATA-SUPPLIER-Q-TECH-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。监管人指示：合同五维外仍按**对外口径扫并罗列**（交付要用技术数据）；表头加「兄弟域同列」。叶不标 `done`。
- 本批算法类型：STAT 4 / COMPUTE 0 / GRAPH 0 / MODEL 3 / third_party 32 / UNKNOWN 0 / MIXED 0
- 本批指标（registry 技术域 **39** 条 = 全量；MCP `metric-query domain=TECH fields=full limit=50`；**未**打开 seed YAML）：
  - STAT：`M_TECH_HEAT_QUERY`, `M_TECH_INVEST_AMOUNT`, `M_TECH_OUTPUT_SCALE`, `M_TECH_PAPER_PATENT_CNT`
  - MODEL：`M_TECH_DS_07_TECH_INNOV_002`, `M_TECH_DS_07_TECH_INNOV_004`, `M_TECH_DS_07_TECH_INNOV_006`
  - third_party：其余 32 条（含 `M_TECH_COMPOSITE_SCORE`, `M_TECH_HEAT_INDEX`, `M_TECH_MATURITY_LEVEL`, `M_TECH_GRAPH_*`, `M_TECH_PATH_*`, `M_TECH_SZ_ASSESS` 等）
- D1：draft 39 / aligned 0。未探库。
- kit：39 条均为 `pending_ods`；**抽不出入站 `dwd_*.column`**。`metrics/calc-logic/TECH/` **无文件**。
- MODEL：入参键不清 → 本批记 **blocked「等唐绍祖入参清单」**，**不进拟升现行**（不问公式、不猜入参列）。
- 游标：sidecar **无** TECH `as_of` → 全进本批（对外题不含 3 条 MODEL）。
- 跳过：MIXED 0；MODEL 3（blocked）；二次未核；CMS-only 未判。
- 甲方去重（不改写）：Q082 / Q083（Q-MO-TECH-01/02）；QC03 技术成熟度口径。
- 补漏：监管人指出「技术领域」轴未单列。`M_TECH_TOPIC_HEAT` / `M_TECH_DEEP_133_1` / `M_TECH_DEEP_134_1` / `M_TECH_DEEP_140_1` 要领域码，不能揉进 TECH-P0-1 技术点主键。产业 `INB*`（ENT-P0-2 / CHAIN-P0-1）**不是**技术领域，兄弟域同列留空。
- 拟升现行：监管人 **2026-09-04 确认升现行**（上表 5 题；不含 MODEL）。
- sidecar：**已 upsert** 36 条（`domain=TECH`，`as_of=2026-09-04`）。挂靠：领域码→P0-2；STAT 四条→P1-2；实体边→P1-3；其余 third_party→P0-1。MODEL×3 不写 sidecar。

| 拟 Q-id | 优先级 | 入站表.列（拟） | 问什么 | 卡住的 metric_id | 兄弟域同列 |
|---------|--------|-----------------|--------|------------------|------------|
| TECH-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出**技术点/技术主题**入站表名、主键列与稳定码列（技术点稳定 ID，不要只用中文名）及样例 3 行 + 空值规则。随口径修订。 | 本批对外 36 条（39−3 MODEL） | |
| TECH-P0-2 | P0 | （缺列：技术领域稳定码未给出） | 请给出技术点/话题归属的**技术领域稳定码**（或 `technology_id`↔领域码对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充。随口径修订。 | `M_TECH_TOPIC_HEAT`, `M_TECH_DEEP_133_1`, `M_TECH_DEEP_134_1`, `M_TECH_DEEP_140_1` | |
| TECH-P1-1 | P1 | （缺列：指数/成熟度/热度值列未给出） | 请说明各指数/成熟度/热度/路径分析结果落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），样例 3 行；不问公式。随口径修订。 | 32 条 third_party | |
| TECH-P1-2 | P1 | （缺列：STAT 原料键未给出） | 请给出支撑「技术热度查询 / 投资额 / 产出规模 / 论文·专利计数」的最少入站 `dwd_*` 表.列（金额列、计数关联键、日期列），样例各 1 行；不请对方聚合。随口径修订。 | `M_TECH_HEAT_QUERY`, `M_TECH_INVEST_AMOUNT`, `M_TECH_OUTPUT_SCALE`, `M_TECH_PAPER_PATENT_CNT` | `ENT-P0-6`（专利权利人稳定码；论文侧若另表仍须本叶点名） |
| TECH-P1-3 | P1 | （缺表：技术点↔机构/专利边） | 请给出技术点稳定码与机构稳定码（或专利主键）相连的入站边表/对照表 + 样例 3 行；不请对方 hang 图。随口径修订。 | `M_TECH_ENTITY_REL`, `M_TECH_EDGE_STRENGTH`, `M_TECH_REL_STRENGTH`, `M_TECH_GRAPH_104_1`, `M_TECH_GRAPH_105_1`, `M_TECH_GRAPH_STRUCT` | |

- blocked（不进对外清单）：`M_TECH_DS_07_TECH_INNOV_002/004/006` — 等唐绍祖入参清单。
- sidecar：**已 upsert**（见上）。拟表仍保留作当日对照。
- 声明：草案标「随口径修订」。不借本叶催智树五维外模块排期，只列交付原料缺口。

## 2026-09-02

- 任务：`DATA-SUPPLIER-Q-TECH-L01`（`in_progress`）。叶不标 `done`。
- **当时判定**：合同五维外 → 本期不开口；现行空表；sidecar 未写。
- **2026-09-04 废止「不开口」对外策略**（监管人改口：交付仍需用技术数据 → 按对外口径罗列）。09-02 类型计数仍有效：STAT 4 / MODEL 3 / third_party 32。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 TECH-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
