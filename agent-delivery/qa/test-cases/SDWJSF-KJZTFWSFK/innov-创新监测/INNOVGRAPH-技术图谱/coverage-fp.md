# 技术图谱 · 功能点覆盖（innov.graph）

> catalog `innov.graph` · 50897 · path `/innov/graph`  
> 用例册：`API-技术图谱-用例.md`（API-00754～00768）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.*`（`_l6-to-catalog-map.yaml`）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.graph.domains | GET | /innov/v1/graph/domains | API-00754～00758 | catalog `status=running` · `runtime=java_api`；§0 **未试调** |
| innov.graph.subgraph | GET | /innov/v1/graph/subgraph | API-00759～00763 | 必填 `domainId`；§0 **未试调** |
| innov.graph.rank | GET | /innov/v1/graph/influence/rank | API-00764～00768 | 可选 `domainId`/`nodeType`/`pageNum`/`pageSize`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.graph \| innov.graph.domains \| domainId \| 算法输出-domainId领域标识 | catalog domainId | API-00754、00756 | 已覆盖 | 主路径 + 字段形态；样例 parentId/level 不设失败条件 |
| innov.graph \| innov.graph.domains \| name \| 算法输出-name领域名称 | catalog name | API-00754、00756 | 已覆盖 | 同上 |
| innov.graph \| innov.graph.domains \| _empty \| 领域树无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「合法请求必空数组」试调证据 |
| innov.graph \| innov.graph.domains \| _fail \| 领域树调用失败 | 契约错误态 | API-00755、00757、00758 | 已覆盖 | 鉴权、错误 HTTP 方法、错误 path |
| innov.graph \| innov.graph.subgraph \| domainId \| 算法输入-domainId领域 | catalog domainId required | API-00759、00761、00762 | 已覆盖 | 主路径 + 缺省 + 非法 id |
| innov.graph \| innov.graph.subgraph \| limit \| 算法输入-limit节点上限 | catalog limit | API-00759、00763 | 部分覆盖 | 主路径含 limit；越界 00763 |
| innov.graph \| innov.graph.subgraph \| nodes \| 算法输出-nodes子图节点 | catalog nodes | API-00759 | 已覆盖 | 禁止 sample 影响力作通过条件 |
| innov.graph \| innov.graph.subgraph \| edges \| 算法输出-edges子图边 | catalog edges | API-00759 | 已覆盖 | 禁止 sample weight 作通过条件 |
| innov.graph \| innov.graph.subgraph \| _empty \| 子图无节点空态 | 契约空结果 | — | 未覆盖 | 无试调证明合法 domainId 必空 nodes/edges |
| innov.graph \| innov.graph.subgraph \| _fail \| 子图调用失败 | 契约错误态 | API-00760、00761、00762、00763 | 已覆盖 | 鉴权 + 入参单缺陷 |
| innov.graph \| innov.graph.rank \| domainId \| 算法输入-domainId领域 | catalog domainId optional | API-00764、00766 | 部分覆盖 | 主路径带 D-AI；非法 id；省略默认 ALL（GRA-RNK-05）待试调后补 |
| innov.graph \| innov.graph.rank \| nodeType \| 算法输入-nodeType实体类型 | catalog nodeType | API-00764、00767 | 部分覆盖 | 主路径省略 nodeType；非法枚举 00767 |
| innov.graph \| innov.graph.rank \| pageNum \| 算法输入-pageNum页码 | catalog pageNum | API-00764 | 已覆盖 | 主路径 pageNum=1 |
| innov.graph \| innov.graph.rank \| pageSize \| 算法输入-pageSize页大小 | catalog pageSize | API-00764、00768 | 已覆盖 | 主路径 + 负值越界 |
| innov.graph \| innov.graph.rank \| list \| 算法输出-list排行列表 | catalog list | API-00764 | 已覆盖 | 禁止 sample rankInDomain/分值作通过条件 |
| innov.graph \| innov.graph.rank \| _empty \| 排行无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空 list 构造 |
| innov.graph \| innov.graph.rank \| _fail \| 排行调用失败 | 契约错误态 | API-00765、00766、00767、00768 | 已覆盖 | 鉴权 + 入参单缺陷 |
| innov.graph \| \| g6_viz \| 联调台 G6 图可视化 | catalog viz graph | — | 未覆盖 | UI 可视化，非 HTTP 契约字段 |
| innov.graph \| \| auto_run \| 页级自动执行 | catalog autoRun=false | — | 未覆盖 | 产品交互，非本 API 册 |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵，去重约） |
|------|----------------------------------|
| 已覆盖 | 12 |
| 部分覆盖 | 3（limit、domainId 省略 ALL、nodeType 主路径省略） |
| 未覆盖 | 5（`_empty`×3 + req_only×2） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **15**（3 endpoint × 5） |
| 编号 | **API-00754**～**API-00768** |
| `_empty` 未覆盖 | **3** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 3 endpoint、`running`×3 |
