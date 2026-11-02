# 时空热点强度值（M_SCIUI_INCUB_038）

> **类型**：需业务建模类（区域×时点热度量化评价 = 热度事实面 + 热度模型双层）｜ **域**：科技成果展示·创新载体孵化载体·科技时空演进展示·热点区域图层｜ **UI 挂载**：科技信息展示系统 → 科技时空演进 → 图层开关「热点强度」（`spaceTimeEvolutionMock.js:71` heat layer，渲染 `SpaceTimeEvolutionPage.jsx` showAreas=heat；KPI 邻挂 `:65` 热点区域 8 个）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（指标名三源 0 命中；INCUB 清单自注「计算方法需要立项调研后才能确定」）｜ **口径归属**：UI 挂载件（`_phase3_471_export.json` row_01=593），SRS 无同名指标（上位叶科技时空演进展示）
> **复现脚本**：`code/M_SCIUI_INCUB_038.py`（薄壳，指向共享探针 `code/_shared_s308_lane_a.py`）｜ **产物**：`code/M_SCIUI_INCUB_038_out.json`
> **四判定摘要**：直接结构 = 否（三源无区域热度结果面）；直接数据 = 否；依赖结构 = 缺（dev chain_hotspot 含 hotspot_score 列 0 行/innovation_event 含 heat_score 列 0 行双空壳）；依赖数据 = 否（久新 geo_yearly 为计数面无热度评分列）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 时空热点强度值需要两层材料：①**热度事实面**（区域×时点×热度值/等级）——dev heat 词族命中 2 表：`chain_hotspot`（13 列含 hotspot_score/is_hot/rank_overall）**0 行**（且为产业链域非时空区域域）、`industry_chain_graph_snapshot` 0 行；另有结构最贴合的时空事件热度预留面 `innovation_event`（20 列含 heat_score/importance_score/lng/lat/city_code）**0 行**空壳；gkx 280 表 heat 词族 **0 命中**；久新 218 表（SHOW TABLES 实数）无 heat/hotspot 词族，最近语义面 `ads_geo_yearly_metrics`（171,736 行）为论文/项目/机构/流动**计数**面无热度评分列。②**热度模型**（评分权重/分档阈值）——三份说明书无定义（INCUB 清单自注需立项调研）；UI 现行为 mock 等级分档（high/medium/watch）阈值亦自设。两层皆缺即无从建模。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（强度读数语义） |
| B4 | 负结论带探针 | absence_probe 四件（dev 词族/dev 事件面/gkx/久新） |
| B5 | 确定性 | 词族匹配为集合判定 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 断言式薄壳重跑产出 |
| B8 | 回执不复收 | 探针可复跑复验 |
| B9 | 单位/日期陷阱 | 单位「个」（KPI 计数）/等级（分档）；mock 时间片为标签 |
| B10 | 口径裁定保守交付 | 不挪用 mock 等级分档充数；久新计数面不强行代理 |
| B11 | 多本账互推 | 与 INCUB_050/051/052（路径强度族）同页面不同域独立留证 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有区域热度结果面吗？ | 无 | dev chain_hotspot/innovation_event 双 0 行空壳；gkx 0；久新无热度词族 |
| 热度模型有定义吗？ | 无 | 清单自注需立项；UI mock 分档阈值自设 |
| 计数面可代理吗？ | 不可 | geo_yearly 城市级计数≠区级热度强度值；模型无定义 |

## 摘要

「时空热点强度值」挂载科技时空演进展示页两处：①图层开关「热点强度」（`spaceTimeEvolutionMock.js:71`，{ key: heat, label: 热点强度, meta: 8 }——控制地图热区面渲染）；②KPI「热点区域」8 个（`:65`，聚合式=Σ level==high，`SpaceTimeEvolutionPage.jsx:656/661/691`）。UI 现行为**等级分档语义**：mock regionStats[].level 三档（high/medium/watch，南山 2022=medium→2024-2026=high）+ 年度 events 序列（118→386）——「强度值」以档位表达，连续分值在 UI 也未定义。数据侧判定：**完全不支持**——dev 双空壳（`chain_hotspot` 含 hotspot_score 列 0 行、`innovation_event` 含 heat_score 列 0 行）、gkx 0、久新无热度词族（geo_yearly 为计数面）。升档路径：热度模型立项 + 区域级计数面落库 → 完全转换支持。

