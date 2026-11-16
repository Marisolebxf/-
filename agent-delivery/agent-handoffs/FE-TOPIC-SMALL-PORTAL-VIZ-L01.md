# FE-TOPIC-SMALL-PORTAL-VIZ-L01 · 专题小屏·门户服务+可视化管理全量复刻 handoff

- **任务**：FE-TOPIC-SMALL-PORTAL-VIZ-L01（feature，XL/13）
- **仓**：`repos/lumen-ui-topic-mobile`（分支 dev，本地工作区待人工确认推送）
- **监管人**：human:孔东；**执行**：agent:frontend-agent
- **完成日**：2026-11-16
- **ponytail**: full（复刻任务不裁功能，只裁移动端不适交互）

## 范围与实现（对照 PC lumen-ui-topic）

### A. 服务链专题服务 5 页（`/service-portal/*`）

| 页面 | 移动端视图 | PC 真源 | 接口 |
|---|---|---|---|
| 全球概况 | `ServicePortalOverviewPage.vue` | PC ServicePortal overview | `svcPortalOverview` |
| 产业分布 | `ServicePortalIndustryDistributionPage.vue` | PC industry-distribution | `svcPortalIndustryDistribution` |
| 区域分布 | `ServicePortalRegionMapPage.vue` | PC region-map | `svcPortalRegionMap` |
| 技术能力 | `ServicePortalCapabilityRankPage.vue` | PC capability-rank | `svcPortalRanking {list_type:TECH}` |
| 深圳服务 | `ServicePortalShenzhenPage.vue` | PC shenzhen（KPI/趋势/饼/柱/地图/区榜/重点机构） | `svcPortalShenzhen` + `svcPortalKeyOrgs` |
| 机构画像抽屉 | `SvcOrgProfileDrawer.vue` + `svcProfileModel.ts` | PC org profile | `svcProfileGet`（新增 `SvcProfileData`/`SvcTechScoreItem` 类型与 `profileGet` 路径） |
| 重点机构 | `SvcPortalKeyOrgSection.vue` + `SvcPortalKeyOrgDrawer.vue`（ext.portal_extension：带头人/简介/规模/业务区域 Leaflet） | PC key-orgs | `svcPortalKeyOrgs` |

### B. 可视化管理 4 页（VIZ）

| 页面 | 路由 | 移动端视图 | PC 真源 | 导出 |
|---|---|---|---|---|
| 企业发展可视化 | `/enterprise/development-viz` | `views/viz/EnterpriseVizPage.vue`（3 Tab：基本画像 KPI+散点+CSV；成长轨迹 时间线+财务图；竞争力 SWOT+雷达） | PC EnterpriseVizPage（a-table→企业选择卡片行） | exportCards CSV ✅ |
| 产业全景可视化 | `/industry-center/overview-viz` | `views/viz/PanoramaVizPage.vue`（3 Tab：规模分布 KPI+地理热力 Leaflet；结构 链图谱+构成饼；趋势预测 10 年线+滑杆 0-20% 增速外推 5 年） | PC PanoramaVizPage | 图表截图/数据卡 ✅ |
| 政策新闻可视化 | `/policy/news-display` | `views/policy/PolicyNewsDisplayPage.vue`（4 Tab：时间轴 粒度/关键词/事件卡/大事抽屉；主题 权重标签墙+聚类分组；影响 范围柱+深度线；扶持与CMS CMS块+缺口卡+省/市强度榜） | PC PolicyNewsDisplayPage | CMS 数据卡 ✅ |
| 产业服务可视化 | `/service/portal-viz` | `views/viz/ServiceVizPage.vue`（3 Tab：资源分布 全国/全球热力+Top20；供需匹配 产业/规模筛选+需求柱+匹配热力；效率案例 雷达+案例卡+详情抽屉） | PC ServiceVizPage | 案例 CSV ✅ |

### C. 政策扶持全量升级（`/policy-portal/overview`）

