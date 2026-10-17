# 企业商业力评估 · 功能点覆盖（entan.biz / L32）

> catalog `entan.biz` · 50897 · path `/entan/biz`  
> **用例册**：`API-企业商业力评估-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00126`～`00141`，共 **16** 条）  
> A 线范围：**L32**（`fp-split-by-api-run/work/L32.md`）  
> 功能点键：`L32 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.biz.rank | POST | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | API-00126～00129、00141 | catalog `status=unavailable` |
| entan.biz.detail | GET | /entan/v1/biz-power/{orgId} | API-00130～00133 | catalog `status=unavailable` |
| entan.biz.weights | GET | /entan/v1/eval/weights | API-00134～00137 | catalog `status=unavailable` |
| entan.biz.report | GET | /entan/v1/enterprises/{orgId}/report | API-00138～00140 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L32 \| entan.biz.rank \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00127、00128、00129、00141 | 部分覆盖 | 缺省/空集合/非法/类型；live 合法集合成功校验待 endpoint available 后补 |
| L32 \| entan.biz.rank \| enterprises \| 算法输出-enterprises企业商业力结果集 | catalog enterprises | API-00126 | 契约占位 | unavailable，禁止 sample 商业力指数作通过条件 |
| L32 \| entan.biz.rank \| _empty \| 商业力得分无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法非空集合必空」试调证据 |
| L32 \| entan.biz.rank \| _fail \| 商业力得分计算失败 | 契约错误态 | API-00126、00127、00128、00129、00141 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| L32 \| entan.biz.detail \| orgId \| 算法输入-orgId企业标识 | catalog orgId | API-00131、00132、00133 | 部分覆盖 | 非法/占位 orgId；鉴权见 00133 |
| L32 \| entan.biz.detail \| market_score \| 算法输出-market_score市场维度得分 | catalog market_score | API-00130 | 契约占位 | unavailable |
| L32 \| entan.biz.detail \| _empty \| 商业力详情无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L32 \| entan.biz.detail \| _fail \| 商业力详情查询失败 | 契约错误态 | API-00130、00131、00132 | 已覆盖 | |
| L32 \| entan.biz.weights \| model \| 算法输入-model模型标识 | catalog model | API-00135、00136、00137 | 部分覆盖 | 缺省/非法/空 model |
| L32 \| entan.biz.weights \| weight \| 算法输出-weight权重结果体 | catalog weight | API-00134 | 契约占位 | 样例为数组、契约字段 weight，执行期 as-built |
| L32 \| entan.biz.weights \| _empty \| 模型权重无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L32 \| entan.biz.weights \| _fail \| 模型权重查询失败 | 契约错误态 | API-00134、00135、00136、00137 | 已覆盖 | |
| L32 \| entan.biz.report \| orgId \| 算法输入-orgId企业标识 | catalog orgId | API-00139、00140 | 部分覆盖 | 非法/占位 orgId |
| L32 \| entan.biz.report \| markdown \| 算法输出-markdown报告正文 | catalog markdown | API-00138 | 契约占位 | unavailable |
| L32 \| entan.biz.report \| _empty \| 评估报告无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L32 \| entan.biz.report \| _fail \| 评估报告生成失败 | 契约错误态 | API-00138、00139、00140 | 已覆盖 | |
| L32 \| （无 endpoint） \| etl_clean_standardize \| 多源市场与产业链数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| six_dimension_indicator_threshold \| 六维度指标与判定阈值 | 需规指标体系 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| biz_model_train_optimize \| 商业力模型训练与优化 | 需规（1）模型训练 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| weighted_business_power_compute \| 加权综合商业力指数计算 | 需规加权综合 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| dimension_detail_analysis_semantic \| 分维度详细分析输出语义 | 需规分维度分析 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| trend_benchmark_semantic \| 趋势变化与行业对标语义 | 需规趋势对标 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| dynamic_biz_refresh \| 动态监测与评估结果更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| cross_enterprise_compare_semantic \| 跨企业对比分析语义 | 需规跨企业对比 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| industry_compare_result_semantic \| 行业对比分析结果语义 | 需规（2）行业对比 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| trend_chart_viz_support \| 趋势变化图表可视化支撑 | 需规（2）趋势图表 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业名称或标识查询语义 | 需规（3）调用方式 | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| api_sdk_invocation \| RestfulAPI 与 SDK 调用 | 需规（3）API/SDK | — | 未覆盖 | req_only |
| L32 \| （无 endpoint） \| biz_report_data_export \| 商业力报告与数据导出 | 需规（3）报告导出 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（四 endpoint `_fail` 契约行） |
| 部分覆盖 | 4（四 endpoint 入参 field） |
| 契约占位 | 4（enterprises / market_score / weight / markdown） |
| 未覆盖 | 17（含 `_empty` 4 + req_only 13） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 16 |
| 编号 | API-00126～API-00141 |
| `_empty` 未覆盖 | 4 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
