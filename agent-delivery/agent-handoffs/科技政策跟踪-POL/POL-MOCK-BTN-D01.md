# POL-MOCK-BTN-D01 · 政策 Mock 页七个按页灌数按钮

> 2026-11-09。在政策 Mock 页现有两个按钮旁加上全景、评价、推演、治理、拆解、对比、研报。确认框、单飞和 4 秒轮询沿用原任务，完成后展示回执。未改任务状态。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 in_progress。本单不调 task-registry，不改状态。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。七个按钮走原来的 `onMockJob` 和 `pollSynth`（4 秒），不另做一套确认、单飞或刷新。回执用现成 `el-table`。未加依赖。未用 YAGNI 跳过确认文案里的序号、表、不整表清空、不动另外两个按钮造的政策行。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

政策 Mock 页顶栏，在「Mock 10 条数据」「真实政策补外围」右侧、「删除所有 Mock 数据」左侧，增加 7 个按钮：全景、评价、推演、治理、拆解、对比、研报。

点击后先看顶栏数据面。若当前是正式库，提示与原灌数按钮同一句：`正式库禁止灌数，请把顶栏「政策」切回 Demo`。判断在点击时重读 `isLive('policy')`，避免页面打开后再切顶栏仍放行。固态电池政策按钮改为同一句、同一次重读。删除按钮的文案未改。

确认框沿用 `ElMessageBox.confirm`。每页写明序号、写入的表、不整表清空，以及不动「Mock 10 条数据」和「真实政策补外围」造的政策行。序号和表名对齐 `polan/mockgen/btn.py` 的回执清单：

| 按钮 | 页键 | 序号 | 写入表 |
|------|------|------|--------|
| 全景 | panorama | 197、198、199、200、205、206、209–218 | 检索三表、动向三表、theme_dist、受众反馈、评估报告、新旧对比、详情对比、部门对比、对标报告。209、212、216、218 只登记已有 ADS，确认框写明本按钮不改这些表 |
| 评价 | evaluation | 219–231 | eval_trend、eval_partition、eval_template、eval_shell、eval_scheme。221、231 不建表。223、226 只登记已有 ADS |
| 推演 | simulation | 232–242 | sim_forecast、sim_result、sim_stakeholder。237 不另建表，240 不建表 |
| 治理 | governance | 604、605 | lineage_index、indicator_lib |
| 拆解 | parse | 606 | semantic |
| 对比 | compare | 610、611、613 | xcmp、xcmp_viz、xcmp_summary |
| 研报 | report | 614–618 | report_analysis、report_insight、report_body、report_trace |

启动接口：`POST /policy/v1/policy/mock/page`，JSON `{"page":"<页键>"}`。网关剥前缀后即 `POST /v1/policy/mock/page`。进度仍是 `GET /policy/v1/policy/mock/synth`，间隔 4 秒。进行中 `data.job` 为 `btn:<页键>`，对应按钮转圈；已有任务在跑时提示后端原文并改盯正在跑的那个任务。结束后刷新政策列表。`data.last.job` 以 `btn:` 开头且带 `receipt` 时，在列表上方展示回执表。列：序号、叶名、表、本次行数、总行数、样例、读取页面、生成方式。`本次写入行数` 为 0 的行用警告色底高亮。重新进入页面且没有任务在跑时，沿用上次回执。

## 测试结果

在 `demo-ui-system-test` 执行（已设 `pnpm_config_verify_deps_before_run=false`，避免 pnpm 10 在跑脚本前重装依赖）：

- `pnpm run lint:eslint`：退出码 1。`[ERR_PNPM_NO_SCRIPT] Missing script: lint:eslint`。本仓 `package.json` 只有 `dev` / `build` / `prettier`，没有 eslint 依赖。按派单未新增依赖，也未改 `package.json`。
- `pnpm run build`：退出码 0。vite v4.5.14，3816 modules，40.65s。产物含 `PolicyMockPage.*.js` / `PolicyMockPage.*.css`。

未在浏览器点这 7 个按钮。管理端要登录，本机没有已开的该仓 dev server，也没有对线上执行灌数。

## 遗留风险

- 页写入仍可能是 0 行（B01 框架）。回执会整表高亮，这是预期。
- `livePlane` 仍是进页时的快照，只用于禁用按钮。点击拦截已重读顶栏。进页时已经是正式库，按钮是禁用的，点不到提示句，与原来两个按钮相同。
- 前端 commit 未推。CI 与 K8s 不会因这次改动更新。
- 未对真实演示库点按钮。

## CI/CD（必填）

- 分支：`dev`
- demo-ui-system-test：`0de7753e0ad758cf429317187f2fad4708f9bf1e`，本地 `dev` 比 `origin/dev` 超前 1，**未 push**
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：前端未推，本次 commit 不会触发该仓 CI
- 部署：无
- K8s rollout：无

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 | 符合。只调 Java/网关已有的 `/policy/v1/policy/mock/page` 与 `/policy/mock/synth`，不直连 Python |
| 不新增依赖 | 符合 |
| D12 | 符合。仍走本仓既有 `/policy/v1` 前缀，未改指向 |
| 可观测 | 沿用 `request` 上已有的 trace。未加新埋点 |
| 未改任务状态 | 符合 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.60（价表无 grok-4.7；按本 epic B01 的 180000→$0.90 同比折算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue`
- `repos/demo-ui-system-test/src/api/policy/index.ts`
- 本 handoff

未提交 `sdd/` 下两份已有改动，未提交 `task-registry.yaml`。
