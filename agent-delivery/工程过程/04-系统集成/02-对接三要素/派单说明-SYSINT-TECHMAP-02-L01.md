# 派单说明 · SYSINT-TECHMAP-02-L01

```text
/goal data-agent
身份：你是数据侧负责人。本单只落实技术域哪些对象能新建本侧表，并经接口同步进本侧库，使后续 LLM 能逐条关联到产业节点并落进新建 DWD。本叶不写同步代码、不调模型、不改业务仓。
强度：ponytail off（定义任务）。不得用 YAGNI 删掉下面已锁定的身份和排除项。

任务：SYSINT-TECHMAP-02-L01
标题：技术节点与产业关联：落实可同步表与新建 DWD
WBS：WBS-02-12
监管人：human:淮政玮。2026-10-31 用户纠正，此前按 data-agent 花名册默认写成徐滕强。claimed_by=agent:data-agent，supervised_by=human:淮政玮。
执行：agent:data-agent。协作 algorithm-agent（关联过程只定粒度，不在本叶调用）、api-agent（同步接口只定边界，不在本叶实现）。同一 task-id，不另开任务。
状态：backlog，未认领。依赖 SYSINT-SURVEY-02-L01。
仓：只写 gkx-orchestration。分支 origin/dev。
开始时间：2026-10-31。完成日期要求：待指定。

已锁定（执行时不得改口）：
技术路线对应候选技术节点，主键是 technology_node_id。
不是正式目录 tech_id，不是代表路径 path_id，不是簇群 community_id，不是子学科 subfield_id。

目标：交出一份落实记录。记录写明哪些久新技术表可以新建本侧表并用接口同步进来，哪些不能。同步进来之后，【建立关联】按 technology_node_id 逐条做，结果落新建 DWD。菜单放在算法中台「维护管理」，与「产业集群映射」「子学科与专题映射」并列，可以是 1 个或多个；每个菜单都有【同步】和【建立关联】。

菜单入口：demo-ui-system-test，http://10.50.69.111:30889/#/ops/subfield-topic 左侧「维护管理」。现有两项是「产业集群映射」「子学科与专题映射」。新菜单挂在这两项下面，路由仍在现有 ops 下。本叶只定菜单名和每个菜单同步哪张表、关联哪张 DWD，不改 opsMenuConfig.ts。

必读：
- 本文件
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/调研记录.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv
- agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA-5.11.0.md §24、§25
- agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TFMAP-02-L01.md（只借【同步】【关联】过程，不借子学科表）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-12）
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. 可同步清单。每张表写久新表名、主键、调研时行数、建议的本侧表角色（节点主数据 / 节点证据 / 排除）、能否经接口同步。ads_technology_profile 必须可同步，主键 technology_node_id。
2. 菜单切分。默认一个菜单「技术节点与产业映射」：【同步】拉节点主数据，【建立关联】把 technology_node_id 对上本侧已有产业节点。若拆成多个菜单，每个菜单的关联主键仍是 technology_node_id，并写明拆分原因。
3. 新建 DWD 的逻辑键：technology_node_id + 本侧产业节点 id。未关联的节点保留目录行，关联列为空。表名在记录里拟定，本叶不执行 DDL。不写入 demo_gkxlumenx_dim.subfield_topic_map，不复用 WBS-02-08 的子学科行。
4. 过程边界写进记录：【同步】才经接口进本侧库，页面查询不直连久新。人点击【建立关联】之后才允许 Python 调 LLM，按节点逐条做。Java 不写提示词、不调模型。LLM 返回的产业节点 id 必须落在本侧已有目录，否则该节点保持未关联。

DoD（与注册表一致）：
1. 技术路线的关联粒度锁定为候选技术节点，主键 technology_node_id。正式 tech_id、代表路径、簇群、子学科都不是这条技术路线的主键。
2. 交出可同步清单：技术域每张候选表写明久新表名、主键、行数量级、能否经接口同步进本侧库，以及不能同步的原因。ads_technology_profile 必须在可同步清单里。正式目录、政策证据空表、投资额、模拟商业价值必须标成还没有或不能当主数据。
3. 维护管理下给出 1 个或多个菜单，与「子学科与专题映射」并列。每个菜单都有【同步】和【建立关联】。建立关联逐条对象是 technology_node_id，结果落新建 DWD（技术节点 ID + 本侧产业节点 ID）。不写入 subfield_topic_map。
4. 本叶只出落实记录和 handoff，不写同步代码、不调 LLM、不改业务仓、不建深度页、不改政策三页、不改 WBS-02-08 与 SYSINT-06-19。handoff 指向派单说明。

handoff：agent-delivery/agent-handoffs/SYSINT-TECHMAP-02-L01.md。含 ponytail: off。evidence 指向该 handoff 和本派单。不要把任务标 done。

禁止：
- 把 tech_id、path_id、community_id、subfield_id 写成技术路线主键。
- 用 ads_technology_commercial_value_simulation 的 8 行模拟数据当技术节点。
- 把 0 行的 ads_technology_policy_evidence 解释成没有政策。
- 重开 WBS-02-03，或新建技术链、人才、科研机构深度分析页。
- 修改 iticsci 专题仓、demo-ui-system-test、Java、Python。
- 改写 subfield_topic_map，或把本叶并进 SYSINT-06-19。
- 本叶执行建表、同步或 LLM。
```

