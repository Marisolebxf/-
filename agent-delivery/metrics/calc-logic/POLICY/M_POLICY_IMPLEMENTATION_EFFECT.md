# 落地实效性（M_POLICY_IMPLEMENTATION_EFFECT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_IMPLEMENTATION_EFFECT |
| 指标名称 | 落地实效性 |
| 一级模块 | 政策分析 |
| 二级模块 | 深圳政策现状分析 |
| 三级模块 | 指标体系构建 |
| 更新频率 | 季 |
| 对齐状态判定 | 待采购 |
| 是否在数据库 | 否 |
| 关联Q编号 | QPOL-02 |


## 口径定义

从落地执行启动、受益覆盖、实施反馈等维度评估选定产业或技术领域的政策落地实效。

## 计算逻辑说明

需求 §1.1.1.2.4.2.6.3 只点名「落地实效性」，未给二级。下列三维对齐科技部政策评估中的组织实施、范围和对象、效果与影响；实施反馈无调查表，不编造满意度。对比单位是城市：默认深圳，可选北京、上海、广州；`city` 含该市名即计入。`rank` 含国家级的政策可计入每个对比市。有效：`status=有效`，且 `expire_date` 为空或不早于统计日。去重键 `id`。未选定对象不计算。该市有效命中政策数为 \(N_c\)。\(N_c=0\) 该市不输出。

**第一步：落到对比城市，取有效命中集。**

**第二步：三维原始值。**

1. **落地执行启动**：已填实施日的有效政策占比。是启动率，不是兑现率。

$$启动率_c = \frac{\text{COUNT(DISTINCT id WHERE }implementation\_date\text{ 非空)}}{N_c}\times 100\%$$

2. **受益覆盖**：该市有效命中政策中 `support_object` 去重种类。无受益企业名单，不用企业数冒充覆盖。空值不计入。

$$受益覆盖_c = \text{COUNT(DISTINCT }support\_object\text{)}$$

3. **实施反馈**：无调查表，本维不计算、不进综合。

**第三步：已出维在对比城市截面 min-max 到 [0,1]。** 同值或缺失取 0.5。实施反馈缺表，综合只用启动率与受益覆盖两维等权（权重待 QPOL-02）。

$$落地实效性_c = \frac{1}{2}(启动得分_c+覆盖得分_c)\times 100$$

\($N_c<3$\) 标「样本不足」。缺启动或覆盖任一原始值则不合成综合分，只出已出维。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 落地实效性 | 落地执行启动 | 实施日已填的有效政策占比 | dwd_policy_base(id, implementation_date, status, expire_date) | 无 |
| 落地实效性 | 受益覆盖 | 支持对象种类去重 | dwd_policy_base(policy_support.support_object) | benefit_enterprise_list-受益企业名单 |
| 落地实效性 | 实施反馈 | 无调查表，不计算 | 无 | feedback_score-实施反馈满意度 |

## 源表字段

- dwd_policy_base(id, rank, city, implementation_date, policy_support, status, expire_date, title, keywords, keypoints, theme) — 去重, 国家级计入各市, 对比城市, 启动率, 受益对象, 有效, 失效, 四字段命中
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- benefit_enterprise_list-受益企业名单（受益覆盖正式口径；现行用 support_object 种类数）
- feedback_score-实施反馈满意度

## 参考文献

落地实效性+科学技术部+https://www.most.gov.cn/ztzl/zdzx/tztg/201612/t20161222_4804.html

落地实效性+University of California, Davis+Sabatier P, Mazmanian D. The implementation of public policy: a framework of analysis[J]. Policy Studies Journal, 1980, 8(4): 538-560.

落地实效性+经济合作与发展组织+https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html
