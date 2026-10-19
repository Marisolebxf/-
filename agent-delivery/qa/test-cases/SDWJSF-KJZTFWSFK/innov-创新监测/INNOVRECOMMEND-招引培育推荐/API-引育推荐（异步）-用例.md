# 智能服务集群-科技专题服务算法库测试用例（引育推荐（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 引育推荐（异步）  
> **catalog**：`entry_id=innov.recommend` · `catalog_page_id=innov.recommend` · path `/innov/recommend`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.recommend`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`，原因：创新监测不在本轮 60 六级；不改 work）  
> **环境**：联调台 50897（本册不写登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批21）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 招引推荐契约 | innov.recommend.attraction | POST | （空） | sub_type* | 2 |
| 2 | 培育推荐契约 | innov.recommend.cultivation | POST | （空） | sub_type* | 2 |

两个 title 的 catalog `status=unavailable`，`path` 均为空字符串。步骤只写「path 为空」，不臆造 URL。`路由route` 记 `—`。

每个接口只有必填 `sub_type`（string），无其它参数。主流程跟 `sampleRequest`：招引 `sub_type=attraction`，培育 `sub_type=cultivation`。反向恰好 1 条：省略 `sub_type`（请求体 `{}`）。不另写非法值，不写备选。备注注明文档标记未交付，正向预期仍按该接口 sampleResponse 逐字段写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01898`～`01901`（闭区间用满，不复用 00001～00888）。`路由route` = path（本页为空，记 `—`）；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.recommend`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01898 | 创新监测 | 引育推荐（异步） | 主流程 | — | 引育推荐（异步） | 招引推荐契约 | 招引推荐契约按文档 sampleRequest 传 sub_type=attraction | 1、sub_type 使用文档示例 attraction | 1.POST（path 为空），请求体取组合 ATTR-01 | 1、返回 body 与 sampleResponse 同层逐字段：task_id（string，示例 REC-20260730-001）、candidate_count（number，示例 3）；2、weights.technology_match（number，示例 34）、weights.growth（number，示例 33）、weights.regional_fit（number，示例 33）；3、rankings 为数组（responseFields 推荐榜），元素含 rank（number）、enterprise_name（string）、recommendation_score（number）、industry_domain（string）、geographic_source（string），示例 1/智芯科技（深圳）有限公司/87.52/新一代信息技术/华南、2/蓝海生物制药有限公司/82.1/生物医药/华东、3/瀚海高端装备股份公司/78.45/高端装备/华北 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=ATTR-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01899 | 创新监测 | 引育推荐（异步） | 异常-入参-缺sub_type | — | 引育推荐（异步） | 招引推荐契约 | 招引推荐契约不传必填 sub_type | 1、请求体不传 sub_type | 1.POST（path 为空），请求体取组合 ATTR-02 | 1、返回 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 rankings 或 weights 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=ATTR-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01900 | 创新监测 | 引育推荐（异步） | 主流程 | — | 引育推荐（异步） | 培育推荐契约 | 培育推荐契约按文档 sampleRequest 传 sub_type=cultivation | 1、sub_type 使用文档示例 cultivation | 1.POST（path 为空），请求体取组合 CULT-01 | 1、返回 body 与 sampleResponse 同层逐字段：task_id（string，示例 REC-20260730-002）、candidate_count（number，示例 2）；2、rankings 为数组（responseFields 培育榜），元素含 rank（number）、enterprise_name（string）、recommendation_score（number）、industry_category（string）、enterprise_scale（string）、development_bottleneck（string），示例 1/湾区智能产业有限公司/84.3/人工智能/中型/高端人才不足、2/南山精密器件有限公司/76.8/先进制造/小型/融资渠道单一 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=CULT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01901 | 创新监测 | 引育推荐（异步） | 异常-入参-缺sub_type | — | 引育推荐（异步） | 培育推荐契约 | 培育推荐契约不传必填 sub_type | 1、请求体不传 sub_type | 1.POST（path 为空），请求体取组合 CULT-02 | 1、返回 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 rankings 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=CULT-02 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ATTR-01 | innov.recommend.attraction | sub_type=attraction | 主路径（sampleRequest） |
| ATTR-02 | innov.recommend.attraction | 不传 sub_type（请求体 {}） | 缺必填 sub_type |
| CULT-01 | innov.recommend.cultivation | sub_type=cultivation | 主路径（sampleRequest） |
| CULT-02 | innov.recommend.cultivation | 不传 sub_type（请求体 {}） | 缺必填 sub_type |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 招引推荐契约 | innov.recommend.attraction | POST | （空） | sub_type* | unavailable |
| 培育推荐契约 | innov.recommend.cultivation | POST | （空） | sub_type* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.recommend.attraction | API-01898、01899 |
| innov.recommend.cultivation | API-01900、01901 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（招引推荐契约、培育推荐契约）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest：attraction、cultivation
- [x] 无其它参数，无备选；每个接口反向恰好 1 条，只省略 sub_type，不另写非法值
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的 task_id、candidate_count、weights 及榜内扩展字段）；反向预期为 message 或 msg 指出 sub_type 缺失或非法
- [x] path 为空，步骤未臆造 URL；unavailable 备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424 / 只写 HTTP 4xx 的预期
- [x] A 线无对应 Lxx；未改 work
- [x] `coverage-fp.md` 已同步 API-01898～01901
- [ ] `code-registry.yaml` 由父控回写（本子任务不改注册表）

**统计**：用例 **4** 条；主流程 **2**、备选 **0**、反向 **2**；编号闭区间 **API-01898**～**API-01901**（父控 R2-批21 分配）。
