# 派单说明 · KG-COMPLY-SDD-L01

> 2026-11-06。定义单。负责人、交付确认人都是 `human:徐滕强`。登记册 DoD 末句仍印着「经 human:唐绍祖 确认」，以本派单和 [分工表](./WBS-全景维护与知识图谱分工.md) 为准。
> 现在是 backlog。`KG-COMPLY-STRUCT-L01`、`KG-COMPLY-ACCEPT-L01` 都还是 ready，没有书面结论。可以先搭说明书章节。空间、验收叶子、细任务清单等这两份结论再写死。

```text
/goal architect-agent
身份：你是资深架构师。本单只写详细设计说明书和细任务清单，不写业务代码，不入图。完整性优先。禁止用 ponytail 删章节、删必须边或删算法清单。禁止用 headroom compress 代替精读需规、L01 和分工表。
登记册执行角色现为 algorithm-agent。本派单不改这个字段。认领时 claimed_by=agent:architect-agent，supervised_by=human:徐滕强。认领被角色字段挡住就停，回报 coordinator，不要改登记册。

任务：KG-COMPLY-SDD-L01
标题：展示与图算法的详细设计，以及给燕大编排智能体的任务清单
Epic：E-SCI-INT
优先级：P0
类型：definition（定义）
负责人：human:徐滕强。交付确认人同为徐滕强。
状态：backlog。依赖 KG-COMPLY-STRUCT-L01、KG-COMPLY-ACCEPT-L01。两单没有书面结论前，不认领开工，不把细任务写死。
仓：gkx-orchestration，分支 dev。只写过程文档。不改业务仓，不改图空间。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
开始时间：2026-11-06。完成日期要求：待指定。

强度：N/A（定义/文档）。本单不写 SQL、ETL、脚本、接口实现。
上下文：headroom 可选。下面必读里的需规、L01、分工表必须读原文。
图：必含 KG-COMPLY-SDD-FLOW。一张 flowchart，只回答三件事：唐绍祖指定的空间上，哪些算法要跑出结果；燕大入图过程如何复用到正式加工线，且正式线结构至少盖住合规范围；后台接口落在整体集成项目还是燕大自己的项目。先画这张图，再写正文。图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。不另画 L0 全局拓扑。

目标：按 SDD 驱动，先写详细设计说明书，再按说明书拆成燕大同学能在与智树共用的编排环境里交给编排智能体执行的任务。每条细任务不靠口头补充。

两条主责写进说明书，不改派：
1. 唐绍祖：需规里图相关的算法，以及算法中台上图相关的算法，都要在他于 KG-COMPLY-STRUCT-L01 指定的空间上跑出结果。没跑出结果不算本期验收完成。本单只写清怎么跑。
2. 燕大：入图过程可复用，不和正式加工线混淆；正式加工线的结构至少包含现在合规范围。后台接口由燕大提供，可在整体集成项目里开发，也可在燕大自己的项目里开发，以运行效率为准。后台开发的过程和任务分解，与 human:徐滕强 或 human:唐绍祖 沟通确定。本单不替燕大写图，不替燕大定接口落点。

必读（按这个顺序）：
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS-全景维护与知识图谱分工.md
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS-全景维护与知识图谱分工-背景.md（合规范围草稿。点数和缺口可引用。正文里「只读 demo_gkx_chain、燕大不入这张图、不夹带技术点、燕大不建技术点」已停用）
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L01-七要素必须三元组与建图需求.md
- agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md
- agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/README.md 及其分析展示、指标展示、算法展示、服务展示
- agent-delivery/diagram-as-contract.md
- KG-COMPLY-STRUCT-L01、KG-COMPLY-ACCEPT-L01 的书面结论（有了再读；没有就在说明书里标「待结论」）
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

已锁定（执行时不得改口）：
入图范围只认 L01 必须三元组 M01–M24。不新增必须边。不建的不写，待确认的不猜。
七要素「技术」= 论文 / 专利 / 项目。技术点可以夹带，单独一层，不并进「技术」，不编成新的必须边。
空间新建还是补 demo_gkx_chain，由唐绍祖在 STRUCT 任务里定。同一套结构两种放法都要能装下。本单不另选空间。
本期是合规验收，不是 GDF 正式加工派单，不替代 WBS-07-00G / 00H。正式线的结构至少包含本期合规范围。
合规里图谱的维护管理可由王建峰、刘剑锋或燕大同学做，人选协商。王建峰尚未入册，定人时再登记。花名册里维护管理现监管人是 human:刘剑锋。
燕大可认领人：human:白鑫凤、human:陈芸飞、human:宋飞扬、human:韩梦蕊、human:兰天驰、human:李周。
前端接线联调，燕大可酌情参加。

范围：
1. 详细设计说明书。覆盖科学技术全景、维护管理、科技知识图谱，以及这些页面要读的图算法。验收叶子以 ACCEPT 的书面结论为准；没有结论的叶子标待定，不写成本期要交付。
2. 算法清单。分两列：需规里图相关的算法，算法中台上图相关的算法。每条写：在指定空间上读什么、怎样算跑出结果、没有结果时是 501 还是空。跑出结果的主责仍是唐绍祖。
3. 入图与正式线。写明入图过程如何复用，正式加工线的结构至少包含 M01–M24，技术点若夹带则单列。不把本期任务写成正式加工派单。
4. 后台接口。只写契约落点的两种允许做法和效率取舍，不选定最终仓库，不写接口实现。过程和任务分解留给与徐滕强或唐绍祖的沟通。
5. 细任务清单。每条包含：读哪张图、验收看什么、不做什么、建议执行人（燕大同学或协商后的维护管理人）、依赖的空间和结构。细任务不得先于说明书。清单先写在说明书里，本单不 task-create。经 human:徐滕强 确认后，再由 coordinator 建单。
6. 图 KG-COMPLY-SDD-FLOW 与正文一致。

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-COMPLY-SDD-L01-详细设计说明书.md

Handoff：
agent-delivery/agent-handoffs/KG-COMPLY-SDD-L01.md
ponytail: N/A（定义/文档）
diagram_id: KG-COMPLY-SDD-FLOW
evidence 指向这份 handoff 和上面的主文。
handoff 写清：说明书路径、算法清单条数、细任务条数、空间是否已采用 STRUCT 结论、验收面是否已采用 ACCEPT 结论。然后 task-update-fields 填 evidence，task-update-status 到 integration。不要写「会签通过」，除非人已经会签。不要改成 done。

禁止：
- 在 STRUCT、ACCEPT 没有书面结论时写死空间名、验收叶子或细任务。
- 把唐绍祖「跑出结果」、燕大「入图可复用 / 后台接口」两条主责改派给别人。
- 替燕大写图、写 nGQL、选定后台仓库并开始实现。
- 把技术点并进七要素「技术」，或给技术点新编必须边。
- 把不建的边写上，或猜待确认的边。
- 把 GDF 正式加工、WBS-07-00G / 00H 写成本期要交付。
- 重开已签收的 KG-7ELEM-BUILD-REQ-L01 至 L05。
- task-create 新叶，或修改本任务以外的 depends_on、状态、DoD。
- 密码、连接串、API Key 写入 git。
```
