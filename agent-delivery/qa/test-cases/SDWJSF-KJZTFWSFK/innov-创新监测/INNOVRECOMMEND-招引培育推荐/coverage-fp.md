# 引育推荐（异步） · A 线功能点覆盖（innov.recommend）

> **catalog_page_id**：`innov.recommend` · path `/innov/recommend`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-引育推荐（异步）-用例.md`（第二轮 **API-01898**～**01901**，共 4 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.recommend`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.recommend.attraction | POST | （空） | API-01898、API-01899 | unavailable |
| innov.recommend.cultivation | POST | （空） | API-01900、API-01901 | unavailable |

两个接口 path 以 catalog 为准，当前为空，步骤未填 URL。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；无其它参数，无备选；必填 `sub_type` 反向为省略该参数。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.recommend.attraction \| 招引推荐契约 | API-01898、API-01899 | 无对应功能点 | 01898 主流程 sampleRequest（sub_type=attraction），断言 task_id、candidate_count、weights（technology_match、growth、regional_fit）、rankings（rank、enterprise_name、recommendation_score、industry_domain、geographic_source）；01899 省略必填 sub_type |
| （无 Lxx） \| innov.recommend.cultivation \| 培育推荐契约 | API-01900、API-01901 | 无对应功能点 | 01900 主流程 sampleRequest（sub_type=cultivation），断言 task_id、candidate_count、rankings（rank、enterprise_name、recommendation_score、industry_category、enterprise_scale、development_bottleneck）；01901 省略必填 sub_type |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2（01898 招引推荐契约、01900 培育推荐契约） |
| 备选-参数组合 | 0 |
| 反向 | 2（01899、01901，均省略 sub_type） |
| 编号 | API-01898～01901 连续 |
| A 线 Lxx | 无 |
