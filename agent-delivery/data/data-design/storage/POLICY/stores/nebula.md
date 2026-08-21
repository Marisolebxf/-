# POLICY · Nebula（一张 G 挂接）

```yaml
---
doc_id: POLICY-STORE-NEBULA
element: POLICY
role: store-nebula
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: nebula
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> 拓扑真源：[`../01-data-flow.md`](../01-data-flow.md) §3（**approved** 施工范围）。本文件只落细表指针，**draft**。

## Space

| 项 | 值 |
|---|---|
| Demo | **仅** `demo_gkx_chain` |
| 正式 | `gkx_chain`（本管线禁写） |
| 废作目标 | `gkx_policy`（v1 §4 DDL 禁止照抄 CREATE SPACE） |
| vid | `FIXED_STRING(80)`（CHAIN）；政策点 `pol:{policy_id}` |

## 本波 DDL（IF NOT EXISTS · B 叶执行）

```ngql
USE demo_gkx_chain;
CREATE TAG IF NOT EXISTS policy(name string, weight double, props string);
CREATE EDGE IF NOT EXISTS support(weight double, factor_type string, src_table string);
CREATE EDGE IF NOT EXISTS apply_to(weight double, src_table string);
CREATE EDGE IF NOT EXISTS regulate(weight double, src_table string);
CREATE EDGE IF NOT EXISTS cite(relation string, weight double);
```

已有 Tag 只 hang：`chain` / `segment` / `enterprise` / `institution`。不新建 `org` / `industry` / `tech` / `talent`。

禁止：`DROP SPACE`；写 `gkx_chain`；`CREATE SPACE gkx_policy`。
