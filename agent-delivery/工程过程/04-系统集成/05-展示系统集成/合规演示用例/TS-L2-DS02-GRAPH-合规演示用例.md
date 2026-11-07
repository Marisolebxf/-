# TS-L2-DS02-GRAPH · 展示技术点图谱 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技发展态势 · 科学技术全景（`/trend/tech-panorama`）
- 需规序号：17–21（需规二级「展示技术点图谱」）
- 需规全文：`agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md`
- 设计：`agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/科学技术全景-系统详细设计说明书.md` §2.1；`sdd/l2/TS-L2-DS02-GRAPH-API.md`（字段名以它为准）、`sdd/l2/TS-L2-DS02-GRAPH-DATA.md`
- 任务：`TS-L2-DS02-DEMO-CASE-L01`（`qa-agent`，监管 `human:淮政玮`）
- 日期：2026-11-07
- 调度核对：见文末

历史测试记录 `测试用例/TS-L2-DS02-TEST-L01.md` 保持原文件，不改写成期望。

## 需规摘录

| 序号 | 名称 | 需规功能描述（原文） |
|---|---|---|
| 17 | 技术点图谱数据输入 | 支持用户通过多种方式输入技术点图谱数据，包括手动输入、文件导入（如Excel、JSON格式）。用户可设置技术点的名称、属性、层级关系等基本信息，系统自动解析并构建数据结构。 |
| 18 | 图结构自动生成 | 系统根据输入的技术点数据，自动计算节点间的关联关系，生成可视化的图结构技术点图谱。图谱中技术点以节点形式展示，技术间关系以连线形式表示，不同层级或类型的技术点可通过不同颜色、形状进行区分。 |
| 19 | 图谱交互操作 | 支持用户对生成的技术点图谱进行多种交互操作，包括缩放、平移、旋转等基本操作，以及节点拖拽调整、展开/折叠子节点、高亮显示特定路径等高级操作，方便用户从不同角度查看技术结构。 |
| 20 | 技术点搜索定位 | 提供技术点搜索功能，用户可通过关键词快速定位到图谱中的特定技术点。搜索结果支持模糊匹配和精确匹配，定位到的技术点会在图谱中高亮显示并自动居中。 |
| 21 | 技术点详情查看 | 用户点击图谱中的技术节点，可查看该技术点的详细信息，包括技术名称、描述、属性参数、发展状态。详情信息以弹窗或侧边栏形式展示，不影响整体图谱的查看。 |

需规公共描述（excel_row 20）：支持按时间轴显示技术领域关键实体之间关联关系的科学技术全景图、技术知识图谱中技术点关联相关的关键实体排名展示。

## 取数

- 时间：2026-11-07 19:58–20:00（第二笔脚本打印 `2026-11-07 20:00:00`）。
- 途径：SSH MCP 连跳板机 `10.50.69.111`，`kubectl exec` 进 `zhipu-tts/lumen-platform-algo-py-c6cb87d4-m68p9`，在 pod 内 `POST http://127.0.0.1:8000/internal/tech-graph/read`。只读，不写图。临时 kubeconfig 用完已删。
- 本机没有展示系统 token，**没有打网关**。下面期望里的数，当日取自 Python 读图与库，网关一跳由 LOOP 首探核对。
- 图空间 `demo_gkx_chain`。分数表 `demo_gkxlumenx_ads.ads_technology_panorama_score`，用 pod 内环境变量口令只读 `SELECT`（会话 `READ ONLY`），口令未打印、未落盘。
- 已知断点：页面发 `selectedNodeId`，Java 收下后以 `techPointId` 下发；Python 只认 `technology_node_id` / `technologyNodeId`。当日在 pod 内用 `techPointId` 打同一个点，返回与未选点相同（`nodes` 200、`relations` 0）。修复单 `TS-L2-DS02-SEL-FIX-L01` 未做。下表凡依赖「选中点」的行，数据情况仍按数据本身定，并加脚注 ¹。

