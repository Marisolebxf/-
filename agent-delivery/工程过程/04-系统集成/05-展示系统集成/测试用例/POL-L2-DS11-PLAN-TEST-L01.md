# POL-L2-DS11-PLAN-TEST-L01 · 推荐方案报告交互展示 · 集成测试用例

- 任务：`POL-L2-DS11-PLAN-TEST-L01`（WBS 行 `WBS-05-23-L2-07F`）
- 日期：2026-11-04
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 被测链路：DS11 推荐方案报告交互展示（SRS 227–231）
- 设计真源：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-ARCH.md`、`sdd/l2/POL-L2-DS11-PLAN-API.md`、`sdd/l2/POL-L2-DS11-PLAN-DATA.md`（2026-11-03 四角色同意，已签收）
- 灌数证据：`POL-L2-DS11-PLAN-GAPFILL-L01.md`（commit `423527e`，`gapfill_policy_eval_scheme` 19 行）
- 实现单：`POL-L2-DS11-PLAN-WIRING-L01`（前端接线，**进行中**——界面验证阶段被测对象）
- 强度：ponytail full

## 0. 接口与链路总览（被测对象）

五叶都在评价页推荐方案工作区内完成，不另开页。浏览器只打 `/display/v1/policy/**`，一次请求只带一种类。全部同步，不建任务、不进 `gkxlumen-topic-async-service`、不调 Python。

| 序号 | 公开资源 | 链路 |
|---|---|---|
| 227 方案对照 | `POST /display/v1/policy/evaluation/jobs`（种类=方案对照） | 前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的 `row_kind=方案对照` 行 |
| 228 参数模拟 | 同一条 `jobs`（种类=参数模拟） | 同链路，按 `scheme_name`+`param_band` 拣 `row_kind=参数模拟` 行 |
| 229 路径与风险 | 同一条 `jobs`（种类=路径与风险） | 同链路，按 `scheme_name` 拣 `row_kind=路径与风险` 行。行上 `metric_id` 固定 `M_POLICY_DS_11_POLICY_EVAL_015`（D4=mock） |
| 230 互动意见 | `GET /display/v1/policy/evaluation/shells`（种类=互动意见） | 同链路，按 `scheme_name` 拣 `row_kind=互动意见` 行。请求只读，不插入 |
| 231 方案报告 | 同一条 `shells`（种类=方案报告） | 同链路，同次读方案对照行+互动意见行，导出正文从行生成。不灌文件、不写对象存储 |

空态契约（API 分册第 8 节）：五叶无行则对应块空，HTTP 成功，**不返回 501、不返回写死 mock、不补默认方案、不造意见**；某次 `jobs`/`shells` 失败不清空 `evaluation/counts` 与其他种类已返回的区块。

230/231 交互壳特殊口径：意见收集与方案归档是**演示态写操作，不落库**。验证点是界面行为诚实——页面新打的意见/采纳动作不产生"已保存成功"的伪造反馈、刷新后消失、库内行数不变；不是"库内有新行"。

## 1. 合规交付主路径数据准备

> 逐条列出验证前必须就位的数据与脚本，全部幂等可重跑。命令为 PowerShell 语法，**不使用 `&&`**。数据库口令只放进程环境变量，取值来源 `repos/lumen-algo-py/k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_PASSWORD`（勿写入脚本与文档明文）。

### DP-01 `gapfill_policy_eval_scheme` 灌数（227/228/229/230 四种类行集）

| 项 | 内容 |
|---|---|
| 前置 | `gkxlumenx_gapfill` 库（10.50.11.76:3306，账号 `gkxlumenx`）可连；脚本 `lumen-algo-py/scripts/seed_gapfill_policy_eval_scheme.py` |
| 操作（幂等） | 在 `repos/lumen-algo-py` 下：`python scripts/seed_gapfill_policy_eval_scheme.py --check`（不连库，校验行并覆写 `scripts/mysql/gapfill_policy_eval_scheme.sql`）；随后 `$env:LUMEN_ALGO_MYSQL_PASSWORD = "<取自 k8s/worker.yaml>"; python scripts/seed_gapfill_policy_eval_scheme.py --apply`（DROP→CREATE→INSERT，可重复） |
| 预期 | **19 行 = 2 方案对照 + 5 参数模拟 + 6 路径与风险 + 6 互动意见**。方案 2 个：研发投入加力方案、人才引育优先方案。参数模拟 5 档：研发方案（资金规模基准档/资金规模加力档/平台支撑强化档）+ 人才方案（人才规模基准档/人才规模扩容档）。路径每方案 3 节点共 6 行，`metric_id` 全部命中 `M_POLICY_DS_11_POLICY_EVAL_015`。意见每方案 3 条共 6 行，分类 评价/评论/建议 各 2 条。全行 `is_mock=1`、`fill_method='manual'`、`gapfill_batch_id='POL-L2-DS11-PLAN-GAPFILL-L01'`、`generated_at='2026-11-03 21:40:00'` |
| 验证 SQL | `SELECT row_kind, COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_scheme GROUP BY row_kind` → 预期 `('互动意见',6)`、`('参数模拟',5)`、`('方案对照',2)`、`('路径与风险',6)`；`SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_scheme WHERE row_kind<>'路径与风险' AND metric_id IS NOT NULL` → 0（其余三种 metric 留空不违例） |
| 幂等重跑 | apply 连跑两次，total 仍 19（先 DELETE 本表再 INSERT，不碰别的表） |
| 已核实 | ✅ 2026-11-04 QA 连库复核（`by_kind`/`is_mock`/`path_with_metric=6`/`other_with_metric=0`/param_keys/意见分类计数全中），见第 5 节结论 |

### DP-02 意见行分类闭集与挂靠（230 前置）

| 项 | 内容 |
|---|---|
| 前置 | DP-01 已 apply |
| 验证 SQL | `SELECT DISTINCT opinion_class FROM gkxlumenx_gapfill.gapfill_policy_eval_scheme WHERE row_kind='互动意见'` → 只有 `评价/评论/建议` 三个值；`SELECT DISTINCT scheme_name FROM gkxlumenx_gapfill.gapfill_policy_eval_scheme WHERE row_kind<>'方案对照'` → 每个名字都对得上某条方案对照行（外行不悬空） |
| 防串库断言 | 互动意见行**不来自**序号 210 的 `gapfill_policy_audience_feedback`：`SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_audience_feedback WHERE 1=1` 的行与 `gapfill_policy_eval_scheme` 意见行 `opinion_text` 无交集（有表则抽查；无表则跳过并记录） |

### DP-231 导出数据面（231 前置，无需新灌）

| 项 | 内容 |
|---|---|
| 前置 | DP-01 已 apply。231 不占 `row_kind`、不灌行、不灌文件 |
| 验证 | 导出正文来源只有两类行：方案对照行（名称/说明/优劣/建议/对照维度）+ 互动意见行（主体/分类/正文/时间）。参数模拟行、路径与风险行**不进入**导出——实现层按读取范围断言，表内无需额外准备 |
| 文件禁区 | 库内无 `.pdf/.docx/.xlsx` 类文件行、无对象存储键（灌数脚本 BANNED 已挡；QA 抽查 `SHOW COLUMNS` 无文件列即可） |

### DP-05 环境前置汇总

| 环境 | 要求 |
|---|---|
| K8s dev | `gkxlumen-display`、`gkxlumen-element` 已发布；`evaluation/jobs` 与 `evaluation/shells` 按种类分发（含本五叶种类） |
| 前端 | `lumen-ui-science-pc` dev 已含 `POL-L2-DS11-PLAN-WIRING-L01` 接线（**当前该单 in_progress，此为第二阶段硬前置**）；mock 态可先走第 3 节本地路径 |
| 观测 | Java Agent 在线，display→element 带 traceId，可按 `X-Trace-Id` 检索 |
| 口令 | 连库口令从 `repos/lumen-algo-py/k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_PASSWORD` 取，只放进程环境变量 |

## 2. 关键路径验证用例

> 每条含编号/前置/步骤/预期/实际结果。**期望未发生必红**：凡预期栏写"不返回/不出现/不调用/不插入"的断言，发生即为失败。联调环境为 K8s dev；WIRING 单完成前，接口路径可在 `gkxlumen-display`/`gkxlumen-element` 侧验证，界面路径标 PENDING。

### TC-01a 227 方案对照 · 正常态（有行）

| 列 | 内容 |
|---|---|
| 编号 | TC-01a |
| 前置 | DP-01 就绪（方案对照 2 行） |
| 步骤 | 1. 记录 `X-Trace-Id`；2. `POST /display/v1/policy/evaluation/jobs`（种类=方案对照，不选方案）；3. 再带单个 `scheme_name` 提交一次 |
| 预期 | HTTP 200；不选方案时返回**全部 2 行**（研发投入加力方案、人才引育优先方案），行含名称/一句说明/对照维度数值/优劣结论/实施建议；选方案时只返回对得上的 1 行；对照维度数值与 DP-01 表内 `compare_dims` 逐项一致；无 501 |
| 实际结果 | PENDING（待 WIRING 完成后 K8s dev 联调） |

### TC-01b 227 方案对照 · 空态（少于两行 / 对不上）

| 列 | 内容 |
|---|---|
| 编号 | TC-01b |
| 前置 | 服务在线 |
| 步骤 | POST jobs 种类=方案对照，`scheme_name` 传一个表内没有的值（如"不存在的方案"） |
| 预期 | HTTP 200；返回**空列表**——不补第二个方案、不造演示分、不返回 demo `policyData.js` 的三条常量、无 501。**红线**：响应里出现写死方案或 `recommendationSchemes` 原文即失败 |
| 实际结果 | PENDING |

### TC-02a 228 参数模拟 · 正常态（方案+参数档对上）

| 列 | 内容 |
|---|---|
| 编号 | TC-02a |
| 前置 | DP-01 就绪 |
| 步骤 | 依次 POST jobs（种类=参数模拟）：研发投入加力方案 × 3 档（资金规模基准档/加力档/平台支撑强化档）、人才引育优先方案 × 2 档（人才规模基准档/扩容档），共 5 组 |
| 预期 | 每组 HTTP 200，返回该 `scheme_name`+`param_band` 唯一行：评估结果原文、一句趋势、一条归档说明，与表内 `eval_result/trend_text/archive_note` 逐字一致；换参数=换查询，**请求内不重算**（响应时间稳定、trace 上无 Python `/internal` 调用、无 `polan.text.simulate` 调用）；无 501 |
| 实际结果 | PENDING |

### TC-02b 228 参数模拟 · 空态（参数档对不上）

| 列 | 内容 |
|---|---|
| 编号 | TC-02b |
| 前置 | DP-01 就绪 |
| 步骤 | POST jobs（种类=参数模拟），`scheme_name=研发投入加力方案`、`param_band=不存在的档位` |
| 预期 | HTTP 200；预览/趋势/归档**全空**——不现算、不返回省级力度情景曲线、不返回 `M_POLICY_SIMULATE` 的基线/变化率、无 501。**红线**：出现弹性公式现算值或推演曲线顶替即失败 |
| 实际结果 | PENDING |

### TC-03a 229 路径与风险 · 正常态（有节点行）

| 列 | 内容 |
|---|---|
| 编号 | TC-03a |
| 前置 | DP-01 就绪 |
| 步骤 | POST jobs（种类=路径与风险），分别带两个 `scheme_name` |
| 预期 | 每方案 HTTP 200 返回 3 个节点行，按库内顺序（表无 `sort_no` 列，读取顺序按 `id` 升序，节点名/时间进度/一句说明/风险标题/一句风险五要素齐备，与表内一致）；无 501 |
| 实际结果 | PENDING |

### TC-03b 229 路径与风险 · 空态与禁区

| 列 | 内容 |
|---|---|
| 编号 | TC-03b |
| 前置 | 服务在线 |
| 步骤 | 1. POST jobs（种类=路径与风险），`scheme_name` 传不存在的值；2. 检查 trace |
| 预期 | HTTP 200；路径和风险**都空**——不读图（trace 无 nGQL/Nebula span）、不返回推演曲线顶替、不返回序号 241 推演页路径、无 501。**红线**：读政策子图或返回 `polan.text.simulate` 曲线即失败 |
| 实际结果 | PENDING |

### TC-04a 230 互动意见 · 正常态（有意见行）

| 列 | 内容 |
|---|---|
| 编号 | TC-04a |
| 前置 | DP-01/DP-02 就绪 |
| 步骤 | GET `shells`（种类=互动意见），分别带两个 `scheme_name` |
| 预期 | 每方案 3 条意见（主体/分类/正文/时间四要素齐备），分类只出现 评价/评论/建议；与表内 `opinion_subject/opinion_class/opinion_text/opinion_at` 一致；不读壳表 `gapfill_policy_eval_shell`、不读模板表 `gapfill_policy_eval_template`、无 501 |
| 实际结果 | PENDING |

### TC-04b 230 互动意见 · 空态 + 不落库（交互壳核心断言）

| 列 | 内容 |
|---|---|
| 编号 | TC-04b |
| 前置 | DP-01 就绪；前端页面可操作（mock 态或 dev 均可） |
| 步骤 | 1. GET shells（种类=互动意见）不选方案 → 断言空；2. 页面上对某方案**新打一条意见并提交**；3. 刷新页面/重进工作区；4. 重跑 DP-01 验证 SQL 的意见计数 |
| 预期 | 步骤 1 未选方案返回**空列表**，不返回全部意见；步骤 2/3 界面行为诚实——提交后可以有"演示态不落库"类明示反馈或仅本地暂存，**不得**出现伪造的"已保存成功/已归档"记录；刷新后新打的字消失（不留浏览器外状态）；步骤 4 库内 `互动意见` 仍为 6 行——**请求不插入、不更新、不删除**。**红线**：库内行数变化即失败 |
| 实际结果 | PENDING（步骤 1 可先行；步骤 2–4 待 WIRING） |

### TC-05a 231 方案报告 · 正常态（从已读行生成）

| 列 | 内容 |
|---|---|
| 编号 | TC-05a |
| 前置 | DP-01 就绪 |
| 步骤 | GET `shells`（种类=方案报告），选一个方案；核对导出内容字段来源 |
| 预期 | HTTP 200；导出正文由该方案**当次读到的**方案对照行（名称/说明/优劣结论/实施建议/对照值）+ 挂其上的互动意见行（主体/分类/正文/时间）拼装，内容与表内行一致；**参数模拟行与路径与风险行不出现在导出正文**；无 501 |
| 实际结果 | PENDING |

### TC-05b 231 方案报告 · 空态与文件禁区（交互壳核心断言）

| 列 | 内容 |
|---|---|
| 编号 | TC-05b |
| 前置 | 服务在线；前端页面可操作 |
| 步骤 | 1. GET shells（种类=方案报告）不带有效方案对照范围 → 断言导出空；2. 页面点"导出/采纳"类操作；3. 检查响应与库 |
| 预期 | 无方案对照行则**导出空**——不返回写死的 PDF/Word/Excel、不返回内嵌文件字节、不写对象存储、不新建桶、前端不直连 RustFS；导出动作可以有"演示态"明示反馈，**不得**伪造"已归档成功"记录；库内行数不变（采纳不插新行）。**红线**：响应中出现文件字节/对象键，或库内多出采纳行即失败 |
| 实际结果 | PENDING（步骤 1 可先行；步骤 2–3 待 WIRING） |

### TC-06 种类隔离与失败不串块（回归）

| 列 | 内容 |
|---|---|
| 编号 | TC-06 |
| 前置 | TC-01a/02a/03a/04a 已有基线返回 |
| 步骤 | 1. 依次单种类提交五次请求，核对每次只返回该种类行；2. 制造一次 `jobs` 失败（如停 element 或断库闪断）；3. 失败后重读 `evaluation/counts` 与其他种类块 |
| 预期 | 一次请求只带一种类——方案对照请求**不**夹带参数模拟/路径/意见行，反之亦然；某次失败后 counts 已返回的短板/机遇条数**不被清空**，其他种类已返回区块**不被清空**；整条 `jobs`/`shells` 未被改成只读方案表（趋势/分区/模板/焦点/摘要种类不受本二级影响） |
| 实际结果 | PENDING |

### TC-07 X-Trace-Id 贯通断言

| 列 | 内容 |
|---|---|
| 编号 | TC-07 |
| 前置 | 观测栈在线 |
| 步骤 | 以固定 traceId（如 `qa-trace-ds11-plan-0001`）注入 `X-Trace-Id` 头发起 TC-01a/02a/03a/04a/05a 五次请求，日志平台检索 |
| 预期 | 同一 traceId 串起：网关 → `gkxlumen-display` → `gkxlumen-element` 各 span；**全链无 Python span、无 topic-async span、无 SSE/任务建单 span**（证明五叶同步只读、不进异步管道、不越层直连） |
| 实际结果 | PENDING |

### 用例汇总

| 编号 | 一句话 | 状态 |
|---|---|---|
| TC-01a/01b | 227 方案对照有值/空态 | 文档就绪；联调 PENDING |
| TC-02a/02b | 228 参数模拟五档/空态 | 文档就绪；联调 PENDING |
| TC-03a/03b | 229 路径风险三节点/空态禁区 | 文档就绪；联调 PENDING |
| TC-04a/04b | 230 意见正常/空态+不落库 | 文档就绪；联调 PENDING |
| TC-05a/05b | 231 报告生成/空态文件禁区 | 文档就绪；联调 PENDING |
| TC-06 | 种类隔离与失败不串块 | 文档就绪；联调 PENDING |
| TC-07 | X-Trace-Id 贯通 | 文档就绪；联调 PENDING |

## 3. 界面操作过程（lumen-ui-science-pc · 政策分析评价页推荐方案工作区）

> 前置：`POL-L2-DS11-PLAN-WIRING-L01` 完成并发布 K8s dev。入口：左侧导航「科技政策跟踪」→「政策分析评价」→ 推荐方案工作区。截图目录 `agent-handoffs/科技政策跟踪-POL/screenshots/POL-L2-DS11-PLAN-TEST-L01/`。每步正常态+空态双路径各一张，截图须含页面状态可辨识要素。

| 步骤 | 操作 | 预期 | 截图 |
|---|---|---|---|
| S1 | 打开政策分析评价页，进入推荐方案工作区 | 227 对比区块渲染：两方案雷达/KPI 并排；MockBadge 🧪 在位（D4=mock）；ⓘ 可点开 | `01-scheme-compare-normal.png` |
| S1b | 227 空态：接口对不上方案（或断行）时查看对比区 | 对比区空态提示，不造第二个方案、不出演示分 | `02-scheme-compare-empty.png` |
| S2 | 228：选方案「研发投入加力方案」+ 切三档参数 | 每档展示对应评估结果/趋势/归档；切参数不自动起任务、无 loading 任务态 | `03-param-sim-bands.png` |
| S2b | 228 空态：选不存在的参数档 | 预览/趋势区空，不出现现算曲线 | `04-param-sim-empty.png` |
| S3 | 229：查看两方案实施路径 | 每方案 3 节点按序展示（节点/时间/说明/风险标题/风险说明）；ⓘ 或角标显示 `M_POLICY_DS_11_POLICY_EVAL_015`（D4=mock 不写成已上线） | `05-path-risk-normal.png` |
| S3b | 229 空态：无路径行方案 | 路径与风险区都空 | `06-path-risk-empty.png` |
| S4 | 230：选方案查看意见列表；在输入框打一条新意见提交后刷新 | 已灌 3 条意见（主体/分类/正文/时间）展示；新意见提交后刷新消失，界面无伪造"已保存成功"，库内行数不变（诚实演示态） | `07-opinions-normal.png` / `08-opinion-demo-no-persist.png` |
| S4b | 230 空态：不选方案 | 意见列表空，不返回全部意见 | `09-opinions-empty.png` |
| S5 | 231：点导出方案报告 | 导出内容从当次读到的方案行+意见行生成（正文可核对）；文件由前端从行生成，无对象存储上传 | `10-report-export-normal.png` |
| S5b | 231 空态：无方案对照行时点导出 | 导出空/不可用提示；无写死文件下发；采纳类操作无伪造归档记录 | `11-report-export-empty.png` |

界面操作结论：**PENDING——`POL-L2-DS11-PLAN-WIRING-L01` 仍 in_progress（2026-11-04 00:14 查注册表），S1–S5b 待其完成并发布后执行**。

## 4. 缺陷与风险记录

| 编号 | 级别 | 描述 | 影响 | 建议 |
|---|---|---|---|---|
| RISK-01 | 观察项 | DATA 分册第 2 节列名（`summary_text`/`verdict_text`/`advice_text`/`compare_items`/`schedule_text`/`node_text`/`risk_text`/`actor_name`/`opinion_kind`/`opinion_text`/`sort_no`）与灌数脚本+线上实际列名（`scheme_brief`/`pros_cons_text`/`suggestion_text`/`compare_dims`/`time_progress`/`node_note`/`risk_note`/`opinion_subject`/`opinion_class`/无 `sort_no`）不一致；线上 26 列已由 QA 连库核实 | 文档层口径分歧。读取方若照 DATA 分册写 SQL 会撞 `Unknown column`（同 DS11-READ 的 BUG-01 教训） | 实现以线上真表为准（GAPFILL 单 `423527e` 为落库真源）；建议 coordinator 令 DATA 分册补一行 as-built 备注，避免后续叶复制错列名 |
| RISK-02 | 依赖 | 界面验证阶段硬依赖 `POL-L2-DS11-PLAN-WIRING-L01`（in_progress）；TC-01b/02b/03b 步骤 1 与 TC-06 种类隔离可在其完成前由 display/element 侧先行 | 第 3 节截图与 TC-04b/05b 的页面步骤暂不能执行 | WIRING 转 done 后 QA 补做第二阶段；本轮不空转等待 |

## 5. 结论

- 数据准备（DP-01/DP-02/DP-231）口径已固化并**连库核实**：19 行四种类行集、`metric_id` 仅路径行命中 6 行、其余种类 0 违例、意见分类闭集齐备——DP-01 状态 ✅。
- 关键路径用例 TC-01~TC-07 共 13 条（五叶正常态+空态双路径、交互壳不落库诚实断言、种类隔离、trace 贯通）已成文，红线断言明确（期望未发生必红）。
- **第二阶段（界面验证+截图）阻塞于 `POL-L2-DS11-PLAN-WIRING-L01`**（in_progress）：S1–S5b 与 TC-04b/05b 页面步骤、TC-01~05 联调实测待其 done 后执行并回填本文档"实际结果"列。
- 每叶判定见 handoff `POL-L2-DS11-PLAN-TEST-L01.md`。
