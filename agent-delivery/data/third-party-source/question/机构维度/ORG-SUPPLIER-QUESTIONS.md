# 机构库 — 给久新的入站缺口问题清单

```yaml
---
doc_id: ORG-SUPPLIER-QUESTIONS
element: ORG
role: source
status: draft
version: "2026-09-04"
updated: 2026-09-04
owner: human:郭万迎
audience: 久新（书面回复） / PM 转发
---
```

> **对接：久新**（科研机构 `ORG`，**不是**产业服务 `SVC`）。本清单只抽 `M_ORG_*` 入站 `dwd_*` 缺口，不与 SVC / 政策 / 企业清单混发。  
> **用途**：只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> **方法**：见 [../README.md](../README.md)。供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **兄弟域同列**：其他域现行待回复里已问过同类入站缺口时填对方 Q-id；无则留空。不代替本叶对久新提问。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 | 兄弟域同列 |
|------|--------|-----------|--------|------------------|------------|------------|
| ORG-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出科研机构入站表名、主键列与稳定码列（组织机构代码或等价，不要只用名称）及样例 3 行。随口径修订。 | `M_ORG_ATTENTION_TREND`, `M_ORG_ATTRACT_SCORE`, `M_ORG_BASE_99_1`, `M_ORG_COLLAB_CHAIN`, `M_ORG_CULTIVATE_SCORE`, `M_ORG_DEEP_149_1`, `M_ORG_DEEP_150_1`, `M_ORG_DEEP_151_1`, `M_ORG_DEEP_152_1`, `M_ORG_DEEP_153_1`, `M_ORG_DEEP_154_1`, `M_ORG_DEEP_155_1`, `M_ORG_GRAPH_114_1`, `M_ORG_GRAPH_115_1`, `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_PERF_QUERY`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_SZ_STATUS`, `M_ORG_TECH_LAYOUT`, `M_ORG_TECH_SCORE` | 2026-09-04 | `SYNTH-P0-5`；`SVC-P0-1`；`ENT-P2-1`（企业主档主键，不替代科研机构库） |
| ORG-P0-2 | P0 | （缺列：产业链/产业领域稳定码） | 请给出科研机构参与的**产业链/产业领域稳定码**（或 `org_id`↔产业码对照）：码列名、合法枚举、JOIN 键、样例 3 行；不要只用产业中文名。随口径修订。 | `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_SZ_STATUS`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT` | 2026-09-04 | `ENT-P0-2`（企业 tags/`INB*`；科研机构侧仍须点名本库对照，勿默认同一张 tags） |
| ORG-P0-3 | P0 | （缺列：学科/技术领域稳定码） | 请给出机构×**学科/前沿方向/技术领域**稳定码（或对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充技术领域。随口径修订。 | `M_ORG_TECH_LAYOUT`, `M_ORG_DEEP_149_1`, `M_ORG_ATTENTION_TREND`, `M_ORG_NEW_TREND` | 2026-09-04 | `TECH-P0-2`（技术点领域码，不替代机构×领域布局） |
| ORG-P1-1 | P1 | （缺列：指数/排名值列未给出） | 请说明各指数/排名落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），并给样例 3 行；不问公式。随口径修订。 | `M_ORG_ATTENTION_TREND`, `M_ORG_ATTRACT_SCORE`, `M_ORG_BASE_99_1`, `M_ORG_COLLAB_CHAIN`, `M_ORG_CULTIVATE_SCORE`, `M_ORG_DEEP_149_1`, `M_ORG_DEEP_150_1`, `M_ORG_DEEP_151_1`, `M_ORG_DEEP_152_1`, `M_ORG_DEEP_153_1`, `M_ORG_DEEP_154_1`, `M_ORG_DEEP_155_1`, `M_ORG_GRAPH_114_1`, `M_ORG_GRAPH_115_1`, `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_SZ_STATUS`, `M_ORG_TECH_LAYOUT`, `M_ORG_TECH_SCORE` | 2026-09-04 | |
| ORG-P1-2 | P1 | （缺列：机构↔论文关联未给出） | 请给出机构稳定码与论文主键相连的入站 `dwd_*` 表.列（或对照表）及样例 3 行；不请对方 COUNT。随口径修订。 | `M_ORG_PERF_QUERY` | 2026-09-04 | |
| ORG-P1-3 | P1 | （缺列：科研机构类型码） | 请给出能圈定/分组**高校 / 科研院所**（及与企业区分）的类型码列或对照表 + 合法枚举 + 样例 3 行（机构主键 + 类型码）。不要只用名称。PERF 可按 `org_type` 分组。随口径修订。 | `M_ORG_PERF_QUERY` | 2026-09-04 | `SYNTH-P0-5`；`SVC-P0-1`（服务圈定类型；本叶要科研机构库类型码） |
| ORG-P1-4 | P1 | （缺列：地理区划/深圳圈定） | 请给出科研机构地理单元码（建议 6 位 adcode）或书面深圳圈定规则 + 样例 3 行；不要只用城市中文名。随口径修订。 | `M_ORG_SZ_STATUS`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_CULTIVATE_SCORE` | 2026-09-04 | `ENT-P0-1`（企业主档区划；科研机构若独立主档仍须本列） |
| ORG-P1-5 | P1 | （缺表：机构↔机构合作边） | 请给出论文/项目等合作记录上**两端均为科研机构稳定码**的入站边表（或可抽出机构–机构边的表.列）+ 样例 3 行；不请对方 hang 图。本问不是 P1-2 的论文 COUNT。随口径修订。 | `M_ORG_COLLAB_CHAIN`, `M_ORG_DEEP_153_1`, `M_ORG_GRAPH_115_1` | 2026-09-04 | `SYNTH-P0-1`（项目–机构边；本叶要科研机构合作网络） |
| ORG-P1-6 | P1 | （缺列：机构↔专利） | 请给出机构稳定码与专利主键相连的入站 `dwd_*` 表.列（权利人须稳定码，不要只给名称）+ 样例 3 行。随口径修订。 | `M_ORG_COLLAB_CHAIN`, `M_ORG_TECH_LAYOUT`, `M_ORG_INDUSTRY_COVER` | 2026-09-04 | `ENT-P0-6`；`SYNTH-P0-4`（企业/联合专利；科研机构权利人仍须对上本库稳定码） |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id，metric_id 并列。MIXED 本波不进本表。 -->

> **2026-09-04**：监管人确认升现行。轴拆 9 题已写入上表；sidecar `as_of=2026-09-04` 已 upsert 22 条。叶不标 `done`。

---

# 分析日志（新的在上）

## 2026-09-04

- 任务：`DATA-SUPPLIER-Q-ORG-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。监管人指示：**重扫机构维**；交付侧仍需科研机构数据项；表头加「兄弟域同列」。叶不标 `done`。
- 合同说明：科研机构专题对接久新；与人才/技术同属「非智树五维合同包」时，仍按**对外口径**列入口缺口（交付要用）。
- 本批算法类型：STAT 1 / COMPUTE 0 / GRAPH 0 / MODEL 0 / third_party 21 / UNKNOWN 0 / MIXED 0
- 本批指标（registry 机构域 **22** 条 = 全量；MCP `metric-query domain=ORG fields=full limit=50`；**未**打开 seed YAML）：
  - STAT：`M_ORG_PERF_QUERY`
  - third_party：其余 21 条（与 2026-09-01 同批 ID）
