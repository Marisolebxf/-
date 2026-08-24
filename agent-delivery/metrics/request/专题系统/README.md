# 专题系统 · A2.1 输出目录

> 任务：`TOPIC-ALGO-GAP-L01` · **截止 2026-08-24 下班前**  
> Schema：[`../A2-GAP-schema.md`](../A2-GAP-schema.md)  
> 派单：`agent-handoffs/算法库联调-ALGO-LIB/给人说明-A2差集拆解-2026-08-21.md`

本目录交：

| 文件 | 用途 |
|------|------|
| `TOPIC-ALGO-GAP-L01.xlsx` | L01 给人主表（Round 17 指针快照，冻结） |
| `TOPIC-ALGO-GAP-L01.yaml` | L01 机器真源 |
| `TOPIC-ALGO-GAP-L01-summary.md` | L01 计数 |
| `TOPIC-ALGO-GAP-L01.md` | L01 说明 |
| `TOPIC-ALGO-GAP-L02.xlsx` | L02 给人主表（A1 ID 回填） |
| `TOPIC-ALGO-GAP-L02.yaml` | L02 机器真源 |
| `TOPIC-ALGO-GAP-L02-summary.md` | L02 计数 |
| `TOPIC-ALGO-GAP-L02.md` | L02 说明 |

主产物 = 表中 `差集判定=missing` 的行。L02 回填 mapped 的 A1 列，**不覆盖** L01 四人套。`pages/` 分页 yaml 在 L02 只加 A1 字段，不回滚 OPEN 指针；以本目录四件套为准。

开工方式曾用 loop（已 FANIN、`halt`）。编排：`agent-handoffs/算法库联调-ALGO-LIB/A2-GAP-loop-编排.md`；状态与 T00 candidates 已挪到 [`../_work/`](../_work/)。