| 读法（pod 内请求体） | 结果 |
|---|---|
| `{"space":"demo_gkx_chain"}`（未选点、无搜索字） | HTTP 200，`code=0`。`nodes` 200，`truncated.nodes=true`。`relations` 0，`relationTypeOptions` 0，`listRecords` 0，`keyPathOptions` 0。`factorItems` = `[{key: technology, label: 技术点}]`。无 `emptyReason`。`timeline` 各项为空 |
| 同上，首个点 | `tcn_000f21ac06aceb9cdd0575e82d0d85fc`「神经性厌食症治疗的临床视角」，`name_en` 空，`role` CORE，`strength` 36.98626428。点上键只有 `factorKey`、`id`、`label`、`name`、`name_en`、`name_zh`、`role`、`strength`、`type` |
| 同上，第二、三个点 | `tcn_008a8b3f1dd54fcac52ebcb2ca81e160`「膳食脂肪摄入与神经健康」BRIDGE 4.67151915；`tcn_00a4d448b5cf18dc94a224e384220ab9`「植物角质层蜡生物合成与功能」BRIDGE 2.69469638 |
| `{"space":"demo_gkx_chain","keyword":"人工智能"}` | `nodes` 190，未截断。前三：`tcn_fceeb0c7b63570598a7fdeb86f709159`「以人为中心的人工智能协作框架」、`tcn_e42a7a9e8cc6a344f98c021fd2b9a784`「人工智能的伦理与认知维度」、`tcn_ba8b61671c5a1344acefbc986cb110f8`「面向数据可视化的人工智能」 |
| `{"space":"demo_gkx_chain","keyword":"深度学习"}` | `nodes` 140 |
| `{"space":"demo_gkx_chain","keyword":"不存在的词zzq"}` | `nodes` 0，`emptyReason=GRAPH_EMPTY` |
| `{"space":"demo_gkx_chain","technology_node_id":"tcn_000f21ac06aceb9cdd0575e82d0d85fc"}` | `nodes` 263（Python 截断标记 `nodes=true`），`relations` 65，`relationTypeOptions` 3：`CO_EVOLUTION`、`KNOWLEDGE_DEPENDENCY`、`PATENT_CONVERGENCE`。`relations` 无 `year`，`timeline.years`、`events` 为空 |
| 同上，`relations` 前两条 | `tcn_000f21ac…` → `tcn_b48b0e2e926c61831d08f279dbab7d8f`，`CO_EVOLUTION`，`evidenceLevel` MEDIUM，`weight` 38.617068；→ `tcn_942399f999b7a2e564b2e3a1a564ccde`，`CO_EVOLUTION`，MEDIUM，46.950401 |
| `{"space":"demo_gkx_chain","techPointId":"tcn_fceeb0c7…"}` | 与未选点相同：`nodes` 200，`relations` 0，`listRecords` 0，`keyPathOptions` 0。证实断点 |
| 分数表 `GROUP BY score_kind` | `influence` 252363，`centrality` 19430，无 `path_priority` |
| 分数表 `subject_id='tcn_000f21ac…'` | `centrality` 41.292 |

## 覆盖表

