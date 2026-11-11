# WBS · 展示系统集成

> **2026-10-27 扩范围（本次变更）**：技术方案的范围口径改为「**展示系统全部目录菜单**」。本表随之从「九个对接菜单」扩为 **七模块 30 叶（DS-01～DS-30）+ 政策核增 PC-1～PC-4 + 维护管理（M10）**全覆盖，并把**展示系统相关的全部已提交任务**（含之前提交的技术架构设计类任务）归集进来逐叶可索引。每叶补「完成情况 · handoff」列，把对应 handoff 写回本表。
> **2026-10-22 梳理**。方案任务 `SYSINT-SCHEME-05-L01` 于 2026-10-23 由 `human:淮政玮` 签收后，同日改回处理中。菜单范围与调用方向以 [技术方案](./技术方案.md) 现稿为准。同日按已写明的人员姓名补建开发任务，任务号回写本表。WBS-05-09 监管人仍是待指定，未建任务。
> **2026-10-22 晚**：草稿已确认作建叶底稿。已有监管人即负责人。完成日期要求取倒排「功能开发」计划完成时间（11月倒排计划 · 科技信息展示系统）。页面计划里冲出该日的叶结束日不写入。开始时间仍待填写。这两列是我方栏位，不是对端承诺。方案行与菜单注册行在倒排里没有单独的功能开发完成日，仍为无截至时间。
> **2026-10-26 `human:淮政玮` 口径**：「展示系统本身就是集成，整体放到展示系统集成」。据此，展示系统的跨页公共物与技术架构设计件也归第 5 项，不再散落在原页面计划。
> **2026-10-27 `human:李伟` 建叶登记**：原以「挂接登记」记入的五件转为正式叶，任务号不变（沿用已有 ID，未新建）；原无监管人的 `BE-TS-IMPL-01`、`BE-TS-DATA-01` 由 `human:李伟` 认领。派单说明见 `agent-handoffs/科技发展态势-TS/派单说明/`。
> **2026-10-28 `human:李伟` 挂接**：创新监测三页（DS-04/05/06）数据打通长任务 `SITUATION-IM`（**23 叶**，WBS-05-19-01～23）挂接 **§4.4**，授权句已生效；边界口径：**可改接口契约，不可改 UI 与实现效果**（角标挂载点属评审层叠加，须满足总控 §0.1 三条）。总控 / 总派单 / 契约 / 前置条件四份：`agent-handoffs/科技发展态势-TS/SITUATION-IM-*.md`；决策纪要本夹 `纪要/2026-10-28-SITUATION-IM-边界与裁定.md`。
> **2026-11-03 收藏订阅与产业码过滤入库**：收藏订阅服务端化（`SITUATION-ENT-FOLLOW-SVR-L01`，05-18-16）22 个后端文件 + 5 表 DDL 已 commit+push（`lumen-svc-platform` `ad3afe9`，upms-api / upms-biz / display / element 四模块编译 EXIT=0），前端 3 文件同步入库（`lumen-ui-science-pc` `04ecf8c`）；同批带产业领域筛选 —— element `EnterpriseController` 8 端点支持 `industryId` 产业码过滤，已从 `WBS-02-13`（只出口径、不改业务仓）析出为独立实现叶 `WBS-02-14` · `SYSINT-INDDISC-02-L02`。
> **2026-11-03 影响力第 6 卡上线**：`SITUATION-ENT-INTEGRATION-STATUS-L01`（WBS-05-18-18）—— 影响力 Tab 新增「项目（含课题）」卡（算法库 `M_INNOV_PROJECT_INFLUENCE` 真实 precompute，58,453 项 / 均分 42.9），display 重打包并拉起 element/innov，同日出全端点对接进度总台账（10 端点 × 11 要素 × 566 指标实测）。
> **2026-11-03 挂接**：科技政策跟踪正式复刻单已在 registry。父行 `WBS-05-23` + 子行 §4.1b。同日补建真数链三张单，并补建存量调研 `POL-DISPLAY-SURVEY-L01`、系统详细设计 `POL-DISPLAY-SDD-L01`。编写顺序是调研 → 详设 → 契约。前后依赖见 [对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md)。专题 `E-E7-POLICY-M1-L06` 不作为展示前置。同日按 SRS level5 拆二级设计，见 §4.1c（7 个一级、26 个二级，每个二级 4 张定义单）。
> 本表列为「开始时间」时未标注的，均为**待填写**。不自行补日期。

---

## 0. 读本与口径

### 0.1 范围（2026-10-27 起）

展示系统**全部一级菜单与叶子页**都在本表有落点（见 §1 菜单全覆盖索引）。三种落点方式：

| 落点方式 | 用于 | 例 |
|---|---|---|
| **本项开发叶**（WBS-05-NN） | 智树做得到、且未被划到第 1 / 2 / 6 / 7 项的菜单 | DS-01～DS-09、人才菜单壳、DS-17～20、DS-25～29、DS-30 四块 |
| **跨项索引**（只登记，不建叶） | 别的集成项做页面或供数，这里记清边界 | DS-21～24（第 7 项）、人才四子页供数（第 2 项 WBS-02-01）、三要素（第 2 项 WBS-02-02）、DS-04 的 `/innov`（已有 `E-INNOV-M1-L08`） |
| **跨页公共物**（WBS-05-25 及以后） | 不是某一页、但属展示系统整体的东西 | 前端公共底座、小屏、门户 iframe、合规对齐、指标盘点 |

### 0.2 编号规则

- `WBS-05-NN` 一条线一行；`NN a / NN b` 表示同一菜单的前端 / 后端两行。
- `WBS-05-08-0N` 是 `WBS-05-08` 的**子任务行**，与 `SYSINT-05-08-0N-L01` 一一对应，不另算菜单。
- `WBS-05-18-0N` 是 `WBS-05-18` 的**子任务行**（SITUATION-ENT 长任务管线 · 企业维度数据跑通，2026-10-27 挂接），口径同 `WBS-05-08-0N`，不另算菜单。
- `WBS-05-19-0N` 是 `WBS-05-19` 的**子任务行**（SITUATION-IM 长任务管线 · 创新监测三页数据打通 + 评审就绪，2026-10-28 挂接），口径同上，不另算菜单。
- `WBS-05-04-01` 是 `WBS-05-04` 的**子任务行**（科技数据资源四视窗对照已建成 GDF，2026-11-02 建叶），不另算菜单。
- `WBS-05-23-0N` 是 `WBS-05-23` 的**子任务行**（科技政策跟踪）。05-23-01～10 挂已有复刻单与契约单；05-23-11～13 是实现、对齐、真联调；05-23-14～15 是存量调研与系统详细设计。`WBS-05-23-L2-*` 是按 SRS level5 拆的二级设计单（§4.1c，26 个二级 × 4）。都不另算菜单。
- 一个 WBS 行可以索引多个任务 ID；反过来一个任务只挂一行，不重复编号。
- **计划叶 `LT-5-*` 不是任务**。`05-展示系统集成工作计划.md` §0 写明「计划叶 ID 不是 registry 任务」。本表只在 §1 的「计划叶」列引用它作排期对照，不当任务号用。

### 0.3 列口径

| 列 | 说明 |
|---|---|
| 状态 | 以 `task-registry.yaml` 的 `status` 为准（现役值：`backlog` / `ready` / `claimed` / `in_progress` / `review` / `pending_test` / `ready_to_sign` / `integration` / `done`）。空白表示**未建任务**。监管人与 registry 的 `supervised_by` 不一致时，以本表登记为准并注明变更。 |
| 完成情况 · handoff | 该任务 handoff / evidence 的**一句话结论 + 落盘路径**。路径相对 `agent-delivery/`（少数相对本夹，已标出）。无同名 handoff 文件的，写明「无同名 handoff」。 |
| 依赖 · 可对端 | 上游依赖与对外交付口径。属于外部对端承诺的，一律保留原文语气，不写成已承诺。 |

### 0.4 真源

| 件 | 路径 | 用作 |
|---|---|---|
| 菜单目录 | `acceptance-catalog/catalog-display-7modules.yaml`（30 叶）、`agent-handoffs/产品整体定义/科技信息展示系统-完整详细设计/02-需求分析.md` | **菜单目录真源** |
| 展示详设 | `agent-handoffs/产品整体定义/科技信息展示系统-完整详细设计/00-目录与阅读指南.md`（v0.2，已同步 A1–A15 裁决） | 页面设计输入 |
| 任务 | `task-registry.yaml`（`status` / `supervised_by` / `repo` / `claimed_by`） | 状态、监管人、仓 |
| 本月计划叶 | `工程过程/02-策划与监控/02-智树工作计划/02-进度/05-展示系统集成工作计划.md` | 页面施工序，不代替本表 |
| 技术方案 | [技术方案.md](./技术方案.md) | 范围与调用方向（**现稿仍按旧范围书写，见 §7**） |
| 架构 | `ARCH-DISPLAY-01.md`（v0.9，裁决人 `human:徐滕强`） | L0–L5、A1–A15 |

### 0.5 与其它项的边界

- **第 2 项**：三要素供数（WBS-02-01 人才、WBS-02-02 技术 / 技术链 / 科研机构）。本表只记菜单侧消费。
- **第 7 项**：知识图谱四页 DS-21～24，以及读图、查图、图指标。本表只索引，不建叶、不重画时序。
- **第 1 项**：第 1 项全链路自研范围内的内容不重复登记。
- **第 6 项**：三方源进 ADS 的 GDF 作业。本表不新开 GDF 包。

## 1. 菜单全覆盖索引

> 七模块 30 叶 + 政策核增 4 叶 + 维护管理。读法：先在下表定位菜单，再到 §2～§5 看该 WBS 行的任务明细与完成情况。

| 一级菜单 | 叶 | 页名 | WBS 叶 | 挂载任务（含状态） | 完成摘要 | 计划叶 |
|---|---|---|---|---|---|---|
| 科技发展态势 | DS-01 | 科技全域态势 | WBS-05-18 | `FE-TS-01A`(integration)、`BE-TS-IMPL-01`(backlog)、`BE-TS-DATA-01`(backlog)、`DS-01-METRIC-OPEN-L01`(integration)、`SITUATION-ENT-*` 长任务管线（10-27 挂接，见 §4.3；11-01 五单 `SITUATION-ENT-D2-L01` / `-D3-L01` / `-MOCK-LEDGER-L01` / `INFLUENCE-FIX-L01` / `GRANULARITY-FIX-L01` 均 integration，11-02 新增 `METRIC-LIB-ALGO-INFLUENCE-L01`(integration)，共 7 条 integration 停本地待走查（含 11-02 完工 `SITUATION-ENT-SPARK-L01`）；11-02 另补登记两条 backlog `SITUATION-ENT-FOLLOW-SVR-L01`（待裁定收藏表归属 upms）/ `SITUATION-ENT-TREND-FEAT-L01`） | 前端整页复刻已 push、三绿；REST 待 `BE-TS-CONTRACT-01` 冻结。指标语义卡仍草稿未签。10-27 起企业维度数据跑通长任务挂接本行；11-01 全维度打通五单（机构不做点位、期刊/会议 mock、mock 台账、影响力 Tab 修复、时间粒度打通）+ 11-02 指标库口径对齐与算法库优先接入（期刊/专家取算法库真实值，论文/专利/服务保留 mock，五卡挂 metric_id），七条 integration 改动停本地未 commit / 未 push 待 `human:李伟` 走查；11-02 要素卡年度趋势 spark 完工（论文 / 人才 / 项目 / 机构接久新真实年度序列，7101 探针末点 = 卡值、无断崖），收藏服务端化按只读铁律改落 upms 待裁定，趋势预测 / 异常监测待裁定，见 §4.3 05-18-15～17 | LT-5-SIT-DS01 |
| 科技发展态势 | DS-02 | 科学技术全景 | WBS-05-01a～01g | `SYSINT-05-01A-L01`(ready)、`SYSINT-05-01B-L01`(ready)、`TS-L2-DS02-ARCH`(ready)、`TS-L2-DS02-SDD`(ready)、`TS-L2-DS02-READ-PY-L01`(backlog)、`TS-L2-DS02-SCORE-L01`(backlog)、`TS-L2-DS02-TEST-L01`(backlog)、`FE-TS-02A`(integration)、`DS-02-METRIC-OPEN-L01`(integration) | 说明书 `TS-L2-DS02-SDD`。展示只做 17–33。34–40 不建单，41–47 归维护管理。入图是第 2 项，不替代本行。实现补读图、灌数、主路径测试三张，会签前不开工 | LT-5-SIT-DS02 |
| 科技发展态势 | DS-03 | 技术发展跟踪 | WBS-05-02a / 02b | `SYSINT-05-02A-L01`(integration)、`SYSINT-05-02B-L01`(integration)、`FE-TS-03A`(integration)、`DS-03-METRIC-OPEN-L01`(integration)、**`SITUATION-TS-TRACKING-EVAL-L01` / `-REPORT-L01` / `-PERSIST-L01`(integration，11-03 补登本轮工作)** | 三个 Tab 可开或空态；材料未到时空态。名称收口为「技术发展跟踪」。11-02～11-03：真评估接入（久新模型产出，不再吃 mock）、报告 HTML/PDF、范围挂载（区域/时间/领域**均真实生效**——领域复用科技全域态势 `subfield_topic_map` 反查，实测 CL-SEI-01 → 39 子学科）、历史与模板落库回读、结果页技术评估榜单表（Top-20）、报告最近列表上限+清理、D9 按 missing 落红问号；**11-06 走查反馈收口并推 origin/dev**：规模（论文）改累计口径（`ads_technology_profile.paper_count`，top20 20/20 非 0）；成熟度对 `NO_PUBLICATION_OBSERVED`（top20 17/20）回落阶段研判 `stage_code`，20/20 有值；并排对比只取最近 3 期（前端 `slice(-3)` + 后端 `HISTORY_MATRIX_PERIODS=3`）；详情面板消费簇群角色/应用案例/瓶颈/演进路径/证据链 5 类后端事实字段；时间轴年份与热力图列轴同源（`heatMatrixYears` 2015-2025）；演示控件收口到 `reviewMode`；type-check/build 三绿；M3-spec 回写 T21/T22 | LT-5-SIT-DS03 |
| 科技发展态势 | DS-04 | 全球创新监测 | WBS-05-19 | `FE-TS-04A`(integration)、`DS-04-METRIC-OPEN-L01`(integration)；已有 `E-INNOV-M1-L08`（tier FULL，路由 `/innov`）；`SITUATION-IM-C11..C15` 五端点 11-03/04 实质 integration（见 §4.4 偏离说明） | 综合 / 实时 / 载体 / 监测 / 能力五块可切换；11-03 走查七项整改 + 11-04 领域补齐（论文/项目 100%）、学者接入（ads_talent_profile 10 万）、图谱「全部」视图双根因修复、三仓代码首次 push 触发 CI；详见 `agent-handoffs/科技发展态势-TS/M4-REMEDIATION-20261103.md` §12-13 与走查准备件 | LT-5-SIT-DS04 |
| 科技发展态势 | DS-05 | 湾区创新监测 | WBS-05-19 | `FE-TS-05A`(integration)、`DS-05-METRIC-OPEN-L01`(integration)；同上 `SITUATION-IM-*` 长任务管线（见 §4.4）；**`SITUATION-IM-C6..C10`(integration) + `D2`(integration) 11-07 完成** | 成果地图 / 四维 / SWOT / 指标四块后端切久新（achievements/capability/indicators 通真实链路，swot/alerts 诚实空态）；前端 P0 NaN 三修 + P1 硬编码七修 + type-check/build 三绿 + push `origin/dev`（commit `514bd84`）；诚实披露：城市有源 8/11、能力分仅广深惠莞 4 城、MECH 子指数隐藏；详见 §4.4 WBS-05-19-10～16 | LT-5-SIT-DS05 |
| 科技发展态势 | DS-06 | 深圳创新监测 | WBS-05-19 | `FE-TS-06A`(integration)、`DS-06-METRIC-OPEN-L01`(integration)；同上 `SITUATION-IM-*` 长任务管线（**pilot 起点**，见 §4.4） | note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」；**模块目录无同名 `FE-TS-06A.md`** | LT-5-SIT-DS06 |
| 科技发展态势 | DS-07 | 科技创新评估 | WBS-05-20 | `FE-TS-07A`(claimed，P2)、`DS-07-METRIC-OPEN-L01`(integration) | 复刻未开工；评估对象范围未补则按详设空态 | LT-5-SIT-DS07 |
| 科技发展态势 | DS-08 | 科技指数 | WBS-05-21 | `FE-TS-08A`(integration)、`FE-DISPLAY-TECHINDEX-NEW-L01`(integration)、`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01`(pending_test)、`DS-08-METRIC-OPEN-L01`(integration) | 九域 + 8 件套 + 算法口径页已出，布局溢出由 fix 8a46d7d 修；mock 权重（40/30/20/10）一致性已修待抽测。**只做展示侧，不做智库后台** | LT-5-SIT-DS08 |
| 科技发展态势 | DS-09 | 科技发展规划 | WBS-05-22 | `FE-TS-09A`(integration)、`DS-09-METRIC-OPEN-L01`(integration) | 综合规划 / 重点领域 / 研究分析可切换；预警模型可 501，不编制规划正文 | LT-5-SIT-DS09 |
| 科技发展态势 | — | 维护管理（M10 · `/trend/maintain/*`，不另开一级菜单） | WBS-05-24 | `FE-TS-10A`(integration) | 图层与数据源、技术图谱关键实体与关系维护；无权限是降级不是白屏。**报价表划掉且工作量为 0 的「维护技术图谱」不实现**。存量调研见[对照-科技发展规划与维护管理-存量任务与依赖.md](./对照-科技发展规划与维护管理-存量任务与依赖.md) A 段 | LT-5-SIT-OPS |
| 科技政策跟踪 | DS-10 | 科创政策全景 | WBS-05-23-03 / 04 | `FE-POL-01A`(pending_test)、`FE-POL-01B`(integration)；基座 `FE-POL-S01`(pending_test) | 检索主链路待测试；其余 4 Tab 联调中，硬依赖 01A。真数等 `BE-POL-CONTRACT-01` | LT-5-POL-DS10 |
| 科技政策跟踪 | DS-11 | 政策分析评价 | WBS-05-23-05 | `FE-POL-02A`(pending_test) | 整页复刻待测试。硬依赖只有基座，与全景可并行。模型未注册保持 501 | LT-5-POL-DS11 |
| 科技政策跟踪 | DS-12 | 政策效果推演 | WBS-05-23-06 | `FE-POL-03A`(integration)；接线 `POL-L2-DS12-WIRING-L01`(integration，WBS-05-23-L2-08E / 09E)；用例 `POL-L2-DS12-EST-TEST-L01`(integration，08F)、`POL-L2-DS12-SIM-TEST-L01`(integration，09F) | 灌数两单与 `POL-L2-DS12-JOBS-IMPL-JAVA` 已签收。推演 ≠ 专题布局推荐 | LT-5-POL-DS12 |
| 科技政策跟踪 | PC-1～PC-4 | 政策数据治理 / 智能政策拆解 / 多维政策对比 / 智能研报生成 | WBS-05-23-07～10 | `FE-POL-04A`(integration)、`05A`(integration)、`06A`(integration)、`07A`(ready_to_sign) | 四页硬依赖都只是基座。ChainSteps 归 04A，06A/07A 仍是占位。PC-4 Job 未注册则 501 | LT-5-POL-PC1～PC4 |
| 科技人才态势 | DS-13～DS-16 | 全球领域人才态势 / 关注地区人才态势 / 重点科技人才画像 / 人才引进推荐评估 | WBS-05-03a / 03b | `SYSINT-05-03A-L01`(ready)、`SYSINT-05-03B-L01`(ready) | **只做菜单壳与非三要素区块**；四子页不重做，供数是 WBS-02-01（第 2 项）；资讯、职位变动、奖项荣誉、引进成本、尽调五类空态 | LT-5-TAL-DS13～DS16 |
| 科技数据资源 | DS-17～DS-20 | 总体 / 接入 / 主题 / 应用四视窗 | WBS-05-04 | `SYSINT-05-04-L01`(claimed，监管 淮政玮 → 实际认领 孔东) | 四个视窗可切换；共建数据未到为空态。R6：data 组供方未找到（原华为云 2026-10-15 退出）。对照已建成 GDF 的分析见 WBS-05-04-01 | LT-5-RES-DS17～DS20 |
| 科技知识图谱 | DS-21～DS-24 | 分析展示 / 指标展示 / 算法展示 / 服务展示 | **跨项索引（第 7 项）** | `FE-DISPLAY-KG-SERVICE-ALIGN-L01`(review) | 本表**不建叶**。第 7 项负责页面与查图；`FE-DISPLAY-KG-SERVICE-ALIGN-L01` 是 demo 侧 DS-24 服务展示合规对齐，原地更新 `ServiceDisplay.jsx` | LT-5-KG-DS21～DS24 |
| 科技成果展示 | DS-25～DS-29 | 软科学成果展示 / 科技创新生态展示 / 科技时空演进展示 / 大型科学仪器共享 / 创新载体孵化载体 | WBS-05-05 | `SYSINT-05-05-L01`(claimed)、`FE-DISPLAY-ACHIEVE-ALIGN-L01`(pending_test) | 五页可打开或空态；仪器只展示、不做预约闭环；时空演进**禁止用专题 B 面时间轴冒充**；口径未绿用角标不改数 | LT-5-ACH-DS25～DS29 |
| 科技服务全景 | DS-30 之① | 科技创新生态服务（全景里唯一智树自研子菜单） | WBS-05-06 | `SYSINT-05-06-L01`(claimed)、`FE-DISPLAY-SVC-ECO-ALIGN-L01`(review) | 列表与详情可开或空态；demo 侧原地更新 `InnovationEcosystem.jsx` | LT-5-SVC-ECO |
| 科技服务全景 | DS-30 之② | 智库服务 | WBS-05-07（子 05-07-01～08，见 §4.1f） | `SYSINT-05-07-L01`(ready)、`FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01`(in_progress)；真实对接 8 子任务待 registry 登记 | 2026-10-23 起**不按跳转**（2026-11-06 细化为：不跳出新页签/新窗口，允许本系统内 iframe 弹框嵌入）；接口已到 9 端点（v1.1 四 GET + docx 五 POST）。智树不做高端智库后台。demo 页按需规 566–574 整改完成。真实对接派单稿：`agent-handoffs/科技服务全景-SVC/派单说明/派单-SYSINT-05-07-THINKTANK-REALDATA-L01.md` | LT-5-SVC-HUB |
| 科技服务全景 | DS-30 之③④⑤ | 科技交流 / 科技竞赛 / 科技传播 | WBS-05-08（子 05-08-01～06） | `SYSINT-05-08-L01`(ready_to_sign)、`SYSINT-05-08-01-L01`(done ✅ 10-30)、`SYSINT-05-08-03-L01`(done ✅ 10-30)、`-02/-04/-05/-06`(done ✅ 10-31)、`SVC-PANORAMA-API-L01`(claimed)、`SVC-PANORAMA-GAP-L01`(ready_to_sign) | -01 签收 ✅；-02 三入口菜单壳（iframe 弹窗）；-03 交流 BFF + FE；-04 竞赛 BFF + FE；-05 传播 BFF + FE；-06 联调验收 —— 六个子任务 2026-10-31 全部 done | LT-5-SVC-HUB |
| 跨全部菜单 | — | 本项菜单注册与用户权限 | WBS-05-09 | 未建任务（监管人待指定） | 相对路径进统一用户中心；地址不写主机名；配菜单的人 2026-10-22 纪要未点名 | LT-5-SSO |

---

## 2. 方案

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-00 · `SYSINT-SCHEME-05-L01` | 系统集成技术方案_展示系统集成 | 淮政玮（执行 `agent:doc-agent`） | `gkx-orchestration` | **in_progress** | 2026-10-23 曾签收、同日改回处理中。五段方案已落到 [技术方案.md](./技术方案.md)；派单说明见本夹 `派单说明-SYSINT-SCHEME-05-L01.md`；handoff 指针 `agent-handoffs/SYSINT-SCHEME-05-L01.md`。**尚未 ready_to_sign** | 五段写在技术方案。范围口径 2026-10-27 扩为全菜单，**方案正文待同步**（见 §7） | 无截至时间 |

---

## 3. 技术架构与契约设计（跨页 · 技术架构设计类）