- D1：draft 22 / aligned 0。D4 仍 `mock`（MCP 只读）。
- kit 回看：22 条 `source_tables` / `source_systems` 均为 `pending_ods`，**仍抽不出任何入站 `dwd_*.column`**。`metrics/calc-logic/ORG/` **仍无文件**。`formula` 均为 `pending_cosign: human:唐绍祖（未签）`；本批非 MODEL → **不问打分公式**。
- 游标：sidecar 已有 ORG `as_of=2026-09-01`；问法未变 → **不新开 Q 号**，复用 ORG-P0-1 / P1-1 / P1-2。
- 入站抽样：**未探库**（无列可对）。
- 跳过：MIXED 0；二次 0；CMS-only 未判。
- 甲方去重（不改写）：Q084–Q092、Q104、Q055。
- 兄弟域交叉（现行 3 题已填）：ORG-P0-1 ↔ `SYNTH-P0-5` / `SVC-P0-1` / `ENT-P2-1`。
- 补漏（与 TECH-P0-2 / TALENT-P0-2 同逻辑）：产业码、学科/技术领域码、机构类型、区划/深圳圈定、机构–机构合作边、机构–专利边 **不能** 揉进 ORG-P0-1 主键。`INB*` ≠ 技术领域；企业主档区划 ≠ 科研机构圈定。
- 拟升现行：监管人 **2026-09-04 10:17 确认升现行**（上表 9 题）。
- sidecar：**已 upsert** 22 条（`domain=ORG`，`as_of=2026-09-04`）。挂靠：产业轴→P0-2；学科/技术领域→P0-3；合作边→P1-5；深圳圈定→P1-4；PERF→P1-2；其余 third_party→P0-1。

