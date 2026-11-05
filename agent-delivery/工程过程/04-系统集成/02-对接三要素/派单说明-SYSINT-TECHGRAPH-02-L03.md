# 派单说明 · SYSINT-TECHGRAPH-02-L03

```text
/goal api-agent
身份：你是 Java 平台工程师。本单只做「技术点图谱」的挂产业。要素已经入图之后，用 Topic 对到已有产业节点，写入关系表。协作 frontend-agent 做五颗按钮，协作 algorithm-agent 只加取 Topic 的字典 op。本单不写 Nebula。
强度：ponytail full
图：必含 SYSINT-TECHGRAPH-02-SEQ。图在方案-SYSINT-TECHGRAPH-02-L01.md「调用」一节。只走「挂产业」那一支。不另画全局拓扑。图文冲突以图为准。

任务：SYSINT-TECHGRAPH-02-L03
标题：技术点图谱经 Topic 挂产业
WBS：WBS-02-21
监管人：human:淮政玮。开工前 task-claim，claimed_by=agent:api-agent，supervised_by=human:淮政玮。状态若仍是 backlog，先由 coordinator 转到 ready 再认领。
执行：agent:api-agent。协作 frontend-agent、algorithm-agent。同一 task-id，不另开任务。
状态：backlog。依赖 SYSINT-TECHGRAPH-02-L01 和 SYSINT-TOPICMAP-02-L01。节点表和 dwd_topic_industry_map 未交出之前不开工。
仓：lumen-topic-py、demo-svc-platform、demo-ui-system-test。分支 origin/dev。工程自检绿后 commit + push origin/dev，commit 带 [agent:<role>]。禁止 force push，禁止推 main。
开始时间：待 L01 与 Topic 映射表之后。完成日期要求：待指定。

已锁定：
五颗按钮各走各的接口：技术点挂产业、论文挂产业、人挂产业·论文、人挂产业·Topic、机构挂产业。点一颗不调用另一颗。
一次请求最多 500 行。页面按页往下翻，本页处理 0 行或失败就停。已写入的页保留。
Topic 只取方案里写的那一列。产业节点只读 dwd_topic_industry_map 里非空的 node_id。对不上的 Topic 跳过并计数，不重跑向量，不补产业节点。
写入 dwd_technology_topic_industry。逻辑键 entity_kind + entity_id + technology_node_id + topic_id + industry_node_id。按键更新，不整表清空。
不写 dwd_tech_node_industry_map、dwd_topic_industry_map、subfield_topic_map。不写 Nebula。专利不挂。
人没有直连表。论文来源和 Topic 来源各一颗按钮，只写自己的 link_source。

调用：demo-ui-system-test → 网关 /ops/v1/tech-graphs/** → gkx-innov。Java 向 lumen-topic-py 取本页 Topic，再读 dwd_topic_industry_map，写入关系表。不调用 lumen-algo-py。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TOPICMAP-02-L01.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/科学技术全景-建图基线.md
任务查询只用 MCP。禁止读 task-registry.yaml。

范围：
1. 表 demo_gkxlumenx_dwd.dwd_technology_topic_industry。列至少有 entity_kind、entity_id、technology_node_id、topic_id、industry_node_id、link_source、写入时间。
2. 五个挂产业接口，路径彼此不同。机构按钮只拿本页已出现在 ads_technology_institution 的机构号，再查 ads_institution_topic_entry。没有本页技术点或本页论文号就 400。
3. 页面五颗按钮，加已挂产业只读列表。列表不触发写入。未选节点时列表为空。

DoD：
1. 五颗按钮都能把对得上产业节点的行写入 dwd_technology_topic_industry。对不上的只计数。
2. 任一按钮的响应里看不出它调用了另一颗按钮或写了 Nebula。
3. 三张已有映射表的行不变。专利没有挂产业按钮。
4. handoff 路径 agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TECHGRAPH-02-L03.md，含 ponytail: full 和 diagram_id: SYSINT-TECHGRAPH-02-SEQ。不要把任务标 done。

禁止：
- 查询 ads_technology_application_case、ads_technology_policy_evidence、ads_patent_analysis_topic。
- 不带本页技术点或本页论文号去扫 ads_talent_topic_profile、ads_institution_topic_entry。
- 改 L01 的节点表语义，或改三张产业映射表。
- 前端直连久新或 Python。lumen 展示页调用本接口。
- task-create 新叶。
```
