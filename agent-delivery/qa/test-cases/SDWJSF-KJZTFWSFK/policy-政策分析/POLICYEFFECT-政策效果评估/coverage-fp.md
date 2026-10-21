# 政策效果评估 · 功能点覆盖（policy.effect / L37）

> catalog `policy.effect` · path `#/policy/effect`  
> A 线真源：`fp-split-by-api-run/work/L37.md`  
> B 线用例：`FUNC-政策效果评估-用例.md`（第三轮 **FUNC-00632**～**FUNC-00638**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.effect.main | GET | /policy/v1/policy/analysis/effect | FUNC-00632～00636 | unavailable |

---

## 功能点 → 用例矩阵（挂 L37.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L37 \| policy.effect.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | FUNC-00632、00633、00635 | 已覆盖 | 主流程不传；EFF-02 补传 440000；EFF-04 非法 |
| L37 \| policy.effect.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | FUNC-00632、00634、00636 | 已覆盖 | sampleRequest limit=20；EFF-03 省略；EFF-05 非法 -1 |
| L37 \| policy.effect.main \| effect_score \| 算法输出-effect_score政策效果评估指数 | catalog effect_score | FUNC-00632 | 已覆盖 | 主流程逐字段断言 effect_score（number）；备选 00633～00634 同结构；含 sampleResponse 的 scope_name、scope_code、impl_effect |
| L37 \| policy.effect.main \| _empty \| 效果评估无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「合法入参必空」条件，不单开空态用例 |
| L37 \| policy.effect.main \| _fail \| 效果评估查询失败 | 契约错误态 | FUNC-00635、00636 | 已覆盖 | 两参数各 1 条非法反向，预期 message 或 msg |
| （页面清单） \| policy.effect \| 接口信息 / 算法测试 | catalog 页签 | FUNC-00637、00638 | 已覆盖 | 单接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L37.md 中 `etl_clean_standardize`、`exec_socio_env_dimensions`、`indicator_weight_compose`、`weighted_effect_compute`、`dimension_evaluation_results`、`improvement_performance_report`、`policy_tag_time_stage_scope`、`realtime_history_tracking`、`api_sdk_platform_auto_eval` 共 9 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 另有 `scope_name`、`scope_code`、`impl_effect`，已写入正向预期；A 线未单列这些 field_key。

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（效果评估） |
| FUNC 用例数 | 7 |
| 主流程 | 1（FUNC-00632） |
| 备选-参数组合 | 2（FUNC-00633、00634） |
| 反向 | 2（FUNC-00635、00636） |
| 清单 | 2（FUNC-00637、00638） |
| 编号 | FUNC-00632～00638 |
| 旧 API 册 | API-01426～01430 作废，见 FUNC 册 §4 |

L37 挂接 endpoint 行 5 + req_only 9；B 线不按 field 拆行。`code-registry` 由父控回写。
