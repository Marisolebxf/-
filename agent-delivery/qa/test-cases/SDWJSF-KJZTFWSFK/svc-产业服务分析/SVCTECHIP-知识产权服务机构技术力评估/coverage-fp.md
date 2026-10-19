# 知识产权服务机构技术力评估 · 功能点覆盖（svc.tech-ip / L44）

> catalog `svc.tech-ip` · path `#/industry-service/tech-ip`  
> A 线真源：`fp-split-by-api-run/work/L44.md`  
> B 线用例：`API-知识产权服务机构技术力评估-用例.md`（第二轮 **API-01674**～**01679**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-ip.models | GET | /entan/v1/svc/models | API-01674～01676 | unavailable |
| svc.tech-ip.m_svc_deep_175_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute | API-01677～01679 | available |

---

## 功能点 → 用例矩阵（挂 L44.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L44 \| svc.tech-ip.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01674、01675、01676 | 已覆盖 | 主路径 kind=tech + 省略 kind + 非法 kind=__invalid__ |
| L44 \| svc.tech-ip.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-01674、01675 | 已覆盖 | 主流程逐字段断言 tech 及 sampleResponse 元素字段；备选 01675 同结构 |
| L44 \| svc.tech-ip.models \| _empty \| 技术力评估无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 tech，无稳定空结果构造条件，不单开空态用例 |
| L44 \| svc.tech-ip.models \| _fail \| 技术力评估查询失败 | 契约错误态 | API-01676 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法 |

---

## req_only 行（无 endpoint 挂接）

L44.md 中 `etl_clean_standardize`、`ip_four_dim_indicators_threshold`、`dimension_item_score_calc`、`weighted_tech_index_synthesis`、`horizontal_org_compare`、`vertical_dynamic_track`、`org_name_query_semantic`、`time_dimension_weight_custom`、`score_report_advice_outputs`、`periodic_schedule_monitor_refresh`、`api_sdk_batch_platform_integration` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 的 tech 元素另有 `org_id`、`service_type`、`score`、`ext.name`、`ext.rank_no`、`dimension_scores`（patents、rdInvestment、experts、cases、standards），已写入 01674 正向预期；A 线只列顶层 field_key `tech`，不按子成员拆行。

---

## B 线独有（A 线未列 endpoint）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-ip.m_svc_deep_175_1 | API-01677、01678、01679 | 无对应功能点 | L44 未列该 compute endpoint；用例仍按 catalog 编写 |
