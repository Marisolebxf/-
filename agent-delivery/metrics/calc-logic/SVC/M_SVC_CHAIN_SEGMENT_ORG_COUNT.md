# 环节服务机构数（M_SVC_CHAIN_SEGMENT_ORG_COUNT）

## 基本信息

- 指标ID: M_SVC_CHAIN_SEGMENT_ORG_COUNT
- 指标名称: 环节服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 短板分析
- 更新频率: 日
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-03

## 口径定义

选定产业领域内, segment归属该服务链环节且存在服务覆盖记录的机构去重数量。

## 计算公式

COUNT(org) WHERE org.segment ∈ stage.segments AND coverage[field_id]存在。

## 源库表字段

demo_gkxlumenx_ads.svc_chain_gap(stage_code, stage_name, org_count_in_stage) — 6行, 六环节全覆盖: 研发1361/IP33/转移4/中试0/检测19/市场化1416

## 待建表字段

环节归属依赖专家知识库(未建)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.4.1; svc_chain_gap有6行环节级数据但环节归属依赖专家知识库未建

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
