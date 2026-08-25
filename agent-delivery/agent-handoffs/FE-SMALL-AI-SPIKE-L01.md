# FE-SMALL-AI-SPIKE-L01 · AI 出效果试点（展示科技全域态势 + 专题企业发展）

> 目标仓：`lumen-ui-science-mobile`。裁剪真源：`FE-SMALL-AI-SPIKE-L01-裁剪与开工包.md`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| Owner | `human:孔东` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `lite`（开工包）；企业总览重建按 `full` |
| 说明 | 未用 YAGNI 跳过 D8 token、D9 MetricMarker（无 id 走红问号）、D10 底栏抽屉、可观测请求头、D12 网关。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP；spike 样板无需大日志。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改 Java/Python 调用链；前端仍 `/api` → 网关 |
| 会签态 | N/A |
| 说明 | 小屏裁剪样板，不改拓扑。 |

## 范围与实现

- 展示 `#/display/trend/tech-overall-situation`：结论条 + 底部 Tab（地图 / 要素 / 事件 / 分析）。地图：QuickFilter + Arco `a-select` 多选图层 + 地图/列表 + MapChrome。要素/事件走 ListCard + 全屏/半屏抽屉（要素详情对齐 demo L6 五块）。分析 Tab 才放论文/专利/机构/专家四卡（demo 首页没有这些卡）+ 要素规模柱 + 论文/专利双轴折线。
- 专题 `#/topic/enterprise-center/overview`：标题「企业发展」，对齐 demo E-32。底部 Tab（概况 / 分布 / 重点 / 深圳）。概况：产业下拉 + 三张 KPI（选定产业企业总数 / 科研人数 / 覆盖未来产业数，metric_id 已挂）+ 集群排名（最多对比 2）+ 2026–2031 趋势。分布：全球/全国/区域/深圳，点位半屏抽屉。重点：竞争力 TopN + 明星 ENT-0001/0006/0007/0004。深圳：历年趋势 + 总部含「深圳」名单。点企业全屏画像抽屉，Tab 对齐 `enterpriseSearchConfig.detailTabs`（工商概况 / 主要团队 / 资质荣誉 / 知识产权 / 经营财务 / 供应链关系 / 关系图谱边列表 / 舆情动态 / 风险待源 / 招投标待源）。
- 路由：`SPIKE_PAGES` 只挂上述两 path，其余导航仍 `PlaceholderView`。
- 共用：`StatCard` / `ListCard` / `QuickFilter` / `ProfileDrawer`（tabs）/ `UnifiedLeafletMap` / `MapChrome` / `PageTabs` / `BackToTop` / `SectionTitle` / `VChart`。
- 备忘：`docs/小屏AI出效果备忘.md`。

对照招标 / demo：小屏 = 中屏核心裁剪，不是整页搬 `App.jsx` / `DevelopmentOverview.tsx`。

## 偏离说明

- 展示总量四卡不在首页常驻，按监管人要求改到分析 Tab。
- 展示 StatCard 无登记 metric_id，走红问号，未伪造 8 件套。
- PC 有图块用 ECharts（监管人 2026-08-25）；本仓新增 `echarts` + `vue-echarts`，仍禁止 G6；关系图谱用边列表。
- 点省/点地区只开抽屉，不跳 PC 分析真页。
- 页内常量对齐 demo 预览样例，标「预览样例」，未走 `@/mock`；`USE_MOCK=false` 时无 fixture 填数。
- 不做对比篮、导出、PermGate、L0 二级产业框。
- NodePort `30896`（避开 admin 30893 / algo 30897），与 `FE-SMALL-SHELL-L01` 一致。

## 产物清单

- `repos/lumen-ui-science-mobile/src/views/display/trend/TechOverallSituationView.vue`
- `repos/lumen-ui-science-mobile/src/views/topic/enterprise/EnterpriseOverviewView.vue`
- `src/views/display/trend/previewSamples.ts` / `src/views/topic/enterprise/previewSamples.ts`
- `src/router/index.ts`（`SPIKE_PAGES`）
- `src/components/{BackToTop,PageTabs,SectionTitle,ProfileDrawer,StatCard}.vue`
- `src/components/map/MapChrome.vue` / `src/config/echarts.ts`
- `docs/小屏AI出效果备忘.md`
- `scripts/breakpoints.test.mjs`

## 验收证据（DoD）

