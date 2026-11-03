# POL-L2-DS11-READ-TEST-L01 · 结果解读报告多维展示 · 集成测试用例

- 任务：`POL-L2-DS11-READ-TEST-L01`（WBS 行 `WBS-05-23-L2-06F`）
- 日期：2026-11-03
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 被测链路：DS11 结果解读报告多维展示（SRS 223–226）
- 设计真源：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-ARCH.md`（已签收）、`sdd/l2/POL-L2-DS11-READ-API.md`
- 实现单：`POL-L2-DS11-READ-IMPL-JAVA`（commit `490071b`/`814d8df`/`30a3192`）、`POL-L2-DS11-READ-IMPL-PY`、`POL-L2-DS11-READ-GAPFILL-L01`（commit `8c0a59c`）
- 强度：ponytail full

## 0. 接口与链路总览（被测对象）

| 序号 | 公开资源 | 链路 |
|---|---|---|
| 223 短板条数 | `GET /display/v1/policy/evaluation/counts` | 前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `{ads}.policy_effect`（`scope_type=region_gap`） |
| 223 焦点指数 | `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_focus_ads` | display → `gkxlumen-topic-async-service` `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → Python `POST /internal/policy/jobs/execute` → `polan.eval.focus.run()` 后读 `ads.policy_focus`（`policy_id IS NOT NULL`） |
| 224 解读条目 + 225 多媒体条目 | `GET /display/v1/policy/evaluation/shells` | display → element → `gkxlumenx_gapfill.gapfill_policy_eval_shell` |
| 226 智能摘要 | 同一条 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_text_parse` | 同上管道 → Python 只读 `ads.policy_text_parse.summary`（请求内不调用 `parse.run`） |

空态契约（API 分册第 7 节）：四叶无行则空，HTTP 成功，不造 0、不返回 501、不返回写死 mock；Job 失败不清空已返回的 counts / shells。

---

## 1. 合规交付主路径数据准备

> 本章逐条列出联调前必须就位的数据与脚本，全部幂等可重跑。所有命令为 PowerShell 语法，**不使用 `&&`**。

### DP-01 ads.policy_effect 的 region_gap 行（223 短板）

| 项 | 内容 |
|---|---|
| 前置 | `gkxlumenx_ads` 库（element `{ads}` 占位符指向的库）可连；`policy_effect` 表存在 |
| 操作 | 已有批次写入：`polan.eval.gap.run()`（`lumen-algo-py/vendor/entan-py`）。**本测试不新开灌数单，不执行 `gap.run`（GET counts 也不调用它）** |
| 预期 | `SELECT scope_code, scope_name, shortboard_cnt, metric_id FROM {ads}.policy_effect WHERE scope_type='region_gap' ORDER BY scope_code` 至少 1 行；`shortboard_cnt` 为正整数；行上 `ext` 含 `is_mock` 与 `QPOL-02` 标记（D4=mock 不写成已上线） |
| 空态分支数据 | 空态用例（TC-01b）不需要删除数据：靠"表存在但查询窗口内无 region_gap 行"的等价stub（联调环境若无行，用只读 SELECT 确认 0 行即可触发空态断言，禁止为造空态去 DELETE 生产行） |

### DP-02 gapfill_policy_eval_shell 灌数（224 解读 + 225 多媒体）

| 项 | 内容 |
|---|---|
| 前置 | `gkxlumenx_gapfill` 库（10.50.11.76:3306）可连；脚本 `lumen-algo-py/scripts/seed_gapfill_policy_eval_shell.py` |
| 操作（幂等） | `python scripts/seed_gapfill_policy_eval_shell.py --check`（不连库，校验行并覆写 `scripts/mysql/gapfill_policy_eval_shell.sql`）；随后 `$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"; python scripts/seed_gapfill_policy_eval_shell.py --apply`（DROP→CREATE→INSERT，可重复） |
| 预期 | **7 行 = 4 解读 + 3 多媒体**（派单背景写"5 行（3 解读 + 2 多媒体）"与 GAPFILL 实现单/脚本不符，以实现单 `POL-L2-DS11-READ-GAPFILL-L01` 为准，见偏离说明）。解读 4 条：研发费用加计扣除、科技型中小企业培育、高新技术企业认定、科技创新成果科普传播（各一句结论+一句应用建议，`subject_name/conclusion_text/suggestion_text` 必填且 `title/caption_text` 为 NULL）；多媒体 3 条：研发费用加计扣除政策图解、科技型中小企业政策宣讲实录、高新技术企业认定要点速览（`title/caption_text` 必填，其余业务列 NULL）。全部行 `is_mock=1`、`metric_id` NULL、`fill_method='manual'`、`gapfill_batch_id='POL-L2-DS11-READ-GAPFILL-L01'`、`generated_at='2026-11-03 21:40:00'` |
| 验证 SQL | `SELECT entry_kind, gap_item, COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_shell WHERE is_mock=1 AND metric_id IS NULL GROUP BY entry_kind, gap_item` → 预期 `('解读','224 分主题分指标互动解读',4)`、`('多媒体','225 多媒体辅助解读',3)`、total 7 |
| 幂等重跑 | apply 后重跑一次 apply，行数仍 7（DROP+CREATE+INSERT 自愈）；--check 后重跑，SQL 镜像字节不变 |

