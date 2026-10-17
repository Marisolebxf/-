# 政策实体与关系 · 功能点覆盖（policy.graph / L07+L08）

> catalog `policy.graph` · 50897 · path `/policy/graph`  
> **用例册**：`API-政策实体与关系-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000419`～`000448`，共 **30** 条）  
> A 线范围：**L07**（ner/main，20 行含 1 req_only）· **L08**（intra/hang，44 行）  
> 功能点键：`Lxx | endpoint_id | field_key | 功能点中文`  
> **A 线核对**：`grep policy.graph fp-split-by-api-run/work/L07.md L08.md`

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.graph.ner | POST | /policy/v1/policy/graph/ner | API-000419, API-000420, API-000421, API-000422, API-000423 | unavailable |
| policy.graph.intra | POST | /policy/v1/policy/graph/intra | API-000424, API-000425, API-000426, API-000427, API-000428 | unavailable |
| policy.graph.hang-support | POST | /policy/v1/policy/graph/hang | API-000429, API-000430, API-000431, API-000432, API-000433 | unavailable |
| policy.graph.hang-apply | POST | /policy/v1/policy/graph/hang | API-000434, API-000435, API-000436, API-000437, API-000438 | unavailable |
| policy.graph.hang-regulate | POST | /policy/v1/policy/graph/hang | API-000439, API-000440, API-000441, API-000442, API-000443 | unavailable |
| policy.graph.main | GET | /policy/v1/policy/graph | API-000444, API-000445, API-000446, API-000447, API-000448 | unavailable |

---

