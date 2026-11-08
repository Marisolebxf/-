# 机构招引培育（SVC-REC）· LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-REC-合规演示用例.md`
- 系统：科技专题服务系统 · 产业服务链分析 · 机构招引培育。不打开页面。
- 监管人：`human:徐滕强`
- 日期：2026-11-07
- 常驻验收单建议 ID：`SVC-REC-DEMO-ACCEPT-LOOP`（**只写进本计划，不建单**；等人说「按 LOOP 跑」才按 §2 建单）

- 状态行（2026-11-08 10:5x，R20261108 第 3 轮，qa-agent@human:徐滕强）：**样本满足=是（7/7 行全对上，零缺口）**；停止原因=通过。读锚点任务 SVC-20261107-032 / -042 / -015 / -007（复用成功任务，0 次签发、0 次 Create）。第 2 轮 401 根因=网关前缀误用（URL 多拼 `/enterprise` 段致路由 401 假阴性），token 一直有效；网关锚定 `https://edu.itic-sci.com/tts/svcz/api/ + /topicAsync/topic/v1/** | /svc/topic/v1/**`（as-built `lumen-ui-topic/src/api/enterprise/paths.ts`）。INB1303 读面 `data_source=empty:chain_unmatched[demo_ads]` + empty=true + items=[] + HTTP 200 本轮正式留档（`lumen-topic-py 49640a4` 线上生效实证，第 1 轮 QUERY 缺口闭合）。未建未签子任务。库侧仍受阻（10.50 内网不可达，database-mcp ETIMEDOUT、跳板 SSH 2 次封顶停止），以接口面 detail/result 快照与 rec-list 读面互证替代，与第 1 轮库审基线无漂移；下轮内网恢复可补一次对账（非阻塞）。验收单=**ready**（不签 done，待 human:徐滕强 按 §6.5.7 步 6 确认收尾）。

## 0. 域数据面备忘（跑 LOOP 前必读）

1. **Job 结果快照不落库**（M2 受阻项④实查证实：`analysis_task.result_data` 全 NULL）：`svc:analysis:attract|cultivate` 的结果随任务记录存于 `gkxlumenx_topic_enterprise.analysis_task.target_params.result_payload`。验收读数=先读任务态，再读该 JSON 字段（`status` / `summary.count` / `summary.top_score` / `attract[]` / `cultivate[]` / `own_gaps` / `yellow_gaps` / `narration.status`）。
2. **受理成功 ≠ 成功**：`POST tasks` 返回 `taskId` 只是受理；须轮询 `GET tasks/{id}` 至 `status=success` 且 `page_mode_hint=process_succeeded_wait_view`，再 `GET tasks/{id}/result` 对照快照字段，成功终态才算对上。
3. **两榜表行滚动**：ADS 榜表（`svc_attraction_recommend` / `svc_cultivation_recommend`）批次会滚动（例：培育榜 2026-11-07 17:01 由 3 行 proxy 切 `svc_rec_cultivate_wanghui_20261107_170132` 50 行）。用例中的「届期值」仅作对照起点；轮内一律**先重签发再读当期**，按新批次行核数。字段结构（weights/own_gaps/yellow_gaps/维度分/advice 结构）不变。
4. **培育权重双口径并存**（本次登记）：页面/Job 快照 `25/30/25/20`（svc_proxy 同款）vs 培育榜 11-07 新批次 `wanghui_v1_signed20261022` 等权 25×4。轮内核「页面 Tag=25/30/25/20」与「榜行 weights 字段=当期批次真值」，两者各自成立即不算缺口；等权正式化属 Q-SVCCHAIN-05 甲方决策，**不为本 LOOP 派修**。
5. 服务地址 `http://10.50.69.111:30892`，网关前缀 `/topicAsync/topic/v1/**`；结果读面经网关 `POST /svc/topic/v1/service/rec-list`（网关剥 `/svc` 后为 Java `/topic/v1/service/rec-list`）。请求头 `systemCode: topic`。

## 1. 覆盖对照与通过线

用例覆盖表 7 行（4 主行 + 3 行为补充行）轮内全部对照；通过线：

