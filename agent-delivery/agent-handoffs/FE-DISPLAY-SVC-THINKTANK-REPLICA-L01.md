# FE-DISPLAY-SVC-THINKTANK-REPLICA-L01 · 智库服务 5 Tab 复刻 + IframeDetailModal + D9 血缘

> WBS-05-07-07；父任务 `SYSINT-05-07-L01`。仓：`repos/lumen-ui-science-pc`。
> demo 真源：`repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx`（ad51a5e）+ `thinkTankModel.js`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:李伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-11-06 用户裁定 05-07 八子任务监管一律沿用李伟；前端执行由孔东负责。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 `InsightDetailDrawer` 兜底、`src/review/` 评审层、`VChart` 注册表、`../styles/demo-tech-service.css` 通用类；不新增依赖、不引入 mock 种子。 |

## Headroom（可选）

| 字段 | 值 |
|-----|-----|
| headroom | `skip` |
| 说明 | 逐页复刻，未走 Headroom 代理。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶只做前端复刻，不改架构图 / 存储流图 / 接口契约图；接口契约以 05-07-01 登记的 ZK-01～ZK-09 与 Java BFF `/v1/think-tank/**` 为准。 |
| 会签态 | 不适用（契约侧由 05-07-01 单独签收） |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | `templates/handoff-template.md` |
| 页面真源 | `ThinkTankService.jsx` + `thinkTankModel.js` + `style.css`（demo，只读对照） |
| 派单与裁定 | `派单说明/派单-SYSINT-05-07-THINKTANK-REALDATA-L01.md`；`对接文档/我方/2026-11-06-智库服务-B1-B5-裁定函.md`、`...-D1-D5-决策函.md` |

## 实现范围

- 路由 `/service/think-tank-service`（`src/router/menu.ts`，惰性加载）；菜单项沿用既有 `navItem('service','think-tank-service','智库服务','think-tank')`。
- 5 Tab：服务类型 / 智库报告 / 智库活动 / 智库专家 / 智库成果；筛选：服务类型、主题、时间范围、时间标签（专家 Tab 停用时间筛选）。
- 4 图表（`VChart`，容器显式高度 220px）：成果·案例·建议饼图、时间趋势折线、按服务类型柱、按主题柱。
- 右侧 3 信息流：重大事件 / 成果发布 / 政策建议（`SideFeed.vue`，第 2 处出现即封装）。
- 分页：5 Tab 共用 `ListPager.vue`，单页 10 条，`total ≤ 10` 不显示。
- 详情：`IframeDetailModal` 站内 iframe 弹框（80vw×80vh、`mask-closable=false`、骨架 loading）；`detailUrl` 为空回落 `InsightDetailDrawer`；活动走 `POST /activities/detail` 合并 7 项问卷汇总；对端禁嵌由弹框右上角「在新窗口打开」降级。
- 数据：只调展示 Java BFF `/display/v1/think-tank/**`，不直连对端、不自带 token；`source=not-configured` / `ZK_NOT_CONFIGURED` 显示「接口待接入」空态，其余 `ZK_*` 汇总到顶部 `a-alert`。

## 与派单 / demo 的差异（需评审知悉）

