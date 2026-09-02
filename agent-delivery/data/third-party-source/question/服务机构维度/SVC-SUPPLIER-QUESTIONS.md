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

> **用途**：只问供应方入站 `dwd_*` 字段与主键。`DATA-SUPPLIER-Q-SVC-L01`：STAT/GRAPH + MODEL 入参后，按待办**挂起项**与**全球名录**补题。本叶**未 live 探库**。证据：`SVC-ALGO-STAT-21-L01-侯佳伟待办.md`（2026-08-28 Demo：圈定 3525 / 深圳 1355；海外 0 行；港澳台有行 ∩ circle 0；无 org×8 领域×6 环节表）。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **sidecar**：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。  
> **不要问对方**：项目 ADS/DWD（`svc_org_card` / `svc_org_circle` / `svc_metric_*` / `related_entities`）；甲方口径 Q-SVC-001/008/010、Q-SVC-004、Q-SVC-006、Q-SVC-007、Q-SVC-009；Q-SVCCHAIN-01…05（权重/阈值/分档公式）；Q-SVCCHAIN-06/07/08 **只问入站表.列**，不问「页面是否仍要该矩阵 / 何时把格子换成真全球」；Q062；请对方 COUNT / 打分 / 训模型；用名称猜点。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。草案口径标「随口径修订」。

跨维已有题、**不在本表重复开号**（sidecar 仍 upsert，`q_id` 指向他维）：

