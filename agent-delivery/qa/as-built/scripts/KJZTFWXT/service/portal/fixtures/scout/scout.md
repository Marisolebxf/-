# 无头实勘 /service-portal（2026-10-14 BATCH32 · svc-portal 回炉）

- surveyed_at: 2026-10-14（`survey-page.mjs` + `_probe.mjs` + `_env-gate-probe.mjs`）
- **env-gate**: `env-gate.json` overall=**pass**（截图 `env-gate-*.png`）
- url: http://111.198.38.90:50892/service-portal/overview（入口 `/service-portal` 重定向）
- title: 专题服务 - 科技专题服务系统
- h1: 全球服务机构概况
- screenshot: page.png / page-*.png / env-gate-*.png

## 壳层

| 控件 | 实勘 |
|------|------|
| 五 Tab | 全球服务机构概况（默认）/ 产业分布 / 区域分布 / 技术能力 / 深圳产业服务介绍 |
| 页头按钮 | primary「深圳产业服务介绍」→ `/service-portal/shenzhen` |
| 产业下拉 | placeholder「全部产业」；选项 **15** 集群（与附录 B 一致） |
| 产业链下拉 | placeholder「全部产业链」；**初始 disabled**；选产业后解锁且不代选 |
| 对比篮 | 常默认展开「共 N 项」；操作前先「关闭对比篮」 |

## 概况 Tab

- 三区块 H3：数量分析 · 历年总量趋势 / 类型分析 · 机构类型占比 / 规模分析 · 人员规模分布
- KPI 实勘标签：全球机构约数 / 本年新增机构 / 环节合计（可重复计）
- 规模区可诚实空：「概况实包无人员规模四档，保持空态」
- 评审开启：指标说明 ×4 类挂点 + 三追溯 +「指标未登记：机构类型占比」
- 关评审 reload：metricBtnCount=0（scout-review-off.json）

## 其余 Tab（二次探针）

| Tab | 子路由 | 要点 |
|-----|--------|------|
| 产业分布 | `/industry-distribution` | 六类/环节/热力；环节与热力常空 |
| 区域分布 | `/region-map` | **全球视图 / 全国视图**；省级排行；无坐标时常无圆点 |
| 技术能力 | `/capability-rank` | 五维等权口径文案；默认产业可无入榜诚实空 |
| 深圳介绍 | `/shenzhen` | 四统计区 + 重点机构墙；墙常「暂无重点机构」 |

## 产物文件

- scout.json / scout.md / page.png — 首勘概况
- scout-deep-*.json / scout-tabs.json / scout-filter-state.json / scout-industry-options.json / scout-after-industry.json / scout-review-off.json / scout-drawer.json / scout-deep.md — 二次探针
