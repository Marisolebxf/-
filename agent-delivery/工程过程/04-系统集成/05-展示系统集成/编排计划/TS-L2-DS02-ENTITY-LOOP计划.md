# TS-L2-DS02-ENTITY · 展示技术点关联实体 · LOOP 执行编排计划

- 状态：2026-11-07 用例覆盖已齐，未执行，等人说「按 LOOP 跑」。可演 5 行，覆盖不到 4 行，设计无资源 1 行（26）。可演行全部待 `TS-L2-DS02-SEL-FIX-L01`。
- 流程：`agent-delivery/产品实现规程.md` §6.5（用例 §6.4）
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-ENTITY-合规演示用例.md`
- 索引：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/科学技术全景-索引.md`
- 系统：科技信息展示系统 · 科学技术全景（`/trend/tech-panorama`），序号 22–27。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

## 1. 要证明什么

用例里数据情况为 `可演` 的行，带 `selectedNodeId` 经展示网关返回 `listRecords`，与期望输出一致：选「神经性厌食症治疗的临床视角」得四类实体（当日 Python 值 61 行：论文 13、专利 20、机构 20、人 8）；换「膳食脂肪摄入与神经健康」得 29 行；样本论文 `W2093980670` 的 `influence` 为 16.4。

通过线：

- 探测 HTTP 200。
- 22 选点后 Top5、23、24 基本属性、25 按类型、27 按影响力名称类型：网关返回的 `listRecords` 条数、类型分布、样本编号、`nodeIds`、`influence` 与用例一致。
- `TS-L2-DS02-SEL-FIX-L01` 未修前，网关预计返回 `listRecords=[]`。这归 QUERY，挂该单，不算数据缺口，不派补数。
- 用例期望写的是「当日取自 Python 读图与库」。网关值与之不一致时，先按 §6.5 分类，不改用例期望。

以下保持现状，不算本 LOOP 的失败，也不为此建子任务：

- 26 的 501（设计无资源）。
- `influence` 来自 D18 mock 表，D4=mock，不改绿。
- 页面实体区不读 `listRecords`（ENTITY-API §8 第 2 条）。这是前端单 `TS-L2-DS02-FE-ENTITY-FIX-L01`，在 LOOP 外；LOOP 不改前端，也不以页面显示判通过。

## 2. 验收单

人说「按 LOOP 跑」之后再建，本文件不建。

| 项 | 值 |
|---|---|
| ID | `TS-L2-DS02-ENTITY-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent`；过滤拣不中、字段名对不上再加 `api-agent` |
| 状态 | 建为 `ready`，不认领。token 失效或映射不存在为 `blocked` |
| 报告 | `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ENTITY-DEMO-ACCEPT-LOOP.md`（只追加「运行 YYYY-MM-DD」） |

样本满足、本轮子任务都已签收或本轮没有子任务、状态行已回写后，验收单改为 `done`，操作人 `human:淮政玮`。未满足留 `ready`。不替代 `TS-L2-DS02-TEST-L01`，不把它标完成。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\display-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer <token>`、`systemCode: display`、`Content-Type: application/json`。不打印、不入库、不进 handoff。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `POST https://edu.itic-sci.com/tid/api/display/v1/situation/panorama/graph`，body `{}` | 只验 token 与映射。200 才往下 |
| 样本 | 同一地址，按用例覆盖表逐行 POST（`selectedNodeId` 为 `tcn_000f21ac06aceb9cdd0575e82d0d85fc`、`tcn_008a8b3f1dd54fcac52ebcb2ca81e160`） | 核可演行 |
| 501 复核 | `POST .../display/v1/situation/panorama/entity-relations`，body `{}` | 只确认仍是 501 |
| 库（图） | Nebula `demo_gkx_chain`，经 Python 只读接口：跳板机 `kubectl exec` 进 `zhipu-tts` 的 `lumen-platform-algo-py` api pod，`POST http://127.0.0.1:8000/internal/tech-graph/read`，body `{"space":"demo_gkx_chain","technology_node_id":"…"}` | 网关空时判断实体在不在 |
| 库（分数） | MySQL `demo_gkxlumenx_ads.ads_technology_panorama_score`，只读 `SELECT ... WHERE subject_id IN (...)`，口令只用 pod 环境变量 | 核 `influence` 行 |

探测返回 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，note 写「token 失效，已通知 human:淮政玮」，不建子任务，不再开一轮，不自动登录。探测 404：同样停止，原因写「接口映射不存在」。

SSH 只读取证守 `ssh-executor-authorized.mdc`：不 `echo` 探活；同一意图 SSH 调用最多 2 次；命令加 `timeout`；跳板机 kubeconfig 副本用完即删。库只 `SELECT`，不 `--apply`，不写 ODS、DWD、ADS、`gapfill_`。

## 4. 缺口怎么派

只比较用例里 `可演` 的行；`覆盖不到` 的四行（22 初始化与关联强度、24 描述时间线统计、25 按时间、27 按强度时间）按 DATA 进入分类。每轮最多三张，先 `task-query` 去重，不改前端。

| 类 | 何时 | 执行人 | 先挂已有单 | 否则新建 |
|---|---|---|---|---|
| DATA | 实体不在库；缺关联强度（`tech_has_*` 边无属性）、实体中文名、年份、时间线 | `data-agent` | 关联实体边与边属性挂 `SYSINT-TECHGRAPH-02-L02`；`influence` 行缺失按 `TS-L2-DS02-SCORE-L01` 的灌数脚本建新单重跑 | `TS-L2-DS02-ENTITY-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | 库里在，网关 `listRecords` 空或拣不中：选中点字段名不一致 | `api-agent` | 选中点挂 `TS-L2-DS02-SEL-FIX-L01` | `TS-L2-DS02-ENTITY-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 预期不出现。影响力是 mock，D4 不改绿；本二级没有算出来的值 | `algorithm-agent` | — | 真出现时 `TS-L2-DS02-ENTITY-DEMO-FIX-R{YYYYMMDD}-ALGO` |
| ENV | 探测 401、424、404 | — | 不建单，通知后停止 | — |

缺口键写法（两轮之间保持一致）：`nebula.demo_gkx_chain.tech_has_{type}.{technology_node_id}->{entity_id}.{属性}`、`nebula.demo_gkx_chain.{entity_tag}.{entity_id}.name_zh`、`ads_technology_panorama_score.{subject_id}.influence`、`display.graph.selectedNodeId->techPointId`。

同一缺口键、同一类、同一预期连续两轮仍在：停止建单，交给 `human:淮政玮`。子任务 handoff 落盘并签收后，才开下一轮。note 不写「联调通过」「会签通过」「集成测试通过」。