| 跟哪题 | 入站列 | 卡住的 SVC metric（STAT 首批 + MODEL） |
|--------|--------|----------------------------------------|
| `ENT-P0-1` | `dwd_org_base_info` 缺稳定行政区划码 | STAT：`M_SVC_PT_SZ_TOTAL`, `M_SVC_PT_SZ_REGION_ORG`, `M_SVC_PT_REGION_ORG`, `M_SVC_SZ_COMPARE_METRIC`。MODEL：`M_SVC_SZ_TIER`, `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_DEEP_180_1`（城市过滤） |
| `ENT-P0-2` | `dwd_org_industry_tags` 企业上链 INB（**不是**门户 8 领域 / 六环节） | MODEL：`M_SVC_ORG_MARKET_HEAT`（产业过滤代理）。STAT/MODEL 的 8×6 已改挂 `SVC-P0-3` |
| `ENT-P0-4` | `dwd_org_annual_financial_info.development_employee` | MODEL：`M_SVC_ORG_TECH_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_DEEP_178_1`, `M_SVC_DEEP_180_1`, `M_SVC_DEEP_181_1` |
| `ENT-P0-5` | 同表 `arch_development_am` / `operating_revenue` | MODEL：`M_SVC_ORG_TECH_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_DEEP_172_1`, `M_SVC_DEEP_180_1`, `M_SVC_DEEP_181_1`。待办：营收全库 286 ∩ 圈定 **0** |
| `ENT-P0-6` | 专利受让人名称未对齐 `org_id` | MODEL：`M_SVC_ORG_TECH_SCORE`, `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_DEEP_175_1` |
| `ENT-P0-7` | `dwd_org_tech_tag` 无稳定码 | MODEL：`M_SVC_DEEP_176_1`, `M_SVC_DEEP_178_1` |
| `ENT-P1-1` | `dwd_patent_legal.status` | MODEL：`M_SVC_ORG_TECH_SCORE`, `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_DEEP_175_1`, `M_SVC_DEEP_179_1` |
| `ENT-P1-2` | `dwd_org_important_news_info` | MODEL：`M_SVC_ORG_TECH_SCORE`, `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_DEEP_174_1`, `M_SVC_DEEP_175_1`, `M_SVC_DEEP_177_1`, `M_SVC_DEEP_178_1`。案例是否供应属甲方 Q-SVC-007，不改写 |
| `ENT-P2-1` | `dwd_org_base_info.org_id` / 信用代码 | STAT：`M_SVC_ORG_TOTAL`。全球总数改挂 `SVC-P0-4` |
| `ENT-P1-3` | `dwd_forg_base_info` 0 行 | 海外主档企业维已问；SVC 全球圈定/灌数排期见 `SVC-P0-4`，不重复开号问「是否 0 行」 |
| `SYNTH-P0-1` | `dwd_zh_project.funded_institution` 是名称不是边 | MODEL：`M_SVC_DEEP_179_1` |
| `POLICY-P0-1` | `dwd_policy_base.keywords` | MODEL：`M_SVC_DEEP_180_1`, `M_SVC_DEEP_181_1`（政策匹配入参；不问权重） |

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| SVC-P0-1 | P0 | `dwd_org_heis_info`（或缺机构大类码列） | 全球/深圳类型分布需要稳定分成**高校 / 科研院所 / 企业**。请确认：① 是否交付 `dwd_org_heis_info`（或等价表），主键如何与 `dwd_org_base_info.org_id` JOIN；② `univ_type`（或同类码）合法值；③ 科研院所是否另表/另码，不要只给中文名称。随口径修订。 | `M_SVC_PT_GLOBAL_TYPE_DIST`, `M_SVC_PT_SZ_TYPE_DIST`, `M_SVC_DEEP_179_1` | 2026-09-02 |
| SVC-P0-2 | P0 | `dwd_org_annual_financial_info.employees_number` | 规模四档与 MODEL 从业人数入参都扫**本列**，不是研发人员、也不是主表 `org_size`（微小中大）。待办 2026-08-28 Demo：本列全库 452 家有数，∩ 圈定 3525 为 **0**（换信用代码仍 0）。请确认：列是否正式交付、空值约定（SQL NULL / 0 / 空串）、年主键（`org_id`+年）；圈定机构为何对不上人数。企业维已问 `development_employee`（ENT-P0-4）。随口径修订。 | `M_SVC_PT_GLOBAL_SCALE_DIST`, `M_SVC_PT_KEYORG_SCALE`, `M_SVC_ORG_TECH_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_DEEP_176_1`, `M_SVC_DEEP_178_1`, `M_SVC_DEEP_180_1`, `M_SVC_DEEP_181_1` | 2026-09-02 |
| SVC-P0-3 | P0 | （缺表）机构 × **8 领域码** × **6 环节码** | 待办第 14–18、20 条挂起：入站**没有**服务记录表。门户/生态字典：8 领域（生物医药 / 电子信息 / 人工智能 / 高端装备 / 新能源 / 前沿新材料 / 量子信息 / 深地深海）× 6 环节（研发与科研合作 / 知识产权与标准 / 技术转移与孵化 / 中试熟化 / 检测认证 / 市场化服务）。请交付：表名 + `org_id`（或信用代码）+ 领域码 + 六环节码 + 样例 3 行（一家可多领域、多环节）；码列合法值。**禁止**用企业上链 INB、服务六类（FINANCE/IP/…）、国标 `industry`、15 集群冒充。广度只要领域轴；环节家数/平均深度/堵点还要环节轴（深度公式、阈值不问）。随口径修订。 | `M_SVC_PT_SZ_FIELD_DIST`, `M_SVC_PT_CHAIN_NODE_ORG`, `M_SVC_CHAIN_SEGMENT_ORG_COUNT`, `M_SVC_CHAIN_SEGMENT_AVG_DEPTH`, `M_SVC_ORG_COVERAGE_BREADTH`, `M_SVC_SZ_CHAIN_COMPLETENESS`, `M_SVC_CHAIN_BOTTLENECK`, `M_SVC_ORG_COVERAGE_DEPTH`, `M_SVC_DEEP_172_1`, `M_SVC_REC_CANDIDATE_CNT` | 2026-09-02 |
| SVC-P0-4 | P0 | `dwd_forg_base_info`（海外主档） | 门户「全球」要海外名录。待办 Demo：**0 行**。企业维 ENT-P1-3 已问是否交付。本问补产业服务：① 何时灌数、行数预期；② `org_id` / `country_code` / `country` 是否稳定、空值；③ 用哪一列圈**服务机构**（不要只给名称）。国内主表无国家列，圈定 3525 全广东不能当真全球。随口径修订。 | `M_SVC_PT_GLOBAL_TOTAL`, `M_SVC_PT_GLOBAL_TYPE_DIST`, `M_SVC_PT_REGION_ORG`, `M_SVC_PT_GLOBAL_SCALE_DIST` | 2026-09-02 |
| SVC-P0-5 | P0 | `dwd_special_hongkong_company` / `dwd_special_taiwan_company` / `dwd_special_aomen_company` | 港澳台三张主体表待办有行（港 40000 / 台 40000 / 澳 792），∩ 圈定 **0**；国内主表 `province` 香港/澳门/台湾 **0**。无港/台/澳经营或行业卫星；共用融资/投资/要闻对台澳为 0，香港也无国标行业列，不能按国内规则圈服务机构。请确认：① 三表与国内 `org_id` 如何对齐；② 有无经营范围/行业码卫星（表名 + 样例 3 行）；③ 国内主档是否补国家/地区稳定码。不要用名称硬套。随口径修订。 | `M_SVC_PT_GLOBAL_TOTAL`, `M_SVC_PT_GLOBAL_TYPE_DIST`, `M_SVC_PT_REGION_ORG`, `M_SVC_PT_GLOBAL_SCALE_DIST` | 2026-09-02 |
| SVC-P1-1 | P1 | （缺表）服务机构 ↔ 服务机构边 | 入站未见「服务–服务」合作/参与边（图谱 `participates` / 影响力 / 关系链两端都要本批服务机构稳定 VID）。投资/股东边（`dwd_org_invest_info` / `dwd_org_shareholder_info`）**不是**服务关系。请交付：表名 + 两端 `org_id`（或信用代码）+ `relation_type` 样例 3 行；合法值至少能标服务合作。不要用名称猜点，不要在供应库 hang 图。随口径修订。 | `M_SVC_GRAPH_DENSITY`, `M_SVC_GRAPH_CENTRALITY`, `M_SVC_GRAPH_INFLUENCE`, `M_SVC_DEEP_173_1` | 2026-09-02 |
| SVC-P1-2 | P1 | `dwd_org_base_info.incorporation_date`（或缺首次开展服务日） | 年度新增、市场热度序列目前只能用工商成立年。待办：圈定 3525 有成立日 3524、缺 1 家。请确认：成立日空值约定；是否另有「首次开展服务」日期列或另表（表名 + 样例 3 行）。斜率/评级映射不问。随口径修订。 | `M_SVC_ORG_NEW_COUNT`, `M_SVC_REC_CANDIDATE_CNT`, `M_SVC_ORG_MARKET_HEAT` | 2026-09-02 |
| SVC-P1-3 | P1 | `dwd_org_annual_financial_info.pure_profit` | 招引/短板/培育推荐要**净利润**作入参（增长率在项目侧算）。同表营收待办全库 286 ∩ 圈定 **0**。请确认本列是否正式交付、空值约定、年主键。不要把上市利润表 `yysr` 当本列。随口径修订。 | `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_DEEP_172_1`, `M_SVC_DEEP_181_1` | 2026-09-02 |
| SVC-P1-4 | P1 | `dwd_org_annual_financial_info.total_assets`（及 `total_liabilities`） | 培育规模、金融技术力要年报**资产（负债）**。待办：年报资产 `zyywsr` ∩ 圈定仅 **12**（深圳 3），财务宽表营收 ∩ 圈定 0。请确认 `total_assets` / `total_liabilities` 是否正式在年报财务表、与资产表关系、空值、年主键。随口径修订。 | `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_DEEP_174_1` | 2026-09-02 |
| SVC-P1-5 | P1 | `dwd_org_recruit_info`（`hiring_number` / `release_date` / `job_title`） | 人力资源服务机构技术力要招聘供给。请确认：表是否交付、与 `org_id` JOIN、空值、样例 3 行（机构 + 岗位人数 + 发布日）。满意度/流程规范是项目待建，不问。随口径修订。 | `M_SVC_DEEP_176_1` | 2026-09-02 |
| SVC-P1-6 | P1 | `dwd_org_subsidiary_info`（`org_id` / `sub_org_id`） | 引入推荐「深圳连接」要子公司边。请确认：表是否交付、两端稳定 `org_id`（或信用代码）、对端子公司城市如何对齐主档；样例 3 行。投资/股东不是本问。随口径修订。 | `M_SVC_DEEP_180_1` | 2026-09-02 |
| SVC-P1-7 | P1 | `dwd_org_risk_shixin` / `dwd_org_company_punish` | 金融服务机构技术力把失信、处罚当风险反向入参。请确认两表是否交付、与 `org_id` JOIN、主键、空值、样例各 1 行。融资事件空表属甲方 Q-SVC-006，不改写。随口径修订。 | `M_SVC_DEEP_174_1` | 2026-09-02 |
| SVC-P1-8 | P1 | `dwd_patent_transfer` | 科创服务机构技术力要专利转移日。请确认：表是否交付、`pn` 如何对专利主表、受让人是否信用代码/`org_id`（不要只给名称）；样例 3 行。申请人名称对齐跟 ENT-P0-6，不另开。随口径修订。 | `M_SVC_DEEP_179_1` | 2026-09-02 |

