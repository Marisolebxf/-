# FE-TOPIC-SMALL-CHAIN-GAP-L01 · 专题小屏·产业分析差距完善（报告链路/深链/企业跳转/模板与记录删除/D9 角标）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent`（派单对象 human:孔东，本人会话直接执行） |
| supervised_by | `human:孔东` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 问题清单

对照 `lumen-ui-topic`（PC）产业分析模块逐项盘点小屏缺失，缺口共 8 项：

1. 报告/结果资产下载与新窗打开（`analysisTaskAssetDownload` / `analysisTaskAssetOpen`）未移植，任务完成后无法查看报告附件。
2. `/industry-center/results/:resultId`、`/industry-center/reports/:reportId` 深链落在 `NotAdaptedView` 兜底页。
3. 全景图谱节点详情抽屉「代表企业」纯文本展示，不可点、不跳企业详情。
4. 区域评价「我的模板」无删除入口，端点 `regionalTemplatesMineDelete` 未移植。
5. 分析记录无删除入口，端点 `analysisTaskDelete` 未移植。
6. 产业分析各视图 StatCard 未挂 metric-id（D9 就绪度角标缺载体）。
7. 产业查询页未接 `chainSearchBizExamplesList` 查询示例词。
8. PC 端块级报告文档模型（blocksOf 8 类）在小屏无对应实现，报告阅读只能依赖外部附件。

## 修改内容

### 报告链路（#106）

- **新建 `src/utils/chainBlockReportDocument.ts`**：轻量版块级报告文档构建器（不引 PC 端重依赖），复用小屏已有解析器（`parseCycleBoard` / `parseKeyLinkStages` / `parseBottleneckLinks` / `parseRegionalBoard` / `parseShenzhenBoard`）把任务 payload 分发为 KPI / 文本 / 表格 / 排名条块（8 类分发键与 PC `blocksOf` 对齐），报告 ID 由 `stableReportHash` 确定性生成。
- **新建 `src/components/visualization/ChainReportSheet.vue`**：Vant 全屏底弹报告阅读器，按块类型渲染，底部提供「下载报告资产」按钮（调 `analysisTaskAssetDownload`）。
- **`src/api/enterprise/analysisTask.ts`**：集成 `analysisTaskAssetDownload` / `analysisTaskAssetOpen`（fetch + `assetRequestHeaders()`，RFC 5987 文件名解析，弹窗拦截回退下载）；批 C 同步补的鉴权头逻辑保留不动。**修复**：清理上次误删残留的孤立 `})`（批 C 版本基线恢复）。
- **`src/components/visualization/ChainAnalysisShell.vue`**：新增 `@open-report` emit；结果相任务完成态追加「查看报告」按钮。

### 深链适配

- **新建 `src/views/industry/IndustryTaskDeepLinkView.vue`**：深链解析页，调 `analysisTaskDetail` 后按 `analysisType` 映射到对应工作区（diagnosis / regional / shenzhen / panorama）并附 `task_id` + `report=1` 查询参数，复用既有工作区渲染。
- **`src/router/index.ts`**：`/industry-center/results/:resultId` 与 `/industry-center/reports/:reportId` 由 NotAdaptedView 改注册为 `IndustryTaskDeepLinkView`。

### 全景图谱企业跳转

- **`src/views/industry/IndustryPanoramaView.vue`**：节点详情抽屉「代表企业」可点；带 `org_id`/`id` 的直接 `router.push('/enterprise/:orgId')`，纯文本（无标识）toast 提示去「查企业」搜索。

### 模板与记录删除

- **`src/api/industry/paths.ts` + `chainUx.ts`**：新增端点定义 `chainRegionalTemplatesMineDelete`（POST `/chain/regional/templates/mine/delete`）。
- **`src/views/industry/IndustryRegionalView.vue`**：`removePersonalTemplate`（`showConfirmDialog` 二次确认 → `chainRegionalTemplatesMineDelete` → 刷新模板列表）。
- **`src/api/enterprise/analysisTask.ts`**：新增 `analysisTaskDelete`（软删，POST `/topicAsync/topic/v1/analysis/tasks/{taskId}/delete`）。
- **诊断/区域/深圳 3 视图**：`removeRecord`（确认弹窗 → `analysisTaskDelete` → 记录列表移除）。

### D9 指标就绪度载体

- **诊断/区域/深圳视图 StatCard** 绑定 metric-id：`M_CHAIN_CYCLE_STAGE`、`M_CHAIN_MARKET_SIZE`、`M_CHAIN_NODE_COUNT`、`M_CHAIN_REGION_INDEX`、`M_CHAIN_SZ_ENTERPRISE_COUNT`（对照 PC 端同名口径）。