### DP-03 policy_focus_ads 任务样本（223 焦点）

| 项 | 内容 |
|---|---|
| 前置 | `ads.policy_focus` 表存在；`polan.eval.focus.run` 可执行（其内部先删除 `policy_id` 非空行再写入，不动 `policy_id` 为空的机遇行） |
| 操作 | 提交 `POST /display/v1/policy/evaluation/jobs`，body `{"sub_type":"policy_focus_ads"}`（不带 items、不带产业 VID——两新键豁免产业 VID XOR 校验） |
| 预期 | Python 侧 `execute_policy_job` 走 `_policy_focus_ads_rows()`：先 `focus_run()` 写表，再 `SELECT focus_score, ext FROM {ads}.policy_focus WHERE policy_id IS NOT NULL`，输出行含 `focus_score` + `ext.title` + `ext.explanation` |
| 幂等重跑 | 同一请求重复提交：每次 Job 重跑 `focus.run()`，删除范围不变，表内 `policy_id` 非空行数不累加；`policy_id` 为空的机遇行始终不被删除（回归断言：跑前后 `SELECT COUNT(*) WHERE policy_id IS NULL` 不变） |

### DP-04 policy_text_parse 任务样本（226 摘要）

| 项 | 内容 |
|---|---|
| 前置 | `ads.policy_text_parse` 表已有解析批次写入的 `summary` 行（行上 `metric_id='M_POLICY_TEXT_PARSE'`） |
| 操作 | 提交 `POST /display/v1/policy/evaluation/jobs`，body `{"sub_type":"policy_text_parse"}` |
| 预期 | Python 走 `_policy_text_parse_rows()`：**只执行** `SELECT summary FROM {ads}.policy_text_parse`，请求内不调用 `polan.text.parse.run` |
| 幂等重跑 / 防破坏断言 | 重复提交 N 次：整表行数与条款结构化行（`summary` 为空的行）数量不变——证明展示请求没有 TRUNCATE 整表（`parse.run` 会清空整表，这是请求内禁止调用它的原因） |

### DP-05 环境前置汇总

| 环境 | 要求 |
|---|---|
| K8s dev | `gkxlumen-display`、`gkxlumen-element`、`gkxlumen-topic-async-service`、`lumen-algo-py` 已发布且含上述 commit |
| 网关 | `/display/v1/**` StripPrefix=1 路由正常 |
| 前端 | `lumen-ui-science-pc` dev（mock 态即可，见第 3 节） |
| 观测 | Java Agent + Python instrument 在线；能按 `X-Trace-Id` 检索日志（tempo/loki） |

---

## 2. 关键路径验证用例

> 每条含编号/前置/步骤/预期/实际结果。实际结果列在本轮执行后回填（联调环境为 K8s dev；本轮以单测+代码走查+mock 前端截图完成可本地验证项，联调环境项标 PENDING）。

