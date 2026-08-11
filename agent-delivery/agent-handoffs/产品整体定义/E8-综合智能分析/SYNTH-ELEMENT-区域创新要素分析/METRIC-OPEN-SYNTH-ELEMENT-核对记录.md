# METRIC-OPEN-SYNTH-ELEMENT-核对记录
# SYNTH-MOD-ELEMENT-METRIC-OPEN-L01 — 区域创新要素分析指标语义卡/开放项核对

> **任务**：SYNTH-MOD-ELEMENT-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:王惠（口径主责）
> **算法共签**：human:唐绍祖（方案 B）
> **日期**：2026-08-11
> **上游**：SYNTH-MOD-ELEMENT-PACK-L01 ✅ done
> **模块**：区域创新要素分析（E8-ELEMENT）
> **算法库**：§10.6-10.9（类型/层次/领域/综合四模型）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ⚠️ 全部待闭合 | 10 个 metric 全部 mapping_status=🔧，公式 pending_algorithm |
| #5 开放项（PendingBadge + Popover） | ✅ 已登记 | Q-SYNTH-02/E-01/E-02/E-04 已登记；catalog 10 条 pending_hint 均 ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ⚠️ 通过 | metric ↔ definition ↔ source_tables 交叉检查完成；10 个指标均缺少完整算法公式 |
| 唐绍祖算法共签 | ✅ 已签署（2026-08-11） | 见 §6 |

> **关键判断**：本叶 10 个指标全部为算法依赖型（mapping_status=🔧），无统计型指标可直接闭合。核心阻塞项为 Q-SYNTH-02（要素评价模型口径未定）和 Q-SYNTH-E-01（类型/层次/领域权重合计规则与合成公式）。要素对象清单以算法库七要素（人才/企业/政策/服务机构/科研机构/资金/空间）为准，废止旧 DEMO 四类（人才/资本/平台/项目）。Q-SYNTH-E-04（§10.6 输入列举缺资金/空间与正文七要素不一致）已登记。

---

## §2 要素分析指标口径摘要（algorithm-agent）

### 2.1 指标清单

| metric_id | 中文名 | 算法库 | 状态 |
|-----------|--------|--------|------|
| M_SYNTH_ELEM_INDEX | 区域创新要素指数（综合） | §10.9 | 🔧 Q-SYNTH-02 |
| M_SYNTH_ELEM_TYPE_INDEX | 区域创新要素类型指数 | §10.6 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_TYPE_SCORE | 七要素类型维得分 | §10.6 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_LEVEL_INDEX | 区域创新要素层次指数 | §10.7 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_LEVEL_SCORE | 七大结构层次评价 | §10.7 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_DOMAIN_INDEX | 区域创新要素领域指数 | §10.8 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_INDICATOR | 要素分项指标值与得分 | §10.6-10.9 | 🔧 Q-SYNTH-02 |
| M_SYNTH_ELEM_WEIGHT | 类型/层次/领域权重分布 | §10.9 | 🔧 Q-SYNTH-E-01 |
| M_SYNTH_ELEM_CONTRIB | 要素贡献度与影响路径 | §8.2.3 | 🔧 Q-SYNTH-E-02 |
| M_SYNTH_ELEM_RANK | 对比范围要素综合排名 | §10.9 | 🔧 Q-SYNTH-02 |

### 2.2 要素对象清单（七要素，算法库权威）

| id | name | 算法库出处 |
|----|------|-----------|
| talent | 创新人才 | §10.6 |
| enterprise | 企业 | §10.6 |
| policy | 政策 | §10.6 |
| service_org | 服务机构 | §10.6 |
| research_org | 科研机构 | §10.6 |
| capital | 资金 | §10.6（输入列举缺，见 Q-SYNTH-E-04） |
| space | 空间 | §10.6（输入列举缺，见 Q-SYNTH-E-04） |

旧 DEMO 四类（人才/资本/平台/项目）已废止为 historical_reference_only。

### 2.3 数据依赖与算法边界

