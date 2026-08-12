# ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01 · 派单说明

> **日期**：2026-08-12  
> **发起 / 执行 / 会签**：`human:淮政玮`（项目负责人亲自认领执行）  
> **协作 Agent**：`architect-agent`（可辅助改稿与对照基线；**会签签字权 = 淮政玮**）  
> **Task ID**：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01`（已 `claimed` · claimed_by / supervised_by = human:淮政玮）  
> **强度**：ponytail off（definition / 会签，不写业务代码）

---

## 1. 为什么派这张单

已新建 **对模型友好的企业维存储文档树**（`data-design/storage/`），约定：

- 根路径 `storage/ENT/`；文件名 **无版本号**
- 覆盖 MySQL（含 **ADS 必含**）· ES · Nebula · MinIO（**平台级一份 + 企业维引用**）
- 含第三方源边界、ETL、**数据流图**；**不含功能设计**
- 关系库叙述 **禁止 PG**；图谱 **仅 NebulaGraph**
- **流图会签 Owner = 架构职责**；本单由 **淮政玮** 亲自审定并签字；未会签前 `stores/*` 不得标「结构已批准」

本单只做 **S1：数据流图会签**，不灌 as-built 细表、不改旧 `data-design/企业/*`。

---

## 2. 必读（按序）

| 序 | 路径 | 用途 |
|---:|---|---|
| 1 | `agent-delivery/data/data-design/storage/README.md` | 体系规范草案（已拍板 4 点） |
| 2 | `agent-delivery/data/data-design/storage/ENT/README.md` | 企业维入口与读序 |
| 3 | `agent-delivery/data/data-design/storage/ENT/00-context.md` | 边界与铁律 |
| 4 | **`…/storage/ENT/01-data-flow.md`** | **会签主件**（三张 Mermaid + 清单） |
| 5 | `agent-delivery/architecture-baseline.md` | D3 ADS / D6 Nebula / D7 工厂 |
| 6 | `agent-delivery/data/data-design/storage/platform/minio.md` | 平台 MinIO（仅核对引用关系） |

**不要**把下列当会签依据：`data-design/企业/` 下功能设计、PG 大稿 stub、旧 v3 文件名版本叙事。

---

## 3. 你要交付什么

### 3.1 会签动作（主）

在 `01-data-flow.md`：

1. 审三张图：批处理主链 / 在线读路径 / 对象产物  
2. 对照基线：Java 只读 ADS、Python 写派生存储、无越层、无 PG/Neo4j  
3. 补全或确认表内「触发 / 失败语义」；暂无法定的登记为开放项（勿留空白「待填」无说明）  
4. 勾选 §4 会签清单  
5. frontmatter 更新：

```yaml
status: approved          # 或保持 draft 并写明驳回原因
signoff_status: approved  # 或 rejected
signoff_by: human:淮政玮
signoff_at: YYYY-MM-DD
```

### 3.2 Handoff（必交）

路径：`agent-delivery/agent-handoffs/企业战略分析-ENT/ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md`

至少含：

- 决议：通过 / 驳回（附修改点）  
- 与 `architecture-baseline` 逐条对照（ADS / 调用链 / Nebula / MinIO）  
- 开放项列表（调度、bucket、失败策略等）  
- 对下游 S2/S3（sources·etl·stores 灌入）的放行或暂缓说明  
- 签字：`human:淮政玮`  
- `ponytail: off`

### 3.3 明确不做

- 不写 Java/Python/前端业务代码  
- 不修改 `data-design/企业/*` 旧稿  
- 不灌 `stores/mysql/*.md` as-built（属后续 data 单）  
- 不评审功能设计页

---

## 4. 认领状态（已执行）

| 角色 | 值 |
|---|---|
| `claimed_by` | **human:淮政玮** |
| `supervised_by` | **human:淮政玮** |
| registry | `claimed`（lock 至约 2026-08-15） |
| 知会 | 数据 Lead / GDF（流图通过后才开 sources·etl 灌数单） |

开工时将状态推到 `in_progress`；handoff 齐备后按 definition 路径推进。

---

## 5. DoD（与 registry 一致）

- [ ] `01-data-flow.md` 与架构基线一致（或有记录的偏离 + 批准）  
- [ ] 会签清单勾选；`signoff_status` + `signoff_by: human:淮政玮` + `signoff_at` 已填  
- [ ] handoff 落盘且含开放项与下游放行结论  
- [ ] 声明：未会签批准前，ENT `stores/*` 不得标 approved  

---

## 6. 下游预告（本单不执行）

```text
本单（流图会签 · 淮政玮）
  → S2 sources + etl 清单（data / GDF）
  → S3 stores 从现网 as-built 灌入（data-agent）
  → S4 旧路径 stub 指向 storage/ENT（coordinator）
```

---

## 7. 会话提示词（可贴 · 淮政玮执行）

```text
/goal ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01
执行人：human:淮政玮（已认领 · claimed_by/supervised_by=human:淮政玮）
协作：architect-agent 可辅助改稿与基线对照；会签签字权=淮政玮
强度：ponytail off
必读（按序）：
  1) data-design/storage/README.md
  2) data-design/storage/ENT/README.md
  3) data-design/storage/ENT/00-context.md
  4) data-design/storage/ENT/01-data-flow.md   ← 会签主件
  5) architecture-baseline.md
  6) data-design/storage/platform/minio.md
交付：
  - 审定并更新 01-data-flow.md（三图 + 触发/失败语义 + §4 清单）
  - frontmatter：signoff_status=approved|rejected，signoff_by=human:淮政玮，signoff_at=日期
  - handoff：agent-handoffs/企业战略分析-ENT/ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md
禁止：
  - 改旧 data-design/企业/*
  - 灌 stores as-built
  - 写业务代码 / 评审功能设计
完成后：状态推进 + 登记开放项与下游 S2/S3 放行结论
```
