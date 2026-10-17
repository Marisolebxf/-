# 产业发展路线历程 · 功能点覆盖（chain.roadmap / L16）

> catalog `chain.roadmap` · 50897 · path `#/chain/roadmap`  
> 用例 `API-产业发展路线历程-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/chain.json`（页 `chain.roadmap`）  
> 功能点键：`L16 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.hotspot.roadmap | GET | /innov/v1/industry/{chainId}/roadmap | API-00389～00393 | catalog `unavailable`；§0 **未试调**；本批为 **金样 5 条** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L16 \| chain.hotspot.roadmap \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00389、00391、00392 | 已覆盖 | 主路径占位 + 非法/缺 path |
| L16 \| chain.hotspot.roadmap \| timeline \| 算法输出-timeline历程时间线 | catalog timeline | — | **未覆盖** | unavailable 金样批未写 live 成功形态；升档后补 |
| L16 \| chain.hotspot.roadmap \| _empty \| 发展历程无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L16 \| chain.hotspot.roadmap \| _fail \| 发展历程查询失败 | 契约错误态 | API-00390、00391、00392、00393 | 已覆盖 | 鉴权、非法 id、缺 path、畸形 id |
| L16 \| chain.hotspot.roadmap \| etl_clean_standardize \| 多源指标标准化清洗 | 需规段一清洗 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| event_indicator_threshold \| 重大事件指标与阈值设定 | 需规事件识别阈值 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| event_identification_detect \| 超阈值重大事件识别 | 需规事件识别算法 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| event_trend_inflection_semantics \| 事件分布与趋势拐点语义 | 需规分析输出趋势 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| dynamic_timeline_refresh \| 历程动态监测与更新 | 需规动态监测更新 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| trend_analysis_report \| 产业发展趋势分析报告 | 需规输出趋势报告 | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| viz_event_distribution \| 可视化事件分布支撑 | 需规输出分布图 | — | 无对应功能点 | req_only（viz 非 responseFields） |
| L16 \| chain.hotspot.roadmap \| api_result_sync \| API 结果服务化同步 | 需规（3）API | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| sdk_invocation \| SDK 调用支持 | 需规（3）SDK | — | 无对应功能点 | req_only |
| L16 \| chain.hotspot.roadmap \| report_chart_export \| 分析报告与数据导出 | 需规（3）导出 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 2（chainId、_fail） |
| 未覆盖（契约 field / _empty） | 2（timeline、_empty） |
| 无对应功能点（req_only） | 10 |
| API 用例条数 | 5（00389～00393） |
| 金样 | API-00389 |
