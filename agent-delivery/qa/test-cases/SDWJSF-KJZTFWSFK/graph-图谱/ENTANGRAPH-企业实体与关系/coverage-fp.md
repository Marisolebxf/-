# 企业实体与关系 · 功能点覆盖（entan.graph / L09+L10）

> catalog `entan.graph` · path `/entan/graph` · 联调台 `https://edu.itic-sci.com/dma/algovwz/`（步骤不写 50897）  
> **用例册**：`FUNC-企业实体与关系-用例.md`（第三轮 **FUNC-00163**～**FUNC-00308**，共 **146** 条，含清单 00307、00308）
> A 线真源：`fp-split-by-api-run/work/L09.md`（20 行，ner/main）与 `L10.md`（130 行，intra/hang）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`。多个 field 可挂同一 FUNC 编号。  
> 12 个接口 catalog `status=unavailable`，用例仍按文档请求/返回编写。`_empty` 无稳定必空入参，记未覆盖，不单开空态用例。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.graph.ner | POST | /entan/v1/entan/graph/ner | FUNC-00163～00173 | unavailable |
| entan.graph.intra-coop | POST | /entan/v1/entan/graph/intra | FUNC-00174～00185 | unavailable |
| entan.graph.intra-invest | POST | /entan/v1/entan/graph/intra | FUNC-00186～00197 | unavailable |
| entan.graph.intra-belong | POST | /entan/v1/entan/graph/intra | FUNC-00198～00209 | unavailable |
| entan.graph.intra-supply | POST | /entan/v1/entan/graph/intra | FUNC-00210～00221 | unavailable |
| entan.graph.hang-industry | POST | /entan/v1/entan/graph/hang | FUNC-00222～00234 | unavailable |
| entan.graph.hang-tech | POST | /entan/v1/entan/graph/hang | FUNC-00235～00247 | unavailable |
| entan.graph.hang-talent | POST | /entan/v1/entan/graph/hang | FUNC-00248～00260 | unavailable |
| entan.graph.hang-policy | POST | /entan/v1/entan/graph/hang | FUNC-00261～00273 | unavailable |
| entan.graph.hang-research | POST | /entan/v1/entan/graph/hang | FUNC-00274～00286 | unavailable |
| entan.graph.hang-service | POST | /entan/v1/entan/graph/hang | FUNC-00287～00299 | unavailable |
| entan.graph.main | GET | /entan/v1/entan/graph | FUNC-00300～00306 | unavailable |
| （页面清单） | — | — | FUNC-00307、00308 | — |

---

## 功能点 → 用例矩阵（挂 L09.md 与 L10.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L09 \| entan.graph.ner \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00163、FUNC-00168 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L09 \| entan.graph.ner \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00163、FUNC-00169 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L09 \| entan.graph.ner \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00163、FUNC-00164、FUNC-00170 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00163、FUNC-00165、FUNC-00171 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00163、FUNC-00166、FUNC-00172 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00163、FUNC-00167、FUNC-00173 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00163 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00163 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00163 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00163 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.ner \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L09 \| entan.graph.ner \| _fail \| 调用失败 | 契约错误态 | FUNC-00168、FUNC-00169、FUNC-00170、FUNC-00171、FUNC-00172、FUNC-00173 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L09 \| entan.graph.main \| center \| 算法输入-center中心 org_id 或 ent: VID | catalog center | FUNC-00300、FUNC-00301、FUNC-00304 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| hops \| 算法输入-hops邻域跳数 | catalog hops | FUNC-00300、FUNC-00302、FUNC-00305 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| limit \| 算法输入-limit节点上限 | catalog limit | FUNC-00300、FUNC-00303、FUNC-00306 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L09 \| entan.graph.main \| nodes \| 算法输出-nodes节点 | catalog nodes | FUNC-00300 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| edges \| 算法输出-edges关系边 | catalog edges | FUNC-00300 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| source \| 算法输出-sourcenebula／pg；space 恒 demo_gkx_chain | catalog source | FUNC-00300 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L09 \| entan.graph.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L09 \| entan.graph.main \| _fail \| 调用失败 | 契约错误态 | FUNC-00304、FUNC-00305、FUNC-00306 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-coop \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00174、FUNC-00179 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00174、FUNC-00180 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00174、FUNC-00175、FUNC-00182 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00174、FUNC-00176、FUNC-00183 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00174、FUNC-00177、FUNC-00184 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00174、FUNC-00178、FUNC-00185 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cooperate"] | catalog relation_whitelist | FUNC-00174、FUNC-00181 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00174 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00174 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00174 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00174 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-coop \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-coop \| _fail \| 调用失败 | 契约错误态 | FUNC-00179、FUNC-00180、FUNC-00181、FUNC-00182、FUNC-00183、FUNC-00184、FUNC-00185 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-invest \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00186、FUNC-00191 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00186、FUNC-00192 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00186、FUNC-00187、FUNC-00194 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00186、FUNC-00188、FUNC-00195 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00186、FUNC-00189、FUNC-00196 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00186、FUNC-00190、FUNC-00197 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["invest"] | catalog relation_whitelist | FUNC-00186、FUNC-00193 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00186 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00186 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00186 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00186 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-invest \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-invest \| _fail \| 调用失败 | 契约错误态 | FUNC-00191、FUNC-00192、FUNC-00193、FUNC-00194、FUNC-00195、FUNC-00196、FUNC-00197 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-belong \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00198、FUNC-00203 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00198、FUNC-00204 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00198、FUNC-00199、FUNC-00206 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00198、FUNC-00200、FUNC-00207 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00198、FUNC-00201、FUNC-00208 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00198、FUNC-00202、FUNC-00209 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["parent_sub"] | catalog relation_whitelist | FUNC-00198、FUNC-00205 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00198 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00198 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00198 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00198 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-belong \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-belong \| _fail \| 调用失败 | 契约错误态 | FUNC-00203、FUNC-00204、FUNC-00205、FUNC-00206、FUNC-00207、FUNC-00208、FUNC-00209 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.intra-supply \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00210、FUNC-00215 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00210、FUNC-00216 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00210、FUNC-00211、FUNC-00218 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00210、FUNC-00212、FUNC-00219 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00210、FUNC-00213、FUNC-00220 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00210、FUNC-00214、FUNC-00221 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["supply"] | catalog relation_whitelist | FUNC-00210、FUNC-00217 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00210 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00210 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00210 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00210 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.intra-supply \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.intra-supply \| _fail \| 调用失败 | 契约错误态 | FUNC-00215、FUNC-00216、FUNC-00217、FUNC-00218、FUNC-00219、FUNC-00220、FUNC-00221 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-industry \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00222、FUNC-00228 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00222、FUNC-00229 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00222、FUNC-00223、FUNC-00230 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00222、FUNC-00224、FUNC-00231 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00222、FUNC-00225、FUNC-00232 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00222、FUNC-00226、FUNC-00233 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["industry"] | catalog dest_types | FUNC-00222、FUNC-00227、FUNC-00234 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00222 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00222 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00222 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00222 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-industry \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-industry \| _fail \| 调用失败 | 契约错误态 | FUNC-00228、FUNC-00229、FUNC-00230、FUNC-00231、FUNC-00232、FUNC-00233、FUNC-00234 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-tech \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00235、FUNC-00241 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00235、FUNC-00242 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00235、FUNC-00236、FUNC-00243 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00235、FUNC-00237、FUNC-00244 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00235、FUNC-00238、FUNC-00245 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00235、FUNC-00239、FUNC-00246 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["technology"] | catalog dest_types | FUNC-00235、FUNC-00240、FUNC-00247 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00235 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00235 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00235 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00235 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-tech \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-tech \| _fail \| 调用失败 | 契约错误态 | FUNC-00241、FUNC-00242、FUNC-00243、FUNC-00244、FUNC-00245、FUNC-00246、FUNC-00247 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-talent \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00248、FUNC-00254 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00248、FUNC-00255 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00248、FUNC-00249、FUNC-00256 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00248、FUNC-00250、FUNC-00257 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00248、FUNC-00251、FUNC-00258 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00248、FUNC-00252、FUNC-00259 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["talent"] | catalog dest_types | FUNC-00248、FUNC-00253、FUNC-00260 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00248 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00248 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00248 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00248 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-talent \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-talent \| _fail \| 调用失败 | 契约错误态 | FUNC-00254、FUNC-00255、FUNC-00256、FUNC-00257、FUNC-00258、FUNC-00259、FUNC-00260 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-policy \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00261、FUNC-00267 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00261、FUNC-00268 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00261、FUNC-00262、FUNC-00269 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00261、FUNC-00263、FUNC-00270 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00261、FUNC-00264、FUNC-00271 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00261、FUNC-00265、FUNC-00272 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["policy"] | catalog dest_types | FUNC-00261、FUNC-00266、FUNC-00273 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00261 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00261 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00261 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00261 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-policy \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-policy \| _fail \| 调用失败 | 契约错误态 | FUNC-00267、FUNC-00268、FUNC-00269、FUNC-00270、FUNC-00271、FUNC-00272、FUNC-00273 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-research \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00274、FUNC-00280 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00274、FUNC-00281 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00274、FUNC-00275、FUNC-00282 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00274、FUNC-00276、FUNC-00283 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00274、FUNC-00277、FUNC-00284 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00274、FUNC-00278、FUNC-00285 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["research"] | catalog dest_types | FUNC-00274、FUNC-00279、FUNC-00286 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00274 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00274 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00274 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00274 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-research \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-research \| _fail \| 调用失败 | 契约错误态 | FUNC-00280、FUNC-00281、FUNC-00282、FUNC-00283、FUNC-00284、FUNC-00285、FUNC-00286 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |
| L10 \| entan.graph.hang-service \| op_id \| 算法输入-op_id写入算子 | catalog op_id | FUNC-00287、FUNC-00293 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| scope \| 算法输入-scopeone/batch | catalog scope | FUNC-00287、FUNC-00294 | 已覆盖 | 主流程合法值 + 缺省反向；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| id \| 算法输入-id企业稳定 org_id（scope=one） | catalog id | FUNC-00287、FUNC-00288、FUNC-00295 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00287、FUNC-00289、FUNC-00296 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | FUNC-00287、FUNC-00290、FUNC-00297 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| filter \| 算法输入-filterscope=batch 过滤，高级 JSON 保持 {all:true} | catalog filter | FUNC-00287、FUNC-00291、FUNC-00298 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| dest_types \| 算法输入-dest_types目标类型，高级 JSON 用 ["service"] | catalog dest_types | FUNC-00287、FUNC-00292、FUNC-00299 | 已覆盖 | 主流程全参 + 单独省略 + 非法值；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | FUNC-00287 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| written_edges \| 算法输出-written_edges写入边 | catalog written_edges | FUNC-00287 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | FUNC-00287 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00287 | 已覆盖 | 主流程逐字段断言该输出；文档 status=unavailable |
| L10 \| entan.graph.hang-service \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定合法入参下必空证据，不单开空态用例 |
| L10 \| entan.graph.hang-service \| _fail \| 调用失败 | 契约错误态 | FUNC-00293、FUNC-00294、FUNC-00295、FUNC-00296、FUNC-00297、FUNC-00298、FUNC-00299 | 已覆盖 | 每个参数一条反向，message 或 msg 指出该参数 |

---

## 计数

- L09 行 **20**、L10 行 **130**，矩阵 **150** 行，均有 endpoint，无 req_only。
- 状态：已覆盖 **138**、部分覆盖 **0**、未覆盖 **12**（未覆盖均为 `_empty`）。
- 输出字段挂该接口主流程编号；入参字段另挂该参数的省略或反向编号。

