# 服务链生态域（SVC-ECO）· LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ECO-合规演示用例.md`
- 系统：科技专题服务系统。不打开页面。
- 监管人：`human:徐滕强`
- 日期：2026-11-07

- 状态：**2026-11-07 第 1 轮已跑**（验收单 `SVC-ECO-DEMO-ACCEPT-LOOP`）：样本满足——6/6 行对上（7.4.1/7.4.2/7.5.1/7.5.2/7.8.1/7.8.2，均带演示态声明），停止=通过。探测 200；复用任务 `SVC-20261105-014` / `SVC-20261107-002` / `SVC-20261107-022`（图谱面另打 POST `/api/svc/topic/v1/service/eco-graph` 对照），未新签发任务；本轮无缺口、无子任务。库侧五表只读核对通过（中试熟化 0/blank 恒定、43,296/42,740、密度 0.000046、TOP5 首名深圳市创新投资集团 253、深圳 14,080/77/0.833）。验收单拨回 `ready`，不签 done。运行节见 `agent-handoffs/E7-产业服务链分析/SVC-ECO-DEMO-ACCEPT-LOOP.md`。

覆盖不到的行在按 LOOP 跑时才分类。本文 6 行均带演示态声明，跑时按声明字段（`runtime_flag` / `pending_client_confirm` / `yellow_gaps` / `own_gaps`）在位与否判齐。不派数据单，不派算法单，不打探测。

## 1. 常驻验收单（等人说「按 LOOP 跑」后按 §6.5.2 新建；本计划只登记建议 ID，不建单）

| 项 | 值 |
|---|---|
| 建议 ID | `SVC-ECO-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`api-agent`、`algorithm-agent` |
| 状态 | 建为 `ready`，不认领 |
| 报告 | `agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-ECO-DEMO-ACCEPT-LOOP.md`（只追加，不覆盖既有章节） |

一轮写完退回 `ready`。不签 `done`。

## 2. 范围与通过线

覆盖表 6 行（7.4.1–7.8.2）逐一对照。每轮核对的行与期望值以《SVC-ECO-合规演示用例》为准，本节列每轮必核的最小通过线：

| 行 | 核对锚点 | 通过线 |
|---|---|---|
| 7.4.1 | `SVC-20261105-014`（或新任务号）`result_payload.gap[]` | 六环节齐；中试熟化 `org_count_in_stage=0` 且 `avg_depth=NULL`、`runtime_flag=blank`（不得补 0）；演示口径声明在位（`q061_pending_client=1`） |
| 7.4.2 | 同上截面 | 「服务空白」判定行 = 0 家环节；「演示规则判定」可读声明在响应载荷/页面声明段在位；不合成薄弱/瓶颈伪警示 |
| 7.5.1 | `SVC-20261107-002` 或 POST `/api/svc/topic/v1/service/eco-graph` | `status=ads_ready`；`space=demo_gkx_chain`；节点 43,296 / 边 42,740；`yellow_gaps` 含 Q060/Q062/Q063/Q-SVC-010/Q-SVCCHAIN-03 |
| 7.5.2 | 同上截面 | 密度 0.000046（`density_formula=2E/(N*(N-1))`）；TOP5 首名「深圳市创新投资集团有限公司」度 253；影响力诚实缺失声明在位、无伪分 |
| 7.8.1 | `SVC-20261107-022`（或新任务号）`sz_compare` + `shenzhen` | 框架名=产业服务链统一评价框架；深圳 规模 14,080 / 技术分 77 / 密度 0.000046 / 完整度 0.833；`own_gaps` 含「口径待 Q-SVC-010」声明 |
| 7.8.2 | 同上截面 | 五城市 cities 齐（广州 19,600 / 全国平均 11,228 / 北京 3 / 上海 null）；梯队 `T1 · 第一梯队（1/8）`、gauge 77；narration 数值与 sz_compare 同源 |

以下保持现状，不算失败，不为此建子任务：

- 上海机构规模 null（ads.svc_org_card 无上海在库行，呈现无数据不造 0）。
- 环节统计为全库词表代理口径，不随产业领域真实切片（GAP-SVC-CHAIN-SEGMENT）；图谱为全网口径非产业切片。
- 图谱关系归并 `participates` 单边型；影响力评分诚实缺失（GAP-SVC-GRAPH-INFLUENCE）。
- 短析任务引用的是 2026-11-05 批次快照（29,120/201/0·0），现库批次（svcmodels_20261107_155402）为 28,842/457/22/0·0——两批次中试熟化 0 恒定，批次间非零值差异按当时实查核对，不追平历史值。
- demo-ui-topic 沙箱另一套确定性演示基准（五城市 1,240/460/1,580/1,350/890）不作为本 LOOP 对照物。

## 3. 库表清单（引用 M2 `SVC-数据调研-20261107.md`；只读 SELECT）

连接：database-mcp 分组 `gkx-mysql` 入口 `demo-gkxlumenx-ods`，跨库限定名。M2 实查 `gkxlumenx-dwd-public-rw-mock` 认证被拒（受阻-已绕行），沿用同分组入口。

| 库.表 | 用途 |
|---|---|
| `demo_gkxlumenx_ads.svc_chain_gap` | 7.4.1/7.4.2 六环节行值（中试熟化 0/blank 恒定核） |
| `demo_gkxlumenx_ads.svc_relation_chain` | 7.5.2 密度 0.000046 / 中心性 TOP5（全网行 `org_id` NULL） |
| `demo_gkxlumenx_dwd.svc_org_graph_hang` | 7.5.1 挂链 43,296 行、单空间 `demo_gkx_chain`（正式库同名表 0 行） |
| `demo_gkxlumenx_ads.svc_org_card` | 7.8 深圳 14,080 / 广州 19,600 / 全国平均 11,228 / 北京 3、上海 0 行 |
| `gkxlumenx_topic_enterprise.analysis_task` | 三类任务（`svc:analysis:{shortboard,graph,shenzhen}`）状态与 `target_params.result_payload` |

库只 `SELECT`。不写 ODS、DWD、ADS、供应方库、`gapfill_`、新 ADS 表。不执行 `--apply`。

## 4. 纯后端调用与 token 约定

token 文件：`~/.gkx/topic-loop-token`（macOS/Linux）或 `%USERPROFILE%\.gkx\topic-loop-token`（Windows），一行 access_token，仓库外。请求头 `Authorization: Bearer <token>`、`systemCode: topic`。token 不进 git、不进 handoff、不打印。不自动重新登录。

验收不新签发任务（复用已签发结果），不带 `force=true`。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/SVC-20261107-022/result?user_id=guest` | 只验 token 和深圳演示任务结果还在不在 |
| 7.4 | `GET …/analysis/tasks/SVC-20261105-014/result?user_id=guest` | 读 `gap[]` 六环节行 |
| 7.5 | `POST http://10.50.69.111:30892/api/svc/topic/v1/service/eco-graph`，body `{"filter":"orgs_and_actors"}` | 图谱面节点/边/统计（只读 `write=false`） |
| 7.8 | 同探测（SVC-20261107-022） | 读 `sz_compare` / `tier` / `shenzhen` / `narration` |
| 库 | §3 五张表 SELECT | 核行值 |