### TC-01a counts 有值分支

| 列 | 内容 |
|---|---|
| 编号 | TC-01a |
| 前置 | DP-01 就绪：`policy_effect` 存在 `scope_type='region_gap'` 行 |
| 步骤 | 1. 抓取请求头 `X-Trace-Id`（无则生成 UUID 记录）；2. `GET /display/v1/policy/evaluation/counts`；3. 记录响应 |
| 预期 | HTTP 200；`data.records[]` 至少 1 行，行含 `scopeCode/scopeName/shortboardCnt`（驼峰由 R 包装序列化）；`shortboardCnt` 为正整数且与 DP-01 验证 SQL 结果一致；响应**不含**机遇字段（`M_POLICY_OPPORTUNITY_COUNT` 读面不在本资源）；无 501 |
| 实际结果 | PENDING（待 K8s dev 联调；本地证据：`PolicyGapfillControllerTest` counts 断言绿，见验收证据） |

### TC-01b counts 空态分支

| 列 | 内容 |
|---|---|
| 编号 | TC-01b |
| 前置 | `policy_effect` 无 `region_gap` 行（或表无行） |
| 步骤 | `GET /display/v1/policy/evaluation/counts` |
| 预期 | HTTP 200；`data.records` 为**空列表**；`shortboardCnt` 字段不出现或为 null——**不得返回 0**；不返回 501；GET 路径未调用 `gap.run`（trace 上无 Python `/internal` 调用） |
| 实际结果 | PENDING（同上；本地证据：`PolicyEvaluationServiceTest`「空计数不变成 0」断言绿） |

### TC-02 shells 渲染（解读 + 多媒体）

| 列 | 内容 |
|---|---|
| 编号 | TC-02 |
| 前置 | DP-02 已 apply（7 行） |
| 步骤 | 1. `GET /display/v1/policy/evaluation/shells`；2. 校验行数与两类行字段；3. 记录 X-Trace-Id |
| 预期 | HTTP 200；`data.records` 7 行（mock 联调环境下为 4 解读 + 3 多媒体）；解读行 `entryKind='解读'` 且专题名/结论/建议三字段非空、`title/caption_text` 空；多媒体行反之；全部行 `isMock=1`；排序 `generated_at DESC, id DESC`；无 501。**注**：行内字段名 `topicOrMetric/caption`（Java SHELL_SQL 旧列名）——线上表已改 `subject_name/caption_text` 列名，见 BUG-01 |
| 实际结果 | **未通过（BUG-01）**：Java `SHELL_SQL` 仍 SELECT `topic_or_metric, caption`，线上表（GAPFILL `8c0a59c` 后）列名为 `subject_name, caption_text` → `Unknown column` 被 `ElementDao.listOrEmpty` 吞掉，`shells` 恒返回空列表。需要 api-agent 修复 SHELL_SQL 列名后复测 |

### TC-03a jobs 白名单校验（非法 subType 拒绝）

| 列 | 内容 |
|---|---|
| 编号 | TC-03a |
| 前置 | 服务在线 |
| 步骤 | 依次 POST body：`{"sub_type":"policy_focus_one"}`、`{"sub_type":"report_jobs"}`、`{"sub_type":"evil_type"}`、`{}`（空 body）、`null`（无 body） |
| 预期 | 每次均**不建任务**：返回失败（`R.failed`，msg 含"sub_type 不在政策分析任务白名单"）；topic-async 侧无任务记录产生（`toAsyncCreateBody` 返回 null 短路，不调用 `asyncClient.create`）；counts/shells 不受影响 |
| 实际结果 | PENDING（待联调；本地证据：`PolicyEvaluationServiceTest` 7 tests 含未知 sub_type 不建任务断言，绿） |

### TC-03b jobs 合法新键不要求 items / 不走产业 VID XOR

