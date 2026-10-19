# 城市对标 · A 线功能点覆盖（innov.cities）

> **catalog_page_id**：`innov.cities` · path `/innov/cities`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-城市对标-用例.md`（第二轮 **API-01875**～**01882**，共 8 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.cities`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.cities.rank | GET | /innov/v1/cities/rank | API-01875、API-01876、API-01877 | running |
| innov.cities.compare | GET | /innov/v1/cities/compare | API-01878、API-01879 | running |
| innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | API-01880、API-01881 | running |
| innov.cities.method | GET | /innov/v1/cities/index-method | API-01882 | running |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「城市排名」的 sampleResponse（`period`、`list` 及元素 `cityCode`、`nameZh`、`indexScore`、`rankGlobal`、`rankDomestic`、`isBenchmark`、`subScores.resource/institution/output/environment`）与 responseFields 的 `list` 都挂在主流程上；与 sample 相反的不传 `scope` 挂备选；`scope` 恰好 1 条非法反向。title「城市对标」的 sampleResponse（`list` 及元素 `cityCode`、`nameZh`、`indexScore`、`rankGlobal`、`resource`、`institution`、`output`、`environment`，以及 `radar` 及元素创新资源、制度环境、创新产出、产业环境）与 responseFields 的 `list` 都挂在该接口主流程上；必填 `cityCodes` 反向为省略。title「政策建议」的 sampleResponse（`reportId`、`title`、`generateMode`、`contentMd`）与 responseFields 的 `title`、`contentMd` 都挂在该接口主流程上；必填 `cityCode` 反向为省略。title「指数方法与权重」的 sampleResponse（`weightVersion`、`methodDesc`、`weights` 及元素 `k`、`desc`、`w`）与 responseFields 的 `weights` 都挂在无参主流程上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.cities.rank \| 城市排名 | API-01875、API-01876、API-01877 | 无对应功能点 | 01875 主流程 sampleRequest scope=global，断言 period、list（cityCode、nameZh、indexScore、rankGlobal、rankDomestic、isBenchmark、subScores）；01876 不传 scope；01877 非法 scope=__invalid__ |
| （无 Lxx） \| innov.cities.compare \| 城市对标 | API-01878、API-01879 | 无对应功能点 | 01878 主流程 sampleRequest cityCodes=440300,110000，断言 list（cityCode、nameZh、indexScore、rankGlobal、resource、institution、output、environment）与 radar；01879 省略必填 cityCodes |
| （无 Lxx） \| innov.cities.advice \| 政策建议 | API-01880、API-01881 | 无对应功能点 | 01880 主流程 path cityCode=440300，断言 title、contentMd 以及 sampleResponse 的 reportId、generateMode；01881 省略必填 cityCode（path 空段 `/innov/v1/cities//advice`） |
| （无 Lxx） \| innov.cities.method \| 指数方法与权重 | API-01882 | 无对应功能点 | 01882 无参主流程，断言 weightVersion、methodDesc、weights（k、desc、w） |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| API 用例数 | 8 |
| 主流程 | 4（01875 城市排名、01878 城市对标、01880 政策建议、01882 指数方法与权重） |
| 备选-参数组合 | 1（01876） |
| 反向 | 3（01877、01879、01881） |
| 编号 | API-01875～01882 连续 |
| A 线 Lxx | 无 |
