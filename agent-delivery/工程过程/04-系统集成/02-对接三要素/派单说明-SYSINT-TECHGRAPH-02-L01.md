# 派单说明 · SYSINT-TECHGRAPH-02-L01

```text
/goal api-agent
身份：你是 Java 平台工程师。本单在算法中台加「技术点图谱」菜单，并把久新技术点同步进本侧节点表。协作 frontend-agent 做页面，协作 algorithm-agent 只加字典 op。向量、入图、写回都不在本单。
强度：ponytail full
图：必含 SYSINT-TECHGRAPH-02-SEQ。图在方案-SYSINT-TECHGRAPH-02-L01.md「调用」一节。不另画全局拓扑。图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。

任务：SYSINT-TECHGRAPH-02-L01
标题：技术点图谱菜单与节点同步
WBS：WBS-02-19
监管人：human:淮政玮。开工前 task-claim，claimed_by=agent:api-agent，supervised_by=human:淮政玮。状态若仍是 backlog，先由 coordinator 转到 ready 再认领。
执行：agent:api-agent。协作 frontend-agent（demo-ui-system-test）、algorithm-agent（lumen-topic-py 字典 op）。同一 task-id，不另开任务。
状态：backlog。依赖 SYSINT-TOPICMAP-02-L01。依赖叶未结束前不改 demo-ui-system-test、demo-svc-platform、lumen-topic-py 里它正在改的文件。
仓：lumen-topic-py、demo-svc-platform、demo-ui-system-test。分支 origin/dev。工程自检绿后 commit + push origin/dev，commit 带 [agent:<role>]。禁止 force push，禁止推 main。
开始时间：2026-11-05。完成日期要求：待指定。

已锁定（执行时不得改口）：
主键是 technology_node_id。不是 tech_id，不是 path_id，不是 topic_id，不是 subfield_id。
菜单名「技术点图谱」，路由 /ops/tech-graph，挂在维护管理，排在「Topic与产业映射」下面。
【同步】只在人点击后发生。打开页面和关键字查询只读本侧表。
中文名用画像 technology_name_zh 原样写入。空就不写中文，不把英文抄进去。
不写 dwd_tech_node_industry_map、dwd_topic_industry_map、subfield_topic_map。
不落边、路径、论文、专利、机构。那些在 L02。
不写 Nebula。lumen 前端不调用本菜单。

目标：本侧有一张可查询的技术点节点表。其他模块以后只读这张表，不在页面打开时打久新。

调用方向（必须落在方案那张图上）：
同步：demo-ui-system-test → demo 网关 /ops/v1/tech-graphs/sync → gkx-innov → lumen-topic-py POST /internal/gkx-svc/dict/query（op=technology_graph_node_page）→ upsert demo_gkxlumenx_dwd.dwd_technology_graph_node。
查询：demo-ui-system-test → 网关 → gkx-innov → 只读这张表。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHGRAPH-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHMAP-02-L01.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-19）
- agent-delivery/architecture-baseline.md
- agent-delivery/diagram-as-contract.md
- demo-ui-system-test：src/views/ops/opsMenuConfig.ts、src/router/index.ts、src/views/ops/pages/TechNodeMapPage.vue
- demo-svc-platform gkx-innov：technode/TechNodeMapController、TechNodeMapService
- lumen-topic-py：gkx_svc_service/jx_dict.py 的 technology_node_page 与 _OPS
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. 字典 op technology_graph_node_page。每页最多 500。SQL 从 ads_technology_profile 左连 ads_technology_graph_node，键 technology_node_id。返回节点号、中文名、英文名、community_role、weighted_degree、community_id、graph_release_id、data_version。没有节点号的行跳过。
2. 表 demo_gkxlumenx_dwd.dwd_technology_graph_node。按 technology_node_id upsert，不整表清空。某一页失败时已写入的页保留，页面写出失败原因。字典返回空则不改表。来源约 19,430 行。建表方式跟 TechNodeMapService 保证表存在的做法一致，不写入供应方库。
3. 菜单。OPS_SUB_MENU 增加 { path: '/ops/tech-graph', label: '技术点图谱' }，路由照抄 /ops/tech-node-map。页面有【同步】、全表数量、关键字查询（最多 200 行）、节点表。没有【关联】，没有边和实体区域（L02 再加）。
4. 网关。路由 id gkx-ops-tech-graphs，Path=/ops/v1/tech-graphs 与 /ops/v1/tech-graphs/**，uri lb://gkx-innov。helm 的 gkx-gateway-dev.yml 与 gkxx.sys_route_conf 两处都要有，过滤器与 gkx-ops-tech-node-maps 逐项相同。不要发会清空只存在于 Redis 的路由的 reload。
5. Java 控制器挂 /v1/tech-graphs，本叶只做 sync 和节点 query、stats。sync 按页调字典，每页不超过 500。

DoD：
1. dwd_technology_graph_node 能按 technology_node_id 同步约 19,430 行，含中文名、英文名、社区角色、加权度、graph_release_id。按主键 upsert，不整表清空。空中文保持空。
2. 来源是 lumen-topic-py op=technology_graph_node_page，每页不超过 500。页面不直连久新。
3. 算法中台维护管理有菜单「技术点图谱」（/ops/tech-graph）。【同步】才打字典。查询只读本侧表，最多 200 行。
4. 不写入三张已有映射表，不建边表，不写 Nebula。
5. handoff 写明表名、op、菜单路径、网关路由 id。架构自检：调用链不越层、Java 不写 nGQL、密码不进 git。handoff 路径 agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TECHGRAPH-02-L01.md，含 ponytail: full 和 diagram_id: SYSINT-TECHGRAPH-02-SEQ。evidence 指向该 handoff、本派单和方案。不要把任务标 done。

可观测：Java 转发沿用 gkx-innov 已有日志。Python 字典沿用已有 OTel。本页数字是同步行数，不为每个节点加指标 ⓘ。

禁止：
- 同步或落库 ads_technology_graph_edge、evolution_path_step、paper、patent、institution。
- 把 tech_id、path_id、topic_id、subfield_id 写成主键。
- 用 8 行 ads_technology_commercial_value_simulation 当节点。
- 把英文名写入中文列。
- 重开 WBS-02-03，或改政策三页、iticsci 专题仓、lumen 展示前端。
- 改 dwd_tech_node_industry_map、dwd_topic_industry_map、subfield_topic_map 的既有行。
- 页面打开或查询时自动同步。
- 用 fixture 或随机数填节点。
- 前端直连 Python、久新或 Nebula。lumen 前端调用本 demo 中台。
- task-create 新叶，或修改本任务以外的 depends_on、状态、DoD。
```
