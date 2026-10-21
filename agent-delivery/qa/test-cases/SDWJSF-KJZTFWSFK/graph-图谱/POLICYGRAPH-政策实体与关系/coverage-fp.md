# 政策实体与关系 · 功能点覆盖（policy.graph / L07+L08）

> catalog `policy.graph` · path `#/policy/graph`  
> A 线真源：`fp-split-by-api-run/work/L07.md`、`work/L08.md`  
> B 线用例：`FUNC-政策实体与关系-用例.md`（第二轮 **FUNC-00531**～**01401**）  
> 联调台 https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.graph.ner | POST | /policy/v1/policy/graph/ner | FUNC-00531～01343 | unavailable |
| policy.graph.intra | POST | /policy/v1/policy/graph/intra | FUNC-00542～01355 | unavailable |
| policy.graph.hang-support | POST | /policy/v1/policy/graph/hang | FUNC-00554～01368 | unavailable |
| policy.graph.hang-apply | POST | /policy/v1/policy/graph/hang | FUNC-00567～01381 | unavailable |
| policy.graph.hang-regulate | POST | /policy/v1/policy/graph/hang | FUNC-00580～01394 | unavailable |
| policy.graph.main | GET | /policy/v1/policy/graph | FUNC-00593～01401 | unavailable |

---