| 拟 Q-id | 优先级 | 入站表.列（拟） | 问什么 | 卡住的 metric_id | 兄弟域同列 |
|---------|--------|-----------------|--------|------------------|------------|
| ORG-P0-1 | P0 | （缺列：主表/主键/稳定码） | 已在现行。科研机构入站表名、主键、稳定码（组织机构代码或等价）。随口径修订。 | 本批 22 条 | `SYNTH-P0-5`；`SVC-P0-1`；`ENT-P2-1` |
| ORG-P0-2 | P0 | （缺列：产业链/产业领域稳定码） | 请给出科研机构参与的**产业链/产业领域稳定码**（或 `org_id`↔产业码对照）：码列名、合法枚举、JOIN 键、样例 3 行；不要只用产业中文名。随口径修订。 | `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_SZ_STATUS`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT` | `ENT-P0-2`（企业 tags/`INB*`；科研机构侧仍须点名本库对照，勿默认同一张 tags） |
| ORG-P0-3 | P0 | （缺列：学科/技术领域稳定码） | 请给出机构×**学科/前沿方向/技术领域**稳定码（或对照表）：码列名、合法枚举、与主表 JOIN 键、样例 3 行；不要只用中文领域名。**禁止**用产业链 `INB*` 冒充技术领域。随口径修订。 | `M_ORG_TECH_LAYOUT`, `M_ORG_DEEP_149_1`, `M_ORG_ATTENTION_TREND`, `M_ORG_NEW_TREND` | `TECH-P0-2`（拟升；技术点领域码，不替代机构×领域布局） |
| ORG-P1-1 | P1 | （缺列：指数/排名值列） | 已在现行。指数/排名落表、主键、更新频率、值列。不问公式。 | 21 条 third_party | |
| ORG-P1-2 | P1 | （缺列：机构↔论文） | 已在现行。机构稳定码↔论文主键。不请对方 COUNT。 | `M_ORG_PERF_QUERY` | |
| ORG-P1-3 | P1 | （缺列：科研机构类型码） | 请给出能圈定/分组**高校 / 科研院所**（及与企业区分）的类型码列或对照表 + 合法枚举 + 样例 3 行（机构主键 + 类型码）。不要只用名称。PERF 可按 `org_type` 分组。随口径修订。 | `M_ORG_PERF_QUERY`（及凡要「专题科研机构名录」的本批指标） | `SYNTH-P0-5`；`SVC-P0-1`（服务圈定类型；本叶要科研机构库类型码） |
| ORG-P1-4 | P1 | （缺列：地理区划/深圳圈定） | 请给出科研机构地理单元码（建议 6 位 adcode）或书面深圳圈定规则 + 样例 3 行；不要只用城市中文名。随口径修订。 | `M_ORG_SZ_STATUS`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_CULTIVATE_SCORE` | `ENT-P0-1`（企业主档区划；科研机构若独立主档仍须本列） |
| ORG-P1-5 | P1 | （缺表：机构↔机构合作边） | 请给出论文/项目等合作记录上**两端均为科研机构稳定码**的入站边表（或可抽出机构–机构边的表.列）+ 样例 3 行；不请对方 hang 图。本问不是 P1-2 的论文 COUNT。随口径修订。 | `M_ORG_COLLAB_CHAIN`, `M_ORG_DEEP_153_1`, `M_ORG_GRAPH_115_1` | `SYNTH-P0-1`（项目–机构边；本叶要科研机构合作网络） |
| ORG-P1-6 | P1 | （缺列：机构↔专利） | 请给出机构稳定码与专利主键相连的入站 `dwd_*` 表.列（权利人须稳定码，不要只给名称）+ 样例 3 行。随口径修订。 | `M_ORG_COLLAB_CHAIN`, `M_ORG_TECH_LAYOUT`, `M_ORG_INDUSTRY_COVER` | `ENT-P0-6`；`SYNTH-P0-4`（企业/联合专利；科研机构权利人仍须对上本库稳定码） |

- 拟改现行：**已升**。sidecar **已 upsert**。

## 2026-09-01

