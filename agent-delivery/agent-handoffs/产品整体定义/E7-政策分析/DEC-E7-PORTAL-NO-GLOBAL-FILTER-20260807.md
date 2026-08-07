# DEC-E7-PORTAL-NO-GLOBAL-FILTER · 政策扶持门户不设全局筛选条

| 字段 | 值 |
|---|---|
| id | `DEC-E7-PORTAL-NO-GLOBAL-FILTER-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认） |
| approval_status | `approved` |
| 上级 | `DEC-E7-PORTAL-TAB-MERGE-A-20260807` |

## 决策

`/policy-portal/overview` 单壳**不挂**页级全局 ContextBar（区域 + 时间 + 产业）。

筛选需求由各一级 Tab / 概览内视图**本地控件**承接，避免与深圳 Tab（区域固定）、地图 scope、概况级别切换冲突。

| 落点 | 本地控制 |
|---|---|
| overview · stats | 产业 Cascader + 地域 Cascader + **同级对照**多选（全国档关闭）；筛选条上下结构、一行三列；URL `industry`/`geo`/`compare` |
| overview · map | 产业 Cascader + 地域 Cascader（**无对照**）；一行两列；与 stats 共享 `industry`/`geo` |
| overview · rank | 省级排名 / 城市排名（不共用 geo/industry/compare）；见 RANK-PRESENTATION |
| coverage | 链图交互；产业选择若需则 Tab 内加 |
| latest | 地域 Cascader（同概览 `PolicyPortalRegionSelect`，stacked）+ 级别多选 |
| shenzhen | 地域锁定深圳域（可下钻各区）+ 共享产业；stats 各区对照；map 地图/列表双视图；见 SHENZHEN-MIRROR |

与产业总览「当前 L0 产业」不同：政策扶持不以页级万能筛选条驱动四 Tab。

## scope_effect

不增删 Bid 叶子；去掉 Demo 空挂全局筛选。
