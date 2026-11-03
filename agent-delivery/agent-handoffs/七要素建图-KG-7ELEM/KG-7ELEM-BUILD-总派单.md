# KG-7ELEM-BUILD · 总派单（厚包）

> 开工先读 [`KG-7ELEM-BUILD-长任务总控.md`](./KG-7ELEM-BUILD-长任务总控.md)。本文件是范围和禁止项。薄条不能单独开工。

## 身份与强度

```text
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师。本单是定义类文档，完整性优先。禁止用 ponytail 强度行删表或删三元组。禁止用 headroom compress 代替精读需求清单、上图台账、入图流程和 storage 入图设计。
强度：N/A（定义/文档）。不写 SQL、ETL、脚本。
上下文：headroom 可选。总控点名的材料必须读原文。
监管人：human:淮政玮。长任务已授权，后续认领不必再问。
认领：claimed_by=agent:data-agent，supervised_by=human:淮政玮，lock_hours=24。note 写 claim_type=coordinator_dispatch。
仓：gkx-orchestration，分支 dev。只写本叶产物。完工后停在本地，不自行 commit / push，除非本会话的人明确说提交。
总控：agent-handoffs/七要素建图-KG-7ELEM/KG-7ELEM-BUILD-长任务总控.md
```

## 共用口径

七要素：企业、产业链环节、科研机构、技术、人才、服务机构、政策。技术 = 论文 / 专利 / 项目。

查询真源：`工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/知识图谱-实体关系属性需求清单.md` v1.2。数字以 §1.5 / §9 为准。

对照材料（不改原文）：

- `工程过程/04-系统集成/07-图数据库集成/对接文档/智谱/SYSINT-SCHEME-07-L03-算法中台上图台账.md`
- 同目录 `SYSINT-SCHEME-07-L06-算法中台入图流程.md`
- 同目录 `SYSINT-SCHEME-07-L04-燕大七要素上图对照.md`
- 同目录 `SYSINT-SCHEME-07-L05-需求减已实现GAP.md`
- 同目录 `SYSINT-SCHEME-07-L07-入图schema差异清单.md`（L05 不得重做这份代码差异）
- `工程过程/04-系统集成/07-图数据库集成/技术方案.md`
- `data/data-design/storage/{ENT,CHAIN,POLICY,SVC,COMP}/etl/pipeline-to-nebula.md` 与各域 `stores/nebula`
- `diagram-as-contract.md`

任务查询只用 MCP。禁止读 `task-registry.yaml`。

## 各叶只写什么

| 叶 | 只写 | 不写 |
|----|------|------|
| L02 | 读图消费三元组（回指 seq 或算法入口）；14 类实体归并或不进七要素 | 必须边裁决、关系总图、建图动作、schema 缺项 |
| L03 | 两端都在七要素上、且 L02 已有消费的必须三元组；不建边及原因；图 `KG-7ELEM-MUST-EDGES` | L02 没有的消费来源；抽取来源；流水线缺口 |
| L04 | L03 每条必须三元组的建图动作、来源占位、已有写图流水线、缺口 | 新的必须边；臆造表名 |
| L05 | L03 必须三元组的 Tag / VID / 属性 / Edge；对照 storage 后的缺项（缺 Tag、缺 Edge、缺属性、无对应存储域） | 改 storage 原文；重做 L07 代码差异；新的必须边 |
| L01 | 把四份收成主文，不改子单已经写定的判定 | 重做四张子单的判定；标 done |

图只在 L03：一张 flowchart，节点只用七要素中文名，只画必须建的边。不另画 L0 全局拓扑，不复制 ENT / CHAIN / SVC 存储流图。

## 交接

每叶 handoff：`agent-handoffs/KG-7ELEM-BUILD-REQ-L0x.md`。`ponytail: N/A（定义/文档）`。填 evidence 后状态到 `integration`。不要写「会签通过」，不要标 `done`。

L01 的 handoff 另写：必须三元组条数、不建条数、待确认条数、存储设计缺项条数、图 ID。
