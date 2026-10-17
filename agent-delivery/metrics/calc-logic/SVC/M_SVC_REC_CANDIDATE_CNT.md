# 候选机构数（M_SVC_REC_CANDIDATE_CNT）

## 基本信息

- 指标ID: M_SVC_REC_CANDIDATE_CNT
- 指标名称: 候选机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构推荐
- 三级模块: 招引 / 培育名单
- 更新频率: n/a
- 对齐状态判定: 废止（2026-10-13 human:徐滕强；lifecycle_stage=retired）
- 是否在数据库: 否
- 关联Q编号: 无（废止后不再挂 Q-SVCCHAIN-05 / Q-SVCCHAIN-08 当指标卡点）

## 口径定义

废止。招引/培育页「共 N 家候选」是当前产业方向与筛选条件下、生成推荐名单后的**结果集条数**（前端 `results.length`），随筛选实时变，不是预聚合统计指标。

判定依据：

1. 页面数字 = 当前推荐结果集 `length`，不请求 Java / Python 出「指标值」。
2. N 随产业方向、机构类型、服务环节等筛选条件变化——本质是实时查询/筛选结果大小。
3. 招引池 = 外部候选（演示 `EXTERNAL_CANDIDATES`）；培育池 = 本土在库（演示 `SERVICE_ORGS`）。名单怎么筛归模型演示，本条不定义「库里有多少候选」。
4. 与已废止的 `M_SVC_ORG_SELECTED_COUNT`（已选 N 家）同类：页面集合大小，不是指标工厂该出的数。
5. 作废 2026-08-28 侯佳伟 1B「仍挂 STAT、查询时 COUNT」口径——连 STAT 身份一并拿掉；「不写 ADS」结论保留并加强为废止。

保留 ID 防冲突。页面可继续显示「共 N 家」，去掉 ⓘ / MetricSpecCard。禁止灌 `svc_metric_*` 本 ID；禁止把圈定 3525 当候选数。

## 计算公式

无。不计算。

## 源库表字段

无。

## 待建表字段

无。不要建表，不要往 `svc_metric_fact` 灌本编号。细稿旧述 `svc_attraction_recommend` / `svc_cultivation_recommend` 50 行演示表**不作源**。

## 参考文献 / 依据

USM/IA/TRACE-SVCCHAIN-RECOMMEND；demo `ServiceRecommendPage.tsx`「共 {results.length} 家」；`SVC-ALGO-STAT-21-L01` 序号 19；`SVC-METRIC-COVER-STAT-L01` 2026-10-13 废止。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-28: 侯佳伟 1B 不写 ADS（仍挂 STAT）
- 2026-10-13: human:徐滕强 判定为实时筛选结果集 length，废止指标身份（同 SELECTED_COUNT）
