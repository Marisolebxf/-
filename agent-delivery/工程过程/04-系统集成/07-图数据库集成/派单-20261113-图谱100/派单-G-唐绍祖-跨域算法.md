# 派单说明 · KG-GRAPH-ALGO-07（包 G · 唐绍祖 · 跨域算法）

> 2026-11-13。淮政玮派。P1，第二批（11-20 起），但**方案与试算要 11-18 前出**（D 包 426 要用）。
> 一句话：现在的算法全在技术点那张小图上跑，需规 426 要的是人才/机构的合作链，得让算法走出技术点图。

```text
/goal algorithm-agent
身份：你是图算法负责人，做过 T08 路径、T09 中心性、T10 社群。本单只做算法与归档，不写接口、不改契约。禁止用 ponytail 删减算法项，禁止在 graphd 里直接跑大循环。

任务：KG-GRAPH-ALGO-07
标题：跨域算法（426 合作链路径 · 433 第二社群算法 · 人才/机构网络中心性）
Epic：E-SCI-INT
优先级：P1（方案与试算 11-18 前）
类型：algorithm
负责人：agent:algorithm-agent，supervised_by=human:唐绍祖。
状态：ready。
仓：gkx-orchestration，分支 dev。产物落归档目录。
图空间：demo_gkx_chain（只读）。
完成日期要求：方案+试算 2026-11-18；全量归档 2026-11-25。

强度：medium。

前置事实（已签收，直接采信）：
- 已有能力全在技术点图：19,430 点、tech_rel 541,428 边。T08 出 BFS/Dijkstra + 5 备选；T09 出 428–432；T10 出 Louvain 180 群。
- 七要素网络规模：person-person `cooperate` 2,525,789（M01）、research-research `cooperate` 3,442,271（M02）、person-research `belong` 72,099（M04）。
- 图库内存 80%，`sum(weight)` 级聚合 518 秒后被拒。**禁止在 graphd 里跑全图迭代。**
- 需规 423 写「支持多种路径搜索算法」，当前只实现 2 种；需规 433 写「多种社群发现算法」，当前只有 Louvain 1 种。
- 需规 426 场景化路径 = 合作链（人才-人才、机构-机构）、成果传播路径。

目标：三件事各出可归档结果 —— ① 426 合作链路径可查；② 433 至少两种社群算法可跑并给出对比；③ 人才/机构网络有中心性榜（同 T12 契约字段，供 D 包按域参数化返回）。

范围：
1. 数据导出（不在 graphd 内计算）
   - 按 Tag 锚定导出邻接表：`person` 的 M01 邻居、`research` 的 M02 邻居，字段含 src/dst/weight/confidence。
   - 分片导出（每片 ≤ 100 万边），落本地临时文件；导出脚本可断点续。
2. 426 合作链路径
   - 输入：起点实体 id + 终点实体 id + 域（person|research）+ 最大跳数。
   - 算法：BFS（最少跳）与 Dijkstra（最低代价，代价 = 1/relation_confidence_score，沿用 T08 已签收公式）。
   - 输出：Top 5 路径（节点序列 + 边 + 每步代价 + 总代价）；无路径返回 `path=[]` 且 `reason=NO_PATH`，不返回假路径。
   - 规模限制：单次查询跳数 ≤ 4；超过返回 `unsupported.code=DEPTH_LIMIT`。
3. 433 第二社群算法
   - 在技术点图上加 **Label Propagation**（轻量、无新依赖、可复现）：固定随机种子、固定迭代上限，输出社群号与规模。
   - 与 Louvain 结果对比：同社区率（NMI 或简单重合率）+ 社群数差异；写清两者适用场景。
   - 不改 Louvain 的既有结论（180 群），只并列新增。
4. 人才/机构网络中心性
   - 对 M01 与 M02 分别算度（含加权度）、PageRank；紧密/中介若在 250 万/344 万边上跑不动，先只出度与 PageRank，并在文档写明「紧密/中介待扩容后再评」。
   - 输出字段与 T12 完全一致（items[{nodeId,rank,score,raw,normalized}]、meta.populationSize、meta.metric_source、meta.scope），供 D 包直接按 domain 参数返回。
5. 归档
   - `对接文档/我方/KG-GRAPH-ALGO-07/` 下按域分目录（person/ research/ tech-lpa/），每份含 JSON + method.md（公式、参数、快照哈希、耗时）。

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-ALGO-07-跨域算法.md

Handoff：
agent-delivery/agent-handoffs/KG-GRAPH-ALGO-07.md
写清：三件事各自的产物路径、覆盖点数、耗时、未跑项与原因。
evidence 指向主文。task-update-status 到 integration，不写 done。

禁止：
- 在 graphd 内跑全图迭代或大聚合。
- 改 T08/T09/T10 已签收口径（代价公式、加权度口径、Louvain B′）。
- 用模型/启发式冒充「预测」能力（404/405 仍是 501）。
- 返回假路径、假社群、假分数。
- 把口令、连接串写进 git。
```

---

## 附：为什么 426 是这一单的核心

需规 426 写的是「场景化路径应用」，举的例子是合作链、成果传播。**合作链在人才和机构那张 600 万条边的网上，不在技术点图上**。现在所有路径算法都在 54 万条边的小图上跑，换个场景就无数据 —— 这不是接口问题，是算法没覆盖。
