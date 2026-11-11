# 603-STRUCT-FDE · 波次 C · 知会 · data

总单：`POL-L2-PC1-STRUCT-FDE-L01`。身份：`agent:data-agent`。日期：2026-11-10。  
定档：**轻**（`603-STRUCT-FDE-B-读法方案.md`）。本波不经 data 实现段。

## 知悉

- **无新表**：不建 ADS / DWD / gapfill / Storage / 字典表；不重开 GDF / C2。
- **两表 Wave0 前端 seed**：标签体系表、字段映射表由展示 live 适配器合并既有 seed 常驻有数；**不**为本两表扩 `governance/results`、不新建读口。
- **写回仍走既有 ADS**：抽取成功仍写 `policy_text_parse`（经既有 enrich 链）；本波不改表结构。
- **影响清单**：已读 B §5——`STRUCT-DATA` / METRIC 后波清掉「两表可空 / 仅 mock 有数」旧句即可，**无 DDL**；本知会不改正文。

无异议、无停机项。
