# 科技专题战略分析 · A 线功能点覆盖（innov.topic-strategy）

> **catalog_page_id**：`innov.topic-strategy` · path `/innov/topic-strategy`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-科技专题战略分析-用例.md`（第三轮 **FUNC-01479**～**01492**，共 14 条：接口 12 + 清单 2）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.topic-strategy`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | FUNC-01479、FUNC-01480、FUNC-01481 | running |
| innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | FUNC-01482、FUNC-01483、FUNC-01484 | available |
| innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | FUNC-01485、FUNC-01486、FUNC-01487 | available |
| innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | FUNC-01488、FUNC-01489、FUNC-01490 | available |
| （页面清单） | — | — | FUNC-01491、FUNC-01492 | — |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.topic-strategy.metrics · 科技专题战略分析指标清单 | FUNC-01479、FUNC-01480、FUNC-01481 | 无对应功能点 | 01479 主流程 sampleRequest module=topic-strategy，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 3 行）与 total=3；01480 不传 module，结构同类；01481 非法 module=__invalid__ |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_25_softsci_012 · 影响力评价与应用反馈 | FUNC-01482、FUNC-01483、FUNC-01484 | 无对应功能点 | 01482 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_25_SOFTSCI_012、hint，以及 responseFields 声明的 metrics、total；01483 不传 module；01484 非法 module=__invalid__ |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_26_eco_012 · 协同绩效与影响力智能评估 | FUNC-01485、FUNC-01486、FUNC-01487 | 无对应功能点 | 01485 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_26_ECO_012、hint，以及 responseFields 声明的 metrics、total；01486 不传 module；01487 非法 module=__invalid__ |
| （无 Lxx） · innov.topic-strategy.m_innov_ds_27_spatio_003 · 热点区域自动识别与预警 | FUNC-01488、FUNC-01489、FUNC-01490 | 无对应功能点 | 01488 主流程 sampleRequest module=topic-strategy，断言 metric_id=M_INNOV_DS_27_SPATIO_003、hint，以及 responseFields 声明的 metrics、total；01489 不传 module；01490 非法 module=__invalid__ |
| （页面清单） · 接口信息 / 算法测试 | FUNC-01491、FUNC-01492 | 无对应功能点 | §6.1 清单：4 接口下拉与 method/path 切换刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| FUNC 用例数 | 14 |
| 主流程 | 4（FUNC-01479、01482、01485、01488） |
| 备选-参数组合 | 4（FUNC-01480、01483、01486、01489） |
| 反向 | 4（FUNC-01481、01484、01487、01490） |
| 清单 | 2（FUNC-01491、01492） |
| 编号 | FUNC-01479～01492 连续 |
| A 线 Lxx | 无 |
| 作废 API 号 | API-02193～02204 不复用 |
