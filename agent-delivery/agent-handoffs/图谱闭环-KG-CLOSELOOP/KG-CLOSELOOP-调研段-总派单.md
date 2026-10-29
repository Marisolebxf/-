# KG-CLOSELOOP · 调研段总派单

> 总控：[`KG-CLOSELOOP-长任务总控.md`](./KG-CLOSELOOP-长任务总控.md)  
> 监管人：`human:淮政玮`  
> 认领：`coordinator_dispatch`，`lock_hours=24`，后续不必再问  
> 仓：`gkx-orchestration`，分支 `dev`。只写文档。完工停在本地，不自行 commit / push，除非该叶 `/goal` 写了「完工即推」。  
> 强度：定义轨，ponytail N/A。禁止用压缩摘要代替精读总控和点名材料。

查询任务只用 MCP `task-get` / `task-query`。禁止读 `task-registry.yaml`。

凭据不落盘。环境地址可以写，密钥不写。

---

## 第一波（四叶并行，文件互斥）

### KG-CLOSELOOP-R01

```text
/goal architect-agent
身份：架构师。本叶只核对燕大平台上的上图事实，不写代码，不改技术方案.md。

任务：KG-CLOSELOOP-R01
标题：燕大七要素上图写侧：抽取链能否跑通
监管人：human:淮政玮
执行：agent:architect-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md

必读：
- 总控 §0、§3、§4、§5
- 工程过程/04-系统集成/07-图数据库集成/对接文档/对端/2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md
- 同目录 对接文档/我方/SYSINT-SCHEME-07-L04-燕大七要素上图对照.md
- 同目录 纪要/2026-10-21-七链图谱构建专题会.md
- 同目录 进度.md 里「仍需燕大书面回复」
- 对接文档/我方/SYSINT-SCHEME-07-L02-对齐轴.md（只用于实体名字对齐）

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R01.md
七要素各一行：源表、TAG、EDGE、抽取脚本是否绑定、测试环境能否跑通一条、卡在哪。
政策、服务机构单独写「还不能闭环」的原因。
写侧能力分列：Schema、构建、审核、删除/修改。10-21 说未开放的，保持未开放，不要写成已经能改点。
第一刀推荐写死一个要素，并写明为什么不是政策、为什么先避开 Organization 默认桶。默认识别论文（Paper），若证据相反再改推荐，改的理由写在文内。
不调用需要密钥的接口。环境不通就写「还没有实测」，禁止编造成功响应。

DoD：
1. 七要素上图表齐全，空着的格子写「还没有」。
2. 写侧四项能力各有开放/未开放/只有快照没有实测。
3. 第一刀要素只有一个，附否决政策的理由。
4. handoff 含 ponytail: N/A。task-update-status 到 ready_to_sign。不写会签通过。不标 done。
```

### KG-CLOSELOOP-R02

```text
/goal data-agent
身份：数据。本叶只核对我方哪一层数据能被燕大抽取链吃进去。不配 GDF 作业，不改库。

任务：KG-CLOSELOOP-R02
标题：我方数据出口能否喂燕大上图
监管人：human:淮政玮
执行：agent:data-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md

必读：
- 总控 §4、§5 第 8、12 条
- 工程过程/04-系统集成/06-GDF数据治理集成/对接文档/工程侧/2026-10-26-要素指标加工与图谱拆解思路.md
- 07 对接文档/我方/SYSINT-SCHEME-07-L03-算法中台上图台账.md
- 对端七要素快照里各 TAG 的源表列（只抽和七要素相关的表）
- GDF-POLICY-MDC-DOC-L01 的 handoff 或派单包里 Graph 段（有则引用，无则写还没有）

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R02.md
每个要素一行：我方表（ODS/DWD/ADS 写明层级）、燕大抽取用的表、字段能对上的比例或「还没有逐列核对」、VID/业务键是否一致、结论是可喂 / 不能喂 / 还没有派单包。
三条上图路径分列现状：GDF {要素}-Graph、我方 nebula loader、燕大抽取链。本叶不选定生产路径，把选择所需的事实交给 R03。
人才、科研机构若只有代码没有灌数证据，写未验证，不写成可喂。

DoD：
1. 七要素各有可喂/不能喂/还没有。
2. VID 与业务键不一致的地方点名。
3. 不新增 GDF 作业，不改表。
4. handoff 含 ponytail: N/A。状态到 ready_to_sign。不标 done。
```

