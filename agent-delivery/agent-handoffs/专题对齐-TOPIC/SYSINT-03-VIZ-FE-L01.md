# SYSINT-03-VIZ-FE-L01 · 可视化四菜单·按门户页复刻（不改门户四页）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 执行 `frontend-agent`。状态由 `in_progress` 改为 `integration`（联调中）。Java 实现单 `SYSINT-03-VIZ-API-L01` 仍由 `human:徐滕强` 监管，本 handoff 不改它的状态。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用门户已有地图、产业链图、企业搜索和已注册 ECharts。词云按页面要求加了仓内依赖 `echarts-wordcloud`。未改门户四页的路由、请求参数和交互。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本会话未使用 Headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无新增架构图。页面调用链仍是浏览器 → Java REST |
| 图 diff | 未改存储流图 |
| 会签态 | 无 |
| 说明 | 新读接口约定写在接口说明，不另画图 |

## 问题清单

- 原 DoD 要求缺数只留空态，并且不安装 `echarts-wordcloud`。2026-11-02 孔东要求先按全局 Mock 开关做出需规页面，再按页面整理 Java 接口。本单按后一口径交付。
- 关掉 `USE_MOCK` 后，没有新接口的块留空。本地 `.env.development` 把 `VITE_APP_USE_MOCK` 改成 `true` 只为查看页面，**未提交**。仓库默认仍是 `false`。

## 修改内容

四个菜单：

| 菜单 | 路由 | 页面 |
|---|---|---|
| 【管】-产业全景可视化 | `/industry-center/overview-viz` | `src/views/viz/panorama/PanoramaVizPage.vue` |
| 【管】-企业发展可视化 | `/enterprise/development-viz` | `src/views/viz/enterprise/EnterpriseVizPage.vue` |
| 【管】-产业服务可视化 | `/service/portal-viz` | `src/views/viz/service/ServiceVizPage.vue` |
| 【管】-政策新闻展示 | `/policy/news-display` | 仍是 `PolicyNewsDisplayPage.vue`，未新建第二套菜单 |

`USE_MOCK` 打开时，需规里这 4 个模块的 24 项交互都在页面上：规模与增长率、按密度着色的热力、环节占比、饼图、历史事件、情景滑块；企业搜索列表后的卡片导出、散点、按年收起的时间轴、财务三条线、SWOT、同行雷达；服务类型、供给疏密、需求、匹配、效能、案例；政策时间轴、重大事件抽屉、词云、聚类图、影响范围柱、影响深度折线。

企业列表复用 `entSearchQuery`。门户四页文件未改。`UnifiedLeafletMap` 只在点位自带 `heat` 时按密度铺色，不带该字段的地图仍是原来的统一热力。

Java 侧新接口收成 4 条，说明见 `可视化四菜单-Java接口清单.md`：`V-I`、`V-E`、`V-S`、`V-P`。旧的搜索、财务趋势、竞争力、产业总览、产业链快照、服务区域图、政策检索和各省政策量继续复用。

## 测试结果

- 本地 `https://localhost:3000`，`USE_MOCK=true`。
- 企业成长时间轴：三个年份为「展开」，最近一年为「收起」，点「展开」后该年事件出现。
- 产业热力画布同时有浅蓝和红色，颜色随密度变化；点开区域详情仍在。
- 服务热力同样有浅蓝、橙、红；表格有空白、正常、饱和。
- 政策重大事件点「查看详情与专家解读」后，抽屉分「详细内容」和「专家解读」。
- 主题聚类是关系图。点「低空经济」列出该簇三条；点「eVTOL 适航审定试点进展」后该条高亮。
- `eslint` 检查了改过的页面和模型文件，通过。`UnifiedLeafletMap.vue` 里原有的 `any` 和未使用变量未改。

## 遗留风险

- 新接口尚未由 Java 实现。关掉 Mock 后，散点、预测、SWOT、同行、服务类型与案例、词云、聚类、影响深度等块为空。
- 预测、SWOT 文字、同行归一化、政策事件和聚类要等 Python `/internal/*`，Java 无结果时应按接口说明把该块标空。
- 供给「空白 / 饱和」阈值是临时规则（`weight<8` / `>20`），口径登记后要改接口里的 `band_rule`。
- `echarts-wordcloud@2.1.0` 的 peer 是 echarts 5，本仓是 echarts 6，安装用了 `--legacy-peer-deps`。本地词云已画出。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`
- commit：`c2d32ee` `[agent:frontend-agent] 可视化四页按需规补齐展示`
- pipeline URL / ID：push 后由 GitLab CI 触发，本 handoff 落盘时尚未回填流水线号
- 部署 namespace / 镜像 tag：K8s dev，随该仓 `dev` 流水线
- K8s rollout：待流水线
- dev 测试 URL：本地 `https://localhost:3000` 四条路由见上表。线上地址随 lumen-ui-topic 的 dev 发布

编排仓本 handoff 与 `可视化四菜单-Java接口清单.md` 一并推 `origin/dev`。

## 可观测性（建议）

- 未新加前端埋点。页面仍走现有 `observability.ts` 请求链。
- 统计卡沿用已有 `ReviewMetricBadges` / `MockBadge`。Mock 数据块挂了 `MockBadge`。

## 涉及文件

lumen-ui-topic：

- `src/views/viz/**`
- `src/views/policy/PolicyNewsDisplayPage.vue`
- `src/views/policy/policyNewsDisplayModel.ts`
- `src/router/menu.ts`
- `src/components/map/UnifiedLeafletMap.vue`
- `src/config/echarts.ts`
- `src/types/echarts-wordcloud.d.ts`
- `package.json`、`package-lock.json`

未改：`IndustryOverviewPage.vue`、`EnterpriseDevelopmentPage.vue`、专题服务门户页、`ServicePortalIndustryCascader.vue`。

gkx-orchestration：

- `agent-delivery/agent-handoffs/专题对齐-TOPIC/可视化四菜单-Java接口清单.md`
- `agent-delivery/agent-handoffs/专题对齐-TOPIC/SYSINT-03-VIZ-FE-L01.md`

## 架构合规

| 项 | 结果 |
|---|---|
| 调用链 前端 → Java | 已接上的读数仍走 Java。Mock 数据在前端，关掉开关不用 |
| Java 不做算法 | 预测和 NLP 写明走 Python `/internal/*` |
| 图谱 Nebula | 本单不碰 |
| D8 Arco / token | 时间轴、抽屉、表格用 Arco；标题用已有 `search-section-title` |
| D9 ⓘ / Mock | 已有指标卡走 review 角标；演示块有 MockBadge |
| D12 不调 demo 服务 | 未配 demo 地址 |
| 门户四页 | 路由、请求参数、交互未改 |

## Cost 回填

没有 Console 精确数。按本会话量级估算。价表没有 Grok 档，沿用主力档（输入 $3/M、输出 $15/M，75/25）。

- actual_tokens: 320000
- model_used: grok-4.7
- actual_cost: 1.92
- cost_warn: green
- 计算：240000×3/1e6 + 80000×15/1e6 = 0.72 + 1.20

ponytail: full