> 这一组不是某一页，是展示系统整体的**技术架构 / 接口契约 / 部署**。之前已提交的 `ARCH-DISPLAY-REDESIGN-L01`、`BE-TS-CONTRACT-01/02`、`BE-TS-AGG-01`、`DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01` 全部在此可索引。
> 关联顺序：`BE-TS-CONTRACT-01` 定「接口怎么取」→ `BE-TS-AGG-01` 定「数据怎么生」→ `BE-TS-DATA-01` 落数 → `BE-TS-IMPL-01` 实现；契约的落库服务是 `gkxlumen-display`，即 `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01` 部署上线的那个 BFF。`ARCH-DISPLAY-REDESIGN-L01` 是这几件的上位架构真源。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-16 · `ARCH-DISPLAY-REDESIGN-L01` | **展示系统架构重新设计**：L0–L5 全栈架构说明书（`ARCH-DISPLAY-01.md` v0.9）+ 架构评审包 + L3 要素域设计 | 徐滕强（执行 `agent:arch-agent`） | `agent-delivery` | **done**（2026-10-26 `human:徐滕强` verified） | handoff `REVIEW-DISPLAY-徐腾强评审包.md`（按「谁能定」分组：徐滕强拍 4 / 指定责任人 4 / 已裁决 8 免回复）；evidence `ARCH-DISPLAY-01.md`。**A1–A15 全部裁定**：A1 展示侧不复用专题侧、自建 `element`:7082 / `graph`:7083 / `datacatalog`:7084，`gkxlumen-display` 为聚合 BFF（唯一对外 `/display/v1/**`）；A3 过渡期可直连久新只读库（须登记切换条件与隔离措施）；A5 反向裁决——暂不强制切正式 ADS（读 `demo_gkxlumenx_ads`，库名配置化，**前端 `VITE_*` / 代理侧仍零 demo**）；A7/R7 久新 42 个 API 未确认，`human:郭万迎` 对外催办；A8 图谱用现网 space `entan`。**遗留 2 项：A9 用户体系（PC / App 是否同一用户池待徐滕强确认）、A11 预跑读表清单（数据 Lead + 唐绍祖出）** | 上位铁律 `architecture-baseline.md` D1–D15；`ARCH-DISPLAY-01.md` §1.6 逐条对照、§1.7 C1–C6 共识溯源 | 已完结 |
| WBS-05-17 · `ARCH-TS-L3-DESIGN-01` | 科技发展态势 **L3 要素域架构设计**：说明书 v0.1（45.7 KB，服务划分 / 包结构 / DDL / 数据架构 / 久新通道抽象 / 降级 / 演进路线） | 徐滕强（随 WBS-05-16） | `agent-delivery` | **review**（2026-10-27 补登记，原无 registry 条目） | 文档已于 2026-10-25 落盘 `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-DESIGN-01.md`。**结论：新建 1 个 `gkxlumen-element`**（不按维度拆 8 个服务；跨维度聚合要同进程），久新 3 维度走 `local-ads`/`jiuxin-http`/`jiuxin-jdbc` 通道抽象做**片段级混合编排**；必复用 `gkxlumen-metrics`、过渡复用 `gkxlumen-innov`、**不复用 `gkxlumen-topic-*`**（偏离基线 §4，需裁决）。**状态 `draft`，非生效基线，裁决前 `BE-TS-IMPL-01` 不动工**；§8 给了不依赖裁决的 Step 1–4 最小验证闭环 | 挂 WBS-05-16（上位架构真源）。depends_on 故意留空——上游契约与聚合方案均 draft 未冻结，不触发 auto_ready | 待 `human:徐滕强` 签署后转 issued |
| WBS-05-17b · `ARCH-TS-L3-01` | 同一设计的**决策摘要单**（20.2 KB，一页签字用：结论摘要 + §7 六项待裁决 A1–A6 + §8 落地路线 + §9 证据索引） | 徐滕强 | `agent-delivery` | **review**（2026-10-27 补登记） | handoff `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-01.md`。**与上一条是同一份设计的两个载体，不是两件独立工作**；贡献分按一次设计计，不叠加。**A5（久新主体键是否对齐）是最大技术风险**，答复前 `channel/jiuxin-*` 只出桩实现。另需知会三项：`InnovSql.java` 指 demo 库违反 D12、待单开整改单；`lumen-algo-py` 零 TS 算法、M1 部分接口依赖建议并行排期；`metric_id` 清单（U6）未登记、D9 ⓘ 角标暂无法对接 | depends_on `ARCH-TS-L3-DESIGN-01`。下游：`BE-TS-IMPL-01`、`FE-TS-S01`、`DEVOPS-LUMEN-TOPIC-PY-SHOW-L01` | 同 05-17 |
| WBS-05-10 · `BE-TS-CONTRACT-01` | 科技发展态势 Java 接口契约定义与数据需求评审（**M0**，出 `API-TS-*` 文档） | 李伟（registry note 写「监管：human:徐滕强」） | `gkx-orchestration` | **claimed**（**仍未冻结**） | 派单 `agent-handoffs/科技发展态势-TS/派单说明/派单-BE-TS-CONTRACT-01.md`；产出 `科技发展态势-TS/API-TS-M1.md` + `BE-TS-CONTRACT-01.md`（M0 八类接口 + 八节枚举 + §9.1 五域）。**M0 三方评审未通过，契约未冻结** | `TS-模块开发规划与任务拆分.md` §4。前端 `FE-TS-01A`～`10A` 按本契约接路径，**未冻结不猜路径**；下游 02A / 04A 的联调闸门卡在这里 | 原定 2026-10-15，**已过期，待重定** |
| WBS-05-15 · `BE-TS-CONTRACT-02` | 科技发展态势 **M2–M9 逐页契约**（`API-TS-M2.md`～`API-TS-M9.md`，按批冻结） | 李伟 | `gkx-orchestration` | **integration**（转分批会签） | 派单 `派单-BE-TS-CONTRACT-02.md`。八份契约已逐字对齐 demo 真源产出，**转分批会签**：批 2 前冻 M2/M3、批 3 前 M4/M5/M6、批 4 前 M7/M8/M9；会签后 AV-1 → ready_to_sign → `human:淮政玮` 签收 | 挂 `BE-TS-CONTRACT-01`（以其 M0 模板为准）。原以「同叶后续」挂在 WBS-05-10，本次给它独立编号以便索引 | 随分批评审（批 2～批 4） |
| WBS-05-11 · `BE-TS-AGG-01` | 科技全域态势 · 产业铺底聚合口径（要素 × 区域 × 时间）+ ADS 标准表落库建议 | 李伟 | `gkx-orchestration` | **claimed** | 派单 `派单-BE-TS-AGG-01.md`；产出 `科技发展态势-TS/TS-聚合方案-产业铺底.md`（三维键 + 11 类要素口径 + ADS 落库清单）。**久新侧源（人才 / 机构 / 论文 / 专利）催办未清零** | `BE-TS-CONTRACT-01`；写数在 Python（D7）。只定口径与落库骨架，不实现 ETL；正式值禁前端自算；排除政策要素 | 原定 2026-10-15，**已过期，待重定** |
| WBS-05-12 · `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01` | 展示聚合 BFF（`gkxlumen-display`）部署层四件套 + 首次部署上线（D15 唯一对外面） | 李伟（执行 `agent:devops-agent`） | `lumen-svc-platform` | **ready_to_sign**（待 `human:李伟` 签收） | handoff `agent-handoffs/DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01.md`；派单 `科技发展态势-TS/派单说明/派单-DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01.md`。四件套入库、helm release deployed、display Pod 1/1 Running、网关 `/display/actuator/health` UP；含三次故障定位（reuse-values / Service ports / `--set` hook）与遗留清单 | 网关 `/display/**` 唯一对外；**不据此写成页面已上线**。design_ref 含 `ARCH-DISPLAY-01.md` §3.1–§3.2 与 D15 | 无截至时间 |
| WBS-05-13 · `BE-TS-IMPL-01` | M1–M9 展示聚合接口实现（Java） | 李伟（2026-10-27 由 `human:李伟` 认领，原无监管人） | 展示 Java（`gkxlumen-display`） | **backlog** | 仅有派单说明 `派单-BE-TS-IMPL-01.md`，**实现尚未开工** | `BE-TS-CONTRACT-01` 冻结、`BE-TS-DATA-01`。Java 不写算法；只读 ADS（D3）；`X-Trace-Id` 贯通；指标带 `metric_id` | 待定（随契约分批评审） |
| WBS-05-14 · `BE-TS-DATA-01` | M2–M9 ADS 数据对接 | 李伟（2026-10-27 认领） | 数据侧 / `lumen-etl-es-py` | **backlog** | 仅有派单说明 `派单-BE-TS-DATA-01.md`，**未开工** | `BE-TS-AGG-01`、`API-TS-M1.md` §9.1 五域。Python 写数（D7）；Java 只读已发布批次；Mock 先行按标准表写 | 待定（随三方源到位） |

## 4. 菜单开发子项

### 4.1 菜单叶（WBS-05-01～05-09、05-18～05-24）

> 表中「仓」只是建议，最终由该行监管人决定。三要素供数在第 2 项，读图 / 查图 / 图指标在第 7 项；本表留该菜单的其余对接对象。**对端未到，页面空态。**

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-01a · `SYSINT-05-01A-L01` | 科学技术全景 · 前端（三要素以外） | 孔东 | `lumen-ui-science-pc` | **ready** | 已建号未开工。同一菜单的 `FE-TS-02A`(integration)：mock 态自测 + type-check / build 绿、push `origin/dev`；handoff `科技发展态势-TS/FE-TS-02A.md` | `SYSINT-SCHEME-05-L01`；WBS-05-01b。页面可开；图谱 / 关键实体 / 路径的读图归第 7 项，本叶不另接一套查图接口；未承诺的块空态；菜单相对路径进统一用户中心 | 2026-10-30 |
| WBS-05-01b · `SYSINT-05-01B-L01` | 科学技术全景 · 后端（三要素以外） | 唐绍祖 | 展示 Java | **ready** | 已建号未开工。三个展示功能以 WBS-05-01c `TS-L2-DS02-ARCH` 为准（菜单 `/trend/tech-panorama`，序号 17–33。入图不在本叶。34–47 在维护管理 `/trend/tech-situation-maintain`） | `SYSINT-SCHEME-05-L01`；三要素供数依赖 WBS-02-02。三要素以外的区块能调到，或返回空；不写假数；三要素算法不在本叶 | 2026-10-30 |
| WBS-05-01c · `TS-L2-DS02-ARCH` | 科学技术全景 · 后台实现架构设计（序号 17–33） | 淮政玮 | `gkx-orchestration` | **ready** | 定义单，角色 `arch-agent`。功能架构稿 `agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md`：展示技术点图谱、关联实体、关键路径。入图仍在第 2 项。会签未做，不标 done。不重做 `FE-TS-02A`，不替代 01a / 01b | 无硬依赖。01b 开工读图以本稿为准。34–47 不在本单 | 无截至时间 |
| WBS-05-02a · `SYSINT-05-02A-L01` | 技术发展跟踪 · 前端 | 孔东 | `lumen-ui-science-pc` | **integration** | 11-03 核对：原记「已建号未开工」与事实不符，现更正。同一菜单 `FE-TS-03A`(integration) 已切 `USE_MOCK=false` 联调真实数据；另有 `SITUATION-TS-TRACKING-EVAL/REPORT/PERSIST-L01` 三单（真评估、报告导出、范围挂载与落库回读 + D9 缺口角标），设计文档 `repos/lumen-ui-science-pc/docs/tracking-真评估接入设计.md`；handoff `科技发展态势-TS/FE-TS-03A.md`。**11-03 下午第二批四项已实测**：产业领域经 `subfield_topic_map` 反查真生效（`CL-SEI-01` → 39 个子学科，提示文案由反查结果驱动）、结果页新增「技术评估榜单」Top-20（10 行预览可展开，只排序格式化不重算）、最近报告 5 条上限 + 两段式清理（「清理」→「确认清理」，`status=deleted` 留痕）、领域提示二态化；验证：前端 lint 0 诊断、`vite build` 绿（built in 1m 27s）、E2E 三项通过 | `SYSINT-SCHEME-05-L01`；WBS-05-02b。结果 / 参数 / 方法三个 Tab 可开，或空态；名称用「技术发展跟踪」；接真实数据源，不写假数 | 2026-11-03 |
| WBS-05-02b · `SYSINT-05-02B-L01` | 技术发展跟踪 · 后端 | 唐绍祖 | 展示 Java | **integration** | 11-03 核对：原记「已建号未开工」与事实不符，现更正。已有 `TrackingController` **13 个端点**：meta / dataset / evaluation(run·progress·result) / parameter-templates(+`-remove`) / report / reports / `report-remove` / report/{id}/download；11-03 补领域反查 `resolveSubfieldIds()`（display → innov `/v1/meta/industry-clusters/industry-subfields` 读 `{dim}.subfield_topic_map` 得 `subfield_ids`，上限 50）与 meta 默认领域修复（原写死空串把前端默认 `CL-FUT-05` 覆盖成空致领域永不生效，现下发首个 `mapped` 集群 `CL-SEI-01`），端点全量实测 **13/13**（15:20 补测 `DELETE /parameter-templates/{key}`：建临时模板 → 删除 `removed=true` → 列表回 5 条，全程 `code=0`）。取数走久新只读通道，评估值为 `technology_insight_mvp_v2` 规则基线产出（只装配不重算）；落库经域服务 `tech_evaluation_history` / `tech_evaluation_report` / `evaluation_template` | `SYSINT-SCHEME-05-L01`；三要素供数依赖 WBS-02-02。三个 Tab 的接口可调，或空；专家评估法、经济分析法没有已签收实现，不在本叶新定义口径；无源字段走 `noSourceFields` 如实声明 | 2026-11-03 |
| WBS-05-03a · `SYSINT-05-03A-L01` | 科技人才态势菜单壳与非三要素区块 · 前端 | 孔东 | `lumen-ui-science-pc` | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`；WBS-05-03b；四子页不重做。菜单可进；非三要素区块有数或空态；四子页不在本叶填数；五类缺失为空态 | 2026-11-05 |
| WBS-05-03b · `SYSINT-05-03B-L01` | 科技人才态势菜单壳与非三要素区块 · 后端 | 唐绍祖 | 展示 Java | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`。四子页供数是 WBS-02-01，本叶不重做四页；非三要素接口可调或空；五类缺失保持空态；不写假数 | 2026-11-05 |
| WBS-05-04 · `SYSINT-05-04-L01` | 科技数据资源（四视窗作为一个菜单） | 淮政玮 → 2026-10-23 改徐滕强 → registry 实际认领 `human:孔东` | `lumen-ui-science-pc`、展示 Java | **claimed** | 监管人两次变更已登记，**未开工** | `SYSINT-SCHEME-05-L01`。对端材料写智谱、未回文前空态；四个视窗可切换；共建数据未到为空态；菜单进统一用户中心 | 2026-11-09 |
| WBS-05-05 · `SYSINT-05-05-L01` | 科技成果展示（五页作为一个菜单） | 徐滕强 | `lumen-ui-science-pc`、展示 Java | **claimed** | 未开工。原型侧的 5 个 New 页由 `FE-DISPLAY-ACHIEVE-ALIGN-L01` 建出（pending_test） | `SYSINT-SCHEME-05-L01`。五页可打开或空态；仪器只做展示，不做预约闭环；口径未绿用角标，不改数 | 2026-11-05 |
| WBS-05-06 · `SYSINT-05-06-L01` | 科技创新生态服务 | 徐滕强 → 2026-10-23 改侯佳伟 | `lumen-ui-science-pc`、展示 Java | **claimed** | 未开工。原型侧对齐见 `FE-DISPLAY-SVC-ECO-ALIGN-L01`（review） | `SYSINT-SCHEME-05-L01`。列表与详情可开，或空态；菜单进统一用户中心 | 2026-11-09 |
| WBS-05-07 · `SYSINT-05-07-L01` | 智库服务 | 李伟（registry 记一线孔东） | `lumen-ui-science-pc`、展示 Java | **ready** | 2026-10-23 起**不按前端跳转**，要求智谱提供接口；接口未到为空态。原型页整改见 `FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01`（in_progress） | `SYSINT-SCHEME-05-L01`。对端是智谱；智树页面能调到智谱接口；**智树不做高端智库后台** | 2026-11-09 |
| WBS-05-08 · `SYSINT-05-08-L01` | 科技交流、科技竞赛、科技传播（父） | 李伟 | `lumen-ui-science-pc` | **ready_to_sign** | 挂接自建任务 `SVC-PANORAMA-API-L01`（父统筹单，claimed）、`SVC-PANORAMA-GAP-L01`（对照表成品，ready_to_sign）。**2026-10-31：六个子任务（-01～-06）全部 done —— -01 对接分析已签收；-02 三入口 iframe 弹窗壳；-03 交流 BFF + FE；-04 竞赛 BFF + FE；-05 传播 BFF + FE；-06 联调验收（实测三页深势真实数据）**。三仓改动已推 `origin/dev`，父任务推进 ready_to_sign 待签收。子任务详见 §4.2 | `SYSINT-SCHEME-05-L01`。对端名称「北大深势」只出现在规约，能力评估文未署此名，**名称核对还没有** | 2026-11-09 |
| **WBS-05-09** | 本项菜单注册与用户权限（全景、技术发展、人才态势、数据资源、成果展示、生态服务、智库、交流、竞赛、传播） | **待指定**（2026-10-22 纪要未点名） | 统一用户中心配置；业务仓不写主机名 | **未建任务** | — | `SYSINT-SCHEME-05-L01`。各菜单叶负责自己的相对路径；这些菜单以相对路径可见，对应用户登录后能进；地址不写主机名；交流 / 竞赛 / 传播跳转失败仍有提示；智库不按跳转走智谱接口 | 无截至时间 |
| WBS-05-18 | 科技全域态势（DS-01，含 M1 聚合 BFF 消费） | 孔东（FE）/ 李伟（BE） | `lumen-ui-science-pc`、`gkxlumen-display` | **integration** | `FE-TS-01A` handoff `科技发展态势-TS/FE-TS-01A.md`：整页复刻 integration；所依赖的底座 `FE-TS-S01` 已 done。后端 `BE-TS-IMPL-01` 未开工。指标卡 `DS-01-METRIC-OPEN-L01`：赋号草稿、类型未签、公式待 `human:唐绍祖` 共签。**2026-10-27 挂接 `SITUATION-ENT` 长任务管线（企业维度数据跑通，子任务见 §4.3，授权人 `human:李伟`）**。**2026-11-03 影响力 Tab 由 5 卡扩为 6 卡（新增项目含课题，算法库真实产物），运行态实测 6 卡全出；11 要素 8 真 3 mock，566 指标 d4 仍全 mock**。**2026-11-03 产业领域筛选后端就绪**：element 8 个企业端点支持 `industryId` 产业码过滤（精确命中或前缀下钻，未传零回归），display `RemoteElementClient` 已透传；前端尚未接线，实现叶见 `WBS-02-14`（`SYSINT-INDDISC-02-L02`） | `FE-TS-S01`、`BE-TS-CONTRACT-01` 冻结（M1）。11 要素图层 / 科创事件双 Tab；久新人才、科研机构、论文、专利未到则**空态** | 计划 LT-5-SIT-DS01：10-16 → 10-20 |
| WBS-05-19 | 创新监测三页（DS-04 全球 / DS-05 湾区 / DS-06 深圳） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-04A` / `05A` / `06A` 三份 handoff 均已 push（`06A` note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」，但模块目录**无同名 `FE-TS-06A.md`**）。已有 innov 事件地图只对齐，不另起一套。**11-03/04 DS-04 专项**：走查七项整改 + 领域/学者接入 + 图谱根因修复，前端改动本会话随文档一并 push（见走查准备件 §一）。**11-07 DS-05 湾区完成**：后端切久新（`RemoteShowPythonClient`，无 `RemoteInnovClient`），achievements/capability/indicators 三端点通真实链路，swot/alerts 诚实空态；前端 P0 NaN 三修（`Number.isFinite` + `fmtPctOrDash()`）+ P1 硬编码七修（图表轴自适应 / markPoint 年份动态 / 标题年份 computed / mock 字典绕过真源 / 伪时间戳诚实化）+ type-check/build 三绿 + push `origin/dev`（commit `514bd84`）；角标挂载（R2）待评审底座（R0）就绪后统一挂载。详见 §4.4 WBS-05-19-10～16 | `BE-TS-CONTRACT-01`（M4 / M5 / M6 契约未冻结）。订阅 / 推送的对端宋泉未确认则该块空态 | 计划 10-28 → 10-31（DS-06 及以后冲出 V1 开发出门） |
| WBS-05-20 | 科技创新评估（DS-07） | 孔东 | `lumen-ui-science-pc` | **claimed**（P2） | `FE-TS-07A` 仅 claimed，复刻未开工 | 评估对象范围未补则按详设空态 | 计划 11-03 → 11-04（结束日 = V1 测试末日） |
| WBS-05-21 | 科技指数（DS-08） | 孔东 / 淮政玮 | `lumen-ui-science-pc`（正式）、`demo-ui-science`（原型侧） | **integration** | `FE-TS-08A` handoff `科技发展态势-TS/FE-TS-08A.md`（三级指标树 / 34 省地图 / 专家 H 指数 / 四维趋势 / 排行榜 / 20 人评议只读）；`FE-DISPLAY-TECHINDEX-NEW-L01` 九域 + 王惠 8 件套 + 唐绍祖算法口径，布局溢出由 fix 8a46d7d 修；`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01` mock 权重 40/30/20/10 派生一致已修，pending_test | **只做展示侧，不做智库后台**。专家评议 20 人只读 | 计划 11-04 → 11-05（晚于 V1 测试） |
| WBS-05-22 | 科技发展规划（DS-09） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-09A` handoff `科技发展态势-TS/FE-TS-09A.md`：综合规划 / 重点领域 / 研究分析可切换。**2026-11-06 存量调研落盘（DS-09 段监管 `human:王梓真`，草稿待复核）**：[对照-科技发展规划与维护管理-存量任务与依赖.md](./对照-科技发展规划与维护管理-存量任务与依赖.md) B 段——三页签建议新建 `TS-L2-DS09-OV` / `KEY` / `RES-*` 四单各一组（建单前查重，顺序 OV→KEY→RES）；契约缺口：序 179 无端点、序 196 无独立端点、FE real 单端点 `/situation/v1/planning/dataset` 与契约 8 端点差异；不并进 `BE-TS-IMPL-01` / `BE-TS-DATA-01`。**2026-11-06 OV 组四单会签通过待真签**：`TS-L2-DS09-OV-ARCH/API/METRIC/DATA`（definition 全 ready_to_sign——曾按总控代签 done，同日监管人 `human:王梓真` 裁定撤销代签、待 human:淮政玮 真签；监管 `human:王梓真`，总控授权新人引导 §4.2；四角色会签 v2 闭环 [综合发展规划-会签.md](../../../../../agent-handoffs/科技发展态势-TS/sdd/l2/会签/综合发展规划-会签.md)；稿与薄 handoff 在 `科技发展态势-TS/sdd/l2/` 与 `科技发展态势-TS/`）。判定：183 真读写订阅（scope_type=planning_resource 零 DDL + 新表 sys_user_planning_push_record）/ 184 501 通道 / 178-182 D18 读表 8 张 ts_plan_*（种子 244 行）。**KEY 组同日完成**：`TS-L2-DS09-KEY-ARCH/API/METRIC/DATA` 四单会签通过（v2 闭环，[重点领域规划-会签.md](../../../../../agent-handoffs/科技发展态势-TS/sdd/l2/会签/重点领域规划-会签.md)）推 ready_to_sign 待真签；9 表 61 行、单端点平铺 9 块、零 501、U8 两裁定采纳。**RES 组同日完成**：`TS-L2-DS09-RES-ARCH/API/METRIC/DATA` 四单会签通过（[研究领域分析-会签.md](../../../../../agent-handoffs/科技发展态势-TS/sdd/l2/会签/研究领域分析-会签.md)；⚠️ 主会话代审——子智能体链路故障已在会签文件声明，G-B3 方案 A / U3 80/65/45 / U9 100/300 裁定，graph 实测 14+13）推 ready_to_sign 待真签。**至此 DS-09 三组 12 张定义单已于 2026-11-09 由菜单负责人 `human:王梓真` 签收全 done**（沿 M10 先例：负责人拍板、agent 代登记，会签记录三份在 `sdd/l2/会签/`）。**实现单状态（2026-11-09 晚）**：`TS-L2-DS09-SEED-L01`（integration：29 表 375 行入库、断言全过、graph_limit 补修 ef6c8a38）、`TS-L2-DS09-IMPL-JAVA-L01`（integration：10 GET+1 PUT、mvn 134/134 绿、svc commit 5295577）、`TS-L2-DS09-WIRING-L01`（in_progress：孔东 11-09 放行 FE 锁，联调闸门升 ready 已开工）、`TS-L2-DS09-TEST-L01`（**ready_to_sign ✅ 2026-11-09**：真机验收 15/15 全过——三页签数据逐项对表、184→501+⚠️、195 导出诚实降级；截图 `科技发展态势-TS/e2e_shots/` 三张、handoff `TS-L2-DS09-TEST-L01.md`；同批 SEED/IMPL/WIRING 联调通过推 pending_test。**DS-09 菜单端到端交付成立**：mock 种子→ADS 29 表 375 行→Java 10+1 端点→前端接线→dev 部署→真机验收）；另建跨菜单缺口单 `BE-TS-EXPORT-CENTER-GAP-L01`（2026-11-10 由 zcode 会话实施，监管改 human:王梓真——display 内实现 M1 §3.8 五端点：Word(.doc)=demo downloadHtmlAsWord 同款 Word-HTML 零新依赖；内存任务注册表+确定性渲染+HMAC 短时签名 URL（不破 display 不直连主库红线）；184 与 direction-warnings 同闸 501（复用 PlanningDirectionAlertGate）；195 模板文案全表行携带零硬编码；7 用例绿，handoff `科技发展态势-TS/BE-TS-EXPORT-CENTER-GAP-L01.md`）。**批 4 冻结 + 运维激活（2026-11-09/10 晚，监管 human:王梓真，追溯登记 `TS-L2-DS09-BATCH4-OPS-L01` pending_test）**：§7-5 items[] / §7-6 reason / §7-7 口径三卡前后端上线实测 200；`ts_plan_push_pool` 建灌 + push-pools Nacos 发布；direction-alert registered=true 翻转生效（direction-warnings 200/61 条）；`ops:planning-alert-gate` 自包含激活任务绿色跑通（Nacos 用户缓存定位与三次迭代教训入 handoff `科技发展态势-TS/TS-L2-DS09-BATCH4-OPS-L01.md`） | 预警模型可 501；**不编制规划正文** | 计划 11-05 → 11-06 |
| WBS-05-23 | 科技政策跟踪（DS-10～DS-12 + 核增 PC-1～PC-4） | 孔东（FE）/ 李伟（契约与实现） | `lumen-ui-science-pc`；demo 原型另计 | **混** | 复刻单见 §4.1b。2026-11-03 另建调研 `POL-DISPLAY-SURVEY-L01`、详设 `POL-DISPLAY-SDD-L01`，以及 `BE-POL-IMPL-01`、`BE-POL-DATA-01`、`FE-POL-REAL-01`。demo 侧仍挂 `DISPLAY-POLICY-GAP-AC-L01`(integration)、`FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01`(in_progress，无同名 handoff)。依赖全文：[对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md) | mock 复刻不等契约。真联调等契约、实现、统计对齐。专题 `E-E7-POLICY-M1-L06` 不是本行前置 | 计划 10-20 → 10-28（DS-10～12 窗内，PC 属 V2）；正式复刻 2026-11-02 已开工 |
| WBS-05-24 | 维护管理（M10 · `/trend/maintain/*`） | 孔东 | `lumen-ui-science-pc` | **integration**（P2） | `FE-TS-10A` handoff `科技发展态势-TS/FE-TS-10A.md`：图层与数据源配置 / 维护技术图谱 / 关键实体与关系维护 / 已有能力入口；无权限是降级不是白屏。**2026-11-06 存量调研落盘（M10 段监管 `human:刘剑锋`）**：[对照-科技发展规划与维护管理-存量任务与依赖.md](./对照-科技发展规划与维护管理-存量任务与依赖.md) A 段——图层与数据源需规锚点 = **M1 序 5–9**；序 34–40 不建单；41–47 建议新建 `TS-L2-M10-ENT-*` 四单（建单前查重）；M10 不并进 `BE-TS-IMPL-01` / `BE-TS-DATA-01` | 挂 DS-01 / DS-02，**不另开一级菜单**。**报价表划掉且工作量为 0 的「维护技术图谱」不实现** | 计划 11-06 → 11-07 |

