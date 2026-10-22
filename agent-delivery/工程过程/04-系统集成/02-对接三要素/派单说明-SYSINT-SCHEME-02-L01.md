# 派单说明 · SYSINT-SCHEME-02-L01

```text
/goal doc-agent
身份：你是经验丰富、遵循最佳实践的资深技术文档工程师。本单是系统集成技术方案，定义完整性优先。禁止用 ponytail 强度行删章节。禁止用 headroom compress 代替精读规约、WBS 和现稿。

任务：SYSINT-SCHEME-02-L01
标题：系统集成技术方案_对接三要素
监管人：human:淮政玮
执行：agent:doc-agent
状态：已是 in_progress。沿用现有认领。锁未过期不要再次 task-claim，不要另开任务。
仓：gkx-orchestration，分支 dev。本单改过程文档，不改业务仓代码。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
开始时间：2026-10-22。完成日期要求：2026-10-25。这两列是我方要求，不是久新承诺。

目标：把「工程过程/04-系统集成/02-对接三要素/技术方案.md」从草案写成可送签收的五段方案。签收操作人是 human:淮政玮。久新三份材料未到之前不得把状态改为 ready_to_sign。库连接坐标已写入技术方案并测通 Doris；数据结构说明、指标和算法说明仍未到。密码不进 git。五段写齐且上述材料到齐、DoD 能逐条对上之后，才可改为 ready_to_sign。不得改成 done。不得建开发叶。

图：必含本方案已有的两张图，并保持与正文一致。
- SYSINT-SCHEME-02-SEQ：§2 sequenceDiagram
- SYSINT-SCHEME-02-FLOW：§3 flowchart
先改图再改文。不另画与 architecture-baseline 冲突的全局拓扑。正式图空间切换归第 7 项，不在本方案里改空间。

必读：
- agent-delivery/系统集成整体过程规约.md §2 第 2 项、§6、§7、§13
- agent-delivery/architecture-baseline.md §2 调用链与 D12
- agent-delivery/data-lineage-policy.md（指标段只消费指标库，不在方案里新定义口径）
- agent-delivery/scope-baseline.md（本页不改范围）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/技术方案.md（在这篇上改，不另起一份）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/README.md（连接坐标；密码不在此文件）
- agent-handoffs/展示系统三要素集成-SCI-INT/ 只作输入，283 个 SRS 叶不算专题已覆盖
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围（只写方案，不派编码）：
1. 展示、专题、数据、指标四侧对上北京久新的技术 / 技术链、人才、科研机构。企业不算科研机构。
2. 展示侧：科技人才态势四子页（WBS-02-01）、科技发展态势八页里的三要素区块（WBS-02-02）。前端不直连久新。
3. 专题侧（WBS-02-03）：系统-04 目前只分析。开不开实现叶由本方案写死；写不死就写「还没有」。
4. 数据（WBS-02-04）：主数据落 ADS，Java 只读。页面不直连久新库。
5. 指标（WBS-02-05）：与指标库对齐。SCI-INT 的分析覆盖不算已对齐。

必须在方案里写死或明确写成「还没有」的口径：
- 调用方向、鉴权、数据落点、缺数时界面表现、智树不做的部分、我方对接文档清单、对端对接文档清单。
- 数据结构说明、指标和算法说明未到的，缺项保持「还没有」。不把「待确认」写成已接入。
- 连接信息只保留已落盘的非密坐标。密码不写入任何文件。

DoD（与注册表一致）：
1. 第 1 段背景、集成需求、对接系统说明写齐；没有材料写「还没有」。
2. 第 2 段应用架构、时序、实现方式写齐；没有材料写「还没有」。
3. 第 3 段数据需求、数据流、加工融合、存储扩展写齐；没有材料写「还没有」。
4. 第 4 段指标、实现方式、与指标库是否对齐、缺项写齐；没有材料写「还没有」。
5. 第 5 段分模块实现、本维 WBS、前端、算法、数据加工写齐，且能对上 WBS-02-00～02-05。没有材料写「还没有」。
6. 能答出调用方向、鉴权、数据落点、缺数表现、智树不做、我方文档清单、对端文档清单。
7. handoff：agent-delivery/agent-handoffs/SYSINT-SCHEME-02-L01.md。ponytail 行写 N/A。evidence 指向该 handoff 和改过的技术方案路径。材料未到齐时保持 in_progress。到齐且 DoD 对上后，task-update-status 到 ready_to_sign。不要写「会签通过」除非人已经签。

禁止：
- task-create 任何开发叶。
- 修改已有任务的 depends_on、状态或 DoD。
- 把本任务标 done，或在三份材料未到时标 ready_to_sign。
- 把智树内部需要日写成久新承诺。完成日期要求只沿用 2026-10-25，不改这个日期。
- 在过程夹里改 scope-baseline。
- 密码、完整连接串写入 git。
```
