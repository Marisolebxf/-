# 服务机构引入推荐 · 功能点覆盖（svc.attract / L49）

> catalog `svc.attract` · path `#/industry-service/attract`  
> A 线真源：`fp-split-by-api-run/work/L49.md`（只读，未改）  
> B 线用例：`API-服务机构引入推荐-用例.md`（第二轮 **API-01704**～**01709**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.attract.models | GET | /entan/v1/svc/models | API-01704～01706 | unavailable |
| svc.attract.m_svc_deep_180_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute | API-01707～01709 | available |

---

## 功能点 → 用例矩阵（挂 L49.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L49 \| svc.attract.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01704、01705、01706 | 已覆盖 | 主路径 kind=attract + 省略可选 kind + 非法 kind=__invalid__ |
| L49 \| svc.attract.models \| attract \| 算法输出-attract引入推荐结果体 | catalog attract | API-01704 | 已覆盖 | 主流程逐字段断言 attract 及 sampleResponse 元素字段；备选 01705 同结构 |
| L49 \| svc.attract.models \| _empty \| 引入推荐无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L49 \| svc.attract.models \| _fail \| 引入推荐查询失败 | 契约错误态 | API-01706 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L49.md 中 `etl_clean_standardize`、`attract_four_dim_indicators_weight`、`standardize_threshold_eval`、`weighted_recommend_index_synthesis`、`priority_rank_list`、`dimension_analysis_report`、`peer_org_compare`、`analysis_dimension_time_tag_scope`、`realtime_monitor_result_refresh`、`index_rank_report_compare_outputs`、`api_sdk_investment_db_integration` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 的 attract 元素另有 `org_id`、`attraction_index`、`priority_level`、`rank_no`、`recommend_reason`、`ext.name`、`dimension_scores.industryFit`、`techLead`、`potential`、`willingness`，已写入 01704 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.attract.m_svc_deep_180_1 | API-01707～01709 | 无对应功能点 | L49 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`attract`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`svc.attract.m_svc_deep_180_1`，3 条用例） |