> **页数口径未统一（待定项）**：`formal-docs-registry.yaml` 记 **34 页**（M1 态势 9 页），`ARCH-DISPLAY-01.md` §6.3 记 **35 页**（trend 10 页）。差异应在于 `/trend/maintain/*`（本表 WBS-05-24）是否计入展示页。**会签前需定口径**；定之前本表两说并列，不自选一个。

### 4.1a WBS-05-04 的子任务（科技数据资源四视窗 · 对照已建成 GDF）

> 2026-11-02 建叶。父行仍是 WBS-05-04 · `SYSINT-05-04-L01`（四视窗页面交付）。本行只分析四个视窗的展示需求里，哪些能从已建成的 GDF 平台得到。不代替父行，不新开 GDF 派单包。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-04-01 · `SYSINT-05-04-01-L01` | 科技数据资源四视窗：对照已建成 GDF，分析哪些展示需求可从平台得到 | 淮政玮 | `gkx-orchestration` | **done**（2026-11-03 `human:淮政玮` 签收） | 已签收。结论见 [SYSINT-05-04-01-L01.md](../../../agent-handoffs/SYSINT-05-04-01-L01.md)：70 条里可得到 0、部分得到 29、得不到 41，没有一条能直接填进四视窗 | 需求清单认详设 `07-功能-科技数据资源.md` 与 `科技数据资源-DR/DR-模块开发规划与任务拆分.md` §4（DS-17～20，seq 330–399）。不等 `SYSINT-05-04-L01` 页面做完。分析结论落盘即本叶完成，不是可对端，不新建 GDF 作业 | 无截至时间 |

### 4.1a2 科技数据资源后台接口

> 2026-11-03 方案：[方案-科技数据资源-后台接口.md](./方案-科技数据资源-后台接口.md)。总控：[DR-RES-长任务总控.md](../../../agent-handoffs/科技数据资源-DR/DR-RES-长任务总控.md)。对外只四个 `GET /display/v1/data-ops/{overview|access|theme|application}/dataset`。表在 `demo_gkxlumenx_ads`，表名 `gapfill_dr_*`。签收条件按 D18。监管人淮政玮。`lumen-svc-platform` 同仓一次只派一叶。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 |
|---|---|---|---|---|
| WBS-05-04-02 · `DR-RES-A0-L01` | 复读久新现网列，确认 `entityStock` / `columnCatalog` 列名 | 淮政玮 | `gkx-orchestration` | 已建单，与契约并行 |
| — · `BE-DR-CONTRACT-01` | 冻结四个 Dataset 路径、信封、键名与 `origin`。不新开契约号 | 淮政玮 | `gkx-orchestration` | 已有单，与 A0 并行 |
| WBS-05-04-03 · `DR-RES-MOCK-DDL-L01` | 在 `demo_gkxlumenx_ads` 建 `gapfill_dr_*` | 淮政玮 | `gkx-orchestration` | 已建单，等 A0 |
| WBS-05-04-04 · `DR-RES-MOCK-LOAD-L01` | Python 灌 `mock_` 行，并按需写 `snap_` | 淮政玮 | `gkx-orchestration` | 已建单，等 DDL |
| WBS-05-04-05 · `DR-RES-C1-L01` | `GET .../overview/dataset` | 淮政玮 | `lumen-svc-platform` | 已建单，等契约和灌数 |
| WBS-05-04-06 · `DR-RES-C2-L01` | `GET .../access/dataset` | 淮政玮 | `lumen-svc-platform` | 已建单，等 C1 |
| WBS-05-04-07 · `DR-RES-C3-L01` | `GET .../theme/dataset` | 淮政玮 | `lumen-svc-platform` | 已建单，等 C2 |
| WBS-05-04-08 · `DR-RES-C4-L01` | `GET .../application/dataset` | 淮政玮 | `lumen-svc-platform` | 已建单，等 C3 |
| WBS-05-04-09 · `DR-RES-D1-L01` | 四条 `real()` 改走 `request()`，MockBadge 看 `origin` | 淮政玮 | `lumen-ui-science-pc` | 已建单，等 C1–C4 到 integration。不自动 push |

### 4.1b WBS-05-23 的子任务（科技政策跟踪 · 只挂已有单）

