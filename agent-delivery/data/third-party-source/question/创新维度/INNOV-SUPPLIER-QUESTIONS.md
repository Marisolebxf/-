# 创新维 — 给三方供应方的入站缺口问题清单

```yaml
---
doc_id: INNOV-SUPPLIER-QUESTIONS
element: INNOV
role: source
status: draft
version: "2026-09-04"
updated: 2026-09-04
owner: human:郭万迎
audience: 三方供应方（书面回复） / PM 转发
---
```

> **域码 `INNOV`（展示科创/创新，不是久新 ORG/TALENT/TECH 三叶）。**  
> **监管**：进度表专题维度Owner 原 **未点名**；本叶由 **`human:郭万迎`** 认领监管（2026-09-04）。  
> **用途**：只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> **方法**：见 [../README.md](../README.md)。供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：[`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。2026-09-04 监管人确认升现行。MODEL/MIXED 不写 sidecar。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 | 兄弟域同列 |
|------|--------|-----------|--------|------------------|------------|------------|
| INNOV-P0-1 | P0 | （缺列：科创要素主表/主键） | 请书面给出科创要素入站表名、主键与稳定码（按 `factor_type`：论文/专利/人才/企业/科研机构/服务机构/会议/项目等，不要只用名称）+ 样例各类型 1 行 + 空值规则。随口径修订。 | `M_INNOV_FACTOR_COUNT`, `M_INNOV_FACTOR_DIST`, `M_INNOV_FACTOR_GROWTH`, `M_INNOV_KPI_BOARD`, `M_INNOV_KPI_BOARD_SZ`, `M_INNOV_CITY_MONITOR_GLOBAL` | 2026-09-04 | |
| INNOV-P0-2 | P0 | （缺列：科技领域稳定码） | 请给出要素/指标过滤用的**科技领域稳定码**（或对照表）：码列名、合法枚举、JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充。随口径修订。 | `M_INNOV_DOMAIN_KPI_SZ`, `M_INNOV_SCI_PAPER`, `M_INNOV_TINN_PATENT_COUNT`, `M_INNOV_SCIINDEX_VALUE`, `M_INNOV_SCIINDEX_INFLUENCE`, `M_INNOV_SCIINDEX_RANK_SCORE`, `M_INNOV_POT_INPUT`, `M_INNOV_POT_OUTPUT` | 2026-09-04 | `TECH-P0-2`；`TALENT-P0-2`；`ORG-P0-3` |
| INNOV-P0-3 | P0 | （缺列：城市/区划稳定码） | 请给出深圳 / 湾区 11 城 / 全球城市圈定用的区划或城市稳定码（建议 adcode 或书面对照）+ 样例 3 行；不要只用城市中文名。随口径修订。 | `M_INNOV_GBA_FACTOR_STAT`, `M_INNOV_GBA_INNOV_RATIO`, `M_INNOV_GBA_INVEST`, `M_INNOV_GBA_OUTPUT_VALUE`, `M_INNOV_GBA_PATENT_GRANT`, `M_INNOV_GBA_PATENT_PAPER`, `M_INNOV_GBA_TECH_CONTRACT`, `M_INNOV_DOMAIN_KPI_SZ`, `M_INNOV_KPI_BOARD_SZ`, `M_INNOV_KEYD_SPATIAL`, `M_INNOV_KEYD_LAND`, `M_INNOV_CITY_MONITOR_GLOBAL` | 2026-09-04 | `ENT-P0-1` |
| INNOV-P1-1 | P1 | （缺列：人才/H 指数落表） | 请说明全球/深圳人才创新指数、专家 H 指数、专家活跃度落在哪张入站 `dwd_*`、主键、值列、更新频率；样例 3 行；不问公式。随口径修订。 | `M_INNOV_CITY_TALENT_INDEX_GLOBAL`, `M_INNOV_CITY_TALENT_INDEX_SZ`, `M_INNOV_EXPERT_HINDEX`, `M_INNOV_EXPERT_ACTIVITY` | 2026-09-04 | `TALENT-P1-1` |
| INNOV-P1-2 | P1 | （缺列：专利申请/授权原料） | 请给出专利主键、申请/授权状态列、权利人稳定码（不要只给名称）、日期列；样例 3 行；不请对方 COUNT。随口径修订。 | `M_INNOV_GBA_PATENT_GRANT`, `M_INNOV_GBA_PATENT_PAPER`, `M_INNOV_TINN_PATENT_COUNT`, `M_INNOV_KPI_BOARD` | 2026-09-04 | `ENT-P0-6`；`ENT-P1-1`；`ORG-P1-6` |
| INNOV-P1-3 | P1 | （缺列：论文主键/被引/完成单位） | 请给出论文主键、被引或影响因子列、第一完成单位稳定码；样例 3 行；不请对方 COUNT。随口径修订。 | `M_INNOV_SCI_PAPER`, `M_INNOV_PAPER_INFLUENCE`, `M_INNOV_GBA_PATENT_PAPER`, `M_INNOV_FACTOR_COUNT` | 2026-09-04 | `ORG-P1-2` |
| INNOV-P1-4 | P1 | （缺列：经费/产值/合同金额） | 请给出 R&D 经费内部支出、高技术产业增加值、区域生产总值、技术合同成交额的入站 `dwd_*` 表.列 + 年主键 + 区划键；样例各 1 行。随口径修订。 | `M_INNOV_GBA_INVEST`, `M_INNOV_GBA_OUTPUT_VALUE`, `M_INNOV_GBA_INNOV_RATIO`, `M_INNOV_GBA_TECH_CONTRACT`, `M_INNOV_PG_FUND`, `M_INNOV_PG_PROJECT`, `M_INNOV_POT_INPUT`, `M_INNOV_POT_OUTPUT` | 2026-09-04 | `ENT-P0-5` |
| INNOV-P1-5 | P1 | （缺表：要素关系边 / 路径 VID） | 请给出科创要素实体稳定码及要素–要素边（边权列可选）入站表；技术路径/空间点若另表请点名主键。不要用名称猜点，不请对方 hang 图。随口径修订。 | `M_INNOV_FACTOR_RELATION`, `M_INNOV_FACTOR_EDGE_WEIGHT`, `M_INNOV_DS_02_PATH_001`, `M_INNOV_DS_02_PATH_002`, `M_INNOV_DS_02_PATH_003`, `M_INNOV_DS_27_SPATIO_012` | 2026-09-04 | |
| INNOV-P1-6 | P1 | （缺列：政策数量分布键） | 请确认政策行主键、类型码、地域码能否支撑「数量/类型/覆盖面」COUNT；**空值与 theme JSON 不重问**（见政策维现行题）。样例 3 行。随口径修订。 | `M_INNOV_PG_COUNT_DIST` | 2026-09-04 | `POLICY-P0-1`；`POLICY-P1-4`；`POLICY-P2-1` |

<!-- MIXED 本波不进。MODEL 入参不清不进。 -->

---

# 分析日志（新的在上）

## 2026-09-04

- 任务：`DATA-SUPPLIER-Q-INNOV-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。监管人要求按 ORG/TALENT/TECH **整域扫描 + 按轴拆题**。叶不标 `done`。
- 派单备注：§3.1 创新 Owner 原为「—」兜底淮政玮；**本次按郭万迎书面认领**，点名后不必改回。
- 本批算法类型（registry **138**；MCP `metric-query domain=INNOV fields=full limit=150`；**未**打开 seed YAML）：STAT 27 / COMPUTE 0 / GRAPH 6 / MODEL 82 / third_party 4 / UNKNOWN 0 / **MIXED 19（跳过）**
- 对外本批：**37** 条（27+6+4）。MODEL 82 **blocked「等唐绍祖入参清单」**，不问公式、不猜入参列。skill 日 cap 30；监管人要求整域逻辑，本批对外 37 一次列完（不拆第二日游标）。
- D1：draft 138 / aligned 0。kit `source_tables` 均为 `pending_ods`，**抽不出 `dwd_*.column`**。`metrics/calc-logic/INNOV/` **无目录**。未探库。
- 跳过：MIXED 19；二次未核细稿；CMS-only 未判。
- 甲方去重（不改写）：Q108–Q149 等 Q-MO-DS* 口径题。
- 轴检查（与 TECH-P0-2 / TALENT-P0-2 / ORG-P0-2/3 同逻辑）：领域码、城市区划、专利、论文、金额台账、图 VID、政策键 **不能** 揉进「要素主键」一问。
- 拟升现行：监管人 **2026-09-04 确认升现行**（上表 9 题）。

| 拟 Q-id | 优先级 | 入站表.列（拟） | 问什么 | 卡住的 metric_id | 兄弟域同列 |
|---------|--------|-----------------|--------|------------------|------------|
| INNOV-P0-1 | P0 | （缺列：科创要素主表/主键） | 请书面给出科创要素入站表名、主键与稳定码（按 `factor_type`：论文/专利/人才/企业/科研机构/服务机构/会议/项目等，不要只用名称）+ 样例各类型 1 行 + 空值规则。随口径修订。 | `M_INNOV_FACTOR_COUNT`, `M_INNOV_FACTOR_DIST`, `M_INNOV_FACTOR_GROWTH`, `M_INNOV_KPI_BOARD`, `M_INNOV_KPI_BOARD_SZ`, `M_INNOV_CITY_MONITOR_GLOBAL` | |
| INNOV-P0-2 | P0 | （缺列：科技领域稳定码） | 请给出要素/指标过滤用的**科技领域稳定码**（或对照表）：码列名、合法枚举、JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充。随口径修订。 | `M_INNOV_DOMAIN_KPI_SZ`, `M_INNOV_SCI_PAPER`, `M_INNOV_TINN_PATENT_COUNT`, `M_INNOV_SCIINDEX_VALUE`, `M_INNOV_SCIINDEX_INFLUENCE`, `M_INNOV_SCIINDEX_RANK_SCORE`, `M_INNOV_POT_INPUT`, `M_INNOV_POT_OUTPUT` | `TECH-P0-2`；`TALENT-P0-2`；`ORG-P0-3` |
| INNOV-P0-3 | P0 | （缺列：城市/区划稳定码） | 请给出深圳 / 湾区 11 城 / 全球城市圈定用的区划或城市稳定码（建议 adcode 或书面对照）+ 样例 3 行；不要只用城市中文名。随口径修订。 | `M_INNOV_GBA_*`（STAT 湾区 7 条）, `M_INNOV_DOMAIN_KPI_SZ`, `M_INNOV_KPI_BOARD_SZ`, `M_INNOV_KEYD_SPATIAL`, `M_INNOV_KEYD_LAND`, `M_INNOV_CITY_MONITOR_GLOBAL` | `ENT-P0-1` |
| INNOV-P1-1 | P1 | （缺列：人才/H 指数落表） | 请说明全球/深圳人才创新指数、专家 H 指数、专家活跃度落在哪张入站 `dwd_*`、主键、值列、更新频率；样例 3 行；不问公式。随口径修订。 | `M_INNOV_CITY_TALENT_INDEX_GLOBAL`, `M_INNOV_CITY_TALENT_INDEX_SZ`, `M_INNOV_EXPERT_HINDEX`, `M_INNOV_EXPERT_ACTIVITY` | `TALENT-P1-1` |
| INNOV-P1-2 | P1 | （缺列：专利申请/授权原料） | 请给出专利主键、申请/授权状态列、权利人稳定码（不要只给名称）、日期列；样例 3 行；不请对方 COUNT。随口径修订。 | `M_INNOV_GBA_PATENT_GRANT`, `M_INNOV_GBA_PATENT_PAPER`, `M_INNOV_TINN_PATENT_COUNT`, `M_INNOV_KPI_BOARD` | `ENT-P0-6`；`ENT-P1-1`；`ORG-P1-6` |
| INNOV-P1-3 | P1 | （缺列：论文主键/被引/完成单位） | 请给出论文主键、被引或影响因子列、第一完成单位稳定码；样例 3 行；不请对方 COUNT。随口径修订。 | `M_INNOV_SCI_PAPER`, `M_INNOV_PAPER_INFLUENCE`, `M_INNOV_GBA_PATENT_PAPER`, `M_INNOV_FACTOR_COUNT` | `ORG-P1-2` |
| INNOV-P1-4 | P1 | （缺列：经费/产值/合同金额） | 请给出 R&D 经费内部支出、高技术产业增加值、区域生产总值、技术合同成交额的入站 `dwd_*` 表.列 + 年主键 + 区划键；样例各 1 行。随口径修订。 | `M_INNOV_GBA_INVEST`, `M_INNOV_GBA_OUTPUT_VALUE`, `M_INNOV_GBA_INNOV_RATIO`, `M_INNOV_GBA_TECH_CONTRACT`, `M_INNOV_PG_FUND`, `M_INNOV_PG_PROJECT`, `M_INNOV_POT_INPUT`, `M_INNOV_POT_OUTPUT` | `ENT-P0-5` |
| INNOV-P1-5 | P1 | （缺表：要素关系边 / 路径 VID） | 请给出科创要素实体稳定码及要素–要素边（边权列可选）入站表；技术路径/空间点若另表请点名主键。不要用名称猜点，不请对方 hang 图。随口径修订。 | `M_INNOV_FACTOR_RELATION`, `M_INNOV_FACTOR_EDGE_WEIGHT`, `M_INNOV_DS_02_PATH_001`, `M_INNOV_DS_02_PATH_002`, `M_INNOV_DS_02_PATH_003`, `M_INNOV_DS_27_SPATIO_012` | |
| INNOV-P1-6 | P1 | （缺列：政策数量分布键） | 请确认政策行主键、类型码、地域码能否支撑「数量/类型/覆盖面」COUNT；**空值与 theme JSON 不重问**（见政策维现行题）。样例 3 行。随口径修订。 | `M_INNOV_PG_COUNT_DIST` | `POLICY-P0-1`；`POLICY-P1-4`；`POLICY-P2-1` |

- `M_INNOV_GBA_FACTOR_STAT`：促成因素 COUNT 跟 P0-1 + P0-3。
- blocked MODEL 82：公式均为 `pending_cosign: human:唐绍祖（未签）`，入参键未清。
- sidecar：**已 upsert** 37 条（`domain=INNOV`，`as_of=2026-09-04`）。MODEL/MIXED 不写。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 INNOV-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