<!-- 一行一列聚类。多指标卡同一列 → 同一 Q-id。MIXED 本波不进本表。二次指标 / CMS-only 不另开题。 -->

---

# 分析日志（新的在上）

## 2026-09-02（待办挂起 + 全球名录）

- 来源：侯佳伟点名把待办**挂起项**与**全球/港澳台**入站缺口写进本清单；8 领域 × 6 环节不再挂 ENT-P0-2。
- 待办 1A 挂起（第 14–18、20 条）→ 供应方只问缺表，不问公式：

| 序号 | metric_id | 挂起原因（待办） | 本表 |
|------|-----------|------------------|------|
| 14 | `M_SVC_PT_SZ_FIELD_DIST` | 深圳领域×六环节无源 | `SVC-P0-3` |
| 15 | `M_SVC_PT_CHAIN_NODE_ORG` | **全球**领域×六环节热力无源 | `SVC-P0-3` |
| 16 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | 无机构×环节 + 深度分公式（公式仍甲方 Q-02） | `SVC-P0-3` |
| 17 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | 无机构×环节成员 | `SVC-P0-3` |
| 18 | `M_SVC_ORG_COVERAGE_BREADTH` | 无机构×领域（不要环节） | `SVC-P0-3` |
| 20 | `M_SVC_SZ_CHAIN_COMPLETENESS` | 完整度公式甲方 Q-04；若用六环节仍无源 | `SVC-P0-3` |
| 19 | `M_SVC_REC_CANDIDATE_CNT` | 1B 不写 ADS；培育按领域筛仍撞无源 | `SVC-P0-3`（领域）+ 已有 `SVC-P1-2`（成立日） |