> 2026-11-03 挂接。父行仍是 WBS-05-23。编写顺序是 05-23-14 调研 → 05-23-15 系统详细设计 → 05-23-02 契约。编号按建单先后，不表示施工先后。依赖全文见 [对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md)。
> mock 复刻链：`FE-POL-S01` → 各页；只有 `FE-POL-01B` 再硬依赖 `FE-POL-01A`。真数链在详设和契约之后。专题 `E-E7-POLICY-M1-L06` 不进下表。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-23-01 · `FE-POL-S01` | 政策跟踪前端基座（菜单 3→7、mock 种子、api 双轨、35 指标镜像） | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-S01.md`。registry note 写已推 `origin/dev`、转待测试；handoff 头仍写停本地。状态以 registry 为准 | 无硬依赖。产品包 `DS10-12-PACK-L01` 已完成 | 无截至时间 |
| WBS-05-23-02 · `BE-POL-CONTRACT-01` | 7 页 63 叶 Java 契约（API-POL）。只出接口契约，不是系统详细设计 | 李伟 | `lumen-svc-platform` | **backlog** | 未开工。规划 `科技政策跟踪-POL/POLICY-模块开发规划与任务拆分.md` §3.1。§4.1c 的 26 份接口分册是输入，本单仍只冻一份 API-POL | WBS 前置是 `POL-DISPLAY-SDD-L01`，并收齐 §4.1c 各二级 `*-API`。注册表 `depends_on` 仍为空（更新工具不能写该字段）。冻结前 FE 不猜路径 | 无截至时间 |
| WBS-05-23-03 · `FE-POL-01A` | 科创政策全景 · 检索主链路 | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-01A.md`。走查后已推 `origin/dev` | 硬依赖 `FE-POL-S01` | 无截至时间 |
| WBS-05-23-04 · `FE-POL-01B` | 科创政策全景 · 动向 / 舆情 / 比对 / 订阅 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-01B.md`。note 写前端链路联调通过，状态仍为联调中 | 硬依赖 `FE-POL-01A` | 无截至时间 |
| WBS-05-23-05 · `FE-POL-02A` | 政策分析评价整页 | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-02A.md`。已推 `origin/dev` | 硬依赖 `FE-POL-S01`。与全景无硬依赖 | 无截至时间 |
| WBS-05-23-06 · `FE-POL-03A` | 政策效果推演整页 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-03A.md`。停本地待验收 | 硬依赖 `FE-POL-S01`。模型未注册则真路径 501 | 无截至时间 |
| WBS-05-23-07 · `FE-POL-04A` | 智能政策库构建（政策数据治理） | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-04A.md` 已入库 | 硬依赖 `FE-POL-S01`。ChainSteps 归本单，06A/07A 的占位等本单合入后替换 | 无截至时间 |
| WBS-05-23-08 · `FE-POL-05A` | 智能政策拆解 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-05A.md` 已入库 | 硬依赖 `FE-POL-S01`。文本解析模型未注册则 501 | 无截至时间 |
| WBS-05-23-09 · `FE-POL-06A` | 多维政策对比 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-06A.md`。停 worktree 待验收 | 硬依赖 `FE-POL-S01`。生成研报跳 07A，须两边合入同一 `dev` 再验 | 无截至时间 |
| WBS-05-23-10 · `FE-POL-07A` | 智能研报生成 | 孔东 | `lumen-ui-science-pc` | **ready_to_sign** | handoff `科技政策跟踪-POL/FE-POL-07A.md` 已入库。文件头仍写停本地，状态以 registry 为准 | 硬依赖 `FE-POL-S01`。Job 未注册则导出 501 | 无截至时间 |
| WBS-05-23-11 · `BE-POL-IMPL-01` | 展示聚合接口实现（`/display/v1/policy/**`） | 李伟 | `lumen-svc-platform` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-CONTRACT-01`。契约未冻结不开工。不实现、不转调 `/topic/v1/policy` | 无截至时间 |
| WBS-05-23-12 · `BE-POL-DATA-01` | 统计读面与已有政策 ADS 对齐 | 李伟 | `gkx-orchestration` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-CONTRACT-01`、`GDF-POLICY-MDC-STAT-L01`。不新开 GDF 包，不写第二套统计脚本 | 无截至时间 |
| WBS-05-23-13 · `FE-POL-REAL-01` | 七页切真实接口并联调 | 孔东 | `lumen-ui-science-pc` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-IMPL-01`、`BE-POL-DATA-01` 与 `FE-POL-01B`、`02A`、`03A`、`04A`、`05A`、`06A`、`07A`。模型未注册保持 501 | 无截至时间 |
| WBS-05-23-14 · `POL-DISPLAY-SURVEY-L01` | 存量调研定稿（四叶合成） | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 四叶已合成。定稿在对照文件第 7 节 | 四叶 handoff 已齐 | 无截至时间 |
| WBS-05-23-16 · `POL-DISPLAY-SURVEY-DS10-L01` | 调研分册 · 科创政策全景 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。能力表 24 行：可接 9，501 共 13，跨项 2 | 无前置。与 17～19 并行 | 无截至时间 |
| WBS-05-23-17 · `POL-DISPLAY-SURVEY-DS11-L01` | 调研分册 · 政策分析评价 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。可接 2，501 共 9，跨项 1。5 行交互壳记未见 | 无前置 | 无截至时间 |
| WBS-05-23-18 · `POL-DISPLAY-SURVEY-DS12-L01` | 调研分册 · 政策效果推演 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。12 条：501 共 10，跨项索引 2，可接统计读面 0 | 无前置。推演与布局推荐分键 | 无截至时间 |
| WBS-05-23-19 · `POL-DISPLAY-SURVEY-PC-L01` | 调研分册 · 核增四页合一 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。可接 0，501 共 12，跨项 5 | 无前置 | 无截至时间 |
| WBS-05-23-15 · `POL-DISPLAY-SDD-L01` | 系统详细设计说明书（三叶合成） | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 已合成 `sdd/科技政策跟踪-系统详细设计说明书.md`。会签未完成。不写 OpenAPI | 三叶 handoff 已齐 | 无截至时间 |
| WBS-05-23-20 · `POL-DISPLAY-SDD-CHAIN-L01` | 详设分册 · 调用链与边界 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。同步读 ADS；Job 未注册则 501。L06 不是展示实现路径 | 调研父单 handoff 已落盘 | 无截至时间 |
| WBS-05-23-21 · `POL-DISPLAY-SDD-METRIC-L01` | 详设分册 · 指标与 501 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。评价 5 行交互壳并入 501。推演与布局推荐分键 | 同上。与 20、22 并行 | 无截至时间 |
| WBS-05-23-22 · `POL-DISPLAY-SDD-INPUT-L01` | 详设分册 · 契约输入清单 | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-03 分册已落盘。25 条资源，不写字段表 | 同上 | 无截至时间 |

### 4.1c WBS-05-23 的二级设计（科技政策跟踪 · 按 SRS level5）

> 2026-11-03 拆解。一级 = SRS 四级页（7）。二级 = SRS `level5`（26）。核增页的叶子标题是「/」，二级名用 `level5`，所以治理、拆解、对比、研报按叶子各成一个二级。每个二级 4 张定义单，不写代码。
>
> 四单顺序：架构（分析、架构、整体流程）先行；接口、指标、数据三单读本二级架构单，彼此并行。二级之间无硬依赖。四单监管人一律 `human:淮政玮`。角色仍是 `arch-agent` / `api-agent` / `algorithm-agent` / `data-agent`。
>
> 不替代 §4.1b。`BE-POL-CONTRACT-01` 仍是唯一 API-POL 冻结口，26 份接口分册只作它的输入。`BE-POL-IMPL-01`、`BE-POL-DATA-01`、`FE-POL-REAL-01` 仍是实现与联调，不在本表重开。不新造指标，不重开 GDF，不消费 `/topic/v1/policy`，推演不含布局推荐。
>
> 注册表状态以建单结果为准。2026-11-03 起本表监管人一律淮政玮，与 registry `supervised_by` 一致。角色不改。

| 一级 | 二级 | SRS 序号 | 四单 |
|---|---|---|---|
| DS-10 科创政策全景 | 多维检索查询 | 197–202 | `POL-L2-DS10-QRY-ARCH` / `POL-L2-DS10-QRY-API` / `POL-L2-DS10-QRY-METRIC` / `POL-L2-DS10-QRY-DATA` |
| DS-10 科创政策全景 | 政策动向跟踪 | 203–206 | `POL-L2-DS10-TREND-ARCH` / `POL-L2-DS10-TREND-API` / `POL-L2-DS10-TREND-METRIC` / `POL-L2-DS10-TREND-DATA` |
| DS-10 科创政策全景 | 政策舆情评估 | 207–212 | `POL-L2-DS10-SENT-ARCH` / `POL-L2-DS10-SENT-API` / `POL-L2-DS10-SENT-METRIC` / `POL-L2-DS10-SENT-DATA` |
| DS-10 科创政策全景 | 政策重点比对 | 213–218 | `POL-L2-DS10-CMP-ARCH` / `POL-L2-DS10-CMP-API` / `POL-L2-DS10-CMP-METRIC` / `POL-L2-DS10-CMP-DATA` |
| DS-11 政策分析评价 | 政策分析报告可视化呈现 | 219–222 | `POL-L2-DS11-VIZ-ARCH` / `POL-L2-DS11-VIZ-API` / `POL-L2-DS11-VIZ-METRIC` / `POL-L2-DS11-VIZ-DATA` |
| DS-11 政策分析评价 | 结果解读报告多维展示 | 223–226 | `POL-L2-DS11-READ-ARCH` / `POL-L2-DS11-READ-API` / `POL-L2-DS11-READ-METRIC` / `POL-L2-DS11-READ-DATA` |
| DS-11 政策分析评价 | 推荐方案报告交互展示 | 227–231 | `POL-L2-DS11-PLAN-ARCH` / `POL-L2-DS11-PLAN-API` / `POL-L2-DS11-PLAN-METRIC` / `POL-L2-DS11-PLAN-DATA` |
| DS-12 政策效果推演 | 效果预估 | 232–236 | `POL-L2-DS12-EST-ARCH` / `POL-L2-DS12-EST-API` / `POL-L2-DS12-EST-METRIC` / `POL-L2-DS12-EST-DATA` |
| DS-12 政策效果推演 | 科技政策推演 | 237–242 | `POL-L2-DS12-SIM-ARCH` / `POL-L2-DS12-SIM-API` / `POL-L2-DS12-SIM-METRIC` / `POL-L2-DS12-SIM-DATA` |
| PC-1 政策数据治理 | 系统引用政策源数据清洗 | 602 | `POL-L2-PC1-CLEAN-ARCH` / `POL-L2-PC1-CLEAN-API` / `POL-L2-PC1-CLEAN-METRIC` / `POL-L2-PC1-CLEAN-DATA` |
| PC-1 政策数据治理 | 政策库结构化 | 603 | `POL-L2-PC1-STRUCT-ARCH` / `POL-L2-PC1-STRUCT-API` / `POL-L2-PC1-STRUCT-METRIC` / `POL-L2-PC1-STRUCT-DATA` |
| PC-1 政策数据治理 | 溯源索引构建 | 604 | `POL-L2-PC1-LINEAGE-ARCH` / `POL-L2-PC1-LINEAGE-API` / `POL-L2-PC1-LINEAGE-METRIC` / `POL-L2-PC1-LINEAGE-DATA` |
| PC-1 政策数据治理 | 规划指标库搭建 | 605 | `POL-L2-PC1-INDLIB-ARCH` / `POL-L2-PC1-INDLIB-API` / `POL-L2-PC1-INDLIB-METRIC` / `POL-L2-PC1-INDLIB-DATA` |
| PC-2 智能政策拆解 | 政策语义理解 | 606 | `POL-L2-PC2-SEM-ARCH` / `POL-L2-PC2-SEM-API` / `POL-L2-PC2-SEM-METRIC` / `POL-L2-PC2-SEM-DATA` |
| PC-2 智能政策拆解 | 条款精细化拆解 | 607 | `POL-L2-PC2-CLAUSE-ARCH` / `POL-L2-PC2-CLAUSE-API` / `POL-L2-PC2-CLAUSE-METRIC` / `POL-L2-PC2-CLAUSE-DATA` |
| PC-2 智能政策拆解 | 关键指标自动提取 | 608 | `POL-L2-PC2-EXTRACT-ARCH` / `POL-L2-PC2-EXTRACT-API` / `POL-L2-PC2-EXTRACT-METRIC` / `POL-L2-PC2-EXTRACT-DATA` |
| PC-2 智能政策拆解 | 政策实体关联 | 609 | `POL-L2-PC2-ENT-ARCH` / `POL-L2-PC2-ENT-API` / `POL-L2-PC2-ENT-METRIC` / `POL-L2-PC2-ENT-DATA` |
| PC-3 多维政策对比 | 跨政策交叉对比 | 610 | `POL-L2-PC3-XCMP-ARCH` / `POL-L2-PC3-XCMP-API` / `POL-L2-PC3-XCMP-METRIC` / `POL-L2-PC3-XCMP-DATA` |
| PC-3 多维政策对比 | 可视化分析呈现 | 611 | `POL-L2-PC3-VIZ-ARCH` / `POL-L2-PC3-VIZ-API` / `POL-L2-PC3-VIZ-METRIC` / `POL-L2-PC3-VIZ-DATA` |
| PC-3 多维政策对比 | 交互式对比配置 | 612 | `POL-L2-PC3-CFG-ARCH` / `POL-L2-PC3-CFG-API` / `POL-L2-PC3-CFG-METRIC` / `POL-L2-PC3-CFG-DATA` |
| PC-3 多维政策对比 | 结果智能输出 | 613 | `POL-L2-PC3-OUT-ARCH` / `POL-L2-PC3-OUT-API` / `POL-L2-PC3-OUT-METRIC` / `POL-L2-PC3-OUT-DATA` |
| PC-4 智能研报生成 | 政策深度分析 | 614 | `POL-L2-PC4-DEEP-ARCH` / `POL-L2-PC4-DEEP-API` / `POL-L2-PC4-DEEP-METRIC` / `POL-L2-PC4-DEEP-DATA` |
| PC-4 智能研报生成 | 洞察结论自动提炼 | 615 | `POL-L2-PC4-INSIGHT-ARCH` / `POL-L2-PC4-INSIGHT-API` / `POL-L2-PC4-INSIGHT-METRIC` / `POL-L2-PC4-INSIGHT-DATA` |
| PC-4 智能研报生成 | 模块化研报自动撰写 | 616 | `POL-L2-PC4-WRITE-ARCH` / `POL-L2-PC4-WRITE-API` / `POL-L2-PC4-WRITE-METRIC` / `POL-L2-PC4-WRITE-DATA` |
| PC-4 智能研报生成 | 研报溯源展示 | 617 | `POL-L2-PC4-TRACE-ARCH` / `POL-L2-PC4-TRACE-API` / `POL-L2-PC4-TRACE-METRIC` / `POL-L2-PC4-TRACE-DATA` |
| PC-4 智能研报生成 | 结果智能输出 | 618 | `POL-L2-PC4-OUT-ARCH` / `POL-L2-PC4-OUT-API` / `POL-L2-PC4-OUT-METRIC` / `POL-L2-PC4-OUT-DATA` |

一级 7，二级 26，定义单 104。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-23-L2-01A · `POL-L2-DS10-QRY-ARCH` | 科创政策全景 · 多维检索查询 · 后台实现架构设计（序号 197–202） | 淮政玮 | `gkx-orchestration` | **integration** | 架构稿 `sdd/l2/POL-L2-DS10-QRY-ARCH.md`。197、198、200 同步读面；199、201、202 为 501。会签未完成 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-01B · `POL-L2-DS10-QRY-API` | 科创政策全景 · 多维检索查询 · 后台接口设计（序号 197–202） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。检索目录同步读面。智能排序、收藏、导出为 501 | 硬依赖本二级 `POL-L2-DS10-QRY-ARCH` | 无截至时间 |
| WBS-05-23-L2-01C · `POL-L2-DS10-QRY-METRIC` | 科创政策全景 · 多维检索查询 · 后台指标设计（序号 197–202） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。检索目录同步读面。智能排序、收藏、导出为 501 | 硬依赖本二级 `POL-L2-DS10-QRY-ARCH` | 无截至时间 |
| WBS-05-23-L2-01D · `POL-L2-DS10-QRY-DATA` | 科创政策全景 · 多维检索查询 · 后台数据架构设计（序号 197–202） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。检索目录同步读面。智能排序、收藏、导出为 501 | 硬依赖本二级 `POL-L2-DS10-QRY-ARCH` | 无截至时间 |
| WBS-05-23-L2-02A · `POL-L2-DS10-TREND-ARCH` | 科创政策全景 · 政策动向跟踪 · 后台实现架构设计（序号 203–206） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。来源监控跨项索引第 6 项。订阅 501。趋势可接，热点、影响、深度报告 501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-02B · `POL-L2-DS10-TREND-API` | 科创政策全景 · 政策动向跟踪 · 后台接口设计（序号 203–206） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。来源监控跨项索引第 6 项。订阅 501。趋势可接，热点、影响、深度报告 501 | 硬依赖本二级 `POL-L2-DS10-TREND-ARCH` | 无截至时间 |
| WBS-05-23-L2-02C · `POL-L2-DS10-TREND-METRIC` | 科创政策全景 · 政策动向跟踪 · 后台指标设计（序号 203–206） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。来源监控跨项索引第 6 项。订阅 501。趋势可接，热点、影响、深度报告 501 | 硬依赖本二级 `POL-L2-DS10-TREND-ARCH` | 无截至时间 |
| WBS-05-23-L2-02D · `POL-L2-DS10-TREND-DATA` | 科创政策全景 · 政策动向跟踪 · 后台数据架构设计（序号 203–206） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。来源监控跨项索引第 6 项。订阅 501。趋势可接，热点、影响、深度报告 501 | 硬依赖本二级 `POL-L2-DS10-TREND-ARCH` | 无截至时间 |
| WBS-05-23-L2-03A · `POL-L2-DS10-SENT-ARCH` | 科创政策全景 · 政策舆情评估 · 后台实现架构设计（序号 207–212） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-03 按说明书第 11 节签收。209、212 读已有 ADS。210、211 只读 gapfill 表。不用 501，接口不直接返回 mock | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-03B · `POL-L2-DS10-SENT-API` | 科创政策全景 · 政策舆情评估 · 后台接口设计（序号 207–212） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。查询对比可接统计。区域差异跨项读图。效果跟踪、反馈、评估报告、匹配为 501 | 硬依赖本二级 `POL-L2-DS10-SENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-03C · `POL-L2-DS10-SENT-METRIC` | 科创政策全景 · 政策舆情评估 · 后台指标设计（序号 207–212） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。查询对比可接统计。区域差异跨项读图。效果跟踪、反馈、评估报告、匹配为 501 | 硬依赖本二级 `POL-L2-DS10-SENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-03D · `POL-L2-DS10-SENT-DATA` | 科创政策全景 · 政策舆情评估 · 后台数据架构设计（序号 207–212） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。查询对比可接统计。区域差异跨项读图。效果跟踪、反馈、评估报告、匹配为 501 | 硬依赖本二级 `POL-L2-DS10-SENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-04A · `POL-L2-DS10-CMP-ARCH` | 科创政策全景 · 政策重点比对 · 后台实现架构设计（序号 213–218） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。部门件数、标杆力度可接。新旧对比、详情对比、对标报告、可视化为 501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-04B · `POL-L2-DS10-CMP-API` | 科创政策全景 · 政策重点比对 · 后台接口设计（序号 213–218） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。部门件数、标杆力度可接。新旧对比、详情对比、对标报告、可视化为 501 | 硬依赖本二级 `POL-L2-DS10-CMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-04C · `POL-L2-DS10-CMP-METRIC` | 科创政策全景 · 政策重点比对 · 后台指标设计（序号 213–218） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。部门件数、标杆力度可接。新旧对比、详情对比、对标报告、可视化为 501 | 硬依赖本二级 `POL-L2-DS10-CMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-04D · `POL-L2-DS10-CMP-DATA` | 科创政策全景 · 政策重点比对 · 后台数据架构设计（序号 213–218） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。部门件数、标杆力度可接。新旧对比、详情对比、对标报告、可视化为 501 | 硬依赖本二级 `POL-L2-DS10-CMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-05A · `POL-L2-DS11-VIZ-ARCH` | 政策分析评价 · 政策分析报告可视化呈现 · 后台实现架构设计（序号 219–222） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 2026-11-03 返工后第二轮四角色同意，同日淮政玮签收。219、220 各一次同步 `jobs`。222 读 `gapfill_policy_eval_template` | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-05B · `POL-L2-DS11-VIZ-API` | 政策分析评价 · 政策分析报告可视化呈现 · 后台接口设计（序号 219–222） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-05C · `POL-L2-DS11-VIZ-METRIC` | 政策分析评价 · 政策分析报告可视化呈现 · 后台指标设计（序号 219–222） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-05D · `POL-L2-DS11-VIZ-DATA` | 政策分析评价 · 政策分析报告可视化呈现 · 后台数据架构设计（序号 219–222） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-06A · `POL-L2-DS11-READ-ARCH` | 政策分析评价 · 结果解读报告多维展示 · 后台实现架构设计（序号 223–226） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。短板条数可接。焦点指数 501。解读、多媒体壳、摘要 501。机遇条数无本段序号，不挂进本二级 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-06B · `POL-L2-DS11-READ-API` | 政策分析评价 · 结果解读报告多维展示 · 后台接口设计（序号 223–226） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。短板条数可接。焦点指数 501。解读、多媒体壳、摘要 501。机遇条数无本段序号，不挂进本二级 | 硬依赖本二级 `POL-L2-DS11-READ-ARCH` | 无截至时间 |
| WBS-05-23-L2-06C · `POL-L2-DS11-READ-METRIC` | 政策分析评价 · 结果解读报告多维展示 · 后台指标设计（序号 223–226） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。短板条数可接。焦点指数 501。解读、多媒体壳、摘要 501。机遇条数无本段序号，不挂进本二级 | 硬依赖本二级 `POL-L2-DS11-READ-ARCH` | 无截至时间 |
| WBS-05-23-L2-06D · `POL-L2-DS11-READ-DATA` | 政策分析评价 · 结果解读报告多维展示 · 后台数据架构设计（序号 223–226） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。短板条数可接。焦点指数 501。解读、多媒体壳、摘要 501。机遇条数无本段序号，不挂进本二级 | 硬依赖本二级 `POL-L2-DS11-READ-ARCH` | 无截至时间 |
| WBS-05-23-L2-07A · `POL-L2-DS11-PLAN-ARCH` | 政策分析评价 · 推荐方案报告交互展示 · 后台实现架构设计（序号 227–231） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 架构稿 `sdd/l2/POL-L2-DS11-PLAN-ARCH.md`。227–231 读 `gapfill_policy_eval_scheme`。2026-11-03 两轮四角色同意并签收 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-07B · `POL-L2-DS11-PLAN-API` | 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计（序号 227–231） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-PLAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-07C · `POL-L2-DS11-PLAN-METRIC` | 政策分析评价 · 推荐方案报告交互展示 · 后台指标设计（序号 227–231） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-PLAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-07D · `POL-L2-DS11-PLAN-DATA` | 政策分析评价 · 推荐方案报告交互展示 · 后台数据架构设计（序号 227–231） | 淮政玮 | `gkx-orchestration` | **done** ✅ 2026-11-03 签收 | 定义单已完成并签收（四角色 12 页会签在 `sdd/l2/会签/`） | 硬依赖本二级 `POL-L2-DS11-PLAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-08A · `POL-L2-DS12-EST-ARCH` | 政策效果推演 · 效果预估 · 后台实现架构设计（序号 232–236） | 淮政玮 | `gkx-orchestration` | **integration** | 架构稿已会签同意。只认 M_POLICY_SIMULATE。布局推荐不在 232–236。未签收 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘 | 无截至时间 |
| WBS-05-23-L2-08B · `POL-L2-DS12-EST-API` | 政策效果推演 · 效果预估 · 后台接口设计（序号 232–236） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-EST-ARCH` | 无截至时间 |
| WBS-05-23-L2-08C · `POL-L2-DS12-EST-METRIC` | 政策效果推演 · 效果预估 · 后台指标设计（序号 232–236） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-EST-ARCH` | 无截至时间 |
| WBS-05-23-L2-08D · `POL-L2-DS12-EST-DATA` | 政策效果推演 · 效果预估 · 后台数据架构设计（序号 232–236） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-EST-ARCH` | 无截至时间 |
| WBS-05-23-L2-08E · `POL-L2-DS12-WIRING-L01` | 政策效果推演 · 效果预估 · 前端接线（序号 232–236，唯一 POST /display/v1/policy/simulation/jobs） | 淮政玮 | `lumen-ui-science-pc` | **integration** | 2026-11-06 页面接线已在 `de8bef7`。与 09E 同一张单：一个页面、一个 jobs。不另开第二张接线单 | 硬依赖 `POL-L2-DS12-EST-GAPFILL-L01`、`POL-L2-DS12-JOBS-IMPL-JAVA`（均已 done） | 无截至时间 |
| WBS-05-23-L2-08F · `POL-L2-DS12-EST-TEST-L01` | 政策效果推演 · 效果预估 · 单元测试用例（合规交付主路径数据准备 + 关键路径验证 + 界面操作过程与截图） | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-06 用例与 11 张截图已落盘。`--check` 通过，未 `--apply`。线上 jobs 404，本机 401 | 硬依赖 `POL-L2-DS12-EST-GAPFILL-L01`、`POL-L2-DS12-JOBS-IMPL-JAVA`（均已 done） | 无截至时间 |
| WBS-05-23-L2-09A · `POL-L2-DS12-SIM-ARCH` | 政策效果推演 · 科技政策推演 · 后台实现架构设计（序号 237–242） | 淮政玮 | `gkx-orchestration` | **integration** | 架构稿已会签同意。237 读已有文本解析行。240 无资源。242 只正文。未签收 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘 | 无截至时间 |
| WBS-05-23-L2-09B · `POL-L2-DS12-SIM-API` | 政策效果推演 · 科技政策推演 · 后台接口设计（序号 237–242） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-SIM-ARCH` | 无截至时间 |
| WBS-05-23-L2-09C · `POL-L2-DS12-SIM-METRIC` | 政策效果推演 · 科技政策推演 · 后台指标设计（序号 237–242） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-SIM-ARCH` | 无截至时间 |
| WBS-05-23-L2-09D · `POL-L2-DS12-SIM-DATA` | 政策效果推演 · 科技政策推演 · 后台数据架构设计（序号 237–242） | 淮政玮 | `gkx-orchestration` | **done** | 2026-11-06 淮政玮签收 | 硬依赖本二级 `POL-L2-DS12-SIM-ARCH` | 无截至时间 |
| WBS-05-23-L2-09E · `POL-L2-DS12-WIRING-L01` | 政策效果推演 · 科技政策推演 · 前端接线（序号 237–242，与 08E 同一张单） | 淮政玮 | `lumen-ui-science-pc` | **integration** | 同一个页面、同一个 jobs。240 不请求该接口。242 不提供文件下载 | 硬依赖 `POL-L2-DS12-SIM-GAPFILL-L01`、`POL-L2-DS12-JOBS-IMPL-JAVA`（均已 done） | 无截至时间 |
| WBS-05-23-L2-09F · `POL-L2-DS12-SIM-TEST-L01` | 政策效果推演 · 科技政策推演 · 单元测试用例（合规交付主路径数据准备 + 关键路径验证 + 界面操作过程与截图） | 淮政玮 | `gkx-orchestration` | **integration** | 2026-11-06 用例与 7 张截图已落盘。`--check` 通过，未 `--apply`。jobs 为 401 | 硬依赖 `POL-L2-DS12-SIM-GAPFILL-L01`、`POL-L2-DS12-JOBS-IMPL-JAVA`（均已 done） | 无截至时间 |
| WBS-05-23-L2-10A · `POL-L2-PC1-CLEAN-ARCH` | 政策数据治理 · 系统引用政策源数据清洗 · 后台实现架构设计（序号 602） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。只读第 6 项已有清洗结果，不重开 GDF | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-10B · `POL-L2-PC1-CLEAN-API` | 政策数据治理 · 系统引用政策源数据清洗 · 后台接口设计（序号 602） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。只读第 6 项已有清洗结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-CLEAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-10C · `POL-L2-PC1-CLEAN-METRIC` | 政策数据治理 · 系统引用政策源数据清洗 · 后台指标设计（序号 602） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。只读第 6 项已有清洗结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-CLEAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-10D · `POL-L2-PC1-CLEAN-DATA` | 政策数据治理 · 系统引用政策源数据清洗 · 后台数据架构设计（序号 602） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。只读第 6 项已有清洗结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-CLEAN-ARCH` | 无截至时间 |
| WBS-05-23-L2-11A · `POL-L2-PC1-STRUCT-ARCH` | 政策数据治理 · 政策库结构化 · 后台实现架构设计（序号 603） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。只读已结构化结果，不重开 GDF | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-11B · `POL-L2-PC1-STRUCT-API` | 政策数据治理 · 政策库结构化 · 后台接口设计（序号 603） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。只读已结构化结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-STRUCT-ARCH` | 无截至时间 |
| WBS-05-23-L2-11C · `POL-L2-PC1-STRUCT-METRIC` | 政策数据治理 · 政策库结构化 · 后台指标设计（序号 603） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。只读已结构化结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-STRUCT-ARCH` | 无截至时间 |
| WBS-05-23-L2-11D · `POL-L2-PC1-STRUCT-DATA` | 政策数据治理 · 政策库结构化 · 后台数据架构设计（序号 603） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。只读已结构化结果，不重开 GDF | 硬依赖本二级 `POL-L2-PC1-STRUCT-ARCH` | 无截至时间 |
| WBS-05-23-L2-12A · `POL-L2-PC1-LINEAGE-ARCH` | 政策数据治理 · 溯源索引构建 · 后台实现架构设计（序号 604） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。未见模型，501，不建实现任务 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-12B · `POL-L2-PC1-LINEAGE-API` | 政策数据治理 · 溯源索引构建 · 后台接口设计（序号 604） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-LINEAGE-ARCH` | 无截至时间 |
| WBS-05-23-L2-12C · `POL-L2-PC1-LINEAGE-METRIC` | 政策数据治理 · 溯源索引构建 · 后台指标设计（序号 604） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-LINEAGE-ARCH` | 无截至时间 |
| WBS-05-23-L2-12D · `POL-L2-PC1-LINEAGE-DATA` | 政策数据治理 · 溯源索引构建 · 后台数据架构设计（序号 604） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-LINEAGE-ARCH` | 无截至时间 |
| WBS-05-23-L2-13A · `POL-L2-PC1-INDLIB-ARCH` | 政策数据治理 · 规划指标库搭建 · 后台实现架构设计（序号 605） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。未见模型，501，不建实现任务 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-13B · `POL-L2-PC1-INDLIB-API` | 政策数据治理 · 规划指标库搭建 · 后台接口设计（序号 605） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-INDLIB-ARCH` | 无截至时间 |
| WBS-05-23-L2-13C · `POL-L2-PC1-INDLIB-METRIC` | 政策数据治理 · 规划指标库搭建 · 后台指标设计（序号 605） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-INDLIB-ARCH` | 无截至时间 |
| WBS-05-23-L2-13D · `POL-L2-PC1-INDLIB-DATA` | 政策数据治理 · 规划指标库搭建 · 后台数据架构设计（序号 605） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。未见模型，501，不建实现任务 | 硬依赖本二级 `POL-L2-PC1-INDLIB-ARCH` | 无截至时间 |
| WBS-05-23-L2-14A · `POL-L2-PC2-SEM-ARCH` | 智能政策拆解 · 政策语义理解 · 后台实现架构设计（序号 606） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。未见模型，501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-14B · `POL-L2-PC2-SEM-API` | 智能政策拆解 · 政策语义理解 · 后台接口设计（序号 606） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC2-SEM-ARCH` | 无截至时间 |
| WBS-05-23-L2-14C · `POL-L2-PC2-SEM-METRIC` | 智能政策拆解 · 政策语义理解 · 后台指标设计（序号 606） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC2-SEM-ARCH` | 无截至时间 |
| WBS-05-23-L2-14D · `POL-L2-PC2-SEM-DATA` | 智能政策拆解 · 政策语义理解 · 后台数据架构设计（序号 606） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC2-SEM-ARCH` | 无截至时间 |
| WBS-05-23-L2-15A · `POL-L2-PC2-CLAUSE-ARCH` | 智能政策拆解 · 条款精细化拆解 · 后台实现架构设计（序号 607） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。只呈现已落库条款树，跨项索引 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-15B · `POL-L2-PC2-CLAUSE-API` | 智能政策拆解 · 条款精细化拆解 · 后台接口设计（序号 607） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。只呈现已落库条款树，跨项索引 | 硬依赖本二级 `POL-L2-PC2-CLAUSE-ARCH` | 无截至时间 |
| WBS-05-23-L2-15C · `POL-L2-PC2-CLAUSE-METRIC` | 智能政策拆解 · 条款精细化拆解 · 后台指标设计（序号 607） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。只呈现已落库条款树，跨项索引 | 硬依赖本二级 `POL-L2-PC2-CLAUSE-ARCH` | 无截至时间 |
| WBS-05-23-L2-15D · `POL-L2-PC2-CLAUSE-DATA` | 智能政策拆解 · 条款精细化拆解 · 后台数据架构设计（序号 607） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。只呈现已落库条款树，跨项索引 | 硬依赖本二级 `POL-L2-PC2-CLAUSE-ARCH` | 无截至时间 |
| WBS-05-23-L2-16A · `POL-L2-PC2-EXTRACT-ARCH` | 智能政策拆解 · 关键指标自动提取 · 后台实现架构设计（序号 608） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。只呈现已落库提取结果，跨项索引 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-16B · `POL-L2-PC2-EXTRACT-API` | 智能政策拆解 · 关键指标自动提取 · 后台接口设计（序号 608） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。只呈现已落库提取结果，跨项索引 | 硬依赖本二级 `POL-L2-PC2-EXTRACT-ARCH` | 无截至时间 |
| WBS-05-23-L2-16C · `POL-L2-PC2-EXTRACT-METRIC` | 智能政策拆解 · 关键指标自动提取 · 后台指标设计（序号 608） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。只呈现已落库提取结果，跨项索引 | 硬依赖本二级 `POL-L2-PC2-EXTRACT-ARCH` | 无截至时间 |
| WBS-05-23-L2-16D · `POL-L2-PC2-EXTRACT-DATA` | 智能政策拆解 · 关键指标自动提取 · 后台数据架构设计（序号 608） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。只呈现已落库提取结果，跨项索引 | 硬依赖本二级 `POL-L2-PC2-EXTRACT-ARCH` | 无截至时间 |
| WBS-05-23-L2-17A · `POL-L2-PC2-ENT-ARCH` | 智能政策拆解 · 政策实体关联 · 后台实现架构设计（序号 609） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。只消费已有子图，Java 不写 nGQL | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-17B · `POL-L2-PC2-ENT-API` | 智能政策拆解 · 政策实体关联 · 后台接口设计（序号 609） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。只消费已有子图，Java 不写 nGQL | 硬依赖本二级 `POL-L2-PC2-ENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-17C · `POL-L2-PC2-ENT-METRIC` | 智能政策拆解 · 政策实体关联 · 后台指标设计（序号 609） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。只消费已有子图，Java 不写 nGQL | 硬依赖本二级 `POL-L2-PC2-ENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-17D · `POL-L2-PC2-ENT-DATA` | 智能政策拆解 · 政策实体关联 · 后台数据架构设计（序号 609） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。只消费已有子图，Java 不写 nGQL | 硬依赖本二级 `POL-L2-PC2-ENT-ARCH` | 无截至时间 |
| WBS-05-23-L2-18A · `POL-L2-PC3-XCMP-ARCH` | 多维政策对比 · 跨政策交叉对比 · 后台实现架构设计（序号 610） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。差异与冲突未见，501。表内件数复用全景分布，不新算 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-18B · `POL-L2-PC3-XCMP-API` | 多维政策对比 · 跨政策交叉对比 · 后台接口设计（序号 610） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。差异与冲突未见，501。表内件数复用全景分布，不新算 | 硬依赖本二级 `POL-L2-PC3-XCMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-18C · `POL-L2-PC3-XCMP-METRIC` | 多维政策对比 · 跨政策交叉对比 · 后台指标设计（序号 610） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。差异与冲突未见，501。表内件数复用全景分布，不新算 | 硬依赖本二级 `POL-L2-PC3-XCMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-18D · `POL-L2-PC3-XCMP-DATA` | 多维政策对比 · 跨政策交叉对比 · 后台数据架构设计（序号 610） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。差异与冲突未见，501。表内件数复用全景分布，不新算 | 硬依赖本二级 `POL-L2-PC3-XCMP-ARCH` | 无截至时间 |
| WBS-05-23-L2-19A · `POL-L2-PC3-VIZ-ARCH` | 多维政策对比 · 可视化分析呈现 · 后台实现架构设计（序号 611） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。未见模型，501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-19B · `POL-L2-PC3-VIZ-API` | 多维政策对比 · 可视化分析呈现 · 后台接口设计（序号 611） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-19C · `POL-L2-PC3-VIZ-METRIC` | 多维政策对比 · 可视化分析呈现 · 后台指标设计（序号 611） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-19D · `POL-L2-PC3-VIZ-DATA` | 多维政策对比 · 可视化分析呈现 · 后台数据架构设计（序号 611） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-VIZ-ARCH` | 无截至时间 |
| WBS-05-23-L2-20A · `POL-L2-PC3-CFG-ARCH` | 多维政策对比 · 交互式对比配置 · 后台实现架构设计（序号 612） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。未见模型，501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-20B · `POL-L2-PC3-CFG-API` | 多维政策对比 · 交互式对比配置 · 后台接口设计（序号 612） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-CFG-ARCH` | 无截至时间 |
| WBS-05-23-L2-20C · `POL-L2-PC3-CFG-METRIC` | 多维政策对比 · 交互式对比配置 · 后台指标设计（序号 612） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-CFG-ARCH` | 无截至时间 |
| WBS-05-23-L2-20D · `POL-L2-PC3-CFG-DATA` | 多维政策对比 · 交互式对比配置 · 后台数据架构设计（序号 612） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。未见模型，501 | 硬依赖本二级 `POL-L2-PC3-CFG-ARCH` | 无截至时间 |
| WBS-05-23-L2-21A · `POL-L2-PC3-OUT-ARCH` | 多维政策对比 · 结果智能输出 · 后台实现架构设计（序号 613） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。对比摘要导出未见，501。不是研报五叶 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-21B · `POL-L2-PC3-OUT-API` | 多维政策对比 · 结果智能输出 · 后台接口设计（序号 613） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。对比摘要导出未见，501。不是研报五叶 | 硬依赖本二级 `POL-L2-PC3-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-21C · `POL-L2-PC3-OUT-METRIC` | 多维政策对比 · 结果智能输出 · 后台指标设计（序号 613） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。对比摘要导出未见，501。不是研报五叶 | 硬依赖本二级 `POL-L2-PC3-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-21D · `POL-L2-PC3-OUT-DATA` | 多维政策对比 · 结果智能输出 · 后台数据架构设计（序号 613） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。对比摘要导出未见，501。不是研报五叶 | 硬依赖本二级 `POL-L2-PC3-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-22A · `POL-L2-PC4-DEEP-ARCH` | 智能研报生成 · 政策深度分析 · 后台实现架构设计（序号 614） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。五叶一个研报 Job，未注册则 501。不是全景对标报告 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-22B · `POL-L2-PC4-DEEP-API` | 智能研报生成 · 政策深度分析 · 后台接口设计（序号 614） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。五叶一个研报 Job，未注册则 501。不是全景对标报告 | 硬依赖本二级 `POL-L2-PC4-DEEP-ARCH` | 无截至时间 |
| WBS-05-23-L2-22C · `POL-L2-PC4-DEEP-METRIC` | 智能研报生成 · 政策深度分析 · 后台指标设计（序号 614） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。五叶一个研报 Job，未注册则 501。不是全景对标报告 | 硬依赖本二级 `POL-L2-PC4-DEEP-ARCH` | 无截至时间 |
| WBS-05-23-L2-22D · `POL-L2-PC4-DEEP-DATA` | 智能研报生成 · 政策深度分析 · 后台数据架构设计（序号 614） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。五叶一个研报 Job，未注册则 501。不是全景对标报告 | 硬依赖本二级 `POL-L2-PC4-DEEP-ARCH` | 无截至时间 |
| WBS-05-23-L2-23A · `POL-L2-PC4-INSIGHT-ARCH` | 智能研报生成 · 洞察结论自动提炼 · 后台实现架构设计（序号 615） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。同一个研报 Job，未注册则 501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-23B · `POL-L2-PC4-INSIGHT-API` | 智能研报生成 · 洞察结论自动提炼 · 后台接口设计（序号 615） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-INSIGHT-ARCH` | 无截至时间 |
| WBS-05-23-L2-23C · `POL-L2-PC4-INSIGHT-METRIC` | 智能研报生成 · 洞察结论自动提炼 · 后台指标设计（序号 615） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-INSIGHT-ARCH` | 无截至时间 |
| WBS-05-23-L2-23D · `POL-L2-PC4-INSIGHT-DATA` | 智能研报生成 · 洞察结论自动提炼 · 后台数据架构设计（序号 615） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-INSIGHT-ARCH` | 无截至时间 |
| WBS-05-23-L2-24A · `POL-L2-PC4-WRITE-ARCH` | 智能研报生成 · 模块化研报自动撰写 · 后台实现架构设计（序号 616） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。同一个研报 Job，未注册则 501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-24B · `POL-L2-PC4-WRITE-API` | 智能研报生成 · 模块化研报自动撰写 · 后台接口设计（序号 616） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-WRITE-ARCH` | 无截至时间 |
| WBS-05-23-L2-24C · `POL-L2-PC4-WRITE-METRIC` | 智能研报生成 · 模块化研报自动撰写 · 后台指标设计（序号 616） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-WRITE-ARCH` | 无截至时间 |
| WBS-05-23-L2-24D · `POL-L2-PC4-WRITE-DATA` | 智能研报生成 · 模块化研报自动撰写 · 后台数据架构设计（序号 616） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-WRITE-ARCH` | 无截至时间 |
| WBS-05-23-L2-25A · `POL-L2-PC4-TRACE-ARCH` | 智能研报生成 · 研报溯源展示 · 后台实现架构设计（序号 617） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。同一个研报 Job，未注册则 501 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-25B · `POL-L2-PC4-TRACE-API` | 智能研报生成 · 研报溯源展示 · 后台接口设计（序号 617） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-TRACE-ARCH` | 无截至时间 |
| WBS-05-23-L2-25C · `POL-L2-PC4-TRACE-METRIC` | 智能研报生成 · 研报溯源展示 · 后台指标设计（序号 617） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-TRACE-ARCH` | 无截至时间 |
| WBS-05-23-L2-25D · `POL-L2-PC4-TRACE-DATA` | 智能研报生成 · 研报溯源展示 · 后台数据架构设计（序号 617） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。同一个研报 Job，未注册则 501 | 硬依赖本二级 `POL-L2-PC4-TRACE-ARCH` | 无截至时间 |
| WBS-05-23-L2-26A · `POL-L2-PC4-OUT-ARCH` | 智能研报生成 · 结果智能输出 · 后台实现架构设计（序号 618） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `arch-agent`。同一个研报 Job，未注册则 501。不是对比页的结果智能输出 | 硬依赖 `POL-DISPLAY-SDD-L01` 说明书已落盘。会签未完成不挡起草 | 无截至时间 |
| WBS-05-23-L2-26B · `POL-L2-PC4-OUT-API` | 智能研报生成 · 结果智能输出 · 后台接口设计（序号 618） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `api-agent`。同一个研报 Job，未注册则 501。不是对比页的结果智能输出 | 硬依赖本二级 `POL-L2-PC4-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-26C · `POL-L2-PC4-OUT-METRIC` | 智能研报生成 · 结果智能输出 · 后台指标设计（序号 618） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `algorithm-agent`。同一个研报 Job，未注册则 501。不是对比页的结果智能输出 | 硬依赖本二级 `POL-L2-PC4-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-26D · `POL-L2-PC4-OUT-DATA` | 智能研报生成 · 结果智能输出 · 后台数据架构设计（序号 618） | 淮政玮 | `gkx-orchestration` | **backlog** | 定义单，角色 `data-agent`。同一个研报 Job，未注册则 501。不是对比页的结果智能输出 | 硬依赖本二级 `POL-L2-PC4-OUT-ARCH` | 无截至时间 |
| WBS-05-23-L2-06E · `POL-L2-DS11-READ-WIRING-L01` | DS11 结果解读报告多维展示 · 前端接线（/display/v1/policy/evaluation/** 三端点接入） | 淮政玮 | `lumen-ui-science-pc` | **ready** | 2026-11-03 新建。counts / shells / jobs 三端点接线 + Mock 开关对齐；只调 /display 前缀，禁止直调 /v1/policy/** | 硬依赖 `POL-L2-DS11-READ-IMPL-JAVA`、`-IMPL-PY`、`-GAPFILL-L01`（均已 done） | 无截至时间 |
| WBS-05-23-L2-06F · `POL-L2-DS11-READ-TEST-L01` | DS11 结果解读报告多维展示 · 单元测试用例（合规交付主路径数据准备 + 关键路径验证 + 界面操作过程与截图） | 淮政玮 | `gkx-orchestration` | **ready** | 2026-11-03 新建。用例文档落 `工程过程/04-系统集成/05-展示系统集成/测试用例/`；界面操作逐步截图嵌入测试报告 | 硬依赖同上三单（均已 done）。在 23 Java + 36 Python 单测基础上补合规交付视角 | 无截至时间 |
| WBS-05-23-L2-05E · `POL-L2-DS11-VIZ-WIRING-L01` | DS11 政策分析报告可视化呈现 · 前端接线（jobs 趋势/分区 + shells 模板 四支接入） | 淮政玮 | `lumen-ui-science-pc` | **ready** | 2026-11-04 新建。219/220 各一次 POST jobs（kind 单种类）、222 GET shells（kind=模板选用）、221 只消费第 7 项已有子图；只调 /display 前缀，禁止直调 /v1/policy/**；Mock 开关对齐 | 硬依赖 `POL-L2-DS11-VIZ-ARCH`、`-API`、`-GAPFILL-L01`（均已 done） | 无截至时间 |
| WBS-05-23-L2-07E · `POL-L2-DS11-PLAN-WIRING-L01` | DS11 推荐方案报告交互展示 · 前端接线（jobs 方案对照/参数模拟/路径风险 + shells 意见/报告 五支接入） | 淮政玮 | `lumen-ui-science-pc` | **ready** | 2026-11-04 新建。227/228/229 各一次 POST jobs、230/231 各一次 GET shells，一次请求只带一种类；未选方案/无行则空；只调 /display 前缀；Mock 开关对齐 | 硬依赖 `POL-L2-DS11-PLAN-ARCH`、`-API`、`-GAPFILL-L01`（均已 done） | 无截至时间 |
| WBS-05-23-L2-05F · `POL-L2-DS11-VIZ-TEST-L01` | DS11 政策分析报告可视化呈现 · 单元测试用例（合规交付主路径数据准备 + 关键路径验证 + 界面操作截图） | 淮政玮 | `gkx-orchestration` | **ready** | 2026-11-04 新建。覆盖 219–222 四叶；用例文档落 `工程过程/04-系统集成/05-展示系统集成/测试用例/`；正常态+空态双路径截图嵌入报告 | 硬依赖 `POL-L2-DS11-VIZ-WIRING-L01`、`-GAPFILL-L01`（灌数已 done） | 无截至时间 |
| WBS-05-23-L2-07F · `POL-L2-DS11-PLAN-TEST-L01` | DS11 推荐方案报告交互展示 · 单元测试用例（合规交付主路径数据准备 + 关键路径验证 + 界面操作截图） | 淮政玮 | `gkx-orchestration` | **testing** | 2026-11-04 阶段一完成：用例文档已落 `工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS11-PLAN-TEST-L01.md`（13 用例，五叶双路径），DP-01 连库核实 19 行四种类行集 ✅；界面截图待 `POL-L2-DS11-PLAN-WIRING-L01` 完成后补做 | 硬依赖 `POL-L2-DS11-PLAN-WIRING-L01`（in_progress，阶段二阻塞点）、`-GAPFILL-L01`（灌数已 done） | 无截至时间 |
| WBS-05-23-L2-07G · `POL-L2-DS11-MOCKAUDIT-L01` | DS11 政策分析评价 · 真实/mock 全量盘点 + 评审模式来源标注（序号 219–231 全叶 + 页面块级；mock 唯一合规形态 = gapfill 缺项表） | 淮政玮 | `lumen-ui-science-pc` + `gkx-orchestration` | **backlog** | 2026-11-11 新建。盘点表落 `agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-MOCKAUDIT-L01-盘点表.md`；三层判定（A 真读面 / B gapfill mock / C 前端演示态）；`?review=1` 评审模式下逐块标注来源，MockBadge reason 统一口径；违规项（绕过 gapfill 的伪造通道）单列挂 FIX 子单。handoff：`POL-L2-DS11-MOCKAUDIT-L01.md` | 硬依赖 `POL-L2-DS11-PLAN-WIRING-L01`（done）；VIZ/READ WIRING 两单未完成叶按分册设计稿如实标注 | 无截至时间 |
### 4.1d 科学技术全景 · 按需规功能拆解（WBS-05-01）

> 2026-11-05。真源 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md`。逐叶对照在 `agent-handoffs/科学技术全景-DS02/功能拆解.md`。功能架构是 WBS-05-01c `TS-L2-DS02-ARCH`。
>
> 本菜单只拆三个功能、序号 17–33。不按 17 叶各开新任务。34–40 不建实现单。41–47 归 WBS-05-24，不在本表建单。

| 需规功能 | 序号 | 落到已有单 | 还不建 |
|---|---|---|---|
| 展示技术点图谱 | 17–21 | 页面 `FE-TS-02A`；接线 `SYSINT-05-01A-L01`；后端 `SYSINT-05-01B-L01`；架构 `TS-L2-DS02-ARCH`。17 的数据在第 2 项 `SYSINT-TECHGRAPH-02-L01`，本页 501 | 不另开搜索、详情、交互单 |
| 展示技术点关联实体 | 22–27 | 同上三张展示单。26 保持 501。27 的影响力身份在 `DS-02-METRIC-OPEN-L01` | 分数灌数待架构会签后再开，不按叶拆 |
| 展示关键路径和关键节点 | 28–33 | 同上三张展示单。路径数据在 `SYSINT-TECHGRAPH-02-L02`（未开工）。比较和播放已在 `FE-TS-02A` | 不另开比较单、播放单 |
| 维护技术图谱 | 34–40 | 无 | 报价划掉。不建单 |
| 维护关键实体及关系 | 41–47 | `FE-TS-10A`、WBS-05-24、`SCI-INT-A03` | 不在科学技术全景展示单里再拆 |

产品叶清单 `SCI-INT-A02`（ready_to_sign）已覆盖 excel 20–36，即序号 17–33。本表不重开那张定义单。

系统详细设计：`TS-L2-DS02-SDD`，稿 `agent-handoffs/科学技术全景-DS02/sdd/科学技术全景-系统详细设计说明书.md`。实现不按叶拆。已有 `FE-TS-02A`、`SYSINT-05-01A-L01`、`SYSINT-05-01B-L01` 不重开。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-01d · `TS-L2-DS02-SDD` | 科学技术全景 · 系统详细设计说明书（序号 17–47 的范围裁定，实现只做 17–33） | 淮政玮 | `gkx-orchestration` | **ready** | 稿已落盘。会签未做，不标 done。34–40 不建单，41–47 归 WBS-05-24 | 功能架构 `TS-L2-DS02-ARCH`。不替代 01a / 01b | 无截至时间 |
| WBS-05-01e · `TS-L2-DS02-READ-PY-L01` | 科学技术全景 · 读图（`POST /internal/tech-graph/read`） | 唐绍祖 | `lumen-algo-py` | **backlog** | 未开工。只读 `demo_gkx_chain`。空图不返回种子。不写图 | 说明书会签。不与 `SYSINT-TECHGRAPH-02-L01` 的写入混成一张单 | 无截至时间 |
| WBS-05-01f · `TS-L2-DS02-SCORE-L01` | 科学技术全景 · 影响力 / 中心度 / 路径优先级灌数 | 徐滕强 | `lumen-algo-py` | **backlog** | 未开工。表 `ads_technology_panorama_score`。D4 保持 mock | 说明书会签。与 01e 同仓，01e 合入后再做 | 无截至时间 |
| WBS-05-01g · `TS-L2-DS02-TEST-L01` | 科学技术全景 · 三个功能主路径测试 | 黄敬洲 | `gkx-orchestration` | **backlog** | 未开工。打开、搜索、点技术点、看实体、看路径、播放。17 与 26 确认为 501 或空 | `SYSINT-05-01A-L01`、`SYSINT-05-01B-L01`、01e、01f | 无截至时间 |

### 4.1e WBS-05-24 的子任务（维护管理 M10 · 按需规分区拆解）

> 2026-11-06。真源：图层与数据源 = `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md` **序 5–9**；关键实体及关系 = `科学技术全景.md` **序 41–47**。存量对照：[对照-科技发展规划与维护管理-存量任务与依赖.md](./对照-科技发展规划与维护管理-存量任务与依赖.md) A 段。**序 34–40 报价划掉不建单**；M10 不并进 `BE-TS-IMPL-01` / `BE-TS-DATA-01`（范围 M1–M9）。开工顺序：先图层与数据源，后关键实体与关系。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-24-L2-01A · `TS-L2-M10-LAYER-ARCH` | 维护管理 · 图层与数据源 · 后台实现架构（M1 序 5–9） | 刘剑锋 | `gkx-orchestration` | **done**（2026-11-06 刘剑锋签收；两轮会签：v2 四角色+条件回填、v3 三角色快审） | 2026-11-06 架构稿已落盘 `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-M10-LAYER-ARCH.md`（含调用链+数据流 Mermaid；**裁定终版 v3（监管人经开发核实：Java 可建业务表写数据）**——`cfg_*` 四表落业务库，DDL+种子+CRUD 全归 Java 领域服务（display 经 Feign 保 D15），**Python 不参与、无灌数单**；当日三演变（v1 直写/v2 归 Python/v3 终版）审计轨迹在稿 §3；序 6/9 读侧归 M1；probe 领域服务出网+SSRF、DB 型 501）。两轮会签闭环（v2 四角色+v3 三角色快审），2026-11-06 签收。handoff `科技发展态势-TS/TS-L2-M10-LAYER-ARCH.md` | 存量调研落盘（对照文档 A 段）；`FE-TS-10A` as-built | 无截至时间 |

| WBS-05-24-L2-01B · `TS-L2-M10-LAYER-API` | 维护管理 · 图层与数据源 · 后台接口设计 | 刘剑锋 | `gkx-orchestration` | **done**（2026-11-06 刘剑锋签收；两轮会签：v2 四角色+条件回填、v3 三角色快审） | 2026-11-06 接口分册落盘 `sdd/l2/TS-L2-M10-LAYER-API.md`：4 组资源 + probe 分型（API 真探测+SSRF/DB 501/填报 400），DTO/枚举/错误码冻结，M10 唯一契约源（BE-TS-CONTRACT-02 不回填）；内部委托 v3（读写经 Feign→领域服务→业务库，Python 不参与，对外契约不变）。handoff `科技发展态势-TS/TS-L2-M10-LAYER-API.md`。v3 快审已过 | `TS-L2-M10-LAYER-ARCH`（done 已签收） | 无截至时间 |
| WBS-05-24-L2-01C · `TS-L2-M10-LAYER-METRIC` | 维护管理 · 图层与数据源 · 后台指标设计 | 刘剑锋 | `gkx-orchestration` | **done**（2026-11-06 刘剑锋签收；METRIC 会签同意+ALGO 快审链） | 2026-11-06 指标分册落盘 `sdd/l2/TS-L2-M10-LAYER-METRIC.md`：复核 ARCH §2 全 N/A **成立**（配置写侧无统计数字；序 6 统计归 M1；probe 时延不注册；cfg_* 无 is_mock/metric_id 列）。handoff `科技发展态势-TS/TS-L2-M10-LAYER-METRIC.md`。待四角色会签 | `TS-L2-M10-LAYER-ARCH`（done 已签收） | 无截至时间 |
| WBS-05-24-L2-01D · `TS-L2-M10-LAYER-DATA` | 维护管理 · 图层与数据源 · 后台数据架构设计 | 刘剑锋 | `gkx-orchestration` | **done**（2026-11-06 刘剑锋签收；两轮会签：v2 四角色+条件回填、v3 三角色快审） | 2026-11-06 数据分册落盘 `sdd/l2/TS-L2-M10-LAYER-DATA.md`：`cfg_*` 四表列级定义（**业务库**，v3 终版）；DDL+种子 26 行+运行时 CRUD 全归 Java 实现单（**无 Python 灌数单**）；**修正 ARCH 种子数 8/9→3/3/9**（demo 源仓核对，会签逐值验证一致）。handoff `科技发展态势-TS/TS-L2-M10-LAYER-DATA.md`。v3 快审已过 | `TS-L2-M10-LAYER-ARCH`（done 已签收） | 无截至时间 |

| WBS-05-24-L2-02A · `TS-L2-M10-BE-IMPL-01` | 维护管理 · 图层与数据源 · Java 实现 | 刘剑锋 | `lumen-svc-platform` | **pending_test**（注册表此前 integration） | 代码完成+评审整改；**2026-11-07 本地联调走通**（接口六场景+页面确认，`TS-L2-M10-LAYER-联调记录-20261107.md`）。遗留：远端 dev 部署待查、local profile 分支待推。handoff `TS-L2-M10-BE-IMPL-01.md`四表 DDL+种子 26 行+领域服务 CRUD+probe（SSRF 黑名单进 DoD）；display 门面 Feign；会签口袋清单（groupId↔group_code 翻译层、utf8mb4、baseline may_read 注记）随单落地；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md) | 定义单四件套（done）；`BE-TS-CONTRACT-02` 不回填 | 无截至时间 |
| WBS-05-24-L2-02B · `FE-TS-10B` | 维护管理 · 图层与数据源 · 前端接线 | 刘剑锋 | `lumen-ui-science-pc` | **pending_test**（注册表此前 integration） | 代码完成+评审整改；**2026-11-07 本地联调走通**（页面确认）。BASE 修复在 feat/m10-maintain-wiring 待合 MR。handoff `FE-TS-10B.md`api 层重写四组资源+probe、差异表六项落地（targetLayerCode/lastSync/testStatus/409 文案/至少留一组放弃/store 服务端化+localStorage 降级）；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md) | `TS-L2-M10-LAYER-API`（done）；`TS-L2-M10-BE-IMPL-01`（联调依赖） | 无截至时间 |

| WBS-05-24-L2-03A · `TS-L2-M10-ENT-ARCH` | 维护管理 · 关键实体与关系 · 后台实现架构（序 41–47） | 刘剑锋 | `gkx-orchestration` | **done**（已签收） | 四角色会签（1 同意+3 有条件，6 处事实修正已回填）+ 条件闭环（C1 裁定 **A：display 代理**）；2026-11-07 刘剑锋签收。handoff `TS-L2-M10-ENT-ARCH.md` | `SCI-INT-A03`（ready_to_sign）；调研=对照文档 A.3.1 | 无截至时间 |
| WBS-05-24-L2-03B · `TS-L2-M10-ENT-API` | 维护管理 · 关键实体与关系 · 后台接口设计 | 刘剑锋 | `gkx-orchestration` | **done**（已签收） | 2026-11-07 分册落盘：7 op 冻结+读端点 R1-R6（display 代理 C1=A）/幂等全 op/409+diff/pending 可读；M10-ENT 唯一契约源。四角色会签+回填+2026-11-07 签收。handoff `TS-L2-M10-ENT-API.md` |写回走 A03 已设计 changes 端点；M10-ENT 唯一契约源 | `TS-L2-M10-ENT-ARCH` | 无截至时间 |
| WBS-05-24-L2-03C · `TS-L2-M10-ENT-METRIC` | 维护管理 · 关键实体与关系 · 后台指标设计 | 刘剑锋 | `gkx-orchestration` | **done**（已签收） | 2026-11-07 分册落盘：叶41 挂 M_TECH_GRAPH_105_1（禁全 N/A）；计数四处 DN-A03-09 一次性豁免建议；strength_manual 永不进指标口径。四角色会签+回填+2026-11-07 签收。handoff `TS-L2-M10-ENT-METRIC.md` |沿 A03 指标卡复核，不新造 | `TS-L2-M10-ENT-ARCH` | 无截至时间 |
| WBS-05-24-L2-03D · `TS-L2-M10-ENT-DATA` | 维护管理 · 关键实体与关系 · 后台数据架构 | 刘剑锋 | `gkx-orchestration` | **done**（已签收） | 2026-11-07 分册落盘：8 决策项方案（gkxlumenx_dwd/Python 单写者/ADS graph_entity_* 新建/N=50 报批）；建表基线 10 张含补漏表。四角色会签+回填+2026-11-07 签收。handoff `TS-L2-M10-ENT-DATA.md` |Nebula 复用+变更表归 Python 写；不建 cfg_ 表 | `TS-L2-M10-ENT-ARCH` | 无截至时间 |

| WBS-05-24-L2-04A · `TS-L2-M10-ENT-PY-IMPL-01` | 维护管理 · ENT · Python 写侧（变更链 12 表+发布投影+存量 seed） | 刘剑锋 | `lumen-algo-py` | **pending_test** | 2026-11-09 代码完成（单测 6/6）。**2026-11-09 走查返工**（edu 500）：`get_conn` 不存在致全端点 500、表无库前缀、不提交事务、plane 默认落 demo 库等 → `4b34c21` 修复（单测 15/15）；DDL 已执行（12 表）。待 edu 接口联调。handoff `TS-L2-M10-ENT-PY-IMPL-01.md`；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md)；联调中补修 `edd426b`（R2 只返回已挂接边） | 定义四单（done） | 无截至时间 |
| WBS-05-24-L2-04B · `TS-L2-M10-ENT-JAVA-IMPL-01` | 维护管理 · ENT · Java 双门面（topic+display） | 刘剑锋 | `lumen-svc-platform` | **pending_test** | 2026-11-08 双门面完成（8d90869）。**2026-11-09 走查返工**（edu 实测 503「无 lumen-algo-py 实例」）：topic→Python Feign 地址改继承 `TOPIC_ALGO_BASE_URL`、topic 门面 `@Inner`、relay 不可达不再 500 → `d8bbea6`（topic 8/8、display ENT 2/2）。**topic 需 `TOPIC_RELEASE=true` 点名发**。待 edu 接口联调。handoff `TS-L2-M10-ENT-JAVA-IMPL-01.md`；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md)（topic 经 #4466 发布） | `TS-L2-M10-ENT-API`（done） | 无截至时间 |
| WBS-05-24-L2-04C · `FE-TS-10C` | 维护管理 · ENT · 前端接线 | 刘剑锋 | `lumen-ui-science-pc` | **pending_test** | 2026-11-08 接线完成。**2026-11-09 走查返工**（页面 mock 文案、窄屏错乱）：real 轨状态只来自 R2/R1（原始终显示页面种子）、统一 axios、去硬编码技术点；分区1 不再回落种子；容器查询+宽表滚动+td flex 修复 → `8d754e2`。维护技术图谱（34–40）不动。待 edu 联调。handoff `FE-TS-10C.md`；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md)；补修 `369f70c`（人工标注） | `TS-L2-M10-ENT-API`（done） | 无截至时间 |
| WBS-05-24-L2-04D · `TS-L2-M10-ENT-SEED-L01` | 维护管理 · ENT · 存量技术点种子（Nebula 实扫） | 刘剑锋 | `lumen-algo-py` | **pending_test** | 2026-11-09 已灌 dev 库 126 行：technology_master active=1 / 假种子软删 2；ADS node=1、edge=61（真实 relation_strength 0.55–2.07）、overlay=61。**范围裁定（刘剑锋 2026-11-09）**：仅灌有真实强度的技术点，全量留 04E。实体名含「示范研究机构/示范研究者」，D4 视为 mock 待产品定角标；强度口径待 algorithm-agent 确认。脚本 `vendor/entan-py/scripts/seed_tech_graph_maintain.py`（0b46d01）。handoff `TS-L2-M10-ENT-SEED-L01.md`；**2026-11-09 edu 联调通过**（真实登录浏览器冒烟）→ [联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md)；冒烟后数据已复原（edge manual 1 / auto 60） | `TS-L2-M10-ENT-DATA`（done） | 无截至时间 |
| WBS-05-24-L2-04E · `TS-L2-M10-ENT-R2-PAGE-L01` | 维护管理 · ENT · R2 分页/技术点检索 + 全量灌数 | 刘剑锋 | `lumen-algo-py` | **backlog** | Nebula 技术点 19,348（去重），R2 无分页全量会一次返回 1.9 万节点；需改 API 分册（会签）+ Python + 前端远程检索，再 `--all` 全量灌数 | `TS-L2-M10-ENT-API`；`TS-L2-M10-ENT-SEED-L01` | 无截至时间 |
| WBS-05-24-L2-05A · `TS-L2-M10-TEST-L01` | 维护管理 · 主路径测试（图层与数据源 + 关键实体与关系各一条 + 截图） | 刘剑锋 | `lumen-ui-science-pc` | **ready** | qa-agent；关 Mock 走 edu 真接口；登录按新人引导 §6；维护技术图谱不在范围；2026-11-09 依赖单联调通过，转 ready 交 qa-agent（冒烟基线见[联调冒烟记录](../../../agent-handoffs/科技发展态势-TS/TS-L2-M10-联调冒烟记录-20261109.md)） | `FE-TS-10B`、`FE-TS-10C`、`TS-L2-M10-ENT-SEED-L01` | 无截至时间 |


### 4.1f WBS-05-07 的子任务（智库服务真实对接 · 8 子任务）

> 2026-11-06。派单依据：对端两套接口已就位 —— v1.1（zwrite-backend，4 GET：报告/成果/枚举/成果统计）+ docx（topic-system，5 POST：德尔菲问卷/专家/Field/重大事件）。智库服务 25 条指标在久新库全部"三源调研批次产物 + 源表为空"，本页**不依赖久新库血缘**，全走外部接口路径；前端按 D9 挂 ⓘ + 四维就绪度，**禁 MockBadge**。派单稿：`agent-handoffs/科技服务全景-SVC/派单说明/派单-SYSINT-05-07-THINKTANK-REALDATA-L01.md`。监管一律 `human:李伟`（一线 `human:孔东`）；执行优先级 **A → B → D → C → E**（用户 2026-11-06 裁定）。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-07-01 · `SYSINT-05-07-01-L01` | A·智库契约登记 + EXT-B4-ZHIKU 建包（9 端点入册 05-API 清单） | 李伟 | `gkx-orchestration` | **review（待款签字）** | **2026-11-06 完成**：05-API 清单 §六 ZK-01～ZK-09 逐字段入册、`EXT-B4-ZHIKU` 建包、技术方案 §1.3/§2/§5 智库行同步、派单稿交叉引用 | 无 | 待填写 |
| WBS-05-07-02 · `SYSINT-05-07-02-L01` | A·智库鉴权打通（v1.1 Bearer + docx X-Portal-Access-Token 双 token） | 李伟 | `gkx-orchestration` | **review（待凭证）** | **2026-11-06 契约部分完成**：`对接文档/我方/2026-11-06-智库服务-鉴权与联调申请.md`（单令牌双头结论 / 失效处置 / 网关转发契约 / 三件套模板）；凭证与联调窗口待李伟获取 | 01 | 待填写 |
| WBS-05-07-03 · `SYSINT-05-07-03-L01` | B·D1–D5 决策函 + B1–B5 冲突裁定（含 B5 专家详情 iframe 弹框 + 技术方案 §2 措辞修） | 李伟 | `gkx-orchestration` | **review（待签字）** | **2026-11-06 起草完成**：D1-D5 决策函 + B1-B5 裁定函双件落 `对接文档/我方/`；B5 定为**本系统内 iframe 弹框**；技术方案 §2 智库行已改「不跳出新页签/新窗口，允许本系统内 iframe 弹框嵌入」（待淮政玮重签） | 无（可与 A 段并行） | 待填写 |
| WBS-05-07-04 · `SYSINT-05-07-04-L01` | B·iframe 嵌入白名单（`zk.example.com` / `edu.itic-sci.com`）+ 成果敏感字段对外合规 | 李伟 | `gkx-orchestration` | **review（待回函）** | **2026-11-06 发出稿就绪**：`对接文档/我方/2026-11-06-智库服务-对端确认函-iframe白名单与字段口径.md`（Q1 四页面嵌入白名单 / Q2 免登录 / Q3 敏感字段 / Q4 HTTPS + C1-C3）；待李伟发送并收回归档 | 03 | 待填写 |
| WBS-05-07-05 · `BE-DISPLAY-SVC-THINKTANK-GATEWAY-L01` | D·展示 Java 网关双路由 + 双鉴权转发 + 信封规范化 | 李伟 | `lumen-svc-platform` | **review（待凭证联调）** | **2026-11-06 实现完成**：`ThinkTankGateway` 双 BASE_URL（A=zwrite / B=topic-system）+ 单令牌双头自动装配 + 两套信封规范化（段 B 以 body code 判 401）+ 仅 50004/10004 退避重试 + 未配置空态；单测 13 项（`ThinkTankEnvelopeTest`），display 全量 105 绿 | 01、02、03 | 待填写 |
| WBS-05-07-06 · `BE-DISPLAY-SVC-THINKTANK-API-L01` | D·智库 9 端点业务转发（报告/成果/问卷/专家/事件）+ 字段映射 | 李伟 | `lumen-svc-platform` | **review（待凭证联调）** | **2026-11-06 实现完成**：`ThinkTankController` `/v1/think-tank` 9 端点 + `ThinkTankBffService` + `ThinkTankFieldMapper`（D2 丢弃 hIndex/引用量、B4 隐藏成果敏感三字段、空态三态透传、`_vendor`/`_error` 透明）；单测 20 项（映射 10 + BFF 10） | 05 | 待填写 |
| WBS-05-07-07 · `FE-DISPLAY-SVC-THINKTANK-REPLICA-L01` | C·5 Tab 复刻 + IframeDetailModal 公共组件 + D9 血缘 | 李伟 | `lumen-ui-science-pc` | **review** | **2026-11-06 复刻完成**：5 Tab/筛选/分页/4 图表/3 信息流/iframe 弹框+抽屉兜底落地；vue-tsc 新增 0 报错、build 退出码 0、浏览器渲染与评审零泄漏 PASS；handoff `FE-DISPLAY-SVC-THINKTANK-REPLICA-L01.md`（含 D9 附录 D 摘要）。**未推送，等人工确认** | 03、04、06 | 待填写 |
| WBS-05-07-08 · `SYSINT-05-07-08-L01` | E·智库真联调与三方验收（9 端点逐字段） | 李伟 | `gkx-orchestration` | ready | registry 已登记，待凭证与前端联调就绪后开工（依赖 04、06、07） | 04、06、07 | 待填写 |

> 状态同步以 `task-registry.yaml` 为准，签收时由 coordinator-agent 落库；本表先行占位。主任务 `SYSINT-05-07-L01` 首个子任务开工时状态由 `ready` 升 `claimed`。完成日期要求按 11 月倒排计划由 PM 填，本表不预填。

### 4.2 WBS-05-08 的子任务（科技交流 / 竞赛 / 传播）

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-08-01 · `SYSINT-05-08-01-L01` | 科技服务全景对接分析（交流 / 竞赛 / 传播） | 李伟 | `lumen-ui-science-pc` | **done** ✅ 2026-10-30 签收 | **已完成并签收**（2026-10-23 晚落盘 271 行纪要 + 深势 MD 接口审计；2026-10-30 `human:李伟` 签收）。evidence：本夹 `纪要/2026-10-23-科技服务全景-深势对接-交流竞赛传播模块优化.md`、`对接文档/对端/2026-10-23-深势-科技服务全景对外开放接口.md`。12 项会议结论全覆盖；字典枚举决策已固化（不走接口）；原型字段映射决策完成（竞赛类型下拉移除、竞赛级别保留并做值映射）；OpenAPI 合规性审计经李伟审阅 | 父 `SYSINT-05-08-L01`。✅ 已签收 | 计划 2026-10-23（实际当日完成，10-30 签收） |
| WBS-05-08-02 · `SYSINT-05-08-02-L01` | 科技服务全景入口跳转壳开发 | 孔东（前端壳） | `lumen-ui-science-pc` | **done** ✅ 2026-10-31 完成 | 已完成。三入口菜单在 `src/router/menu.ts` 注册（tech-communication / tech-competition / tech-communication-analysis）；跳转方案按 `human` 2026-10-31 指示定为 **iframe 弹窗**，公共组件 `views/service/components/DetailIframeModal.vue`，标题栏保留「在新窗口打开」兜底；深势详情页实测无 `X-Frame-Options` / 无 CSP `frame-ancestors`，可内嵌；深势不支持字段（奖金、竞赛类型下拉、点赞排序）均不展示。handoff：[`SYSINT-05-08-02-L01.md`](../../../agent-handoffs/SYSINT-05-08-02-L01.md) | 父 `-08-L01`（claimed）、`-08-01`（done ✅）均满足 | 2026-11-03 |
| WBS-05-08-03 · `SYSINT-05-08-03-L01` | 科技交流页面对接（BFF + FE，深势 3 接口代理） | 李伟（BFF 主责） | `lumen-svc-platform` | **done** ✅ 2026-10-30 完成 | 已完成 ✅ BFF 三文件 + 前端 API + 页面 + menu 路由。BFF：`RemoteDeepShiClient`（4 方法全 `@NoToken`）+ `ExchangeBffService`（四类并行 + 分区降级 + 8 组内嵌枚举字典）+ `ExchangeController`（6 端点：overview/list/detail/sync/recommendation/dictionaries）。深势寻址 `gkxlumen.deep-shi.base-url`。前端：`api/service/exchange.ts` + `views/service/tech-communication/index.vue`（四类 Tab + 活动列表 + KPI 卡 + 详情弹框 + 空/加载/错误三态）+ router menu.ts resolve。三绿：mvn compile / vue-tsc / pnpm build。降级：深势不可达返回 `_bff_source=deep-shi-unreachable` 空壳不 5xx；字典 BFF 内嵌不走接口。2026-10-31 走查返工：原型复刻、`geo.ts` 地址模糊匹配、前端分页、四类 stats 只取首份。handoff：[`SYSINT-05-08-03-L01.md`](../../../agent-handoffs/SYSINT-05-08-03-L01.md) | 父 `-08-L01`、`-08-01`（done ✅）均满足 | 2026-10-30（提前） |
| WBS-05-08-04 · `SYSINT-05-08-04-L01` | 科技竞赛页面对接（BFF + FE，深势 4 接口代理） | 李伟（BFF 主责） | `lumen-svc-platform` | **done** ✅ 2026-10-31 完成 | 已完成。BFF：`RemoteDeepShiClient` 扩 4 端点 + `CompetitionBffService`/`CompetitionController`（`/v1/competition/list`·`resource`·`ranking`·`discussion`）+ security 放行。前端：`api/service/competition.ts` + `views/service/tech-competition`（KPI 3 卡 + 筛选「全部」项 + 4 Tab：进行中/即将开始/已结束/排行榜）。human 走查裁定偏差：奖金全部移除（非空态占位）、社区讨论 Tab 移除、竞赛级别改用接口真实 5 值（国家级/省级/市级/行业级/学校级）、竞赛类型改常规赛/认证赛本地过滤、榜单自动探测有数据竞赛（实测 36 场中 11 场有榜）。handoff：[`SYSINT-05-08-04-L01.md`](../../../agent-handoffs/SYSINT-05-08-04-L01.md) | 父 `-08-L01`、`-08-01`（done ✅）均满足 | 2026-11-11 |
| WBS-05-08-05 · `SYSINT-05-08-05-L01` | 科技传播页面对接（BFF + FE，深势 3 接口代理） | 李伟（BFF 主责） | `lumen-svc-platform` | **done** ✅ 2026-10-31 完成 | 已完成。BFF：`RemoteDeepShiClient` 扩 3 端点 + `CommunicationBffService`/`CommunicationController`（`/v1/communication/content/list`·`detail`·`sync`）+ security 放行。前端：`api/service/communication.ts` + `views/service/tech-communication-analysis`。human 走查裁定：列表服务端分页（8/16/24）、分类导航走接口原生 `contentTypes` 过滤（实测 `contentTypes=1` → total=22）、补排序（LATEST/HOTTEST）、时间轴按原型 `Timeline mode="alternate"` 自绘左右交替（Arco 无该模式）、详情 iframe 弹窗。handoff：[`SYSINT-05-08-05-L01.md`](../../../agent-handoffs/SYSINT-05-08-05-L01.md) | 父 `-08-L01`、`-08-01`（done ✅）均满足。**BFF 与入口壳方案已统一为 iframe 弹窗** | 2026-11-18 |
| WBS-05-08-06 · `SYSINT-05-08-06-L01` | 科技服务全景三板块联调验收 | 李伟（QA 归总控） | `lumen-ui-science-pc` | **done** ✅ 2026-10-31 完成 | 已完成（human 判定联调已完成）。实测：三页 BFF 端点（localhost:7099）均返回深势真实数据——交流 activityCount=247 / participantCount=2243 / organizationCount=79 / expertCount=107，竞赛 competitionCount=36，传播 totalContentCount=47；竞赛 ranking/resource/discussion 与传播 detail/sync 下钻正常；地址自由文本 → `geo.ts` 三级模糊匹配容错降级验证通过（未匹配项不上图并如实提示数量）；竞赛类型下拉移除、竞赛级别值映射、奖金移除均验证通过；三页 `vue-tsc` + `vite build` 绿。handoff：[`SYSINT-05-08-06-L01.md`](../../../agent-handoffs/SYSINT-05-08-06-L01.md)、跨任务决策轨迹：[`SYSINT-05-08-决策与过程记录.md`](../../../agent-handoffs/SYSINT-05-08-决策与过程记录.md) | `-08-02`～`-08-05` 全部完成 ✅ | 2026-10-31（提前） |

> **2026-10-26 `human:李伟` 挂接**：`SVC-PANORAMA-API-L01`、`SVC-PANORAMA-GAP-L01` 两件自建任务挂在 WBS-05-08 下，不新开叶。产物 `工程过程/02-策划与监控/01-总集大项目整体计划/09-科技服务全景接口需求评估/科技服务全景-页面维度供数缺口自研对照表.md`（161 行，§五 10 项待会签）。今日快照已出，百分比不回改，明日快照按注册表现状态计入。

### 4.3 WBS-05-18 的子任务（SITUATION-ENT 长任务管线 · 企业维度数据跑通）

> 2026-10-27 `human:李伟` 授权长任务（**授权句已生效：「后续认领不必再问」**）。目标：DS-01 科技全域态势页企业维度数据在 `USE_MOCK=false` 下全链路真实闭环（前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → demo 库 DWD/ADS）。**边界铁律：可改接口契约，不可改 UI 与实现效果**（`views/situation/**` diff 为零）。总控 / 总派单 / 契约草案：`agent-handoffs/科技发展态势-TS/SITUATION-ENT-长任务总控.md` / `SITUATION-ENT-总派单.md` / `SITUATION-ENT-API-CONTRACT-01.md`。
> registry 任务由 coordinator 走 MCP `task-create` 建单后回写本表状态列（**禁手改 `task-registry.yaml`**）。`supervised_by` 按总控 = `human:李伟`（D1 前端叶的仓属 `lumen-ui-science-pc`，WBS-05-18 行 FE 口径监管孔东，本管线叶归总控授权人）。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-18-01 · `SITUATION-ENT-A0-L01` | 数据/环境体检（只读：element 六端点 curl、`enterprise_base`/`enterprise_score`/两张 dist 表行数与脏值、网关 `10.50.69.111:30895` 可达性、真实 token 获取方式） | 李伟 | `lumen-svc-platform`（只读） | **ready_to_sign**（AV-0 过，2026-10-27） | handoff `agent-handoffs/科技发展态势-TS/SITUATION-ENT-A0-L01.md`：库四表行数核验（189,115/189,115/30/35）+ 脏值（1,132 空坐标/353 异常年）+ 六端点全 200 + `/map` 基线存档（objectPoints 现状空）；网关真源 `10.50.69.111:30895` health 200；element 旧实例僵死已重建重启 | 无 | 无截至时间 |
| WBS-05-18-02 · `SITUATION-ENT-C1-L01` | element 对象级企业点位端点（U3：`enterprise_score` 坐标 Top-N，脏坐标剔除，不建新表） | 李伟 | `lumen-svc-platform` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C1-L01.md`：`GET /v1/element/enterprise/points` 已上线（Top-N 默认 100 硬顶 500、city/district 过滤、脏坐标剔除、join 显式 COLLATE）；自测 4 组全 200 稳态 <1s；**单测 7/7 绿**。修两坑：patent_valid_count 整列 NULL 被误示为 0（改 patent_grant_count，NULL 时省略 relatedElements）、element 低版本 surefire 静默跳过 JUnit5（已声明 3.2.5）。⚠️ 改动停本地未 commit（走查后推） | A0 ≥ integration | 无截至时间 |
| WBS-05-18-03 · `SITUATION-ENT-C2-L01` | display `/v1/situation/map` objectPoints 接线 + `/overview` 联调（Feign 降级路径演练） | 李伟 | `lumen-svc-platform` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C2-L01.md`：新增 Feign `enterprisePoints`（@NoToken/@Inner 配对），`/map` objectPoints **0 → 100**、正常路径不再吐 emptyReason；**对照 A0 基线字段级差分：factorItems/regions/cascade/legend 全部 identical**（仅 objectPoints 变化）；降级演练（停 element）仍 200 + 空 + UNREACHABLE reason；修正降级文案的不实陈述。⚠️ 改动停本地未 commit | C1 ≥ integration | 无截至时间 |
| WBS-05-18-04 · `SITUATION-ENT-C3-L01` | `POST /v1/situation/influence` 实现（U1/U2：`enterprise_score` 占位，正式指标 `M_INNOV_ENTERPRISE_INFLUENCE` 算法未上线记缺口不翻转） | 李伟 | `lumen-svc-platform` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C3-L01.md`：element `GET /v1/element/enterprise/influence` + display `POST /v1/situation/influence`（返回即 `InfluenceDataset`，前端零结构映射）。**契约 bump v1.2**：v1.1 §2 的简化结构 `{count,averageScore,items}` 与冻结 TS 类型不符，已按 U5 改正。自测 6 组全 200（默认 189,115/avg 37.78 · 深圳市 95,600 · 南山区 16,039 · 搜索京泉华 2 家 · 要素过滤出局 · 降级 200 空态）；修一处真实缺陷（聚合查询漏传 args → 带过滤即 500）；element 单测仍 7/7 绿。⚠️ 改动停本地未 commit | C2 ≥ integration；契约 v1.2 | 无截至时间 |
| WBS-05-18-05 · `SITUATION-ENT-D1-L01` | 前端契约适配 + 全局 `USE_MOCK=false` 切换（U4：timeline/events/cluster/compare 404 → 诚实空态，错误处理只在 api 层；三绿 + 视图 diff 为零自检） | 李伟（执行 FE） | `lumen-ui-science-pc` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-D1-L01.md`：USE_MOCK=false + api 层诚实空态（独立轻量 axios，无报错弹窗）+ vite 代理剥 `/display` 前缀（**本地 401 真凶：无网关时服务前缀无人剥**）；三绿达成（type-check / build 57.91s / 浏览器冒烟真实数据渲染 + 截图存档）；`views/situation/**` 与 styles **diff 为零**。⚠️ 改动停本地未 commit；走查观察项 2 条记录在 handoff | C2/C3 ≥ integration | 无截至时间 |
| WBS-05-18-06 · `SITUATION-ENT-C4-L01` | 筛选参数贯通（走查反馈：「筛选框没和接口数据挂钩」） | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C4C5-L01.md`：根因是 display `/map` `/overview` **完全不消费入参**（`scopeLabel` 甚至写死「全量样本」）。新增 `Scope` 翻译层（regionPaths/searchTerm/timeRange → city/district/name/注册年）+ element 侧 `appendScope` 统一过滤（overview/regions/districts/trend/points/influence 全接）。**地图级联选项刻意不随筛选收缩**（否则导航会被自己的筛选吃掉）。自测：深圳 95,600 / 腾讯 19 / 2025–2026 3,183 / 深圳+2025–2026 1,564，均与库级一致；/influence 深圳+2020–2026 **23,837 = 库 join 计数**。⚠️ 不支持项已诚实声明：学科领域无逐行列、日周月季无数据源、多选地域只取首项。改动停本地未 commit | D1 ≥ integration | 无截至时间 |
| WBS-05-18-07 · `SITUATION-ENT-C5-L01` | 聚类分析真实数据接入（走查反馈：「聚类没数据展示」） | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C4C5-L01.md`：`/cluster` 此前**根本不存在**（D1 收为空态）。新增 element `/v1/element/enterprise/cluster` + display `POST /v1/situation/cluster`，前端改回 `post()`。四维逐列核对后只接三个真源：influence=score_total、conversion=tech_power.**transfer_score**、collaboration=tech_power.**cooperation_score**；**growth 无源**（`revenue_growth_rate` 整列 NULL）→ 空桶 + emptyReason，不补 0。**排坑**：`centrality_norm`/`pagerank_score` 逐行等于 score_total（同份分的拷贝），不能当第二维度。页面实跑：高影响力 200(Top 70.3)/高转化 200(Top 96.5)/高合作 200(Top 100)/高增长 0。改动停本地未 commit | C1/D1 ≥ integration | 无截至时间 |
| WBS-05-18-08 · `SITUATION-ENT-C6-L01` | 要素比较 `/compare` 端点补全（用户走查反馈：「接口要补上，只有一个要素可先无法验证」） | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-10-27） | handoff `科技发展态势-TS/SITUATION-ENT-C6-L01.md`：新增 display `POST /v1/situation/compare`（复用 element `/trend` 的注册年计数），返回 `{years, series, availableFactorKeys, notes}`，**契约 bump v1.3**（`notes` 为可选新增，视图零改动）；前端 `fetchSituationCompare` 从「未上线空态 shim」切回 `post()`。七组自测全 200：深圳市 2022–2024 = **4032/3658/2628（与库级 join 计数逐位吻合）**、东莞 1815/1636/1079、南山区、关键词「腾讯」、只勾 scholar 空态。**只有 enterprise 有年度序列，刻意不伪造第二条曲线**，原因写在 `notes`；UI 如实停在「当前可比要素 (1/4)」。**顺带修真问题**：`scopeOf` 此前只认 `regionPaths`，compare/influence 的 `activeRegionKey` 被**静默忽略**（返回全量不报错）→ 现按 regionPaths→activeRegionKey→focusRegionKeys 解析。三绿（type-check / build 1m6s / 浏览器冒烟无报错弹窗）。⚠️ 改动停本地未 commit | C4 ≥ integration | 无截至时间 |
| WBS-05-18-09 · `SITUATION-ENT-D2-L01` | 非企业要素落点：论文/人才/项目/机构/课题/成果走市域色阶 + 机构榜单；机构不做对象级点位（实测久新坐标=城市质心）；专利无市域源诚实降级；顺带修 `SituationController` 5 处失真注释 | 李伟 | `lumen-svc-platform` + `lumen-topic-py` | **integration**（2026-11-01） | handoff `科技发展态势-TS/SITUATION-ENT-D2-L01.md`：py 新增 `POST /internal/gkx-show/geo/factor-metrics`（市域聚合，8 城有数，year=2025）+ `carrier-list` cities 过滤；display `/map` 改为 `regions.layerKeys` 随勾选要素联动 + `institutionRanking` 榜单 + `notes`，**机构伪点位移除**（`objectPoints` 仅企业）；`unsupportedFactors` 如实声明专利无市域源（`ads_geo_yearly_metrics` 无 `patent_count`）。验证：py_compile OK / 实库直调 count=8 / Java 编译与打包 exit 0 / 重打 jar 重启 py+display 后页面实跑通过（悬停「深圳市 · 论文 影响力 24904.0」，无白屏无报错弹窗，仅勾专利为空态，地图无机构点位）。前端零改动；`notes`/`institutionRanking` 前端未消费（另单再议）。⚠️ 改动停本地未 commit 未 push | 草案 §3-D2 / §1.1（`ADS_SCHEMA.md` 6.30.0） | `SITUATION-ENT-C2-L01` | 无截至时间 |
| WBS-05-18-10 · `SITUATION-ENT-D3-L01` | 期刊 / 会议两要素代码层 mock（数仓真无源，`ADS_SCHEMA.md` §24.10 明列缺失）；集中单一 Provider，评审模式 🧪 角标、非评审模式正常展示 | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-01 完工：display 层 `SituationMockProvider` + 前端 `MockBadge`；V1–V8 验证全过；改动停本地未 commit 待走查） | handoff `科技发展态势-TS/SITUATION-ENT-D3-L01.md`；规格 `D3-spec/spec.md` | 无 | 无截至时间 |
| WBS-05-18-11 · `SITUATION-ENT-MOCK-LEDGER-L01` | mock 台账（跨页公共）：登记全部代码层 mock 点位、计划替换的真实源与去掉条件，供后期去 mock 接真数 | 李伟 | `gkx-orchestration` | **integration**（2026-11-01 随 D3 完工：`科技发展态势-TS/mock-ledger.md` 已建，表头 + D3 首条 4 行登记；停本地待走查） | 台账 `科技发展态势-TS/mock-ledger.md` | `SITUATION-ENT-D3-L01` | 无截至时间 |
| WBS-05-18-12 · `INFLUENCE-FIX-L01` | 影响力 Tab 三缺陷修复（用户走查：「没跟筛选变动 / 只有企业+机构 / 值是错的」）：要素守门统一、机构卡吃地域与关键词、机构影响力按 INNOV 统一范式归一化、对象数量缺口径显示「—」、缺源 3 类 mock 补齐；**追加（2026-11-01 用户指令）年份放开到 2015 + 服务机构要素接线**（服务项目卡由不可达改为可达，默认 5 类卡） | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-01 完工：后端 7 条端点 + 追加 4 条端点 + 前端三绿 + 页面实跑通过（5 卡、年份可选 2015）；停本地待走查） | handoff `科技发展态势-TS/INFLUENCE-FIX-L01.md`；规格 `INFLUENCE-FIX-spec/spec.md`；台账「影响力登记」3 行 | `SITUATION-ENT-D3-L01` | 无截至时间 |
| WBS-05-18-13 · `GRANULARITY-FIX-L01` | 多时间粒度趋势打通（需规「日/月/季/年等不同时间维度的趋势展示」）：element trend 加 granularity 白名单真实重分桶（registration_date 日粒度事实列）、display overview 透传 + trendGranularity 回传、前端趋势标题/轴注随粒度；久新五要素仅年度粒度如实标注不摊薄；含年份滑块塌缩浏览器验证 | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-01 完工：element 五档 curl 合计均 38,308 + display 透传 + 前端三绿 + 浏览器实测切月/季生效；停本地待走查） | handoff `科技发展态势-TS/GRANULARITY-FIX-L01.md` | `INFLUENCE-FIX-L01` | 无截至时间 |
| WBS-05-18-14 · `METRIC-LIB-ALGO-INFLUENCE-L01` | 指标库口径对齐 + 算法库优先接入（影响力 Tab）：按 xlsx 更新影响力指标定义，并把算法库 precompute 真实值接入期刊 / 专家；论文 / 专利 / 服务项目保留 mock + 🧪，企业 / 机构保留可筛真实源；五卡全挂真实 metric_id 或卡级红「?」+ 缺口说明，受 @/review 门控 | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-02 完工：两探针数值无回归、五卡血缘齐、前端三绿 + 页面实跑；改动停本地未 commit / 未 push 待走查） | handoff `科技发展态势-TS/METRIC-LIB-ALGO-INFLUENCE-L01.md`：新增 Feign `RemoteAlgoScienceClient`（@NoToken 直连 :8000）+ 七指标常量 + `algoValueOf/subMap/attachMetric/markMock/buildTechnologyOutputCard/journalSubFactor/buildScholarInfluenceCard`；前端 `types/situation.ts` 扩 8 字段、`MetricSpecHint.vue` 加「口径局限」行、`metricCatalog.ts` 加 `INFLUENCE_METRIC_SOURCE/INFLUENCE_GAP_NOTE`、`InfluenceTab.vue` 卡头与子类挂 ⓘ / 红「?」+ 🧪。实测 journal n=2796 avg=4.1 无 mock、scholar n=21316 avg=50.0 items=46 无 mock、paper/patent/service mock=true | `GRANULARITY-FIX-L01`（05-18-13）；算法库 `demo-algo-science` precompute 可达（不可达降级回 mock） | 无截至时间 |
| WBS-05-18-15 · `SITUATION-ENT-SPARK-L01` | 实时数据监控要素卡年度趋势 spark 接真实数据（需规「时间轴趋势」；demo 原型每卡有 2020–2026 趋势线，此前 8 卡 `series=null` 全显「暂无趋势数据」）：论文 / 人才 / 项目 / 机构接 py `monitor/yearly-trend` 真实年度序列（缺年 null 断点、不完整年 2026 排除、近 10 年窗口），卡值与序列同源者挂「末点即卡上数值」、不同源者（论文 / 人才）挂口径差说明；企业（等 ADS 逐年存量回补）/ 专利 / 期刊 / 会议维持空态不造数 | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-02 完工：7101 实例 `/overview` 探针实测 talent 159,546 / project 392,032 / institution 48,444 三卡末点与卡值一字不差、paper 858,620 按口径差标注、无 2026 断崖；javac 全量编译 EXIT=0 + 前端 vue-tsc EXIT=0；改动停本地未 commit / 未 push 待走查） | handoff `科技发展态势-TS/SITUATION-ENT-GAP-FILL-20261102.md` §二（含实施记录）：`SituationController` 新增 `sparkSeriesOf` + `SPARK_CALIBER_DIFF_NOTE/SAME_NOTE`、`buildFactorCards` 加 `yearlyRows` 参数、`/overview` 复用单次 `monitorYearlyTrend`；前端 `types/situation.ts` 加 `caliberNote`、`chartBuilders.buildFactorSparkOption` tooltip 展示口径 | `SITUATION-ENT-C6-L01`（企业存量快照）；py `monitor/yearly-trend` 可达 | 无截至时间 |
| WBS-05-18-16 · `SITUATION-ENT-FOLLOW-SVR-L01` | **统一用户行为表服务端化**（收藏 / 订阅 / 标签 / 预警规则 / 推送记录；需规「基础信息查看功能·要素收藏和标签管理」）：范围由「要素收藏」扩展为覆盖全站 **10 页 15 个功能点**（原 15 个功能点均为 localStorage / 组件 ref 会话态，`src/api` 无任何收藏订阅接口）。DDL 已落盘 `lumen-svc-platform/db/9x_gkxlumenx_user_behavior.sql` 并**已在远程 `gkxlumenx`（upms 主库）执行建表** 5 张：`sys_user_relation`(17 字段) / `sys_user_tag`(11) / `sys_user_relation_tag`(8) / `sys_user_subscription_rule`(22) / `sys_user_notification`(16，建而不装，依赖 R8)。⚠️ 2026-11-02 归属三次校正：① display 只读 BFF（`application.yml:23`）不得落表；② `ARCH-DISPLAY-01.md:513`「写 `app_user`」是 **A9 未定**时旧表述，现确认 PC 用户 = 统一用户中心 SSO userId（非 `app_user`、非 `sys_user.user_id`），**不 join `sys_user`**；③ 否决 `gkxlumenx_dim`（`code_region` 注释「源 PG `dim.admin_division`」= ETL 同步，写入会被覆盖）与新建 `gkxlumenx_behavior` 库（需新增数据源），**拍板落 `gkxlumenx`** | 李伟 | `lumen-svc-platform` + `lumen-ui-science-pc` | **integration**（2026-11-02 **DDL 已执行**：远程 `10.50.11.76:3306` 库 `gkxlumenx` 五表建成，`EXIT=0`、`information_schema` 实查字段数 17/11/8/22/16 与索引 `uk_user_relation(tenant_id,user_id,relation_type,source_page,target_type,target_id)` 均与设计一致；**后端 17 文件已实现**（4 Entity + 3 DTO + 1 VO + 4 Mapper + Service/Impl + `@Inner` Controller 11 端点 + `@NoToken` Feign 11 方法 + display 转发 11 端点），`mvn compile` **EXIT=0**；**前端 `api/userBehavior.ts` + `useFollow` 服务端化 + 标签管理接线**（`factorTagStore` 改服务端 + 后端 `tags-by-target`，未收藏自动补 follow），`vue-tsc --build` **EXIT=0**；⚠️ **未联调**（Nacos `:8848` 本机/远程均不可达，upms 起不来）；**2026-11-03 已 commit+push**：后端 `lumen-svc-platform` `ad3afe9`（22 文件）+ 前端 `lumen-ui-science-pc` `04ecf8c`（`api/userBehavior.ts` / `useFollow.ts` / `factorTagStore.ts`，3 文件 +470/−91），远程库建表已生效需走查） | handoff `科技发展态势-TS/USER-BEHAVIOR-UNIFIED-TABLE-20261102.md`（设计论点 / 15 功能点落位映射 / 归属决策记录含 dim 与否决项 / 执行验证证据 / 后续 8 项清单） | 需规 excel_row 12「基础信息查看功能」；D4 决策注释 `useFollow.ts`；`ARCH-DISPLAY-01.md` §10.9、§10.9.1、`:513`；`gkxlumen-display/application.yml:23` 只读铁律 | `BE-TS-CONTRACT-01` 冻结（尚未产出）；R8 XXL-Job 未部署（通知实装阻塞）；upms 建表已完成 | 无截至时间 |
| WBS-05-18-17 · `SITUATION-ENT-TREND-FEAT-L01` | 需规「监测数据趋势变化查看功能」剩余子项：趋势预测（基于历史数据预测未来趋势）、异常监测（自动识别标记异常点 / 突变点）——demo 原型无此二子项形态，未实现且此前未登记，本次补登记 | 李伟 | 待定 | **backlog**（待监管人裁定是否纳入本期：demo 无原型、无数据源支撑，属需规超 demo 差集；handoff `科技发展态势-TS/SITUATION-ENT-GAP-FILL-20261102.md` §三） | 需规 excel_row 15；`SITUATION-ENT-SPARK-L01`（真实趋势先行） | 待裁定 | 无截至时间 |

| WBS-05-18-18 · `SITUATION-ENT-INTEGRATION-STATUS-L01` | 影响力 Tab 增第 6 卡「项目（含课题）」走算法库真实产物；出全端点对接进度总台账；display 重打包 + element/innov 拉起 | 李伟 | `lumen-svc-platform` + `gkx-orchestration` | **integration**（2026-11-03，已 commit+push，停人工走查） | 项目卡走 `M_INNOV_PROJECT_INFLUENCE` precompute：58,453 项 / 均分 42.9 / 1986—2021 国自然口径。**产物 `score.top10_v2` 只有 UUID 无项目名**，榜单改出承担机构维度（按承担项目数）+ 条目名后缀「（承担项目）」，`caliberNote` 与 `metricLimitations` 双处声明非对象级榜。顺修 4 处 `Long` 被平台 Jackson 序列化成字符串（`project.item.score` / `enterprise.count` / `service.count` / `dataset.totalCount`）+ 企业均分收敛 1 位小数。部署：display 113.9 MB 重打包重启（`JAVA_HOME` 须切 JDK 17；旧进程不停会让 `repackage` 把 jar 写成 0.2 MB 空壳），element / innov 拉起（此前 DOWN，企业卡与 4 个 innov 端点被假性降级）。台账 `科技发展态势-TS/SITUATION-ENT-INTEGRATION-STATUS-20261103.md`：10 端点 / 11 要素 **8 真 3 mock** / 影响力 6 卡（3 真 + 1 混合 + 2 mock）/ 566 指标 **d4 全 mock** / 10 项真实缺口 | 算法库 `:8000` 通用 `/compute`；**项目名缺失需算法侧把项目名落进产物**才可出对象级榜 | 无截至时间 |
| WBS-05-18-19 · `SITUATION-ENT-SUBSCRIPTION-PUSH-L01` | 订阅推送实装（P0 单模块闭环，承接 05-18-16 后续清单第 6 项「通知实装」，R8 已解除）：XXL-Job 调度器 `subscriptionPushJob` + scope_type 分派命中判定引擎 + global-innovation 4 适配器（region/city/domain/carrier）+ 频率三档（hourly/daily/weekly）闸门 + 通知双写（站内 `sys_user_notification` + 门户 MessageCenterClient） | 李伟 | `lumen-svc-platform`（gkxlumen-display + gkxlumen-upms） | **integration**（2026-11-05 已 commit + push `origin/dev`，待人工签收） | handoff [SITUATION-ENT-SUBSCRIPTION-PUSH-L01](../../../agent-handoffs/科技发展态势-TS/SITUATION-ENT-SUBSCRIPTION-PUSH-L01.md)：upms 3 端点 + 通知实体/Mapper/DTO；display `SubscriptionPushJob` + `subscription/` 4 适配器 + `SubscriptionNotifyService` 双写；`mvn compile` BUILD OK；display 启动日志 `register jobhandler success, name:subscriptionPushJob`；`sys_user_subscription_rule` 0 行，**跑批未端到端验证**（诚实边界已在 handoff 写明） | `SITUATION-ENT-FOLLOW-SVR-L01`（表已建+规则 CRUD ✅）；XXL-Job 已部署（`AnalysisStatusReconcileJob` 在跑 ✅） | 无截至时间 |
| WBS-05-18-20 · `SITUATION-ENT-M1-REAL-DATA-20261105` | M1 科技全域态势真实数据收口：接入外部权威库 `demo_gkxlumenx_ai`（机构 7,842 / 专家 21,316 / 期刊 1,514 / 论文学科 TOP10_X），期刊要素改全量名录 **3,401**（中 2,796 + 英 605，替代 mock 7200 与质量榜 1514），企业影响力按用户裁定改用「综合企业评分」`score_total`（188,775 家 / 均分 37.8），会议维持 mock 1,280；技术产出卡级统计剔除 mock 子类并修 `ISCORR_X→TOP10_X` 口径；收藏补链（`removeFollow` 同步服务端 remove + 打开面板 `refreshFromServer`） | 李伟 | `lumen-svc-platform` + `lumen-topic-py` + `lumen-ui-science-pc` | **integration**（2026-11-05 本地实跑：show-py 8082 新增 demo 只读通道与两端点、display 7099 重打包重启、`/influence` 机构/专家/期刊/论文/企业均真实；`mvn package` BUILD OK + `vue-tsc --noEmit` exit 0；已按用户指令 commit+push） | handoff `科技发展态势-TS/SITUATION-ENT-M1-REAL-DATA-20261105.md`（含 D1–D6 决策留痕 / 数据源行数 / 端点实测 / 7 项剩余缺口）。决策摘要：D1 企业影响力=`enterprise_score.score_total`（用户 2026-11-05 裁定）；D2 期刊=全量名录 3,401；D3 会议保持 mock（算法库 `M_INNOV_CONFERENCE_INFLUENCE` 完全不支持）；D4 其余能接都接；D5 企业影响力不读 demo 库（我方库）；D6 收藏两缺口补链。遗留：会议 / 专利影响力 / 服务机构影响力 3 处 mock，论文仅学科维，收藏端到端待 upms+登录，search-py 未启动降级 | `METRIC-AUTH-DATA-1105-L01`（9 源 / 31 表 / 32.4 万行）；`M_INNOV_ENTERPRISE_INFLUENCE` 仅算法库清单「部分支持、未归久新」；`SITUATION-ENT-FOLLOW-SVR-L01`（收藏表已建） | 无截至时间 |

> 验收（U6）：**本地联调 + 人工走查**（对规约 §11.2「只认 K8s 已发布」的授权豁免，仅本管线有效），走查清单见总控 §4。git 默认只 commit 不 push，走查通过后监管人人工推。同仓 Convoy：`lumen-svc-platform` / `lumen-ui-science-pc` 各同时只派 1 张 coding 单。

### 4.4 WBS-05-19 的子任务（SITUATION-IM 长任务管线 · 创新监测三页数据打通 + 评审就绪）

> **2026-10-28 `human:李伟` 授权长任务**（**授权句已生效：「后续认领不必再问」**）。目标：DS-04 全球 / DS-05 湾区 / DS-06 深圳三页在 `USE_MOCK=false` 下从「裸 fetch 不存在的路由 + 一次性 dataset」跑成「真实后端端点 + 筛选联动 + 诚实空态 + 指标血缘/就绪度角标」闭环。
> **边界口径（与 ENT 不同）**：**可改接口契约；不可改 UI 与实现效果**。ENT 的判据是 `views/situation/**` diff 为零；本管线**额外允许**「接线层（api / types / models / stores）+ 评审层（review / lineage）+ 角标挂载点」，但**只允许接线层动作，不允许任何效果变化**：`styles/*.css` 零 diff、视图结构与组件层级不动、角标关闭后 DOM 零残留（三条判据见总控 §0.1）。
> registry 任务由 coordinator 按 **`human:李伟` 2026-10-28 授权的路径 2**（无 task MCP 工具，直接更新 `task-registry.yaml` + 每份 handoff/commit 注明）建单后回写本表状态列。本管线 `supervised_by` = 总控授权人 `human:李伟`（WBS-05-19 行 FE 口径监管孔东，本管线叶归总控授权人）。
> **开工前勾选已毕（2026-10-28 `human:李伟`）**：C1=①（角标不算 UI 改动，须满足三条判据）· C2=①（registry 授权直改）· C4=①（IM 契约作本期真源）· C10=走查签收 `human:李伟`；C3/C5/C6/C7/C8/C9 按默认① → **勾选表由阻塞件转为留痕件，A0 可开工**。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-19-01 · `SITUATION-IM-A0-L01` | 体检（无代码）：innov 可用端点清单与行数、企业四表脏值复核、三页逐卡片有源/空态判定、**统计数字 ↔ `metric_id` 逐条映射表**、天地图可达性、是否触及结构升级 | 李伟 | `gkx-orchestration`（含 `lumen-svc-platform` 只读核验） | **integration**（2026-10-28 完成体检，待 `human:李伟` 签收） | **体检报告已出** `agent-handoffs/科技发展态势-IM/SITUATION-IM-A0-L01.md`：① innov 现有 34 端点清单，其中≈20 张卡片可直接喂数；② **7 项能力缺 → B2 命中，需 innov 新增 `/internal/*`（结构升级，已升级待批）**；③ 算法侧未就位 → B3 命中，按 C3=① 空态处理；④ **innov 本地未起（7090 未监听**）、display 7099 / element 7082 实测 200、前端 3000 未起；⑤ metric_id 映射：三页对齐约 55 条，映射不上的走红问号；⑥ 天地图 key 已配（公网瓦片，可达性未实测）。**未签 off 前为 integration** | 无 | 无截至时间 |
| WBS-05-19-02 · `SITUATION-IM-R0-L01` | 评审底座：`src/review/` + 组件升级（8 件套 + 就绪度四行 + 自闸）+ readiness 只读镜像 + **`SITUATION-IM-data-gap-catalog.yaml`** | 李伟 | `lumen-ui-science-pc` | **claimed**（2026-10-28 建单，`agent:frontend-agent`，lock 24h） | 未开工。DoD = 三绿 + 关闭评审 DOM 零泄漏 + `pending_hint` 有真源文件 + 样式零新增。**按 C8=① 与 C1 并行**（两仓各一张） | 可与 C 段并行（C8=①） | 无截至时间 |
| WBS-05-19-03 · `SITUATION-IM-C1-L01` | **pilot 首叶 · M6 深圳 `carriers`**：`POST /v1/situation/shenzhen-innovation/carriers`（display + `RemoteInnovClient` + **innov 侧新增 `/internal/innov/v1/shenzhen/carriers`**） | 李伟 | `lumen-svc-platform` | **integration**（2026-10-28 完成实装，待 `human:李伟` 签收） | 交付：innov `ShenzhenController.java` + display `ShenzhenInnovationController.java` + `RemoteInnovClient.shenzhenCarriers`（`@NoToken`↔`@Inner` 配对）。**编译通过**（JDK17）、等价 SQL 实测深圳 3 条有真实经纬度与指数。诚实表：9 字段有源 / 12 字段无源登记 `noSourceFields`，未伪造数值。⚠️ **HTTP 端到端自测未做**：本机缺 Nacos 且 Feign url 依赖其占位符，innov 无法独立启动 —— 记为「未动态验证」，非代码问题。同日已完成 `innovPy` 灌数（`carrier_index` 0→140、`city_index` 0→365 等；正式库零写入） | A0 ≥ integration；与 R0 并行 | 无截至时间 |
| WBS-05-19-04～07 · `SITUATION-IM-C2..C5-L01` | M6 深圳其余 4 端点：`city-benchmark` / `operation-timeline` / `field-distribution` / `indicator-systems` | 李伟 | `lumen-svc-platform` | 待建 | 未开工。**pilot 顺序按 A0 §9 调整**：C1 carriers → C4 city-benchmark → C5 operation-timeline → C3 field-distribution → C2 indicator-systems（最可能 blocked 的排最后） | **C1 验过 pilot 范式后**再放，同仓串行 | 无截至时间 |
| WBS-05-19-08 · `SITUATION-IM-D1-L01` | M6 前端装配接线：api 去裸 fetch + `models/` 装配层 + 页级 store + 空态 | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工。DoD = 三绿 + tabs/styles **零 diff** + 页面实跑 | C1–C5 ≥ integration | 无截至时间 |
| WBS-05-19-09 · `SITUATION-IM-R1-L01` | M6 角标挂载（按 A0 映射表逐数字挂 ⓘ / 红问号 / 🧪） | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工。挂不上的列遗留，**不显伪 8 件套** | D1 + R0 ≥ integration | 无截至时间 |
| WBS-05-19-10～14 · `SITUATION-IM-C6..C10-L01` | M5 湾区 5 端点：`achievements` / `capability` / `swot` / `indicators` / `alerts`（**契约前缀 `bay-innovation`，勿按菜单名改路径**） | 李伟 | `lumen-svc-platform` | **integration**（2026-11-07 后端切久新完成，待 `human:李伟` 签收） | **2026-11-07 后端切久新**：控制器 `BayInnovationController.java` 注入 `RemoteShowPythonClient`（无 `RemoteInnovClient`），achievements / capability / indicators 三端点通久新真实链路；swot + alerts 诚实空态（久新无对应表）。诚实披露：城市有源 8/11（广深珠佛莞惠江肇），港澳中山无源；能力分仅广深惠莞 4 城（我方 ads `capabilityScore`），其余 null；MECH 子指数久新无 → 隐藏；yoy/mom/unit/calcMethod 久新无 → 空态。Python 侧 snake_case → Java camelCase `toSnake()` 统一转换，否则读不到静默取 null。代码已入库 `gkxlumen-display` | — | 无截至时间 |
| WBS-05-19-15 · `SITUATION-IM-D2-L01` | M5 前端接线 | 李伟 | `lumen-ui-science-pc` | **integration**（2026-11-07 三绿 + push，待 `human:李伟` 签收） | **2026-11-07 前端真实数据对接完成**：P0 NaN bug 三修（`bayAreaModel.ts:326` 改 `Number.isFinite`、`IndicatorsTab.vue:446` / `915-916` yoy/mom `fmtPctOrDash()` + NaN 不染红）；P1 硬编码七修（CapacityTab Y 轴自适应 / markPoint 年份动态 / 标题年份 computed、OverviewTab mock 城市绕过真源改 props+fallback+watch、AlertCenterDrawer 伪时间戳诚实化）；type-check（`vue-tsc --noEmit` 零错误）+ build（`vite build` 1m35s）三绿；已 push `origin/dev`（commit `514bd84`） | C6–C10 ≥ integration | 无截至时间 |
| WBS-05-19-16 · `SITUATION-IM-R2-L01` | M5 角标挂载 | 李伟 | `lumen-ui-science-pc` | **claimed**（评审层门控待接） | M5 已具备真实数据链路，指标 8 件套 + 四维就绪度角标挂载待 R0 评审底座就绪后统一挂载；关闭评审模式后 DOM 零泄漏 | D2 + R0 | 无截至时间 |
| WBS-05-19-17～21 · `SITUATION-IM-C11..C15-L01` | M4 全球 5 端点：`achievements` / `realtime` / `carriers` / `alerts` / `cities`（写面 deferred） | 李伟 | `lumen-svc-platform` | **integration**（2026-11-03/04 实质完成，待 `human:李伟` 签收；⚠️ 走法偏离见下） | **未走 pilot 范式**：M4 五端点（+契约外 `relations`/`talents` 共 7 个）实现在独立 `GlobalInnovationController.java`（非 SituationController 契约路径），数据源走 `RemoteShowPythonClient` → `gkx_show_service` 久新 Doris 真实链路（非 innov `/internal/*`）。实测：achievements 五类型 100/100 条带领域（论文/项目 100% 经 topic 维表）、carriers 100/100、cities/talents 100%（talents `with_location` 100% 有坐标）、realtime KPI 11 币种经费；代码已 push（`lumen-svc-platform b453975+a0f9e46`、`lumen-topic-py cc77099+97cd284`，CI 发版）。`alerts` 无预警事件表维持空态（同铁律）。偏离留痕 `agent-handoffs/科技发展态势-TS/M4-REMEDIATION-20261103.md` §12-13。**2026-11-06 更新**：`alerts` 改为读 mock 演示表 `gkxlumenx.sys_innovation_alert_mock`（6 条，`is_mock=1`，迁移 `db/migration/20261106_m4_alert_mock.sql`），响应透出 `mock=true/mockNote`，前端展示「演示数据（Mock）」角标 —— **该区块数据为 mock，不得当作真实预警**；留痕 `M4-ALERT-MOCK-20261106.md` + `mock-ledger.md` 预警登记节。**2026-11-06 建表已在 dev 库（`10.50.11.76:3306/gkxlumenx`）执行并回读 6 条、`is_mock` 全 1，幂等复跑通过**；`alerts` HTTP 端到端待 upms 起来后复验。真实预警结果表仍缺，算端未上线 | 端到端已验，无需 pilot 前置 | 无截至时间 |
| WBS-05-19-22 · `SITUATION-IM-D3-L01` | M4 前端接线 | 李伟 | `lumen-ui-science-pc` | **integration**（2026-11-06 预警区块接线完成，待 `human:李伟` 签收） | M4 其余区块已接；**2026-11-06 补齐预警**：api `GET/alerts` 接入 + `InnovationAlert` 加 `isMock/mockReason/mockVersion` + 页面「演示数据（Mock）」角标（`IconExperiment`）。⚠️ 预警数据为 mock（见 C11–C15 行）；`alertsMock` 清理随真实预警表上线执行 | C11–C15 ≥ integration | 无截至时间 |
| WBS-05-19-23 · `SITUATION-IM-R3-L01` | M4 角标挂载 | 李伟 | `lumen-ui-science-pc` | 部分完成（关键点位已挂，未逐数字全覆盖） | **integration**（2026-11-06 核实）：已挂 7 处 —— `M_INNOV_DS_04_MONITOR_001/002`（监测）、`M_INNOV_CARRIER_RANK_001`、`M_INNOV_CARRIER_RANK_GLOBAL`（排行）、`M_INNOV_KPI_BOARD`（实时 KPI，经 MetricKpiGrid 按 metricId 挂）、`M_INNOV_ACHIEVE_VALUE`（详情）、`M_INNOV_CITY_MONITOR_GLOBAL`（城市）；`ReviewMetricBadges` 自闸（评审开关开启且 metricId 存在才渲染）。⚠️ D9 严格口径「每个统计数字必有 ⓘ」尚未逐数字覆盖，是否接受「关键点位」口径待 `human:李伟` 拍板 | D3 + R0 | 无截至时间 |

**端点 × 任务 ID 对照**（全部 `POST /display/v1/situation/**`，前端 BASE 写死 `/display/v1/situation`）：

| 页 | 任务 | 端点 |
|---|---|---|
| M6 深圳 | C1 / C2 / C3 / C4 / C5 | `/shenzhen-innovation/carriers` · `/indicator-systems` · `/field-distribution` · `/city-benchmark` · `/operation-timeline` |
| M5 湾区 | C6 / C7 / C8 / C9 / C10 | `/bay-innovation/achievements` · `/capability` · `/swot` · `/indicators` · `/alerts` |
| M4 全球 | C11 / C12 / C13 / C14 / C15 | `/global-innovation/achievements` · `/realtime` · `/carriers` · `/alerts` · `/cities` |

**文件索引（本管线圈）**：

| 件 | 路径 | 作用 |
|---|---|---|
| 长任务总控 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-长任务总控.md` | U1–U12 裁定、边界铁律、叶表、走查清单（§4） |
| 总派单（厚包） | `agent-handoffs/科技发展态势-TS/SITUATION-IM-总派单.md` | 八条铁律、逐叶 DoD、`/goal` 头模板 |
| 契约真源 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-API-CONTRACT-01.md` | 端点 / 入参 / 信封 / 偏离表 / deferred |
| 前置条件与未决项 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-前置条件与未决项.md` | Part A 已具备 / Part B 缺口 / Part C 待拍板 C1–C10 |
| **开工前勾选表** | `agent-handoffs/科技发展态势-TS/SITUATION-IM-开工前勾选表.md` | C1–C10 逐项勾选（`human:李伟` 留痕，开工前必填） |
| 跑任务提示词 | `agent-delivery/prompts/SITUATION-IM-三个创新监测页面整体打通-跑任务提示词.md` | 复制即用执行说明（含 12 处前序纠错） |
| 就绪度真源 | `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml` | 143 条，D4 全 mock |
| 决策纪要 | 本夹 `纪要/2026-10-28-SITUATION-IM-边界与裁定.md` | 拍板记录与理由 |
| 逐叶 handoff | `agent-handoffs/科技发展态势-IM/{task-id}.md` | 每叶一份，`ponytail:` + cost 四字段 |

> **pilot 闸门**：C1–C5 → D1 → R1 必须**先跑通并走查通过一页**，才放 M5 / M4 的 C 段（避免 15 个端点按错误范式批量复制）。
> **停本地**：本管线所有改动 commit 后停本地，**走查通过后由 `human:李伟` 人工推送**（U11）。同仓 Convoy 同 §4.3。

## 5. 展示系统公共底座与跨页物

> 这些不是某一页，但属展示系统整体。按 2026-10-26 `human:淮政玮`「展示系统本身就是集成」的口径归第 5 项。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-25 · `FE-TS-S01` | 前端公共底座：布局 / 筛选 / 地图 / 图表 / 抽屉 / 导出收藏 / Mock 开关 / 九页路由骨架 | 孔东 | `lumen-ui-science-pc` | **done** | handoff `科技发展态势-TS/FE-TS-S01.md`：`WorkbenchLayout` + `FilterBar` 已落成，`FE-TS-01A`～`10A` 全部依赖本叶。规划里其余底座项（S02 天地图 key 迁 env、S03 Mock 开关层、S04～S08）**未见独立任务登记** | 调用链铁律：前端 → Java REST → Python `/internal/*`；`X-Trace-Id` / traceparent 请求头 + 前端埋点；`USE_MOCK=false` 零 fixture | 已完结 |
| WBS-05-26 · `FE-DISPLAY-SMALL-BATCH-A` / `-B` | 展示小屏：批 A 态势 / 指数类首页；批 B 政策 / 成果 / 服务跳转类 | 孔东（批 B 未标注监管人） | `lumen-ui-science-mobile` | 批 A **done**（2026-09-02 `human:淮政玮` 签收）；批 B **backlog** | 批 A handoff `agent-handoffs/FE-DISPLAY-SMALL-BATCH-A.md`：小屏态势 / 指数类 Mock 可翻、CTA 可达。批 B 无 handoff | `小屏断点与裁剪规则.md`。D12：正式开发只在 `lumen-*` | 批 A 已完结；批 B 待定 |
| WBS-05-27 · `LUMEN-DISPLAY-PORTAL-IFRAME-L01` | `lumen-ui-science-pc` 统一门户 iframe 认证对接移植（`systemCode=display`） | registry 未标注 `supervised_by`；`claimed_by` 孔东 | `lumen-ui-science-pc` | **integration** | handoff `agent-handoffs/门户集成-PORTAL/LUMEN-DISPLAY-PORTAL-IFRAME-L01.md`：9 新文件 + 10 处改造完成，六点要求全落地、三绿（type-check / 自检 / build）。**改动停在本地工作区，待孔东人工验收，未 commit / push** | 与 `门户集成-PORTAL` 交叉引用 | 待孔东验收 |
| WBS-05-28 | 展示侧合规对齐与原型校准（原型仓侧纯前端，不走 demo 运行时） | 淮政玮 / 郭万迎 / 孔东 | `demo-ui-science` | 混：`integration` 2 · `pending_test` 3 · `review` 2 · `in_progress` 2 | 分批完成情况：<br>· `FE-DISPLAY-ACHIEVE-ALIGN-L01`(pending_test) — 成果 5 个 New 页已建 + 符合度核查清单，2026-08-07 auto-verify 后待抽查；handoff `展示对齐-DISPLAY/FE-DISPLAY-ACHIEVE-ALIGN-L01.md`（⚠ registry evidence 仍写旧路径 `agent-handoffs/FE-DISPLAY-ACHIEVE-ALIGN-L01.md`）<br>· `FE-DISPLAY-SVC-ECO-ALIGN-L01`(review) — 原地更新 `InnovationEcosystem.jsx`<br>· `FE-DISPLAY-KG-SERVICE-ALIGN-L01`(review) — 策略 A 原地更新 `ServiceDisplay.jsx`，符合度评估正文已迁本目录<br>· `FE-DISPLAY-TECHINDEX-NEW-L01`(integration) — 九域 + 王惠 8 件套 + 唐绍祖算法口径；布局溢出已由 fix 8a46d7d 修<br>· `FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01`(pending_test) — 40/30/20/10 权重派生一致 + node 自检通过，纯前端无后端接口<br>· `FE-DISPLAY-GI-TOPBAR-OVERLAY-L01`(pending_test) — 窄视口顶栏换行修复 + 断言<br>· `FE-DISPLAY-PROTO-TUNE-20260827-L01`(integration) — Wave1 A 包落地 ba7daf8，三态缺口清单落盘；handoff 附 `-开工包.md` / `-缺口清单.md`；明确不碰政策跟踪页与总集单白名单<br>· `FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01`(in_progress，**无同名 handoff 文件**)<br>· `FE-DISPLAY-TOTALCHECK-20260817-L01`(in_progress，registry 未标 `supervised_by`，note 写「监管预定 human:孙英哲」；**无同名 handoff 文件**) | D12：正式开发只在 `lumen-*`；demo 仓只作原型对照，**禁止 merge 进 lumen** | 随各批评审 |
| WBS-05-29 | 展示指标盘点与指标语义卡（DS-01～DS-09 逐菜单 + 展示系统总盘） | 淮政玮 / 王惠 | `gkx-orchestration` | **integration**（9 条）+ **claimed**（1 条） | · `DS-01`～`DS-09-METRIC-OPEN-L01`：9 份 handoff 在 `agent-handoffs/算法库联调-ALGO-LIB/DS-0X-METRIC-OPEN-L01.md`。每条含「核对记录 + 赋号表 + open-loop 机器卡 + id-assign yaml + questions.yaml」。**统一口径：赋号草稿、类型未签、公式 pending `human:唐绍祖`、未写 seed / 展示 catalog / QUESTIONS、不标 done** —— 这是它们长期卡在 integration 的原因<br>· `SCI-DISPLAY-METRIC-L123-INV`(claimed)：handoff `agent-handoffs/SCI-DISPLAY-METRIC-L123-INV.md`，正文 `metrics/inventory/展示系统/SCI-DISPLAY-METRIC-L123-INV.md`（84 KB）。DoD 仍列「全部坚果覆盖 / cite 三态无空」，**未见验收结论** | `产品定义评审规程.md` §3.2；`给人说明-指标与算法工作类型与流程梳理.md` §8.4；`metrics/request/展示系统/A2-GAP-page-catalog.yaml` | 待 `human:唐绍祖` 公式共签后转 signed |
| WBS-05-30 · `SYSINT-MESSAGE-CENTER-L01` | 门户消息中心对接（消息推送开放接口：通知 `portal_notice_msg` / 待办 `portal_todo_msg`），`systemCode=TECH_INFO_DISPLAY` | 李伟 | `lumen-svc-platform`（`gkxlumen-display`） | **integration**（集成底座 done，25 功能点接线 pending） | handoff `agent-handoffs/SYSINT-MESSAGE-CENTER-L01.md`：`MessageCenterClient`（RestTemplate，X-System-Code/X-System-Secret 认证 + 503 退避重试 + 统一响应解析）+ `MessageCenterProperties`/`Configuration` + 通知/待办报文 DTO + `application-local.yml` 配置，`mvn compile` 通过；改动停在本地工作区待验收 | 消息中心对接文档（飞书 wiki `X0rcwvemmiqS28kjthPcjVylnCe`）；`system-secret` 生产走 Nacos 不入 git | 待验收 |

> WBS-05-28 内的 `FE-DISPLAY-ACHIEVE-ALIGN-L01` / `SVC-ECO-ALIGN-L01` / `TECHINDEX-NEW-L01` / `TECHINDEX-MOCK-ALGO-L01` / `SVC-THINKTANK-RECTIFY-L01` 同时在 §1 的对应菜单行出现（成果、生态服务、指数、智库）。那是**菜单视角**的重叠引用，编号归属仍在 05-28，不重复计数。

---

## 6. 完成情况汇总

### 6.1 按状态计数（2026-10-31 快照，读 `task-registry.yaml`）

| 状态 | 条数 | 涉及 WBS 行 / 任务 |
|---|---|---|
| done | **8** | 05-16 `ARCH-DISPLAY-REDESIGN-L01`；05-25 `FE-TS-S01`；05-26 批 A `FE-DISPLAY-SMALL-BATCH-A`；05-08-02～05-08-06（5 条，2026-10-31 完成） |
| ready_to_sign | **4** | 05-12 `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01`；05-08 父 `SYSINT-05-08-L01`（2026-10-31 推进）；05-08-01 `SYSINT-05-08-01-L01`；05-08 挂接 `SVC-PANORAMA-GAP-L01` |
| integration | **25** | 05-15 `BE-TS-CONTRACT-02`；05-18 `FE-TS-01A`；05-01a `FE-TS-02A`；05-02a `FE-TS-03A`；05-19 `FE-TS-04A/05A/06A`；05-21 `FE-TS-08A`；05-22 `FE-TS-09A`；05-24 `FE-TS-10A`；05-27 `LUMEN-DISPLAY-PORTAL-IFRAME-L01`；05-28 `TECHINDEX-NEW-L01` + `PROTO-TUNE-L01`；05-29 `DS-01`～`DS-09-METRIC-OPEN-L01`（9 条）；**11-03 补登 `SITUATION-TS-TRACKING-EVAL-L01` / `-REPORT-L01` / `-PERSIST-L01`（3 条）** |
| pending_test | **3** | 05-28 内 `ACHIEVE-ALIGN-L01`、`TECHINDEX-MOCK-ALGO-L01`、`GI-TOPBAR-OVERLAY-L01` |
| review | **4** | 05-17 / 05-17b `ARCH-TS-L3-DESIGN-01`、`ARCH-TS-L3-01`（待 `human:徐滕强` 裁决 A1–A6）；05-28 内 `SVC-ECO-ALIGN-L01`、`KG-SERVICE-ALIGN-L01` |
| claimed | **8** | 05-10 `BE-TS-CONTRACT-01`；05-11 `BE-TS-AGG-01`；05-20 `FE-TS-07A`；05-29 内 `SCI-DISPLAY-METRIC-L123-INV`；05-04、05-05、05-06 `SYSINT-05-0X-L01`；05-08 挂接 `SVC-PANORAMA-API-L01` |
| in_progress | **5** | 05-00 `SYSINT-SCHEME-05-L01`；05-23 内 `DISPLAY-POLICY-GAP-AC-L01`、`POLICY-TRACK-OPT-L01`；05-28 内 `SVC-THINKTANK-RECTIFY-L01`、`TOTALCHECK-L01` |
| backlog | **3** | 05-13 `BE-TS-IMPL-01`；05-14 `BE-TS-DATA-01`；05-26 批 B `FE-DISPLAY-SMALL-BATCH-B` |
| ready | **7** | 05-01a / 01b / 02a / 02b / 03a / 03b、05-07（全部 `SYSINT-05-0X-L01`） |
| **合计** | **65** | 另有 05-09（未建任务）不计入。2026-10-27 新增 ARCH-TS-L3 两件；SITUATION-ENT-A0-L01（05-18-01）已建并 `ready_to_sign`。另有 05-18-02～05（管线 C1/C2/C3/D1，registry 待建）不计入 |

> **2026-11-03**：上表仍是 10-31 快照，**没有**把 §4.1b 的政策单算进去（含当日补建的 `BE-POL-IMPL-01`、`BE-POL-DATA-01`、`FE-POL-REAL-01` 三张 backlog）。`DISPLAY-POLICY-GAP-AC-L01` 现为 integration，不再算 in_progress。政策单状态以 §4.1b 为准，不在这里重算总条数。

### 6.2 当前卡点

| # | 卡点 | 影响的行 | 谁能解 |
|---|---|---|---|
| C1 | `BE-TS-CONTRACT-01` **M0 未评审通过 / 契约未冻结**（已过原定 2026-10-15） | 05-10 自身，以及下游全部 `FE-TS-*` 复刻页（05-18 / 05-19 / 05-21 / 05-22 / 05-24）的 REST 联调闸门 | M0 三方：孔东 / 徐滕强 / 唐绍祖 |
| C2 | 05-10、05-11 的完成日期要求**已过期、待重定** | 05-10、05-11 | 监管人 `human:李伟` |
| C3 | DS-01～09 九张指标语义卡**赋号草稿、公式未签**（2026-08-22 起卡 integration） | 05-29 | `human:唐绍祖` 公式共签 |
| C4 | 页数口径 34 vs 35 未定 | 05-24 是否计入，以及全部菜单计数 | 会签前由 `human:淮政玮` 定 |
| C5 | WBS-05-09 无监管人、未建任务 | 全部菜单的可见性 | 待指定 |
| C6 | 数据资源（05-04）**供方仍未找到**；久新 42 个 API 未确认 | 05-04、05-11 的久新侧源 | `human:郭万迎` 对外催办（久新侧 李乐 / 任欢） |
| C7 | ~~05-08-02～05-08-06 无监管人、全部 backlog~~ **2026-10-31 已解决**：五个子任务全部 `done`（`human` 判定联调已完成，三页 BFF 端点实测真实数据），监管人同步登记 | 交流 / 竞赛 / 传播三入口 | 已关闭 |
| C8 | ~~`ARCH-TS-L3-DESIGN-01` / `ARCH-TS-L3-01` 有成品无 registry 条目~~ **2026-10-27 已解决**：两条已补登记入 `task-registry.yaml`（status `review`，`supervised_by` = `human:徐滕强`），WBS-05-17 / 05-17b 已可被任务系统索引 | 05-17 / 05-17b | 已关闭 |
| C9 | **`ARCH-TS-L3-01` §7 六项待裁决 A1–A6 未签署**，L3 归属（`gkxlumen-element` vs 复用 `topic-*`）未定；`BE-TS-IMPL-01` 因此开工无依据 | 05-17 / 05-17b / 05-13 | `human:徐滕强` 逐项签署 |
| C10 | **A5 久新主体键是否对齐**未答复（`ARCH-TS-L3-01` 标为最大技术风险），`channel/jiuxin-*` 只能出桩实现 | 05-17b、05-18 的久新要素 | `human:郭万迎` 向久新催办（侧 李乐 / 任欢） |

### 6.3 变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-03 | **科技数据资源后台接口建单**：方案改为四个 Dataset GET。建 `DR-RES-A0/DDL/LOAD/C1–C4/D1`，契约沿用 `BE-DR-CONTRACT-01`。总控 `科技数据资源-DR/DR-RES-长任务总控.md`。表名 `gapfill_dr_*` |
| 2026-11-03 | **科技数据资源对照 GDF 签收**：`SYSINT-05-04-01-L01` 由 `human:淮政玮` 签收为 done。结论不变：70 条可得到 0、部分得到 29、得不到 41 |
| 2026-11-02 | **科技数据资源对照 GDF**：WBS-05-04-01 监管人改为淮政玮，状态随 `SYSINT-05-04-01-L01` 到 ready_to_sign。结论见 `agent-handoffs/SYSINT-05-04-01-L01.md`：70 条可得到 0、部分得到 29、得不到 41 |
| 2026-11-02 | **科技数据资源对照 GDF**：WBS-05-04 下新增子任务行 05-04-01（`SYSINT-05-04-01-L01`，backlog）。只分析四视窗展示需求哪些可从已建成 GDF 得到，不代替 `SYSINT-05-04-L01`，不新开 GDF 派单包。监管人待指定 |
| 2026-10-22 | 草案梳理；按已写明姓名补建开发任务并回写任务号 |
| 2026-10-23 | 方案签收后改回处理中；05-04 / 05-06 监管人变更登记 |
| 2026-10-26 | `SVC-PANORAMA-*` 挂接 05-08；`human:淮政玮` 定「展示系统整体归第 5 项」 |
| 2026-10-27 | **扩为全菜单 + 全任务归集**：新增 05-15～05-29 共 15 行（技术架构设计组 05-15～05-17、缺失菜单 05-18～05-24、跨页公共物 05-25～05-29）；每行补「完成情况 · handoff」列；`BE-TS-IMPL-01` / `BE-TS-DATA-01` 由 `human:李伟` 认领 |
| 2026-10-27 | **补登记 `ARCH-TS-L3-DESIGN-01` / `ARCH-TS-L3-01`** 入 `task-registry.yaml`（status `review`，监管 `human:徐滕强`，`E-FE-TECH-SITUATION`）；WBS-05-17 拆为 05-17 / 05-17b 两行（同一设计的两个载体）；任务总数 62 → 64；卡点 C8 关闭，新增 C9（A1–A6 未签署）、C10（A5 久新主体键未答复） |
| 2026-10-27 | **DS-01 企业维度数据跑通长任务挂接**：WBS-05-18 下新增子任务行 05-18-01～05（`SITUATION-ENT-A0/C1/C2/C3/D1-L01`，registry 待 coordinator 走 MCP 建单）；总控/总派单/契约草案 3 份落 `agent-handoffs/科技发展态势-TS/`；授权人 `human:李伟`（U1–U8 已拍板：influence 纳入一期、`enterprise_score` 占位、对象级点位纳入、全局 `USE_MOCK=false`、lumen 现实现为契约真源、本地联调+人工走查验收、就绪度角标不纳入） |
| 2026-10-27 | **A0 叶完成**：`SITUATION-ENT-A0-L01` 建单（MCP）→ 认领 → `ready_to_sign`（AV-0 过，evidence/cost 已回填）；体检报告 + `/map` 基线存档落 `科技发展态势-TS/`；发现并修复 element 本地旧实例僵死（环境操作，未改业务代码） |
| 2026-10-27 | **C1 叶完成**：`SITUATION-ENT-C1-L01`（api-agent，监管李伟）→ `integration`：新增 `GET /v1/element/enterprise/points`（对象级点位），自测 4 组 + 单测 7/7 绿；单据按总控 §6.2「A0 有 handoff 即解锁 C 段」以 backlog 建单（registry ready 门禁要求依赖 done，A0 待签收）。同步修正：真网关地址 = `10.50.69.111:30895`（Nacos 无 gkxlumen-element → K8s 路径缺口） |
| 2026-10-28 | **地域范围支持选到整市**：用户要求「可以选到深圳市」。查 Arco 源码确认不是配置问题——`cascader-option.js` L61-73 只在 `option.isLeaf` 时回调选中，父节点点击只展开，且无 `change-on-select`（第一版按 antd 习惯加的同名属性是无效的，已撤并在注释写明依据）。改在数据层：`withCityWholeOption()` 给每个有下级的城市补叶子子项（label=`深圳市（全市）`、value 仍取城市名），选中后 `regionPaths=[["深圳市"]]` 由 `resolveRegionPath` 还原，后端 `scopeOf` 按 city 聚合；区县路径 `[["深圳市","南山区"]]` 不受影响；回显用 `:format-label` 只显示末级，避免「深圳市 / 深圳市（全市）」重复。页面实跑：选「深圳市（全市）」→ 回显「深圳市（全市）」/ scope「城市：深圳市」/ KPI 95,600 家；选南山区回归 16,039 家不变。type-check 0、build ✓。留痕同 §五之五 |
| 2026-10-28 | **走查反馈第 6 条追加修复（地图定位滞后一拍）**：用户复测报「切换后地图中心点是第二次切换才换到第一个点的位置」。根因：补适配的 watch 用 `focusPositions.length` 判断数据更新，而深圳→南山这类切换点位数恒为 1（30→30 同理）→ 切换瞬间那次 fit（旧坐标）之后不再纠正；第一版的一次性 `pendingScopeFit` 标记也会在"旧数据 fit 成功"时被清掉（组件重挂必踩）。改为**坐标签名**（点数+首尾点）比对 + `lastFocusedKey` 记录已适配签名，签名不同即适配；零点回落不记签名，等数据到达再定位。实测连续切换 南山→福田→罗湖：zoom 10，center 依次 22.553/114.019、22.538/114.050、22.562/114.138，全部即时（修复前第一次切换后仍停在 zoom 3.5 全国视野）。center 是 `regions ∪ objectPoints` 点位云中心，非行政区几何中心。留痕同 §五之五 |
| 2026-10-28 | **走查反馈第 6 条修复（地图与地域范围联动 / 初始定位）**：用户报「地图应随地域范围自动定位，初始化也不该是全球地图」。根因两级：`FactorMapSection` 从不传 center/zoom/fit，`TiandituMap` 只有受控 setView、**无 fitBounds 能力**；默认 `[35.86,104.19]`/zoom 4 + 本页地图面板仅 420×482 → 视野跨 ~90° 经度。按 demo `SharedRegionMap#focusMapToRegions` + `sharedRegionMapViewport.js`（含单测）实现：`focusPositions`（>1 fitBounds / =1 定位 / 0 回落）、`viewportFocusKey`（initial/reset/scope 才 refit，layers 保持用户视口）、`resetView` 改为重新适配当前点位、`zoomSnap 0.25`，并加 **按容器比例自适应的 fit padding**（demo 的 128px 留白在 420px 面板上把 zoom 压到 2，实测修正前视野跨 147°）。**顺带修真 bug**：`/overview` 漏传 `regionPaths` → 选地域级联后 KPI/趋势/分布仍全量、与地图对不上（已补类型+入参+watch key）。页面实跑：初始 zoom 3.5 / 视野覆盖中国 / 30 标记；选南山区 → zoom 10 定位南山 / KPI 16,039 家 / scope「区县：南山区」（修正前地图完全不动、KPI 189,115）。**观察项未改**：地域级联单选点城市只展开不落选（只能选到区县），需产品定 `change-on-select` 或确认交互。留痕 `SITUATION-ENT-C6-L01.md` §五之五 |
| 2026-10-28 | **走查反馈第 5 条修复（统计指标与图脱节）**：用户报「统计指标展示功能和图关联有问题，对不上，有时还点不上」。三个根因：① 饼图判定 `chartType==='pie' || statMetric==='share'` → 「分布比例」下点折线出现「按钮亮折线 / 标题写折线 / 实际画饼」三处不一致；② 取值口径混用——「数量统计」用百分比 `value` 而非 `rawValue`（家），「增长趋势」拿同一年分布占比充时间趋势；③ 交互死角——growth 下饼图 `disabled` 无说明、指标下拉用 `:selected` 非受控。修复：抽出 `effectiveChartType` 作唯一真源（按钮/标题/渲染统一）、`sliceValue` 按指标取 rawValue 或 value（图例千分位/两位小数）、增长趋势改用后端 `trendSeries`（折线多序列 + 柱状按年一根）、`v-model` 受控、disabled 加 title、CSV 导出跟随指标（数量/占比/年度序列）。页面九宫格实跑全一致，导出提示正确，`pageerror` 0，type-check exit 0。留痕 `SITUATION-ENT-C6-L01.md` §五之四 |
| 2026-10-27 | **走查反馈第 4 条修复（领域分布饼图 >100%）**：用户报「饼图显示超过 100%，可能是数量直接拼的」——确认属实。`buildVisibleSlices()` 把 `enterpriseCount`（如 186842）直接当切片 `value`，而 demo 契约（`normalizeRows`）输出的是归一化百分比，前端模板无条件渲染 `{{value}}%`。已修为 2 位小数百分比 + `rawValue` 保留数量（int，避免 Long 被序列化成字符串），并用**最大余数法**保证合计恰 100.00%（直接末项补齐会把合成生物 26 家抹成 0%）。页面实跑：98.86/0.58/0.49/0.04/0.02/0.01，合计 100.00%，无 >100% 项。**附带上报**：① 源表 `ads.enterprise_domain_dist` 2025 年人工智能 ratio 本就是 98.86，饼图「一整块」是数据倾斜非渲染 bug；② demo 的分布图恒画百分比，「数量统计」标签与数据不对应属原型瑕疵，未擅改。留痕 `SITUATION-ENT-C6-L01.md` §五之三 |
| 2026-10-27 | **待数据侧交付：ADS 逐年企业存量快照**（阻塞 KPI「企业」卡 sparkline；用户裁定「等 ADS」，不做累计注册近似）。需求已写成可执行契约：`year` + `total_count`（建议带 city/district），年份 2020–2026，**末点须等于同筛选条件下的存量总量**（无筛选 189,115），含注销/异常须给 `status` 列或口径说明。接上后改 element `/trend`（`mode=stock`）+ display `buildFactorCards()` 的 `series`，前端零改动；验收＝卡上数值 == sparkline 末点。原型依据：demo `overviewData.js` L89-94 `enterprise.rawValues`（6.8→9.2 万家，年份轴 2020–2026）为逐年**存量**口径，与卡上数值同口径。详见 `SITUATION-ENT-C6-L01.md` §五之二末尾 |
| 2026-10-27 | **KPI 卡片口径收敛（方案 B，用户裁定）**：用户追问「为什么要拆成 5 张、是需规要求吗」，追溯结论为**无任何书面依据、实现者自选**（SRS O-02 要求四类资质**并集去重为一个值**、§354 把四类定位为梯度培育**筛选项**；demo 原型与 lumen 冻结 mock 均只有 1 张「企业」卡，无 `unicorn`/`gazelle` key；总控文档的「KPI 五值」是本管线自写的走查清单，属自证循环）。数据侧证明拆开有害：专精特新 14,903 家中 14,707 同属高企，四项相加 43,594 而并集去重仅 **28,185**（虚高 55%）。故按用户选定的 **B（对齐原型）** 收敛为 1 张「企业」卡，删 `seriesOf` 与无用的 `typeDist` 调用；前端零改动。五组筛选复测全 200（189,115 / 深圳 95,600 / 南山 16,039 / 腾讯 19 / 2025-2026 3,183），页面 `.stat-cell--factor` 1 张、`独角兽`与`瞪羚` 0 次出现。留痕 `SITUATION-ENT-C6-L01.md` §五之二 |
| 2026-10-27 | **走查反馈第 3 条修复（KPI 卡重复）**：用户问「独角兽企业有五个，是不是改出来的 bug」。定位为**前后端接缝的键值冲突**：后端 5 张卡 `factorKey` 全是 `enterprise`（要素维度），前端 `OverviewTab.vue` 却拿 `factorKey ?? key` 当卡片主键 → Map 互相覆盖只剩最后一张（unicorn）、键列表仍有 5 个 → 渲染 5 张「独角兽企业 167 家」。**非 C4/C5 引入、非平台历史代码**（`SituationController.java` 是本长任务新增未跟踪文件），是本轮装配 KPI（C3/D1）即埋下、D1 冒烟漏看。已修：前端抽出 `cardKey(item)=item.key` 作卡片身份键（`metric-id` 保留 factorKey 语义），并修同款撞键让地域导出行不再全写成「167家」。页面实跑 5 张卡各自正确（189,115 / 27,936 / 14,903 / 588 / 167）。**待产品确认**：demo 原型这张卡是要素粒度的「企业数」，是否收敛成 1 张未擅改。留痕 `SITUATION-ENT-C6-L01.md` §五之二 |
| 2026-10-27 | **走查反馈第三叶完成（C6）**：`SITUATION-ENT-C6-L01`（要素比较 `/compare` 端点从无到有 + 前端切回真实调用，**契约 bump v1.3** 新增可选 `notes` 承载口径备注）。用户原话「只有一个要素可以先无法验证但要补全接口」→ 落为：接口入参齐全（地域/关键词/年份全部真实生效），但**只有 enterprise 有真实年度序列，故不伪造第二条曲线**，UI 如实显示「当前可比要素 (1/4)」。自测中揪出并修复 `scopeOf` 只认 `regionPaths` 导致 compare/influence 地域筛选**静默忽略**的问题。handoff `科技发展态势-TS/SITUATION-ENT-C6-L01.md`；改动停本地未 commit |
| 2026-10-27 | **走查反馈两叶完成（C4/C5）**：`SITUATION-ENT-C4-L01`（筛选参数贯通——根因 display /map /overview 不消费入参，加 `Scope` 翻译层 + element `appendScope` 统一过滤；级联选项刻意不随筛选收缩）、`SITUATION-ENT-C5-L01`（`/cluster` 端点从无到有 + 前端接线；四维只接三真源，**growth 无源留空桶不补 0**；排掉 `centrality_norm/pagerank_score` 冒充第二维度）。过程中自测揪出并修掉自写 bug：SQL 片段缺尾空格导致 `?ORDER BY` 语法错误，且被「分区降级」吞成空数组——**无过滤用例全绿、只有传参才炸**。两叶 handoff 合并落 `科技发展态势-TS/SITUATION-ENT-C4C5-L01.md`；改动停本地未 commit |
| 2026-10-27 | **C2/C3/D1 叶完成（管线代码面收口）**：`SITUATION-ENT-C2-L01`（/map objectPoints 0→100，对照 A0 基线其余字段逐字节一致 + 降级演练）、`SITUATION-ENT-C3-L01`（/influence 实现，**契约 bump v1.2** 修正响应结构，6 组自测 + 降级 200）、`SITUATION-ENT-D1-L01`（USE_MOCK=false + api 层诚实空态 + vite 代理剥 `/display` 前缀，三绿 + 浏览器冒烟真实数据渲染）。四叶均 integration 待人工签收；**发现并记录：本地联调 401 真凶 = 无网关时 `/display` 服务前缀无人剥**。全部改动停本地未 commit，等人工走查（总控 §4）后统一推 |
| 2026-10-31 | **05-08 六个子任务全部 done + 父任务推进 `ready_to_sign`**：`SYSINT-05-08-02/04/05/06-L01` 回写 `done`，六份 handoff（`SYSINT-05-08-02/03/04/05/06-L01.md` + `SYSINT-05-08-决策与过程记录.md`）落 `agent-handoffs/`；父 `SYSINT-05-08-L01` 由 `claimed` 推进 `ready_to_sign`（`ready_to_sign_at` / `sign_off_requested_at` = 2026-10-31），待监管人签收。三仓（`lumen-ui-science-pc` `78fce5e` / `lumen-svc-platform` `d5728d3` / 本仓 `77fa6606`）已推 `origin/dev`。§6.1 计数：done 3→8、claimed 9→8、ready_to_sign 3→4，合计 65 不变；卡点 C7 关闭 |

---

## 7. 与 [技术方案.md](./技术方案.md) 的差异（待同步）

> 技术方案由 `human:淮政玮` 监管、`agent:doc-agent` 执行，当前仍是 **in_progress**（2026-10-23 曾签收，同日改回）。这次扩范围**先落到本表**；技术方案正文按新口径改写属于方案任务自身的工作，本表不代改，只把需要跟着改的地方列清楚。技术方案修改前，下面各行仍按现稿执行；二者冲突时，任务索引以本表为准，范围口径以本次 2026-10-27 扩范围裁定为准。

| # | 技术方案现稿位置 | 现稿写法 | 新范围下的改法 |
|---|---|---|---|
| D1 | §1.2 集成需求表、`不进本项` 段 | 明确写「不进本项：政策跟踪、全域 / 湾区 / 深圳监测、科技创新评估、科技指数、科技发展规划、维护页」 | 这些菜单已在 §1 索引、落到 05-18～05-24，删除该排除行 |
| D2 | §5 分模块对接表 | 只有 WBS-05-00～05-09 九行 | 扩为 §1 的全菜单行 + §3 技术架构设计组 + §5 跨页公共物组 |
| D3 | §2.1 应用架构「展示 Java 使用哪一个已经存在的服务：还没有」 | 仍写「还没有」 | `ARCH-DISPLAY-01.md` A1 / A10 已裁定：`gkxlumen-display` 为聚合 BFF，唯一对外 `/display/v1/**`，且 `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01` 已部署上线（health UP）。此项可写成已定，不再是「还没有」 |
| D4 | §1.3 对接系统说明 | 写「Doris 直连不写入本方案的调用方向」 | ARCH A3 已准予「过渡期直连久新只读库」，但须登记切换条件与隔离措施；「写不写」待 `human:淮政玮` 在方案里定 |
| D5 | §1.1、§4.1 | 「2026-10-20 妙记把 560 余个指标比对记为我方待办」 | 与 `DS-0X-METRIC-OPEN-L01`、`SCI-DISPLAY-METRIC-L123-INV`（05-29）挂钩，逐条对齐仍没有完成，保持「还没有」 |

---

## 8. 明确不在本表（保留边界）

- 第 1 项范围内的政策跟踪、全域 / 湾区 / 深圳监测等**若改由第 1 项自研**，则从本表相应行撤下并改标为「跨项索引」。现状：这些页仍未划到第 1 项叶，故留在本表 05-19 / 05-20 / 05-21 / 05-22 / 05-23；一旦改判，立即改标为「跨项索引」。
- 知识图谱四页 DS-21～24 归第 7 项。本表只做索引行，不建叶、不重画查图时序。
- 第 2 项的三要素供数（WBS-02-01、WBS-02-02）。本表只记菜单侧消费。
- 第 6 项的数据工厂作业。本表不新开 GDF 包、不加字段。
- 统一登录产品本身。本表只有 WBS-05-09 的菜单注册与权限配置动作。
- 大型科学仪器的预约闭环；报价表划掉且工作量为 0 的行（含「维护技术图谱」）。
- 第 3 项、第 4 项的专题页面与门户页面：只在 §5 的 WBS-05-27 作为交叉引用出现，页面本体不属于展示系统。

