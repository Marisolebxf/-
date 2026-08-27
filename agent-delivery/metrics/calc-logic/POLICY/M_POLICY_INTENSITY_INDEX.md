# 政策力度指数（M_POLICY_INTENSITY_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_INTENSITY_INDEX |
| 指标名称 | 政策力度指数 |
| 一级模块 | 政策分析 |
| 二级模块 | 政策扶持门户 |
| 三级模块 | 政策力度排名 |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方QPOL-02 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QPOL-02 |


## 口径定义

在选定产业或技术领域范围内，按城市从效果、覆盖、成本三维综合评定的政策力度指数，取值0—100。

## 计算逻辑说明

**第一步：落到对比城市。** 配置页选定一条产业链或已勾选的技术领域；未选定不计算。国内政策库中标题或关键词点到该对象、统计日仍有效的政策（`status=有效`，且 `expire_date` 为空或不早于运行日）。对比单位是城市：`city` 含该市名即计入该市。`rank` 含国家级的政策可计入每个对比市。去重键 `id`。该市有效政策数为 \($N_c$\)，\(N_c=0\) 则该市三维原始值缺失。

**第二步：三维原始值（只用库内字段，三维互不共用同一计数）。**

1. **效果维**（实施是否启动、有没有支持方式）：

$$效果_c = \frac{1}{2}\left(\frac{\text{COUNT}(implementation\_date\text{非空})}{N_c}+\frac{\text{COUNT}(support\_way\text{至少1条非空})}{N_c}\right)$$

字段：`implementation_date`、`policy_support.support_way`。

2. **覆盖维**（该市内部的对象广度与区县广度；不再数省/市，城市粒度下省/市去重无意义）：

$$覆盖_c = \text{COUNT(DISTINCT }support\_object\text{)}+\text{COUNT(DISTINCT }district\text{)}$$

字段：`policy_support.support_object`、`district`。空值不计入。国家级政策无区县时只贡献对象种类。

3. **成本维**（有扶持行为即视为有资源投入安排，无金额不编造拨款）：

$$成本_c = \frac{\text{COUNT}(support\_behavior\text{至少1条非空})}{N_c}$$

字段：`policy_support.support_behavior`。

**第三步：对比城市截面标准化。** 集合 \(C\) 为本次勾选的对比城市。各维原始值 min-max 到 [0,1]，**公式内不乘 100**：

$$得分_{c,j} = \frac{x_{c,j}-\min_{c'\in C}(x_{c',j})}{\max_{c'\in C}(x_{c',j})-\min_{c'\in C}(x_{c',j})}$$

全市该维同值，或该市该维缺失，则该维得分取 0.5。

**第四步：综合分。** 三维等权（权重待 QPOL-02）。先平均再 ×100，指数为 0—100：

$$政策力度指数_c = \frac{1}{3}(效果得分_c+覆盖得分_c+成本得分_c)\times 100$$

**第五步：缺失分支。** \($N_c=0$\) 该市不输出指数。件数少不用占比冒充力度：\(N_c<3\) 时该市指数标「样本不足」，仍出数但不得单独排名第一。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 政策力度指数 | 效果维度 | 实施日已填占比与支持方式已填占比的平均 | dwd_policy_base(implementation_date, policy_support.support_way) | 无 |
| 政策力度指数 | 覆盖维度 | 支持对象种类数 + 区县去重数 | dwd_policy_base(policy_support, district) | 无 |
| 政策力度指数 | 成本维度 | 有扶持行为命中的占比 | dwd_policy_base(policy_support.support_behavior) | 无 |

## 源表字段

- dwd_policy_base(id, rank, city, district, status, expire_date, implementation_date, title, keywords, keypoints, theme, policy_support) — 去重, 国家级计入各市, 对比城市, 区内覆盖, 有效, 失效, 实施是否启动, 四字段命中, 扶持对象/行为/方式
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- support_amount-扶持金额（成本维正式口径；现行用 support_behavior 非空占比）
