# 服务机构培育推荐 · 功能点覆盖（svc.cultivate / L50）

> catalog `svc.cultivate` · 50897 · path `/industry-service/cultivate`  
> 用例 `API-服务机构培育推荐-用例.md`  
> A 线范围：**L50**（`fp-split-by-api-run/work/L50.md`）  
> 功能点键：`L50 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.cultivate.models | GET | /entan/v1/svc/models | API-000634～API-000638 | catalog `status=unavailable`；本页验收取 `kind=cultivate` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L50 \| svc.cultivate.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000634、API-000636、API-000637 | 已覆盖 | SVCCULTIVATE-01 cultivate 主路径；非法 kind 见 02/636；非本页 gap 见 03/637 |
| L50 \| svc.cultivate.models \| cultivate \| 算法输出-cultivate培育推荐结果体 | catalog cultivate | API-000638 | 契约占位 | unavailable，禁止 sample 培育指数/优先级作通过条件 |
| L50 \| svc.cultivate.models \| _empty \| 培育推荐无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=cultivate 必空」试调证据 |
| L50 \| svc.cultivate.models \| _fail \| 培育推荐查询失败 | 契约错误态 | API-000634、API-000635、API-000636、API-000637 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L50 \| \| etl_clean_standardize \| 多源机构数据清洗标准化 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L50 \| \| cultivate_four_dim_indicators_weight \| 四维指标权重阈值体系 | 需规指标体系权重阈值 | — | 未覆盖 | req_only |
| L50 \| \| standardize_threshold_eval \| 维度指标标准化与阈值判定 | 需规标准化阈值 | — | 未覆盖 | req_only |
| L50 \| \| weighted_cultivate_index_synthesis \| 加权综合培育推荐指数 | 需规加权培育指数 | — | 未覆盖 | req_only |
| L50 \| \| cultivate_rank_list \| 培育推荐排序名单 | 需规推荐排序 | — | 未覆盖 | req_only |
| L50 \| \| single_dimension_scores \| 单维度评分输出 | 需规单维评分 | — | 未覆盖 | req_only |
| L50 \| \| recommend_explanation_cultivate_advice \| 推荐说明与培育建议 | 需规说明与建议 | — | 未覆盖 | req_only |
| L50 \| \| region_type_field_time_source_scope \| 地域机构类型产业筛选语义 | 需规（3）调用与筛选 | — | 未覆盖 | req_only |
| L50 \| \| realtime_monitor_result_refresh \| 实时监控与结果更新 | 需规（3）实时更新 | — | 未覆盖 | req_only |
| L50 \| \| index_rank_dimension_advice_outputs \| 指数排序维分建议五类输出 | 需规（2）五类输出 | — | 未覆盖 | req_only |
| L50 \| \| api_sdk_institution_policy_investment_integration \| API SDK 与机构政策投融资对接 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`cultivate`） |
| 未覆盖 | 12（含 `_empty` 1 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000634～API-000638 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
