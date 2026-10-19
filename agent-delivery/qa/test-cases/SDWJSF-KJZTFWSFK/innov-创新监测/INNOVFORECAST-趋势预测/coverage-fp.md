# 趋势预测 · A 线功能点覆盖（innov.forecast）

> **catalog_page_id**：`innov.forecast` · path `/innov/forecast`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-趋势预测-用例.md`（第二轮 **API-01883**～**01893**，共 11 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.forecast`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | API-01883、API-01884 | running |
| innov.forecast.contributions | GET | /innov/v1/forecast/contributions | API-01885、API-01886、API-01887、API-01888、API-01889、API-01890 | running |
| innov.forecast.bursts | GET | /innov/v1/forecast/bursts | API-01891、API-01892、API-01893 | running |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「领域趋势预测」的 sampleResponse（`forecastMode`，`history` 及元素 `statYear`、`value`，`predictions` 及元素 `predictPeriod`、`predictValue`、`ciLower`、`ciUpper`）与 responseFields 的 `history`、`predictions` 都挂在主流程上；必填 `domainId` 反向为省略 path 段。title「创新点贡献度」的 sampleResponse（`total`，`list` 及元素 `targetId`、`title`、`eventType`、`contribution`、`predictValue`）与 responseFields 的 `list` 都挂在该接口主流程上；与 sample 相反的不传 `pageNum`、不传 `pageSize` 挂备选；必填 `domainId` 反向为省略，`pageNum`、`pageSize` 各 1 条非法反向。title「主题突变」的 sampleResponse（数组元素 `topicName`、`domainId`、`burstStart`、`burstScore`）与 responseFields 的 `topicName`、`burstScore` 都挂在该接口主流程上；与 sample 相反的不传 `domainId` 挂备选；`domainId` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.forecast.domain \| 领域趋势预测 | API-01883、API-01884 | 无对应功能点 | 01883 主流程 sampleRequest path domainId=D-AI，断言 forecastMode、history（statYear、value）、predictions（predictPeriod、predictValue、ciLower、ciUpper）；01884 省略必填 path 段 domainId |
| （无 Lxx） \| innov.forecast.contributions \| 创新点贡献度 | API-01885、API-01886、API-01887、API-01888、API-01889、API-01890 | 无对应功能点 | 01885 主流程 sampleRequest domainId=D-AI、pageNum=1、pageSize=10，断言 total、list（targetId、title、eventType、contribution、predictValue）；01886 不传 pageNum；01887 不传 pageSize；01888 省略必填 domainId；01889 非法 pageNum；01890 非法 pageSize |
| （无 Lxx） \| innov.forecast.bursts \| 主题突变 | API-01891、API-01892、API-01893 | 无对应功能点 | 01891 主流程 sampleRequest domainId=D-AI，断言 data 为数组，元素 topicName、burstScore，以及 sampleResponse 的 domainId、burstStart；01892 不传 domainId；01893 非法 domainId |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 11 |
| 主流程 | 3（01883 领域趋势预测、01885 创新点贡献度、01891 主题突变） |
| 备选-参数组合 | 3（01886、01887、01892） |
| 反向 | 5（01884、01888、01889、01890、01893） |
| 编号 | API-01883～01893 连续 |
| A 线 Lxx | 无 |
