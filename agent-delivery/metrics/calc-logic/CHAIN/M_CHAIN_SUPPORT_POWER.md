# 配套服务（M_CHAIN_SUPPORT_POWER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SUPPORT_POWER |
| 指标名称 | 配套服务 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的配套生态竞争力得分，取值0—100。对齐算法库配套生态竞争力，由政策覆盖率和融资环境合成。

## 计算逻辑说明

二维等权。先按区域、链、年计算政策覆盖率和融资事件数，再在同一产业链、同一统计年度对全部对比区域做截面min-max归一化到[0,1]，算术平均后乘100。某维全部区域取值相同则该维取0.5。默认等权，前端可调权重但不另建权重表。区域用机构所在省、市过滤，深圳场景取city="深圳市"。从dwd_industry_chain_info确定目标产业链；融资维关联dwd_org_industry_tags取链上企业，再关联dwd_org_base_info筛区域。库无独立服务机构产业链表，不纳入本指标。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域产业指数 | 配套生态 | 政策覆盖率 | 政策命中环节数/全链环节数×100%。分母为dwd_industry_chain_info中该链industry_link_code去重件数。分子为至少被一条有效政策命中的industry_link_code去重件数。政策库无环节外键，用industry_link_name出现在title、keywords、keypoints或theme判定命中。政策须status为有效、publish_year不晚于统计年，且province或city落在目标区域，或rank含国家级 | dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策; dwd_policy_base(id, title, keywords, keypoints, theme, province, city, status, publish_year, rank) — 政策去重, 标题匹配环节, 关键词匹配环节, 要点匹配环节, 主题匹配环节, 政策省份, 政策城市, 有效状态, 发布年, 国家级覆盖全部区域 | 无 |
| 区域产业指数 | 配套生态 | 融资环境 | 区域链上融资事件去重件数。链上企业credit_code关联dwd_org_financing_info.external_id，并经dwd_org_base_info按province、city筛区域，按org_id与completion_date去重；completion_date所在年不晚于统计年 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code) — 链上企业筛选, 信用代码关联; dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市; dwd_org_financing_info(org_id, external_id, completion_date) — 融资企业标识, 信用代码关联, 融资完成时间 | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策
- dwd_org_industry_tags(industry_code, credit_code) — 链上企业筛选, 信用代码关联
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市
- dwd_policy_base(id, title, keywords, keypoints, theme, province, city, status, publish_year, rank) — 政策去重, 标题匹配环节, 关键词匹配环节, 要点匹配环节, 主题匹配环节, 政策省份, 政策城市, 有效状态, 发布年, 国家级覆盖全部区域
- dwd_org_financing_info(org_id, external_id, completion_date) — 融资企业标识, 信用代码关联, 融资完成时间

## 待建字段

- 无

## 参考文献

- 配套服务｜中国中小企业发展促进中心｜中国中小企业发展促进中心. 2025年度中小企业发展环境评估报告[R]. 北京, 2025. https://www.tanchang.gov.cn/zfxxgk/public/32129002/148149154.html
