# 协同—创新产出关联结果（M_SYNTH_COLLAB_OUTPUT_CORR）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_COLLAB_OUTPUT_CORR |
| 指标名称 | 协同—创新产出关联结果 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新协同分析 |
| 三级模块 | 协同效果评估 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-C-03 |

## 口径定义

选定区域内、评估窗口内，协同网络结构与联合发明专利产出的统计关联。协同侧取 `M_SYNTH_COLLAB_INDEX` 的指数、密度、中心度（区域×年）；产出侧为同年联合发明专利授权去重数。输出三条 Pearson 相关系数，取值 \([-1,1]\)。

对象=协同结构与产出的相关，不是再算一遍协同指数，也不是把联合发明专利数既当 X 又当 Y。

## 计算逻辑说明

本指标不另建协同网。建网与完整度 / 中心度 / 密度 / 指数见 `M_SYNTH_COLLAB_INDEX`（算法库入口同 `M_SYNTH_191_1`）。

### 第一步：取协同侧 \(X\)（区域×年）

评估窗口默认近 5 个统计年（页面选 3 年则用 3 年）。对窗口内每个统计年读取：

- \(X_1\) = 区域创新协同指数（`M_SYNTH_COLLAB_INDEX`）
- \(X_2\) = 网络密度（INDEX 密度子项）
- \(X_3\) = 网络中心度（INDEX 中心度子项，平均点度中心性）

该年不成网或指数为空，该年不进样本。协同指数是完整度、中心度、密度标准化后加权的 0—100 分，不是联合专利件数。

### 第二步：算产出侧 \(Y\)（区域×年）

联合发明专利数 \(Y_t\)：`dwd_patent` 按 `pn` 去重后，同时满足：

- 发明且已授权：`kind` 为发明，`granted_number` 非空
- 年窗：`pbdt_year = t`
- 联合：`dwd_patent_applicants` 中同一 `pn` 的去重申请人 \(\ge 2\)
- 区域归属：`first_applicant_name` 对齐本区域 `dwd_org_base_info.name_cn`

产出归属用第一申请人，与活力 / 要素专利对齐一致。建网边要求双方都在本区域才连边，跨区域联合专利计入 \(Y\)，但不一定进入本区域协同网。因此 \(Y\) 与密度 / 中心度同出专利源、但不同构；指数还含完整度与项目 / 人才边，与 \(Y\) 更不是同一变量。

### 第三步：组样本并算相关

样本粒度：同一区域、窗口内按年展开。一对 $(X_{k,t}, Y_t) $为一条样本。默认同年（滞后 = 0）。

$$
r_k = \frac{\sum_t (X_{k,t}-\bar{X}_k)(Y_t-\bar{Y})}{\sqrt{\sum_t (X_{k,t}-\bar{X}_k)^2\sum_t (Y_t-\bar{Y})^2}}
$$

有效样本 \(n<3\)，或任一侧方差为 0：不出系数、不画散点趋势，标 `status=insufficient`。

不做回归、不把 p 值当作上线门槛。页面按区域各自的时间序列出 \(r\)，不做多区域截面相关。禁止「导致 / 提升 / 影响效应」表述。密度、中心度的边含联合专利，与 \(Y\) 部分同源，\(r\) 偏高只说明结构相关。

### 第四步：输出

区域一行：$r_{\text{index}}、r_{\text{density}}、r_{\text{centrality}}$、有效样本 \(n\)、`status`、窗口。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 协同—创新产出关联结果 | 协同指数—联合发明专利相关 | 区域创新协同指数与联合发明专利授权数的统计关联。 | $Pearson(X_1, Y)，n\ge 3$ | 协同侧同 M_SYNTH_COLLAB_INDEX；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 发明授权,第一申请人对齐,年窗；dwd_patent_applicants(pn, sequence, name) — 联合申请人；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,存续 | 无 |
|  | 网络密度—联合发明专利相关 | 协同网络密度与联合发明专利授权数的统计关联。 | $Pearson(X_2, Y)，n\ge 3$ | 同上 | 无 |
|  | 网络中心度—联合发明专利相关 | 协同网络中心度与联合发明专利授权数的统计关联。 | $Pearson(X_3, Y)，n\ge 3$ | 同上 | 无 |

## 源表字段

- 协同侧：同 `M_SYNTH_COLLAB_INDEX` / `M_SYNTH_191_1`（不另建网）
- dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 发明授权,第一申请人对齐,年窗
- dwd_patent_applicants(pn, sequence, name) — 联合申请人判定
- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,存续

## 待建字段

- 无
