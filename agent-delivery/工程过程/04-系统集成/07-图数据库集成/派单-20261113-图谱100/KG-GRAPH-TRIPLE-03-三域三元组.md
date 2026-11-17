# KG-GRAPH-TRIPLE-03 · 三域三元组推进记录

- 执行负责人：宋飞扬；派单监管：徐滕强。
- 任务范围：104/105、110/111、114/115，截止 2026-11-25。
- 当前阶段（2026-11-17）：MCP已认领并in_progress；PERSON/RESEARCH两域12操作已本地实现。TECH 9操作待COVER-01；线上发布、完整图索引和正式网关联调未完成。
- 基准：gkx-orchestration dev `cc3cb25d033a8a0746a4ecd0a2cbaff80e784dae`；不重开已签收 T03/T08。

## 步1设计准备（历史记录）

精读 SVC pipeline-to-nebula 全文，区分“同构契约”与“复制旧写图行为”。核对三个业务仓访问和当前架构入口；三域只读消费，本阶段零图/源库写入。

1. 三份 storage 文档：TECH / PERSON / RESEARCH 的 `etl/pipeline-to-nebula.md`（共 21 op）。
2. 同目录 `KG-GRAPH-TRIPLE-03-op-contracts.json`：机器可读 op 与三层路径映射。
3. `KG-GRAPH-TRIPLE-03-op清单.md`：21 行，实测状态均为 not_run。
4. `KG-GRAPH-TRIPLE-03-task-create-request.json`：保留真实 COVER-01 依赖；不能把不存在的任务当 ready。
5. `KG-GRAPH-TRIPLE-03-联调清单.md`：离线/在线验收步骤与未决项。

## 11-13开工核对（历史记录，已被11-17更新取代）

MCP `task-get KG-GRAPH-TRIPLE-03` 与 `task-get KG-GRAPH-COVER-01` 均返回 Task not found。派单写 ready 只是文档字段，不能声称已认领。按 `task-claiming-guide.md` §6 先认领后业务编码；目前只交设计准备。未手改登记册，未代建其他人的任务。

轻量探测 `10.50.75.136:9669` 返回拒绝连接；没有运行 sum/count 压测，没有重启进程。扩容/重启由 PLAT-09 环境方处理。恢复后先精确VID小样本，合作榜离线完整索引不得在HTTP内扫全图。

## 需要留意的范围

- 21 op 是本稿的接口分解，不是宣称派单原文已经列出了这21个名字；待实现按清单逐项保留。
- 技术点关联端点用 tech_person/tech_institution 等实际 Tag/VID，不与 person/research 主数据混用。
- cooperate 必须按端点 Tag 分组；无向遍历正反都读、结果去重，不新增反向边。
- research全量包含company主数据，详情保留类型，M02/M04不混入company端点。
- 机构关联补齐前 partial 明示；无证据的 props 字段为 null。
- 合作度=唯一邻居数，不能拿合作强度或截断样本排名代替全域榜。

## 原后续闸门（历史记录）

协调员补建上游及本任务并落实依赖状态后，经 MCP 正式认领。步1契约齐→Python成对接口→Java精确ops路由→UI四态，按顺序。图库停服期间不伪造任何网关成功回执。完整联调通过前不将整单标 integration/done。

前端仓本次 AGENTS 明确要求人工确认才能 push；当前仅完成文档，尚未触发该发布步骤。

## 2026-11-17 · 两域实施更新

依据唐绍祖11-16答复和会签，宋飞扬授权先做科研机构114/115、人才110/111。通过仓内task-mcp-cli（stdio MCP应急通道）认领后置in_progress，保留徐滕强监管及COVER-01依赖；未代领其他任务。主仓基准bb82c1d8。

- 两份storage契约及机器契约已更新口径，TECH操作仍保留未实现状态。
- Python：实体详情、邻域、子图、关联对象共8实时操作，以及检索/浏览4索引消费操作；全部/v1与/internal成对。缺完整索引返回503，不把源表快照冒充当前图。
- Java：gkxlumen-innov新增明确12操作白名单、Feign纯透传，保留Python HTTP状态；只准备网关person/research精确ops路由模板，不抢其他域或M10。
- 前端：两个认证路由、实体/关系/关联/浏览入口；真实边权口径，四态与实际调用记录，条件变化清旧结果，不自动查询。
- 小样本：当前图库认证、DESCRIBE通过，person/research为name+props字符串；T04覆盖后的节点props与T03源导出不同，禁止复用旧源快照冒充实时图库。精确VID、正反合作读取已实测；无全图聚合，无图/源库写入，无服务重启。

证据：`KG-GRAPH-TRIPLE-03-two-domain-python-live.json`（本地Python→真实图库，含空态及超邻域阈值503）；两域本地验证与发布清单见同目录`KG-GRAPH-TRIPLE-03-两域本地实施与待发布.md`。这不是正式Java网关回执。

当前真实限制：空间无Tag索引；名称检索与全域合作度排序等待完整、验证过的图库快照索引。已实现独立离线索引构建器，但本轮未启动全图导出/构建，不使用早期源表/样本替代完整图。高连接度实体的邻域排序超过500候选时503，子图按200点/500边/20次查询上限明确截断。

整单维持in_progress，TECH、完整索引、正式部署及网关联调补齐后再申请integration；本阶段handoff不作为整单完成/AV-0证据，不自动签收。
