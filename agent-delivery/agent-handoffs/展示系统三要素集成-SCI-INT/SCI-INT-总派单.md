# SCI-INT · 总派单（厚包）

> 总控：[`SCI-INT-长任务总控.md`](./SCI-INT-长任务总控.md)（**未授权前不得建单开跑**）  
> 监管：`human:淮政玮` · 仓：`gkx-orchestration` `origin/dev` · 强度：`ponytail off`（分析叶，完整性优先）  
> 本文件 = 全部 36 叶的铁律、卡片 schema、逐叶范围与 DoD、`/goal` 头。薄派单条只引用本文件章节号。

---

## 1. 通用铁律（每叶 `/goal` 必带）

1. **只读业务仓**：可读 `repos/demo-*`、`repos/lumen-*` 定位现状，**禁止**改任何业务仓文件。  
2. **真源优先级**：SRS 叶（`bid-reference/srs/02-科技信息展示系统/…`）> 页面映射（`metrics/request/展示系统/pages/DS-*.yaml`）> 缺口表（`DS-ALGO-GAP-L01/L02.yaml`）> 久新清单（`metrics/request/九新-技术机构人才/JIUXIN-TECH-ORG-TALENT-L01.yaml`）> demo 代码。冲突写进卡片 `conflicts`，不自行裁决。  
3. **指标查询只走 MCP** `metric-registry`（`metric-get` / `metric-query`）；任务状态只走 MCP `task-registry`。  
4. **一叶一产物**：`产物/{task-id}.yaml`（卡片集，§2 schema）+ `{task-id}.md` handoff。不写别的叶的产物文件。  
5. **防漏**：A 段范围内每个 SRS 叶都要有卡片（非三要素也要，`dimension: NONE_3E`）；B 段范围内每个 metric_id 都要有卡片。handoff 附「范围内条数 / 已出卡数 / 差集」三个数，差集必须为 0。  
6. **诚实**：对端是否提供、字段是否存在，查不到就写 `unknown` + 开放项，**禁止**推测成已有。  
7. 调用链、图谱、D12 铁律见总控 §3；违反的设计方案不得写进卡片，只能写进 `risks`。

---

## 2. 集成项卡片 schema（唯一格式）

```yaml
# 产物/{task-id}.yaml
task_id: SCI-INT-A01
scope_count: 16          # 范围内 SRS 叶数或 metric 数
card_count: 16
gap: []                  # 差集，必须为空
cards:
  - int_id: INT-A-TECH-001        # INT-{A|B|C|D}-{TAL|TECH|ORG|X}-{nnn}；X=非三要素或跨要素
    layer: page|metric|data|test
    # —— 来源 ——
    srs: {excel_row: 4, seq: 1, path: "…/科技全域态势/地图操作/放大/缩小"}
    page_ref: DS-01-MAP            # DS 页面映射 id（A 段必填）
    dimension: [TECH, ORG]         # TAL|TECH|ORG|NONE_3E|OTHER
    # —— 依赖 ——
    dep_kind: [data, metric, algorithm, graph, service, push, export, write_back]
    metric_ids: [M_TECH_GRAPH_STRUCT]
    metric_domain_other: []        # 页面用到的 INNOV/SYNTH 等非三要素域指标
    algorithm_type: third_party    # 来自 MCP，不自填
    integration_pattern: IP-03     # B01 模式编号；B01 未出前填 TBD
    # —— 分工 ——
    ours: [frontend, java_facade]  # frontend|java_facade|python_internal|etl|graph_load
    counterpart: jiuxin            # jiuxin|gkx_mysql_raw|trsgraph|other:<名>|none
    delivery_form: API             # API|SQL|Python|table|file|none|unknown
    jiuxin_row_id: null            # 对上 JIUXIN 51 行之一
    # —— 调用链与契约草案 ——
    call_chain:
      fe_route: /situation/global   # lumen 路由；不存在写 null
      java: "GET /innov/v1/…"       # 草案，标 draft
      python: "POST /internal/…"
      downstream: "久新 API / ADS 表 / Nebula space"
    contract_draft:
      request: [region_code, time_range, domain_code, page, size]
      response_key_fields: [id, name, lat, lng, score]
      granularity: {time: month, geo: city}
      freshness: T+1               # realtime|T+1|weekly|offline
    # —— 现状与缺口 ——
    status:
      demo: "demo-ui-science src/pages/…（有/无/部分）"
      lumen: "lumen-ui-science-pc src/views/situation/…（有/无/部分）"
      d1_d4: {d1: draft, d4: mock}  # 来自 MCP
    gaps: ["…"]
    conflicts: []
    decision_needed: []            # 需甲方 / 久新拍板的问题（草案）
    structure_escalation: false
    risks: []
    test_points: ["契约：…", "降级：对端超时显示空态+角标"]
    confidence: high|medium|low
```

