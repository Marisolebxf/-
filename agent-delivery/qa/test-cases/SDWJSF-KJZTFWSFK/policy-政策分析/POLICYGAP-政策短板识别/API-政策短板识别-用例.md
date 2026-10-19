# 智能服务集群-科技专题服务算法库测试用例（政策短板识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策短板识别  
> **catalog**：`entry_id=policy.gap` · `catalog_page_id=policy.gap` · path `/policy/gap`  
> **A 线对照**：`fp-split-by-api-run/work/L38.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `policy.json`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 短板分析 | policy.gap.shortboard |

两个查询参数均可选：`scope_code`、`limit`。主流程对齐 `sampleRequest`：只传 `limit=20`，不传 `scope_code`。`scope_code` 的合法补传值取参数说明中的省/市编码示例 `440000`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01431**～**API-01435**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.gap`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01431 | 政策分析 | 政策短板识别 | 主流程 | — | 政策短板识别 | 短板分析 | 短板分析按文档示例只传 limit=20、不传 scope_code 时返回短板字段 | 1、limit 使用文档示例 20；不传 scope_code | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-01 | 1、返回 body 的 data 为数组；2、元素含 scope_name（string，sampleResponse 区域名）；3、元素含 shortboard_cnt（number，responseFields 短板数）；4、结构与 sampleResponse 一致，示例为汕尾市/9、河源市/7、梅州市/6 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | M_POLICY_SHORTBOARD_COUNT | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01432 | 政策分析 | 政策短板识别 | 备选-参数组合 | 补传 scope_code | 政策短板识别 | 短板分析 | 短板分析补传可选 scope_code=440000，limit 保持文档示例 20 | 1、scope_code=440000；limit=20 | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-02 | 1、返回 body 的 data 为数组；2、元素仍含 scope_name（string）、shortboard_cnt（number，responseFields 短板数）；3、结构与 sampleResponse 同类，示例字段仍为 scope_name 与 shortboard_cnt | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | M_POLICY_SHORTBOARD_COUNT | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01433 | 政策分析 | 政策短板识别 | 备选-参数组合 | 省略 limit | 政策短板识别 | 短板分析 | 短板分析不传可选 limit，scope_code 保持主路径不传 | 1、不传 scope_code；不传 limit | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-03 | 1、返回 body 的 data 为数组；2、元素仍含 scope_name（string）、shortboard_cnt（number，responseFields 短板数）；3、结构与 sampleResponse 同类，示例字段仍为 scope_name 与 shortboard_cnt | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | M_POLICY_SHORTBOARD_COUNT | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01434 | 政策分析 | 政策短板识别 | 异常-入参-非法scope_code | — | 政策短板识别 | 短板分析 | 短板分析 scope_code 非法，limit 保持文档合法值 20 | 1、limit=20 | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-04 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 shortboard_cnt 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01435 | 政策分析 | 政策短板识别 | 异常-入参-非法limit | — | 政策短板识别 | 短板分析 | 短板分析 limit 非法，scope_code 保持主路径不传 | 1、不传 scope_code | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 shortboard_cnt 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GAP-01 | policy.gap.shortboard | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| GAP-02 | policy.gap.shortboard | scope_code=440000；limit=20 | 只补传可选 scope_code（说明示例 440000） |
| GAP-03 | policy.gap.shortboard | 不传 scope_code；不传 limit | 只省略可选 limit |
| GAP-04 | policy.gap.shortboard | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| GAP-05 | policy.gap.shortboard | 不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 短板分析 | policy.gap.shortboard | GET | /policy/v1/policy/analysis/gap | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.gap.shortboard | API-01431、01432、01433、01434、01435 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「短板分析」在功能点列出现，且有 1 条主流程（API-01431）
- [x] 有参接口：sampleRequest 主流程 1 条；scope_code 补传 1 条、limit 省略 1 条；每个参数恰好 1 条非法反向（01434、01435）
- [x] unavailable 仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse（scope_name、shortboard_cnt）；反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01431～01435

**统计**：用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01431**～**API-01435**（父控 R2-批10 分配）。
