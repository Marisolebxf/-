# 政策机遇识别 · 功能点覆盖（policy.opportunity / L39）

> catalog `policy.opportunity` · path `#/policy/opportunity`  
> A 线真源：`fp-split-by-api-run/work/L39.md`  
> B 线用例：`API-政策机遇识别-用例.md`（第二轮 **API-01436**～**01440**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.gap.opportunity | GET | /policy/v1/policy/analysis/opportunity | API-01436～01440 | unavailable |

---

## 功能点 → 用例矩阵（挂 L39.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L39 \| policy.gap.opportunity \| region_code \| 算法输入-region_code区域编码 | catalog region_code | API-01438、01439 | 已覆盖 | 01438 补传 440300；01439 非法 region_code。主流程按 sampleRequest 不传 |
| L39 \| policy.gap.opportunity \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-01436、01437、01440 | 已覆盖 | 主流程 limit=20 + 省略 + 非法 limit=-1 |
| L39 \| policy.gap.opportunity \| opportunity_cnt \| 算法输出-opportunity_cnt政策机遇数量 | catalog opportunity_cnt | API-01436 | 已覆盖 | 主流程逐字段断言 opportunity_cnt（number）；备选 01437、01438 同结构。文档标记未交付 |
| L39 \| policy.gap.opportunity \| _empty \| 机遇分析无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L39 \| policy.gap.opportunity \| _fail \| 机遇分析查询失败 | 契约错误态 | API-01439、01440 | 已覆盖 | 两参数各 1 条非法反向，预期 message 或 msg |

---

## req_only 行（无 endpoint 挂接）

L39.md 中 `etl_clean_standardize`、`attention_influence_stability_dimensions`、`indicator_weight_opportunity_eval`、`opportunity_list_semantic`、`trend_analysis_report`、`visualization_outputs`、`strategy_advice_outputs`、`policy_tag_time_dimension_scope`、`realtime_opportunity_refresh`、`auto_push_platform_integration`、`api_sdk_standard_invoke` 共 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 另有 `region_code`、`relation_degree`，已写入正向预期；A 线未把 `relation_degree` 单列 field_key。
