# DEC-E7-PORTAL-TAB-MERGE-A · 政策扶持门户一级 Tab 合并（方案 A）

| 字段 | 值 |
|---|---|
| id | `DEC-E7-PORTAL-TAB-MERGE-A-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认选 A） |
| approval_status | `approved` |
| source_relation | product_interpretation |
| 上级 | `DEC-E7-PORTAL-INCLUDE-20260805` |

## 决策

智慧服务门户「政策扶持」**Bid 六叶子（P-17~P-22）能力不删**，一级导航对齐产业链总览，收成 **4 个一级 Tab**（单壳 `/policy-portal/overview`）：

| 一级 Tab | key | 承接 Bid | Tab 内结构 |
|---|---|---|---|
| 政策概览（默认） | `overview` | P-17 + P-18 + P-20 | Segmented：`stats` / `map` / `rank`；stats/map 本地产业+地域（stats 另有同级对照）；rank 省/市榜（见后续 DEC） |
| 产业覆盖 | `coverage` | P-19 | 链图 + 覆盖/缺口 |
| 最新政策动态 | `latest` | P-21 | 时间线 |
| 深圳政策 | `shenzhen` | P-22 | S1 四段镜像：`szView=stats\|map\|coverage\|latest`；对照=各区；**无力度榜**（见 SHENZHEN-MIRROR） |

旧独立路由 `/policy-portal/map|intensity-rank|industry-coverage|latest|shenzhen` **redirect** 到对应 `?tab=`（概览内加 `view=`）。

## 不变

- 门户只入篮、不发起分析、不生成报告  
- 与专题 `/policy/*` 分轨  
- Bid 六叶子仍可在 TRACE / 走查中逐条验收（Tab 内视图 = 叶子落点）

## scope_effect

不增删 Bid 叶子；改变门户 IA 一级分页与 Demo 路由形态。
