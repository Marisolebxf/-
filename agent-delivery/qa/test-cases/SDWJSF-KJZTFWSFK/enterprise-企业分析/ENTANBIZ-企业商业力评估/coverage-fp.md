# 企业商业力评估 · 功能点覆盖（entan.biz / L32）

> catalog `entan.biz` · path `#/entan/biz`  
> A 线真源：`fp-split-by-api-run/work/L32.md`  
> B 线用例：`API-企业商业力评估-用例.md`（第二轮 **API-00976**～**00983**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.biz.rank | POST | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | API-00976、00977 | unavailable |
| entan.biz.detail | GET | /entan/v1/biz-power/{orgId} | API-00978、00979 | unavailable |
| entan.biz.weights | GET | /entan/v1/eval/weights | API-00980、00981 | unavailable |
| entan.biz.report | GET | /entan/v1/enterprises/{orgId}/report | API-00982、00983 | unavailable |

---

## 功能点 → 用例矩阵（挂 L32.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L32 \| entan.biz.rank \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | API-00976、00977 | 已覆盖 | 合法集合 + 缺 enterprise_codes |
| L32 \| entan.biz.rank \| enterprises \| 算法输出-enterprises企业商业力结果集 | API-00976 | 已覆盖 | 主流程断言 value.enterprises 及元素字段 |
| L32 \| entan.biz.rank \| _empty \| 商业力得分无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L32 \| entan.biz.rank \| _fail \| 商业力得分计算失败 | API-00977 | 部分覆盖 | 仅缺 enterprise_codes 反向 |
| L32 \| entan.biz.detail \| orgId \| 算法输入-orgId企业标识 | API-00978、00979 | 已覆盖 | 合法 orgId + 缺 orgId |
| L32 \| entan.biz.detail \| market_score \| 算法输出-market_score市场维度得分 | API-00978 | 已覆盖 | 正向断言 market_score |
| L32 \| entan.biz.detail \| _empty \| 商业力详情无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L32 \| entan.biz.detail \| _fail \| 商业力详情查询失败 | API-00979 | 部分覆盖 | 仅缺 orgId 反向 |
| L32 \| entan.biz.weights \| model \| 算法输入-model模型标识 | API-00980、00981 | 已覆盖 | 合法 model + 缺 model |
| L32 \| entan.biz.weights \| weight \| 算法输出-weight权重结果体 | API-00980 | 已覆盖 | 正向断言数组元素 weight |
| L32 \| entan.biz.weights \| _empty \| 模型权重无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L32 \| entan.biz.weights \| _fail \| 模型权重查询失败 | API-00981 | 部分覆盖 | 仅缺 model 反向 |
| L32 \| entan.biz.report \| orgId \| 算法输入-orgId企业标识 | API-00982、00983 | 已覆盖 | 合法 orgId + 缺 orgId |
| L32 \| entan.biz.report \| markdown \| 算法输出-markdown报告正文 | API-00982 | 已覆盖 | 正向断言 markdown |
| L32 \| entan.biz.report \| _empty \| 评估报告无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L32 \| entan.biz.report \| _fail \| 评估报告生成失败 | API-00983 | 部分覆盖 | 仅缺 orgId 反向 |

---

## req_only 行（无 endpoint 挂接）

L32.md 中 `etl_clean_standardize`、`six_dimension_indicator_threshold`、`biz_model_train_optimize`、`weighted_business_power_compute`、`dimension_detail_analysis_semantic`、`trend_benchmark_semantic`、`dynamic_biz_refresh`、`cross_enterprise_compare_semantic`、`industry_compare_result_semantic`、`trend_chart_viz_support`、`enterprise_id_name_query_scope`、`api_sdk_invocation`、`biz_report_data_export` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
