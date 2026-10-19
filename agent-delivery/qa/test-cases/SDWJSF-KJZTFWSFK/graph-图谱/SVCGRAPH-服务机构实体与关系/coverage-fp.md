# 服务机构实体与关系 · 功能点覆盖（svc.graph / L11+L12）

> catalog `svc.graph` · path `#/industry-service/graph`  
> A 线真源：`fp-split-by-api-run/work/L11.md`、`work/L12.md`  
> B 线用例：`API-服务机构实体与关系-用例.md`（第二轮 **API-01536**～**01646**）  
> 联调台端口 50897（本册不打开页面）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.graph.ner | POST | /entan/v1/svc/graph/ner | API-01536～API-01546 | unavailable |
| svc.graph.intra | POST | /entan/v1/svc/graph/intra | API-01547～API-01558 | unavailable |
| svc.graph.hang-industry | POST | /entan/v1/svc/graph/hang | API-01559～API-01571 | unavailable |
| svc.graph.hang-tech | POST | /entan/v1/svc/graph/hang | API-01572～API-01582 | unavailable |
| svc.graph.hang-enterprise | POST | /entan/v1/svc/graph/hang | API-01583～API-01593 | unavailable |
| svc.graph.hang-gov | POST | /entan/v1/svc/graph/hang | API-01594～API-01604 | unavailable |
| svc.graph.hang-talent | POST | /entan/v1/svc/graph/hang | API-01605～API-01615 | unavailable |
| svc.graph.hang-policy | POST | /entan/v1/svc/graph/hang | API-01616～API-01626 | unavailable |
| svc.graph.hang-research | POST | /entan/v1/svc/graph/hang | API-01627～API-01637 | unavailable |
| svc.graph.main | GET | /entan/v1/svc/graph | API-01638～API-01646 | unavailable |

---

