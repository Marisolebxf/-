# WBS · 展示系统集成

> **2026-10-27 扩范围（本次变更）**：技术方案的范围口径改为「**展示系统全部目录菜单**」。本表随之从「九个对接菜单」扩为 **七模块 30 叶（DS-01～DS-30）+ 政策核增 PC-1～PC-4 + 维护管理（M10）**全覆盖，并把**展示系统相关的全部已提交任务**（含之前提交的技术架构设计类任务）归集进来逐叶可索引。每叶补「完成情况 · handoff」列，把对应 handoff 写回本表。
> **2026-10-22 梳理**。方案任务 `SYSINT-SCHEME-05-L01` 于 2026-10-23 由 `human:淮政玮` 签收后，同日改回处理中。菜单范围与调用方向以 [技术方案](./技术方案.md) 现稿为准。同日按已写明的人员姓名补建开发任务，任务号回写本表。WBS-05-09 监管人仍是待指定，未建任务。
> **2026-10-22 晚**：草稿已确认作建叶底稿。已有监管人即负责人。完成日期要求取倒排「功能开发」计划完成时间（11月倒排计划 · 科技信息展示系统）。页面计划里冲出该日的叶结束日不写入。开始时间仍待填写。这两列是我方栏位，不是对端承诺。方案行与菜单注册行在倒排里没有单独的功能开发完成日，仍为无截至时间。
> **2026-10-26 `human:淮政玮` 口径**：「展示系统本身就是集成，整体放到展示系统集成」。据此，展示系统的跨页公共物与技术架构设计件也归第 5 项，不再散落在原页面计划。
> **2026-10-27 `human:李伟` 建叶登记**：原以「挂接登记」记入的五件转为正式叶，任务号不变（沿用已有 ID，未新建）；原无监管人的 `BE-TS-IMPL-01`、`BE-TS-DATA-01` 由 `human:李伟` 认领。派单说明见 `agent-handoffs/科技发展态势-TS/派单说明/`。
> **2026-10-28 `human:李伟` 挂接**：创新监测三页（DS-04/05/06）数据打通长任务 `SITUATION-IM`（**23 叶**，WBS-05-19-01～23）挂接 **§4.4**，授权句已生效；边界口径：**可改接口契约，不可改 UI 与实现效果**（角标挂载点属评审层叠加，须满足总控 §0.1 三条）。总控 / 总派单 / 契约 / 前置条件四份：`agent-handoffs/科技发展态势-TS/SITUATION-IM-*.md`；决策纪要本夹 `纪要/2026-10-28-SITUATION-IM-边界与裁定.md`。
> **2026-11-03 挂接**：科技政策跟踪正式复刻单已在 registry。父行 `WBS-05-23` + 子行 §4.1b。同日补建真数链三张单，并补建存量调研 `POL-DISPLAY-SURVEY-L01`、系统详细设计 `POL-DISPLAY-SDD-L01`。编写顺序是调研 → 详设 → 契约。前后依赖见 [对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md)。专题 `E-E7-POLICY-M1-L06` 不作为展示前置。
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
- `WBS-05-23-0N` 是 `WBS-05-23` 的**子任务行**（科技政策跟踪）。05-23-01～10 挂已有复刻单与契约单；05-23-11～13 是实现、对齐、真联调；05-23-14～15 是存量调研与系统详细设计。不另算菜单。
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
| 科技发展态势 | DS-01 | 科技全域态势 | WBS-05-18 | `FE-TS-01A`(integration)、`BE-TS-IMPL-01`(backlog)、`BE-TS-DATA-01`(backlog)、`DS-01-METRIC-OPEN-L01`(integration)、`SITUATION-ENT-*` 长任务管线（10-27 挂接，待建，见 §4.3） | 前端整页复刻已 push、三绿；REST 待 `BE-TS-CONTRACT-01` 冻结。指标语义卡仍草稿未签。10-27 起企业维度数据跑通长任务挂接本行 | LT-5-SIT-DS01 |
| 科技发展态势 | DS-02 | 科学技术全景 | WBS-05-01a / 01b | `SYSINT-05-01A-L01`(ready)、`SYSINT-05-01B-L01`(ready)、`FE-TS-02A`(integration)、`DS-02-METRIC-OPEN-L01`(integration) | 对接叶已建号未开工；复刻页 integration；读图归第 7 项 | LT-5-SIT-DS02 |
| 科技发展态势 | DS-03 | 技术发展跟踪 | WBS-05-02a / 02b | `SYSINT-05-02A-L01`(ready)、`SYSINT-05-02B-L01`(ready)、`FE-TS-03A`(integration)、`DS-03-METRIC-OPEN-L01`(integration) | 三个 Tab 可开或空态；材料未到时空态。名称收口为「技术发展跟踪」 | LT-5-SIT-DS03 |
| 科技发展态势 | DS-04 | 全球创新监测 | WBS-05-19 | `FE-TS-04A`(integration)、`DS-04-METRIC-OPEN-L01`(integration)；已有 `E-INNOV-M1-L08`（tier FULL，路由 `/innov`）；**`SITUATION-IM-*` 长任务管线（10-28 挂接，待建，见 §4.4）** | 综合 / 实时 / 载体 / 监测 / 能力五块可切换；不另起一套 innov 地图 | LT-5-SIT-DS04 |
| 科技发展态势 | DS-05 | 湾区创新监测 | WBS-05-19 | `FE-TS-05A`(integration)、`DS-05-METRIC-OPEN-L01`(integration)；同上 `SITUATION-IM-*` 长任务管线（见 §4.4） | 成果地图 / 四维 / SWOT / 指标四块已完成，联调待 REST | LT-5-SIT-DS05 |
| 科技发展态势 | DS-06 | 深圳创新监测 | WBS-05-19 | `FE-TS-06A`(integration)、`DS-06-METRIC-OPEN-L01`(integration)；同上 `SITUATION-IM-*` 长任务管线（**pilot 起点**，见 §4.4） | note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」；**模块目录无同名 `FE-TS-06A.md`** | LT-5-SIT-DS06 |
| 科技发展态势 | DS-07 | 科技创新评估 | WBS-05-20 | `FE-TS-07A`(claimed，P2)、`DS-07-METRIC-OPEN-L01`(integration) | 复刻未开工；评估对象范围未补则按详设空态 | LT-5-SIT-DS07 |
| 科技发展态势 | DS-08 | 科技指数 | WBS-05-21 | `FE-TS-08A`(integration)、`FE-DISPLAY-TECHINDEX-NEW-L01`(integration)、`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01`(pending_test)、`DS-08-METRIC-OPEN-L01`(integration) | 九域 + 8 件套 + 算法口径页已出，布局溢出由 fix 8a46d7d 修；mock 权重（40/30/20/10）一致性已修待抽测。**只做展示侧，不做智库后台** | LT-5-SIT-DS08 |
| 科技发展态势 | DS-09 | 科技发展规划 | WBS-05-22 | `FE-TS-09A`(integration)、`DS-09-METRIC-OPEN-L01`(integration) | 综合规划 / 重点领域 / 研究分析可切换；预警模型可 501，不编制规划正文 | LT-5-SIT-DS09 |
| 科技发展态势 | — | 维护管理（M10 · `/trend/maintain/*`，不另开一级菜单） | WBS-05-24 | `FE-TS-10A`(integration) | 图层与数据源、技术图谱关键实体与关系维护；无权限是降级不是白屏。**报价表划掉且工作量为 0 的「维护技术图谱」不实现** | LT-5-SIT-OPS |
| 科技政策跟踪 | DS-10 | 科创政策全景 | WBS-05-23-03 / 04 | `FE-POL-01A`(pending_test)、`FE-POL-01B`(integration)；基座 `FE-POL-S01`(pending_test) | 检索主链路待测试；其余 4 Tab 联调中，硬依赖 01A。真数等 `BE-POL-CONTRACT-01` | LT-5-POL-DS10 |
| 科技政策跟踪 | DS-11 | 政策分析评价 | WBS-05-23-05 | `FE-POL-02A`(pending_test) | 整页复刻待测试。硬依赖只有基座，与全景可并行。模型未注册保持 501 | LT-5-POL-DS11 |
| 科技政策跟踪 | DS-12 | 政策效果推演 | WBS-05-23-06 | `FE-POL-03A`(integration) | 双工作台联调中，停本地待验收。推演 ≠ 专题布局推荐 | LT-5-POL-DS12 |
| 科技政策跟踪 | PC-1～PC-4 | 政策数据治理 / 智能政策拆解 / 多维政策对比 / 智能研报生成 | WBS-05-23-07～10 | `FE-POL-04A`(in_progress)、`05A`(integration)、`06A`(integration)、`07A`(ready_to_sign) | 四页硬依赖都只是基座。ChainSteps 归 04A，06A/07A 仍是占位。PC-4 Job 未注册则 501 | LT-5-POL-PC1～PC4 |
| 科技人才态势 | DS-13～DS-16 | 全球领域人才态势 / 关注地区人才态势 / 重点科技人才画像 / 人才引进推荐评估 | WBS-05-03a / 03b | `SYSINT-05-03A-L01`(ready)、`SYSINT-05-03B-L01`(ready) | **只做菜单壳与非三要素区块**；四子页不重做，供数是 WBS-02-01（第 2 项）；资讯、职位变动、奖项荣誉、引进成本、尽调五类空态 | LT-5-TAL-DS13～DS16 |
| 科技数据资源 | DS-17～DS-20 | 总体 / 接入 / 主题 / 应用四视窗 | WBS-05-04 | `SYSINT-05-04-L01`(claimed，监管 淮政玮 → 实际认领 孔东) | 四个视窗可切换；共建数据未到为空态。R6：data 组供方未找到（原华为云 2026-10-15 退出）。对照已建成 GDF 的分析见 WBS-05-04-01 | LT-5-RES-DS17～DS20 |
| 科技知识图谱 | DS-21～DS-24 | 分析展示 / 指标展示 / 算法展示 / 服务展示 | **跨项索引（第 7 项）** | `FE-DISPLAY-KG-SERVICE-ALIGN-L01`(review) | 本表**不建叶**。第 7 项负责页面与查图；`FE-DISPLAY-KG-SERVICE-ALIGN-L01` 是 demo 侧 DS-24 服务展示合规对齐，原地更新 `ServiceDisplay.jsx` | LT-5-KG-DS21～DS24 |
| 科技成果展示 | DS-25～DS-29 | 软科学成果展示 / 科技创新生态展示 / 科技时空演进展示 / 大型科学仪器共享 / 创新载体孵化载体 | WBS-05-05 | `SYSINT-05-05-L01`(claimed)、`FE-DISPLAY-ACHIEVE-ALIGN-L01`(pending_test) | 五页可打开或空态；仪器只展示、不做预约闭环；时空演进**禁止用专题 B 面时间轴冒充**；口径未绿用角标不改数 | LT-5-ACH-DS25～DS29 |
| 科技服务全景 | DS-30 之① | 科技创新生态服务（全景里唯一智树自研子菜单） | WBS-05-06 | `SYSINT-05-06-L01`(claimed)、`FE-DISPLAY-SVC-ECO-ALIGN-L01`(review) | 列表与详情可开或空态；demo 侧原地更新 `InnovationEcosystem.jsx` | LT-5-SVC-ECO |
| 科技服务全景 | DS-30 之② | 智库服务 | WBS-05-07 | `SYSINT-05-07-L01`(ready)、`FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01`(in_progress) | 2026-10-23 起**不按跳转**，要求智谱提供接口；接口未到为空态。智树不做高端智库后台。demo 页按需规 566–574 整改中 | LT-5-SVC-HUB |
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
| WBS-05-01b · `SYSINT-05-01B-L01` | 科学技术全景 · 后端（三要素以外） | 唐绍祖 | 展示 Java | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`；三要素供数依赖 WBS-02-02。三要素以外的区块能调到，或返回空；不写假数；三要素算法不在本叶 | 2026-10-30 |
| WBS-05-02a · `SYSINT-05-02A-L01` | 技术发展跟踪 · 前端 | 孔东 | `lumen-ui-science-pc` | **ready** | 已建号未开工。同一菜单的 `FE-TS-03A`(integration)；handoff `科技发展态势-TS/FE-TS-03A.md` | `SYSINT-SCHEME-05-L01`；WBS-05-02b。结果 / 参数 / 方法三个 Tab 可开，或空态；名称用「技术发展跟踪」 | 2026-10-30 |
| WBS-05-02b · `SYSINT-05-02B-L01` | 技术发展跟踪 · 后端 | 唐绍祖 | 展示 Java | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`；三要素供数依赖 WBS-02-02。三个 Tab 的接口可调，或空；专家评估法、经济分析法没有已签收实现，不在本叶新定义口径 | 2026-10-30 |
| WBS-05-03a · `SYSINT-05-03A-L01` | 科技人才态势菜单壳与非三要素区块 · 前端 | 孔东 | `lumen-ui-science-pc` | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`；WBS-05-03b；四子页不重做。菜单可进；非三要素区块有数或空态；四子页不在本叶填数；五类缺失为空态 | 2026-11-05 |
| WBS-05-03b · `SYSINT-05-03B-L01` | 科技人才态势菜单壳与非三要素区块 · 后端 | 唐绍祖 | 展示 Java | **ready** | 已建号未开工 | `SYSINT-SCHEME-05-L01`。四子页供数是 WBS-02-01，本叶不重做四页；非三要素接口可调或空；五类缺失保持空态；不写假数 | 2026-11-05 |
| WBS-05-04 · `SYSINT-05-04-L01` | 科技数据资源（四视窗作为一个菜单） | 淮政玮 → 2026-10-23 改徐滕强 → registry 实际认领 `human:孔东` | `lumen-ui-science-pc`、展示 Java | **claimed** | 监管人两次变更已登记，**未开工** | `SYSINT-SCHEME-05-L01`。对端材料写智谱、未回文前空态；四个视窗可切换；共建数据未到为空态；菜单进统一用户中心 | 2026-11-09 |
| WBS-05-05 · `SYSINT-05-05-L01` | 科技成果展示（五页作为一个菜单） | 徐滕强 | `lumen-ui-science-pc`、展示 Java | **claimed** | 未开工。原型侧的 5 个 New 页由 `FE-DISPLAY-ACHIEVE-ALIGN-L01` 建出（pending_test） | `SYSINT-SCHEME-05-L01`。五页可打开或空态；仪器只做展示，不做预约闭环；口径未绿用角标，不改数 | 2026-11-05 |
| WBS-05-06 · `SYSINT-05-06-L01` | 科技创新生态服务 | 徐滕强 → 2026-10-23 改侯佳伟 | `lumen-ui-science-pc`、展示 Java | **claimed** | 未开工。原型侧对齐见 `FE-DISPLAY-SVC-ECO-ALIGN-L01`（review） | `SYSINT-SCHEME-05-L01`。列表与详情可开，或空态；菜单进统一用户中心 | 2026-11-09 |
| WBS-05-07 · `SYSINT-05-07-L01` | 智库服务 | 李伟（registry 记一线孔东） | `lumen-ui-science-pc`、展示 Java | **ready** | 2026-10-23 起**不按前端跳转**，要求智谱提供接口；接口未到为空态。原型页整改见 `FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01`（in_progress） | `SYSINT-SCHEME-05-L01`。对端是智谱；智树页面能调到智谱接口；**智树不做高端智库后台** | 2026-11-09 |
| WBS-05-08 · `SYSINT-05-08-L01` | 科技交流、科技竞赛、科技传播（父） | 李伟 | `lumen-ui-science-pc` | **ready_to_sign** | 挂接自建任务 `SVC-PANORAMA-API-L01`（父统筹单，claimed）、`SVC-PANORAMA-GAP-L01`（对照表成品，ready_to_sign）。**2026-10-31：六个子任务（-01～-06）全部 done —— -01 对接分析已签收；-02 三入口 iframe 弹窗壳；-03 交流 BFF + FE；-04 竞赛 BFF + FE；-05 传播 BFF + FE；-06 联调验收（实测三页深势真实数据）**。三仓改动已推 `origin/dev`，父任务推进 ready_to_sign 待签收。子任务详见 §4.2 | `SYSINT-SCHEME-05-L01`。对端名称「北大深势」只出现在规约，能力评估文未署此名，**名称核对还没有** | 2026-11-09 |
| **WBS-05-09** | 本项菜单注册与用户权限（全景、技术发展、人才态势、数据资源、成果展示、生态服务、智库、交流、竞赛、传播） | **待指定**（2026-10-22 纪要未点名） | 统一用户中心配置；业务仓不写主机名 | **未建任务** | — | `SYSINT-SCHEME-05-L01`。各菜单叶负责自己的相对路径；这些菜单以相对路径可见，对应用户登录后能进；地址不写主机名；交流 / 竞赛 / 传播跳转失败仍有提示；智库不按跳转走智谱接口 | 无截至时间 |
| WBS-05-18 | 科技全域态势（DS-01，含 M1 聚合 BFF 消费） | 孔东（FE）/ 李伟（BE） | `lumen-ui-science-pc`、`gkxlumen-display` | **integration** | `FE-TS-01A` handoff `科技发展态势-TS/FE-TS-01A.md`：整页复刻 integration；所依赖的底座 `FE-TS-S01` 已 done。后端 `BE-TS-IMPL-01` 未开工。指标卡 `DS-01-METRIC-OPEN-L01`：赋号草稿、类型未签、公式待 `human:唐绍祖` 共签。**2026-10-27 挂接 `SITUATION-ENT` 长任务管线（企业维度数据跑通，子任务见 §4.3，授权人 `human:李伟`）** | `FE-TS-S01`、`BE-TS-CONTRACT-01` 冻结（M1）。11 要素图层 / 科创事件双 Tab；久新人才、科研机构、论文、专利未到则**空态** | 计划 LT-5-SIT-DS01：10-16 → 10-20 |
| WBS-05-19 | 创新监测三页（DS-04 全球 / DS-05 湾区 / DS-06 深圳） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-04A` / `05A` / `06A` 三份 handoff 均已 push（`06A` note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」，但模块目录**无同名 `FE-TS-06A.md`**）。已有 innov 事件地图只对齐，不另起一套 | `BE-TS-CONTRACT-01`（M4 / M5 / M6 契约未冻结）。订阅 / 推送的对端宋泉未确认则该块空态 | 计划 10-28 → 10-31（DS-06 及以后冲出 V1 开发出门） |
| WBS-05-20 | 科技创新评估（DS-07） | 孔东 | `lumen-ui-science-pc` | **claimed**（P2） | `FE-TS-07A` 仅 claimed，复刻未开工 | 评估对象范围未补则按详设空态 | 计划 11-03 → 11-04（结束日 = V1 测试末日） |
| WBS-05-21 | 科技指数（DS-08） | 孔东 / 淮政玮 | `lumen-ui-science-pc`（正式）、`demo-ui-science`（原型侧） | **integration** | `FE-TS-08A` handoff `科技发展态势-TS/FE-TS-08A.md`（三级指标树 / 34 省地图 / 专家 H 指数 / 四维趋势 / 排行榜 / 20 人评议只读）；`FE-DISPLAY-TECHINDEX-NEW-L01` 九域 + 王惠 8 件套 + 唐绍祖算法口径，布局溢出由 fix 8a46d7d 修；`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01` mock 权重 40/30/20/10 派生一致已修，pending_test | **只做展示侧，不做智库后台**。专家评议 20 人只读 | 计划 11-04 → 11-05（晚于 V1 测试） |
| WBS-05-22 | 科技发展规划（DS-09） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-09A` handoff `科技发展态势-TS/FE-TS-09A.md`：综合规划 / 重点领域 / 研究分析可切换 | 预警模型可 501；**不编制规划正文** | 计划 11-05 → 11-06 |
| WBS-05-23 | 科技政策跟踪（DS-10～DS-12 + 核增 PC-1～PC-4） | 孔东（FE）/ 李伟（契约与实现） | `lumen-ui-science-pc`；demo 原型另计 | **混** | 复刻单见 §4.1b。2026-11-03 另建调研 `POL-DISPLAY-SURVEY-L01`、详设 `POL-DISPLAY-SDD-L01`，以及 `BE-POL-IMPL-01`、`BE-POL-DATA-01`、`FE-POL-REAL-01`。demo 侧仍挂 `DISPLAY-POLICY-GAP-AC-L01`(integration)、`FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01`(in_progress，无同名 handoff)。依赖全文：[对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md) | mock 复刻不等契约。真联调等契约、实现、统计对齐。专题 `E-E7-POLICY-M1-L06` 不是本行前置 | 计划 10-20 → 10-28（DS-10～12 窗内，PC 属 V2）；正式复刻 2026-11-02 已开工 |
| WBS-05-24 | 维护管理（M10 · `/trend/maintain/*`） | 孔东 | `lumen-ui-science-pc` | **integration**（P2） | `FE-TS-10A` handoff `科技发展态势-TS/FE-TS-10A.md`：图层与数据源配置 / 维护技术图谱 / 关键实体与关系维护 / 已有能力入口；无权限是降级不是白屏 | 挂 DS-01 / DS-02，**不另开一级菜单**。**报价表划掉且工作量为 0 的「维护技术图谱」不实现** | 计划 11-06 → 11-07 |

> **页数口径未统一（待定项）**：`formal-docs-registry.yaml` 记 **34 页**（M1 态势 9 页），`ARCH-DISPLAY-01.md` §6.3 记 **35 页**（trend 10 页）。差异应在于 `/trend/maintain/*`（本表 WBS-05-24）是否计入展示页。**会签前需定口径**；定之前本表两说并列，不自选一个。

### 4.1a WBS-05-04 的子任务（科技数据资源四视窗 · 对照已建成 GDF）

> 2026-11-02 建叶。父行仍是 WBS-05-04 · `SYSINT-05-04-L01`（四视窗页面交付）。本行只分析四个视窗的展示需求里，哪些能从已建成的 GDF 平台得到。不代替父行，不新开 GDF 派单包。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-04-01 · `SYSINT-05-04-01-L01` | 科技数据资源四视窗：对照已建成 GDF，分析哪些展示需求可从平台得到 | 淮政玮 | `gkx-orchestration` | **done**（2026-11-03 `human:淮政玮` 签收） | 已签收。结论见 [SYSINT-05-04-01-L01.md](../../../agent-handoffs/SYSINT-05-04-01-L01.md)：70 条里可得到 0、部分得到 29、得不到 41，没有一条能直接填进四视窗 | 需求清单认详设 `07-功能-科技数据资源.md` 与 `科技数据资源-DR/DR-模块开发规划与任务拆分.md` §4（DS-17～20，seq 330–399）。不等 `SYSINT-05-04-L01` 页面做完。分析结论落盘即本叶完成，不是可对端，不新建 GDF 作业 | 无截至时间 |

### 4.1b WBS-05-23 的子任务（科技政策跟踪 · 只挂已有单）

> 2026-11-03 挂接。父行仍是 WBS-05-23。编写顺序是 05-23-14 调研 → 05-23-15 系统详细设计 → 05-23-02 契约。编号按建单先后，不表示施工先后。依赖全文见 [对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md)。
> mock 复刻链：`FE-POL-S01` → 各页；只有 `FE-POL-01B` 再硬依赖 `FE-POL-01A`。真数链在详设和契约之后。专题 `E-E7-POLICY-M1-L06` 不进下表。

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-23-01 · `FE-POL-S01` | 政策跟踪前端基座（菜单 3→7、mock 种子、api 双轨、35 指标镜像） | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-S01.md`。registry note 写已推 `origin/dev`、转待测试；handoff 头仍写停本地。状态以 registry 为准 | 无硬依赖。产品包 `DS10-12-PACK-L01` 已完成 | 无截至时间 |
| WBS-05-23-02 · `BE-POL-CONTRACT-01` | 7 页 63 叶 Java 契约（API-POL）。只出接口契约，不是系统详细设计 | 李伟 | `lumen-svc-platform` | **backlog** | 未开工。规划 `科技政策跟踪-POL/POLICY-模块开发规划与任务拆分.md` §3.1 | WBS 前置是 `POL-DISPLAY-SDD-L01`。注册表 `depends_on` 仍为空（更新工具不能写该字段）。冻结前 FE 不猜路径 | 无截至时间 |
| WBS-05-23-03 · `FE-POL-01A` | 科创政策全景 · 检索主链路 | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-01A.md`。走查后已推 `origin/dev` | 硬依赖 `FE-POL-S01` | 无截至时间 |
| WBS-05-23-04 · `FE-POL-01B` | 科创政策全景 · 动向 / 舆情 / 比对 / 订阅 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-01B.md`。note 写前端链路联调通过，状态仍为联调中 | 硬依赖 `FE-POL-01A` | 无截至时间 |
| WBS-05-23-05 · `FE-POL-02A` | 政策分析评价整页 | 孔东 | `lumen-ui-science-pc` | **pending_test** | handoff `科技政策跟踪-POL/FE-POL-02A.md`。已推 `origin/dev` | 硬依赖 `FE-POL-S01`。与全景无硬依赖 | 无截至时间 |
| WBS-05-23-06 · `FE-POL-03A` | 政策效果推演整页 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-03A.md`。停本地待验收 | 硬依赖 `FE-POL-S01`。模型未注册则真路径 501 | 无截至时间 |
| WBS-05-23-07 · `FE-POL-04A` | 智能政策库构建（政策数据治理） | 孔东 | `lumen-ui-science-pc` | **in_progress** | 无同名 handoff | 硬依赖 `FE-POL-S01`。ChainSteps 归本单，06A/07A 的占位等本单合入后替换 | 无截至时间 |
| WBS-05-23-08 · `FE-POL-05A` | 智能政策拆解 | 孔东 | `lumen-ui-science-pc` | **integration** | note 写 handoff 已落盘；主仓目录未见 `FE-POL-05A.md` | 硬依赖 `FE-POL-S01`。文本解析模型未注册则 501 | 无截至时间 |
| WBS-05-23-09 · `FE-POL-06A` | 多维政策对比 | 孔东 | `lumen-ui-science-pc` | **integration** | handoff `科技政策跟踪-POL/FE-POL-06A.md`。停 worktree 待验收 | 硬依赖 `FE-POL-S01`。生成研报跳 07A，须两边合入同一 `dev` 再验 | 无截至时间 |
| WBS-05-23-10 · `FE-POL-07A` | 智能研报生成 | 孔东 | `lumen-ui-science-pc` | **ready_to_sign** | 主仓目录未见 `FE-POL-07A.md`。note 写未 commit / push，ChainSteps 仍是占位 | 硬依赖 `FE-POL-S01`。Job 未注册则导出 501 | 无截至时间 |
| WBS-05-23-11 · `BE-POL-IMPL-01` | 展示聚合接口实现（`/display/v1/policy/**`） | 李伟 | `lumen-svc-platform` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-CONTRACT-01`。契约未冻结不开工。不实现、不转调 `/topic/v1/policy` | 无截至时间 |
| WBS-05-23-12 · `BE-POL-DATA-01` | 统计读面与已有政策 ADS 对齐 | 李伟 | `gkx-orchestration` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-CONTRACT-01`、`GDF-POLICY-MDC-STAT-L01`。不新开 GDF 包，不写第二套统计脚本 | 无截至时间 |
| WBS-05-23-13 · `FE-POL-REAL-01` | 七页切真实接口并联调 | 孔东 | `lumen-ui-science-pc` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `BE-POL-IMPL-01`、`BE-POL-DATA-01` 与 `FE-POL-01B`、`02A`、`03A`、`04A`、`05A`、`06A`、`07A`。模型未注册保持 501 | 无截至时间 |
| WBS-05-23-14 · `POL-DISPLAY-SURVEY-L01` | 存量调研：七页 × 已有任务 × 指标判定 | 徐滕强 | `gkx-orchestration` | **ready** | 2026-11-03 新建。初稿已在 [对照-科技政策跟踪-存量任务与依赖.md](./对照-科技政策跟踪-存量任务与依赖.md)，本单补全后定稿 | 无硬依赖。不代替契约，也不代替详设 | 无截至时间 |
| WBS-05-23-15 · `POL-DISPLAY-SDD-L01` | 系统详细设计说明书 | 徐滕强 | `gkx-orchestration` | **backlog** | 2026-11-03 新建。未开工 | 硬依赖 `POL-DISPLAY-SURVEY-L01`。说明书会签后才作为 `BE-POL-CONTRACT-01` 的输入。不写 OpenAPI 字段表 | 无截至时间 |

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
| WBS-05-19-10～14 · `SITUATION-IM-C6..C10-L01` | M5 湾区 5 端点：`achievements` / `capability` / `swot` / `indicators` / `alerts`（**契约前缀 `bay-innovation`，勿按菜单名改路径**） | 李伟 | `lumen-svc-platform` | 待建 | 未开工 | **pilot 链路验过**（C1–D1–R1） | 无截至时间 |
| WBS-05-19-15 · `SITUATION-IM-D2-L01` | M5 前端接线 | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工 | C6–C10 ≥ integration | 无截至时间 |
| WBS-05-19-16 · `SITUATION-IM-R2-L01` | M5 角标挂载 | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工 | D2 + R0 | 无截至时间 |
| WBS-05-19-17～21 · `SITUATION-IM-C11..C15-L01` | M4 全球 5 端点：`achievements` / `realtime` / `carriers` / `alerts` / `cities`（写面 deferred） | 李伟 | `lumen-svc-platform` | 待建 | 未开工。`realtime` 的 D2 轮询以 Open Item 结论为准（C5） | pilot 链路验过 | 无截至时间 |
| WBS-05-19-22 · `SITUATION-IM-D3-L01` | M4 前端接线 | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工 | C11–C15 ≥ integration | 无截至时间 |
| WBS-05-19-23 · `SITUATION-IM-R3-L01` | M4 角标挂载 | 李伟 | `lumen-ui-science-pc` | 待建 | 未开工 | D3 + R0 | 无截至时间 |

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

> WBS-05-28 内的 `FE-DISPLAY-ACHIEVE-ALIGN-L01` / `SVC-ECO-ALIGN-L01` / `TECHINDEX-NEW-L01` / `TECHINDEX-MOCK-ALGO-L01` / `SVC-THINKTANK-RECTIFY-L01` 同时在 §1 的对应菜单行出现（成果、生态服务、指数、智库）。那是**菜单视角**的重叠引用，编号归属仍在 05-28，不重复计数。

---

## 6. 完成情况汇总

### 6.1 按状态计数（2026-10-31 快照，读 `task-registry.yaml`）

| 状态 | 条数 | 涉及 WBS 行 / 任务 |
|---|---|---|
| done | **8** | 05-16 `ARCH-DISPLAY-REDESIGN-L01`；05-25 `FE-TS-S01`；05-26 批 A `FE-DISPLAY-SMALL-BATCH-A`；05-08-02～05-08-06（5 条，2026-10-31 完成） |
| ready_to_sign | **4** | 05-12 `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01`；05-08 父 `SYSINT-05-08-L01`（2026-10-31 推进）；05-08-01 `SYSINT-05-08-01-L01`；05-08 挂接 `SVC-PANORAMA-GAP-L01` |
| integration | **22** | 05-15 `BE-TS-CONTRACT-02`；05-18 `FE-TS-01A`；05-01a `FE-TS-02A`；05-02a `FE-TS-03A`；05-19 `FE-TS-04A/05A/06A`；05-21 `FE-TS-08A`；05-22 `FE-TS-09A`；05-24 `FE-TS-10A`；05-27 `LUMEN-DISPLAY-PORTAL-IFRAME-L01`；05-28 `TECHINDEX-NEW-L01` + `PROTO-TUNE-L01`；05-29 `DS-01`～`DS-09-METRIC-OPEN-L01`（9 条） |
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

