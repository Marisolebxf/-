# SVC-ORG-DEMO-ACCEPT-LOOP · 服务机构分析演示样本反复验收（handoff，只追加）

- 任务：`SVC-ORG-DEMO-ACCEPT-LOOP`（Epic E7-产业服务链分析；agent=qa-agent；监管人=human:徐滕强；强度=ponytail full）
- 规程：`agent-delivery/产品实现规程.md` §6.5（一轮四步 §6.5.4，报告 §6.5.5）
- 计划：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ORG-LOOP计划.md`

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md`（6 行可演，0 覆盖不到）
- 库：只读。database-mcp 组 `gkx-mysql` → 连接 `demo-gkxlumenx-ods`，跨库限定名查 `demo_gkxlumenx_dwd.svc_org_circle` / `demo_gkxlumenx_ads.svc_org_card` / `demo_gkxlumenx_ads.svc_metric_series` / `demo_gkxlumenx_ads.svc_tech_power_score` / `gkxlumenx_topic_enterprise.svc_compare_basket_item` / `gkxlumenx_topic_enterprise.analysis_task`。零写操作。
- 样本满足：**否**
- 停止：继续（缺口待派 + 待补签发；无 token/映射/重复缺口停止）

### 步① 探测

- token 文件存在且非空（值不入档）；`POST /tts/svcz/api/enterprise/topic/v1/recommend`（头 `authorization: Bearer <token>` + `systemcode: topic`，body `{"count":1}`）→ **HTTP 200，code=0**，返回 1 条机构卡（广州集趣…）。轮首探测通过，进样本对照。

### 步② 批次前置与库侧真值

| 核对项 | 实查 | 与用例/计划 | 结论 |
|---|---|---|---|
| `svc_org_circle` 批次 | 单批次 `svc-fseed-20261020`，43,296 行 | 同 | ✅ 无重灌 |
| `svc_tech_power_score` 批次 | `calc_batch_id=svcmodels_20261107_155402`（列名实况；计划写作 etl_batch_id 为同义笔误），300 行，`model_version=svc_proxy_v1.3` | 同 | ✅ 无重灌 |
| 机构集合 5 org_id（双奉/君智容/星诚优威/航羿/中科为） | 5/5 命中 `svc_org_card`，名称与类型候选（INNOV×3、IP×2）一致 | 同 | ✅ |
| 趋势 2022–2026（`svc_metric_series.M_SVC_ORG_NEW_COUNT`，列 `period`/`value`） | 2779 / 2330 / 1885 / 1251 / 36 | 同值同序 | ✅ |
| 评分两行（君智容/星诚优威） | score 均 40.0000，`SVC_INNOV_TECH_POWER`，weights 五维各 20，dimension_scores 0/1（cases=1、rdInvestment=1、其余 0），ext.name 同名 | 分值/权重/形态一致 | ✅ |
| **对比篮 `svc_compare_basket_item`（guest）** | **实查仅 2 行：id=62 东莞东劲新能源（0071aadf…）、id=63 东莞双奉（007050fc…）；用例期望 6 行（含君智容 id=60、星诚优威 id=61）缺 4 行** | **不一致** | ❌ DATA 缺口 |

### 步③ 逐行对照（接口值 vs 库值 vs 期望；本轮默认不签发，只读复用既有 success 快照）

