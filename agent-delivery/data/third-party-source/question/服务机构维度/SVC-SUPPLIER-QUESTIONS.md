# 产业服务库 — 给三方供应方的问题清单

```yaml
---
doc_id: SVC-SUPPLIER-QUESTIONS
element: SVC
role: source
status: draft
version: "2026-09-02"
updated: 2026-09-02
owner: human:侯佳伟
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：只问供应方入站 `dwd_*` 字段与主键。本批 20 条 STAT/GRAPH（`DATA-SUPPLIER-Q-SVC-L01` 当日 cap）；按表.列聚类。本叶**未 live 探库**（本机无 `gkx-mysql-raw/.env.local`），证据沿用 calc-logic 细稿、`SVC-29指标-缺口核对底稿`、STAT-21 Demo 50100（卡面 3525 / 深圳 1355）与企业维 ENT 探针。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 ADS/DWD（`svc_org_card` / `svc_org_circle` / `svc_metric_*` / `related_entities`）；甲方口径 Q-SVC-001/008/010（服务机构 vs 企业边界）、Q-SVC-004（district 提取规则）、Q-SVC-009（industry 列是否另表，已在决策清单问供应方）、Q-SVCCHAIN-*、Q062；请对方替我们 COUNT / 打分；用名称猜图谱点。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

跨维已有题、**不在本表重复开号**（卡住的 SVC 指标 sidecar 仍回填，`q_id` 指向企业维）：

| 跟哪题 | 入站列 | 本批卡住的 SVC metric |
|--------|--------|------------------------|
| `ENT-P0-1` | `dwd_org_base_info` 缺稳定行政区划码 | `M_SVC_PT_SZ_TOTAL`, `M_SVC_PT_SZ_REGION_ORG`, `M_SVC_PT_REGION_ORG`, `M_SVC_SZ_COMPARE_METRIC` |
| `ENT-P0-2` | `dwd_org_industry_tags` 产业/环节码非 INB | `M_SVC_PT_SZ_FIELD_DIST`, `M_SVC_PT_CHAIN_NODE_ORG`, `M_SVC_SZ_CHAIN_COMPLETENESS`, `M_SVC_CHAIN_SEGMENT_ORG_COUNT`, `M_SVC_CHAIN_SEGMENT_AVG_DEPTH`, `M_SVC_ORG_COVERAGE_BREADTH` |
| `ENT-P2-1` | `dwd_org_base_info.org_id` / 信用代码 | `M_SVC_ORG_TOTAL`, `M_SVC_PT_GLOBAL_TOTAL` |

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| SVC-P0-1 | P0 | `dwd_org_heis_info`（或缺机构大类码列） | 全球/深圳类型分布需要稳定分成**高校 / 科研院所 / 企业**。请确认：① 是否交付 `dwd_org_heis_info`（或等价表），主键如何与 `dwd_org_base_info.org_id` JOIN；② `univ_type`（或同类码）合法值；③ 科研院所是否另表/另码，不要只给中文名称。随口径修订。 | `M_SVC_PT_GLOBAL_TYPE_DIST`, `M_SVC_PT_SZ_TYPE_DIST` | 2026-09-02 |
| SVC-P0-2 | P0 | `dwd_org_annual_financial_info.employees_number` | 规模四档（&lt;50 / 50–200 / 200–500 / &gt;500）扫**从业人数**，不是研发人员列。请确认列是否正式交付、空值约定（SQL NULL / 0 / 空串）、年主键（`org_id`+年）。企业维已问 `development_employee`（ENT-P0-4），本列不是同一问。随口径修订。 | `M_SVC_PT_GLOBAL_SCALE_DIST`, `M_SVC_PT_KEYORG_SCALE` | 2026-09-02 |
| SVC-P1-1 | P1 | （缺表）服务机构 ↔ 服务机构边 | 入站未见「服务–服务」合作/参与边（图谱 `participates` 两端都要本批服务机构稳定 VID）。投资/股东边（`dwd_org_invest_info` / `dwd_org_shareholder_info`）**不是**服务关系。请交付：表名 + 两端 `org_id`（或信用代码）+ `relation_type` 样例 3 行；合法值至少能标服务合作。不要用名称猜点，不要在供应库 hang 图。随口径修订。 | `M_SVC_GRAPH_DENSITY`, `M_SVC_GRAPH_CENTRALITY` | 2026-09-02 |
| SVC-P1-2 | P1 | `dwd_org_base_info.incorporation_date`（或缺首次开展服务日） | 年度新增目前只能用工商成立年。请确认：成立日空值约定；是否另有「首次开展服务」日期列或另表（表名 + 样例 3 行）。随口径修订。 | `M_SVC_ORG_NEW_COUNT`, `M_SVC_REC_CANDIDATE_CNT` | 2026-09-02 |

<!-- 一行一列聚类。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。二次指标 / CMS-only 不另开题。 -->

---

# 分析日志（新的在上）

## 2026-09-02

- 本批算法类型：STAT 18 / COMPUTE 0 / GRAPH 2 / MODEL 0 / third_party 0 / UNKNOWN 0 / **MIXED 0（本波跳过）**
- 本批指标（禁止超 `DATA-SUPPLIER-Q-SVC-L01` 当日 cap 20）：
  - STAT：`M_SVC_ORG_TOTAL`, `M_SVC_ORG_NEW_COUNT`, `M_SVC_ORG_COVERAGE_BREADTH`, `M_SVC_PT_GLOBAL_TOTAL`, `M_SVC_PT_GLOBAL_TYPE_DIST`, `M_SVC_PT_REGION_ORG`, `M_SVC_PT_GLOBAL_SCALE_DIST`, `M_SVC_PT_KEYORG_SCALE`, `M_SVC_PT_SZ_TOTAL`, `M_SVC_PT_SZ_TYPE_DIST`, `M_SVC_PT_SZ_REGION_ORG`, `M_SVC_PT_SZ_FIELD_DIST`, `M_SVC_PT_CHAIN_NODE_ORG`, `M_SVC_SZ_COMPARE_METRIC`, `M_SVC_SZ_CHAIN_COMPLETENESS`, `M_SVC_CHAIN_SEGMENT_ORG_COUNT`, `M_SVC_CHAIN_SEGMENT_AVG_DEPTH`, `M_SVC_REC_CANDIDATE_CNT`
  - GRAPH：`M_SVC_GRAPH_CENTRALITY`, `M_SVC_GRAPH_DENSITY`
- D1 快照：aligned 0 / draft 20（本批；MCP `metric-query` domain=SVC `fields=full`，禁止改矩阵）
- 入站抽样：**本叶未再探库**（无 `.env.local`）。对照：STAT-21 Demo `svc_org_card`=3525、深圳=1355（项目 ADS，**不问供应方**）；企业维 ENT-P0-1/P0-2/P0-4/P2-1 live `gkx` 结论可复用。
- kit：本批官方 STAT 多数 `source_tables=pending_ods` + `formula=pending_cosign`；细稿里的 `demo_gkxlumenx_ads.svc_*` 是项目侧，不编成供应方题。
- 跳过、不进对外清单（本批）：
  - CMS / 会话集合：`M_SVC_ORG_SELECTED_COUNT`、`M_SVC_TYPE_DIST_QUERY`
  - UNKNOWN 旧 ID / 别名：`M_SVC_ORG_CNT`, `M_SVC_NEW_CNT`, `M_SVC_SZ_SCALE`, `M_SVC_SZ_DISTRICT`, `M_SVC_INDUSTRY_LAYOUT`, `M_SVC_INVEST_Y`, `M_SVC_RELATION_DENSITY`, `M_SVC_RELATION_RISK`
  - MODEL 18 条 + `M_SVC_GRAPH_112_1` / `113_1` / `M_SVC_BASE_101_1`：超出当日 cap，下一轮
  - 甲方 Q-SVC-001/008/010/004/009、Q-SVCCHAIN-01…08、Q062：不改写
  - 二次：候选名单若只派生自招引分，缺口跟 `M_SVC_REC_ATTRACT_SCORE`（MODEL，下批）；本批 `REC_CANDIDATE_CNT` 只问成立日原料
- 跨维复用、不新开 SVC Q：见文首表（ENT-P0-1 / ENT-P0-2 / ENT-P2-1）
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| SVC-P0-1 | `dwd_org_heis_info` / 大类码 | 细稿要高校/院所/企业；STAT-21 三类 ∩ 主体表空则 0/0/N | 表名、JOIN 键、univ_type 枚举 |
| SVC-P0-2 | `employees_number` | STAT-21 年报缺人数曾内存造数；ENT 只问过研发人员列 | 从业人数正式列、空值、年主键 |
| SVC-P1-1 | 服务–服务边 | 细稿 `svc_relation_chain` 为演示边；投资/股东不是服务关系 | 两端稳定 org_id + relation_type 3 行 |
| SVC-P1-2 | `incorporation_date` | 新增只能用工商成立年；「首次开展服务」无列 | 空值；是否另有首次服务日 |

- 声明：草案口径标「随口径修订」。监管人 `human:侯佳伟` 开工本叶，现行表按拟改落盘。
- sidecar：本批 upsert 20 条（4 条挂 SVC-P0/P1；16 条 `q_id` 指向 ENT-P0-1 / ENT-P0-2 / ENT-P2-1）。清单见 `source-gap-index.yaml`。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 SVC-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
