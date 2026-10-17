# 培育企业综合推荐 · 功能点覆盖（entan.cultivate / L34）

> catalog `entan.cultivate` · 50897 · path `/entan/cultivate`  
> 用例册：`API-培育企业综合推荐-用例.md`（API-00147～00151）  
> A 线真源：`fp-split-by-api-run/work/L34.md`（catalog 契约行 4 条；req_only 行 10 条见文末）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| entan.cultivate.recommend | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | API-00147～00151 | catalog `status=unavailable` |

---

## 功能点 → 用例矩阵（catalog 契约行）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L34 \| entan.cultivate.recommend \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00147、00149、00150、00151 | 契约占位 / 入参异常 | endpoint unavailable；合法集合主路径待 available 后补 live 断言 |
| L34 \| entan.cultivate.recommend \| rankings \| 算法输出-rankings培育推荐排名体 | catalog rankings | API-00147 | 契约占位 | 禁止 sample recommendation_score 作通过条件 |
| L34 \| entan.cultivate.recommend \| _empty \| 培育推荐无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 codes 下 rankings 必空」构造证据 |
| L34 \| entan.cultivate.recommend \| _fail \| 培育推荐计算失败 | 契约错误态 | API-00147、00149、00150、00151 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |

---

## A 线 req_only 行（B 线无单独 API 用例）

| field_key（摘要） | 状态 | 说明 |
|-------------------|------|------|
| etl_clean_standardize | 无对应功能点 | 需规采集清洗；catalog 无独立 endpoint |
| triple_dimension_indicator_threshold | 无对应功能点 | 三维指标阈值在模型侧验收 |
| historical_sample_model_train | 无对应功能点 | 训练语义非 HTTP 契约行 |
| weighted_cultivation_index_compute | 无对应功能点 | 由 compute + rankings 协同，不拆行 |
| threshold_rank_preferred_select | 无对应功能点 | 同上 |
| dynamic_policy_market_refresh | 无对应功能点 | 动态更新非独立 API |
| preferred_rank_industry_viz_outputs | 无对应功能点 | 语义由 rankings 承载 |
| analysis_report_semantic | 无对应功能点 | catalog 无 report path |
| industry_policy_scale_filter_scope | 无对应功能点 | 入参仅 enterprise_codes |
| api_sdk_platform_export | 无对应功能点 | 无 export endpoint |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| API 用例数 | 5 |
| 契约 field 行（L34 表内带 endpoint） | 4 |
| 已覆盖（含契约占位） | 3 field 键（enterprise_codes、rankings、_fail） |
| 未覆盖 | 1（_empty） |
| req_only 行 | 10（反表登记，不要求 API 编号） |
