# 竞争力-配套环境（M_CHAIN_REG_COMP_SUPPORT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMP_SUPPORT |
| 指标名称 | 竞争力-配套环境 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业竞争力评价 |
| 三级模块 | 竞争力指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

从政策支持、融资环境、服务机构等维度评估区域配套环境竞争力。

## 计算逻辑说明

采用加权平均。维度：政策支持/融资环境/服务机构。权重待甲方确认。

| 三级指标 | 计算方式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- |
| 政策覆盖率 | 相关政策覆盖环节占全链环节数的比例 | dwd_industry_chain_info(industry_link_code, industry_link_name); dwd_policy_base(id, title, keywords, keypoints, theme, city, status) | 无 |
| 融资事件 | 链上企业融资事件去重件数 | dwd_org_financing_info(org_id, external_id, completion_date); dwd_org_industry_tags(credit_code); dwd_org_base_info(city) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策覆盖
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联融资事件
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 区域城市筛选
- dwd_policy_base(id, title, keywords, keypoints, theme, city, status) — 政策去重(政策支持/政策覆盖率), 标题/关键词/要点/主题匹配环节, 区域, 有效状态
- dwd_org_financing_info(org_id, external_id, completion_date) — 融资事件去重(融资环境), 信用代码关联, 融资时间

## 待建字段

- 无

## 参考文献

- 配套环境竞争力｜国家市场监督管理总局｜国家市场监督管理总局, 国家标准化管理委员会. 企业竞争力评价规范: GB/T 40957—2021[S/OL]. (2021-11-26)[2026-08-19]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B
- 配套环境竞争力｜国务院｜国务院. 李强主持召开国务院常务会议 审议通过关于加快发展先进制造业集群的意见等[EB/OL]. (2023-05-05)[2026-08-19]. https://www.gov.cn/yaowen/2023-05/05/content_5754266.htm