## 2026-10-31 执行顺序

用户下令分两步，且第二步同叶开发，覆盖上文「不改业务仓、不写同步代码」：

1. 方案：[方案-SYSINT-TECHMAP-02-L01.md](./方案-SYSINT-TECHMAP-02-L01.md)。一个菜单。只同步 `ads_technology_profile`。
2. 开发到算法中台：`demo-ui-system-test` 菜单，`gkx-innov` 写 `dwd_tech_node_industry_map`，字典与模型仍走已有 Python 内部接口。不改子学科映射，不改 iticsci。
3. 纠正已发布到 lumen 的全景「主流技术路线」。该页签不再读子学科映射。改读 `demo_gkxlumenx_dwd.dwd_tech_node_industry_map` 的 `technology_node_id`。没有关联行就保持「暂无已发布主流技术路线」。

## 附：调研结论（2026-10-22 调研记录 + schema 5.11.0 §24–§25）

库是久新 Doris `gkx_technology_analysis_dev`。技术域 29 张 `ads_technology_*`。ADS 不建外键，关系靠同名 ID 列。

身份：

| 概念 | 主键 | 和本叶的关系 |
|---|---|---|
| 候选技术节点 | `technology_node_id` | **技术路线就是这个节点。** 画像和图节点各 19,430 行。`node_identity_type=RESEARCH_CLUSTER_CANDIDATE` |
| 来源研究簇 | `research_cluster_id` | 写在节点行上，一对一。不是第二条技术路线 |
| 正式技术目录 | `tech_id` | 列在画像上，全部为空，`mapping_status=UNMAPPED`。映射表还没有，不能同步成主数据 |
| 簇群 | `community_id` | 1,731 行，其中 1,708 个单节点簇。算法快照，不是技术路线主键 |
| 代表路径 | `path_id, step_order` | 47,909 步。每个目标节点一条导航路径，不是节点身份 |

可作节点证据、由本叶决定是否随节点同步的表：`ads_technology_paper`、`ads_technology_patent`、`ads_technology_institution`、`ads_technology_application_case`，以及热点、潜力、阶段、年度指标。它们的关联键都是 `technology_node_id`，不单独成为技术路线。

排除：

- `ads_technology_graph_edge`、`ads_technology_evolution_edge`：节点和节点的边，各 587,252 行。不是产业关联的主体。
- `ads_technology_commercial_value_simulation`：主键是 `catalog_release_id + tech_id`，8 行，`SYNTHETIC_SIMULATION`。不挂 `technology_node_id`。
- `ads_technology_policy_evidence`：0 行。
- `M_TECH_INVEST_AMOUNT`：还没有。市场、收入、融资未接入。
- 指标名里的「技术点」对上的就是这 19,430 个节点，没有另一张叫技术点的表。
- 子学科 `subfield_id` 是 WBS-02-08 的技术领域口径，不是本叶的技术路线。
