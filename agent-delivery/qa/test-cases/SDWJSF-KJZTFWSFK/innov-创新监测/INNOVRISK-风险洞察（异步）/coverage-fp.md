# 风险洞察（异步） · A 线功能点覆盖（innov.risk）

> **catalog_page_id**：`innov.risk` · path `/innov/risk`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-风险洞察（异步）-用例.md`（第三轮 **FUNC-01164**～**01169**，共 6 条：接口 4 + 清单 2）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.risk`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.risk.supply | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | FUNC-01164、FUNC-01165 | running |
| innov.risk.pain | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | FUNC-01166、FUNC-01167 | running |
| （页面清单） | — | — | FUNC-01168、FUNC-01169 | — |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选 `enterprise_codes` 随 sampleRequest 全参写在主流程，不单开备选；必填 `sub_type` 反向为省略该参数。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.risk.supply \| 供应链风险图谱契约 | FUNC-01164、FUNC-01165 | 无对应功能点 | 01164 主流程 sampleRequest（sub_type=supply_chain、enterprise_codes 双码），断言 summary（display_mode、data_time、enterprises）、nodes（id、name、relation_type、influence_score、is_key）、edges（src、dst、relation_type）、key_nodes（name、relation_type、influence_score、is_key、suggestion）、break_risks（name、risk_level、impact、suggestion）；01165 省略必填 sub_type |
| （无 Lxx） \| innov.risk.pain \| 发展痛难点契约 | FUNC-01166、FUNC-01167 | 无对应功能点 | 01166 主流程 sampleRequest（sub_type=pain_points、enterprise_codes 双码），断言 summary（diagnosis_method、data_time）、dimension_cards（dimension、priority、issue_count、affected_enterprise_count）、issues（title、priority、dimension、affected_enterprise_count、evidence）；01167 省略必填 sub_type |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-01168、FUNC-01169 | 无对应功能点 | §6.1 清单：2 接口下拉与 method/path 切换刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6 |
| 主流程 | 2（01164 供应链风险图谱契约、01166 发展痛难点契约） |
| 备选-参数组合 | 0 |
| 反向 | 2（01165、01167，均省略 sub_type） |
| 清单 | 2（01168、01169） |
| 编号 | FUNC-01164～01169 连续 |
| A 线 Lxx | 无 |
| 作废 API 号 | API-01894～01897 不复用 |