编号段：A 段 `INT-A-*`，B `INT-B-*`，C `INT-C-*`，D `INT-D-*`；每叶在自己段内从本叶分配的号段起编（§3 表「号段」列），避免并行冲突。

---

## 3. 叶表（建单字段直接取本表）

公共字段：`repo=gkx-orchestration` · `epic=E-SCI-INT` · `supervised_by=human:淮政玮` · `claim_type=coordinator_dispatch` · `lock_hours=24`。

| ID | 标题 | agent | task_type | 点 / 难度 | 估 token | depends_on | 号段 |
|----|------|-------|-----------|-----------|----------|------------|------|
| P00 | 底座：卡片模板 + 283 叶 / 93 指标基线清单 | coordinator-agent | chore | 3 / S | 60k | — | — |
| A01 | 科技全域态势（16） | product-agent | spike | 3 / M | 80k | P00 | 001–099 |
| A02 | 科学技术全景·展示（17） | product-agent | spike | 5 / M | 100k | P00 | 100–199 |
| A03 | 科学技术全景·维护（14，含图谱写回） | product-agent | spike | 5 / L | 100k | P00 | 200–299 |
| A04 | 技术发展跟踪（8） | product-agent | spike | 2 / S | 60k | P00 | 300–399 |
| A05 | 全球创新监测·成果与实时数据（17） | product-agent | spike | 5 / M | 100k | P00 | 400–499 |
| A06 | 全球创新监测·载体排行 / 监测分析 / 城市（16） | product-agent | spike | 5 / M | 100k | P00 | 500–599 |
| A07 | 湾区创新监测（23） | product-agent | spike | 5 / M | 110k | P00 | 600–699 |
| A08 | 深圳创新监测（24） | product-agent | spike | 5 / M | 110k | P00 | 700–799 |
| A09 | 科技创新评估（23） | product-agent | spike | 5 / M | 110k | P00 | 800–899 |
| A10 | 科技指数（19） | product-agent | spike | 3 / M | 90k | P00 | 900–999 |
| A11 | 科技发展规划（19） | product-agent | spike | 3 / M | 90k | P00 | 1000–1099 |
| A12 | 全球领域人才态势（23） | product-agent | spike | 5 / M | 110k | P00 | 1100–1199 |
| A13 | 关注地区人才态势（11） | product-agent | spike | 3 / S | 70k | P00 | 1200–1299 |
| A14 | 重点科技人才画像（28） | product-agent | spike | 5 / L | 120k | P00 | 1300–1399 |
| A15 | 人才引进推荐评估（25） | product-agent | spike | 5 / L | 120k | P00 | 1400–1499 |
| B01 | 指标分层集成架构 + 按类型集成模式总则 | architect-agent | definition | 8 / L | 120k | P00 | 001–099 |
| B02 | 人才·深度模型 156–165（10） | algorithm-agent | spike | 5 / M | 100k | B01 | 100–199 |
| B03 | 人才·基础 / 图谱 / 页面派生（15） | algorithm-agent | spike | 5 / M | 100k | B01 | 200–299 |
| B04 | 人才·引进评估 DS-16（6）+ 结构统计（1） | algorithm-agent | spike | 3 / M | 80k | B01 | 300–399 |
| B05 | 技术·深度模型 130–140（11） | algorithm-agent | spike | 5 / M | 100k | B01 | 400–499 |
| B06 | 技术·基础 / 图谱 / 路径派生（12） | algorithm-agent | spike | 5 / M | 100k | B01 | 500–599 |
| B07 | 技术·MODEL 3 + STAT 4 + 评估热度类 9（16） | algorithm-agent | spike | 5 / M | 110k | B01 | 600–699 |
| B08 | 机构·深度模型 149–155（7） | algorithm-agent | spike | 3 / M | 80k | B01 | 700–799 |
| B09 | 机构·基础 / 图谱 / 派生 / 统计（15） | algorithm-agent | spike | 5 / M | 100k | B01 | 800–899 |
| C01 | 人才·三方源入站盘点 | data-agent | spike | 5 / M | 110k | P00 | 001–099 |
| C02 | 技术链·三方源入站盘点 | data-agent | spike | 5 / M | 110k | P00 | 100–199 |
| C03 | 科研机构·三方源入站盘点 | data-agent | spike | 5 / M | 110k | P00 | 200–299 |
| C04 | 图谱数据集成（TRSGraph 三要素 tag/edge、灌入、更新） | data-agent | spike | 5 / L | 120k | C01 C02 C03 | 300–399 |
| C05 | ADS / ES / 地理维表 / 对端结果回流 | data-agent | spike | 5 / L | 120k | C04 | 400–499 |
| D01 | 集成测试策略与环境（对端 Mock、契约测试、环境） | qa-agent | spike | 3 / M | 80k | P00 | 001–099 |
| D02 | 契约测试用例集（页面 × 对端接口） | qa-agent | spike | 5 / L | 120k | A01–A15 B02–B09 D01 | 100–399 |
| D03 | 数据对账 + 就绪度升级（mock→live）验收标准 | qa-agent | spike | 5 / M | 100k | B02–B09 C05 D01 | 400–599 |
| D04 | 端到端链路 + 非功能（超时降级、trace、性能） | qa-agent | spike | 5 / M | 100k | A01–A15 C05 D01 | 600–799 |
| Z01 | 汇总：集成依赖总表 + 久新接口需求说明 + 决策 / 风险 | architect-agent | definition | 8 / L | 200k | A* B* C* D* | — |
| Z02 | 架构评审会签 | architect-agent | definition | 3 / M | 60k | Z01 | — |

