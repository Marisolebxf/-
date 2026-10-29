# 科技信息展示系统 · 技术架构设计说明书

| 项 | 内容 |
|---|---|
| **文档 ID** | `ARCH-DISPLAY-01` |
| **版本** | **v0.9**（架构已裁决：15 项**全部裁定**，其中 A9 / A11 待回填） |
| **状态** | `reviewed` —— 2026-10-26 徐腾强裁决答复，**待签收** |
| **范围** | 科技信息展示系统 **L0–L5 全栈**：前端 → 网关 → 展示聚合 BFF → 领域服务 → 算法/门面 → 数据面，含横切机制与部署 |
| **规模** | 7 组 35 页（PC 端 `lumen-ui-science-pc`） |
| **起草** | `agent:architect-agent` |
| **裁决人** | `human:徐腾强 @qike366.com`（架构师，D15 落地人） |
| **知会** | `李伟`（契约监管）· `孔东`（前端）· `堂绍祖`（算法/门面）· 数据 Lead · `郭万迎`（PM） |
| **仓** | `gkx-orchestration`（架构真源，不落业务代码） |

**文档关系**

| 文档 | 定位 | 与本文关系 |
|---|---|---|
| `architecture-baseline.md` | 全项目架构基线 D1–D15 | **上位铁律**，本文全部遵守 |
| `_archive/architecture-display-optimized.md` | 展示系统「优化方案」提案（2026-10-20） | ⛔ **已归档**：结论全部并入本文，仅保留决策追溯，不再维护 |
| `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-DESIGN-01.md` | TS 模块 L3 **详细设计**（16 节） | 本文 §7.3 的下钻文档 |
| `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-01.md` | L3 决策摘要单 | 一页签字用 |

**修订记录**

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-10-25 | 初稿：L0–L5 全栈骨架 |
| v0.2 | 2026-10-25 | 补全各层实现细节：§6 完整端点清单与聚合/降级/缓存实现、§4 前端工程结构与契约生成、§9 数据模型、§12 部署配置；精简与 L3 文档重复内容 |
| v0.3 | 2026-10-25 | ① 合并 `architecture-display-optimized.md` 独有内容（F1–F10 → §2.4、D1–D15 兼容性对照 → §1.6、备选方案对比 → §3.5、Q-DISP-01~09 → A 系列编号）；② **要素域服务改名 `gkxlumen-situation` → `gkxlumen-element`**（A2 已确认），三份文档同步 |
| v0.4 | 2026-10-25 | 补入 2026-10-20 徐腾强 × 李拜六口头共识：**§1.7 决策溯源**（C1–C6）、**§7.7 与共识 C1 的偏差说明**（⚠️ 需 A1 重裁）、**§9.5 秒开预跑读模型**、**§10.8 页面秒开策略**、**§10.9 订阅模块**；新增裁决项 **A14**（预跑组合规模）、**A15**（订阅模块归属） |
| v0.5 | 2026-10-25 | ✅ **A1 裁决落地**：徐腾强确认「**展示侧不复用专题侧**」→ 新建 3 个 L3 服务。§7.6 升级为**复用边界清单**（必须复用 / 可复用 / 不复用 / 自建四类），§7.7 与 A1 标记为已裁决 |
| v0.6 | 2026-10-25 | ✅ **异步复用边界裁定**：徐腾强确认「**异步任务复用专题**」→ `gkxlumen-topic-async-service` 移入「已确认复用」，§10.5 标注已裁决，**展示侧不自造任务体系**；§7.6 与 A15 同步（订阅模块 (a) 方案随之收敛） |
| v0.7 | 2026-10-25 | ✅ 三项裁决落地：**A12** 采纳 §6.7 缓存 TTL 分档（可调参数）· **A14** 定 **(b) 分级预跑**策略（具体枚举量级待产品定义，开发时落地）· **A15** 订阅模块定 **(a)** 复用异步执行能力。待拍由 13 → 10 项 |
| v0.8 | 2026-10-25 | ✅ 两项裁决落地：**A6** 门面实装前**先直读 ADS**（实装后按场景分流：纯查询直读 / 需算法走门面），§8.2 同步；**A13** 契约生成选 **`openapi-typescript`**（只生成类型、不接管请求层）。待拍由 10 → 8 项 |
| **v0.9** | **2026-10-26** | ✅ **徐腾强裁决答复落地，A1–A15 全部裁定**。**A4** = (a) `/display/v1/**` 一步到位（网关转发优先） · **A10** 通过（按聚合 BFF 实装：页面聚合/读缓存/分区降级/就绪度注入） · **A3** 准予过渡期直连久新（**新增可选路径：下沉 `gkx_show_service`**，须登记切换条件与隔离措施） · **A7** 落人——**郭万迎催办，久新侧 李乐 / 任欢** · **A8** 用现网 space **`entan`**（燕大本期不切源、不并行，**R4 关闭**）。⚠️ **A5 反向裁决（≠提交方建议）**：**暂不强制切正式 ADS**，新建服务先与现网一致（读 `demo_gkxlumenx_ads` + 库名配置化），待正式库有数、专题侧切库时统一整改 → **R1 由「阻塞」降为「已知延后」**。新增 **§10.9.1** 答复 A9（`app_user` = **平台自有** App 端库，非三方），并澄清 **A11** 口径（预跑读模型 = **ADS 物化表 T+1**，**不是** Redis 页面缓存；后者属 §6.7 分档） |

---

## 1. 概述

### 1.1 背景

科技信息展示系统面向领导驾驶舱、业务分析师、产业与技术研究、政策与资源配置、创新主体运营、数据治理六类角色，提供 7 组 35 页的科技态势展示。

前端 35 页已完成（mock 态），但后端**尚未形成完整技术栈**：L2 `gkxlumen-display` 仅骨架、L3 无承载服务、网关缺 `/display/**` 路由、展示侧 Python 门面仍为空壳。本文给出 L0–L5 全栈架构设计。

### 1.2 范围

**覆盖**：L0 前端 · L1 网关 · L2 展示聚合 BFF · L3 领域服务 · L4 算法与门面 · L5 数据面 · 横切机制（缓存/降级/可观测/权限/异步/契约）· 部署 · 演进路线。

**不覆盖**：专题服务系统（`lumen-ui-topic` 及其域服务，仅在共享边界处标注）；算法内部实现；ETL 内部实现；L3 领域服务内部实现细节（见下钻文档）。

### 1.3 目标与非目标

| 目标 | 说明 |
|---|---|
| **G1 单入口** | 前端只认 `/display/v1/**` 一个后端面 |
| **G2 分层不越界** | display 不碰 DB/Python；领域服务不写算法 |
| **G3 供方无关** | 三方供方形态变化不动业务代码 |
| **G4 诚实降级** | 分区降级 + `empty_reason`；禁造数、禁造 0 |
| **G5 全栈可观测** | 单一 trace 贯穿前端 → 网关 → BFF → 领域 → Python |

| 非目标 | 说明 |
|---|---|
| 通用查询引擎 | 不做 DSL / 联邦 SQL / 规则引擎 |
| 计算下沉 Java | 算法归 Python（D2） |
| 改造专题侧服务 | 展示另起炉灶，不绑专题发布节奏 |

### 1.4 术语

| 术语 | 含义 |
|---|---|
| **组（group）** | 前端一级导航，7 个：`trend`/`policy`/`talent`/`data`/`graph`/`results`/`service` |
| **区块（block）** | 页面内需独立 loading/空态/错误态的区域，**接口粒度的最小单位** |
| **维度 / 要素** | 业务分类：企业/产业链/服务机构/政策/科研机构/人才/技术/综合服务 |
| **供方** | 智树自建 / 久新 / 燕大 / 智谱 / 深势 |
| **通道（Channel）** | 数据获取途径：`local-ads`/`jiuxin-http`/`jiuxin-jdbc`/`yanda` 等 |
| **片段（Fragment）** | 一次查询的最小数据来源单元，带 `emptyReason` |
| **分区降级** | 聚合接口中某下游失败时仅该分区置空并给原因，不影响其他分区 |

### 1.5 关键约束（基线条款）

| 条款 | 约束 | 本文落点 |
|---|---|---|
| **D2** | 算法归 Python | §8 |
| **D3** | Java 仅读 `*_ads` + `app_user` 读写；禁扫 ODS/DWD；禁写 ADS | §9.4 |
| **D4** | 收藏/标签带写面落服务端 | §10.5 |
| **D5** | 路由划分 `/display/**`、`/topic/**`、`/innov/**`、`/metrics/**` | §5.2 |
| **D7** | 三方源经数据工厂 `ODS→DWD→ADS`，不传导到契约面 | §7.3.3 |
| **D9** | 指标注册于 `/metrics/v1/catalog`，前端禁自填就绪度 | §6.8 |
| **D12** | `demo-*` 不得进入 lumen 调用链 | ⚠️ §14 R1 |
| **D15** | 展示单入口 `/display/v1/**`；展示 BFF 不直连 Python/DB；Python 门面三重隔离 | §3.2 / §8.4 |

### 1.6 与 `architecture-baseline` 的兼容性对照

> 本表为评审用「本文是否违反基线」的逐条证明。

| 决策 | 本文影响 | 说明 |
|---|---|---|
| D1 共享聚合核心 | ⚠️ **偏离** | 基线要求展示优先复用 `/topic/v1`；本文因数据形态差异（要素 count/落点/热力 vs 检索/画像/对比篮）与 D15 三重隔离，**新建要素域服务**而非复用 `topic-*`（A1） |
| D2 算法统一出口 | ✅ 不变 | 算法经 `/internal/*` 与注册中心调用，Java 不写算法 |
| D3 契约面 = ADS | ✅ 强化 | 读模型落 ADS 内；领域服务只读 |
| D4 前端职责切分 | ✅ 收敛 | 前端不再拼装多接口；收藏/标签/导出带写面落服务端 |
| D5 网关路由划分 | ✅ 沿用 | `/display/**` 为展示唯一对外前缀 |
| D7 契约先行 + Mock 先行 | ✅ 沿用 | 三方源未定期间按 D7 出桩 + Mock，不造假数 |
| D9 指标 8 件套血缘 | ✅ 补注入层 | display 统一注入四维角标 |
| D12 仓隔离 | ⚠️ **现网违反** | `demo_gkxlumenx_ads` 现网普遍使用（R1），需单开整改 |
| D13 Kafka | ✅ 沿用 | 异步事件走 Kafka / async-service |
| D15 展示门面三重隔离 | ✅ 强化 | 新建要素域服务为展示侧，**不经**专题侧门面（:8080/:8081） |
| 服务边界 | ⚠️ **需会签** | 新增 3 个 L3 服务属服务边界新增（A1） |
| 「薄 BFF」表述 | ⚠️ **需会签** | 由「薄」升为「聚合 BFF」，属角色强化而非边界变更（A10） |

### 1.7 决策溯源（2026-10-20 架构口头共识）

> 来源：徐腾强 × 李拜六 群聊，2026-10-20 11:22–11:29。本节为**已确认的口头共识**；本文与之**一致的部分直接落地**，**冲突部分单列裁决**（见 §7.7 / A1）。

