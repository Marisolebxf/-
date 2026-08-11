# METRIC-OPEN-SYNTH-COLLAB-核对记录
# SYNTH-MOD-COLLAB-METRIC-OPEN-L01 — 区域创新协同分析指标语义卡开放项核对

> **任务**：SYNTH-MOD-COLLAB-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:王惠（口径主责）
> **算法共签**：human:唐绍祖（方案 B）
> **日期**：2026-08-11
> **上游**：SYNTH-MOD-COLLAB-PACK-L01 ✅ done
> **模块**：区域创新协同分析（E8-COLLAB）
> **算法库**：§10.10 区域创新协同分析模型

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ⚠️ 全部待闭合 | 6 个 metric 全部 mapping_status=🔧，公式 pending_algorithm |
| #5 开放项（PendingBadge + Popover） | ✅ 已登记 | Q-SYNTH-03/C-01~C-05 已登记；catalog 6 条 pending_hint 均 ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ⚠️ 通过 | metric ↔ definition ↔ source_tables 交叉检查完成；6 个指标均缺少完整算法公式 |
| 唐绍祖算法共签 | ✅ 已签署（2026-08-11） | 见 §6 |

> **关键判断**：本叶 6 个指标全部为算法依赖型（mapping_status=🔧），无统计型指标可直接闭合。核心阻塞项为 Q-SYNTH-C-01（完整度/中心度/密度的正式分母、图类型、边去重加权口径）和 Q-SYNTH-C-02（三指标标准化、权重、校准窗口、集群/孤立判据）。旧 SYNTH-REGION 遗漏完整度指标的问题已修正（新增 M_SYNTH_COLLAB_COMPLETENESS）。旧演示态以密度×强度合成协同指数已废止，仅允许三指标归一等权作为明确标注的临时演示口径。

---

## §2 协同分析指标口径摘要（algorithm-agent）

### 2.1 指标清单

| metric_id | 中文名 | 临时公式 | 正式公式 | 状态 |
|-----------|--------|---------|---------|------|
| M_SYNTH_COLLAB_COMPLETENESS | 协同网络完整度 | 有关系主体数/有效主体总数×100% | pending_algorithm | 🔧 Q-SYNTH-C-01 |
| M_SYNTH_COLLAB_CENTRALITY | 协同网络中心度 | degree/(N-1) | pending_algorithm | 🔧 Q-SYNTH-C-01 |
| M_SYNTH_COLLAB_DENSITY | 协同网络密度 | 2E/[N×(N-1)] | pending_algorithm | 🔧 Q-SYNTH-C-01 |
| M_SYNTH_COLLAB_INDEX | 区域创新协同指数 | 三指标归一等权 | pending_algorithm | 🔧 Q-SYNTH-C-02 |
| M_SYNTH_COLLAB_RELATION_INPUT | 协同关系输入统计 | COUNT(DISTINCT event_id) GROUP BY type | 已定义（SQL） | 🔧 Q-SYNTH-C-01 |
| M_SYNTH_COLLAB_OUTPUT_CORR | 协同—创新产出关联结果 | 演示数据集相关系数 | pending_algorithm | 🔧 Q-SYNTH-C-03 |

### 2.2 禁止项

- ✅ **废止密度×强度**：旧演示态以密度×强度合成协同指数已废止为权威；仅允许三指标归一等权作为明确标注的临时演示口径
- ✅ **完整度不得遗漏**：旧 SYNTH-REGION 指标目录遗漏完整度，本叶新增 M_SYNTH_COLLAB_COMPLETENESS 并贯穿 TRACE/USM/UX/Wireframe
- ✅ **关联结果禁止因果表述**：演示数据集只给关联描述，样本不足不画线、不出系数

### 2.3 数据依赖与算法边界

