# POL-L2-DS11-VIZ-TEST-L01 · 政策分析报告可视化呈现 · 集成测试用例

- 任务：`POL-L2-DS11-VIZ-TEST-L01`（WBS 行 `WBS-05-23-L2-05F`）
- 日期：2026-11-04
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 被测链路：DS11 政策分析评价 · 政策分析报告可视化呈现（SRS **219–222** 四叶）
- 设计真源：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-ARCH.md`、`sdd/l2/POL-L2-DS11-VIZ-API.md`、`sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- 数据单：`POL-L2-DS11-VIZ-GAPFILL-L01`（trend 44 行 / partition 41 行，2026-11-03 已落库）、`POL-L2-DS11-VIZ-TEMPLATE-L01`（template 10 行 / 6 模板，2026-11-03 已落库）
- 强度：ponytail full
- 本轮状态：第一阶段（用例文档 + 连库数据验证）已完成；第二阶段（界面验证 + 截图）待 `POL-L2-DS11-VIZ-WIRING-L01`（前端接线）完成后执行，见第 3、5 节

## 0. 接口与链路总览（被测对象）

| 序号 | 公开资源 | 链路（同步，不建任务） |
|---|---|---|
| 219 多维指标趋势图 | `POST /display/v1/policy/evaluation/jobs`，`kind=趋势` | 前端 → 网关 → `gkxlumen-display`（`PolicyEvaluationService.syncKind`）→ `gkxlumen-element` `GET /v1/element/policy/evaluation/trend` → `gkxlumenx_gapfill.gapfill_policy_eval_trend` |
| 220 分区/群体对比分析图 | 同一资源另一次请求，`kind=分区` | display `syncKind` → element `GET /v1/element/policy/evaluation/partition` → `gkxlumenx_gapfill.gapfill_policy_eval_partition` |
| 221 多维结构关联图 | **不设 `/display/v1/policy` 资源** | 只消费第 7 项已有政策子图（`E-E7-POLICY-M1-L02` 已完成）。挂接空则弦线图、关系网、路径都空。无任何新请求 |
| 222 报告模板定制与批量导出 | `GET /display/v1/policy/evaluation/shells`，`kind=模板选用` | display → element → `gkxlumenx_gapfill.gapfill_policy_eval_template`（**实现现状缺口，见 GAP-01**） |

空态契约（API 分册第 7 节）：四叶无行或条件对不上则空，**HTTP 成功**，不造 0、不造曲线、不返回 501、不返回写死 mock；`kind` 与 `sub_type` 同传则该块空，不建任务不读表；某块读失败不清空同页 counts / shells 已返回内容。

219/220/222 不进 `gkxlumen-topic-async-service`、不调 Python、不占并发锁、不发 SSE——**期望未发生必红**（见 TC-06）。

---

## 1. 合规交付主路径数据准备

> 三张 gapfill 表均由灌数单建表灌入，**本测试不新开灌数单、不执行任何写库操作**，连库验证只做只读 SELECT。库实例 `10.50.11.76:3306`，账号 `gkxlumenx`，库 `gkxlumenx_gapfill`。口令取自 `repos/lumen-algo-py/k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_PASSWORD`（LUMEN_ALGO_MYSQL_HOST/PORT/USER 同源），**只置入进程环境变量，不打印、不写入脚本与本文**。所有命令为 PowerShell 语法，不使用 `&&`。

### DP-01 gapfill_policy_eval_trend（219 趋势，44 行）

