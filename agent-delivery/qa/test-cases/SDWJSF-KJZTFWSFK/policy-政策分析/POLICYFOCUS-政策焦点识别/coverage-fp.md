# 政策焦点识别 · 功能点覆盖（policy.focus / L35）

> catalog `policy.focus` · 50897 · path `/policy/focus`  
> 用例 `API-政策焦点识别-用例.md`  
> A 线范围：**L35**（`fp-split-by-api-run/work/L35.md`）  
> 功能点键：`L35 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.focus.main | GET | /policy/v1/policy/analysis/focus | API-000449～API-000453 | catalog `status=unavailable`；不含 `policy.focus-one` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L35 \| policy.focus.main \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | API-000451 | 部分覆盖 | 非法/不存在 id；列表模式（空 policy_id）见 FOC-01 / API-000449，live 语义待 available |
| L35 \| policy.focus.main \| region_code \| 算法输入-region_code区域编码 | catalog region_code | API-000449 | 部分覆盖 | FOC-01 合法 region_code=440300；非法 region（FOC-04）本轮无独立用例 |
| L35 \| policy.focus.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000449、API-000452 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L35 \| policy.focus.main \| focus_score \| 算法输出-focus_score焦点指数 | catalog focus_score | API-000453 | 契约占位 | unavailable，禁止 sample 指数作通过条件 |
| L35 \| policy.focus.main \| _empty \| 焦点识别无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L35 \| policy.focus.main \| _fail \| 焦点识别查询失败 | 契约错误态 | API-000449、API-000450、API-000451、API-000452 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L35 \| \| etl_clean_standardize \| 政策文本与执行数据标准化清洗 | 需规（1） | — | 未覆盖 | req_only |
| L35 \| \| multidim_indicator_expert_threshold \| 多维度指标体系与评估阈值 | 需规指标体系 | — | 未覆盖 | req_only |
| L35 \| \| indicator_weight_trend_eval \| 指标权重计算与趋势特征识别 | 需规权重与趋势 | — | 未覆盖 | req_only |
| L35 \| \| focus_bottleneck_extract \| 焦点与堵点清单提取 | 需规焦点堵点提取 | — | 未覆盖 | req_only |
| L35 \| \| focus_bottleneck_suggestion_outputs \| 焦点列表堵点清单与优化建议输出 | 需规（2）三类输出 | — | 未覆盖 | req_only |
| L35 \| \| associated_analysis_report \| 关联分析报告语义 | 需规（2）关联报告 | — | 未覆盖 | req_only |
| L35 \| \| dynamic_source_threshold_refresh \| 数据源与阈值动态更新 | 需规动态更新 | — | 未覆盖 | req_only |
| L35 \| \| policy_tag_online_retrieval \| 政策标签在线检索语义 | 需规（3）标签检索 | — | 未覆盖 | req_only |
| L35 \| \| dimension_time_datasource_scope \| 分析维度时间区间与数据源类型 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L35 \| \| api_sdk_policy_system_monitor \| API SDK 政策系统对接与监测 | 需规（3）API/SDK | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 2（`policy_id`、`region_code`） |
| 契约占位 | 1（`focus_score`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000449～API-000453 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
