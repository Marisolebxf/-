# 深圳梯队位置 · A 线功能点覆盖（svc.sz-tier）

> **catalog_page_id**：`svc.sz-tier` · path `#/industry-service/sz-tier`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.sz-tier`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **B 线用例**：`FUNC-深圳梯队位置-用例.md`（第三轮 **FUNC-00956**～**FUNC-00963**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.sz-tier`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.sz-tier.main | GET | /entan/v1/svc/sz-tier | FUNC-00956～00958 | unavailable |
| svc.sz-tier.m_svc_sz_tier | POST | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | FUNC-00959～00961 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「深圳梯队」的 sampleResponse（`dims` 及元素 `dim`、`dim_key`、`tier`）与 responseFields 的 `dims` 都挂在主流程上；title「深圳梯队位置」的 sampleResponse（`metric_id`、`hint`）与 responseFields 的 `dims` 都挂在该接口主流程上。可选 `industry` 与 sample 相反的不传挂备选；每个参数恰好 1 条非法反向。`深圳梯队` catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| svc.sz-tier.main \| 深圳梯队 | FUNC-00956、00957、00958 | 无对应功能点 | 00956 主流程 sampleRequest industry=人工智能，断言 dims 及元素 dim、dim_key、tier（示例 机构数量/org_count/T1、技术力得分/tech_score/T2、服务链完整度/chain_coverage/T1）；00957 不传 industry；00958 非法 industry=__invalid__。文档标记未交付 |
| （无 Lxx） \| svc.sz-tier.m_svc_sz_tier \| 深圳梯队位置 | FUNC-00959、00960、00961 | 无对应功能点 | 00959 主流程 sampleRequest industry=人工智能，断言 metric_id=M_SVC_SZ_TIER、hint，以及 responseFields 的 dims；00960 不传 industry；00961 非法 industry=__invalid__ |
| （页面清单） \| svc.sz-tier \| 接口信息 / 算法测试 | FUNC-00962、00963 | 已覆盖 | 双接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 8 |
| 主流程 | 2（00956 深圳梯队、00959 深圳梯队位置） |
| 备选-参数组合 | 2（00957、00960） |
| 反向 | 2（00958、00961） |
| 清单 | 2（00962、00963） |
| 编号 | FUNC-00956～00963 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01722～01727 作废，见 FUNC 册 §4 |
