# 服务机构实体与关系 · 功能点覆盖（svc.graph / L11+L12）

> catalog `svc.graph` · 50897 · path `/industry-service/graph`  
> **用例册**：`API-服务机构实体与关系-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000534`～`000583`，共 **50** 条）  
> A 线范围：**L11**（ner/main）· **L12**（intra/hang-*）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`  
> **A 线核对**：`grep svc.graph fp-split-by-api-run/work/L11.md L12.md`

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.graph.ner | POST | /entan/v1/svc/graph/ner | API-000534, API-000535, API-000536, API-000537, API-000538 | unavailable |
| svc.graph.intra | POST | /entan/v1/svc/graph/intra | API-000539, API-000540, API-000541, API-000542, API-000543 | unavailable |
| svc.graph.hang-industry | POST | /entan/v1/svc/graph/hang | API-000544, API-000545, API-000546, API-000547, API-000548 | unavailable |
| svc.graph.hang-tech | POST | /entan/v1/svc/graph/hang | API-000549, API-000550, API-000551, API-000552, API-000553 | unavailable |
| svc.graph.hang-enterprise | POST | /entan/v1/svc/graph/hang | API-000554, API-000555, API-000556, API-000557, API-000558 | unavailable |
| svc.graph.hang-gov | POST | /entan/v1/svc/graph/hang | API-000559, API-000560, API-000561, API-000562, API-000563 | unavailable |
| svc.graph.hang-talent | POST | /entan/v1/svc/graph/hang | API-000564, API-000565, API-000566, API-000567, API-000568 | unavailable |
| svc.graph.hang-policy | POST | /entan/v1/svc/graph/hang | API-000569, API-000570, API-000571, API-000572, API-000573 | unavailable |
| svc.graph.hang-research | POST | /entan/v1/svc/graph/hang | API-000574, API-000575, API-000576, API-000577, API-000578 | unavailable |
| svc.graph.main | GET | /entan/v1/svc/graph | API-000579, API-000580, API-000581, API-000582, API-000583 | unavailable |

---

## 2. 功能点 → 用例（L11+L12 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L11 \| svc.graph.ner \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| scope \| 算法输入-scopeone/batch | catalog scope | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| id \| 算法输入-id机构稳定 org_id（scope=one） | catalog id | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| mode \| 算法输入-moderule/llm | catalog mode | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-000534, API-000535, API-000536, API-000537, API-000538 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-000534 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.ner \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000534 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-000534 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.ner \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L11 \| svc.graph.ner \| _fail \| 调用失败 | 契约错误态 | API-000535, API-000536, API-000537, API-000538 | 已覆盖 | 契约占位+入参失败哨兵 |
| L11 \| svc.graph.main \| q \| 算法输入-q机构名检索 | catalog q | API-000579, API-000580, API-000581, API-000582, API-000583 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.main \| center \| 算法输入-center中心节点 VID | catalog center | API-000579, API-000580, API-000581, API-000582, API-000583 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.main \| hops \| 算法输入-hops邻域跳数 | catalog hops | API-000579, API-000580, API-000581, API-000582, API-000583 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.main \| limit \| 算法输入-limit节点上限 | catalog limit | API-000579, API-000580, API-000581, API-000582, API-000583 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L11 \| svc.graph.main \| nodes \| 算法输出-nodes节点 | catalog nodes | API-000579 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.main \| edges \| 算法输出-edges关系边 | catalog edges | API-000579 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.main \| source \| 算法输出-sourcehang／nebula／demo_gkx_chain；space 恒 demo_gkx_chain | catalog source | API-000579 | 契约占位 | 禁止 sample 数值作通过条件 |
| L11 \| svc.graph.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L11 \| svc.graph.main \| _fail \| 调用失败 | 契约错误态 | API-000580, API-000581, API-000582, API-000583 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.intra \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| scope \| 算法输入-scopeone/batch | catalog scope | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| mode \| 算法输入-moderule/llm | catalog mode | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["participates"] | catalog relation_whitelist | API-000539, API-000540, API-000541, API-000542, API-000543 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.intra \| written_edges \| 算法输出-written_edgesparticipates 边 | catalog written_edges | API-000539 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.intra \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000539 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.intra \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.intra \| _fail \| 调用失败 | 契约错误态 | API-000540, API-000541, API-000542, API-000543 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-industry \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| scope \| 算法输入-scopeone/batch | catalog scope | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| id \| 算法输入-id机构稳定 org_id，禁止用名称猜 VID | catalog id | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| mode \| 算法输入-moderule/llm | catalog mode | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000544, API-000545, API-000546, API-000547, API-000548 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-industry \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000544 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-industry \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-industry \| _fail \| 调用失败 | 契约错误态 | API-000545, API-000546, API-000547, API-000548 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-tech \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| scope \| 算法输入-scopeone/batch | catalog scope | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| mode \| 算法输入-moderule/llm | catalog mode | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000549, API-000550, API-000551, API-000552, API-000553 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-tech \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000549 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-tech \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-tech \| _fail \| 调用失败 | 契约错误态 | API-000550, API-000551, API-000552, API-000553 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-enterprise \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| scope \| 算法输入-scopeone/batch | catalog scope | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| mode \| 算法输入-moderule/llm | catalog mode | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000554, API-000555, API-000556, API-000557, API-000558 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-enterprise \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000554 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-enterprise \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-enterprise \| _fail \| 调用失败 | 契约错误态 | API-000555, API-000556, API-000557, API-000558 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-gov \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| scope \| 算法输入-scopeone/batch | catalog scope | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| mode \| 算法输入-moderule/llm | catalog mode | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000559, API-000560, API-000561, API-000562, API-000563 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-gov \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000559 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-gov \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-gov \| _fail \| 调用失败 | 契约错误态 | API-000560, API-000561, API-000562, API-000563 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-talent \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| scope \| 算法输入-scopeone/batch | catalog scope | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| mode \| 算法输入-moderule/llm | catalog mode | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000564, API-000565, API-000566, API-000567, API-000568 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-talent \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000564 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-talent \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-talent \| _fail \| 调用失败 | 契约错误态 | API-000565, API-000566, API-000567, API-000568 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-policy \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| scope \| 算法输入-scopeone/batch | catalog scope | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| mode \| 算法输入-moderule/llm | catalog mode | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000569, API-000570, API-000571, API-000572, API-000573 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-policy \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000569 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-policy \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-policy \| _fail \| 调用失败 | 契约错误态 | API-000570, API-000571, API-000572, API-000573 | 已覆盖 | 契约占位+入参失败哨兵 |
| L12 \| svc.graph.hang-research \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| scope \| 算法输入-scopeone/batch | catalog scope | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| id \| 算法输入-id机构稳定 org_id | catalog id | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| mode \| 算法输入-moderule/llm | catalog mode | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| dest_types \| 算法输入-dest_types终点白名单 | catalog dest_types | API-000574, API-000575, API-000576, API-000577, API-000578 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L12 \| svc.graph.hang-research \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000574 | 契约占位 | 禁止 sample 数值作通过条件 |
| L12 \| svc.graph.hang-research \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L12 \| svc.graph.hang-research \| _fail \| 调用失败 | 契约错误态 | API-000575, API-000576, API-000577, API-000578 | 已覆盖 | 契约占位+入参失败哨兵 |
---

## 3. §I 计数

| 指标 | 值 |
|------|-----|
| API 用例 | 50（000534～000583） |
| catalog endpoint | 10 |
| L11+L12 矩阵行 | 95 |
| `_empty` 未覆盖 | 10 |
| 金样 | API-000534 |
| 鉴权代表 | API-000535 |
| FUNC | 0 |
| code-registry / run-log | 未改（父控） |