- 任务：`DATA-SUPPLIER-Q-ORG-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。监管人已确认本日志拟改；已升现行待回复并 upsert sidecar。叶仍不标 `done`。
- 本批算法类型：STAT 1 / COMPUTE 0 / GRAPH 0 / MODEL 0 / third_party 21 / UNKNOWN 0 / MIXED 0
- 本批指标（registry 机构域 22 条 = cap 22；sidecar 无 ORG `as_of` → 全进本批）：
  - STAT：`M_ORG_PERF_QUERY`
  - third_party：`M_ORG_ATTENTION_TREND`, `M_ORG_ATTRACT_SCORE`, `M_ORG_BASE_99_1`, `M_ORG_COLLAB_CHAIN`, `M_ORG_CULTIVATE_SCORE`, `M_ORG_DEEP_149_1`, `M_ORG_DEEP_150_1`, `M_ORG_DEEP_151_1`, `M_ORG_DEEP_152_1`, `M_ORG_DEEP_153_1`, `M_ORG_DEEP_154_1`, `M_ORG_DEEP_155_1`, `M_ORG_GRAPH_114_1`, `M_ORG_GRAPH_115_1`, `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_SZ_STATUS`, `M_ORG_TECH_LAYOUT`, `M_ORG_TECH_SCORE`
- D1 快照：aligned 0 / draft 22（本批；MCP 只读，禁止改矩阵）。D4 全 `mock`。
- kit 回看（MCP `metric-query domain=ORG fields=full`；**未**打开 `metrics/registry` YAML）：
  - 22 条 `source_tables` / `source_systems` 均为 `pending_ods`，**抽不出任何入站 `dwd_*.column`**。
  - `metrics/calc-logic/ORG/` **无文件** → 入站列不猜表名（不把映射报告 / Q055 里的 `dwd_org_*` 写进拟题表.列）。
  - `formula` 均为 `pending_cosign: human:唐绍祖（未签）`。本批 kit 类型是 **third_party / STAT**，不是 MODEL：问指数落表与最少键，**不问打分公式**。未记「等唐绍祖入参清单」（那条只绑 MODEL 入参键不清）。
  - 若干 ID 名带 GRAPH/DEEP、定义里写过建议 COMPUTE/GRAPH：**本波仍按 kit `algorithm_type`**，不按名字拆 MIXED。
- 入站抽样：**未探库**。kit 无入站表.列可对；禁止为凑证据猜 `dwd_org_*` 去 COUNT。需要证据时再只读 live `gkx`、`is_deleted=0`。
- 跳过、不进对外清单：
  - MIXED：0
  - 二次（formula / 细稿 `<- metric:`）：0
  - CMS-only / 无入站 `dwd_*` 依赖：0 条可判 CMS-only；22 条均为 `pending_ods`（未核 ≠ 已确认无表）
  - 游标已分析：0（`source-gap-index.yaml` 无 ORG `as_of`）
- 甲方去重（`客户决策清单跟踪表.md`，**不改写成久新题**）：Q084–Q092（Q-MO-ORG-01…09）、Q104（Q-MO-QUERY-02）是口径/拆 ID；Q055 是机构库到位时间（已登记甲方/供方）。拟题只问「表名+主键列+稳定码列+指数落点」，不复述 Q055 的空表名单，不把 `dwd_org_base_info`（SVC 圈定）串进本叶。
- 拟新 Q（监管人确认后已写入现行表；复用 0）：

| 拟 Q-id | 优先级 | 入站表.列（拟） | 现象 | 请久新确认 | 卡住的 metric_id |
|---------|--------|-----------------|------|------------|------------------|
| ORG-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 22 条均 `pending_ods`；无细稿列。缺稳定主键则图谱 hang / 去重 / 指数对不上 VID | 请书面给出科研机构入站**表名 + 主键列名 + 稳定码列名**（组织机构代码或等价机构码，不要只用名称）+ 样例 3 行（对方主键 + 码原值）+ 空值规则。随口径修订。 | 本批 22 条 |
| ORG-P1-1 | P1 | （指数/排名落点未给出） | 21 条 kit=`third_party`；不问建模与公式 | 请说明各指数/排名/模型输出落在哪张入站 `dwd_*`、主键、更新频率；若与 P0-1 同一表则复用该表名，仍须点名**值列**。给表名 + 样例 3 行。随口径修订。 | 21 条 third_party（不含 `M_ORG_PERF_QUERY`） |
| ORG-P1-2 | P1 | （机构↔论文关联列未给出） | STAT「查询结果·科研机构绩效」= 结果集内关联论文数 COUNT；不请对方 COUNT | 请给出把机构稳定码与论文主键连上的入站 `dwd_*` **表.列**（或对照表）+ 样例 3 行。随口径修订。 | `M_ORG_PERF_QUERY` |

- 拟复用 Q：无（本域尚无现行 Q-id）。
- 声明：草案口径标「随口径修订」。本批不把 GRAPH 名指标改问 hang 公式；不把 SVC 服务机构题并进来。
- sidecar：本批 upsert 22 条（`domain=ORG`，`as_of=2026-09-01`）。21 条 third_party → `ORG-P0-1`；`M_ORG_PERF_QUERY` → `ORG-P1-2`。清单见 `source-gap-index.yaml`。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 ORG-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
