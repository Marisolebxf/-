# 政策力度评估模型（M_POLICY_DEEP_167_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DEEP_167_1 |
| 指标名称 | 政策力度评估模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | （算法库未挂页） |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方GAP-ALGO-TYPE-UNSIGNED；与力度评分同维 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对有效政策从效果、覆盖、成本三维量化的政策力度评估模型综合结果，输出力度指数、分维报告与排行榜；取值 0—100。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。综合统计默认仅国内（QPOL-05），国际政策 dwd_global_policy_base 不进综合分。本 ID 为算法库模型，原型页不挂本 metricId。

第一步：三维原始值与力度评分/指数相同（见下表）。

第二步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（权重待 QPOL-02）后 ×100。全样本同值取 0.5。N<3 标「样本不足」。

第三步：输出力度指数、分维报告、排行榜。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策力度评估模型 | 效果维度 | 实施日完备率 | 从实施是否启动、支持方式是否写明评估政策的输出成效安排。 | I(implementation_date 非空)；城市级改为占比 | dwd_policy_base(id, implementation_date) — 去重, 实施日 | 无 |
| 政策力度评估模型 | 效果维度 | 支持方式完备率 | 从实施是否启动、支持方式是否写明评估政策的输出成效安排。 | I(support_way 至少 1 条非空)；城市级改为占比 | dwd_policy_base(id, policy_support.support_way) — 去重, 支持方式 | 无 |
| 政策力度评估模型 | 覆盖维度 | 支持对象种类数 | 从支持对象种类与区县落地评估政策影响范围。 | COUNT(DISTINCT support_object) | dwd_policy_base(id, policy_support.support_object) — 去重, 支持对象 | 无 |
| 政策力度评估模型 | 覆盖维度 | 区县落地标记 | 从支持对象种类与区县落地评估政策影响范围。 | I(district 非空)；城市级改为 COUNT(DISTINCT district) | dwd_policy_base(id, district) — 去重, 区县 | 无 |
| 政策力度评估模型 | 成本维度 | 扶持行为完备率 | 从是否写明扶持行为评估资源投入安排；无金额不编造拨款。 | I(support_behavior 至少 1 条非空) | dwd_policy_base(id, policy_support.support_behavior) — 去重, 扶持行为 | support_amount-扶持金额 |

## 源表字段

- dwd_policy_base(id, implementation_date, district, status, expire_date, publish_year, city, rank, title, keywords, keypoints, theme, policy_support) — 去重, 实施日, 区县, 有效, 失效, 同年截面, 城市排行, 国家级, 四字段命中, 对象/行为/方式
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- support_amount-扶持金额（成本维正式口径
- 现行用 support_behavior 是否非空）

## 参考资料

政策力度测量|南京大学商学院|浙江省科技厅重点软科学项目(2016C25G2010003)|仲为国,彭纪生,孙文祥. 政策测量、政策协同与经济绩效——基于创新政策的实证研究(1978-2006) [J]. 南方经济, 2008, (7): 45-58+67.
