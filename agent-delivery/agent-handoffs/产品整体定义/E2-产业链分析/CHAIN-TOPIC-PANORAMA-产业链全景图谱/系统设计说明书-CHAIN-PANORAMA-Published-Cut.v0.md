# 系统设计说明书 · 产业链全景「发布切面」V1

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.2.1-draft |
| 日期 | 2026-08-16 |
| 状态 | **提交架构评审**（非正式基线冻结；会签前不得当生产 OpenAPI） |
| 范围 | ① 产业全要素图谱能力面 + API 服务（算法 Bid `.2` / `.2.15`）；② 专题全景页对其中「链结构切面」的消费（当前状态 / 状态对比 / 演进时间轴） |
| 一句话 | **全要素图谱是底座（DWD 账本 + 亿集查图 + 五类 API）；全景演进是底座上的发布切面（边上裁切 → 冻整图 → 只播刻度）** |
| 产品锚点 | `US-CHAIN-PANORAMA-02/03/04`；IA / UX-SPEC / Wireframe |
| 招标真源 | 算法库 `1.1.1.1.1.1.1.2` 产业全要素图谱、`.2.15` API 服务、`.3.1` 产业链全景模型；系统方案 `1.1.1.2.4.5.3` 全要素图谱管理（运营，本页不承接） |
| 架构锚点 | `DEC-CHAIN-PANORAMA-STATUS-COMPARE-20260812`；DWD v5；ADS v2；`graph-engine.md`；`designs/houtai-arch-discussion.md` 第五轮 |
| 缺口 | `GAP-CHAIN-PANORAMA-SNAPSHOT-API` / `Q062` |
| 工程范式 | 时间层（DWD 边/主体账本）× 在线图谱（亿集查图 API / 物理库见 Q5）× 发布切面（ADS 整图包）× 专题时间轴 |
| 不是 | 轨迹引擎；把全景页做成全要素图谱中台或亿集管理台；前端直连图库；CMS 发展历程；门户全景演进 |
| 合作方材料 | `designs/亿集知识图谱/`：**另一项目合作方**提供的引擎概要，**不是**本项目招标真源，也不是可复制的运行时 |

**会签对象**：架构师 `human:李伟` · 架构 Lead `human:徐滕强` · 数据 Lead · 体验 `human:高颖` · 算法 `human:唐绍祖` · PM `human:郭万迎`

---

## 0. 架构评审封面（必读）

### 0.1 建议决议

**通过本文作为 V1 实现真源**：全要素图谱 API 分面 + 全景发布切面算法（§5）+ 包契约。下列项须在会签栏勾选（见 §16）：

| ID | 待决 | 本文推荐 |
| --- | --- | --- |
| CUT-D1 | 业务「开始分析」是否允许 INSERT 新 published 包 | **正式环境：否。** 只选用已有刻度。Demo Job N3 可写 `demo_*`，不升正式库 |
| CUT-D2 | 画布：DEC 双图 vs 单画布叠加 | **V1 单画布叠加** |
| CUT-D3 | 回溯截至时节点属性语义 | **禁止宣称节点 as-of 正确** |
| CUT-D4 | 招标五类图谱 API 与全景切面 API 是否分面 | **分面。** 可视化 API = 返回图 JSON，前端渲染，不出图文件 |
| CUT-D5 | V1 切面是否必须带七要素主体 | **企业集合必带**（`entity_rel` as-of）；其余要素 V1 可空诚实，不编造 |
| CUT-D6 | 股权/合作/社交等跨类型关系是否进切面 | **不进。** 只走 A 面当前图；业务态不得标成「截至 T」 |
| CUT-D7 | 亿集引擎与本页切面的关系 | **能力平面，不是切面真源。** A 面经查图 API；B 面只裁项目 DWD；推理必须回写 DWD |

### 0.2 铁律自检（实现必须保持）

| # | 检查项 | 本文设计 |
| --- | --- | --- |
| 1 | 算法只在 Python | 本仓：裁切、diff、布局、查图适配、相似度/指标。抽取/融合/推理脚本在**亿集**执行（对方 Python）。Java 无 NER/nGQL |
| 2 | 调用链 | 前端 → 网关 `/chain/**` → `gkxlumen-topic-chain` → Feign Python `/internal/v1/chain/**` |
| 3 | 图谱引擎 | 在线 A 面：Python → **亿集查图 API**（物理库=Nebula 或亿集自管，见 houtai **Q5**，应用不感知）。**禁止** Java/前端直连；**历史对比/播放禁止从 live 图导出（B 面）** |
| 4 | 可观测 | 全链路 `traceparent`；包内带 `snapshot_id` |
| 5 | CI/CD | 设计类本稿；实现叶随各仓 pipeline |
| 6 | D12 | lumen 不打 demo 服务；Demo 写库仅 `demo_gkxlumenx_ads` |
| 7 | 方案 A | 走 `gkxlumen-topic-chain`，不另造前端直连 Python |
| 8 | ADS | Python 写发布包；Java 只读（现网经 Feign，不扫 DWD） |
| 9 | D8/D10 | 控件/图例/时间轴位置以 Wireframe + UX-SPEC 为准，不另造工具栏 |

### 0.3 读者

| 读者 | 必读 |
| --- | --- |
| 架构 / Tech Lead | §0～§3、§1.6、§8.0、§15～§16 |
| 数据 Lead | §1.5、§1.6、§3～§5、§7、附录 A / C |
| Python | §5～§8、§10、§12 |
| Java | §8、§10、§12 |
| 前端 | §4、§8.0 B 面、§9 |
| QA | §4、§9、§13、附录 B |

---

## 1. 目的与问题

### 1.1 业务问题

政府决策人员要在同一 `chain_id` 上：

1. 看一个已发布的「数据截至」整图（当前状态）
2. 核对两个截至之间的结构变化（状态对比）
3. 沿已发布截至序列播放（演进时间轴）

产品文案禁用「快照」：用 **数据截至 / 当前状态 / 状态对比 / 基准时间 / 对比时间 / 演进时间轴**。底层字段仍用 `snapshot_id`。

### 1.2 工程约束（为何不能纯 as-of）

DWD v5：

| 对象 | 时间策略 | 后果 |
| --- | --- | --- |
| `industry_chain` / `industry_chain_node` | **SCD1 当前版** | 不能回放节点名、阶段、简介 |
| `industry_chain_node_rel` / `entity_rel` | `[valid_from, valid_to)` 账本 | **可以**按 T 裁边 |
| 布局坐标 | 不在 DWD | 对比必须冻在包里 |

