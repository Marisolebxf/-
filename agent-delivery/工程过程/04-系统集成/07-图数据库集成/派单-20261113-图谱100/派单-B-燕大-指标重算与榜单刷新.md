# 派单说明 · KG-GRAPH-RECALC-02（包 B · 燕大 · 指标重算与榜单刷新）

> 2026-11-13。淮政玮派。P0，紧跟 A。**A 灌完不重算 = 白灌**：接口读的是榜单，边变了榜没变，428/432/435/437 的数字还是旧的。
> 一句话：用 A 灌完的新数据重算四类榜，和上一版逐项 diff，变了的地方要能解释。

```text
/goal data-agent
身份：你是资深图算法工程师，负责在大图上做离线预计算并把结果归档成可被接口直接读取的 JSON。本单不写接口、不改契约，只重算与出 diff。禁止用 ponytail 删减指标项，禁止用 headroom compress 代替精读 T09/T10 的口径。

任务：KG-GRAPH-RECALC-02
标题：技术点层指标重算与榜单刷新（428–432、435、437 数据面）
Epic：E-SCI-INT
优先级：P0
类型：data_task
负责人：human:韩梦蕊（监管 human:唐绍祖）。claimed_by=human:韩梦蕊 或 agent:algorithm-agent，supervised_by=human:唐绍祖。
状态：ready。依赖 KG-GRAPH-COVER-01 完成并交 integration。
仓：gkx-orchestration，分支 dev。产物落本仓归档目录，不写业务仓。
图空间：demo_gkx_chain（只读）。
完成日期要求：2026-11-18（P0 窗口，必须早于 D 包接口联调）。

强度：medium。允许写批处理脚本，必须限定并发，禁止无 Tag 锚定全表扫。

前置事实（已签收，直接采信）：
- T09-S1 已出四份归档：degree-full.json（19,430 行）、weighted-degree-full.json（19,430 行）、composite-recomputed.json（1,500 行）、degree 加权口径 = 入射边（入+出）relation_confidence_score/100 求和，degreeBasis=weight_sum_incident。
- T10 已出：180 个成形社群、435 行属性表（规模/内部边/平均度/密度/核心点）、Louvain B′ 定案。
- T12 契约已签收：字段为 items[{nodeId,rank,score,raw,normalized}]、meta.populationSize、meta.metric_source（透传 space/快照起止/nodes_sha256/edges_sha256/method/formula）、meta.scope。
- 图库内存到 80% watermark，大聚合可能被拒；重算优先在本地算（导出邻接表后离线跑），不在图库内跑大循环。

目标：把 428/429/430/431/432/435/437 七项的数据面刷新到与新边一致，并给出与上一版的 diff；接口方（D 包）拿到的 JSON 与 T12 契约字段完全一致。

范围：
1. 重算四项中心性：度（含加权度，口径不变：入射边求和）、紧密、中介、PageRank；输出 19,430 点整榜，可分页。
2. 重算综合榜（432）：四项各 0.25 权重，输出 1,500 点，rank 1..1500 连续、score 单调降。
3. 重算社群（435/437）：Louvain 同一实现、同一随机种子；输出社群号、规模、内部边、平均度、密度、核心点。社团数若与 180 差异超 ±10%，必须单独说明原因，不得静默改口径。
4. community_id 回填校验：A 包回填后，图内 community_id 与本次重算结果应对得上；若对不上，以图内为准并记录差异条数。
5. diff 报告：与 T09-S1 / T10 归档逐项比，给出「新增点、分值变化 Top20、排名变动 Top20、社群迁出迁入数」四张表；分值变化必须能用「边补了 45,824 条」解释。
6. 归档路径：沿用 T09-S1 目录结构，新建 `对接文档/燕大/KG-GRAPH-RECALC-02/`（不要覆盖 T09-S1 旧档）。

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-RECALC-02-重算与diff.md
归档 JSON 放 `对接文档/燕大/KG-GRAPH-RECALC-02/`，脚本同目录。

Handoff：
agent-delivery/agent-handoffs/KG-GRAPH-RECALC-02.md
写清：七项产物路径、行数、与旧版 diff 摘要、社群数变化、未完成项。
evidence 指向主文与归档目录。task-update-status 到 integration，不写 done。

禁止：
- 改 T09-S1 / T10 的旧归档文件（只新增）。
- 改 T12 契约字段名或结构。
- 改加权度口径（入射边求和是签收过的，不许改成出边或简单度数）。
- 无 Tag 锚定全表扫；图库内跑大循环。
- 在图里写任何点或边（本单只读）。
- 把口令、连接串写进 git。
```

---

## 附：为什么这一单必须紧跟 A

现在的榜是「边还没灌满」时算的。A 灌完 4.6 万条关系边、247 万条机构边后，度、PageRank、中介中心性都会变，社群也可能重划。**不重算，428 的榜首还是旧榜首，业务一点就会问「为什么新加的机构没进榜」**。本单的价值就在 diff：变了多少、为什么变，能当场答出来。
