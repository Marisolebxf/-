# 科技创新服务机构技术力评估 · 功能点覆盖（svc.tech-innov / L48）

> catalog `svc.tech-innov` · path `#/industry-service/tech-innov`  
> A 线真源：`fp-split-by-api-run/work/L48.md`（只读，未改）  
> B 线用例：`API-科技创新服务机构技术力评估-用例.md`（第二轮 **API-01698**～**01703**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-innov.models | GET | /entan/v1/svc/models | API-01698～01700 | unavailable |
| svc.tech-innov.m_svc_deep_179_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_179_1/compute | API-01701～01703 | available |

---

## 功能点 → 用例矩阵（挂 L48.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L48 \| svc.tech-innov.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01698、01699、01700 | 已覆盖 | 主路径 kind=tech + 省略可选 kind + 非法 kind=__invalid__ |
| L48 \| svc.tech-innov.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-01698 | 已覆盖 | 主流程逐字段断言 tech 及 sampleResponse 元素字段；备选 01699 同结构 |
| L48 \| svc.tech-innov.models \| _empty \| 技术力评估无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L48 \| svc.tech-innov.models \| _fail \| 技术力评估查询失败 | 契约错误态 | API-01700 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L48.md 中 `etl_clean_standardize`、`innov_four_dim_threshold_weight`、`dimension_standard_score_calc`、`weighted_index_rank_synthesis`、`subscore_weight_ratio_outputs`、`trend_analysis_advice`、`dynamic_monitor_param_refresh`、`eval_period_source_dimension`、`org_tag_online_search`、`auto_eval_system_integration`、`api_sdk_standard_call` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 的 tech 元素另有 `org_id`、`service_type`、`score`、`ext.name`、`ext.rank_no`、`dimension_scores.patents`、`rdInvestment`、`experts`、`cases`、`standards`，已写入 01698 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-innov.m_svc_deep_179_1 | API-01701～01703 | 无对应功能点 | L48 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`tech`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`svc.tech-innov.m_svc_deep_179_1`，3 条用例） |
