# 派单说明 · SYSINT-SCHEME-06-L01

```text
/goal doc-agent
身份：你是经验丰富、遵循最佳实践的资深技术文档工程师。本单是系统集成技术方案，定义完整性优先。禁止用 ponytail 强度行删章节。禁止用 headroom compress 代替精读规约、WBS 和现稿。

任务：SYSINT-SCHEME-06-L01
标题：系统集成技术方案_GDF数据治理集成
监管人：human:淮政玮
执行：agent:doc-agent
状态：已是 in_progress。沿用现有认领。锁未过期不要再次 task-claim，不要另开任务。
仓：gkx-orchestration，分支 dev。本单改过程文档，不改业务仓代码。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
开始时间：无已记录开始时间。完成日期要求：暂无截至时间。这两列不是对端承诺。不自行补一个截止日期。done 操作人是 human:淮政玮。

目标：把「工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md」从草案写成可送签收的五段方案。签收操作人是 human:淮政玮。你只能在五段写齐、DoD 能逐条对上之后，把状态改为 ready_to_sign。不得改成 done。不得建开发叶。执行结果未回，不把任何域写成已跑通。可投递包和预填 DRAFT 不是可对端。

图：必含本方案已有的两张图，并保持与正文一致。
- SYSINT-SCHEME-06-SEQ：§2 sequenceDiagram（供应方只读 → GDF → ODS → DWD；Java 只读 ADS）
- SYSINT-SCHEME-06-FLOW：§3 flowchart
先改图再改文。不另画与 architecture-baseline 冲突的全局拓扑。GDF 可触发亿集 API，不直写图库；读图归第 7 项。

必读：
- agent-delivery/系统集成整体过程规约.md §2 第 6 项、§6、§7、§13
- agent-delivery/architecture-baseline.md §2 调用链与 D12
- agent-delivery/data-lineage-policy.md（GDF 不发明指标口径）
- agent-delivery/scope-baseline.md（本页不改范围）
- agent-delivery/data/GDF/GDF协作指南.md
- agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/WBS.md
- agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md（在这篇上改，不另起一份）
- 现行派单包：企业 v4、产业链 v2、政策 v1。历史包 v1–v3 不施工
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围（只写方案，不派编码）：
1. 供应方库只读进入 GDF，映射到自建 DWD / ADS。Java 只读 ADS。页面不直接接三方源。本项不进统一用户中心。
2. 已有包：企业（WBS-06-01）、产业链（WBS-06-02）、政策 v1 到 policy_base_info（WBS-06-03）。产业链分析六表只贴不洗。政策 v1 不含 ES。
3. 无包但已列入方案：市场研究金融 / 宏观 / 行业分析（WBS-06-04～06）、产业资讯（WBS-06-07）、培训三课（WBS-06-08～10）、论文、专利、项目报告、全球科技人才（WBS-06-11～14）。
4. 2026-10-22 晚纳入、工作计划仍未填：服务机构、国外机构库、国内政策、国外政策（WBS-06-15～18）。国内政策、国外政策不并进政策 v1。没有包之前写「还没有」，不算已排期。

必须在方案里写死或明确写成「还没有」的口径：
- 调用方向、鉴权、数据落点、缺数时界面表现、智树不做的部分、我方对接文档清单、对端对接文档清单。
- 无派单包、无执行结果的域，缺项写「还没有」。不估进度。
- 产业资讯表在客户决策清单 2026-08-25 禁止业务使用。未解除则不上屏。
- 培训次数和课时仍是问号，不写成已承诺。
- 与指标库逐条对齐还没有用本方案做完的，保持「还没有」。口径仍归指标负责人。
- 密码不进 git。

DoD（与注册表一致）：
1. 第 1 段背景、集成需求、对接系统说明写齐；没有材料写「还没有」。
2. 第 2 段应用架构、时序、实现方式写齐；没有材料写「还没有」。
3. 第 3 段数据需求、数据流、加工融合、存储扩展写齐；没有材料写「还没有」。新增或变更字段只认现行包，不另增列。
4. 第 4 段指标、实现方式、与指标库是否对齐、缺项写齐；没有材料写「还没有」。
5. 第 5 段分模块实现、本维 WBS、前端、算法、数据加工写齐，且能对上 WBS-06-00～06-18。没有材料写「还没有」。
6. 能答出调用方向、鉴权、数据落点、缺数表现、智树不做、我方文档清单、对端文档清单。
7. handoff：agent-delivery/agent-handoffs/SYSINT-SCHEME-06-L01.md。ponytail 行写 N/A。evidence 指向该 handoff 和改过的技术方案路径。然后 task-update-status 到 ready_to_sign。不要写「会签通过」除非人已经签。

禁止：
- task-create 任何开发叶，或在 GDF 里配作业。
- 把未回传的执行结果写成已跑通，或把三方源接到前端。
- 把本任务标 done。
- 自行填写开始时间或截至时间。
- 在过程夹里改 scope-baseline。
- 密码写入 git。建图算法和读图页面不写进本方案。
```
