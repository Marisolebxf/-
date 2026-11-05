# 派单说明 · SYSINT-TECHGRAPH-02-L01

```text
/goal api-agent
身份：你是 Java 平台工程师。本单在算法中台加「技术点图谱」菜单，并做七颗实体按钮。协作 frontend-agent 做页面，协作 algorithm-agent 做字典分页和入图。边上图、挂产业不在本单。
强度：ponytail full
图：必含 SYSINT-TECHGRAPH-02-SEQ。图在方案-SYSINT-TECHGRAPH-02-L01.md「调用」一节。本单只走「技术点入库」和「实体入图」。不另画全局拓扑。图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。

任务：SYSINT-TECHGRAPH-02-L01
标题：技术点图谱菜单与实体入图
WBS：WBS-02-19
监管人：human:淮政玮。开工前 task-claim，claimed_by=agent:api-agent，supervised_by=human:淮政玮。状态若仍是 backlog，先由 coordinator 转到 ready 再认领。
执行：agent:api-agent。协作 frontend-agent（demo-ui-system-test）、algorithm-agent（lumen-topic-py 字典 op，lumen-algo-py 写点）。同一 task-id，不另开任务。
状态：backlog。依赖 SYSINT-TOPICMAP-02-L01。依赖叶未结束前不改它正在改的文件。
仓：lumen-topic-py、lumen-algo-py、demo-svc-platform、demo-ui-system-test。分支 origin/dev。工程自检绿后 commit + push origin/dev，commit 带 [agent:<role>]。禁止 force push，禁止推 main。
开始时间：2026-11-05。完成日期要求：待指定。

已锁定（执行时不得改口）：
主键是 technology_node_id。不是 tech_id，不是 path_id，不是 topic_id，不是 subfield_id。
菜单名「技术点图谱」，路由 /ops/tech-graph，挂在维护管理，排在「Topic与产业映射」下面。
七颗按钮各走各的接口。点一颗不调用另一颗，不写边，不挂产业。打开页面和关键字查询不打久新，也不入图。
一次请求最多 500 行。页面按页往下翻，本页处理 0 行或失败就停。已写入的页保留。
图空间只写 demo_gkx_chain。Tag 只用方案里的 tech_point、tech_paper、tech_patent、tech_institution、tech_person。VID 用方案里的前缀。
人入图·论文只查 ads_talent_research_achievement。人入图·Topic 只查本页论文的 primary_topic_id。同一人两路都有时，后一颗只补自己的来源标记。
中文名用画像 technology_name_zh 原样写入。空就不写中文，不把英文抄进去。
不写 dwd_tech_node_industry_map、dwd_topic_industry_map、subfield_topic_map，也不建 dwd_technology_topic_industry。
不写 gkx_chain。lumen 前端不调用本菜单。Java 不写 nGQL。

目标：技术点先有本侧节点表，再有一颗只写点的入图按钮。论文、专利、机构、两路人各自只写自己的点。

调用方向（必须落在方案那张图上）：
技术点入库：demo-ui-system-test → demo 网关 → gkx-innov → lumen-topic-py op=technology_graph_node_page → upsert dwd_technology_graph_node。
其余六颗入图：同一网关 → gkx-innov → 该按钮自己的字典页 → lumen-algo-py POST /internal/tech-graph/vertex。
节点查询：网关 → gkx-innov → 只读节点表。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/科学技术全景-建图基线.md
- agent-delivery/architecture-baseline.md
- agent-delivery/diagram-as-contract.md
- demo-ui-system-test：src/views/ops/opsMenuConfig.ts、src/router/index.ts、src/views/ops/pages/TechNodeMapPage.vue
- demo-svc-platform gkx-innov：technode/TechNodeMapController、TechNodeMapService
- lumen-topic-py：gkx_svc_service/jx_dict.py 的 technology_node_page 与 _OPS
- lumen-algo-py：已有 /internal/topic-industry/link 的挂法，本单新开 /internal/tech-graph/vertex，不改 Topic 关联接口
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. 字典 op technology_graph_node_page，以及论文、专利、机构、人·论文、人·Topic 五个分页 op。每页最多 500。节点 SQL 从 ads_technology_profile 左连 ads_technology_graph_node。没有节点号的行跳过。人和机构的 op 没有本页技术点或本页论文号就拒绝。
2. 表 demo_gkxlumenx_dwd.dwd_technology_graph_node。只有「技术点入库」写它。按 technology_node_id upsert，不整表清空。来源约 19,430 行。建表方式跟 TechNodeMapService 保证表存在的做法一致。
3. lumen-algo-py 的 /internal/tech-graph/vertex 按请求里的一种 Tag 写 demo_gkx_chain。一种请求不写第二种 Tag，不写 Edge。
4. 菜单。OPS_SUB_MENU 增加 { path: '/ops/tech-graph', label: '技术点图谱' }，路由照抄 /ops/tech-node-map。页面有七颗实体按钮、全表数量、关键字查询（最多 200 行）、节点表。没有边上图按钮，没有挂产业按钮（L02、L03 再加）。
5. 网关。路由 id gkx-ops-tech-graphs，Path=/ops/v1/tech-graphs 与 /ops/v1/tech-graphs/**，uri lb://gkx-innov。helm 的 gkx-gateway-dev.yml 与 gkxx.sys_route_conf 两处都要有，过滤器与 gkx-ops-tech-node-maps 逐项相同。不要发会清空只存在于 Redis 的路由的 reload。
6. Java 控制器挂 /v1/tech-graphs。七个写入路径彼此不同，另加节点 query、stats。

DoD：
1. 「技术点入库」能按 technology_node_id 写入约 19,430 行。按主键 upsert，不整表清空。空中文保持空。这颗按钮不写 Nebula。
2. 其余六颗按钮各自只把一种点写入 demo_gkx_chain 的对应 Tag。响应里没有边，也没有产业节点。
3. 算法中台维护管理有菜单「技术点图谱」（/ops/tech-graph）。查询只读本侧表，最多 200 行。
4. 不写入三张已有映射表，不建关系表，不写 Edge，不写 gkx_chain。
5. handoff 写明表名、op、Tag、菜单路径、网关路由 id。架构自检：调用链不越层、Java 不写 nGQL、密码不进 git。handoff 路径 agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TECHGRAPH-02-L01.md，含 ponytail: full 和 diagram_id: SYSINT-TECHGRAPH-02-SEQ。evidence 指向该 handoff、本派单和方案。不要把任务标 done。

可观测：Java 转发沿用 gkx-innov 已有日志。Python 沿用已有 OTel。本页数字是本页处理行数，不为每个节点加指标 ⓘ。

禁止：
- 在实体按钮里写 Edge，或调用挂产业。
- 把 tech_id、path_id、topic_id、subfield_id 写成技术点主键。
- 用七要素 Tag 名 technology、paper、person 写这些点。
- 用 8 行 ads_technology_commercial_value_simulation 当节点。
- 把英文名写入中文列。
- 查询 ads_technology_application_case、ads_technology_policy_evidence、ads_patent_analysis_topic。
- 不带本页论文号去扫 ads_talent_topic_profile。
- 重开 WBS-02-03，或改政策三页、iticsci 专题仓、lumen 展示前端。
- 改三张已有映射表的既有行。
- 页面打开或查询时自动入库、自动入图。
- 用 fixture 或随机数填节点。
- 前端直连 Python、久新或 Nebula。lumen 前端调用本 demo 中台。
- task-create 新叶，或修改本任务以外的 depends_on、状态、DoD。
```
