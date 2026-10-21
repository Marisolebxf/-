# 服务机构培育推荐 · 功能点覆盖（svc.cultivate / L50）

> catalog `svc.cultivate` · path `#/industry-service/cultivate`  
> A 线真源：`fp-split-by-api-run/work/L50.md`（只读，未改）  
> B 线用例：`FUNC-服务机构培育推荐-用例.md`（第三轮 **FUNC-00940**～**FUNC-00947**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.cultivate.models | GET | /entan/v1/svc/models | FUNC-00940～00942 | unavailable |
| svc.cultivate.m_svc_deep_181_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | FUNC-00943～00945 | available |

---

## 功能点 → 用例矩阵（挂 L50.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L50 \| svc.cultivate.models \| kind \| 算法输入-kind模型类型 | catalog kind | FUNC-00940、00941、00942 | 已覆盖 | 主路径 kind=cultivate + 省略可选 kind + 非法 kind=__invalid__ |
| L50 \| svc.cultivate.models \| cultivate \| 算法输出-cultivate培育推荐结果体 | catalog cultivate | FUNC-00940、00941 | 已覆盖 | 主流程逐字段断言 cultivate 及 sampleResponse 元素字段；备选 00941 同结构 |
| L50 \| svc.cultivate.models \| _empty \| 培育推荐无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L50 \| svc.cultivate.models \| _fail \| 培育推荐查询失败 | 契约错误态 | FUNC-00942 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L50.md 中 `etl_clean_standardize`、`cultivate_four_dim_indicators_weight`、`standardize_threshold_eval`、`weighted_cultivate_index_synthesis`、`cultivate_rank_list`、`single_dimension_scores`、`recommend_explanation_cultivate_advice`、`region_type_field_time_source_scope`、`realtime_monitor_result_refresh`、`index_rank_dimension_advice_outputs`、`api_sdk_institution_policy_investment_integration` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 的 cultivate 元素另有 `org_id`、`cultivation_index`、`priority_level`、`growth_stage`、`advice`、`ext.name`、`dimension_scores`（scale、innovation、effect、marketGap），已写入 00940 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.cultivate.m_svc_deep_181_1 | FUNC-00943～00945 | 无对应功能点 | L50 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 页面清单（联调台 tab）

| 场景 | 对应用例编号 | 状态 |
|------|--------------|------|
| 接口信息-清单 | FUNC-00946 | 已覆盖 |
| 算法测试-清单 | FUNC-00947 | 已覆盖 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`cultivate`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`svc.cultivate.m_svc_deep_181_1`，3 条用例） |
| 页面清单 | 2（00946、00947） |
