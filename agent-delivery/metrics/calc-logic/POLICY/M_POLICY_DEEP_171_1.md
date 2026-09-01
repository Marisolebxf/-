# 政策布局推荐模型（M_POLICY_DEEP_171_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DEEP_171_1 |
| 指标名称 | 政策布局推荐模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | （算法库未挂页） |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方GAP-ALGO-TYPE-UNSIGNED；融合机遇+短板 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

在选定产业或技术领域范围内，按政策主题统计既已过机遇线、又存在短板可对冲的方向数。

## 计算逻辑说明

机遇侧读 `M_POLICY_OPPORTUNITY_COUNT` 综合分；短板侧读 `M_POLICY_SHORTBOARD_COUNT` 的维判定。短板是缺口（低于阈值记 1），完整率不得当作正向分加进推荐指数。

**第一步：方向键。** 政策方向 = `theme` 拆开后的去重条目（数组或分隔符切开）。空主题不进方向集。一条政策可落入多个方向。方向 \(t\) 的政策子集为 \($P_t$\)（命中本对象且 `theme` 含 \(t\)）。

**第二步：机遇方向。** 不重算关注度/影响力/稳定性。

$$Opp_t = I\bigl(\,P_t\text{ 中至少 1 条政策的机遇综合分}\ge T_{\text{机遇}}\,\bigr)$$

\($T_{\text{机遇}}$\) 与机遇数同一阈值（现行 60，待 QPOL-02）。

**第三步：短板方向。** 不把覆盖/有效/合规的完整率加权相加。

1. **对象级覆盖维**：按短板数已写规则，对选定对象整库判定覆盖性是否为短板。对象覆盖为短板时，各方向的覆盖维都记缺口（单主题铺不满八类，不算该主题自己的覆盖短板）。
2. **主题级有效维、合规维**：把 \($P_t$\) 套短板数已写阈值（有效占比 / 时效占比；文号规范率 / 正文完整率）。

$$Short_t = I(\text{对象覆盖为短板}\ \lor\ P_t\text{有效维为短板}\ \lor\ P_t\text{合规维为短板})$$

**第四步：对冲计数。** 只数两边同时成立的方向。单一条件，不用「≥60 或高于均值」。

$$政策布局建议数 = \text{COUNT(DISTINCT }t\text{ WHERE }Opp_t=1\text{ 且 }Short_t=1)$$

任一侧全 0 则输出 0。默认仍是同时成立才计 1。

| 一级指标       | 二级指标 | 指标说明                                    | 源表字段                                                     | 待建字段                     |
| -------------- | -------- | ------------------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| 政策布局建议数 | 机遇方向 | 该主题至少 1 条政策已过机遇综合分阈值       | 读 M_POLICY_OPPORTUNITY_COUNT；方向键 dwd_policy_base(id, theme) — 去重, 主题 | theme缺失率达96%，疑似不可用 |
| 政策布局建议数 | 短板方向 | 对象覆盖缺口，或该主题子集触发有效/合规短板 | 读 M_POLICY_SHORTBOARD_COUNT；方向键 dwd_policy_base(id, theme) — 去重, 主题 | theme缺失率达96%，疑似不可用 |

## 源表字段

- dwd_policy_base(id, theme, keywords, content, ministry, quote_policy, title, publish_code, publish_year, status, expire_date, implementation_date, abstract, keypoints) — 去重, 方向键与机遇复用, 短板复用（类型文本/有效/时效/文号/正文）
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链与覆盖分母（仅产业锚点）

本指标不另开计算字段。机遇侧读 `M_POLICY_OPPORTUNITY_COUNT`，短板侧读 `M_POLICY_SHORTBOARD_COUNT`。

## 待建字段

无

## 参考文献

政策布局建议数+科技专题服务算法库+§1.1.1.1.1.1.1.8.6

政策工具量化+清华大学公共管理学院+黄萃, 赵培强, 苏竣. 基于政策工具视角的中国科技创新政策文本量化研究[J]. 科学学研究, 2014, 32(12): 1764-1773.


