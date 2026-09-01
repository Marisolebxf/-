# 区域产业生态（M_CHAIN_REG_ECOSYSTEM）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_ECOSYSTEM |
| 指标名称 | 区域产业生态 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的链上企业去重数量。库无上下游协同度、公共服务配套度正式字段，本指标计企业集聚规模，不拆协同与配套。

## 计算逻辑说明

COUNT(DISTINCT credit_code)。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上企业；用credit_code关联dwd_org_base_info.external_id，按province、city筛区域后按credit_code去重。

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code) — 链上企业筛选, 信用代码关联
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市

## 待建字段

- 无