- 需求判定：**UI 挂载件**（SRS 无同名；INCUB 清单 row_01=593）。
- 复现状态：负证据断言脚本已跑通（双空壳断言）。
- 档位结论：**完全不支持**（热度事实面与模型双层皆缺）。
- 关键事实：dev `innovation_event`（20 列含 heat_score/lng/lat）是最贴合本件的预留面——0 行空壳证设计意图在库。
- 升档路径：模型立项 + 区域计数面 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 科技时空演进展示。两处挂载：①**图层开关**——mock layers[1]（`spaceTimeEvolutionMock.js:71`，heat 层，meta=8）→ `SpaceTimeEvolutionPage.jsx` 地图 `showAreas=layers.heat`（热区面开关）；②**KPI 邻挂**——kpis[2]（`:65`，热点区域 8 个，trendLabel「3 个重点」），聚合逻辑 `buildRegionStatsTotals` 系（`:656/661` current/previous 双期、`:691` 当期）均 `level === "high" ? 1 : 0` 累加。等级分档数据源：mock regions[].regionStats（`:108-112` 南山 2022-2026 逐年 level + events/paths/activeObjects）。

mock 值全部为演示常量（8 个热点/3 个重点/年度序列 118→386），不参与支持度结论。

### 1.2 为什么需要本指标

热点强度回答「哪个区域在什么时候最活跃」：图层开关控制热区可视化，等级分档辅助管理者定位高热区域（3 个重点）。SRS 上位叶（科技时空演进展示）要求时空分布可视化——热点强度是热区渲染的量化依据。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「时空热点强度值」指标名未出现；INCUB 清单（row_01=593）自注「对某方面能力或状态的量化评价——计算方法需要立项调研后才能确定」；UI mock 用等级分档（阈值自设）非连续强度值。

### 1.4 类似指标权威方法可行性分析概要

热点强度在学术/官方体系的对应物：科技热点探测（文献计量突现检测 burst detection）、区域创新热度指数（专利/论文密度加权）、产业热点监测（新闻/投资事件热度）。方法族对照：

| 方法族 | 数据轴 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| 突现检测（Kleinberg burst） | 主题×时序词频 | 成果事实面+时序 | **近似有**（久新 geo/成果面可算计数）但无现成热度输出 |
| 区域创新热度指数（密度加权） | 区域×成果计数 | 区域级计数面 | **部分**（geo_yearly 城市级，区级缺） |
| 事件热度评分（dev 预留面） | 事件×热度分 | 事件热度表 | **无（innovation_event 0 行）** |

结论：无论哪种方法族，热度模型（权重/阈值）均需立项裁定且区域级事实面缺位；负结论件。完整版见附录 C。

### 1.5 引用来源

- mock：`repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:71` — heat 图层；`:65` — hotRegions KPI；`:108-112` — regionStats 分档。
- 组件：`repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:656/661/691` — Σhigh 聚合。
- dev 预留面：`gkxlumenx_ads.innovation_event`（20 列）/ `gkxlumenx_ads.chain_hotspot`（13 列）——快照列级留证。
- SRS：上位叶科技时空演进展示（`bid-reference/srs/02-科技信息展示系统/科技成果展示/`）。

### 1.6 推测原意与推测定义

**推测定义（负结论件，仅记录语义）**：$\text{heat}_{r,t} = g(\text{events}_{r,t}, \text{paths}_{r,t}, \text{objects}_{r,t})$，$g$ 为热度聚合模型（UI 现行为三档离散化 $L(\text{heat}) \in \{\text{high},\text{medium},\text{watch}\}$，阈值自设）。此式在本库**不可计算**（区域级事实面与模型 $g$ 双缺；久新 geo_yearly 城市级计数仅覆盖 $g$ 的一部分原料且区域粒度不符）。

**降档/升档触发器（B10 模板）**：热度模型立项（分档阈值/权重）+ 区域级计数面落库（geo_yearly 下钻区级或事件流落库）→ 完全转换支持；热点结果面直连（如第三方热点监测服务）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | 上位叶：科技时空演进展示 |
| 所属页面 | 科技时空演进展示 |
| 所属面板 | 地图图层开关（heat）+ KPI 区（hotRegions） |
| 本件叶 | 时空热点强度值（UI 挂载件 INCUB row_01=593） |
| 相邻叶 | INCUB_050/051/052（路径强度族，同页不同域）/ STE KPI 族（events/paths/activeObjects） |
| UI 容器 | 地图 + 右栏排行 + KPI 条 |

