# 政策效果推演（M_POLICY_SIMULATE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_SIMULATE |
| 指标名称 | 政策效果推演 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | - |
| 更新频率 | 日 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QPOL-02 |

## 口径定义

以省级政策力度指数为基线，对「扶持力度」「覆盖面」等参数化情景做弹性推演，输出基线值、模拟值、增量与变化曲线。对象=政策（区域/产业/主题粒度），基线=省级力度指数，输出=`ads.policy_simulate(baseline_value, simulated_value, delta_rate, curve)`。情景与弹性系数待 QPOL-02 确认。

## 计算逻辑说明

采用「基线 + 弹性推演」两步：先取省级政策力度指数为基线，再对扶持力度、覆盖面等情景参数按弹性系数外推模拟效果值。

### 第一步：确定基线（省级力度指数）

取 `policy_intensity` 中 `scope_type='province'`（或 `rank_no` 对应省级）的 `intensity_index` / `intensity_score` 为基线 `B`。若无省级，按 `rank_no` 取全局力度指数分位。

```sql
SELECT scope_code, scope_name, intensity_index, intensity_score, rank_no, calc_batch_id
FROM gkx.policy_intensity
WHERE scope_type = 'province'
ORDER BY intensity_index DESC;
```

### 第二步：参数化情景设定

情景由 `policy_simulation_param` 承载：扶持力度 `support_intensity`、覆盖面 `coverage_scope`、政策类型 `policy_type`、实施时间 `implementation_time`。情景为参数化假设值（QPOL-02 待定）。

### 第三步：弹性推演

以弹性系数 `e`（待 QPOL-02）将情景参数相对基线的变化率映射为效果变化率：

$$
\Delta Y = e \cdot \frac{X_{sim} - X_{base}}{X_{base}}
$$

$$
Y_{sim} = B \times (1 + \Delta Y)
$$

其中 `X` 为情景参数（扶持力度/覆盖面），`Y` 为推演效果，`e` 为弹性系数。预测区间取 `policy_prediction_indicator.predicted_upper / predicted_lower`。

### 第四步：写表

输出 `ads.policy_simulate(scenario_id, scope_type, scope_code, params, baseline_value, simulated_value, delta_rate, curve, model_version, calc_batch_id)`。

```sql
-- 弹性推演示意
SELECT b.scope_code,
       b.intensity_index AS baseline_value,
       ROUND(b.intensity_index * (1 + :e * (:support_sim - :support_base) / NULLIF(:support_base,0)), 4) AS simulated_value,
       ROUND(:e * (:support_sim - :support_base) / NULLIF(:support_base,0), 4) AS delta_rate
FROM gkx.policy_intensity b
WHERE b.scope_type = 'province';
```

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策效果推演 | 基线力度 | 省级政策力度指数 | 以省级力度指数为推演基线。 | B = policy_intensity.intensity_index(省级) | policy_intensity(scope_type, scope_code, scope_name, intensity_index, intensity_score, industry_coverage, rank_no, metric_id, calc_batch_id) — 政策力度指数基线 | 无 |
|  | 扶持力度情景 | 扶持力度参数情景 | 对政策扶持力度做参数化情景设定。 | X = support_intensity 情景值 | policy_simulation_param(simulation_id, policy_type, coverage_scope, support_intensity, implementation_time, simulation_dimensions, custom_params) — 仿真参数 | 仿真参数实际数据（现表 0 行） |
|  | 覆盖面情景 | 覆盖面参数情景 | 对政策覆盖对象/区域范围做参数化情景设定。 | X = coverage_scope 情景值 | policy_simulation_param(simulation_id, coverage_scope, simulation_dimensions) — 覆盖面参数；policy_intensity(scope_code, industry_coverage) — 现有覆盖度 | 覆盖面情景实际数据（现表 0 行） |
|  | 弹性推演结果 | 效果变化率与预测区间 | 弹性系数外推效果值与变化率、预测上下界。 | ΔY=e·ΔX/X；Y_sim=B·(1+ΔY) | policy_prediction_indicator(simulation_id, indicator_name, base_value, predicted_value, predicted_upper, predicted_lower, change_rate, prediction_period) — 预测指标；policy_intensity_eval(policy_id, intensity_index, effect_score, coverage_score, cost_score, intensity_level, rank_province) — 力度评估明细 | 弹性系数表(QPOL-02)；预测指标实际数据（现表 0 行）；policy_intensity_eval 实际数据（现表 0 行） |

## 源表字段

- policy_intensity(scope_type, scope_code, scope_name, intensity_index, intensity_score, industry_coverage, rank_no, metric_id, calc_batch_id) — 省级政策力度指数基线（有数据）
- policy_intensity_eval(policy_id, eval_batch_no, intensity_index, effect_score, coverage_score, cost_score, intensity_level, rank_nationwide, rank_province) — 政策力度评估明细（表结构存在，0 行）
- policy_simulation_param(simulation_id, simulation_type, policy_id, policy_type, coverage_scope, support_intensity, implementation_time, simulation_dimensions, custom_params) — 政策仿真参数（表结构存在，0 行）
- policy_prediction_indicator(simulation_id, indicator_name, indicator_category, base_value, predicted_value, predicted_upper, predicted_lower, change_rate, prediction_period) — 推演预测指标（表结构存在，0 行）
- policy_simulation_result(simulation_id, result_type, result_summary, quantitative_result, spatial_distribution, temporal_trend, visualization_data, confidence_level) — 政策仿真结果（表结构存在，0 行）
- dwd_policy_base(id, title, type, province, city, rank, publish_date, status, is_deleted) — 政策基础信息（情景对象）

## 待建字段

- 弹性系数表（QPOL-02）：扶持力度/覆盖面情景相对效果变化的弹性系数 `e`，现库无系数参数表。
- `policy_simulation_param`、`policy_prediction_indicator`、`policy_intensity_eval`、`policy_simulation_result` 的实际数据（现均 0 行，仅表结构）。

## 参考资料

[1] 政策效果推演.md｜序号 232—242（未出台政策仿真模拟：用户输入政策类型、覆盖范围、支持力度、实施时间，基于历史数据和数学模型仿真预测经济/社会/创新效果；新出台政策效果预测；多维度效果评估）。

[2] 政策力度评估模型｜科技专题服务算法库.md｜1.1.1.1.1.1.1.8.2（效果维度、覆盖维度、成本维度三维加权生成政策力度指数）。

[3] 政策效果评估模型｜科技专题服务算法库.md｜1.1.1.1.1.1.1.8.3（执行效果、社会经济效应、环境影响多维加权生成政策效果评估指数）。

[4] 弹性系数｜国家统计局｜国民经济核算体系（弹性系数=因变量变动率 ÷ 自变量变动率，用于测度政策参数变化对效果变化的响应强度）。