合计 36 叶，估 ≈ 3.6M token。

---

## 4. 逐叶范围与 DoD

> 每叶 DoD 都隐含 §1 铁律 + handoff（含 `ponytail: N/A`、cost 四字段、架构合规自检）。下面只写本叶特有项。

### P00 底座
- 输入：SRS 两个目录全部 `.md`；MCP `metric-query` domain=人才/技术/机构。
- 产出：`产物/P00-baseline.yaml`：283 行 SRS 叶（excel_row / seq / path / 归属叶 A01–A15）+ 93 行指标（metric_id / algorithm_type / 归属叶 B02–B09）+ JIUXIN 51 行 row_id 清单；`产物/_card-template.yaml`（§2 原样）。
- DoD：SRS 计数 196 + 87；指标计数 32 + 39 + 22；每行恰好归属一个叶；自检脚本放 `产物/_work/P00-check.py`（assert 计数和唯一归属）。

### A 段通用
- 输入：`SCI-INT-架构级初稿.md` §1 本页行（起点，须逐条复核）、本叶 SRS 文件（含需规功能描述原文）、对应 `DS-*.yaml`、`DS-ALGO-GAP-L01/L02.yaml`、JIUXIN yaml；现状对照 `repos/demo-ui-science`（定位对应页）与 `repos/lumen-ui-science-pc/src/views/situation|innov`、`src/api/*`；Java 侧对照 `repos/lumen-svc-platform/gkxlumen-innov`、`gkxlumen-metrics`。
- 每个 SRS 叶一张卡；一个 SRS 叶若依赖多个对端能力，拆成多张卡（同 `srs.excel_row`）。
- DoD：差集 0；三要素卡 `call_chain` 四段齐全（允许 `draft`）；页面上出现的统计数字都挂 `metric_ids` 或标 `metric_missing`；INNOV / SYNTH 等域指标写进 `metric_domain_other`；页面级交互（地图、筛选、导出、订阅、推送、报告生成）判断是否需要后台服务并写 `dep_kind`。