因此 V1 **不做**「任意日历日切整图」，也 **不做** 轨迹引擎。只做：**发布时把当时能诚实裁出的整图冻成一个刻度。**

### 1.3 设计目标

| 目标 | 说明 |
| --- | --- |
| 时间层在账本 | 边/主体关系继续只在 DWD 演进；ADS 不建永久边表 |
| 切面在发布 | 每个刻度 = 不可变整图 JSON（节点属性 + 边 + 布局） |
| 播放只走刻度 | 时间轴刻度 = 该链 `publish_status=published` 的 `effective_at` 序列 |
| 前端不算正式 diff | 五类变化由服务端 `graph_diff` 给出 |
| 三套 snapshot 分家 | 图谱发布包 ≠ Job Input/Result ≠ CMS 历程 |

### 1.4 非目标（V1）

- 节点改 SCD2 / 任意日 as-of 整图
- 独立轨迹/补间物理引擎、实时推送
- 跨 `chain_id` 对比；产业全链路视图级切面
- 把状态对比做成 Analysis Job
- 技术替代（`tech_replace`）正式归类
- 已确认变化 KPI（`M_CHAIN_ENTERPRISE_NEW_COUNT` 不替代 diff 证据）
- 门户全景演进（已归专题，见门户 SCOPE DEC）
- 把「全要素图谱管理」运营台（实体生命周期编辑、图谱绘制工具）做进专题全景页
- 招标原文中的 SDK 对外、词云图、前端直连图库
- 社群发现 / 最短路径作为独立 API（概述有、`.2.15`(5) 未单列；V1 不交付，501）
- 深圳产业链另起第二套切面表/引擎（`.3.2` 用同一套切面 + `chain_id` 或企业地域过滤）
- 把股权、人物社交等跨类型关系冻进全景包，或在历史模式下当 as-of
- 把 `designs/亿集知识图谱/` 当招标条款或本仓可复制代码；把亿集建图工作流/管理 UI 嵌进专题全景页
- 从亿集（或 Nebula）**当前图**导出当作历史切面；亿集脚本直连供应方 `gkx` 绕过项目 DWD

### 1.5 招标对照（源需求 / 本轮决策 / 待确认）

算法库把「产业全要素图谱」写成**能力底座**，不是单页。全景页只消费其中「以产业链为主线的结构 + 挂接主体 + 可视化」。

| 源章节 | 原文要点 | 本轮决策（落在哪） | 待确认 |
| --- | --- | --- | --- |
| 算法 `.2` 总述 | 七类实体抽取融合；图库+推理；API 支撑检索/关系/语义/可视化/聚类 | 底座 = DWD 账本 + **亿集建图/查图**（GDF 触发）+ Python `/internal/graph/**`；**不**在全景页重做 14 路 NER | 推理规则集；houtai Q5 物理库 |
| `.2` 五大流程 | 环节定义 → 要素提取 → 消歧 → 知识推理 → 入库 | 环节定义=DWD 链/节点；提取/消歧=ETL/算法库叶子；推理写回 DWD rel（带 `valid_from`）；入库=Nebula 投影 + **发布切面** | 推理写回频率 |
| `.2.1`～`.2.14` | 七要素识别 + 关系抽取 | **不在本稿实现**；产出必须进 DWD `entity_rel` / 各权威域，切面只读 | — |
| **`.2.15` API 五件套** | 实体检索、关系查询、可视化、语义相似度、网络指标 | 见 **§8.0**；全景页只用「可视化（图 JSON）」+ 关系/主体查询的链内子集 | 语义相似度模型版本 |
| `.2.15`(2) 举例 | 股权关系、人物社交 | **A 面当前图**；不进 B 面切面包（CUT-D6） | 权重字段是否展示 |
| `.2` 概述 | 节点重要性、社群发现、路径分析、聚类 | 重要性 ⊂ `.2.15`(5) 中心度；社群/路径/聚类 **V1 不单开**，未就绪 501 | 是否另叶 |
| 算法 `.3.1` 全景模型 | 上下游可视化；按环节查关系与主体；环节内属性统计；动态更新；Restful | 结构+主体 → 发布切面包；**环节统计走 ADS `metric_fact`（Java 只读，禁止前端从图包加总当正式 KPI）**；动态更新=账本变更后**再发布刻度** | CUT-D1 |
| 算法 `.3.1` 「可视化工具录入」 | 模板录入、维护上下游 | **运营台**（同系统 `.4.5.3`），不是专题全景页 | — |
| 算法 `.3.2` 深圳产业链 | 按地域筛出深圳全景 | **不另做切面引擎**。独立深圳链 = 另一 `chain_id`；同一链上的深圳主体 = 权威域地域过滤 | 产品选哪种 |
| 算法 `.3.3` 发展路线历程 | 重大事件时间线 | **CMS / 资讯事件**，≠ 图谱时间轴（已有门户 DEC） | — |
| 系统 `.4.5.3` 全要素图谱管理 | 七类实体状态与时间线、关系演化、绘制/导出；面向图谱工程师 | **运营台**（admin）；给账本提供人工补录/状态标记；**不是**专题全景页 | 运营台 Epic 未排 |

分层口诀：

```text
.2 / .2.15     全要素图谱底座（实体+关系+五类 API）
.3.1 / .3.2    全景 / 深圳全景（同一套切面，不另起引擎）
专题全景页      选用已发布切面做可视化与演进
.4.5.3         运营台维护账本（本页不接）
亿集引擎        合作方能力平面：建图/融合/查图；不是切面账本
```

### 1.6 合作方参考 · 亿集知识图谱（非招标真源）

路径：`agent-delivery/designs/亿集知识图谱/亿级知识图谱引擎平台 概要设计.md`。  
**性质**：另一项目上的合作方材料（会议纪要级概要），**不能**替代 `bid-reference/`，**不能**当本仓实现说明书。已有架构讨论：`designs/houtai-arch-discussion.md` **第五轮**（GDF 编排面 vs 亿集能力面）。

四平面（与全景切面对齐，不另造第五套）：

| 平面 | 谁 | 本页怎么用 |
| --- | --- | --- |
| 编排 | GDF | 调亿集 Schema/建图任务；**不**直写图库 |
| 表 | 项目 ODS/DWD | **切面唯一裁切真源**（`node_rel` / `entity_rel` 账本） |
| 图谱能力 | **亿集**（合作方引擎） | 建图：实体/事实/推理脚本在对方平台执行；用图：A 面经 Python 调**查图 API** |
| 在线服务 | Java + Python `/internal` | 前端永不直连亿集管理面；查询凭证 ≠ 管理凭证（houtai Q9） |

