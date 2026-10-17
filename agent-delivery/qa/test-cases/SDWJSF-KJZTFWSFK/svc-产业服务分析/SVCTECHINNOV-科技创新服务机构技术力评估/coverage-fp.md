# 科技创新服务机构技术力评估 · 功能点覆盖（svc.tech-innov / L48）

> catalog `svc.tech-innov` · 50897 · path `/industry-service/tech-innov`  
> 用例 `API-科技创新服务机构技术力评估-用例.md`  
> A 线范围：**L48**（`fp-split-by-api-run/work/L48.md`）  
> 功能点键：`L48 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-innov.models | GET | /entan/v1/svc/models | API-00624～API-00628 | catalog `status=unavailable`；本页验收取 `kind=tech`；展示过滤 `service_type=INNOV` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L48 \| svc.tech-innov.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-00624、API-00626、API-00627 | 已覆盖 | SVCTECHINNOV-01 tech 主路径；非法 kind 见 02/00626；非本页 gap 见 03/00627 |
| L48 \| svc.tech-innov.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-00628 | 契约占位 | unavailable，禁止 sample 指数/排名/维度分作通过条件 |
| L48 \| svc.tech-innov.models \| _empty \| 技术力评估无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 必空」试调证据 |
| L48 \| svc.tech-innov.models \| _fail \| 技术力评估查询失败 | 契约错误态 | API-00624、API-00625、API-00626、API-00627 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind/页语义失败 |
| L48 \| \| etl_clean_standardize \| 多源机构数据清洗标准化 | 需规（1）采集标准化 | — | 未覆盖 | req_only |
| L48 \| \| innov_four_dim_threshold_weight \| 四维指标与阈值权重体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L48 \| \| dimension_standard_score_calc \| 各维度标准化指标得分 | 需规指标计算 | — | 未覆盖 | req_only |
| L48 \| \| weighted_index_rank_synthesis \| 加权综合技术力指数与排名 | 需规加权指数排名 | — | 未覆盖 | req_only |
| L48 \| \| subscore_weight_ratio_outputs \| 维度得分与权重占比输出 | 需规（2）分项权重 | — | 未覆盖 | req_only |
| L48 \| \| trend_analysis_advice \| 趋势分析与改进建议语义 | 需规（2）趋势建议 | — | 未覆盖 | req_only |
| L48 \| \| dynamic_monitor_param_refresh \| 动态监测与参数更新 | 需规（4）动态监测 | — | 未覆盖 | req_only |
| L48 \| \| eval_period_source_dimension \| 评估周期与来源维度调用语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L48 \| \| org_tag_online_search \| 机构标签在线检索语义 | 需规（3）标签检索 | — | 未覆盖 | req_only |
| L48 \| \| auto_eval_system_integration \| 自动化评估与管理系统对接 | 需规（3）系统对接 | — | 未覆盖 | req_only |
| L48 \| \| api_sdk_standard_call \| API SDK 标准化调用 | 需规（3）API/SDK | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`tech`） |
| 未覆盖 | 12（含 `_empty` 1 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-00624～API-00628 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
