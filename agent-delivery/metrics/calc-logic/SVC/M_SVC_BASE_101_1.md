# 服务机构基础指标模型构建（M_SVC_BASE_101_1）· 封面号说明

## 基本信息

- 指标ID: M_SVC_BASE_101_1
- 指标名称: 服务机构基础指标模型构建
- 定位: 算法库 SRS **ALGO-SVC-BASE-101 整叶封面**（需求目录页）
- 一级归属: 05 深度挖掘算法 / 科技专题服务算法库 / 产业服务 / 基础指标
- 算法类型: STAT（T0-X 建议类型，未签——封面无算法语义，纯占位）
- 更新频率: n/a
- 对齐状态判定: 封面身份（2026-08-27 侯佳伟 1A 2A 3A；2026-10-13 human:徐滕强 选 B 落 seed v0.2.0）
- 是否在数据库: 否（恒 0 行是设计）
- 验收单元: ALGO-SVC-BASE-101（L−F 未挂页，无 UI 落点，不挂 MetricSpecCard）

## 这不是指标，是目录

需规 101 正文是**六大核心指标体系**，不是"算一个什么数"。T0-X 注册时给整叶挂的占位身份证。它：

- **不是复合指标 / 不是加权总分**（侯佳伟口述拍板原话）——不聚合、不加权、不出数
- **无统计口径可定义**：对象、度量、公式全在分项各自定义（每条分项 8 件套自己齐）
- 分项**回指** 05·101 作需求来源（srs_refs 挂本叶），但**不回写**封面任何数

## 六套对照（谁出哪块）

| 六套（需规 101） | 分项 ID | 类型 | 出处 |
|---|---|---|---|
| ① 全球服务机构产业布局 | `M_SVC_INDUSTRY_LAYOUT` | UNKNOWN（不在 STAT 21 批） | 50100 A1 |
| ② 全球服务机构分布 | `M_SVC_PT_GLOBAL_TOTAL` / `M_SVC_PT_REGION_ORG` / `M_SVC_PT_GLOBAL_TYPE_DIST` | STAT | STAT 21 序号 6/8/7 |
| ③ 投融资动态资讯 | `M_SVC_INVEST_Y` | UNKNOWN（不在本批） | 50100 A3 |
| ④ 新增动态 | `M_SVC_ORG_NEW_COUNT` | STAT | STAT 21 序号 2 ✅ |
| ⑤ 深圳规模 | `M_SVC_PT_SZ_TOTAL` / `M_SVC_PT_KEYORG_SCALE` | STAT | STAT 21 序号 11/10 |
| ⑥ 深圳分布 | `M_SVC_PT_SZ_REGION_ORG` / `M_SVC_PT_SZ_TYPE_DIST` / `M_SVC_PT_SZ_FIELD_DIST` | STAT | STAT 21 序号 13/12/14 |

另：①③底下真正做"分析"的是 MODEL 叶（`M_SVC_ORG_COVERAGE_DEPTH` 服务深度模型分、`M_SVC_ORG_TECH_SCORE` 技术力模型分，归唐绍祖模型轨），同样不回写封面。

## 三禁（治理规则）

1. **本 ID 不出数、不灌 ADS**：`svc_metric_fact` / `svc_metric_series` / `svc_metric_dist` 里本编号恒 0 行；出现即错
2. **分项回指、不回写**：分项需求来源继续挂 `05·101`，实现写"本合同叶=101，本条只出这一块"；禁止把分项 COUNT 加总写进本 ID、禁止用封面号顶替任一分项
3. **禁止 `COUNT(*)` / `compute_metric('M_SVC_BASE_101_1')` 顶替**：50100 `/industry-service/basic` 继续只出 A1–A6 六折叠块，各挂分项 ID

再灌一格"101 总数"会和第 1 条（ORG_TOTAL）、门户全球（第 6 条）、深圳规模（第 11 条）撞车。

## 计算公式

无。封面号不出数。

## 源库表字段

无。不建表、不灌数。

## 验收

- fact / series / dist 本编号保持 **0 行**
- 算法路由表（`lumen-algo-py`）没有本 ID
- 50100 A1–A6 不改挂本 ID

## 参考文献 / 依据

需规 `bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业服务/基础指标.md`（ALGO-SVC-BASE-101）；`SVC-ALGO-STAT-21-L01-侯佳伟待办.md` 序号 5（2026-08-27 1A 2A 3A + 封面回指规则表）；`ALGO-LIB-T0X-REGISTER-L01`（T0-X 占位注册）；`SVC-METRIC-COVER-STAT-L01` 2026-10-13 选 B。

## 更新记录

- 2026-08-24: T0-X 注册占位身份证（0.1.0，definition 空话）
- 2026-08-27: 侯佳伟拍板封面不出数 + 六套对照 + 三禁（未落 seed）
- 2026-10-13: human:徐滕强 选 B，封面身份落 seed v0.2.0（本文档建立）
