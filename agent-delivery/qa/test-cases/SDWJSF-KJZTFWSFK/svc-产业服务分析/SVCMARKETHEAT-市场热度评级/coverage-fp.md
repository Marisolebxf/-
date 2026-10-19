# 市场热度评级 · A 线功能点覆盖（svc.market-heat）

> **catalog_page_id**：`svc.market-heat` · path `/industry-service/market-heat`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.market-heat`（原因：不扩六级）。不改 `work/`。  
> **用例册**：`API-市场热度评级-用例.md`（第二轮 **API-01716**～**01721**，共 6 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.market-heat`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.market-heat.main | GET | /entan/v1/svc/market-heat | API-01716、API-01717、API-01718 | unavailable |
| svc.market-heat.m_svc_org_market_heat | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | API-01719、API-01720、API-01721 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| svc.market-heat.main \| 市场热度 | API-01716、API-01717、API-01718 | 无对应功能点 | 01716 主流程 sampleRequest（industry=人工智能），断言 market_heat_level、trend_slope、volatility、series 及元素 year、new_org_count；01717 省略可选 industry；01718 非法 industry。文档标记未交付 |
| （无 Lxx） \| svc.market-heat.m_svc_org_market_heat \| 市场热度评级 | API-01719、API-01720、API-01721 | 无对应功能点 | 01719 主流程 sampleRequest（industry=人工智能），断言 metric_id、hint 与 responseFields 的 market_heat_level、series；01720 省略可选 industry；01721 非法 industry |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 6 |
| 主流程 | 2（01716 市场热度、01719 市场热度评级） |
| 备选-参数组合 | 2（01717、01720） |
| 反向 | 2（01718、01721） |
| 编号 | API-01716～01721 连续 |
| A 线 Lxx | 无 |