## 2. 功能点 → 用例（L07+L08 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L07 \| policy.graph.ner \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-000419、API-000420、API-000421、API-000422、API-000423 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L07 \| policy.graph.ner \| scope \| 算法输入-scopeone/batch | catalog scope | API-000419、API-000420、API-000421、API-000422、API-000423 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L07 \| policy.graph.ner \| id \| 算法输入-id政策稳定 ID（scope=one） | catalog id | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| mode \| 算法输入-moderule/llm | catalog mode | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| filter \| 算法输入-filterscope=batch 过滤对象，高级 JSON 保持 {all:true} | catalog filter | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| written_nodes \| 算法输出-written_nodes写入点 | catalog written_nodes | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-000419 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.ner \| _empty \| 查询无数据空态 | catalog 契约 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L07 \| policy.graph.ner \| _fail \| 调用失败 | catalog 契约 | API-000420、API-000421、API-000422、API-000423 | 已覆盖 | 契约占位+入参失败哨兵 |
| L07 \| policy.graph.ner \| policy_entity_pipeline \| 政策实体识别需规语义 | 需规 | — | 不纳入 | req_only |
| L07 \| policy.graph.main \| center \| 算法输入-center中心节点 VID 或 policy_id | catalog center | API-000444、API-000445、API-000446、API-000447、API-000448 | 部分覆盖 | unavailable 占位+非法 center |
| L07 \| policy.graph.main \| steps \| 算法输入-steps邻域跳数 | catalog steps | API-000444、API-000445、API-000446、API-000447、API-000448 | 部分覆盖 | unavailable 占位+非法 steps |
| L07 \| policy.graph.main \| limit \| 算法输入-limit节点上限 | catalog limit | API-000444、API-000445、API-000446、API-000447、API-000448 | 部分覆盖 | unavailable 占位+limit 越界 |
| L07 \| policy.graph.main \| nodes \| 算法输出-nodes节点 | catalog nodes | API-000444 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.main \| edges \| 算法输出-edges关系边 | catalog edges | API-000444 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.main \| source \| 算法输出-sourcenebula／ads／镜像；space 恒 demo_gkx_chain | catalog source | API-000444 | 契约占位 | 禁止 sample 数值作通过条件 |
| L07 \| policy.graph.main \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L07 \| policy.graph.main \| _fail \| 调用失败 | 契约错误态 | API-000445、API-000446、API-000447 | 已覆盖 | 契约占位+入参失败哨兵 |
| L08 \| policy.graph.intra \| op_id \| 算法输入-op_id写入算子 | catalog op_id | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| scope \| 算法输入-scopeone/batch | catalog scope | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| id \| 算法输入-id政策稳定 ID | catalog id | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| mode \| 算法输入-moderule/llm | catalog mode | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| relation_whitelist \| 算法输入-relation_whitelist白名单，高级 JSON 用 ["cite"] | catalog relation_whitelist | API-000424, API-000425, API-000426, API-000427, API-000428 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.intra \| written_edges \| 算法输出-written_edgescite 边 | catalog written_edges | API-000424 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.intra \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000424 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.intra \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L08 \| policy.graph.intra \| _fail \| 调用失败 | 契约错误态 | API-000425, API-000426, API-000427, API-000428 | 已覆盖 | 契约占位+入参失败哨兵 |
| L08 \| policy.graph.hang-support \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| scope \| 算法输入-scopeone/batch | catalog scope | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| id \| 算法输入-id政策稳定 ID，禁止用名称猜 VID | catalog id | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| mode \| 算法输入-moderule/llm | catalog mode | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000429, API-000430, API-000431, API-000432, API-000433 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-support \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["support"] | catalog relation_whitelist | API-000429 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-support \| written_edges \| 算法输出-written_edgessupport 边 | catalog written_edges | API-000429 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-support \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000429 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-support \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L08 \| policy.graph.hang-support \| _fail \| 调用失败 | 契约错误态 | API-000430, API-000431, API-000432, API-000433 | 已覆盖 | 契约占位+入参失败哨兵 |
| L08 \| policy.graph.hang-apply \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| scope \| 算法输入-scopeone/batch | catalog scope | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| id \| 算法输入-id政策稳定 ID | catalog id | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| mode \| 算法输入-moderule/llm | catalog mode | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000434, API-000435, API-000436, API-000437, API-000438 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-apply \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["apply_to"] | catalog relation_whitelist | API-000434 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-apply \| written_edges \| 算法输出-written_edgesapply_to 边 | catalog written_edges | API-000434 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-apply \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000434 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-apply \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L08 \| policy.graph.hang-apply \| _fail \| 调用失败 | 契约错误态 | API-000435, API-000436, API-000437, API-000438 | 已覆盖 | 契约占位+入参失败哨兵 |
| L08 \| policy.graph.hang-regulate \| op_id \| 算法输入-op_id必须带 op_id | catalog op_id | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| scope \| 算法输入-scopeone/batch | catalog scope | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| id \| 算法输入-id政策稳定 ID | catalog id | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| mode \| 算法输入-moderule/llm | catalog mode | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| dry_run \| 算法输入-dry_run不写 ADS/Nebula | catalog dry_run | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| filter \| 算法输入-filterbatch 过滤对象 | catalog filter | API-000439, API-000440, API-000441, API-000442, API-000443 | 部分覆盖 | unavailable 占位+必填/非法哨兵 |
| L08 \| policy.graph.hang-regulate \| relation_whitelist \| 算法输入-relation_whitelist高级 JSON 用 ["regulate"] | catalog relation_whitelist | API-000439 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-regulate \| written_edges \| 算法输出-written_edgesregulate 边 | catalog written_edges | API-000439 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-regulate \| skipped \| 算法输出-skipped四码跳过 | catalog skipped | API-000439 | 契约占位 | 禁止 sample 数值作通过条件 |
| L08 \| policy.graph.hang-regulate \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定合法入参下必空证据 |
| L08 \| policy.graph.hang-regulate \| _fail \| 调用失败 | 契约错误态 | API-000440, API-000441, API-000442, API-000443 | 已覆盖 | 契约占位+入参失败哨兵 |

---

## 3. §I 计数

| 指标 | 值 |
|------|-----|
| API 用例 | 30（000419～000448） |
| catalog endpoint | 6 |
| L07+L08 矩阵行（含 req_only） | 67 |
| `_empty` 未覆盖 | 6 |
| req_only 不纳入 | 1 |
| 金样 | API-000419 |
| 鉴权代表 | API-000420 |
| FUNC | 0 |
| code-registry / run-log | 未改（父控） |
