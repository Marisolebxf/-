# 载体分析 · A 线功能点覆盖（innov.carriers）

> **catalog_page_id**：`innov.carriers` · path `/innov/carriers`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-载体分析-用例.md`（第三轮 **FUNC-01131**～**01140**，共 10 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.carriers`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.carriers.rank | GET | /innov/v1/carriers/rank | FUNC-01131～01135 | running |
| innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | FUNC-01136、FUNC-01137 | running |
| innov.carriers.method | GET | /innov/v1/carriers/index-method | FUNC-01138 | running |

页面清单：**FUNC-01139**（接口信息）、**FUNC-01140**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「载体排行」的 sampleResponse（`total`、`period`、`list` 及元素 `carrierId`、`name`、`carrierType`、`indexScore`、`rankTotal`、`subScores.output` / `quality` / `activity` / `performance`）与 responseFields 的 `list` 都挂在主流程上；可选参数与 sample 相反的不传挂备选；每个参数恰好 1 条非法反向。title「载体详情」的 sampleResponse（`info.carrierId` / `name` / `carrierType`，`trend` 及元素 `statPeriod`、`indexScore`、`rankTotal`，`radar` 及元素 `成果产出`、`成果质量`、`创新活跃`、`转化绩效`）与 responseFields 的 `info`、`trend` 都挂在该接口主流程上；必填 `carrierId` 反向为省略。title「指数方法与权重」的 sampleResponse（`weightVersion`、`methodDesc`、`weights` 及元素 `k`、`desc`、`w`）与 responseFields 的 `methodDesc`、`weights` 都挂在无参主流程上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.carriers.rank \| 载体排行 | FUNC-01131～01135 | 无对应功能点 | 01131 主流程 sampleRequest pageNum=1、pageSize=20 金样 RNK-01；01132 不传 pageNum；01133 不传 pageSize；01134 非法 pageNum=not-a-page；01135 非法 pageSize=not-a-size |
| （无 Lxx） \| innov.carriers.detail \| 载体详情 | FUNC-01136、FUNC-01137 | 无对应功能点 | 01136 主流程 path carrierId=CAR-01；01137 省略必填 carrierId |
| （无 Lxx） \| innov.carriers.method \| 指数方法与权重 | FUNC-01138 | 无对应功能点 | 01138 无参主流程 |
| （页面清单） | FUNC-01139、FUNC-01140 | 无对应功能点 | 三接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 10 |
| 主流程 | 3（01131 载体排行、01136 载体详情、01138 指数方法与权重） |
| 备选-参数组合 | 2（01132、01133） |
| 反向 | 3（01134、01135、01137） |
| 清单 | 2（01139、01140） |
| 编号 | FUNC-01131～01140 连续 |
| A 线 Lxx | 无 |
| 已作废 | API-01867～01874（第二轮 API 册已删） |
