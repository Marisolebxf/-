# INDEX · CHAIN 功能设计说明书（会议三点对照）

> **日期**：2026-08-06  
> **规程**：`产品定义评审规程.md` v2.7 §3.5  
> **存放约定**：正文与各叶子**交互五件套同目录**；本 INDEX 仅作跨叶子导航  
> **状态**：CMS 门户落位已收 v0.2；其余 FDS 仍为骨架

---

## 1. 会议交付 ↔ 工件

| # | 会议要求 | 工件（叶子同目录） | 状态 |
| --- | --- | --- | --- |
| 1 | 总览/全景：L0→L1→下钻；图谱控制边界 | [`CHAIN-PORTAL-OVERVIEW-产业链总览/FUNC-DESIGN-CHAIN-PORTAL-OVERVIEW-PANORAMA.md`](./CHAIN-PORTAL-OVERVIEW-产业链总览/FUNC-DESIGN-CHAIN-PORTAL-OVERVIEW-PANORAMA.md) | skeleton v0.1 |
| 2 | CMS 文案落位；不耦合算法层 | [`CHAIN-PORTAL-OVERVIEW-产业链总览/SPEC-CMS-CHAIN-PORTAL-CONTENT.md`](./CHAIN-PORTAL-OVERVIEW-产业链总览/SPEC-CMS-CHAIN-PORTAL-CONTENT.md) | v0.2-portal-only |
| 3 | 运行诊断：入口/参数/快照/导出个人中心 | [`CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/FUNC-DESIGN-CHAIN-TOPIC-DIAGNOSIS.md`](./CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/FUNC-DESIGN-CHAIN-TOPIC-DIAGNOSIS.md) | skeleton v0.1 |

---

## 2. 基准交互五件套（同目录共存）

| 模块 | 目录内容 |
| --- | --- |
| 门户总览 | `CHAIN-PORTAL-OVERVIEW-产业链总览/`：IA/TRACE/USM/Wireframe/UX-SPEC + DEC* + **FUNC-DESIGN** + **SPEC-CMS** |
| 专题全景（对照） | `CHAIN-TOPIC-PANORAMA-产业链全景图谱/`（本轮无独立 FDS） |
| 产业运行诊断 | `CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/`：交互五件套 + **FUNC-DESIGN** |

---

## 3. 任务登记建议（registry · 人工/coordinator）

| 建议 leaf | 依赖 | Evidence |
| --- | --- | --- |
| `CHAIN-PORTAL-OVERVIEW-FDS-L01` | UX-L01（总览） | 总览目录 FUNC-DESIGN + SPEC-CMS |
| `CHAIN-TOPIC-DIAGNOSIS-FDS-L01` | UX-L01（诊断） | 诊断目录 FUNC-DESIGN |

> 不自动 merge task-registry；按需 `task-create`。

---

## 4. 下一步填充顺序

1. 总览/全景 §3～§4 与 UX-SPEC 逐条对齐 + §6 结构 API 示例  
2. CMS block_key 与 Wireframe 终表 + 会签「不耦合算法」  
3. 诊断 §3.2 字段表 + §4/§5 快照与个人中心 API  
4. 架构抽检 → 升骨架为 v1.0  