| 项 | 内容 |
|---|---|
| 前置 | 库 `gkxlumenx_gapfill` 可连（只读）；表由 GAPFILL 单 commit `0942212` 建 |
| 操作（只读） | `$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"` 后以任意 MySQL 只读客户端执行下述验证 SQL |
| 验证 SQL 1（总行数） | `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_trend` → 预期 **44** |
| 验证 SQL 2（分维） | `SELECT switch_dim, COUNT(*), COUNT(DISTINCT metric_name) FROM gkxlumenx_gapfill.gapfill_policy_eval_trend GROUP BY switch_dim` → 预期 **时间 24 行/4 指标、区域 12 行/2 指标、类别 8 行/2 指标** |
| 验证 SQL 3（正常态拣行样本） | `SELECT dim_value, point_value, is_key_point, is_fluctuation FROM ... WHERE switch_dim='时间' AND metric_name='科技政策连续出台数' ORDER BY dim_value` → 预期 6 行 2021–2026：48→62→75→83→79(波动)→91(重点) |
| 验证 SQL 4（空态拣行） | `... WHERE switch_dim='行业'` → 预期 **0 行**（`行业` 不是 219 的切换维，是 220 的对象类——闭集互不串用） |
| 验证 SQL 5（追溯列） | `SELECT COUNT(*) FROM ... WHERE is_mock=1 AND metric_id IS NULL AND fill_method='manual' AND gap_item='219 多维指标趋势图'` → 预期 **44**（全部行） |
| 幂等基线 | 灌数单 `--apply` 先 DELETE 再 INSERT，连跑两次行数不变（已由 data-agent 验证；QA 只读复核行数即可，不重跑写库） |

**列名 as-built 说明**：`POL-L2-DS11-VIZ-DATA` 第 2 节的列名 `axis_kind`/`axis_position`/`compare_value`，落库与 element `TREND_SQL` 实际为 `switch_dim`/`dim_value`/`point_value`，且新增 `is_key_point`/`is_fluctuation` 两标记列（重点/波动标注的载体）。测试按 **as-built** 断言；差异属灌数单对 DATA 分册的实现落词，由 DATA 分册签收人知悉，不在本单修文（本单禁改设计文档）。

### DP-02 gapfill_policy_eval_partition（220 分区，41 行）

| 项 | 内容 |
|---|---|
| 前置 | 同 DP-01；表由同一 GAPFILL 单建 |
| 验证 SQL 1（总行数） | `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_partition` → 预期 **41** |
| 验证 SQL 2（分对象类） | `SELECT object_kind, COUNT(*) FROM ... GROUP BY object_kind` → 预期 **地区 24、行业 10、目标群体 7** |
| 验证 SQL 3（正常态拣行样本） | `SELECT object_name, compare_value FROM ... WHERE object_kind='行业' AND resource_direction='财政资金' ORDER BY compare_value` → 预期 5 行：新材料 96.5、新能源 104、生物医药 121、高端装备 118、电子信息 132.5 |
| 验证 SQL 4（投向闭集） | `SELECT DISTINCT resource_direction FROM ... ORDER BY resource_direction` → 预期只有 财政资金、人才引进、创新平台、税费减免（非空四值） |
| 验证 SQL 5（空态拣行） | `... WHERE object_kind='行业' AND resource_direction='装备制造'` → 预期 **0 行**（投向对不上） |
| 验证 SQL 6（追溯列） | 同 DP-01 口径，`gap_item='220 分区/群体对比分析图'` → 预期 **41** |

### DP-03 gapfill_policy_eval_template（222 模板，10 行 / 6 模板）