## 功能点 → 用例矩阵（挂 L11.md、L12.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L11 | svc.graph.ner | op_id | 算法输入-op_id写入算子 | API-01536、API-01541 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L11 | svc.graph.ner | scope | 算法输入-scopeone/batch | API-01536、API-01542 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L11 | svc.graph.ner | id | 算法输入-id机构稳定 org_id（scope=one） | API-01537、API-01543 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L11 | svc.graph.ner | mode | 算法输入-moderule/llm | API-01536、API-01538、API-01544 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01536、API-01539、API-01545 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | filter | 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | API-01536、API-01540、API-01546 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | written_nodes | 算法输出-written_nodes写入点 | API-01536 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | skipped | 算法输出-skipped四码跳过 | API-01536 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | space | 算法输出-space恒 demo_gkx_chain | API-01536 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L11 | svc.graph.ner | _fail | 调用失败 | API-01541、API-01542、API-01543、API-01544、API-01545、API-01546 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L11 | svc.graph.main | q | 算法输入-q机构名检索 | API-01638、API-01639、API-01643 | 已覆盖 | 主流程按 sampleRequest 传空串，备选不传该键，反向非法 |
| L11 | svc.graph.main | center | 算法输入-center中心节点 VID | API-01638、API-01640、API-01644 | 已覆盖 | 主流程按 sampleRequest 传空串，备选不传该键，反向非法 |
| L11 | svc.graph.main | hops | 算法输入-hops邻域跳数 | API-01638、API-01641、API-01645 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.main | limit | 算法输入-limit节点上限 | API-01638、API-01642、API-01646 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.main | nodes | 算法输出-nodes节点 | API-01638 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | edges | 算法输出-edges关系边 | API-01638 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | source | 算法输出-sourcehang／nebula／demo_gkx_chain；space 恒 demo_gkx_chain | API-01638 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L11 | svc.graph.main | _fail | 调用失败 | API-01643、API-01644、API-01645、API-01646 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.intra | op_id | 算法输入-op_id写入算子 | API-01547、API-01552 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | scope | 算法输入-scopeone/batch | API-01547、API-01553 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | id | 算法输入-id机构稳定 org_id | API-01548、API-01555 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L12 | svc.graph.intra | mode | 算法输入-moderule/llm | API-01547、API-01549、API-01556 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01547、API-01550、API-01557 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | filter | 算法输入-filterbatch 过滤对象 | API-01547、API-01551、API-01558 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | relation_whitelist | 算法输入-relation_whitelist白名单，高级 JSON 用 ["participates"] | API-01547、API-01554 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | written_edges | 算法输出-written_edgesparticipates 边 | API-01547 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.intra | skipped | 算法输出-skipped四码跳过 | API-01547 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.intra | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.intra | _fail | 调用失败 | API-01552、API-01553、API-01554、API-01555、API-01556、API-01557、API-01558 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-industry | op_id | 算法输入-op_id必须带 op_id | API-01559、API-01565 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-industry | scope | 算法输入-scopeone/batch | API-01559、API-01566 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-industry | id | 算法输入-id机构稳定 org_id，禁止用名称猜 VID | API-01559、API-01560、API-01567 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | mode | 算法输入-moderule/llm | API-01559、API-01561、API-01568 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01559、API-01562、API-01569 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | filter | 算法输入-filterbatch 过滤对象 | API-01559、API-01563、API-01570 | 已覆盖 | 主流程在 sampleRequest 外补 filter={all:true}，备选不传，反向非法 |
| L12 | svc.graph.hang-industry | dest_types | 算法输入-dest_types终点白名单 | API-01559、API-01564、API-01571 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | skipped | 算法输出-skipped四码跳过 | API-01559 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-industry | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-industry | _fail | 调用失败 | API-01565、API-01566、API-01567、API-01568、API-01569、API-01570、API-01571 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-tech | op_id | 算法输入-op_id必须带 op_id | API-01572、API-01577 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-tech | scope | 算法输入-scopeone/batch | API-01572、API-01578 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-tech | id | 算法输入-id机构稳定 org_id | API-01572、API-01573、API-01579 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | mode | 算法输入-moderule/llm | API-01572、API-01574、API-01580 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01572、API-01575、API-01581 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | dest_types | 算法输入-dest_types终点白名单 | API-01572、API-01576、API-01582 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | skipped | 算法输出-skipped四码跳过 | API-01572 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-tech | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-tech | _fail | 调用失败 | API-01577、API-01578、API-01579、API-01580、API-01581、API-01582 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-enterprise | op_id | 算法输入-op_id必须带 op_id | API-01583、API-01588 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-enterprise | scope | 算法输入-scopeone/batch | API-01583、API-01589 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-enterprise | id | 算法输入-id机构稳定 org_id | API-01583、API-01584、API-01590 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | mode | 算法输入-moderule/llm | API-01583、API-01585、API-01591 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01583、API-01586、API-01592 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | dest_types | 算法输入-dest_types终点白名单 | API-01583、API-01587、API-01593 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | skipped | 算法输出-skipped四码跳过 | API-01583 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-enterprise | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-enterprise | _fail | 调用失败 | API-01588、API-01589、API-01590、API-01591、API-01592、API-01593 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-gov | op_id | 算法输入-op_id必须带 op_id | API-01594、API-01599 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-gov | scope | 算法输入-scopeone/batch | API-01594、API-01600 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-gov | id | 算法输入-id机构稳定 org_id | API-01594、API-01595、API-01601 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | mode | 算法输入-moderule/llm | API-01594、API-01596、API-01602 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01594、API-01597、API-01603 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | dest_types | 算法输入-dest_types终点白名单 | API-01594、API-01598、API-01604 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | skipped | 算法输出-skipped四码跳过 | API-01594 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-gov | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-gov | _fail | 调用失败 | API-01599、API-01600、API-01601、API-01602、API-01603、API-01604 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-talent | op_id | 算法输入-op_id必须带 op_id | API-01605、API-01610 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-talent | scope | 算法输入-scopeone/batch | API-01605、API-01611 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-talent | id | 算法输入-id机构稳定 org_id | API-01605、API-01606、API-01612 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | mode | 算法输入-moderule/llm | API-01605、API-01607、API-01613 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01605、API-01608、API-01614 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | dest_types | 算法输入-dest_types终点白名单 | API-01605、API-01609、API-01615 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | skipped | 算法输出-skipped四码跳过 | API-01605 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-talent | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-talent | _fail | 调用失败 | API-01610、API-01611、API-01612、API-01613、API-01614、API-01615 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-policy | op_id | 算法输入-op_id必须带 op_id | API-01616、API-01621 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-policy | scope | 算法输入-scopeone/batch | API-01616、API-01622 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-policy | id | 算法输入-id机构稳定 org_id | API-01616、API-01617、API-01623 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | mode | 算法输入-moderule/llm | API-01616、API-01618、API-01624 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01616、API-01619、API-01625 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | dest_types | 算法输入-dest_types终点白名单 | API-01616、API-01620、API-01626 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | skipped | 算法输出-skipped四码跳过 | API-01616 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-policy | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-policy | _fail | 调用失败 | API-01621、API-01622、API-01623、API-01624、API-01625、API-01626 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-research | op_id | 算法输入-op_id必须带 op_id | API-01627、API-01632 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-research | scope | 算法输入-scopeone/batch | API-01627、API-01633 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-research | id | 算法输入-id机构稳定 org_id | API-01627、API-01628、API-01634 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | mode | 算法输入-moderule/llm | API-01627、API-01629、API-01635 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | dry_run | 算法输入-dry_run不写 ADS/Nebula | API-01627、API-01630、API-01636 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | dest_types | 算法输入-dest_types终点白名单 | API-01627、API-01631、API-01637 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | skipped | 算法输出-skipped四码跳过 | API-01627 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-research | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-research | _fail | 调用失败 | API-01632、API-01633、API-01634、API-01635、API-01636、API-01637 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |

---

## 计数

- A 线行：L11 **20** + L12 **75** = **95**
- 已覆盖 **85**；部分覆盖 **0**；未覆盖 **10**（均为 `_empty`，无稳定空结果构造条件）
- 本页 10 个 endpoint 均在 L11 或 L12 出现，无 B 线独有接口