| # | 共识 | 原文要点 | 本文落地 |
|---|---|---|---|
| **C1** | **Java 侧只增加一个聚合服务** | 「java 这吧只增加一个聚合服务，其他的都复用专题那边的链路？」→「理论上是这样的」 | ✅ 对外面上成立：`gkxlumen-display` 是**唯一新增对外 Java 服务**，L3 全部 `@Inner` 不对外。⚠️ **但「复用专题链路」与调研不符，见 §7.7 / A1** |
| **C2** | **聚合服务只做调用和聚合，查询由各专题提供** | 「这个服务只做调用和聚合数据，其余所有查询操作都由各专题提供，因为不止咱们自己还有其他公司的」 | ✅ §6.2 display 职责边界（不写算法、不直连 DB、不造数） |
| **C3** | **异步复用专题，不自建** | 「异步任务复用专题」「如果是独立的，那就完全没问题」 | ✅ §10.5 复用 `gkxlumen-topic-async-service`；**订阅模块见 §10.9 / A15** |
| **C4** | **展示侧新增 Python 模块自供数** | 「可能在聚合服务下面再增加一个 python 模块，用来给我们自己供数部分提供功能支持」 | ✅ `gkx_show_service` :8082（D15 已有）；⚠️ **当前是骨架，见 R3 / A6** |
| **C5** | **故障隔离：一个挂了不影响另一个** | 「其中一个挂了不会影响另一个，异步任务本身不影响前端界面」 | ✅ §6.6 分区降级 + §10.2；异步失败**不阻断页面** |
| **C6** | **后期可彻底隔离** | 「后期拆分 单独服务再创建一个就算彻底隔离」 | ✅ §13 拆分触发条件表 |

**与专题系统的边界公式**（徐腾强 11:28 原话归纳）：

```
同步链路   = Java 聚合服务（display）+ 展示侧 Python（gkx_show_service）
异步链路   = Java 聚合服务（display）+ 异步复用专题（topic-async-service）
自建维度   = Java 聚合服务 + 展示侧 Python（不经 :8080/:8081 专题侧门面）
```

---

## 2. 系统全景

### 2.1 七组 35 页

来源：`repos/lumen-ui-science-pc/src/router/menu.ts:38-122`

| 组 | key | 页 | 页面 |
|---|---|---|---|
| 科技发展态势 | `trend` | 10 | 科技全域态势 · 科学技术全景 · 技术发展跟踪 · 全球创新监测 · 湾区创新监测 · 深圳创新监测 · 科技创新评估 · 科技指数 · 科技发展规划 · 维护管理 |
| 科技政策跟踪 | `policy` | 3 | 科创政策全景 · 政策分析评价 · 政策效果推演 |
| 科技人才态势 | `talent` | 4 | 全球领域人才态势 · 关注地区人才态势 · 重点科技人才画像 · 人才引进推荐评估 |
| 科技数据资源 | `data` | 4 | 总体视窗 · 接入视窗 · 主题视窗 · 应用视窗 |
| 科技知识图谱 | `graph` | 4 | 分析展示 · 指标展示 · 算法展示 · 服务展示 |
| 科技成果展示 | `results` | 5 | 软科学成果展示 · 科技创新生态展示 · 科技时空演进展示 · 大型科学仪器共享 · 创新载体孵化载体 |
| 科技服务全景 | `service` | 5 | 科技创新生态服务 · 智库服务 · 科技交流 · 科技竞赛 · 科技传播 |

### 2.2 用户角色与权限影响

来源：`menu.ts:126-132`

| key | 角色 | 权限含义 |
|---|---|---|
| `executive` | 领导驾驶舱用户 | 全域视图，指标口径最全 |
| `analyst` | 业务分析师用户 | 可下钻明细、可导出 |
| `researcher` | 产业与技术研究用户 | 技术/成果维度深，可看图谱 |
| `policy` | 政策与资源配置用户 | 政策推演、资源分配 |
| `operator` | 创新主体运营用户 | 企业/载体运营视角，字段脱敏更严 |
| `governance` | 数据治理与模型运维用户 | 数据资源视窗、就绪度与血缘可见 |

> 角色影响两处实现：**数据权限下推**（§10.4）与**缓存键 `permScope`**（§6.7）。

### 2.3 供方分布总表

| 组 | 主供方 | 数据形态 | 承载 L3 |
|---|---|---|---|
| `trend` | 智树 ADS + 久新 + 算法 | 统计 / 落点 / 事件 / 指数 | `element` |
| `policy` | 智树自建（E7 模块自研） | ADS/DWD 自建表 + `polan` 算法 | `element` |
| `talent` | **久新** | SQL/Python/API 三类交付（API 42 未确认）+ Nebula | `element` |
| `results` | **久新（拟供未回）** | 拟落 ADS；协作网络读图归燕大 | `element` |
| `service` | 智谱（智库）+ ADS（生态）+ **外部跳转** | 见 §7.5 | `element`（部分） |
| `graph` | **燕大** | 平台 HTTP API + Nebula | `graph`（新建） |
| `data` | ⚠️ **供方未找到** | 元数据 / 接入台账 | `datacatalog`（新建） |

### 2.4 现状诊断（可复现事实）

| # | 事实 | 证据 |
|---|---|---|
| F1 | **`gkxlumen-display` 骨架已建，业务端点未实装**——端口 7099，仅 `DomainHealthAggregator` + 3 个 Feign 探活；聚合端点、缓存、降级注入均未填 | `gkxlumen-display/src/main/resources/application.yml:2`；`.../service/DomainHealthAggregator.java` |
| F2 | **`/display/**` 网关路由缺失**，但前端已按 `/situation/v1`、`/innov/v1` 出契约 | 路由表 `db/9x_gkxlumenx_sys_route_conf_lumen_core.sql`：仅 `/innov`、`/metrics`、`/policy`、`/topic`、`/chain`、`/svc` |
| F3 | 前端 **7 组 35 页仅「科技发展态势」1 组实装**，其余回落占位 | `src/router/menu.ts:133-156` `resolveNavComponent` |
| F4 | **一页多接口、前端拼装** | `api/situation/index.ts` 7 个端点；`api/innov/index.ts` 20+ 端点 |
| F5 | **无展示读缓存** | Redis 仅用于网关限流 / SSE 分发 / 幂等；无页面级响应缓存 |
| F6 | **契约真源三处漂移** | 外部（06/06b/06c/06d）· 前端 `@/types/*`（手写）· 各 Controller 自定义；缺「真源 → 生成」链路 |
| F7 | 三库访问路径展示侧**无承载层固化** | ADS/Nebula/ES 角色已约定，但无 L3 服务承接 |
| F8 | **就绪度四维角标（D9）注入点未定** | 前端禁自填，但无统一注入层 |
| F9 | **7 组中 6 组无对应 L3 领域服务** | L3 现有服务均属专题侧或创新监测；`gkxlumen-innov` `InnovSql` 指向 `demo_gkxlumenx_ads`（违反 D12） |
| F10 | **久新供给形态未定**——API / 直连库 / 混合均未确认；同一查询可能需「部分调 API + 部分查库」再拼装；10 类要素责任人栏「久新-？」未落人 | `TS-聚合方案-产业铺底.md` §2；`architecture-baseline.md` §2.2 |

**归因**：① 接入面碎片化（前端直连 4+ 服务前缀）② 聚合缺位（多接口拼装留给前端）③ 契约与路由脱节（有契约无路由）④ 读路径未分层（无缓存）⑤ 降级无策略（弱依赖失败拖垮整页）⑥ 治理缺位（D9 就绪度、空态口径无注入层）。

> 现状诊断已并入本文（原 `architecture-display-optimized.md` §2.1，含 F1–F10 证据）。

---

## 3. 架构总览

### 3.1 分层架构

