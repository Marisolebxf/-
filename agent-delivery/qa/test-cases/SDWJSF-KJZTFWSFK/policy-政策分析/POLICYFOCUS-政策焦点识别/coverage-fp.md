# 政策焦点识别 · 功能点覆盖（policy.focus / L35）

> catalog `policy.focus` · path `#/policy/focus`  
> A 线真源：`fp-split-by-api-run/work/L35.md`  
> B 线用例：`FUNC-政策焦点识别-用例.md`（第三轮 **FUNC-00602**～**FUNC-00610**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.focus.main | GET | /policy/v1/policy/analysis/focus | FUNC-00602～00608 | unavailable |

---

## 功能点 → 用例矩阵（挂 L35.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L35 \| policy.focus.main \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | FUNC-00602、00603、00606 | 已覆盖 | 全参 + 省略 + 非法 policy_id |
| L35 \| policy.focus.main \| region_code \| 算法输入-region_code区域编码 | catalog region_code | FUNC-00602、00604、00607 | 已覆盖 | 全参 + 省略 + 非法 region_code |
| L35 \| policy.focus.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | FUNC-00602、00605、00608 | 已覆盖 | 全参 limit=20 + 省略 + 非法 limit=-1 |
| L35 \| policy.focus.main \| focus_score \| 算法输出-focus_score焦点指数 | catalog focus_score | FUNC-00602 | 已覆盖 | 主流程逐字段断言 focus_score（number）；备选 00603～00605 同结构 |
| L35 \| policy.focus.main \| _empty \| 焦点识别无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L35 \| policy.focus.main \| _fail \| 焦点识别查询失败 | 契约错误态 | FUNC-00606、00607、00608 | 已覆盖 | 三参数各 1 条非法反向，预期 message 或 msg |
| （页面清单） \| policy.focus \| 接口信息 / 算法测试 | catalog 页签 | FUNC-00609、00610 | 已覆盖 | 单接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L35.md 中 `etl_clean_standardize`、`multidim_indicator_expert_threshold`、`indicator_weight_trend_eval`、`focus_bottleneck_extract`、`focus_bottleneck_suggestion_outputs`、`associated_analysis_report`、`dynamic_source_threshold_refresh`、`policy_tag_online_retrieval`、`dimension_time_datasource_scope`、`api_sdk_policy_system_monitor` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 另有 `relation_degree`、`opportunity_cnt`、`ext.title`，已写入正向预期；A 线未单列这些 field_key。

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（焦点识别） |
| FUNC 用例数 | 9 |
| 主流程 | 1（FUNC-00602） |
| 备选-参数组合 | 3（FUNC-00603～00605） |
| 反向 | 3（FUNC-00606～00608） |
| 清单 | 2（FUNC-00609、00610） |
| 编号 | FUNC-00602～00610 |
| 旧 API 册 | API-01402～01408 作废，见 FUNC 册 §4 |
