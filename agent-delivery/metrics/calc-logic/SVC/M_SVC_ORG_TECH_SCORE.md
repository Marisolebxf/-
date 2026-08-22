# 技术力综合得分（M_SVC_ORG_TECH_SCORE）

## 基本信息

- 指标ID: M_SVC_ORG_TECH_SCORE
- 指标名称: 技术力综合得分
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 技术力评估
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-01

## 口径定义

按用户配置的维度与权重加权的机构技术力综合分(0-100)。正式维度口径/归一基准/默认权重待算法定义卡。

## 计算公式

演示态: Σ dim_norm × weight, dim_norm = value / max(compare_set)。正式口径待算法定义卡。

## 源库表字段

demo_gkxlumenx_ads.svc_tech_power_score(org_id, model_id, score, dimension_scores) — 283行, 含5维: cases/experts/patents/standards/rdInvestment; 6类服务类型各有model_id

## 待建表字段

归一化基准正式定义、默认权重配置(当前为对比集合最大值归一)、高级研发人才数字段

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.3.1; svc_tech_power_score有283行, 5维评分有值但归一基准和权重未正式定义

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
