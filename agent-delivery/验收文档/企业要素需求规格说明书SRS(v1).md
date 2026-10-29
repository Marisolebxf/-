# 企业要素 需求规格说明书（SRS）

| 属性 | 内容 |
|------|------|
| 文档名称 | 企业要素（ENT）需求规格说明书（SRS） |
| 版本 / 日期 / 作者 | **V1.0 / 2026-06-18 / [agent:doc-agent] + [human:待PM终审]** |
| 文档状态 | Markdown 初稿（待 PM 终审；本期不转 docx） |
| 文档风格 | IEEE 830 风格（软件需求规格说明） |
| 适用系统 | 科技专题服务系统 · 战略分析 + 智慧服务门户 · 集群服务（企业要素 ENT 子模块） |
| 支撑基线 | `ENT-functional-design-v2.md`（v2.1.0，18 个验收点 E-20~E-37） |
| 运行环境 | React + Vite + Arco Design 前端（D8） / Java REST（只读 ADS） / Python `/internal/*`（算法、图谱） |

---

## 文档目的

本文档是 **企业要素（ENT）** 的需求规格说明书，按 IEEE 830 风格系统定义企业要素全链路的功能需求、非功能需求、外部接口需求与需求-验收追溯关系，作为后续概要设计（HLD）、详细设计、开发与甲方验收的需求基线。

> **内容来源声明**：本说明书为"格式参考、内容发挥"产物。版式对齐 IEEE 830 与正式件章节体系；**全部需求条目、术语口径、页面与指标内容严格来自下列内容真源**，doc-agent 不自创需求、不扩大范围、不替甲方判定业务口径。凡涉及"完成度 / 验收通过 / 满足全部验收"等结论性措辞均回避，留待 PM 终审；业务口径未定项统一标注"待甲方确认"。

## 读者对象

| 读者 | 关注章节 |
|------|---------|
| PM / 架构师（评审/拍板方） | §2 总体描述、§6 其他需求（开放项）、§7 追溯矩阵 |
| 业务分析师 / 招商专员（最终用户代表） | §3 功能需求、§4 非功能需求 |
| ui-agent / frontend（实现方） | §3 功能需求、§4 非功能需求、§5 外部接口需求 |
| api-agent / algorithm-agent / data-agent（承接方） | §3 处理逻辑、§5 软件/数据接口、§6 开放项 |
| qa-agent（验收方） | §3 验收点溯源、§7 需求-验收追溯矩阵 |

## 关联文档清单（内容真源）

| # | 文档 | 路径 | 在本 SRS 中的角色 |
|---|------|------|------------------|
| 1 | 企业要素功能设计说明书（FDS） | `demo-ui-topic/docs/ia/enterprise/ENT-functional-design-v2.md`（v2.1.0） | **主输入**：三层架构、18 功能点 WBS、UX 铁律、非功能需求、验收矩阵 |
| 2 | 企业要素信息架构（IA） | `demo-ui-topic/docs/ia/enterprise/ENT-IA.md` | 站点地图、页面清单、路由 |
| 3 | 企业要素用户旅程（User Flow） | `demo-ui-topic/docs/ia/enterprise/ENT-userflow.md` | 用户角色、主/异常路径、13 个埋点 |
| 4 | 企业分析低保真线框（Wireframe） | `demo-ui-topic/docs/ia/enterprise/ENT-wireframe.md` | 字段表（6 列）、49 个 metric_id |
| 5 | 验收点细则 | `agent-delivery/acceptance-catalog/catalog-topic-enterprise.yaml` | E-20~E-37 范围描述与逐条溯源 |
| 6 | 企业域数据库设计（v1） | `agent-delivery/data/企业域数据库设计(v1).md` | 数据接口（只读 ADS）、metric 来源 |
| 7 | 团队 AI 公约 / 架构基线 | `agent-delivery/architecture-baseline.md`、`.cursor/rules/00-team-constitution.mdc` | 约束（架构铁律 D1~D9） |
| 8 | 数据血缘规约（D9） | `agent-delivery/data-lineage-policy.md` | 指标 8 件套、口径透明要求 |

---

## 目录

