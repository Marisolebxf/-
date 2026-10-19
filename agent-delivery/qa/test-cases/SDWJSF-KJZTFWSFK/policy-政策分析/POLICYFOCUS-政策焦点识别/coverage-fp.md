# 政策焦点识别 · 功能点覆盖（policy.focus / L35）

> catalog `policy.focus` · path `#/policy/focus`  
> A 线真源：`fp-split-by-api-run/work/L35.md`  
> B 线用例：`API-政策焦点识别-用例.md`（第二轮 **API-01402**～**01408**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.focus.main | GET | /policy/v1/policy/analysis/focus | API-01402～01408 | unavailable |

---

## 功能点 → 用例矩阵（挂 L35.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L35 \| policy.focus.main \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | API-01402、01403、01406 | 已覆盖 | 全参 + 省略 + 非法 policy_id |
| L35 \| policy.focus.main \| region_code \| 算法输入-region_code区域编码 | catalog region_code | API-01402、01404、01407 | 已覆盖 | 全参 + 省略 + 非法 region_code |
| L35 \| policy.focus.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-01402、01405、01408 | 已覆盖 | 全参 limit=20 + 省略 + 非法 limit=-1 |
| L35 \| policy.focus.main \| focus_score \| 算法输出-focus_score焦点指数 | catalog focus_score | API-01402 | 已覆盖 | 主流程逐字段断言 focus_score（number）；备选 01403～01405 同结构 |
| L35 \| policy.focus.main \| _empty \| 焦点识别无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L35 \| policy.focus.main \| _fail \| 焦点识别查询失败 | 契约错误态 | API-01406、01407、01408 | 已覆盖 | 三参数各 1 条非法反向，预期 message 或 msg |

---

## req_only 行（无 endpoint 挂接）

L35.md 中 `etl_clean_standardize`、`multidim_indicator_expert_threshold`、`indicator_weight_trend_eval`、`focus_bottleneck_extract`、`focus_bottleneck_suggestion_outputs`、`associated_analysis_report`、`dynamic_source_threshold_refresh`、`policy_tag_online_retrieval`、`dimension_time_datasource_scope`、`api_sdk_policy_system_monitor` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 另有 `relation_degree`、`opportunity_cnt`、`ext.title`，已写入正向预期；A 线未单列这些 field_key。
