# 服务机构引入推荐 · 功能点覆盖（svc.attract / L49）

> catalog `svc.attract` · 50897 · path `/industry-service/attract`  
> 用例 `API-服务机构引入推荐-用例.md`  
> A 线范围：**L49**（`fp-split-by-api-run/work/L49.md`）  
> 功能点键：`L49 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.attract.models | GET | /entan/v1/svc/models | API-000629～API-000633 | catalog `status=unavailable`；本页验收取 `kind=attract` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L49 \| svc.attract.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000629、API-000631、API-000632 | 已覆盖 | SVCATTRACT-01 attract 主路径；非法 kind 见 02/631；非本页 gap 见 03/632 |
| L49 \| svc.attract.models \| attract \| 算法输出-attract引入推荐结果体 | catalog attract | API-000633 | 契约占位 | unavailable，禁止 sample 推荐指数/排序作通过条件 |
| L49 \| svc.attract.models \| _empty \| 引入推荐无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=attract 必空」试调证据 |
| L49 \| svc.attract.models \| _fail \| 引入推荐查询失败 | 契约错误态 | API-000629、API-000630、API-000631、API-000632 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L49 \| \| etl_clean_standardize \| 多源机构数据清洗标准化 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L49 \| \| attract_four_dim_indicators_weight \| 四维指标权重阈值体系 | 需规指标体系权重阈值 | — | 未覆盖 | req_only |
| L49 \| \| standardize_threshold_eval \| 维度指标标准化与阈值判定 | 需规标准化阈值 | — | 未覆盖 | req_only |
| L49 \| \| weighted_recommend_index_synthesis \| 加权综合推荐指数 | 需规加权推荐指数 | — | 未覆盖 | req_only |
| L49 \| \| priority_rank_list \| 推荐优先级排序名单 | 需规优先级排序 | — | 未覆盖 | req_only |
| L49 \| \| dimension_analysis_report \| 各维度指标分析报告 | 需规维度分析报告 | — | 未覆盖 | req_only |
| L49 \| \| peer_org_compare \| 同类机构对比分析 | 需规同类对比 | — | 未覆盖 | req_only |
| L49 \| \| analysis_dimension_time_tag_scope \| 分析维度时间标签筛选语义 | 需规（3）调用与检索 | — | 未覆盖 | req_only |
| L49 \| \| realtime_monitor_result_refresh \| 实时监控与结果更新 | 需规（3）实时更新 | — | 未覆盖 | req_only |
| L49 \| \| index_rank_report_compare_outputs \| 指数排序报告对比四类输出 | 需规（2）四类输出 | — | 未覆盖 | req_only |
| L49 \| \| api_sdk_investment_db_integration \| API SDK 与招商产业平台对接 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`attract`） |
| 未覆盖 | 12（含 `_empty` 1 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000629～API-000633 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
