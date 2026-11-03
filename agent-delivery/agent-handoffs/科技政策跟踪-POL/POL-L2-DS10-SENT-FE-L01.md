# POL-L2-DS10-SENT-FE-L01 · 科创政策全景 · 政策舆情评估页签前端接线

- 任务：`POL-L2-DS10-SENT-FE-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:frontend-agent`
- 强度：ponytail full
- 用户故事：`US-DS-POL-03`（SRS 207–212 中的 209/210/211/212 四卡）
- 设计依据（已签收，未偏离）：`sdd/l2/POL-L2-DS10-SENT-API.md`、`sdd/l2/POL-L2-DS10-SENT-ARCH.md`
- 代码仓：`lumen-ui-science-pc` @ `origin/dev` commit **73cc1e8**（7 文件，+734/−64）
- 伴单：后端 `POL-L2-DS10-SENT-API` 已上线 dev（`PolicyPanoramaController`）

## 1. 交付范围

「政策舆情评估」页签（SentimentTab）四块卡片从 mock 种子切到真实接口，`USE_MOCK=true` 保留 demo 种子演示。改动全部落在全景舆情 Tab 与公共 API 层；检索页签已接线代码未动（`index.vue` 未改，工作区另有一处他人未提交改动未纳入本单）。

新增文件：

- `src/views/policy/panorama/sentimentLive.ts` — 无框架依赖纯函数：渠道闭包映射（问卷/在线评价/意见征集 → survey/rating/opinion）、反馈行映射、统计（无评分不造 0）、报告行映射（问题/建议按行拆）、jobs 受理体、taskId 双读法、错误文案提取
- `src/views/policy/panorama/FE-POL-SENT-LIVE.test.mjs` — 最小自检（node 直跑）

## 2. 每块卡片接线前后对照

### 2.1 政策受众反馈收集（FeedbackPanel.vue · SRS 210）

| | 接线前 | 接线后（USE_MOCK=false） |
|---|---|---|
| 数据源 | `policyFeedbackData` 种子 + 渠道统计种子 | `GET /display/v1/policy/panorama/feedback` → `gkxlumenx_gapfill.gapfill_policy_audience_feedback` 行 |
| 统计卡 | 种子固定数（86/4.3/40 等） | 从真实行计算：条数=行数；平均分=有评分行的均值（无评分显示「—」不造 0）；五星数=Math.round(score)===5 行数 |
| 渠道切换 | 种子过滤 | 同一闭包过滤（行渠道为中文值「问卷/在线评价/意见征集」，`channelKeyOf` 归一；未知渠道行剔除） |
| 意见聚类块 | 种子演示 | **仅 USE_MOCK=true 显示**（缺项表无聚类列，真实态不造演示聚类） |
| 空态 | 种子永非空 | 空列表显 `a-empty`「暂无问卷反馈/暂无在线评价/暂无征集意见」；失败卡内 `a-alert` 提示，不清其它卡 |
| 详情弹窗 | 种子全字段 | 只显后端有的列（渠道/反馈人/关联政策/时间/评分（空不显示评分行）/意见正文）；「真实需求」「认同数」「标签」仅种子态 |

请求样例：`GET /display/v1/policy/panorama/feedback`（无参数）。行字段：`id, subject_name, channel, opinion_text, score, policy_id, feedback_at, is_mock`（score 可空）。

### 2.2 政策效果评估报告（SentimentTab 内列表 + EvaluationReportModal.vue · SRS 211）

| | 接线前 | 接线后 |
|---|---|---|
| 数据源 | `policyEvaluationReports` 种子（3 份，含 5 维评分） | `GET /display/v1/policy/panorama/assessment-report` → `gapfill_policy_assessment_report` 行 |
| 列表行 | 标题/评估机构/日期/综合得分 | `scope_text`（评估范围）/`generated_at`；每行挂 MockBadge |
| 查看报告 | 种子维度得分/结论 | 达成度+社会影响合并为结论、`problem_text`/`suggestion_text` 按行拆、`report_body` 正文段（modal 补「报告正文」区块）；无评分显「—（本报告未提供评分）」不造分 |
| 下载 | Message 演示提示 | 从读到的行生成 txt 下载（内容=达成度/影响/问题/建议/正文，符合 ARCH「下载内容来自该行」）；USE_MOCK=true 保留演示提示 |
| 空态 | 永非空 | `a-empty`「暂无可用报告」；失败卡内提示 |

