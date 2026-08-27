# 政策力度评分（M_POLICY_INTENSITY_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_INTENSITY_SCORE |
| 指标名称 | 政策力度评分 |
| 一级模块 | 政策分析 |
| 二级模块 | 政策深度分析 |
| 三级模块 | 政策力度评估 |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方QPOL-02 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QPOL-02 |


## 口径定义

在选定产业或技术领域范围内，对单条有效政策从效果、覆盖、成本三维综合评定的政策力度评分，取值0—100。

## 计算逻辑说明

三维字段与 `M_POLICY_INTENSITY_INDEX` 相同，粒度改为单条政策。指数按城市截面比，本指标按同对象、同统计年的政策截面比。未选定对象不计算。有效：`status=有效`，且 `expire_date` 为空或不早于统计日。去重键 `id`。三维互不共用同一计数。权重待 QPOL-02。

**第一步：确定命中有效政策集。** 产业或技术领域按四字段命中。

**第二步：单条政策原始值。**

1. **效果维**（实施是否启动、有没有支持方式）：

$$效果_i = \frac{1}{2}\bigl(I(implementation\_date\text{非空})+I(support\_way\text{至少1条非空})\bigr)$$

字段：`implementation_date`、`policy_support.support_way`。

2. **覆盖维**（该条政策的对象种类与是否落到区县；不再数省/市）：

$$覆盖_i = \text{COUNT(DISTINCT }support\_object\text{)}+I(district\text{非空})$$

字段：`policy_support.support_object`、`district`。空值不计入。

3. **成本维**（有扶持行为即视为有资源投入安排，无金额不编造拨款）：

$$成本_i = I(support\_behavior\text{至少1条非空})$$

字段：`policy_support.support_behavior`。

**第三步：同对象、同统计年政策截面标准化。** 各维 min-max 到 [0,1]，**公式内不乘 100**。全样本该维同值，或该条该维缺失，取 0.5。

$$得分_{i,j} = \frac{x_{i,j}-\min_{i'}(x_{i',j})}{\max_{i'}(x_{i',j})-\min_{i'}(x_{i',j})}$$

**第四步：综合分。** 先平均再 ×100：

$$政策力度评分_i = \frac{1}{3}(效果得分_i+覆盖得分_i+成本得分_i)\times 100$$

**第五步：缺失分支。** 三维原始值皆空不输出。同对象同统计年有效政策 \(N<3\) 标「样本不足」，仍出数但不得单独排名第一。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 政策力度评分 | 效果维度 | 该条实施日已填与支持方式已填的平均 | dwd_policy_base(implementation_date, policy_support.support_way) — 实施日, 支持方式 | 无 |
| 政策力度评分 | 覆盖维度 | 该条支持对象种类数 + 区县是否已填 | dwd_policy_base(policy_support.support_object, district) — 支持对象, 区县 | 无 |
| 政策力度评分 | 成本维度 | 该条扶持行为是否非空 | dwd_policy_base(policy_support.support_behavior) — 扶持行为 | support_amount-扶持金额 |

## 源表字段

- dwd_policy_base(id, implementation_date, district, status, expire_date, publish_year, title, keywords, keypoints, theme, policy_support) — 去重, 效果维实施日, 覆盖维区县, 有效, 失效, 同年截面, 四字段命中, 对象/行为/方式
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- support_amount-扶持金额（成本维正式口径；现行用 support_behavior 是否非空）

## 参考文献

政策力度评分+经济合作与发展组织+https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html