- PC 真源：`PolicyPortalPage.vue`（569 行六 Tab）+ 5 Panel + `policyPortalModel.ts` + `policyPortalTabs.ts` + `policyPortalLive.ts`
- 移动端：`PolicyPortalView.vue` 重写为六 Tab 全量（概况统计/政策地图/产业覆盖/力度排名/最新动态/深圳对比，深圳含 4 视图二级 Tab）
- 新增 `policyPortalModel.ts`（PC model+tabs 合并移植；live 层复用本仓 `policyIndicators`/`industryClusters` 封装替代 PC 裸 fetch——本仓 USE_MOCK=false 定死，无绕 Mock 需求）
- 新增 `PolicyPortalChainGraph.vue`（G6 dagre LR 覆盖图，覆盖度着色、缺口红描边、tap 选中；连线缺失时用 `industryPanoramaSnapshot` 回填 edges）
- 诚实性契约同源：政策总量只读 `headline.M_POLICY_TOTAL_COUNT`；力度指数缺数留空不折算；覆盖只读 `portal_gaps.nodes`；城市榜只读 `city_count_continuity`；级别直传中文（#7165869483）；连续性/时序只读各地区自身字段不摊全库
- 原「力度排名与产业覆盖请前往 PC 端」降级条幅移除

### D. 基建

- `src/router/index.ts`：ADAPTED_PAGES 注册 9 个新路由（service-portal 5 + viz 4）
- `src/views/viz/vizPage.css` + `VizSectionTitle.vue`：VIZ 页统一小屏样式
- `src/api/service/{paths,index,types}.ts`：`profileGet` 端点与 `svcProfileGet`
- `ServicePortalShell.vue`：修 `<script setup>` 内 `export const`（build 编译器报错；vue-tsc 宽容掩盖）

## 逐页裁剪清单（砍掉项对照）

| PC 能力 | 小屏处理 | 依据 |
|---|---|---|
| a-table 数据表 | 卡片列表（`viz-row`/`svc-portal-rank-list`/ListCard） | Design-mobile §10 表格转卡片 |
| echarts-wordcloud 词云 | 权重标签墙（themeTermSize 字号分级） | 依赖未装；不加新依赖（ponytail 铁律 2） |
| 聚类力导图 graph | 可折叠聚类分组列表 | 小屏性能 |
| Arco Cascader/Select | van-cascader / van-popup+picker / dropdown | 组件栈 |
| 政策门户对比篮多选 a-select | checkbox popup（≤5 对照同 PC POLICY_COMPARE_MAX） | 保留全部功能 |
| SWOT 四象限 | 2×2 卡片 | 布局等价 |
| CSV 导出 | 全保留（exportCards 等） | 用户 2026-11-16 真全量裁定 |
| 地图 | UnifiedLeafletMap（同 PC 点/热力/选择） | 复用 |

## 产物清单

- 新增：`src/views/viz/{EnterpriseVizPage,PanoramaVizPage,ServiceVizPage,VizSectionTitle}.vue`、`src/views/viz/vizPage.css`、`src/views/policy/{policyPortalModel.ts,PolicyPortalChainGraph.vue}`、`src/views/service/{SvcOrgProfileDrawer,svcProfileModel.ts,SvcPortalKeyOrgSection,SvcPortalKeyOrgDrawer,ServicePortalShenzhenPage}.vue` 等
- 重写：`src/views/policy/PolicyPortalView.vue`（紧凑版→六 Tab 全量）
- 修改：`src/router/index.ts`、`src/api/service/*`、`ServicePortalShell.vue`（export 修复）

## 验收证据

- `npx vue-tsc --noEmit -p tsconfig.app.json` → 0 错误（2026-11-16 本地）
- `npm test` → 49 pass / 0 fail（node:test 套件）
- `npm run build` → ✓ built in 10.54s（既有 preset chunk 体积警告，非本次引入）
- `VITE_APP_USE_MOCK=false`（.env.development/.env.production 均已定死）；全部数据走 gateway Java 真接口

## 架构合规自检（§2 铁律）

- ✅ 调用链：前端 → Java REST（gateway），无越层、无 demo-* 服务（D12）
- ✅ D8/D10：Arco/Vant 组件状态语义保留；主色 #165DFF token 一致
- ✅ D9：统计数字 ⓘ 走 StatCard metric-id / MetricMarker（reviewMode 门控）；诚实空态（暂无/缺字段说明），无伪数据
- ✅ USE_MOCK=false：零 fixture 填数
- ✅ 无新依赖（词云降级标签墙即为此）
- ✅ commit 规约：本机孔东裁定（2026-11-12），改动停工作区待人工 commit/push

## cost

- actual_tokens ≈ 520k（跨 2 会话累计，含 PC 真源通读）
- model_used: glm-5.3
- actual_cost ≈ $6.8
- cost_warn: green
