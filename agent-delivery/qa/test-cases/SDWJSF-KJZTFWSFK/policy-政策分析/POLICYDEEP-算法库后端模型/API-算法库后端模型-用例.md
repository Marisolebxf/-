# 智能服务集群-科技专题服务算法库测试用例（算法库后端模型 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 算法库后端模型  
> **catalog**：`entry_id=policy.deep` · `catalog_page_id=policy.deep` · path `/policy/deep`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.deep`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.deep`（不扩六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 后端模型 | policy.deep.models | GET | unavailable |

本页 1 个接口。`scope_code`、`limit` 均可选。`sampleRequest` 同时传 `scope_code=440300`、`limit=50`。备选与 sample 相反：不传 `scope_code`（保留 `limit=50`）、不传 `limit`（保留 `scope_code=440300`）。反向各 1 条非法，不把省略写成反向。path 以 catalog JSON 为准：`GET /policy/v1/policy/analysis/focus`。`status=unavailable`，仍按该接口 `sampleResponse` 写正向返回字段。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01513**～**API-01517**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.deep`、组合 id。旧号 API-000524～000528 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01513 | 政策分析 | 算法库后端模型 | 主流程 | — | 算法库后端模型 | 后端模型 | 后端模型按文档 sampleRequest 传 scope_code=440300、limit=50 | 1、scope_code 使用文档示例 440300；limit=50 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 MOD-01 | 1、返回 body 含 rows（array，responseFields 后端模型索引）；2、元素含 model（string）、model_name（string）、metric_id（string）、index（number）；3、与 sampleResponse 逐字段一致：model=focus、model_name=政策焦点识别模型、metric_id=M_POLICY_DEEP_166_1、index=82.6；model=intensity、model_name=政策力度评估模型、metric_id=M_POLICY_DEEP_167_1、index=78.4；model=effect、model_name=政策效果评估模型、metric_id=M_POLICY_DEEP_168_1、index=75.1；model=gap、model_name=政策短板识别模型、metric_id=M_POLICY_DEEP_169_1、index=3；model=opportunity、model_name=政策机遇识别模型、metric_id=M_POLICY_DEEP_170_1、index=9；model=layout、model_name=政策布局推荐模型、metric_id=M_POLICY_DEEP_171_1、index=6 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01514 | 政策分析 | 算法库后端模型 | 备选-参数组合 | 省略 scope_code | 算法库后端模型 | 后端模型 | 后端模型不传可选 scope_code，limit 保持 sample 的 50 | 1、不传 scope_code；limit=50 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 MOD-02 | 1、返回 body 含 rows（array，responseFields 后端模型索引）；2、元素仍含 model（string）、model_name（string）、metric_id（string）、index（number）；3、字段与 sampleResponse 逐字段同类，示例值（focus/政策焦点识别模型/M_POLICY_DEEP_166_1/82.6，intensity/政策力度评估模型/M_POLICY_DEEP_167_1/78.4，effect/政策效果评估模型/M_POLICY_DEEP_168_1/75.1，gap/政策短板识别模型/M_POLICY_DEEP_169_1/3，opportunity/政策机遇识别模型/M_POLICY_DEEP_170_1/9，layout/政策布局推荐模型/M_POLICY_DEEP_171_1/6）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01515 | 政策分析 | 算法库后端模型 | 备选-参数组合 | 省略 limit | 算法库后端模型 | 后端模型 | 后端模型不传可选 limit，scope_code 保持 sample 的 440300 | 1、scope_code=440300；不传 limit | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 MOD-03 | 1、返回 body 含 rows（array，responseFields 后端模型索引）；2、元素仍含 model（string）、model_name（string）、metric_id（string）、index（number）；3、字段与 sampleResponse 逐字段同类，示例值（focus/政策焦点识别模型/M_POLICY_DEEP_166_1/82.6，intensity/政策力度评估模型/M_POLICY_DEEP_167_1/78.4，effect/政策效果评估模型/M_POLICY_DEEP_168_1/75.1，gap/政策短板识别模型/M_POLICY_DEEP_169_1/3，opportunity/政策机遇识别模型/M_POLICY_DEEP_170_1/9，layout/政策布局推荐模型/M_POLICY_DEEP_171_1/6）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01516 | 政策分析 | 算法库后端模型 | 异常-入参-非法scope_code | — | 算法库后端模型 | 后端模型 | 后端模型 scope_code 非法，limit 保持 sample 的 50 | 1、limit=50 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 MOD-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 model、model_name、metric_id、index 的成功业务 rows | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01517 | 政策分析 | 算法库后端模型 | 异常-入参-非法limit | — | 算法库后端模型 | 后端模型 | 后端模型 limit 非法，scope_code 保持 sample 的 440300 | 1、scope_code=440300 | 1.GET /policy/v1/policy/analysis/focus，查询参数取组合 MOD-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 model、model_name、metric_id、index 的成功业务 rows | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MOD-01 | policy.deep.models | scope_code=440300；limit=50 | 主路径（sampleRequest） |
| MOD-02 | policy.deep.models | 不传 scope_code；limit=50 | 与 sample 相反：省略可选 scope_code |
| MOD-03 | policy.deep.models | scope_code=440300；不传 limit | 与 sample 相反：省略可选 limit |
| MOD-04 | policy.deep.models | scope_code=__invalid__；limit=50 | 只破坏 scope_code |
| MOD-05 | policy.deep.models | scope_code=440300；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 后端模型 | policy.deep.models | GET | /policy/v1/policy/analysis/focus | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.deep.models | API-01513、01514、01515、01516、01517 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「后端模型」在功能点列出现，且有 1 条主流程（API-01513）
- [x] 与 sample 相反的传/不传各 1 条备选：省略 scope_code（01514）、省略 limit（01515）
- [x] 每个参数恰好 1 条非法反向（01516 scope_code、01517 limit）；省略未写成反向
- [x] unavailable 仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01513～01517；A 线写无对应 Lxx

**统计**：接口 **1**；用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01513**～**API-01517**（父控 R2-批12 分配，连续用满）。
