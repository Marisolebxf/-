# 派单包：SVC-DATA-ANALYSIS-L01 — 服务机构维度数据分析报告

- **任务 ID**：SVC-DATA-ANALYSIS-L01
- **派发角色**：coordinator-agent（PM 确认：草案 B + P1）
- **承接角色**：data-agent
- **监管人**：human:侯佳伟
- **认领**：`claimed` · `coordinator_dispatch` · `claimed_by=agent:data-agent`
- **锁定窗口**：认领起 +4h（见 registry `lock_until`）
- **Epic**：E-ALGO-LIB-DEMO
- **仓**：`agent-delivery`（编排资产；`cicd: skip_design_only`）
- **effort / difficulty**：8 / L · est.tokens 250k
- **派发时间**：2026-08-04

---

## 1. 背景

专题服务系统 **服务机构维度**需先做数据分析，再进入实现波次。算法侧已有 `SVC-ALGO-DESIGN-L01`（§9 十模型设计）；数据侧已有 DWD v1 底稿与 Mapping v2，但缺一份可验收的**数据分析报告**（设计复核 + 指标 + 三方缺口 + 待决策）。

本任务只出报告与决策清单回填，不写 Java/前端、不强制 ETL/ADS 灌数。

---

## 2. 范围（必做）

报告路径：

`agent-delivery/data/data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md`

### 2.1 DWD 表设计方案

- 以 `服务机构域数据库设计(v1).md` + Mapping v2 为起点复核/修订
- 写清：表清单、主键/业务键、分层（ODS→DWD→ADS）、与 ENT/ORG 交叉边界
- 偏离 v1 须 as-built 说明

### 2.2 服务机构指标

- 对齐招标 `科技专题服务算法库.md` 服务机构相关章节
- 对齐 `SVC-ALGO-DESIGN-L01` 模型数据依赖
- 尽量给出 metric_id / 口径要点（D9 八件套可先列骨架，缺口径标 🟡）

### 2.3 第三方数据缺口

- 对照 `gkx-mysql-raw`、机构要素库清单、Mapping v2
- 按「有无表 / 有无行 / 关键字段缺失」列缺口矩阵

### 2.4 问题或待决策项

- 回填 `客户决策清单跟踪表.md`
- **禁止**替甲方拍板业务口径

---

## 3. 必读

| 文件 | 用途 |
|------|------|
| `data/data-design/服务机构/服务机构域数据库设计(v1).md` | DWD 底稿 |
| `data/GDF/Mapping/服务机构/服务机构相关-ODS到DWD字段映射分析报告(v2).md` | 字段映射 |
| `bid-reference/科技专题服务算法库.md` | 需规范围 |
| `agent-handoffs/算法库联调-ALGO-LIB/SVC-ALGO-DESIGN-L01.md` | 算法依赖交叉 |
| `data-lineage-policy.md` | D9 血缘 |
| `客户决策清单跟踪表.md` | 开放项登记 |
| `architecture-baseline.md` | 架构铁律 |

---

## 4. DoD

见 `task-registry.yaml#SVC-DATA-ANALYSIS-L01.definition_of_done`。

完工 handoff：`agent-handoffs/服务机构-SVC/SVC-DATA-ANALYSIS-L01.md`（含 cost 四字段）。

---

## 5. /goal 话术（复制到新会话）

```markdown
/goal data-agent
身份：你是经验丰富的数据工程师 / 数据架构师，精通 ODS→DWD→ADS 分层、指标血缘（D9）与三方源缺口分析。
任务 ID：SVC-DATA-ANALYSIS-L01
监管人：human:侯佳伟
认领类型：coordinator_dispatch
仓：agent-delivery（仅文档/数据设计资产；cicd skip_design_only）
必读：本派单包 + 服务机构域数据库设计(v1) + Mapping v2 + 科技专题服务算法库.md + SVC-ALGO-DESIGN-L01 + data-lineage-policy.md + 客户决策清单跟踪表.md
目标：输出服务机构维度数据分析报告（四章：DWD表设计方案、服务机构指标、第三方数据缺口、问题或待决策项）；开放项回填决策清单；不得替甲方拍板；不写 Java/前端、不强制 ETL 灌数。
完工：handoff agent-handoffs/服务机构-SVC/SVC-DATA-ANALYSIS-L01.md + cost 四字段；status→review。
```
