# 服务机构实体与关系 · 功能点覆盖（svc.graph / L11+L12）

> catalog `svc.graph` · path `#/industry-service/graph`  
> A 线真源：`fp-split-by-api-run/work/L11.md`、`work/L12.md`  
> B 线用例：`FUNC-服务机构实体与关系-用例.md`（第三轮 **FUNC-00746**～**00858**）  
> 联调台：`https://edu.itic-sci.com/dma/algovwz/`（FUNC 用例在联调台执行）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.graph.ner | POST | /entan/v1/svc/graph/ner | FUNC-00746～00756 | unavailable |
| svc.graph.intra | POST | /entan/v1/svc/graph/intra | FUNC-00757～00768 | unavailable |
| svc.graph.hang-industry | POST | /entan/v1/svc/graph/hang | FUNC-00769～00781 | unavailable |
| svc.graph.hang-tech | POST | /entan/v1/svc/graph/hang | FUNC-00782～00792 | unavailable |
| svc.graph.hang-enterprise | POST | /entan/v1/svc/graph/hang | FUNC-00793～00803 | unavailable |
| svc.graph.hang-gov | POST | /entan/v1/svc/graph/hang | FUNC-00804～00814 | unavailable |
| svc.graph.hang-talent | POST | /entan/v1/svc/graph/hang | FUNC-00815～00825 | unavailable |
| svc.graph.hang-policy | POST | /entan/v1/svc/graph/hang | FUNC-00826～00836 | unavailable |
| svc.graph.hang-research | POST | /entan/v1/svc/graph/hang | FUNC-00837～00847 | unavailable |
| svc.graph.main | GET | /entan/v1/svc/graph | FUNC-00848～00856 | unavailable |

---