| 项 | 内容 |
|---|---|
| 前置 | 同 DP-01；表由 TEMPLATE 单（修复 commit 后）建 |
| 验证 SQL 1（总行数/模板数） | `SELECT COUNT(*), COUNT(DISTINCT template_name) FROM gkxlumenx_gapfill.gapfill_policy_eval_template` → 预期 **10 / 6** |
| 验证 SQL 2（闭集全覆盖） | `SELECT COUNT(DISTINCT analysis_dim), COUNT(DISTINCT chart_kind) FROM ...` → 预期 **6 / 5**（维度六值：时间/区域/类别/地区/行业/目标群体；图表五值：趋势/柱状/热力/弦线/关系网） |
| 验证 SQL 3（正常态拣行样本） | `SELECT report_period, analysis_dim, chart_kind FROM ... WHERE template_name='区域政策效果季度对比' ORDER BY id` → 预期 2 行：季度/地区/柱状、季度/地区/热力 |
| 验证 SQL 4（空态拣行） | `... WHERE template_name='不存在的模板'` → 预期 **0 行** |
| 验证 SQL 5（并格回归） | `SELECT COUNT(*) FROM ... WHERE report_period LIKE '%,%' OR analysis_dim LIKE '%,%' OR chart_kind LIKE '%,%'` → 预期 **0**（DATA 第 5 节：多组合拆多行，不并格） |
| 验证 SQL 6（追溯列） | 同上口径，`gap_item='222 报告模板定制与批量导出'`、`gapfill_batch_id='POL-L2-DS11-VIZ-TEMPLATE-L01'` → 预期 **10** |

### DP-04 221 数据前提（无表，不准备）

221 不建表、不灌数（DATA 第 4 节）。唯一前提是第 7 项政策子图 `E-E7-POLICY-M1-L02` 已完成（注册表可查）与前端只消费不新开资源。**禁止**为让弦线图「有画面」把演示页弦线矩阵/路径灌进三张缺项表（ARCH §5.3 明确不做）。

### DP-05 环境前置汇总

| 环境 | 要求 | 现状（2026-11-04 00:xx） |
|---|---|---|
| K8s dev 后端 | `gkxlumen-display` / `gkxlumen-element` 已发布且含 trend/partition 端点 | **待确认发布版本**（代码在 `lumen-svc-platform` dev 已有；219/220 链路就绪） |
| 222 后端 | element template 端点 + display shells `kind=模板选用` 分发 | **缺失（GAP-01，见第 4 节）** |
| 网关 | `/display/v1/**` StripPrefix=1 路由正常 | 沿 READ 联调基线 |
| 前端 | `lumen-ui-science-pc` 政策分析评价页可视化区四叶接线（`POL-L2-DS11-VIZ-WIRING-L01`） | **in_progress（阻塞界面验证阶段）** |
| 观测 | 能按 `X-Trace-Id` 检索日志 | 沿 READ 联调基线 |

---

## 2. 关键路径验证用例

> 每条含编号/前置/步骤/预期/实际结果。接口联调用例以 K8s dev 为准；本轮先完成**连库数据验证**（DP 章已执行，结果见各 DP 行），接口与界面用例按 GAP-01 / WIRING 进度标注 PENDING。**期望未发生必红**：凡预期「不返回 501 / 不建任务 / 不调 Python / 不返回写死 mock / 不清空其他块」的负向断言，一旦发生即为红。

### TC-01a 219 趋势正常态（时间维整条序列）

| 列 | 内容 |
|---|---|
| 编号 | TC-01a |
| 前置 | DP-01 就绪；display/element 已发布 |
| 步骤 | 1. 记录/注入 `X-Trace-Id`；2. `POST /display/v1/policy/evaluation/jobs`，body `{"kind":"趋势","switch":["时间"],"metric":["科技政策连续出台数"]}`；3. 校验响应 |
| 预期 | HTTP 200；`data.records` **恰好 6 行**（2021–2026），`pointValue` 依次 48/62/75/83/79/91 与 DP-01 验证 SQL 3 一致；`2026` 行 `is_key_point=1`、`2025` 行 `is_fluctuation=1`；每行 `isMock=1`；无 501、无任务 ID（同步返回非 Job）、无写死序列 |
| 实际结果 | PENDING（待 K8s dev 联调；数据面已验证见 DP-01） |

### TC-01b 219 趋势空态（双路径）

