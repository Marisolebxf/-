# 深圳产业服务机构数量（M_SVC_PT_SZ_TOTAL）

## 基本信息

- 指标ID: M_SVC_PT_SZ_TOTAL
- 指标名称: 深圳产业服务机构数量
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 深圳产业服务
- 更新频率: 年度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

深圳市产业服务机构去重总数(按年)。'产业服务机构'认定口径未定。

## 计算公式

COUNT(DISTINCT org_id) WHERE city=深圳 GROUP BY year。

## 源库表字段

demo_gkxlumenx_ads.svc_metric_fact(metric_id=M_SVC_SZ_SCALE, value=1355) — 2行; demo_gkxlumenx_ads.svc_org_card(city字段) — 3525行

## 待建表字段

产业服务机构认定口径正式定义(当前依赖svc_org_circle圈定规则)

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.5; svc_metric_fact有M_SVC_SZ_SCALE=1355, 认定口径依赖svc_org_circle

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