从纪要**可对齐、不可照搬**的点：

| 亿集说法 | 本稿落地 | 明确不抄 |
| --- | --- | --- |
| 建图 / 用图 分家 | 建图=GDF→亿集；用图 A 面=查图 API；全景演进=B 面切面 | 不把建图工作流做进专题页 |
| 实体 / 关系 / 推理 独立脚本 | 对应招标 `.2.1`～`.2.14` + 推理；脚本在**亿集侧**执行 | 不在本仓重做一套脚本运行时 |
| 事实边 vs 推理边 | 事实读 DWD；推理回写 DWD（`valid_from`=推理日）后再进下一刻度 | 禁止只写入亿集当前图、账本没有 |
| 定时 / 事件更新 | 更新的是**当前图**；全景时间轴仍要**再发布刻度** | 禁止把「亿集刷新」当成播放帧 |
| 查图：关键词、子图、过滤；大结果指针化 | A 面可走查图 API；大图返回指针/诚实截断 | B 面链图必须整包，禁止只给指针 |
| 禁 NL2SQL 直查图库 | 与调用链铁律一致 | — |
| 社群发现、相似专家网络 | 属亿集平台算法；A 面 V1 未就绪 **501**（CUT-D4 已收） | 不因纪要有就在全景页做 |
| Schema 全员可见、按单位隔离空间 | 租户对齐网关后再开（houtai Q6） | 不进全景 V1 |
| 内置实体不可改 / 可自定义图谱 | 对方产品（纪要写 Scikim） | 本项目七要素 Schema 以招标+DWD 为准 |
| 物理图库 | **houtai Q5 未决**（亿集自管 vs Nebula） | 应用只认查图 API；`source` 对外可报 `yiji` |

**硬约束（CUT-D7）**：推理、融合、属性更新只要要进全景演进，**必须先落项目 DWD 账本**。亿集图 = 当前投影。`publish_cut` **只读 DWD**，禁止 `EXPORT` 亿集/Nebula 当前图当 `graph_snapshot`。

---

## 2. 概念模型

```text
【底座 · 产业全要素图谱】
  七要素实体（权威域 + DWD 挂接）
  链内上下游 node_rel + 链/节点↔主体 entity_rel   ← 时间账本（切面真源）
  知识推理：亿集执行 → **回写 DWD rel**（valid_from=推理日）
  当前投影：亿集图存储（Q5）← GDF 触发建图；应用不直连
  五类平台 API：Python 调亿集查图 API + 本仓指标/相似度

【切面 · 全景发布】
  指定 chain_id + T
  裁 DWD node_rel + entity_rel(as-of T) + 冻节点属性 + 布局
  → ADS graph_snapshot / graph_diff
  禁止从亿集当前图导出

【消费】
  专题全景页：只读切面（当前/对比/时间轴）
  深度分析 Job：按需调 A 面「当前图」关系与指标
  运营台 / 亿集管理面：写 Schema 与建图任务，不写 ADS 切面
```

| 名词 | 定义 | 业务文案 |
| --- | --- | --- |
| 时间层 | DWD 关系半开区间账本 | 不出现 |
| 发布切面 / 刻度 | 一次发布写入的不可变整图包 | 数据截至 = `effective_at` |
| `snapshot_id` | 包主键 | 仅服务字段 / ReviewMode |
| `layout_baseline_id` | 坐标对齐代 | 不出现 |
| 专题时间轴 | 已发布刻度的播放头 | 演进时间轴 |
| Job Snapshot | 生成分析输入/结果冻品 | 与本稿无关 |
| CMS 历程 | 门户发展阶段叙事 | 不等于图谱演进 |
| 平台 API | `.2.15` 五类，默认打 **当前** 亿集查图 / DWD | 内部字段 |
| 切面 API | 已发布包的目录/整图/diff | 数据截至 / 对比 / 时间轴 |

**口诀**：底座管七要素与在线查询；账本记变化；发布出刻度；时间轴只拨刻度。

---

## 3. 分层职责

```text
DWD                          ADS                         在线引擎
链/节点 SCD1 当前版            graph_snapshot 目录+整图包    亿集当前图（查图 API）
边/主体 rel 有效期账本         graph_diff 五类事件          禁止当历史真源
                             禁止永久边表
```

| 层 | 存什么 | 不存什么 |
| --- | --- | --- |
| DWD 链/节点 | 当前属性 | 多版历史整图 |
| DWD `node_rel` / `entity_rel` | 带有效期的关系 | 布局、五类 diff 结论 |
| ADS `graph_snapshot` | `snapshot_id`、`effective_at`、整图 JSON/ref | 可写第二边真源 |
| ADS `graph_diff` | 两刻度间变化 + `confirm_status` | 前端伪造的变化数 |
| 亿集图存储 | 当前投影（Q5：自管或 Nebula） | 历史对比、切面账本 |
| CMS | 发展历程正文 | 图谱节点/边 |

表结构真源：

- DWD：`data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md`
- ADS：`data-design/产业链/产业链-ADS表设计-原型与Handoff驱动(v2).md` §5.9 / §5.10
- 存储入口：`data-design/storage/CHAIN/stores/mysql/ads.md`

五大流程落点（算法 `.2`）：

| 流程 | 落点 | V1 |
| --- | --- | --- |
| （1）环节与上下游定义 | DWD `industry_chain` / `node` / `node_rel` | 已有结构 |
| （2）要素与属性提取 | 各权威域 + `entity_rel`；全景只读挂接 | 企业必挂；其余可空 |
| （3）实体构建与消歧 | GDF 触发 → **亿集**实体脚本；产出进权威域 / DWD | **不在全景实现叶** |
| （4）知识推理 | 亿集推理脚本 → **必须回写** DWD rel（新 `valid_from`） | 可空；有则下一次发布进入切面 |
| （5）图谱入库 | 亿集当前投影 + ADS 发布切面 | 切面=历史入口；亿集图≠历史真源 |

本稿 **不改表清单**，冻结：底座 API 分面、裁切算法、包 JSON、全景读口与播放语义。

---

## 4. 产品行为（实现必须对齐）

### 4.1 三种模式

| 模式 | 控件 | 读什么 |
| --- | --- | --- |
| 当前状态（默认） | 查看时间 Select | 一个 published 包；默认最新 |
| 状态对比 | 基准时间 / 对比时间 | 两包 + `diffs?base=&compare=` |
| 演进时间轴 | 图谱下方播放/暂停/步进 | 该链 published 序列，指针停在 `snapshot_id` |

