# 产业发展路线历程 · 功能点覆盖（chain.roadmap / L16）

> catalog `chain.roadmap` · path `#/chain/roadmap`  
> A 线真源：`fp-split-by-api-run/work/L16.md`  
> B 线用例：`API-产业发展路线历程-用例.md`（第二轮 **API-01300**～**01303**）  
> C 线用例：`FUNC-产业发展路线历程-用例.md`（第三轮 **FUNC-00509**～**00514**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | API 用例 | FUNC 用例 | catalog status |
|-------------|--------|------|----------|-----------|----------------|
| chain.hotspot.roadmap | GET | /innov/v1/industry/{chainId}/roadmap | API-01300、01301 | FUNC-00509、00510 | unavailable |
| chain.roadmap.m_chain_deep_119_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute | API-01302、01303 | FUNC-00511、00512 | available |

---

## 功能点 → 用例矩阵（挂 L16.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L16 \| chain.hotspot.roadmap \| chainId \| 算法输入-chainId产业标识 | API-01300、01301；FUNC-00509、00510 | 已覆盖 | 合法 path chainId=INB1701 + 缺 chainId；规则来源 catalog chainId |
| L16 \| chain.hotspot.roadmap \| timeline \| 算法输出-timeline历程时间线 | API-01300；FUNC-00509 | 已覆盖 | 主流程按 sampleResponse 断言 timeline（array）及嵌套 year、key_events；规则来源 catalog timeline |
| L16 \| chain.hotspot.roadmap \| _empty \| 发展历程无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且 timeline 为空」构造条件；规则来源 契约空结果 |
| L16 \| chain.hotspot.roadmap \| _fail \| 发展历程查询失败 | API-01301；FUNC-00510 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 API-01300 / FUNC-00509 的预期同时断言 sampleResponse 中未单独挂 L16 行的 `timeline[].year`、`timeline[].key_events` 及 `key_events[]` 的 `date`、`type`、`type_name`、`title`、`enterprise`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L16.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B/C 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多源指标标准化清洗，规则来源 需规段一清洗）、`event_indicator_threshold`（重大事件指标与阈值设定，规则来源 需规事件识别阈值）、`event_identification_detect`（超阈值重大事件识别，规则来源 需规事件识别算法）、`event_trend_inflection_semantics`（事件分布与趋势拐点语义，规则来源 需规分析输出趋势）、`dynamic_timeline_refresh`（历程动态监测与更新，规则来源 需规动态监测更新）、`trend_analysis_report`（产业发展趋势分析报告，规则来源 需规输出趋势报告）、`viz_event_distribution`（可视化事件分布支撑，规则来源 需规输出分布图）、`api_result_sync`（API 结果服务化同步，规则来源 需规（3）API）、`sdk_invocation`（SDK 调用支持，规则来源 需规（3）SDK）、`report_chart_export`（分析报告与数据导出，规则来源 需规（3）导出）。

---

## B/C 线独有（catalog 有、L16 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L16 \| chain.roadmap.m_chain_deep_119_1 \| — \| 产业发展路线历程模型 | API-01302、01303；FUNC-00511、00512 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L16 未给该 endpoint 挂 field 行 |
| （页面清单）接口信息 / 算法测试 | FUNC-00513、00514 | 无对应功能点 | 联调台 tab 与 catalog 下拉一致性 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| FUNC 用例数 | 6（FUNC-00509～00514） |
| API 主流程 | 2（API-01300 产业发展路线历程、API-01302 产业发展路线历程模型） |
| API 反向 | 2（API-01301、API-01303，均为缺 chainId） |
| FUNC 主流程 | 2（00509 产业发展路线历程、00511 产业发展路线历程模型） |
| FUNC 反向 | 2（00510、00512，均为缺 chainId） |
| FUNC 清单 | 2（00513 接口信息、00514 算法测试） |
| 编号 | API-01300～01303；FUNC-00509～00514 |
| L16 挂接行 | 4（已覆盖 2、部分覆盖 1、未覆盖 1） |
| L16 req_only | 10（无对应功能点） |