| 列 | 内容 |
|---|---|
| 编号 | TC-03b |
| 前置 | DP-03/DP-04 数据就绪 |
| 步骤 | POST `{"sub_type":"policy_focus_ads"}`（不带 items/industry_vid）；POST `{"sub_type":"policy_text_parse"}`（同） |
| 预期 | 均进入异步建任务流程（不因缺 items 或产业 VID 二选一被拒）；对比回归：POST `{"sub_type":"policy_focus"}` 不带 items 仍被拒（既有键保持原校验） |
| 实际结果 | PENDING（待联调；本地证据：Java `PolicyAnalysisTypesTest` + Python `test_policy_job.py` 两新键白名单断言绿） |

### TC-04a jobs 异步轮询完成（policy_focus_ads）

| 列 | 内容 |
|---|---|
| 编号 | TC-04a |
| 前置 | DP-03 就绪；登录态有效（display 自动补 `user_id`） |
| 步骤 | 1. POST jobs `{"sub_type":"policy_focus_ads","client_request_id":"qa-focus-001"}`，记录返回的 `task_id`；2. 轮询任务详情（`GET /display/v1/policy/jobs/{taskId}`——`387502a` 新增透传端点，或经前端任务面板）至终态；3. 校验 result |
| 预期 | 任务终态成功；result 为 `ads.policy_focus` 中 `policy_id` 非空行的 `focus_score`+`ext.title`+`ext.explanation` 数组；无行则空数组（不返回写死指数、不返回 `focus-one` 当场计算结果）；重复提交（DP-03 幂等）后机遇行数不变 |
| 实际结果 | PENDING（待联调；本地证据：Python `test_policy_job.py` `_policy_focus_ads_rows` 空表/有表两分支 + dispatch 断言绿） |

### TC-04b jobs 异步轮询完成（policy_text_parse）

| 列 | 内容 |
|---|---|
| 编号 | TC-04b |
| 前置 | DP-04 就绪 |
| 步骤 | 1. POST jobs `{"sub_type":"policy_text_parse","client_request_id":"qa-parse-001"}`；2. 轮询至终态；3. 校验 result 与表未被清空 |
| 步骤补充 | 3'. 跑前后各执行 `SELECT COUNT(*) FROM {ads}.policy_text_parse` |
| 预期 | 终态成功；result 为 `summary` 列行数组；**表行数不变、条款结构化行不被清空**（证明请求未调用 `parse.run`）；无行则空（不返回写死段落） |
| 实际结果 | PENDING（待联调；本地证据：Python 测试断言"请求 SQL 只有 SELECT summary"绿） |

### TC-05 X-Trace-Id 贯通断言

| 列 | 内容 |
|---|---|
| 编号 | TC-05 |
| 前置 | 观测栈在线（tempo/loki 可检索） |
| 步骤 | 1. 以固定 traceId（如 `qa-trace-ds11-read-0001`）发起 TC-01a 请求（注入 `X-Trace-Id` 头）；2. 同 traceId 发起 TC-04a；3. 在日志/trace 平台按该 traceId 检索 |
| 预期 | 同一 traceId 串起：网关 → `gkxlumen-display`（counts 或 PolicyEvaluationService）→ `gkxlumen-element`（counts 路径）/ `gkxlumen-topic-async-service` → Python `/internal/policy/jobs/execute`（jobs 路径）各 span；counts 同步链无 Python span（证明 GET 未调 `gap.run`/未越层） |
| 实际结果 | PENDING（待 K8s dev + 观测栈联调） |

### TC-06 Job 失败不清空 counts/shells（回归）

| 列 | 内容 |
|---|---|
| 编号 | TC-06 |
| 前置 | TC-01a、TC-02 已通过（有基线值） |
| 步骤 | 1. 制造 Job 失败（如 Python 侧 DB 闪断或提交会触发异常的参数）；2. Job 失败后重读 counts、shells |
| 预期 | counts/shells 返回与失败前一致（只读资源不被 Job 失败清空） |
| 实际结果 | PENDING（待联调；本地证据：`PolicyEvaluationServiceTest`「任务失败后 counts/shells 仍可再读」断言绿） |

### 用例汇总

