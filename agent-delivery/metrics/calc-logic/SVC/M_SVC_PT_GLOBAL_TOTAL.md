# 全球服务机构总数（M_SVC_PT_GLOBAL_TOTAL）

## 基本信息

- 指标ID: M_SVC_PT_GLOBAL_TOTAL
- 指标名称: 全球服务机构总数
- 一级模块: 产业服务链分析 → 专题服务（门户 SVCCHAIN-PORTAL）
- 二级模块: 全球服务机构概况（左上 KPI + 历年总量趋势）
- 算法类型: STAT（建议类型；formula 待唐绍祖补签）
- 更新频率: daily（随圈定工厂 T2 同一趟）
- 对齐状态判定: 部分闭合（2026-10-13 徐滕强；国内格可执行、全球格挂 Q-SVCCHAIN-07）
- 是否在数据库: 否（fact/series 本编号未灌，IMPL T2 补）
- 关联Q编号: Q-SVCCHAIN-06（口径伞）/ Q-SVCCHAIN-07（全球名录）

## 口径定义

门户「全球服务机构总数」占位指标。现网 = 国内圈定切片（svc_org_circle，3525，全广东），格子先写圈定值并强制「目前只有国内数据，全球待接入」提醒（悬停 + ⚠️ Q-SVCCHAIN-07）。

- 人口：svc_org_circle 全量（与 M_SVC_ORG_TOTAL 同池同数）
- series：按工商成立年累加存量；无成立日 1 家不进序列（fact 3525 为准、series 末年 3524，页面注记）
- 本年新增 = 本条 series 相邻年差（存量差，侯佳伟 3A）；数值等价于当年成立数（第 2 条 M_SVC_ORG_NEW_COUNT 事件口径），取序列差与折线自洽，不改挂
- 全球格：真全球名录待 Q-SVCCHAIN-07（海外 dwd_forg_base_info 0 行；港/台/澳 ∩ circle = 0）

禁止：缩放 89600；线上 JOIN ODS；把港澳台/海外并进 circle；旧号 M_SVC_ORG_CNT 顶替。

## 计算公式

[SEED 仅工厂 svcseed / GDF]
fact.value = COUNT(*) FROM svc_org_circle          -- 现网 3525；org_id 唯一键无需 DISTINCT
series     = 按工商成立年累加存量                    -- 末年 ≈3525；无成立日 1 家不进

[SERVE 线上只读 ADS]
SELECT period, value FROM ads.svc_metric_series WHERE metric_id='M_SVC_PT_GLOBAL_TOTAL';
本年新增 = series[末年] - series[上年]

pending_cosign: human:唐绍祖（formula 待补签）

## 源库表字段

- SEED 真源：dwd svc_org_circle（org_id 唯一键）；成立年 JOIN ODS dwd_org_base_info.incorporation_date 一次（工厂投影期）
- SERVE 契约：ads.svc_metric_fact / ads.svc_metric_series 本 ID 行

## 验收不变量

- fact.value = COUNT(*) FROM svc_org_circle（页面非 89600）
- series 末年 = 3524（1 家无成立日）；页面总数显 fact 3525 并注记
- 页面有「仅国内，全球待接入」提醒 + ⚠️ Q-07
- 本年新增 = 折线末两点差（KPI 与图自洽）

## 参考文献 / 依据

招标 05·101 六套第（2）块；SVC-ALGO-STAT-21-L01 序号 6（2026-08-28 改锁 1C 2国内 3A）；Q-SVCCHAIN-06/07 决策卡；SVC-METRIC-COVER-STAT-L01 2026-10-13 徐滕强拍板（1-A fact 为准 / 2 存量差 / 3 源表 circle / 4 挂 Q-06）。

## 更新记录

- 2026-08-21: 初版（王惠模拟，引废弃 svc_global_dist）
- 2026-08-28: 侯佳伟改锁 1C 2国内 3A（未落 seed）
- 2026-10-13: 徐滕强拍板四疑点，seed v0.2.0 部分闭合（本文重写）