| 依赖项 | 影响指标 | 说明 |
|--------|---------|------|
| Q-SYNTH-C-01 | COMPLETENESS/CENTRALITY/DENSITY/RELATION_INPUT | 正式分母、图类型、边去重加权、子图筛选与聚合口径 |
| Q-SYNTH-C-02 | INDEX | 三指标标准化、权重、校准窗口、集群/孤立判据 |
| Q-SYNTH-C-03 | OUTPUT_CORR | 产出指标、样本粒度、相关方法与最小样本数 |
| Q-SYNTH-C-05 | RELATION_INPUT | 产业领域筛选 taxonomy、主体标签映射、ODS→DWD 字段可用性 |
| Q-SYNTH-V-02 | 全部（共享） | 默认三元组三叶共享 |
| pending_ods_* | COMPLETENESS/CENTRALITY/DENSITY/RELATION_INPUT | ODS 表尚未建 |

---

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | D3 | pending_ref | pending_hint |
|-----------|---------------|-----|-------------|-------------|
| M_SYNTH_COLLAB_COMPLETENESS | 🔧 | pending_ods | Q-SYNTH-C-01 | pending_ods_cooperation_subject/relation 表未建 |
| M_SYNTH_COLLAB_CENTRALITY | 🔧 | pending_ods | Q-SYNTH-C-01 | pending_ods_cooperation_subject/relation 表未建 |
| M_SYNTH_COLLAB_DENSITY | 🔧 | pending_ods | Q-SYNTH-C-01 | pending_ods_cooperation_subject/relation 表未建 |
| M_SYNTH_COLLAB_INDEX | 🔧 | n/a | Q-SYNTH-C-02 | D1=missing；公式不存在 |
| M_SYNTH_COLLAB_RELATION_INPUT | 🔧 | pending_ods | Q-SYNTH-C-01 | pending_ods_joint_patent/cooperation_project/talent_flow 表未建 |
| M_SYNTH_COLLAB_OUTPUT_CORR | 🔧 | n/a | Q-SYNTH-C-03 | D1=missing；相关方法/样本门槛未定 |

---

## §4 开放项闭合表

| 编号 | 关联 metric | 当前状态 | 待闭合动作 |
|------|-----------|---------|-----------|
| Q-SYNTH-03 | 全部（总开放项） | 🟡 待算法 | 算法 Lead 出定义卡 + 语义 Owner + 甲方确认 |
| Q-SYNTH-C-01 | COMPLETENESS/CENTRALITY/DENSITY/RELATION_INPUT | 🟡 待算法 | 算法 Lead + 语义 Owner 确认分母/图类型/边权/聚合口径 |
| Q-SYNTH-C-02 | INDEX | 🟡 待算法 | 算法 Lead + 语义 Owner + 甲方确认标准化/权重/校准/判据 |
| Q-SYNTH-C-03 | OUTPUT_CORR | 🟡 待算法 | 算法 Lead + 语义 Owner + 甲方确认关联方法/样本门槛 |
| Q-SYNTH-C-04 | 策略建议 | 🟡 待产品 | 产品 Owner + 算法 Lead + 甲方确认建议生成/审核边界 |
| Q-SYNTH-C-05 | RELATION_INPUT | 🟡 待 GDF | GDF + data-agent + 语义 Owner 确认 taxonomy/字段可用性 |

---

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 三叶合规节点全覆盖 |
| PDR-05: 完整度指标新增 | ✅ | M_SYNTH_COLLAB_COMPLETENESS 贯穿 TRACE/USM/UX/Wireframe |
| PDR-06: metric ↔ definition 一致性 | ✅ | 6 个 metric 已在 cfg_metric-SYNTH-seed 注册 |
| PDR-06: 密度×强度废止 | ✅ | 仅允许三指标归一等权作为临时演示 |
| PDR-06: pending_hint ≥80 字 | ✅ | 6 条全部达标 |

---

## §6 语义会签（方案 B 双签）

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-11 | ✅ 算法侧交付完成：6 指标 mapping_status 评估、全部如实标记🔧、Q-SYNTH-03/C-01~C-05 不伪闭合、密度×强度已废止、完整度已新增 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签说明：区域创新协同分析 6 个指标的 mapping_status 评估、数据缺口登记、开放项纪律均与 bid-reference §10.10 及 TRACE-SYNTH-COLLAB 一致。旧 SYNTH-REGION 遗漏完整度指标的问题已修正。旧演示态以密度×强度合成协同指数已废止为权威，仅允许三指标归一等权作为明确标注的临时演示口径。全部 6 个指标为算法依赖型，公式 pending_algorithm。