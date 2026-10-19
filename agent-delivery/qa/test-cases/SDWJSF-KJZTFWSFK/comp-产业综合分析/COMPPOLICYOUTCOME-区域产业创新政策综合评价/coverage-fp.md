# 区域产业创新政策综合评价 · 功能点覆盖（comp.policy-outcome / L54）

> catalog `comp.policy-outcome` · path `#/industry-comp/policy-outcome`  
> A 线真源：`fp-split-by-api-run/work/L54.md`（只读，未改）  
> B 线用例：`API-区域产业创新政策综合评价-用例.md`（第二轮 **API-01792**～**01801**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.policy-outcome`

> **path 独占**：`GET /comp/v1/comp/region-policy-outcome` 为本页 `政策成果评价` 独占，与同模块其它 `region-*-outcome` path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute` 只挂 title「区域产业创新政策综合评价模型」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.policy-outcome.main | GET | /comp/v1/comp/region-policy-outcome | API-01792～01796 | unavailable |
| comp.policy-outcome.m_synth_185_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | API-01797～01801 | available |

---

## 功能点 → 用例矩阵（挂 L54.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L54 \| comp.policy-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-01792、01793、01795 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L54 \| comp.policy-outcome.main \| year \| 算法输入-year年份 | catalog year | API-01792、01794、01796 | 已覆盖 | 主路径 year=2025 + 省略可选 year + 非法 year=-1 |
| L54 \| comp.policy-outcome.main \| index \| 算法输出-index政策创新成果指数 | catalog index | API-01792 | 已覆盖 | 主流程断言 index（number，示例 66.3）；备选 01793、01794 同结构。文档标记未交付 |
| L54 \| comp.policy-outcome.main \| _empty \| 政策成果评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L54 \| comp.policy-outcome.main \| _fail \| 政策成果评价查询失败 | 契约错误态 | API-01795、01796 | 部分覆盖 | 仅非法 region、非法 year 的 message 或 msg；可选省略按备选正向，不把「不传」写成失败 |
| L54 \| （req_only） \| etl_nlp_policy_standardize \| 政策专题库采集与文本结构化 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| three_dim_indicators_threshold \| 三维政策指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| weight_threshold_synthesis \| 维度指标加权综合指数 | 需规加权综合 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| dimension_sub_eval_results \| 单维度分项评价结果 | 需规（2）分项评价 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| regional_rank_compare \| 区域排名与横向对比 | 需规区域对比排名 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| trend_viz_analysis_report \| 趋势分析与可视化报告 | 需规趋势可视化 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| historical_time_series \| 历史对比与时间序列分析 | 需规历史时序 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| region_time_policy_category_scope \| 区域时间政策类别查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| online_monitor_refresh \| 在线监测与结果刷新 | 需规（3）监测展示 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| index_sub_rank_advice_outputs \| 指数分项排名建议四类输出 | 需规（2）四类输出 | — | 无对应功能点 | 不单开 API 用例 |
| L54 \| （req_only） \| api_sdk_decision_platform \| API SDK 与决策分析系统对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 API 用例 |

sampleResponse 中另有、A 线未单列的 field 已写入 API-01792 正向预期（备选 01793、01794 同结构）：`rank`、`yoy`、`adv`、`radar`（政策供给 / 政策力度 / 政策效果）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`。不按这些字段各开一条用例。

---

## B 线独有 endpoint（L54 未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.policy-outcome.m_synth_185_1 | API-01797～01801 | 无对应功能点 | L54 只挂 GET `comp.policy-outcome.main`。01797 主流程 sampleRequest（region=440300、year=2025），断言 metric_id、hint，并要求 responseFields 的 index；01798 省略 region；01799 省略 year；01800 非法 region；01801 非法 year |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（region、year、index） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| 无对应功能点 | 11（req_only）+ 1 个 B 线 endpoint（m_synth_185_1，5 条用例） |
| L54 矩阵行 | 16 |
| API 用例 | 10（01792～01801，连续用满） |
| 主流程 | 2（01792 政策成果评价；01797 区域产业创新政策综合评价模型） |
| 备选 | 4（01793、01794、01798、01799） |
| 反向 | 4（01795、01796、01800、01801） |
