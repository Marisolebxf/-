# 当前分析机构数（M_SVC_ORG_SELECTED_COUNT）

## 基本信息

- 指标ID: M_SVC_ORG_SELECTED_COUNT
- 指标名称: 当前分析机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 产业领域分析
- 更新频率: n/a
- 对齐状态判定: 废止（2026-10-13 human:徐滕强；lifecycle_stage=retired）
- 是否在数据库: 否
- 关联Q编号: 无

## 口径定义

废止。分析页「已选 N 家 / 对比机构 N 家」是用户勾选 `org_id` 后的会话 UI 计数，不是指标。

判定依据（前者，不是后者）：

1. 选择器勾的是具体机构，确认后写入 `serviceCenterStore.selection` 或 `evalConfig.compareOrgIds`。
2. 领域筛选「不改分析指纹」，不把勾选变成条件查询。
3. 页面数字 = 数组 `length`，不请求 Java / Python。
4. `lumen-algo-py` `calc_org_selected_count` 去 `COUNT(*) FROM svc_org_card` 是错实现，和入库总数撞数。

后者（勾选一组条件、后端查符合条件的总数）在本页不存在。

保留 ID 防冲突。页面可继续显示已选家数，去掉 ⓘ / MetricSpecCard。后续删 `/internal/v1/svcan/org/selected-count`。

## 计算公式

无。不计算。

## 源库表字段

无。

## 待建表字段

无。不要建表，不要往 `svc_metric_fact` 灌本编号。

## 参考文献 / 依据

demo `ServiceOrgAnalysisPage.tsx` 指标条 `analysisOrgCount`；`SVC-ALGO-STAT-21-L01` 序号 3；`SVC-METRIC-COVER-STAT-L01` 2026-10-13 废止。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 先钉会话数组 length
- 2026-10-13: 判定为 UI 勾选家数，废止指标身份