| 依赖项 | 影响指标 | 说明 |
|--------|---------|------|
| Q-SYNTH-02 | INDEX/INDICATOR/RANK | 要素评价模型口径未定（分类字典、四维评价权重与阈值、影响关联算法） |
| Q-SYNTH-E-01 | TYPE_INDEX/TYPE_SCORE/LEVEL_INDEX/LEVEL_SCORE/DOMAIN_INDEX/WEIGHT | 类型/层次/领域权重合计规则、阈值来源与合成公式展示口径 |
| Q-SYNTH-E-02 | CONTRIB | 要素贡献路径/影响关联算法与可视化口径 |
| Q-SYNTH-E-04 | TYPE_INDEX/TYPE_SCORE/INDICATOR | §10.6 输入列举缺资金/空间与正文七要素一致性 |
| Q-SYNTH-V-02 | 全部（共享） | 默认三元组三叶共享 |

---

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | D3 | pending_ref | pending_hint |
|-----------|---------------|-----|-------------|-------------|
| M_SYNTH_ELEM_INDEX | 🔧 | n/a | Q-SYNTH-02 | D1=missing；公式不存在 |
| M_SYNTH_ELEM_TYPE_INDEX | 🔧 | n/a | Q-SYNTH-E-01 | D1=missing；七要素输入缺资金/空间 |
| M_SYNTH_ELEM_TYPE_SCORE | 🔧 | partial | Q-SYNTH-E-01 | 资金/空间数据缺口 |
| M_SYNTH_ELEM_LEVEL_INDEX | 🔧 | n/a | Q-SYNTH-E-01 | D1=missing；公式不存在 |
| M_SYNTH_ELEM_LEVEL_SCORE | 🔧 | partial | Q-SYNTH-E-01 | 结构维度定义待确认 |
| M_SYNTH_ELEM_DOMAIN_INDEX | 🔧 | n/a | Q-SYNTH-E-01 | D1=missing；知识图谱 ODS 未建 |
| M_SYNTH_ELEM_INDICATOR | 🔧 | partial | Q-SYNTH-02 | 资金/空间数据缺口 |
| M_SYNTH_ELEM_WEIGHT | 🔧 | n/a | Q-SYNTH-E-01 | D1=missing；权重定义不存在 |
| M_SYNTH_ELEM_CONTRIB | 🔧 | n/a | Q-SYNTH-E-02 | D1=missing；贡献度算法未定 |
| M_SYNTH_ELEM_RANK | 🔧 | n/a | Q-SYNTH-02 | D1=missing；排名依赖 INDEX |

---

## §4 开放项闭合表

| 编号 | 关联 metric | 当前状态 | 待闭合动作 |
|------|-----------|---------|-----------|
| Q-SYNTH-02 | INDEX/INDICATOR/RANK | 🟡 待算法 | 算法 Lead 出定义卡 + 甲方确认 |
| Q-SYNTH-E-01 | TYPE/LEVEL/DOMAIN/WEIGHT | 🟡 待算法 | 算法 Lead + 语义 Owner 确认权重/阈值/公式 |
| Q-SYNTH-E-02 | CONTRIB | 🟡 待算法 | 算法 Lead 确认贡献路径/影响关联算法 |
| Q-SYNTH-E-04 | TYPE_INDEX/TYPE_SCORE/INDICATOR | 🟡 待算法库 | §10.6 输入列举与正文七要素一致性确认 |

---

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 七要素清单以算法库为准 |
| PDR-05: 旧四类要素废止 | ✅ | 人才/资本/平台/项目仅 historical_reference |
| PDR-06: metric ↔ definition 一致性 | ✅ | 10 个 metric 已在 cfg_metric-SYNTH-seed 注册 |
| PDR-06: source_tables 完整度 | ⚠️ | 资金/空间数据缺口（Q-SYNTH-E-04） |
| PDR-06: pending_hint ≥80 字 | ✅ | 10 条全部达标 |

---

## §6 语义会签（方案 B 双签）

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-11 | ✅ 算法侧交付完成：10 指标 mapping_status 评估、全部如实标记🔧、Q-SYNTH-02/E-01/E-02/E-04 不伪闭合、旧四类已废止 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签说明：区域创新要素分析 10 个指标的 mapping_status 评估、数据缺口登记、开放项纪律均与 bid-reference §10.6-10.9 及 TRACE-SYNTH-ELEMENT 一致。要素对象清单以算法库七要素为准，旧 DEMO 四类已废止为 historical_reference_only。Q-SYNTH-E-04（§10.6 输入列举缺资金/空间）已登记，UI 仍按七要素展示并诚实标注输入缺口。全部 10 个指标为算法依赖型，公式 pending_algorithm。