| 叶 | SRS 文件 · excel_rows | DS 页面映射 | 本叶额外关注 |
|----|----------------------|-------------|--------------|
| A01 | `科技全域态势.md` · 4–19 | DS-01-MAP / LAYERS / FACTORS / EVENTS | 图层数据源配置、要素搜索、事件重要性分级是否算法 |
| A02 | `科学技术全景.md` · 20–36 | DS-02-TECHGRAPH / ENTITY / PATH | 图结构生成、关键路径算法归属（久新 vs 我方 Python + Nebula） |
| A03 | `科学技术全景.md` · 37–50 | DS-02-MAINTAIN-GRAPH / MAINTAIN-ENTITY | **写回链路**：谁持有图谱主数据、版本控制落在哪、与久新同步方式；默认 `structure_escalation` 候选 |
| A04 | `技术发展跟踪.md` · 51–58 | DS-03-RESULT / WORKFLOW | 评估工作流参数配置是否需对端开放参数 |
| A05 | `全球创新监测.md` · 59–75 | DS-04-ACHIEVE-OVERVIEW / ACHIEVE-DETAIL / REALTIME | 「实时」的真实时效、知识图谱落图、实体影响赋分 |
| A06 | `全球创新监测.md` · 76–91 | DS-04-CARRIER-RANK / MONITOR / CITY | 载体＝机构的口径；订阅 / 智能推送的服务归属 |
| A07 | `湾区创新监测.md` · 92–114 | DS-05-GBA-ACHIEVE / CAPACITY / ANALYSIS / INDICATOR | SWOT 与报告生成是否大模型能力 |
| A08 | `深圳创新监测.md` · 115–138 | DS-06-CARRIER / INDICATOR / DOMAIN / CITY | 多层级地理（市 / 区 / 街道）维表 |
| A09 | `科技创新评估.md` · 139–161 | DS-07-SCI-CREATE / TECH-INNOV / INDUSTRY-POTENTIAL / POLICY-GUARD | 政策保障力多为 `NONE_3E`，仍出卡 |
| A10 | `科技指数.md` · 162–180 | DS-08-INDICATOR / VIZ / RANK | 专家 H 指数 / 活跃度 = TAL；排行历史快照存储 |
| A11 | `科技发展规划.md` · 181–199 | DS-09-COMPREHENSIVE / KEY-DOMAIN / RESEARCH | 人才流动监控、资源推送、竞争情报报告 |
| A12 | `全球领域人才态势.md` · 246–268 | DS-13-TALENT-GLOBAL | 华人占比、迁徙图的数据来源 |
| A13 | `关注地区人才态势.md` · 269–279 | DS-14-TALENT-REGION | 中国 / 深圳两级地图、报告导出 |
| A14 | `重点科技人才画像.md` · 280–307 | DS-15-TALENT-PROFILE | 隐私保护、基础信息校验更新（写回）、合作网络图谱 |
| A15 | `人才引进推荐评估.md` · 308–332 | DS-16-TALENT-RECRUIT | 6 条 missing 指标不向久新要假 API；成本模型数据采集来源 |

### B01 指标分层集成架构总则
- 输入：`SCI-INT-架构级初稿.md` §2（起点，须逐条复核）、`architecture-baseline.md`、`data-lineage-policy.md`、`给人说明-指标与算法工作类型与流程梳理.md`、JIUXIN handoff、`lumen-svc-platform/gkxlumen-metrics` 现状、`lumen-algo-py` 现有 `/internal` 结构。
- 产出：分层图（前端 ⓘ / 角标 → `/metrics/v1/catalog` → Java 业务门面 → Python `/internal` → 对端 / ADS / Nebula）+ 集成模式表 `IP-01…IP-nn`，至少覆盖：
  - STAT：ADS 预聚合，Java 只读；
  - COMPUTE：Python 计算，结果入 ADS 或同步返回；
  - MODEL：Python 模型服务，同步 / 异步 Job 判据；
  - GRAPH：Python + Nebula；
  - third_party × 交付形态三种：久新交 SQL → ETL / ADS；交 Python → 并入 `lumen-algo-py`；交 API → Python 适配层封装（鉴权、限流、超时、缓存、熔断），Java 只调 Python；
  - 结果快照、版本、`metric_id` 与 8 件套挂接、Mock 切换开关。
