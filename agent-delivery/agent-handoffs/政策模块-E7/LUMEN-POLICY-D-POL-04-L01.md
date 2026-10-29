# LUMEN-POLICY-D-POL-04-L01 · 政策专题 D · /policy/recommendation 深圳三维结果板

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-POL-03-L01.md`](./LUMEN-POLICY-D-POL-03-L01.md) `0891b6ff` · [`LUMEN-POLICY-D-POL-02-L01.md`](./LUMEN-POLICY-D-POL-02-L01.md) `ed592164` · [`LUMEN-POLICY-D-WAITVIEW-L01.md`](./LUMEN-POLICY-D-WAITVIEW-L01.md) `d6e13bd` · [`LUMEN-POLICY-D-POL-01-L01.md`](./LUMEN-POLICY-D-POL-01-L01.md) `67628df0` · [`LUMEN-POLICY-C-TASK-L01.md`](./LUMEN-POLICY-C-TASK-L01.md) `6b91104`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。未回滚产业链 `KEEP_ANALYSIS_QUERY`。未改 `/policy/overview` 时序板与 `/policy/analysis` 区域板。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用配置区合并样式 / `IndustryMetricCard` / `IndustryResultReportEntry` / `SystemReportReader` / `@/review` / `analysisTaskResult` / POL-02/03 结果板模式；未贴 JSX；未 new 地图；未复制第二套任务队列；未做政策文档 Tab、未让查询页入篮。配置区/过程壳已有未拆。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 结果板只消费 Java `GET /topicAsync/topic/v1/analysis/tasks/{id}/result`；切条件不自动 create；succeeded 不自动跳结果。工厂 ODS→GDF→DWD→ADS 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

US-E7-POL-04，金路径 #5。路由仅 `/policy/recommendation`（`analysisKey=policy_sz_3d`，提交 `javaType=policy_shenzhen`）：

1. 配置区「指标体系构建」沿用 POL-01 合并样式：三维每维**行内调节一级权重**，合计必须 **100%** 才能提交（`weightOk = weightTotal === 100`）；下方自由勾选核心指标入模（维内等权）。未做成独立权重表 + 独立折叠。
2. 把 WAITVIEW `policy-analysis-result-placeholder`（仅 recommendation）换成深圳三维结果板：冻结配置快照、三维得分、仪表盘/雷达、优势短板下钻、优化建议；结果只读不可变。
3. 提交 `javaType=policy_shenzhen`（URL 别名仍 `policy_sz_3d`）。**禁止**裸键 `shenzhen`（SVC）。
4. 数据只来自 Java `GET /topicAsync/topic/v1/analysis/tasks/{id}/result`；空/缺字段诚实空 + 评审角标。禁止 fixture。前端不算分。
5. QPOL-02 权重/指标口径 ⚠️「待甲方确认」，不改绿。统计数字旁 ⓘ 只读 catalog/readiness。
6. 配置区 / 过程壳 / 记录 Tab 保持 POL-01 + WAITVIEW；本叶未拆。
7. I2-12：切条件不自动 create；点「查看结果」才进本叶；当天成功打开 wait_view；「重新分析」`force=true`；Job failed 停过程壳，不当空态。

## 权重合计 100% 如何闸

配置页 `weightTotal` 为三维一级权重求和；`weightOk` 要求 `=== 100`。`canGenerate` 在 `policy_sz_3d` 上同时要求 `weightOk && indicatorOk`。不满足时「开始分析」disabled，footer 文案为「三维权重合计须为 100%（当前 x%）」。一键均分写入 34/33/33。

## 结果板区块

冻结配置条（一级权重 + 入模清单只读）→ 综合得分提示 → 三维 KPI 卡（短板/达标标注）→ 仪表盘 + 雷达 → 深圳政策对标下钻（仅入模指标）→ 优化建议策略卡。报告入口挂已有 `SystemReportReader`。

## 偏离说明

- 现网 Job snapshot 多为 harness `{result.results[]}`：policy_id 列表不当作三维得分；结果板结构在、字段诚实空，禁止 Demo fixture 填综合得分或 OPP 策略文案。
- 前端不按一级权重 × 维内等权自行聚合得分。
- 未改 `/policy/overview` 时序结果板；未改 `/policy/analysis` 区域结果板。
- 未改 vite / package.json / `.gitignore`。未回滚 `KEEP_ANALYSIS_QUERY`。

## 产物清单

- 代码：`lumen-ui-topic` `5c5caaf5664f592bbbfc0ed97e5b31e726e680d6` → `origin/dev`
- 本文 handoff

## 菜单路径（本叶改）

| 侧栏 | path | 页 |
|------|------|----|
| 政策时序分析 | `/policy/overview` | 配置 + 过程壳 + 时序结果板（未改） |
| 区域政策对比 | `/policy/analysis` | 配置 + 过程壳 + 区域对比结果板（未改） |
| 深圳政策现状分析 | `/policy/recommendation` | 配置 + 过程壳 + **深圳三维结果板** + 报告阅读 |

## Java 调用

| 动作 | 方法 | 路径 |
|------|------|------|
| 查看结果 | `analysisTaskResult` GET | `/topicAsync/topic/v1/analysis/tasks/{id}/result` |
| 重新分析 | `analysisTaskCreate` POST | `/topicAsync/topic/v1/analysis/tasks`（`force=true`，`analysisType=policy_shenzhen`） |
| poll / 记录 | 沿用 WAITVIEW | GET `{id}` / POST list |

未调 `#106` asset、未调 demo-*、未直打 Python、未提交裸键 `shenzhen`。