### 查询示例词

- **`src/views/industry/IndustrySearchView.vue`**：接入 `chainSearchBizExamplesList`，加载后渲染 `exampleKeywords` 可点搜索。

### 可选代码自检

- **新建 `scripts/chain-gap.test.mjs`**：Node 原生 test，断言路由注册、API 导出、报告构建器分发键、深链组件挂载、删除入口存在、企业跳转逻辑；非新框架，符合 ponytail「留一个可运行检查」要求。

## 测试结果

- `node --test scripts/chain-gap.test.mjs`：**6/6 pass**（0 fail，duration 176ms）
- `npm run type-check`（`vue-tsc --build`）：**0 错误**
- 防漏扫描（附录 D 摘要）：D.1 页面差集——本单范围内 `/industry-center/*` 5 视图 + 深链页与 PC 对齐无缺页；D.2 本地 KPI 接线——5 个 metric-id 全部绑定 StatCard；D.3/D.4/D.5 无错挂（本单未新增指标定义，仅引用既有 metric_id）。

## 遗留风险

- 报告块构建器为轻量移植版，PC 端个别重依赖块类型（如需大屏 ECharts 实例的块）未复刻，小屏以表格/排名条替代展示——升级路径：后续如需完全一致的报告排版再引 PC 块渲染器。
- 深链页依赖 `analysisTaskDetail` 接口返回 `analysisType` 字段；若后端历史任务缺该字段，回退到诊断工作区（兜底逻辑已写）。
- `analysisTaskAssetDownload` 在 Mock 模式下走 `window.open` 真网关会 404/424——批 C 已在 `assetRequestHeaders` 处理 Mock token 剥离，真实联调待后端联测（见 CI/CD 段）。

## CI/CD（必填）

- 分支：`dev`（本地工作区，**未 commit**——孔东本地规约 `fe-local-no-auto-commit.mdc`，等人工确认）
- commit：待孔东确认后由本人或会话指令提交
- pipeline URL / ID：待 push 后回填
- 部署 namespace / 镜像 tag：N/A（前端仓 CI 自动）
- K8s rollout：待 push
- dev 测试 URL / 命令与结果：本地 `npm run dev` 已起，`/industry-center` 手工走查：诊断→生成任务→完成→查看报告→下载资产→删除记录链路通；深链 `/industry-center/results/test-id` 正确重定向工作区。

## 可观测性（建议）

- OTEL_SERVICE_NAME：lumen-ui-topic-mobile（仓内既有 `observability.ts` 已覆盖）
- traceId（dev 抽样）：asset 请求带 `X-Trace-Id` / `traceparent` 头（`assetRequestHeaders` 生成）
- Tempo / Loki：有（经网关）

## 涉及文件

**新建（本任务）**
- `repos/lumen-ui-topic-mobile/src/utils/chainBlockReportDocument.ts`
- `repos/lumen-ui-topic-mobile/src/components/visualization/ChainReportSheet.vue`
- `repos/lumen-ui-topic-mobile/src/views/industry/IndustryTaskDeepLinkView.vue`
- `repos/lumen-ui-topic-mobile/scripts/chain-gap.test.mjs`

**修改（本任务）**
- `src/api/enterprise/analysisTask.ts`（资产下载/打开 + `analysisTaskDelete` + 孤立括号修复）
- `src/api/industry/paths.ts`、`src/api/industry/chainUx.ts`（模板删除端点）
- `src/router/index.ts`（深链注册）
- `src/components/visualization/ChainAnalysisShell.vue`（查看报告按钮）
- `src/views/industry/IndustryDiagnosisView.vue`（报告/记录删除/深链恢复/D9）
- `src/views/industry/IndustryRegionalView.vue`（模板删除/记录删除/报告/深链/D9）
- `src/views/industry/IndustryShenzhenView.vue`（报告/记录删除/深链恢复/D9）
- `src/views/industry/IndustryPanoramaView.vue`（企业跳转）
- `src/views/industry/IndustrySearchView.vue`（示例词）

**不在本单范围（其他会话批 C 改动，未触碰）**
- `evaluation.ts` / `profileDetail.ts` / `Enterprise*View.vue` / `stats*.ts` / `types/*` / `mocks/*` / `useMobileAsyncAnalysis.ts` / `PageTabs.vue` / `main.css` / `enterprise-remediation.test.mjs`（属 FE-TOPIC-SMALL-ENT-L01）
