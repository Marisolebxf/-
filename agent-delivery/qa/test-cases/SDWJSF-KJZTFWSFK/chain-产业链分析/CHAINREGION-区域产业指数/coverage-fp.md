# 区域产业指数 · 功能点覆盖（chain.region / L23）

> catalog `chain.region` · path `#/chain/region`  
> A 线真源：`fp-split-by-api-run/work/L23.md`  
> B 线用例：`API-区域产业指数-用例.md`（第二轮 **API-01274**～**01279**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.region.main | GET | /innov/v1/industry/{chainId}/region-index | API-01274、01275 | unavailable |
| chain.region.competitiveness | GET | /innov/v1/industry/{chainId}/competitiveness | API-01276、01277 | unavailable |
| chain.region.m_chain_deep_126_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute | API-01278、01279 | available |

---

## 功能点 → 用例矩阵（挂 L23.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L23 \| chain.region.main \| chainId \| 算法输入-chainId产业标识 | API-01274、01275 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L23 \| chain.region.main \| region_index \| 算法输出-region_index区域指数体 | API-01274 | 已覆盖 | 主流程按 sampleResponse 断言数组元素上的 region_index（number）；规则来源 catalog region_index |
| L23 \| chain.region.main \| _empty \| 区域产业指数无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无指数数据」构造条件；规则来源 契约空结果 |
| L23 \| chain.region.main \| _fail \| 区域产业指数查询失败 | API-01275 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |
| L23 \| chain.region.competitiveness \| chainId \| 算法输入-chainId产业标识 | API-01276、01277 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L23 \| chain.region.competitiveness \| competitiveness_index \| 算法输出-competitiveness_index竞争力评价体 | API-01276 | 已覆盖 | 同条主流程断言 competitiveness_index（number）；规则来源 catalog competitiveness_index |
| L23 \| chain.region.competitiveness \| _empty \| 竞争力评价无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无评价数据」构造条件；规则来源 契约空结果 |
| L23 \| chain.region.competitiveness \| _fail \| 竞争力评价查询失败 | API-01277 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L23.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多源产业数据标准化清洗）、`tri_dimension_indicator_threshold`（三维度指标与权重阈值）、`weighted_region_index_compute`（三维度加权综合指数）、`region_index_trend_analysis`（指数趋势与时间序列分析）、`strength_weakness_assessment`（优势与短板评估）、`tri_dimension_competitiveness_eval`（三维度竞争力综合评价）、`inter_region_comparison`（区域间对比分析）、`region_tag_query_scope`（区域标签实时查询语义）、`trend_analysis_report`（趋势分析报告）、`region_comparison_chart_data`（区域对比分析图表数据）、`analysis_report_export`（分析报告与数据导出）。

---

## B 线独有（catalog 有、L23 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L23 \| chain.region.m_chain_deep_126_1 \| — \| 区域产业指数模型 | API-01278、01279 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L23 未给该 endpoint 挂 field 行 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 6 |
| 主流程 | 3（API-01274 区域指数、API-01276 竞争力评价、API-01278 区域产业指数模型） |
| 反向 | 3（API-01275、01277、01279，均为缺 chainId） |
| 编号 | API-01274～01279 |
| L23 挂接行 | 8（已覆盖 4、部分覆盖 2、未覆盖 2） |
| L23 req_only | 11（无对应功能点） |