- 全球纬度（待办 §6 / Q-SVCCHAIN-07 入站半截）：

| 入站 | 待办现网 | 本表 |
|------|----------|------|
| `dwd_forg_base_info` | **0 行** | `SVC-P0-4`（灌数/国家码/服务机构圈定列；0 行本身跟 ENT-P1-3） |
| 港/台/澳 `dwd_special_*` | 有行 ∩ circle **0**；无经营·行业卫星 | `SVC-P0-5` |
| 国内主表国家列 / `province` 港台澳 | 无 / **0** | 写入 `SVC-P0-5` 第③问 |

- 不问：权重阈值（Q-01…05）；页面是否仍要矩阵、何时把 3525 换成真全球（仍甲方）。不问 COUNT。
- sidecar：上列 STAT/MODEL 的 `q_id` 从 ENT-P0-2 / ENT-P2-1 改挂 `SVC-P0-3` / `SVC-P0-4`。
- 声明：监管人 `human:侯佳伟`。随口径修订。

## 2026-09-02（MODEL 入参）

- 本批算法类型：STAT 0 / COMPUTE 0 / GRAPH 0 / MODEL 18 / third_party 0 / UNKNOWN 0 / **MIXED 0（本波跳过）**
- 本批指标（禁止超当日 cap 20；本批 18）：
  - `M_SVC_CHAIN_BOTTLENECK`, `M_SVC_GRAPH_INFLUENCE`, `M_SVC_ORG_COVERAGE_DEPTH`, `M_SVC_ORG_MARKET_HEAT`, `M_SVC_ORG_TECH_SCORE`, `M_SVC_REC_ATTRACT_SCORE`, `M_SVC_REC_CULTIVATE_SCORE`, `M_SVC_SZ_TIER`, `M_SVC_DEEP_172_1`, `M_SVC_DEEP_173_1`, `M_SVC_DEEP_174_1`, `M_SVC_DEEP_175_1`, `M_SVC_DEEP_176_1`, `M_SVC_DEEP_177_1`, `M_SVC_DEEP_178_1`, `M_SVC_DEEP_179_1`, `M_SVC_DEEP_180_1`, `M_SVC_DEEP_181_1`
