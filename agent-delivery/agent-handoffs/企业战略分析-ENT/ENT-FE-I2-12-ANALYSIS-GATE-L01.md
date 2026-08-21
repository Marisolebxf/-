# ENT-FE-I2-12-ANALYSIS-GATE-L01 · lumen 企业评估/风险/引育 — I2-12 开始分析与当日条件复用

> 格式参考 `templates/handoff-template.md` + `templates/fe-replica-visual-dod.md`。  
> **本叶范围**：三个异步分析工作区的 **W4 / I2-12 门控**（开始分析、切条件不 create、指纹单飞、上海自然日复用）。不重铺布局、不改报告阅读器、不新造地图。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 2026-08-21 coordinator 抽查 W4 已过；本文件补 AV-1 缺项（偏离 / 架构勾选 / R1–R5 / cost）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 composable / Java analysisTask / 任务历史；新增单一纯函数门控 `analysisTaskGate.ts`。未用 YAGNI 跳过 I2-12、附录 E、D8/D9/D10、只调 Java。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶对照 Demo `analysisTaskGate.ts` + 规程 I2-12，禁止 compress 代替门控。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改存储流图；沿用企业分析任务 `analysis_task` + Redis 指纹锁（见 `ENT-API-I2-12-ANALYSIS-GATE-L01`） |
| 会签态 | N/A（纯前端门控，不碰拓扑） |

## 1. 范围与实现

- 企业评估、风险洞察、引育推荐三个正式工作区仅在用户点击「开始分析」时创建任务，切换条件不自动创建。
- 规范化分析条件并生成稳定 SHA-256 `analysis_fp`。
- 提交前识别同指纹运行中任务和当天成功任务；分别恢复运行态或直接打开结果。
- 「重新分析」发送 `force=true`；后端仍兜底复用同指纹运行中任务。
- 创建接口统一传递 `analysis_fp` / `force`，URL 查询态同步保存 `analysis_fp`。
- Create 返回当天成功复用任务时直接取结果，仅 `running` 订阅 SSE。
- 引育历史任务恢复时回填不可变筛选/候选集/权重快照，确保「重新分析」条件不漂移。
- 后端无时区 `LocalDateTime` 明确按 `Asia/Shanghai` 墙钟时间解析。
- 任务列表核验与任务恢复分别处理错误，恢复失败不再误报为列表核验失败。
- 企业评估「重新分析」前重新执行当前任务条件预检，避免沿用配置页的旧预检结果。
- 引育任务恢复等待候选工作台 URL 写入后再切处理中，避免并发路由更新覆盖 `entry`。
- SSE 监听注册后立即查询一次任务详情，补偿 Java 提交后异步投递 Python 时可能抢跑的成功/失败/取消终态。
- Create 返回非运行、非成功状态时直接进入对应错误/取消态，不再错误拉取成功结果。
- Create 请求直接失败时，企业评估与风险洞察统一切到结果错误态并清理 `task_id`。
- 三个工作区发起新任务前清空旧 `activeTask`；Create 失败时不再把上一条成功任务误挂到本次错误结果。
- 企业评估与风险洞察开始创建新任务时同步清除 URL 旧 `task_id`，避免路由 watch 并发恢复上一条任务。

## 2. 偏离说明

对照 `demo-ui-topic` `src/app/system-tasks/analysisTaskGate.ts`（commit `b5e6430`）与 `产品实现规程.md` I2-12 / 附录 E：

| 项 | Demo / 规程 | lumen as-built | 理由 |
|----|-------------|----------------|------|
| 指纹载体 | 系统任务 `processingRoute`/`resultRoute` 的 URL `analysis_fp` | Java `target_params.analysis_fp` + 页面 URL 同步 | 正式任务中心契约在 Java；前端预检与后端 Redis 锁同一指纹 |
| 成功态枚举 | `succeeded` | 同时认 `success`（Java）与 `succeeded` | 正式异步任务表用 `success` |
| 用户维度 | 本地 `systemTaskStore.userId` | Java `userId`；缺省时不误伤同指纹 | 沿用现网客户端 `user_id`，服务端登录态取用户不在本叶 |
| 过程壳 wait_view | 服务机构等须点「查看分析结果」才进结果 | 本三页沿用已有结果工作区：当天成功 `restore_result` 直接打开结果 | 与 Demo 企业评估/风险/引育一致；不是服务机构过程壳 |
| 视觉五维 | 全页复刻 | **本叶只做 W4 门控**，不重铺卡片/地图/报告 | `/goal` 范围=I2-12；布局/样式/评审挂点沿用既有页 |
| Q-ANALYSIS-01 | 自然日 + 重新分析 | 已按临时基线实现 | 仍为 🟡，UI 不把口径改绿 |
| CI 金路径 | 本叶非产业链页 | Pipeline #5365 绿含 `e2e:chain-gold` | 金路径红项由 `LUMEN-CHAIN-FE-REPLICA-FIX-L01` commit `91e9d47` 修；**不计入本叶代码偏离** |

无范围外改动：未贴 JSX、未直连 Python、未用 Demo fixture 填数。

## 3. 复刻五维验收（R1–R5）

本叶 `/goal` 范围 = 企业评估 / 风险洞察 / 引育推荐 **W4 门控**，不是查询 Hub，也不是视觉铺齐叶。

