# 派单说明 · KG-GRAPH-TRIPLE-03（包 C · 燕大 · 专题三域图谱三元组）

> 2026-11-13。淮政玮派。P1，第二批（11-20 起）。**这六个叶子是专题系统唯一完全没有派单的部分**，而它们要的数据**早就在图里**（合规入图 T02/T03/T04 灌的），不需要重新灌。
> 一句话：照产业服务域（SVC）那套「四步走」范式，把技术链、人才、科研机构三域的 `/internal` 接口和页面各做一遍。

```text
/goal frontend-agent
身份：你是熟悉本仓图谱三元组闭环范式的工程师。本单按已跑通的 SVC 范式执行，叶内四步 data→algo→api→frontend，不跳步。禁止用 ponytail 删减 op_id，禁止用 headroom compress 代替精读 SVC 的 pipeline-to-nebula.md。

任务：KG-GRAPH-TRIPLE-03
标题：专题三域图谱三元组（技术链 104/105 · 人才 110/111 · 科研机构 114/115）
Epic：E-SCI-INT
优先级：P1
类型：feature
负责人：human:宋飞扬（监管 human:徐滕强）。claimed_by=human:宋飞扬 或 agent:frontend-agent，supervised_by=human:徐滕强。
状态：ready。依赖 KG-GRAPH-COVER-01（技术链的关联机构依赖机构边补满）。
仓：gkx-orchestration（契约与 storage 文档）+ lumen-algo-py（Python /internal）+ lumen-svc-platform（Java 透传）。前端在 lumen-ui-topic。
完成日期要求：2026-11-25（P1 窗口，不得晚于 S6 培训）。

强度：medium。

前置事实（已实测，直接采信）：
- tech_point VID = `tp:<technology_node_id>`，19,430 点；tech_rel 541,428 条；tech_has_paper 108,337、tech_has_patent 172,644、tech_has_person 111,578、tech_has_institution 51,000（A 包补至 ≥95%）。
- person VID = `person:<id>`，100,000 点；M01 cooperate 2,525,789、M04 belong 72,099。
- research VID = `inst:<id>`，83,745 点；M02 cooperate 3,442,271、M08 participate 17,426。
- 服务机构 VID 是 `institution:<id>`，科研机构是 `inst:<id>`，两者前缀不同，**极易写错，必须按本单写**。
- 图空间 demo_gkx_chain，只读消费；本单不灌新数据、不建新边、不改 schema。

目标：三域各有 `/v1` + `/internal/*` 成对接口，Java 只透传，UI 有三档（正常/空态/501）与每 op_id 的 apiview 记录，页面可点。

范围（三域 × 四步，逐域交付）：

一、技术链 104/105（`/internal/tech/graph*`）
1. A 技术点本体：检索（关键词/名称）、详情（name_zh/name_en/community_role/weighted_degree/community_id）。
2. B 技术-技术关系：邻居、子图（≤2 跳）、边型 tech_rel 带 weight 与 confidence。
3. C 技术-四类关联：论文（tech_has_paper）、专利（tech_has_patent）、人才（tech_has_person）、机构（tech_has_institution）。**关联机构在 A 包补满前只出已有部分，页面按「数据正在补充中」明示，不许假装为空。**
4. D 浏览：按社群/角色/度数排序的浏览列表。

二、人才 110/111（`/internal/person/graph*`）
1. A 人才本体：检索、详情（姓名/机构/领域若 props 有）。
2. B 人才-人才合作：合作邻居、合作子图（M01，无向，去重后 2,525,789）。
3. C 人才-机构归属：belong（M04，72,099）。
4. D 浏览：按合作度排序的人才榜（可分页）。

三、科研机构 114/115（`/internal/research/graph*`）
1. A 机构本体：检索、详情。
2. B 机构-机构合作：M02 合作邻居/子图（无向去重）。
3. C 机构-项目承担：M08 participate（17,426）。
4. D 浏览：按合作度排序的机构榜。

四、四步规矩（照 SVC 范式，不另创）
1. 步 1 storage：新建 `storage/TECH/etl/pipeline-to-nebula.md`、`storage/PERSON/etl/pipeline-to-nebula.md`、`storage/RESEARCH/etl/pipeline-to-nebula.md`，与 `storage/SVC/etl/pipeline-to-nebula.md` 同构；每个 op_id 写入参/出参；diagram_id 分别为 TECH-GRAPH-TRIPLE / PERSON-GRAPH-TRIPLE / RESEARCH-GRAPH-TRIPLE。**步 1 文档未齐，禁止写 Python。**
2. 步 2 Python：出 `/v1/*` 与 `/internal/*` 成对；全部 `dry_run`；禁止按名称猜 VID（必须按 id 前缀拼）。
3. 步 3 Java：网关 graph 路由必须插在 catch-all 之前；Feign 指对应域 Python；禁止 catch-all 直连 Python 写图。**`/internal` 未齐，禁止动 Java。**
4. 步 4 UI：每域页面四档（正常/空态/501/不可用）+ apiview 每 op_id；请求一律打 Java 网关，source=demo_gkx_chain。**网关未插 Java，禁止接线 UI。**

五、与在途任务的关系（不得重复）
- 产业链 102/103 已有 `DEMO-CHAIN-GRAPH-TRIPLE-UI-L01`，政策 106/107 已有 `DEMO-POLICY-GRAPH-TRIPLE-UI-L01`，企业 108/109 已有 `DEMO-ENT-GRAPH-TRIPLE-UI-L01`，产业服务 112/113 已有 `DEMO-SVC-GRAPH-TRIPLE-UI-L01`，综合 116 已有 `DEMO-COMP-GRAPH-TRIPLE-UI-L01`。**本单只做 104/105、110/111、114/115，不碰以上任何一张单的文件与路由。**

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-TRIPLE-03-三域三元组.md
各域 op_id 清单、契约表、curl 记录同目录。

Handoff：
agent-delivery/agent-handoffs/KG-GRAPH-TRIPLE-03.md
写清：三域 op_id 条数、三份 storage 文档路径、经网关 curl 结果、diagram_id、未完成项。
evidence 指向主文。task-update-status 到 integration，不写 done。

禁止：
- 灌新数据、建新边、改 schema、建第二空间。
- 照名称拼 VID（research 是 `inst:`，服务机构是 `institution:`，写错必查不出）。
- 抢先改 CHAIN/POLICY/ENT/SVC/COMP 五张单的文件或路由。
- 跳过步 1 直接写 Python，或跳过 `/internal` 直接接 UI。
- 把口令、连接串写进 git。
```

---

## 附：为什么这三域能快

这三域不是我方新造的需求，是需规 102–115 里本来就有的七个维度中的三个。**合规入图已经把它们的数据灌进 `demo_gkx_chain` 了**（人才 10 万点、机构 8 万点、技术点 1.9 万点，合作边 596 万条），只是没接口、没页面。照着 SVC 的现成范式走一遍，比从零做一域快得多。
