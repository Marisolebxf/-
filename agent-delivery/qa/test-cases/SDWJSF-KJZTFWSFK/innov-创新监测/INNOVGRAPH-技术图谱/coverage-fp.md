# 技术图谱 · A 线功能点覆盖（innov.graph）

> **catalog_page_id**：`innov.graph` · path `/innov/graph`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-技术图谱-用例.md`（第二轮 **API-01853**～**01866**，共 14 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.graph`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.graph.domains | GET | /innov/v1/graph/domains | API-01853 | running |
| innov.graph.subgraph | GET | /innov/v1/graph/subgraph | API-01854、API-01855、API-01856、API-01857 | running |
| innov.graph.rank | GET | /innov/v1/graph/influence/rank | API-01858、API-01859、API-01860、API-01861、API-01862、API-01863、API-01864、API-01865、API-01866 | running |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「领域树」的 sampleResponse（数组元素 `domainId`、`name`、`parentId`、`level`、`domainSource`）与 responseFields 的 `domainId`、`name` 都挂在主流程上。title「领域子图」的 sampleResponse（`period`、`nodes` 及元素 `nodeId`、`nodeType`、`name`、`influenceScore`、`rank`，`edges` 及元素 `src`、`dst`、`edgeType`、`weight`）与 responseFields 的 `nodes`、`edges` 都挂在该接口主流程上；与 sample 相反的不传 `limit` 挂备选；必填 `domainId` 反向为省略，`limit` 恰好 1 条非法反向。title「影响分排行」的 sampleResponse（`total`、`period`、`list` 及元素 `nodeId`、`nodeType`、`name`、`influenceScore`、`rankInDomain`）与 responseFields 的 `list` 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.graph.domains \| 领域树 | API-01853 | 无对应功能点 | 01853 主流程无参，断言 data 为数组，元素 domainId、name，以及 sampleResponse 的 parentId、level、domainSource（示例 D-AI/人工智能/空串/1/seed，D-BIO/生物医药/空串/1/seed） |
| （无 Lxx） \| innov.graph.subgraph \| 领域子图 | API-01854、API-01855、API-01856、API-01857 | 无对应功能点 | 01854 主流程 sampleRequest domainId=D-AI、limit=60，断言 period、nodes（nodeId、nodeType、name、influenceScore、rank）、edges（src、dst、edgeType、weight）；01855 不传 limit；01856 省略必填 domainId；01857 非法 limit=not-a-limit |
| （无 Lxx） \| innov.graph.rank \| 影响分排行 | API-01858、API-01859、API-01860、API-01861、API-01862、API-01863、API-01864、API-01865、API-01866 | 无对应功能点 | 01858 主流程 sampleRequest domainId=D-AI、pageNum=1、pageSize=20、不传 nodeType，断言 total、period、list（nodeId、nodeType、name、influenceScore、rankInDomain）；01859 不传 domainId；01860 传 nodeType=org；01861 不传 pageNum；01862 不传 pageSize；01863～01866 分别非法 domainId、nodeType、pageNum、pageSize |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 14 |
| 主流程 | 3（01853 领域树、01854 领域子图、01858 影响分排行） |
| 备选-参数组合 | 5（01855、01859、01860、01861、01862） |
| 反向 | 6（01856、01857、01863、01864、01865、01866） |
| 编号 | API-01853～01866 连续 |
| A 线 Lxx | 无 |
