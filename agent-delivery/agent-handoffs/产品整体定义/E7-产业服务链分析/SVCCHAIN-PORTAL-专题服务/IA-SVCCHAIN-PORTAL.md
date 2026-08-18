# IA-SVCCHAIN-PORTAL｜专题服务（门户展示）信息架构

> **版本**：v1.1（TOPIC-SVCCHAIN-R2C；2026-08-07 修订：去掉全球概况页尾快速入口，页内切换仅用顶部子导航；左侧菜单顺序固定为门户展示→查询→分析）
> **原始需求**：展示系统 Bid §1.1.1.1.1.1.1.33（33.1-33.5，序号 97-104）
> **实现仓**：demo-ui-topic `src/app/pages/service-portal/`（新建门户页组，命名对齐 `policy-portal` 门户惯例）
> **产品对标**：`E-31-企业发展/`（E-32 全球概况 / E-35 深圳介绍 / E-33 重点对象模式）  
> **本轮决策（Q068 · P7）**：产业下拉 = 15 个产业集群，与政策扶持同款级联（同一集群 API）。任务 `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`。

## 1. 模块目标与边界

**做**：门户展示侧"专题服务"页组——五个展示页（全球概况 / 产业分布 / 区域分布 / 技术能力 / 深圳介绍）+ 统一的重点机构详情抽屉；面向公开浏览与接待场景，承担认知建立与向分析侧分流。

**不做**：机构检索（分析侧 `/service-center/search`）、覆盖/趋势/评估分析工作台（ORG-ANALYSIS）、链路短板与图谱（ECOSYSTEM）、招引培育名单（RECOMMEND）、机构主数据维护。门户页出现的分析动作一律是**跳转分流**，不在门户内复刻分析能力。

## 2. 对象与稳定身份

| 对象 | 稳定 ID | 说明 |
| --- | --- | --- |
| 服务机构 | `org_id`（`svc-org-XXX`） | 与分析侧共用同一主数据 `SERVICE_ORGS`（CT-SVC-ORG-02）；详情抽屉、榜单、入篮均用此 ID |
| 产业领域 | `field_id`（`field-XXX`） | 与分析侧同一字典 `SERVICE_FIELDS` |
| 服务链环节 | `stage_id` | 复用 ECOSYSTEM `CHAIN_STAGES` 六环节字典（CT-SVC-PT-01） |
| 门户聚合统计 | `servicePortalData` 数据集 | 全球/全国/深圳聚合口径（Wave 0 确定性 Mock），与实体子集分层，见 §6 |
| 重点机构扩展档案 | `KEY_ORG_PROFILES[org_id]` | 仅新增门户展示字段（领导人/人数/营收/业务点位），不覆盖主数据 |

## 3. IA 结构

```text
/service-portal（门户专题服务页组；左侧菜单顺序对齐企业/产业/政策：专题服务展示 → 服务机构查询 → 专题分析）
├─ /service-portal/overview 全球服务机构概况（默认落点，33.1）
│   ├─ KPI 区（全球总数 / 本年新增 / 覆盖领域数）
│   ├─ 数量分析区：历年总量趋势折线（97）
│   ├─ 类型分析区：类型占比环形（98）
│   └─ 规模分析区：规模四档条形（99）
│   （页内切其他门户子页：走 ServicePortalShell 顶部子导航；不在页尾重复快捷入口）
├─ /service-portal/industry-distribution 服务机构产业分布（33.2）
│   ├─ 产业选择器（15 个产业集群，可再选 L0；无映射空态）
│   ├─ 服务链节点分布主视图（链路分层 + 环节条形，CT-SVC-PT-01）
│   └─ 环节展开：代表机构列表（下钻详情抽屉）
├─ /service-portal/region-map 服务机构区域分布（33.3）
│   ├─ Tab: global 全球分布（Leaflet 比例圆点 + 区域排名列表）
│   └─ Tab: china 全国分布（同构 + "进入深圳介绍"入口）
├─ /service-portal/capability-rank 服务机构技术能力（33.4）
│   ├─ 产业页签（15 个产业集群；无映射空态）
│   ├─ 固定口径说明卡（等权五维 · ⚠️ Q-SVCCHAIN-01 · 🧪）
│   └─ Top30 榜单（名次/机构/类型/综合分/五维迷你条/入篮）
├─ /service-portal/shenzhen 深圳产业服务介绍（33.5）
│   ├─ 深圳 KPI 区
│   ├─ 数量区：历年趋势折线（100）
│   ├─ 类型区：类型占比环形（101）
│   ├─ 领域区：领域 × 服务链环节分布（102，结合深圳产业链全景分层）
│   ├─ 区域区：深圳十区地图 + 排名列表（103）
│   └─ 重点产业服务机构卡片墙（104 入口）
└─ Drawer: 重点机构详情（org 参数驱动，四板块：概况/规模/领域/业务分布；跨页共用）
```