顶栏「数据截至」与工作区时间下拉 **同源**：选项 = 该 `chain_id` 的 published `effective_at` 列表（新在上）。不得用浏览器当前日期冒充。

### 4.2 顶栏 Job vs 演进读模型

| 动作 | 正式 V1（CUT-D1 推荐） | Demo as-built（例外） |
| --- | --- | --- |
| 默认进页 | SYNC 读最新 published，不建 task | 同左 |
| 改产业/链/截至后「开始分析」 | `chain:panorama:graph` **选用**已有包；无包则失败诚实空，**不 INSERT** | Job N3 可向 `demo_gkxlumenx_ads` INSERT |
| 状态对比 / 时间轴 | 同步 GET，不开 Job | 同左 |

**禁止**把 Job Input/Result Snapshot 与 `graph_snapshot` 混表。七键分析字段不得写入全景包。

### 4.3 交互硬约束（摘自 USM/UX）

- 只比较同一 `chain_id`；schema / `layout_baseline_id` 不兼容 → 禁止对比，保留最近有效单状态
- 无证据不得标已确认变化；V1 全部 `pending`（待补证）合法
- 无已确认变化 → 结构仍在，文案「该范围无已确认变化」，禁止伪变化 KPI
- 时间轴仅图谱下方，与图谱共占首屏剩余高度，间距 16px
- `prefers-reduced-motion`：禁止连续补间，只步进
- 进结构列表：停播、回当前状态、隐藏演进控件/图例/详情变化标识
- 换对象前先停播
- 某刻度无当前节点 → 「该快照中不存在」，不自动换节点
- 业务态不得出现「快照 / schema 版本」；Q062 浮层仅 ReviewMode
- 图例色：新增绿、退出红、关系变化蓝、主体变化紫、技术替代橙；必须有中文，不能只靠颜色
- 工具栏复用 `SharedMapChrome`，左上；图例左下单列

---

## 5. 发布切面算法（V1 核心）

执行方：**仅 Python**。触发方见 CUT-D1。一次发布 = 一次切面，失败不写库。

### 5.1 输入

| 字段 | 约束 |
| --- | --- |
| `chain_id` | 必填；L1 链；禁止 L0 产业当切面对象 |
| `effective_at`（T） | 必填；业务截至；**包内自描述，禁止下拉 2024-06、实际按发布夜裁切** |
| `source_release_id` | 作业号 |
| `schema_version` | V1 固定 `panorama.graph.cut.v1` |

### 5.2 边与主体裁切（真 as-of）

对 `industry_chain_node_rel` **以及** `industry_chain_entity_rel`（CUT-D5：企业必裁；其余 `entity_type` 有则裁、无则空）：

```text
alive_at(T) ⇔
  chain_id = ?
  AND valid_from <= T
  AND (valid_to IS NULL OR valid_to > T)
  AND is_deleted = 0
```

半开区间与 DWD v5 §7.2.10 一致。墓碑行（`is_deleted=1`）不进入切面。

结构键：

```text
edge_key = (chain_id, source_node_id, target_node_id, relation_type)
```

同一 `edge_key` 在 T 存活多行 → 发布失败（`CUT_OVERLAP`），不写包。

`entity_rel` 防重键按 DWD：`(chain_id, node_scope_key, entity_type, entity_id, relation_type)`。V1 包内只物化 **业务键 + 类型 + 关系类型**，不复制企业画像全文（权威域另查）。无法解析的 `entity_id` 不进包、不提供「查看企业」。

### 5.3 节点集合（属性非 as-of）

```text
node_ids =
    { 边裁切结果的 source ∪ target }
  ∪ { industry_chain_node 中 chain_id=? AND is_deleted=0 的当前节点 }
```

属性一律读 SCD1 **当前行**（含已删但仍被历史边引用的最后一行）。  
**CUT-D3**：包内节点属性语义 = `generated_at` 时刻的当前版，不是 T。ReviewMode 在 `generated_at.date != effective_at.date` 时必须可见「节点属性为发布时当前版」。BusinessMode 不展示该内部说明。

V1 **禁止**为了补历史刻度而用今天的节点属性回填，并在业务态宣称「这是 T 日节点」。补历史只能：当时已发布的包，或等节点 SCD2。

### 5.4 布局继承（空间稳定）

1. 取该链上一 `published` 且未 `deprecated` 的包为 `prev`
2. 若 `prev.layout_baseline_id` 存在：
   - 旧 `node_id`：**复制** `prev` 坐标，禁止重算打乱
   - 新节点：按 `stage_code` 落入上/中/下游列，在列内追加，不移动旧点
   - 继承成功 → **沿用** `layout_baseline_id`
3. 无法继承（首包、阶段体系变更、人工强制重排）→ 生成新 `layout_baseline_id`，全图确定性分层布局
4. 新基线包 **不得** 与旧基线包对比/串播（API 返回 `LAYOUT_INCOMPATIBLE`）

V1 坐标确定性：同一输入多次发布，旧点坐标必须字节级稳定（继承路径）。

### 5.5 写入

1. `snapshot_id` 新生成（建议 `snap:{chain_id}:{yyyyMMdd}:{shortid}`）
2. `generated_at = now()`
3. `publish_status = published`
4. 同链同 `effective_at` 再发：旧包 `deprecated`，新 `snapshot_id`（DEC R5）
5. 不同 `effective_at` 并存，供时间轴
6. payload：**整图 JSON**（§7）；小图可内嵌 `payload_json`，大图 `payload_ref`；**禁止只存 ID 回查当前节点**
7. 预计算与 **时间序上一 published**（按 `effective_at` 升序的前驱，不看 deprecated）的 diff，写入 `graph_diff`
8. 失败整单回滚；亿集/Nebula 读失败 **不挡** 发布（fail-soft；切面不依赖 live 图）

### 5.6 明确不做

| 项 | 原因 |
| --- | --- |
| 按 T 回查节点史 | 无 SCD2 |
| 发布时从 Nebula/亿集 导出当历史 | 在线库会被后续建图覆盖 |
| 轨迹插值生成中间帧 | 无刻度即无图 |
| 用户播放时现场裁 DWD | 节点会穿帮；且 Java 不扫 DWD |
| 用 A 面 live view 驱动时间轴 | 当前图会被后续投影覆盖，历史穿帮 |
| 亿集脚本直连供应方 `gkx` | 失去贴源验收；houtai Q1 |

---

## 6. Diff 算法（服务端）

输入：两包 payload（已冻），不是 live DWD。

