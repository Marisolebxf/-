# METRIC-OPEN-SYNTH-VITALITY-核对记录
# SYNTH-MOD-VITALITY-METRIC-OPEN-L01 — 区域创新活力分析指标语义卡/开放项核对

> **任务**：SYNTH-MOD-VITALITY-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:王惠（口径主责）
> **算法共签**：human:唐绍祖（方案 B）
> **日期**：2026-08-11
> **上游**：SYNTH-MOD-VITALITY-PACK-L01 ✅ done
> **模块**：区域创新活力分析（E8-VITALITY）
> **算法库**：§10.5 区域创新活力综合分析模型

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ⚠️ 全部待闭合 | 5 个 metric 全部 mapping_status=🔧，公式 pending_algorithm |
| #5 开放项（PendingBadge + Popover） | ✅ 已登记 | Q-SYNTH-01/Q-SYNTH-V-01/Q-SYNTH-V-02 已登记；catalog 5 条 pending_hint 均 ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ⚠️ 通过 | metric ↔ definition ↔ source_tables 交叉检查完成；5 个指标均缺少完整算法公式 |
| 唐绍祖算法共签 | ✅ 已签署（2026-08-11） | 见 §6 |

> **关键判断**：本叶 5 个指标全部为算法依赖型（mapping_status=🔧），无统计型指标可直接闭合。核心阻塞项为 Q-SYNTH-01（活力指数综合评价模型无算法定义卡）和 Q-SYNTH-V-01（四维权重合计规则、阈值来源与合成公式展示口径）。当前阶段如实记录全部开放项，不伪闭合。一级维度以算法库科技/产业/人才/政策为准，废止旧 DEMO 主体/产出/投入/转化四维。

---

## §2 活力分析指标口径摘要（algorithm-agent）

### 2.1 指标清单

| metric_id | 中文名 | 定义 | 公式 | 状态 |
|-----------|--------|------|------|------|
| M_SYNTH_VIT_INDEX | 区域创新活力指数 | 四维加权求和合成的综合指数 | pending_algorithm | 🔧 Q-SYNTH-01 |
| M_SYNTH_VIT_DIM_SCORE | 四维单维评分 | 各维度内分项指标加权归一化 | pending_algorithm | 🔧 Q-SYNTH-V-01 |
| M_SYNTH_VIT_INDICATOR | 活力分项指标值与得分 | 四维下分项指标原始值与归一化得分 | pending_algorithm | 🔧 Q-SYNTH-01 |
| M_SYNTH_VIT_WEIGHT | 维度权重分布 | 四维在指数合成中的权重 | pending_algorithm | 🔧 Q-SYNTH-V-01 |
| M_SYNTH_VIT_RANK | 对比范围活力排名 | INDEX 计算结果排序 | 依赖 INDEX | 🔧 Q-SYNTH-01 |

### 2.2 数据依赖与算法边界

| 依赖项 | 影响指标 | 说明 |
|--------|---------|------|
| Q-SYNTH-01 | INDEX/INDICATOR/RANK | 活力指数综合评价模型无算法定义卡（指标体系正式清单/维度权重/归一化基准/指数合成公式） |
| Q-SYNTH-V-01 | DIM_SCORE/WEIGHT | 四维权重合计规则、阈值来源与产品侧计算方法展示口径 |
| Q-SYNTH-V-02 | 全部（共享） | 默认深圳/全国重点城市/最近3年是否与甲方正式一致（三叶共享） |
| 区域创新科技/产业/人才/政策专题库 | 全部 | ODS 表尚未建立，数据接入前保持 mock |

---

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS源表 | DWD表 | pending_ref | pending_hint |
|-----------|---------------|---------|-------|-------------|-------------|
| M_SYNTH_VIT_INDEX | 🔧 | — | — | Q-SYNTH-01 | 公式 pending_algorithm；区域创新科技/产业/人才/政策专题库 ODS 尚未建 |
| M_SYNTH_VIT_DIM_SCORE | 🔧 | — | — | Q-SYNTH-V-01 | 公式 pending_algorithm；权重合计规则与阈值来源待确认 |
| M_SYNTH_VIT_INDICATOR | 🔧 | — | — | Q-SYNTH-01 | 分项指标池待算法定义卡确认；专题库 ODS 尚未建 |
| M_SYNTH_VIT_WEIGHT | 🔧 | — | — | Q-SYNTH-V-01 | D1=missing；权重定义不存在 |
| M_SYNTH_VIT_RANK | 🔧 | — | — | Q-SYNTH-01 | D1=missing；排名依赖 INDEX 公式闭合 |

---

## §4 开放项闭合表

| 编号 | 关联 metric | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q-SYNTH-01 | INDEX/INDICATOR/RANK | 🟡 待算法 | TRACE-SYNTH-VITALITY #open_questions | 算法 Lead（唐绍祖）出定义卡 + 甲方确认 |
| Q-SYNTH-V-01 | DIM_SCORE/WEIGHT | 🟡 待算法 | TRACE-SYNTH-VITALITY #open_questions | 算法 Lead + 语义 Owner（王惠）确认权重/阈值/展示口径 |
| Q-SYNTH-V-02 | 全部（共享） | 🟡 待 PM | CT-SYN-CTX；DEC-VIT-BATCH-DEFAULT | PM 向甲方确认默认三元组 |

---

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 一级维度以算法库科技/产业/人才/政策为准 |
| PDR-05: 旧 SYNTH-REGION 维权体系废止 | ✅ | 旧主体/产出/投入/转化四维仅 historical_reference |
| PDR-06: metric ↔ definition 一致性 | ✅ | 5 个 metric 已在 cfg_metric-SYNTH-seed 注册 |
| PDR-06: source_tables 完整度 | ⚠️ | 全部 pending（专题库 ODS 尚未建） |
| PDR-06: pending_hint ≥80 字 | ✅ | 5 条全部达标 |

---

## §6 语义会签（方案 B 双签）

> 方案 B §1.4.2：口径主责 human:王惠；算法共签 human:唐绍祖

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-11 | ✅ 算法侧交付完成：5 指标 mapping_status 评估、全部如实标记🔧、Q-SYNTH-01/V-01 不伪闭合、旧维权体系已废止 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签说明：区域创新活力分析 5 个指标的 mapping_status 评估、数据缺口登记、开放项纪律（Q-SYNTH-01/V-01 不伪闭合）均与 bid-reference §10.5 及 TRACE-SYNTH-VITALITY 一致。一级维度以算法库科技/产业/人才/政策为准，旧 SYNTH-REGION 的主体/产出/投入/转化四维已废止为 historical_reference_only。全部 5 个指标为算法依赖型，公式 pending_algorithm，当前阶段如实记录开放项。