| 列 | 内容 |
|---|---|
| 编号 | TC-01b |
| 前置 | 同上 |
| 步骤 | 依次 POST 三种 body：① `{"kind":"趋势","switch":["时间"],"metric":["不存在的指标"]}`；② `{"kind":"趋势","switch":[],"metric":["研发投入强度"]}`（缺维）；③ `{"kind":"趋势","switch":["行业"],"metric":["研发投入强度"]}`（闭集外维） |
| 预期 | 三次均 HTTP 200、`data.records` 为**空列表**——不得返回 501、不得补默认曲线、不得返回演示页 2020–2026 写死序列；③ 中 `行业` 是 220 对象类，混用必须落空（闭集互斥） |
| 实际结果 | PENDING |

### TC-02a 220 分区正常态（行业全量 + 投向过滤）

| 列 | 内容 |
|---|---|
| 编号 | TC-02a |
| 前置 | DP-02 就绪 |
| 步骤 | 1. POST jobs body `{"kind":"分区","subject":"行业"}`；2. 再 POST `{"kind":"分区","subject":"行业","allocation":"财政资金"}`；3. 校验两次响应行集 |
| 预期 | 第 1 次 HTTP 200、`records` **10 行**（DP-02 验证 SQL 2 行业组），柱状与热力由前端用同一批行渲染（后端不建第三套数据）；第 2 次 `records` **5 行**且与 DP-02 验证 SQL 3 逐行一致；每行 `isMock=1`；无 501 |
| 实际结果 | PENDING |

### TC-02b 220 分区空态（对象闭集外 + 投向对不上）

| 列 | 内容 |
|---|---|
| 编号 | TC-02b |
| 前置 | 同上 |
| 步骤 | 依次 POST：① `{"kind":"分区","subject":"时间"}`（219 的维，闭集外对象）；② `{"kind":"分区","subject":"行业","allocation":"装备制造"}`（投向对不上）；③ `{"kind":"分区"}`（缺对象） |
| 预期 | 三次均 HTTP 200、`records` 空列表——不补默认对象、不返回演示城市名单矩阵、不返回 501；① 证明 219 的 `switch` 值与 220 的 `subject` 值闭集互斥 |
| 实际结果 | PENDING |

### TC-03a 222 模板选用正常态

| 列 | 内容 |
|---|---|
| 编号 | TC-03a |
| 前置 | DP-03 就绪；**GAP-01 修复后**（display shells `kind=模板选用` 分发 + element template 端点上线） |
| 步骤 | `GET /display/v1/policy/evaluation/shells?kind=模板选用&template=区域政策效果季度对比` |
| 预期 | HTTP 200；`records` 2 行（季度/地区/柱状 + 季度/地区/热力），与 DP-03 验证 SQL 3 一致；每行 `isMock=1`；无 501、无写死模板清单 |
| 实际结果 | **阻塞（GAP-01）**：当前 display `PolicyEvaluationService.shells` 对 `kind=模板选用` 落入兜底空列表（分发未写该支），element 亦无 template 端点。**按「期望未发生必红」判红**——数据已在库但接口读不出，222 交付主路径断 |

### TC-03b 222 空态（模板对不上 + 导出条件不齐）

| 列 | 内容 |
|---|---|
| 编号 | TC-03b |
| 前置 | 同 TC-03a |
| 步骤 | ① `GET shells?kind=模板选用&template=不存在的模板`；② `template=科技政策月度动态报告` 且 `format=PDF` 但缺 `period`/`dimension`/`chart_type` |
| 预期 | ① `records` 空，模板区空；② 不生成文件、响应不含内嵌写死文件；模板对得上时仍只返回选用行。两路径均 HTTP 200、无 501 |
| 实际结果 | 阻塞（GAP-01，同上；当前实现「恒空」，①② 与正常态不可区分，无法证明空态来自条件对不上） |

### TC-04 221 空态诚实（无资源、无报错）

