# 市场营销服务机构技术力评估 · 功能点覆盖（svc.tech-mkt / L46）

> catalog `svc.tech-mkt` · path `#/industry-service/tech-mkt`  
> A 线真源：`fp-split-by-api-run/work/L46.md`（只读，未改 work）  
> B 线用例：`FUNC-市场营销服务机构技术力评估-用例.md`（第三轮 **FUNC-00908**～**FUNC-00915**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-mkt.models | GET | /entan/v1/svc/models | FUNC-00908～00910 | unavailable |
| svc.tech-mkt.m_svc_deep_177_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute | FUNC-00911～00913 | available |
| （页面清单） | — | — | FUNC-00914、00915 | — |

---

## 功能点 → 用例矩阵（挂 L46.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L46 \| svc.tech-mkt.models \| kind \| 算法输入-kind模型类型 | catalog kind | FUNC-00908、00909、00910 | 已覆盖 | 主路径 kind=tech + 省略可选 kind + 非法 kind=__invalid__ |
| L46 \| svc.tech-mkt.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | FUNC-00908、00909 | 已覆盖 | 主流程逐字段断言 tech 及 sampleResponse 元素字段；备选 00909 同结构 |
| L46 \| svc.tech-mkt.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 tech 名单，无稳定空结果构造条件，不单开空态用例 |
| L46 \| svc.tech-mkt.models \| _fail \| 技术力评价查询失败 | 契约错误态 | FUNC-00910 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L46.md 中 `etl_clean_standardize`、`core_indicator_threshold_weight`、`feature_metric_compute`、`weighted_aggregate_tech_index`、`horizontal_rank_compare`、`subscore_weight_level_outputs`、`trend_analysis_report`、`dynamic_monitor_weight_refresh`、`org_industry_region_scope`、`batch_auto_report`、`api_sdk_embed` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 的 tech 元素另有 `org_id`、`service_type`、`score`、`ext.name`、`ext.rank_no`、`dimension_scores`（patents、rdInvestment、experts、cases、standards），已写入 00908 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-mkt.m_svc_deep_177_1 | FUNC-00911～00913 | 无对应功能点 | L46 未列该 compute endpoint 的 field_key；用例仍按 catalog 编写 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`tech`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| 无对应功能点 | 11（req_only）+ 1（compute endpoint） |
