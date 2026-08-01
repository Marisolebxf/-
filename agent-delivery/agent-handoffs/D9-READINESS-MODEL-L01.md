# D9-READINESS-MODEL-L01 —— 指标四维就绪度模型草案 + ENT-EVAL 矩阵样例

> **任务**：D9-READINESS-MODEL-L01
> **执行**：agent:data-agent（监管 human:淮政玮）
> **日期**：2026-08-01
> **状态**：✅ 交付（草案性质；正式生效待会签）

---

## 1. 范围与实现

| 项 | 说明 |
|----|------|
| 背景 | 项目负责人 2026-08-01 决策：单一 `mapping_status` 混装四类语义，拆为四维正交模型（D1 定义对齐 / D2 项目内结构支撑 / D3 三方源映射 / D4 接入状态）并配套 UI 图标字典 |
| 与 bid 对照 | 不新增业务功能点；属 D9 数据血缘治理增强（评审/审计场景），范围 ±10% 无影响 |
| 消费方 | ENT-MOD-EVAL-READINESS-UI-L01（demo-ui-topic 落地）；后续各模块矩阵按同 schema 扩展 |

## 2. 产物清单

| 产物 | 路径 |
|------|------|
| v1.3 增补草案（模型 + 迁移映射 + 图标字典 + 会签待办） | `agent-delivery/designs/data-lineage-v1.3-readiness-draft.md` |
| ENT-EVAL 四维就绪度矩阵（13 指标填样，schema 内嵌） | `agent-delivery/metrics/metric-readiness-matrix-ENT-EVAL.yaml` |
| 本 handoff | `agent-delivery/agent-handoffs/D9-READINESS-MODEL-L01.md` |

## 3. 关键设计决策

1. **四维正交**：D2（自家结构，责任=架构师）与 D3（源覆盖，责任=甲方/GDF）分离，评审现场可直指责任方。
2. **D4 用阶段清单不用百分比**：ods_synced / dwd_loaded / es_indexed / graph_loaded / verified 五阶段，可验证可追责。
3. **⏳ OdsPendingBadge 不再单独实现**：语义并入 D3=pending_ods（IconClockCircle）。
4. **不伪闭合**：矩阵所有 D2 判定标 `provisional`，待 lineage-subcoord 核验；D3 引用 METRIC-OPEN-L01 结论，8/20 ODS 稳定后复判。
5. **不改写既有铁律**：评审模式 §5 位置字典、gap catalog 文案真源、❌ 不伪造数值、模块复核另轨——全部保持。

## 4. 偏离说明

- `Design.md` §7.4.1「四组件互斥优先级」与 UX §4.1/评审模式 §5 冲突：本草案建议改为「并存排列顺序」，**留待会签时一并修订**，本任务未直接改 Design.md（P0 文档，需 D8 流程）。
- 13 条 EVAL 指标的 D1 分布（aligned 5 / draft 8）与 L01 核对记录的 mapping_status 分布（2✅/8🔧/1❌/2⚠️）不是同一口径（四维拆分后 🔧 的「公式待实现」不再占状态位），已在矩阵 `legacy_mapping_status` 列保留对照。

## 5. 验收证据

- 矩阵 13/13 条覆盖 cfg_metric-ENT-seed EVAL 段全部 metric_id（E-23×7 / E-24×2 / E-30×4）
- 每条 D3 gap 摘要与 `ENT-EVAL-data-gap-catalog.yaml` 语义一致（长文案仍以 catalog 为准）
- cicd: skip_design_only（设计类，无 pipeline）

## 6. 架构合规自检（公约 §2 十条）

| # | 项 | 结果 |
|---|----|------|
| 1 | 算法只在 Python | ✅ N/A（无代码） |
| 2 | 调用链不越层 | ✅ N/A |
| 3 | NebulaGraph | ✅ 图 schema 仅作 D2 评估对象 |
| 4 | 可观测性 | ✅ N/A |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo2 只读 merge | ✅ N/A |
| 7 | 共享聚合核心 | ✅ Wave1 消费点定为 /metrics/v1/catalog |
| 8 | 数据策略（ADS 先行/Mock） | ✅ D4=mock 如实标注 |
| 9 | D8 前端规范 | ✅ 图标字典全 Arco Icon + 既有状态色 |
| 10 | D9 血缘 | ✅ 本任务即 D9 增强；文案真源不变 |
| 11 | D10 交互 | ✅ 入口层组件沿用既有交互契约 |

## 7. 开放项 / 会签待办

- [ ] 王惠：D1/D3 枚举与判定规则口径确认
- [ ] 唐绍祖：D2 与 formula_status 关系、D4 阶段清单确认
- [ ] 架构师：D2 判定权 + lineage-subcoord 核验流程确认
- [ ] 会签通过后：并入 data-lineage-policy.md（v1.3）+ 修订 Design.md §7.4.1 措辞
- [ ] 后续：其余模块矩阵按本 schema 扩展；飞书进度看板（用户已预告，另立任务）

## 8. Cost（registry 已回填）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 120_000 |
| actual_tokens | 100_000 |
| model_used | claude-fable-5 |
| actual_cost | 0.60 |
| cost_warn | green |
