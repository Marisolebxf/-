# LUMEN-SVC-FE-WORKSPACE-VISUAL-C1 · 产业服务链 WORKSPACE 视觉复刻

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：ENTRY 视觉、E1 金路径伪绿、React merge 进 Vue、伪造未白名单 Job KPI。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用「轻量/空壳」跳过 Demo 上下文条/页签/过程与结果骨架；对照 Demo class + `serviceCenter.css` + CHAIN 过程壳。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对齐 demo service-center WORKSPACE 四页；禁止 compress 代替对照。 |

## 范围与实现

`lumen-ui-topic` 纠正 WORKSPACE 视觉降级：四页按 `demo-ui-topic` 已评审结构复刻。数据可空，**UI 结构不可砍**。只调 Java `analysisTask` + `/svc`（D12）。

### 机构分析 `/service/institution-judgment`

- 三 workspace（field/trend/capability）由侧栏 query 驱动；页内「当前分析 + 分析记录」双 Tab
- `svc-context-bar`（领域 / 已选机构 / 对比篮 CTA）+ `svc-metrics-strip`
- Coverage：热力/矩阵切换 + 图表区骨架 + `svc-conclusion-grid`
- Trend：时间窗 + 折线骨架 + `svc-heat-panel`
- Capability：`svc-eval-dims` 权重配置 + 对比篮对象 + 排名/雷达结果壳
- Job 未白名单：idle gate「开始分析」仅提示；禁止只 Alert+Empty

### 生态 `/service/chain-analysis`

- 双 Tab；上下文条产业领域
- **短板**：保留 Java `svc:analysis:shortboard` + `IndustryAnalysisProcessShell`；结果补地铁轨道图 `svc-eco-metro` + 瓶颈面板 + 清单表
- **图谱**：关系/节点过滤 `svc-eco-graph-filters` + 图区骨架（不伪跑）
- **深圳**：评价框架 + 指标多选 + `svc-eco-compare-grid` + 梯队仪表盘骨架

### 招引/培育 `/service/institution-decision`

- 双 Tab；上下文条重点产业方向
- Attract：固定权重 Tag + 生成按钮 + `svc-rank-row` 名单壳（诚实空）
- Cultivate：机构类型/环节筛选 + 权重 + 培育建议结构壳

### 维护 `/service/maintenance`

- 左栏 15 项分区导航（内容运营/图谱运营/分析配置）
- 门户工作台：视图切换 + 类型筛选 + 表壳（写侧 disabled）
- 其它分区：占位 Descriptions 壳

## 视觉验收 V1–V7

| # | 项 | 结果 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | ✅ 四页 workbench / maintenance |
| V2 | 检索 Hub Hero（本叶非 ENTRY） | ✅ N/A（ENTRY 已在 `9ae4d87`）；本叶工作台对齐 Demo `svc-workbench` |
| V3 | 卡片/列表内部标题+摘要横向；操作不漂 | ✅ `svc-rank-row` / metro station body / context-bar tags flex |
| V4 | 一个节点一套 layout；不叠 result-card 网格 | ✅ 无 `industry-search-result-card`；用 Demo `svc-*` class |
| V5 | `min-width: 0` 仅在 flex 子项截断处 | ✅ rank-row 正文列 `min-width:0`；context tags `min-width:240px` |
| V6 | 空态诚实；有结构则保留配置/结果骨架 | ✅ 无数 Empty；配置区/地铁/过滤器/名单壳完整保留 |
| V7 | 不叠互斥 result-card class | ✅ selfcheck 断言 |

## 偏离说明（as-built）

| 项 | Demo | As-built | 理由 |
|---|---|---|---|
| 栈 | Arco React | Arco Vue | 禁止 React merge；语义+布局对齐 |
| 机构/推荐 Job | Demo 本地 systemTask | 诚实空 + Message；结构保留 | Java 白名单仅 shortboard |
| 图谱/深圳结果 | Demo Mock 图/柱 | 配置+骨架空 | 不伪跑、不伪造 KPI |
| 维护写侧 | Demo 本地状态机 | 按钮 disabled | OPS 另单；结构对齐 |

## 产物清单