## 二、计算过程

**从缺。** 本件判「完全不支持」，不设伪公式（F4）；三源否定性证据入 §三与附录 B；§2.7 一句话说明薄壳行为。

### 2.7 复现代码结果展示（薄壳行为说明）

代码 `code/M_SCIUI_INCUB_038.py`：装载共享探针快照 `_shared_s308_lane_a_out.json` → 断言三源表数（542/280/218）与 dev `chain_hotspot`/`innovation_event` 双 0 行 + 关键列在（hotspot_score/heat_score）→ 落盘判档产物（负结论 derived null 登记）。断言通过（退出码 0）。对照需求功能要求（热点区域可视化与分档）：**不满足**，须待热度模型与区域事实面双落定。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 区域热度结果面（区域×时点×热度值/等级） | dev / gkx / jiuxin | — | — | **不存在** | **缺（主降档因）** |
| D2 | 时空事件热度预留面 | dev | `gkxlumenx_ads.innovation_event`（heat_score 列） | 0 行 | 结构在无数据 | 空壳（证设计意图） |
| D3 | 产业链热点面（证伪对象） | dev | `gkxlumenx_ads.chain_hotspot`（hotspot_score 列） | 0 行 | 空壳且域错位 | 代理不可用 |
| D4 | 热度模型（权重/分档阈值） | 文档侧 | — | — | **不存在** | 缺（清单自注需立项） |

`support_judgment="完全不支持"`，与文首一致（闸 6）。

### 3.2 D1 热度面三源探针（absence_probe 全记录）

否定性证据四件套：**查了什么**——heat/hotspot 词族表名扫描 + dev 预留面行数实证 + 久新语义核；**条件**——dev 542 表、gkx 280 表、久新 218 表（`SHOW TABLES` 现场实数）；**结果**——dev 命中 2 表（chain_hotspot 产业链域 0 行/graph_snapshot 0 行）、innovation_event 时空域预留面 0 行、gkx 0（`word_heat=[]`）、久新无热度词族（geo_yearly 计数面无热度评分列）。四缺失情形归属：**表不存在**（区域热度域无任何有效结构）。

### 3.3 D2/D3 空壳面证据

`innovation_event`（20 列：event_type/title/summary/event_time/importance_level/importance_score/heat_score/country_code/city_code/admin_code/lng/lat/orgs/persons/domains/source_refs 等）是 dev 的**时空事件热度预留面**——结构最贴合本件（事件×热度分×地理坐标），0 行空壳证设计意图在库。`chain_hotspot`（13 列含 news_freq_score/investment_score/enterprise_growth_score/hotspot_score/is_hot/rank_overall）为产业链热点评分面——域错位（链非区域）且 0 行。

### 3.4 久新计数面的代理证伪（B10）

久新 `ads_geo_yearly_metrics`（171,736 行，2000-2026）承载地理×年五计数（paper/project/institution/mobility_event/new_institution）——可作热度模型**原料**，但：①区域粒度为城市级（深圳=单点 loc_E16782C21F18EBF8A59C1E98F9C9860B），非 UI 区级（南山/宝安/坪山/光明）分档语义；②热度模型（计数→强度值的映射/权重）无定义；③连续强度值与 mock 三档的离散化阈值均未定。原料≠结果面——代理不可用，不构成部分支持。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| heat 词族探针 | dev 2 表（产业链域）/ gkx 0 / 久新无热度词族 |
| innovation_event | 0 行（20 列空壳，heat_score 列在） |
| chain_hotspot | 0 行（13 列空壳，hotspot_score 列在） |
| 久新 geo_yearly | 171,736 行计数面（城市级，无热度列）——代理证伪 |
| UI 分档链 | :108-112 regionStats level → :656/691 Σhigh 聚合 → :65 KPI/`:71` 图层 |
| 判档 | 完全不支持（产物 = 文首） |

## 四、数据缺失情况

### 4.1 区域热度事实面零承载（结构级，主因）

