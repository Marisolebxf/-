# 入库服务机构总数（M_SVC_ORG_TOTAL）

## 基本信息

- 指标ID: M_SVC_ORG_TOTAL
- 指标名称: 入库服务机构总数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 产业领域分析
- 更新频率: 日
- 对齐状态判定: 已对齐（2026-10-13 钉表）
- 是否在数据库: 是（圈定池；卡面不是本条）
- 关联Q编号: Q-SVC-010

## 口径定义

服务机构库 = 项目 DWD `svc_org_circle`（现网库 `demo_gkxlumenx_dwd`）。

`org_id` 已有唯一键 `uk_svc_org_circle_org`，一行一家机构。入池 = ODS `dwd_org_base_info` 按规则 A `svc_rule_demo_kw_v1.1` 挂入。`pending_client_confirm=1` 仍算已入库。

## 计算公式

```
COUNT(*) FROM svc_org_circle
```

不用 `DISTINCT`。不数 `svc_org_card`、`svc_metric_fact`、ODS 全量、`svc_org_base`。

## 源库表字段

demo_gkxlumenx_ads.svc_metric_fact(metric_id=M_SVC_ORG_CNT, value=3525) — 2行; demo_gkxlumenx_ads.svc_org_card(org_id) — 3525行; demo_gkxlumenx_dwd.svc_org_circle(org_id) — 3525行

## 待建表字段

无

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.1; metric_fact有3525条, org_card和org_circle均有3525行, 口径一致

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 库钉 `svc_org_circle`；唯一键所以 `COUNT(*)`
