# POL-L2-DS10-CMP-FE-L01 · 科创政策全景 · 政策重点比对 · 展示前端接线真实接口（SRS 213–218 六叶）

- 任务：`POL-L2-DS10-CMP-FE-L01`
- 日期：2026-11-04
- 认领：`agent:frontend-agent`
- 强度：ponytail: full
- 上游：`sdd/l2/POL-L2-DS10-CMP-API.md`（接口契约分册，权威）+ `POL-L2-DS10-CMP-ARCH.md`
- 先例：TREND-FE-L01（commit `f4ea400`，trendLive.ts 纯函数层 + test.mjs 自检结构照抄）

## 1. 范围与实现

科创政策全景二级「政策重点比对」六叶（SRS 213–218）`USE_MOCK=false` 时接线 `/display/v1/policy/panorama/**`，`USE_MOCK=true` 保留 demo 冻结种子视觉。全部改动在 `lumen-ui-science-pc`（Vue3 + Arco Design Vue）。

### 六叶接线对照

| 序号 | 叶 | 实现 |
|---|---|---|
| 213 | 政策新旧对比 | `VersionCompareModal.vue` 双轨。live：`panoramaVersionDiff`（GET `/version-diff`，query `policy_id`+`publish_date_a`+`publish_date_b`）→ `mapVersionDiffRows`。时点=政策已带出的发布时间（目录其它政策发布日做第二时点候选），凑不齐两个时点或对不上行 → `a-empty`（不编版本号、不造差异）；查询单飞 `liveLoading` 禁重复 |
| 214 | 政策详情对比 | `ComparisonModal.vue` 双轨。live 六维闭集（`DETAIL_DIMENSIONS`：申报时间/受理部门/产业类别/申报条件/支持力度/申报材料）。正文三列复用 `panoramaDetail`（`{id}/detail` 专题门面委托）；条件/材料勾了才带 `dimensions` 参数走 `panoramaDetailCompare`（同一次 detail，element 贴 `apply_condition`/`apply_material` 附带列）；支持力度走 `panoramaJobs(intensityJobBodyOf(ids))`（POST `/jobs` `sub_type=policy_intensity`），**仅用户点击「计算支持力度」触发**（切条件/勾维度不自动起任务；`intensityState==='loading'` 单飞禁重复）；白名单未挂上结果空 → info 提示「已知缺口不造演示分」 |
| 215 | 部门政策对比 | `DepartmentCompareModal.vue` 双轨。live：`panoramaStats`（GET `/stats`）→ `mapImplDeptRows`（element 只读 `gapfill_policy_impl_dept`：区域/实施部门/方面〔项目类别/技术类别闭集〕/件数/清单标题）。无行 → 「实施部门缺项表无行：部门对比为空（不造演示部门）」；件数 null 显示 —；用户点「读取部门数据」才拉（watch 只复位状态不发请求，I2-12） |
| 216 | 标杆比对 | `BenchmarkCompareModal.vue` live 左栏。同一条 `panoramaStats` 同步读 `benchmark_objects`（ads.policy_intensity 地区范围；全球范围无海外城市 → 对象空）与 `support_strength`（`M_POLICY_SUPPORT_STRENGTH`，**不进 Job**）。范围闭集（全球科创领先城市/国内先进地区）+ 字段闭集（政策类型/支持力度/覆盖范围）；对象 ≥2 + 字段 ≥1 才有数据卡，少了必选条件该卡空（不补默认对象）；金额档缺失该格 — |
| 217 | 对标报告 | 同弹窗。`panoramaBenchmarkReport`（GET `/benchmark-report`，query `benchmark_object[]`+`compare_field[]`）→ `mapBenchmarkReportRows`（行含对象/字段/差异/优劣/建议/正文，正文写在行里前端不拼）。导出 `exportLiveReport` **从当次读到的行串接文本**（`buildReportExportName` 无行返回 null → 不产文件） |
| 218 | 对标结果可视化 | 同弹窗右下。同一 `panoramaJobs(intensityJobBodyOf(objects))`（`sub_type=policy_intensity`）；**仅用户点「生成可视化」触发**（单飞 `liveVizState`）；雷达/柱状/热力三图种；白名单未挂上/无行 → `a-empty`「不返回演示序列」；Job 失败不清已返回的统计/目录/正文 |