## 4. URL 契约

| 参数 | 作用页 | 语义 | 示例 |
| --- | --- | --- | --- |
| `field` | industry-distribution / capability-rank | 当前产业领域 | `?field=field-bio` |
| `tab` | region-map | 区域层级 `global/china` | `?tab=china` |
| `org` | 任意门户页 | 打开重点机构详情抽屉 | `?org=svc-org-001` |

URL 参数为分享/恢复契约；产业选择、区域页签等偏好走 localStorage（`topic-svc-portal-*` 前缀，见 UX-SPEC §6）。参数非法时清除该参数并 Message 提示，不白屏。

## 5. Frame 职责

| Frame | 名称 | 职责 | 对应故事 |
| --- | --- | --- | --- |
| `F-SVC-PT-01` | 全球概况页 | KPI、趋势、类型、规模、结论条（切页走顶部子导航） | US-01 |
| `F-SVC-PT-02` | 产业分布页 | 产业选择、链路节点分布、环节代表机构 | US-02 |
| `F-SVC-PT-03` | 区域分布页 | 全球/全国地图 + 排名列表 | US-03 |
| `F-SVC-PT-04` | 技术能力页 | 产业页签、口径说明卡、Top30 榜单 | US-04 |
| `F-SVC-PT-05` | 深圳介绍页 | 深圳四类统计 + 重点机构卡片墙 | US-05、US-06 |
| `F-SVC-PT-06` | 重点机构详情抽屉 | 四板块详情 + 分析侧分流动作 | US-06 |

## 6. 数据与服务边界（两层数据分层）

| 层 | 数据 | 承载 | 约束 |
| --- | --- | --- | --- |
| 聚合层 | 全球/全国/深圳的总量、趋势、类型、规模、区域、链路节点分布 | `servicePortalData.ts`（确定性 Mock） | 口径未定标 ⚠️ Q-SVCCHAIN-06；UI 明示"演示聚合数据集"；层级一致性：深圳 ≤ 全国 ≤ 全球 |
| 实体层 | 环节代表机构、Top30 榜单、重点机构卡片与详情 | `serviceCenterData.SERVICE_ORGS`（与分析侧共享，24 家演示子集）+ `KEY_ORG_PROFILES` 门户扩展档案 | 同一 org_id 同一数值；扩展档案只增字段不覆盖主数据 |

- Wave 0 全 Mock，禁止运行时随机数（AC 可复现）。
- 目标态：前端 → Java REST `/topic/v1/service-portal/**`（聚合统计）+ `/topic/v1/service-chain/orgs/**`（实体）；不直连 Python、不写 nGQL。
- 技术力综合分为分析侧 `computeEvaluation` 同一实现的固定等权应用（CT-SVC-PT-03），门户不另建第二套计算。

## 7. 复用契约