- D1 快照：aligned 1（`M_SVC_ORG_TECH_SCORE`）/ draft 17（registry lib `queryMetrics` domain=SVC `algorithm_type=MODEL`；禁止改矩阵）
- 入站抽样：**本叶仍未探库**。人数/营收/资产交叉用待办 2026-08-28 Demo `demo_gkxlumenx_ods`（圈定 3525）：`employees_number` ∩ 圈定 0；`operating_revenue` ∩ 圈定 0；年报资产 `zyywsr` ∩ 圈定 12。项目 ADS 卡面列**不问供应方**。
- 问法：只问 MODEL **入参**表.列；不问权重、极值归一化、招引/培育/梯队公式（甲方 Q-SVCCHAIN-01…05）。入参对不上表的记 blocked，等唐绍祖，不编列。
- 跳过、不进对外清单（本批）：
  - 权重/阈值/分档：Q-SVCCHAIN-01（技术力）、02（深度/热度映射）、03（堵点规则）、04（梯队框架）、05（招引/培育权重）
  - 六环节/全球名录入站表：当时未开，见上节 `SVC-P0-3` / `P0-4` / `P0-5`（侯佳伟点名后补）
  - 融资空表：Q-SVC-006（`DEEP_174` 的 `dwd_org_financing_info`）
  - 质量/案例/伙伴是否供应：Q-SVC-007（案例资讯代理跟 ENT-P1-2）
  - 项目待建：`svc_coop_*`、`svc_csat_score`、`svc_process_standard_flag`、`svc_chain_stage_map`
  - `dwd_industry_chain_info` 目录叶子：CHAIN 切片（李伟）
  - `M_SVC_GRAPH_112_1` / `113_1` / `M_SVC_BASE_101_1`：仍留后续（非本批 MODEL）
- `M_SVC_DEEP_177_1`：调研/策划**无专用 dwd**，细稿只写资讯关键词代理 → sidecar 挂 `ENT-P1-2`，记「等唐绍祖入参清单」，不新开题。
- 新开 SVC 题 6 条：`SVC-P1-3`…`P1-8`。旧题补现象：`SVC-P0-2` 写入待办 ∩ 圈定 0；`SVC-P1-1`/`P1-2`/`P0-1` 加挂 MODEL。
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| SVC-P0-2 | `employees_number` | 待办：全库 452 ∩ 圈定 0；`org_size`≠人数四档 | 正式列、空值、年主键、为何对不上圈定 |
| SVC-P1-3 | `pure_profit` | 同表营收 ∩ 圈定 0；上市 `yysr` ∩ 圈定 0 | 净利润列是否交付 |
| SVC-P1-4 | `total_assets` / `total_liabilities` | 待办 `zyywsr` ∩ 圈定 12 | 年报财务是否有资产/负债列 |
| SVC-P1-5 | `dwd_org_recruit_info` | 细稿入参；本叶未探行数 | 表、JOIN、样例 3 行 |
| SVC-P1-6 | `dwd_org_subsidiary_info` | 引入推荐深圳连接；投资/股东不是本问 | 两端 org_id、样例 |
| SVC-P1-7 | 失信 / 处罚 | 金融技术力反向入参 | 两表是否交付 |
| SVC-P1-8 | `dwd_patent_transfer` | 科创技术力转移日 | 表、pn、受让人码 |

- 声明：草案口径标「随口径修订」。监管人 `human:侯佳伟`。不问公式。
- sidecar：本批 upsert 18 条 MODEL（`as_of=2026-09-02`）。SVC 累计 38。

## 2026-09-02（STAT/GRAPH 首批）

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
  - MODEL 18 条 + `M_SVC_GRAPH_112_1` / `113_1` / `M_SVC_BASE_101_1`：当时超出 cap，见上节 MODEL
  - 甲方 Q-SVC-001/008/010/004/009、Q-SVCCHAIN-01…08、Q062：不改写
  - 二次：候选名单若只派生自招引分，缺口跟 `M_SVC_REC_ATTRACT_SCORE`；本批 `REC_CANDIDATE_CNT` 只问成立日原料
- 跨维复用、不新开 SVC Q：见文首表（ENT-P0-1 / ENT-P0-2 / ENT-P2-1）
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| SVC-P0-1 | `dwd_org_heis_info` / 大类码 | 细稿要高校/院所/企业；STAT-21 三类 ∩ 主体表空则 0/0/N | 表名、JOIN 键、univ_type 枚举 |
| SVC-P0-2 | `employees_number` | STAT-21 年报缺人数曾内存造数；ENT 只问过研发人员列 | 从业人数正式列、空值、年主键 |
| SVC-P1-1 | 服务–服务边 | 细稿 `svc_relation_chain` 为演示边；投资/股东不是服务关系 | 两端稳定 org_id + relation_type 3 行 |
| SVC-P1-2 | `incorporation_date` | 新增只能用工商成立年；「首次开展服务」无列 | 空值；是否另有首次服务日 |

- 声明：草案口径标「随口径修订」。监管人 `human:侯佳伟` 开工本叶，现行表按拟改落盘。
- sidecar：首批 upsert 20 条（4 条挂 SVC-P0/P1；16 条 `q_id` 指向 ENT-P0-1 / ENT-P0-2 / ENT-P2-1）。

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id（如 SVC-P0-1） |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