1. **100 条快照 + 客户端筛选**：BFF `pageSize` 上限 100，demo 为全量客户端筛选；为保证服务类型 / 主题 / 时间标签 / 时间范围的组合筛选与 demo 一致，首屏取 `pageSize=100` 快照后在客户端过滤、本地分页。超过 100 条的档案不在本页统计口径内，已在 ⓘ 口径中写明「当前样本派生」。
2. **`/achievements/stats` 已封装未消费**：聚合口径需与 demo 的 `buildAggregate` 一致（按当前筛选样本派生成果/案例/建议），统计端点改成服务端聚合会与 demo 视觉不一致，故本页未调用；接口封装保留在 `src/api/service/thinkTank.ts`，08 联调时可按需切换。
3. **IframeDetailModal 新路径**：派单要求落 `src/components/IframeDetailModal/`；仓内已有 `src/views/service/components/DetailIframeModal.vue`（3 页共用）。本次按派单新建通用件、仅智库页使用，**不重构**既有 3 页，避免越界改动；后续若统一，再单独立单迁移。
4. **无四维就绪度角标（D9 诚实性）**：`DS-30-THINKTANK` 的 `metric_open_status=missing` 且指标清单明确「禁止发明 M_*」，本页数字全部由外部接口列表派生或取自分页 total，没有正式 `metric_id`。按决策函 N5，不挂 D1-D4 角标、不挂 MockBadge，改为统计数字旁 ⓘ 口径说明（`src/review/thinkTankLineage.ts` + `ThinkTankLineageHint.vue`，自闸 `review.reviewMode`）。
5. **服务类型 5 类为运营临时目录**：`policy_research` / `strategy_consulting` / `evaluation` / `talent_training` / `academic_exchange`；后端临时映射（报告 1/2→政策研究、3→战略咨询；成果→战略咨询）待对端主档下发改回。服务类型计数只派生、不作指标。
6. **专家不展示 H 指数 / 引用量**（D2 裁定）；成果敏感三字段（`actual_investment` / `roi_percent` / `satisfaction`）后端已剥除（B4 裁定），前端不补造。
7. **活动详情只显示 7 项问卷汇总**，问答正文不入页面。

## 测试结果

- `.\node_modules\.bin\vue-tsc.cmd --build`：**新增/修改文件 0 报错**；仅剩既有基线错误（未触碰，见下）。
  - `src/api/situation/panorama.ts(35,16)` `optionalPost` 未定义
  - `src/api/situation/shenzhenInnovation.ts(59,3)/(74,3)` `fundingAmountCny` 重复声明
  - `src/views/situation/bay-innovation/tabs/OverviewTab.vue(666/803)` `flylineRelationConfig` 不存在
  - `src/views/situation/shenzhen-innovation/tabs/CompareTab.vue(227,51)` EChartsOption 类型不匹配
  - 说明：本机 Node v20.18.0 低于 `engines.node`（^20.19.0 || >=22.12.0），`pnpm type-check` 被 pnpm 引擎检查拦截，改用 `node_modules/.bin/vue-tsc.cmd --build` 空跑。
- `.\node_modules\.bin\vite.cmd build`：**退出码 0**，构建成功（仅 Node 版本提示与 unocss/browserslist 警告，非阻塞）。
- 浏览器实测（`http://localhost:3000/service/think-tank-service`，本地 dev server）：
  - 页面标题「智库服务」、筛选栏（服务类型/主题/时间范围/时间标签）、5 个 Tab、4 个图表卡、右侧 3 个信息流卡全部渲染，无白屏、无红色 JS 报错。
  - 5 个 Tab 逐个切换正常，无崩溃。
  - 清空 `localStorage.lumen-review-mode` 后刷新，正文未出现 `metric_id` / `GAP-` / `就绪度` / `口径说明` 等评审字样，5 Tab 仍在 —— **DOM 零泄漏 PASS**。
  - 本地展示 Java（`127.0.0.1:7099`）对 `/display/v1/think-tank/**` 当前返回 401（本地实例未含智库端点），页面按设计显示顶部「部分接口暂不可用」+ 空态；真实数据三态待 08 联调验收。

## D9 附录 D 防漏扫描摘要

