# M1 科创事件地图 · A 线功能点覆盖（innov.events）

> **catalog_page_id**：`innov.events` · path `/innov/events`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-科创事件地图-用例.md`（第二轮 **API-01826**～**01852**，共 27 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.events`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.events.list | GET | /innov/v1/events | API-01826～01840 | running |
| innov.events.geo | GET | /innov/v1/events | API-01841、API-01842 | running |
| innov.events.heatmap | GET | /innov/v1/events/heatmap | API-01843～01847 | running |
| innov.events.detail | GET | /innov/v1/events/{eventId} | API-01848、API-01849 | running |
| innov.events.relations | GET | /innov/v1/events/{eventId}/relations | API-01850、API-01851 | running |
| innov.events.types | GET | /innov/v1/dict/event-types | API-01852 | running |

列表与点位同 path，验收以 `endpoint_id` 区分，用例都留在本页。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条反向（必填为省略该参数）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.events.list \| 事件列表 | API-01826～01840 | 无对应功能点 | 01826 主流程 sampleRequest（pageNum=1、pageSize=20），断言 total、list 及元素 eventId、title、importanceLevel、importanceScore、eventTime、eventType、cityCode；01827～01831 分别补传 startTime、endTime、eventTypes、importanceLevels、keyword；01832 省略 pageNum；01833 省略 pageSize；01834～01840 分别非法 startTime、endTime、eventTypes、importanceLevels、keyword、pageNum、pageSize |
| （无 Lxx） \| innov.events.geo \| 地图点位 | API-01841、API-01842 | 无对应功能点 | 01841 主流程 mode=geo，断言 type、features 及元素 type、geometry、coordinates、properties；01842 省略必填 mode。与列表同 path |
| （无 Lxx） \| innov.events.heatmap \| 热力聚合 | API-01843～01847 | 无对应功能点 | 01843 主流程不传时间，断言 lng、lat、weight；01844 补传 startTime；01845 补传 endTime；01846 非法 startTime；01847 非法 endTime |
| （无 Lxx） \| innov.events.detail \| 事件详情 | API-01848、API-01849 | 无对应功能点 | 01848 主流程 eventId=EVT-001，断言 eventId、importanceDetail 及 title、eventType、eventTime、importanceLevel、importanceScore、summary、k、v；01849 省略必填 eventId |
| （无 Lxx） \| innov.events.relations \| 关联分析 | API-01850、API-01851 | 无对应功能点 | 01850 主流程 eventId=EVT-001，断言 relType、relName 及 relId、relDesc、score；01851 省略必填 eventId |
| （无 Lxx） \| innov.events.types \| 事件类型字典 | API-01852 | 无对应功能点 | 01852 无参主流程，断言 eventType、nameZh、color |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 6 |
| title 数 | 6 |
| API 用例数 | 27 |
| 主流程 | 6（01826 事件列表、01841 地图点位、01843 热力聚合、01848 事件详情、01850 关联分析、01852 事件类型字典） |
| 备选-参数组合 | 9（01827～01833、01844、01845） |
| 反向 | 12（01834～01840、01842、01846、01847、01849、01851） |
| 编号 | API-01826～01852 连续 |
| A 线 Lxx | 无 |
