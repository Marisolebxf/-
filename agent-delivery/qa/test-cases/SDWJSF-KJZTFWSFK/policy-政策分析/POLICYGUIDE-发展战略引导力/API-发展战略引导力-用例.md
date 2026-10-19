# 智能服务集群-科技专题服务算法库测试用例（发展战略引导力 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 发展战略引导力  
> **catalog**：`entry_id=policy.guide` · `catalog_page_id=policy.guide` · path `/policy/guide`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guide` · endpoint `policy.guide.main`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guide`，原因：不扩六级；不改 work）  
> **环境**：联调台 50897（本册不写登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 引导力 | policy.guide.main | unavailable（文档标记未交付，仍按请求/返回说明编写） |

本页仅此 1 个 title。查询参数 `scope_code`、`limit` 均为可选。`sampleRequest` 只带 `limit=20`，不传 `scope_code`。`scope_code` 的合法补传值取参数说明「省/市编码，如 440000」。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01503`～`01507`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.guide`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01503 | 政策分析 | 发展战略引导力 | 主流程 | — | 发展战略引导力 | 引导力 | 引导力按文档 sampleRequest 仅传 limit=20、不传 scope_code | 1、limit 使用文档 sampleRequest 的 20 | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-01 | 1、返回 body 为对象，与 sampleResponse 同层含 model_id（string）、count（number）、rows（array，responseFields 组合分行）；2、rows 元素含 scope_name（string）、effect_score（number）、layout_rec_cnt（number）、metric_id（string）；3、sampleResponse 示例 model_id=guide、count=1、一行 scope_name=广东省、effect_score=72.4、layout_rec_cnt=3、metric_id=M_POLICY_DS_07_POLICY_GUARD_001 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | M_POLICY_DS_07_POLICY_GUARD_001 | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01504 | 政策分析 | 发展战略引导力 | 备选-参数组合 | 补传 scope_code | 发展战略引导力 | 引导力 | 引导力补传可选 scope_code=440000，limit 保持 20 | 1、scope_code 使用参数说明示例 440000；limit=20 | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-02 | 1、返回 body 为对象，同层含 model_id（string）、count（number）、rows（array，responseFields 组合分行）；2、rows 元素含 scope_name（string）、effect_score（number）、layout_rec_cnt（number）、metric_id（string）；3、字段结构与 sampleResponse 一致（示例 model_id=guide、count=1、广东省、effect_score=72.4、layout_rec_cnt=3、metric_id=M_POLICY_DS_07_POLICY_GUARD_001） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | M_POLICY_DS_07_POLICY_GUARD_001 | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01505 | 政策分析 | 发展战略引导力 | 备选-参数组合 | 省略 limit | 发展战略引导力 | 引导力 | 引导力不传可选 limit，scope_code 保持不传 | 1、不传 scope_code；不传 limit | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-03 | 1、返回 body 为对象，同层含 model_id（string）、count（number）、rows（array，responseFields 组合分行）；2、rows 元素仍含 scope_name（string）、effect_score（number）、layout_rec_cnt（number）、metric_id（string）；3、结构与 sampleResponse 同类（示例 model_id=guide、count=1、广东省、effect_score=72.4、layout_rec_cnt=3、metric_id=M_POLICY_DS_07_POLICY_GUARD_001） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | M_POLICY_DS_07_POLICY_GUARD_001 | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01506 | 政策分析 | 发展战略引导力 | 异常-入参-非法scope_code | — | 发展战略引导力 | 引导力 | 引导力 scope_code 非法，limit 保持 20 | 1、limit=20 保持文档合法值 | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01507 | 政策分析 | 发展战略引导力 | 异常-入参-非法limit | — | 发展战略引导力 | 引导力 | 引导力 limit 非法，不传 scope_code | 1、不传 scope_code，与 sampleRequest 一致 | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GUIDE-01 | policy.guide.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| GUIDE-02 | policy.guide.main | scope_code=440000（params 说明「如 440000」）；limit=20 | 单独补传可选 scope_code（与 sample 相反：sample 不传） |
| GUIDE-03 | policy.guide.main | 不传 scope_code；不传 limit | 单独省略可选 limit（与 sample 相反：sample 传 limit=20） |
| GUIDE-04 | policy.guide.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| GUIDE-05 | policy.guide.main | 不传 scope_code；limit=-1 | 只破坏 limit |

两参数同时都不传即 GUIDE-03。主流程已覆盖「不传 scope_code」，GUIDE-02 已覆盖「传 scope_code」。

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 引导力 | policy.guide.main | GET | /policy/v1/policy/analysis/guide | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.guide.main | API-01503、01504、01505、01506、01507 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「引导力」在功能点列出现，且有 1 条主流程（API-01503）
- [x] 正向：sampleRequest（仅 limit=20、不传 scope_code）+ 补传 scope_code + 省略 limit；预期逐字段写出 sampleResponse（model_id、count、rows，以及行内 scope_name、effect_score、layout_rec_cnt、metric_id）
- [x] 反向：scope_code、limit 各恰好 1 条非法；预期为 message 或 msg 指出该参数非法
- [x] unavailable 仍按文档返回体写主流程，备注注明未交付
- [x] 无登录 / Token / 401 / 424 / 契约占位 / 只写 HTTP 4xx 的预期
- [x] 未按 field 一行一用例；A 线无对应 Lxx
- [x] `coverage-fp.md` 已同步 API-01503～01507
- [ ] `code-registry.yaml` 由父控回写（本子任务不改注册表）

**统计**：用例 **5** 条；主流程 **1**、备选 **2**、反向 **2**；编号闭区间 **API-01503**～**API-01507**（父控 R2-批12 分配）。
