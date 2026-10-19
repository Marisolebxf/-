# 服务机构管理 · A 线功能点覆盖（innov.service-org）

> **catalog_page_id**：`innov.service-org` · path `/innov/service-org`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-服务机构管理-用例.md`（第二轮 **API-02205**～**02210**，共 6 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.service-org`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.service-org.metrics | GET | /innov/v1/innov/metrics | API-02205、API-02206、API-02207 | unavailable |
| innov.service-org.m_innov_ds_29_incubator_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | API-02208、API-02209、API-02210 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传 `module` 挂备选；`module` 恰好 1 条非法反向。GET metrics 的 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.service-org.metrics \| 服务机构管理指标清单 | API-02205、API-02206、API-02207 | 无对应功能点 | 02205 主流程 sampleRequest（module=service-org），断言 metrics 元素 metric_id=M_INNOV_DS_29_INCUBATOR_006、name=影响力评价、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED 与 total=1；02206 不传 module；02207 非法 module。catalog status=unavailable |
| （无 Lxx） \| innov.service-org.m_innov_ds_29_incubator_006 \| 影响力评价 | API-02208、API-02209、API-02210 | 无对应功能点 | 02208 主流程 sampleRequest（module=service-org），断言 metric_id=M_INNOV_DS_29_INCUBATOR_006、hint，以及 responseFields 的 metrics、total；02209 不传 module；02210 非法 module |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 6 |
| 主流程 | 2 |
| 备选-参数组合 | 2（均不传 module） |
| 反向 | 2（均非法 module） |
| 编号 | API-02205～02210 连续 |
| A 线 Lxx | 无 |