| `change_type` | 判定 | V1 |
| --- | --- | --- |
| `node_add` | `node_id` 在 compare 有、base 无 | 做 |
| `node_exit` | base 有、compare 无 | 做 |
| `edge_change` | 同 `edge_key` 属性变化，或边对称差（可拆 `edge_add`/`edge_exit` 进 `detail_json`，对外仍可归本类） | 做 |
| `entity_change` | 两包 `entities[]` 对称差（V1 以 enterprise 为准） | **做** |
| `tech_replace` | 无结构字段 | **禁止输出** |
| 名称微调 / `sort_no` | — | 不进五类；可进详情 |

`confirm_status`：无 `evidence_refs` → 必须 `pending`。V1 允许全 pending。  
`confirmed` 仅在证据规则闭合后由后续任务打开。

非相邻刻度：

- 优先提示选用相邻 published（避免「大跃进」）
- 仍请求则 **现场算** 一次，可写临时 diff 或只返回不落库（实现选一，API 对前端透明）
- 禁止 O(N²) 预计算全部配对

前端禁止把本地对称差当正式结论；本地高亮只能映射服务端事件。

---

## 7. 整图包 JSON（`panorama.graph.cut.v1`）

```json
{
  "schema_version": "panorama.graph.cut.v1",
  "snapshot_id": "snap:INB130301:20260731:ab12",
  "industry_id": "INB1303",
  "chain_id": "INB130301",
  "effective_at": "2026-07-31T23:59:59+08:00",
  "generated_at": "2026-08-01T02:10:00+08:00",
  "source_release_id": "rel_20260801_01",
  "layout_baseline_id": "lay:INB130301:v3",
  "node_attr_as_of": "generated_at",
  "stages": [
    { "stage_code": "upstream", "stage_name": "上游", "sort_no": 1 }
  ],
  "nodes": [
    {
      "node_id": "n_pkg",
      "node_name": "封装测试",
      "stage_code": "midstream",
      "node_type": "process",
      "status": "active",
      "description": "…",
      "sort_no": 2,
      "x": 420,
      "y": 180,
      "entities": [
        {
          "entity_type": "enterprise",
          "entity_id": "ent_…",
          "relation_type": "belongs_to",
          "relation_id": "chain-entity-rel:…"
        }
      ]
    }
  ],
  "edges": [
    {
      "relation_id": "node-rel:…",
      "source_node_id": "n_wafer",
      "target_node_id": "n_pkg",
      "relation_type": "supply",
      "relation_direction": "forward",
      "evidence_refs": []
    }
  ]
}
```

| 规则 | 说明 |
| --- | --- |
| 节点必含 `x,y` | 无坐标视为包非法，拒绝发布 |
| `node_attr_as_of` | V1 恒为 `generated_at` |
| `entities` | CUT-D5：`enterprise` 必有数组（可空列表=该环节无企业，诚实）；`institution`/`talent`/`technology`/`policy`/`service_institution` V1 可缺省为 `[]` |
| 禁止字段 | `high_end_index` / `bottleneck_score` / `is_key_node` / `cycle_stage` 等七键结论 |
| 断点 | 结构缺口用边标记（如 `relation_type=breakpoint` 或 `detail`），前端红虚线 +「断点」文本；不得用「瓶颈关注」标签替代 |

现网 SYNC 薄包（仅 `id/name/description` + `source/target/type`）**不合格**。实现叶必须升到本契约；升包期间 API `honesty.payload_thin=true`，演进模式禁用或降级为单状态。

---

## 8. API 服务（招标 `.2.15` + 全景切面）

调用链不变：前端 → 网关 `/chain/**` → `gkxlumen-topic-chain` → Feign Python `/internal/*`。  
**禁止**前端/Java 直连 Nebula；**禁止**把 SDK 作为 V1 交付物（招标「SDK」收口为 Java REST）。  
招标原文「词云图」不进专题全景页（±10% 内不扩）。

### 8.0 分面（CUT-D4）

| 面 | 对应招标 | 数据面 | 谁用 |
| --- | --- | --- | --- |
| **A. 平台 API（当前图）** | `.2.15`（1）（2）（4）（5）及（3）的 live 形态 | DWD 当前有效 rel + **亿集查图 API** | 检索、深度分析 Job、运营预览 |
| **B. 切面 API（已发布）** | `.2.15`（3）可视化在全景页的历史形态；`.3.1` 全景输出 | ADS `graph_snapshot` / `diff` | 专题全景当前/对比/时间轴 |

A 面默认 `as_of` 省略 = 当前。V1 **不**对 A 面做任意日 as-of（节点 SCD1）。历史可视化只走 B 面。

#### A 面 · 产业全要素图谱 API（`.2.15` 逐条）

路径前缀建议（服务内）：`/topic/v1/industry/graph/**` → Python `/internal/v1/chain/graph/**`。与现网 `/panorama/snapshot` 并存，不互相替代。

| 招标项 | 能力 | V1 契约方向 | 算法位置 | 全景页是否调用 |
| --- | --- | --- | --- | --- |
| （1）实体检索 | 关键词/名称查实体；分页排序 | `GET .../graph/entities?q=&type=&page=&size=&sort=` 打权威域/ADS 目录，**不是**切面包内全文检索 | Python；禁 Java NER | 否（对象 Select 走 catalog） |
| （2）实体关系查询 | 跨类型关系；方向与权重；原文举例含股权、社交 | `GET .../graph/relations?from_id=&to_id=&types=&direction=` Python 调 **亿集查图**（当前子图）；DWD 当前有效 rel 可作事实边校对。`weight` 只读，**禁止回写**。股权/社交 **不进** B 面（CUT-D6） | Python 适配亿集；禁 Java nGQL | 详情「上下游」优先用 **B 面包内边**；跨类型探索才用 A（当前，非 as-of） |
| （3）图谱可视化 | 关系图、词云 | **只返回 nodes/edges JSON**。Live：`GET .../graph/view` 经查图 API（无布局冻结）。历史：B 面。**禁止嵌亿集前端**（houtai Q7：专题自绘） | Python 组装 | **历史/对比/播放只用 B** |
| （4）语义相似度 | 两实体相似度；深度学习模型 | `POST .../graph/similarity {a, b}`；模型须 `cfg_model_registry`；响应带 `model_id`/`version`；无模型 → **501** + honesty，禁止假分 | Python 深度模型 | 否 |
| （5）网络指标 | 密度、中心度 | `GET .../graph/metrics?chain_id=&kinds=density,centrality`；中心度可写 ADS `metric_fact`。社群/相似专家若仅亿集有、未注册本仓 → **501** | Python 或代理亿集（须 `cfg_model_registry`） | 全景页不把中心度当演进图例 |

