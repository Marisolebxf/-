# 智能服务集群-科技专题服务算法库测试用例（企业成长与产业匹配 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业成长与产业匹配  
> **catalog**：`entry_id=entan.growth-match` · `catalog_page_id=entan.growth-match` · path `/entan/growth-match`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.growth-match`，原因「不扩六级」；不改 `work/`，不按 `field_key` 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批4）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 成长潜力（企业集合） | entan.growth-match.potential | unavailable |
| 2 | 产业匹配度（企业集合） | entan.growth-match.match | unavailable |
| 3 | M_ENT_AGGLOMERATION_INDEX | entan.growth-match.potential.m_ent_agglomeration_index | available |
| 4 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | available |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（附录 A 引用该组）。

清单以 `lumen-ui-algo-apiview/src/catalog/entan.json` 该页 `endpoints[]` 为准（4 个 title）。as-built yaml 的 `endpoint_count: 2` 为旧计数，本册不采用。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01149**～**API-01156**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.growth-match`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01149 | 企业分析 | 企业成长与产业匹配 | 主流程 | — | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力（企业集合）按文档 sampleRequest 的 enterprise_codes 返回示例字段 | 1、enterprise_codes 使用文档 sampleRequest 四元组 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 POT-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_ENT_GROWTH_POTENTIAL）、metric_name_zh（string，示例 成长潜力）；2、value 在 sampleResponse 中为对象，内含 value（number，示例 72.5）、dimensions（object：market_expand number 示例 68.0、profit_growth number 示例 74.0、asset_accumulate number 示例 76.0）、hint（string，示例 mock 阶段数据，三维等权重与行业均值比较（Q015 待补））；3、responseFields 声明 value 为 number（成长潜力得分）；4、data_source（string，示例 mock）、confidence（string，示例 medium）；5、calc_process 为对象，含 definition（string，示例 成长潜力）、formula（string，示例 市场扩张/利润增长/资产积累三维等权）、source_tables（array，示例含 成长潜力缺口表）、model_version（string，示例 entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | M_ENT_GROWTH_POTENTIAL | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=POT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01150 | 企业分析 | 企业成长与产业匹配 | 异常-入参-缺enterprise_codes | — | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力（企业集合）不传 enterprise_codes | 1、无 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 POT-02 | 1、返回 body 的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_GROWTH_POTENTIAL 且带 value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=POT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01151 | 企业分析 | 企业成长与产业匹配 | 主流程 | — | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度（企业集合）按文档 sampleRequest 的 enterprise_codes 返回示例字段 | 1、enterprise_codes 使用文档 sampleRequest 四元组 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 MAT-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_ENT_INDUSTRY_MATCH_SCORE）、metric_name_zh（string，示例 产业匹配度）；2、value 在 sampleResponse 中为对象，内含 value（number，示例 0.82）、upstream_degree（number，示例 2.4）、centroid_degree（number，示例 0.71）、chain_relevance（number，示例 1.15）、hint（string，示例 mock 阶段数据，依赖投入产出表上游度/质心度（Q015 待补））；3、responseFields 声明 value 为 number（产业匹配度）；4、data_source（string，示例 mock）、confidence（string，示例 medium）；5、calc_process 为对象，含 definition（string，示例 产业匹配度）、formula（string，示例 上游度/质心度/产业链相关性）、source_tables（array，示例含 投入产出表）、model_version（string，示例 entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | M_ENT_INDUSTRY_MATCH_SCORE | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=MAT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01152 | 企业分析 | 企业成长与产业匹配 | 异常-入参-缺enterprise_codes | — | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度（企业集合）不传 enterprise_codes | 1、无 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 MAT-02 | 1、返回 body 的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_INDUSTRY_MATCH_SCORE 且带 value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=MAT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01153 | 企业分析 | 企业成长与产业匹配 | 主流程 | — | 企业成长与产业匹配 | M_ENT_AGGLOMERATION_INDEX | M_ENT_AGGLOMERATION_INDEX 按文档 sampleRequest 的 enterprise_codes 返回示例字段 | 1、enterprise_codes 使用文档 sampleRequest 四元组 | 1.POST /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute，请求体取组合 AGG-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_ENT_AGGLOMERATION_INDEX）、hint（string，示例 compute 响应,以实际调用为准）；2、responseFields 声明 value 为 number（成长潜力得分）；3、sampleResponse 未给出 value 示例值，返回中应出现 responseFields 所列 value | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | M_ENT_AGGLOMERATION_INDEX | INTEG | | | endpoint_id=entan.growth-match.potential.m_ent_agglomeration_index catalog_page_id=entan.growth-match 组合=AGG-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01154 | 企业分析 | 企业成长与产业匹配 | 异常-入参-缺enterprise_codes | — | 企业成长与产业匹配 | M_ENT_AGGLOMERATION_INDEX | M_ENT_AGGLOMERATION_INDEX 不传 enterprise_codes | 1、无 | 1.POST /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute，请求体取组合 AGG-02 | 1、返回 body 的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_AGGLOMERATION_INDEX 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | | INTEG | | | endpoint_id=entan.growth-match.potential.m_ent_agglomeration_index catalog_page_id=entan.growth-match 组合=AGG-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01155 | 企业分析 | 企业成长与产业匹配 | 主流程 | — | 企业成长与产业匹配 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 按文档 sampleRequest 的 enterprise_codes 返回示例字段 | 1、enterprise_codes 使用文档 sampleRequest 四元组 | 1.POST /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute，请求体取组合 IND-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_ENT_DS_07_INDUSTRY_POTENTIAL_006）、hint（string，示例 compute 响应,以实际调用为准）；2、responseFields 声明 value 为 number（成长潜力得分）；3、sampleResponse 未给出 value 示例值，返回中应出现 responseFields 所列 value | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | INTEG | | | endpoint_id=entan.growth-match.potential.m_ent_ds_07_industry_potential_006 catalog_page_id=entan.growth-match 组合=IND-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01156 | 企业分析 | 企业成长与产业匹配 | 异常-入参-缺enterprise_codes | — | 企业成长与产业匹配 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 不传 enterprise_codes | 1、无 | 1.POST /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute，请求体取组合 IND-02 | 1、返回 body 的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_DS_07_INDUSTRY_POTENTIAL_006 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | | INTEG | | | endpoint_id=entan.growth-match.potential.m_ent_ds_07_industry_potential_006 catalog_page_id=entan.growth-match 组合=IND-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| POT-01 | entan.growth-match.potential | enterprise_codes=["0218337e44ca794fee9850cf1627b03b","05dc8024336db695425572625773381b","0551ccfde6aa2b3c52e647e283204040","05ff69620c962ce3bbb852351f077299"] | 主路径全参（sampleRequest） |
| POT-02 | entan.growth-match.potential | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| MAT-01 | entan.growth-match.match | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| MAT-02 | entan.growth-match.match | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| AGG-01 | entan.growth-match.potential.m_ent_agglomeration_index | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| AGG-02 | entan.growth-match.potential.m_ent_agglomeration_index | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| IND-01 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| IND-02 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 成长潜力（企业集合） | entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | enterprise_codes* | unavailable |
| 产业匹配度（企业集合） | entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | enterprise_codes* | unavailable |
| M_ENT_AGGLOMERATION_INDEX | entan.growth-match.potential.m_ent_agglomeration_index | POST | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | enterprise_codes* | available |
| M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.growth-match.potential | API-01149、01150 |
| entan.growth-match.match | API-01151、01152 |
| entan.growth-match.potential.m_ent_agglomeration_index | API-01153、01154 |
| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | API-01155、01156 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现且各有 1 条主流程（功能项=主流程）
- [x] 每接口仅必填 enterprise_codes：正向 1 条（sampleRequest）+ 反向 1 条（缺该参数）；无可选参数，不另写备选
- [x] unavailable（成长潜力、产业匹配度）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse（含嵌套）与 responseFields；反向预期为 message 或 msg 指出缺少 enterprise_codes
- [x] 无对应 Lxx，不改 work，不按 field_key 一行一用例
- [x] `coverage-fp.md` 已同步 API-01149～01156

**统计**：用例 **8** 条（主流程 **4**、反向 **4**）；编号闭区间 **API-01149**～**API-01156**（父控 R2-批4 分配，用满）。
