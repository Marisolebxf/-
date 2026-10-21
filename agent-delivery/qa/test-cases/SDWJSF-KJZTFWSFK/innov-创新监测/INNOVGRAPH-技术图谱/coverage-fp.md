# 技术图谱 · A 线功能点覆盖（innov.graph）

> **catalog_page_id**：`innov.graph` · path `/innov/graph`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-技术图谱-用例.md`（第三轮 **FUNC-01115**～**01130**，共 16 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.graph`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.graph.domains | GET | /innov/v1/graph/domains | FUNC-01115 | running |
| innov.graph.subgraph | GET | /innov/v1/graph/subgraph | FUNC-01116、FUNC-01117、FUNC-01118、FUNC-01119 | running |
| innov.graph.rank | GET | /innov/v1/graph/influence/rank | FUNC-01120～FUNC-01128 | running |

页面清单：**FUNC-01129**（接口信息）、**FUNC-01130**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条反向（必填为省略该参数）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.graph.domains \| 领域树 | FUNC-01115 | 无对应功能点 | 01115 无参主流程，断言 data 为数组，元素 domainId、name，以及 sampleResponse 的 parentId、level、domainSource（示例 D-AI/人工智能、D-BIO/生物医药） |
| （无 Lxx） \| innov.graph.subgraph \| 领域子图 | FUNC-01116～01119 | 无对应功能点 | 01116 主流程 sampleRequest domainId=D-AI、limit=60，断言 period、nodes、edges；01117 不传 limit；01118 省略必填 domainId；01119 非法 limit=not-a-limit |
| （无 Lxx） \| innov.graph.rank \| 影响分排行 | FUNC-01120～01128 | 无对应功能点 | 01120 主流程 sampleRequest domainId=D-AI、pageNum=1、pageSize=20、不传 nodeType，断言 total、period、list；01121 不传 domainId；01122 传 nodeType=org；01123 不传 pageNum；01124 不传 pageSize；01125～01128 分别非法 domainId、nodeType、pageNum、pageSize |
| （页面清单） | FUNC-01129、FUNC-01130 | 无对应功能点 | 三接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 16 |
| 主流程 | 3（01115 领域树、01116 领域子图、01120 影响分排行） |
| 备选-参数组合 | 5（01117、01121、01122、01123、01124） |
| 反向 | 6（01118、01119、01125、01126、01127、01128） |
| 页面清单 | 2（01129、01130） |
| 编号 | FUNC-01115～01130 连续 |
| A 线 Lxx | 无 |
