# KG-7ELEM-LOAD · 总派单（厚包）

> 开工以 [`KG-7ELEM-LOAD-长任务总控`](./KG-7ELEM-LOAD-长任务总控.md) 为准。薄条不能单独开工。  
> 2026-10-30 本会话已授权开跑 L02–L06。L01 仍等五份 handoff 且 ≥ integration。L06 的久新材料与只读探查以派单说明为准，其他叶不连 Doris。

```text
/goal data-agent
身份：资深数据架构/数据工程师。定义文档，完整性优先。禁止用 ponytail 删掉三问里的任一类。禁止用 headroom compress 代替读代码和已签收必须边。

类型：definition。仓 gkx-orchestration，分支 dev。只写本叶产物和 handoff。
监管：supervised_by=human:淮政玮。claim_type=coordinator_dispatch。lock_hours=24。
强度：N/A（定义/文档）。
协作：algorithm-agent。只在代码入口对不上时核对。不改算法仓。

共同输入（只读）：
- 已签收 KG-7ELEM-BUILD-REQ-L03 必须三元组
- 已签收 KG-7ELEM-BUILD-REQ-L05 建图 schema
- 本域 storage 的 etl/pipeline-to-nebula.md 与 stores/nebula（有则读）
- 我方已实现写图代码：lumen-algo-py，以及对接文档里已经点名的入口
- 燕大已实现代码：yanda/tech-kg-api。只作已实现对照，不选燕大 space 作生产，不把未签收对照写成放行

本叶只回答总控第 3 节的三问，且只回答分给本叶的必须三元组。
我方和燕大分开写。没有代码就写未实现。没有表名就写待确认。
第 3 问可以在本叶目录附 Python 示例脚本，只说明核心逻辑。不接真实库，不执行，不加新依赖，不放进业务仓。示例不能把未实现写成已实现。
不执行 nGQL，不连图库，不改业务仓代码，不改 storage，不改已签收建图正文。

落盘后 handoff 写清：本域三问各几条，其中待确认几条，燕大有代码但我方没有的几条。
task-update-status 到 integration。不要写会签通过。不要标 done。
```

| 叶 | 范围 | 产物 |
|----|------|------|
| L02 | 企业端点，以及两端都是企业的必须边：`cooperate`、`supply`、`parent_sub`。企业到环节的 `participates`、企业到政策的 `policy_apply_to`、服务到企业的 `service_provide` 若源在企业表，也在本叶写来源，并注明另一端归哪一叶 | `07-图数据库集成/KG-7ELEM-LOAD-PATH-L02-企业.md` |
| L03 | 产业链环节，以及 `depends_on`、企业或服务机构 `participates` 到环节 | `KG-7ELEM-LOAD-PATH-L03-产业链.md` |
| L04 | 政策端点，以及 `cite`（政策—政策）、`policy_relate`、`policy_apply_to`、`publish`。向量或语义相似只在代码里已有时写成已实现 | `KG-7ELEM-LOAD-PATH-L04-政策.md` |
| L05 | 服务机构端点 `institution`，以及服务机构之间不建的边不要补上。`participates` 到环节、`service_provide` 到企业，写服务机构这一端的来源 | `KG-7ELEM-LOAD-PATH-L05-服务机构.md` |
| L06 | 科研机构、人才、技术。必须边：`cooperate`、`belong`、`participate`、`author_of`、`research_coop`、`talent_coop`、技术 `cite`、`publish` 的科研机构一端。没有独立 pipeline-to-nebula。`technology` 技术点不计入 | `KG-7ELEM-LOAD-PATH-L06-科研人才技术.md` |
| L01 | 五叶都 ≥ integration 且有 handoff 后，收成三问总表。不新裁 | `KG-7ELEM-LOAD-PATH-L01-上图路径方案.md` |

同一条边若跨两域，两叶都写自己这一端的来源，汇总时合成一行，不把两套说法改成第三套。
