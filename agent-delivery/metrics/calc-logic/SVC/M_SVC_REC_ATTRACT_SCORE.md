# 招引综合评分（M_SVC_REC_ATTRACT_SCORE）

## 基本信息

- 指标ID: M_SVC_REC_ATTRACT_SCORE
- 指标名称: 招引综合评分
- 一级模块: 产业服务链分析
- 二级模块: 服务机构推荐
- 三级模块: 引入推荐
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-05

## 口径定义

外部候选机构按招引模型四指标(产业匹配度/技术领先性/发展潜力/对外合作意愿)加权的综合得分。指标量化来源与默认权重未经甲方确认。

## 计算公式

演示态: Σ(indicator × weight) / 100。

## 源库表字段

demo_gkxlumenx_ads.svc_attraction_recommend(org_id, attraction_index, dimension_scores, priority_level, rank_no) — 50行, 含4维: techLead/potential/industryFit/willingness

## 待建表字段

四指标量化来源正式定义、默认权重甲方确认、名单入围阈值

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.6.1; svc_attraction_recommend有50行, 4维评分有值但量化来源和权重未经甲方确认

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
