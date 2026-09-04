# 科技动态 — 给外部对接方的缺口问题清单

```yaml
---
doc_id: TNIE-SUPPLIER-QUESTIONS
element: TNIE
role: source
status: draft
version: "2026-09-04"
updated: 2026-09-04
owner: human:郭万迎
audience: 外部对接方（CMS / 资讯库 / 入站 dwd，不限是否久新） / PM 转发
---
```

> **域码 `TNIE`（科技动态）。** 对接方**不限久新**：凡生产依赖的外部系统（内容运营 CMS、资讯库、入站 `dwd_*`）都列题。  
> **监管**：进度表专题维度Owner **`human:郭万迎`**。任务 `DATA-SUPPLIER-Q-TNIE-L01`。  
> **仍不问**：本方 `ads_*` / SQLite / `/internal/tech-news` 派生列、`related_entities`、甲方 Q-*、请对方替我们 `len(events)`。  
> **方法**：见 [../README.md](../README.md)。sidecar：[`../source-gap-index.yaml`](../source-gap-index.yaml)。  
> **兄弟域同列**：`ENT-P1-2` 是企业重点资讯表，不替代科创事件主档。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主。草案标「随口径修订」。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 | 兄弟域同列 |
|------|--------|-----------|--------|------------------|------------|------------|
| TNIE-P0-1 | P0 | （缺：科创事件外部主档；系统未点名） | 请书面点名生产主档落在哪套**外部**系统（久新/其它 CMS、资讯库、入站 `dwd_*`，可并列），以及稳定事件/新闻主键、`publish_status`（门户是否只收已发布）、与本系统 JOIN 键、样例 3 条。不要用本方 `ads_tech_news_*` / `sandbox_sqlite_*`。随口径修订。 | `M_TNIE_EVENT_COUNT` | 2026-09-04 | `ENT-P1-2`（企业重点资讯，不替代科创事件） |
| TNIE-P0-2 | P0 | （缺：抽取原料正文或 URL） | 请给出可供四要素抽取的**正文列**或稳定可抓取 URL（编码、空值规则）+ 样例 3 条（主键 + 正文或 URL）。不问本方 `len(response.events)`。随口径修订。 | `M_TNIE_EVENT_COUNT` | 2026-09-04 | |
| TNIE-P1-1 | P1 | （缺：标题 / 时间 / 地点 / 描述） | 请给出事件详情四字段在外部资源上的列名（或 CMS `content_type` + 字段）+ 空值规则 + 样例 3 条。对应展示「科创事件」详情，不是本方 ADS。随口径修订。 | `M_TNIE_EVENT_COUNT` | 2026-09-04 | |
| TNIE-P1-2 | P1 | （缺：发生时间 vs 发布时间） | 请点名日/周/月/自定义区间过滤用哪一列时间戳、时区、发生时间与发布时间是否两列 + 样例 3 条。随口径修订。 | `M_TNIE_EVENT_COUNT` | 2026-09-04 | |
| TNIE-P1-3 | P1 | （缺：相关主体稳定码） | 请给出事件↔机构/人员的外部稳定码列（或对照表）+ 样例 3 条；不要只用中文名。不问本方 `related_entities`。随口径修订。 | `M_TNIE_EVENT_COUNT` | 2026-09-04 | `ORG-P0-1`；`TALENT-P1-4`（机构/人才主键，事件侧仍须点名本资源挂接列） |

<!-- MIXED 本波不进。本方 ADS/抽取 API 不问字段名。甲方 Q-* 不改写。 -->

> **2026-09-04**：`human:郭万迎` 改口径——外部依赖一律列题，不限久新；CMS/资讯库不再因「非 dwd」跳过。上表 5 题已写入；sidecar `as_of=2026-09-04` 1 条挂 `TNIE-P0-2`。叶不标 `done`。

---

# 分析日志（新的在上）

## 2026-09-04（口径修订 · 外部一律列题）

- 任务：`DATA-SUPPLIER-Q-TNIE-L01`（`in_progress`；`supervised_by=human:郭万迎`）。监管人当场改口径：**对接方不限久新，凡依赖外部都列清单**。CMS / 资讯库与入站 `dwd_*` 同列；仍不问本方 ADS/SQLite/内部抽取 API 的表名当「入站列」。
- 本批：STAT 1（`M_TNIE_EVENT_COUNT`）/ MIXED 0 / MODEL 0。MCP `metric-query domain=TNIE fields=full`；**未**打开 seed YAML。
- kit：`formula=len(response.events)`；`source_tables` 仍是项目 ADS/SQLite（**禁问对方要这些表**）；`source_systems` 是本方网关/mock。生产原料与展示列表不在 kit 表名里。
- 外部依赖（展示 DS-01 科创事件 `other_system` + 抽取要正文）：CMS 或资讯库的事件主档、正文/URL、详情四字段、时间戳、相关主体码。E31 CMS 契约**尚未**登记科创事件 `content_type`，故 P0-1 先问系统身份，不猜表名。
- 轴拆（不把领域/区划/机构主档折进主键题）：P0-1 主档系统+主键+发布态；P0-2 正文/URL；P1-1 详情四字段；P1-2 时间轴；P1-3 主体稳定码。
- 跳过、不进对外清单：MIXED 0；二次 0；**本方计算路径**（Java/Python `/internal/tech-news`、mock sqlite）0 题。
- 甲方去重（不改写）：是否纳入正式 KPI；Q051 产业实体边界；事件类型枚举（PDR 🟡）。
- 拟升→现行：**5**（监管人要求当场补表）。拟复用 0。CHAIN 资讯表已弃用，不挂 CHAIN 题号。
- sidecar：upsert **1**（`M_TNIE_EVENT_COUNT` → `TNIE-P0-2`；摘要指向 P0-1）。`source_gap_indexed` TNIE=1。

## 2026-09-04（首扫 · 已作废跳过结论）

- 当时按旧规则把本条判 CMS-only / 无入站 dwd → 拟升 0。**已被同日口径修订作废**，现行表以上节为准。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id |
| 对接系统 | CMS / 资讯库 / 入站 `dwd_*` / 其它（写名称） |
| 现状 | 资源名 / 字段 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