探测返回 401、424，或正文是「访问令牌不存在」「用户凭证已过期」「token expired」：停止本轮，验收单 `blocked`，note 只写「token 失效，已通知 human:徐滕强」，不建子任务，不再开下一轮。探测返回 404：停止并通知，原因写「接口映射不存在」或「演示任务结果不可读」，不算补数缺口。

## 5. 一轮四步

1. **探测**：带本机 token 打 §4 探测笔。
2. **只读库 + 调接口**：§3 五表 SELECT；§4 四笔接口按行核对期望值。
3. **对照**：逐行比 §2 通过线（可演行）。`覆盖不到` 的行不拿来判通过；用例没写期望的行不另造预期。
4. **缺口分类**：对不上的行按类建子任务，先去重。

通过：接口 HTTP 成功，返回与该行期望输出一致，且该行约定的过滤能拣到该结果。演示态声明的缺失（如 `q061_pending_client`/`pending_client_confirm` 不再为 1、yellow_gaps 缺项）按行对照声明字段在位性判定。

## 6. 缺口分类（DATA / QUERY / ALGO / ENV）

| 类 | 看到的情况 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | `svc_chain_gap` 中试熟化被填成非 0/非 blank；`svc_org_graph_hang` 行数变动；`svc_org_card` 城市切片值漂移；任务结果载荷缺行 | `data-agent` | `SVC-ECO-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | 行在，`/result`、`/eco-graph` 过滤或等值拣不中（如 user_id 归属、industry 参数丢行） | `api-agent` | `SVC-ECO-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 行在且键一致，密度/TOP5/梯队/narration 值对不上期望，或演示判定面板输出口径外档位 | `algorithm-agent` | `SVC-ECO-DEMO-FIX-R{YYYYMMDD}-ALGO` |
| ENV | 探测 401 / 424 / 404 | 不建单，通知后停止 | — |

- **每轮最多 3 张子任务**；一条缺口只归一类；先查 `task-query` 去重，不重复建单。
- **同一缺口连续两轮仍在**：停止建单，交给人（`human:徐滕强`）。
- 本域既有缺口引用不新造编号：Q061 / Q062 / Q063 / Q060 / Q-SVC-010 / Q-SVCCHAIN-02 / 03 / 04 / 08 / Q-SVC-011、GAP-SVC-CHAIN-SEGMENT / GAP-SVC-CHAIN-BOTTLENECK / GAP-SVC-GRAPH-INFLUENCE / GAP-SVC-SZ-CHAIN-COMPLETENESS。跑轮中确认的新缺口登记进 `SVCCHAIN-缺口登记总表.md`（M4 归并），子任务只引用不另造。
- 子任务 handoff 落盘后才把验收单拨回 `ready`。只有数据或算法子任务明确要求重算时才另签发任务，签发号写入该子任务 handoff，验收单改读新号；验收轮自己不签发。

## 7. 状态行

覆盖已齐，未执行。等人说「按 LOOP 跑」。
