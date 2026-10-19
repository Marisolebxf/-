# 智能服务集群-科技专题服务算法库测试用例（政策力度评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策力度评估  
> **catalog**：`entry_id=policy.intensity` · `catalog_page_id=policy.intensity` · path `/policy/intensity`  
> **A 线对照**：`fp-split-by-api-run/work/L36.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 力度评估 | policy.intensity.main |

三个查询参数均可选：`scope_type`、`scope_code`、`limit`。`sampleRequest` 只含 `scope_type=province`、`limit=20`，不含 `scope_code`。备选各动一个参数，与 sample 相反：不传 `scope_type`、传入 `scope_code=440000`（参数说明示例）、不传 `limit`。反向各 1 条非法，不把省略写成反向。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01419**～**API-01425**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.intensity`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01419 | 政策分析 | 政策力度评估 | 主流程 | — | 政策力度评估 | 力度评估 | 力度评估按文档 sampleRequest 传 scope_type=province、limit=20、不传 scope_code | 1、scope_type=province；limit=20；不传 scope_code | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-01 | 1、返回 body 的 data 为数组；2、元素含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number，responseFields 力度指数）、industry_coverage（number）；3、与 sampleResponse 逐字段一致，示例第1条 rank_no=1、scope_type=policy、scope_code=POL_IC_EU、scope_name=欧盟芯片法案配套实施细则、intensity_index=91.2、industry_coverage=72.5，第2条 rank_no=2、scope_type=policy、scope_code=POL_SZ_IC、scope_name=深圳市加快集成电路产业发展若干措施、intensity_index=88.6、industry_coverage=69.8，第3条 rank_no=3、scope_type=province、scope_code=440000、scope_name=广东省、intensity_index=87.3、industry_coverage=76.2 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01420 | 政策分析 | 政策力度评估 | 备选-参数组合 | 省略 scope_type | 政策力度评估 | 力度评估 | 力度评估不传可选 scope_type，limit 保持 sample 的 20、不传 scope_code | 1、不传 scope_type；limit=20；不传 scope_code | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-02 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number，responseFields 力度指数）、industry_coverage（number）；3、字段与 sampleResponse 逐字段同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01421 | 政策分析 | 政策力度评估 | 备选-参数组合 | 传入 scope_code | 政策力度评估 | 力度评估 | 力度评估传入可选 scope_code=440000，scope_type 与 limit 保持 sample | 1、scope_type=province；scope_code=440000；limit=20 | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-03 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number，responseFields 力度指数）、industry_coverage（number）；3、字段与 sampleResponse 逐字段同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01422 | 政策分析 | 政策力度评估 | 备选-参数组合 | 省略 limit | 政策力度评估 | 力度评估 | 力度评估不传可选 limit，scope_type 保持 sample 的 province、不传 scope_code | 1、scope_type=province；不传 limit；不传 scope_code | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-04 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number，responseFields 力度指数）、industry_coverage（number）；3、字段与 sampleResponse 逐字段同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01423 | 政策分析 | 政策力度评估 | 异常-入参-非法scope_type | — | 政策力度评估 | 力度评估 | 力度评估 scope_type 非法，其余保持 sample | 1、limit=20；不传 scope_code | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-05 | 1、返回 body 的 message 或 msg 指出 scope_type 非法；2、不返回含 intensity_index 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01424 | 政策分析 | 政策力度评估 | 异常-入参-非法scope_code | — | 政策力度评估 | 力度评估 | 力度评估 scope_code 非法，其余保持 sample | 1、scope_type=province；limit=20 | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-06 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 intensity_index 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01425 | 政策分析 | 政策力度评估 | 异常-入参-非法limit | — | 政策力度评估 | 力度评估 | 力度评估 limit 非法，其余保持 sample | 1、scope_type=province；不传 scope_code | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 intensity_index 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-07 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INT-01 | policy.intensity.main | scope_type=province；不传 scope_code；limit=20 | 主路径（sampleRequest） |
| INT-02 | policy.intensity.main | 不传 scope_type；不传 scope_code；limit=20 | 省略可选 scope_type（sample 含 scope_type） |
| INT-03 | policy.intensity.main | scope_type=province；scope_code=440000；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| INT-04 | policy.intensity.main | scope_type=province；不传 scope_code；不传 limit | 省略可选 limit（sample 含 limit） |
| INT-05 | policy.intensity.main | scope_type=__invalid__（不在 province、policy、空）；不传 scope_code；limit=20 | 只破坏 scope_type |
| INT-06 | policy.intensity.main | scope_type=province；scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| INT-07 | policy.intensity.main | scope_type=province；不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 力度评估 | policy.intensity.main | GET | /policy/v1/policy/analysis/intensity | scope_type?；scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.intensity.main | API-01419、01420、01421、01422、01423、01424、01425 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「力度评估」在功能点列出现，且有 1 条主流程（API-01419）
- [x] 与 sample 相反的传/不传各 1 条备选：省略 scope_type（01420）、传入 scope_code（01421）、省略 limit（01422）
- [x] 每个参数恰好 1 条非法反向（01423～01425）；省略未写成反向
- [x] unavailable 仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01419～01425

**统计**：接口 **1**；用例 **7** 条（主流程 1、备选 3、反向 3）；编号闭区间 **API-01419**～**API-01425**（父控 R2-批10 分配，连续用满）。
