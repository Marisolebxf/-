# 智能服务集群-科技专题服务算法库测试用例（企业基础指标 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 企业基础指标  
> **catalog**：`entry_id=entan.basic` · `catalog_page_id=entan.basic` · path `#/entan/basic`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L02.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（下拉框 title 原文）

| # | title | endpoint_id | METHOD | path | status |
|---|--------|-------------|--------|------|--------|
| 1 | 筛选项 | entan.basic.filters | GET | /entan/v1/meta/filters | unavailable |
| 2 | 重点企业提取 | entan.basic.key-enterprises | GET | /entan/v1/key-enterprises | unavailable |
| 3 | 企业类型分布 | entan.basic.type-distribution | GET | /entan/v1/type-distribution | unavailable |
| 4 | 企业领域分布 | entan.basic.domain-distribution | GET | /entan/v1/domain-distribution | unavailable |
| 5 | 新增企业数量 | entan.basic.new-enterprises | GET | /entan/v1/new-enterprises | unavailable |
| 6 | 企业重点资讯统计 | entan.news.stats | GET | /entan/v1/news/stats | unavailable |
| 7 | 企业重点资讯明细 | entan.news.list | GET | /entan/v1/news | unavailable |

本页 7 个接口在 catalog 均为 `status=unavailable`；用例仍按各接口 `sampleRequest` / `sampleResponse` / `responseFields` 编写返回 body 预期，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00026**～**FUNC-00058**，共 **33** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.basic`、组合 id、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- 
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00026 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 筛选项 | 验证筛选项功能，检查无参调用后返回文档中的产业、城市、领域与年份筛选项字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「筛选项」；3.不填查询参数，点击调用 | 1、返回 body 的 data 为对象；2、含 industries（array）、cities（array）、domains（array）、years（array）；3、文档 sampleResponse 示例 industries 含「人工智能」、cities 含「深圳市」、domains 含「人工智能」「商业航天」、years 含 2024 与 2025（示例值说明形态，不断言固定计数） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/meta/filters |  |  | FUNC-00026 | endpoint_id=entan.basic.filters catalog_page_id=entan.basic 组合=— catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00027 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查填写 chainId=INB1701 industry、city、scale、limit 查询后返回重点企业清单字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.填写 industry=、city=、scale=、limit=150（catalogsampleRequest），点击调用 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number）；3、文档 sampleResponse 示例还含 headquarters_city、enterprise_scale、industry、patent_grant_count、tech_transaction_amount | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | M_ENT_TOTAL_COUNT |  | FUNC-00027 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00028 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查不传 industry 时仍返回文档清单字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.不传 industry，填写 city=深圳市、scale=大、limit=150，点击调用 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number）；3、结构与 sampleResponse 一致，可为空数组 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00028 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00029 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查不传 city 时仍返回文档清单字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.不传 city，填写 industry=人工智能、scale=大、limit=150，点击调用 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00029 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-03 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00030 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查不传 scale 时仍返回文档清单字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.不传 scale，填写 industry=人工智能、city=深圳市、limit=150，点击调用 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00030 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-04 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00031 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查不传 limit 时仍返回文档清单字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.不传 limit，填写 industry=人工智能、city=深圳市、scale=大，点击调用 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00031 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-05 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00032 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查 industry 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.填写 industry=__invalid__、city=深圳市、scale=大、limit=150，点击调用 | 1、返回 body 的 message 或 msg 说明 industry 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00032 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-06 场景=异常-入参-非法industry |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00033 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查 city 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.填写 industry=人工智能、city=__invalid__、scale=大、limit=150，点击调用 | 1、返回 body 的 message 或 msg 说明 city 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00033 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-07 场景=异常-入参-非法city |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00034 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查 scale 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.填写 industry=人工智能、city=深圳市、scale=__invalid__、limit=150，点击调用 | 1、返回 body 的 message 或 msg 说明 scale 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00034 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-08 场景=异常-入参-非法scale |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00035 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 重点企业提取 | 验证重点企业提取功能，检查 limit 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「重点企业提取」；3.填写 industry=人工智能、city=深圳市、scale=大、limit=-1，点击调用 | 1、返回 body 的 message 或 msg 说明 limit 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises |  |  | FUNC-00035 | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-09 场景=异常-入参-非法limit |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00036 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业类型分布 | 验证企业类型分布功能，检查 year=2025 时返回 rows 类型分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业类型分布」；3.填写 year=2025，点击调用 | 1、返回 body 的 data 为对象；2、含 rows（array）；3、rows 元素含 type_name（string）、enterprise_count（number）；4、文档 sampleResponse 含 year=2025 及示例类型行 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution |  |  | FUNC-00036 | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00037 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业类型分布 | 验证企业类型分布功能，检查不传 year 时仍返回 rows 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业类型分布」；3.不传 year，点击调用 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 type_name、enterprise_count 字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution |  |  | FUNC-00037 | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00038 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业类型分布 | 验证企业类型分布功能，检查 year 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业类型分布」；3.填写 year=__invalid__，点击调用 | 1、返回 body 的 message 或 msg 说明 year 缺失或非法；2、不返回含可信 rows.enterprise_count 的成功统计 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution |  |  | FUNC-00038 | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-03 场景=异常-入参-非法year |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00039 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业领域分布 | 验证企业领域分布功能，检查 year=2025 时返回 rows 领域分布与增长率字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业领域分布」；3.填写 year=2025，点击调用 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 domain（string）、enterprise_count（number）、growth_rate（number）；3、文档 sampleResponse 示例 domain=「人工智能」 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution |  |  | FUNC-00039 | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00040 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业领域分布 | 验证企业领域分布功能，检查不传 year 时仍返回 rows 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业领域分布」；3.不传 year，点击调用 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 domain、enterprise_count、growth_rate | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution |  |  | FUNC-00040 | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00041 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业领域分布 | 验证企业领域分布功能，检查 year 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业领域分布」；3.填写 year=__invalid__，点击调用 | 1、返回 body 的 message 或 msg 说明 year 缺失或非法；2、不返回含可信 growth_rate 的成功统计 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution |  |  | FUNC-00041 | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-03 场景=异常-入参-非法year |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00042 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 新增企业数量 | 验证新增企业数量功能，检查 domain=ALL 时返回 rows 新增趋势字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「新增企业数量」；3.填写 domain=ALL，点击调用 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 stat_year（number）、new_count（number）、cumulative_count（number）；3、文档 sampleResponse 含 2023、2024 示例行 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises | M_ENT_NEW_COUNT_Y |  | FUNC-00042 | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00043 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 新增企业数量 | 验证新增企业数量功能，检查不传 domain 时仍返回 rows 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「新增企业数量」；3.不传 domain，点击调用 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 stat_year、new_count、cumulative_count | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises |  |  | FUNC-00043 | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00044 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 新增企业数量 | 验证新增企业数量功能，检查 domain 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「新增企业数量」；3.填写 domain=__invalid__，点击调用 | 1、返回 body 的 message 或 msg 说明 domain 缺失或非法；2、不返回含可信 new_count 的成功趋势 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises |  |  | FUNC-00044 | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-03 场景=异常-入参-非法domain |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00045 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯统计 | 验证企业重点资讯统计功能，检查 news_type 为空（全部）时返回月度统计字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯统计」；3.填写 news_type=（空，catalogsampleRequest），点击调用 | 1、返回 body 的 data 为数组；2、元素含 stat_month（string）、news_type（string）、type_name（string）、news_count（number）、total_amount（number）、growth_rate（number）；3、文档 sampleResponse 含 financing、product 等示例行 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | M_ENT_NEWS_STAT |  | FUNC-00045 | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00046 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯统计 | 验证企业重点资讯统计功能，检查 news_type=financing 时返回融资类统计字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯统计」；3.填写 news_type=financing，点击调用 | 1、返回 body 的 data 为数组；2、元素含 stat_month、news_type、type_name、news_count、total_amount、growth_rate；3、news_type 为 financing 或 type_name 为「融资」 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats |  |  | FUNC-00046 | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00047 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯统计 | 验证企业重点资讯统计功能，检查 news_type 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯统计」；3.填写 news_type=__invalid__，点击调用 | 1、返回 body 的 message 或 msg 说明 news_type 缺失或非法；2、不返回含可信 news_count 的成功统计 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats |  |  | FUNC-00047 | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-03 场景=异常-入参-非法news_type |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00048 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查填写 chainId=INB1701分页参数查询后返回 list 与分页元数据 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.填写 news_type=、keyword=、page=1、size=15（catalogsampleRequest），点击调用 | 1、返回 body 的 data 为对象；2、含 list（array）、total（number）、page（number）、size（number）；3、list 元素含 enterprise_name、news_type、title、amount、finance_round、counterparty、region、publish_time（见 sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | M_ENT_NEWS_DETAIL |  | FUNC-00048 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-01 catalog_status=unavailable 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00049 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查不传 news_type 时仍返回 list 分页结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.不传 news_type，填写 keyword=、page=1、size=15，点击调用 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00049 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00050 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查不传 keyword 时仍返回 list 分页结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.不传 keyword，填写 news_type=financing、page=1、size=15，点击调用 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00050 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-03 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00051 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查不传 page 时仍返回 list 分页结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.不传 page，填写 news_type=financing、keyword=、size=15，点击调用 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00051 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-04 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00052 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查不传 size 时仍返回 list 分页结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.不传 size，填写 news_type=financing、keyword=、page=1，点击调用 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00052 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-05 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00053 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查 news_type 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.填写 news_type=__invalid__、page=1、size=15，点击调用 | 1、返回 body 的 message 或 msg 说明 news_type 缺失或非法；2、不返回含可信 list 的成功分页 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00053 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-06 场景=异常-入参-非法news_type |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00054 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查 keyword 超长非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.填写 news_type=financing、keyword=（重复字符超512）、page=1、size=15，点击调用 | 1、返回 body 的 message 或 msg 说明 keyword 非法；2、不返回含可信 list 的成功分页 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00054 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-07 场景=异常-入参-非法keyword |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00055 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查 page 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.填写 news_type=financing、page=abc、size=15，点击调用 | 1、返回 body 的 message 或 msg 说明 page 缺失或非法；2、不返回含可信 list 的成功分页 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00055 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-08 场景=异常-入参-非法page |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00056 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 企业重点资讯明细 | 验证企业重点资讯明细功能，检查 size 非法时返回该参数错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.接口下拉选择「企业重点资讯明细」；3.填写 news_type=financing、page=1、size=-1，点击调用 | 1、返回 body 的 message 或 msg 说明 size 缺失或非法；2、不返回含可信 list 的成功分页 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news |  |  | FUNC-00056 | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-09 场景=异常-入参-非法size |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00057 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 接口信息 | 验证企业基础指标的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.停留在「接口信息」页签；3.记录默认选中项概览区的 method、path 与接口标题；4.下拉切换到「重点企业提取」 | 1、页头接口数量与下拉项数均为 7；2、下拉名称与 catalog title 一致；3、默认项概览标题、method、path 对应当前选中接口；4、切换至「重点企业提取」后概览 method=GET、path=/entan/v1/key-enterprises，且参数表与示例区有内容刷新；1、确认页头显示「7 个接口」；2、核对「当前接口」下拉项数量为 7，名称依次为「筛选项」「重点企业提取」「企业类型分布」「企业领域分布」「新增企业数量」「企业重点资讯统计」「企业重点资讯明细」；3、确认概览区 method、path 变为 GET /entan/v1/key-enterprises，参数表与示例区随之刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/basic |  | INTEG |  | FUNC-00057 | catalog_page_id=entan.basic 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00058 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 企业基础指标模型构建 | 企业基础指标 | 算法测试 | 验证企业基础指标的算法测试功能，检查下拉与调用区 method、path 随接口切换正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「企业基础指标」；2.切换到「算法测试」页签；3.记录当前选中项调用区展示的 method、path；4.下拉切换到「企业重点资讯明细」 | 1、算法测试页签下拉数量与名称同 catalog 共 7 项；2、切换前调用区 method、path 与所选接口一致；3、切换至「企业重点资讯明细」后调用区 method=GET、path=/entan/v1/news，请求区正常刷新；1、核对「当前接口」下拉项数量为 7，名称与「接口信息」页签一致；2、确认调用区 method、path 变为 GET /entan/v1/news，请求参数区正常刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/basic |  | INTEG |  | FUNC-00058 | catalog_page_id=entan.basic 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| KEY-01 | entan.basic.key-enterprises | industry=；city=；scale=；limit=150（catalog sampleRequest） | 主路径全参 |
| KEY-02 | entan.basic.key-enterprises | 不传 industry；city=深圳市；scale=大；limit=150 | 省略 industry |
| KEY-03 | entan.basic.key-enterprises | industry=人工智能；不传 city；scale=大；limit=150 | 省略 city |
| KEY-04 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；不传 scale；limit=150 | 省略 scale |
| KEY-05 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=大；不传 limit | 省略 limit |
| KEY-06 | entan.basic.key-enterprises | industry=__invalid__；city=深圳市；scale=大；limit=150 | 只破坏 industry |
| KEY-07 | entan.basic.key-enterprises | industry=人工智能；city=__invalid__；scale=大；limit=150 | 只破坏 city |
| KEY-08 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=__invalid__；limit=150 | 只破坏 scale |
| KEY-09 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=大；limit=-1 | 只破坏 limit |
| TYP-01 | entan.basic.type-distribution | year=2025 | 主路径 |
| TYP-02 | entan.basic.type-distribution | 不传 year | 省略 year |
| TYP-03 | entan.basic.type-distribution | year=__invalid__ | 非法 year |
| DOM-01 | entan.basic.domain-distribution | year=2025 | 主路径 |
| DOM-02 | entan.basic.domain-distribution | 不传 year | 省略 year |
| DOM-03 | entan.basic.domain-distribution | year=__invalid__ | 非法 year |
| NEW-01 | entan.basic.new-enterprises | domain=ALL | 主路径 |
| NEW-02 | entan.basic.new-enterprises | 不传 domain | 省略 domain |
| NEW-03 | entan.basic.new-enterprises | domain=__invalid__ | 非法 domain |
| NST-01 | entan.news.stats | news_type=（空，catalog sampleRequest） | 全部类型 |
| NST-02 | entan.news.stats | news_type=financing | 文档选项合法值 |
| NST-03 | entan.news.stats | news_type=__invalid__ | 非法 news_type |
| NLST-01 | entan.news.list | news_type=；keyword=；page=1；size=15（catalog sampleRequest） | 主路径全参 |
| NLST-02 | entan.news.list | 不传 news_type；keyword=；page=1；size=15 | 省略 news_type |
| NLST-03 | entan.news.list | news_type=financing；不传 keyword；page=1；size=15 | 省略 keyword |
| NLST-04 | entan.news.list | news_type=financing；keyword=；不传 page；size=15 | 省略 page |
| NLST-05 | entan.news.list | news_type=financing；keyword=；page=1；不传 size | 省略 size |
| NLST-06 | entan.news.list | news_type=__invalid__；page=1；size=15 | 只破坏 news_type |
| NLST-07 | entan.news.list | news_type=financing；keyword=（重复字符超 512）；page=1；size=15 | 只破坏 keyword |
| NLST-08 | entan.news.list | news_type=financing；page=abc；size=15 | 只破坏 page |
| NLST-09 | entan.news.list | news_type=financing；page=1；size=-1 | 只破坏 size |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | title | METHOD | path | status | params |
|-------------|-------|--------|------|--------|--------|
| entan.basic.filters | 筛选项 | GET | /entan/v1/meta/filters | unavailable | — |
| entan.basic.key-enterprises | 重点企业提取 | GET | /entan/v1/key-enterprises | unavailable | industry、city、scale、limit（均可选） |
| entan.basic.type-distribution | 企业类型分布 | GET | /entan/v1/type-distribution | unavailable | year |
| entan.basic.domain-distribution | 企业领域分布 | GET | /entan/v1/domain-distribution | unavailable | year |
| entan.basic.new-enterprises | 新增企业数量 | GET | /entan/v1/new-enterprises | unavailable | domain |
| entan.news.stats | 企业重点资讯统计 | GET | /entan/v1/news/stats | unavailable | news_type |
| entan.news.list | 企业重点资讯明细 | GET | /entan/v1/news | unavailable | news_type、keyword、page、size |

---

## 2. endpoint → 用例简表

| endpoint_id | title | 用例编号 |
|-------------|-------|----------|
| entan.basic.filters | 筛选项 | FUNC-00026 |
| entan.basic.key-enterprises | 重点企业提取 | FUNC-00027～00035 |
| entan.basic.type-distribution | 企业类型分布 | FUNC-00036～00038 |
| entan.basic.domain-distribution | 企业领域分布 | FUNC-00039～00041 |
| entan.basic.new-enterprises | 新增企业数量 | FUNC-00042～00044 |
| entan.news.stats | 企业重点资讯统计 | FUNC-00045～00047 |
| entan.news.list | 企业重点资讯明细 | FUNC-00048～00056 |
| （页面清单） | 接口信息 / 算法测试 | FUNC-00057～00058 |

---

## 3. §I 交卷自检计数

| 检查项 | 计数 / 结论 |
|--------|-------------|
| 本页 title 数 | **7**（§0 清单） |
| 功能点列可搜到的 title | **7** / 7（另 2 条清单用例功能点为接口信息、算法测试） |
| 每 title 至少 1 条 `场景=主流程` | **7** / 7 |
| 用例总数 | **33**（FUNC-00026～00058） |
| 鉴权 / Token / 401 / 424 用例 | **0** |
| 步骤含 GET/POST | **0** |
| 清单用例 | **2**（FUNC-00057 接口信息-清单、FUNC-00058 算法测试-清单） |
| 正向用例（主流程+备选） | **19** |
| 反向用例（异常-入参） | **12** |
| unavailable 接口主流程按文档 body | **7** / 7 |
| `coverage-fp.md` | 已同步 FUNC 编号 |
