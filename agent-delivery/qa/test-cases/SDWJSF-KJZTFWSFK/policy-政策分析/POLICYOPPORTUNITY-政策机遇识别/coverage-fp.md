# 政策机遇识别 · 功能点覆盖（policy.opportunity / L39）

> catalog `policy.opportunity` · 50897 · path `/policy/opportunity`  
> 用例 `API-政策机遇识别-用例.md`  
> A 线范围：**L39**（`fp-split-by-api-run/work/L39.md`）  
> 功能点键：`L39 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.gap.opportunity | GET | /policy/v1/policy/analysis/opportunity | API-000474～API-000478 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L39 \| policy.gap.opportunity \| region_code \| 算法输入-region_code区域编码 | catalog region_code | API-000474、API-000476 | 已覆盖 | 主路径 440300 + 非法 region |
| L39 \| policy.gap.opportunity \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000474、API-000477 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L39 \| policy.gap.opportunity \| opportunity_cnt \| 算法输出-opportunity_cnt政策机遇数量 | catalog opportunity_cnt | API-000474、API-000478 | 契约占位 | unavailable，禁止 sample 机遇数作通过条件 |
| L39 \| policy.gap.opportunity \| _empty \| 机遇分析无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L39 \| policy.gap.opportunity \| _fail \| 机遇分析查询失败 | 契约错误态 | API-000474、API-000475、API-000476、API-000477 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L39 \| \| etl_clean_standardize \| 多源政策文本解读数据预处理 | 需规（1） | — | 未覆盖 | req_only |
| L39 \| \| attention_influence_stability_dimensions \| 关注度影响力稳定性三维指标体系 | 需规三维指标 | — | 未覆盖 | req_only |
| L39 \| \| indicator_weight_opportunity_eval \| 指标数值计算与权重评估 | 需规指标权重 | — | 未覆盖 | req_only |
| L39 \| \| opportunity_list_semantic \| 政策机遇清单语义 | 需规（2）机遇清单 | — | 未覆盖 | req_only |
| L39 \| \| trend_analysis_report \| 政策机遇趋势分析报告语义 | 需规（2）趋势报告 | — | 未覆盖 | req_only |
| L39 \| \| visualization_outputs \| 可视化结果与图表数据语义 | 需规（2）可视化 | — | 未覆盖 | req_only |
| L39 \| \| strategy_advice_outputs \| 策略建议输出语义 | 需规（2）策略建议 | — | 未覆盖 | req_only |
| L39 \| \| policy_tag_time_dimension_scope \| 政策标签时间区间与分析维度查询 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L39 \| \| realtime_opportunity_refresh \| 实时监测与机遇结果刷新 | 需规实时监测 | — | 未覆盖 | req_only |
| L39 \| \| auto_push_platform_integration \| 自动推送与平台集成语义 | 需规（3）平台推送 | — | 未覆盖 | req_only |
| L39 \| \| api_sdk_standard_invoke \| API SDK 标准化调用 | 需规（3）API/SDK | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`region_code`、`limit`、`_fail`） |
| 契约占位 | 1（`opportunity_cnt`） |
| 未覆盖 | 12（含 `_empty` 1 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000474～API-000478 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
