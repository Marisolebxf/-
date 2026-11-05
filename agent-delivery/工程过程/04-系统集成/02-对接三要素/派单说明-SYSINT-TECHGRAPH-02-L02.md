# 派单说明 · SYSINT-TECHGRAPH-02-L02

```text
/goal api-agent
身份：你是 Java 平台工程师。本单只做「技术点图谱」的边上图，以及边、路径、实体的只读列表。协作 frontend-agent 做八颗按钮，协作 algorithm-agent 做字典分页和写边。不补点，不挂产业。
强度：ponytail full
图：必含 SYSINT-TECHGRAPH-02-SEQ。图在方案-SYSINT-TECHGRAPH-02-L01.md「调用」一节。只走「边上图」那一支。不另画全局拓扑。图文冲突以图为准。

任务：SYSINT-TECHGRAPH-02-L02
标题：技术点图谱边上图
WBS：WBS-02-20
监管人：human:淮政玮。开工前 task-claim，claimed_by=agent:api-agent，supervised_by=human:淮政玮。状态若仍是 backlog，先由 coordinator 转到 ready 再认领。
执行：agent:api-agent。协作 frontend-agent、algorithm-agent。同一 task-id，不另开任务。
状态：backlog。依赖 SYSINT-TECHGRAPH-02-L01。L01 未交出菜单、节点表和实体入图之前不开工。
仓：lumen-topic-py、lumen-algo-py、demo-svc-platform、demo-ui-system-test。分支 origin/dev。工程自检绿后 commit + push origin/dev，commit 带 [agent:<role>]。禁止 force push，禁止推 main。
开始时间：待 L01 之后。完成日期要求：待指定。

已锁定：
八颗按钮各走各的接口：技术点关系上图、低证据关系上图、论文上图、专利上图、机构上图、人上图·论文、人上图·Topic、路径上图。点一颗不调用另一颗，不写点，不挂产业。
一次请求最多 500 行。页面按页往下翻，本页处理 0 行或失败就停。
任一端点不在 demo_gkx_chain 上就跳过并计数，不创建这个点。
技术点关系上图只写 evidence_level 为 HIGH 或 MEDIUM 的 tech_rel。低证据关系上图只写 LOW。路径写入 tech_path_step，不写入 tech_rel。
人边上的来源标记只由对应那颗按钮写入。
只读列表不写图。边和路径列表每页最多 50。论文、专利、机构、两路人默认各 20 条。列表查询必须带 technology_node_id，没有就 400。
不建边表、路径表、实体表。不写 gkx_chain。不写三张已有映射表。Java 不写 nGQL。

调用：demo-ui-system-test → 网关 /ops/v1/tech-graphs/** → gkx-innov → lumen-topic-py 取一页 → lumen-algo-py POST /internal/tech-graph/edge。列表查询不调用 edge。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/科学技术全景-建图基线.md
- lumen-topic-py：gkx_svc_service/jx_dict.py
- lumen-algo-py：L01 的 /internal/tech-graph/vertex。本单只加 /internal/tech-graph/edge
任务查询只用 MCP。禁止读 task-registry.yaml。

范围：
1. 八个字典分页 op，分别对应八颗按钮。都要求能按页取，人的两颗没有本页论文号或本页 topic_id 就拒绝。
2. Java 八个写入路径彼此不同。edge 接口按请求里的一种 Edge 写入 demo_gkx_chain。
3. 页面八颗按钮，加上关系、路径、论文、专利、机构、人的只读列表。未选节点时列表为空，不发查询。

DoD：
1. 八颗按钮各自只写方案里的那一种 Edge。缺端点的行被跳过，图上不因此多出一个点。
2. 技术点关系上图的结果里没有 LOW。低证据那颗的结果里没有 HIGH、MEDIUM。路径不进 tech_rel。
3. 只读列表不改变图。没有 technology_node_id 的列表查询被拒绝。边、路径、论文、专利、机构、人不落本侧新表。
4. handoff 路径 agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TECHGRAPH-02-L02.md，含 ponytail: full 和 diagram_id: SYSINT-TECHGRAPH-02-SEQ。不要把任务标 done。

禁止：
- 在边上图里创建顶点，或调用挂产业。
- 全量把 58 万边、4.8 万路径步或 252 万机构行写入本侧 MySQL。
- 查询 ads_technology_application_case、ads_technology_policy_evidence、ads_patent_analysis_topic。
- 不带本页 paper_id 或 primary_topic_id 去扫人才表。
- 把科研项目写成市场应用。
- 在本页做增删改、导入、版本。
- 改 L01 的节点表和 Tag 语义，或改三张产业映射表。
- 前端直连久新或 Python。lumen 展示页调用本接口。
- task-create 新叶。
```