```
┌──────────────────────────────────────────────────────────────┐
│ L0  前端  lumen-ui-science-pc（Vite7 + Vue3 + TS + Arco）      │
│     7 组 35 页 · nginx 容器 · NodePort 30891                  │
│     唯一出口 /api/display/v1/** · traceparent 已注入          │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ L1  网关  gkxlumen-gateway :9999（NodePort 30895）             │
│     路由 · 鉴权(upms/auth) · Redis 限流 · CORS · 超时 30s      │
│     /display/** → StripPrefix=1 → lb://gkxlumen-display        │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ L2  展示聚合 BFF  gkxlumen-display :7099  /display/v1/**       │
│     区块级端点 · Feign 并行 · 分区降级 · Redis 缓存             │
│     D9 就绪度注入 · ⛔ 不直连 DB / Python                       │
└──────────────────────────────────────────────────────────────┘
        ↓ Feign 并行        ↓            ↓              ↓
┌─────────────────┐ ┌────────────┐ ┌──────────────┐ ┌──────────┐
│ L3 element      │ │ graph      │ │ datacatalog  │ │ metrics  │
│    :7082 新建   │ │ :7083 新建 │ │ :7084 新建   │ │ :7091    │
│ 要素域 24 页    │ │ 图谱域 4页 │ │ 数据资源 4页 │ │ 指标复用 │
└─────────────────┘ └────────────┘ └──────────────┘ └──────────┘
        ↓                ↓
┌──────────────────────────────────────┐   ┌─────────────────┐
│ L4 算法与门面（Python）                │   │ 复用            │
│  gkx_show_service  :8082 【骨架】      │   │  gkxlumen-innov │
│  lumen-algo-py     :8000 / :8001      │   │  :7090（过渡）  │
│  燕大图谱平台 10.50.183.56:8093       │   └─────────────────┘
│  专题侧：search :8080 · svc :8088     │
│          ai :8081                     │
└──────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────┐
│ L5  数据面                                                     │
│  MySQL ADS(只读) · NebulaGraph(经Python) · ES(检索)           │
│  Redis(缓存/限流) · Kafka(事件) · MinIO(导出/报告)             │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 调用链铁律

```
终端 → gkxlumen-gateway → gkxlumen-display（/display/v1/**）
     → Feign 并行 → { element | graph | datacatalog | metrics | innov }
         ├─ element（要素域）→ 智树维度读 ADS；三方维度直调久新/智谱/深势
         ├─ graph（图谱域）  → 燕大平台 / Python 图适配（Java 禁直连 nGQL）
         ├─ datacatalog      → 元数据 / 接入台账
         └─ 需算法加工       → Feign → lumen-algo-py /internal/*
```

**四条不可违反**：

| # | 铁律 | 依据 |
|---|---|---|
| 1 | 前端**禁**直连 Python / DB / Nebula | D15 |
| 2 | display **禁**直连 Python / DB | D15 |
| 3 | Java **禁**写算法、**禁** nGQL | D2 / 存储规约 |
| 4 | `demo-*` **禁**入展示调用链 | D12（⚠️ 现网普遍违反，见 §14 R1） |

### 3.3 服务清单总表

| 层 | 服务 | 端口 | 归属 | 职责 | 状态 |
|---|---|---|---|---|---|
| L1 | `gkxlumen-gateway` | 9999 | 展示 | 路由/鉴权/限流 | ✅ |
| L2 | `gkxlumen-display` | 7099 | 展示 | 区块聚合 BFF | 🟡 骨架 |
| L3 | **`gkxlumen-element`** | **7082** | 展示 | 要素域（24 页） | ❌ 新建 |
| L3 | **`gkxlumen-graph`** | **7083** | 展示 | 图谱域（4 页） | ❌ 新建 |
| L3 | **`gkxlumen-datacatalog`** | **7084** | 展示 | 数据资源域（4 页） | ❌ 新建 |
| L3 | `gkxlumen-innov` | 7090 | 展示 | 载体/事件/城市指数 | ✅ **过渡复用** |
| L3 | `gkxlumen-metrics` | 7091 | 🔗 共享 | 指标注册中心 | ✅ **必复用** |
| L3 | `gkxlumen-topic-async-service` | 7094 | 🔗 共享 | 统一任务 + SSE | ✅ 复用 |
| L3 | `gkxlumen-topic-*` | 7080/7081/7093/7095/7097 | ❌ 专题 | 企业/链/政策/服务机构 | ⛔ 不复用 |
| L3 | `gkxlumen-cms` | — | ❌ 平台 | 内容管理 | ⛔ 不复用 |
| L4 | `gkx_show_service` | 8082 | 展示 | 展示侧门面 | 🟡 **骨架** |
| L4 | `lumen-algo-py` | 8000/8001 | 🔗 共享 | 算法 | ✅ |
| L4 | `gkx_search_service` | 8080 | ❌ 专题 | 专题门面 | ⛔ 不碰 |
| L4 | `gkx_ai_service` | 8081 | ❌ 专题 | AI 服务 | ⛔ 不碰 |
| L4 | `gkx_svc_service` | 8088 | ❌ 专题 | 产业服务链 | ⛔ 不碰 |

### 3.4 端口与地址总表

| 组件 | 地址 | 暴露 |
|---|---|---|
| 前端 PC | NodePort **30891** | 外 |
| 网关 | NodePort **30895** | 外 |
| Nacos | ClusterIP 8848 / NodePort 30849 | 内/外 |
| Grafana | `10.50.69.111:31300` | 外 |
| Tempo / Loki | 30202 / 30311 | 外 |
| MySQL | `10.50.11.76:3306` | 内 |
| ES | `10.50.11.76:9200` | 内 |
| Kafka | `10.50.11.76:9092` | 内 |
| Redis | `10.50.69.111:16379`（lumen 库 7） | 内 |
| MinIO | `10.50.69.111:19000`（桶 `gkx-lumen`） | 内 |
| Nebula（现网） | `10.50.75.136:9669` space `entan` | 内 |
| 燕大图谱平台 | `10.50.183.56:8093` space `gkx_local_1` | 内 |

> **端口分配**：`values.yaml` 已占 7080/7081/7090–7099，**7082–7084 空闲**，分配给三个新建服务。

### 3.5 备选方案对比（聚合 BFF 层）

| | 方案 A（本文） | 方案 B（保守） | 方案 C（折中） |
|---|---|---|---|
| 做法 | 实装 display 聚合 BFF，前端单入口 | 不落 BFF；补路由 + 契约生成，前端继续拼装 | 前端保留多接口，补路由 + 契约 + 缓存（网关层） |
| 首屏性能 | 高（服务端并行 + 缓存） | 低（浏览器拼装） | 中 |
| 一致性 | 高（区块级一致） | 低（多接口时序不一） | 中 |
| 降级能力 | 强（分区降级） | 弱 | 中 |
| 改动面 | 中（新增端点 + 路由 + 缓存） | 小 | 中 |
| 结论 | **推荐** | 备选（时间极紧时） | — |

**L3 服务数备选**（详见 §7.2）：1 个（全塞要素域，图谱栈差异过大）· **3 个（推荐）** · 7 个（一组一服务，供方重复对接、跨组聚合退化 Feign）。

---

## 4. L0 前端层

### 4.1 技术栈

| 项 | 事实 | 证据 |
|---|---|---|
| 构建 | **Vite 7** + Vue3 + TS + Arco Design + UnoCSS | `lumen-ui-science-pc/package.json:8-11,65` |
| 类型检查 | `vue-tsc` | `package.json:10` |
| 部署 | nginx 容器（`nginx:1.27-alpine`），`COPY ./dist /data`，EXPOSE 80 | `docker/Dockerfile:1-12` |
| K8s | NodePort **30891**，ConfigMap `gkx-lumen-pc-nginx` | `k8s/lumen-pc.yaml:4,52,85-92,123` |
| 代理 | `proxy_pass → gkxlumen-platform-gateway…:9999` | `k8s/lumen-pc.yaml` |
| 链路 | `traceparent` 已注入 | `src/utils/request.ts:69-71` |
| Mock | `VITE_APP_USE_MOCK`（`.env.development:8-9`），回退 `ENABLE_MOCK_AUTH` | `src/config/app.ts:9-12` |

### 4.2 工程结构

```
lumen-ui-science-pc/
├─ src/
│  ├─ router/menu.ts            7 组 35 页路由定义（:38-122）
│  ├─ api/
│  │   ├─ request.ts            统一封装：解包 {code,data,msg} + Bearer + traceparent
│  │   ├─ situation/index.ts    ⚠️ 当前 BASE='/situation/v1'（需改为 /display/v1/trend）
│  │   ├─ innov/index.ts        ⚠️ 当前 BASE='/innov/v1'（过渡态，待退役）
│  │   └─ ...
│  ├─ types/*.ts                ❌ 手写类型（无生成，见 §4.7）
│  ├─ config/app.ts             USE_MOCK 开关
│  ├─ mock/                     mock 数据（USE_MOCK=false 时禁用）
│  ├─ utils/observability.ts    埋点
│  ├─ components/
│  │   └─ UnifiedLeafletMap     地图统一封装（天地图）
│  └─ views/                    7 组页面组件
├─ docker/Dockerfile
└─ k8s/lumen-pc.yaml
```

### 4.3 请求层规范

`src/utils/request.ts` 已具备的基座能力（保留并强化）：

| 能力 | 说明 |
|---|---|
| 统一解包 | `{code, data, msg}`，非 0 统一走错误处理 |
| Bearer | Token 自动携带 |
| `traceparent` | 全链路追踪透传（`:69-71`） |
| 错误提示 | 统一 toast / 错误态 |

**需新增**：

| 能力 | 说明 |
|---|---|
| **区块级并发控制** | 同页多区块接口并发上限，避免浏览器连接耗尽 |
| **分区空态渲染** | 按 `empty_reason` 渲染差异化空态 |
| **超时分级** | 轮询类（realtime 30s）与首屏类（3s）分开配置 |

### 4.4 Mock 机制

```
VITE_APP_USE_MOCK=true   → 走 src/mock/**（当前开发态）
VITE_APP_USE_MOCK=false  → 走真实后端，且禁止回落 @/mock/**
```

联调验收标准：**`USE_MOCK=false` 时不得有任何页面走样例数**（对应 NFR「禁造数」）。

### 4.5 契约生成方案（解决 R2）

现状：`src/types/*.ts` **全手写**，`package.json` 无 `openapi-typescript`/`orval` → 契约三处漂移（后端 Controller / 外部接口文档 / 前端手写）。

**目标链路（W1 引入）**：

```
gkxlumen-display 出 OpenAPI（springdoc）
   ↓ openapi-typescript
src/types/generated/api.d.ts（生成产物，禁手改）
   ↓ 引入
页面与 api/*.ts 只消费生成类型
```

配套：CI 校验「生成产物与 OpenAPI 一致」，不一致即失败。

### 4.6 地图与可视化

- 统一封装 `UnifiedLeafletMap` + 天地图
- **按视野加载**：地图移动/缩放时按 bbox 请求，不一次拉全量（对应 §11 性能约束）
- 热力图/散点/区域分级共用一套图层配置

### 4.7 前端规范（禁用项）

| 禁用 | 说明 |
|---|---|
| ❌ 直连 Python / DB / Nebula | D15 |
| ❌ 自填就绪度 ⓘ | 只读消费 display 注入值（D9） |
| ❌ 硬编码缺口文案 | 真源 `data-gap-catalog.yaml` |
| ❌ `USE_MOCK=false` 走 mock | 禁造数 |
| ❌ 禁造 0 / 禁进度百分比 | 诚实性原则 |
| ❌ 手写 API 类型 | 用生成产物（§4.5） |

---

## 5. L1 接入层（网关）

### 5.1 职责

路由 · 鉴权（`gkxlumen-upms`/`gkxlumen-auth`）· Redis 限流 · CORS · 超时控制。

### 5.2 路由规则与现状

| 项 | 规则 |
|---|---|
| 唯一对外前缀 | `/display/**` → `lb://gkxlumen-display` |
| 路径剥离 | **GlobalFilter 已剥第一段，禁止再配 `StripPrefix`**（`db/9x_gkxlumenx_sys_route_conf_topic_chain.sql:3`） |
| 限流 | `RequestRateLimiter` + `remoteAddrKeyResolver`（burst 100000 / replenish 10000） |
| CORS | metadata：`allowedOrigins:*`、`allowCredentials:true` |
| 超时 | `response-timeout: 30000` |

**路由现状**：

| 路由 | 目标 | 状态 |
|---|---|---|
| `/innov/**`、`/metrics/**`、`/policy/**`、`/topic/**`、`/chain/**`、`/svc/**` | 各域服务 | ✅ 已配 |
| **`/display/**`** | `gkxlumen-display` | ❌ **缺失** |

**新增 `db/9x_gkxlumenx_sys_route_conf_display.sql`**（格式对齐 `..._topic_chain.sql`）：

```sql
INSERT INTO `sys_route_conf` (`id`,`route_name`,`route_id`,`predicates`,`filters`,`uri`,`sort_order`,`metadata`,`create_by`,`del_flag`)
SELECT <id>, '展示聚合BFF', 'gkxlumen-display-biz',
  CAST('[{"args": {"_genkey_0": "/display/**"}, "name": "Path"}]' AS JSON),
  CAST('[{"args": {"key-resolver": "#{@remoteAddrKeyResolver}", "redis-rate-limiter.burstCapacity": "100000", "redis-rate-limiter.replenishRate": "10000"}, "name": "RequestRateLimiter"}]' AS JSON),
  'lb://gkxlumen-display-biz', 0,
  CAST('{"cors": {"allowedHeaders": "*", "allowedMethods": "*", "allowedOrigins": "*", "allowedCredentials": true}, "response-timeout": 30000}' AS JSON),
  'agent:api-agent', '0'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM `sys_route_conf`
  WHERE `route_id`='gkxlumen-display-biz' AND `del_flag`='0');
```

> 新建的 `element` / `graph` / `datacatalog` **不配网关路由**——仅内网 Feign 调用。

### 5.3 鉴权链路

```
请求 → 网关鉴权（upms/auth，解析 Token → userId/roles/region/dept）
     → 透传用户信息头 → display
     → display 做数据权限下推（§10.4）+ 缓存键 permScope
```

---

## 6. L2 展示聚合 BFF（`gkxlumen-display`）

### 6.1 定位与粒度判据

> **display 是前端唯一业务入口；接口粒度是「页面区块」，不是「整页」。**

| 原则 | 内容 |
|---|---|
| **入口唯一** | 35 页所有请求经 `/display/v1/**` |
| **接口 = 区块** | 判据：**UI 上需要独立 loading / 空态 / 错误态的，就是独立接口** |
| **接口内跨域并行** | 一个接口可 Feign 并行调多个域服务；单域超时只降级该维度 |
| **禁止纵向合并** | 不得把多区块合并成一个大响应（一个慢接口拖垮整页） |

### 6.2 职责边界

| 职责 | **不做** |
|---|---|
| 区块级聚合（Feign 并行 + 裁剪 + 一致性） | ❌ 不写算法（D2） |
| Redis 页面级读缓存 | ❌ **不直连 DB / Python**（D15） |
| 分区降级 + 诚实空态 | ❌ 不造数、不造 0 |
| D9 就绪度注入 | ❌ 不自填状态、不改绿 |
| 出 OpenAPI（前端唯一契约真源） | ❌ 不复制 graph controller |

### 6.3 区块端点清单（7 组）

路径规范：`/display/v1/{group}/{page}/{action}`

#### trend 科技发展态势（10 页）

| 端点 | 页面 · 区块 | 跨域聚合 |
|---|---|---|
| `GET /display/v1/trend/layers` | 全域态势 · 11 要素 chips + 统计 | 各要素 count 并行 |
| `GET /display/v1/trend/regions` | 全域态势 · 地图 + 落点 + 热力 | **多要素并行**（如企业 + 科研机构） |
| `GET /display/v1/trend/objects/search` | 全域态势 · 检索列表 | 多要素合并 + 统一分页 |
| `GET /display/v1/trend/objects/{id}/detail` | 全域态势 · 详情抽屉 | 四 kind 统一契约 |
| `GET /display/v1/trend/events` | 全域态势 · 事件时间轴 | 事件 + 舆情 |
| `GET /display/v1/trend/realtime` | 全域态势 · 实时监控 KPI | 30s 轮询 |
| `GET /display/v1/trend/tech/panorama` | 技术全景 | 技术分类树 + 热度 |
| `GET /display/v1/trend/tech/tracking` | 技术发展跟踪 | 趋势 + 对比 |
| `GET /display/v1/trend/monitor/{scope}` | 全球/湾区/深圳监测（`scope=global|bay|shenzhen`） | 区域指标 + 排名 |
| `GET /display/v1/trend/evaluation` | 科技创新评估 | 算法（algo-py） |
| `GET /display/v1/trend/index` | 科技指数 | 指数列表/详情/排名 |
| `GET /display/v1/trend/planning` | 科技发展规划 | 规划/指标/进度 |
| `/display/v1/trend/maintain/*` | 维护管理 | 配置类（写） |
| `/display/v1/trend/favorites`、`/tags` | 收藏/标签 | 写 `app_user` |
| `/display/v1/trend/export/*` | 导出任务中心 | 异步（§10.5） |

#### policy 科技政策跟踪（3 页）

| 端点 | 页面 · 区块 |
|---|---|
| `GET /display/v1/policy/panorama` | 科创政策全景 · 政策分布 + 统计 |
| `GET /display/v1/policy/search` | 全景 · 政策检索 |
| `GET /display/v1/policy/{id}/detail` | 全景 · 政策详情 |
| `GET /display/v1/policy/analysis` | 政策分析评价 · 分析维度 |
| `POST /display/v1/policy/simulation` | 政策效果推演 · **异步任务**（算法） |

#### talent 科技人才态势（4 页）

| 端点 | 页面 · 区块 | 说明 |
|---|---|---|
| `GET /display/v1/talent/global` | 全球领域人才态势 | 久新 |
| `GET /display/v1/talent/local` | 关注地区人才态势 | 久新 |
| `GET /display/v1/talent/{id}/profile` | 重点科技人才画像 | 久新 + 算法 |
| `GET /display/v1/talent/recommend` | 人才引进推荐评估 | 久新 + 算法（algo-py `/v1/talent-recommend/compute`） |

#### data 科技数据资源（4 页）

| 端点 | 页面 · 区块 |
|---|---|
| `GET /display/v1/data/overview` | 总体视窗 |
| `GET /display/v1/data/access` | 接入视窗（来源渠道/归集量/更新周期） |
| `GET /display/v1/data/theme` | 主题视窗 |
| `GET /display/v1/data/application` | 应用视窗（调用统计/接口状态） |

#### graph 科技知识图谱（4 页）

| 端点 | 页面 · 区块 | 说明 |
|---|---|---|
| `GET /display/v1/graph/analysis` | 分析展示 | 子图/关系 |
| `GET /display/v1/graph/indicators` | 指标展示 | 图谱指标 |
| `GET /display/v1/graph/algorithms` | 算法展示 | 中心性/社群等 |
| `GET /display/v1/graph/service` | 服务展示 | 图谱服务能力 |

> ⚠️ 全部经 `gkxlumen-graph` → Python 图适配，**Java 禁直连 nGQL**。

#### results 科技成果展示（5 页）

| 端点 | 页面 · 区块 |
|---|---|
| `GET /display/v1/results/soft-science` | 软科学成果展示 |
| `GET /display/v1/results/ecology` | 科技创新生态展示 |
| `GET /display/v1/results/evolution` | 科技时空演进展示 |
| `GET /display/v1/results/instrument` | 大型科学仪器共享 |
| `GET /display/v1/results/carrier` | 创新载体孵化载体 |

#### service 科技服务全景（5 页）

| 端点 | 页面 · 区块 | 说明 |
|---|---|---|
| `GET /display/v1/service/ecology` | 科技创新生态服务 | ADS（有则读，否则空态） |
| `GET /display/v1/service/think-tank` | 智库服务 | **智谱 API** |
| — | 科技交流 / 科技竞赛 / 科技传播 | ❌ **外部跳转，不经 Java** |

> `service` 组 5 页中**仅 2 页需后端**，不要按 5 页估算工作量。

### 6.4 响应包络与分区

```jsonc
{
  "code": 0,
  "data": { /* 必达区：来自 ADS / 读模型 */ },
  "optional": { /* 可降级区：图谱 / 预测 / 洞察，失败为 null */ },
  "readiness": { /* D9：四维 + 指标 8 件套 */ },
  "meta": {
    "traceId": "...",
    "dataVersion": "2026-10-25T10:00:00Z",
    "cacheHit": true,
    "degraded": [ { "factor_key": "institution", "empty_reason": "科研机构服务不可用" } ]
  },
  "msg": "ok"
}
```

### 6.5 并行聚合实现

沿用 `DomainHealthAggregator` 范式（`CompletableFuture` + `orTimeout` + `exceptionally`），并按区块端点推广。

**通用聚合器骨架**：

```java
@Component
public class BlockAggregator {

