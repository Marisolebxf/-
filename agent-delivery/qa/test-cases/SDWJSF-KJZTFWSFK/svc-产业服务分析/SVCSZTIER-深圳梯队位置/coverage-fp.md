# 深圳梯队位置 · A 线功能点覆盖（svc.sz-tier）

> **catalog_page_id**：`svc.sz-tier` · path `/industry-service/sz-tier`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.sz-tier`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-深圳梯队位置-用例.md`（第二轮 **API-01722**～**01727**，共 6 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.sz-tier`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.sz-tier.main | GET | /entan/v1/svc/sz-tier | API-01722、API-01723、API-01724 | unavailable |
| svc.sz-tier.m_svc_sz_tier | POST | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | API-01725、API-01726、API-01727 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「深圳梯队」的 sampleResponse（`dims` 及元素 `dim`、`dim_key`、`tier`）与 responseFields 的 `dims` 都挂在主流程上；title「深圳梯队位置」的 sampleResponse（`metric_id`、`hint`）与 responseFields 的 `dims` 都挂在该接口主流程上。可选 `industry` 与 sample 相反的不传挂备选；每个参数恰好 1 条非法反向。`深圳梯队` catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| svc.sz-tier.main \| 深圳梯队 | API-01722、API-01723、API-01724 | 无对应功能点 | 01722 主流程 sampleRequest industry=人工智能，断言 dims 及元素 dim、dim_key、tier（示例 机构数量/org_count/T1、技术力得分/tech_score/T2、服务链完整度/chain_coverage/T1）；01723 不传 industry；01724 非法 industry=__invalid__。文档标记未交付 |
| （无 Lxx） \| svc.sz-tier.m_svc_sz_tier \| 深圳梯队位置 | API-01725、API-01726、API-01727 | 无对应功能点 | 01725 主流程 sampleRequest industry=人工智能，断言 metric_id=M_SVC_SZ_TIER、hint，以及 responseFields 的 dims；01726 不传 industry；01727 非法 industry=__invalid__ |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 6 |
| 主流程 | 2（01722 深圳梯队、01725 深圳梯队位置） |
| 备选-参数组合 | 2（01723、01726） |
| 反向 | 2（01724、01727） |
| 编号 | API-01722～01727 连续 |
| A 线 Lxx | 无 |
