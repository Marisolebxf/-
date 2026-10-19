# 政策力度评估 · 功能点覆盖（policy.intensity / L36）

> catalog `policy.intensity` · path `#/policy/intensity`  
> A 线真源：`fp-split-by-api-run/work/L36.md`  
> B 线用例：`API-政策力度评估-用例.md`（第二轮 **API-01419**～**01425**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.intensity.main | GET | /policy/v1/policy/analysis/intensity | API-01419～01425 | unavailable |

---

## 功能点 → 用例矩阵（挂 L36.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L36 \| policy.intensity.main \| scope_type \| 算法输入-scope_type范围类型 | catalog scope_type | API-01419、01420、01423 | 已覆盖 | sample 传 province + 省略 + 非法 scope_type |
| L36 \| policy.intensity.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-01419、01421、01424 | 已覆盖 | sample 不传 + 传入 440000 + 非法 scope_code |
| L36 \| policy.intensity.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-01419、01422、01425 | 已覆盖 | sample limit=20 + 省略 + 非法 limit=-1 |
| L36 \| policy.intensity.main \| intensity_index \| 算法输出-intensity_index政策力度指数 | catalog intensity_index | API-01419 | 已覆盖 | 主流程逐字段断言 intensity_index（number）；备选 01420～01422 同结构 |
| L36 \| policy.intensity.main \| _empty \| 力度评估无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L36 \| policy.intensity.main \| _fail \| 力度评估查询失败 | 契约错误态 | API-01423、01424、01425 | 已覆盖 | 三参数各 1 条非法反向，预期 message 或 msg |

---

## req_only 行（无 endpoint 挂接）

L36.md 中 `etl_clean_standardize`、`effect_coverage_cost_dimensions`、`weighted_intensity_compute`、`threshold_grade_classify`、`horizontal_vertical_track`、`dimension_analysis_report`、`intensity_ranking_semantic`、`trend_predict_outputs`、`policy_category_time_scope`、`api_sdk_embed_export` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 另有 `rank_no`、`scope_type`、`scope_code`、`scope_name`、`industry_coverage`，已写入正向预期；A 线未单列这些 field_key。
