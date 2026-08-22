# 入库服务机构总数（M_SVC_ORG_TOTAL）

## 基本信息

- 指标ID: M_SVC_ORG_TOTAL
- 指标名称: 入库服务机构总数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 产业领域分析
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-SVCCHAIN-01

## 口径定义

当前服务机构库内可分析的机构去重总数(按org_id去重)。

## 计算公式

COUNT(DISTINCT org_id)。

## 源库表字段

demo_gkxlumenx_ads.svc_metric_fact(metric_id=M_SVC_ORG_CNT, value=3525) — 2行; demo_gkxlumenx_ads.svc_org_card(org_id) — 3525行; demo_gkxlumenx_dwd.svc_org_circle(org_id) — 3525行

## 待建表字段

无

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.1; metric_fact有3525条, org_card和org_circle均有3525行, 口径一致

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