## 验收证据

- `node src/views/policy/policyShenzhen.selfcheck.mjs`：`policyShenzhen.selfcheck ok`
- `node src/views/policy/policyRegional.selfcheck.mjs`：`policyRegional.selfcheck ok`
- `node src/views/policy/policyTimeseries.selfcheck.mjs`：`policyTimeseries.selfcheck ok`
- `node src/views/policy/policyWaitView.selfcheck.mjs`：`policyWaitView.selfcheck ok`
- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数；mock 开时 snapshot 形状=Java 包络（空/harness list 诚实空）

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ recommendation 结果：冻结快照 + 三维得分 + 仪表盘/雷达 + 短板下钻 + 优化建议；配置区合并样式；一节点一套 layout |
| R2 交互 | ✅ 空 / 加载 / 失败（过程壳）/ wait_view / 点查看才进结果 / 权重合计≠100% 禁提交 / 条件脏不 create / 重新分析 force |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；复用 `industry-diagnosis` 结果皮肤 + `--sci-primary` |
| R4 评审 | ✅ 只从 `@/review`：`E7-POL-F03-RESULT-BOARD` / `E7-POL-F03-STRATEGY-CARDS` / `E7-POL-F03-INDICATOR-BUILD-TRACE` + MetricSpecCard / PendingBadge；关评审零泄漏 |
| R5 Mock | ✅ 开：`registerApiMock` + `analysisTaskStore` Java 形状空包；关：只渲染 Java 实包 |

### 检索皮肤 V1–V7

本叶 **无检索页**（查询已由 POL-01c 交付）。下列 **N/A**：

| # | 结果 |
|---|------|
| V1 | N/A 本叶无检索 Hub；工作区页底仍用 `--sci-bg-page` / `#d8e7fc` |
| V2 | N/A 无检索 Hero |
| V3 | N/A 无检索结果卡 |
| V4 | N/A 未叠检索卡 class |
| V5 | N/A 无检索内容列 |
| V6 | N/A 检索空态属 POL-01c |
| V7 | N/A 无 `industry-search-result-card` |

### 工作区 W1–W4

| # | 结果 |
|---|------|
| W1 | ✅ **结果板必过**（得分 / 优势短板 / 优化建议）。配置区/过程壳/记录 Tab 继承 POL-01 + WAITVIEW，未拆 |
| W2 | N/A Demo `/policy/recommendation` 无关系图（无 G6 产业链图）；本页未用 ECharts 冒充关系图（仪表盘/雷达是得分可视化） |
| W3 | ✅ Demo 有报告入口：挂已有 `SystemReportReader`（`PolicyShenzhenReportHost`），未新造阅读器 |
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同指纹 inflight 复用过程；当天成功打开 wait_view；点「查看结果」才进本叶；「重新分析」`force=true`；Job failed 停过程壳 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP、不算分 |
| 前端→Java→Python `/internal/*` | ✅ 结果只调 Java GET `.../tasks/{id}/result` |
| 图谱 Nebula | ✅ 不 new 地图、不直连 nGQL；W2 N/A |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；对照 Demo 深圳结果 + 本仓 POL-02/03 结果板 |
| D9 8 件套 | ✅ ⓘ 只读 catalog/readiness；QPOL-02 ⚠️ 不改绿 |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL |
| I2-12 | ✅ 见 W4 |

## 测试结果

- 深圳 / 区域 / 时序 / wait_view / menu 自检、vue-tsc 通过。
- 联调确认：recommendation 结果板只打 Java result；切条件不 create；succeeded 不自动跳结果；提交 `policy_shenzhen`；未改 overview/analysis 结果板。

## 遗留风险

- 现网 Job 空 snapshot 时得分/雷达/策略诚实空，需 Python/Java 结果包补 `dims` / `composite` / `strategies` 后才有线。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`5c5caaf5664f592bbbfc0ed97e5b31e726e680d6`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://10.50.69.111:30892`（发布后：`/policy/recommendation` 开始分析 → wait_view → 查看结果 → 深圳三维结果板）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/utils/policyShenzhenResult.ts` | 新增：解析 Java result 实包 |
| `src/components/policy/PolicyShenzhenResultBoard.vue` | 新增：深圳三维结果板 |
| `src/components/policy/PolicyShenzhenReportHost.vue` | 新增：挂 `SystemReportReader` |
| `src/views/policy/PolicyAnalysisConfigPage.vue` | recommendation 换结果板；overview/analysis 结果板不动 |
| `src/views/policy/policyShenzhen.selfcheck.mjs` | 新增自检 |
| `src/views/policy/policyTimeseries.selfcheck.mjs` 等 | 占位断言改为深圳结果板 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 145000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.18 |
| cost_warn | green |
