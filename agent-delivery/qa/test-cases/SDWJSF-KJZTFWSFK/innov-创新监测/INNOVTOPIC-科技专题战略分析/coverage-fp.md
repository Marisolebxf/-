# 科技专题战略分析 · A 线功能点覆盖（innov.topic-strategy）

> **catalog_page_id**：`innov.topic-strategy` · path `/innov/topic-strategy`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-科技专题战略分析-用例.md`（第二轮 **API-02193**～**02204**，共 12 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.topic-strategy`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | API-02193、API-02194、API-02195 | unavailable |
| innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | API-02196、API-02197、API-02198 | available |
| innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | API-02199、API-02200、API-02201 | available |
| innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | API-02202、API-02203、API-02204 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.topic-strategy.metrics · 科技专题战略分析指标清单 | API-02193、API-02194、API-02195 | 无对应功能点 | API-02193 主流程 sampleRequest module=topic-strategy，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 3 行）与 total=3；API-02194 不传 module，结构同类；API-02195 非法 module=__invalid__。catalog status=unavailable，备注未交付 |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_25_softsci_012 · 影响力评价与应用反馈 | API-02196、API-02197、API-02198 | 无对应功能点 | API-02196 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_25_SOFTSCI_012、hint，以及 responseFields 声明的 metrics、total；API-02197 不传 module；API-02198 非法 module=__invalid__ |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_26_eco_012 · 协同绩效与影响力智能评估 | API-02199、API-02200、API-02201 | 无对应功能点 | API-02199 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_26_ECO_012、hint，以及 responseFields 声明的 metrics、total；API-02200 不传 module；API-02201 非法 module=__invalid__ |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_27_spatio_003 · 热点区域自动识别与预警 | API-02202、API-02203、API-02204 | 无对应功能点 | API-02202 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_27_SPATIO_003、hint，以及 responseFields 声明的 metrics、total；API-02203 不传 module；API-02204 非法 module=__invalid__ |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| API 用例数 | 12 |
| 主流程 | 4（API-02193、API-02196、API-02199、API-02202） |
| 备选-参数组合 | 4（API-02194、API-02197、API-02200、API-02203） |
| 反向 | 4（API-02195、API-02198、API-02201、API-02204） |
| 编号 | API-02193～02204 连续用满 |
| A 线 Lxx | 无 |
