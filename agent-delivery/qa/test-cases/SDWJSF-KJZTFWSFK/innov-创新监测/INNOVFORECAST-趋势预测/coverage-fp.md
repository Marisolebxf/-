# 趋势预测 · A 线功能点覆盖（innov.forecast）

> **catalog_page_id**：`innov.forecast` · path `/innov/forecast`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-趋势预测-用例.md`（第三轮 **FUNC-01151**～**01163**，共 13 条；旧 API-01883～01893 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.forecast`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | FUNC-01151、FUNC-01152 | running |
| innov.forecast.contributions | GET | /innov/v1/forecast/contributions | FUNC-01153～01158 | running |
| innov.forecast.bursts | GET | /innov/v1/forecast/bursts | FUNC-01159～01161 | running |

页面清单：**FUNC-01162**（接口信息）、**FUNC-01163**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「领域趋势预测」的 sampleResponse（`forecastMode`，`history` 及元素 `statYear`、`value`，`predictions` 及元素 `predictPeriod`、`predictValue`、`ciLower`、`ciUpper`）与 responseFields 的 `history`、`predictions` 都挂在主流程上；必填 `domainId` 反向为不传 path 段。title「创新点贡献度」的 sampleResponse（`total`，`list` 及元素 `targetId`、`title`、`eventType`、`contribution`、`predictValue`）与 responseFields 的 `list` 都挂在该接口主流程上；与 sample 相反的不传 `pageNum`、不传 `pageSize` 挂备选；必填 `domainId` 反向为省略，`pageNum`、`pageSize` 各 1 条非法反向。title「主题突变」的 sampleResponse（数组元素 `topicName`、`domainId`、`burstStart`、`burstScore`）与 responseFields 的 `topicName`、`burstScore` 都挂在该接口主流程上；与 sample 相反的不传 `domainId` 挂备选；`domainId` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.forecast.domain \| 领域趋势预测 | FUNC-01151、FUNC-01152 | 无对应功能点 | 01151 主流程 sampleRequest path domainId=D-AI（金样 DOM-01），断言 forecastMode、history（statYear、value）、predictions（predictPeriod、predictValue、ciLower、ciUpper）；01152 不传必填 domainId |
| （无 Lxx） \| innov.forecast.contributions \| 创新点贡献度 | FUNC-01153～01158 | 无对应功能点 | 01153 主流程 sampleRequest domainId=D-AI、pageNum=1、pageSize=10，断言 total、list（targetId、title、eventType、contribution、predictValue）；01154 不传 pageNum；01155 不传 pageSize；01156 省略必填 domainId；01157 非法 pageNum；01158 非法 pageSize |
| （无 Lxx） \| innov.forecast.bursts \| 主题突变 | FUNC-01159～01161 | 无对应功能点 | 01159 主流程 sampleRequest domainId=D-AI，断言 data 为数组，元素 topicName、burstScore，以及 sampleResponse 的 domainId、burstStart；01160 不传 domainId；01161 非法 domainId |
| （页面清单） | FUNC-01162、FUNC-01163 | 无对应功能点 | 三接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 13 |
| 主流程 | 3（01151 领域趋势预测、01153 创新点贡献度、01159 主题突变） |
| 备选-参数组合 | 3（01154、01155、01160） |
| 反向 | 5（01152、01156、01157、01158、01161） |
| 清单 | 2（01162、01163） |
| 编号 | FUNC-01151～01163 连续 |
| A 线 Lxx | 无 |
| 金样 | FUNC-01151 |
