# 引育推荐（异步） · A 线功能点覆盖（innov.recommend）

> **catalog_page_id**：`innov.recommend` · path `/innov/recommend`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-引育推荐（异步）-用例.md`（第三轮 **FUNC-01170**～**01175**，共 6 条：接口 4 + 清单 2）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.recommend`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.recommend.attraction | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | FUNC-01170、FUNC-01171 | running |
| innov.recommend.cultivation | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | FUNC-01172、FUNC-01173 | running |

页面清单：**FUNC-01174**（接口信息）、**FUNC-01175**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选 `enterprise_codes` 不写备选；必填 `sub_type` 反向为省略该参数。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.recommend.attraction \| 招引推荐契约 | FUNC-01170、FUNC-01171 | 无对应功能点 | 01170 主流程 sampleRequest（sub_type=attraction、enterprise_codes 文档两码），断言 task_id、candidate_count、weights（technology_match、growth、regional_fit）、rankings（rank、enterprise_name、recommendation_score、industry_domain、geographic_source）；01171 省略必填 sub_type |
| （无 Lxx） \| innov.recommend.cultivation \| 培育推荐契约 | FUNC-01172、FUNC-01173 | 无对应功能点 | 01172 主流程 sampleRequest（sub_type=cultivation、enterprise_codes 文档两码），断言 task_id、candidate_count、rankings（rank、enterprise_name、recommendation_score、industry_category、enterprise_scale、development_bottleneck）；01173 省略必填 sub_type |
| （页面清单） | FUNC-01174、FUNC-01175 | 无对应功能点 | 双接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6 |
| 主流程 | 2（01170 招引推荐契约、01172 培育推荐契约） |
| 备选-参数组合 | 0 |
| 反向 | 2（01171、01173，均省略 sub_type） |
| 清单 | 2（01174、01175） |
| 编号 | FUNC-01170～01175 连续 |
| A 线 Lxx | 无 |
| 已作废 | API-01898～01901（第二轮 API 册已删） |
