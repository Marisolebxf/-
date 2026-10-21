# 企业成长与产业匹配 · 功能点覆盖（entan.growth-match）

> catalog `entan.growth-match` · path `#/entan/growth-match`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.growth-match`（原因：不扩六级）。不改 `work/`。  
> B 线用例：`FUNC-企业成长与产业匹配-用例.md`（第三轮 **FUNC-00332**～**00341**；旧 API-01149～01156 作废）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | FUNC-00332、00333 | unavailable |
| entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | FUNC-00334、00335 | unavailable |
| entan.growth-match.potential.m_ent_agglomeration_index | POST | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | FUNC-00336、00337 | available |
| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | FUNC-00338、00339 | available |
| （页面清单） | — | — | FUNC-00340、00341 | — |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse（含嵌套）与 responseFields 都挂在该接口的主流程上；缺 `enterprise_codes` 挂在同接口的反向用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.growth-match.potential \| 成长潜力（企业集合） | FUNC-00332、00333 | 无对应功能点 | 00332 主流程按 sampleResponse 与 responseFields 写返回体；00333 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.growth-match.match \| 产业匹配度（企业集合） | FUNC-00334、00335 | 无对应功能点 | 00334 主流程；00335 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.growth-match.potential.m_ent_agglomeration_index \| M_ENT_AGGLOMERATION_INDEX | FUNC-00336、00337 | 无对应功能点 | 00336 主流程；00337 缺 enterprise_codes。catalog status=available |
| （无 Lxx） \| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 \| M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | FUNC-00338、00339 | 无对应功能点 | 00338 主流程；00339 缺 enterprise_codes。catalog status=available |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00340、00341 | 无对应功能点 | 下拉 4 项与 catalog title 一致；切换后概览/调用区刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| FUNC 用例数 | 10 |
| 主流程 | 4（FUNC-00332、00334、00336、00338） |
| 备选-参数组合 | 0 |
| 反向 | 4（FUNC-00333、00335、00337、00339） |
| 清单 | 2（FUNC-00340、00341） |
| 编号 | FUNC-00332～00341 |
| A 线 Lxx | 无 |
