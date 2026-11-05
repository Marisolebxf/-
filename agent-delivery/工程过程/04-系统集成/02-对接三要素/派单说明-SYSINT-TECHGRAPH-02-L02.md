# 派单说明 · SYSINT-TECHGRAPH-02-L02

```text
/goal api-agent
身份：你是 Java 平台工程师。本单给「技术点图谱」菜单补上选定节点之后的边、路径和关联实体。只按节点分页查询，不把大表同步进本侧库。协作 frontend-agent 做页面，协作 algorithm-agent 只加字典 op。
强度：ponytail full
图：必含 SYSINT-TECHGRAPH-02-SEQ。图在方案-SYSINT-TECHGRAPH-02-L01.md「调用」一节。查询走图里「边、路径、论文、专利、机构」那一支。不另画全局拓扑。

任务：SYSINT-TECHGRAPH-02-L02
标题：技术点图谱按节点查看边、路径和关联实体
WBS：WBS-02-20
监管人：human:淮政玮。开工前 task-claim，claimed_by=agent:api-agent，supervised_by=human:淮政玮。状态若仍是 backlog，先由 coordinator 转到 ready 再认领。
执行：agent:api-agent。协作 frontend-agent、algorithm-agent。同一 task-id，不另开任务。
状态：backlog。依赖 SYSINT-TECHGRAPH-02-L01。L01 未交出菜单和节点表之前不开工。
仓：lumen-topic-py、demo-svc-platform、demo-ui-system-test。分支 origin/dev。工程自检绿后 commit + push origin/dev，commit 带 [agent:<role>]。禁止 force push，禁止推 main。
开始时间：待 L01 之后。完成日期要求：待指定。

已锁定：
每次查询必须带 technology_node_id。没有节点号就 400，禁止不带条件扫全表。
边默认只要 evidence_level 为 HIGH 或 MEDIUM。请求显式要求时才含 LOW。
论文、专利默认各 20 条，按 representative_rank。机构默认 20 条，按 institution_rank。边和路径每页最多 50。
人才区域只有固定缺口文案，不查人才表，不借 Topic 桥充数。
不建边表、路径表、实体表。不写 Nebula。不提供增删改。

调用：demo-ui-system-test → 网关 /ops/v1/tech-graphs/** → gkx-innov → lumen-topic-py 按节点分页。节点列表仍只读 L01 的本侧表。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv（只核对行数量级，不重扫库）
- lumen-topic-py：gkx_svc_service/jx_dict.py
任务查询只用 MCP。禁止读 task-registry.yaml。

范围：
1. 五个字典 op：technology_graph_edge_page、technology_graph_path_page、technology_graph_paper_page、technology_graph_patent_page、technology_graph_institution_page。都要求 technology_node_id。边 op 读 ads_technology_graph_edge，路径 op 读 ads_technology_evolution_path_step，实体三个 op 读对应的 paper、patent、institution 表。
2. Java 在已有 /v1/tech-graphs 上增加这五个查询。不新增 sync。
3. 页面在已选定节点下显示关系、路径、论文、专利、机构。关系筛选默认不含 LOW，并可改成含 LOW。人才一栏只显示方案里的那句缺口文案。未选节点时这四个区域为空，不发查询。

DoD：
1. 选定一个已同步节点后，能分页看到它的邻边、路径步、代表论文、代表专利、关联机构。未选节点不发这些查询。
2. 边默认不含 LOW。论文和专利按代表排名，机构按机构排名，默认各 20 条。边和路径每页不超过 50。
3. 没有 technology_node_id 的查询被拒绝。这五类数据不落本侧新表。
4. 人才区域只有缺口文案，页面上看不到编造的人名。
5. handoff 路径 agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TECHGRAPH-02-L02.md，含 ponytail: full 和 diagram_id: SYSINT-TECHGRAPH-02-SEQ。不要把任务标 done。

禁止：
- 全量同步 58 万边、4.8 万路径步或 252 万机构行。
- 查询 ads_technology_application_case、ads_technology_policy_evidence、ads_talent_topic_profile。
- 把科研项目写成市场应用，或把 0 行政策表写成没有政策。
- 在本页做增删改、导入、版本、入图。
- 改 L01 的节点表语义，或改三张产业映射表。
- 前端直连久新或 Python。lumen 展示页调用本接口。
- task-create 新叶。
```