| 锚点 | 通过线 |
|---|---|
| 7.6.1 受理 | Create 返回 `taskId`（`SVC-YYYYMMDD-NNN` 形态）+ `status ∈ {queued,running}`；过程页五阶段推进；同条件重复发起返回同一 `taskId` |
| 7.6.2 全量切片 | 轮内重签发后：`result_payload.status="ads_ready"`、`summary.count=50`、`summary.top_score` = 当期榜表 `MAX(attraction_index)`（今日批次 90.0000）；rec-list `items` 数与 `summary.count` 一致、首行 rank_no=1 |
| 7.6.2 生物医药切片 | `selected_industry="INB2503"`、`summary.count` = 当期榜表 ∩ `chain_code=INB2503` 去重机构数（今日表值 7）；`narration.status` ∈ {ok, skipped}（ok 时文案须含「演示口径」「不作对外招商承诺」） |
| 7.6.2 集成电路切片（诚实空） | `status="empty"`、`summary.count=0`、`attract=[]`；rec-list `empty=true`、`items=[]`、HTTP 200；页面空态文案点名产业；**不回退全量、不造数**。缺口分类见 §4（Q-SVC-011） |
| 7.7.1 受理与门控 | fp=`svc|cultivate|{path}`；筛选类型或环节=0 项时按钮禁用+拦截文案；权重 Tag=25/30/25/20 |
| 7.7.2 名单与建议 | 重签发后 `summary.count=50`、`summary.top_score` = 当期 `MAX(cultivation_index)`（今日批次 95.3634）；首行 rank 1、行含维度分与建议结构（`advice_gen` ∈ {llm, rule}，建议文本引用该行维度值）；维度空值行省略该维（不写 0 分）；入篮后 `svc_compare_basket_item` 行数 +1（guest 篮现 6 行） |
| I2-12 | 切条件 0 次 Create；同条件重复发起复用同 `taskId` 且不增记录行；当天已成功直开结果；结果页工具条有「重新分析」 |

库侧基线（今日实查，轮内核「结构不变 + 行数/批次数对上」）：招引榜 50 行（`svcmodels_20261107_155402`）、培育榜 50 行（`svc_rec_cultivate_wanghui_20261107_170132`）、挂链 INB1309 186,964 / INB2503 5,267 / INB1303+1306+1333 = 0、REC Job success 91（attract 56 / cultivate 35）。

## 2. 验收单（等人说「按 LOOP 跑」后才建）

| 项 | 值 |
|---|---|
| ID | `SVC-REC-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent` |
| 状态 | 建为 `ready`，不认领（claim_type=coordinator_dispatch，锁 24h） |
| 依赖 | 本用例（SVC-REC-合规演示用例）已齐；不依赖任何 `done` 单 |
| 报告 | `agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-REC-DEMO-ACCEPT-LOOP.md`（**只追加**） |

一轮写完退回 `ready`。不签 `done`。

## 3. 后端调用

token 文件：`~/.gkx/topic-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer`、`systemCode: topic`。与展示系统的 token 文件分开。不打印、不入库。

验收轮**新签发**两枚 REC Job（与只用既有结果锚点的政策 LOOP 不同：本域 Job 快照不落独立表、榜表批次滚动，既有锚点快照数值会过时；重签发是本域核对口径）。不传 `force=true`（同条件复用既有任务即满足 I2-12 复用核对）；「重新分析」语义的强制重跑**不在验收轮**使用。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `GET /topicAsync/topic/v1/analysis/tasks/running?user_id=guest` | 只验 token 与网关可达 |
| 签发① | `POST /topicAsync/topic/v1/analysis/tasks`（attract，industry 为空，fp `svc\|attract\|*`） | 全量招引切片 |
| 签发② | 同上（attract，`industry="INB2503"`，fp `svc\|attract\|CL-SEI-02.INB2503`） | 生物医药切片 |
| 签发③ | 同上（attract，`industry="INB1303"`，fp `svc\|attract\|CL-SEI-01.INB1303`） | 集成电路诚实空切片 |
| 签发④ | 同上（cultivate，fp `svc\|cultivate\|*`） | 培育全量切片 |
| 轮询 | `GET /topicAsync/topic/v1/analysis/tasks/{task_id}?user_id=guest`（≥1.5s 间隔） | 至 `status=success`（或 failed） |
| 结果 | `GET /topicAsync/topic/v1/analysis/tasks/{task_id}/result?user_id=guest` | 读 `result_payload` 对照 §1 通过线 |
| 读面 | `POST /svc/topic/v1/service/rec-list`（kind=attract/cultivate，limit=50，chain_codes 按切片） | 与快照 `summary` 对照（items 数、首行 rank/score） |
| 库 | 只读 `demo_gkxlumenx_ads.svc_attraction_recommend` / `svc_cultivation_recommend` / `demo_gkxlumenx_dwd.enterprise_industry_chain` / `gkxlumenx_topic_enterprise.analysis_task` / `svc_compare_basket_item` | 核对 §1 库侧基线与批次一致性 |

