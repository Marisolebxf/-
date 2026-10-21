# 区域产业创新政策综合评价 · 功能点覆盖（comp.policy-outcome / L54）

> catalog `comp.policy-outcome` · path `#/industry-comp/policy-outcome`  
> A 线真源：`fp-split-by-api-run/work/L54.md`（只读，未改 work）  
> **B 线用例**：`FUNC-区域产业创新政策综合评价-用例.md`（第三轮 **FUNC-01038**～**FUNC-01049**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.policy-outcome`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

> **path 独占**：`GET /comp/v1/comp/region-policy-outcome` 为本页 `政策成果评价` 独占。`POST /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute` 只挂 title「区域产业创新政策综合评价模型」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.policy-outcome.main | GET | /comp/v1/comp/region-policy-outcome | FUNC-01038～01042 | unavailable |
| comp.policy-outcome.m_synth_185_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | FUNC-01043～01047 | available |

---

## 功能点 → 用例矩阵（挂 L54.md）

同一 field_key 的多种场景挂在同一组 FUNC 号上，不按 field_key 各写一条用例。`政策成果评价` 的 sampleResponse 另有 `rank`、`yoy`、`adv`、`radar`（政策供给 / 政策力度 / 政策效果）、`bar_items`、`pie_items`、`rows`（name / score / rank / tag / note），已写入 01038～01040 正向预期；A 线未单列这些 field_key。`responseFields` 只声明顶层 `index`（政策指数）。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L54 \| comp.policy-outcome.main \| region \| 算法输入-region区域标签 | catalog region | FUNC-01038、01039、01041 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L54 \| comp.policy-outcome.main \| year \| 算法输入-year年份 | catalog year | FUNC-01038、01040、01042 | 已覆盖 | 主路径 year=2025 + 省略可选 year + 非法 year=-1 |
| L54 \| comp.policy-outcome.main \| index \| 算法输出-index政策创新成果指数 | catalog index | FUNC-01038、01039、01040 | 已覆盖 | 主流程与两条备选断言 index（number，示例 66.3）及 sampleResponse 其余字段；catalog unavailable |
| L54 \| comp.policy-outcome.main \| _empty \| 政策成果评价无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空指数与名单，无稳定空结果构造条件，不单开空态用例 |
| L54 \| comp.policy-outcome.main \| _fail \| 政策成果评价查询失败 | 契约错误态 | FUNC-01041、01042 | 部分覆盖 | 仅非法 region、非法 year；预期 message 或 msg 指出该参数非法。省略参数记备选。上游或网关失败未单开 |
| （页面清单） \| comp.policy-outcome \| 接口信息 / 算法测试 | 联调台清单 | FUNC-01048、01049 | 已覆盖 | 双接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L54.md 中下列 11 行 **req_only**，endpoint 为空，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L54 \| （req_only） \| etl_nlp_policy_standardize \| 政策专题库采集与文本结构化 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| three_dim_indicators_threshold \| 三维政策指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| weight_threshold_synthesis \| 维度指标加权综合指数 | 需规加权综合 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| dimension_sub_eval_results \| 单维度分项评价结果 | 需规（2）分项评价 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| regional_rank_compare \| 区域排名与横向对比 | 需规区域对比排名 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| trend_viz_analysis_report \| 趋势分析与可视化报告 | 需规趋势可视化 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| historical_time_series \| 历史对比与时间序列分析 | 需规历史时序 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| region_time_policy_category_scope \| 区域时间政策类别查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| online_monitor_refresh \| 在线监测与结果刷新 | 需规（3）监测展示 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| index_sub_rank_advice_outputs \| 指数分项排名建议四类输出 | 需规（2）四类输出 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L54 \| （req_only） \| api_sdk_decision_platform \| API SDK 与决策分析系统对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 FUNC 用例 |

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.policy-outcome.m_synth_185_1 | FUNC-01043～01047 | 无对应功能点 | L54 未列该 POST endpoint 的 field_key。01043 主流程 sampleRequest（region=440300、year=2025），断言 metric_id、hint 与 responseFields 的 index；01044 省略 region；01045 省略 year；01046 非法 region；01047 非法 year |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`region`、`year`、`index`）+ 清单 2 |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`comp.policy-outcome.m_synth_185_1`，5 条用例） |
| FUNC 用例条数 | **12**（01038～01049） |
| 主流程 | 2（01038 政策成果评价；01043 区域产业创新政策综合评价模型） |
| 备选 | 4（01039、01040、01044、01045） |
| 反向 | 4（01041、01042、01046、01047） |
| 清单 | 2（01048、01049） |
| 编号闭区间 | **FUNC-01038**～**FUNC-01049** |
| 金样 | FUNC-01038 |
| 旧 API 册 | API-01792～01801 作废，见 FUNC 册 §4 |
