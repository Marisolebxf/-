# ENT-FE-I2-12-ANALYSIS-GATE-L01 完工 Handoff

## 1. 范围与实现

- 企业评估、风险洞察、引育推荐三个正式工作区仅在用户点击“开始分析”时创建任务，切换条件不自动创建。
- 规范化分析条件并生成稳定 SHA-256 `analysis_fp`。
- 提交前识别同指纹运行中任务和当天成功任务；分别恢复运行态或直接打开结果。
- “重新分析”发送 `force=true`；后端仍兜底复用同指纹运行中任务。
- 创建接口统一传递 `analysis_fp` / `force`，URL 查询态同步保存 `analysis_fp`。
- 代码评审修复：Create 返回当天成功复用任务时直接取结果，仅 `running` 订阅 SSE。
- 引育历史任务恢复时回填不可变筛选/候选集/权重快照，确保“重新分析”条件不漂移。
- 后端无时区 `LocalDateTime` 明确按 `Asia/Shanghai` 墙钟时间解析。
- 二次评审修复：任务列表核验与任务恢复分别处理错误，恢复失败不再误报为列表核验失败。
- 企业评估“重新分析”前重新执行当前任务条件预检，避免沿用配置页的旧预检结果。
- 引育任务恢复等待候选工作台 URL 写入后再切处理中，避免并发路由更新覆盖 `entry`。
- FDE 全链复核：SSE 监听注册后立即查询一次任务详情，补偿 Java 提交后异步投递 Python 时可能抢跑的成功/失败/取消终态。
- Create 返回非运行、非成功状态时直接进入对应错误/取消态，不再错误拉取成功结果。
- Create 请求直接失败时，企业评估与风险洞察统一切到结果错误态并清理 `task_id`，不再停留在无任务的处理中页面。
- 三个工作区发起新任务前清空旧 `activeTask`，Create 失败时不再把上一条成功任务误挂到本次错误结果。
- 企业评估与风险洞察 Create 失败后的“重试”重新执行创建流程，不再依赖已清空的旧 `activeTask`。
- 风险任务恢复的连续路由更新均携带 `analysis_fp`，避免异步 `router.replace` 竞态丢失指纹。
- 企业评估与风险洞察开始创建新任务时同步清除 URL 旧 `task_id`，避免路由 watch 并发恢复上一条任务。

## 2. 产物

- commit：[`de62696`](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/commit/de62696e9ed791b13a44f822c2482952c7813062)
- `src/composables/analysisTaskGate.ts`
- `src/composables/useEvalTask.ts`
- `src/composables/enterpriseEvalActions.ts`
- `src/composables/useEnterpriseRisk.ts`
- `src/composables/useRecruit.ts`
- 企业分析 API 类型与三个创建封装
- `scripts/analysis-task-gate.test.mts`
- 三个工作区“开始分析 / 重新分析”交互更新
- 已推送 `origin/dev`。

## 3. 附录 E 扫描摘要

- E.1 页清单：企业评估、风险洞察、引育推荐均已覆盖。
- E.2 CTA：三个工作区均有显式“开始分析”，已有结果时提供“重新分析”。
- E.3 禁自动 create：条件变化仅更新本地/URL 状态。
- E.4 单飞：前端预检 + Java Redis 原子兜底。
- E.5 当天复用：前端识别 + Java 按上海时区 `end_time` 兜底。
- P0 遗漏：0。

## 4. 验收证据

- `node --experimental-strip-types --test scripts/analysis-task-gate.test.mts`：10/10 通过（含失败重试、风险恢复指纹及新建前清理旧任务 ID 回归）。
- `npm run type-check`：通过。
- 全部修改 TS / Vue 文件 ESLint：通过。
- 生产构建：通过。
- Java 联动测试：8/8 通过。
- Pipeline：[#5353](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5353)；`frontend:build`、镜像、Trivy 与 `deploy:k8s` 通过。
- `e2e:chain-gold`：重跑 [job #23304](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/23304) 仍为 3/6；失败用例与基线 commit `c214c7c` 的 [job #23195](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/23195) 完全一致，均为产业链页面，不属于本任务企业三工作区变更范围。该红项仍阻止本任务宣称 CI 全绿。

## 5. 架构合规

- 正式调用链：✅ `lumen-ui-topic → gkxlumen-topic-async-service → lumen-topic-py`。
- D8/D10：✅ 保留正式 Vue + Arco 页面结构及显式 CTA 交互。
- D9：✅ 本任务不新增统计指标或伪造数据。
- D12：✅ 未调用 `demo-svc-topic-py` 或其他 demo 服务。
- CI/CD：⚠️ 已完成构建与 K8s 发布；全局 `e2e:chain-gold` 存量红项待独立修复，当前不可关单。

ponytail: full — 复用现有 composable/API/任务历史，新增单一纯函数门控模块与最小契约字段。
