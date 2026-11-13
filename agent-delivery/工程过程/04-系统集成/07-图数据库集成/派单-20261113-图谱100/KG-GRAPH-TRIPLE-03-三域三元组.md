# KG-GRAPH-TRIPLE-03 · 三域三元组推进记录

- 执行负责人：宋飞扬；派单监管：徐滕强。
- 任务范围：104/105、110/111、114/115，截止 2026-11-25。
- 当前阶段：步 1 设计完成（待复核）；正式 MCP 建单/认领未成功，Python/Java/UI 未开工。
- 基准：gkx-orchestration dev `cc3cb25d033a8a0746a4ecd0a2cbaff80e784dae`；不重开已签收 T03/T08。

## 已完成的独立工作

精读 SVC pipeline-to-nebula 全文，区分“同构契约”与“复制旧写图行为”。核对三个业务仓访问和当前架构入口；三域只读消费，本阶段零图/源库写入。

1. 三份 storage 文档：TECH / PERSON / RESEARCH 的 `etl/pipeline-to-nebula.md`（共 21 op）。
2. 同目录 `KG-GRAPH-TRIPLE-03-op-contracts.json`：机器可读 op 与三层路径映射。
3. `KG-GRAPH-TRIPLE-03-op清单.md`：21 行，实测状态均为 not_run。
4. `KG-GRAPH-TRIPLE-03-task-create-request.json`：保留真实 COVER-01 依赖；不能把不存在的任务当 ready。
5. `KG-GRAPH-TRIPLE-03-联调清单.md`：离线/在线验收步骤与未决项。

## 开工核对

MCP `task-get KG-GRAPH-TRIPLE-03` 与 `task-get KG-GRAPH-COVER-01` 均返回 Task not found。派单写 ready 只是文档字段，不能声称已认领。按 `task-claiming-guide.md` §6 先认领后业务编码；目前只交设计准备。未手改登记册，未代建其他人的任务。

轻量探测 `10.50.75.136:9669` 返回拒绝连接；没有运行 sum/count 压测，没有重启进程。扩容/重启由 PLAT-09 环境方处理。恢复后先精确VID小样本，合作榜离线完整索引不得在HTTP内扫全图。

## 需要留意的范围

- 21 op 是本稿的接口分解，不是宣称派单原文已经列出了这21个名字；待实现按清单逐项保留。
- 技术点关联端点用 tech_person/tech_institution 等实际 Tag/VID，不与 person/research 主数据混用。
- cooperate 必须按端点 Tag 分组；无向遍历正反都读、结果去重，不新增反向边。
- research全量包含company主数据，详情保留类型，M02/M04不混入company端点。
- 机构关联补齐前 partial 明示；无证据的 props 字段为 null。
- 合作度=唯一邻居数，不能拿合作强度或截断样本排名代替全域榜。

## 后续闸门

协调员补建上游及本任务并落实依赖状态后，经 MCP 正式认领。步1契约齐→Python成对接口→Java精确ops路由→UI四态，按顺序。图库停服期间不伪造任何网关成功回执。完整联调通过前不将整单标 integration/done。

前端仓本次 AGENTS 明确要求人工确认才能 push；当前仅完成文档，尚未触发该发布步骤。
