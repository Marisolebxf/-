# 机构库 — 给久新的入站缺口问题清单

```yaml
---
doc_id: ORG-SUPPLIER-QUESTIONS
element: ORG
role: source
status: draft
version: "2026-09-01"
updated: 2026-09-01
owner: human:郭万迎
audience: 久新（书面回复） / PM 转发
---
```

> **对接：久新**（科研机构 `ORG`，**不是**产业服务 `SVC`）。本清单只抽 `M_ORG_*` 入站 `dwd_*` 缺口，不与 SVC / 政策 / 企业清单混发。  
> **用途**：只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> **方法**：见 [../README.md](../README.md)。供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。2026-09-01 监管人已确认分析日志，已升现行待回复并回填 sidecar。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| ORG-P0-1 | P0 | （缺列：kit 未给出 `dwd_*.col`） | 请书面给出科研机构入站表名、主键列与稳定码列（组织机构代码或等价，不要只用名称）及样例 3 行。随口径修订。 | `M_ORG_ATTENTION_TREND`, `M_ORG_ATTRACT_SCORE`, `M_ORG_BASE_99_1`, `M_ORG_COLLAB_CHAIN`, `M_ORG_CULTIVATE_SCORE`, `M_ORG_DEEP_149_1`, `M_ORG_DEEP_150_1`, `M_ORG_DEEP_151_1`, `M_ORG_DEEP_152_1`, `M_ORG_DEEP_153_1`, `M_ORG_DEEP_154_1`, `M_ORG_DEEP_155_1`, `M_ORG_GRAPH_114_1`, `M_ORG_GRAPH_115_1`, `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_PERF_QUERY`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_SZ_STATUS`, `M_ORG_TECH_LAYOUT`, `M_ORG_TECH_SCORE` | 2026-09-01 |
| ORG-P1-1 | P1 | （缺列：指数/排名值列未给出） | 请说明各指数/排名落在哪张入站 `dwd_*`、主键与更新频率（须点名值列），并给样例 3 行；不问公式。随口径修订。 | `M_ORG_ATTENTION_TREND`, `M_ORG_ATTRACT_SCORE`, `M_ORG_BASE_99_1`, `M_ORG_COLLAB_CHAIN`, `M_ORG_CULTIVATE_SCORE`, `M_ORG_DEEP_149_1`, `M_ORG_DEEP_150_1`, `M_ORG_DEEP_151_1`, `M_ORG_DEEP_152_1`, `M_ORG_DEEP_153_1`, `M_ORG_DEEP_154_1`, `M_ORG_DEEP_155_1`, `M_ORG_GRAPH_114_1`, `M_ORG_GRAPH_115_1`, `M_ORG_INDUSTRY_COVER`, `M_ORG_NEW_TREND`, `M_ORG_SZ_ADVANTAGE`, `M_ORG_SZ_PAINPOINT`, `M_ORG_SZ_STATUS`, `M_ORG_TECH_LAYOUT`, `M_ORG_TECH_SCORE` | 2026-09-01 |
| ORG-P1-2 | P1 | （缺列：机构↔论文关联未给出） | 请给出机构稳定码与论文主键相连的入站 `dwd_*` 表.列（或对照表）及样例 3 行；不请对方 COUNT。随口径修订。 | `M_ORG_PERF_QUERY` | 2026-09-01 |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id，metric_id 并列。MIXED 本波不进本表。 -->

---

# 分析日志（新的在上）

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
