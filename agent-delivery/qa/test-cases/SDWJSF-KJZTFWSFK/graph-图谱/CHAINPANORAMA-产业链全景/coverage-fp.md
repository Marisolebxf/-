# 产业链全景 · 功能点覆盖（chain.panorama / L05+L14）

> catalog `chain.panorama` · 50897 · path `/chain/panorama`  
> **用例册**：`API-产业链全景-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00312`～`00325`，共 **14** 条）  
> A 线范围：**L05**（ops，16 行含 1 req_only）· **L14**（main，8 行含 3 req_only）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`  
> **A 线核对**：`grep chain.panorama fp-split-by-api-run/work/L05.md L14.md`（本子任务静态 grep，未读 code-registry）

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.panorama.main | GET | /chain/v1/chain/{chainId}/panorama | API-00312, API-00313, API-00314 | running |
| chain.panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | API-00315～API-00325 | running |

---

## 2. 功能点 → 用例（L05+L14 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L05 \| chain.panorama.ops \| op_id \| 算法输入-op_id步1 §17.1 写入算子 | catalog op_id | API-00315、API-00321 | 部分覆盖 | 主路径+非法 path op_id；live 后执行期复核 |
| L05 \| chain.panorama.ops \| scope \| 算法输入-scopeone 或 batch | catalog scope | API-00315、API-00316、API-00317、API-00323 | 已覆盖 | 主路径+缺省+非法+batch |
| L05 \| chain.panorama.ops \| id \| 算法输入-idscope=one 时填写稳定 chain_id | catalog id | API-00315、API-00322 | 已覆盖 | 主路径+scope=one 缺 id |
| L05 \| chain.panorama.ops \| filter \| 算法输入-filterscope=batch 时填写 chain_ids、industry_id、chain_level 或 all=true | catalog filter | API-00323 | 已覆盖 | batch 组合 OPS-08 |
| L05 \| chain.panorama.ops \| mode \| 算法输入-moderule 或 llm | catalog mode | API-00315、API-00324 | 已覆盖 | rule 主路径+llm 备选 |
| L05 \| chain.panorama.ops \| dry_run \| 算法输入-dry_runtrue 时返回计划写入项但不写 ADS/Nebula | catalog dry_run | API-00315、API-00325 | 已覆盖 | true 主路径+false 备选 |
| L05 \| chain.panorama.ops \| relation_whitelist \| 算法输入-relation_whitelistB/C 必填；页面按 op_id 自动提交 | catalog relation_whitelist | API-00318、API-00319 | 已覆盖 | 主路径+缺省 |
| L05 \| chain.panorama.ops \| dest_types \| 算法输入-dest_typesC 档目标类型；页面按 op_id 自动提交 | catalog dest_types | API-00320 | 已覆盖 | C 类 OPS-06 |
| L05 \| chain.panorama.ops \| written_nodes \| 算法输出-written_nodes本次写入或 dry_run 计划写入的节点 | catalog written_nodes | API-00315 | 已覆盖 | 类型断言；禁止 sample 条数 |
| L05 \| chain.panorama.ops \| written_edges \| 算法输出-written_edges本次写入或 dry_run 计划写入的边 | catalog written_edges | API-00315、API-00318 | 已覆盖 | A/B 路径 |
| L05 \| chain.panorama.ops \| skipped \| 算法输出-skippedempty_field/no_stable_id/not_in_wave/vid_too_long | catalog skipped | API-00315、API-00325 | 已覆盖 | array 形态 |
| L05 \| chain.panorama.ops \| source \| 算法输出-sourcenebula/ads/dry_run/rule_fallback | catalog source | API-00315、API-00324 | 已覆盖 | string 形态 |
| L05 \| chain.panorama.ops \| space \| 算法输出-space恒为 demo_gkx_chain | catalog space | API-00315 | 已覆盖 | string 形态 |
| L05 \| chain.panorama.ops \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L05 \| chain.panorama.ops \| _fail \| 调用失败 | 契约错误态 | API-00316、API-00317、API-00319、API-00321、API-00322 | 已覆盖 | 入参失败哨兵 |
| L05 \| chain.panorama.ops \| entity_recog_pipeline \| 产业实体识别流水线 | 需规 | — | 不纳入 | req_only |
| L14 \| chain.panorama.main \| chainId \| 算法输入-chainId稳定产业链 ID | catalog chainId | API-00312、API-00314 | 已覆盖 | 合法+非法 |
| L14 \| chain.panorama.main \| nodes \| 算法输出-nodes环节节点 | catalog nodes | API-00312 | 已覆盖 | array 形态；禁止 sample 条数 |
| L14 \| chain.panorama.main \| edges \| 算法输出-edges上下游关系 | catalog edges | API-00312 | 已覆盖 | array 形态 |
| L14 \| chain.panorama.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空 chainId 证据 |
| L14 \| chain.panorama.main \| _fail \| 调用失败 | 契约错误态 | API-00314 | 已覆盖 | 非法 chainId |
| L14 \| chain.panorama.main \| etl_clean_standardize \| 多源采集信息标准化清洗 | 需规 | — | 不纳入 | req_only |
| L14 \| chain.panorama.main \| panorama_visual_modeling \| 上下游全景可视化建模 | 需规 | — | 不纳入 | req_only |
| L14 \| chain.panorama.main \| sdk_invocation \| SDK 调用支持 | 需规 | — | 不纳入 | req_only |

---

## 3. §I 计数

| 指标 | 值 |
|------|-----|
| API 用例 | 14（00312～00325） |
| catalog endpoint | 2 |
| L05+L14 live field 行 | 20 |
| 矩阵已覆盖/部分覆盖 | 18 |
| `_empty` 未覆盖 | 2 |
| req_only 不纳入 | 4 |
| 金样 | API-00312 |
| 鉴权代表 | API-00313 |