### KG-CLOSELOOP-R04

```text
/goal algorithm-agent
身份：算法。本叶只整理燕大查询和分析接口的可调用程度。不实现算法，不写 nGQL 生产查询。

任务：KG-CLOSELOOP-R04
标题：燕大查询与分析接口可调用契约
监管人：human:淮政玮
执行：agent:algorithm-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md

必读：
- 总控 §3 第 1、4 条，§5 第 5、6、7、14 条
- 07-图数据库集成/README.md 测试环境与九类查询
- 07-图数据库集成/沟通流水.md
- 07-图数据库集成/进度.md 的 Q-KG 表
- 需求清单里的 31 项计算能力与九条读接口（KG-01～KG-09，路径以 06d 字段级需求为准，只作我方需求，不当成燕大已实现）
- srs/07 九个叶子只作招标对照

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R04.md
每条能力一行，状态只允许：可调用 / 仅有样例 / 还没有契约。
列：名称、对方路径或 nGQL 与否、鉴权方式（不写密钥）、限额与截断（没有写还没有）、对应我方哪类页面或指标（不知道就写还没有）。
Q-KG 未书面回复的单列，禁止改写成已确认。
PageRank、Louvain、Degree 以「作业已跑通」和「在线接口可调用」分开写。两者不是一回事。

DoD：
1. 读端点、九类查询、已知图算法作业都进表。
2. 样例与契约分开。
3. 未回复的 Q-KG 保留未回复。
4. handoff 含 ponytail: N/A。状态到 ready_to_sign。不标 done。
```

### KG-CLOSELOOP-R05

```text
/goal product-agent
身份：产品。本叶列专题系统和展示系统里图谱展示和相关指标要消费什么。不改页面，不新造口径。

任务：KG-CLOSELOOP-R05
标题：专题与展示的图谱消费清单
监管人：human:淮政玮
执行：agent:product-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md §6.3

必读：
- 总控 §6.3
- 07-图数据库集成/技术方案.md §5.1（未登记的保持还没有，本叶补登记到自己的 handoff，不改技术方案.md）
- 展示详设 08-功能-科技知识图谱.md 的 DS-21～DS-24
- 专题侧至少点名：产业链、企业、服务、政策、人才页上的图。没打开的页面写还没有

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R05.md
四列：页面、图上展示什么、走燕大接口 / 自研算法 / 页面关系图（G6、ECharts）/ 只读 ADS、归本闭环还是排除。
统计数字旁要能挂上的 metric_id 写上；没有就写还没有，禁止临时编号。
CMS overlay 标明排除。第 3 项不碰 Nebula 的图标明排除。
第一刀建议只保留一条展示或专题路径，其余写后续。选择理由写出来。

DoD：
1. 展示四页和专题五个点名对象都有行。没看到的写还没有。
2. 排除项有排除理由。
3. 不改技术方案.md，不改指标 seed。
4. handoff 含 ponytail: N/A。状态到 ready_to_sign。不标 done。
```

---

## 第二波

### KG-CLOSELOOP-R03

依赖：`KG-CLOSELOOP-R01`、`KG-CLOSELOOP-R02` 已有 handoff，状态 ≥ ready_to_sign。