- DoD：每个模式写清 责任层 / 时效 / 失败降级 / 可观测埋点 / 测试要点；93 指标的初始模式映射表（B02–B09 细化）。

### B02–B09 通用
- 输入：B01、MCP `metric-get`（逐条取 8 件套 + D1–D4 + srs_refs）、JIUXIN yaml、对应 SRS `05-深度挖掘算法` 库叶、A2 专题 yaml（`TOPIC-TECH/ORG/TALENT-05.yaml`）作对照。
- 每个 metric_id 一张卡：模式编号、对端 / 交付形态 / JIUXIN 行、输入数据（表 / 字段 / 图谱）、输出（结构、粒度）、调用方式（同步 / 异步 Job）、被哪些页面用（来自 srs_refs + A 段卡片，A 未出时先按 srs_refs）、缺口。
- DoD：差集 0；`algorithm_type` 与 MCP 一致，若认为 type 不对写进 `conflicts`，不改。

| 叶 | metric_id 清单 |
|----|----------------|
| B02 | `M_TALENT_DEEP_156_1` … `M_TALENT_DEEP_165_1` |
| B03 | `M_TALENT_BASE_98_1` `GRAPH_110_1` `GRAPH_111_1` `ACADEMIC_SCORE` `ATTRACT_SCORE` `CULTIVATE_SCORE` `INDUSTRY_SCORE` `FLOW_TRACK` `ORG_DIST` `REGIONAL_DIST` `RELATION_NET` `SUPPLY_STRUCT` `SZ_STATUS` `SZ_SUPPLY_DEMAND` `UNIV_NEW`（前缀均 `M_TALENT_`） |
| B04 | `M_TALENT_DS_16_TALENT_RECRUIT_005/006/007/010/013/025` · `M_TALENT_STRUCT_QUERY` |
| B05 | `M_TECH_DEEP_130_1` … `M_TECH_DEEP_140_1` |
| B06 | `M_TECH_BASE_96_1` `GRAPH_104_1` `GRAPH_105_1` `EDGE_STRENGTH` `ENTITY_INFLUENCE` `ENTITY_REL` `ENTITY_TOP5` `GRAPH_STRUCT` `PATH_CENTRALITY` `PATH_KEYNODE` `PATH_PRIORITY` `REL_STRENGTH`（前缀 `M_TECH_`） |
| B07 | `M_TECH_DS_07_TECH_INNOV_002/004/006` · `HEAT_QUERY` `INVEST_AMOUNT` `OUTPUT_SCALE` `PAPER_PATENT_CNT` · `COMPOSITE_SCORE` `CONVERT_BOTTLENECK` `HEAT_INDEX` `LIFE_STAGE` `MATURITY_LEVEL` `POTENTIAL_SCORE` `STAGE_JUDGE` `SZ_ASSESS` `TOPIC_HEAT`（前缀 `M_TECH_`） |
| B08 | `M_ORG_DEEP_149_1` … `M_ORG_DEEP_155_1` |
| B09 | `M_ORG_BASE_99_1` `GRAPH_114_1` `GRAPH_115_1` `ATTENTION_TREND` `ATTRACT_SCORE` `COLLAB_CHAIN` `CULTIVATE_SCORE` `INDUSTRY_COVER` `NEW_TREND` `PERF_QUERY` `SZ_ADVANTAGE` `SZ_PAINPOINT` `SZ_STATUS` `TECH_LAYOUT` `TECH_SCORE`（前缀 `M_ORG_`） |

### C01–C03 三方源入站盘点（按要素）
- 输入：`data/third-party-source/`（`gkx-mysql-raw` 连接与供应方约束、`question/` 已出题）、`data/data-design/`、`data/ddl/`、`data/GDF/`、B 段指标卡里的 `source_tables`（MCP）；在途任务 `DATA-SUPPLIER-Q-TALENT-L01` 的产物只引用不改。
- 每张源表 / 源实体一张卡：源系统、表、关键字段、主键 / 实体对齐键（人名消歧、机构名归一）、覆盖范围（全球 / 中国 / 深圳）、更新频率、行数（可引用最近快照，不连库）、缺口、对应指标与页面。
- DoD：三要素各自的「实体主数据」来源结论（谁是人才 / 机构 / 技术点的主数据）；ID 对齐方案草案；未知项进开放项。只读，不跑写库操作；连库查询只允许只读且写明 SQL。

