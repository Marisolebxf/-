# 培育综合评分（M_SVC_REC_CULTIVATE_SCORE）

## 基本信息

- 指标ID: M_SVC_REC_CULTIVATE_SCORE
- 指标名称: 培育综合评分
- 一级模块: 产业服务链分析
- 二级模块: 服务机构推荐
- 三级模块: 培育推荐
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-05

## 口径定义

深圳本土在库机构按培育模型四维度(现有规模/技术创新能力/服务成效/市场缺口)加权的综合得分。维度量化来源未定。

## 计算公式

演示态: Σ(dim_norm × weight) / 100。

## 源库表字段

demo_gkxlumenx_ads.svc_cultivation_recommend(org_id, cultivation_index, dimension_scores, growth_stage, priority_level) — 50行, 含4维: scale/effect/marketGap/innovation

## 待建表字段

四维度量化来源正式定义、默认权重甲方确认

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.7.1; svc_cultivation_recommend有50行, 4维评分有值但量化来源和权重未定

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