| 项 | 结论 | 依据 |
|----|------|------|
| D.1 页面差集 | 通过 | DS-30 智库页唯一；demo 5 Tab + 4 图表 + 3 信息流 + 筛选/分页/详情全部落地，无缺页。demo 顶部 KPI（总成果/总投资/回报率/满意度）属 03-高端智库需规，566-574 范围外且已在 demo 侧移除，本页不建。 |
| D.2 本地 KPI 接线 | 通过 | 页面无 KPI 卡；服务类型计数、3 类聚合、时间趋势、按服务/主题分布全部由接口快照派生，无本地硬编码数值；服务类型 5 类是运营目录常量（非指标），已由 ⓘ 说明。 |
| D.3 镜像 vs 矩阵 | 通过（白名单） | 本页**不引入** `readinessSeed` 镜像：DS-30-THINKTANK `metric_open_status=missing`、禁止发明 `M_*`；按 D9「禁止自填」，以 ⓘ 口径替代四维角标（决策函 N5）。 |
| D.4 错挂 / 正名 | 通过 | 未挂 MockBadge / SchemaGapBadge / PendingBadge / IngestingBadge；未把外部接口字段错挂为本地指标；`kind='think-tank'` 已登记到 `InsightDetail` 联合类型。 |
| D.5 契约防漏 | 通过（1 项声明） | 9 端点中 8 个被页面消费：`/reports`、`/achievements`、`/enums`、`/activities/page`、`/activities/detail`、`/experts/page`、`/experts/field-options`、`/major-events/page`；`/achievements/stats` 已封装未消费，原因见「与派单 / demo 的差异」第 2 条，非漏接。 |

## 遗留风险

- 100 条快照上限：对端档案总量超过 100 时，本页统计只覆盖前 100 条（按报告发布时间 / 成果默认序）。08 联调若发现总量超限，需改为服务端分页 + 服务端聚合，届时统计口径需与 PM 确认。
- 真实数据三态（有 `detail_url` 嵌入 / 空 `detail_url` 兜底抽屉 / 对端禁嵌降级）尚未在真链路实测，依赖 05-07-04 白名单回函与 05-07-08 联调。
- `IframeDetailModal` 与既有 `DetailIframeModal` 并存，存在后续统一成本（已声明差异，不在本叶重构）。
- 本地展示 Java 未含智库端点时统一 401，页面按「接口不可用」展示；与「待接入」空态（`ZK_NOT_CONFIGURED`）在 UI 上可区分（前者顶部告警、后者空态文案「接口待接入」）。

## CI/CD（必填）

- 分支：`lumen-ui-science-pc` → `origin/dev`（**未推送**）
- commit：无。按仓规「提交推送默认人工确认（用户裁定 2026-11-05）」，改动停在本地工作区，等当前会话用户明确确认后再 commit + push；提交信息将带 `[agent:frontend-agent]`。
- pipeline URL / ID：待推送后触发
- 部署 namespace / 镜像 tag：以 CI 产物为准
- 本地验证命令：`.\node_modules\.bin\vue-tsc.cmd --build`、`.\node_modules\.bin\vite.cmd build`、`http://localhost:3000/service/think-tank-service`

## 可观测性（建议）

- OTEL_SERVICE_NAME：无（前端静态页）
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

新增：

- `repos/lumen-ui-science-pc/src/api/service/thinkTank.ts`
- `repos/lumen-ui-science-pc/src/views/service/think-tank/index.vue`
- `repos/lumen-ui-science-pc/src/views/service/think-tank/model.ts`
- `repos/lumen-ui-science-pc/src/views/service/think-tank/ListPager.vue`
- `repos/lumen-ui-science-pc/src/views/service/think-tank/SideFeed.vue`
- `repos/lumen-ui-science-pc/src/views/service/think-tank/styles.css`
- `repos/lumen-ui-science-pc/src/review/thinkTankLineage.ts`
- `repos/lumen-ui-science-pc/src/review/ThinkTankLineageHint.vue`
- `repos/lumen-ui-science-pc/src/components/IframeDetailModal/index.vue`

修改：

- `repos/lumen-ui-science-pc/src/review/index.ts`（导出智库 ⓘ 口径与组件）
- `repos/lumen-ui-science-pc/src/components/drawer/detailModel.ts`（`InsightDetail.kind` 增 `'think-tank'`）
- `repos/lumen-ui-science-pc/src/router/menu.ts`（`think-tank-service` 惰性组件映射）
- `gkx-orchestration/agent-delivery/agent-handoffs/FE-DISPLAY-SVC-THINKTANK-REPLICA-L01.md`（本文件）
