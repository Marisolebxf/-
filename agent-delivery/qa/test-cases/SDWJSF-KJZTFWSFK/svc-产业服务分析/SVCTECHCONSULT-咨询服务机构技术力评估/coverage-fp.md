# 咨询服务机构技术力评估 · 功能点覆盖（svc.tech-consult / L47）

> catalog `svc.tech-consult` · path `#/industry-service/tech-consult`  
> A 线真源：`fp-split-by-api-run/work/L47.md`（只读，未改）  
> B 线用例：`FUNC-咨询服务机构技术力评估-用例.md`（第三轮 **FUNC-00916**～**FUNC-00923**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-consult.models | GET | /entan/v1/svc/models | FUNC-00916～00918 | unavailable |
| svc.tech-consult.m_svc_deep_178_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute | FUNC-00919～00921 | available |

---

## 功能点 → 用例矩阵（挂 L47.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L47 \| svc.tech-consult.models \| kind \| 算法输入-kind模型类型 | catalog kind | FUNC-00916、00917、00918 | 已覆盖 | 主路径 kind=tech + 省略可选 kind + 非法 kind=__invalid__ |
| L47 \| svc.tech-consult.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | FUNC-00916、00917 | 已覆盖 | 主流程逐字段断言 tech 及 sampleResponse 元素字段；备选 00917 同结构 |
| L47 \| svc.tech-consult.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L47 \| svc.tech-consult.models \| _fail \| 技术力评价查询失败 | 契约错误态 | FUNC-00918 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L47.md 中 `etl_clean_standardize`、`consult_four_dim_threshold_weight`、`dimension_metric_compute`、`weighted_tech_index_synthesis`、`strength_weakness_gap_list`、`improvement_direction_suggestions`、`trend_analysis_report`、`org_name_industry_time_scope`、`batch_auto_eval_viz`、`bundled_outputs_in_tech`、`api_sdk_decision_platform` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 的 tech 元素另有 `org_id`、`service_type`、`score`、`ext.name`、`ext.rank_no`、`dimension_scores.patents`、`rdInvestment`、`experts`、`cases`、`standards`，已写入 00916 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-consult.m_svc_deep_178_1 | FUNC-00919～00921 | 无对应功能点 | L47 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 页面清单（联调台 tab）

| 场景 | 对应用例编号 | 状态 |
|------|--------------|------|
| 接口信息-清单 | FUNC-00922 | 已覆盖 |
| 算法测试-清单 | FUNC-00923 | 已覆盖 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`tech`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`svc.tech-consult.m_svc_deep_178_1`，3 条用例） |
| 页面清单 | 2（00922、00923） |