    private static final Map<String, Long> TIMEOUT_MS = Map.of(
        "map",   3000L,   // 地图类
        "kpi",   1000L,   // KPI 类
        "search",2000L,
        "export",10000L
    );

    public <T> CompletableFuture<Partition<T>> supply(String name,
                                                      String blockType,
                                                      Supplier<T> caller) {
        long ms = TIMEOUT_MS.getOrDefault(blockType, 2000L);
        return CompletableFuture.supplyAsync(caller::get)
                .orTimeout(ms, TimeUnit.MILLISECONDS)
                .thenApply(Partition::ok)
                .exceptionally(ex -> Partition.degraded(name, reasonOf(ex)));
    }

    /** 聚合：任一分区失败不影响其他分区，失败信息进 meta.degraded[] */
    public <T> AggregatedResult<T> join(List<CompletableFuture<Partition<T>>> futures) {
        // 逐分区 join，收集 degraded，组装 meta
    }
}
```

**要点**：

- 编排线程池**独立配置**，不复用 Feign 默认池
- 队列容量与拒绝策略显式配置；拒绝时降级为 `empty_reason`，**不抛异常**

### 6.6 分区降级实现

| 层 | 降级对象 | 表现 |
|---|---|---|
| display | 域服务分区 | 该分区 `null` + `empty_reason` → `meta.degraded[]` |
| L3 element | 数据片段（Fragment） | 该片段 `empty`，其余片段照常返回 |

**原则：任一分区失败不放大为 5xx。**

`empty_reason` 取值规范：

| 场景 | 文案 |
|---|---|
| 通道超时 | `"XX 服务响应超时"` |
| 通道异常 | `"XX 服务不可用"` |
| 数据未就绪（阶段一） | `"XX 数据接入中"` |
| 查询无结果 | `"暂无数据"` |

### 6.7 缓存设计

| 项 | 设计 |
|---|---|
| 键 | `disp:{group}/{page}:{filtersHash}:{permScope}:{dataVersion}` |
| TTL | 按页热度分档（**当前默认关闭，TTL 300s**，`configs/gkxlumen-display-dev.yml:19-21`） |
| 失效 | 权限变化（`permScope`）或数据版本（`dataVersion`）变化**自动失效**，避免脏缓存 |
| 层级 | 浏览器（可选 SW）→ display Redis（页面级）→ **域服务不叠缓存** |
| 例外 | 久新通道延迟高时，在 `channel/jiuxin-*` 内做**通道级短 TTL**，对 domain 透明 |

**TTL 分档建议**：

| 页面类型 | TTL | 理由 |
|---|---|---|
| 实时监控 KPI | 10–30s | 30s 轮询 |
| 地图落点 | 5–10 min | 数据变化慢 |
| 统计/排行 | 10 min + `dataVersion` 失效 | 批次更新 |
| 详情 | 5 min | — |
| 导出配置 | 30 min | 少变 |

### 6.8 D9 就绪度注入

```
/metrics/v1/catalog（gkxlumen-metrics，指标 8 件套唯一真源）
        ↓ Feign
   display 注入 readiness{}
        ↓
   前端只读消费 ⓘ 角标（禁自填）