1. [引言](#1-引言)
2. [总体描述](#2-总体描述)
3. [功能需求](#3-功能需求)
4. [非功能需求](#4-非功能需求)
5. [外部接口需求](#5-外部接口需求)
6. [其他需求](#6-其他需求)
7. [需求-验收追溯矩阵](#7-需求-验收追溯矩阵)

---

## 1. 引言

### 1.1 编写目的

本 SRS 定义企业要素（ENT）从门户展示到专题战略研判、再到内容运营的全链路软件需求，供设计、开发、测试与验收各方作为统一需求基线引用。文中"功能需求"逐条对应功能设计 v2.1 的 18 个验收点（E-20~E-37），并回链验收细则 `catalog-topic-enterprise.yaml`。

### 1.2 范围

企业要素全链路 = **三层**（FDS §1.4 / §6）：

- **Layer A · 门户集群服务 · 企业发展**（展示层，E-31~E-35）：A0 企业发展首页 / A1 企业整体概况 / A2 重点企业全景图 / A3 明星企业介绍 / A4 深圳企业介绍 / A5 一张图·企业图层。
- **Layer B · 专题战略分析 · 企业分析**（研判层，E-20~E-30）：P0 企业分析概述 / P1 重点企业类型分析 / P2 重点企业领域分布 / P3 能力评估（技术力 E-23 / 商业力 E-24）/ P5 深圳企业现状分析 / P6 引育推荐（招引 E-26 / 培育 E-27）/ P8 供应链关系 / P9 发展痛难点 / P10 企业竞争力。
- **Layer C · 内容运营后台**（E-36 可视化展示内容管理 / E-37 门户企业发展内容管理）。

**范围边界**（FDS §5）：门户壳层、登录、导航、基础服务（智能搜索/推荐/阅读）由门户厂商负责，不在本范围；我方实现企业要素业务能力、页面、API、算法，供门户以 iframe / Deep Link / REST 调用。集群服务其余菜单仅在涉及企业指标时供数，不建页。

> **范围铁律**（FDS §1.3）：Layer B 战略分析 10 个三级叶子功能（E-21~E-30）不增不减（±10%）；Layer A/B 分责验收、数据同源。

### 1.3 读者与本文档使用方式

本文档读者见首页"读者对象"。功能需求章节（§3）按页面/验收点组织，每条采用统一结构（输入 / 处理 / 输出 / 优先级 / 验收点溯源）；§7 提供 FR ↔ E-XX ↔ 页面 ↔ metric_id 的双向追溯。

### 1.4 术语定义

| 术语 | 定义（口径与 bid / FDS v2.1 一致） |
|------|----------------------------------|
| 企业类型 | 外企 / 高企（高新技术企业）/ 小微（科技型中小）/ 上市等分类（精确判定规则待甲方确认，Q010） |
| 明星企业 | 行业内龙头企业，展示产品功能全景、技术优势、团队实力、产业生态图谱（E-34；入选规则由运营配置，Q020） |
| 重点企业 | 按专利数、技术交易额等阈值筛选的重点企业（E-33 / catalog E-03） |
| 技术力 | 围绕技术人才储备、技术创新成果、技术转化效率、技术合作网络、研发投入强度等设计的企业技术力指数（E-23 / catalog E-16） |
| 商业力 | 围绕市场规模、产品竞争力、品牌影响力、技术合作程度、产业链覆盖率、关键环节参与度等设计的企业商业力指数（E-24 / catalog E-17） |
| 综合竞争力 | 整合技术力、商业力等维度的综合竞争力评估（E-30；P10 为唯一入口，DC3） |
| 招引（推荐） | 从全国范围智能筛选高成长性、关键技术型企业的招商引资推荐（E-26 / catalog E-18） |
| 培育（推荐） | 聚焦深圳本地、识别有潜力但面临瓶颈的优质企业的梯度培育推荐（E-27 / catalog E-19） |
| 供应链关系 | 企业上下游供应链网络结构、关键节点识别与断链风险（E-28 / catalog E-15、E-28） |
| 痛难点 | 企业在技术、市场、融资、管理等维度的瓶颈与痛点诊断（E-29 / catalog E-14、E-29） |
| 产业链定位 | 企业在产业链中的环节角色（上游 / 中游 / 下游、链主等） |
| JudgmentStrip | 研判摘要条：每页顶部"关注什么→为什么→建议下一步"（UX-01） |
| CompareBasket（对比篮） | 跨页保留的企业对比集合（≤10 家），承载对象联动（FDS §7.2） |
| ContextBar | 全局上下文栏（产业 / 时间窗 / 区域 / 企业类型 / 对比篮） |
| metric_id | 统计指标的全局唯一编码，前缀 `M_ENT_*`（D9 八件套元数据的主键） |
| Deep Link（深链） | Layer A → Layer B 携带上下文参数的跳转 |
| embed 模式 | 门户以 iframe 嵌入 Layer A 的运行模式（隐藏侧栏、产业上下文只读） |
| ADS | 应用结果层（`ads.ent_*`），Java 只读契约面 |
| Mock 阶段（Wave 0/试点） | 数据以 Mock 填充阶段，统计数字旁须有 🧪 标识 |

### 1.5 缩写

ENT=企业要素；FDS=功能设计说明书；HLD=概要设计说明书；IA=信息架构；ADS=应用结果层；DWD=标准明细层；CMS=内容管理系统；GIS=地理信息可视化；NF=非功能需求；FR=功能需求。

---

## 2. 总体描述

### 2.1 产品视角

企业要素是 **科技专题服务系统**「战略分析 · 企业分析」与 **智慧服务门户**「集群服务 · 企业发展」的企业切片实现，是更大平台的子模块（FDS §1.1 / §5）。它复用平台共享聚合核心（展示与专题两前端共享 Java 聚合层），不独立成系统。

产品一句话定位（FDS §1.2）：**同一套企业数据，两种使用深度**——门户 Layer A 让人"3 分钟看懂产业"，专题 Layer B 让人"15 分钟产出决策"，二者深链互通、数据同源、不重复造数、不混在同一页。

### 2.2 三层定位（A / B / C）

| 层 | 定位 | 用户心智 | 主要出口 |
|----|------|---------|---------|
| Layer A 门户展示 | 浏览、感知产业企业态势 | "这个产业企业怎么样？" | 深链 Layer B / 企业详情 |
| Layer B 专题研判 | 配置、对比、诊断、导出 | "我该招谁、培谁、怎么帮？" | PDF / 名单 / 汇报截图 |
| Layer C 内容运营 | 维护展示内容与配置 | "维护明星企业、展示区块" | 驱动 Layer A 渲染 |

### 2.3 用户类型与特征

来源 FDS §4.1 / User Flow：

| 角色 | 主要 Layer | 核心诉求 |
|------|-----------|---------|
| 产业浏览者 / 访客 | A | 快速了解某产业有多少企业、龙头是谁 |
| 领导 / 决策者 | A → B | 5 分钟掌握态势，必要时下钻招引名单 |
| 业务分析师 | B | 筛选 → 对比 → 诊断 → 导出，链路一气呵成 |
| 招商 / 育商专员 | B（P6） | 拿名单、看依据、对接一企一策 |
| 内容运营 | C | 维护明星企业介绍、全景图标注、深圳介绍文案 |

### 2.4 运行环境

| 维度 | 要求（架构铁律 / D8） |
|------|----------------------|
| 前端 | React + Vite + **Arco Design**（`@arco-design/web-react`）+ ECharts + AntV G6 + Leaflet + dayjs；主色 `#165DFF`、页面底色 `#D8E7FC`（D8） |
| 应用服务 | Java REST，**只读 ADS**；不写算法、不直连 nGQL |
| 算法服务 | Python `/internal/*`（NLP、图谱、模型推理） |
| 图谱 | NebulaGraph（`10.50.75.136:9669`），space `gkx_enterprise`；**禁 Neo4j** |
| 数据 | 标准表 ADS 先行 + Mock 数据填充；三方源到位后由数据工厂做映射 |
| 部署 | K8s dev（CI 触发 rollout） |

### 2.5 设计约束（架构铁律）

| 约束 | 内容 |
|------|------|
| C-01 | 算法仅在 Python；Java 禁止 NLP / 图谱算法 / 模型推理 |
| C-02 | 调用链：前端 → Java REST → Python `/internal/*`，不可越层 |
| C-03 | 图谱使用 NebulaGraph，禁止 Neo4j |
| C-04 | 可观测性：Java Agent + Python instrument + 前端 `observability.ts`（埋点必加） |
| C-05 | 前端规范唯一来源 D8（Arco 栈、token、组件、配色） |
| C-06 | 数据血缘 D9：界面每个统计指标须有"8 件套"元数据，统计数字旁有 ⓘ；Mock 阶段有 🧪 |
| C-07 | Java 只读 ADS；数据策略 ADS 先行 + Mock 填充 |
| C-08 | 业务口径决策只能甲方拍板，歧义项登记开放项并标 ⚠️"待甲方确认" |

### 2.6 假设与依赖

| # | 假设 / 依赖 | 影响 |
|---|------------|------|
| AD-01 | 门户厂商提供登录、SSO、壳层与基础服务，并支持 iframe / 深链集成 | Layer A embed 集成（Q021 门户 embed SSO 待确认） |
| AD-02 | 三方"要素库"（186 张 `dwd_*` 贴源表）按映射报告口径可用 | DWD/ADS 数据填充 |
| AD-03 | algorithm-agent 落地 🔧 算法字段（30 条 metric 对应模型），Python `/internal/*` 提供推理 | 能力/竞争力/供应链/痛难点/引育等算法类需求 |
| AD-04 | data-agent 提供 ADS 13 表 + cfg_metric 49 条注册，Mock 数据按 `mock_*` 批次填充 | 全部统计指标供数与血缘 |
| AD-05 | 市场份额 / 品牌声量 / 客户集中度等无来源字段需额外采购（K-O7） | 商业力 / 竞争力部分指标暂置空 |
| AD-06 | 业务口径开放项（Q010~Q020 等）由甲方拍板前按团队临时默认值试运行 | 多处统计口径标 ⚠️ |

---

## 3. 功能需求

> 说明：本章每条功能需求（FR-NN）对应功能设计 v2.1 的一个验收点（E-XX）。优先级取自 FDS §17.1 与验收矩阵 §16（P0=最高，依次 P1/P2）。"验收点溯源"列回链 `catalog-topic-enterprise.yaml` 的范围描述。统计指标的口径、来源与血缘见数据库设计（v1）与 wireframe 字段表，本章不重复全量字段。

### 3.0 功能需求总览

| FR | 名称 | 对应 E | 层 | 路由 | 优先级 |
|----|------|--------|----|------|--------|
| FR-01 | 企业发展首页 | E-31 | A | `/cluster/enterprise` | P0 |
| FR-02 | 企业整体概况 | E-32 | A | `/cluster/enterprise/general` | P0 |
| FR-03 | 重点企业全景图 | E-33 | A | `/cluster/enterprise/panorama` | P1 |
| FR-04 | 明星企业介绍 | E-34 | A | `/cluster/enterprise/star`(`/:code`) | P1 |
| FR-05 | 深圳企业介绍 | E-35 | A | `/cluster/enterprise/shenzhen` | P1 |
| FR-06 | 企业分析概述（战略驾驶舱） | E-20 | B | `/enterprise/overview` | P0 |
| FR-07 | 重点企业类型分析 | E-21 | B | `/enterprise/type-distribution` | P0 |
| FR-08 | 重点企业领域分布分析 | E-22 | B | `/enterprise/domain-distribution` | P1 |
| FR-09 | 技术力评估对比 | E-23 | B | `/enterprise/capability`（技术力 Tab） | P1 |
| FR-10 | 商业力评估对比 | E-24 | B | `/enterprise/capability`（商业力 Tab） | P1 |
| FR-11 | 深圳企业现状分析 | E-25 | B | `/enterprise/status-analysis` | P1 |
| FR-12 | 招引企业推荐 | E-26 | B | `/enterprise/recommendation`（招引 Tab） | P1 |
| FR-13 | 培育企业推荐 | E-27 | B | `/enterprise/recommendation`（培育 Tab） | P1 |
| FR-14 | 企业供应链关系分析 | E-28 | B | `/enterprise/supply-chain` | P1 |
| FR-15 | 企业发展痛难点分析 | E-29 | B | `/enterprise/pain-points` | P1 |
| FR-16 | 企业竞争力分析 | E-30 | B | `/enterprise/competitiveness` | P1 |
| FR-17 | 可视化展示内容管理 | E-36 | C | 后台 | P2 |
| FR-18 | 门户企业发展内容管理 | E-37 | C | 后台 | P2 |

> 补充：A5 一张图·企业图层（`/cluster/map/enterprise`）为门户一张图企业切片供数与图层（FDS §9.6），非独立验收点，归入 Layer A 范围；本 SRS 在 FR-01 备注中体现，不单列 FR。

---

### 3.1 Layer A · 门户集群服务（FR-01 ~ FR-05）

#### FR-01 企业发展首页（E-31）

| 项 | 内容 |
|----|------|
| 输入 | 当前产业上下文（`industry`，门户可只读传入）；用户从门户菜单进入 |
| 处理 | 加载企业发展首页：产业摘要（来自 CMS / 模板）；汇总 4 张关键指标卡（企业总数、重点企占比、深圳企业数、明星企业数）；渲染四宫格入口（概况 / 全景 / 明星 / 深圳）与"进入战略分析 → P0"入口 |
| 输出 | 首页含 4 张 MetricCard（点击下钻对应子页）+ 四宫格入口 + 进入战略分析 ActionBar；A5 一张图企业图层入口（供数+图层） |
| 优先级 | P0 |
| 验收点溯源 | catalog E-31：企业发展作为快速入口核心，含企业整体概况、重点企业全景图、明星企业介绍、深圳企业介绍 |

#### FR-02 企业整体概况（E-32）

| 项 | 内容 |
|----|------|
| 输入 | 产业上下文；时间窗 |
| 处理 | 统计分析行业内企业：总体数量及历年发展趋势、全球/全国分布、科研/从业人数；地图按区域聚合 |
| 输出 | 企业总数 + 历年新增趋势（折线）、企业分布（地图 + 图表）、科研人数指标；顶部展示型 JudgmentStrip（1 个"深度分析 → P0"链接）；地图点击省份深链 P1 并带 `region` |
| 关键指标 | `M_ENT_TOTAL_COUNT`、`M_ENT_NEW_COUNT_Y`、`M_ENT_REGIONAL_COUNT`、科研人数（⚠️ Q019 口径待确认） |
| 约束 | 禁止权重配置、招引名单、痛难点诊断（仅展示，深度能力深链 Layer B）；与 P0 数据同源（DC4） |
| 优先级 | P0 |
| 验收点溯源 | catalog E-32：展示总体数量、历年发展趋势、全球/全国分布及科研人数 |

#### FR-03 重点企业全景图（E-33）

| 项 | 内容 |
|----|------|
| 输入 | 产业上下文；产业链节点选择 |
| 处理 | 按产业分类展示全产业链重点企业及基础信息；提供重点企业规模统计（类型×国省市）与领域统计（关键词→链） |
| 输出 | 产业链重点企业全景（链树 + DataCard，点击企业 → DetailDrawer）、规模统计（地图 + 图表，深链 P1）、领域统计（热力/桑基，深链 P2）；顶部结论先行一句 |
| 优先级 | P1 |
| 验收点溯源 | catalog E-33：展示全产业链重点企业及基础信息，提供规模统计与领域统计 |

#### FR-04 明星企业介绍（E-34）

| 项 | 内容 |
|----|------|
| 输入 | 产业 / 标签筛选（列表页）；`enterprise_code`（详情页） |
| 处理 | 对行业龙头明星企业重点介绍；明星名单由运营配置（Q020），非全量算法 TopN；详情整合 CMS 内容与 ADS 指标 |
| 输出 | 列表页（卡片网格 + 筛选）；详情页四模块：产品功能全景图、技术优势可视化、团队实力展示、产业生态图谱（只读 GraphCanvas）；底部"供应链分析 → P8""竞争力 → P10"深链 |
| 优先级 | P1 |
| 验收点溯源 | catalog E-34：展示产品功能全景图、技术优势可视化、团队实力多维展示、产业生态图谱 |

#### FR-05 深圳企业介绍（E-35）

| 项 | 内容 |
|----|------|
| 输入 | 产业上下文 |
| 处理 | 在统一企业评价框架内对深圳企业分析统计：数量及趋势、领域分布、规模分布、深圳重点企业 |
| 输出 | 深圳企业数量+趋势、领域分布（链树+图表）、规模分布（饼/柱）、重点企业表（DetailDrawer）；顶部结论先行一句；页底"多城市对标分析 → P5"CTA（展示 vs 研判分流点） |
| 关键指标 | `M_ENT_SZ_COUNT` 等（与 P5 同源） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-35：展示深圳企业数量、领域分布、规模分布和深圳重点企业 |

---

### 3.2 Layer B · 专题战略分析（FR-06 ~ FR-16）

> Layer B 各页统一遵守页面骨架（FDS §8）：ContextBar（全局上下文 + 对比篮）+ JudgmentStrip + MetricCard + 筛选 + 主可视化 + 研判面板 + 明细表 + DetailDrawer。全局筛选与对比篮跨页保留（NF-05），切换产业二次确认清空对比篮。

#### FR-06 企业分析概述 / 战略驾驶舱（E-20）

| 项 | 内容 |
|----|------|
| 输入 | 目标产业 + 时间窗（SearchableCascadeFilter） |
| 处理 | 计算本产业企业生态总体态势（总数、创新型占比、新增趋势、研发投入、专利、高企）；生成 JudgmentStrip 研判摘要（关注/原因/建议动作）；TopN 区域与重点企业 |
| 输出 | JudgmentStrip + 5 张 MetricCard（带 ⓘ / 🧪）+ 历年新增趋势 + 全国分布热力 + 重点企业 TopN + 关键结论与下钻入口（EvidenceList）；KPI 可下钻、地图点击 → P1、TopN → 对比篮 |
| 关键指标 | `M_ENT_TOTAL_COUNT`、`M_ENT_INNOVATIVE_COUNT`（⚠️ Q011）、`M_ENT_NEW_COUNT_Y`、`M_ENT_AVG_RD_INVESTMENT`、`M_ENT_PATENT_TOTAL`、`M_ENT_HIGH_TECH_COUNT`（⚠️ Q010） |
| 约束 | **不含** E-31~E-35 内容（明星/深圳/科研 Tab 迁出 Layer A，DC2/DC3）；与 A1 同产业下 `M_ENT_TOTAL_COUNT` 一致（X-01） |
| 优先级 | P0 |
| 验收点溯源 | catalog E-20：构建从宏观企业生态到微观个体画像的穿透式洞察体系 |

#### FR-07 重点企业类型分析（E-21）

| 项 | 内容 |
|----|------|
| 输入 | 产业级联 + 企业类型多选（外企/高企/小微/上市）+ 地理层级（国/省/市） |
| 处理 | 按"产业—类型—区域"三维框架，在国家、省、市三级地理维度下钻分析分布特征；计算类型数量/占比、区域企业数/密度、集聚指数 |
| 输出 | 4 张 MetricCard（匹配总数/外企占比/高企占比/上市占比）、三级地理下钻地图（气泡/分级填色，含数量/占比/集聚指数研判 Tab）、企业类型结构堆叠柱、区域企业清单表（可导出）；地图、类型、柱图、表格四方联动 |
| 关键指标 | `M_ENT_TYPE_MATCH_COUNT`、`M_ENT_TYPE_COUNT`（⚠️ Q010）、`M_ENT_TYPE_RATIO`、`M_ENT_REGIONAL_COUNT`、`M_ENT_REGIONAL_DENSITY`、`M_ENT_AGGLOMERATION_INDEX` |
| 约束 | GIS 三级下钻为复杂交互（Leaflet 行政区划下钻），不简化为静态图（DC5）；空态给"清除类型/扩大区域"快捷按钮（EX-01） |
| 优先级 | P0 |
| 验收点溯源 | catalog E-21：按产业与企业类型筛选，国/省/市三级地理下钻 |

#### FR-08 重点企业领域分布分析（E-22）

| 项 | 内容 |
|----|------|
| 输入 | 一家或多家重点企业（单/多选）+ 领域映射口径 + 时间窗 |
| 处理 | 自动解析企业业务范围、产品线与技术标签并映射至具体产业领域，计算覆盖广度与深度、多元化指数 |
| 输出 | 3 张 MetricCard（覆盖领域数/多元化指数/核心领域深度）、企业×领域覆盖矩阵（热力）+ 跨领域分布图谱（桑基/树）、领域覆盖明细表、企业领域详情抽屉（业务/产品/技术标签 → 领域映射证据） |
| 关键指标 | `M_ENT_DOMAIN_COVERAGE_COUNT`、`M_ENT_DOMAIN_COVERAGE_BREADTH`、`M_ENT_DOMAIN_COVERAGE_DEPTH`、`M_ENT_DIVERSIFICATION_INDEX` |
| 优先级 | P1 |
| 验收点溯源 | catalog E-22：解析业务/产品/技术标签映射产业领域，计算覆盖广度与深度 |

#### FR-09 技术力评估对比（E-23）

| 项 | 内容 |
|----|------|
| 输入 | 目标产业 + 对比企业（多选 ≥2）+ 技术力指标勾选与权重配置 |
| 处理 | 内置多维技术力评估模型（技术人才储备/创新成果/转化效率/合作网络/研发投入强度等），支持自定义指标与权重，多企业横向对比；权重合计必须=100% 才能生成评估 |
| 输出 | 技术力雷达图（多企业多维）、综合评分排名（条形）、详细数据对比表（综合评分/关键指标/等级 StatusTag）、差距分析报告（EvidenceList，自然语言） |
| 关键指标 | `M_ENT_TECH_POWER_SCORE`、`M_ENT_TECH_RANK`、`M_ENT_PATENT_GRANT_COUNT`、`M_ENT_RD_INVESTMENT_RATIO` 等 |
| 约束 | 权重≠100% 或对比企业<2 时"生成评估"禁用并提示（EX-02/EX-03）；技术力 Tab 与商业力 Tab 独立权重、切换不丢配置；指标库与默认权重待甲方确认（Q014） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-23：多维技术力评估模型，自定义指标与权重，输出雷达图、排名表、差距分析报告 |

#### FR-10 商业力评估对比（E-24）

| 项 | 内容 |
|----|------|
| 输入 | 目标产业 + 对比企业（多选 ≥2）+ 商业力指标与权重（独立于技术力 Tab） |
| 处理 | 基于市场份额、营收增长、盈利能力等指标构建商业力模型，支持自定义评价维度并进行企业间横向对比 |
| 输出 | 商业力雷达图、综合评分排名、营收增长趋势折线、详细数据对比表 |
| 关键指标 | `M_ENT_BUSINESS_POWER_SCORE`、`M_ENT_REVENUE_LATEST`、`M_ENT_REVENUE_GROWTH_RATE`、`M_ENT_PROFIT_MARGIN`、`M_ENT_MARKET_SHARE`（❌ 无来源，K-O7） |
| 约束 | 同 FR-09 权重校验；市场份额等无数据源字段暂置空并标注 |
| 优先级 | P1 |
| 验收点溯源 | catalog E-24：基于市场份额、营收增长、盈利能力构建商业力模型，自定义维度横向对比 |

#### FR-11 深圳企业现状分析（E-25）

| 项 | 内容 |
|----|------|
| 输入 | 产业链 + 环节 + 对标城市多选 |
| 处理 | 聚焦深圳本地企业，按产业链/环节自动筛选相关企业，与全国及其他重点城市多维对标，评估深圳企业在产业链中的位置、竞争力水平及生态完整性 |
| 输出 | 4 张 MetricCard（深圳企业数/平均技术力/企业密度/产业链完整度）、深圳vs对标城市雷达 + 产业链环节对比柱、深圳企业产业链定位（链中角色标注）、深圳相关企业清单表；含产业链定位 / 多城市对标两个工作台 Tab |
| 关键指标 | `M_ENT_SZ_COUNT`、`M_ENT_CITY_AVG_TECH_POWER`、`M_ENT_CITY_DENSITY`、`M_ENT_CHAIN_COMPLETENESS`、`M_ENT_SZ_CHAIN_POSITION`、`M_ENT_KEY_NODE_COUNT` |
| 约束 | 对标城市默认集合待甲方确认（Q016）；竞争力归并至 P10（去重，移除本页综合竞争力 Tab） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-25：聚焦深圳企业，多维对标评估位置、竞争力与生态完整性 |

#### FR-12 招引企业推荐（E-26）

| 项 | 内容 |
|----|------|
| 输入 | 产业方向 + 区域/企业类型/成长性筛选 + 招引策略（强链/补链/智能/存量） |
| 处理 | 基于深圳产业发展方向，从全国范围智能筛选高成长性、关键技术型企业；按产业相关度、政策匹配度、生态连接度综合计算招引推荐指数 |
| 输出 | 招引推荐名单（推荐指数/核心优势/关键指标/合作价值）+ 企业价值分析与一企一策建议抽屉；补链为 P5 链位缺口默认策略 |
| 关键指标 | `M_ENT_ATTRACTION_INDEX`、`M_ENT_GROWTH_POTENTIAL`、`M_ENT_INDUSTRY_MATCH_SCORE`、`M_ENT_POLICY_MATCH_SCORE`、`M_ENT_RECOMMEND_COUNT` |
| 约束 | 招引推荐指数阈值与权重待甲方确认（Q015） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-26：从全国智能筛选高成长性、关键技术型企业，生成招引推荐名单及依据 |

#### FR-13 培育企业推荐（E-27）

| 项 | 内容 |
|----|------|
| 输入 | 产业方向 + 梯度培育层（创新型/专精特新/瞪羚/小巨人/独角兽/规上/上市）+ 指标配置 |
| 处理 | 聚焦深圳市内企业，识别具备潜力但面临发展瓶颈的优质企业；按产业相关度、政策匹配度、成长潜力、创新能力综合计算培育推荐指数 |
| 输出 | 培育推荐名单 + 培育建议（一企一策）+ 梯度培育层（可折叠）；与招引 Tab 同构页面、推荐逻辑不同 |
| 关键指标 | `M_ENT_CULTIVATION_INDEX`、`M_ENT_GROWTH_POTENTIAL`、`M_ENT_INDUSTRY_MATCH_SCORE`、`M_ENT_POLICY_MATCH_SCORE` |
| 约束 | 培育推荐指数阈值与权重待甲方确认（Q015） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-27：识别深圳潜力但遇瓶颈的优质企业，提供培育建议与名单 |

#### FR-14 企业供应链关系分析（E-28）

| 项 | 内容 |
|----|------|
| 输入 | 产业 + 区域 + 企业类型 + 中心企业搜索 + 关系范围（级数） |
| 处理 | 融合工商、招投标、舆情等多源信息构建企业供应链知识图谱（NebulaGraph）；支持多级下钻、关键节点（中心性）识别、断链风险识别 |
| 输出 | 供应链图谱（中心企业 + 供应商/客户多级，节点可点展开）+ 关键节点中心性排名 + 风险分析与结论（EvidenceList）；含单链下钻 / 多链对比两个工作台 Tab、图谱概览/关键节点/风险三个研判 Tab |
| 关键指标 | `M_ENT_SUPPLIER_COUNT`、`M_ENT_CORE_SUPPLIER_COUNT`、`M_ENT_NODE_CENTRALITY`、`M_ENT_SUPPLY_CHAIN_RISK`、`M_ENT_RELATION_STRENGTH` |
| 约束 | 图谱为复杂交互（AntV G6 + NebulaGraph），不简化为静态图（DC5）；节点过多（>200）自动折叠并提供"仅看核心供应商"（EX-05）；高风险节点一键"诊断痛难点 → P9"；核心供应商阈值/断链风险评级待甲方确认（Q017） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-28：构建供应链知识图谱，多级下钻、关键节点识别、断链风险识别 |

#### FR-15 企业发展痛难点分析（E-29）

| 项 | 内容 |
|----|------|
| 输入 | 产业 + 企业选择 + 诊断维度勾选（技术/市场/融资/管理） |
| 处理 | 基于专家知识库与行业信息构建多维度痛难点诊断模型，自动识别技术、市场、资金、管理等瓶颈，生成结构化问题报告与改进建议 |
| 输出 | 痛难点总数与各维度严重度 MetricCard、痛难点分类统计柱 + 深圳企业vs行业最佳雷达、详细问题清单表（维度/问题描述/严重度/成因）、解决方案与最佳实践（可导出报告） |
| 关键指标 | `M_ENT_PAINPOINT_COUNT`、`M_ENT_PAINPOINT_SEVERITY`、`M_ENT_PAINPOINT_GAP` |
| 约束 | 诊断维度与阈值依赖专家知识库，口径待甲方确认（Q018） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-29：多维度痛难点诊断模型，自动生成结构化问题报告与改进建议 |

#### FR-16 企业竞争力分析（E-30）

| 项 | 内容 |
|----|------|
| 输入 | 目标产业 + 对比企业（多选）+ 综合评估框架指标库勾选与赋权 |
| 处理 | 提供整合技术力、商业力等维度的综合竞争力评估框架，支持用户自定义指标体系，企业评分、排名与短板提示；可一键导入 P3 技术力/商业力子维度得分 |
| 输出 | 竞争力雷达对比 + 综合排名（条形）+ 优势短板分析 + 详细指标对比表 + 分析结论与短板提示（EvidenceList） |
| 关键指标 | `M_ENT_COMPETITIVENESS_SCORE`、`M_ENT_COMPETITIVENESS_RANK`、`M_ENT_SHORTBOARD_COUNT`、`M_ENT_INNOVATION_INDEX` |
| 约束 | P10 为竞争力**唯一入口**（DC3，消除重复分数）；与 P3 共享技术力/商业力底层得分；指标体系与默认权重待甲方确认（Q014） |
| 优先级 | P1 |
| 验收点溯源 | catalog E-30：整合技术力、商业力的综合竞争力评估框架，自定义指标体系评分排名短板提示 |

---

### 3.3 Layer C · 内容运营后台（FR-17 ~ FR-18）

#### FR-17 可视化展示内容管理（E-36）

| 项 | 内容 |
|----|------|
| 输入 | 运营人员对 Layer A 展示区块的开关、排序、配置操作 |
| 处理 | 后台维护可视化展示内容（产业全景、新兴科技、企业发展、科研力量、领军人才、产业服务、政策新闻、产研报告等的展示管理）；以页面配置驱动 Layer A 渲染 |
| 输出 | 区块开关/排序配置生效，Layer A 按配置渲染；所见即所得预览；变更记录可追溯 |
| 优先级 | P2 |
| 验收点溯源 | catalog E-36：支持产业全景、企业发展等可视化展示内容管理 |

#### FR-18 门户企业发展内容管理（E-37）

| 项 | 内容 |
|----|------|
| 输入 | 运营人员维护明星企业 CMS、全景图标注、深圳介绍文案等 |
| 处理 | 后台管理维护门户系统展示内容（企业发展内容管理及其他专题内容管理）；供 A2/A3/A4 读取 |
| 输出 | 内容发布后 Layer A 读取生效（目标 ≤5min）；demo-ui-topic 阶段可用 JSON Mock 模拟 CMS，正式环境走内容运营中心 |
| 优先级 | P2 |
| 验收点溯源 | catalog E-37：管理维护门户展示内容，含企业发展内容管理及其他专题内容管理 |

---

## 4. 非功能需求

> 来源：FDS §15（NF-01~NF-10）+ 架构铁律 + D9 血缘 + User Flow 埋点。

### 4.1 架构合规类

| ID | 需求 |
|----|------|
| NF-01 | 算法仅在 Python 实现（技术力/商业力/竞争力/招引培育/供应链中心性/断链风险/痛难点等模型）；Java 不实现算法 |
| NF-02 | 图谱（供应链/生态）使用 NebulaGraph，禁止 Neo4j |
| NF-03 | 前端 lumen 正式栈：Arco Design + ECharts + AntV G6 + Leaflet（D8） |

### 4.2 性能与加载体验

| ID | 需求 |
|----|------|
| NF-04 | 首屏 KPI 区域 LCP < 2.5s（正式环境） |
| NF-10 | 加载体验：筛选/评估/图谱等异步操作有 skeleton 或进度态，禁止白屏；筛选确认后 300ms 内出现 skeleton（UX-06） |

### 4.3 可用性与上下文一致性

| ID | 需求 |
|----|------|
| NF-05 | 对比篮、筛选状态在刷新与 Tab 切换时不丢失（跨页上下文持久，UX-04） |
| NF-08 | 可访问性：键盘可达、焦点可见、图表/地图有文字替代与 aria-label（X-07） |
| NF-09 | 响应式：最小宽度 1280；embed 模式自适应容器宽度 |

### 4.4 安全与集成

| ID | 需求 |
|----|------|
| NF-06 | embed 模式遵循 CORS / 白名单；门户 iframe 集成的跨域与样式隔离（门户 embed SSO 见 Q021） |
| NF-11 | 调用链安全：前端 → Java REST → Python `/internal/*` 不可越层；Java 只读 ADS，前端不直连数据库/图谱 |

### 4.5 数据血缘与可观测性（D9 / C-04）

| ID | 需求 |
|----|------|
| NF-07 | 数据血缘（D9）：界面每个统计指标挂 metric_id 与"8 件套"元数据，统计数字旁有 ⓘ（MetricSpecCard）；Wave 0/Mock 阶段统计数字旁有 🧪（MockBadge）；待确认口径有 ⚠️ 角标 |
| NF-12 | 可观测性埋点：前端 `observability.ts` 接入 13 个埋点事件（见下表），事件命名以 `observability.ts` 既有约定为准（开放项） |
| NF-13 | 算法/数据降级：算法结果未就绪不阻塞主界面，MetricSpecCard 降级显示"数据说明加载中"；图谱节点过载自动折叠（EX-04/EX-05） |

**埋点事件清单（NF-12，来源 User Flow §3）**：

| # | 事件 | 触发场景 |
|---|------|---------|
| 1 | `ent_overview_view` | 进入企业分析概述 P0 |
| 2 | `ent_filter_apply` | 应用产业/区域/企业类型筛选 |
| 3 | `geo_drilldown` | P1 国→省→市三级地理下钻 |
| 4 | `indicator_config` | P3/P10 配置指标与权重 |
| 5 | `evaluate_run` | 触发技术力/商业力/竞争力评估 |
| 6 | `detail_open` | 打开企业画像 DetailDrawer |
| 7 | `graph_expand` | 供应链图谱节点展开 |
| 8 | `report_export` | 导出报告 / 名单 / 截图 |
| 9 | `metric_spec_view` | 点击 ⓘ 查看数据说明卡 |
| 10 | `mock_badge_view` | hover 🧪 Mock 标识 |
| 11 | `ent_basket_add` / `ent_basket_remove` | 对比篮增删 |
| 12 | `ent_judgment_action_click` | 点击 JudgmentStrip 建议动作链 |
| 13 | `ent_portal_deep_link` | Layer A → B 深链跳转 |

> 非功能需求合计 **13 条**（NF-01 ~ NF-13）。

---

## 5. 外部接口需求

### 5.1 用户界面（页面清单）

| 层 | 页面 | 路由 |
|----|------|------|
| A | A0 企业发展首页 | `/cluster/enterprise` |
| A | A1 企业整体概况 | `/cluster/enterprise/general` |
| A | A2 重点企业全景图 | `/cluster/enterprise/panorama` |
| A | A3 明星企业介绍（列表/详情） | `/cluster/enterprise/star`、`/cluster/enterprise/star/:code` |
| A | A4 深圳企业介绍 | `/cluster/enterprise/shenzhen` |
| A | A5 一张图·企业图层 | `/cluster/map/enterprise` |
| B | P0 企业分析概述 | `/enterprise/overview` |
| B | P1 重点企业类型分析 | `/enterprise/type-distribution` |
| B | P2 重点企业领域分布分析 | `/enterprise/domain-distribution` |
| B | P3 企业能力评估对比 | `/enterprise/capability` |
| B | P5 深圳企业现状分析 | `/enterprise/status-analysis` |
| B | P6 企业引育推荐分析 | `/enterprise/recommendation` |
| B | P8 企业供应链关系分析 | `/enterprise/supply-chain` |
| B | P9 企业发展痛难点分析 | `/enterprise/pain-points` |
| B | P10 企业竞争力分析 | `/enterprise/competitiveness` |
| C | 内容运营后台（E-36/E-37） | 后台 |

UI 通用组件契约（D8 §9）：PageShell / TopicSidebar / ContextBar / JudgmentStrip / MetricCard / SearchableCascadeFilter / FilterBar / ChartPanel / MapPanel / GraphCanvas / DataTable / EvidenceList / SectionPanel / DetailDrawer / PrimaryWorkbenchTabs / SecondaryAnalysisTabs / StatusTag / DataCard（共 18 个）。

### 5.2 软件接口

| 接口类 | 模式 | 说明 |
|--------|------|------|
| 门户嵌入（Layer A） | iframe | 门户菜单打开 Layer A，如 `/cluster/enterprise/general?industry=x&embed=1`；embed 模式隐藏侧栏、产业只读 |
| 深链（A → B） | Deep Link | 携带 `industry / region / enterprise_code / strategy / suggested_action` 等参数跳转（深链参数表见 FDS §13.2） |
| 门户消费 API（Layer A） | REST | `GET /api/v1/ent/overview` 等；门户首页 KPI、企业实体检索 `GET /api/v1/ent/search?q=` |
| 分析 API（Layer B） | REST | `/api/v1/ent/analysis/*` 研判类接口 |
| 企业画像 API（共用） | REST | `/api/v1/ent/enterprise/{code}`（DetailDrawer） |

调用链：前端 → Java REST → ADS（只读）；算法 → Python `/internal/*`（C-01/C-02）。

### 5.3 数据接口

- Java 仅**只读** ADS 应用结果层（`ads.ent_*` 13 表，契约面冻结），不写算法、不直连 nGQL（C-07）。
- 统计字段 100% 挂 metric_id（前缀 `M_ENT_*`），口径与血缘见数据库设计（v1）cfg_metric 注册（49 条，8 件套）。
- 图谱数据由 Python 灌入 NebulaGraph `gkx_enterprise`，中心性/最短路径结果回写 `ent_supply_chain` 供 Java 只读。
- Mock 阶段 ADS `calc_batch_id` 前缀 `mock_`，UI 显示 🧪。

---

## 6. 其他需求

### 6.1 数据口径开放项（待甲方确认）

> 业务口径决策只能甲方拍板（C-08）；试点期按团队临时默认值先跑，UI 标 ⚠️"待甲方确认"。

| # | 开放项 | 影响功能 / 指标 | 临时默认 |
|---|--------|----------------|---------|
| O-01（Q010） | 企业类型判定规则（外企/高企/小微/上市精确口径） | FR-07、`M_ENT_TYPE_COUNT`、`M_ENT_HIGH_TECH_COUNT` | 按资质/荣誉标签解析 |
| O-02（Q011） | "创新型企业"口径（=高企∪专精特新∪瞪羚∪独角兽？） | FR-06、`M_ENT_INNOVATIVE_COUNT` | 四类资质并集去重 |
| O-03（Q012） | 行政区划下钻精度（到市/到区县）+ 密度分母（面积/GDP） | FR-07、`REGIONAL_COUNT/DENSITY`、`AGGLOMERATION_INDEX` | 到市级 |
| O-04（Q013） | 领域覆盖广度/深度计算口径（领域全集、权重） | FR-08、`DOMAIN_COVERAGE_*`、`DIVERSIFICATION_INDEX` | 链节点全集 |
| O-05（Q014） | 技术力/商业力/竞争力指标库构成与默认权重 | FR-09/FR-10/FR-16、`*_SCORE` | 原型默认权重 |
| O-06（Q015） | 招引/培育推荐指数阈值与权重 | FR-12/FR-13、`ATTRACTION/CULTIVATION_INDEX` | 多因子等权 |
| O-07（Q016） | 对标城市默认集合（北京/上海/苏州/广州…） | FR-11、`CITY_*` | 北上苏广 |
| O-08（Q017） | 供应链核心供应商阈值 + 断链风险评级规则 | FR-14、`CORE_SUPPLIER_COUNT`、`SUPPLY_CHAIN_RISK`、`NODE_CENTRALITY` | chain_score 分位阈值 |
| O-09（Q018） | 痛难点诊断维度与阈值（依赖专家知识库） | FR-15、`PAINPOINT_*` | 技术/市场/融资/管理四维 |
| O-10（Q019） | 科研人数统计口径（A1） | FR-02、科研人数 | `employees_number` 代理 |
| O-11（Q020） | 明星企业入选规则（CMS vs 算法，A3） | FR-04、FR-18 | 运营配置 |
| O-12（Q021） | 门户 embed SSO 集成方案 | NF-06、Layer A 集成 | 待门户厂商联调 |

> 另有 K-O7：市场份额/品牌声量/客户集中度无数据源，需额外采购（影响 FR-10/FR-16 的 `M_ENT_MARKET_SHARE` 等），暂置空。埋点事件命名（NF-12）以 `observability.ts` 既有约定为准。

### 6.2 国际化与合规预留

- 企业名称支持中英文（数据库已含 `enterprise_name_en`）；界面文案以中文为主，国际化为预留能力。
- 数据合规：企业数据展示遵循数据来源与合规要求；外部数据采购（K-O7）须满足授权与合规。

---

## 7. 需求-验收追溯矩阵

### 7.1 FR ↔ E-XX ↔ 页面 ↔ metric_id

| FR | E-XX | catalog 验收点 | 页面 | 代表 metric_id |
|----|------|---------------|------|----------------|
| FR-01 | E-31 | 企业发展快速入口 | A0 `/cluster/enterprise` | （入口聚合，无独立 metric） |
| FR-02 | E-32 | 整体概况 | A1 `/cluster/enterprise/general` | `M_ENT_TOTAL_COUNT`、`M_ENT_NEW_COUNT_Y`、`M_ENT_REGIONAL_COUNT` |
| FR-03 | E-33 | 重点企业全景 | A2 `/cluster/enterprise/panorama` | （规模/领域统计派生） |
| FR-04 | E-34 | 明星企业介绍 | A3 `/cluster/enterprise/star` | （CMS 关联，非算法 TopN） |
| FR-05 | E-35 | 深圳企业介绍 | A4 `/cluster/enterprise/shenzhen` | `M_ENT_SZ_COUNT` |
| FR-06 | E-20 | 企业分析概述 | P0 `/enterprise/overview` | `M_ENT_TOTAL_COUNT`、`M_ENT_INNOVATIVE_COUNT`、`M_ENT_PATENT_TOTAL`、`M_ENT_HIGH_TECH_COUNT` |
| FR-07 | E-21 | 类型分析 | P1 `/enterprise/type-distribution` | `M_ENT_TYPE_*`、`M_ENT_REGIONAL_*`、`M_ENT_AGGLOMERATION_INDEX` |
| FR-08 | E-22 | 领域分布 | P2 `/enterprise/domain-distribution` | `M_ENT_DOMAIN_COVERAGE_*`、`M_ENT_DIVERSIFICATION_INDEX` |
| FR-09 | E-23 | 技术力评估 | P3 `/enterprise/capability` | `M_ENT_TECH_POWER_SCORE`、`M_ENT_TECH_RANK` |
| FR-10 | E-24 | 商业力评估 | P3 `/enterprise/capability` | `M_ENT_BUSINESS_POWER_SCORE`、`M_ENT_REVENUE_*`、`M_ENT_PROFIT_MARGIN` |
| FR-11 | E-25 | 深圳现状 | P5 `/enterprise/status-analysis` | `M_ENT_SZ_*`、`M_ENT_CITY_*`、`M_ENT_CHAIN_COMPLETENESS` |
| FR-12 | E-26 | 招引推荐 | P6 `/enterprise/recommendation` | `M_ENT_ATTRACTION_INDEX`、`M_ENT_RECOMMEND_COUNT` |
| FR-13 | E-27 | 培育推荐 | P6 `/enterprise/recommendation` | `M_ENT_CULTIVATION_INDEX`、`M_ENT_GROWTH_POTENTIAL` |
| FR-14 | E-28 | 供应链关系 | P8 `/enterprise/supply-chain` | `M_ENT_SUPPLIER_COUNT`、`M_ENT_NODE_CENTRALITY`、`M_ENT_SUPPLY_CHAIN_RISK` |
| FR-15 | E-29 | 痛难点 | P9 `/enterprise/pain-points` | `M_ENT_PAINPOINT_COUNT`、`M_ENT_PAINPOINT_SEVERITY`、`M_ENT_PAINPOINT_GAP` |
| FR-16 | E-30 | 竞争力分析 | P10 `/enterprise/competitiveness` | `M_ENT_COMPETITIVENESS_SCORE`、`M_ENT_COMPETITIVENESS_RANK`、`M_ENT_SHORTBOARD_COUNT` |
| FR-17 | E-36 | 可视化内容管理 | C 后台 | （配置驱动，无统计 metric） |
| FR-18 | E-37 | 门户内容管理 | C 后台 | （CMS，无统计 metric） |

### 7.2 覆盖性自检

- 功能需求 **18 条**（FR-01 ~ FR-18），逐条对应验收点 E-20~E-37，覆盖 **18/18 = 100%**（Layer A 5 + Layer B 11 + Layer C 2）。
- Layer B 10 个三级叶子功能（E-21~E-30）1:1 覆盖，符合 ±10% 范围铁律（E-23/E-24 与 E-26/E-27 为页面合并、功能点独立）。
- 非功能需求 **13 条**（NF-01 ~ NF-13）。
- 开放项 **12 条**（O-01 ~ O-12）+ 无来源采购项 K-O7。

> 本矩阵仅作需求-验收追溯，不代表完成度或验收结论；实际通过与否由 qa-agent 测试与 PM 终审判定。

---

**文档结束 — 企业要素需求规格说明书（SRS）V1.0（Markdown 初稿，待 PM 终审）**
