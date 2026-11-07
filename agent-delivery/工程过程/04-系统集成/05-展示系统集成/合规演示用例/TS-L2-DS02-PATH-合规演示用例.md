# TS-L2-DS02-PATH · 展示关键路径和关键节点 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技发展态势 · 科学技术全景（`/trend/tech-panorama`）
- 需规序号：28–33（需规二级「展示关键路径和关键节点」）
- 需规全文：`agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md`
- 设计：`agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/科学技术全景-系统详细设计说明书.md` §2.3；`sdd/l2/TS-L2-DS02-PATH-API.md`（字段名以它为准）、`sdd/l2/TS-L2-DS02-PATH-DATA.md`
- 任务：`TS-L2-DS02-DEMO-CASE-L01`（`qa-agent`，监管 `human:淮政玮`）
- 日期：2026-11-07
- 调度核对：见文末

历史测试记录 `测试用例/TS-L2-DS02-TEST-L01.md`（当时路径区为空态）保持原文件，不改写成期望。

## 需规摘录

| 序号 | 名称 | 需规功能描述（原文） |
|---|---|---|
| 28 | 关键路径数据接收与处理 | 系统能够接收后端分析得出的关键路径数据，包括路径上的技术节点序列、节点间的关联关系以及路径的重要性指标。数据以结构化格式传输，系统自动解析并整合到现有技术知识图谱中。 |
| 29 | 关键节点识别与标记 | 根据节点的重要性指标（如中心度、影响力）自动识别关键节点，并在图谱中以特殊样式进行标记，如放大节点、改变颜色或添加特殊图标，使其在视觉上与其他节点区分开来。 |
| 30 | 路径详情查看 | 用户点击关键路径上的任意节点或连线，可查看该路径的详细信息，包括路径的技术意义、发展历程、关键突破点。详情以弹窗或侧边栏形式展示，不影响整体图谱的查看。 |
| 31 | 关键路径筛选与过滤 | 提供关键路径筛选器，用户可按路径类型、重要性级别、时间范围等条件筛选显示关键路径。支持多条件组合筛选，满足不同分析需求。 |
| 32 | 路径比较分析 | 支持同时选择多条关键路径进行对比分析，系统以并排或重叠方式展示多条路径，帮助用户理解不同技术发展路径的异同点和关联性。 |
| 33 | 关键路径动态演示 | 提供关键路径的动态演示功能，按时间顺序展示技术发展路径的形成过程。用户可控制演示速度，暂停或继续演示，便于理解技术发展的历史脉络。 |

需规公共描述（excel_row 20）：支持按时间轴显示技术领域关键实体之间关联关系的科学技术全景图、技术知识图谱中技术点关联相关的关键实体排名展示。

## 取数

- 时间：2026-11-07 19:58–20:00。途径同 `TS-L2-DS02-GRAPH-合规演示用例.md`「取数」：跳板机 `kubectl exec` 进 `lumen-platform-algo-py` pod，`POST 127.0.0.1:8000/internal/tech-graph/read`；分数表只读 `SELECT`。本机没有展示系统 token，**没有打网关**。期望里的数当日取自 Python 读图与库，网关一跳由 LOOP 首探核对。
- `TS-L2-DS02-SCORE-L01` 灌数时图上还没有 `tech_path_step`。当日读图已能读到路径步（见下表），但分数表仍没有 `path_priority` 行。
- 已知断点：选中点经 Java 以 `techPointId` 下发，Python 不认，网关当前返回 `keyPathOptions=[]`。修复单 `TS-L2-DS02-SEL-FIX-L01` 未做。依赖选中点的行加脚注 ¹。

