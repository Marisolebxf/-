# 区域产业指数 · 功能点覆盖（chain.region / L23）

> catalog `chain.region` · 50897 · path `#/chain/region`  
> 用例 `API-区域产业指数-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/chain.json`（页 `chain.region`）  
> 功能点键：`L23 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐；A 行来源 grep `work/L23.md`）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.region.main | GET | /innov/v1/industry/{chainId}/region-index | API-00360～00366 | catalog `unavailable`；§0 **未试调** |
| chain.region.competitiveness | GET | /innov/v1/industry/{chainId}/competitiveness | API-00367～00373 | catalog `unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L23 \| chain.region.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00360、00362、00363、00366 | 已覆盖 | 合法主路径 + 非法/缺 path + 备选 id |
| L23 \| chain.region.main \| region_index \| 算法输出-region_index区域指数体 | catalog region_index | API-00365 | 契约占位 | unavailable；成功形态预备，不写 sample 分值 |
| L23 \| chain.region.main \| _empty \| 区域产业指数无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L23 \| chain.region.main \| _fail \| 区域产业指数查询失败 | 契约错误态 | API-00362、00363、00361、00364 | 已覆盖 | 非法 id、缺 path、鉴权、缺租户 |
| L23 \| chain.region.competitiveness \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00367、00368、00369、00371 | 已覆盖 | 主路径 + 非法/缺 path + 备选 id |
| L23 \| chain.region.competitiveness \| competitiveness_index \| 算法输出-competitiveness_index竞争力评价体 | catalog competitiveness_index | API-00370 | 契约占位 | unavailable；成功形态预备 |
| L23 \| chain.region.competitiveness \| _empty \| 竞争力评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L23 \| chain.region.competitiveness \| _fail \| 竞争力评价查询失败 | 契约错误态 | API-00368、00369、00372、00373 | 已覆盖 | 非法 id、缺 path、畸形 id、错误方法；鉴权见 API-00361 |
| L23 \| （无 endpoint） \| etl_clean_standardize \| 多源产业数据标准化清洗 | 需规（1）采集清洗 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| tri_dimension_indicator_threshold \| 三维度指标与权重阈值 | 需规指标体系 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| weighted_region_index_compute \| 三维度加权综合指数 | 需规分析计算 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| region_index_trend_analysis \| 指数趋势与时间序列分析 | 需规趋势分析 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| strength_weakness_assessment \| 优势与短板评估 | 需规（2）优势短板 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| tri_dimension_competitiveness_eval \| 三维度竞争力综合评价 | 需规竞争力评价 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| inter_region_comparison \| 区域间对比分析 | 需规区域对比 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| region_tag_query_scope \| 区域标签实时查询语义 | 需规（3）区域标签 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| trend_analysis_report \| 趋势分析报告 | 需规（2）趋势报告 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| region_comparison_chart_data \| 区域对比分析图表数据 | 需规（2）对比图表 | — | 无对应功能点 | req_only |
| L23 \| （无 endpoint） \| analysis_report_export \| 分析报告与数据导出 | 需规（3）导出 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 6（两 endpoint 的 chainId、region_index/competitiveness_index 占位、_fail） |
| 未覆盖 | 2（两 endpoint 各 _empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 14（00360～00373） |
| 金样 | API-00360 |
