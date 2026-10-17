# 知识产权服务机构技术力评估 · 功能点覆盖（svc.tech-ip / L44）

> catalog `svc.tech-ip` · 50897 · path `/industry-service/tech-ip`  
> 用例 `API-知识产权服务机构技术力评估-用例.md`  
> A 线范围：**L44**（`fp-split-by-api-run/work/L44.md`）  
> 功能点键：`L44 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-ip.models | GET | /entan/v1/svc/models | API-000604～API-000608 | catalog `status=unavailable`；本页验收取 `kind=tech`；展示过滤 `service_type=IP` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L44 \| svc.tech-ip.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000604、API-000606、API-000607 | 已覆盖 | SVCTECHIP-01 tech 主路径；非法 kind 见 02/606；非本页 gap 见 03/607 |
| L44 \| svc.tech-ip.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-000608 | 契约占位 | unavailable，禁止 sample 指数/机构名/维度分作通过条件 |
| L44 \| svc.tech-ip.models \| _empty \| 技术力评估无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 本页语义必空」试调证据 |
| L44 \| svc.tech-ip.models \| _fail \| 技术力评估查询失败 | 契约错误态 | API-000604、API-000605、API-000606、API-000607 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind/页语义失败 |
| L44 \| \| etl_clean_standardize \| 多源机构数据清洗标准化 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L44 \| \| ip_four_dim_indicators_threshold \| 四维指标与行业阈值体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L44 \| \| dimension_item_score_calc \| 各维度单项指标得分 | 需规单项得分 | — | 未覆盖 | req_only |
| L44 \| \| weighted_tech_index_synthesis \| 加权合成技术力指数 | 需规加权合成 | — | 未覆盖 | req_only |
| L44 \| \| horizontal_org_compare \| 机构间横向对比 | 需规横向比较 | — | 未覆盖 | req_only |
| L44 \| \| vertical_dynamic_track \| 同一机构纵向动态跟踪 | 需规纵向跟踪 | — | 未覆盖 | req_only |
| L44 \| \| org_name_query_semantic \| 按机构名称查询语义 | 需规（3）机构名称 | — | 未覆盖 | req_only |
| L44 \| \| time_dimension_weight_custom \| 时间维度与权重定制 | 需规（3）调用参数 | — | 未覆盖 | req_only |
| L44 \| \| score_report_advice_outputs \| 得分报告与评估建议输出 | 需规（2）四类输出 | — | 未覆盖 | req_only |
| L44 \| \| periodic_schedule_monitor_refresh \| 周期性监测与指数刷新 | 需规（3）周期监测 | — | 未覆盖 | req_only |
| L44 \| \| api_sdk_batch_platform_integration \| API SDK 与平台批量评估 | 需规（3）系统对接 | — | 未覆盖 | req_only |

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
| 编号 | API-000604～API-000608 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