A 面错误：无图谱 → 诚实空；无权不返回邻居摘要。`source`：`yiji|nebula|pg|error`（对接亿集时报 `yiji`；底层是否 Nebula 见 Q5，不透出给前端业务态）。

招标「知识扩充 / 智能交互」**不**单开开放式 Agent。扩充 = 推理写回 DWD 后下次发布；交互 = 已有检索/问答走 Job/RAG 叶，不塞进全景切面。

#### B 面 · 全景切面 API（现网扩展）

网关前缀与现网一致。Java **原样透传** Python JSON，不扫 DWD，不签发 Job `result_snapshot_id`。

### 8.1 路径

**B 面（全景切面）**

| 语义 | Java（服务内） | Python |
| --- | --- | --- |
| 秒开当前包（已有） | `GET /topic/v1/industry/panorama/snapshot` | `GET /internal/v1/chain/sync/snapshot` |
| 刻度目录 | `GET /topic/v1/industry/panorama/snapshots` | `GET /internal/v1/chain/sync/snapshots` |
| 按 ID 取整图 | `GET /topic/v1/industry/panorama/graphs/{snapshotId}` | `GET /internal/v1/chain/sync/graphs/{snapshotId}` |
| 两刻度 diff | `GET /topic/v1/industry/panorama/diffs` | `GET /internal/v1/chain/sync/diffs` |
| 节点详情 | `GET /topic/v1/industry/panorama/nodes/{nodeId}` | `GET /internal/v1/chain/sync/node-detail` |

**A 面（平台 · `.2.15`，V1 可分叶）**

| 招标 | Java（服务内） | Python |
| --- | --- | --- |
| （1）实体检索 | `GET /topic/v1/industry/graph/entities` | `GET /internal/v1/chain/graph/entities` |
| （2）关系查询 | `GET /topic/v1/industry/graph/relations` | `GET /internal/v1/chain/graph/relations` |
| （3）live 可视化 JSON | `GET /topic/v1/industry/graph/view` | `GET /internal/v1/chain/graph/view` |
| （4）语义相似度 | `POST /topic/v1/industry/graph/similarity` | `POST /internal/v1/chain/graph/similarity` |
| （5）网络指标 | `GET /topic/v1/industry/graph/metrics` | `GET /internal/v1/chain/graph/metrics` |

查询参数同时接受 camelCase / snake_case。A 面未就绪时返回 501 + honesty，**禁止**用切面包冒充 live 检索。

### 8.1.1 A 面响应骨架（评审用，非正式 OpenAPI）

```text
GET  .../graph/entities?q=&type=&page=&size=&sort=
  200 { items:[{entity_id, entity_type, name}], total, honesty }

GET  .../graph/relations?from_id=&to_id=&types=&direction=
  200 { nodes, edges:[{relation_type, direction, weight?}], source: yiji|nebula|pg|error }

GET  .../graph/view?chain_id=
  200 { nodes, edges }          # 无 x,y 冻结承诺；禁止驱动时间轴

POST .../graph/similarity
  body { a:{id|name}, b:{id|name} }
  200 { score, model_id, model_version } | 501

GET  .../graph/metrics?chain_id=&kinds=density,centrality
  200 { density?, centrality:[{id, degree?, pagerank?}], source }
  kinds 含 community|path → 501
```

详情若同时打开 B 面切面与 A 面股权/社交：A 面结果必须带 `as_of: "current"`；BusinessMode 不显示该字段，也不得写成「该截至下的股权」。

### 8.2 目录 `GET .../snapshots?chain_id=`

只返回 `publish_status=published` AND `is_deleted=0`，按 `effective_at` **降序**。

```json
{
  "chain_id": "INB130301",
  "items": [
    {
      "snapshot_id": "snap:INB130301:20260731:ab12",
      "effective_at": "2026-07-31T23:59:59+08:00",
      "layout_baseline_id": "lay:INB130301:v3",
      "schema_version": "panorama.graph.cut.v1",
      "is_current": true
    }
  ]
}
```

`is_current` = 该链最新 published。空列表 → 诚实空，不 200 造假图。

### 8.3 整图 `GET .../graphs/{snapshotId}`

返回 §7 包。鉴权失败不返回节点摘要。Deprecated 包默认 404；ReviewMode 可加 `include_deprecated=1`。

### 8.4 Diff `GET .../diffs?base=&compare=`

| 条件 | 行为 |
| --- | --- |
| 缺参 / 跨 chain | 400 |
| 任一侧非 published | 404 |
| `layout_baseline_id` 不同 | 409 `LAYOUT_INCOMPATIBLE`；body 不含伪事件 |
| 有预计算 | 直接读 `graph_diff` |
| 无预计算 | Python 现场算；可提示 `adjacent_recommended` |

```json
{
  "base_snapshot_id": "snap:…:20260131:…",
  "compare_snapshot_id": "snap:…:20260731:…",
  "layout_baseline_id": "lay:INB130301:v3",
  "adjacent": true,
  "changes": [
    {
      "diff_id": "d1",
      "change_type": "node_add",
      "subject_type": "node",
      "subject_id": "n_new",
      "confirm_status": "pending",
      "evidence_refs": []
    }
  ]
}
```

`changes=[]` 且两边结构合法 → 前端 Info「该范围无已确认变化」（V1 全 pending 时用「无已确认变化」仍然成立）。

### 8.5 节点详情

绑定 `chain_id + node_id + snapshot_id`。旧响应不得覆盖新选择（校验三元组）。对比态可附 `base_snapshot_id`，详情给前后摘要；缺节点返回 `missing_in_snapshot=true`。

---

## 9. 前端落地

仓：`lumen-ui-topic`（专题正式仓；对照 demo 只读不 merge）。

### 9.1 状态

`snapshotMode ∈ {current, compare, timeline}`  
`baseSnapshot` / `compareSnapshot` / `playheadSnapshot`  
`playback ∈ {idle, playing, paused}`

进页：拉目录 → 默认 current=最新 → `GET graphs/{id}`。  
对比：校验基线 → 并行 graphs×2 + diffs。  
时间轴：目录升序为刻度；播放头切换只换 `graphs/{id}`，并用 **相邻** diff 着色（第 0 帧无 diff）。

### 9.2 播放

| 项 | V1 |
| --- | --- |
| 间隔 | 1000ms（可配置 800–1200） |
| 预取 | 播放头 ±2 个包 + 相邻 diff |
| 基线不同 | 硬切，不 tween |
| 基线相同 | 允许透明度变化；reduced-motion 则硬切 |
| 停播 | 改产业/链、开始分析、进结构列表、卸载页 |

禁止把播放描述为实时流。