探测 401 / 424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，通知 `human:徐滕强`，不建子任务，不再开一轮。探测 404：停止，原因写「接口映射不存在」，不改成补数。

库只 `SELECT`。不写 ODS / DWD / ADS / 供应方库 / `gapfill_` / 新 ADS；不改 `analysis_task`；不删对比篮行。

## 4. 缺口怎么派

只比较 §1 那几项。每轮最多 **3** 张子任务（`SVC-REC-DEMO-FIX-R{YYYYMMDD}-*`）。不改前端，不改锚点匹配。

| 类 | 何时派 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | 榜表行数/批次与基线对不上（如招引榜≠50、培育榜被清空）、挂链计数漂移（INB2503 去重机构数≠切片 cnt 基线）、INB1303/1306/1333 挂链仍 0 且甲方已拍补数、对比篮表不可读 | `data-agent` | `SVC-REC-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | rec-list 与快照 `summary` 不一致（items 数 ≠ count、首行 rank ≠ 1、chain_codes 切片不生效/回退全量）、`GET result` 读不到快照、受理链路（Create/轮询/result）契约错 | `algorithm-agent`（lumen-topic-py 查询面归算法域） | `SVC-REC-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 快照结构缺失/字段错（缺 weights/own_gaps/yellow_gaps、维度分错位）、评分与当期榜表行不一致（top_score ≠ 表 MAX）、培育建议结构与行维度不对应、narration 伪 OK | `algorithm-agent` | `SVC-REC-DEMO-FIX-R{YYYYMMDD}-ALGO` |
| ENV | 网关不可达、K8s dev 服务未发布、Python 服务 5xx、`systemCode`/token 熔断（探测即败） | `devops-agent`（或停轮上报） | `SVC-REC-DEMO-FIX-R{YYYYMMDD}-ENV` |

不派单的情形：
- **Q-SVC-011（INB1303/1306/1333 挂链 0 行）**：诚实空是期望本身。除非甲方/供方已拍板补数并落库，否则不派 DATA 单；空态若消失或回退全量才是 QUERY 缺口。
- **Q-SVCCHAIN-05（模型正式口径未定）**：演示态声明是期望本身。权重双口径并存（页面 25/30/25/20 vs 榜批次 25×4）不派修；等权正式化走甲方决策链。
- 培育 `growth_stage` 全 NULL、`priority_level` 全 high：批次事实，不派修。
- LLM narration 为 `skipped`（empty 切片）：预期行为，不派修。

同一缺口键连续两轮仍在：停止建单，交 `human:徐滕强`。子任务 handoff 落盘后才把验收单拨回 `ready`。下一轮**重新签发** REC Job 读当期快照（本域口径，不沿用上一轮 task_id）；验收轮自己不改库、不重算。

## 5. 确认后的第一轮顺序

1. 按 §2 建 `SVC-REC-DEMO-ACCEPT-LOOP` 为 `ready`；认领，`supervised_by=human:徐滕强`。
2. 读本机 topic token；探测 running 接口。探测失败按 §3 停。
3. 依次签发 4 枚 Job（§3 表），轮询至终态；每枚读 `result_payload` + 调 rec-list 对照；库侧 `SELECT` 基线核对。
4. 按 §1 通过线逐项判定；有缺口才按 §4 建子任务（≤3 张），验收当轮不改库、不重算。
5. 写报告一节（只追加）。§1 全部对上才算本轮通过，验收单留在 `ready`；等待人说下一轮或签收。

- ~~状态行（2026-11-08 09:5x，R20261108 第二轮…）~~（第 2 轮结果已并入上方第 3 轮状态行；blocked 前提经 coordinator 复核证伪，详见 handoff 第 3 轮节「根因澄清」）
