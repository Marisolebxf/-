# SVC-DATA-ANALYSIS-L01 — 服务机构维度数据分析报告（handoff · v2.2 实查定论）

> **任务**：SVC-DATA-ANALYSIS-L01
> **执行人 / 监管人**：human:侯佳伟
> **认领类型**：coordinator_dispatch · claimed_by=human:侯佳伟
> **Epic**：E-ALGO-LIB-DEMO
> **仓**：agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`）
> **日期**：2026-08-05
> **状态**：🟡 integration（v2.2 实查定论后重新进入联调）

---

## 0. 版本演进说明

本报告经 4 轮迭代，每轮均基于新事实推翻前一轮假设：

| 版本 | 触发 | 核心修正 |
|------|------|---------|
| v1（作废） | 基于 Mapping v2 | 用 `dwd_org_reg_info`（0 行空表，已移出承诺） |
| v2.0（误判） | 监管人指出 reg_info 作废 | 改 `dwd_org_base_info`；误信承诺文档 xlsx 的 industry 字段 |
| v2.1（修正） | 监管人提供实际建表 DDL | industry 实际不存在，改 business_scope；但误用 org_type 作主准入 |
| **v2.2（实查定论，本版）** | **监管人提供 ODS 库直连，实查字段值分布** | **org_type 仅工商组织形式（无服务机构语义），主准入失效；district 正名（v2.1 误记 area）** |

---

## 1. 产出物清单（v2.2）

| 文件 | 路径 | 说明 |
|------|------|------|
| 数据分析报告 v2.2 | `data/data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md` | ODS 实查定论：industry❌ + org_type 不可用 + district 正名 + 四版变更对照附录 |
| 客户决策清单跟踪表 | `agent-delivery/客户决策清单跟踪表.md` §2.ae | v2.2：Q-SVC-001 升🔴、Q-SVC-004 正名 district、Q-SVC-008/009 更新、新增 Q-SVC-010（🔴阻断级） |
| 本 handoff | `agent-handoffs/服务机构-SVC/SVC-DATA-ANALYSIS-L01.md` | 本文件（v2.2 实查定论） |
| ODS 实查脚本 | `gkx-orchestration/scripts/probe-ods-base-info.py` | 直连 gkxlumenx_ods 查表结构+值分布（可复现） |
| task-registry.yaml | `agent-delivery/` | integration（v2.2 后保持） |

## 2. 范围证明

| 派单包要求 | v2.2 落点 | 完成 |
|------------|---------|------|
| §2.1 DWD 表设计方案 | 报告 §1（ODS 实查字段映射 + 六类打标签实查定论 + financing 表无承诺源处置） | ✅ |
| §2.2 服务机构指标 | 报告 §2（M1 六项重对齐 + M3 十项 + 八件套骨架更新） | ✅ |
| §2.3 第三方数据缺口 | 报告 §3（承诺表 live 状态 + 非承诺表标注 + 14项缺口矩阵） | ✅ |
| §2.4 问题或待决策项 | 报告 §4 + 决策清单 §2.ae（Q-SVC-001/004~010） | ✅ |

## 3. v2.2 关键发现（供签收人速读）

1. **industry 字段不存在（v2.1 已发现，v2.2 实查确认）**：承诺文档 xlsx 列了 industry 等7字段，实际 `dwd_org_base_info` 建表无任何 industry 字段（ODS 库 SHOW CREATE TABLE 确认）。
2. **🔴 org_type 不能用于服务机构准入（v2.2 新发现，推翻 v2.1）**：org_type 非空率 100%，但实查值分布——TOP 值全是"有限责任公司(自然人独资)""个人独资企业""事业单位"等**工商组织形式**，**无任何"检测/知识产权/研发/技术转移"等服务机构语义**。v2.1 的 R1''（org_type 主准入）作废。
3. **🔴 服务机构准入本身无可靠主路径（v2.2 核心结论）**：industry 不存在 + org_type 仅组织形式 + business_scope 自由文本质量不足 → 当前数据**既无法可靠圈定"哪些机构是服务机构"，更无法精确区分六类**。新增 Q-SVC-010（🔴 阻断级）。
4. **district 字段正名（v2.2 修正 v2.1）**：实际字段名是 `district`（varchar(50) 区县），不是 v2.1 写的 `area`。Q-SVC-004 仍可关闭。
5. **六类打标签唯一可用信号**：只剩 `business_scope`（非空率 99.1%），但自由文本质量参差，只能"尽力而为 + 人工复核"，UI 须带「待核验」角标，准确率有上限。
6. **incorporation_year 无直字段**：只有 incorporation_date(varchar)，需解析年份（M1 #4 从 ✅ 降为 🔧）。
7. **lng_lat 合并字段**：无 addr_lng/addr_lat 分字段，需拆分。
8. **投融资指标完全无源**：financing_info 和 invest_info 均移出 Wave A 承诺（维持 v2.0 结论）。

## 4. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | Java 只读 ADS | ✅ |
| 3 | 图谱 NebulaGraph | ✅ |
| 4 | 数据血缘 D9（八件套骨架，缺口标 ❌/⚠️，未伪闭合） | ✅ |
| 5 | 不替甲方拍板 | ✅（Q-SVC-010 阻断级交甲方+供方） |
| 6 | cicd: skip_design_only | ✅ |
| 7 | cost 四字段 | ✅ |
| 8 | **数据真源以 ODS 库实查为准（最权威）** | ✅ |

## 5. Cost（v2.2 累计）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 320_000 |
| actual_tokens | 290_000（v1 180k + v2.0 40k + v2.1 30k + v2.2 实查 40k） |
| model_used | zs-glm-5.2 |
| actual_cost | 1.00 |
| cost_warn | green |

## 6. 验证证据

- `SVC-DATA-ANALYSIS-L01-数据分析报告.md` v2.2 含四章 + 架构合规 + 依赖风险 + v1→v2.0→v2.1→v2.2 四版变更对照附录
- 报告基于 ODS 库直连实查（`gkxlumenx_ods.dwd_org_base_info` @ 111.198.38.90:34306，2026-08-05 human:侯佳伟 授权）
- 实查脚本 `scripts/probe-ods-base-info.py` 可复现（SHOW CREATE TABLE + COUNT + 字段值分布 + 非空率）
- `客户决策清单跟踪表.md` §2.ae 已更新（Q-SVC-001 升🔴 / 004 正名 district / 008-009 更新 / 010 新增）
- 本阶段 `cicd: skip_design_only`

## 7. 待会签 / 待办

| 项 | 责任 | 状态 |
|----|------|------|
| 报告 v2.2 review | human:侯佳伟 | ✅ 已完成（2026-08-05） |
| 任务发起人审核 | human:淮政玮 / 徐腾强 | 待审核 |
| **Q-SVC-010 阻断级决策**（准入无主路径） | PM / 甲方 / 供方 | 🔴 待决策（最高优先） |
| Q-SVC-009 industry 字段供方核验 | PM / 供应方 | 待确认 |
| D-1 算法说明文档落盘 | algorithm-agent（human:唐绍祖） | 待跟进 |
| Q-SVC-004 关闭确认 | PM | 待确认 |
| Q-SVC-005/006/007 甲方确认 | PM / 甲方 / 供应方 | 待确认 |
| ETL 基于 base_info 实施 | data-agent / algorithm-agent | 待实现波次 |

## 8. 开放项引用（决策清单 ID）

- 已存在：Q-ALGO-006（✅）、Q-SVC-002~003（🟡）、Q060~Q063（🟡）
- v2.2 升级：Q-SVC-001（🟡→🔴，准入无主路径）
- v2.2 正名：Q-SVC-004（🟢 可关闭，district 直字段）
- v2.2 更新：Q-SVC-005（实查确认 20000 行）、Q-SVC-008（仅 business_scope）、Q-SVC-009（实查确认）
- v2.2 新增：**Q-SVC-010（🔴 阻断级，准入无主路径，须甲方+供方共同决策）**