## 功能点 → 用例矩阵（挂 L11.md、L12.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L11 | svc.graph.ner | op_id | 算法输入-op_id写入算子 | FUNC-00746、FUNC-00751 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L11 | svc.graph.ner | scope | 算法输入-scopeone/batch | FUNC-00746、FUNC-00752 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L11 | svc.graph.ner | id | 算法输入-id机构稳定 org_id（scope=one） | FUNC-00747、FUNC-00753 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L11 | svc.graph.ner | mode | 算法输入-moderule/llm | FUNC-00746、FUNC-00748、FUNC-00754 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00746、FUNC-00749、FUNC-00755 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | filter | 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | FUNC-00746、FUNC-00750、FUNC-00756 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.ner | written_nodes | 算法输出-written_nodes写入点 | FUNC-00746 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | skipped | 算法输出-skipped四码跳过 | FUNC-00746 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | space | 算法输出-space恒 demo_gkx_chain | FUNC-00746 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.ner | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L11 | svc.graph.ner | _fail | 调用失败 | FUNC-00751、FUNC-00752、FUNC-00753、FUNC-00754、FUNC-00755、FUNC-00756 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L11 | svc.graph.main | q | 算法输入-q机构名检索 | FUNC-00848、FUNC-00849、FUNC-00853 | 已覆盖 | 主流程按 sampleRequest 传空串，备选不传该键，反向非法 |
| L11 | svc.graph.main | center | 算法输入-center中心节点 VID | FUNC-00848、FUNC-00850、FUNC-00854 | 已覆盖 | 主流程按 sampleRequest 传空串，备选不传该键，反向非法 |
| L11 | svc.graph.main | hops | 算法输入-hops邻域跳数 | FUNC-00848、FUNC-00851、FUNC-00855 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.main | limit | 算法输入-limit节点上限 | FUNC-00848、FUNC-00852、FUNC-00856 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L11 | svc.graph.main | nodes | 算法输出-nodes节点 | FUNC-00848 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | edges | 算法输出-edges关系边 | FUNC-00848 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | source | 算法输出-sourcehang／nebula／demo_gkx_chain；space 恒 demo_gkx_chain | FUNC-00848 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L11 | svc.graph.main | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L11 | svc.graph.main | _fail | 调用失败 | FUNC-00853、FUNC-00854、FUNC-00855、FUNC-00856 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.intra | op_id | 算法输入-op_id写入算子 | FUNC-00757、FUNC-00762 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | scope | 算法输入-scopeone/batch | FUNC-00757、FUNC-00763 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | id | 算法输入-id机构稳定 org_id | FUNC-00758、FUNC-00765 | 已覆盖 | sample 未带该参数；备选传入合法值，反向非法 |
| L12 | svc.graph.intra | mode | 算法输入-moderule/llm | FUNC-00757、FUNC-00759、FUNC-00766 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00757、FUNC-00760、FUNC-00767 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | filter | 算法输入-filterbatch 过滤对象 | FUNC-00757、FUNC-00761、FUNC-00768 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.intra | relation_whitelist | 算法输入-relation_whitelist白名单，高级 JSON 用 ["participates"] | FUNC-00757、FUNC-00764 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.intra | written_edges | 算法输出-written_edgesparticipates 边 | FUNC-00757 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.intra | skipped | 算法输出-skipped四码跳过 | FUNC-00757 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.intra | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.intra | _fail | 调用失败 | FUNC-00762、FUNC-00763、FUNC-00764、FUNC-00765、FUNC-00766、FUNC-00767、FUNC-00768 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-industry | op_id | 算法输入-op_id必须带 op_id | FUNC-00769、FUNC-00775 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-industry | scope | 算法输入-scopeone/batch | FUNC-00769、FUNC-00776 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-industry | id | 算法输入-id机构稳定 org_id，禁止用名称猜 VID | FUNC-00769、FUNC-00770、FUNC-00777 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | mode | 算法输入-moderule/llm | FUNC-00769、FUNC-00771、FUNC-00778 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00769、FUNC-00772、FUNC-00779 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | filter | 算法输入-filterbatch 过滤对象 | FUNC-00769、FUNC-00773、FUNC-00780 | 已覆盖 | 主流程在 sampleRequest 外补 filter={all:true}，备选不传，反向非法 |
| L12 | svc.graph.hang-industry | dest_types | 算法输入-dest_types终点白名单 | FUNC-00769、FUNC-00774、FUNC-00781 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-industry | skipped | 算法输出-skipped四码跳过 | FUNC-00769 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-industry | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-industry | _fail | 调用失败 | FUNC-00775、FUNC-00776、FUNC-00777、FUNC-00778、FUNC-00779、FUNC-00780、FUNC-00781 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-tech | op_id | 算法输入-op_id必须带 op_id | FUNC-00782、FUNC-00787 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-tech | scope | 算法输入-scopeone/batch | FUNC-00782、FUNC-00788 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-tech | id | 算法输入-id机构稳定 org_id | FUNC-00782、FUNC-00783、FUNC-00789 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | mode | 算法输入-moderule/llm | FUNC-00782、FUNC-00784、FUNC-00790 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00782、FUNC-00785、FUNC-00791 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | dest_types | 算法输入-dest_types终点白名单 | FUNC-00782、FUNC-00786、FUNC-00792 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-tech | skipped | 算法输出-skipped四码跳过 | FUNC-00782 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-tech | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-tech | _fail | 调用失败 | FUNC-00787、FUNC-00788、FUNC-00789、FUNC-00790、FUNC-00791、FUNC-00792 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-enterprise | op_id | 算法输入-op_id必须带 op_id | FUNC-00793、FUNC-00798 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-enterprise | scope | 算法输入-scopeone/batch | FUNC-00793、FUNC-00799 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-enterprise | id | 算法输入-id机构稳定 org_id | FUNC-00793、FUNC-00794、FUNC-00800 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | mode | 算法输入-moderule/llm | FUNC-00793、FUNC-00795、FUNC-00801 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00793、FUNC-00796、FUNC-00802 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | dest_types | 算法输入-dest_types终点白名单 | FUNC-00793、FUNC-00797、FUNC-00803 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-enterprise | skipped | 算法输出-skipped四码跳过 | FUNC-00793 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-enterprise | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-enterprise | _fail | 调用失败 | FUNC-00798、FUNC-00799、FUNC-00800、FUNC-00801、FUNC-00802、FUNC-00803 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-gov | op_id | 算法输入-op_id必须带 op_id | FUNC-00804、FUNC-00809 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-gov | scope | 算法输入-scopeone/batch | FUNC-00804、FUNC-00810 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-gov | id | 算法输入-id机构稳定 org_id | FUNC-00804、FUNC-00805、FUNC-00811 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | mode | 算法输入-moderule/llm | FUNC-00804、FUNC-00806、FUNC-00812 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00804、FUNC-00807、FUNC-00813 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | dest_types | 算法输入-dest_types终点白名单 | FUNC-00804、FUNC-00808、FUNC-00814 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-gov | skipped | 算法输出-skipped四码跳过 | FUNC-00804 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-gov | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-gov | _fail | 调用失败 | FUNC-00809、FUNC-00810、FUNC-00811、FUNC-00812、FUNC-00813、FUNC-00814 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-talent | op_id | 算法输入-op_id必须带 op_id | FUNC-00815、FUNC-00820 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-talent | scope | 算法输入-scopeone/batch | FUNC-00815、FUNC-00821 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-talent | id | 算法输入-id机构稳定 org_id | FUNC-00815、FUNC-00816、FUNC-00822 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | mode | 算法输入-moderule/llm | FUNC-00815、FUNC-00817、FUNC-00823 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00815、FUNC-00818、FUNC-00824 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | dest_types | 算法输入-dest_types终点白名单 | FUNC-00815、FUNC-00819、FUNC-00825 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-talent | skipped | 算法输出-skipped四码跳过 | FUNC-00815 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-talent | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-talent | _fail | 调用失败 | FUNC-00820、FUNC-00821、FUNC-00822、FUNC-00823、FUNC-00824、FUNC-00825 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-policy | op_id | 算法输入-op_id必须带 op_id | FUNC-00826、FUNC-00831 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-policy | scope | 算法输入-scopeone/batch | FUNC-00826、FUNC-00832 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-policy | id | 算法输入-id机构稳定 org_id | FUNC-00826、FUNC-00827、FUNC-00833 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | mode | 算法输入-moderule/llm | FUNC-00826、FUNC-00828、FUNC-00834 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00826、FUNC-00829、FUNC-00835 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | dest_types | 算法输入-dest_types终点白名单 | FUNC-00826、FUNC-00830、FUNC-00836 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-policy | skipped | 算法输出-skipped四码跳过 | FUNC-00826 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-policy | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-policy | _fail | 调用失败 | FUNC-00831、FUNC-00832、FUNC-00833、FUNC-00834、FUNC-00835、FUNC-00836 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |
| L12 | svc.graph.hang-research | op_id | 算法输入-op_id必须带 op_id | FUNC-00837、FUNC-00842 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-research | scope | 算法输入-scopeone/batch | FUNC-00837、FUNC-00843 | 已覆盖 | 必填：主流程传入，反向缺省 |
| L12 | svc.graph.hang-research | id | 算法输入-id机构稳定 org_id | FUNC-00837、FUNC-00838、FUNC-00844 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | mode | 算法输入-moderule/llm | FUNC-00837、FUNC-00839、FUNC-00845 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | dry_run | 算法输入-dry_run不写 ADS/Nebula | FUNC-00837、FUNC-00840、FUNC-00846 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | dest_types | 算法输入-dest_types终点白名单 | FUNC-00837、FUNC-00841、FUNC-00847 | 已覆盖 | 主流程按 sample 传入，备选省略，反向非法 |
| L12 | svc.graph.hang-research | skipped | 算法输出-skipped四码跳过 | FUNC-00837 | 已覆盖 | 主流程按 sampleResponse 与 responseFields 断言 |
| L12 | svc.graph.hang-research | _empty | 查询无数据空态 | — | 未覆盖 | 无稳定空结果构造条件 |
| L12 | svc.graph.hang-research | _fail | 调用失败 | FUNC-00842、FUNC-00843、FUNC-00844、FUNC-00845、FUNC-00846、FUNC-00847 | 已覆盖 | 各参数反向，message 或 msg 指出该参数 |

---

## 计数

- A 线行：L11 **20** + L12 **75** = **95**
- 已覆盖 **85**；部分覆盖 **0**；未覆盖 **10**（均为 `_empty`，无稳定空结果构造条件）
- 本页 10 个 endpoint 均在 L11 或 L12 出现，无 B 线独有接口
