# 智能服务集群-科技专题服务算法库测试用例（培育企业综合推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 培育企业综合推荐  
> **catalog**：`entry_id=entan.cultivate` · `catalog_page_id=entan.cultivate` · path `/entan/cultivate`  
> **A 线对照**：`fp-split-by-api-run/work/L34.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批3）  
> **环境**：联调台 50897（本册不试调）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 培育企业推荐指数（企业集合） | entan.cultivate.recommend |

**enterprise_codes 试调取值**（catalog `sampleRequest` / `example`）：`0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`。本接口 `status=unavailable`，仍按文档请求与 sampleResponse 编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00988**～**API-00989**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.cultivate`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00988 | 企业分析 | 培育企业综合推荐 | 主流程 | — | 培育企业综合推荐 | 培育企业推荐指数（企业集合） | 培育企业推荐指数（企业集合）按文档示例 enterprise_codes 计算培育推荐指数 | 1、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.POST /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute，请求体取组合 CUL-01 | 1、返回 body 含 metric_id（string，sampleResponse 示例 M_ENT_CULTIVATION_INDEX）、metric_name_zh（string，示例培育推荐指数）；2、value 为 object，value.result 为 object，含 sub_type（string，示例 cultivation）、candidate_count（number，示例 2）；3、value.result.rankings 为 array（responseFields 名 rankings，培育推荐清单；示例未另给顶层 rankings），元素含 enterprise_code（string）、enterprise_name（string）、rank（number）、industry_category（string）、enterprise_scale（string）、development_bottleneck（string）、recommendation_score（number）；4、sampleResponse 示例两条：rank=1、enterprise_code=0218337e44ca794fee9850cf1627b03b、enterprise_name=云启智元科技股份有限公司、industry_category=人工智能、enterprise_scale=中型、development_bottleneck=人才、recommendation_score=91.2，以及 rank=2、enterprise_code=05dc8024336db695425572625773381b、enterprise_name=星辰半导体香港有限公司、industry_category=人工智能、enterprise_scale=小型、development_bottleneck=资金、recommendation_score=82.6；5、data_source（string，示例 real）、confidence（string，示例 high）；6、calc_process 为 object，含 definition（string，示例培育推荐指数）、formula（string，示例技术壁垒/市场成长/团队背景加权）、source_tables（string 数组，示例 innov.analysis.cultivation）、model_version（string，示例 entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | M_ENT_CULTIVATION_INDEX | INTEG | | | endpoint_id=entan.cultivate.recommend catalog_page_id=entan.cultivate 组合=CUL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00989 | 企业分析 | 培育企业综合推荐 | 异常-入参-缺enterprise_codes | — | 培育企业综合推荐 | 培育企业推荐指数（企业集合） | 培育企业推荐指数（企业集合）不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute，请求体取组合 CUL-02 | 1、返回 body 的 message 或 msg 指出缺 enterprise_codes；2、不返回含 recommendation_score 的成功业务 rankings | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.cultivate.recommend catalog_page_id=entan.cultivate 组合=CUL-02 catalog_status=unavailable |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CUL-01 | entan.cultivate.recommend | enterprise_codes=0218337e44ca794fee9850cf1627b03b、05dc8024336db695425572625773381b、0551ccfde6aa2b3c52e647e283204040、05ff69620c962ce3bbb852351f077299 | 主路径全参（sampleRequest） |
| CUL-02 | entan.cultivate.recommend | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 培育企业推荐指数（企业集合） | entan.cultivate.recommend | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | enterprise_codes* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.cultivate.recommend | API-00988、00989 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 本接口仅 1 个必填参数、无可选参数：文档示例正向 1 条 + 缺 enterprise_codes 反向 1 条；无备选-参数组合
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 反向预期为 message/msg 指出缺 enterprise_codes，不写 HTTP 4xx / 401 / 424
- [x] `coverage-fp.md` 已同步 API-00988～00989
- [x] 两条步骤 75 字：path 本身 55 字，加上 METHOD 与组合 id 无法再压到 60 且仍写出 path

**统计**：用例 **2** 条（主流程 1、反向 1）；编号闭区间 **API-00988**～**API-00989**（父控 R2-批3 分配）。作废旧号 API-00147～00151，不复用 API-00001～00888。
