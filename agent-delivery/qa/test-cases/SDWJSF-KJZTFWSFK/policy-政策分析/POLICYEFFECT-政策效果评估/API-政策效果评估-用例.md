# 智能服务集群-科技专题服务算法库测试用例（政策效果评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策效果评估  
> **catalog**：`entry_id=policy.effect` · `catalog_page_id=policy.effect` · path `/policy/effect`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.effect` · endpoint `policy.effect.main`  
> **A 线对照**：`fp-split-by-api-run/work/L37.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 50897（本册不写登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 效果评估 | policy.effect.main | unavailable（文档标记未交付，仍按请求/返回说明编写） |

本页仅此 1 个 title。查询参数 `scope_code`、`limit` 均为可选。`sampleRequest` 只带 `limit=20`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01426`～`01430`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.effect`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01426 | 政策分析 | 政策效果评估 | 主流程 | — | 政策效果评估 | 效果评估 | 效果评估按文档 sampleRequest 仅传 limit=20、不传 scope_code | 1、limit 使用文档 sampleRequest 的 20 | 1.GET /policy/v1/policy/analysis/effect，查询参数取组合 EFF-01 | 1、返回 body 的 data 为数组，与 sampleResponse 同为列表；2、元素含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、sampleResponse 示例三行：深圳市/440300/effect_score 82.4/impl_effect 71.2，广东省/440000/79.1/68.6，北京市/110000/77.8/66，非空元素应出现上述字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG | | | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01427 | 政策分析 | 政策效果评估 | 备选-参数组合 | 补传 scope_code | 政策效果评估 | 效果评估 | 效果评估补传可选 scope_code=440000，limit 保持 20 | 1、scope_code 使用 params 说明示例 440000；limit=20 | 1.GET /policy/v1/policy/analysis/effect，查询参数取组合 EFF-02 | 1、返回 body 的 data 为数组；2、元素含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、字段结构与 sampleResponse 一致（示例含深圳市 82.4/71.2、广东省 79.1/68.6、北京市 77.8/66） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG | | | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01428 | 政策分析 | 政策效果评估 | 备选-参数组合 | 省略 limit | 政策效果评估 | 效果评估 | 效果评估仅传 scope_code=440000、不传可选 limit | 1、scope_code=440000；不传 limit | 1.GET /policy/v1/policy/analysis/effect，查询参数取组合 EFF-03 | 1、返回 body 的 data 为数组；2、元素仍含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG | | | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01429 | 政策分析 | 政策效果评估 | 异常-入参-非法scope_code | — | 政策效果评估 | 效果评估 | 效果评估 scope_code 非法，limit 保持 20 | 1、limit=20 保持文档合法值 | 1.GET /policy/v1/policy/analysis/effect，查询参数取组合 EFF-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | | INTEG | | | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01430 | 政策分析 | 政策效果评估 | 异常-入参-非法limit | — | 政策效果评估 | 效果评估 | 效果评估 limit 非法，不传 scope_code | 1、不传 scope_code，与 sampleRequest 一致 | 1.GET /policy/v1/policy/analysis/effect，查询参数取组合 EFF-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 effect_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | | INTEG | | | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EFF-01 | policy.effect.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| EFF-02 | policy.effect.main | scope_code=440000（params 说明「如 440000」）；limit=20 | 单独补传可选 scope_code |
| EFF-03 | policy.effect.main | scope_code=440000；不传 limit | 单独省略可选 limit |
| EFF-04 | policy.effect.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| EFF-05 | policy.effect.main | 不传 scope_code；limit=-1 | 只破坏 limit |

两参数同时都不传不单列：主流程已覆盖「不传 scope_code」，备选 EFF-03 已覆盖「不传 limit」。

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 效果评估 | policy.effect.main | GET | /policy/v1/policy/analysis/effect | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.effect.main | API-01426、01427、01428、01429、01430 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「效果评估」在功能点列出现，且有 1 条主流程（API-01426）
- [x] 正向：sampleRequest 全参（仅 limit）+ 单独补传 scope_code + 单独省略 limit；预期逐字段写出 sampleResponse（scope_name、scope_code、effect_score、impl_effect）
- [x] 反向：scope_code、limit 各恰好 1 条非法；预期为 message 或 msg 指出该参数非法
- [x] unavailable 仍按文档返回体写主流程，备注注明未交付
- [x] 无登录 / Token / 401 / 424 / 契约占位 / 只写 HTTP 4xx 的预期
- [x] 未按 L37 field 一行一用例
- [x] `coverage-fp.md` 已同步 API-01426～01430
- [ ] `code-registry.yaml` 由父控回写（本子任务不改注册表）

**统计**：用例 **5** 条；主流程 **1**、备选 **2**、反向 **2**；编号闭区间 **API-01426**～**API-01430**（父控 R2-批10 分配）。
