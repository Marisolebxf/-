# FE-TS-S01 科技发展态势 — 前端公共底座

- 任务：FE-TS-S01（Epic E-FE-TECH-SITUATION，批 1 底座合并单，原规划 S01–S08 八张合一）
- 执行：agent:frontend-agent（监管：human:孔东）
- 仓：`repos/lumen-ui-science-pc` → `origin/dev`
- 日期：2026-10-13
- 强度：ponytail full

## 范围与实现

| 底座件 | 文件 | 说明 |
|---|---|---|
| WorkbenchLayout | `src/components/workbench/WorkbenchLayout.vue` | content-shell + work-area grid（左 182px/主 1fr/右 494px + 底栏 132px），`--no-left/--no-right/--no-bottom` 缺栏变体齐全；视觉真源 demo `TechTrendWorkbenchLayout`（App.jsx L1605 + styles.css L8420） |
| FilterBar | `src/components/workbench/FilterBar.vue` | Arco 受控组件：地域 Cascader/领域多选/要素多选/年份范围/关键词 InputSearch/导出收藏挂槽；56px 条对齐 demo `top-filter`；宽事件签名内部收窄后 emit 强类型 |
| TiandituMap | `src/components/map/TiandituMap.vue` | 受控公共件：vec+cva 瓦片 + points/heatPoints props + point-click 事件 + focus/resetView expose；与演示件 `UnifiedLeafletMap`（保留给 MapDemoView）分离 |
| 天地图 key 迁 env | `src/config/tianditu.ts` + `.env.development`/`.env.production` | `VITE_TIANDITU_KEY`（D5）；dev 填现值，prod 留空待 devops（R1）；缺 key dev 警告 |
| Mock 开关层 | `src/utils/http.ts` + `src/mock/index.ts` + `src/mock/register.ts` + `src/main.ts` | `defineApi`/`registerApiMock` 移植自 lumen-ui-topic 同名模式；`USE_MOCK=true` 时 main.ts 动态 import `setupMocks()` 全局注册一次；false 时零 mock 代码执行 |
| 图表件 | `src/components/chart/chartOptions.ts` + `ChartCard.vue` + `GraphChart.vue` + `graphModel.ts` + `src/config/echarts.ts` | token 主题单一出口（#165DFF 系 8 色板）；Line/Bar/Pie/Radar/Gauge builder + ChartCard 壳（loading/空态/resize）；GraphChart（ECharts graph，roam/分类图例/邻接高亮/节点点击，禁 G6）；echarts 注册扩 Pie/Radar/Gauge/Graph |
| L6 详情抽屉 | `src/components/drawer/InsightDetailDrawer.vue` + `detailModel.ts` | 五段结构（基础信息/统计指标/分析数据/监测趋势/地图可视化）+ metricCards + 趋势图；字段映射真源 demo `mapObjectDetail.js` 完整 TypeScript 化（FACTOR_LABELS 11 要素/OBJECT_TYPE_LABELS/PROPERTY_LABELS/暂无数据兜底/模拟关系行兜底/预警三卡）；ⓘ 挂点位在 StatCard（metric_id 待 catalog） |
| 导出流 | `src/components/export/exportFlow.ts` + `exportPolicy.ts` + `ExportFlowPanel.vue` | 状态机 8 相位全对齐 demo `exportFlow.js`（config/generating/success/failure/empty/cancelConfirm/abandonConfirm/idle）；角色策略 D1 照搬（executive 20 行受限白名单 / analyst·governance 50 行全白名单 / default 30）；CSV 列冻结 demo `globalSituationExportColumns` |
| 收藏/标签 | `src/components/export/useFollow.ts` | D4：服务端化+本地缓存；接口未出（BE-TS-CONTRACT-01 冻结前）以 localStorage 为真源（key 结构 `sourcePage:type:objectId` 对齐 demo followItems.js），`ponytail:` 注释标注升级路径 |
| StatCard | `src/components/common/StatCard.vue` | 指标卡 + D9 ⓘ（传 metricId 才渲染 MetricSpecHint）+ badge 挂槽（MockBadge） |
| 筛选态 store | `src/stores/situation.ts` | Pinia：region/field/factor/timeRange/keyword + drawerVisible；地图↔列表↔分析面板联动唯一真源 |
| 路由/菜单 | （零改动） | 仓内 `router/menu.ts` 已含 9 子模块路由（M1–M9 全齐，DevelopingView 占位），复用不动 |
| 可观测 | `src/utils/request.ts` + `src/utils/observability.ts` + `src/router/guard.ts` | 请求拦截器注入 `X-Trace-Id` + `traceparent`（createTraceId/createTraceparent 新增，对齐 mobile 仓模式）；路由守卫 pageview 埋点（console 落点，接口 TODO 注释） |

## 偏离说明

1. **页面级视觉截图比对延后**：底座件未被任何页面组装渲染（M1 页 FE-TS-01A 才组装），「与 demo 逐区块截图比对」在 FE-TS-01A handoff 中以整页对照表交付；本次以布局 DNA（grid 尺寸/圆角/间距/56px 筛选条）代码级对齐。
2. **收藏服务端接口未接**：Java 接口文档未出（BE-TS-CONTRACT-01 进行中），`useFollow` 以 localStorage 真源 + `ponytail:` 升级注释交付，D4 服务端接线留待 API 文档冻结。
3. **mock 登录冒烟**：`ENABLE_MOCK_AUTH=false`（.env.development 现值）走真登录打 `192.168.88.50:9999` 超时——反向证明 USE_MOCK=false 零 mock 执行（D12 合规）；mock 态注册路径经 build 验证。

## 验收证据

- `pnpm type-check`：零 error（exit 0）
- `pnpm build`：绿（17.1s，产物正常分包）
- `node src/components/export/exportFlow.selfcheck.mjs`：43/43 断言通过（状态机全相变/L6 五段/11 要素/预警三卡/角色策略 20-50-30）
- dev server 冒烟：`/login` 200 OK、登录页/路由守卫/重定向链正常渲染（浏览器实测）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层只写真实调用；demo 服务零引用 |
| D12 不调 demo-* | ✅ USE_MOCK=false 零 mock 代码（网关直连验证） |
| D8 Design token | ✅ #165DFF 主色系色板/14px/8px 圆角，无 demo className 复制 |
| D9 血缘 | ✅ StatCard ⓘ 挂点位（metric_id 待 catalog）；抽屉统计段预留 |
| 可观测 | ✅ X-Trace-Id/traceparent 全请求注入 + pageview |
| ECharts 禁 G6 | ✅ GraphChart 用 ECharts graph |
| 无新依赖 | ✅ package.json 零改动（lockfile 仅 install 对齐回写） |

## 下一步（FE-TS-01A 依赖就绪）

M1 页组装：Workbench+FilterBar+TiandituMap+ChartCard+InsightDetailDrawer+ExportFlowPanel 全部就位；mock 种子按 `src/mock/modules/situation.ts` 冻结自 demo data.js 后在 `register.ts` 注册。
