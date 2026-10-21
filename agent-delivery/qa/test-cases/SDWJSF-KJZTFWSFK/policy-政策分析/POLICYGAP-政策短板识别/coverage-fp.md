# 政策短板识别 · 功能点覆盖（policy.gap / L38）

> catalog `policy.gap` · path `#/policy/gap`  
> A 线真源：`fp-split-by-api-run/work/L38.md`  
> B 线用例：`FUNC-政策短板识别-用例.md`（第三轮 **FUNC-00639**～**FUNC-00645**）  
> 联调台 https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.gap.shortboard | GET | /policy/v1/policy/analysis/gap | FUNC-00639～00643 | unavailable |

---

## 功能点 → 用例矩阵（挂 L38.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L38 \| policy.gap.shortboard \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | FUNC-00639、00640、00642 | 已覆盖 | 主路径不传 + 补传 440000 + 非法 scope_code |
| L38 \| policy.gap.shortboard \| limit \| 算法输入-limit结果条数上限 | catalog limit | FUNC-00639、00641、00643 | 已覆盖 | 主路径 limit=20 + 省略 + 非法 limit=-1 |
| L38 \| policy.gap.shortboard \| shortboard_cnt \| 算法输出-shortboard_cnt短板数 | catalog shortboard_cnt | FUNC-00639 | 已覆盖 | 主流程逐字段断言 shortboard_cnt（number）；备选 00640、00641 同结构 |
| L38 \| policy.gap.shortboard \| _empty \| 短板分析无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L38 \| policy.gap.shortboard \| _fail \| 短板分析查询失败 | 契约错误态 | FUNC-00642、00643 | 已覆盖 | 两参数各 1 条非法反向，预期 message 或 msg |
| （页面清单） \| policy.gap \| 接口信息 / 算法测试 | catalog 页签 | FUNC-00644、00645 | 已覆盖 | 单接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L38.md 中 `etl_clean_standardize`、`coverage_exec_goal_compliance_dims`、`indicator_weight_eval`、`below_threshold_shortboard_id`、`shortboard_list_structured`、`cause_analysis_association`、`improvement_strategy_suggest`、`policy_tag_time_dimension_scope`、`monitoring_trend_push`、`api_sdk_platform_gap` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 另有 `scope_name`，已写入正向预期；A 线未单列该 field_key。

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（短板分析） |
| FUNC 用例数 | 7 |
| 主流程 | 1（FUNC-00639） |
| 备选-参数组合 | 2（FUNC-00640、00641） |
| 反向 | 2（FUNC-00642、00643） |
| 清单 | 2（FUNC-00644、00645） |
| 编号 | FUNC-00639～00645 |
| 旧 API 册 | API-01431～01435 作废，见 FUNC 册 §4 |
