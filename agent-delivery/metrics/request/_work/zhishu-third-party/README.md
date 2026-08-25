# 智树范围 → seed `third_party`（2026-08-25）

> 淮政玮口头：按智树工作范围确定 API/`third_party` 并更新 seed。  
> 只改 `algorithm_type`（写入 `third_party`，不写 `API`）。不改口径 / 公式 / 源表 / D1。  
> 回滚：`apply-result.json` 的 `applied[].from`。脚本：`apply-zhishu-scope-third-party.mjs`。

## 切面

| 打 `third_party` | 不打 |
|---|---|
| A1 `coverage_status: third_party` 的 37 库叶（TECH/ORG/TALENT 基础/图谱/深度；本批已是 47 条存量） | 企业 / 产业链 / 产业服务 / 政策 / 综合自算 |
| 专题 3/4/5 域其余消费指标（机构/技术链/人才深度，含 STAT 页面核） | 展示态势完整链路：DS-07 科技创新评估 3 条 MODEL |
| 展示人才态势 DS-13–16、知识图谱 DS-21–24 的 OPEN 号 | 态势技术要素计数 3 条 STAT；查询结果 `*_QUERY` |
| 已有人才指数 / 专家 H 指数 4 条 INNOV（本批已是 third_party） | `M_INNOV_PLAN_TALENT_FLOW` 等发展规划人才流动（智树） |
| | 数据资源 DS-17–20：运营 STAT / other_system，不按页号灌 |

九新对人表「交付形态 SQL/Python/API」仍是对接轴，**不等于** seed 类型。seed 用 `third_party` 表示智树不写这段计算。`M_SYNTH_GRAPHAPI_116_1` A1 覆盖 `full`、seed 已是 `third_party`（封装图谱能力），本批未改。

## 结果

| | 条数 |
|---|---:|
| 本批改写 | **56** |
| 此前已是 third_party | 47 |
| 改后全库 third_party | **103** |
| 改前 → 改后类型 | MODEL 228→203 · GRAPH 53→32 · STAT 164→158 · MIXED 33→31 · COMPUTE 7→5 |

改写分域：TALENT 18 · SYNTH 14（图谱页 OPEN）· TECH 13 · ORG 11。

进度表：`third_party` 不再被 `.upper()` 误打成 UNKNOWN。卡点「算法（唐绍祖）」387 → **292**。这 103 条按综合就绪走（多为口径待确认），不进绿框。离线表已覆写 `registry/export/指标与数据开发进度.xlsx`。
