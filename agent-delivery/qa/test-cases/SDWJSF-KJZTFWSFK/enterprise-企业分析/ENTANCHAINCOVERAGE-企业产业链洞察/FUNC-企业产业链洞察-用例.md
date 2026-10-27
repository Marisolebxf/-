# 智能服务集群-科技专题服务算法库测试用例（企业产业链洞察 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业产业链洞察  
> **catalog**：`entry_id=entan.chain-coverage` · `catalog_page_id=entan.chain-coverage` · path `#/entan/chain-coverage`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.chain-coverage`  
> **A 线对照**：无对应 Lxx（`_l6-to-catalog-map.yaml` catalog_skip `entan.chain-coverage`，reason 不扩六级；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批5；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 重点企业全景图（企业集合） | entan.chain-coverage.keypano |
| 2 | 多元化指数（企业集合） | entan.chain-coverage.diversification |
| 3 | 领域覆盖深度（企业集合） | entan.chain-coverage.coverage-depth |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（可替换为环境有效企业标识，附录组合表引用该组）。

本页 3 个接口均只有必填 `enterprise_codes`，无可选参数。每接口 1 条主流程（sampleRequest 全参）+ 1 条反向（缺 `enterprise_codes`）。三接口 catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00324**～**FUNC-00331**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.chain-coverage`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00324 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 重点企业全景图（企业集合） | 验证重点企业全景图（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回全景覆盖率等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「重点企业全景图（企业集合）」；4.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_KEYPANO_DOMAIN_SUMMARY）、metric_name_zh（string，示例重点企业全景图）；2、value 为 object，含 coverage_rate（number，responseFields 全景覆盖率，示例 0.68）、evidence_level（string，示例证据充分）、mapped_keywords（number，示例 17）、total_keywords（number，示例 25）、domain_summary（string，示例 mock 阶段数据，依赖 dwd_paper_base/dwd_patent_base 关键词抽取与领域映射（Q013 待补））；3、data_source（string，示例 mock）、confidence（string，示例 medium）；4、calc_process 为 object，含 definition（string，示例重点企业全景图）、formula（string，示例关键词映射覆盖率）、source_tables（string 数组，示例 dwd_paper_base、dwd_patent_base）、model_version（string，示例 entan-v1.0）。示例文案与数值说明 sampleResponse 形态，字段与结构须与文档一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | M_ENT_KEYPANO_DOMAIN_SUMMARY | INTEG |  | FUNC-00324 | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=KPN-01 catalog_status=unavailable 场景=主流程 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00325 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 重点企业全景图（企业集合） | 验证重点企业全景图（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「重点企业全景图（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 coverage_rate 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute |  | INTEG |  | FUNC-00325 | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=KPN-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00326 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 多元化指数（企业集合） | 验证多元化指数（企业集合）功能，检查填写 enterprise_codes 同 KPN-01 后返回多元化指数等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「多元化指数（企业集合）」；4.填写 enterprise_codes 同 KPN-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_DIVERSIFICATION_INDEX）、metric_name_zh（string，示例多元化指数）；2、value 为 object，含 value（number，responseFields 多元化指数，示例 0.68）、node_count（number，示例 12）、hint（string，示例 mock 阶段数据，基于 dwd_org_industry_tags 节点占比香农熵（Q013 待补））；3、data_source（string，示例 mock）、confidence（string，示例 medium）；4、calc_process 为 object，含 definition（string，示例多元化指数）、formula（string，示例产业节点占比香农熵）、source_tables（string 数组，示例 dwd_org_industry_tags）、model_version（string，示例 entan-v1.0）。示例文案与数值说明 sampleResponse 形态，字段与结构须与文档一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | M_ENT_DIVERSIFICATION_INDEX | INTEG |  | FUNC-00326 | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=DIV-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00327 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 多元化指数（企业集合） | 验证多元化指数（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「多元化指数（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 value.value 与 node_count 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute |  | INTEG |  | FUNC-00327 | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=DIV-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00328 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 验证领域覆盖深度（企业集合）功能，检查填写 enterprise_codes 同 KPN-01 后返回领域覆盖深度等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「领域覆盖深度（企业集合）」；4.填写 enterprise_codes 同 KPN-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_DOMAIN_COVERAGE_DEPTH）、metric_name_zh（string，示例领域覆盖深度）；2、value 为 object，含 value（number，responseFields 领域覆盖深度，示例 0.75）、max_level（number，示例 4）、hint（string，示例 mock 阶段数据，命中节点最大层级/产业链最大层级（Q013 待补））；3、data_source（string，示例 mock）、confidence（string，示例 medium）；4、calc_process 为 object，含 definition（string，示例领域覆盖深度）、formula（string，示例命中节点最大层级占比）、source_tables（string 数组，示例产业链层级表）、model_version（string，示例 entan-v1.0）。示例文案与数值说明 sampleResponse 形态，字段与结构须与文档一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | M_ENT_DOMAIN_COVERAGE_DEPTH | INTEG |  | FUNC-00328 | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=DEP-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00329 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 验证领域覆盖深度（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换至「算法测试」tab；3.接口下拉选择「领域覆盖深度（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 value.value 与 max_level 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute |  | INTEG |  | FUNC-00329 | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=DEP-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00330 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 接口信息 | 验证企业产业链洞察的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应重点企业全景图（企业集合） POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute；4、切换后概览对应多元化指数 POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00330 | catalog_page_id=entan.chain-coverage 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00331 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业产业链洞察 | 算法测试 | 验证企业产业链洞察的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业产业链洞察」；2.切换到「算法测试」tab；3.下拉切换到「领域覆盖深度（企业集合）」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「领域覆盖深度（企业集合）」；3、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00331 | catalog_page_id=entan.chain-coverage 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| KPN-01 | entan.chain-coverage.keypano | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| KPN-02 | entan.chain-coverage.keypano | 不传 enterprise_codes | 缺必填 enterprise_codes |
| DIV-01 | entan.chain-coverage.diversification | enterprise_codes 同 KPN-01 | 主路径全参（sampleRequest） |
| DIV-02 | entan.chain-coverage.diversification | 不传 enterprise_codes | 缺必填 enterprise_codes |
| DEP-01 | entan.chain-coverage.coverage-depth | enterprise_codes 同 KPN-01 | 主路径全参（sampleRequest） |
| DEP-02 | entan.chain-coverage.coverage-depth | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 重点企业全景图（企业集合） | entan.chain-coverage.keypano | POST | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | enterprise_codes* | unavailable |
| 多元化指数（企业集合） | entan.chain-coverage.diversification | POST | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | enterprise_codes* | unavailable |
| 领域覆盖深度（企业集合） | entan.chain-coverage.coverage-depth | POST | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | enterprise_codes* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.chain-coverage.keypano | FUNC-00324、00325 |
| entan.chain-coverage.diversification | FUNC-00326、00327 |
| entan.chain-coverage.coverage-depth | FUNC-00328、00329 |
| （页面清单） | FUNC-00330、00331 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参 1 条主流程；必填 enterprise_codes 恰好 1 条反向；无可选参数，无备选-参数组合
- [x] 三接口 unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规（catalog_skip 不扩六级）
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（多接口页含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00324～00331

**统计**：接口 **3**；主流程 **3**；反向 **3**；清单 **2**；合计 **8** 条；编号闭区间 **FUNC-00324**～**FUNC-00331**（父控 R3-批5 分配）。
