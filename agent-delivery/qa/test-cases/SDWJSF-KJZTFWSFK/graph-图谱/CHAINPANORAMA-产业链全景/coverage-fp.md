# 产业链全景 · 功能点覆盖（chain.panorama / L05+L06+L14）

> catalog `chain.panorama` · path `#/chain/panorama`  
> A 线真源：`fp-split-by-api-run/work/L05.md`、`L06.md`、`L14.md`  
> B 线用例：`API-产业链全景-用例.md`（第二轮 **API-01220**～**01238**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | API-01220～01234 | running |
| chain.panorama.main | GET | /chain/v1/chain/{chainId}/panorama | API-01235、01236 | running |
| chain.panorama.m_chain_deep_117_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute | API-01237、01238 | available |

---

## 功能点 → 用例矩阵（挂 L05.md / L14.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L05 \| chain.panorama.ops \| op_id \| 算法输入-op_id步1 §17.1 写入算子 | API-01220、01227 | 已覆盖 | sampleRequest + 缺 op_id |
| L05 \| chain.panorama.ops \| scope \| 算法输入-scopeone 或 batch | API-01220、01228 | 已覆盖 | sampleRequest + 缺 scope |
| L05 \| chain.panorama.ops \| id \| 算法输入-idscope=one 时填写稳定 chain_id | API-01220、01221、01229 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| filter \| 算法输入-filterscope=batch 时填写 chain_ids、industry_id、chain_level 或 all=true | API-01222、01230 | 已覆盖 | sample 未含该键，备选传入 + 非法 |
| L05 \| chain.panorama.ops \| mode \| 算法输入-moderule 或 llm | API-01220、01223、01231 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| dry_run \| 算法输入-dry_runtrue 时返回计划写入项但不写 ADS/Nebula | API-01220、01224、01232 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| relation_whitelist \| 算法输入-relation_whitelistB/C 必填；页面按 op_id 自动提交 | API-01225、01233 | 已覆盖 | sample 未含该键，备选传入 + 非法 |
| L05 \| chain.panorama.ops \| dest_types \| 算法输入-dest_typesC 档目标类型；页面按 op_id 自动提交 | API-01226、01234 | 已覆盖 | sample 未含该键，备选传入 + 非法 |
| L05 \| chain.panorama.ops \| written_nodes \| 算法输出-written_nodes本次写入或 dry_run 计划写入的节点 | API-01220 | 已覆盖 | 主流程逐字段断言；同接口备选预期相同 |
| L05 \| chain.panorama.ops \| written_edges \| 算法输出-written_edges本次写入或 dry_run 计划写入的边 | API-01220 | 已覆盖 | 同条主流程 |
| L05 \| chain.panorama.ops \| skipped \| 算法输出-skippedempty_field/no_stable_id/not_in_wave/vid_too_long | API-01220 | 已覆盖 | 同条主流程 |
| L05 \| chain.panorama.ops \| source \| 算法输出-sourcenebula/ads/dry_run/rule_fallback | API-01220 | 已覆盖 | 同条主流程；示例值为 demo_gkx_chain |
| L05 \| chain.panorama.ops \| space \| 算法输出-space恒为 demo_gkx_chain | API-01220 | 已覆盖 | 同条主流程 |
| L05 \| chain.panorama.ops \| _empty \| 查询无数据空态 | API-01220 | 已覆盖 | sampleResponse 的 written_nodes/written_edges/skipped 即为空数组，写在主流程预期 |
| L05 \| chain.panorama.ops \| _fail \| 调用失败 | API-01227～01234 | 已覆盖 | 8 条入参反向，message/msg 指出该参数 |
| L14 \| chain.panorama.main \| chainId \| 算法输入-chainId稳定产业链 ID | API-01235、01236 | 已覆盖 | 合法 + 缺 chainId |
| L14 \| chain.panorama.main \| nodes \| 算法输出-nodes环节节点 | API-01235 | 已覆盖 | 主流程逐字段断言 |
| L14 \| chain.panorama.main \| edges \| 算法输出-edges上下游关系 | API-01235 | 已覆盖 | 同条主流程 |
| L14 \| chain.panorama.main \| _empty \| 查询无数据空态 | API-01235 | 已覆盖 | sampleResponse 的 nodes/edges 即为空数组，写在主流程预期 |
| L14 \| chain.panorama.main \| _fail \| 调用失败 | API-01236 | 已覆盖 | 缺 chainId，message/msg 指出 chainId |

---

## req_only 行（无 endpoint 挂接）

L05 `entity_recog_pipeline`（产业实体识别流水线）、L06 `relation_extract_pipeline` / `relation_empty` / `relation_fail`、L14 `etl_clean_standardize` / `panorama_visual_modeling` / `sdk_invocation` 共 **7** 行无 catalog endpoint。B 线记 **无对应功能点**，不单独开 API 用例。

---

## B 线独有（联调台有、A 线 L05/L06/L14 未列 endpoint）

| title | endpoint_id | 对应用例 | 状态 |
|-------|-------------|----------|------|
| 产业链全景模型 | chain.panorama.m_chain_deep_117_1 | API-01237、01238 | 无对应功能点 |

主流程 API-01237 仍按该接口 sampleResponse 写 metric_id、hint。A 线三张表没有该 endpoint 的 field 行。