| 复用 | 来源 | 约束 |
| --- | --- | --- |
| 门户壳层 | `development/portalShared`（JudgmentStrip / SectionPanel） | 自建 `ServicePortalShell`（面包屑+结论条），不复制企业域业务逻辑 |
| EChart 容器 | `components/common/EChart.tsx` | 图表语义与 metric_id 由本模块定义 |
| Leaflet 地图 | `policy-portal/PolicyLeafletMap`（GeoPoint 比例圆点通用件） | 仅传数据与图例文案，不改政策语义（CT-SVC-PT-04） |
| 服务链环节字典 | `service-center/serviceEcosystemData.CHAIN_STAGES` | 六环节字典唯一来源（CT-SVC-PT-01），不自造第二套 |
| 技术力模型 | `service-center/serviceCenterModel.computeEvaluation` + `CAPABILITY_DIM_DEFS` | 固定等权配置调用（CT-SVC-PT-03），Q-SVCCHAIN-01 诚实态沿用 |
| 评审层/徽章 | `service-center/ServiceReviewMount` + `SvcMetricBadges` + `serviceReadinessSeed` + `serviceReviewData` | 新指标登记进同一镜像文件（M_SVC_PT_* 段），mount_id 用 `SVC-PT-*` |
| 对比篮 | `ServiceOrgBasketButton`（系统篮 `service_org`） | CT-SVC-ORG-03 触点扩展：门户榜单行 + 详情抽屉 |
| 禁止 | import `pages/enterprise/*` 业务组件、复制 E2 CHAIN 数据模型 | 对标仅限交互模式 |

## 8. 指标登记（8 件套见 TRACE，就绪度四维见 readinessSeed）

| metric_id | 中文名 | D1 | 呈现 |
| --- | --- | --- | --- |
| `M_SVC_PT_GLOBAL_TOTAL` | 全球服务机构总数（含历年） | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_GLOBAL_TYPE_DIST` | 全球服务机构类型分布 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_GLOBAL_SCALE_DIST` | 全球服务机构规模分布 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_CHAIN_NODE_ORG` | 产业链节点服务机构数 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_REGION_ORG` | 区域服务机构数 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_ORG_TECH_SCORE`（复用） | 技术力综合得分 | draft（Q-SVCCHAIN-01） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_SZ_TOTAL` | 深圳产业服务机构数量 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_SZ_TYPE_DIST` | 深圳机构类型统计 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_SZ_FIELD_DIST` | 深圳机构产业领域分布 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_SZ_REGION_ORG` | 深圳机构区域分布 | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_PT_KEYORG_SCALE` | 重点机构规模档案值（人数/营收） | draft（Q-SVCCHAIN-06） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_ORG_COVERAGE_DEPTH`（复用） | 服务深度得分（详情领域板块） | draft（Q-SVCCHAIN-02） | ⓘ(橙点) + ⚠️ + 🧪 |

## 9. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-SVC-PT-01 | 本叶子 ← ECOSYSTEM | 服务链六环节字典 `CHAIN_STAGES` 为链路节点分布唯一字典来源；"结合产业链全景图"的展示分层语义参照 E2 全景交互心智（REUSE-MATRIX-CHAIN 原则），不复制 CHAIN 数据模型 |
| CT-SVC-PT-02 | 本叶子 → ORG-ANALYSIS | 门户详情抽屉"进入分析侧画像"跳 `/service/institution-judgment?org={org_id}`，分析侧按既有 org 参数契约打开同一机构画像 |
| CT-SVC-PT-03 | 本叶子 ← ORG-ANALYSIS | Top30 排名分 = `computeEvaluation` 固定等权应用；`M_SVC_ORG_TECH_SCORE` 指标复用，Q-SVCCHAIN-01 诚实态一体沿用，禁止门户另造技术力口径 |
| CT-SVC-PT-04 | 本叶子 ← 政策门户 | `PolicyLeafletMap` 作为通用比例圆点地图容器复用（GeoPoint 接口），图例/配色语义由本模块传参 |
| CT-SVC-ORG-03（扩展） | 本叶子 → 系统对比篮 | 门户榜单行与详情抽屉新增 `service_org` 入篮触点，篮语义/上限/分发不变 |
