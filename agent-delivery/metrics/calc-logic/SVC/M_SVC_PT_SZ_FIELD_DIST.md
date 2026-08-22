# 深圳机构产业领域分布（M_SVC_PT_SZ_FIELD_DIST）

## 基本信息

- 指标ID: M_SVC_PT_SZ_FIELD_DIST
- 指标名称: 深圳机构产业领域分布
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 深圳产业服务
- 更新频率: 季度
- 对齐状态判定: 未对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

深圳产业服务机构按产业领域×服务链环节的服务分布计数。一家机构可服务多个领域, 各领域合计大于机构总数。

## 计算公式

COUNT(org) WHERE city=深圳 GROUP BY field_id, stage_id。

## 源库表字段

demo_gkxlumenx_dwd.svc_org_circle(hit_fields含industry_l1-l4_name) — 3525行; demo_gkxlumenx_ads.svc_metric_dist — 97行

## 待建表字段

机构×领域×环节服务记录正式数据源(当前hit_fields为工商标签匹配, 非服务记录)

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.5; hit_fields为工商标签匹配结果非真实服务记录, 口径不一致

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
