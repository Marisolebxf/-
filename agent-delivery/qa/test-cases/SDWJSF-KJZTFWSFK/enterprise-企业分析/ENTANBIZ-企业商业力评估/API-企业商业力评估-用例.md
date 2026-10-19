# 智能服务集群-科技专题服务算法库测试用例（企业商业力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业商业力评估  
> **catalog**：`entry_id=entan.biz` · `catalog_page_id=entan.biz` · path `/entan/biz`  
> **A 线对照**：`fp-split-by-api-run/work/L32.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批2）  
> **环境**：联调台 50897（本册不试调）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业商业力得分（企业集合） | entan.biz.rank |
| 2 | 商业力详情 | entan.biz.detail |
| 3 | 模型权重 | entan.biz.weights |
| 4 | 评估报告 | entan.biz.report |

**试调取值**（catalog `sampleRequest` / `example`）：`enterprise_codes` 为 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`；`orgId` 为 `0218337e44ca794fee9850cf1627b03b`；`model` 为 `biz_power`。四接口 `status=unavailable`，仍按文档请求与 sampleResponse 编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00976**～**API-00983**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.biz`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00976 | 企业分析 | 企业商业力评估 | 主流程 | — | 企业商业力评估 | 企业商业力得分（企业集合） | 企业商业力得分（企业集合）按文档示例 enterprise_codes 查询商业力得分 | 1、enterprise_codes 使用文档示例四码 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，组合RNK-01 | 1、返回 body 的 data 含 metric_id（string，sampleResponse 示例 M_ENT_BUSINESS_POWER_SCORE）、metric_name_zh（string，示例企业商业力得分）；2、value 为对象，enterprises 为数组（responseFields 企业商业力得分明细）；3、元素含 org_id（string）、enterprise_name（string）、biz_power_index（number）、market_score（number）、product_score（number）、brand_score（number）、cooperation_score（number）、chain_coverage_score（number）、chain_keynode_score（number）；4、data_source（string）、confidence（string）；5、calc_process 含 definition（string）、formula（string）、source_tables（string 数组）、model_version（string） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=RNK-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00977 | 企业分析 | 企业商业力评估 | 异常-入参-缺enterprise_codes | — | 企业商业力评估 | 企业商业力得分（企业集合） | 企业商业力得分（企业集合）不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，组合RNK-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 biz_power_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=RNK-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00978 | 企业分析 | 企业商业力评估 | 主流程 | — | 企业商业力评估 | 商业力详情 | 商业力详情按文档示例 orgId 查询六维得分与趋势 | 1、orgId 使用文档示例 0218337e44ca794fee9850cf1627b03b | 1.GET /entan/v1/biz-power/{orgId}，路径取组合 DTL-01 | 1、返回 body 的 data 含 market_score（number，responseFields 市场得分）、product_score（number）、brand_score（number）、cooperation_score（number）、chain_coverage_score（number）、chain_keynode_score（number）；2、trend 为数组，元素含 year（number）、value（number）；3、与 sampleResponse 一致（示例 market_score=90、product_score=88、brand_score=82、cooperation_score=79、chain_coverage_score=84、chain_keynode_score=76、year=2024、value=86） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=DTL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00979 | 企业分析 | 企业商业力评估 | 异常-入参-缺orgId | — | 企业商业力评估 | 商业力详情 | 商业力详情不传 orgId | 1、路径不提供 orgId | 1.GET /entan/v1/biz-power/{orgId}，路径取组合 DTL-02 | 1、返回 body 的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 market_score 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=DTL-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00980 | 企业分析 | 企业商业力评估 | 主流程 | — | 企业商业力评估 | 模型权重 | 模型权重按文档示例 model=biz_power 查询 | 1、model 使用文档示例 biz_power | 1.GET /entan/v1/eval/weights，查询参数取组合 WGT-01 | 1、返回 body 的 data 为数组（sampleResponse 即为数组）；2、元素含 name_zh（string）、weight（number，responseFields 权重）、description（string）；3、与 sampleResponse 一致（示例 name_zh=市场、weight=0.22、description=市场份额） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=WGT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00981 | 企业分析 | 企业商业力评估 | 异常-入参-缺model | — | 企业商业力评估 | 模型权重 | 模型权重不传 model | 1、不传 model | 1.GET /entan/v1/eval/weights，查询参数取组合 WGT-02 | 1、返回 body 的 message 或 msg 说明 model 缺失或非法；2、不返回含 weight 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=WGT-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00982 | 企业分析 | 企业商业力评估 | 主流程 | — | 企业商业力评估 | 评估报告 | 评估报告按文档示例 orgId 查询报告正文 | 1、orgId 使用文档示例 0218337e44ca794fee9850cf1627b03b | 1.GET /entan/v1/enterprises/{orgId}/report，路径取组合 RPT-01 | 1、返回 body 的 data 含 markdown（string，responseFields 报告正文）；2、与 sampleResponse 一致（示例 markdown 为商业力评估报告标题文本） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=RPT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00983 | 企业分析 | 企业商业力评估 | 异常-入参-缺orgId | — | 企业商业力评估 | 评估报告 | 评估报告不传 orgId | 1、路径不提供 orgId | 1.GET /entan/v1/enterprises/{orgId}/report，路径取组合 RPT-02 | 1、返回 body 的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 markdown 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=RPT-02 catalog_status=unavailable |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | entan.biz.rank | enterprise_codes=0218337e44ca794fee9850cf1627b03b、05dc8024336db695425572625773381b、0551ccfde6aa2b3c52e647e283204040、05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| RNK-02 | entan.biz.rank | 不传 enterprise_codes | 缺必填 enterprise_codes |
| DTL-01 | entan.biz.detail | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| DTL-02 | entan.biz.detail | 不传 orgId | 缺必填 orgId |
| WGT-01 | entan.biz.weights | model=biz_power | 主路径（sampleRequest） |
| WGT-02 | entan.biz.weights | 不传 model | 缺必填 model |
| RPT-01 | entan.biz.report | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| RPT-02 | entan.biz.report | 不传 orgId | 缺必填 orgId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业商业力得分（企业集合） | entan.biz.rank | POST | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | enterprise_codes* | unavailable |
| 商业力详情 | entan.biz.detail | GET | /entan/v1/biz-power/{orgId} | orgId* | unavailable |
| 模型权重 | entan.biz.weights | GET | /entan/v1/eval/weights | model* | unavailable |
| 评估报告 | entan.biz.report | GET | /entan/v1/enterprises/{orgId}/report | orgId* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.biz.rank | API-00976、00977 |
| entan.biz.detail | API-00978、00979 |
| entan.biz.weights | API-00980、00981 |
| entan.biz.report | API-00982、00983 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 每接口仅 1 个必填参数、无可选参数：文档示例正向 1 条 + 该参数反向 1 条；无备选-参数组合
- [x] unavailable 四接口仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 反向预期为该参数的 message/msg 说明，不写传输层状态码
- [x] `coverage-fp.md` 已同步 API-00976～00983
- [x] rank 两条步骤 73 字：path 本身 58 字，加上 METHOD 与组合 id 无法再压到 60 且仍写出 path；其余 6 条步骤 ≤60 字

**统计**：用例 **8** 条（主流程 4、反向 4）；编号闭区间 **API-00976**～**API-00983**（父控 R2-批2 分配）。