| 读法（pod 内请求体） | 结果 |
|---|---|
| `{"space":"demo_gkx_chain"}`（未选点） | `keyPathOptions` 0。`nodes` 200，每点有 `role`、`strength`。首三点：`tcn_000f21ac06aceb9cdd0575e82d0d85fc` CORE 36.98626428；`tcn_008a8b3f1dd54fcac52ebcb2ca81e160` BRIDGE 4.67151915；`tcn_00a4d448b5cf18dc94a224e384220ab9` BRIDGE 2.69469638 |
| `{"space":"demo_gkx_chain","technology_node_id":"tcn_000f21ac06aceb9cdd0575e82d0d85fc"}` | `keyPathOptions` 2，`truncated.paths=false` |
| 同上，第 1 条路径 | `id` `tep_8392b7f8d44d14cae932645cd242f5bd`，`rank` 1，`name`「暴食症的临床视角 → 神经性厌食症治疗的临床视角 → 神经性厌食症的临床并发症」，`summary` 空串。`stageIds`：`tcn_061a17b4051d92288f0d4710db5e304a`、`tcn_000f21ac06aceb9cdd0575e82d0d85fc`、`tcn_aa67ddbee470e617c056728a8bfd376f`。`nodes[0]`「暴食症的临床视角」CORE，`strength` 38.37885702，`stageKey` "0"，`typeKey` technology，`timeLabel` 空 |
| 同上，第 2 条路径 | `id` `tep_6cddc27aa4e88a50756093fd6d76ef86`，`rank` 2，`name`「暴食症的临床视角 → 神经性厌食症治疗的临床视角」，两步 |
| `{"space":"demo_gkx_chain","technology_node_id":"tcn_008a8b3f1dd54fcac52ebcb2ca81e160"}` | `keyPathOptions` 1：`tep_981d5e3d4e7c7f13fe3ce7d5ed09bb95`「肥胖中的炎症与代谢功能障碍 → 膳食脂肪摄入与神经健康」，两步 |
| 同上，`techPointId` 代替 | `keyPathOptions` 0（断点） |
| 分数表 `GROUP BY score_kind` | `centrality` 19430，`influence` 252363，**`path_priority` 0 行** |
| 分数表 `centrality` 抽查 | `tcn_000f21ac…` 41.292，`tcn_008a8b3f…` 48.805，`tcn_00a4d448…` 43.136 |

## 覆盖表

