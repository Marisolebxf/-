# 服务链短板分析 · 功能点覆盖（svc.gap / L41）

> catalog `svc.gap` · path `#/industry-service/gap`  
> A 线真源：`fp-split-by-api-run/work/L41.md`  
> B 线用例：`API-服务链短板分析-用例.md`（第二轮 **API-01647**～**01655**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.gap.models | GET | /entan/v1/svc/models | API-01647～01649 | unavailable |
| svc.gap.m_svc_org_coverage_depth | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | API-01650～01652 | available |
| svc.gap.m_svc_deep_172_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | API-01653～01655 | available |

---

## 功能点 → 用例矩阵（挂 L41.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L41 \| svc.gap.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-01647、01648、01649 | 已覆盖 | 主路径 kind=gap + 省略可选 kind + 非法 kind=__invalid__ |
| L41 \| svc.gap.models \| gap \| 算法输出-gap短板分析结果体 | catalog gap | API-01647 | 已覆盖 | 主流程逐字段断言 gap 及 sampleResponse 元素字段；备选 01648 同结构 |
| L41 \| svc.gap.models \| _empty \| 短板分析无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L41 \| svc.gap.models \| _fail \| 短板分析查询失败 | 契约错误态 | API-01649 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg；省略 kind 按可选参数记备选 |

---

## req_only 行（无 endpoint 挂接）

L41.md 中 `etl_clean_standardize`、`quality_efficiency_type_indicators`、`indicator_weak_link_locate`、`cause_resource_process_match`、`gap_optimization_advice`、`dynamic_monitor_threshold_refresh`、`org_tag_dimension_time_scope`、`auto_monitor_trend_alert`、`locate_cause_advice_outputs`、`api_sdk_ops_platform` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 的 gap 元素另有 `stage_name`、`stage_code`、`org_count_in_stage`、`avg_depth`、`runtime_flag`、`q061_score`，已写入 01647 正向预期；A 线未单列这些 field_key。

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.gap.m_svc_org_coverage_depth | API-01650～01652 | 无对应功能点 | L41 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |
| svc.gap.m_svc_deep_172_1 | API-01653～01655 | 无对应功能点 | L41 未列该 endpoint 的 field_key；用例仍按 catalog 编写 |
