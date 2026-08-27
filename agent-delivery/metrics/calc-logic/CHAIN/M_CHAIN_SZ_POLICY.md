# 深圳政策维度（M_CHAIN_SZ_POLICY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_POLICY |
| 指标名称 | 深圳政策维度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | 综合优势 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q058+QC08 |


## 口径定义

从政策覆盖数量与支持强度等维度评估深圳政策相对优势。

## 计算逻辑说明

政策数量、政策强度等维度加权评分。权重待甲方确认。

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称匹配政策
- dwd_policy_base(id, title, keywords, keypoints, theme, city, status) — 政策去重(政策数量), 标题/关键词/要点/主题匹配产业, 深圳城市, 有效状态

## 待建字段

- fiscal_sci_tech_exp-财政科技拨款
- general_public_budget-地方一般公共预算支出

## 参考文献

- 深圳政策维度｜深圳市发展和改革委员会｜深圳市发展和改革委员会. 深圳战略性新兴产业风头正盛[EB/OL]. (2026-02-24)[2026-08-19]. https://www.sz.gov.cn/cn/zjsz/fwts_1_3/tzdt_1/content/post_12650791.html
- 深圳政策维度｜国务院｜国务院. 李强主持召开国务院常务会议 审议通过关于加快发展先进制造业集群的意见等[EB/OL]. (2023-05-05)[2026-08-19]. https://www.gov.cn/yaowen/2023-05/05/content_5754266.htm

对应Excel超链接：.\指标计算逻辑-V2\M_CHAIN_SZ_POLICY.md
