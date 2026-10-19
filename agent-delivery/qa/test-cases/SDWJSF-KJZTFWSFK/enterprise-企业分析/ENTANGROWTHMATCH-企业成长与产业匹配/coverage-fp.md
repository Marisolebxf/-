# 企业成长与产业匹配 · 功能点覆盖（entan.growth-match）

> catalog `entan.growth-match` · path `/entan/growth-match`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.growth-match`（原因：不扩六级）。不改 `work/`。  
> B 线用例：`API-企业成长与产业匹配-用例.md`（第二轮 **API-01149**～**01156**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | API-01149、01150 | unavailable |
| entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | API-01151、01152 | unavailable |
| entan.growth-match.potential.m_ent_agglomeration_index | POST | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | API-01153、01154 | available |
| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | API-01155、01156 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse（含嵌套）与 responseFields 都挂在该接口的主流程上；缺 `enterprise_codes` 挂在同接口的反向用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.growth-match.potential \| 成长潜力（企业集合） | API-01149、01150 | 无对应功能点 | 01149 主流程按 sampleResponse 与 responseFields 写返回体；01150 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.growth-match.match \| 产业匹配度（企业集合） | API-01151、01152 | 无对应功能点 | 01151 主流程；01152 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.growth-match.potential.m_ent_agglomeration_index \| M_ENT_AGGLOMERATION_INDEX | API-01153、01154 | 无对应功能点 | 01153 主流程；01154 缺 enterprise_codes。catalog status=available |
| （无 Lxx） \| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 \| M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | API-01155、01156 | 无对应功能点 | 01155 主流程；01156 缺 enterprise_codes。catalog status=available |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4（JSON；yaml `endpoint_count: 2` 为旧计数） |
| title 数 | 4 |
| API 用例数 | 8 |
| 主流程 | 4（API-01149、01151、01153、01155） |
| 反向 | 4（API-01150、01152、01154、01156） |
| 编号 | API-01149～01156 |
| A 线 Lxx | 无 |
