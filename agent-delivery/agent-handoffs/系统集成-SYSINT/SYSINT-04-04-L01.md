# SYSINT-04-04-L01 · 门户企业发展展示页

> **任务**：SYSINT-04-04-L01（`task_type=feature`，E-PM-DELIVERY，WBS-04-04）
> **执行**：`human:孔东` · **监管**：`human:孔东`
> **仓库**：`lumen-ui-topic`（门户页）；专题 Java 本阶段无新增提交，联调沿用既有企业专题 REST
> **日期**：2026-10-26 · **强度**：ponytail full
> **ponytail:** full。复用专题服务门户产业级联与地图组件；指标旁保留评审层 MetricBadges；`USE_MOCK` 时走 registerApiMock，非 mock 禁止 fixture 冒充实数。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-10-24 开工。2026-10-26 推进至 **integration（联调中）**；接口字段对齐与联调优化留后续迭代，**本 handoff 不标联调通过**。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 四页签对齐 Demo `enterprise-center/overview` 信息架构；未另起 UI 栈。共享 `ServicePortalIndustryCascader` 与 `servicePortal.css`。 |

## 问题清单

- 需规 75–78 四块内容已落四个页签壳子与主要图表/列表；与 Java 真实字段、空态、分页边界仍在联调中打磨。
- 统一用户中心相对路径菜单注册属 `SYSINT-04-06-L01`，本叶仅在智树侧栏挂 `【门】-企业发展` 便于本地走查。
- 不是 WBS-03-05（运维可视化）；不与 CMS 运营页混用。

## 修改内容

| 区域 | 说明 |
|------|------|
| `EnterpriseDevelopmentPage.vue` | 四页签：整体概况 / 重点企业全景 / 明星企业 / 深圳企业；`?tab=` 切换 |
| `DevelopmentOverviewPanel.vue` | 产业 KPI、对比趋势、全球/全国/区域/深圳分布地图与列表 |
| `KeyEnterprisesPanel.vue` | 产业链上中下游重点企业、资质与规模结构 |
| `StarEnterprisesPanel.vue` | 明星企业档案、产品分页、团队与合作网络 |
| `ShenzhenEnterprisesPanel.vue` | 深圳数量、领域、规模、增长趋势与重点企业 |
| `portalFormat.ts` / `enterpriseDevelopment.css` | 门户页图表色与布局 token |
| `menu.ts` | 注册 `【门】-企业发展` 路由 |
| `ServicePortalIndustryCascader.vue` 等 | 与专题服务门户共用的产业路径选择；mock 目录 `portalAggregates` / `topicApiCatalog` 补企业发展门户块 |
| `stats-featured.ts` | 明星/深圳等类型与接口形状对齐（联调待续） |
| `UnifiedLeafletMap.vue` | 门户分布图小修（与 04-04 地图联调相关） |

数据路径：面板内调用 `@/api/enterprise` 既有 stats / featured / shenzhen 等 Java REST；浏览器不直连 Python。

## 测试结果

- `node src/views/service/servicePortalOverview.selfcheck.mjs` 通过（产业路径序列化回归）。
- 本地走查：四页签可切换；`USE_MOCK=true` 下各面板有数。真接口联调与字段差异修正 **未完工**。

## 遗留风险

- 部分接口响应字段与 UI 展示仍可能对不齐，需与专题 Java 对照 OpenAPI/实网逐项改。
- 缺数、超时、部分 metric 未就绪时的空态与角标需联调轮次补全。
- K8s dev 未在本 handoff 单独验收；待 CI 绿后由监管人走查门户相对路径嵌入场景。

## CI/CD

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`4a4977d4206ee850ba0c47ffc26bb1d49344af99`（`feat(portal): 门户企业发展四页签初版 [human:孔东]`）
- pipeline URL / ID：（待 CI 触发后补）
- 部署 namespace / 镜像 tag：随 `lumen-ui-topic` dev CI
- K8s rollout：待 pipeline
- dev 测试 URL：智树 dev 环境 `【门】-企业发展` 菜单（相对路径以 `SYSINT-04-06` 为准）

## 可观测性

- 页面请求经既有 `observability.ts` 封装；本叶未新增独立 OTEL 服务名。

## 架构合规

| 铁律 | 结果 |
|------|------|
| 调用链 前端 → Java REST → Python | 符合。页面只调企业专题 Java API |
| D8 Arco + 仓内 token | 符合 |
| D9 统计数字旁 ⓘ / 评审角标 | 符合（`ReviewMetricBadges`） |
| D12 不调用 demo 服务 | 符合 |
| 普通用户页，非 WBS-03-05 运维可视化 | 符合 |

## 2026-10-26 走查：产业筛选与趋势

监管人走查后的页面调整，仍在联调中，**不标联调通过**。

- 页顶「选择产业」对齐 demo 横排卡片，控件仍用 `ServicePortalIndustryCascader`。无 `industry` 参数时默认第一个一级集群。
- 明星企业、重点企业两个页签不显示页顶筛选。明星企业页产业级联与明星企业下拉同一行；重点企业页级联放在「重点企业 N 家」前。
- 企业整体概况排名可多选对比，不再限制两个产业。
- 深圳企业趋势按所选产业分线（`shenzhenIndustryTrend.ts`）。接口未返分产业序列时按当年企业数比例生成演示曲线，文件内有 ponytail 注释。
- 四页签产业路径由 `enterpriseDevelopmentIndustry.ts` 写入 URL `industry`。

本地未跑完整构建。`.env.development` 的 `VITE_ENABLE_MOCK_AUTH` 为个人环境，未纳入提交。

- 分支：`lumen-ui-topic` `dev`
- commit：`a9bf61d85bdd46a26b28cef16d66f1821f8da1b4`（`fix(portal): 企业发展四页签产业筛选与趋势走查 [agent:frontend-agent]`）
- pipeline / K8s：未 push，待监管人确认后再推 `origin/dev`

## 涉及文件

- `repos/lumen-ui-topic/src/views/enterprise/development/**`
- `repos/lumen-ui-topic/src/router/menu.ts`
- `repos/lumen-ui-topic/src/views/service/ServicePortalIndustryCascader.vue`
- `repos/lumen-ui-topic/src/views/service/servicePortalIndustryScope.ts`
- `repos/lumen-ui-topic/src/mock/enterprise/portalAggregates.ts`
- `repos/lumen-ui-topic/src/mock/enterprise/topicApiCatalog.ts`
- `repos/lumen-ui-topic/src/api/enterprise/types/stats-featured.ts`
- `repos/lumen-ui-topic/src/components/map/UnifiedLeafletMap.vue`
