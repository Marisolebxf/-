# 政策库 — 给三方供应方的问题清单

```yaml
---
doc_id: POLICY-SUPPLIER-QUESTIONS-20260901
element: POLICY
role: source
status: draft
version: "2026-09-01"
updated: 2026-09-01
owner: human:淮政玮
audience: 三方供应方（书面回复） / PM 转发
---
```

> **用途**：政策图谱 C 档 hang 必须 `FETCH` 产业链已有 VID（`chain:{chain_id}` / `segment:{node_id}`，如 `INB1701`）。供应库当前几乎只有名称或空值，对不上码。本清单只问**供应方 `dwd_*` 字段与主键**，不把项目派生列甩给对方。  
> **抽样**：2026-09-01 Demo 贴源 `demo_gkxlumenx_ods.dwd_policy_base`，`is_deleted=0`，**47050** 行（与供应库 `gkx.dwd_policy_base` 同构镜像；验收仍以 live `gkx` 为准）。  
> **DDL 真源**：[`data-design/storage/POLICY/sources/ods-ddl.md`](../data-design/storage/POLICY/sources/ods-ddl.md)。  
> **供应方约束**：[`gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> **不要问对方**：项目 DWD `policy_base_info.related_entities`（我方 `ods_to_dwd` 拼的，供应库无此列）；政策类型展示归类 QPOL-01（甲方口径）；图谱 C 回写供应库（C 不写入站表）。

请对方**逐条**按文末模板回复。

---

## P0 请书面确认并给样例

### 1. 空值约定

字段里大量是**字符串 `"NULL"`**，不是 SQL `NULL`。

| 字段 | 字符串 `"NULL"`（约） | 全表 | 占比 |
|---|---|---|---|
| `theme` | 45010 | 47050 | 95.7% |
| `keywords` | 46685 | 47050 | 99.2% |
| `quote_policy` | 45491 | 47050 | 96.7% |
| `ministry` | 约 44216 为空 / `"NULL"` | 47050 | ~94% |

请确认：未抽取时应用 SQL `NULL`、空串，还是 `"NULL"`？后续批次能否统一？

### 2. `theme` 口径对不上 DDL

DDL COMMENT：对政策背景、指导思想等做标准化拆解与提炼。

实测非空值是**标签 JSON 数组**，例如 `["监督管理"]`、`["科技创新","产业发展"]`，不是产业名，也不是指导思想正文。

请确认：

- `theme` 正式语义是什么？
- 合法枚举 / 码表是什么？
- 是否另有「目标产业 / 细分产业」字段或另表？

### 3. 产业稳定编码（图谱刚需）

现有字段对不上产业链 `chain_id` / `node_id`（`INB*`）。没有码只能挂名称，**无法上图**。

请确认并交付其一：

1. 政策行上增加产业 / 环节编码列（建议对齐 `INB1701`、`INB17010102`）；或
2. 给出政策 `id` ↔ 产业链码对照表（表名 + 样例 3 行）。

### 4. `policy_support` JSON 正式 schema

实测为**数组**，元素形如：

| 键 | 实值例子 |
|---|---|
| `condition` | `["具有独立法人资格", …]` |
| `support_way` | `["设备引进"]` / `["获得奖励/资质"]` |
| `support_object` | `"企业"` / `"从业人员/人才"` / `"其他"` |
| `support_behavior` | `["税收优惠"]` / `["职称评定"]` |

请提供：完整 JSON Schema、枚举、空值规则。并确认：

- `support_object` 是否会给到企业 / 机构**统一社会信用代码或组织机构代码**，还是永远只有角色词？
- 有没有「目标产业编码」？当前抽样**没有**。

---

## P1 请说明有没有、在哪张表

### 5. 关联主体主键

政策 ↔ 企业 / 科研机构 / 服务机构，是否有稳定 ID？在 `dwd_policy_base` 还是另表？请给**表名 + 3 条样例**（政策 `id` + 对方主键）。

### 6. `quote_policy` 引用政策

约 96% 为 `"NULL"`。有值时是标题、文号，还是被引政策的稳定 `id`？图谱引用边需要对方 `id`，不要只给标题。

### 7. `ministry` 发文部门

约 94% 空。空是否表示未抽取？有值时能否配组织机构代码，而不只是名称？

### 8. `type` / `rank` / `status` 枚举闭集

请给合法值清单。`rank` 是否严格为国家级 / 省级 / 市级 / 区县级？`status` 是否只有有效 / 失效？

---

## P2 技术约定

### 9. `id` 长度与撞号

当前最长 8 字符，我方图 VID 为 `pol:{id}`（space `vid_length=80`）。请确认不会超过 80 字符，也不会与国际表 `dwd_global_policy_base.id` 撞号。

### 10. 行过滤

`is_history` / `is_deleted` / `insert_remark` 的当前行过滤规则请书面写清（我方默认 `is_deleted=0`）。

### 11. 国际表 `dwd_global_policy_base`

无 `status` / `expire_date` / `rank`。国内国际如何区分有效政策？

---

## 请对方每条按此格式回

| 项 | 内容 |
|---|---|
| 问题编号 | 1–11 |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：`id` + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |

---

## 抽样备注（项目侧，不发给对方也可）

- 产业 hang 输入槽：我方 DWD `related_entities.industry` ← `ods_to_dwd` 抄 `theme` 或 `policy_support` 内「目标产业」；`theme` 为 `"NULL"` 时槽内就是 `["NULL"]`。
- 图谱 C（`POLICY_RE_SUPPORT` 等）只 **读** 该槽做 `FETCH`，**不回写**供应库、也不回写 DWD。
- 对照产业链已存在点：`chain:INB1701`（新一代信息技术）、`segment:INB17010102`（晶圆制造）。