接口地址一律写展示网关。请求体按页面 `graphReadParams` 实发字段写：`selectedFieldValues`、`timeRange`（Java 不读，本表省略）、`currentYear`（固定 `null`）、`keyword`（空则不发）、`selectedNodeId`。期望写展示接口应出现的七个字段（`nodes`、`relations`、`keyPathOptions`、`timeline`、`listRecords`、`relationTypeOptions`、`factorItems`）与当日事实值。

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 17 技术点图谱数据输入 | 科学技术全景 · 图谱区 | 手动录入或导入 Excel / JSON | 本页无录入入口 | `POST /display/v1/situation/panorama/import`（`.../manual` 同） | 任意体 | HTTP 501，`code=1`，`data=null`，`msg`「序号 17 不在本页写入」。不调读图，不落库。`graph` 带 `action=import` 等写入动作时同样 501 | 设计无资源（说明书 §2.1：点由第 2 项写入，本页不收输入） |
| 18 图结构自动生成 · 节点 | 科学技术全景 · 图谱区 | 打开页面，不选领域，不填搜索，不选点 | 页面加载 | `POST /display/v1/situation/panorama/graph` | `{"selectedFieldValues":[],"currentYear":null,"selectedNodeId":null}` | HTTP 200，`code=0`，七个字段齐。`nodes` 200 个技术点（`type`=技术点，`factorKey`=technology），首个 `tcn_000f21ac06aceb9cdd0575e82d0d85fc`「神经性厌食症治疗的临床视角」`role` CORE。`role` 取 CORE / BRIDGE 等，用于区分样式。`relations=[]`、`relationTypeOptions=[]`（未选点恒空）。`factorItems` 只有「技术点」。`listRecords=[]`、`keyPathOptions=[]`。无 `emptyReason`。Python 侧 `truncated.nodes=true`，网关是否透出 `truncated` 由首探记录（API 分册 §6 记该标记可能丢） | 可演 |
| 18 图结构自动生成 · 连线与关系类型 | 同上 | 在画布上点「神经性厌食症治疗的临床视角」 | 点节点即重发 `graph` | 同上 | `{"selectedFieldValues":[],"currentYear":null,"selectedNodeId":"tcn_000f21ac06aceb9cdd0575e82d0d85fc"}` | HTTP 200。`relations` 65 条（Python 当日值），每条有 `source`、`target`、`relationType`、`evidenceLevel`、`weight`，无 `year`。`relationTypeOptions` 三项：`CO_EVOLUTION`、`KNOWLEDGE_DEPENDENCY`、`PATENT_CONVERGENCE`，用于区分连线。首条 `tcn_000f21ac…` → `tcn_b48b0e2e926c61831d08f279dbab7d8f`，`CO_EVOLUTION`，MEDIUM，`weight` 38.617068。`nodes` Python 返回 263，Java 上限 200，网关条数与截断标记由首探记录 | 可演 ¹ |
| 19 图谱交互操作 | 同上 | 缩放、平移、拖拽节点；点节点后展开邻居、高亮连线 | 页面内操作，不发请求 | 无 | 无 | 不发请求。缩放、平移、拖拽用第 18 行「节点」那次返回的 200 个点。展开邻居与高亮连线用第 18 行「连线」那次返回的 65 条 `relations`。高亮路径用 `TS-L2-DS02-PATH` 第 28 行的 `keyPathOptions`。旋转、折叠是画布能力，不依赖后端字段 | 可演 ¹（展开、高亮部分） |
| 20 技术点搜索定位 · 模糊 | 科学技术全景 · 搜索框 | 搜索框填「人工智能」 | 回车或点搜索 | 同上 | `{"selectedFieldValues":[],"currentYear":null,"keyword":"人工智能","selectedNodeId":null}` | HTTP 200。`nodes` 190 个，名称含「人工智能」（`name_zh` / `name_en` CONTAINS）。前三：`tcn_fceeb0c7b63570598a7fdeb86f709159`「以人为中心的人工智能协作框架」、`tcn_e42a7a9e8cc6a344f98c021fd2b9a784`「人工智能的伦理与认知维度」、`tcn_ba8b61671c5a1344acefbc986cb110f8`「面向数据可视化的人工智能」。`relations=[]`。高亮与居中在页面完成。无命中词（如「不存在的词zzq」）返回 200、`nodes` 空、`emptyReason=GRAPH_EMPTY`，不报 502 | 可演 |
| 20 技术点搜索定位 · 精确 | 同上 | 搜索框填全名「以人为中心的人工智能协作框架」 | 回车或点搜索 | 同上 | `{"selectedFieldValues":[],"currentYear":null,"keyword":"以人为中心的人工智能协作框架","selectedNodeId":null}` | HTTP 200。`nodes` 含 `tcn_fceeb0c7b63570598a7fdeb86f709159`，页面按名称等值把它定位、高亮、居中。条数不多于 190（该串含「人工智能」）。当日未单独打这一笔，条数由首探记录，不写死 | 可演 |
| 21 技术点详情查看 · 名称与属性参数 | 科学技术全景 · 详情侧栏 | 点「神经性厌食症治疗的临床视角」 | 点节点打开侧栏 | 同上 | 用第 18 行「节点」那次返回即可；点选后重发的请求同第 18 行「连线」 | 侧栏读 `nodes[]` 中该点：`name_zh`「神经性厌食症治疗的临床视角」，`name_en` 空（不抄英文），`role` CORE，`strength` 36.98626428（标「关系强度」），`centrality` 41.292（Java 按编号叠加分数表；D4=mock，带 MockBadge）。不挡整图 | 可演 |
| 21 技术点详情查看 · 描述与发展状态 | 同上 | 同上 | 同上 | 同上 | 同上 | 不编描述与发展状态 | 覆盖不到：缺技术点描述、发展状态字段。点上只有名称、角色、加权度，读图不返回这两项 |

¹ 数据在库：pod 内用 `technology_node_id` 能读到。经网关时 Java 以 `techPointId` 下发，Python 不认，当前网关会返回未选点形状（`relations` 空）。这是查询缺口，挂 `TS-L2-DS02-SEL-FIX-L01`，不派补数。

## 一条主路径

只串可演行。17 不进入，21 的描述与发展状态不进入。条件不另做排列组合。

1. 序号 18（节点）：打开 `/trend/tech-panorama`，不选领域、不填搜索。请求 `{"selectedFieldValues":[],"currentYear":null,"selectedNodeId":null}`。应看到 200 个技术点，`relations` 空，图例只有「技术点」。
2. 序号 19：在这张图上缩放、平移、拖拽一个节点。不发请求。
3. 序号 20（模糊）：搜索框填「人工智能」。应得到 190 个点，前三为「以人为中心的人工智能协作框架」「人工智能的伦理与认知维度」「面向数据可视化的人工智能」。
4. 序号 20（精确）：搜索框改填「以人为中心的人工智能协作框架」。该点被定位并居中。清空搜索框回到第 1 步的图。
5. 序号 21（名称与属性）：点「神经性厌食症治疗的临床视角」。侧栏显示中文名、`role` CORE、关系强度 36.98626428、中心度 41.292（带 Mock 角标）。
6. 序号 18（连线）与 19（展开、高亮）：同一次点击重发 `graph`，带 `selectedNodeId=tcn_000f21ac06aceb9cdd0575e82d0d85fc`。应出现 65 条连线、三种关系类型。¹ 待 `TS-L2-DS02-SEL-FIX-L01`。

## 调度核对

需规 17–21 各有至少一行。可演 6 行（18 节点、18 连线、19、20 模糊、20 精确、21 名称与属性）。覆盖不到 1 行（21 描述与发展状态，缺字段）。设计无资源 1 行（17，501）。可演行中 18 连线、19 依赖选中点一跳（脚注 ¹）。主路径只串可演行。本文不建演示样本循环，不派数据单，不派算法单。
