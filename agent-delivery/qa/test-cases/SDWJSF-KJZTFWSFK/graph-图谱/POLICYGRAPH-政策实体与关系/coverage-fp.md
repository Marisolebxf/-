# 政策实体与关系 · 功能点覆盖（policy.graph / L07+L08）

> catalog `policy.graph` · path `#/policy/graph`  
> A 线真源：`fp-split-by-api-run/work/L07.md`、`work/L08.md`  
> B 线用例：`API-政策实体与关系-用例.md`（第二轮 **API-01333**～**01401**）  
> 联调台端口 50897（本册不打开页面）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.graph.ner | POST | /policy/v1/policy/graph/ner | API-01333～01343 | unavailable |
| policy.graph.intra | POST | /policy/v1/policy/graph/intra | API-01344～01355 | unavailable |
| policy.graph.hang-support | POST | /policy/v1/policy/graph/hang | API-01356～01368 | unavailable |
| policy.graph.hang-apply | POST | /policy/v1/policy/graph/hang | API-01369～01381 | unavailable |
| policy.graph.hang-regulate | POST | /policy/v1/policy/graph/hang | API-01382～01394 | unavailable |
| policy.graph.main | GET | /policy/v1/policy/graph | API-01395～01401 | unavailable |

---

## 功能点 → 用例矩阵（挂 L07.md、L08.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L07 \| policy.graph.ner \| op_id \| 算法输入-op_id写入算子 | API-01333、API-01338 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L07 \| policy.graph.ner \| scope \| 算法输入-scopeone/batch | API-01333、API-01339 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L07 \| policy.graph.ner \| id \| 算法输入-id政策稳定 ID（scope=one） | API-01333、API-01334、API-01340 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| mode \| 算法输入-moderule/llm | API-01333、API-01335、API-01341 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | API-01333、API-01336、API-01342 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| filter \| 算法输入-filterscope=batch 过滤对象，高级 JSON 保持 {all:true} | API-01337、API-01343 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L07 \| policy.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | API-01333 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| skipped \| 算法输出-skipped四码跳过 | API-01333 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | API-01333 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L07 \| policy.graph.ner \| _fail \| 调用失败 | API-01338、API-01339、API-01340、API-01341、API-01342、API-01343 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L07 \| policy.graph.main \| center \| 算法输入-center中心节点 VID 或 policy_id | API-01395、API-01396、API-01399 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| steps \| 算法输入-steps邻域跳数 | API-01395、API-01397、API-01400 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| limit \| 算法输入-limit节点上限 | API-01395、API-01398、API-01401 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| nodes \| 算法输出-nodes节点 | API-01395 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| edges \| 算法输出-edges关系边 | API-01395 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| source \| 算法输出-sourcenebula／ads／镜像；space 恒 demo_gkx_chain | API-01395 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L07 \| policy.graph.main \| _fail \| 调用失败 | API-01399、API-01400、API-01401 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.intra \| op_id \| 算法输入-op_id写入算子 | API-01344、API-01349 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| scope \| 算法输入-scopeone/batch | API-01344、API-01350 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| id \| 算法输入-id政策稳定 ID | API-01345、API-01352 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.intra \| mode \| 算法输入-moderule/llm | API-01344、API-01346、API-01353 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | API-01344、API-01347、API-01354 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| filter \| 算法输入-filterbatch 过滤对象 | API-01344、API-01348、API-01355 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cite"] | API-01344、API-01351 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| written_edges \| 算法输出-written_edgescite 边 | API-01344 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.intra \| skipped \| 算法输出-skipped四码跳过 | API-01344 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.intra \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.intra \| _fail \| 调用失败 | API-01349、API-01350、API-01351、API-01352、API-01353、API-01354、API-01355 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-support \| op_id \| 算法输入-op_id必须带 op_id | API-01356、API-01362 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-support \| scope \| 算法输入-scopeone/batch | API-01356、API-01363 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-support \| id \| 算法输入-id政策稳定 ID，禁止用名称猜 VID | API-01356、API-01357、API-01364 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| mode \| 算法输入-moderule/llm | API-01356、API-01358、API-01365 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | API-01356、API-01359、API-01366 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| filter \| 算法输入-filterbatch 过滤对象 | API-01360、API-01367 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-support \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["support"] | API-01356、API-01361、API-01368 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| written_edges \| 算法输出-written_edgessupport 边 | API-01356 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-support \| skipped \| 算法输出-skipped四码跳过 | API-01356 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-support \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-support \| _fail \| 调用失败 | API-01362、API-01363、API-01364、API-01365、API-01366、API-01367、API-01368 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-apply \| op_id \| 算法输入-op_id必须带 op_id | API-01369、API-01375 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-apply \| scope \| 算法输入-scopeone/batch | API-01369、API-01376 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-apply \| id \| 算法输入-id政策稳定 ID | API-01369、API-01370、API-01377 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| mode \| 算法输入-moderule/llm | API-01369、API-01371、API-01378 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | API-01369、API-01372、API-01379 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| filter \| 算法输入-filterbatch 过滤对象 | API-01373、API-01380 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-apply \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["apply_to"] | API-01369、API-01374、API-01381 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| written_edges \| 算法输出-written_edgesapply_to 边 | API-01369 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-apply \| skipped \| 算法输出-skipped四码跳过 | API-01369 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-apply \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-apply \| _fail \| 调用失败 | API-01375、API-01376、API-01377、API-01378、API-01379、API-01380、API-01381 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-regulate \| op_id \| 算法输入-op_id必须带 op_id | API-01382、API-01388 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-regulate \| scope \| 算法输入-scopeone/batch | API-01382、API-01389 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-regulate \| id \| 算法输入-id政策稳定 ID | API-01382、API-01383、API-01390 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| mode \| 算法输入-moderule/llm | API-01382、API-01384、API-01391 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | API-01382、API-01385、API-01392 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| filter \| 算法输入-filterbatch 过滤对象 | API-01386、API-01393 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-regulate \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["regulate"] | API-01382、API-01387、API-01394 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| written_edges \| 算法输出-written_edgesregulate 边 | API-01382 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-regulate \| skipped \| 算法输出-skipped四码跳过 | API-01382 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-regulate \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-regulate \| _fail \| 调用失败 | API-01388、API-01389、API-01390、API-01391、API-01392、API-01393、API-01394 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |

---

## req_only 行（无 endpoint 挂接）

L07.md 中 `policy_entity_pipeline`（政策实体识别需规语义）为 **req_only**，无 catalog endpoint。B 线记 **无对应功能点**，不单独开 API 用例。

## 计数

- L07 挂 endpoint 的功能点 19 行（ner 11 + main 8）；req_only 1 行不进矩阵。
- L08 功能点 44 行（intra / hang-support / hang-apply / hang-regulate 各 11）。
- 矩阵 63 行。`_empty` 6 行未覆盖；其余按对应用例标已覆盖。
- 用例 69 条：主流程 6、备选 26、反向 37。

