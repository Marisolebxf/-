# 政策力度指数（M_POLICY_INTENSITY_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_INTENSITY_INDEX |
| 指标名称 | 政策力度指数 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | 政策力度排名 |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方QPOL-02；门户已挂本 ID |
| 是否在数据库 | 否 |
| 关联Q编号 | QPOL-02 |

## 口径定义

按城市从效果、覆盖、成本三维综合评定的政策力度指数，取值 0—100。分数越高表示该市政策实施力度越强。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。综合统计默认仅国内（QPOL-05），国际政策 dwd_global_policy_base 不进综合分。对比单位是城市：city 含该市名即计入；rank 含国家级的政策可计入每个对比市。该市有效政策数为 N_c，N_c=0 不输出。

第一步：城市级原始值（见下表）。三维互不共用同一计数。

第二步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（权重待 QPOL-02）后 ×100。全样本同值取 0.5。N<3 标「样本不足」。

第三步：三维等权平均 ×100。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策力度指数 | 效果维度 | 实施日完备占比 | 从该市有效政策中实施已启动、支持方式已写明的平均占比评估输出成效。 | COUNT(implementation_date 非空) / N_c | dwd_policy_base(id, city, implementation_date) — 去重, 城市, 实施日 | 无 |
| 政策力度指数 | 效果维度 | 支持方式完备占比 | 从该市有效政策中实施已启动、支持方式已写明的平均占比评估输出成效。 | COUNT(support_way 至少 1 条非空) / N_c | dwd_policy_base(id, city, policy_support.support_way) — 去重, 城市, 支持方式 | 无 |
| 政策力度指数 | 覆盖维度 | 支持对象种类数 | 从该市内部的对象广度与区县广度评估政策影响范围。 | COUNT(DISTINCT support_object)，空值不计入 | dwd_policy_base(id, city, policy_support.support_object) — 去重, 城市, 支持对象 | 无 |
| 政策力度指数 | 覆盖维度 | 区县去重数 | 从该市内部的对象广度与区县广度评估政策影响范围。 | COUNT(DISTINCT district)，空值不计入 | dwd_policy_base(id, city, district) — 去重, 城市, 区县 | 无 |
| 政策力度指数 | 成本维度 | 扶持行为完备占比 | 从该市有效政策中写明扶持行为的占比评估资源投入安排；无金额不编造拨款。 | COUNT(support_behavior 至少 1 条非空) / N_c | dwd_policy_base(id, city, policy_support.support_behavior) — 去重, 城市, 扶持行为 | support_amount-扶持金额 |

## 源表字段

- dwd_policy_base(id, rank, city, district, status, expire_date, implementation_date, title, keywords, keypoints, theme, policy_support) — 去重, 国家级计入各市, 对比城市, 区内覆盖, 有效, 失效, 实施是否启动, 四字段命中, 扶持对象/行为/方式
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- support_amount-扶持金额（成本维正式口径
- 现行用 support_behavior 非空占比）

## 参考资料

政策力度测量|南京大学商学院|浙江省科技厅重点软科学项目(2016C25G2010003)|仲为国,彭纪生,孙文祥. 政策测量、政策协同与经济绩效——基于创新政策的实证研究(1978-2006) [J]. 南方经济, 2008, (7): 45-58+67.
