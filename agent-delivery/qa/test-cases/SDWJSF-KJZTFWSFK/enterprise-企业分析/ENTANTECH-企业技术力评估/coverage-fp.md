# 企业技术力评估 · 功能点覆盖（entan.tech / L31）

> catalog `entan.tech` · path `#/entan/tech`  
> A 线真源：`fp-split-by-api-run/work/L31.md`  
> B 线用例：`FUNC-企业技术力评估-用例.md`（第三轮 **FUNC-00131**～**00142**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.tech.rank | POST | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | FUNC-00131、00132 | unavailable |
| entan.tech.detail | GET | /entan/v1/tech-power/{orgId} | FUNC-00133、00134 | unavailable |
| entan.tech.weights | GET | /entan/v1/eval/weights | FUNC-00135、00136 | unavailable |
| entan.tech.report | GET | /entan/v1/enterprises/{orgId}/report | FUNC-00137、00138 | unavailable |
| entan.tech.rank.m_ent_ds_07_industry_potential_005 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | FUNC-00139、00140 | available |
| （页面清单） | — | — | FUNC-00141、00142 | — |

---

## 功能点 → 用例矩阵（挂 L31.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L31 \| entan.tech.rank \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | FUNC-00131、00132 | 已覆盖 | 合法集合 + 缺 enterprise_codes |
| L31 \| entan.tech.rank \| enterprises \| 算法输出-enterprises企业技术力结果集 | FUNC-00131 | 已覆盖 | 主流程断言 value.enterprises 及元素字段 |
| L31 \| entan.tech.rank \| _empty \| 技术力得分无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L31 \| entan.tech.rank \| _fail \| 技术力得分计算失败 | FUNC-00132 | 部分覆盖 | 仅缺 enterprise_codes 反向 |
| L31 \| entan.tech.detail \| orgId \| 算法输入-orgId企业标识 | FUNC-00133、00134 | 已覆盖 | 合法 + 缺 orgId |
| L31 \| entan.tech.detail \| talent_score \| 算法输出-talent_score人才维度得分 | FUNC-00133 | 已覆盖 | |
| L31 \| entan.tech.detail \| trend \| 算法输出-trend技术力趋势 | FUNC-00133 | 已覆盖 | 同条主流程，含 year、value |
| L31 \| entan.tech.detail \| _empty \| 技术力详情无数据空态 | — | 未覆盖 | |
| L31 \| entan.tech.detail \| _fail \| 技术力详情查询失败 | FUNC-00134 | 部分覆盖 | 仅缺 orgId |
| L31 \| entan.tech.weights \| model \| 算法输入-model模型标识 | FUNC-00135、00136 | 已覆盖 | |
| L31 \| entan.tech.weights \| weight \| 算法输出-weight权重配置 | FUNC-00135 | 已覆盖 | 数组元素含 weight |
| L31 \| entan.tech.weights \| _empty \| 模型权重无数据空态 | — | 未覆盖 | |
| L31 \| entan.tech.weights \| _fail \| 模型权重查询失败 | FUNC-00136 | 部分覆盖 | 仅缺 model |
| L31 \| entan.tech.report \| orgId \| 算法输入-orgId企业标识 | FUNC-00137、00138 | 已覆盖 | |
| L31 \| entan.tech.report \| markdown \| 算法输出-markdown评估报告正文 | FUNC-00137 | 已覆盖 | |
| L31 \| entan.tech.report \| _empty \| 评估报告无数据空态 | — | 未覆盖 | |
| L31 \| entan.tech.report \| _fail \| 评估报告生成失败 | FUNC-00138 | 部分覆盖 | 仅缺 orgId |

---

## B 线独有（L31 未列 endpoint）

| endpoint_id | title | 用例编号 | 标记 |
|-------------|-------|----------|------|
| entan.tech.rank.m_ent_ds_07_industry_potential_005 | 技术影响力评估 | FUNC-00139、00140 | 无对应功能点 |

catalog 有该接口（status=available），L31 未挂 field 行，不按 field 拆用例。

---

## req_only 行（无 endpoint 挂接）

L31.md 中 `etl_clean_standardize`、`five_dimension_indicator_threshold`、`tech_power_model_train_optimize`、`weighted_tech_power_index`、`dimension_tech_power_analysis`、`strength_weakness_analysis`、`improvement_suggestion_generate`、`dynamic_tech_power_refresh`、`benchmark_assessment_semantics`、`enterprise_id_name_query_scope`、`viz_report_data_export` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。
