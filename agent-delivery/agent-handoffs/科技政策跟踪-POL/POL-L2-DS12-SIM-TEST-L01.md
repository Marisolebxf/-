# POL-L2-DS12-SIM-TEST-L01 · 科技政策推演 · 集成测试

- 任务：`POL-L2-DS12-SIM-TEST-L01`（WBS 行 `WBS-05-23-L2-09F`）
- 日期：2026-11-06
- 监管：`human:淮政玮`
- 执行：`agent:qa-agent`
- 用户故事：`US-DS-POL-06`
- 状态：保持 `in_progress`（本轮不改 task-registry，不标 done）
- 上游：`sdd/l2/POL-L2-DS12-SIM-API.md`、`sdd/l2/POL-L2-DS12-SIM-DATA.md`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 已认领，本轮不改注册表 |

## 范围与实现

对科技政策推演 SRS 237–242 做集成测试。效果预估种类不在本叶，未改 `POL-L2-DS12-EST-TEST-L01`。

1. 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-SIM-TEST-L01.md`
   - DP-01～DP-04：脚本 `--check`、`--apply` 条件、解析表不灌、环境
   - TC-01～TC-07：行数与主体闭集、文本解析、四类必须 `policy_id`、解读不生成文件、240 不请求、空表契约、TraceId
   - 界面 S1～S7
2. 页面：`lumen-ui-science-pc` 科技政策推演工作台，`USE_MOCK=false`。七张截图在用例同目录 `POL-L2-DS12-SIM-TEST-L01\`。
3. 未改 lumen 业务仓。未 commit，未 push。

## 测试发现

### BUG-01（P1）匿名推演读口 401

- 直连 `POST http://10.50.69.111:30895/display/v1/policy/simulation/jobs`，body `{"kind":"文本解析","policy_id":"18363390"}`，HTTP 401，`msg` 为「访问令牌不存在」。
- 网关回写 `X-Trace-Id: 8625a312d1fd2d44ae15772d57014481`。
- `gkxlumen-display-dev.yml` 的 `ignore-urls` 没有 `/v1/policy/**`。同文件写明展示侧接口不校验登录（human:孔东 2026-10-31）。
- 页面五次 jobs（文本解析、重点可视化、影响范围、路径预测、解读报告）同样 401。`fetchPolicySimulationJob` 使用 `optional: true`，失败后 `liveRows` 为空，界面显示「没有该政策的解析行」等文案。
- `GET /display/actuator/health` 为 200。401 发生在进入 `PolicySimulationService.jobs` 之前，因此「HTTP 成功且 records 为空、不返回 501」以及剥 `clauses` / `clause_meta` 都还没有在线上响应里核对。

### 已核对通过的部分

- `--check`：`gapfill_policy_sim_result` 20，`gapfill_policy_sim_stakeholder` 3。意见行种类只有「参与意见」，主体为决策者、评估者、利益攸关方。
- 环境无 `LUMEN_ALGO_MYSQL_PASSWORD`，`--apply` 未执行。口令未进 git、未进用例。
- 未选政策：不发 jobs，文案「未选择政策文本，不可解析」。
- 政策关联页签：打开后新增 jobs 为 0，文案「本页没有政策子图读法，不请求推演接口」。
- 解读报告：只有「生成解读报告」，无下载、无 PDF、无 Word。

## 偏离说明

| 项 | 说明 |
|---|---|
| `--apply` | 口令不在环境中，按派单停在 `--check`。线上 20+3 行是否已入库，本轮未知 |
| 空表与剥条款 | 匿名链路停在 401。display 源码在条件不齐或 Feign 失败时返回 `R.ok({records:[]})`；element `stripClauses` 去掉两个条款键并保留行。二者都未在本轮 HTTP 响应中出现 |
| 页头数字 | 截图含写死的 86.5 / 78 / 7 / 3。推演结果区仍是空文案，没有用 fixture 填数。记为用例 OBS-01 |
| 本机入口 | 展示前端配置的 `127.0.0.1:7099` 当时无进程，本轮临时把该端口转到网关。直连 `30895` 的 401 与页面 XHR 的 401 一致。临时转发不进 git |
| 注册表 | 按本轮约束不调用 task-update，不标 done |

## 产物清单

| 产物 | 路径 |
|---|---|
| 测试用例 | `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-SIM-TEST-L01.md` |
| 截图 7 张 | 同目录 `POL-L2-DS12-SIM-TEST-L01\`：`01-empty-no-policy.png`、`02-text-parse.png`、`03-focus.png`、`04-impact.png`、`05-path.png`、`06-report-no-download.png`、`07-relation-empty.png` |
| 本 handoff | `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-TEST-L01.md` |
| 代码改动 | 无 |

## 验收证据

- `python scripts/seed_gapfill_policy_sim_result.py --check` 退出码 0，行数 20 与 3。脚本与 SQL 镜像的 `git status --short` 为空。
- 直连网关 jobs：HTTP 401，trace `8625a312d1fd2d44ae15772d57014481`。
- display health HTTP 200；已发布展示前端 HTTP 200。
- 本地 `http://127.0.0.1:3001/policy/policy-effect-simulation` 走完 S1–S7，XHR 记录见用例 TC-02～TC-05。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端 → Java → Python `/internal` | 本叶设计为 display → element 同步读，不调 Python。实测停在网关 401，未越层调用 `polan.text.parse.run` |
| 算法只在 Python | 本轮未要求 Java 做解析或推演 |
| D9 / 空态 | 结果区保持空文案。页头写死分值已单独记录，没有当成 jobs 数据 |
| D16 | 只校验 gapfill 脚本，未写 ODS / DWD / ADS，未执行 `--apply` |
| D18 | 页面结果区没有填 fixture。接口写死 mock 因 401 未测到控制器 |
| 240 | 页面未请求 `simulation/jobs`，本轮也未另发关联接口 |
| 人工确认 / 前端推送 | 未改前端仓，未 push |

## CI/CD

- 分支：未改业务仓，无新 commit
- pipeline：无
- 部署：沿用已发布网关 `10.50.69.111:30895`、展示前端 `30891`。本轮不发布
- K8s：display health 200。本轮 kubectl 未继续下钻（前序调用在列出 Pod 后返回跳板登录页，按会话上限停止）

## 可观测性

- traceId：`8625a312d1fd2d44ae15772d57014481`
- Tempo / Loki：本轮未检索。该 trace 对应网关 401

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 80000 |
| model_used | grok-4.7 |
| actual_cost | 0.40 |
| cost_warn | green |
| user_story | `US-DS-POL-06` |

估算。本会话无计量接口，未回写注册表。低于黄线（单任务 > $5）。

ponytail: full —— 用例按会跑的读口书写；灌数复用已有脚本且只做 `--check`；240 不另造请求；截图为实机空态，未用 fixture 填推演结果。未用 YAGNI 跳过 D9 空态、可观测 trace 与调用链核对。

## 遗留

1. BUG-01 放行或换统一用户中心令牌后，复测 TC-02、TC-03、TC-06：有解析行则去掉 `clauses` 与 `clause_meta` 且行仍在；四类结果无行则 HTTP 成功、`records` 为空。
2. 环境补上 `LUMEN_ALGO_MYSQL_PASSWORD` 后再决定是否 `--apply`。口令仍不得写入 git 或用例。
3. 页头写死分值（OBS-01）留给前端单，不在本叶改页面。