### 9.3 叠加绘制

单画布：compare 包坐标落点 + diff 着色。  
宽度 < 1100px **仍单画布**（叠加不依赖并排）。DEC「双图画布」不作为 V1 必做（CUT-D2）。

---

## 10. 时序

### 10.1 发布（Python 写 ADS）

```text
Ops/Demo Job
  → Python cut(chain_id, T)
  → 读 DWD node_rel + entity_rel as-of T；节点 SCD1 当前版
  → 挂接 entities（企业必有数组）
  → 继承布局
  → INSERT graph_snapshot + 相邻 graph_diff（含 entity_change）
  → 失败回滚
```

正式环境推荐独立发布作业（数据工厂 / 管理端），不绑普通用户「开始分析」。

### 10.2 状态对比（读）

```text
FE → GW /chain/topic/v1/industry/panorama/snapshots?chain_id=
FE → 用户选基准/对比
FE → GW .../graphs/{base} 与 .../graphs/{compare}
FE → GW .../diffs?base=&compare=
Java Feign Python（只读 ADS 包）
FE 叠加绘制；详情带 snapshot_id
```

### 10.3 时间轴

```text
FE 拉 snapshots 升序
playhead=i → graphs[items[i]] + diffs(items[i-1], items[i])
播放 i++ 直至末帧
```

---

## 11. 与现网 as-built 的差距（评审时对齐排期）

| 能力 | 现网 | 本稿 V1 |
| --- | --- | --- |
| 秒开最新包 | SYNC + Java `.../panorama/snapshot` | 保留 |
| 刻度目录 / 按 ID 取图 / diffs | **无** | **必补** |
| Job 改条件写 published | Demo N3 可写 `demo_*` | 正式 CUT-D1=只读选用 |
| payload 含布局 | Job 声称整图；SYNC 仍薄 | 必须 §7，薄包禁用演进 |
| `graph_diff` | 发布时相邻预计算；SYNC 曾 0 条 | 对比/播放依赖非空或现场算 |
| 时间轴 UI | 产品有、工程未接这 3 个读口 | 接目录+播放头 |
| `.2.15` 五类平台 API | 无独立 `/graph/**` 分面 | A 面按 §8.0 分叶；相似度无模型 501 |
| 切面包企业集合 | SYNC 薄包无 entities | CUT-D5 必带 enterprise 数组 |

实现拆单建议（不自动建 registry）：① B 面 Python 读口 → Java 三路由 → 前端三模式；② 发布作业正式化；③ A 面五 API 按招标 `.2.15` 另叶（可与 ent-analysis 中心度复用，禁止在 Java 算）。

---

## 12. 可观测与诚实性

- 所有读写带 `traceparent` / `X-Trace-Id`
- 读空：`honesty.published=false`，`snapshot=null`，HTTP 仍 200（与现网秒开一致）或 404（按 ID）；**禁止** 200 假图
- D9：本页不把 diff 条数当统计指标宿主；`M_CHAIN_MARKET_SIZE` 继续 Q056 空值
- Mock 包 `source_system/mock` 或 ReviewMode 可见；BusinessMode 不出现 schema 字样
- 包非法（无坐标、七键污染）→ 发布失败；已写入的薄包读时 `honesty.payload_thin=true`

---

## 13. 验收（DoD）

### 13.1 数据

- [ ] 演示链 ≥ 2 个 published 包，同 `layout_baseline_id`，payload 含 `x,y`
- [ ] 边裁切可用 DWD 账本解释（抽检 1 条 `valid_to` 闭区间边，T 之后包中应消失）
- [ ] 同 `effective_at` 再发：旧 deprecated，新 id
- [ ] 包内节点含 `entities` 数组；企业 `entity_id` 可解析或诚实不进包
- [ ] Job Result 表与 `graph_snapshot` 无混写

### 13.2 API

- [ ] B 面目录只含 published
- [ ] 跨链 / 基线不兼容 → 不返回伪 diff
- [ ] `tech_replace` 零输出
- [ ] 无证据事件均为 pending
- [ ] A 面与 B 面路径分面；live `graph/view` 不得被拿去播时间轴
- [ ] 相似度无注册模型 → 501 + honesty，无假分
- [ ] 网络指标计算在 Python（或经注册代理亿集）；响应可含 `source: yiji|nebula|pg|error`
- [ ] `kinds=community|path` 或词云请求 → 501，无假图
- [ ] 切面包 `edges` 不含股权/社交等跨类型边（CUT-D6）
- [ ] 发布作业不 `EXPORT` 亿集/Nebula 当前图（CUT-D7）

### 13.3 产品

- [ ] 三模式可切换；时间轴在图谱下且首屏内
- [ ] 播放/暂停/步进；reduced-motion 无补间
- [ ] 结构列表退出演进
- [ ] BusinessMode 无「快照」字样、无 Q062 DOM
- [ ] 五类图例中文+色；技术替代可图例在、事件空

### 13.4 架构

- [ ] 前端不直连 Python/Nebula/亿集管理 API/DB
- [ ] lumen 调用链无 demo 服务
- [ ] 历史模式零 live 查图 / 零 live nGQL
- [ ] 正式库无业务用户 INSERT published（CUT-D1 若通过）
- [ ] A 面 live 与 B 面历史分路径，时间轴零 live 图
- [ ] 推理边若进切面，DWD 账本可解释（CUT-D7）

---

## 14. 阶段

| 阶段 | 内容 |
| --- | --- |
| **V1（本稿）** | 底座 A/B 分面；A 面经亿集查图 API；全景只消费 B 面刻度（裁 DWD）；整图包含布局+企业挂接 |
| **生产增强** | 发布与选用分离；相邻 diff 全预计算；证据闭合后 confirmed；payload 大图对象存储；A 面五 API 齐；推理写回进入后续刻度 |
| **时间层升级（另决策）** | 节点 SCD2 后，A 面才允许查询时 as-of；B 面可降为缓存；**全景交互与文案不变** |

---

## 15. 开放项（会签必须表态）

