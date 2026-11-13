# TS-L2-DS09-TALENT-RANGE-L01 · talent-flow 实现 range 时间窗过滤(契约 §218 欠账)

## 任务认领(必填)

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:zcode` |
| supervised_by | `human:王梓真` |
| 任务 | `TS-L2-DS09-TALENT-RANGE-L01`(epic E-FE-TECH-SITUATION,P1,S/2 分) |

## 背景

用户核对需规 182(SRS 原文无时间维度要求,「提供人才流动趋势分析和预警功能」)后,核对契约 OV-API v2 §218:**2026-11-11 新增 range 语义并三家会签**(records 按 flow_date 窗口过滤、stats 三数现算、net_inflow/institution_flows/od_nodes 全窗口),前端 OverviewTab 已按契约发参(`?range=3m/6m/12m`),但后端 `talentFlow` 端点只有 flow_type/risk_level 两参数——**range 被忽略,时间维度切换整卡无响应**(前端已接线、契约已签、后端欠账)。

## 实现(commit `c5d624f8`,MR !27 → dev `ce31ad79` 部署)

| 文件 | 改动 |
|---|---|
| `PlanningController.java` | talentFlow 增 `range` 参数(3m/6m/12m,默认 12m,出枚举 400,复用 OVERVIEW_RANGES) |
| `PlanningQueryService.java` | ① records[] 按 flow_date(缺行回落 updated_at 前 10 位)落窗口过滤(新增 `inRangeWindow`:窗口起点=now- N 月的当月 1 日);② stats 三数(warning_count/学术→产业/产业→学术)按过滤后记录现算;③ **net_inflow/institution_flows/od_nodes 保持全窗口聚合**(契约明文口径,TOPS 卡无时间标签与之自洽——设计上就哪些该动哪些不该动) |

前端零改动(早已按契约发参)。

## 测试与验证

- 单测:PlanningQueryServiceTest 新增 2 例(range 窗口过滤边界含 flow_date 缺行回落/stats 现算/全窗口块不受影响;非法窗口 Service 侧保守回落 12m,枚举校验归 Controller);既有 2 例更新为三参调用;PlanningControllerTest 1 处签名同步;
- **模块全量 196 测试 0 失败**(禁 Maven 缓存实跑);
- 线上验证(部署后实测):
  - `range=12m` → records 5 行、stats 预警 2/学→产 29/产→学 10;
  - `range=3m` → records 0(种子全在 2026-03,窗口外,诚实空态)、三数归 0;
  - TOPS/od_nodes/net_inflow 两窗一致(全窗口口径 ✓)。

## 部署注记

- 流水线 5199 helm:deploy 标红为已知假红(helm 客户端限流超时)+ tempo 可观测组件存量 503(probe x4613/11h,建议单独处理);display 等全部服务 pod 实际已滚动到新版本(rollout summary 佐证),以线上行为验证为准。

## 关联

- 183 推送链路已闭环(OPS-SEQ183-XXLJOB-DEPLOY-L01,2026-11-13 结案);
- TS-DS09 用例 182 行可演,演示话术补口径:「重点机构 TOPS 为全窗口净流入统计;时间维度作用于流动记录明细、stats 三数与桑基链路」。
