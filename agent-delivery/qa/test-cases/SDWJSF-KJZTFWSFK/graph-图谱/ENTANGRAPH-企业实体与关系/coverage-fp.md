# 企业实体与关系 · 功能点覆盖（entan.graph / L09+L10）

> catalog `entan.graph` · path `/entan/graph` · 调试台文档页 50897（不作为用例步骤）  
> **用例册**：`API-企业实体与关系-用例.md`（第二轮 **API-00990**～**API-01133**，共 **144** 条）  
> A 线真源：`fp-split-by-api-run/work/L09.md`（20 行，ner/main）与 `L10.md`（130 行，intra/hang）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`。多个 field 可挂同一 API 编号。  
> 12 个接口 catalog `status=unavailable`，用例仍按文档请求/返回编写。`_empty` 无稳定必空入参，记未覆盖，不单开空态用例。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.graph.ner | POST | /entan/v1/entan/graph/ner | API-00990～01000 | unavailable |
| entan.graph.intra-coop | POST | /entan/v1/entan/graph/intra | API-01001～01012 | unavailable |
| entan.graph.intra-invest | POST | /entan/v1/entan/graph/intra | API-01013～01024 | unavailable |
| entan.graph.intra-belong | POST | /entan/v1/entan/graph/intra | API-01025～01036 | unavailable |
| entan.graph.intra-supply | POST | /entan/v1/entan/graph/intra | API-01037～01048 | unavailable |
| entan.graph.hang-industry | POST | /entan/v1/entan/graph/hang | API-01049～01061 | unavailable |
| entan.graph.hang-tech | POST | /entan/v1/entan/graph/hang | API-01062～01074 | unavailable |
| entan.graph.hang-talent | POST | /entan/v1/entan/graph/hang | API-01075～01087 | unavailable |
| entan.graph.hang-policy | POST | /entan/v1/entan/graph/hang | API-01088～01100 | unavailable |
| entan.graph.hang-research | POST | /entan/v1/entan/graph/hang | API-01101～01113 | unavailable |
| entan.graph.hang-service | POST | /entan/v1/entan/graph/hang | API-01114～01126 | unavailable |
| entan.graph.main | GET | /entan/v1/entan/graph | API-01127～01133 | unavailable |

---

## 功能点 → 用例矩阵（挂 L09.md 与 L10.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L09 \| entan.graph.ner \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-00990、00995 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L09 \| entan.graph.ner \| scope \| 算法输入-scopeone/batch | catalog scope | API-00990、00996 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L09 \| entan.graph.ner \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-00990、00991、00997 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| mode \| 算法输入-moderule/llm | catalog mode | API-00990、00992、00998 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-00990、00993、00999 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-00990、00994、01000 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-00990 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-00990 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-00990 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-00990 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L09 \| entan.graph.ner \| _fail \| 调用失败 | 契约错误态 | API-00995、00996、00997、00998、00999、01000 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L09 \| entan.graph.main \| center \| 算法输入-center中心 org_id 或 ent: VID | catalog center | API-01127、01128、01131 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| hops \| 算法输入-hops邻域跳数 | catalog hops | API-01127、01129、01132 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| limit \| 算法输入-limit节点上限 | catalog limit | API-01127、01130、01133 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| nodes \| 算法输出-nodes节点 | catalog nodes | API-01127 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| edges \| 算法输出-edges关系边 | catalog edges | API-01127 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| source \| 算法输出-sourcenebula／pg；space 恒 demo_gkx_chain | catalog source | API-01127 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L09 \| entan.graph.main \| _fail \| 调用失败 | 契约错误态 | API-01131、01132、01133 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-coop \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01001、01006 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| scope \| 算法输入-scopeone/batch | catalog scope | API-01001、01007 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01001、01002、01009 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| mode \| 算法输入-moderule/llm | catalog mode | API-01001、01003、01010 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01001、01004、01011 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01001、01005、01012 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cooperate"] | catalog relation_whitelist | API-01001、01008 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01001 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01001 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01001 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01001 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-coop \| _fail \| 调用失败 | 契约错误态 | API-01006、01007、01008、01009、01010、01011、01012 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-invest \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01013、01018 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| scope \| 算法输入-scopeone/batch | catalog scope | API-01013、01019 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01013、01014、01021 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| mode \| 算法输入-moderule/llm | catalog mode | API-01013、01015、01022 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01013、01016、01023 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01013、01017、01024 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["invest"] | catalog relation_whitelist | API-01013、01020 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01013 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01013 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01013 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01013 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-invest \| _fail \| 调用失败 | 契约错误态 | API-01018、01019、01020、01021、01022、01023、01024 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-belong \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01025、01030 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| scope \| 算法输入-scopeone/batch | catalog scope | API-01025、01031 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01025、01026、01033 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| mode \| 算法输入-moderule/llm | catalog mode | API-01025、01027、01034 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01025、01028、01035 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01025、01029、01036 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["parent_sub"] | catalog relation_whitelist | API-01025、01032 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01025 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01025 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01025 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01025 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-belong \| _fail \| 调用失败 | 契约错误态 | API-01030、01031、01032、01033、01034、01035、01036 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-supply \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01037、01042 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| scope \| 算法输入-scopeone/batch | catalog scope | API-01037、01043 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01037、01038、01045 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| mode \| 算法输入-moderule/llm | catalog mode | API-01037、01039、01046 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01037、01040、01047 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01037、01041、01048 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["supply"] | catalog relation_whitelist | API-01037、01044 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01037 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01037 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01037 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01037 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-supply \| _fail \| 调用失败 | 契约错误态 | API-01042、01043、01044、01045、01046、01047、01048 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-industry \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01049、01055 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| scope \| 算法输入-scopeone/batch | catalog scope | API-01049、01056 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01049、01050、01057 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| mode \| 算法输入-moderule/llm | catalog mode | API-01049、01051、01058 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01049、01052、01059 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01049、01053、01060 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["industry"] | catalog dest_types | API-01049、01054、01061 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01049 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01049 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01049 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01049 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-industry \| _fail \| 调用失败 | 契约错误态 | API-01055、01056、01057、01058、01059、01060、01061 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-tech \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01062、01068 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| scope \| 算法输入-scopeone/batch | catalog scope | API-01062、01069 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01062、01063、01070 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| mode \| 算法输入-moderule/llm | catalog mode | API-01062、01064、01071 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01062、01065、01072 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01062、01066、01073 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["technology"] | catalog dest_types | API-01062、01067、01074 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01062 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01062 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01062 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01062 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-tech \| _fail \| 调用失败 | 契约错误态 | API-01068、01069、01070、01071、01072、01073、01074 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-talent \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01075、01081 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| scope \| 算法输入-scopeone/batch | catalog scope | API-01075、01082 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01075、01076、01083 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| mode \| 算法输入-moderule/llm | catalog mode | API-01075、01077、01084 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01075、01078、01085 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01075、01079、01086 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["talent"] | catalog dest_types | API-01075、01080、01087 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01075 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01075 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01075 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01075 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-talent \| _fail \| 调用失败 | 契约错误态 | API-01081、01082、01083、01084、01085、01086、01087 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-policy \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01088、01094 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| scope \| 算法输入-scopeone/batch | catalog scope | API-01088、01095 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01088、01089、01096 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| mode \| 算法输入-moderule/llm | catalog mode | API-01088、01090、01097 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01088、01091、01098 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01088、01092、01099 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["policy"] | catalog dest_types | API-01088、01093、01100 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01088 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01088 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01088 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01088 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-policy \| _fail \| 调用失败 | 契约错误态 | API-01094、01095、01096、01097、01098、01099、01100 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-research \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01101、01107 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| scope \| 算法输入-scopeone/batch | catalog scope | API-01101、01108 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01101、01102、01109 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| mode \| 算法输入-moderule/llm | catalog mode | API-01101、01103、01110 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01101、01104、01111 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01101、01105、01112 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["research"] | catalog dest_types | API-01101、01106、01113 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01101 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01101 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01101 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01101 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-research \| _fail \| 调用失败 | 契约错误态 | API-01107、01108、01109、01110、01111、01112、01113 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-service \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-01114、01120 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| scope \| 算法输入-scopeone/batch | catalog scope | API-01114、01121 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | API-01114、01115、01122 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| mode \| 算法输入-moderule/llm | catalog mode | API-01114、01116、01123 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-01114、01117、01124 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | API-01114、01118、01125 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["service"] | catalog dest_types | API-01114、01119、01126 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-01114 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | API-01114 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-01114 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-01114 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-service \| _fail \| 调用失败 | 契约错误态 | API-01120、01121、01122、01123、01124、01125、01126 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |

---

## 计数

- L09 行 **20**、L10 行 **130**，矩阵 **150** 行，均有 endpoint，无 req_only。
- 状态：已覆盖 **138**、部分覆盖 **0**、未覆盖 **12**（未覆盖均为 `_empty`）。
- 输出字段挂该接口主流程编号；入参字段另挂该参数的省略或反向编号。