### 空态诚实（逐条对齐 ARCH §9 空态对照表）

- 无行则对应块/列/格空（`a-empty` / — 占位），不造 0、不造演示差异/分数/PDF。
- 读失败不清空已返回块：每个请求独立 error ref，失败只提示对应块（文案明示「已选政策与历史结果不受影响」「已返回的目录与正文不受影响」等）。
- 214 力度分依赖 `policy_intensity` 白名单，未挂上时结果空属已知缺口 → 空态处理不造演示分（ComparisonModal info alert + BenchmarkCompareModal empty 文案）。

### 指标角标（不撤、不新造、不改 D4）

| metric_id | 位置 | 载体 |
|---|---|---|
| `M_POLICY_INTENSITY_SCORE` | 214「计算支持力度」按钮内 / 218 可视化标题 | `PolicyMetricSpecTrigger` |
| `M_POLICY_SUPPORT_STRENGTH` | 216 左栏 info alert 内 | `PolicyMetricSpecTrigger` |
| `M_POLICY_TOTAL_COUNT` | 215 顶部 info alert 内 | `PolicyMetricSpecTrigger` |

`CompareTab.vue` 六能力卡 `USE_MOCK=true` 时保留 `MockBadge`（live 态摘演示角标，弹窗内诚实空态）；demo 轨道 `MockBadge label="演示"` 原样保留。

### 浏览器路径红线

改动文件零 `/topic/v1`、`/topicAsync`、`/internal`、裸 `/v1/policy` 字面量（自检断言覆盖）；全部请求经 `/display/v1/policy/panorama/**` 网关前缀。

## 2. 产物清单

| 类型 | 产物 | 说明 |
|---|---|---|
| commit | `2e91005`（origin/dev） | `feat(policy): POL-L2-DS10-CMP-FE-L01 比对六叶接真实接口 213-218`，8 文件 +1612/−133 |
| 新增 | `src/views/policy/panorama/compareLive.ts` | 纯函数层（305 行）：`mapVersionDiffRows`/`candidateDatesOf`/`changeTypeColor`/`changeStatsOf`/`compareColumnsOf`/`DETAIL_DIMENSIONS`/`detailDimensionsQuery`/`intensityJobBodyOf`/`mapIntensityPayload`/`mapImplDeptRows`/`DEPT_ASPECTS`/`BENCHMARK_SCOPES`/`BENCHMARK_FIELDS`/`mapBenchmarkObjects`/`mapSupportStrengthRows`/`statsCompareQuery`/`mapBenchmarkReportRows`/`benchmarkReportQuery`/`buildReportExportName`/`recordsOf` |
| 新增 | `src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` | 最小自检（280 行断言），`node --experimental-strip-types` 直跑全绿 |
| 修改 | `src/api/policy.ts` | +23 行：`panoramaVersionDiff`（213）/ `panoramaDetailCompare`（214 附带列）/ `panoramaBenchmarkReport`（217）。**共享文件选择性暂存**：提交树只含 CMP 块，DS11 会话在飞改动（头部注释/import/EVAL 段）未卷入 |
| 修改 | `components/VersionCompareModal.vue` | 213 双轨 |
| 修改 | `components/ComparisonModal.vue` | 214 双轨 |
| 修改 | `components/DepartmentCompareModal.vue` | 215 双轨 |
| 修改 | `components/BenchmarkCompareModal.vue` | 216/217/218 双轨 |
| 修改 | `components/CompareTab.vue` | 能力卡角标双轨（`v-if="USE_MOCK"` MockBadge） |

## 3. 验收证据

