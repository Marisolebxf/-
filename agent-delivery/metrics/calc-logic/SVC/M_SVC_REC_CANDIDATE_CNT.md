# 候选机构数（M_SVC_REC_CANDIDATE_CNT）

## 基本信息

- 指标ID: M_SVC_REC_CANDIDATE_CNT
- 指标名称: 候选机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构推荐
- 三级模块: 培育推荐
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-05

## 口径定义

当前产业方向与筛选范围内参与名单计算的候选机构数量(招引=外部候选; 培育=本土在库)。

## 计算公式

COUNT(candidates | filter)。

## 源库表字段

demo_gkxlumenx_ads.svc_attraction_recommend — 50行(招引); demo_gkxlumenx_ads.svc_cultivation_recommend — 50行(培育)

## 待建表字段

外部候选机构库正式结构(当前为演示数据)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.6.2/7.2; 招引50行+培育50行, 外部候选库结构仅规划未建

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