| 需规行 | 复用快照（HTTP） | 期望（用例） | 接口实测（result 载荷，经 target_params.result_payload） | 库值 | 判定 |
|---|---|---|---|---|---|
| 7.1.1 覆盖分析 | `SVC-20261107-019`（coverage，200/success，同型 2 家） | 3 家 matrix：双奉 82 / 君智容 91 / 星诚优威 66；`org_count=3`、`avg_breadth≈2.24` | matrix 4 格：君智容 INB1309/INB170102 均 **91**、星诚优威均 **66**；summary `avg_breadth=2.24`；`yellow_gaps=[Q-SVCCHAIN-02, GAP-SVC-MATRIX-SRC]`、`pending_client_confirm=1` | 3 家 org_id 全在 `svc_org_card`；**双奉 82 无任何库侧/快照承载面**（含 007050fc… 的 success coverage 任务 5 条全是 2026-10-21/22 旧波，`matrix=[]`） | 部分：君智容 91 / 星诚 66 / breadth ✅；**双奉 82 无证据 → 待补签发（监管人说「签发」后按用例请求列 POST 一次）** |
| 7.1.2 矩阵图 | 同 019（读同 taskId，200） | 四象限 3 点：广度 2 × 深度 82/91/66；切回热力图同源 | 同一份 matrix：每家广度=2 格、深度 91/66 实值；`avg_depth=480.56`（快照原始累计口径，用例已注明两口径差） | 同上 | 部分：随 7.1.1（缺第三家点）；已载值 ✅ |
| 7.2.1 新增趋势 | `SVC-20261106-008`（trend，200/success，INB1309 行） | 9 曲线 × 17 点；2010=1,501；2022–2026=2779/2330/1885/1251/36；window_hint 全量截窗 | series 9 曲线×17 点；「全部」「人工智能」两曲线 2010=1501、近窗五点 **逐点全等**；`window_hint` 逐字一致；`yellow_gaps=[GAP-SVC-TREND-FIELD, Q060]` | ADS `svc_metric_series` 五点同值同序 | ✅ 对上（接口+库双证） |
| 7.2.2 市场热度 | 同 06-008（读同 taskId） | INB1309 1 星低迷三行原文（1057.3 / 2938.7 / -64.0%）；INB2503 1 星低迷 -67.5%；INB1204 insufficient 不评级 | heat 段 INB1309 / INB2503 / INB1204 三行 **逐字一致**（含「序列仅 2 个年度点，不足 3 点不评级」、stars=null） | 同快照 yellow_gaps + pending=1 | ✅ 对上（演示规则判定口径，🧪） |
| 7.3.1 技术力评估 | `SVC-20261107-020`（tech_power，200/success，同 2 家） | INNOV 两行 score 恒 40.0 **同分并列 rank_no 1/2**；批次 v1.3；weights 五维等权 20 | 两行 score=40.0 ✅、dimension_scores 0/1 ✅、weights 等权 20 ✅；**但 rank_no=26 / 50（全池 300 行全局序，非选定集合展示序 1/2）**；**payload 自报 `model_version=svc_proxy_v1.2`（库批次行是 v1.3）** | `svc_tech_power_score` 两行 40.0、weights 等权、批次 `svcmodels_20261107_155402` + `svc_proxy_v1.3` | 部分：分值/权重 ✅；**rank 展示序 + 版本自报 ❌ → ALGO** |
| 7.3.2 雷达对比 | 同 020（读同 taskId） | 五维 0/1 归一后重合（演示态）；同分稳定序 1/2 | dimension_scores 0/1 两行一致（归一后重合实情成立）；并列序同 7.3.1 问题（26/50） | 库 dimension_scores 两行一致 | 部分：多边形重合 ✅；**并列序随 ALGO 单** |

输入前置（非需规行）：7.1.1/7.3.1 的「从对比篮直勾 id 57/60/61」在当前库不可复现（见步②对比篮缺口）。

### 步④ 缺口分类与子任务

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `gkxlumenx_topic_enterprise.svc_compare_basket_item.user_id=guest.{004671cd…,007d0adc…}` | DATA | 篮内仅 2 行（id=62 东劲、id=63 双奉），君智容/星诚优威及另 2 行缺失 | 用例查库节 6 行（含 id=60/61） | 按 2026-11-05 操作语义补回缺行（source=对比篮新增；行 id 允许漂移） | `SVC-ORG-DEMO-FIX-R20261107-DATA`（ready） |
| `analysis_task.svc:analysis:org_coverage.{三家组合}` | QUERY | 含三家 org_ids 的 success 任务 0 条；双奉 82 深度无承载面 | 7.1.1 三家 matrix（82/91/66） | 监管人明确说「签发」后按用例请求列 POST 一次，新快照核 depths（依赖 DATA 单先修篮） | `SVC-ORG-DEMO-FIX-R20261107-QUERY`（ready；本轮未 POST） |
| `analysis_task.SVC-20261107-020.result_payload.tech_power.rows.rank_no / model_version` | ALGO | 同分两行 rank_no=26/50（全池序）；payload 自报 v1.2 | 选定集合内并列 rank_no 1/2；自报版本与批次 v1.3 一致 | 快照装配层按选定集合重排展示序；model_version 自报取源表批次值。**不改库内 40/20 恒分**（Q-SVCCHAIN-01+Q060 演示态声明） | `SVC-ORG-DEMO-FIX-R20261107-ALGO`（ready） |

- 去重：`task-query` 无同缺口键既有未完成单（现存 DEMO-FIX 单均为政策模块），3 张均新建。
- 按计划 §6：子任务只核对/登记/报告；本轮只建单升 ready、不认领、不改库、不改代码、未签发新分析任务。

### 结论与下一轮建议

