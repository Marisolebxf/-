# SVC-DATA-ANALYSIS-L01 — 服务机构维度数据分析报告（handoff）

> **任务**：SVC-DATA-ANALYSIS-L01
> **执行人 / 监管人**：human:侯佳伟
> **认领类型**：coordinator_dispatch · claimed_by=human:侯佳伟
> **Epic**：E-ALGO-LIB-DEMO
> **仓**：agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`）
> **日期**：2026-08-05
> **状态**：🟡 ready_to_sign（待任务发起人淮政玮/徐腾强审核签收）

---

## 1. 产出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 数据分析报告 | `data/data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md` | 四章主交付：DWD 复核 / 指标 / 缺口 / 待决策 + 架构合规 + 依赖风险 + 附录对照全表 |
| 客户决策清单跟踪表 | `agent-delivery/客户决策清单跟踪表.md` | 新增 §2.ae：Q-SVC-005 / Q-SVC-006 / Q-SVC-007（🟡） |
| 本 handoff | `agent-handoffs/服务机构-SVC/SVC-DATA-ANALYSIS-L01.md` | 本文件 |
| task-registry.yaml | `agent-delivery/` | claimed → review → ready_to_sign，evidence/cost 回填（经 MCP） |

## 2. 范围证明（对照派单包 §2 必做）

| 派单包要求 | 本报告落点 | 完成 |
|------------|-----------|------|
| §2.1 DWD 表设计方案（表清单/主键/分层/与 ENT 边界/偏离 as-built） | 报告 §1（复核结论 + 3 处补强 + 表清单 + 主键边界） | ✅ |
| §2.2 服务机构指标（对齐 bid + SVC-ALGO-DESIGN + metric_id/口径骨架） | 报告 §2（M1 六项 + M3 十项 + 八件套骨架 2 例） | ✅ |
| §2.3 第三方数据缺口（有无表/有无行/关键字段缺失矩阵） | 报告 §3（现状表 + 12 项缺口矩阵 + 三级分级） | ✅ |
| §2.4 问题或待决策项（回填决策清单，不替甲方拍板） | 报告 §4 + 决策清单 §2.ae（新增 3 项） | ✅ |

## 3. 关键发现（供签收人速读）

1. **DWD v1 可承接**：v1.0.0 设计无颠覆性修订，仅 3 处补强（product_info 空表退化规则 / invest_info 未承诺兜底 / 旁路命名归一）。
2. **指标两层 16 项**：M1 基础 6 项（对齐 bid §4.1.1.1.1.1.1.1.4）+ M3 深度 10 项（对齐 bid §4.1.1.1.1.1.1.9）；M1 可算路径用真数，缺口路径标 🧪/⚠️。
3. **三方缺口 12 项**：3 项 🔴 阻断（product/tags 空 + invest 未承诺 + 服务质量/案例无源），2 项 ⚠️ 样例，其余 🟡 待定。
4. **新增 3 项决策**：Q-SVC-005（量级口径）/ Q-SVC-006（invest Wave B）/ Q-SVC-007（服务质量/案例三方源）；均已给临时默认，不阻塞。
5. **依赖缺口 D-1（高风险）**：SVC-ALGO-DESIGN-L01 handoff 声称产出的 `docs/产业服务算法设计说明.md` 在 `demo-algo-ent-analysis` 仓内**查无实体文件**；本报告 §2.3 口径要点来自 bid 原文 + handoff 声称的 model_id，建议 coordinator 跟进 algorithm-agent 补落盘。

## 4. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python（本报告为数据设计，未涉及 Java 算法） | ✅ |
| 2 | Java 只读 ADS（SVC 指标经 gkxlumen-metrics） | ✅ |
| 3 | 图谱 NebulaGraph（gkx_service，未引入 Neo4j） | ✅ |
| 4 | 数据血缘 D9（八件套骨架，缺口径标 🟡，未伪闭合） | ✅ |
| 5 | 不替甲方拍板（所有歧义登记决策清单） | ✅ |
| 6 | cicd: skip_design_only | ✅ |
| 7 | cost 四字段已填写 | ✅ |

## 5. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 250_000 |
| actual_tokens | 180_000 |
| model_used | zs-glm-5.2 |
| actual_cost | 0.60 |
| cost_warn | green |

## 6. 验证证据

- `data/data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md` 含四章 + 架构合规 + 依赖风险 + 附录对照全表；M1 6 项 + M3 10 项 + 缺口 12 项 + 决策 11 项（含新增 3 项）
- `客户决策清单跟踪表.md` §2.ae 已登记 Q-SVC-005 / Q-SVC-006 / Q-SVC-007，状态 🟡
- 本阶段 `cicd: skip_design_only`，不强制 CI

## 7. 待会签 / 待办

| 项 | 责任 | 状态 |
|----|------|------|
| 报告 review | human:侯佳伟 | ✅ 已完成（2026-08-05） |
| 任务发起人审核 | human:淮政玮 / 徐腾强 | 待审核 |
| D-1 算法说明文档落盘 | algorithm-agent（human:唐绍祖） | 待跟进 |
| Q-SVC-005/006/007 甲方确认 | PM / 甲方 / 供应方 | 待确认 |
| ETL 退化规则 + cfg_metric 注册 | data-agent / algorithm-agent | 待实现波次 |

## 8. 开放项引用（决策清单 ID）

- 已存在：Q-ALGO-006（✅）、Q-SVC-001~004（🟡）、Q060~Q063（🟡）
- 本任务新增：Q-SVC-005 / Q-SVC-006 / Q-SVC-007（🟡）
