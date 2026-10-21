# 深圳产业链 · 功能点覆盖（chain.topic-panorama / L15）

> catalog `chain.topic-panorama` · path `/chain/topic-panorama`  
> A 线真源：`fp-split-by-api-run/work/L15.md`（28 行：20 live + 8 req_only）  
> B 线用例：`FUNC-深圳产业链-用例.md`（第三轮 **FUNC-00428**～**00448**）  
> 功能点键：`L15 | endpoint_id | field_key | 功能点中文`。多个 field 可挂同一 FUNC 编号。  
> `_empty` 无稳定必空入参，记未覆盖，不单开空态用例。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.topic-panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | FUNC-00428～00442 | running |
| chain.topic-panorama.main | GET | /chain/v1/chain/{chainId}/panorama | FUNC-00443、00444 | running |
| chain.topic-panorama.m_chain_deep_118_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute | FUNC-00445、00446 | available |
| （页面清单） | — | — | FUNC-00447、00448 | — |

---

## 功能点 → 用例矩阵（挂 L15.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L15 \| chain.topic-panorama.ops \| op_id \| 算法输入-op_id操作标识 | catalog op_id | FUNC-00428、00435 | 已覆盖 | 主流程合法值 + 缺省反向 |
| L15 \| chain.topic-panorama.ops \| scope \| 算法输入-scope作用域 | catalog scope | FUNC-00428、00436 | 已覆盖 | 主流程合法值 + 缺省反向 |
| L15 \| chain.topic-panorama.ops \| id \| 算法输入-id实体标识 | catalog id | FUNC-00428、00429、00437 | 已覆盖 | 主流程 + 省略 + 非法值 |
| L15 \| chain.topic-panorama.ops \| filter \| 算法输入-filter过滤条件 | catalog filter | FUNC-00430、00438 | 已覆盖 | sample 未含，备选传入 + 非法值 |
| L15 \| chain.topic-panorama.ops \| mode \| 算法输入-mode运行模式 | catalog mode | FUNC-00428、00431、00439 | 已覆盖 | 主流程 + 省略 + 非法值 |
| L15 \| chain.topic-panorama.ops \| dry_run \| 算法输入-dry_run试运行 | catalog dry_run | FUNC-00428、00432、00440 | 已覆盖 | 主流程 + 省略 + 非法值 |
| L15 \| chain.topic-panorama.ops \| relation_whitelist \| 算法输入-relation_whitelist关系白名单 | catalog relation_whitelist | FUNC-00433、00441 | 已覆盖 | sample 未含，备选传入 + 非法值 |
| L15 \| chain.topic-panorama.ops \| dest_types \| 算法输入-dest_types目标类型 | catalog dest_types | FUNC-00434、00442 | 已覆盖 | sample 未含，备选传入 + 非法值 |
| L15 \| chain.topic-panorama.ops \| written_nodes \| 算法输出-written_nodes写入节点 | catalog written_nodes | FUNC-00428 | 已覆盖 | 主流程逐字段断言；备选正向同结构 |
| L15 \| chain.topic-panorama.ops \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00428 | 已覆盖 | 主流程逐字段断言；备选正向同结构 |
| L15 \| chain.topic-panorama.ops \| skipped \| 算法输出-skipped跳过统计 | catalog skipped | FUNC-00428 | 已覆盖 | 主流程逐字段断言；备选正向同结构 |
| L15 \| chain.topic-panorama.ops \| source \| 算法输出-source数据来源 | catalog source | FUNC-00428 | 已覆盖 | 主流程逐字段断言；备选正向同结构 |
| L15 \| chain.topic-panorama.ops \| space \| 算法输出-space图空间 | catalog space | FUNC-00428 | 已覆盖 | 主流程逐字段断言；备选正向同结构 |
| L15 \| chain.topic-panorama.ops \| _empty \| 图谱写入无数据空态 | 契约空结果 | FUNC-00428 | 已覆盖 | sampleResponse 空数组写在主流程预期 |
| L15 \| chain.topic-panorama.ops \| _fail \| 图谱写入调用失败 | 契约错误态 | FUNC-00435～00442 | 已覆盖 | 8 个参数各 1 条反向，message 或 msg 指出该参数 |
| L15 \| chain.topic-panorama.main \| chainId \| 算法输入-chainId产业链标识 | catalog chainId | FUNC-00443、00444 | 已覆盖 | 主流程合法值 + 缺省反向 |
| L15 \| chain.topic-panorama.main \| nodes \| 算法输出-nodes节点集合 | catalog nodes | FUNC-00443 | 已覆盖 | 主流程逐字段断言 |
| L15 \| chain.topic-panorama.main \| edges \| 算法输出-edges边集合 | catalog edges | FUNC-00443 | 已覆盖 | 主流程逐字段断言 |
| L15 \| chain.topic-panorama.main \| _empty \| 全景查询无数据空态 | 契约空结果 | FUNC-00443 | 已覆盖 | 空 nodes/edges 写在主流程预期 |
| L15 \| chain.topic-panorama.main \| _fail \| 全景查询调用失败 | 契约错误态 | FUNC-00444 | 已覆盖 | 缺 chainId，message 或 msg 指出该参数 |
| （页面清单） \| 接口信息 / 算法测试 | 联调台 tab | FUNC-00447、00448 | 无对应功能点 | 3 接口下拉与 method/path 刷新 |

---

## B 线独有（联调台有、A 线未挂 field）

| 说明 | 对应用例 | 状态 |
|------|----------|------|
| `chain.topic-panorama.m_chain_deep_118_1`（深圳产业链模型）在 L15 无 field_key 行 | FUNC-00445、00446 | 无对应功能点 |

---

## req_only 行（无 endpoint 挂接）

L15.md 下列行无 catalog endpoint / field，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 状态 |
|----------|----------|------|
| L15 \| sz_panorama_etl_import \| 多源要素清洗入图 | 需规数据获取清洗 | 无对应功能点 |
| L15 \| panorama_upstream_downstream_map \| 全景映射上下游节点 | 需规（1）全景映射 | 无对应功能点 |
| L15 \| sz_geo_attr_filter \| 深圳地域属性筛选 | 需规（1）地域筛选 | 无对应功能点 |
| L15 \| manual_panorama_update \| 人工录入与增量更新 | 需规（1）人工更新 | 无对应功能点 |
| L15 \| attr_stats_analysis_report \| 属性统计及分析报告 | 需规（2）属性统计 | 无对应功能点 |
| L15 \| chain_stage_retrieval \| 产业链环节检索 | 需规应用端环节检索 | 无对应功能点 |
| L15 \| viz_panorama_display \| 可视化图谱呈现 | 需规（2）可视化 | 无对应功能点 |
| L15 \| panorama_data_export \| 全景数据导出 | 需规（3）导出 | 无对应功能点 |

---

## 计数

| 指标 | 值 |
|------|-----|
| FUNC 用例 | 21（00428～00448） |
| 主流程 / 备选 / 反向 / 清单 | 3 / 6 / 10 / 2 |
| catalog endpoint | 3 |
| L15 live field 行 | 20 |
| 已覆盖（live field） | 20 |
| `_empty` | 2（写在主流程预期，不单开） |
| req_only | 8（无对应功能点） |
| B 线独有接口 | 1（深圳产业链模型 metric，无 A 线 field） |
| 主流程编号 | FUNC-00428、FUNC-00443、FUNC-00445 |
| code-registry | 本子任务未改（父控回写） |
