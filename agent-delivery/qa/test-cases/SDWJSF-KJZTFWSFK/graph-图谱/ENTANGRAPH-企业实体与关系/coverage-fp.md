# 企业实体与关系 · 功能点覆盖（entan.graph / L09+L10）

> catalog `entan.graph` · 50897 · path `/entan/graph`  
> **用例册**：`API-企业实体与关系-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00167`～`00211`，共 **45** 条）  
> A 线范围：**L09**（ner/main，20 行）· **L10**（intra/hang，130 行）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`  
> L11（`svc.graph`）与本页无关，未纳入矩阵。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.graph.ner | POST | /entan/v1/entan/graph/ner | API-00167, API-00168, API-00169, API-00170 | unavailable |
| entan.graph.intra-coop | POST | /entan/v1/entan/graph/intra | API-00171, API-00172, API-00173, API-00174, API-00175 | unavailable |
| entan.graph.intra-invest | POST | /entan/v1/entan/graph/intra | API-00176, API-00177, API-00178, API-00179, API-00180 | unavailable |
| entan.graph.intra-belong | POST | /entan/v1/entan/graph/intra | API-00181, API-00182, API-00183, API-00184, API-00185 | unavailable |
| entan.graph.intra-supply | POST | /entan/v1/entan/graph/intra | API-00186, API-00187, API-00188, API-00189, API-00190 | unavailable |
| entan.graph.hang-industry | POST | /entan/v1/entan/graph/hang | API-00191, API-00192, API-00193 | unavailable |
| entan.graph.hang-tech | POST | /entan/v1/entan/graph/hang | API-00194, API-00195, API-00196 | unavailable |
| entan.graph.hang-talent | POST | /entan/v1/entan/graph/hang | API-00197, API-00198, API-00199 | unavailable |
| entan.graph.hang-policy | POST | /entan/v1/entan/graph/hang | API-00200, API-00201, API-00202 | unavailable |
| entan.graph.hang-research | POST | /entan/v1/entan/graph/hang | API-00203, API-00204, API-00205 | unavailable |
| entan.graph.hang-service | POST | /entan/v1/entan/graph/hang | API-00206, API-00207, API-00208 | unavailable |
| entan.graph.main | GET | /entan/v1/entan/graph | API-00209, API-00210, API-00211 | unavailable |

---

## 2. 功能点 → 用例（L09+L10 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L09 \| entan.graph.ner \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00167、API-00168、API-00169、API-00170 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L09 \| entan.graph.ner \| scope \| 算法输入-scopeone/batch | catalog scope | API-00167、API-00168、API-00169、API-00170 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L09 \| entan.graph.ner \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| mode \| 算法输入-moderule/llm | catalog mode | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00167 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.ner \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L09 \| entan.graph.ner \| _fail \| 调用失败 | 契约错误态 | API-00168、API-00169、API-00170 | 已覆盖 | 契约占位+入参失败哨兵 |
| L09 \| entan.graph.main \| center \| 算法输入-center中心 org_id 或 ent: VID | catalog center | API-00209、API-00210、API-00211 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L09 \| entan.graph.main \| hops \| 算法输入-hops邻域跳数 | catalog hops | API-00209、API-00210、API-00211 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L09 \| entan.graph.main \| limit \| 算法输入-limit节点上限 | catalog limit | API-00209、API-00210、API-00211 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L09 \| entan.graph.main \| nodes \| 算法输出-nodes节点 | catalog nodes | API-00209 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.main \| edges \| 算法输出-edges关系边 | catalog edges | API-00209 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.main \| source \| 算法输出-sourcenebula／pg；space 恒 demo_gkx_chain | catalog source | API-00209 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L09 \| entan.graph.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L09 \| entan.graph.main \| _fail \| 调用失败 | 契约错误态 | API-00210、API-00211 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.intra-coop \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00171、API-00172、API-00173、API-00174、API-00175 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-coop \| scope \| 算法输入-scopeone/batch | catalog scope | API-00171、API-00172、API-00173、API-00174、API-00175 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-coop \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| mode \| 算法输入-moderule/llm | catalog mode | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cooperate"] | catalog relation_whitelist | API-00171、API-00172、API-00173、API-00174、API-00175 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-coop \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00171 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-coop \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.intra-coop \| _fail \| 调用失败 | 契约错误态 | API-00172、API-00173、API-00174、API-00175 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.intra-invest \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00176、API-00177、API-00178、API-00179、API-00180 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-invest \| scope \| 算法输入-scopeone/batch | catalog scope | API-00176、API-00177、API-00178、API-00179、API-00180 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-invest \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| mode \| 算法输入-moderule/llm | catalog mode | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["invest"] | catalog relation_whitelist | API-00176、API-00177、API-00178、API-00179、API-00180 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-invest \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00176 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-invest \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.intra-invest \| _fail \| 调用失败 | 契约错误态 | API-00177、API-00178、API-00179、API-00180 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.intra-belong \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00181、API-00182、API-00183、API-00184、API-00185 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-belong \| scope \| 算法输入-scopeone/batch | catalog scope | API-00181、API-00182、API-00183、API-00184、API-00185 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-belong \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| mode \| 算法输入-moderule/llm | catalog mode | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["parent_sub"] | catalog relation_whitelist | API-00181、API-00182、API-00183、API-00184、API-00185 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-belong \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00181 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-belong \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.intra-belong \| _fail \| 调用失败 | 契约错误态 | API-00182、API-00183、API-00184、API-00185 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.intra-supply \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00186、API-00187、API-00188、API-00189、API-00190 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-supply \| scope \| 算法输入-scopeone/batch | catalog scope | API-00186、API-00187、API-00188、API-00189、API-00190 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-supply \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| mode \| 算法输入-moderule/llm | catalog mode | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["supply"] | catalog relation_whitelist | API-00186、API-00187、API-00188、API-00189、API-00190 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.intra-supply \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00186 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.intra-supply \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.intra-supply \| _fail \| 调用失败 | 契约错误态 | API-00187、API-00188、API-00189、API-00190 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-industry \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00191、API-00192、API-00193 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-industry \| scope \| 算法输入-scopeone/batch | catalog scope | API-00191、API-00192、API-00193 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-industry \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| mode \| 算法输入-moderule/llm | catalog mode | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["industry"] | catalog dest_types | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00191 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-industry \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-industry \| _fail \| 调用失败 | 契约错误态 | API-00192、API-00193 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-tech \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00194、API-00195、API-00196 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-tech \| scope \| 算法输入-scopeone/batch | catalog scope | API-00194、API-00195、API-00196 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-tech \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| mode \| 算法输入-moderule/llm | catalog mode | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["technology"] | catalog dest_types | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00194 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-tech \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-tech \| _fail \| 调用失败 | 契约错误态 | API-00195、API-00196 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-talent \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00197、API-00198、API-00199 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-talent \| scope \| 算法输入-scopeone/batch | catalog scope | API-00197、API-00198、API-00199 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-talent \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| mode \| 算法输入-moderule/llm | catalog mode | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["talent"] | catalog dest_types | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00197 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-talent \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-talent \| _fail \| 调用失败 | 契约错误态 | API-00198、API-00199 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-policy \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00200、API-00201、API-00202 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-policy \| scope \| 算法输入-scopeone/batch | catalog scope | API-00200、API-00201、API-00202 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-policy \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| mode \| 算法输入-moderule/llm | catalog mode | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["policy"] | catalog dest_types | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00200 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-policy \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-policy \| _fail \| 调用失败 | 契约错误态 | API-00201、API-00202 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-research \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00203、API-00204、API-00205 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-research \| scope \| 算法输入-scopeone/batch | catalog scope | API-00203、API-00204、API-00205 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-research \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| mode \| 算法输入-moderule/llm | catalog mode | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["research"] | catalog dest_types | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00203 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-research \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-research \| _fail \| 调用失败 | 契约错误态 | API-00204、API-00205 | 已覆盖 | 契约占位+入参失败哨兵 |
| L10 \| entan.graph.hang-service \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00206、API-00207、API-00208 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-service \| scope \| 算法输入-scopeone/batch | catalog scope | API-00206、API-00207、API-00208 | 部分覆盖 | unavailable 占位+必填/非法哨兵；live 后补主路径 |
| L10 \| entan.graph.hang-service \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| mode \| 算法输入-moderule/llm | catalog mode | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["service"] | catalog dest_types | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00206 | 契约占位 | 禁止 sample 数值作通过条件；live 后补字段类型断言 |
| L10 \| entan.graph.hang-service \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L10 \| entan.graph.hang-service \| _fail \| 调用失败 | 契约错误态 | API-00207、API-00208 | 已覆盖 | 契约占位+入参失败哨兵 |

---

## 3. §I 计数

| 项 | 值 |
|----|-----|
| A 线功能点行（L09+L10） | **150** |
| catalog endpoint 数 | **12** |
| API 用例数 | **45**（00167～00211） |
| 金样号 | **API-00167** |
| 异常-鉴权 | **API-00168**（全页代表） |
| `_empty` 行 | **12** 行 **未覆盖** |
| 矩阵行非未覆盖 | **138** / 150 |
| code-registry | 父控回写 next_seq ≥ **212** |