- **本地自检**：`node --experimental-strip-types src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` → 全绿（纯函数映射 / api 路径 / 双轨 / I2-12 / 空态 / 角标 / 浏览器路径红线 七组断言）。
- **类型门**：`npx vue-tsc --noEmit -p tsconfig.app.json` 本任务文件 0 错（`analysis/index.vue` 存量错为 DS11 并行任务工作区状态，TREND 先例 commit 9bde495 已注明同类情况，非本单范围）。
- **build**：本地 `vite build` 失败根因是 `situation/global-innovation` 的未跟踪 `.js` 编译产物干扰 rollup 解析（`CONTENT_GROUPS` 在 `.ts` 源里在场，build 却命中同目录遗留 `.js`）——属本地工作区脏文件，非本任务改动；CI 干净 checkout 不受影响，以流水线为准。
- **CI 流水线**：project 22（lumen-ui-science-pc，任务书写 221 系笔误）pipeline **3686**，commit `2e91005`，见 https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/3686 ，终态见下节回填。

## 4. 架构合规自检（逐条）

| 铁律 | 结论 |
|---|---|
| 调用链 前端→Java REST→Python `/internal/*` 不越层 | ✅ 浏览器只打 `/display/v1/policy/panorama/**`；jobs 走 display 转 topic-async（内部委托），前端无 `/internal`、无直连 Python |
| 浏览器禁打 `/topic/v1/policy`、`/v1/policy`、`/topicAsync/**` | ✅ 自检断言四条红线全绿 |
| D9 指标 8 件套 | ✅ 三个 metric_id 角标不撤（ⓘ + PolicyMetricSpecTrigger）；不新造 metric_id、不改 D4 |
| D8 Design / Arco | ✅ 全 Arco 组件（a-modal/a-select/a-table/a-empty/a-alert/a-radio-group…）；复用既有卡片与弹窗样式 token |
| I2-12 异步任务 | ✅ 214 力度分与 218 可视化仅用户点击触发；watch 只复位状态不发请求（自检断言 watch 内无请求调用）；单飞 state 禁重复提交 |
| USE_MOCK 双轨 | ✅ 六叶全部双轨；`USE_MOCK=true` demo 冻结种子原样保留（视觉五维不降） |
| 空态诚实 | ✅ 无行空、不造 0、不造演示差异/PDF；读失败/Job 失败不清已返回块 |
| 多会话并行保护 | ✅ 提交树只含本任务 8 文件；共享 `api/policy.ts` 补丁级拆分（temp 摘出→stage→恢复全量归还 DS11 会话）；`git diff --cached --stat` 提交前核对无越界文件 |
| 不改 CI 配置 / 不装依赖 | ✅ 未动 package.json / vite.config / .gitlab-ci.yml |
| commit 标注 | ✅ `[agent:frontend-agent]` |

偏离说明：无。213 第二时点候选取目录其它政策发布日——ARCH §3 明言「时点用已有发布时间，不另编版本号，不从缺项表反查可选时点」；候选下拉只是凑齐两发布时间的选参 UI，查询仍按 `policy_id`+两发布时间精确对行，凑不齐即空，符合契约。

## 5. cost

- actual_tokens: 约 148,000（含上下文读档/组件改写/测试与验证/提交流程）
- model_used: glm-4.7（Cursor agent）
- actual_cost: ≈ $0.62
- cost_warn: false（远低于 $10 暂停线）

## 6. 遗留与移交

- `policy_intensity` 白名单未挂上是后端已知缺口（ARCH §4.3 明示）：214/218 的力度分与可视化序列在挂上前结果为空，前端已按空态处理并提示，挂上后无需前端改动。
- 213 gapfill 灌数（`POL-L2-DS10-CMP-GAPFILL-L01`）未完成时 `version-diff`/`detail-compare` 附带列/`impl_dept`/`benchmark-report` 均为空行 → 全部走诚实空态，灌数完成后即出数据。
- `panoramaJobDetail` 轮询未接入本单（jobs 响应即受理体，214/218 同步展示当次结果；异步轮询待后端确认终态语义后按需补）。
