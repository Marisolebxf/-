# 派单说明 · KG-7ELEM-BUILD-REQ-L01

> 2026-10-30 起，这五张单是长任务。开工以 [`KG-7ELEM-BUILD-长任务总控`](../../../agent-handoffs/七要素建图-KG-7ELEM/KG-7ELEM-BUILD-长任务总控.md) 和厚包为准。下游解锁看前序 handoff 且状态 ≥ integration，不等 done。监管人固定 `human:淮政玮`，后续认领不必再问。本文件只保留范围细则。

```text
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师。本单是定义类文档，完整性优先。禁止用 ponytail 强度行删表或删三元组。禁止用 headroom compress 代替精读需求清单、上图台账和入图流程。

任务：KG-7ELEM-BUILD-REQ-L01
标题：七要素必须三元组与建图需求：由展示查询清单与依赖图谱的算法收敛
Epic：E-SCI-INT
优先级：P0
类型：definition（定义）。本单是汇总。2026-10-30 已由 human:淮政玮 认领（claimed_by / supervised_by 都是 human:淮政玮）。不要再次 task-claim，不要把本单标 done。
执行已拆成三张子单，本单不重复做判定：
- KG-7ELEM-BUILD-REQ-L02 消费清单与实体归并。当前 ready，长任务可直接领。
- KG-7ELEM-BUILD-REQ-L03 必须三元组与关系总图。L02 有 handoff 且 ≥ integration 再领，不等 done。
- KG-7ELEM-BUILD-REQ-L04 建图动作与缺口。L03 有 handoff 且 ≥ integration 再领。可与 L05 并行。
- KG-7ELEM-BUILD-REQ-L05 建图完整 schema 与存储设计缺项。与 L04 同一道门。对照 storage 设计，不改 storage 文档，不重做 SYSINT-SCHEME-07-L07。
子单认领：claimed_by=agent:data-agent，supervised_by=human:淮政玮，lock_hours=24。note 写 claim_type=coordinator_dispatch。不必再问监管人。
协作：algorithm-agent。只在 SYSINT-SCHEME-07-L03 / L06 的索引对不上代码、且必须回指入口时请对方核对。不改算法仓。
仓：gkx-orchestration，分支 dev。只写过程文档，不改业务仓代码，不改图空间。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
签收操作人：human:淮政玮。
前置：KG-YANDA-SCHEMA-REQ-L01 已 done。查询侧数字以该单 v1.2 正文 §1.5 / §9 为准：保留 98 叶、转背景 16 叶、不相关 457 叶，飞书收回 84。不要用 §2.1 里残留的 81 / 15 / 475。

强度：N/A（定义/文档）。本单不写 SQL、ETL、脚本。
上下文：headroom 可选。需求清单、SYSINT-SCHEME-07-L03、L04、L06 必须读原文，禁止 compress 代替精读。
图：必含 KG-7ELEM-MUST-EDGES。一张 flowchart，只回答「七要素之间哪些边必须建」。先画这张图，再写关系总表，图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。不另画 L0 全局拓扑，不复制 ENT-STORAGE-FLOW / CHAIN-STORAGE-FLOW / SVC-STORAGE-FLOW。节点只用七要素中文名。必须建的边用实线，明确不建的不画进这张图（写在关系总表的「不建」列）。

必读（按这个顺序）：
- agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/知识图谱-实体关系属性需求清单.md（v1.2，查询侧真源）
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/智谱/SYSINT-SCHEME-07-L03-算法中台上图台账.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/智谱/SYSINT-SCHEME-07-L06-算法中台入图流程.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/智谱/SYSINT-SCHEME-07-L04-燕大七要素上图对照.md（只用来标「燕大已有 EDGE / 新建」，不是已放行契约）
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/智谱/SYSINT-SCHEME-07-L05-需求减已实现GAP.md（只作对照，不重做差集）
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/技术方案.md（调用链与「建图不进页面请求」的边界）
- agent-delivery/diagram-as-contract.md
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

目标：把已签收的展示查询需求，加上真正读图或写图的算法，收成七要素闭包里必须支持的三元组，以及七类之间要建哪些关系。产出是建图需求，不是接口实现，也不是另一份 GAP。

七要素（名称锁定，不得增删改名）：
企业、产业链环节、科研机构、技术、人才、服务机构、政策。
七要素里的「技术」= 论文 / 专利 / 项目。展示清单里的 technology（技术点 / 技术方向）不是这一类，归「不进七要素建图」。

范围（三张子单各写各的文件，总单只汇总）：
1. L02 消费清单。从 v1.2 查询侧里真正读图的部分（实体详情、邻接、路径、子图、图计算），加上 SYSINT-SCHEME-07-L03 / L06 已索引的读图或写图算法入口，逐条列出要的三元组：起点类型、关系、终点类型、用途。每条回指需规 seq，或回指算法入口（文件或指标 id）。统计指标、纯前端交互、图谱版本和批量导入不进这张表。
2. L02 归并表。展示清单 14 类实体逐类归入上面七个名字，或标「不进七要素建图」。不进的至少包括：technology 技术点、field、topic、dataset、event、activity、innovation_carrier。服务机构只在确有消费时进入七要素，不因为 SAD 里有这个名字就单建边。落盘 KG-7ELEM-BUILD-REQ-L02-消费与归并.md。
3. L03 必须三元组表。只收 L02 已列出、且两端都是七要素的三元组。列：起点要素、关系、终点要素、方向、基数、必须或可选、消费来源、燕大现有 EDGE 复用还是新建。没有消费的边不要写进「必须」。不新开 L02 没有的消费来源。
4. L03 关系总表，并配图 KG-7ELEM-MUST-EDGES。七类两两之间：必须建 / 明确不建。不建要写原因，只允许三种：无消费、已有边覆盖、待确认。落盘 KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md。
5. L04 建图需求。L03 每条必须三元组一行：建图动作、抽取来源占位、SYSINT-SCHEME-07-L03 / L06 里是否已有写图流水线、缺口。不新增、不删除必须边。表名在来源材料里没有的，写「待确认」，禁止臆造表名、枚举和样本量。落盘 KG-7ELEM-BUILD-REQ-L04-建图需求.md。
6. L05 建图 schema。只覆盖 L03 必须三元组：Tag、VID、属性、Edge、方向。再对照 data/data-design/storage 下 ENT、CHAIN、POLICY、SVC、COMP 的 pipeline-to-nebula.md 与 stores/nebula。缺项只写存储设计没有、但建图 schema 需要的 Tag、Edge、属性，或七要素没有对应存储域。不改这些存储文档。不把 SYSINT-SCHEME-07-L07 的代码差异再做一遍。落盘 KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md。
7. 总单 L01 把上面四份收成主文，不改四张子单已经写定的判定。

主文路径（新建，不改 v1.2 清单，不改 SYSINT-SCHEME-07-L03–L06）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L01-七要素必须三元组与建图需求.md

Handoff：
agent-delivery/agent-handoffs/KG-7ELEM-BUILD-REQ-L01.md
ponytail: N/A（定义/文档）
evidence 指向这份 handoff 和上面的主文路径。
handoff 写清：必须三元组条数、不建条数、待确认条数、图 ID。然后 task-update-fields 填 evidence，task-update-status 到 integration。不要写「会签通过」，除非人已经会签。不要改成 done。done 只由 human:淮政玮 签收。

禁止：
- 重做 KG-YANDA-SCHEMA-REQ-L01 的 99 条属性清单，或重做 KG-YANDA-GAP-L01 的差集计数。
- 把 SYSINT-SCHEME-07-L03 / L04 / L05 未签收台账写成已放行契约。引用时标明文件状态。
- 把 technology 技术点并进七要素「技术」。
- 把论文、专利、项目降成技术点的属性。七要素「技术」仍是论文 / 专利 / 项目三类可查询节点。
- 写 REST、改 Nebula space、配 GDF 作业、改 lumen-algo-py / Java / 前端。
- 在过程夹里改 scope-baseline。
- 密码、连接串、API Key 写入 git。
```
