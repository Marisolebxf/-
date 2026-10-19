# 智能服务集群-科技专题服务算法库测试用例（条件保障力 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 条件保障力  
> **catalog**：`entry_id=policy.guard` · `catalog_page_id=policy.guard` · path `/policy/guard`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guard`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guard`（不扩六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 保障力 | policy.guard.main | GET | unavailable |

可选参数两个：`scope_code`、`limit`。`sampleRequest` 只含 `limit=20`，不含 `scope_code`。备选与 sample 相反：传入 `scope_code=440000`（参数说明「如 440000」）、不传 `limit`。反向各 1 条非法，不把省略写成反向。path 为 `/policy/v1/policy/analysis/guard`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01508**～**API-01512**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.guard`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01508 | 政策分析 | 条件保障力 | 主流程 | — | 条件保障力 | 保障力 | 保障力按文档 sampleRequest 只传 limit=20、不传 scope_code | 1、不传 scope_code；limit=20 | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GRD-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：model_id（string，示例 guard）、count（number，示例 1）；2、rows 为数组（responseFields 组合分行）；3、rows 元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01509 | 政策分析 | 条件保障力 | 备选-参数组合 | 传入 scope_code | 条件保障力 | 保障力 | 保障力传入可选 scope_code=440000，limit 保持 sample 的 20 | 1、scope_code=440000；limit=20 | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GRD-02 | 1、返回 body 为对象；2、仍含 model_id（string，示例 guard）、count（number，示例 1）；3、rows 为数组（responseFields 组合分行），元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008），与 sampleResponse 逐字段同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01510 | 政策分析 | 条件保障力 | 备选-参数组合 | 省略 limit | 条件保障力 | 保障力 | 保障力不传可选 limit，也不传 scope_code | 1、不传 scope_code；不传 limit | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GRD-03 | 1、返回 body 为对象；2、仍含 model_id（string，示例 guard）、count（number，示例 1）；3、rows 为数组（responseFields 组合分行），元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008），与 sampleResponse 逐字段同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01511 | 政策分析 | 条件保障力 | 异常-入参-非法scope_code | — | 条件保障力 | 保障力 | 保障力 scope_code 非法，limit 保持 sample 的 20 | 1、limit=20 | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GRD-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01512 | 政策分析 | 条件保障力 | 异常-入参-非法limit | — | 条件保障力 | 保障力 | 保障力 limit 非法，不传 scope_code | 1、不传 scope_code | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GRD-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GRD-01 | policy.guard.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| GRD-02 | policy.guard.main | scope_code=440000；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明「如 440000」） |
| GRD-03 | policy.guard.main | 不传 scope_code；不传 limit | 省略可选 limit（sample 含 limit） |
| GRD-04 | policy.guard.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| GRD-05 | policy.guard.main | 不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 保障力 | policy.guard.main | GET | /policy/v1/policy/analysis/guard | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.guard.main | API-01508、01509、01510、01511、01512 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「保障力」在功能点列出现，且有 1 条主流程（API-01508）
- [x] 与 sample 相反的传/不传各 1 条备选：传入 scope_code（01509）、省略 limit（01510）
- [x] 每个参数恰好 1 条非法反向（01511 scope_code、01512 limit）；省略未写成反向
- [x] unavailable 的「保障力」仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01508～01512；A 线写无对应 Lxx

**统计**：接口 **1**；用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01508**～**API-01512**（父控 R2-批12 分配，连续用满）。