| 产物 | 路径 |
|---|---|
| FE commit（结构壳） | `repos/lumen-ui-topic` `8b6c615d175883609bbdb1214daf97a604a99c0f` |
| FE commit（样式/404 监管返工） | `repos/lumen-ui-topic` `6d413fa` · `fix(svc): SearchHub hero skin + route 404 guards [agent:frontend-agent]` |
| 四页 | `src/views/service-center/Service{OrgAnalysis,ChainAnalysis,Recommend,Maintenance}Page.vue` |
| CSS | `src/views/service-center/serviceCenter.css` · `src/assets/search-workspace.css`（`.svc-org-search-page` Hero） |
| 配置 | `src/config/svcWorkspace.ts` · `serviceMaintenanceConfig.ts` |
| selfcheck | `src/utils/svcWorkspaceVisual.selfcheck.mjs` · `serviceOrgSearchModel.selfcheck.mjs` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-WORKSPACE-VISUAL-C1.md` |

## 监管返工（2026-08-17 · 样式白壳 / 页面 404）

| 根因 | 修复 |
|---|---|
| SearchHub Hero 背景只挂 `.enterprise-search-page` / `.industry-search-page`，查询根 class 为 `.svc-org-search-page` → 白壳 | `search-workspace.css` 选择器并入 `.svc-org-search-page`；查询页根同时挂 `enterprise-search-page` |
| `navItem` 跨组 `routeName=maintenance` 撞名；侧栏 `router.push({name})` 可能串页/异常 | `svc-maintenance` 唯一 routeName；`DefaultLayout` / 门户 Tab 改 **path** 跳转 |
| 裸 `/service-portal`、误写 `/service/search` 无注册 → SPA 404 | `routes.ts` redirect → overview / `svc-search`；对比篮只走 `/service-center/search` |
| API `/svc/topic/v1/**` | 契约路径正确（网关 `Path=/svc/**` + GlobalFilter StripPrefix=1 → 服务内 `/topic/v1/**`）。本机未起 gateway，**不**宣称集群 API 绿 |

**CSS 挂载确认**：`main.css` → `search-workspace.css`；查询页 `serviceOrgSearch.css`；门户 `servicePortal.css`；工作区 `serviceCenter.css`（均已 import）。门户 Tab 用 `global-workbench-tabs`（同文件皮肤）。

## 验收证据

| 项 | 结果 |
|---|---|
| selfcheck | ✅ `node src/utils/svcWorkspaceVisual.selfcheck.mjs` |
| search selfcheck | ✅ `node src/utils/serviceOrgSearchModel.selfcheck.mjs`（含 `.svc-org-search-page` 选择器断言） |
| shortboard selfcheck | ✅ `node src/utils/svcAnalysisTask.selfcheck.mjs` |
| type-check | ✅ `npm run type-check` |
| D12 | ✅ 仅 Java analysisTask + `/svc`；无 demo-* |
| 禁止纯 Alert+Empty 宣称完成 | ✅ 四页均含 Demo 级结构壳 |
| push | ✅ `origin/dev` @ `6d413fa` |

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 前端 → Java REST | ✅ shortboard analysisTask；查询/门户既有 `/svc` |
| 3 | Nebula | ✅ 图谱仅壳，不直连 |
| 4 | 可观测 | ✅ request `X-Trace-Id`；TraceInfoIcon |
| D8/D10 | Arco + Design token / svc-* class | ✅ |
| D9 | metric_id + Q-SVC-010 诚实空 | ✅ ReviewMetricBadges |
| D12 | 禁 demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~18 万（含监管返工本轮） |
| actual_cost | 估 <$10 |
| cost_warn | false |

## 联调确认

**联调通过 / 联调确认**：WORKSPACE 四页结构对齐 Demo；ENTRY SearchHub Hero 选择器已覆盖 `.svc-org-search-page`；侧栏/门户 path 跳转 + 深链 redirect 防 SPA 404。短板仍经 Java analysisTask；其余工作区诚实空+完整壳。集群 `/svc` 真调依赖 gateway+topic-svc 发布，本 agent **不**伪绿。下一叶：段 E / 签收。本单转 **integration**，不标 done。
