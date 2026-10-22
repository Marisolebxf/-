# 派单说明 · SYSINT-SCHEME-03-L01

```text
/goal doc-agent
身份：你是经验丰富、遵循最佳实践的资深技术文档工程师。本单是系统集成技术方案，定义完整性优先。禁止用 ponytail 强度行删章节。禁止用 headroom compress 代替精读规约、WBS 和现稿。

任务：SYSINT-SCHEME-03-L01
标题：系统集成技术方案_专题系统集成
监管人：human:淮政玮
执行：agent:doc-agent
状态：已是 in_progress。沿用现有认领。锁未过期不要再次 task-claim，不要另开任务。
仓：gkx-orchestration，分支 dev。本单改过程文档，不改业务仓代码。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
开始时间：无开始时间。完成日期要求：2026-11-05。这个日期取科技专题服务系统功能开发较晚的那一档，不是系统测试或上线日。

目标：把「工程过程/04-系统集成/03-专题系统集成/技术方案.md」从草案写成可送签收的五段方案。签收操作人是 human:淮政玮。你只能在五段写齐、DoD 能逐条对上之后，把状态改为 ready_to_sign。不得改成 done。不得建开发叶。

图：必含本方案已有的两张图，并保持与正文一致。
- SYSINT-SCHEME-03-SEQ：§2 sequenceDiagram（对端/运营 → 网关 → Java → overlay；可视化 → 网关 → Java → ADS / Python /internal/*）
- SYSINT-SCHEME-03-FLOW：§3 flowchart（真源、overlay、ADS、可视化页面）
先改图再改文。不另画与 architecture-baseline 冲突的全局拓扑。不把图空间切换写进本方案。

必读：
- agent-delivery/系统集成整体过程规约.md §2 第 3 项、§6、§7、§13
- agent-delivery/architecture-baseline.md §2 调用链与 D12
- agent-delivery/data-lineage-policy.md（指标段只消费指标库，不在方案里新定义口径）
- agent-delivery/scope-baseline.md（本页不改范围）
- agent-delivery/工程过程/04-系统集成/03-专题系统集成/WBS.md
- agent-delivery/工程过程/04-系统集成/03-专题系统集成/技术方案.md（在这篇上改，不另起一份）
- agent-delivery/工程过程/04-系统集成/04-门户系统集成/纪要/2026-10-22-统一用户中心菜单配置.md
- agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-字段与读接口契约.md 及四份 PORTAL-CMS 契约
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围（只写方案，不派编码）：
1. 基础数据：产品链、企业、政策、产业服务机构。技术链、科研机构、人才归第 2 项，不写进本方案的实现范围。已在注册表的基础数据叶保持原 ID、原 depends_on，不要把 SYSINT-SCHEME-03-L01 追进去。
2. 内容管理四菜单：智树做页面、接口、数据。使用人是运维人员。
3. 可视化四菜单：智树做前后端。使用人是运维人员。不是第 4 项门户上给普通用户看的那四页，不合并、不删 WBS-04 的页。
4. 收口：八个菜单的相对路径和用户权限是 WBS-03-18。配菜单的人纪要未点名，方案里写「还没有」，不要指定人名。

必须在方案里写死或明确写成「还没有」的口径：
- 四个内容菜单与现网用词：产业全景 / 专题全景 / 产业概况，专题服务 / 产业服务，政策扶持 / 政策新闻。不能拍板的写「还没有」，不要用别的维度的名字填上。
- 调用方向、鉴权、数据落点、缺数时界面表现、智树不做的部分、我方对接文档清单、对端对接文档清单。
- 指标与指标库逐条对齐还没有做完的，保持「还没有」。不把 PORTAL-CMS-METRIC-COVER-L01 的 claimed 写成已对齐。
- 企业发展契约已确认。专题全景、专题服务、政策扶持三份仍是草案的，按草案引用，不改字段。

DoD（与注册表一致）：
1. 第 1 段背景、集成需求、对接系统说明写齐；没有材料写「还没有」。
2. 第 2 段应用架构、时序、实现方式写齐；没有材料写「还没有」。
3. 第 3 段数据需求、数据流、加工融合、存储扩展写齐；没有材料写「还没有」。不新造表名，不在回写单未签收前写新字段。
4. 第 4 段指标、实现方式、与指标库是否对齐、缺项写齐；没有材料写「还没有」。
5. 第 5 段分模块实现、本维 WBS、前端、算法、数据加工写齐，且能对上 WBS-03-00 以及 03-01～03-18 的现有行。没有材料写「还没有」。
6. 能答出调用方向、鉴权、数据落点、缺数表现、智树不做、我方文档清单、对端文档清单。
7. handoff：agent-delivery/agent-handoffs/SYSINT-SCHEME-03-L01.md。ponytail 行写 N/A。evidence 指向该 handoff 和改过的技术方案路径。然后 task-update-status 到 ready_to_sign。不要写「会签通过」除非人已经签。

禁止：
- task-create 任何开发叶，含内容管理、可视化、WBS-03-18。
- 修改 CMS-JX-*、PORTAL-CMS-* 已有任务的 depends_on、状态或 DoD。
- 把本任务标 done。
- 把智树内部出门日写成对端承诺。完成日期要求只沿用 2026-11-05，不改这个日期。
- 在过程夹里改 scope-baseline。
- 密码、连接串写入 git。
```