请求样例：`GET /display/v1/policy/panorama/assessment-report`。行字段：`id, scope_text, achievement_text, social_impact, problem_text, suggestion_text, report_body, generated_at, is_mock`。

### 2.3 政策实施效果跟踪（ImplementationTracker.vue · SRS 209）

| | 接线前 | 接线后 |
|---|---|---|
| 数据源 | `policyImplementationData` 种子表格 | `POST /display/v1/policy/panorama/jobs` body `{"sub_type":"policy_effect"}`（异步任务） |
| 起任务 | 无（种子直显） | **受理制**：仅用户点「开始分析」才 POST（I2-12：挂载/切条件不自动起任务）；受理后按钮禁用（同条件单飞）；失败卡内 `a-alert` 提示且不清反馈/报告同步块 |
| 结果展示 | 种子表 | 受理提示含 taskId（`AnalysisTaskEntity` 序列化 `taskId`，兼容 `task_id`）；idle 态 `a-empty`「暂无实施效果数据，点击开始分析生成」不造 0 |
| 角标 | 无 | 工具栏挂 `PolicyMetricSpecTrigger metric-id="M_POLICY_IMPLEMENTATION_EFFECT"`（镜像有此指标）+ MockBadge |

### 2.4 政策匹配与推送（SentimentTab open-match 入口 · SRS 212）

| | 接线前 | 接线后 |
|---|---|---|
| 入口 | 「配置匹配与推送」按钮开种子匹配弹窗 | USE_MOCK=true 保留原按钮；false 时卡片内联「匹配主体 + 开始匹配」：`POST jobs` body `{"sub_type":"policy_match","params":{"subject_id":"E0001"}}` |
| 起任务 | 无 | 仅点「开始匹配」才 POST（切主体编号只改本地状态）；受理后按钮禁用（单飞）；失败如实提示（匿名时后端拒「未获取到当前用户」，前端原样展示不伪造用户） |
| 结果 | 种子匹配列表 | 受理提示含 taskId；无外发推送通道，文案如实说明「仅返回匹配列表」 |
| 角标 | 卡头 MockBadge | 保留 + `PolicyMetricSpecTrigger metric-id="M_POLICY_MATCH"` |

**subject 放 `params.subject_id` 的依据**：display `toAsyncCreateBody` 白名单只转发 `params`/`draft`（顶层 `subject` 会被丢弃）；Python `polan/job.py _match_where` 读 `body.params.subject_id` 过滤 `ads.policy_match`。主体沿用受控画像编号（E0001/U0001，ARCH §4.6）。

## 3. 交互铁律（I2-12）落实

- ✅ 切条件不自动起任务：效果/匹配均无 watch 自动 POST；挂载只拉同步 GET（反馈/报告）
- ✅ 同用户同条件单飞：受理未闭合前按钮 `disabled`（无轮询通道，不伪造完成态）
- ✅ 失败不清同步块：反馈/报告/统计卡数据不受 jobs 失败影响，仅对应卡内 `a-alert`
- ✅ 空态诚实：`a-empty` + 诚实文案；不造 0（无评分「—」）、不造演示分、无 501 充当
- ✅ 匿名如实提示：后端拒/空身份时展示 `msg` 原文
- ⚠️ 当天复用 / 重新分析 / 结果回读：**依赖任务查询端点，见 §5 缺口**

## 4. 工程验证（三绿）

| 项 | 命令 | 结果 |
|---|---|---|
| 类型 | `npx vue-tsc --noEmit` | ✅ 0 错误 |
| 构建 | `pnpm build` | ✅ built in 1m16s |
| 自检 | `node src/views/policy/panorama/FE-POL-SENT-LIVE.test.mjs` | ✅ 全绿（纯函数映射/api 路径锚点/双轨/I2-12/空态/角标/浏览器路径红线） |
| 回归 | `node src/views/policy/panorama/FE-POL-01B.test.mjs` | ✅ 全绿 |

