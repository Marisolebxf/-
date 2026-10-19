# 培育企业综合推荐 · 功能点覆盖（entan.cultivate / L34）

> catalog `entan.cultivate` · path `#/entan/cultivate`  
> A 线真源：`fp-split-by-api-run/work/L34.md`  
> B 线用例：`API-培育企业综合推荐-用例.md`（第二轮 **API-00988**～**00989**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.cultivate.recommend | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | API-00988、00989 | unavailable |

---

## 功能点 → 用例矩阵（挂 L34.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L34 \| entan.cultivate.recommend \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | API-00988、00989 | 已覆盖 | 合法集合 + 缺 enterprise_codes |
| L34 \| entan.cultivate.recommend \| rankings \| 算法输出-rankings培育推荐排名体 | API-00988 | 已覆盖 | 主流程断言 value.result.rankings 及元素字段 |
| L34 \| entan.cultivate.recommend \| _empty \| 培育推荐无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L34 \| entan.cultivate.recommend \| _fail \| 培育推荐计算失败 | API-00989 | 部分覆盖 | 仅缺 enterprise_codes 反向 |

---

## req_only 行（无 endpoint 挂接）

L34.md 中 `etl_clean_standardize`、`triple_dimension_indicator_threshold`、`historical_sample_model_train`、`weighted_cultivation_index_compute`、`threshold_rank_preferred_select`、`dynamic_policy_market_refresh`、`preferred_rank_industry_viz_outputs`、`analysis_report_semantic`、`industry_policy_scale_filter_scope`、`api_sdk_platform_export` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
