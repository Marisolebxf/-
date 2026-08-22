# 环节平均服务深度（M_SVC_CHAIN_SEGMENT_AVG_DEPTH）

## 基本信息

- 指标ID: M_SVC_CHAIN_SEGMENT_AVG_DEPTH
- 指标名称: 环节平均服务深度
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 短板分析
- 更新频率: 周
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-02

## 口径定义

环节内机构在选定领域服务深度得分的算术平均。深度口径沿用Q-SVCCHAIN-02, 未定。

## 计算公式

pending_algorithm(演示态: AVG(coverage[field_id].depth) WHERE org ∈ stage)。

## 源库表字段

demo_gkxlumenx_ads.svc_chain_gap(avg_depth) — 6行, 有avg_depth值: 研发92.09/IP74.39/转移80/中试null/检测75/市场化72.44

## 待建表字段

服务深度评分算法定义卡(口径未定)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.4.1; svc_chain_gap有avg_depth值但深度口径未正式定义

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
