# WBS · 展示系统集成

> **2026-10-27 扩范围（本次变更）**：技术方案的范围口径改为「**展示系统全部目录菜单**」。本表随之从「九个对接菜单」扩为 **七模块 30 叶（DS-01～DS-30）+ 政策核增 PC-1～PC-4 + 维护管理（M10）**全覆盖，并把**展示系统相关的全部已提交任务**（含之前提交的技术架构设计类任务）归集进来逐叶可索引。每叶补「完成情况 · handoff」列，把对应 handoff 写回本表。
> **2026-10-22 梳理**。方案任务 `SYSINT-SCHEME-05-L01` 于 2026-10-23 由 `human:淮政玮` 签收后，同日改回处理中。菜单范围与调用方向以 [技术方案](./技术方案.md) 现稿为准。同日按已写明的人员姓名补建开发任务，任务号回写本表。WBS-05-09 监管人仍是待指定，未建任务。
> **2026-10-22 晚**：草稿已确认作建叶底稿。已有监管人即负责人。完成日期要求取倒排「功能开发」计划完成时间（11月倒排计划 · 科技信息展示系统）。页面计划里冲出该日的叶结束日不写入。开始时间仍待填写。这两列是我方栏位，不是对端承诺。方案行与菜单注册行在倒排里没有单独的功能开发完成日，仍为无截至时间。
> **2026-10-26 `human:淮政玮` 口径**：「展示系统本身就是集成，整体放到展示系统集成」。据此，展示系统的跨页公共物与技术架构设计件也归第 5 项，不再散落在原页面计划。
> **2026-10-27 `human:李伟` 建叶登记**：原以「挂接登记」记入的五件转为正式叶，任务号不变（沿用已有 ID，未新建）；原无监管人的 `BE-TS-IMPL-01`、`BE-TS-DATA-01` 由 `human:李伟` 认领。派单说明见 `agent-handoffs/科技发展态势-TS/派单说明/`。
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
| 科技发展态势 | DS-01 | 科技全域态势 | WBS-05-18 | `FE-TS-01A`(integration)、`BE-TS-IMPL-01`(backlog)、`BE-TS-DATA-01`(backlog)、`DS-01-METRIC-OPEN-L01`(integration) | 前端整页复刻已 push、三绿；REST 待 `BE-TS-CONTRACT-01` 冻结。指标语义卡仍草稿未签 | LT-5-SIT-DS01 |
| 科技发展态势 | DS-02 | 科学技术全景 | WBS-05-01a / 01b | `SYSINT-05-01A-L01`(ready)、`SYSINT-05-01B-L01`(ready)、`FE-TS-02A`(integration)、`DS-02-METRIC-OPEN-L01`(integration) | 对接叶已建号未开工；复刻页 integration；读图归第 7 项 | LT-5-SIT-DS02 |
| 科技发展态势 | DS-03 | 技术发展跟踪 | WBS-05-02a / 02b | `SYSINT-05-02A-L01`(ready)、`SYSINT-05-02B-L01`(ready)、`FE-TS-03A`(integration)、`DS-03-METRIC-OPEN-L01`(integration) | 三个 Tab 可开或空态；材料未到时空态。名称收口为「技术发展跟踪」 | LT-5-SIT-DS03 |
| 科技发展态势 | DS-04 | 全球创新监测 | WBS-05-19 | `FE-TS-04A`(integration)、`DS-04-METRIC-OPEN-L01`(integration)；已有 `E-INNOV-M1-L08`（tier FULL，路由 `/innov`） | 综合 / 实时 / 载体 / 监测 / 能力五块可切换；不另起一套 innov 地图 | LT-5-SIT-DS04 |
| 科技发展态势 | DS-05 | 湾区创新监测 | WBS-05-19 | `FE-TS-05A`(integration)、`DS-05-METRIC-OPEN-L01`(integration) | 成果地图 / 四维 / SWOT / 指标四块已完成，联调待 REST | LT-5-SIT-DS05 |
| 科技发展态势 | DS-06 | 深圳创新监测 | WBS-05-19 | `FE-TS-06A`(integration)、`DS-06-METRIC-OPEN-L01`(integration) | note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」；**模块目录无同名 `FE-TS-06A.md`** | LT-5-SIT-DS06 |
| 科技发展态势 | DS-07 | 科技创新评估 | WBS-05-20 | `FE-TS-07A`(claimed，P2)、`DS-07-METRIC-OPEN-L01`(integration) | 复刻未开工；评估对象范围未补则按详设空态 | LT-5-SIT-DS07 |
| 科技发展态势 | DS-08 | 科技指数 | WBS-05-21 | `FE-TS-08A`(integration)、`FE-DISPLAY-TECHINDEX-NEW-L01`(integration)、`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01`(pending_test)、`DS-08-METRIC-OPEN-L01`(integration) | 九域 + 8 件套 + 算法口径页已出，布局溢出由 fix 8a46d7d 修；mock 权重（40/30/20/10）一致性已修待抽测。**只做展示侧，不做智库后台** | LT-5-SIT-DS08 |
| 科技发展态势 | DS-09 | 科技发展规划 | WBS-05-22 | `FE-TS-09A`(integration)、`DS-09-METRIC-OPEN-L01`(integration) | 综合规划 / 重点领域 / 研究分析可切换；预警模型可 501，不编制规划正文 | LT-5-SIT-DS09 |
| 科技发展态势 | — | 维护管理（M10 · `/trend/maintain/*`，不另开一级菜单） | WBS-05-24 | `FE-TS-10A`(integration) | 图层与数据源、技术图谱关键实体与关系维护；无权限是降级不是白屏。**报价表划掉且工作量为 0 的「维护技术图谱」不实现** | LT-5-SIT-OPS |
| 科技政策跟踪 | DS-10 | 科创政策全景 | WBS-05-23 | `DISPLAY-POLICY-GAP-AC-L01`(in_progress)、`FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01`(in_progress) | GAP 档 A 37 条 + 档 C 校验闸门已在 demo 仓落地**未 commit**，待 `human:淮政玮` 本地 `pnpm dev` 验；原型优化仍 in_progress | LT-5-POL-DS10 |
| 科技政策跟踪 | DS-11 | 政策分析评价 | WBS-05-23 | 同上 | 三类报告可视化 | LT-5-POL-DS11 |
| 科技政策跟踪 | DS-12 | 政策效果推演 | WBS-05-23 | 同上 | 效果预估与推演页可切换；与专题 `.8.6` 分键（推演 ≠ 布局推荐） | LT-5-POL-DS12 |
| 科技政策跟踪 | PC-1～PC-4 | 政策数据治理 / 智能政策拆解 / 多维政策对比 / 智能研报生成 | WBS-05-23 | 同上 | 核增四叶，计入政策跟踪不另开一级菜单；演示级边界写在页上。**PC-4 的 Job 未注册则导出入口按 501 / 空态** | LT-5-POL-PC1～PC4 |
| 科技人才态势 | DS-13～DS-16 | 全球领域人才态势 / 关注地区人才态势 / 重点科技人才画像 / 人才引进推荐评估 | WBS-05-03a / 03b | `SYSINT-05-03A-L01`(ready)、`SYSINT-05-03B-L01`(ready) | **只做菜单壳与非三要素区块**；四子页不重做，供数是 WBS-02-01（第 2 项）；资讯、职位变动、奖项荣誉、引进成本、尽调五类空态 | LT-5-TAL-DS13～DS16 |
| 科技数据资源 | DS-17～DS-20 | 总体 / 接入 / 主题 / 应用四视窗 | WBS-05-04 | `SYSINT-05-04-L01`(claimed，监管 淮政玮 → 实际认领 孔东) | 四个视窗可切换；共建数据未到为空态。R6：data 组供方未找到（原华为云 2026-10-15 退出） | LT-5-RES-DS17～DS20 |
| 科技知识图谱 | DS-21～DS-24 | 分析展示 / 指标展示 / 算法展示 / 服务展示 | **跨项索引（第 7 项）** | `FE-DISPLAY-KG-SERVICE-ALIGN-L01`(review) | 本表**不建叶**。第 7 项负责页面与查图；`FE-DISPLAY-KG-SERVICE-ALIGN-L01` 是 demo 侧 DS-24 服务展示合规对齐，原地更新 `ServiceDisplay.jsx` | LT-5-KG-DS21～DS24 |
| 科技成果展示 | DS-25～DS-29 | 软科学成果展示 / 科技创新生态展示 / 科技时空演进展示 / 大型科学仪器共享 / 创新载体孵化载体 | WBS-05-05 | `SYSINT-05-05-L01`(claimed)、`FE-DISPLAY-ACHIEVE-ALIGN-L01`(pending_test) | 五页可打开或空态；仪器只展示、不做预约闭环；时空演进**禁止用专题 B 面时间轴冒充**；口径未绿用角标不改数 | LT-5-ACH-DS25～DS29 |
| 科技服务全景 | DS-30 之① | 科技创新生态服务（全景里唯一智树自研子菜单） | WBS-05-06 | `SYSINT-05-06-L01`(claimed)、`FE-DISPLAY-SVC-ECO-ALIGN-L01`(review) | 列表与详情可开或空态；demo 侧原地更新 `InnovationEcosystem.jsx` | LT-5-SVC-ECO |
| 科技服务全景 | DS-30 之② | 智库服务 | WBS-05-07 | `SYSINT-05-07-L01`(ready)、`FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01`(in_progress) | 2026-10-23 起**不按跳转**，要求智谱提供接口；接口未到为空态。智树不做高端智库后台。demo 页按需规 566–574 整改中 | LT-5-SVC-HUB |
| 科技服务全景 | DS-30 之③④⑤ | 科技交流 / 科技竞赛 / 科技传播 | WBS-05-08（子 05-08-01～06） | `SYSINT-05-08-L01`(claimed)、`SYSINT-05-08-01-L01`(ready_to_sign)、`-02`～`-06`(backlog)、`SVC-PANORAMA-API-L01`(claimed)、`SVC-PANORAMA-GAP-L01`(ready_to_sign) | 详见 §4.2 | LT-5-SVC-HUB |
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
| WBS-05-08 · `SYSINT-05-08-L01` | 科技交流、科技竞赛、科技传播（父） | 李伟 | `lumen-ui-science-pc` | **claimed** | 挂接自建任务 `SVC-PANORAMA-API-L01`（父统筹单，claimed）、`SVC-PANORAMA-GAP-L01`（对照表成品，ready_to_sign）。子任务见 §4.2 | `SYSINT-SCHEME-05-L01`。对端名称「北大深势」只出现在规约，能力评估文未署此名，**名称核对还没有** | 2026-11-09 |
| **WBS-05-09** | 本项菜单注册与用户权限（全景、技术发展、人才态势、数据资源、成果展示、生态服务、智库、交流、竞赛、传播） | **待指定**（2026-10-22 纪要未点名） | 统一用户中心配置；业务仓不写主机名 | **未建任务** | — | `SYSINT-SCHEME-05-L01`。各菜单叶负责自己的相对路径；这些菜单以相对路径可见，对应用户登录后能进；地址不写主机名；交流 / 竞赛 / 传播跳转失败仍有提示；智库不按跳转走智谱接口 | 无截至时间 |
| WBS-05-18 | 科技全域态势（DS-01，含 M1 聚合 BFF 消费） | 孔东（FE）/ 李伟（BE） | `lumen-ui-science-pc`、`gkxlumen-display` | **integration** | `FE-TS-01A` handoff `科技发展态势-TS/FE-TS-01A.md`：整页复刻 integration；所依赖的底座 `FE-TS-S01` 已 done。后端 `BE-TS-IMPL-01` 未开工。指标卡 `DS-01-METRIC-OPEN-L01`：赋号草稿、类型未签、公式待 `human:唐绍祖` 共签 | `FE-TS-S01`、`BE-TS-CONTRACT-01` 冻结（M1）。11 要素图层 / 科创事件双 Tab；久新人才、科研机构、论文、专利未到则**空态** | 计划 LT-5-SIT-DS01：10-16 → 10-20 |
| WBS-05-19 | 创新监测三页（DS-04 全球 / DS-05 湾区 / DS-06 深圳） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-04A` / `05A` / `06A` 三份 handoff 均已 push（`06A` note「handoff 已 push ea1e4aad；lumen b4e1eda；联调确认」，但模块目录**无同名 `FE-TS-06A.md`**）。已有 innov 事件地图只对齐，不另起一套 | `BE-TS-CONTRACT-01`（M4 / M5 / M6 契约未冻结）。订阅 / 推送的对端宋泉未确认则该块空态 | 计划 10-28 → 10-31（DS-06 及以后冲出 V1 开发出门） |
| WBS-05-20 | 科技创新评估（DS-07） | 孔东 | `lumen-ui-science-pc` | **claimed**（P2） | `FE-TS-07A` 仅 claimed，复刻未开工 | 评估对象范围未补则按详设空态 | 计划 11-03 → 11-04（结束日 = V1 测试末日） |
| WBS-05-21 | 科技指数（DS-08） | 孔东 / 淮政玮 | `lumen-ui-science-pc`（正式）、`demo-ui-science`（原型侧） | **integration** | `FE-TS-08A` handoff `科技发展态势-TS/FE-TS-08A.md`（三级指标树 / 34 省地图 / 专家 H 指数 / 四维趋势 / 排行榜 / 20 人评议只读）；`FE-DISPLAY-TECHINDEX-NEW-L01` 九域 + 王惠 8 件套 + 唐绍祖算法口径，布局溢出由 fix 8a46d7d 修；`FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01` mock 权重 40/30/20/10 派生一致已修，pending_test | **只做展示侧，不做智库后台**。专家评议 20 人只读 | 计划 11-04 → 11-05（晚于 V1 测试） |
| WBS-05-22 | 科技发展规划（DS-09） | 孔东 | `lumen-ui-science-pc` | **integration** | `FE-TS-09A` handoff `科技发展态势-TS/FE-TS-09A.md`：综合规划 / 重点领域 / 研究分析可切换 | 预警模型可 501；**不编制规划正文** | 计划 11-05 → 11-06 |
| WBS-05-23 | 科技政策跟踪（DS-10～DS-12 + 核增 PC-1～PC-4） | 淮政玮 / 郭万迎 | `demo-ui-science`（原型侧）；正式仓落地未排 | **in_progress** | `DISPLAY-POLICY-GAP-AC-L01` handoff `agent-handoffs/展示系统-政策跟踪/DISPLAY-POLICY-GAP-AC-L01.md`：6 簇代码已落地**未 commit**，待 `human:淮政玮` 本地 `pnpm dev` 验 demo，本单禁 git commit。`FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01` 仍 in_progress（**无同名 handoff 文件**） | PC-4 的 Job 未注册则导出入口按 501 / 空态。冻范围依据为详设 §5 与 `USM-DS10-12-科技政策跟踪.md` | 计划 10-20 → 10-28（DS-10～12 窗内，PC 属 V2） |
| WBS-05-24 | 维护管理（M10 · `/trend/maintain/*`） | 孔东 | `lumen-ui-science-pc` | **integration**（P2） | `FE-TS-10A` handoff `科技发展态势-TS/FE-TS-10A.md`：图层与数据源配置 / 维护技术图谱 / 关键实体与关系维护 / 已有能力入口；无权限是降级不是白屏 | 挂 DS-01 / DS-02，**不另开一级菜单**。**报价表划掉且工作量为 0 的「维护技术图谱」不实现** | 计划 11-06 → 11-07 |

> **页数口径未统一（待定项）**：`formal-docs-registry.yaml` 记 **34 页**（M1 态势 9 页），`ARCH-DISPLAY-01.md` §6.3 记 **35 页**（trend 10 页）。差异应在于 `/trend/maintain/*`（本表 WBS-05-24）是否计入展示页。**会签前需定口径**；定之前本表两说并列，不自选一个。

### 4.2 WBS-05-08 的子任务（科技交流 / 竞赛 / 传播）

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-08-01 · `SYSINT-05-08-01-L01` | 科技服务全景对接分析（交流 / 竞赛 / 传播） | 李伟 | `lumen-ui-science-pc` | **ready_to_sign** | **已完成**（2026-10-23 晚落盘 271 行纪要 + 深势 MD 接口审计）。evidence：本夹 `纪要/2026-10-23-科技服务全景-深势对接-交流竞赛传播模块优化.md`、`对接文档/对端/2026-10-23-深势-科技服务全景对外开放接口.md`。12 项会议结论全覆盖；字典枚举决策已固化（不走接口）；原型字段映射决策完成（竞赛类型下拉移除、竞赛级别保留并做值映射）；OpenAPI 合规性审计经李伟审阅 | 父 `SYSINT-05-08-L01`。待监管人签收 | 计划 2026-10-23（实际当日完成） |
| WBS-05-08-02 · `SYSINT-05-08-02-L01` | 科技服务全景入口跳转壳开发 | 未标注 | `lumen-ui-science-pc` | **backlog** | 未开工 | `SYSINT-05-08-L01`、`-08-01` 签收通过。三个门户入口菜单注册；跳转深势 `detailUrl` 或 iframe；**不展示深势不支持的字段（奖金、竞赛类型下拉、点赞排序等）**；空 / 加载 / 错误三态齐全 | 计划 2026-10-28 |
| WBS-05-08-03 · `SYSINT-05-08-03-L01` | 科技交流页面对接（BFF + FE，深势 3 接口代理） | 未标注 | `lumen-svc-platform` | **backlog** | 未开工 | `-08-01` 签收 | 待定 |
| WBS-05-08-04 · `SYSINT-05-08-04-L01` | 科技竞赛页面对接（BFF + FE，深势 4 接口代理） | 未标注 | `lumen-svc-platform` | **backlog** | 未开工 | `-08-01` 签收 | 待定 |
| WBS-05-08-05 · `SYSINT-05-08-05-L01` | 科技传播页面对接（BFF + FE，深势 3 接口代理） | 未标注 | `lumen-svc-platform` | **backlog** | 未开工 | `-08-01` 签收 | 待定 |
| WBS-05-08-06 · `SYSINT-05-08-06-L01` | 科技服务全景三板块联调验收 | 未标注 | `lumen-ui-science-pc` | **backlog** | 未开工 | `-08-02`～`-08-05` 完成 | 待定 |

> **2026-10-26 `human:李伟` 挂接**：`SVC-PANORAMA-API-L01`、`SVC-PANORAMA-GAP-L01` 两件自建任务挂在 WBS-05-08 下，不新开叶。产物 `工程过程/02-策划与监控/01-总集大项目整体计划/09-科技服务全景接口需求评估/科技服务全景-页面维度供数缺口自研对照表.md`（161 行，§五 10 项待会签）。今日快照已出，百分比不回改，明日快照按注册表现状态计入。

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

### 6.1 按状态计数（2026-10-27 快照，读 `task-registry.yaml`）

| 状态 | 条数 | 涉及 WBS 行 / 任务 |
|---|---|---|
| done | **3** | 05-16 `ARCH-DISPLAY-REDESIGN-L01`；05-25 `FE-TS-S01`；05-26 批 A `FE-DISPLAY-SMALL-BATCH-A` |
| ready_to_sign | **3** | 05-12 `DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01`；05-08-01 `SYSINT-05-08-01-L01`；05-08 挂接 `SVC-PANORAMA-GAP-L01` |
| integration | **22** | 05-15 `BE-TS-CONTRACT-02`；05-18 `FE-TS-01A`；05-01a `FE-TS-02A`；05-02a `FE-TS-03A`；05-19 `FE-TS-04A/05A/06A`；05-21 `FE-TS-08A`；05-22 `FE-TS-09A`；05-24 `FE-TS-10A`；05-27 `LUMEN-DISPLAY-PORTAL-IFRAME-L01`；05-28 `TECHINDEX-NEW-L01` + `PROTO-TUNE-L01`；05-29 `DS-01`～`DS-09-METRIC-OPEN-L01`（9 条） |
| pending_test | **3** | 05-28 内 `ACHIEVE-ALIGN-L01`、`TECHINDEX-MOCK-ALGO-L01`、`GI-TOPBAR-OVERLAY-L01` |
| review | **4** | 05-17 / 05-17b `ARCH-TS-L3-DESIGN-01`、`ARCH-TS-L3-01`（待 `human:徐滕强` 裁决 A1–A6）；05-28 内 `SVC-ECO-ALIGN-L01`、`KG-SERVICE-ALIGN-L01` |
| claimed | **9** | 05-10 `BE-TS-CONTRACT-01`；05-11 `BE-TS-AGG-01`；05-20 `FE-TS-07A`；05-29 内 `SCI-DISPLAY-METRIC-L123-INV`；05-04、05-05、05-06、05-08 `SYSINT-05-0X-L01`；05-08 挂接 `SVC-PANORAMA-API-L01` |
| in_progress | **5** | 05-00 `SYSINT-SCHEME-05-L01`；05-23 内 `DISPLAY-POLICY-GAP-AC-L01`、`POLICY-TRACK-OPT-L01`；05-28 内 `SVC-THINKTANK-RECTIFY-L01`、`TOTALCHECK-L01` |
| backlog | **8** | 05-13 `BE-TS-IMPL-01`；05-14 `BE-TS-DATA-01`；05-08-02～05-08-06（5 条）；05-26 批 B `FE-DISPLAY-SMALL-BATCH-B` |
| ready | **7** | 05-01a / 01b / 02a / 02b / 03a / 03b、05-07（全部 `SYSINT-05-0X-L01`） |
| **合计** | **64** | 另有 05-09（未建任务）不计入。2026-10-27 新增 ARCH-TS-L3 两件 |

### 6.2 当前卡点

| # | 卡点 | 影响的行 | 谁能解 |
|---|---|---|---|
| C1 | `BE-TS-CONTRACT-01` **M0 未评审通过 / 契约未冻结**（已过原定 2026-10-15） | 05-10 自身，以及下游全部 `FE-TS-*` 复刻页（05-18 / 05-19 / 05-21 / 05-22 / 05-24）的 REST 联调闸门 | M0 三方：孔东 / 徐滕强 / 唐绍祖 |
| C2 | 05-10、05-11 的完成日期要求**已过期、待重定** | 05-10、05-11 | 监管人 `human:李伟` |
| C3 | DS-01～09 九张指标语义卡**赋号草稿、公式未签**（2026-08-22 起卡 integration） | 05-29 | `human:唐绍祖` 公式共签 |
| C4 | 页数口径 34 vs 35 未定 | 05-24 是否计入，以及全部菜单计数 | 会签前由 `human:淮政玮` 定 |
| C5 | WBS-05-09 无监管人、未建任务 | 全部菜单的可见性 | 待指定 |
| C6 | 数据资源（05-04）**供方仍未找到**；久新 42 个 API 未确认 | 05-04、05-11 的久新侧源 | `human:郭万迎` 对外催办（久新侧 李乐 / 任欢） |
| C7 | 05-08-02～05-08-06 无监管人、全部 backlog | 交流 / 竞赛 / 传播三入口 | 待指定 |
| C8 | ~~`ARCH-TS-L3-DESIGN-01` / `ARCH-TS-L3-01` 有成品无 registry 条目~~ **2026-10-27 已解决**：两条已补登记入 `task-registry.yaml`（status `review`，`supervised_by` = `human:徐滕强`），WBS-05-17 / 05-17b 已可被任务系统索引 | 05-17 / 05-17b | 已关闭 |
| C9 | **`ARCH-TS-L3-01` §7 六项待裁决 A1–A6 未签署**，L3 归属（`gkxlumen-element` vs 复用 `topic-*`）未定；`BE-TS-IMPL-01` 因此开工无依据 | 05-17 / 05-17b / 05-13 | `human:徐滕强` 逐项签署 |
| C10 | **A5 久新主体键是否对齐**未答复（`ARCH-TS-L3-01` 标为最大技术风险），`channel/jiuxin-*` 只能出桩实现 | 05-17b、05-18 的久新要素 | `human:郭万迎` 向久新催办（侧 李乐 / 任欢） |

### 6.3 变更记录

| 日期 | 变更 |
|---|---|
| 2026-10-22 | 草案梳理；按已写明姓名补建开发任务并回写任务号 |
| 2026-10-23 | 方案签收后改回处理中；05-04 / 05-06 监管人变更登记 |
| 2026-10-26 | `SVC-PANORAMA-*` 挂接 05-08；`human:淮政玮` 定「展示系统整体归第 5 项」 |
| 2026-10-27 | **扩为全菜单 + 全任务归集**：新增 05-15～05-29 共 15 行（技术架构设计组 05-15～05-17、缺失菜单 05-18～05-24、跨页公共物 05-25～05-29）；每行补「完成情况 · handoff」列；`BE-TS-IMPL-01` / `BE-TS-DATA-01` 由 `human:李伟` 认领 |
| 2026-10-27 | **补登记 `ARCH-TS-L3-DESIGN-01` / `ARCH-TS-L3-01`** 入 `task-registry.yaml`（status `review`，监管 `human:徐滕强`，`E-FE-TECH-SITUATION`）；WBS-05-17 拆为 05-17 / 05-17b 两行（同一设计的两个载体）；任务总数 62 → 64；卡点 C8 关闭，新增 C9（A1–A6 未签署）、C10（A5 久新主体键未答复） |

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

