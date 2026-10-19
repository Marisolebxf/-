# 焦点识别(单个政策) · 功能点覆盖（policy.focus-one / L35 单政策变体）

> catalog `policy.focus-one` · path `/policy/focus-one`  
> A 线真源：`fp-split-by-api-run/work/L35.md`（现行稿只挂 `policy.focus`，path 为 GET `/policy/v1/policy/analysis/focus`）  
> 挂接：`fp-split-by-api-run/_l6-to-catalog-map.yaml` `catalog_skip` · `policy.focus-one` = L35 的单政策变体，挂 L35 时按 path 去重  
> B 线用例：`API-焦点识别(单个政策)-用例.md`（第二轮 **API-01409**～**01418**）  
> 不改 `work/L35.md`。不把 `policy.focus` 的 field 再灌成一套用例。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.focus-one.main | POST | /policy/v1/policy/analysis/focus-one | API-01409～01418 | unavailable（备注注明未交付；用例仍按文档返回体写） |

下拉 title 仅 **单条焦点识别**。主流程 API-01409；备选（省略 mode / title / execution / aux）API-01410～01413；反向（缺 text、非法 mode / title / execution / aux）API-01414～01418。

---

## path 去重（L35 已有行，本页不开用例）

`work/L35.md` 表行 16。其中 6 行挂在 GET `/policy/v1/policy/analysis/focus`（`policy.focus.main`），与本页 POST `/policy/v1/policy/analysis/focus-one` 不是同一 path。按 path 去重，这些 field 留给政策焦点识别页，本页用例编号留空。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L35 \| policy.focus.main \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | — | 无对应功能点 | path 为 GET focus，非本页 POST focus-one |
| L35 \| policy.focus.main \| region_code \| 算法输入-region_code区域编码 | catalog region_code | — | 无对应功能点 | 同上 |
| L35 \| policy.focus.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | — | 无对应功能点 | 同上 |
| L35 \| policy.focus.main \| focus_score \| 算法输出-focus_score焦点指数 | catalog focus_score | — | 无对应功能点 | 同上；本页文档输出是 focus_list / bottleneck_list / suggestions |
| L35 \| policy.focus.main \| _empty \| 焦点识别无数据空态 | 契约空结果 | — | 无对应功能点 | 同上；本页不为空态单开用例 |
| L35 \| policy.focus.main \| _fail \| 焦点识别查询失败 | 契约错误态 | — | 无对应功能点 | 同上；本页反向只覆盖本接口 5 个入参 |

其余 10 行 `endpoint_id` 为空、`catalog_status=req_only`，无本页 path。B 线记 **无对应功能点**，不单独开 API 用例：

| 功能点键 | 规则来源 | 状态 |
|----------|----------|------|
| L35 \| etl_clean_standardize \| 政策文本与执行数据标准化清洗 | 需规（1）标准化处理 | 无对应功能点 |
| L35 \| multidim_indicator_expert_threshold \| 多维度指标体系与评估阈值 | 需规指标体系 | 无对应功能点 |
| L35 \| indicator_weight_trend_eval \| 指标权重计算与趋势特征识别 | 需规权重与趋势 | 无对应功能点 |
| L35 \| focus_bottleneck_extract \| 焦点与堵点清单提取 | 需规焦点堵点提取 | 无对应功能点 |
| L35 \| focus_bottleneck_suggestion_outputs \| 焦点列表堵点清单与优化建议输出 | 需规（2）三类输出 | 无对应功能点 |
| L35 \| associated_analysis_report \| 关联分析报告语义 | 需规（2）关联报告 | 无对应功能点 |
| L35 \| dynamic_source_threshold_refresh \| 数据源与阈值动态更新 | 需规动态更新 | 无对应功能点 |
| L35 \| policy_tag_online_retrieval \| 政策标签在线检索语义 | 需规（3）标签检索 | 无对应功能点 |
| L35 \| dimension_time_datasource_scope \| 分析维度时间区间与数据源类型 | 需规（3）调用范围 | 无对应功能点 |
| L35 \| api_sdk_policy_system_monitor \| API SDK 政策系统对接与监测 | 需规（3）API/SDK | 无对应功能点 |

---

## 本页 B 线独有（L35 未列本 path）

现行 `L35.md` 没有 POST focus-one 的 field 行。下列键不在 A 线表内，状态记 **无对应功能点**。同一接口的 sampleResponse / responseFields 挂在主流程与备选上，不按 field 各写一条用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （L35 未列） \| policy.focus-one.main \| mode \| 算法输入-mode | API-01409、01410、01415 | 无对应功能点 | 01409 传 sample mode=rule；01410 不传；01415 mode=__invalid__ |
| （L35 未列） \| policy.focus-one.main \| title \| 算法输入-title | API-01409、01411、01416 | 无对应功能点 | 01409 传 sample 标题；01411 不传；01416 title 为 number |
| （L35 未列） \| policy.focus-one.main \| text \| 算法输入-text | API-01409、01414 | 无对应功能点 | 01409 传 sample 政策文本；01414 不传必填 text |
| （L35 未列） \| policy.focus-one.main \| execution \| 算法输入-execution | API-01409、01412、01417 | 无对应功能点 | 01409 传 sample 执行数据；01412 不传；01417 execution 为 number |
| （L35 未列） \| policy.focus-one.main \| aux \| 算法输入-aux | API-01409、01413、01418 | 无对应功能点 | 01409 传 sample 辅助数据；01413 不传；01418 aux 为 number |
| （L35 未列） \| policy.focus-one.main \| focus_list \| 算法输出-focus_list | API-01409～01413 | 无对应功能点 | 正向预期逐字段含 focus_list 及元素 term、score、evidence |
| （L35 未列） \| policy.focus-one.main \| bottleneck_list \| 算法输出-bottleneck_list | API-01409～01413 | 无对应功能点 | 正向预期含 bottleneck_list 及元素 item、evidence |
| （L35 未列） \| policy.focus-one.main \| suggestions \| 算法输出-suggestions | API-01409～01413 | 无对应功能点 | 正向预期含 suggestions 及元素 item、reason |
| （L35 未列） \| policy.focus-one.main \| persisted \| sampleResponse-persisted | API-01409～01413 | 无对应功能点 | sampleResponse 多出字段，随主流程与备选断言；responseFields 未列 |

---

## 计数

| 项 | 数 |
|----|----|
| 本页接口 | 1 |
| 用例 | 10（主流程 1 + 备选 4 + 反向 5） |
| 编号 | API-01409～API-01418 |
| L35 GET path 行 | 6（无对应功能点，不灌用例） |
| L35 req_only | 10（无对应功能点） |
| 本页 B 线 field | 9（无对应功能点，挂在上述 10 条上） |
