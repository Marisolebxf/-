# TS-L2-DS02-PATH · 展示关键路径和关键节点 · LOOP 执行编排计划

- 状态：2026-11-07 QUERY 挂图谱 QUERY（`pending_test`）。DATA=`pending_test`：`path_priority` 已灌；正文/类型/年份人拍板扩列 → 挂 `TS-L2-DS02-SCHEMA-EXPAND-L01`。待 display 分数叠加核 pathPriority。验收单 ready。
- 流程：`agent-delivery/产品实现规程.md` §6.5（用例 §6.4）
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-PATH-合规演示用例.md`
- 索引：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/科学技术全景-索引.md`
- 系统：科技信息展示系统 · 科学技术全景（`/trend/tech-panorama`），序号 28–33。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

## 1. 要证明什么

用例里数据情况为 `可演` 的行，经展示网关返回与期望输出一致：不选点时 `nodes` 带 `role`、`strength`、`centrality`（样本 `tcn_000f21ac…` 41.292）；选「神经性厌食症治疗的临床视角」后 `keyPathOptions` 两条（`tep_8392b7f8d44d14cae932645cd242f5bd` 三步、`tep_6cddc27aa4e88a50756093fd6d76ef86` 两步），步序与端点名称对得上。

通过线：

- 探测 HTTP 200。
- 29：不选点就能核，网关 `nodes[].centrality` 与分数表一致。
- 28 节点序列、30 步序与端点、32、33：须带 `selectedNodeId` 后出现 `keyPathOptions`。`TS-L2-DS02-SEL-FIX-L01` 未修前，网关预计返回 `[]`，归 QUERY，挂该单，不算数据缺口。32、33 不发请求，只核它们依赖的第 28 行返回。
- 用例期望写的是「当日取自 Python 读图与库」。网关值与之不一致时，先按 §6.5 分类，不改用例期望。

以下保持现状，不算本 LOOP 的失败，也不为此建子任务：

- `pathPriority`、`centrality` 来自 D18 mock 表，D4=mock，不改绿。三条分数都不按 ALGO 处理。
- 路径只带与选中点直接相连的步（PATH-ARCH 遗留 2），「整条还是局部」待会签，不在 LOOP 里改。
- 不改前端。前端单 `TS-L2-DS02-FE-ENTITY-FIX-L01` 在 LOOP 外。

## 2. 验收单

人说「按 LOOP 跑」之后再建，本文件不建。

| 项 | 值 |
|---|---|
| ID | `TS-L2-DS02-PATH-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent`；过滤拣不中、字段名对不上再加 `api-agent` |
| 状态 | 建为 `ready`，不认领。token 失效或映射不存在为 `blocked` |
| 报告 | `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-PATH-DEMO-ACCEPT-LOOP.md`（只追加「运行 YYYY-MM-DD」） |

样本满足、本轮子任务都已签收或本轮没有子任务、状态行已回写后，验收单改为 `done`，操作人 `human:淮政玮`。未满足留 `ready`。不替代 `TS-L2-DS02-TEST-L01`，不把它标完成。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\display-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer <token>`、`systemCode: display`、`Content-Type: application/json`。不打印、不入库、不进 handoff。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `POST https://edu.itic-sci.com/tid/api/display/v1/situation/panorama/graph`，body `{}` | 只验 token 与映射。200 才往下 |
| 样本 | 同一地址，按用例覆盖表逐行 POST（不选点一次；`selectedNodeId=tcn_000f21ac06aceb9cdd0575e82d0d85fc` 一次） | 核可演行 |
| 库（图） | Nebula `demo_gkx_chain`，经 Python 只读接口：跳板机 `kubectl exec` 进 `zhipu-tts` 的 `lumen-platform-algo-py` api pod，`POST http://127.0.0.1:8000/internal/tech-graph/read`，body `{"space":"demo_gkx_chain","technology_node_id":"…"}` | 网关空时判断 `tech_path_step` 在不在 |
| 库（分数） | MySQL `demo_gkxlumenx_ads.ads_technology_panorama_score`，只读 `SELECT score_kind, COUNT(*) ... GROUP BY score_kind` 与按编号 `SELECT` | 核 `centrality` 行、`path_priority` 行 |

探测返回 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，note 写「token 失效，已通知 human:淮政玮」，不建子任务，不再开一轮，不自动登录。探测 404：同样停止，原因写「接口映射不存在」。

SSH 只读取证守 `ssh-executor-authorized.mdc`：不 `echo` 探活；同一意图 SSH 调用最多 2 次；命令加 `timeout`；跳板机 kubeconfig 副本用完即删。库只 `SELECT`，不 `--apply`，不写 ODS、DWD、ADS、`gapfill_`。

## 4. 缺口怎么派

只比较用例里 `可演` 的行；`覆盖不到` 的三行（28 重要性、30 正文、31）按 DATA 进入分类。每轮最多三张，先 `task-query` 去重，不改前端。

| 类 | 何时 | 执行人 | 先挂已有单 | 否则新建 |
|---|---|---|---|---|
| DATA | 路径步不在库；`path_priority` 0 行；缺路径类型字段、年份、技术意义正文 | `data-agent` | 路径步与路径属性挂 `SYSINT-TECHGRAPH-02-L02`；`path_priority` 按 `TS-L2-DS02-SCORE-L01` 的灌数脚本建新单重跑（图上已有 `tech_path_step`，`path_id` 可对齐） | `TS-L2-DS02-PATH-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | 库里在，网关 `keyPathOptions` 空：选中点字段名不一致；`pathPriority` 有行却没叠加 | `api-agent` | 选中点挂 `TS-L2-DS02-SEL-FIX-L01` | `TS-L2-DS02-PATH-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 预期不出现。中心度、优先级都是 mock，D4 不改绿 | `algorithm-agent` | — | 真出现时 `TS-L2-DS02-PATH-DEMO-FIX-R{YYYYMMDD}-ALGO` |
| ENV | 探测 401、424、404 | — | 不建单，通知后停止 | — |

缺口键写法（两轮之间保持一致）：`nebula.demo_gkx_chain.tech_path_step.{path_id}.{step_order}`、`nebula.demo_gkx_chain.tech_path_step.{path_id}.{属性}`、`ads_technology_panorama_score.{path_id}.path_priority`、`ads_technology_panorama_score.{technology_node_id}.centrality`、`display.graph.selectedNodeId->techPointId`。

同一缺口键、同一类、同一预期连续两轮仍在：停止建单，交给 `human:淮政玮`。子任务 handoff 落盘并签收后，才开下一轮。note 不写「联调通过」「会签通过」「集成测试通过」。
