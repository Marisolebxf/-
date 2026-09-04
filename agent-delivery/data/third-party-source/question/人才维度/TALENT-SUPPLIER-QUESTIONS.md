# 人才库 — 给久新的入站缺口问题清单

```yaml
---
doc_id: TALENT-SUPPLIER-QUESTIONS
element: TALENT
role: source
status: draft
version: "2026-09-04"
updated: 2026-09-04
owner: human:郭万迎
audience: 久新（书面回复） / PM 转发
---
```

> **对接：久新**（人才专题 `TALENT`）。  
> **用途**：只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> **合同说明**：智树专题五维合同包不含人才分析专题交付；**但我方交付仍会用到人才指标/数据项**，故按对外口径继续列入口缺口（监管人 2026-09-04 确认）。综合五维已问过的同类列见「兄弟域同列」，不重复改写甲方 Q。  
> **方法**：见 [../README.md](../README.md)。供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：[`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。2026-09-04 监管人确认升现行。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 | 兄弟域同列 |
|------|--------|-----------|--------|------------------|------------|------------|
| TALENT-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出**人才库**入站表名、主键列与稳定码列（学者/人才稳定 ID，不要只用姓名）及样例 3 行 + 空值规则。随口径修订。 | 本批 32 条 `M_TALENT_*` | 2026-09-04 | `SYNTH-P2-1`（`scholar_id` 与人才库主键是否同一套） |
| TALENT-P0-2 | P0 | （缺列：产业/技术领域稳定码未给出） | 请给出人才/话题归属的**产业或技术领域稳定码**（或 `talent_id`↔领域码对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充人才领域码。随口径修订。 | `M_TALENT_ORG_DIST`, `M_TALENT_REGIONAL_DIST`, `M_TALENT_SUPPLY_STRUCT`, `M_TALENT_SZ_SUPPLY_DEMAND`, `M_TALENT_UNIV_NEW`, `M_TALENT_INDUSTRY_SCORE`, `M_TALENT_FLOW_TRACK` | 2026-09-04 | |
| TALENT-P1-1 | P1 | （缺列：指数/排名值列未给出） | 请说明各指数/排名/模型输出落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），样例 3 行；不问公式。随口径修订。 | 31 条 third_party（不含 `M_TALENT_STRUCT_QUERY`） | 2026-09-04 | |
| TALENT-P1-2 | P1 | （缺表：人才流动/任职变迁边） | 请给出人才在机构间流动或任职变迁的入站 `dwd_*`（两端含人才稳定码 + 机构稳定码 + 事件日）表名 + 样例 3 行；或书面「不交付」。不请对方算流动率。随口径修订。 | `M_TALENT_FLOW_TRACK`, `M_TALENT_DEEP_157_1`, `M_TALENT_RELATION_NET`, `M_TALENT_GRAPH_110_1`, `M_TALENT_GRAPH_111_1`, `M_TALENT_DEEP_160_1` | 2026-09-04 | `SYNTH-P0-3`（综合维人才流动边；本叶补人才库侧主键口径） |
| TALENT-P1-3 | P1 | （缺列：学历/职称/年龄分箱键） | 请给出支撑结构分箱的入站列（默认最高学历；职称/年龄若有则点名列），样例各 1 行；不请对方 COUNT。**领域码见 P0-2，所属机构见 P1-4，不写进本问。** 随口径修订。 | `M_TALENT_STRUCT_QUERY`, `M_TALENT_SUPPLY_STRUCT` | 2026-09-04 | |
| TALENT-P1-4 | P1 | （缺列：当前所属机构稳定码） | 请给出人才**当前所属**机构的入站键（`talent_id` + 机构稳定码 / 组织机构代码，或对照表）+ 样例 3 行；不要只用机构名称。本问不是流动边（流动见 P1-2）。随口径修订。 | `M_TALENT_ORG_DIST`, `M_TALENT_UNIV_NEW`, `M_TALENT_FLOW_TRACK` | 2026-09-04 | `ORG-P0-1`；`ENT-P2-1`；`SYNTH-P0-5` |
| TALENT-P1-5 | P1 | （缺列：人才地理区划码） | 请给出人才计数用的地理单元码列（国家/省级；全球库含境外），或书面确认只通过所属机构 JOIN 主档区划。样例 3 行；不要只用城市中文名。随口径修订。 | `M_TALENT_REGIONAL_DIST`, `M_TALENT_FLOW_TRACK` | 2026-09-04 | `ENT-P0-1`（企业主档区划；若人才无独立地理列可复用所属机构 JOIN，仍须书面确认） |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id，metric_id 并列。MIXED 本波不进本表。 -->

---

# 分析日志（新的在上）

## 2026-09-04

- 任务：`DATA-SUPPLIER-Q-TALENT-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。监管人指示：合同五维外仍按**对外口径扫并罗列**（交付要用人才数据）；表头加「兄弟域同列」。叶不标 `done`。
- 本批算法类型：STAT 1 / COMPUTE 0 / GRAPH 0 / MODEL 0 / third_party 31 / UNKNOWN 0 / MIXED 0
- 本批指标（registry 人才域 **32** 条 = 全量；MCP `metric-query domain=TALENT fields=full limit=50`；**未**打开 seed YAML）：
  - STAT：`M_TALENT_STRUCT_QUERY`
  - third_party：`M_TALENT_ACADEMIC_SCORE`, `M_TALENT_ATTRACT_SCORE`, `M_TALENT_BASE_98_1`, `M_TALENT_CULTIVATE_SCORE`, `M_TALENT_DEEP_156_1`…`M_TALENT_DEEP_165_1`, `M_TALENT_DS_16_TALENT_RECRUIT_005/006/007/010/013/025`, `M_TALENT_FLOW_TRACK`, `M_TALENT_GRAPH_110_1`, `M_TALENT_GRAPH_111_1`, `M_TALENT_INDUSTRY_SCORE`, `M_TALENT_ORG_DIST`, `M_TALENT_REGIONAL_DIST`, `M_TALENT_RELATION_NET`, `M_TALENT_SUPPLY_STRUCT`, `M_TALENT_SZ_STATUS`, `M_TALENT_SZ_SUPPLY_DEMAND`, `M_TALENT_UNIV_NEW`
- D1：draft 32 / aligned 0。未探库。
- kit：32 条均为 `pending_ods`；**抽不出入站 `dwd_*.column`**。`metrics/calc-logic/TALENT/` **无文件**。不问公式。
- 游标：sidecar **无** TALENT `as_of` → 全进本批。
- 跳过：MIXED 0；二次未核细稿；CMS-only 未判。
- 甲方去重（不改写）：Q093 / Q102 等口径题；Q064/Q066 人才 UID 与评价维。
- 补漏（与 TECH-P0-2 同逻辑，监管人要求再扫轴）：领域/产业过滤、当前所属机构、地理区划 **不能** 揉进 TALENT-P0-1 主键或原 P1-3「结构键大杂烩」。产业 `INB*`（ENT-P0-2）**不是**人才技术领域码。
- 拟升现行：监管人 **2026-09-04 确认升现行**（上表 7 题）。
- sidecar：**已 upsert** 32 条（`domain=TALENT`，`as_of=2026-09-04`）。挂靠：领域过滤→P0-2；流动/关系→P1-2；`M_TALENT_STRUCT_QUERY`→P1-3；其余→P0-1。

| 拟 Q-id | 优先级 | 入站表.列（拟） | 问什么 | 卡住的 metric_id | 兄弟域同列 |
|---------|--------|-----------------|--------|------------------|------------|
| TALENT-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出**人才库**入站表名、主键列与稳定码列（学者/人才稳定 ID，不要只用姓名）及样例 3 行 + 空值规则。随口径修订。 | 本批 32 条 | `SYNTH-P2-1`（`scholar_id` 与人才库主键是否同一套） |
| TALENT-P0-2 | P0 | （缺列：产业/技术领域稳定码未给出） | 请给出人才/话题归属的**产业或技术领域稳定码**（或 `talent_id`↔领域码对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充人才领域码。随口径修订。 | `M_TALENT_ORG_DIST`, `M_TALENT_REGIONAL_DIST`, `M_TALENT_SUPPLY_STRUCT`, `M_TALENT_SZ_SUPPLY_DEMAND`, `M_TALENT_UNIV_NEW`, `M_TALENT_INDUSTRY_SCORE`, `M_TALENT_FLOW_TRACK` | |
| TALENT-P1-1 | P1 | （缺列：指数/排名值列未给出） | 请说明各指数/排名/模型输出落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），样例 3 行；不问公式。随口径修订。 | 31 条 third_party（不含 `M_TALENT_STRUCT_QUERY`） | |
| TALENT-P1-2 | P1 | （缺表：人才流动/任职变迁边） | 请给出人才在机构间流动或任职变迁的入站 `dwd_*`（两端含人才稳定码 + 机构稳定码 + 事件日）表名 + 样例 3 行；或书面「不交付」。不请对方算流动率。随口径修订。 | `M_TALENT_FLOW_TRACK`, `M_TALENT_DEEP_157_1`, `M_TALENT_RELATION_NET`, `M_TALENT_GRAPH_110_1`, `M_TALENT_GRAPH_111_1`, `M_TALENT_DEEP_160_1` | `SYNTH-P0-3`（综合维人才流动边；本叶补人才库侧主键口径） |
| TALENT-P1-3 | P1 | （缺列：学历/职称/年龄分箱键） | 请给出支撑结构分箱的入站列（默认最高学历；职称/年龄若有则点名列），样例各 1 行；不请对方 COUNT。**领域码见 P0-2，所属机构见 P1-4，不写进本问。** 随口径修订。 | `M_TALENT_STRUCT_QUERY`, `M_TALENT_SUPPLY_STRUCT` | |
| TALENT-P1-4 | P1 | （缺列：当前所属机构稳定码） | 请给出人才**当前所属**机构的入站键（`talent_id` + 机构稳定码 / 组织机构代码，或对照表）+ 样例 3 行；不要只用机构名称。本问不是流动边（流动见 P1-2）。随口径修订。 | `M_TALENT_ORG_DIST`, `M_TALENT_UNIV_NEW`, `M_TALENT_FLOW_TRACK` | `ORG-P0-1`；`ENT-P2-1`；`SYNTH-P0-5`（机构侧主键/类型；本叶要人才→机构 JOIN） |
| TALENT-P1-5 | P1 | （缺列：人才地理区划码） | 请给出人才计数用的地理单元码列（国家/省级；全球库含境外），或书面确认只通过所属机构 JOIN 主档区划。样例 3 行；不要只用城市中文名。随口径修订。 | `M_TALENT_REGIONAL_DIST`, `M_TALENT_FLOW_TRACK` | `ENT-P0-1`（企业主档区划；若人才无独立地理列可复用所属机构 JOIN，仍须书面确认） |

- sidecar：**已 upsert**（见上）。拟表仍保留作当日对照。
- 声明：草案标「随口径修订」。不把综合维已问列改写成重复甲方题；本叶仍可对久新问人才库主表（与 SYNTH 交叉引用）。

## 2026-09-02

- 任务：`DATA-SUPPLIER-Q-TALENT-L01`（`in_progress`）。叶不标 `done`。
- **当时判定**：合同五维外 → 本期不开口；现行空表；sidecar 未写。
- **2026-09-04 废止「不开口」对外策略**（监管人改口：交付仍需用人数据 → 按对外口径罗列）。09-02 类型计数仍有效作对照：STAT 1 / third_party 31。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 TALENT-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
