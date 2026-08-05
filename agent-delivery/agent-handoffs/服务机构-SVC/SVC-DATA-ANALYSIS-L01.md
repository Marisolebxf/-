# SVC-DATA-ANALYSIS-L01 — 服务机构维度数据分析报告（handoff · v2 重写）

> **任务**：SVC-DATA-ANALYSIS-L01
> **执行人 / 监管人**：human:侯佳伟
> **认领类型**：coordinator_dispatch · claimed_by=human:侯佳伟
> **Epic**：E-ALGO-LIB-DEMO
> **仓**：agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`）
> **日期**：2026-08-05
> **状态**：🟡 integration（v2 重写后重新进入联调）

---

## 0. v2 重写说明

v1 基于 `服务机构相关-ODS到DWD字段映射分析报告(v2).md`，使用了已作废的表名 `dwd_org_reg_info`。监管人 human:侯佳伟 指出：最新国内机构主表是 `dwd_org_base_info`（见 GDF-ENT-WORKPACK-v1.2 命名词典 + Wave A 承诺40表 + Mapping v3）。v2 基于最新事实**全部重做**，不照搬 v1。

**v1 作废依据**：
- `01-命名与分层词典.md` v1.2 §2：承诺主表 `dwd_org_base_info`，`dwd_org_reg_info` 是旧名
- `02-WaveA-贴源表清单.yaml` line 126：`dwd_org_reg_info` 在 removed_vs_v1_1（"承诺主表为 dwd_org_base_info"）
- `09-企业维-ODS到DWD-Mapping说明-v3.md` §0：明确作废 Mapping v2
- `国内机构库-ODS到DWD字段映射分析报告.md`：`dwd_org_reg_info` live = 0 行空表

---

## 1. 产出物清单（v2）

| 文件 | 路径 | 说明 |
|------|------|------|
| 数据分析报告 v2 | `data/data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md` | 基于 base_info 体系重写四章 + 架构合规 + 依赖风险 + v1→v2 变更对照附录 |
| 客户决策清单跟踪表 | `agent-delivery/客户决策清单跟踪表.md` §2.ae | v2 修订：Q-SVC-004 可关闭、Q-SVC-005/006 更新、新增 Q-SVC-008 |
| 本 handoff | `agent-handoffs/服务机构-SVC/SVC-DATA-ANALYSIS-L01.md` | 本文件（v2 重写） |
| task-registry.yaml | `agent-delivery/` | integration（v2 重写后保持） |

## 2. 范围证明

| 派单包要求 | v2 落点 | 完成 |
|------------|---------|------|
| §2.1 DWD 表设计方案 | 报告 §1（base_info 重做字段映射 + 六类打标签新路径 + financing 表无承诺源处置） | ✅ |
| §2.2 服务机构指标 | 报告 §2（M1 六项重对齐 + M3 十项 + 八件套骨架更新） | ✅ |
| §2.3 第三方数据缺口 | 报告 §3（承诺表 live 状态 + 非承诺表标注 + 12项缺口矩阵） | ✅ |
| §2.4 问题或待决策项 | 报告 §4 + 决策清单 §2.ae（Q-SVC-004~008） | ✅ |

## 3. v2 关键发现（供签收人速读）

1. **主表修正**：`dwd_org_reg_info`（0行空表）→ `dwd_org_base_info`（20,000行）；Mapping v2 作废，用 v3。
2. **六类打标签不再阻断**：v1 依赖 product_info（空），v2 发现 base_info 自带 `industry`/`industry_l1_name` 字段（有数），可直接做主路径；product_info 空只影响"经营范围补判"，非阻断。
3. **投融资指标完全无源**：`financing_info` 和 `invest_info` 均移出 Wave A 承诺40表，M_SVC_INVEST_Y 从 v1 的"半边可算"降级为"❌ 无承诺源"。
4. **tag_info 移出承诺**：v1 的 R3 准入辅助规则作废；打标签规则改为 R1'(base_info.industry)+R2'(product_info 补判)+R3'(org_type 辅助)。
5. **district 不再是问题**：base_info 自带 `area` 直字段，Q-SVC-004 可关闭。
6. **org_size 无字段**：v1 误以为有，v2 确认 base_info 无 org_size（G8'）。
7. **新增 Q-SVC-008**：base_info.industry 做六类打标签需要码表对齐规则，待 algorithm-agent 出词典。

## 4. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | Java 只读 ADS | ✅ |
| 3 | 图谱 NebulaGraph | ✅ |
| 4 | 数据血缘 D9（八件套骨架，缺口标 ❌/⚠️，未伪闭合） | ✅ |
| 5 | 不替甲方拍板 | ✅ |
| 6 | cicd: skip_design_only | ✅ |
| 7 | cost 四字段 | ✅ |
| 8 | **数据真源以承诺表为准（不照搬 live 旧名）** | ✅ |

## 5. Cost（v2 累计）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 250_000 |
| actual_tokens | 220_000（v1 180k + v2 重写 40k） |
| model_used | zs-glm-5.2 |
| actual_cost | 0.75 |
| cost_warn | green |

## 6. 验证证据

- `SVC-DATA-ANALYSIS-L01-数据分析报告.md` v2 含四章 + 架构合规 + 依赖风险 + v1→v2 变更对照附录
- 报告基于 GDF-ENT-WORKPACK-v1.2 命名词典 + Wave A 承诺40表 + Mapping v3 重做
- `客户决策清单跟踪表.md` §2.ae 已更新（Q-SVC-004 可关闭 / 005-006 修订 / 008 新增）
- 本阶段 `cicd: skip_design_only`

## 7. 待会签 / 待办

| 项 | 责任 | 状态 |
|----|------|------|
| 报告 v2 review | human:侯佳伟 | ✅ 已完成（2026-08-05） |
| 任务发起人审核 | human:淮政玮 / 徐腾强 | 待审核 |
| D-1 算法说明文档落盘 | algorithm-agent（human:唐绍祖） | 待跟进 |
| Q-SVC-004 关闭确认 | PM | 待确认 |
| Q-SVC-005/006/007/008 甲方确认 | PM / 甲方 / 供应方 | 待确认 |
| ETL 基于 base_info 实施 | data-agent / algorithm-agent | 待实现波次 |

## 8. 开放项引用（决策清单 ID）

- 已存在：Q-ALGO-006（✅）、Q-SVC-001~003（🟡）、Q060~Q063（🟡）
- v2 修订：Q-SVC-004（🟢 可关闭）、Q-SVC-005（表名更新）、Q-SVC-006（扩展 financing）
- v2 维持：Q-SVC-007
- v2 新增：Q-SVC-008（industry 码表对齐）
