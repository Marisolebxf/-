# M1 科创事件地图 · A 线功能点覆盖（innov.events）

> **catalog_page_id**：`innov.events` · path `/innov/events`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-科创事件地图-用例.md`（第三轮 **FUNC-01086**～**01114**，共 29 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.events`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.events.list | GET | /innov/v1/events | FUNC-01086～01100 | running |
| innov.events.geo | GET | /innov/v1/events | FUNC-01101、FUNC-01102 | running |
| innov.events.heatmap | GET | /innov/v1/events/heatmap | FUNC-01103～01107 | running |
| innov.events.detail | GET | /innov/v1/events/{eventId} | FUNC-01108、FUNC-01109 | running |
| innov.events.relations | GET | /innov/v1/events/{eventId}/relations | FUNC-01110、FUNC-01111 | running |
| innov.events.types | GET | /innov/v1/dict/event-types | FUNC-01112 | running |

列表与点位同 path，验收以 `endpoint_id` 区分，用例都留在本页。页面清单：**FUNC-01113**（接口信息）、**FUNC-01114**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条反向（必填为省略该参数）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.events.list \| 事件列表 | FUNC-01086～01100 | 无对应功能点 | 01086 主流程 sampleRequest（pageNum=1、pageSize=20）金样 LST-01；01087～01091 分别补传 startTime、endTime、eventTypes、importanceLevels、keyword；01092 省略 pageNum；01093 省略 pageSize；01094～01100 分别非法 startTime、endTime、eventTypes、importanceLevels、keyword、pageNum、pageSize |
| （无 Lxx） \| innov.events.geo \| 地图点位 | FUNC-01101、FUNC-01102 | 无对应功能点 | 01101 主流程 mode=geo；01102 省略必填 mode。与列表同 path |
| （无 Lxx） \| innov.events.heatmap \| 热力聚合 | FUNC-01103～01107 | 无对应功能点 | 01103 主流程不传时间；01104 补传 startTime；01105 补传 endTime；01106 非法 startTime；01107 非法 endTime |
| （无 Lxx） \| innov.events.detail \| 事件详情 | FUNC-01108、FUNC-01109 | 无对应功能点 | 01108 主流程 eventId=EVT-001；01109 省略必填 eventId |
| （无 Lxx） \| innov.events.relations \| 关联分析 | FUNC-01110、FUNC-01111 | 无对应功能点 | 01110 主流程 eventId=EVT-001；01111 省略必填 eventId |
| （无 Lxx） \| innov.events.types \| 事件类型字典 | FUNC-01112 | 无对应功能点 | 01112 无参主流程 |
| （页面清单） | FUNC-01113、FUNC-01114 | 无对应功能点 | 六接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 6 |
| title 数 | 6 |
| FUNC 用例数 | 29 |
| 主流程 | 6（01086 事件列表、01101 地图点位、01103 热力聚合、01108 事件详情、01110 关联分析、01112 事件类型字典） |
| 备选-参数组合 | 9（01087～01093、01104、01105） |
| 反向 | 12（01094～01100、01102、01106、01107、01109、01111） |
| 清单 | 2（01113 接口信息、01114 算法测试） |
| 编号 | FUNC-01086～01114 连续 |
| A 线 Lxx | 无 |