| ID | 内容 | Owner | 本文默认 |
| --- | --- | --- | --- |
| CUT-D1 | 正式「开始分析」可否写 published | 架构 + PM | 否 |
| CUT-D2 | 单画布叠加 vs 双图 | 体验 | 单画布 |
| CUT-D3 | 回溯截至的节点属性话术 | 数据 + 体验 | 不宣称节点 as-of |
| CUT-D4 | A/B API 分面；可视化是否只出 JSON | 架构 + 算法 | 分面；只出 JSON |
| CUT-D5 | 切面是否必带企业集合 | 数据 + 产品 | 企业必带，可空数组 |
| CUT-D6 | 股权/社交等是否进切面 | 架构 + 算法 | 不进；A 面当前图 |
| CUT-D7 | 亿集 vs DWD 切面 | 架构 + 数据 + 算法 | 亿集=能力平面；切面只裁 DWD；推理回写 DWD |
| OPEN-CHAIN-ADS-V2-04 | payload 内嵌阈值 vs 仅 MinIO | 数据 | V1 演示链内嵌 |
| Q062 | 证据规则何时允许 confirmed | 唐绍祖 + 徐滕强 | V1 全 pending |
| GAP 关闭 | OpenAPI 字段以本稿升正式 | 架构 | 会签后关 GAP 的「未冻」部分 |
| houtai Q5 | 亿集物理库 vs Nebula | 架构 | 应用只经查图 API，本稿不拍板 |

---

## 16. 会签栏

| 角色 | CUT-D1 | CUT-D2 | CUT-D3 | CUT-D4 | CUT-D5 | CUT-D6 | CUT-D7 | 总决议 | 签字 | 日期 | 意见 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 架构师 `human:李伟` | 是/否 | | | | | | | 通过 / 整改 | | | |
| 架构 Lead `human:徐滕强` | | | | | | | | | | | |
| 数据 Lead | | | | | | | | | | | |
| 体验 `human:高颖` | | | | | | | | | | | |
| 算法 `human:唐绍祖` | | | | | | | | | | | |
| PM `human:郭万迎` | | | | | | | | | | | |

总决议「通过」后：本稿升 `v1.0`；`GAP-CHAIN-PANORAMA-SNAPSHOT-API` 改为「契约已冻、待实现叶」；B 面按 §11 拆单，A 面 `.2.15` 另叶。**禁止**前端自算正式 diff，**禁止**轨迹引擎立项，**禁止**把运营台或亿集管理台画进专题全景页，**禁止**把股权/社交冻进切面冒充历史，**禁止**从亿集当前图导出切面。

---

## 17. 修订

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.2.1-draft | 2026-08-16 | 接入合作方亿集概要（另一项目材料，非招标）：CUT-D7 能力平面 vs DWD 切面；A 面经查图 API |
| v0.2-draft | 2026-08-16 | 对齐算法 Bid `.2` / `.2.15` / `.3.1` / `.3.2` 与系统 Bid `.4.5.3`：A/B 分面、五类 API、企业挂接、CUT-D6 跨类型关系不进切面 |
| v0.1-draft | 2026-08-16 | 首版：冻结「账本→发布切面→刻度播放」 |

---

## 附录 A · 裁切伪代码

```text
function publish_cut(chain_id, T, release_id):
  assert_not_l0(chain_id)
  edges = dwd.node_rel.alive_at(chain_id, T)   # never EXPORT yiji/nebula live graph
  ents  = dwd.entity_rel.alive_at(chain_id, T)  # V1: enterprise required; others optional
  assert unique edge_key(edges) else fail CUT_OVERLAP
  node_ids = nodes_of(edges) ∪ dwd.nodes.current(chain_id)
  nodes = [ scd1_attrs(n) + inherited_or_placed_xy(n) + attach(ents, n) for n in node_ids ]
  prev = latest_published(chain_id)
  layout_id = prev.layout_baseline_id if inherit_ok(prev, nodes) else new_layout_id()
  payload = pack(schema=v1, effective_at=T, generated_at=now, layout_id, nodes, edges)
  assert all nodes have x,y
  assert every node has entities array  # enterprise may be []
  assert no seven_key fields
  deprecate_same_effective_at(chain_id, T)
  insert snapshot(published, payload)
  if prev and prev.layout_baseline_id == layout_id:
    insert graph_diff(prev, new, compute_diff(prev.payload, payload))  # includes entity_change
  commit
```

## 附录 B · QA 最小脚本

1. 目录 ≥2 刻度，最新 `is_current=true`
2. 对比同基线：新增/退出有文本+色
3. 人为改 compare 为另一 `layout_baseline_id`（夹具）→ 409，画布不出现伪变化
4. 播放到末帧、暂停、步进；开结构列表后播放头重置
5. ReviewMode 开 Q062；关评审模式 DOM 无 `snapshot_id` / `GAP-` / `schema_version`
6. 断网后保留最近成功刻度时间，不标成「最新」
7. 时间轴请求不得打 `/graph/view`（A 面 live）
8. `POST .../graph/similarity` 无模型时 501，无假分
9. 切面包 `edges` 抽检无股权/社交类型
10. `GET .../graph/metrics?kinds=community` → 501

## 附录 C · 招标条款 → 接口/层（便于会签抽检）

| 招标 | 条款 | 本稿 |
| --- | --- | --- |
| `.2` | 七类实体知识网络 | DWD 挂接 + 权威域；切面只冻链上挂接 |
| `.2` 五大流程 | 定义/抽取/消歧/推理/入库 | §3 表；抽取叶子不在全景页 |
| `.2.15`(1) | 实体检索 API | A `GET .../graph/entities` |
| `.2.15`(2) | 关系查询 API | A `GET .../graph/relations`；全景结构边走 B 包 |
| `.2.15`(3) | 可视化 API | JSON 图；live=A `view`；历史=B `graphs/{id}` |
| `.2.15`(4) | 语义相似度 | A `POST .../graph/similarity`；无模型 501 |
| `.2.15`(5) | 网络密度/中心度 | A `GET .../graph/metrics`；Python 图算法 |
| `.2.15`(2) | 股权 / 社交 | A 面当前图；**不进**切面（CUT-D6） |
| `.2.15`(5) 外 | 社群发现 / 路径 / 聚类 | V1 501，不单开 |
| `.3.1` | 按环节查关系与主体 | B 包 `edges` + `entities` |
| `.3.1` | 环节内属性统计 | ADS `metric_fact`；禁止前端从图包加总 |
| `.3.1` | 可视化工具录入 | 运营台，不是本页 |
| `.3.2` | 深圳产业链 | 同一套切面；另一 `chain_id` 或地域过滤 |
| `.3.1` | 动态更新 | 账本变 → 再发布刻度，不是播放 live |
| `.3.1` | Restful / SDK | 仅 Java REST；无 V1 SDK |
| `.3.3` | 发展历程时间线 | CMS/资讯，≠ 本时间轴 |
| 系统 `.4.5.3` | 实体/关系生命周期、绘制导出 | 运营台；本页不接 |
| （合作方·非招标） | 亿集建图/用图/查图 API | §1.6；CUT-D7；物理库 houtai Q5 |