### C04 图谱数据集成
- TRSGraph 中三要素相关 tag / edge 现状 vs 页面与指标需要（技术点图谱、关键路径、人才关系链、科研合作链）；灌入链路（谁写、频率、增量 / 全量）；与 A03 / A14 写回需求的冲突点。
- DoD：所需 tag / edge 清单 + 现有 / 缺失标记；新增项全部 `structure_escalation: true`。

### C05 标准层 / 维表 / 回流
- ADS 标准表、ES 索引（`lumen-etl-es-py`）需求清单；全球 / 湾区 / 深圳地理维表与领域分类维表；久新模型结果回流落库位置与快照版本。
- DoD：每张需要的 ADS 表 / 索引一张卡（字段草案、来源、刷新）；新表全部 `structure_escalation: true`。

### D01 测试策略与环境
- 契约测试方式（对端 Mock 服务、录制回放、契约文件归属）、环境（dev / 联调 / 对端测试环境）、测试数据（Demo 库 `demo_gkxlumenx_*`，禁正式库）、准入准出。
- DoD：策略文档 + 每种集成模式（B01 IP 编号）的必测项模板。

### D02 契约测试用例集
- 来源：A 段 + B 段卡片里每个对端接口。每接口至少：正常、空数据、字段缺失、超时降级、鉴权失败五类中的适用项。
- DoD：每个 `counterpart != none` 的卡片至少 1 条契约用例 + 1 条降级用例。

### D03 数据对账与就绪度升级标准
- 每条指标从 `mock` → `ingesting` → `live` 的验收口径：对账方法（抽样、总量、区域分布）、容差、证据格式；与 `data-lineage-policy.md` D1–D4 对齐。
- DoD：93 指标逐条有对账方法；无法对账的写原因。

### D04 端到端与非功能
- 按页面挑关键链路（每页 ≥ 1 条），定义前端 → Java → Python → 对端的 trace 校验点、超时预算、降级表现（空态 + 角标）、性能目标（草案，标待确认）。
- DoD：9 页面 + 4 人才子页每页 ≥ 1 条端到端用例。

### Z01 汇总
- 合并全部 `产物/*.yaml` → `产物/SCI-INT-集成依赖总表.xlsx` + `.yaml`；分 sheet：页面 / 指标 / 数据 / 测试 / 对端接口需求 / 决策项草案 / 风险 / 结构升级项 / 跨域指标（`metric_domain_other`）。
- 校验：总控 §5 六条判据逐条出数。
- 对久新接口需求说明：`产物/SCI-INT-久新接口需求说明.md`（按 JIUXIN 行号组织，只写需求，不写成已确认）。
- DoD：§5 判据全绿；脚本 `产物/_work/Z01-merge.py` 带 assert（差集、编号唯一、模式编号合法）。

### Z02 架构会签
- 按铁律 §2 逐条审 Z01（调用链、Nebula、D12、可观测、算法只在 Python）；结构升级项给李伟的清单。
- DoD：会签记录 + 打回项（若有）开修单。

---

## 5. `/goal` 头（复制后补本叶 ID）

```text
/goal SCI-INT-{ID}
强度：ponytail off（分析叶，完整性优先，不写业务代码）
仓：gkx-orchestration · 分支 origin/dev · 只读 repos/*
监管：human:淮政玮 · claim_type=coordinator_dispatch · lock_hours=24
必读：agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-长任务总控.md
      agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-总派单.md §1 §2 §4「{ID}」
产出：产物/SCI-INT-{ID}.yaml（§2 schema）+ SCI-INT-{ID}.md handoff（范围数 / 卡片数 / 差集、ponytail、cost 四字段、架构合规）
完成：task-update-fields evidence + note 后转 integration；不点 done
```