| # | 项 | 结果 |
|---|-----|------|
| R1 布局 | 三页既有配置区 / 结果区 / 记录结构未拆；本叶不新增互斥 layout | ✅ 沿用；一节点一套 layout 未改坏 |
| R2 交互 | 空 / 加载 / 失败 / 有结果 / 条件脏；切条件不 create；「开始分析」「重新分析」 | ✅ W4 主交付 |
| R3 样式 | `--sci-*` / 页底 / Arco 条件栏主按钮，本叶不改皮肤 | ✅ 未另起灰白后台 |
| R4 评审 | 只从 `@/review` 挂点；本叶未自造 ⓘ | ✅ mount：`ENT-EVAL-F05-PAGE-TITLE`、`ENT-RISK-F00-PAGE-TITLE`、`ENT-RECRUIT-F00-PAGE-TITLE`、`ENT-RECRUIT-REVIEW-STATE` |
| R5 Mock | `USE_MOCK=false` 走 Java 实包；Mock 仅既有 `USE_MOCK` 开关，无页内 `const MOCK_` 撑门控 | ✅ |

检索皮肤 V1–V7：本叶非查询 Hub → **N/A**。

### 工作区 W1–W4

| # | 项 | 结果 |
|---|-----|------|
| W1 | 配置区 / 过程/结果 / 记录 | ✅ 既有三页结构，本叶未拆 |
| W2 | 关系图 | N/A（本叶不改图；风险供应链图沿用既有组件） |
| W3 | 报告入口 | N/A（本叶不改 `SystemReportReader`；风险报告面板沿用） |
| W4 | 切条件不自动起任务；条件栏「开始分析」；同用户同条件一条在跑；当天已成功直接打开结果 | ✅ coordinator 抽查已过 |

## 4. 附录 E 扫描摘要

- E.1 页清单：企业评估、风险洞察、引育推荐均已覆盖。
- E.2 CTA：`EvalConfigPanel` / `RiskTaskConfiguration` / `RecruitFilterPanel`·`RecruitReviewConfigPanel` 均有「开始分析」；结果区均有「重新分析」。
- E.3 禁自动 create：条件变化仅更新本地/URL 状态；create 只走点击回调。
- E.4 单飞：前端 `decideAnalysisTaskGate` 预检 + Java Redis 原子兜底。
- E.5 当天复用：`Asia/Shanghai` 自然日 + `endTime`；`force=true` 才同日再 create（仍受单飞约束）。
- P0 遗漏：0。P1：无。

## 5. 产物清单

- 仓：`repos/lumen-ui-topic` `origin/dev`
- commit：[`de62696`](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/commit/de62696e9ed791b13a44f822c2482952c7813062)
- `src/composables/analysisTaskGate.ts`
- `src/composables/useEvalTask.ts` / `enterpriseEvalActions.ts`
- `src/composables/useEnterpriseRisk.ts`
- `src/composables/useRecruit.ts`
- 企业分析 API 类型与三个创建封装
- `scripts/analysis-task-gate.test.mts`
- 三个工作区「开始分析 / 重新分析」交互
- 本 handoff

## 6. 验收证据

- `node --experimental-strip-types --test scripts/analysis-task-gate.test.mts`：10/10 通过
- `npm run type-check`：通过
- 全部修改 TS / Vue 文件 ESLint：通过
- 生产构建：通过
- Java 联动测试：8/8 通过（`ENT-API-I2-12-ANALYSIS-GATE-L01`）
- Pipeline：[\#5365](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5365) 全绿（含本任务 `de62696`）
- `deploy:k8s` [job \#23337](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/23337) 通过
- `e2e:chain-gold` [job \#23338](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/23338) 通过

## 7. CI/CD

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`de62696`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5365（Passed）
- 部署 namespace / 镜像 tag：K8s dev / 跟 Pipeline \#5365
- K8s rollout：`deploy:k8s` Job `#23337` success
- 联调确认：三个工作区 I2-12 门控抽查通过（开始分析/重新分析、切条件不 create、指纹单飞、上海自然日复用）

## 8. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 前端不跑算法 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ `lumen-ui-topic → gkxlumen-topic-async-service → lumen-topic-py` |
| 3 | 图谱 NebulaGraph | ✅ 不直连 |
| 4 | 可观测性 | ✅ 沿用 analysisTask 请求链 `X-Trace-Id` |
| 5 | CI/CD | ✅ Pipeline \#5365 绿 + K8s rollout |
| 6 | demo 不 merge lumen | ✅ Vue 重写，禁止贴 JSX |
| 7 | 方案 A / 只调 Java | ✅ |
| 8 | 标准表 / 诚实空 | ✅ 不造分析结论；失败走错误态 |
| 9 | D8 Design.md | ✅ 保留正式 Vue + Arco 条件栏主按钮 |
| 10 | D9 血缘 | ✅ 本叶不新增统计指标、不伪造口径、不自造 ⓘ |
| 11 | D10 交互 | ✅ 显式 CTA；条件未就绪禁用；状态覆盖加载/失败/复用 |
| 12 | D12 正式隔离 | ✅ 未调用 `demo-svc-topic-py` 或其他 demo 服务 |

## 9. cost（完工回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 240000（会话估计：门控实现 + 多轮评审修复；不含产业链金路径修叶、不含 SEARCH 问答。source: session_estimate） |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.40（按 budget-estimate 主力档 in/out 代理公式；Grok 无独立价表） |
| cost_warn | green |

## 10. 遗留风险

- Q-ANALYSIS-01 仍为 🟡：自然日窗口上线前须甲方书面确认。
- 前端门控是预检；并发单飞以 Java Redis 为准。
- 客户端传入 `user_id` 沿用现网契约，登录态服务端取用户不在本叶。