已知无关红：`node src/views/policy/policy.test.mjs` 的「种子冻结」断言在本机因 `demo-ui-science` 与 `lumen-ui-science-pc` 克隆行尾（CRLF/LF）不一致而 diff 误报——基线 commit `86ef333`（2026-11-02）未触碰 `policySeed.ts`，后端真源 `e277bd7`（2026-08-20）早于基线，内容未漂移；非本单引入、非本单修复。CI/Linux 环境行尾一致，不受影响。

## 5. jobs 轮询缺口（重要）

`gkxlumen-display` 的 `PolicyPanoramaController` 只有 `POST /v1/policy/panorama/jobs`（受理），**未暴露任务查询端点**（无 `GET jobs/{taskId}` / `GET jobs/{taskId}/result`）。上游 `gkxlumen-topic-async-service` 有 `GET /topic/v1/analysis/tasks/{taskId}` 与 `/result`，但浏览器禁止直打（D12 / 设计分册红线）。按任务指令未自造端点路径：

- 效果卡/匹配卡当前为「受理 + 提示进行中」，代码内留 `TODO(POL-L2-DS10-SENT-FE-L01)` 注释
- **缺口补法建议**：display 增加 `GET /display/v1/policy/panorama/jobs/{taskId}` 委托 `GET /topic/v1/analysis/tasks/{taskId}`（同 jobs 受理的委托方向）。端点上线后前端接：轮询→结果渲染（区域效果行 `scope_type=region_effect`、时序 `M_POLICY_IMPLEMENTATION_EFFECT`；匹配行 `policy_title/match_score/match_reasons/rank_no`）→当天成功同条件直接打开结果→「重新分析」传 `force:true`（`jobBodyOf` 已支持）

## 6. 请求样例汇总

```
GET  /display/v1/policy/panorama/feedback
GET  /display/v1/policy/panorama/assessment-report
POST /display/v1/policy/panorama/jobs   {"sub_type":"policy_effect"}
POST /display/v1/policy/panorama/jobs   {"sub_type":"policy_match","params":{"subject_id":"E0001"}}
```

浏览器全部请求只落 `/display/v1/policy/**`；自检断言 `api/policy.ts` 与四个组件源码中无 `/topicAsync`、`/policy/topic`、`/internal`、`/v1/policy/match`。

## 7. 架构合规自检

- ✅ 调用链：前端 → display REST →（内部委托），无越层
- ✅ D12：无任何 `demo-*`、`/topicAsync/**`、`/policy/topic/**`、`/internal/*` 浏览器请求
- ✅ D9：统计旁 ⓘ（PolicyMetricSpecTrigger，reviewMode 自闸）；mock 行 MockBadge 不撤；空态不造 0 不造分
- ✅ I2-12：切条件不自动起任务 / 单飞 / 失败不清同步块 / 空态诚实（见 §3）
- ✅ 布局不动：卡片结构、demo 已评审视觉保持，仅换数据源
- ✅ 未改 Java/Python；未改 USE_MOCK 语义之外的全局配置；未改 Design token
- ✅ commit 带 `[agent:frontend-agent]`；push `origin/dev`；被拒不 force（本次 pull --no-rebase 后直推成功）

## 8. 产物清单

- `lumen-ui-science-pc` @ dev：`73cc1e8`（`src/api/policy.ts`、`sentimentLive.ts`、`FE-POL-SENT-LIVE.test.mjs`、`FeedbackPanel.vue`、`SentimentTab.vue`、`ImplementationTracker.vue`、`EvaluationReportModal.vue`）
- 本 handoff（gkx-orchestration @ dev）

ponytail: full —— 纯函数抽 `sentimentLive.ts` 是为 node 自检可 import（组件内联映射无法直测）；未加轮询/状态机等端点未就绪的空转代码。
