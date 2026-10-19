# 智能服务集群-科技专题服务算法库测试用例（政策焦点识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策焦点识别  
> **catalog**：`entry_id=policy.focus` · `catalog_page_id=policy.focus` · path `/policy/focus`  
> **A 线对照**：`fp-split-by-api-run/work/L35.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `policy.json`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 焦点识别 | policy.focus.main |

三个查询参数均可选：`policy_id`、`region_code`、`limit`。主流程取全参：`policy_id`、`region_code` 对齐 sampleResponse 首条 `POL_SZ_IC` / `440300`，`limit` 对齐 sampleRequest 的 `20`（params.example 为 100，以 sampleRequest 为准）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01402**～**API-01408**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.focus`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01402 | 政策分析 | 政策焦点识别 | 主流程 | — | 政策焦点识别 | 焦点识别 | 焦点识别按文档示例 policy_id、region_code、limit 全参查询返回焦点字段 | 1、policy_id=POL_SZ_IC；region_code=440300；limit=20 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-01 | 1、返回 body 的 data 为数组；2、元素含 policy_id（string）、region_code（string）、focus_score（number，responseFields 焦点指数）、relation_degree（number）、opportunity_cnt（number）；3、元素含 ext 对象及其中 title（string）；4、结构与 sampleResponse 一致，示例含 POL_SZ_IC、region_code=440300、focus_score=88.6、relation_degree=0.72、opportunity_cnt=6、ext.title=深圳市加快集成电路产业发展若干措施，以及 POL_GD_AI（440000、84.1、0.66、5、广东省推动人工智能产业发展行动方案）、POL_BJ_BIO（110000、81.3、0.61、4、北京市生物医药产业促进办法） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01403 | 政策分析 | 政策焦点识别 | 备选-参数组合 | 省略 policy_id | 政策焦点识别 | 焦点识别 | 焦点识别不传可选 policy_id，region_code 与 limit 保持文档合法值 | 1、region_code=440300；limit=20 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-02 | 1、返回 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01404 | 政策分析 | 政策焦点识别 | 备选-参数组合 | 省略 region_code | 政策焦点识别 | 焦点识别 | 焦点识别不传可选 region_code，policy_id 与 limit 保持文档合法值 | 1、policy_id=POL_SZ_IC；limit=20 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-03 | 1、返回 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01405 | 政策分析 | 政策焦点识别 | 备选-参数组合 | 省略 limit | 政策焦点识别 | 焦点识别 | 焦点识别不传可选 limit，policy_id 与 region_code 保持文档合法值 | 1、policy_id=POL_SZ_IC；region_code=440300 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-04 | 1、返回 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01406 | 政策分析 | 政策焦点识别 | 异常-入参-非法policy_id | — | 政策焦点识别 | 焦点识别 | 焦点识别 policy_id 非法，其余参数保持文档合法值 | 1、region_code=440300；limit=20 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-05 | 1、返回 body 的 message 或 msg 指出 policy_id 非法；2、不返回含 focus_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01407 | 政策分析 | 政策焦点识别 | 异常-入参-非法region_code | — | 政策焦点识别 | 焦点识别 | 焦点识别 region_code 非法，其余参数保持文档合法值 | 1、policy_id=POL_SZ_IC；limit=20 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-06 | 1、返回 body 的 message 或 msg 指出 region_code 非法；2、不返回含 focus_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01408 | 政策分析 | 政策焦点识别 | 异常-入参-非法limit | — | 政策焦点识别 | 焦点识别 | 焦点识别 limit 非法，其余参数保持文档合法值 | 1、policy_id=POL_SZ_IC；region_code=440300 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 FOC-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 focus_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | | INTEG | | | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-07 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| FOC-01 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；limit=20 | 主路径全参（sampleResponse 首条标识 + sampleRequest.limit） |
| FOC-02 | policy.focus.main | 不传 policy_id；region_code=440300；limit=20 | 省略可选 policy_id |
| FOC-03 | policy.focus.main | policy_id=POL_SZ_IC；不传 region_code；limit=20 | 省略可选 region_code |
| FOC-04 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；不传 limit | 省略可选 limit |
| FOC-05 | policy.focus.main | policy_id=__invalid__；region_code=440300；limit=20 | 只破坏 policy_id |
| FOC-06 | policy.focus.main | policy_id=POL_SZ_IC；region_code=__invalid__；limit=20 | 只破坏 region_code |
| FOC-07 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 焦点识别 | policy.focus.main | GET | /policy/v1/policy/analysis/focus | policy_id?；region_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.focus.main | API-01402、01403、01404、01405、01406、01407、01408 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「焦点识别」在功能点列出现，且有 1 条主流程（API-01402）
- [x] 有参接口：sample 全参 1 条；每个可选参数单独省略 1 条备选（01403～01405）；每个可选参数 1 条非法反向（01406～01408）
- [x] unavailable 仍按 catalog 返回体写主流程，备注注明未交付
- [x] 只覆盖业务入参与返回 body；反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01402～01408

**统计**：用例 **7** 条（主流程 1、备选 3、反向 3）；编号闭区间 **API-01402**～**API-01408**（父控 R2-批9 分配）。
