# 风险洞察（异步） · A 线功能点覆盖（innov.risk）

> **catalog_page_id**：`innov.risk` · path `/innov/risk`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-风险洞察（异步）-用例.md`（第二轮 **API-01894**～**01897**，共 4 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.risk`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.risk.supply | POST | （空） | API-01894、API-01895 | unavailable |
| innov.risk.pain | POST | （空） | API-01896、API-01897 | unavailable |

两个接口 path 以 catalog 为准，当前为空，步骤未填 URL。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；无其它参数，无备选；必填 `sub_type` 反向为省略该参数。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.risk.supply \| 供应链风险图谱契约 | API-01894、API-01895 | 无对应功能点 | 01894 主流程 sampleRequest（sub_type=supply_chain），断言 summary（display_mode、data_time、enterprises）、nodes（id、name、relation_type、influence_score、is_key）、edges（src、dst、relation_type）、key_nodes（name、relation_type、influence_score、is_key、suggestion）、break_risks（name、risk_level、impact、suggestion）；01895 省略必填 sub_type |
| （无 Lxx） \| innov.risk.pain \| 发展痛难点契约 | API-01896、API-01897 | 无对应功能点 | 01896 主流程 sampleRequest（sub_type=pain_points），断言 summary（diagnosis_method、data_time）、dimension_cards（dimension、priority、issue_count、affected_enterprise_count）、issues（title、priority、dimension、affected_enterprise_count、evidence）；01897 省略必填 sub_type |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2（01894 供应链风险图谱契约、01896 发展痛难点契约） |
| 备选-参数组合 | 0 |
| 反向 | 2（01895、01897，均省略 sub_type） |
| 编号 | API-01894～01897 连续 |
| A 线 Lxx | 无 |