- 6 行：2 行对上（7.2.1 / 7.2.2）、4 行部分（7.1.1 / 7.1.2 / 7.3.1 / 7.3.2），样本未满足，验收单留 `ready`。
- 顺序建议：先派 DATA 修篮 → 监管人「签发」后 QUERY 单建三机构快照 → ALGO 单修展示序与版本自报 → 重开第 2 轮验收。
- 成本：本轮远低于 $10 告警线（cost_warn=green）。
- 脱敏：本轮无口令、token 入档；token 文件只读未改。

## 签发 2026-11-07

- 任务：`SVC-ORG-DEMO-ACCEPT-LOOP`（监管人 human:徐滕强 已说「签发」，规程 §6.5.7 步 3；api-agent 执行；ponytail full）
- 前置：MCP `task-query` 确认 QUERY 单 ready（本次签发=其待签发项）、ALGO 单 pending_test（修复 commit 已在线）；database MCP 只读查重后签发，零写库、零改代码；token 只读文件、未打印未入档；临时响应快照已清理。
- 查重（`gkxlumenx_topic_enterprise.analysis_task`，只读；fp 位于 `target_params.input_payload.analysis_fp`）：
  - 三机构 fp `svc|field||007050fc…,004671cd…,007d0adc…`：**0 命中**，签发合法；
  - 两机构 fp `svc|capability||004671cd…,007d0adc…`：已有 success `SVC-20261107-020`（08:14，ALGO 修复**前**引擎产物）与 `SVC-20261106-011`（11-06）。跨日/跨版本重建有既有先例（POL 域 POLICY-20261107-021；SVC 11-06→11-07 同 fp 两笔均 success），按派单要求两笔均 POST 新签发，不带 force，均 `reused=false`。
- 端点：首网关一次通，未启用备选 `https://edu.itic-sci.com/tts/lumen/api`。签发 `POST https://edu.itic-sci.com/tts/svcz/api/topicAsync/topic/v1/analysis/tasks`（头 `authorization: Bearer <token>` + `systemcode: topic`；POL 域同构路径先例）；取证 `GET …/tasks/{taskId}/result?user_id=guest`。请求体=用例 7.1.1 / 7.3.1 请求列逐字段。
- 签发与取证结果：

| # | 任务 | analysisType / fp | 签发 | 终态 | 关键取证 |
|---|---|---|---|---|---|
| 1 | `SVC-20261107-048` | `svc:analysis:org_coverage` / `svc\|field\|\|007050fc…,004671cd…,007d0adc…`（三机构） | 22:05:45，HTTP 200 `code=0`、`reused=false`、`status=running` | `success`（约 38s，库侧 cost_seconds=8） | `matrix` 6 格：**东莞双奉 depth=82**（INB1309 与 INB170102 各一格，此前无证据，首证到手）、君智容 91×2、星诚优威 66×2；summary `org_count=3`、`matrix_fill_rate=1.0`、`avg_depth=480.49`（快照原始累计口径）、`avg_breadth=2.24`、`field_count=2`；`yellow_gaps=[Q-SVCCHAIN-02, GAP-SVC-MATRIX-SRC]`、`pending_client_confirm=1`；载荷自报 `model_version=svc_proxy_v1.2`（coverage 面常量，属 QUERY 单范围外，未处理） |
| 2 | `SVC-20261107-049` | `svc:analysis:tech_power` / `svc\|capability\|\|004671cd…,007d0adc…`（两机构） | 22:05:45，HTTP 200 `code=0`、`reused=false`、`status=running` | `success`（约 38s，库侧 cost_seconds=20） | 顶层 `model_version=svc_proxy_v1.3` ✅（源表批次 `svcmodels_20261107_155402`）；`tech_power.rows` 300 行（全池），`tech` 列表 300 行同序；行级 `model_version` 均 v1.3、score 40.0/20.0 与库一致；**两家顶层 rank_no=126（君智容）/150（星诚优威），全池全局序而非选定集合内 1/2**（详见 ALGO 验证结论）；`weights` 五维各 20、`yellow_gaps=[Q060]`、`pending_client_confirm=1` |