```text
/goal architect-agent
身份：架构师。本叶只给图空间唯一落点的建议。不改空间，不改技术方案.md。

任务：KG-CLOSELOOP-R03
标题：生产图空间唯一落点建议
监管人：human:淮政玮
执行：agent:architect-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md §5 第 1 条

必读：R01、R02 handoff；architecture-baseline 里 Nebula 那条；技术方案.md 里 demo_gkx_chain 的段落（只读）；E-PLATFORM-P0-TRSGRAPH-L01 的任务说明（MCP task-get）。

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R03.md
列出现有空间：demo_gkx_chain、gkx_policy、gkx_local_1、gkx_full_1，各是谁在写、能不能当生产。
给一个推荐：第一刀读和写落在哪一个空间。双写生产禁止。
另外两条上图路径写成停用或只作对照。
推荐若要改掉 L01 锁的 demo_gkx_chain，写成「待授权人确认」，本叶不改 L01。

DoD：
1. 四个空间都有归宿。
2. 推荐只有一个生产空间。
3. 不执行切换。
4. handoff 含 ponytail: N/A。状态到 ready_to_sign。不标 done。
```

### KG-CLOSELOOP-R06

依赖：`KG-CLOSELOOP-R04` 已有 handoff，状态 ≥ ready_to_sign。

```text
/goal algorithm-agent
身份：算法。本叶划分哪些计算用燕大、哪些必须自研。不写实现代码。

任务：KG-CLOSELOOP-R06
标题：自研算法与燕大分析接口的边界
监管人：human:淮政玮
执行：agent:algorithm-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md §3 第 5 条

必读：R04 handoff；L05 里计算能力差集；需求清单 31 项计算。指标是否已有 metric_id 用 MCP metric-registry 查，禁止通读 metrics/registry 种子 YAML。查不到写还没有。

产出：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-R06.md
31 项各归一类：燕大在线可调用 / 只有离线作业 / lumen-algo-py 自研 / 不做。
自研行必须有 metric_id，或者写明还没有身份证、因此第一刀不做。
Java 不出现在实现列。时序类在图快照空白时归「不做」。

DoD：
1. 31 项都有归类。归不进去的写还没有对应项。
2. 自研清单是短名单，每条有 metric_id 或明确不做。
3. 不写算法代码。
4. handoff 含 ponytail: N/A。状态到 ready_to_sign。不标 done。
```

---

## 第三波

### KG-CLOSELOOP-SCHEME-L01

依赖：R03、R05、R06 已有 handoff，状态 ≥ ready_to_sign。R01、R02、R04 的结论经这三份带入，不再单列依赖。

```text
/goal doc-agent
身份：技术文档。定义完整性优先。禁止用 ponytail 删章节。

任务：KG-CLOSELOOP-SCHEME-L01
标题：七要素上图与图谱消费实施方案
监管人：human:淮政玮
执行：agent:doc-agent
仓：gkx-orchestration，分支 dev
总控：agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-长任务总控.md

必读：总控全文；R01～R06 六份 handoff；07/技术方案.md 只为列出「相对 L01 的范围变更」，不改该文件。

产出：
- agent-delivery/工程过程/04-系统集成/07-图数据库集成/实施方案.md
- agent-delivery/agent-handoffs/图谱闭环-KG-CLOSELOOP/KG-CLOSELOOP-SCHEME-L01.md

实施方案章节至少包括：
1. 两项目标各一条可执行步骤。第一刀限制在一个要素、一个图空间、一条页面。步骤写到谁做、在哪做、怎样算通过。目标两周内能开工，不写没有负责人的平台建设。
2. 智树 / 燕大工作边界定稿。总控 §4 的草案被证据改掉的地方逐条说明。
3. 总控 §5 的 15 件事逐条给结论或「待拍板」。待拍板不得超过总控点名的两件，除非新发现结构歧义。
4. 相对 SYSINT-SCHEME-07-L01 的范围变更清单。标明 L01 在签收前仍然有效的句子（调用链、501、禁止假图）。
5. 风险：环境、Policy TAG、Organization 混装、双空间、凭据、未回复的 Q-KG。
6. 明确不做什么：不派开发叶、不改图空间、不嵌管理界面、不在本叶把方案标 done。

DoD：
1. 实施方案.md 六节都在。没有证据的句子写还没有，禁止补造。
2. 第一刀只有一个要素、一个空间、一条页面。
3. 工作边界是表，不是口号。
4. handoff 含 ponytail: N/A，evidence 指向上述两个路径。状态到 ready_to_sign。不写会签通过。不标 done。不 task-create 开发叶。
```
