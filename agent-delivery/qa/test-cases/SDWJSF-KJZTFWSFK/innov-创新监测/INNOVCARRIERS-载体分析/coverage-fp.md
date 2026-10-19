# 载体分析 · A 线功能点覆盖（innov.carriers）

> **catalog_page_id**：`innov.carriers` · path `/innov/carriers`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-载体分析-用例.md`（第二轮 **API-01867**～**01874**，共 8 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.carriers`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.carriers.rank | GET | /innov/v1/carriers/rank | API-01867、API-01868、API-01869、API-01870、API-01871 | running |
| innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | API-01872、API-01873 | running |
| innov.carriers.method | GET | /innov/v1/carriers/index-method | API-01874 | running |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「载体排行」的 sampleResponse（`total`、`period`、`list` 及元素 `carrierId`、`name`、`carrierType`、`indexScore`、`rankTotal`、`subScores.output` / `quality` / `activity` / `performance`）与 responseFields 的 `list` 都挂在主流程上；可选参数与 sample 相反的不传挂备选；每个参数恰好 1 条非法反向。title「载体详情」的 sampleResponse（`info.carrierId` / `name` / `carrierType`，`trend` 及元素 `statPeriod`、`indexScore`、`rankTotal`，`radar` 及元素 `成果产出`、`成果质量`、`创新活跃`、`转化绩效`）与 responseFields 的 `info`、`trend` 都挂在该接口主流程上；必填 `carrierId` 反向为省略。title「指数方法与权重」的 sampleResponse（`weightVersion`、`methodDesc`、`weights` 及元素 `k`、`desc`、`w`）与 responseFields 的 `methodDesc`、`weights` 都挂在无参主流程上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.carriers.rank \| 载体排行 | API-01867、API-01868、API-01869、API-01870、API-01871 | 无对应功能点 | 01867 主流程 sampleRequest pageNum=1、pageSize=20，断言 total、period、list（carrierId、name、carrierType、indexScore、rankTotal、subScores.output/quality/activity/performance）；01868 不传 pageNum；01869 不传 pageSize；01870 非法 pageNum=not-a-page；01871 非法 pageSize=not-a-size |
| （无 Lxx） \| innov.carriers.detail \| 载体详情 | API-01872、API-01873 | 无对应功能点 | 01872 主流程 path carrierId=CAR-01，断言 info（carrierId、name、carrierType）、trend（statPeriod、indexScore、rankTotal）、radar（成果产出、成果质量、创新活跃、转化绩效）；01873 省略必填 carrierId |
| （无 Lxx） \| innov.carriers.method \| 指数方法与权重 | API-01874 | 无对应功能点 | 01874 无参主流程，断言 weightVersion、methodDesc、weights（k、desc、w） |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 8 |
| 主流程 | 3（01867 载体排行、01872 载体详情、01874 指数方法与权重） |
| 备选-参数组合 | 2（01868、01869） |
| 反向 | 3（01870、01871、01873） |
| 编号 | API-01867～01874 连续 |
| A 线 Lxx | 无 |
