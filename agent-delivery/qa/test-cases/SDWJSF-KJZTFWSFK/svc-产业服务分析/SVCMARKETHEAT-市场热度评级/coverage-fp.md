# 市场热度评级 · 功能点覆盖（svc.market-heat）

> **catalog_page_id**：`svc.market-heat` · path `#/industry-service/market-heat`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.market-heat`（原因：不扩六级）。不改 `work/`。  
> **B 线用例**：`FUNC-市场热度评级-用例.md`（第三轮 **FUNC-00948**～**FUNC-00955**）  
> **契约**：`lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.market-heat`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.market-heat.main | GET | /entan/v1/svc/market-heat | FUNC-00948～00950 | unavailable |
| svc.market-heat.m_svc_org_market_heat | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | FUNC-00951～00953 | available |
| （页面清单） | — | — | FUNC-00954、00955 | — |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行；每个 title 的 sampleResponse 与 responseFields 挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；`industry` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| svc.market-heat.main \| 市场热度 | FUNC-00948、00949、00950 | 无对应功能点 | 00948 主流程 sampleRequest（industry=人工智能），断言 market_heat_level、trend_slope、volatility、series 及元素 year、new_org_count；00949 省略可选 industry；00950 非法 industry。文档标记未交付 |
| （无 Lxx） \| svc.market-heat.m_svc_org_market_heat \| 市场热度评级 | FUNC-00951、00952、00953 | 无对应功能点 | 00951 主流程 sampleRequest（industry=人工智能），断言 metric_id、hint 与 responseFields 的 market_heat_level、series；00952 省略可选 industry；00953 非法 industry |

---

## 页面清单（联调台 tab）

| 场景 | 对应用例编号 | 状态 |
|------|--------------|------|
| 接口信息-清单 | FUNC-00954 | 已覆盖 |
| 算法测试-清单 | FUNC-00955 | 已覆盖 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 8 |
| 主流程 | 2（00948 市场热度、00951 市场热度评级） |
| 备选-参数组合 | 2（00949、00952） |
| 反向 | 2（00950、00953） |
| 清单 | 2（00954、00955） |
| 编号 | FUNC-00948～00955 连续 |
| A 线 Lxx | 无（catalog_skip） |