- **ALGO 修复验证结论**：修复 commit `0084025`（lumen-algo-py，2026-11-07 21:41，意图=选定集合 score 降序稳定排序、顶层 rank_no 从 1 递增 + 版本自报取源表批次行）**一半生效一半未生效**：
  - ✅ 版本自报：顶层与 `engine_meta.model_version` 均 `svc_proxy_v1.3`（旧快照 020 自报 v1.2，修复前后对照成立）；`tech_power.rows` 行级 300 行全部 v1.3、批次 ID 与库一致。
  - ❌ 展示序：两家 rank_no=126/150（全池 300 行全局序）。根因定位（代码实读）：`engine.fetch_models` tech 读面无 org_ids 形参，仅按 `industry`（chain_ids）切片——本任务 industry 为空 → `sorted(rows)` 排序对象=全池 300 行，顶层 rank_no=1..300；`leaf_tech_power` 装配只做 `limit` 截断（default 300），`params.org_ids` 两处消费（`leaf_org_coverage` / graph 物化）均不经 tech 分支。commit 注释「同分并列 1/2」仅在 chain_ids 过滤后行集≤2 的场景成立。**期望「选定集合内 1/2」未达成**，需求未闭环，如实记录不改期望；若监管人裁定继续修，建议给 fetch_models tech 读面加 `org_ids` 形参（切片后再排序，最小 diff）。
- 网关与状态：签发走前端域名网关 `edu.itic-sci.com/tts/svcz/api/topicAsync/**`，与 LOOP 计划接口地址真源一致；两笔均未遇 404/超时，无需备选前缀。
- cost：actual_tokens ≈ 80,000；model_used = `glm-5.3-Flash`；actual_cost ≈ $0.4；cost_warn = `green`。
- 脱敏：token 全程未打印、未入档；本节无口令入档。