## 功能点 → 用例矩阵（挂 L07.md、L08.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L07 \| policy.graph.ner \| op_id \| 算法输入-op_id写入算子 | FUNC-00531、FUNC-00536 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L07 \| policy.graph.ner \| scope \| 算法输入-scopeone/batch | FUNC-00531、FUNC-00537 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L07 \| policy.graph.ner \| id \| 算法输入-id政策稳定 ID（scope=one） | FUNC-00531、FUNC-00532、FUNC-00538 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| mode \| 算法输入-moderule/llm | FUNC-00531、FUNC-00533、FUNC-00539 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | FUNC-00531、FUNC-00534、FUNC-00540 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.ner \| filter \| 算法输入-filterscope=batch 过滤对象，高级 JSON 保持 {all:true} | FUNC-00535、FUNC-00541 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L07 \| policy.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | FUNC-00531 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| skipped \| 算法输出-skipped四码跳过 | FUNC-00531 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | FUNC-00531 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.ner \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L07 \| policy.graph.ner \| _fail \| 调用失败 | FUNC-00536、FUNC-00537、FUNC-00538、FUNC-00539、FUNC-00540、FUNC-00541 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L07 \| policy.graph.main \| center \| 算法输入-center中心节点 VID 或 policy_id | FUNC-00593、FUNC-00594、FUNC-00597 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| steps \| 算法输入-steps邻域跳数 | FUNC-00593、FUNC-00595、FUNC-00598 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| limit \| 算法输入-limit节点上限 | FUNC-00593、FUNC-00596、FUNC-00599 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L07 \| policy.graph.main \| nodes \| 算法输出-nodes节点 | FUNC-00593 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| edges \| 算法输出-edges关系边 | FUNC-00593 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| source \| 算法输出-sourcenebula／ads／镜像；space 恒 demo_gkx_chain | FUNC-00593 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L07 \| policy.graph.main \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L07 \| policy.graph.main \| _fail \| 调用失败 | FUNC-00597、FUNC-00598、FUNC-00599 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.intra \| op_id \| 算法输入-op_id写入算子 | FUNC-00542、FUNC-00547 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| scope \| 算法输入-scopeone/batch | FUNC-00542、FUNC-00548 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| id \| 算法输入-id政策稳定 ID | FUNC-00543、FUNC-00550 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.intra \| mode \| 算法输入-moderule/llm | FUNC-00542、FUNC-00544、FUNC-00551 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | FUNC-00542、FUNC-00545、FUNC-00552 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| filter \| 算法输入-filterbatch 过滤对象 | FUNC-00542、FUNC-00546、FUNC-00553 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.intra \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cite"] | FUNC-00542、FUNC-00549 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.intra \| written_edges \| 算法输出-written_edgescite 边 | FUNC-00542 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.intra \| skipped \| 算法输出-skipped四码跳过 | FUNC-00542 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.intra \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.intra \| _fail \| 调用失败 | FUNC-00547、FUNC-00548、FUNC-00549、FUNC-00550、FUNC-00551、FUNC-00552、FUNC-00553 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-support \| op_id \| 算法输入-op_id必须带 op_id | FUNC-00554、FUNC-00560 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-support \| scope \| 算法输入-scopeone/batch | FUNC-00554、FUNC-00561 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-support \| id \| 算法输入-id政策稳定 ID，禁止用名称猜 VID | FUNC-00554、FUNC-00555、FUNC-00562 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| mode \| 算法输入-moderule/llm | FUNC-00554、FUNC-00556、FUNC-00563 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | FUNC-00554、FUNC-00557、FUNC-00564 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| filter \| 算法输入-filterbatch 过滤对象 | FUNC-00558、FUNC-00565 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-support \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["support"] | FUNC-00554、FUNC-00559、FUNC-00566 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-support \| written_edges \| 算法输出-written_edgessupport 边 | FUNC-00554 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-support \| skipped \| 算法输出-skipped四码跳过 | FUNC-00554 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-support \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-support \| _fail \| 调用失败 | FUNC-00560、FUNC-00561、FUNC-00562、FUNC-00563、FUNC-00564、FUNC-00565、FUNC-00566 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-apply \| op_id \| 算法输入-op_id必须带 op_id | FUNC-00567、FUNC-00573 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-apply \| scope \| 算法输入-scopeone/batch | FUNC-00567、FUNC-00574 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-apply \| id \| 算法输入-id政策稳定 ID | FUNC-00567、FUNC-00568、FUNC-00575 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| mode \| 算法输入-moderule/llm | FUNC-00567、FUNC-00569、FUNC-00576 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | FUNC-00567、FUNC-00570、FUNC-00577 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| filter \| 算法输入-filterbatch 过滤对象 | FUNC-00571、FUNC-00578 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-apply \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["apply_to"] | FUNC-00567、FUNC-00572、FUNC-00579 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-apply \| written_edges \| 算法输出-written_edgesapply_to 边 | FUNC-00567 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-apply \| skipped \| 算法输出-skipped四码跳过 | FUNC-00567 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-apply \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-apply \| _fail \| 调用失败 | FUNC-00573、FUNC-00574、FUNC-00575、FUNC-00576、FUNC-00577、FUNC-00578、FUNC-00579 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L08 \| policy.graph.hang-regulate \| op_id \| 算法输入-op_id必须带 op_id | FUNC-00580、FUNC-00586 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-regulate \| scope \| 算法输入-scopeone/batch | FUNC-00580、FUNC-00587 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L08 \| policy.graph.hang-regulate \| id \| 算法输入-id政策稳定 ID | FUNC-00580、FUNC-00581、FUNC-00588 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| mode \| 算法输入-moderule/llm | FUNC-00580、FUNC-00582、FUNC-00589 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | FUNC-00580、FUNC-00583、FUNC-00590 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| filter \| 算法输入-filterbatch 过滤对象 | FUNC-00584、FUNC-00591 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L08 \| policy.graph.hang-regulate \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["regulate"] | FUNC-00580、FUNC-00585、FUNC-00592 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L08 \| policy.graph.hang-regulate \| written_edges \| 算法输出-written_edgesregulate 边 | FUNC-00580 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-regulate \| skipped \| 算法输出-skipped四码跳过 | FUNC-00580 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L08 \| policy.graph.hang-regulate \| _empty \| 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L08 \| policy.graph.hang-regulate \| _fail \| 调用失败 | FUNC-00586、FUNC-00587、FUNC-00588、FUNC-00589、FUNC-00590、FUNC-00591、FUNC-00592 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |

---

## req_only 行（无 endpoint 挂接）

L07.md 中 `policy_entity_pipeline`（政策实体识别需规语义）为 **req_only**，无 catalog endpoint。B 线记 **无对应功能点**，不单独开 FUNC 用例。

## 计数

- L07 挂 endpoint 的功能点 19 行（ner 11 + main 8）；req_only 1 行不进矩阵。
- L08 功能点 44 行（intra / hang-support / hang-apply / hang-regulate 各 11）。
- 矩阵 63 行。`_empty` 6 行未覆盖；其余按对应用例标已覆盖。
- 用例 71 条（FUNC-00531～00601）：接口调用 69（主流程 6、备选 26、反向 37）+ 清单 2。