接口地址一律写展示网关。请求体按页面 `graphReadParams` 实发字段写（`timeRange` Java 不读，省略）。32、33 在页面内完成，不另发请求。

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 28 关键路径数据接收与处理 · 节点序列 | 科学技术全景 · 关键路径区 | 点「神经性厌食症治疗的临床视角」 | 点节点即重发 `graph` | `POST /display/v1/situation/panorama/graph` | `{"selectedFieldValues":[],"currentYear":null,"selectedNodeId":"tcn_000f21ac06aceb9cdd0575e82d0d85fc"}` | HTTP 200，七个字段齐。`keyPathOptions` 2 条：`tep_8392b7f8d44d14cae932645cd242f5bd`（`rank` 1，三步）与 `tep_6cddc27aa4e88a50756093fd6d76ef86`（`rank` 2，两步）。每条有 `id`、`name`、`stageIds`、`nodes[]`（`id`、`name_zh`、`role`、`stageKey`）、`relationIds`（设计固定 `[]`）、`pathPriority` 键。路径只带与选中点直接相连的步（PATH-ARCH 遗留 2） | 可演 ¹ |
| 28 关键路径数据接收与处理 · 重要性指标 | 同上 | 同上 | 同上 | 同上 | 同上 | 两条路径 `pathPriority` 为 `null`，不编优先级 | 覆盖不到：缺路径优先级分数行（`ads_technology_panorama_score` 无 `path_priority`） |
| 29 关键节点识别与标记 | 科学技术全景 · 图谱区 | 打开页面，不选点 | 页面加载 | 同上 | `{"selectedFieldValues":[],"currentYear":null,"selectedNodeId":null}` | HTTP 200。`nodes` 每点有 `role`（CORE / BRIDGE 等）与 `strength`，页面据此放大、变色。`centrality` 由 Java 按编号叠加分数表：`tcn_000f21ac…` 41.292、`tcn_008a8b3f…` 48.805、`tcn_00a4d448…` 43.136；无行为 `null`。D4=mock，带 MockBadge | 可演 |
| 30 路径详情查看 · 步序与端点 | 关键路径区 → 详情侧栏 | 在第 28 行结果里点路径 `tep_8392b7f8…` | 点路径，不另发请求 | 同上（读第 28 行那次返回） | 同第 28 行 | 侧栏按 `stageKey` 列三步：「暴食症的临床视角」→「神经性厌食症治疗的临床视角」→「神经性厌食症的临床并发症」，各带 `role`。不挡整图 | 可演 ¹ |
| 30 路径详情查看 · 技术意义、历程、突破 | 同上 | 同上 | 同上 | 同上 | 同上 | `summary` 空串，不编正文 | 覆盖不到：缺路径技术意义、发展历程、关键突破正文 |
| 31 关键路径筛选与过滤 | 关键路径区筛选器 | 路径类型、重要性档、时间范围任选 | 页面内筛 | 同上（读第 28 行那次返回） | 同第 28 行 | 不编类型、档位和年份。类型条件不截数据；选了重要性档，两条路径都因 `pathPriority=null` 不进档 | 覆盖不到：缺路径类型字段（无 `pathType` / `typeKey`）；缺 `path_priority` 分数行；缺年份（`timeLabel` 空，`timeline` 空） |
| 32 路径比较分析 | 关键路径区比较 | 在第 28 行结果里勾选两条路径 | 页面内比较，不发请求 | 无 | 无 | 用第 28 行那次返回的两条路径并排或重叠：共有「暴食症的临床视角」「神经性厌食症治疗的临床视角」两步，`tep_8392b7f8…` 多一步「神经性厌食症的临床并发症」 | 可演 ¹ |
| 33 关键路径动态演示 | 关键路径区播放 | 选路径 `tep_8392b7f8…`，点播放，再暂停、继续、调速 | 页面内计时，不发请求 | 无 | 无 | 按 `nodes[]` 顺序逐步推进三步，可播放、暂停、继续、调速、重置。按步播放，不按年份换图（说明书 §2.3） | 可演 ¹ |

¹ 数据在库：pod 内用 `technology_node_id` 能读到。经网关时 Java 以 `techPointId` 下发，Python 不认，当前网关返回 `keyPathOptions=[]`。这是查询缺口，挂 `TS-L2-DS02-SEL-FIX-L01`，不派补数。

## 一条主路径

只串可演行。28 的重要性、30 的正文、31 不进入。条件不另做排列组合。

1. 序号 29：打开 `/trend/tech-panorama`，不选点。图上 CORE 与 BRIDGE 节点样式不同；「神经性厌食症治疗的临床视角」中心度 41.292（带 Mock 角标）。
2. 序号 28：点「神经性厌食症治疗的临床视角」。请求带 `selectedNodeId=tcn_000f21ac06aceb9cdd0575e82d0d85fc`。路径区出现 2 条：`tep_8392b7f8…`（三步）、`tep_6cddc27a…`（两步）。
3. 序号 30：点 `tep_8392b7f8…`。侧栏列出三步端点名称。
4. 序号 32：勾选两条路径比较，共有前两步，第一条多一步。
5. 序号 33：选 `tep_8392b7f8…` 播放，暂停、继续、调速。

第 2–5 步依赖选中点一跳，待 `TS-L2-DS02-SEL-FIX-L01`。

## 调度核对

需规 28–33 各有至少一行。可演 5 行（28 节点序列、29、30 步序与端点、32、33）。覆盖不到 3 行（28 重要性、30 正文、31）。设计无资源 0 行。可演行中 28、30、32、33 依赖选中点一跳（脚注 ¹）。主路径只串可演行。本文不建演示样本循环，不派数据单，不派算法单。
