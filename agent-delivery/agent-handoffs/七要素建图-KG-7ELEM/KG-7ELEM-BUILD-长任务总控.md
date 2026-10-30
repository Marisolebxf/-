# KG-7ELEM-BUILD · 七要素建图需求 · 长任务总控

> **日期**：2026-10-30  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：把已签收的展示查询需求，加上真正读图或写图的算法，收成七要素必须三元组、建图动作，以及建图 schema 相对 storage 存储设计的缺项。  
> **模式**：长任务。只写文档，不改业务仓代码，不开开发叶。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **过程夹**：[`07-图数据库集成`](../../工程过程/04-系统集成/07-图数据库集成/WBS.md) 的 WBS-07-00E～00E4  
> **锁**：`lock_hours=24`。`supervised_by=human:淮政玮`。`claim_type=coordinator_dispatch`（`task-claim` 没有该字段，认领时写入该叶 note）

本文件是 2026-10-30 的一次授权。`KG-7ELEM-BUILD-REQ-L01` 已由淮政玮认领，作为汇总，不重复做子单判定。L02 起按下面的箭头领，不必再回聊天确认。

厚包：[`KG-7ELEM-BUILD-总派单.md`](./KG-7ELEM-BUILD-总派单.md)  
薄条：[`KG-7ELEM-BUILD-派单条.md`](./KG-7ELEM-BUILD-派单条.md)  
过程夹里的 [`派单说明-KG-7ELEM-BUILD-REQ-L01.md`](../../工程过程/04-系统集成/07-图数据库集成/派单说明-KG-7ELEM-BUILD-REQ-L01.md) 只作范围细则，开工以本总控和厚包为准。

---

## 1. 叶表

全部仓：`gkx-orchestration`，分支 `origin/dev`。执行 `data-agent`。`ponytail:` 写 `N/A`（定义/文档）。

| 波 | 任务 | WBS | 状态门 | 产物 |
|----|------|-----|--------|------|
| 1 | `KG-7ELEM-BUILD-REQ-L02` 消费清单与实体归并 | 00E1 | 查询清单 `KG-YANDA-SCHEMA-REQ-L01` 已 done。本叶当前 ready，可直接认领 | `07-图数据库集成/KG-7ELEM-BUILD-REQ-L02-消费与归并.md` |
| 2 | `KG-7ELEM-BUILD-REQ-L03` 必须三元组与关系总图 | 00E2 | L02 有 handoff，且状态 ≥ `integration`。不等 `done` | `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`，图 `KG-7ELEM-MUST-EDGES` |
| 3 | `KG-7ELEM-BUILD-REQ-L04` 建图动作与缺口 | 00E3 | L03 有 handoff，且状态 ≥ `integration`。与 L05 并行 | `KG-7ELEM-BUILD-REQ-L04-建图需求.md` |
| 3 | `KG-7ELEM-BUILD-REQ-L05` 建图 schema 与存储设计缺项 | 00E4 | 同 L04 的门。与 L04 并行 | `KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md` |
| 4 | `KG-7ELEM-BUILD-REQ-L01` 汇总 | 00E | L02～L05 都有 handoff，且都 ≥ `integration`。本叶已认领，不要再次 task-claim | `KG-7ELEM-BUILD-REQ-L01-七要素必须三元组与建图需求.md` |

handoff 一律 `agent-handoffs/KG-7ELEM-BUILD-REQ-L0x.md`，与各叶 DoD 一致。evidence 指向该 handoff 和上表产物。

```text
L02 → L03 → L04 ─┐
              └→ L05 ─┴→ L01 汇总
```

L04 与 L05 产物路径不同，可以并行。禁止两叶改同一个文件。禁止改 `技术方案.md`、storage 设计原文、`task-registry.yaml`（注册表只走 MCP）。

---

## 2. 已拍板（执行中不许再问）

1. 七要素名称锁定：企业、产业链环节、科研机构、技术、人才、服务机构、政策。技术 = 论文 / 专利 / 项目。展示清单的 `technology` 技术点不并进技术。
2. 只写文档。不写 REST，不改 Nebula space，不配 GDF，不改 `lumen-algo-py` / Java / 前端。
3. 正式空间仍是技术方案里的 `demo_gkx_chain`。本管线不改空间，不选燕大 `gkx_local_1` / `gkx_full_1` 当生产。
4. 查询侧数字以 `KG-YANDA-SCHEMA-REQ-L01` v1.2 正文 §1.5 / §9 为准：保留 98、转背景 16、不相关 457，飞书收回 84。不用 §2.1 残留的 81 / 15 / 475。
5. 表名、枚举、样本量在来源材料里没有的，写「待确认」或「存储设计未写」。禁止臆造。
6. `SYSINT-SCHEME-07-L02`～`L05`、`L07` 只作对照。未签收的不写成已放行契约。不重做差集，不重做 L07 的代码差异，不回头改那些文件。
7. 结构歧义（新图空间、改 VID 生产规则、新写正式库）停在该叶，升级 `human:李伟`。其余叶继续。
8. `ready_to_sign → done` 只由 `human:淮政玮` 点。签收可以积压，不挡下一波。
9. 段 E 不启用。本管线没有编码、没有发布、没有金路径。不派 qa-agent，不等黄敬洲。

---

## 3. 无人值守

1. 升 ready 的条件只有规约 §6.2：前序 handoff 已在，且状态 ≥ `integration`。然后 `task-claim`：`claimed_by=agent:data-agent`，`supervised_by=human:淮政玮`，`lock_hours=24`。note 写上 `claim_type=coordinator_dispatch`。
2. 定义叶的完成路径是 `in_progress → integration → ready_to_sign`。交 handoff 和 evidence 后停在 `integration`。不要写「会签通过」，除非人已经会签。不要标 `done`。
3. lease 过期：同一监管人续领，不改本总控。
4. 凭据、API Key、连接口令不进 git。

卡住只允许：真环境不通导致读不了已点名的材料、正式库误写风险、第 2 节第 7 条的结构升级。