## 运行 2026-11-08（第 2 轮）

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md`（6 行可演，0 覆盖不到）
- 库：只读。database-mcp 连接 `demo-gkxlumenx-ods` 本轮 2 次 SELECT 连续失败（EADDRNOTAVAIL → 连接关闭态），按派单规约记受阻、不探活；本轮对照改以 HTTP 任务载荷取证（`GET …/tasks/{id}/result` + `target_params.result_payload`）；批次前置沿用第 1 轮库侧实查结论，本轮载荷内 `calc_batch_id=svcmodels_20261107_155402` 同值旁证无重灌。零写操作。
- 样本满足：**否**
- 停止：**重复缺口**（rank_no 全池序，同缺口键、同类、同预期连续两轮不收敛 → 按规程 §6.5.4 停止建单，交监管人 human:徐滕强）

### 步① 探测

- token 文件存在且非空（值不入档）；`POST /tts/svcz/api/enterprise/topic/v1/recommend`（头 `authorization: Bearer <token>` + `systemcode: topic`，body `{"count":1}`）→ **HTTP 200，code=0**。轮首探测通过。

### 步② 重签发 tech_power（核心；监管人 2026-11-08 口令「签发」）

- 请求体 = 用例 7.3.1 请求列逐字段（君智容 `004671cd…` + 星诚优威 `007d0adc…`，`cap_w="25,25,20,20,10"`），**未带 force**。
- `POST /topicAsync/topic/v1/analysis/tasks` → HTTP 200、`reused=false`（跨日同 fp 新建，先例成立）、任务 **`SVC-20261108-001`**（id=2203），09:48:47 创建、09:48:57 success（`total_cost_ms=8243`，4 节点走满）。
- 取证（result 端点仅任务壳：`resultData=null`、`resultAssetId=res-SVC-20261108-001`，值经 `target_params.result_payload`）：

| 取证项 | 期望 | 实测 | 判定 |
|---|---|---|---|
| model_version（顶层 + `engine_meta` + 300 行行级） | `svc_proxy_v1.3` | `svc_proxy_v1.3`（第 1 轮快照 020 自报 v1.2 的病根已根治） | ✅ |
| calc_batch_id | `svcmodels_20261107_155402` | 同值 | ✅ |
| score / dimension_scores / weights | 40.0 / 0-1 / 五维等权 20 | 同 | ✅ |
| **rank_no（君智容 / 星诚优威）** | **选定集合内并列 1 / 2** | **126 / 150**——`tech_power.rows` 300 行全池序、`tech` 列表 300 行同序，行集未按 org_ids 切片 | ❌ |
| yellow_gaps / pending_client_confirm | `["Q060"]` / 1 | 同 | ✅ |

- **ALGO 修复（lumen-algo-py `c084e7c`）线上验证结论：未生效**。deploy:api + deploy:worker success（09:10）早于任务创建（09:48:47），时序上引擎不应在跑旧版；但返回行集仍为全池 300 行（若 org_ids 切片生效应为 2 行或顶层 rank 1/2）。旁证字段：`engine=svcmodels`、`assembly_version=svcan-assembly-v1.0`、`data_plane=demo`、`data_source=demo_ads`、`trace_id=3ae36bae16fdd23b4eb70ea2a48a515d`。两条待监管人裁定排查方向（不在 LOOP 范围，不自行排查）：① 该演示网关在线引擎是否确由 `lumen-algo-py` 本次部署承载（`data_plane=demo` 指向 demo 侧装配，存在部署目标 ≠ 调用目标的可能，注意镜像缓存类陷阱）；② `fetch_models` tech 读面 org_ids 切片代码路径是否真被执行（trace_id 可追）。

### 步③ 其余行复验（只读）

| 需规行 | 依据 | 实测 | 判定 |
|---|---|---|---|
| 7.1.1 覆盖分析 | `SVC-20261107-048`（HTTP result，success） | matrix 6 格：双奉 82×2 / 君智容 91×2 / 星诚优威 66×2；summary `org_count=3`、`matrix_fill_rate=1.0`、`avg_breadth=2.24`、`avg_depth=480.49` | ✅ 全等 |
| 7.1.2 矩阵图 | 同 048 读 | 同一份 matrix：三家广度各 2、深度 82/91/66（`avg_depth` 快照原始累计口径，用例已注明两口径差） | ✅ |
| 7.2.1 新增趋势 | `SVC-20261106-008`（HTTP result） | 「全部」曲线 2010=1,501、2022–2026 = 2,779/2,330/1,885/1,251/36 **逐点全等** | ✅ |
| 7.2.2 市场热度 | 同 008 读 | INB1309 1 星低迷三行依据逐字（1057.3 / 2938.7 / -64.0%）；INB2503 1 星低迷（-67.5%）；insufficient 不评级行在；`yellow_gaps=[GAP-SVC-TREND-FIELD, Q060]` | ✅ |
| 7.3.1 技术力评估 | `SVC-20261108-001`（本轮重签发） | 分值/版本/批次/权重 ✅；**rank_no 126/150 ❌** | ❌ ALGO（见步②） |
| 7.3.2 雷达对比 | 同 001 读 | `dimension_scores` 0/1 两行一致、归一后重合 ✅；并列序随 7.3.1 ❌ | ❌ 随 ALGO |
| 对比篮 guest 4 行（id 62/63/64/65） | 库 SELECT | **受阻**：database MCP 连续 2 次失败（`EADDRNOTAVAIL` / 连接关闭态），按派单规约记受阻不探活；篮行修复落库已由第 1 轮 data-agent handoff 证实，待下一轮库侧复核 | 记受阻，不计缺口 |

### 步④ 缺口分类与子任务

| 缺口键 | 类 | 现况 | 预期 | 挂到任务 |
|---|---|---|---|---|
| `analysis_task.svc:analysis:tech_power.result_payload.tech_power.rows.rank_no` | ALGO | 连续两轮同现（SVC-20261107-049 与 SVC-20261108-001 均 126/150 全池序）；`c084e7c` 部署 success 但线上行为未变 | 选定集合内并列 rank_no 1/2 | **两轮停（§6.5.4 / §6.5.7 步 9）：不建第三张单，交 human:徐滕强 决定** |

- 本轮 **0 张**新建（两轮停铁律；同缺口键去重后不可再建 `SVC-ORG-DEMO-FIX-R20261108-ALGO`）。DATA / QUERY 两缺口键本轮已消除：048 success 补齐三机构深度证据、篮行修复落库（库侧复核因 DB 受阻顺延）。
- 监管人裁定选项参考：a) 排查部署目标与调用目标是否同一服务（旁证 `data_plane=demo`）；b) 按 trace_id 追切片路径是否执行；c) 若修代码，另开带标签新单（不受两轮停约束的存量单复用）。

### 结论

- 6 行：**4 行对上**（7.1.1 / 7.1.2 / 7.2.1 / 7.2.2）、**2 行仍差同一 ALGO 缺口**（7.3.1 / 7.3.2 rank 展示序）；样本未满足，验收单回 `ready`（不签 done）。
- 停止原因 = 重复缺口：等 human:徐滕强 裁定后再开第 3 轮。
- 下一轮开工动作：先重试 database MCP（1 次即止）补对比篮 4 行库侧复核；再验 7.3.1（若裁定后有新修复）。
- cost：actual_tokens ≈ 70,000；model_used = `glm-5.3-Flash`；actual_cost ≈ $0.35；cost_warn = `green`。
- 脱敏：token 全程未打印、未入档；本节无口令入档；临时响应文件（/tmp/svc_*.json）已清理。