| 列 | 内容 |
|---|---|
| 编号 | TC-04 |
| 前置 | 前端 WIRING 完成；第 7 项子图挂接可为空 |
| 步骤 | 1. 打开政策分析评价页可视化区「多维结构关联图」块；2. 打开浏览器 DevTools Network，停留该块并切换图种（弦线图/关系网）；3. 尝试路径查看 |
| 预期 | **验证点是空态诚实而非报错**：子图挂接空时弦线图、关系网两图均呈空态提示（无画面、无假矩阵），路径查看不可用或空；Network 面板**不出现** `/display/v1/policy/**` 新增资源（221 不设资源）、**不出现** `/topic/v1/policy/graph`、**不出现** `/v1/policy/**`、无 `policyData.js` 常量注入；页面无 JS 报错、无 501 |
| 实际结果 | PENDING（界面验证阶段执行；mock 态可先在本地复核空态文案） |

### TC-05 kind 与 sub_type 同传短路（回归）

| 列 | 内容 |
|---|---|
| 编号 | TC-05 |
| 前置 | display/element 在线 |
| 步骤 | POST jobs body `{"kind":"趋势","sub_type":"policy_focus_ads","switch":["时间"],"metric":["研发投入强度"]}` |
| 预期 | HTTP 200、`records` 空——不建任务（topic-async 无新任务）、不读趋势表（trace 上无 element trend span）、不转发异步（无 `/topic/v1/analysis/tasks` 调用）；API 分册第 2 节规则的负向验证 |
| 实际结果 | PENDING |

### TC-06 不越层回归（同步链无 Python / 无异步）

| 列 | 内容 |
|---|---|
| 编号 | TC-06 |
| 前置 | TC-01a、TC-02a 各留一条 `X-Trace-Id` |
| 步骤 | 在观测平台按 traceId 检索两条链路 |
| 预期 | span 链为 网关 → display → element → MySQL；**不出现** `gkxlumen-topic-async-service` span、**不出现** Python `/internal/policy/jobs/execute` span、无 SSE、无并发锁占用——219/220 同步读链的「期望未发生」断言；同页已返回的 counts / shells 内容不受这两次请求影响 |
| 实际结果 | PENDING |

### 用例汇总

| 编号 | 一句话 | 状态 |
|---|---|---|
| TC-01a/01b | 219 趋势正常/空态 | 数据面已验（DP-01）；接口 PENDING |
| TC-02a/02b | 220 分区正常/空态 | 数据面已验（DP-02）；接口 PENDING |
| TC-03a/03b | 222 模板正常/空态 | **判红（GAP-01 后端链路缺失）** |
| TC-04 | 221 空态诚实 | PENDING（界面阶段） |
| TC-05 | kind+sub_type 短路 | PENDING |
| TC-06 | 同步链不越层 | PENDING |

---

## 3. 界面操作过程（lumen-ui-science-pc · 政策分析评价页可视化区）

> **本阶段 PENDING**：依赖 `POL-L2-DS11-VIZ-WIRING-L01`（2026-11-04 00:13 仍 in_progress，前端工作区有未提交改动）。接线完成后按本节步骤执行；截图存 `agent-handoffs/科技政策跟踪-POL/screenshots/POL-L2-DS11-VIZ-TEST-L01/`，每张须含浏览器地址栏与页面状态，正常态+空态双路径成对截取。

| 步骤 | 操作 | 预期 | 截图文件名 |
|---|---|---|---|
| S1 | 打开 K8s dev 前端，进入「科技政策跟踪 → 政策分析评价」可视化区 | 四块齐备：多维指标趋势图、分区/群体对比分析图、多维结构关联图、报告模板定制与批量导出；无 JS 报错 | `01-open-viz-tab.png` |
| S2 | 219 正常态：切换维选「时间」，勾选指标「科技政策连续出台数」 | 曲线 6 点（2021–2026）；2026 重点标注、2025 波动标注；🧪 MockBadge 在位 | `02-trend-normal.png` |
| S3 | 219 空态：勾选闭集外或对不上的组合 | 图区空态提示，不出现写死曲线/五维雷达 | `03-trend-empty.png` |
| S4 | 220 正常态：对象选「行业」，图种不选（柱+热力同出） | 柱状与热力用同一批 10 行渲染 | `04-partition-normal.png` |
| S5 | 220 空态：投入选「装备制造」 | 该图空态提示，不出现演示城市名单 | `05-partition-empty.png` |
| S6 | 221 空态：查看弦线图/关系网两图种 | 两图空态诚实（无假矩阵/假路径），Network 无新增 policy 资源请求 | `06-structure-empty.png` |
| S7 | 222 正常态：模板选「区域政策效果季度对比」 | 返回选用行（季度/地区/柱状+热力）；不选格式只看行不生成文件 | `07-template-normal.png` |
| S8 | 222 空态：导出条件不齐（缺周期/维度/图表类型）点导出 | 不生成文件、空态提示；操作日志无假记录 | `08-template-empty.png` |

