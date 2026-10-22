# LUMEN-SVC-JAVA-JOB-L02 · 深圳服务链现状分析空白修复

- 任务类型：bugfix（前端已验，后端结构性缺口补读面）
- 时间：2026-10-22 16:20–17:45
- 执行：agent:frontend / agent:algorithm / agent:api（监管人：徐滕强）

## 现象

「深圳服务链现状分析」页（svc:analysis:shenzhen）任务显示成功但横向对比区空白：「当前结果快照无城市场景，无法绘制对比图」。

## 根因（证据链）

1. **读面错配**：topic-py `_LEAF_SVCAN_PATH["shenzhen"] = /internal/v1/svcan/models?kind=all`。`kind=all` 只返回六容器（gap/relation/tech/attract/cultivate），**没有任何城市对比结构**。任务 `SVC-20261022-079` payload 实测确认。
2. **数据结构性缺口**：ADS 只有深圳单城真值（`M_SVC_SZ_SCALE=14033`、区县分布 9 行、tech_power 300 行、relation_chain 51 行），北上广/全国基准行 0 条。demo 年代是前端写死五城矩阵（`CITY_METRIC_VALUES`），lumen 规约（禁止前端 fixture、缺城不补列）不允许照抄，所以此前直接空。
3. **衍生 bug A（f-string 丢 f）**：新增 `_sz_compare` 的两条 SQL 第二段字符串缺 `f` 前缀，`{ads}` 字面量下发 MySQL 被当库名 → `1142 SELECT denied` → `_q` fail-soft 吞掉 → 诚实降级 missing。线上 pod 打印真实 SQL 抓到。
4. **衍生 bug B（status 误标 empty）**：`fetch_models` 的 `has` 检查只认五容器键，`kind=sz` 拿到 `compare.cities` 后仍报 `empty=true`。

## 修复

| 仓 | commit | 内容 |
|---|---|---|
| lumen-algo-py | `ba6900f` → `b7c6c4f` → `3a08e37` | 新增 `fetch_models(kind=sz)` + `/internal/v1/svcan/models/sz` 路由：深圳列 ADS 真值（scale=M_SVC_SZ_SCALE / tech=svc_tech_power_score 均值 / density=svc_relation_chain 汇总行），北上广与全国平均=冻结演示值复刻 demo（data_flag=mock，Q-SVC-010 待甲方口径），缺行诚实缺格；tier 认 M_SVC_SZ_TIER（当前缺行 → label 空 + basis 注明）；修 f 前缀；修 status 标记 |
| lumen-topic-py | `39be306` | `_LEAF_SVCAN_PATH["shenzhen"]` 改 `/internal/v1/svcan/models/sz`；补路由断言测试 |
| lumen-ui-topic | `0f4daf6` | 自检镜像 `parseCompare` 补嵌套 `metrics` 数组解析 + 五城真实形态断言（解析器本体无需改，`compare.cities[].metrics[]` 正好命中 `ingestCityObject` nestedMetrics 契约） |

另有前序提交 `8ceaff5`（技术力评估解析 svcan tech 读面，已由用户验证）。

## 验证

- algo-py：14/14 单测绿（含「SQL 不得含未插值占位符」回归）；pipeline 2726 全绿含 e2e:chain-gold。
- topic-py：18/18 绿；`deploy:search-py` manual job 手动触发成功。
- 线上 E2E（跳板 → search-py `POST /internal/gkx-svc/analysis/tasks/create`）：
  - `E2E-SZ-F-20261022-174101` → `status=succeeded`，payload `status=ads_ready`、`empty=false`
  - 深圳 metrics：`scale=14033 (ads)`、`tech=33.54 (ads)`、`density=4.6e-05 (ads)`
  - 基准城 nat/bj/sh/gz 全部 `data_flag=mock`
  - tier：M_SVC_SZ_TIER 缺行，label 空（诚实态，页面上梯仪表盘不渲染，只显结论区）
- E2E 任务为 Python 内存态（`_TASKS` dict），不落库不占分析上限。

## 架构合规自检

- D2 调用链 ✅ 前端 → Java → topic-py → algo-py `/internal/*`，无越层
- D9 血缘 ✅ 每格带 `metric_id` + `data_flag`（ads/mock/missing 三态），缺值不填 0，基准城明确 mock 不冒充真值
- ⚠️ 待甲方确认：五城对比基准数值（Q-SVC-010）、梯队分档口径（Q-SVCCHAIN-04）仍是演示值，黄灯已随 payload 上送
- 已知坑记录：镜像 tag=latest 不触发 K8s 滚动，CI deploy 后需 `rollout restart`（deploy:api/worker/search-py 均如此）

## 遗留

- `M_SVC_SZ_TIER`、`M_SVC_SZ_CHAIN_COMPLETENESS` ADS 无行 → 梯队仪表盘不渲染（诚实空）；待甲方口径后由数据侧补种子。
- algo-py 镜像 latest tag 的滚动问题建议 devops 评估改 sha tag（本次未动）。
