# 人力资源服务机构技术力评估 · 功能点覆盖（svc.tech-hr / L45）

> catalog `svc.tech-hr` · path `#/industry-service/tech-hr`  
> A 线真源：`fp-split-by-api-run/work/L45.md`（只读，未改 work）  
> B 线用例：`API-人力资源服务机构技术力评估-用例.md`（第二轮 **API-01680**～**01685**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-hr.models | GET | /entan/v1/svc/models | API-01680～01682 | unavailable |
| svc.tech-hr.m_svc_deep_176_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute | API-01683～01685 | available |

---

## 功能点 → 用例矩阵（挂 L45.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L45 \| svc.tech-hr.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01680、01681、01682 | 已覆盖 | 主路径 kind=tech + 省略可选 kind + 非法 kind=__invalid__ |
| L45 \| svc.tech-hr.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-01680、01681 | 已覆盖 | 主流程逐字段断言 tech 及 sampleResponse 元素字段；备选 01681 同结构 |
| L45 \| svc.tech-hr.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 tech 名单，无稳定空结果构造条件，不单开空态用例 |
| L45 \| svc.tech-hr.models \| _fail \| 技术力评价查询失败 | 契约错误态 | API-01682 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L45.md 中 `etl_clean_standardize`、`core_indicator_threshold_weight`、`feature_metric_compute`、`ml_aggregate_tech_index`、`horizontal_rank_compare`、`subscore_threshold_outputs`、`trend_analysis_report`、`dynamic_monitor_weight_refresh`、`org_time_dimension_scope`、`auto_eval_continuous_monitor`、`api_sdk_viz_platform` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 的 tech 元素另有 `org_id`、`service_type`、`score`、`ext.name`、`ext.rank_no`、`dimension_scores`（patents、rdInvestment、experts、cases、standards），已写入 01680 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-hr.m_svc_deep_176_1 | API-01683～01685 | 无对应功能点 | L45 未列该 compute endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`tech`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| 无对应功能点 | 11（req_only）+ 1（compute endpoint） |