| 条 | 结果 |
|---|---|
| 展示 1 页总览可演示 | ✅ 科技全域态势 |
| 专题 1 页可演示 | ✅ 企业发展（企业总览路由） |
| 可复用提示词/改法备忘 | ✅ `docs/小屏AI出效果备忘.md` |
| 开工包「要」清单可点 | ✅ 筛选 / 图层多选 / 复位 / 抽屉分 Tab / 下钻空壳仍占位 |
| ponytail lite / 企业 full | ✅ |
| Owner=孔东 | ✅ |

复刻五维：本叶是裁剪样板不是 Demo 1:1。R3 token `#D8E7FC`/`#165DFF`；R5 `USE_MOCK` 默认 false、无 fixture 填数。

## 测试结果

- `pnpm test`：8 passed（断点、无叠层、展示/专题菜单、预览路由、spike 两页映射、L6 抽屉、企业 KPI/画像 Tab）
- `pnpm type-check`：`vue-tsc --build` 通过（exit 0）
- 浏览器：监管人点选迭代（指标卡迁分析 Tab、图层改多选、企业 KPI 对照 demo）；本会话无浏览器 MCP，以 Vite 编译 200 + 本地 `pnpm dev` 为准

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 200000（in+out 估算；含两页重建与监管人改点，会话模型 Cursor Grok 4.6；source: session_estimate） |
| model_used | `claude-sonnet-4.5`（registry 枚举按 B 档口径） |
| actual_cost | 1.08（frontend 默认 80/20 × B 档 $3/$15 per M） |
| cost_warn | green |

## 遗留风险

- 展示四指标无 registry id，评审开时红问号属预期；`M_ENT_RESEARCHER_COUNT` 镜像可能缺，同样红问号，禁止手改 `readiness.generated.ts`
- 企业画像团队/供应链为占位 mock；风险/招投标保持待源文案
- K8s rollout / GitLab pipeline 以 push 后为准

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-ui-science-mobile` + `gkx-orchestration`）
- commit：`lumen-ui-science-mobile` `92d107fe1232d2278ee692a118254897c738a187`
- pipeline URL / ID：push 后 GitLab `lumen-ui-science-mobile` pipelines
- 部署 namespace / 镜像 tag：CI 触发后填写
- K8s rollout：push 后看 `http://192.168.88.50:30896`
- dev 测试 URL / 命令与结果：本地 `pnpm test`；`pnpm type-check`；`pnpm dev` → `#/display/trend/tech-overall-situation` 与 `#/topic/enterprise-center/overview`

## 可观测性

- 请求拦截器仍写 `X-Trace-Id` + `traceparent`（`src/utils/request.ts`）
- 本叶未加新埋点事件（开工包允许）
- Tempo / Loki：无本叶新配置

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 本仓无算法 |
| 2 调用链 前端→Java→Python | ✅ 仅 `/api` |
| 3 Nebula | ✅ 未引入 |
| 4 可观测 | ✅ trace 头保留 |
| 5 CI/CD | 🟡 push `origin/dev` 后看 pipeline |
| 6 demo 不污染 lumen | ✅ 只对照 demo 结构，未 merge |
| 7 方案 A / D12 | ✅ 仍走 `gkxlumen-platform-gateway` |
| 8 ADS | ✅ 页内预览样例，非 live |
| 9 D8 | ✅ token / Arco Vue；图层用 `a-select` 多选 |
| 10 D9 | ✅ StatCard → MetricMarker；无 id 红问号；有 id 走镜像 |
| 11 D10 | ✅ 底栏抽屉；未叠互斥 display |
| 12 D12 | ✅ 未调 demo 服务 |

## 涉及文件

- `repos/lumen-ui-science-mobile/src/views/display/trend/TechOverallSituationView.vue`
- `repos/lumen-ui-science-mobile/src/views/topic/enterprise/EnterpriseOverviewView.vue`
- `repos/lumen-ui-science-mobile/src/router/index.ts`
- `repos/lumen-ui-science-mobile/src/assets/main.css`
- `repos/lumen-ui-science-mobile/docs/小屏AI出效果备忘.md`
- `repos/lumen-ui-science-mobile/scripts/breakpoints.test.mjs`
- `agent-delivery/agent-handoffs/FE-SMALL-AI-SPIKE-L01.md`
- `agent-delivery/agent-handoffs/FE-SMALL-AI-SPIKE-L01-裁剪与开工包.md`

## 问题清单

- spike 完工路径：`in_progress` → `ready_to_sign`（待 `human:淮政玮` 签收）
- 丽影改专题页时不要动 `src/views/display/**`
