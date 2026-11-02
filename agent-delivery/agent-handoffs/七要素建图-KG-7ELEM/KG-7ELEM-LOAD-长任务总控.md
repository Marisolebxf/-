# KG-7ELEM-LOAD · 七要素上图路径 · 长任务总控

> **日期**：2026-10-30  
> **授权**：`human:淮政玮` 要求把上图路径收成一条长任务。2026-10-30 本会话已授权开跑 L02–L06。L01 仍等五份 handoff 且状态 ≥ integration。  
> **目标**：按已签收的必须三元组，对照我方和燕大已经实现的代码，回答三类上图路径：关系库能直接上、缺项要先加工、不能靠源表要先用其他技术。  
> **模式**：长任务。只读代码、只写文档。不改业务仓，不执行 nGQL，不开开发叶，不派段 E。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **监管人**：`human:淮政玮`。`claim_type=coordinator_dispatch` 写在各叶 note 里。`lock_hours=24`。

厚包：[`KG-7ELEM-LOAD-总派单.md`](./KG-7ELEM-LOAD-总派单.md)  
薄条：[`KG-7ELEM-LOAD-派单条.md`](./KG-7ELEM-LOAD-派单条.md)

---

## 1. 为什么这样切

规约 §5、§6：长任务按能独立交付的叶子切。下游解锁看前序 handoff 且状态 ≥ integration，不等签收。同仓 **coding** 同时只派一张。这六张都是定义文档，产物路径互斥，五张调研可以并行，不违反同仓 coding 一单。

不按三个问题切成三张大叶。企业、产业链、政策、服务、科研/人才/技术的代码和表不在一处，一张叶横扫所有域会漏。每个域自己回答三个问题，汇总叶只合并，不重查。

段 E 不启用。没有发布、没有金路径、不派 qa-agent。

---

## 2. 叶表

全部仓：`gkx-orchestration` `origin/dev`。执行 `data-agent`，协作 `algorithm-agent` 只在代码入口对不上时核对。`ponytail:` 写 `N/A`。

| 波 | 任务 | WBS | 状态门 | 产物 |
|----|------|-----|--------|------|
| 1 | `KG-7ELEM-LOAD-PATH-L02` 企业 | 00F1 | 必须三元组 L03、schema L05 已 done。本叶 ready | `KG-7ELEM-LOAD-PATH-L02-企业.md` |
| 1 | `KG-7ELEM-LOAD-PATH-L03` 产业链 | 00F2 | 同 L02 | `KG-7ELEM-LOAD-PATH-L03-产业链.md` |
| 1 | `KG-7ELEM-LOAD-PATH-L04` 政策 | 00F3 | 同 L02 | `KG-7ELEM-LOAD-PATH-L04-政策.md` |
| 1 | `KG-7ELEM-LOAD-PATH-L05` 服务机构 | 00F4 | 同 L02 | `KG-7ELEM-LOAD-PATH-L05-服务机构.md` |
| 1 | `KG-7ELEM-LOAD-PATH-L06` 科研机构、人才、技术 | 00F5 | 同 L02 | `KG-7ELEM-LOAD-PATH-L06-科研人才技术.md` |
| 2 | `KG-7ELEM-LOAD-PATH-L01` 汇总 | 00F | L02～L06 都有 handoff，且都 ≥ integration。不等 done | `KG-7ELEM-LOAD-PATH-L01-上图路径方案.md` |

```text
L02 ─┐
L03 ─┤
L04 ─┼→ L01
L05 ─┤
L06 ─┘
```

禁止两叶改同一个文件。禁止改已签收的 L01–L05 建图正文、初始化脚本、storage 原文、`SYSINT-SCHEME-07-L06`、业务仓代码。注册表只走 MCP。

---

## 3. 每张调研叶都要回答的三问

只覆盖该域分到的必须三元组。我方实现和燕大实现分成两列，不把燕大代码写成生产放行。

1. 关系库现在就能上的：源表、字段、Tag 或 Edge、代码入口、上图步骤。入口要能在仓库里打开。
2. 因关系数据缺项不能直接上、要先加工的：缺哪张表或哪一列。建议加工落在哪一层。不写 ODS、不写供应方库。建议可以是 DWD/ADS 映射或 `gapfill_` 前缀，只写方法，不建表、不灌数。
3. 不能靠源表、要先用其他技术的：技术名称、现有代码有没有、建议落在 Python 哪一类入口。Java 不做 NLP、向量或模型推理。没有代码的写成「未实现」，禁止把设想写成已实现。这一问可以在本叶产物旁附 Python 示例脚本，只说明核心逻辑。脚本放在该叶自己的目录，不放进业务仓，不加新依赖，不接真实库，不执行。已有实现仍按仓库里的代码写，示例不能代替「已实现」。

表名、字段、枚举在材料里没有的，写「待确认」。`SYSINT-SCHEME-07-L02` 至 `L05`、`L07` 未签收，引用时标明。`technology` 技术点不计入七要素「技术」。

L06 另读 `工程过程/04-系统集成/07-图数据库集成/派单说明-KG-7ELEM-LOAD-PATH-L06.md`。久新原文和只读探查只给 L06。L02–L05 不连 Doris，不读链接信息。

---

## 4. 开工

本总控写完时五张调研是 ready，汇总是 backlog。领取时 `claimed_by=agent:data-agent`，`supervised_by=human:淮政玮`。五张调研同时领。汇总等五份 handoff。每叶停在 integration，不写「会签通过」，不标 done。
