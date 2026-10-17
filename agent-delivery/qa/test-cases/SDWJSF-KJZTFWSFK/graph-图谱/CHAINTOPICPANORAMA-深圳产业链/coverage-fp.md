# 深圳产业链 · 功能点覆盖（chain.topic-panorama / L15）

> catalog `chain.topic-panorama` · 50897 · path `/chain/topic-panorama`  
> **用例册**：`API-深圳产业链-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00326`～`00339`，共 **14** 条）  
> A 线范围：**L15**（hang · ops+main，20 live + 8 req_only）  
> 功能点键：`L15 | endpoint_id | field_key | 功能点中文`  
> **A 线核对**：`grep chain.topic-panorama fp-split-by-api-run/work/L15.md`（本子任务静态 grep，未读 code-registry）  
> **合表备注**：REST path 与 `chain.panorama` 相同；矩阵以 `chain.topic-panorama.*` endpoint_id 区分专题页验收归属。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.topic-panorama.main | GET | /chain/v1/chain/{chainId}/panorama | API-00326, API-00327, API-00328 | running |
| chain.topic-panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | API-00329～API-00339 | running |

---

## 2. 功能点 → 用例（L15 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L15 \| chain.topic-panorama.ops \| op_id \| 算法输入-op_id操作标识 | catalog op_id | API-00329、API-00335 | 部分覆盖 | 主路径+非法 path op_id；live 后执行期复核 |
| L15 \| chain.topic-panorama.ops \| scope \| 算法输入-scope作用域 | catalog scope | API-00329、API-00330、API-00331、API-00337 | 已覆盖 | 主路径+缺省+非法+batch |
| L15 \| chain.topic-panorama.ops \| id \| 算法输入-id实体标识 | catalog id | API-00329、API-00336 | 已覆盖 | 主路径+scope=one 缺 id |
| L15 \| chain.topic-panorama.ops \| filter \| 算法输入-filter过滤条件 | catalog filter | API-00337 | 已覆盖 | batch 组合 OPS-08 |
| L15 \| chain.topic-panorama.ops \| mode \| 算法输入-mode运行模式 | catalog mode | API-00329、API-00338 | 已覆盖 | rule 主路径+llm 备选 |
| L15 \| chain.topic-panorama.ops \| dry_run \| 算法输入-dry_run试运行 | catalog dry_run | API-00329、API-00339 | 已覆盖 | true 主路径+false 备选 |
| L15 \| chain.topic-panorama.ops \| relation_whitelist \| 算法输入-relation_whitelist关系白名单 | catalog relation_whitelist | API-00332、API-00333 | 已覆盖 | 主路径+缺省 |
| L15 \| chain.topic-panorama.ops \| dest_types \| 算法输入-dest_types目标类型 | catalog dest_types | API-00334 | 已覆盖 | C 类 OPS-06 |
| L15 \| chain.topic-panorama.ops \| written_nodes \| 算法输出-written_nodes写入节点 | catalog written_nodes | API-00329 | 已覆盖 | 类型断言；禁止 sample 条数 |
| L15 \| chain.topic-panorama.ops \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00329、API-00332 | 已覆盖 | A/B 路径 |
| L15 \| chain.topic-panorama.ops \| skipped \| 算法输出-skipped跳过统计 | catalog skipped | API-00329、API-00339 | 已覆盖 | array 形态 |
| L15 \| chain.topic-panorama.ops \| source \| 算法输出-source数据来源 | catalog source | API-00329、API-00338 | 已覆盖 | string 形态 |
| L15 \| chain.topic-panorama.ops \| space \| 算法输出-space图空间 | catalog space | API-00329 | 已覆盖 | string 形态 |
| L15 \| chain.topic-panorama.ops \| _empty \| 图谱写入无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L15 \| chain.topic-panorama.ops \| _fail \| 图谱写入调用失败 | 契约错误态 | API-00330、API-00331、API-00333、API-00335、API-00336 | 已覆盖 | 入参失败哨兵 |
| L15 \| chain.topic-panorama.main \| chainId \| 算法输入-chainId产业链标识 | catalog chainId | API-00326、API-00328 | 已覆盖 | 合法+非法 |
| L15 \| chain.topic-panorama.main \| nodes \| 算法输出-nodes节点集合 | catalog nodes | API-00326 | 已覆盖 | array 形态；禁止 sample 条数 |
| L15 \| chain.topic-panorama.main \| edges \| 算法输出-edges边集合 | catalog edges | API-00326 | 已覆盖 | array 形态 |
| L15 \| chain.topic-panorama.main \| _empty \| 全景查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空 chainId 证据 |
| L15 \| chain.topic-panorama.main \| _fail \| 全景查询调用失败 | 契约错误态 | API-00328 | 已覆盖 | 非法 chainId |
| L15 \| sz_panorama_etl_import \| 多源要素清洗入图 | 需规数据获取清洗 | — | 不纳入 | req_only |
| L15 \| panorama_upstream_downstream_map \| 全景映射上下游节点 | 需规（1）全景映射 | — | 不纳入 | req_only |
| L15 \| sz_geo_attr_filter \| 深圳地域属性筛选 | 需规（1）地域筛选 | — | 不纳入 | req_only |
| L15 \| manual_panorama_update \| 人工录入与增量更新 | 需规（1）人工更新 | — | 不纳入 | req_only |
| L15 \| attr_stats_analysis_report \| 属性统计及分析报告 | 需规（2）属性统计 | — | 不纳入 | req_only |
| L15 \| chain_stage_retrieval \| 产业链环节检索 | 需规应用端环节检索 | — | 不纳入 | req_only |
| L15 \| viz_panorama_display \| 可视化图谱呈现 | 需规（2）可视化 | — | 不纳入 | req_only |
| L15 \| panorama_data_export \| 全景数据导出 | 需规（3）导出 | — | 不纳入 | req_only |

---

## 3. §I 计数

| 指标 | 值 |
|------|-----|
| API 用例 | 14（00326～00339） |
| catalog endpoint | 2 |
| L15 live field 行 | 20 |
| 矩阵已覆盖/部分覆盖 | 18 |
| `_empty` 未覆盖 | 2 |
| req_only 不纳入 | 8 |
| 金样 | API-00326 |
| 鉴权代表 | API-00327 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/graph-图谱/CHAINTOPICPANORAMA-深圳产业链/` |
| code-registry | 父控回写 next_seq ≥ **340** |
