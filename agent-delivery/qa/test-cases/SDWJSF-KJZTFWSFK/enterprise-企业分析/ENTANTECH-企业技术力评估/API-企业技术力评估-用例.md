# 智能服务集群-科技专题服务算法库测试用例（企业技术力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业技术力评估  
> **catalog**：`entry_id=entan.tech` · `catalog_page_id=entan.tech` · path `/entan/tech`  
> **A 线对照**：`fp-split-by-api-run/work/L31.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境标识**：50897（不写入步骤）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 企业技术力得分（企业集合） | entan.tech.rank | unavailable |
| 2 | 技术力详情 | entan.tech.detail | unavailable |
| 3 | 模型权重 | entan.tech.weights | unavailable |
| 4 | 评估报告 | entan.tech.report | unavailable |
| 5 | 技术影响力评估 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | available |

**试调取值**（catalog `sampleRequest`）：`enterprise_codes` 为 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`；`orgId` 为 `0218337e44ca794fee9850cf1627b03b`；`model` 为 `tech_power`。

本页 JSON 共 **5** 个 endpoint。每个接口仅 1 个必填参数、无可选参数：1 条主流程 + 1 条反向。`unavailable` 仍按文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00966**～**API-00975**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.tech`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00966 | 企业分析 | 企业技术力评估 | 主流程 | — | 企业技术力评估 | 企业技术力得分（企业集合） | 企业技术力得分（企业集合）按文档示例 enterprise_codes 计算 | 1、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，组合RANK-01 | 1、返回 body 含 metric_id（string）、metric_name_zh（string）、data_source（string）、confidence（string）；2、value 为对象，其中 enterprises 为数组（responseFields 企业技术力得分明细）；3、元素含 org_id（string）、enterprise_name（string）、tech_power_index（number）、talent_score（number）、innovation_score（number）、transfer_score（number）、cooperation_score（number）、investment_score（number）；4、calc_process 含 definition（string）、formula（string）、source_tables（string 数组）、model_version（string）；5、与 sampleResponse 一致（示例 metric_id=M_ENT_TECH_POWER_SCORE，metric_name_zh=企业技术力得分，data_source=real，confidence=high，formula=五维加权，model_version=entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=RANK-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00967 | 企业分析 | 企业技术力评估 | 异常-入参-缺enterprise_codes | — | 企业技术力评估 | 企业技术力得分（企业集合） | 企业技术力得分（企业集合）不传 enterprise_codes | 1、不传 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，组合RANK-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 tech_power_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=RANK-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00968 | 企业分析 | 企业技术力评估 | 主流程 | — | 企业技术力评估 | 技术力详情 | 技术力详情按文档示例 orgId 查询 | 1、orgId 使用文档示例 0218337e44ca794fee9850cf1627b03b | 1.GET /entan/v1/tech-power/{orgId}，路径参数取组合 DTL-01 | 1、返回 body 含 org_id（string）、enterprise_name（string）、talent_score（number，responseFields 人才得分）、innovation_score（number）、transfer_score（number）、cooperation_score（number）、investment_score（number）；2、trend 为数组（responseFields 年度趋势），元素含 year（number）、value（number）；3、与 sampleResponse 一致（示例 org_id=0218337e44ca794fee9850cf1627b03b，trend 含 year 2023/2024/2025） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=DTL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00969 | 企业分析 | 企业技术力评估 | 异常-入参-缺orgId | — | 企业技术力评估 | 技术力详情 | 技术力详情不传 orgId | 1、不传 orgId | 1.GET /entan/v1/tech-power/{orgId}，路径参数取组合 DTL-02 | 1、返回 body 的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 talent_score 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | | INTEG | | | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=DTL-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00970 | 企业分析 | 企业技术力评估 | 主流程 | — | 企业技术力评估 | 模型权重 | 模型权重按文档示例 model 查询 | 1、model 使用文档示例 tech_power | 1.GET /entan/v1/eval/weights，查询参数取组合 WGT-01 | 1、返回 body 为数组；2、元素含 name_zh（string）、weight（number，responseFields 权重）、description（string）；3、与 sampleResponse 一致（示例 name_zh=技术创新，weight=0.28，description=专利与论文） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=WGT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00971 | 企业分析 | 企业技术力评估 | 异常-入参-缺model | — | 企业技术力评估 | 模型权重 | 模型权重不传 model | 1、不传 model | 1.GET /entan/v1/eval/weights，查询参数取组合 WGT-02 | 1、返回 body 的 message 或 msg 说明 model 缺失或非法；2、不返回含 weight 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=WGT-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00972 | 企业分析 | 企业技术力评估 | 主流程 | — | 企业技术力评估 | 评估报告 | 评估报告按文档示例 orgId 查询 | 1、orgId 使用文档示例 0218337e44ca794fee9850cf1627b03b | 1.GET /entan/v1/enterprises/{orgId}/report，路径参数取组合 RPT-01 | 1、返回 body 含 markdown（string，responseFields 报告正文）；2、与 sampleResponse 一致（示例 markdown 为「# 技术力评估报告」） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=RPT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00973 | 企业分析 | 企业技术力评估 | 异常-入参-缺orgId | — | 企业技术力评估 | 评估报告 | 评估报告不传 orgId | 1、不传 orgId | 1.GET /entan/v1/enterprises/{orgId}/report，路径参数取组合 RPT-02 | 1、返回 body 的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 markdown 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=RPT-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00974 | 企业分析 | 企业技术力评估 | 主流程 | — | 企业技术力评估 | 技术影响力评估 | 技术影响力评估按文档示例 enterprise_codes 计算 | 1、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.POST /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute，组合INF-01 | 1、返回 body 含 metric_id（string）、hint（string）；2、responseFields 另声明 enterprises（array，企业技术力得分明细），sampleResponse 未展开元素字段，成功结果应含 enterprises；3、示例来自 sampleResponse：metric_id=M_ENT_DS_07_INDUSTRY_POTENTIAL_005，hint=compute 响应,以实际调用为准 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | M_ENT_DS_07_INDUSTRY_POTENTIAL_005 | INTEG | | | endpoint_id=entan.tech.rank.m_ent_ds_07_industry_potential_005 catalog_page_id=entan.tech 组合=INF-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00975 | 企业分析 | 企业技术力评估 | 异常-入参-缺enterprise_codes | — | 企业技术力评估 | 技术影响力评估 | 技术影响力评估不传 enterprise_codes | 1、不传 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute，组合INF-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 metric_id 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | | INTEG | | | endpoint_id=entan.tech.rank.m_ent_ds_07_industry_potential_005 catalog_page_id=entan.tech 组合=INF-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RANK-01 | entan.tech.rank | enterprise_codes=0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| RANK-02 | entan.tech.rank | 不传 enterprise_codes | 缺必填 enterprise_codes |
| DTL-01 | entan.tech.detail | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| DTL-02 | entan.tech.detail | 不传 orgId | 缺必填 orgId |
| WGT-01 | entan.tech.weights | model=tech_power | 主路径（sampleRequest） |
| WGT-02 | entan.tech.weights | 不传 model | 缺必填 model |
| RPT-01 | entan.tech.report | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| RPT-02 | entan.tech.report | 不传 orgId | 缺必填 orgId |
| INF-01 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | enterprise_codes=0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| INF-02 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业技术力得分（企业集合） | entan.tech.rank | POST | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | enterprise_codes* | unavailable |
| 技术力详情 | entan.tech.detail | GET | /entan/v1/tech-power/{orgId} | orgId* | unavailable |
| 模型权重 | entan.tech.weights | GET | /entan/v1/eval/weights | model* | unavailable |
| 评估报告 | entan.tech.report | GET | /entan/v1/enterprises/{orgId}/report | orgId* | unavailable |
| 技术影响力评估 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.tech.rank | API-00966、00967 |
| entan.tech.detail | API-00968、00969 |
| entan.tech.weights | API-00970、00971 |
| entan.tech.report | API-00972、00973 |
| entan.tech.rank.m_ent_ds_07_industry_potential_005 | API-00974、00975 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 5 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向 + 每参数恰好 1 条反向（本页均为单必填、无可选，无备选-参数组合）
- [x] unavailable（得分集合、详情、权重、报告）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 无鉴权类用例；反向预期为该参数的 message/msg，不单写状态码
- [x] `coverage-fp.md` 已同步 API-00966～00975

**统计**：用例 **10** 条（主流程 5、反向 5）；编号闭区间 **API-00966**～**API-00975**（父控 R2-批2 分配，连续无跳号）。