执行时同步核对：每张图旁 🧪 MockBadge（D4=mock）与统计数字旁 ⓘ 入口在位；`USE_MOCK=false` 时全部走 `/display/v1/policy/**` 真接口（Network 校验），无 `@/mock` 或 demo fixture 填数。

---

## 4. 缺陷与风险记录

| 编号 | 级别 | 描述 | 影响 | 建议 |
|---|---|---|---|---|
| GAP-01 | **P1（阻塞 222 全部用例与四叶合绿）** | 222 读取链路后端两侧缺失：`gkxlumen-display` `PolicyEvaluationService.shells` 对 `kind=模板选用` 落兜底空列表（分发只写了互动意见/方案报告两支，注释直言「模板选用无表返回空」）；`gkxlumen-element` `PolicyGapfillController` 无 template 端点（测试还断言 `assertFalse(shell.contains("template"))`）。而 `gapfill_policy_eval_template` 已灌 10 行（TEMPLATE 单已落库） | `GET shells?kind=模板选用` 恒空，数据在库读不出：222 交付主路径断，TC-03a 判红；且空态与「条件对不上」不可区分，TC-03b 无法证明 | 派 api-agent 补两处：element `GET /v1/element/policy/evaluation/template`（读 `gapfill_policy_eval_template`，按 `template_name` 拣行）+ display shells 分发补 `模板选用` 支；同步修 element 测试断言。修复后复测 TC-03a/03b |
| 风险 R1 | 提示 | DP 章列名 as-built（`switch_dim`/`dim_value`/`point_value`）与 DATA 分册列名（`axis_kind`/`axis_position`/`compare_value`）不一致；`is_key_point`/`is_fluctuation` 为 DATA 未列的加列 | 契约冻结（`BE-POL-CONTRACT-01`）时若按 DATA 原文定列名将再度错位（参照 READ 单 BUG-01 教训） | 契约冻结时以 as-built 为准或先修 DATA 分册 |
| 风险 R2 | 提示 | K8s dev 已发布的 display/element 版本是否含 trend/partition 端点未核实 | TC-01/02 联调可能因版本滞后假红 | 联调前核对 dev 镜像版本含 `lumen-svc-platform` dev 分支对应 commit |

## 5. 结论

- 数据面：三张 gapfill 表行集与追溯列已按 DP-01/02/03 连库只读验证通过（trend 44、partition 41、template 10/6 模板，分组与拣行样本逐条一致）——第一阶段数据准备判定 **绿**。
- 接口面：219/220 后端链路代码就绪（display `syncKind` + element 两端点），联调用例待 K8s dev 执行；222 判 **红（GAP-01）**：后端读链缺失，需 api-agent 补 element template 端点与 display 分发支后复测。
- 界面面：PENDING，阻塞于 `POL-L2-DS11-VIZ-WIRING-L01`；操作步骤与截图清单已固化（第 3 节），接线合入后即可执行。
- 四叶当前判定：219 数据绿/接口待联调；220 数据绿/接口待联调；221 待界面阶段（验证空态诚实）；222 **红（GAP-01）**。