| 编号 | 一句话 | 状态 |
|---|---|---|
| TC-01a/01b | counts 有值/空态 | 单测绿；联调 PENDING |
| TC-02 | shells 3+2（实际 4+3）渲染 | **未通过（BUG-01 列名错位）** |
| TC-03a/03b | jobs 白名单与两新键豁免 | 单测绿；联调 PENDING |
| TC-04a/04b | 两 Job 异步完成与防破坏 | 单测绿；联调 PENDING |
| TC-05 | X-Trace-Id 贯通 | PENDING |
| TC-06 | Job 失败不清空只读面 | 单测绿；联调 PENDING |

---

## 3. 界面操作过程（lumen-ui-science-pc · 结果解读页）

> 前置：前端 `pnpm dev`（mock 态）。入口：左侧导航「科技政策跟踪」→ 页签「政策分析评价」→ 子 Tab「结果解读报告多维展示」。截图目录 `agent-handoffs/科技政策跟踪-POL/assets/POL-L2-DS11-READ-TEST-L01/`。

| 步骤 | 操作 | 预期 | 截图 |
|---|---|---|---|
| S1 | 打开 `http://localhost:5173`，进入「政策分析评价」页，点击子 Tab「结果解读报告多维展示」 | 出现 T41 闸门条（评审模式）与四块：热点问题分析看板、分主题分指标互动解读、多媒体+智能摘要、政策文本辅助解读 | `01-open-interpret-tab.png` |
| S2 | 查看短板卡：热点问题分析看板内的热度条形图与问题列表 | 图表渲染（异常标红）、列表可读；MockBadge 🧪 在卡片右上；统计数字旁 ⓘ 可点开 MetricSpecCard | `02-shortboard-board.png` |
| S3 | 展开解读：在「分主题分指标互动解读」点选专题按钮，再点指标 CheckableTag 聚焦 | 指标行重新排序（聚焦项置顶）、结论高亮与应用建议展示 | `03-interactive-interpret.png` |
| S4 | 触发焦点指数任务：在看板焦点区点击触发任务按钮（mock 态走本地任务状态机） | 任务进入执行中 → 轮询 → 完成，展示焦点指数结果卡 | `04-focus-job.png` |
| S5 | 查看结果：多媒体辅助面板标题/说明渲染；智能摘要块展示摘要文本 | 多媒体 3 条标题+说明、摘要可编辑态展示、🧪 角标在位 | `05-summary-media.png` |

界面操作结论：mock 态五步全部可操作（截图见第 4 节嵌入）；接真实后端后 S2 数据源切换为 `counts`/`shells`/`jobs`，交互不变。

---

## 4. 缺陷与风险记录

| 编号 | 级别 | 描述 | 影响 | 建议 |
|---|---|---|---|---|
| BUG-01 | **P1（阻塞 shells 联调）** | `gkxlumen-element` `PolicyGapfillController.SHELL_SQL` 仍 SELECT 旧列 `topic_or_metric`、`caption`；GAPFILL 单 `8c0a59c` 后线上表列已改 `subject_name`、`caption_text`。`Unknown column` 异常被 `ElementDao.listOrEmpty` 捕获后返回空列表 | `GET /display/v1/policy/evaluation/shells` 恒空，224/225 两叶在联调环境等于无数据 | 派 api-agent 修复 SHELL_SQL 为 `subject_name, caption_text`（一行改动 + 对应单测列名断言），随后复测 TC-02 |

风险（非缺陷）：

- 派单背景「shells 5 行（3 解读 + 2 多媒体）」与实现真源 7 行（4+3）不一致，测试按 7 行断言（见 handoff 偏离说明）。
- counts 的空态分支在联调环境难以无损构造（不能 DELETE 生产行）；若环境恰有数据，TC-01b 以单测证据 + 代码走查（`records` 空列表路径）为准。

## 5. 结论

- 数据准备（DP-01~04）口径已固化，全部幂等。
- 后端既有单测（Java 23 + Python 36）覆盖了 TC-01/03/04/06 的核心断言，全绿。
- **TC-02 被 BUG-01 阻塞**：需先修复 Java SHELL_SQL 列名错位，再上 K8s dev 完成 TC-01a/02/04/05 联调复测。
- 前端 mock 态操作链路（S1–S5）可走通并已截图（见 assets 目录）。
