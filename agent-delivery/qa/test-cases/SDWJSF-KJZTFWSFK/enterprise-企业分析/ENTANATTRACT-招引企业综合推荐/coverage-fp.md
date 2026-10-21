# 招引企业综合推荐 · 功能点覆盖（entan.attract / L33）

> catalog `entan.attract` · path `#/entan/attract`  
> A 线真源：`fp-split-by-api-run/work/L33.md`  
> B 线用例：`../ENTANATTRACT-企业招引潜力评估/FUNC-企业招引潜力评估-用例.md`（第三轮 **FUNC-00153**～**00158**；旧 API-00984～00987 作废）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.attract.recommend | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | FUNC-00153、00154 | unavailable |
| entan.attract.recommend.m_ent_policy_match_score | POST | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | FUNC-00155、00156 | available |

---

## 功能点 → 用例矩阵（挂 L33.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L33 \| entan.attract.recommend \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | FUNC-00153、00154 | 已覆盖 | 合法集合 + 缺 enterprise_codes |
| L33 \| entan.attract.recommend \| rankings \| 算法输出-rankings招引推荐排名体 | FUNC-00153 | 已覆盖 | 主流程断言 value.result.rankings 及元素字段 |
| L33 \| entan.attract.recommend \| _empty \| 招引推荐无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L33 \| entan.attract.recommend \| _fail \| 招引推荐计算失败 | FUNC-00154 | 部分覆盖 | 仅缺 enterprise_codes 反向 |

---

## B 线独有（L33 未列 endpoint）

| endpoint_id | title | 用例编号 | 标记 |
|-------------|-------|----------|------|
| entan.attract.recommend.m_ent_policy_match_score | 政策匹配度 | FUNC-00155、00156 | 无对应功能点 |

catalog 有该接口（status=available），L33 未挂 field 行，不按 field 拆用例。

---

## req_only 行（无 endpoint 挂接）

L33.md 中 `etl_clean_standardize`、`triple_dimension_indicator_threshold`、`historical_sample_model_train`、`weighted_attraction_index_compute`、`threshold_rank_preferred_select`、`dynamic_policy_data_refresh`、`preferred_list_industry_rank_outputs`、`analysis_report_semantic`、`tag_industry_region_filter_scope`、`api_sdk_platform_export` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
