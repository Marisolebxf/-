# 智能服务集群-科技专题服务算法库测试用例（招引企业综合推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 招引企业综合推荐  
> **catalog**：`entry_id=entan.attract` · `catalog_page_id=entan.attract` · path `/entan/attract`  
> **A 线对照**：`fp-split-by-api-run/work/L33.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境标识**：50897（不写入步骤）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批3）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 招引企业推荐指数（企业集合） | entan.attract.recommend | unavailable |
| 2 | 政策匹配度 | entan.attract.recommend.m_ent_policy_match_score | available |

**试调取值**（catalog `sampleRequest`）：`enterprise_codes` 为 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`。

本页 JSON 共 **2** 个 endpoint。每个接口仅必填 `enterprise_codes`、无可选参数：1 条主流程 + 1 条反向。`unavailable` 仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00984**～**API-00987**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.attract`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00984 | 企业分析 | 招引企业综合推荐 | 主流程 | — | 招引企业综合推荐 | 招引企业推荐指数（企业集合） | 招引企业推荐指数（企业集合）按文档示例 enterprise_codes 计算 | 1、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.POST /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute，请求体取组合 ATR-01 | 1、返回 body 含 metric_id（string，示例 M_ENT_ATTRACTION_INDEX）、metric_name_zh（string，示例招引推荐指数）、data_source（string，示例 real）、confidence（string，示例 high）；2、value 为对象，value.result 含 sub_type（string，示例 attraction）、candidate_count（number，示例 2）；3、value.result.weights 含 technology_match（number，示例 40）、growth（number，示例 35）、regional_fit（number，示例 25）；4、value.result.rankings 为数组（responseFields 名 rankings，招引推荐清单），元素含 enterprise_code（string）、enterprise_name（string）、rank（number）、industry_domain（string）、geographic_source（string）、target_traits（string 数组）、recommendation_score（number）；5、calc_process 含 definition（string，示例招引推荐指数）、formula（string，示例技术匹配/成长性/区域适配加权）、source_tables（string 数组，示例 innov.analysis.attraction）、model_version（string，示例 entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | M_ENT_ATTRACTION_INDEX | INTEG | | | endpoint_id=entan.attract.recommend catalog_page_id=entan.attract 组合=ATR-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00985 | 企业分析 | 招引企业综合推荐 | 异常-入参-缺enterprise_codes | — | 招引企业综合推荐 | 招引企业推荐指数（企业集合） | 招引企业推荐指数（企业集合）不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute，请求体取组合 ATR-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 recommendation_score 与 rankings 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | | INTEG | | | endpoint_id=entan.attract.recommend catalog_page_id=entan.attract 组合=ATR-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00986 | 企业分析 | 招引企业综合推荐 | 主流程 | — | 招引企业综合推荐 | 政策匹配度 | 政策匹配度按文档示例 enterprise_codes 计算 | 1、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.POST /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute，请求体取组合 POL-01 | 1、返回 body 含 metric_id（string，sampleResponse 示例 M_ENT_POLICY_MATCH_SCORE）、hint（string，示例 compute 响应,以实际调用为准）；2、responseFields 声明 rankings（array，招引推荐清单），sampleResponse 未展开元素字段，成功结果应含 rankings | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | M_ENT_POLICY_MATCH_SCORE | INTEG | | | endpoint_id=entan.attract.recommend.m_ent_policy_match_score catalog_page_id=entan.attract 组合=POL-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00987 | 企业分析 | 招引企业综合推荐 | 异常-入参-缺enterprise_codes | — | 招引企业综合推荐 | 政策匹配度 | 政策匹配度不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute，请求体取组合 POL-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 与 rankings 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.attract.recommend.m_ent_policy_match_score catalog_page_id=entan.attract 组合=POL-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ATR-01 | entan.attract.recommend | enterprise_codes=0218337e44ca794fee9850cf1627b03b、05dc8024336db695425572625773381b、0551ccfde6aa2b3c52e647e283204040、05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| ATR-02 | entan.attract.recommend | 不传 enterprise_codes | 缺必填 enterprise_codes |
| POL-01 | entan.attract.recommend.m_ent_policy_match_score | enterprise_codes=0218337e44ca794fee9850cf1627b03b、05dc8024336db695425572625773381b、0551ccfde6aa2b3c52e647e283204040、05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| POL-02 | entan.attract.recommend.m_ent_policy_match_score | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 招引企业推荐指数（企业集合） | entan.attract.recommend | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | enterprise_codes* | unavailable |
| 政策匹配度 | entan.attract.recommend.m_ent_policy_match_score | POST | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.attract.recommend | API-00984、00985 |
| entan.attract.recommend.m_ent_policy_match_score | API-00986、00987 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向 + 每参数恰好 1 条反向（本页均为单必填、无可选，无备选-参数组合）
- [x] unavailable（招引企业推荐指数（企业集合））仍按 catalog 返回体写主流程，备注注明未交付
- [x] 无鉴权类用例；反向预期为该参数的 message/msg，不单写状态码
- [x] `coverage-fp.md` 已同步 API-00984～00987

**统计**：用例 **4** 条（主流程 2、反向 2）；编号闭区间 **API-00984**～**API-00987**（父控 R2-批3 分配，连续无跳号）。
