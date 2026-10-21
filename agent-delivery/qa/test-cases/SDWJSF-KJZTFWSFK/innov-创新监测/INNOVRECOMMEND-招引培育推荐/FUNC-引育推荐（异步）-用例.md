# 智能服务集群-科技专题服务算法库测试用例（引育推荐（异步） FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.recommend` · `catalog_page_id=innov.recommend` · path `/innov/recommend`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.recommend`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 招引推荐契约 | innov.recommend.attraction | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | sub_type*；enterprise_codes? | 2 |
| 2 | 培育推荐契约 | innov.recommend.cultivation | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | sub_type*；enterprise_codes? | 2 |

两个 title 均为 catalog `status=running`。合计 **4** 条接口调用 + 清单 **2** 条 = **6** 条。主流程跟各接口 `sampleRequest`（含 `sub_type` 与文档示例 `enterprise_codes`）。可选 `enterprise_codes` 不写备选；每个接口反向恰好 1 条，只省略必填 `sub_type`，不另写非法值。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01170**～**FUNC-01175**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.recommend`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01170 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 招引推荐契约 | 验证招引推荐契约功能，检查填写 sub_type=attraction、enterprise_codes=91440300MA5DA8YX7E,91440300752531479N 传 sub_type=attraction 与文档示例 enterprise_codes 后返回字段与 sampleResponse 一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、sub_type=attraction；enterprise_codes=两码 | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「招引推荐契约」；4.填写 sub_type=attraction、enterprise_codes=91440300MA5DA8YX7E,91440300752531479N，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：task_id（string，示例 REC-20260730-001）、candidate_count（number，示例 3）；2、weights.technology_match（number，示例 34）、weights.growth（number，示例 33）、weights.regional_fit（number，示例 33）；3、rankings 为数组（responseFields 推荐榜），元素含 rank（number）、enterprise_name（string）、recommendation_score（number）、industry_domain（string）、geographic_source（string），示例 1/智芯科技（深圳）有限公司/87.52/新一代信息技术/华南、2/蓝海生物制药有限公司/82.1/生物医药/华东、3/瀚海高端装备股份公司/78.45/高端装备/华北 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | M_ENT_ATTRACTION_INDEX | INTEG |  |  | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=ATTR-01 场景=主流程 金样 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01171 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 招引推荐契约 | 验证招引推荐契约功能，检查不传必填 sub_type 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 sub_type | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「招引推荐契约」；4.不传 sub_type（请求体 {} 或仅保留非 sub_type 字段），点击调用 | 1、返回面板 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 rankings 或 weights 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute |  | INTEG |  |  | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=ATTR-02 场景=异常-入参-缺sub_type catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01172 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 培育推荐契约 | 验证培育推荐契约功能，检查填写 sub_type=cultivation、enterprise_codes=91440300MA5DA8YX7E,91440300752531479N 传 sub_type=cultivation 与文档示例 enterprise_codes 后返回字段与 sampleResponse 一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、sub_type=cultivation；enterprise_codes=两码 | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「培育推荐契约」；4.填写 sub_type=cultivation、enterprise_codes=91440300MA5DA8YX7E,91440300752531479N，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：task_id（string，示例 REC-20260730-002）、candidate_count（number，示例 2）；2、rankings 为数组（responseFields 培育榜），元素含 rank（number）、enterprise_name（string）、recommendation_score（number）、industry_category（string）、enterprise_scale（string）、development_bottleneck（string），示例 1/湾区智能产业有限公司/84.3/人工智能/中型/高端人才不足、2/南山精密器件有限公司/76.8/先进制造/小型/融资渠道单一 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | M_ENT_CULTIVATION_INDEX | INTEG |  |  | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=CULT-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01173 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 培育推荐契约 | 验证培育推荐契约功能，检查不传必填 sub_type 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 sub_type | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「培育推荐契约」；4.不传 sub_type（请求体 {}），点击调用 | 1、返回面板 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 rankings 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute |  | INTEG |  |  | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=CULT-02 场景=异常-入参-缺sub_type catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01174 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 接口信息 | 验证引育推荐（异步）的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（招引推荐契约、培育推荐契约）；3、默认项概览 method=POST、path=/entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute；4、切换后概览对应培育推荐契约 POST /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.recommend 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01175 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 引育推荐（异步） | 算法测试 | 验证引育推荐（异步）的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「引育推荐（异步）」；2.切换至「算法测试」tab；3.接口下拉切换到「培育推荐契约」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 2 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.recommend 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ATTR-01 | innov.recommend.attraction | sub_type=attraction；enterprise_codes=91440300MA5DA8YX7E,91440300752531479N | 主路径（sampleRequest） |
| ATTR-02 | innov.recommend.attraction | 不传 sub_type（请求体 {} 或仅保留非 sub_type 字段） | 缺必填 sub_type |
| CULT-01 | innov.recommend.cultivation | sub_type=cultivation；enterprise_codes=91440300MA5DA8YX7E,91440300752531479N | 主路径（sampleRequest） |
| CULT-02 | innov.recommend.cultivation | 不传 sub_type（请求体 {}） | 缺必填 sub_type |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 招引推荐契约 | innov.recommend.attraction | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | sub_type*；enterprise_codes? | running |
| 培育推荐契约 | innov.recommend.cultivation | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | sub_type*；enterprise_codes? | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.recommend.attraction | FUNC-01170、01171 |
| innov.recommend.cultivation | FUNC-01172、01173 |
| （页面清单） | FUNC-01174、01175 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title（招引推荐契约、培育推荐契约）均在功能点列出现，且各有 1 条 `场景=主流程`
- [x] 主流程跟 sampleRequest（含 sub_type 与 enterprise_codes）；无备选；每个接口反向恰好 1 条，只省略 sub_type
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的 task_id、candidate_count、weights 及榜内扩展字段）
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 catalog 页（引育推荐（异步））填写；A 线无 Lxx
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01170～01175

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **6** 条；主流程 **2**、备选 **0**、反向 **2**、清单 **2**；编号闭区间 **FUNC-01170**～**FUNC-01175**（R3 innov.recommend）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **6** |
| 编号闭区间 | **FUNC-01170**～**FUNC-01175** |
| 接口向（不含清单） | **4** |
| 主流程 | **2** |
| 备选-参数组合 | **0** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-引育推荐（异步）-用例.md`（API-01898～01901 作废，不复用） |
| 鉴权用例 | **0** |
