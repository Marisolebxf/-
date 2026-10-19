# 服务机构培育推荐 · 功能点覆盖（svc.cultivate / L50）

> catalog `svc.cultivate` · path `#/industry-service/cultivate`  
> A 线真源：`fp-split-by-api-run/work/L50.md`（只读，未改 work）  
> B 线用例：`API-服务机构培育推荐-用例.md`（第二轮 **API-01710**～**01715**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.cultivate.models | GET | /entan/v1/svc/models | API-01710～01712 | unavailable |
| svc.cultivate.m_svc_deep_181_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | API-01713～01715 | available |

---

## 功能点 → 用例矩阵（挂 L50.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L50 \| svc.cultivate.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01710、01711、01712 | 已覆盖 | 主路径 kind=cultivate + 省略可选 kind + 非法 kind=__invalid__ |
| L50 \| svc.cultivate.models \| cultivate \| 算法输出-cultivate培育推荐结果体 | catalog cultivate | API-01710、01711 | 已覆盖 | 主流程逐字段断言 cultivate 及 sampleResponse 元素字段；备选 01711 同结构 |
| L50 \| svc.cultivate.models \| _empty \| 培育推荐无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 cultivate 名单，无稳定空结果构造条件，不单开空态用例 |
| L50 \| svc.cultivate.models \| _fail \| 培育推荐查询失败 | 契约错误态 | API-01712 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L50.md 中 `etl_clean_standardize`、`cultivate_four_dim_indicators_weight`、`standardize_threshold_eval`、`weighted_cultivate_index_synthesis`、`cultivate_rank_list`、`single_dimension_scores`、`recommend_explanation_cultivate_advice`、`region_type_field_time_source_scope`、`realtime_monitor_result_refresh`、`index_rank_dimension_advice_outputs`、`api_sdk_institution_policy_investment_integration` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L50 \| \| etl_clean_standardize \| 多源机构数据清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L50 \| \| cultivate_four_dim_indicators_weight \| 四维指标权重阈值体系 | 需规指标体系权重阈值 | — | 无对应功能点 | req_only |
| L50 \| \| standardize_threshold_eval \| 维度指标标准化与阈值判定 | 需规标准化阈值 | — | 无对应功能点 | req_only |
| L50 \| \| weighted_cultivate_index_synthesis \| 加权综合培育推荐指数 | 需规加权培育指数 | — | 无对应功能点 | req_only |
| L50 \| \| cultivate_rank_list \| 培育推荐排序名单 | 需规推荐排序 | — | 无对应功能点 | req_only |
| L50 \| \| single_dimension_scores \| 单维度评分输出 | 需规单维评分 | — | 无对应功能点 | req_only |
| L50 \| \| recommend_explanation_cultivate_advice \| 推荐说明与培育建议 | 需规说明与建议 | — | 无对应功能点 | req_only |
| L50 \| \| region_type_field_time_source_scope \| 地域机构类型产业筛选语义 | 需规（3）调用与筛选 | — | 无对应功能点 | req_only |
| L50 \| \| realtime_monitor_result_refresh \| 实时监控与结果更新 | 需规（3）实时更新 | — | 无对应功能点 | req_only |
| L50 \| \| index_rank_dimension_advice_outputs \| 指数排序维分建议五类输出 | 需规（2）五类输出 | — | 无对应功能点 | req_only |
| L50 \| \| api_sdk_institution_policy_investment_integration \| API SDK 与机构政策投融资对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

sampleResponse 的 cultivate 元素另有 `org_id`、`cultivation_index`、`priority_level`、`growth_stage`、`advice`、`ext.name`、`dimension_scores`（scale、innovation、effect、marketGap），已写入 01710 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.cultivate.m_svc_deep_181_1 | API-01713～01715 | 无对应功能点 | L50 未列该 compute endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`cultivate`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| 无对应功能点 | 11（req_only）+ 1（compute endpoint） |
