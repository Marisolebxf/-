# 重点机构规模档案值（M_SVC_PT_KEYORG_SCALE）

## 基本信息

- 指标ID: M_SVC_PT_KEYORG_SCALE
- 指标名称: 重点机构规模档案值
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 重点机构详情
- 更新频率: 年度
- 对齐状态判定: 未对齐
- 是否在数据库: 否
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

重点产业服务机构的当前人数与年营收(档案字段直读, 非计算指标)。无正式年报/申报数据源。

## 计算公式

档案字段直读(staff_count / annual_revenue_yi / scale_band)。

## 源库表字段

demo_gkxlumenx_ads.svc_org_profile_card — 表存在但0行; demo_gkxlumenx_ads.svc_org_card — 3525行但无人数/营收字段

## 待建表字段

机构人数字段、年营收字段、机构规模档案表

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.5(104); svc_org_profile_card表0行, 无人数/营收数据源

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
