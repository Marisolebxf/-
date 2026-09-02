# 综合维（COMP）存储设计 — 入口

> **读我**：本目录是综合·图谱 API（SRS **116**）的 **draft 指针**，不是第二张图、不是新 Tag/Edge 真源。  
> **规范**：[`../README.md`](../README.md)  
> **本叶**：`DEMO-COMP-GRAPH-TRIPLE-UI-L01` · 监管人 `human:徐滕强`

```yaml
---
doc_id: COMP-STORAGE-INDEX
element: COMP
role: index
status: draft
version: "2026-09-02"
updated: 2026-09-02
task_id: DEMO-COMP-GRAPH-TRIPLE-UI-L01
---
```

## 读序

1. [`etl/pipeline-to-nebula.md`](./etl/pipeline-to-nebula.md) — **本叶契约**（只读查询 + 灌数零图谱）
2. 一张 G 口径 → [`../README.md`](../README.md) 决策 #7 · space `demo_gkx_chain`
3. 企业写入契约（本叶只消费、不改）→ [`../ENT/etl/pipeline-to-nebula.md`](../ENT/etl/pipeline-to-nebula.md)

## 已锁定

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/COMP/` |
| 本叶范围 | **仅 D + 116 五查询**；**无 A/B/C 写入** |
| Space | 只读 `demo_gkx_chain`；禁止综合第二张图 / `CREATE SPACE` |
| 边 | **不另造边**；消费各域已上图三元组 |
| 流图 | **不新建** `01-data-flow.md`（不翻签 ENT/CHAIN 已批准拓扑） |
| 灌数 | 综合基础页无独立贴源；禁止借综合灌数建图/投影 |

本叶只写文档，不改 Python / Java / Vue，不 APPLY DDL，不灌数。