```

- element 只返回 `metric_id`，**就绪度判定与注入在 display 完成**
- ⚠️ 阻塞：`metric_id` 清单未登记 → D9 ⓘ 暂无法对接

### 6.9 超时预算

| 层 | 建议 | 说明 |
|---|---|---|
| 网关 | `response-timeout: 30000` | 现网路由配置 |
| display → L3 | 地图 3s / KPI 1s / 检索 2s / 导出 10s（可配，替代现有固定 2000ms） | §6.5 |
| L3 → 通道 | HTTP connect/read；JDBC `queryTimeout` | 通道级独立 |
| 前端轮询 | realtime 30s | 天然独立 |

### 6.10 现状与缺口

| 项 | 状态 |
|---|---|
| 模块 | ✅ 已建（`DomainHealthAggregator` + 3 Feign 探活） |
| 端口 | 7099 |
| Redis 缓存 | 配置存在，**默认关闭** |
| 聚合端点 | ❌ 未填（仅 `/v1/aggregations/health`） |
| `/display/**` 路由 | ❌ 未配 |

---

## 7. L3 领域服务层

> **本节给全景与边界；`element` 内部实现细节见 `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-DESIGN-01.md`（16 节）。**

### 7.1 划分判据

| 判据 | 内容 | 结论 |
|---|---|---|
| **① 跨维度聚合频率** | 聚合越频繁越该同进程 | 8 个共享维度并入 `element`（本地方法调用 vs Feign） |
| **② 供方对接集中度** | 同一供方只应有一处对接（凭证/限流/重试/容错收敛） | 久新唯一收敛于 `channel/jiuxin-*` |
| **③ 消费方数量** | 被 ≥2 系统消费才值得独立成服务 | `element` 仅服务展示，**不拆更多服务** |

### 7.2 为什么是 3 个服务（不是 1 个、不是 7 个）

| 方案 | 问题 |
|---|---|
| 1 个（全塞 element） | 图谱域技术栈（Nebula + 平台 API）与要素域（MySQL ADS）差异过大；燕大账号/space 需独立管控 |
| 7 个（一组一服务） | 人才/成果/技术等要素被多组复用 → 同一供方（久新）被 3 个服务重复对接，凭证/限流/重试分散；跨组聚合退化 Feign |
| **3 个（推荐）** | 按**数据域/供方边界**切：要素域 · 图谱域 · 数据资源域 |

### 7.3 `gkxlumen-element`（要素域，24 页）

| 项 | 值 |
|---|---|
| 端口 / 服务名 | **7082** / `gkxlumen-element-biz` |
| 路由 | `/element/v1/**`，**全部 `@Inner`**，仅内网 Feign，不配网关路由 |
| 主数据源 | `gkxlumenx_ads`（`@Primary`，`read-only: true`） |
| 第二数据源 | 久新库（`@Qualifier`，`read-only: true`）— 需 D3 豁免 |
| 写库 | `app_user` 家族（收藏/标签/导出） |

**包结构**：

```
domain/     【按维度 = 对外语义】
  enterprise/ chain/ service/ policy/     → 智树自建，直读 ADS
  institution/ talent/ tech/              → 久新，接口隔离
  achievement/ carrier/                   → 成果 / 载体
  general/                                → 综合服务（横切编排）
channel/    【按供方 = 技术防腐层】
  local-ads/  jiuxin-http/  jiuxin-jdbc/  yanda/  zhipu/  shenshi/
support/    ElementDao（gkxlumenx_ads 全限定名）
```

**片段级混合编排**（应对「久新部分给 API、部分靠自己查库、需拼装」）：

```
一次「科研机构详情」查询
  ├─ jiuxin.institution.base     → jiuxin-jdbc   （自己查库）
  ├─ jiuxin.institution.metrics  → jiuxin-http   （久新有现成 API）
  └─ jiuxin.institution.relation → local-ads     （我方 ADS）
  三片段并行/串行获取后在 Assembler 内拼装
```

配置仅描述「片段 → 通道」，**编排是手写 Java**：

```yaml
gkxlumen:
  element:
    channels:
      default: local-ads
      mapping:
        jiuxin.institution.base:     jiuxin-jdbc
        jiuxin.institution.metrics:  jiuxin-http
        jiuxin.institution.relation: local-ads
```

**硬性约束 C1–C5**（详见 L3 详细文档 §6.7）：

| # | 约束 |
|---|---|
| C1 | 久新数据源**只能**由 `channel/jiuxin-jdbc/` 持有（保障可拆分） |
| C2 | **主体键归一化**：片段间传递用 `object_id`，不用供方原始键 |
| C3 | **不复刻 `InnovSql.qualify()` 的 demo 映射** |
| C4 | 双数据源：业务库显式建 bean 并标 `@Primary`；`@Qualifier` **必须显式** |
| C5 | 库名/凭证走 Nacos + K8s Secret，不硬编码、不进 git |

### 7.4 `gkxlumen-graph`（图谱域，4 页）

| 项 | 值 |
|---|---|
| 端口 | **7083** |
| 路由 | `/graph/v1/**`，`@Inner` |
| 数据源 | 不直连图库；经燕大平台 API / Python 图适配 |
| 职责 | 子图查询、图谱指标、算法结果展示、服务能力 |

**关键约束**：**Java 禁直连 nGQL**（存储规约），必须经 Python 适配层。

⚠️ **待裁决（A8）**：现网 Nebula（`10.50.75.136:9669` space `entan`）与燕大（`10.50.183.56:8093` space `gkx_local_1`，87.54 万实体 / 61.88 万关系）是**两套图谱**，graph 组用哪一套需定。

### 7.5 `gkxlumen-datacatalog`（数据资源域，4 页）

| 项 | 值 |
|---|---|
| 端口 | **7084** |
| 路由 | `/datacatalog/v1/**`，`@Inner` |
| 数据 | 元数据 / 接入台账（来源渠道、表、归集量、更新周期、调用统计、接口状态） |
| ⚠️ 风险 | **供方未找到**（原华为云大数据团队 2026-10-15 退出）→ 4 页暂空态 |

### 7.6 复用边界清单（✅ 已裁决 · 2026-10-25）

> **裁决**：徐腾强确认「**展示侧不复用专题侧**」——展示系统**不复用专题的业务查询链路**，改为自建 L3 服务（A1 定为 **(a) 新建 3 个**）。
>
> ⚠️ **「不复用」≠ 一刀切**。下表是**权威边界**：平台级与指标级能力**仍必须复用**，否则违反上位铁律。开发请以本表为准。

**✅ 必须复用（不复用即违规）**

| 服务 | 为什么必须复用 | 依据 |
|---|---|---|
| `gkxlumen-gateway` | 全项目统一入口，展示不自开网关 | D5 |
| `gkxlumen-upms` / `gkxlumen-auth` | 统一鉴权 / SSO / 权限，业务服务不各自实现 | D6 |
| `gkxlumen-metrics` | **指标口径唯一真源**；D9 要求「指标 8 件套 + 四维就绪度」仅由 `/metrics/v1/catalog` 供给，前端禁自填 | **D9 铁律** |
| `lumen-algo-py`（共用算法） | 算法统一出口，注册后经 `/internal/*` 调用 | D2 |

**✅ 已确认复用（基础设施，非业务查询链路）**

| 服务 | 理由 | 裁决 |
|---|---|---|
| `gkxlumen-topic-async-service` | **它是独立服务**（非耦合在业务项目里）。复用其任务表 / SSE / MinIO / Redis 并发锁，避免重复造任务体系 | ✅ **已确认复用**（2026-10-25 徐腾强：「异步任务复用专题」）。展示侧只做「提交任务 + 订阅 SSE + 取结果」**薄适配，不自造任务体系** |
| `gkxlumen-innov` | 载体 / 事件 / 城市指数已实线，**过渡复用** | 🟡 过渡；后续按要素迁入 `gkxlumen-element` |

**⛔ 不复用（本次裁决范围）**

| 服务 | 不复用原因 |
|---|---|
| `gkxlumen-topic-*`（enterprise / chain / svc / policy 等） | 数据形态不同（检索 / 画像 / 对比篮 vs count / 落点 / 热力 / 时间序列）；展示所需形态**未实装**；供方通道（久新 / 燕大 / 智谱 / 深势）与专题侧不同 |
| `gkx_search_service` :8080 | 专题侧 Python 门面，复用即违反 **D15 三重隔离** |
| `gkx_ai_service` :8081 · `gkx_svc_service` :8088 | 同上，专题侧 |
| `gkxlumen-cms` | 平台侧内容管理（写侧） |

**🆕 展示侧自建**

| 组件 | 说明 |
|---|---|
| `gkxlumen-element` :7082 · `gkxlumen-graph` :7083 · `gkxlumen-datacatalog` :7084 | 本次新建的 L3 服务（A1 = (a)） |
| `gkx_show_service` :8082 | 展示侧专属 Python 门面（D15 已有；⚠️ **当前是骨架**，见 R3 / A6） |

> **一句话边界**：**业务数据链路自建 · 基础设施与指标口径复用 · 专题侧 Python 门面绝不碰。**

### 7.7 ⚠️ 与共识 C1 的偏差（需 A1 裁决）

共识 C1 为「**Java 只增加一个聚合服务，其他复用专题链路**」；本文 §7.2 建议**新建 3 个 L3 服务**，与之不符。差异原因：

| 维度 | 共识 C1 的前提 | 调研实际 |
|---|---|---|
| 专题侧可供复用 | 专题链路已实装、可直接提供查询 | 展示所需形态（要素 count / 落点 / 热力 / 时间序列）在 `gkxlumen-topic-*` **未实装**；已实装的是检索 / 画像 / 对比篮（`gkx_search_service` 76 端点） |
| 隔离要求 | — | 复用 topic-* 意味着下游接专题侧 Python 门面 :8080，**与 D15 三重隔离直接冲突** |
| 供方通道 | 「不止咱们自己还有其他公司的」 | 展示侧供方（久新 / 燕大 / 智谱 / 深势）与专题侧不同，**通道无法共用** |

**本文结论**：C1 中「只增加一个聚合服务」在**对外暴露面**上成立（display 唯一对外，L3 全部 `@Inner`）；但「复用专题链路」在数据形态与 D15 上不成立，故建议**新建而非复用**。

> ✅ **已裁决（2026-10-25 · 徐腾强）**：「**展示侧不复用专题侧**」。确认 **A1 = (a) 新建 3 个 L3 服务**，接受与共识 C1 的偏离。边界细则见 **§7.6**。
>
> **连带效果**：展示侧既不复用专题，则原担心的「专题侧对外供给第三方的可见性过滤**污染展示侧查询结果**」问题**自动消解**，不再需要确认。

---

## 8. L4 算法与门面层（Python）

### 8.1 服务清单（实测）

| 服务 | 端口 | 路由前缀 | 现状 | 归属 |
|---|---|---|---|---|
| **`gkx_show_service`** | 8082 | `/internal/gkx-show/**` | 🟡 **骨架**：仅 `/healthz` + `meta/ping`，`data_source:"none"` | **展示侧** |
| `lumen-algo-py` | 8000 / 8001 | `/v1/evaluation/compute`、`/v1/risk-insight/compute`、`/v1/talent-recommend/compute`、`/gdf/tasks` | ✅ 实线（chain/entan/evaluation/industry/policy 等子模块） | 🔗 共用 |
| `gkx_ai_service` | 8081 | `/internal/gkx-ai/**` | ✅ 实线 18 端点 | ❌ 专题侧 |
| `gkx_search_service` | 8080 | `/internal/gkx-search/**` | ✅ 实线 76 端点 | ❌ 专题侧 |
| `gkx_svc_service` | 8088 | `/internal/gkx-svc/**` | ✅ 实线 11 路由 | ❌ 专题侧 |
| `gkx_ai_worker` | — | 无 HTTP | Kafka asyncio 消费 | ❌ 专题侧 |
| `lumen-etl-es-py` | 8000 | — | 读 DWD 写 ES `gkx_enterprise` | ETL |

### 8.2 展示侧门面现状（关键缺口 R3）

**`gkx_show_service` 仍是骨架**（`main.py:71-94`：`data_source:"none"`，端点仅 `/healthz` + `meta/ping`）。

含义：D15 指定的「展示侧专属门面」**实际不存在**，依赖它的路径全部不可达。

**应对**（✅ A6 已裁决）：阶段一走「Java 直读 ADS」（`storage/README.md:89` 明文允许「ADS 契约面 → Java 只读」）。门面实装后按场景分流——纯查询 / 聚合 / 分页**继续直读 ADS**（D3），需算法加工**走门面**（D2）。

### 8.3 调用约定

| 场景 | 走法 |
|---|---|
| 纯查询 / 聚合 / 分页 | **Java 直读 ADS** |
| 需算法加工 | Feign → `lumen-algo-py` `/internal/*` |
| 图谱 | Feign → Python 图适配；**Java 禁直连 nGQL** |
| 展示自建维度门面（未来） | Feign → `gkx_show_service` :8082 |

### 8.4 三重隔离（D15）

`gkx_show_service`（展示侧）与 `gkx_search_service`（专题侧）**进程级 + 镜像级 + 路由级**隔离，协作边界由 `CODEOWNERS` 划定（`repos/lumen-topic-py/CODEOWNERS:7,11`）。

---

## 9. L5 数据面

### 9.1 存储清单

| 存储 | 实例 | 用途 | 展示读写 | 写入方 |
|---|---|---|---|---|
| **MySQL ADS** | `10.50.11.76:3306` | 契约面 / 明细真源 | **Java 只读** | Python / 数据工厂 |
| **NebulaGraph** | `10.50.75.136:9669`（`entan`）；燕大 `10.50.183.56:8093`（`gkx_local_1`） | 图谱 | **经 Python，Java 禁直连** | 燕大 / Python |
| **Elasticsearch** | `10.50.11.76:9200`，索引 `gkx_enterprise` | 检索 | 经 Python 适配 | `lumen-etl-es-py` |
| **Redis** | `10.50.69.111:16379`，lumen 库 **7** | 缓存 / 限流 / SSE / 任务配额 | 读写 | — |
| **Kafka** | `10.50.11.76:9092`，topic `gkx.analysis.result`（+`.dlq`） | 异步任务事件 | 生产/消费分离 | — |
| **MinIO** | `10.50.69.111:19000`，桶 **`gkx-lumen`** | 导出 / 报告资产 | Java 写；**前端经后端下载** | — |

### 9.2 数据模型

**展示侧新建表**（前缀 `ts_`，落 `db/9x_gkxlumenx_element.sql`，命名对齐 `9x_gkxlumenx_cms.sql`）：

| 表 | 用途 | 关键字段 |
|---|---|---|
| `ts_factor_stat` | 要素统计（地域 × 时间） | `factor_key`、`region_code`、`stat_date`、`granularity`、`object_count`、`metric_value`、`yoy_growth`、`metric_id` |
| `ts_object` | 对象主表（跨要素统一） | `object_id`(PK，**归一化统一键**)、`object_type`、`source`、`source_key`(供方原始键，仅追溯)、`name`、`region_code`、`lon`/`lat`、`status` |
| `ts_object_metric` | 对象指标 | `object_id`、`metric_id`、`stat_date`、`value`、`unit` |
| `ts_event` | 科创事件 | `event_id`、`title`、`event_type`、`importance`、`occur_date`、`region_code`、`summary` |
| `ts_opinion` | 舆情 | `id`、`event_id`、`source`、`sentiment`、`publish_time`、`content` |
| `ts_favorite` | 收藏（`app_user` 家族） | `user_id`、`object_id`、`object_type`、`created_at` |
| `ts_tag` / `ts_object_tag` | 标签 | `tag_id`、`user_id`、`name` / 关联表 |
| `ts_export_task` | 导出任务 | `task_id`、`user_id`、`status`、`file_url` + 审计字段 |

**索引策略**：`ts_factor_stat(factor_key, region_code, stat_date)`、`ts_object(object_type, region_code)`、`ts_object(source, source_key)`、`ts_object_metric(object_id, metric_id, stat_date)`。

**复用表**：智树自建维度读现有 ADS（`enterprise_*`、`svc_*`、政策表、载体表等），**复用现成表不新建**（`TS-聚合方案 §1.3`）。

### 9.3 数据流

```
【写】Python（algo / ETL / 数据工厂）→ gkxlumenx_ads.ts_*
【读】display → Feign → element
        ├─ channel/local-ads   → gkxlumenx_ads.ts_*     （只读）
        ├─ channel/jiuxin-http → 久新 API                （只读）
        └─ channel/jiuxin-jdbc → 久新库                  （只读，需豁免）
【写】element → app_user 家族（收藏/标签/导出，D4）
```

**久新两阶段演进**：

| 阶段 | 通路 | 依据 |
|---|---|---|
| 一（现在） | `domain/*` → `channel/jiuxin-*` → 久新 | D15 §2.2 |
| 二（数据工厂就绪） | `domain/*` → `channel/local-ads` → `ts_*` | D7 |

切换方式：**改 `ChannelProperties.mapping`，domain 与 Assembler 零改动**。

### 9.4 只读约束与事务边界

| 约束 | 实现 |
|---|---|
| ADS 只读 | Hikari `read-only: true` |
| 久新库只读 | Hikari `setReadOnly(true)` + `poolName` 显式 |
| 事务 | `DataSourceTransactionManagerAutoConfiguration` 按 single-candidate 绑 `@Primary`；**写操作仅针对 `app_user`**，ADS / 久新库不参与事务 |
| 多数据源 | 业务库显式建 bean 并标 `@Primary`；注入处 `@Qualifier` **必须显式**（否则静默连错库） |

### 9.5 秒开预跑读模型（2026-10-20 决策）

> 决策（徐腾强）：**每个页面都要做秒开策略**——页面默认筛选条件的数据**凌晨提前跑好**，用户进来秒开；用户操作了未预跑的筛选项，则回退**实时查询**。

**预跑规格（以「科技全域态势 · 科创要素」为例）**：

| 项 | 内容 |
|---|---|
| 预跑维度 | 地域范围 **×** 学科领域 **×** 科创要素 的**全部组合方式** |
| 附加维度 | **一个默认年范围** |
| 触发时机 | 凌晨跑批（T+1），产出后写 `dataVersion` |
| 不预跑（走实时） | **时间筛选**、**搜索定位输入框** |

**读路径判定**：

```
请求进入
  ├─ 筛选条件 ∈ 预跑组合（且年为默认）→ 读预跑表（毫秒级 = 秒开）
  └─ 否则（改了时间 / 用了搜索框）      → 实时查询 ADS（秒级）
```

**⚠️ 组合规模是笛卡尔积（A14 已裁决 = 分级预跑）**：

预跑量 = |地域| × |学科领域| × |科创要素|，随维度增长极快：

| 地域 | 学科 | 要素 | 组合数 |
|---|---|---|---|
| 10 | 20 | 11 | 2,200 |
| 30 | 50 | 11 | 16,500 |
| 100 | 100 | 11 | **110,000** |

**已选定（A14 = b 分级预跑）**：① **分级预跑**——高频组合全跑、长尾按需触发并缓存；② 预跑表按 `dimHash` 联合主键，命中即返回；③ 未命中实时查询后**异步回填**预跑表。

> **待补输入**：地域 / 学科 / 要素的**具体枚举量级由产品定义，开发时再落地**——本次只定「分级」这个策略，不定具体跑哪几种组合。

**落点**：预跑结果落 ADS 内展示读表（建议前缀 `ts_preagg_*`，**最终命名依赖 A11**），Python ETL 凌晨产出；display **只读**，缓存键含 `dataVersion`（§6.7）——新批次产出即自然失效，**无脏缓存**。

---

## 10. 横切机制

### 10.1 缓存

见 §6.7（键、TTL 分档、失效策略）。

### 10.2 分区降级

见 §6.6（display 分区 + L3 片段两级降级，均不放大为 5xx）。

### 10.3 可观测

| 层 | 方案 |
|---|---|
| 前端 | `traceparent` 注入（`src/utils/request.ts:69-71`） |
| Java | **OTel JavaAgent 2.19.0**，`OTEL_EXPORTER_OTLP_ENDPOINT=http://<release>-otel-collector:4318`（`templates/_helpers.tpl:134-135`） |
| Python | `OTEL_SERVICE_NAME` + `TraceHeaderMiddleware` |
| 后端 | Tempo 30202 / Loki 30311 / Grafana `10.50.69.111:31300` |
| display 补指标 | 聚合耗时 · 各分区耗时 · 缓存命中率 · 降级次数 · `dataVersion` 分布 |
| L3 补日志 | 片段降级必须 `warn` 且带 `capabilityKey` + 耗时 |

### 10.4 权限与脱敏

- 网关统一鉴权（upms/auth）；display 做**数据权限下推**（region / dept 级）
- 敏感字段（人才联系方式等）在 **display 层脱敏**，最小权限 + 审计
- 缓存键含 `permScope`，权限变化自动失效

### 10.5 异步任务与导出（✅ 复用专题已确认）

> 2026-10-25 裁决：**异步任务复用专题**（`gkxlumen-topic-async-service`）。展示侧**不自造任务体系**，只做薄适配。依据：共识 C3「异步任务复用专题」「如果是独立的，那就完全没问题」，且李拜六确认该服务是**独立的**。

- 重分析 / 报告 / 导出：display 仅做「提交任务 + 订阅 SSE + 取结果」薄适配，**不自造任务体系**
- 复用 `gkxlumen-topic-async-service`：统一任务表 + SSE（Redis 分发）+ Redis 并发锁 + XXL-Job 状态修正 + **MinIO 大结果外置**
- 规则：切条件**不**自动起任务；同用户同条件仅一条在跑；当天已成功直接打开结果
- **禁止前端直连对象存储**；文件经后端签名/代理下载

### 10.6 契约治理（三层单向流）

```
外部真源（06 / 06b / 06c / 06d）
   ↓
后端 OpenAPI（gkxlumen-display 对外唯一契约）
   ↓ openapi-typescript 生成
前端类型（@/types/generated/*，废止手写漂移）
```

- 指标 8 件套 + 四维就绪度：仅 `/metrics/v1/catalog` 供给 → display 转发注入
- 缺口长文案真源 = `{模块}/data-gap-catalog.yaml`，禁前端硬编码
- CI 校验生成产物与 OpenAPI 一致

### 10.7 错误处理与空态

| 层 | 处理 |
|---|---|
| L3 | 片段失败 → `Fragment.empty(key, reason)`，不抛异常 |
| L2 | 分区失败 → `null` + `empty_reason` → `meta.degraded[]` |
| L0 | 按 `empty_reason` 渲染差异化空态；**禁造 0、禁进度百分比** |
| 异常兜底 | `GlobalBizExceptionHandler`（已处理 Exception / SQLException / FeignException） |

### 10.8 页面秒开策略（预跑 + 实时回退）

> 2026-10-20 徐腾强决策；与 §9.5 预跑读模型配套，本节讲**链路编排**。

| 环节 | 设计 |
|---|---|
| 进入页面 | 前端带**默认筛选条件**请求 → display 判定命中预跑 → 读预跑表 → **毫秒级返回** |
| 命中判定 | 请求筛选条件 → 算 `dimHash` → 查预跑表主键；命中则直接返回 |
| 未命中回退 | 筛选含「非默认时间范围」或「搜索定位关键词」→ **实时查询** ADS，走 §9.2 正常读路径 |
| 回退体验 | 回退为秒级（非毫秒级），前端给 loading 态；**不得因回退而报错或空态** |
| 预跑失效 | `dataVersion` 变更（凌晨新批次）→ 缓存键失效 → 下次请求读新批次 |
| **降级** | 预跑表未产出 / 跑批失败 → **整体回退实时查询**，`meta.degraded[]` 标 `preagg_unavailable`；**页面仍可用（慢但不空）** |

**⚠️ 秒开能否成立的关键：默认筛选条件必须前后端一致**

建议由**后端下发**页面默认筛选（`GET /display/v1/{group}/{page}/defaults`），**禁前端硬编码**。

> 若前端硬编码一套默认值、后端预跑用了另一套，**所有请求都会回退实时查询，秒开策略完全失效且静默**——不报错、不告警，上线后极难定位。故此项列为 **W1 验收项**。

### 10.9 订阅模块（展示系统自有业务）

> 2026-10-20 共识：展示系统**有自己的订阅等业务模块**；「规划做一个订阅模块，我在想共用专题的哪个」（李拜六）——**具体复用哪个服务当时未定点**。

**现状**：❓ **未定点**。对话中李拜六仅说「理论上」复用，未指名服务；徐腾强亦未就此给出结论。这是本次梳理发现的**共识空档**。

**✅ 裁决结论**（A15 = (a)；2026-10-26 徐腾强对已裁决项**无异议，按执行**）：

| 方案 | 做法 | 评价 |
|---|---|---|
| (a) **复用 `gkxlumen-topic-async-service`** | 订阅的**任务调度 / SSE / 结果存储**全部复用；展示侧只建「订阅关系 + 触发规则」 | ✅ **推荐**——与 C3「异步复用专题」一致，不自造任务体系 |
| (b) 展示侧自建订阅服务 | 独立服务 | ❌ 与 C3 冲突，重复建设 |
| (c) 落 `gkxlumen-element` 内 | 订阅作为 element 的一个 domain 包 | 🟡 可行但订阅是**跨组横切**（不只要素域），放 element 内边界不清 |

**订阅链路（建议）**：

```
用户订阅（页面 / 指标 / 要素）
   ↓ 写订阅关系（展示侧库，D4 `app_user` 家族 — 依赖 A9）
   ↓ 定时触发（XXL-Job；或凌晨预跑产出后触发）
   ↓ 提交任务 → gkxlumen-topic-async-service（复用：任务表 + SSE + MinIO）
   ↓ 结果推送（站内 / 邮件）
```

**约束**：

- 订阅**只复用异步执行能力**；订阅关系与触发规则属展示侧，**不落专题库**
- 大结果走 MinIO（D14 桶 `gkxlumen`）；**禁前端直连对象存储**
- ⚠️ **XXL-Job 当前 Helm 未部署（R8）**——订阅定时触发依赖它，需先确认部署计划
- 与秒开策略联动：订阅推送宜**挂在凌晨预跑产出之后**，否则推送的是昨日数据

### 10.9.1 用户体系选型（回答 A9 · 2026-10-26）

> 徐腾强要求方案侧先说明 `app_user` **「是哪一类库、谁建的（平台自有 / 还是三方提供）」**，再定运维 / DBA 落点。

**查证结论**（依据代码与建表脚本）：

| 项 | 结论 |
|---|---|
| 类别 | ✅ **平台自有**（**非三方提供**） |
| 谁建的 | `gkxlumen-app-server`；MyBatis-Plus 实体 `AppUser` / `AppUserMapper`，版权 `Copyright (c) 2018-2026 gkxlumen` |
| 建表脚本 | `db/999gkxlumenx_app.sql`（亦见于 `db/0gkxlumenx_boot.sql`） |
| 归属 | **App 端（移动端）用户体系**；与 `upms` 的 `sys_user`（管理后台）**并列两套** |
| 关键字段 | `user_id` / `username` / `phone` / `email` / `wx_openid` / `tenant_id` |

**A9 的性质随之变了**：不再是「库未找到 → 问运维」，而是**「展示系统（PC 端）用哪一套用户体系」**。

| 方案 | 做法 | 评价 |
|---|---|---|
| (a) **复用 `upms` 的 `sys_user`** | 写库走 `gkxlumen-upms` 体系 | ✅ **建议**——PC 端常规做法；`upms` 本就在「必须复用」清单（D6 鉴权）；收藏 / 标签 / 订阅属 **PC 侧用户行为** |
| (b) 跨端共用 `app_user` | PC 与 App 共用一套用户表 | 🟡 **仅当 PC 与 App 确为同一用户池**才成立；否则 App 端表混入 PC 行为数据，两侧语义打架 |
| (c) 展示侧自建 `display_user_*` | 新建用户表 | ❌ 与 D6 冲突（鉴权应统一），重复建设 |

**⚠️ 阻塞面**：A9 未定 → **订阅关系、收藏、标签、导出配置均无处落库**，直接卡住 A15（订阅模块）实装。

**请你二选一**：确认 PC 与 App 是否同一用户池 → **是则 (b)，否则 (a)**。

---

## 11. 非功能设计

| 维度 | 要求 |
|---|---|
| 性能 | 驾驶舱首屏 P95 ≤ 3s；GIS 按视野加载；**图失败不挡 KPI** |
| 一致性 | 指标口径唯一真源 = ADS 契约面；**禁前端/Java 造数** |
| 诚实性 | 空态 `null + empty_reason`；禁造 0；禁进度百分比 |
| **数据量** | ⚠️ 地图落点需早期验证；达数万级须 SQL 聚合或按视野分页，**不可全量透传** |
| N+1 | 禁止：对象列表与指标须批量查询 |
| 慢查询 | 所有 ADS 查询设 `queryTimeout` |
| 容量 | 新服务无状态，副本 2，可水平扩 |

---

## 12. 部署与配置

### 12.1 部署基线

| 项 | 事实 |
|---|---|
| Helm | `repos/lumen-svc-platform/helm/gkxlumen-platform/`（`values.yaml` / `values-lumen.yaml`） |
| 命名空间 | `dev` |
| 镜像仓库 | `harbor.htmisoft.net/gkx` |
| Nacos | ClusterIP 8848；namespace `public`；group `DEFAULT_GROUP`；配置库 `gkxlumenx_config` |
| 前端 | `frontend.enabled=false`（独立部署，NodePort 30891） |
| CI | `.gitlab-ci.yml`（lumen-svc-platform / lumen-topic-py / lumen-algo-py / lumen-ui-science-*） |

### 12.2 新增服务部署项

| 服务 | 需新增 |
|---|---|
| `gkxlumen-element` | Helm 模块块（端口 7082）+ `configs/gkxlumen-element-dev.yml` + `db/9x_gkxlumenx_element.sql` |
| `gkxlumen-graph` | Helm 模块块（7083）+ `configs/gkxlumen-graph-dev.yml` |
| `gkxlumen-datacatalog` | Helm 模块块（7084）+ `configs/gkxlumen-datacatalog-dev.yml` |
| `gkxlumen-display` | `db/9x_gkxlumenx_sys_route_conf_display.sql`（§5.2） |

### 12.3 `element` 数据源配置示例

```yaml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${SITUATION_MYSQL_HOST:10.50.11.76}:${SITUATION_MYSQL_PORT:3306}/${SITUATION_MYSQL_DB:gkxlumenx_ads}?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    username: ${SITUATION_MYSQL_USER:gkxlumenx}
    password: ${SITUATION_MYSQL_PASSWORD}
    hikari:
      maximum-pool-size: 10
      read-only: true          # D3：Java 对 ADS 只读

gkxlumen:
  element:
    channels:
      default: local-ads
      mapping:
        # jiuxin.institution.base:    jiuxin-jdbc
        # jiuxin.institution.metrics: jiuxin-http
      timeout-ms:
        jiuxin-http: 3000
        jiuxin-jdbc: 2000
        local-ads:   1500
    jiuxin:
      http:
        base-url: ${JIUXIN_API_BASE_URL:}
        connect-timeout-ms: 3000
        read-timeout-ms: 10000
      jdbc:
        host: ${JIUXIN_MYSQL_HOST:}
        port: ${JIUXIN_MYSQL_PORT:3306}
        db:   ${JIUXIN_MYSQL_DB:}
        username: ${JIUXIN_MYSQL_USER:}
        password: ${JIUXIN_MYSQL_PASSWORD:}   # K8s Secret，不进 git
```

> ⚠️ 库名默认值受 §14 R1 影响（`gkxlumenx_ads` 现网未出现，需先统一口径）。

---

## 13. 演进路线

| 波次 | 内容 | 出口 |
|---|---|---|
| **W1** | ① display 补全 + `/display/**` 路由 + OpenAPI 契约；② **新建 `gkxlumen-element`**（骨架 + 双数据源 + `ts_*` DDL + `domain/enterprise` 链路）；③ `trend` 组区块端点；④ 前端类型生成链路 | trend 组关 `USE_MOCK` 可跑通：**FE → 网关 → display → element → ADS** 闭环 |
| **W2** | `element` 铺开 chain / service / policy；`talent` / `results` 组端点 | 三组页面从占位转实装 |
| **W3** | `gkxlumen-graph`（燕大）+ `gkxlumen-datacatalog`；久新通道填实现 | graph / data 组实装 |
| **W4** | 缓存 / 分区降级 / 异步收口；退役前端直连 `/innov`、`/situation` | 单入口达成，指标入 OTel |

**拆分触发条件**：

| 触发 | 动作 |
|---|---|
| 专题系统也要调久新 | `channel/jiuxin-*` 拆为 `gkxlumen-supplier-jiuxin`（判据③） |
| 某 domain 包膨胀 / 需独立发布 | 该包 → 独立模块 → 服务（C1 已预留边界） |
| 燕大/智谱/深势 被 ≥2 服务调用 | 对应通道独立成服务 |

---

## 14. 风险与开放问题

### 14.1 全局风险（本次调研发现）

| # | 风险 | 影响 | 建议 |
|---|---|---|---|
| **R1** | **现网 Java 读的是 `demo_gkxlumenx_ads`，配置中从未出现无 demo 前缀的 ADS 库**（`DEPLOY-LUMEN.md:42`、`configs/gkxlumen-topic-svc-biz-dev.yml:10`） | D12 违规是**系统性状态**，不止 `InnovSql` 一处 | ⚠️ **A5 已裁决 ≠ 提交方建议：暂不强制整改**。新建服务**先与现网一致（读 `demo_gkxlumenx_ads`，库名配置化）**，等正式库有数、专题侧切库时统一整改。**原则：不为改名先把联调切挂** → **本风险由「阻塞」降为「已知延后」** |
| **R2** | **前端类型全手写，无 OpenAPI 生成** | 契约三处漂移无法根治 | ✅ **A13 已裁决**：`openapi-typescript` 只生成类型、不接管请求层；W1 落地生成链路（§4.5） |
| **R3** | **`gkx_show_service` 仍为骨架**（`data_source:"none"`） | D15 展示侧门面不存在，依赖路径全不可达 | ✅ **A6 已裁决**：阶段一走 Java 直读 ADS，门面实装后按场景分流；**门面实装排期仍需定责任人** |
| **R4** | **两套图谱**：现网 Nebula `entan` vs 燕大 `gkx_local_1` | graph 组用哪套未定；目标 space 名与现网不一致 | ✅ **A8 已裁决：用我方自建图谱（现网 space `entan`）**；燕大 `gkx_local_1` **本期不切源、不并行**，后期统一迁移 → **风险关闭** |
| **R5** | **`app_user` 库未找到** | D4 收藏/标签/导出写库落点未定 | 🟡 **已查明**：`app_user` 是**平台自有表**（`gkxlumen-app-server` 的 MyBatis-Plus 实体 `AppUser`，版权属 gkxlumen），**非三方提供**；属 **App 端用户体系**，与 `upms sys_user`（管理后台）**并列两套**。**待决策展示系统用哪套** → **A9 / §10.9.1** |
| **R6** | **`data` 组供方未找到**（原华为云团队 2026-10-15 退出） | 4 页只能空态 | PM 重新寻源或转自采 |
| **R7** | **久新 42 个 API 一条未确认**（talent + results 共 9 页） | 通道清单无法确定 | ✅ **已落人**（2026-10-26）：**郭万迎（PM）对外催办，久新侧对接人优先找 李乐 / 任欢**；与主体键问题合并催办；答复前只出桩 |
| **R8** | **XXL-Job 模块存在但 Helm 未部署** | 异步任务状态修正能力现网可能不可用 | 确认部署计划 |

### 14.2 L3 已有风险（详见 L3 详细文档 §14）

| # | 风险 |
|---|---|
| **R9** | **久新主体键与库主键是否同一套**——未对齐则混合拼装产出错数据**且不报错**（最大技术风险） |
| **R10** | 直连久新库违反 D3/D7，需豁免登记 |

---

## 15. 待裁决项（请徐腾强签署）

| # | 议题 | 选项 | **建议** | 依据 |
|---|---|---|---|---|
| **A1** | L3 新建几个服务 | (a) 3 个（element/graph/datacatalog）(b) 2 个（data 暂缓）(c) 按组切 7 个 | ✅ **已裁决 = (a) 新建 3 个**（2026-10-25 徐腾强：「展示侧不复用专题侧」）；若 data 供方迟迟未定可先退 **(b)** | §7.2 · **§7.6 复用边界清单** · §7.7（偏离说明，已接受） |
| **A2** | 要素域服务命名 | 保持 `gkxlumen-situation` / 改 `gkxlumen-element` | ✅ **已确认改为 `gkxlumen-element`**（2026-10-25）：承载 24 页跨 5 组；`situation` 易被误解为只服务 trend 组；`element` 对齐基线 D1「七要素」既有术语 | §7.3 |
| **A3** | 直连久新库 D3/D7 豁免 | 准予并登记 / 不准 / 下沉 Python | ✅ **已裁决：准予过渡期直连久新只读库**（2026-10-26）。**两条实现路径均可，按实现方便选**：(a) **Java 侧直连**　(b) **下沉到展示侧 Python `gkx_show_service`**。**必须登记切换条件与隔离措施，避免永久旁路 ADS**。→ **已选 (b) 并于 2026-10-29 落地，切换条件与隔离措施见 §15.1** | D3 / D7；答复 A7 前 `channel/jiuxin-*` 仍出桩 |
| **A4** | 路径前缀与迁移顺序（吸收原 Q-DISP-04） | 一步到位 `/display/v1/**` / 先补 `/situation/**` 再迁 | ✅ **已裁决 = (a) 一步到位 `/display/v1/**`**（2026-10-26）。徐腾强：**「方便网关正确转发，不再先补 `/situation/**`」** | D5 / D15 |
| **A5** | **`demo_gkxlumenx_ads` 整改口径**（R1） | 统一切 `gkxlumenx_ads` / 沿用 demo | ⚠️ **已裁决 ≠ 提交方建议**（2026-10-26）：**暂不强制切正式 ADS**。现状——业务数据都在 `demo_*`、正式库基本没数、**专题侧也仍读 demo 尚未切库**。**新建展示服务先与现网一致（读 `demo_gkxlumenx_ads`，库名配置化）**，等正式库有数、专题侧切库时再统一整改。**原则：不为改名先把联调切挂**。→ **R1 由「阻塞」降为「已知延后」**，整改单改为**跟随专题侧切库节奏** | D12；R1；**与 §7.6 / 数据源配置强相关** |
| **A6** | 智树自建维度读法 | 先直读 ADS / 必须走 `gkx_show_service` | ✅ **已裁决 = 先直读 ADS**（2026-10-25）。**仅限门面实装前**；门面实装后按场景分流——纯查询 / 聚合 / 分页**继续直读 ADS**（D3），需算法加工**走门面**（D2，`policy` 组 `polan` 算法大概率走此路） | D3；`storage/README.md:89`；R3 |
| **A7** | 久新主体键对齐——**谁去问、何时答复** | 指定责任人 + 时限 | ✅ **责任人已落**（2026-10-26）：**郭万迎（PM）对外催办**；**久新侧对接人优先找 李乐 / 任欢**。答复前 `channel/jiuxin-*` **只出桩**，避免错键**静默错数** → R9 责任人栏已填实 | R9 |
| **A8** | 图谱用哪一套（R4） | 燕大 / 现网 Nebula / 统一 | ✅ **已裁决：现阶段继续用我方自建图谱（现网 space `entan`）**（2026-10-26）。燕大 `gkx_local_1` **本期不切源、不并行**，后期统一迁移 → **R4 关闭** | R4 |
| **A9** | `app_user` 库落点（R5） | 确认库名 / 新建 / 换用 `sys_user` | 🟡 **方案侧已答复，待你决策**（2026-10-26）：查证结果——`app_user` 是**平台自有表**（`gkxlumen-app-server` 的 MyBatis-Plus 实体 `AppUser`，版权属 gkxlumen），**非三方提供**；属 **App 端用户体系**，与 `upms` 的 `sys_user`（管理后台）**并列两套**；字段含 `phone` / `email` / `wx_openid`。**选项**：(a) 复用 `upms sys_user`（PC 常规）(b) 跨端共用 `app_user` (c) 展示侧自建 `display_user_*`。**建议 (a)**，除非 PC 与 App 确为同一用户池 → **详见 §10.9.1** | D4；R5；影响 A15 订阅写库 |
| **A10** | `gkxlumen-display` 由「薄 BFF」升为「聚合 BFF」的角色强化会签（原 Q-DISP-01） | 通过 / 不通过 | ✅ **已裁决：通过**（2026-10-26）。徐腾强确认「**`gkxlumen-display` 一开始就是按聚合服务定义的**」，按聚合 BFF 实装即可：**页面聚合 / 读缓存 / 分区降级 / 就绪度注入**。**不新增服务** | §1.6 / §6 |
| **A11** | 预聚合读模型的**表清单与刷新频率**（原 Q-DISP-02） | 需与 Python ETL 对齐 | 🟡 **口径已澄清，待数据侧出清单**（2026-10-26）：澄清「预聚合读模型」= **ADS 层预跑物化表**（§9.5，按 `dimHash` 联合主键），**不是 Redis 页面缓存**（后者属 **A12 / §6.7 分档**，徐腾强口径「缓存 12h 过夜失效即可」在此适用）。**交付物**：① 预跑读表清单（源表 / 指标 / 维度组合）② 刷新频率 → **已对齐 T+1 凌晨跑批**（与指标侧最快频率一致）。清单由 **数据 Lead + 算法唐绍祖** 出一版 | §9.5；依赖指标侧 T+1 |
| **A12** | 缓存 TTL 与失效策略分档（原 Q-DISP-03） | 按页热度分档 | ✅ **已裁决：采纳 §6.7 分档表**（2026-10-25）——实时监控 10–30s / 地图 5–10min / 统计 10min / 详情 5min / 导出配置 30min。**属可调参数，上线后按需微调** | 架构 + 运维 |
| **A13** | 契约生成工具链选型（原 Q-DISP-05） | `openapi-typescript` / `orval` / 其他 | ✅ **已裁决 = `openapi-typescript`**（2026-10-25）：**只生成类型**、零运行时依赖，**不接管请求层**（保留 `request.ts` 的 traceparent 等定制逻辑） | 前端 + 架构 |
| **A14** | **秒开预跑的组合规模**（§9.5） | (a) 全组合笛卡尔积预跑 (b) **分级预跑**（高频全跑 + 长尾按需） (c) 维度降维 | ✅ **已裁决 = (b) 分级预跑**（2026-10-25）。**本次仅定策略**；地域 / 学科 / 要素的**具体枚举量级待产品定义，开发时再落地** | 徐腾强 2026-10-20 秒开决策；100×100×11 = **11 万组合**，全量预跑代价高 |
| **A15** | **订阅模块归属**（§10.9） | (a) 复用 `topic-async-service` + 展示侧订阅关系 (b) 展示侧自建 (c) 落 `element` 内 | ✅ **已裁决 = (a)**（2026-10-25）：订阅**只复用异步执行能力**，订阅关系与触发规则落展示侧，不落专题库 | 依赖 A9（`app_user` 落点）与 R8（XXL-Job 未部署） |

> **编号说明**：本文 A 系列已吸收原 `architecture-display-optimized.md` 的 Q-DISP-01~09（Q-DISP-04 并入 A4，06→A1，07→A3，08→A7，09→§6.1 已修正并落地），**不再保留双编号**。

---

### 15.1 A3 落地登记：久新库只读直连链路

A3 裁决要求「**必须登记切换条件与隔离措施，避免永久旁路 ADS**」。本条为该要求的正式登记。

**落地日期**：2026-10-29　**实现路径**：**(b) 下沉展示侧 Python `gkx_show_service`**

**未选 (a) Java 直连的原因**：`gkx_show_service` 在 D15 中已被定为展示系统专属 Python 门面；
若 Java 直连，将与「展示 BFF 不直连外部库」的分层不一致，且与专题侧
（`SYSINT-DICT-02-L01` 已定 Java 只转发、不直连）口径相左。

#### 链路

```
展示系统 Java（gkxlumen-innov）
  └─ RemoteShowPythonClient   @FeignClient("gkxlumen-platform-show-py")
       └─ POST /internal/gkx-show/gba/indicator/*
            └─ gkx_show_service   FastAPI :8082，前缀 /internal/gkx-show/**
                 └─ gkx_show_service/jiuxin.py   久新只读通道（唯一出口）
                      └─ 久新 Doris  47.93.119.170:29030 / gkx_technology_analysis_dev
```

Java 侧**不直连久新、不使用只读账号**；久新凭据仅存在于 Python 侧环境变量。

#### 隔离措施（A3 要求项之一）

| # | 措施 | 落点 |
|---|---|---|
| 1 | 收敛单一通道 | 久新访问只走 `gkx_show_service/jiuxin.py`；禁止在 `views/` 内散写 SQL 或自建连接 |
| 2 | 只读 | SQL 白名单仅放行单条 `SELECT`，拦截 `INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/TRUNCATE/REPLACE/GRANT` 及多语句 |
| 3 | 配置可切 | 总开关 `GKX_JIUXIN_ENABLED`；置 `0` 即整体停用并回落空态，**不旁路到其他库** |
| 4 | 凭据不进 git | `GKX_JIUXIN_PASSWORD` 只走 K8s Secret / 环境变量；`.env.example` 该行保持注释且为空 |

#### 切换条件（A3 要求项之二）

> **切换条件：数据工厂（GDF）`ts_*` 表就绪后，改读 ADS，本链路停用。**

判据与步骤：

1. GDF 完成久新源入湖，产出 `ts_*` 结果表并落 ADS；
2. ADS 中对应指标有数据且通过口径比对；
3. 将 `GKX_JIUXIN_ENABLED` 置 `0`，本链路整体停用；
4. 接口路径保持不变、改为读 ADS，**对上游 Java 无感**。

**未满足前本链路保持启用**。避免「永久旁路 ADS」的责任人为本切换条件的 Owner
（待指定；建议落数据 Lead，与 A11 预跑读表清单同一责任人）。

#### 落地证据（2026-10-29 实测）

| 检查项 | 结果 |
|---|---|
| `/healthz` | `jiuxin_readonly_channel: "up"` |
| `/gba/indicator/capability` | `reachable: true`；命中湾区城市 7 个 |
| `/gba/indicator/paper` | 真实数据，例：广州 2024=`31788`、2025=`44556` |
| 只读防护 | `DROP TABLE` / `SELECT 1; DELETE` 均被拦截 |

#### 已知限制

**专利授权量口径不可靠，禁止对外出数。** 按「专利 → 机构 → 城市」关联实测，
2024 年深圳仅得 1 条、广州/东莞 0 条，而算法库既有产出为「广州 2024 授权 99,136」，
相差 4 个数量级——机构关联覆盖率极低。接口固定返回 `quality="unreliable"`，
调用方不得作为指标真值展示；出数前须先确定城市级授权口径。

**工程侧记录**：`lumen-topic-py` 仓 `docs/JIUXIN-LINK.md`。

---

## 16. 附录：关键证据索引

| # | 文件 | 关键位置 |
|---|---|---|
| 1 | `lumen-ui-science-pc/src/router/menu.ts` | `:38-122` 七组 35 页；`:126-132` 六类角色 |
| 2 | `lumen-ui-science-pc/package.json` | `:8-11` Vite7；无 OpenAPI 生成工具（R2） |
| 3 | `lumen-ui-science-pc/src/utils/request.ts` | `:69-71` traceparent |
| 4 | `lumen-ui-science-pc/src/config/app.ts` | `:9-12` USE_MOCK |
| 5 | `lumen-svc-platform/db/9x_gkxlumenx_sys_route_conf_topic_chain.sql` | 路由格式；**禁止再配 StripPrefix** |
| 6 | `lumen-svc-platform/gkxlumen-display/src/main/resources/application.yml` | `:2` 7099；`:20-26` 职责边界 |
| 7 | `.../display/service/DomainHealthAggregator.java` | 并行 + 分区降级范式 |
| 8 | `lumen-svc-platform/gkxlumen-innov/src/main/resources/application.yml` | `:19-27` ADS + read-only |
| 9 | `lumen-svc-platform/gkxlumen-cms/.../SourceDataSourceConfig.java` | `:29-49 @Primary`；`:51-75` 只读源 + `@Qualifier` |
| 10 | `helm/gkxlumen-platform/values.yaml` | 端口占用；**7082–7084 空闲**；存储地址 |
| 11 | `helm/.../configs/gkxlumen-display-dev.yml` | `:19-21` 缓存默认关闭 TTL 300s |
| 12 | `helm/.../templates/_helpers.tpl` | `:134-135` OTel JavaAgent 2.19.0 |
| 13 | `lumen-topic-py/gkx_show_service/main.py` | `:71-94` 骨架；`data_source:"none"`（R3） |
| 14 | `lumen-topic-py/CODEOWNERS` | `:7,11` 门面隔离边界 |
| 15 | `gkx-orchestration/.../storage/README.md` | `:85-93` 存储角色；`:89` ADS「Java 只读」 |
| 16 | `gkx-orchestration/agent-delivery/architecture-baseline.md` | D1–D15 · §2.2 · §4 |
| 17 | `agent-handoffs/科技发展态势-TS/ARCH-TS-L3-DESIGN-01.md` | L3 详细设计（§7.3 下钻） |
| 18 | `agent-handoffs/展示系统三要素集成-SCI-INT/技术方案.md` | `:32-37,160-189` 各组供方与形态 |

---

**签署栏**

| 角色 | 姓名 | 裁决（A1–A9） | 日期 |
|---|---|---|---|
| 架构师 | 徐腾强 @qike366.com | | |
| 契约监管 | 李伟 | | |
| 前端 | 孔东（A4 / R2） | | |
| 算法·门面 | 堂绍祖（A6 / R3） | | |
| 数据 Lead | （R1 / R4 / R5） | | |
| PM | 郭万迎（R6 / R7 外部催办） | | |
