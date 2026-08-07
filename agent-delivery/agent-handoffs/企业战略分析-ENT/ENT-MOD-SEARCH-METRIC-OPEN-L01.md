# ENT-MOD-SEARCH-METRIC-OPEN-L01 —— 企业查询指标语义与 ODS/DWD 数据缺口核对

> **任务**：ENT-MOD-SEARCH-METRIC-OPEN-L01
> **执行人**：algorithm-agent（human:唐绍祖）+ data-agent
> **口径主责**：human:王惠（方案 B §1.4.2）
> **日期**：2026-07-22（2026-07-30 目录修正；2026-08-05 实质瑕疵修复）
> **状态**：✅ 实质完工（待王惠口径会签后可签收）

---

## 1. 产出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| METRIC-OPEN-ENT-SEARCH-核对记录.md | agent-handoffs/产品整体定义/E1-企业查询/ | #4 适用性、指标矩阵(9条)、PDR-05/06 自检、方案B双签表 |
| ENT-SEARCH-data-gap-catalog.yaml | agent-handoffs/产品整体定义/E1-企业查询/ | UI 缺口文案溯源 ≥2 条 ≥80 字 pending_hint |
| cfg_metric-ENT-seed.yaml | agent-delivery/metrics/ | 检索相关条目已更新 & 8 件套字段 |

> 路径修正说明（2026-07-30）：核对记录原表误写为 `agent-handoffs/产品整体定义/`，实际位于 `agent-handoffs/产品整体定义/E1-企业查询/`（与 data-gap-catalog 同目录、与 task-registry evidence 一致）。本次按淮政玮反馈订正。

## 2. 2026-08-05 实质瑕疵修复（淮政玮 08-03 签收检查三项）

| # | 瑕疵 | 修复 |
|---|------|------|
| ① | Q037 错挂：决策清单=空态推荐≤30，核对/catalog 写成「明星企业定义」 | ✅ Q037 更正为「空态推荐≤30 条，不个性化」；明星定义改挂 Q041/Q048 |
| ② | §3 贴源矩阵仅 5 行，未对齐 catalog 9 条 | ✅ 补齐至 9 行（新增 M_ENT_DOMAIN_COVERAGE_BREADTH / M_ENT_SUPPLY_CHAIN_RISK / M_ENT_MARKET_SHARE / M_ENT_STAR_ENTERPRISE_COUNT） |
| ③ | 「12 metric」表述与 TRACE/catalog 不一致 | ✅ TRACE coverage_summary metrics_required=12 / metrics_mapped=11，核对记录 §1 已对齐「12 个 metric 中 11 个已映射，1 个待 Q019 闭合」 |

## 3. 范围证明

- ✅ 仅处理检索触点指标口径（非 NL 检索算法本身）
- ✅ 不替甲方闭合 Q033~Q037 最终业务口径
- ✅ 不包含 Java/Python 检索算法实现

## 4. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 仅改动 agent-delivery 文档,未动 demo 页面 | ✅ |
| 2 | metric 口径引用 PDR/Decision,非新拍板 | ✅ |
| 3 | pending_hint ≥80 字 | ✅ |
| 4 | 唐绍祖 §1.4.1 会签 | ✅ |
| 5 | cost 四字段已填写 | ✅ |
| 6 | 方案 B 双签：王惠口径会签 | ⏳ 待王惠签署 |

## 5. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 120_000 |
| actual_tokens | 85_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.52 |
| cost_warn | green |

## 6. 方案 B 双签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-05 | ✅ Q037 错挂已更正；§3 矩阵补齐至 9 条与 catalog 对齐 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

> 王惠口径会签 + 唐绍祖算法共签闭合后，状态可推进至 ready_to_sign。
