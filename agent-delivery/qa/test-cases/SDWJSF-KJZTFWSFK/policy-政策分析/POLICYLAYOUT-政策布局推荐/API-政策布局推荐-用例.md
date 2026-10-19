# 智能服务集群-科技专题服务算法库测试用例（政策布局推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策布局推荐  
> **catalog**：`entry_id=policy.layout` · `catalog_page_id=policy.layout` · path `/policy/layout`  
> **A 线对照**：`fp-split-by-api-run/work/L40.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台文档（真源 `policy.json`；本册不打开页面）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 布局推荐 | policy.layout.main |

两个查询参数均可选：`scope_code`、`limit`。`sampleRequest` 仅 `limit=20`（`params.example` 为 100，主流程以 sampleRequest 为准）。`scope_code` 的 `example` 为空，说明举例 `440000`，补传取该说明值。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01441**～**API-01445**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.layout`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01441 | 政策分析 | 政策布局推荐 | 主流程 | — | 政策布局推荐 | 布局推荐 | 布局推荐按文档 sampleRequest 仅传 limit=20、不传 scope_code | 1、limit 使用文档 sampleRequest 取值 20 | 1.GET /policy/v1/policy/analysis/layout，查询参数取组合 LAY-01 | 1、返回 body 的 data 为数组；2、元素含 scope_name（string）、layout_rec_cnt（number，responseFields 建议数）、recommendations（string 数组）；3、结构与 sampleResponse 一致，示例含 scope_name=深圳市、layout_rec_cnt=8、recommendations 含「补强EDA工具链」「扩大流片补贴」，以及广州市（layout_rec_cnt=5、recommendations 含「引入检测认证」）、杭州市（layout_rec_cnt=4、recommendations 含「人才安居配套」） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/layout | M_POLICY_LAYOUT_REC_COUNT | INTEG | | | endpoint_id=policy.layout.main catalog_page_id=policy.layout 组合=LAY-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01442 | 政策分析 | 政策布局推荐 | 备选-参数组合 | 省略 limit | 政策布局推荐 | 布局推荐 | 布局推荐不传可选 limit，也不传 scope_code | 1、无查询参数 | 1.GET /policy/v1/policy/analysis/layout，查询参数取组合 LAY-02 | 1、返回 body 的 data 为数组；2、元素仍含 scope_name（string）、layout_rec_cnt（number）、recommendations（string 数组）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/layout | M_POLICY_LAYOUT_REC_COUNT | INTEG | | | endpoint_id=policy.layout.main catalog_page_id=policy.layout 组合=LAY-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01443 | 政策分析 | 政策布局推荐 | 备选-参数组合 | 补传 scope_code | 政策布局推荐 | 布局推荐 | 布局推荐补传可选 scope_code=440000，limit 保持文档 sampleRequest 的 20 | 1、scope_code=440000；limit=20 | 1.GET /policy/v1/policy/analysis/layout，查询参数取组合 LAY-03 | 1、返回 body 的 data 为数组；2、元素仍含 scope_name（string）、layout_rec_cnt（number）、recommendations（string 数组）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/layout | M_POLICY_LAYOUT_REC_COUNT | INTEG | | | endpoint_id=policy.layout.main catalog_page_id=policy.layout 组合=LAY-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01444 | 政策分析 | 政策布局推荐 | 异常-入参-非法scope_code | — | 政策布局推荐 | 布局推荐 | 布局推荐 scope_code 非法，limit 保持文档合法值 | 1、limit=20 | 1.GET /policy/v1/policy/analysis/layout，查询参数取组合 LAY-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 layout_rec_cnt 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/layout | | INTEG | | | endpoint_id=policy.layout.main catalog_page_id=policy.layout 组合=LAY-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01445 | 政策分析 | 政策布局推荐 | 异常-入参-非法limit | — | 政策布局推荐 | 布局推荐 | 布局推荐 limit 非法，不传 scope_code | 1、不传 scope_code | 1.GET /policy/v1/policy/analysis/layout，查询参数取组合 LAY-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 layout_rec_cnt 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/layout | | INTEG | | | endpoint_id=policy.layout.main catalog_page_id=policy.layout 组合=LAY-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| LAY-01 | policy.layout.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| LAY-02 | policy.layout.main | 不传 scope_code；不传 limit | 省略可选 limit |
| LAY-03 | policy.layout.main | scope_code=440000；limit=20 | 补传可选 scope_code |
| LAY-04 | policy.layout.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| LAY-05 | policy.layout.main | 不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 布局推荐 | policy.layout.main | GET | /policy/v1/policy/analysis/layout | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.layout.main | API-01441、01442、01443、01444、01445 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「布局推荐」在功能点列出现，且有 1 条主流程（API-01441）
- [x] 有参接口：sampleRequest 主流程 1 条；省略 limit 1 条（01442）；补传 scope_code 1 条（01443）；每个参数 1 条非法反向（01444、01445）
- [x] unavailable 仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01441～01445

**统计**：接口 **1**；用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01441**～**API-01445**（父控 R2-批11 分配，连续用满）。