区域×时点热度值是时空分析引擎的输出（事件聚合+模型评分），三源无镜像：dev 预留面空壳、gkx/久新无热度词族。四缺失情形归属：**表不存在**。修复动作是**时空分析链路建设**（事件流落库+热度模型），库内无法构建。

### 4.2 热度模型连带缺失

等级分档阈值（high/medium/watch 的边界）与连续强度值的口径均无定义——INCUB 清单自注「需立项调研」。即使计数面下钻区级，模型裁定仍是前置事项。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 热度模型立项（分档阈值/权重） | 业务建模 | 本件 + 图层渲染 | 清单自注呼应 |
| 区域级计数面落库 | 数据工程 | 本件 + 区级排行 | geo 下钻或事件流 |
| innovation_event 灌数 | 数据工程 | 本件 | 预留面激活 |

档位后果：模型 + 区域面双落定 → 完全转换支持；热度结果面直连 → 完全直接支持；无动作 → 维持完全不支持。推荐：与路径强度族（050/051/052）合并推时空分析链路立项。

## 参考文献

不适用（负结论件，无可复现步骤；热点探测方法参照文献计量突现检测体系）。

# 附件

## 附录 A 原始需求原文摘录

「时空热点强度值」指标名在三份说明书未出现（INCUB 清单第 593 行提取自 UI mock 图层开关与 KPI）。清单语义注：「对某方面能力或状态的量化评价（科技企业孵化器运营监测平台场景）——计算方法需要立项调研后才能确定」。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 时空热点强度 / 热点强度值 | 主需求 / SRS | 0（指标名） |
| 热点强度 | UI 图层标签（`:71`） | 组件文案 |
| 热点区域 | UI KPI（`:65`） | 组件文案 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INCUB_038_out.json`（20261102 实跑）。
- 共享探针：`code/_snapshots/_shared_s308_lane_a_out.json`（S3-08 路 A 族级探针，dev 542 / gkx 280 / 久新 218 实数）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INCUB_038_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INCUB_038 | 文首 |
| `batch` | 标识 | S3-08 | 文首 |
| `ui_evidence` | 证据 | 3 条（图层/KPI/聚合） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3 |
| `facts.ui_level_semantics` | 语义登记 | 三档等级分档 + Σhigh 聚合 | §1.1 |
| `facts.dev_innovation_event_heat` | 空壳证据 | 20 列 0 行 | §3.3 |
| `facts.dev_chain_hotspot` | 空壳证据 | 13 列 0 行（域错位） | §3.3 |
| `derived[0]` | 负结论 | null 登记 | §二 |
| `absence_probe` | 负证据 | 四件 | §3.2 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |
| `notes` | 披露 | 代理证伪 + 模型缺 | §3.4 |
| `base_years_*` | 基期三键 | used=[] / missing=[2021-2026] / note | §〇 摘要 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 数据轴 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 突现检测 | 文献计量 | 主题×时序 | 无现成输出 | 中 |
| 区域热度指数 | 创新指数体系 | 区域×计数 | 城市级计数（区级缺） | 中 |
| 事件热度评分 | dev 预留面 | 事件×热度 | **空壳** | 最高（目标态） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 缺口 |
|---|---|---|
| 区域热度结果面 | 三源 0 表 | 时空分析链路（主因） |
| innovation_event | dev 20 列 0 行 | 空壳 |
| chain_hotspot | 0 行 | 产业链域错位 |
| 区域级计数 | 久新城市级 | 区级粒度缺 |
| 热度模型 | 无 | 立项事项 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 热度模型立项 + innovation_event 灌数 | 模型裁定 |
| v2 | 区级计数下钻 + 等级分档切真 | 区域面落库 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 分档阈值争议 | 中 | 模型立项 + 双口径 |
| 城市计数被误当区级热点 | 中 | 粒度披露 |

### C.5 总判

**完全不支持**：区域热度事实面与模型双层三源零承载（innovation_event 空壳留证设计意图）；久新计数面代理证伪（粒度+模型双缺）；升档路径为时空分析链路立项，触发器写死 §1.6。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INCUB_038.py` | 退出码 0（断言通过），落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_lane_a.py` | 快照三源表数 542/280/218 |
| 空壳复核 | `innovation_event` / `chain_hotspot` | 双 0 行 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| §二从缺纪律 | F4 | 本件 §二仅 §2.7 一句 |
