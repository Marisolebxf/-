# 智能服务集群-科技专题服务算法库测试用例（企业供应链关系分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业供应链关系分析  
> **catalog**：`entry_id=entan.supply-chain` · `catalog_page_id=entan.supply-chain` · path `/entan/supply-chain`  
> **A 线对照**：`fp-split-by-api-run/work/L30.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **联调台端口**：50897（环境说明，不写入步骤）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业供应链断链风险（企业集合） | entan.supply-chain.risk |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（可替换为环境有效企业标识）。本接口仅此 1 个必填参数，无可选参数。catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00964**～**API-00965**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.supply-chain`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00964 | 企业分析 | 企业供应链关系分析 | 主流程 | — | 企业供应链关系分析 | 企业供应链断链风险（企业集合） | 企业供应链断链风险（企业集合）按文档示例 enterprise_codes 返回断链风险字段 | 1、enterprise_codes 使用文档示例四元组 | 1.POST /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute，请求体取组合 SCR-01 | 1、返回 body 含 metric_id（string，sampleResponse 示例 M_ENT_SUPPLY_CHAIN_RISK）、metric_name_zh（string，示例供应链断链风险等级）；2、value 为 object，value.result 为 object，含 sub_type（string，示例 supply_chain）、report_status（string，示例 not_created）；3、value.result.summary 为 object，含 enterprises（string 数组，示例云启智元科技股份有限公司、星辰半导体香港有限公司）、relation_scope（string，示例 supplier）、display_mode（string，示例 graph）、data_time（string，示例 2026-09-03）；4、value.result.key_nodes 为 array，元素含 id、name、relation_type、suggestion（string），influence_score（number），is_key（boolean）；5、value.result.break_risks 为 array（responseFields 断链风险清单），元素含 id、name、risk_level、impact、suggestion（string），sampleResponse 示例两条（上游供应商 B/高、下游客户 C/中）；6、data_source（string，示例 real）、confidence（string，示例 high）；7、calc_process 为 object，含 definition、formula、model_version（string）与 source_tables（string 数组，示例 innov.analysis.supply_chain）。示例文案与数值说明 sampleResponse 形态，字段与结构须与文档一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | M_ENT_SUPPLY_CHAIN_RISK | INTEG | | | endpoint_id=entan.supply-chain.risk catalog_page_id=entan.supply-chain 组合=SCR-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00965 | 企业分析 | 企业供应链关系分析 | 异常-入参-缺enterprise_codes | — | 企业供应链关系分析 | 企业供应链断链风险（企业集合） | 企业供应链断链风险（企业集合）不传 enterprise_codes | 1、请求体不传 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute，请求体取组合 SCR-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 break_risks 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | | INTEG | | | endpoint_id=entan.supply-chain.risk catalog_page_id=entan.supply-chain 组合=SCR-02 catalog_status=unavailable |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SCR-01 | entan.supply-chain.risk | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| SCR-02 | entan.supply-chain.risk | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业供应链断链风险（企业集合） | entan.supply-chain.risk | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | enterprise_codes* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.supply-chain.risk | API-00964、00965 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「企业供应链断链风险（企业集合）」在功能点列出现且有 ≥1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例全参 1 条主流程；必填 enterprise_codes 恰好 1 条反向；无可选参数，无备选组合
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权用例；正向预期写出 sampleResponse 字段（含 value、break_risks 及子字段）；反向预期为 message/msg 指出缺少 enterprise_codes
- [x] `coverage-fp.md` 已同步 API-00964～00965

**统计**：接口 **1**；用例 **2** 条（主流程 **1**、反向 **1**）；编号闭区间 **API-00964**～**API-00965**（父控 R2-批2 分配）。第一轮旧号不复用、不保留旧行。

**步骤字数**：`1.POST` + 完整 path 已 61 字，再加组合 id 后步骤为 75 字，无法同时满足「完整 path」与「≤60 字」。本册按金样句式保留 METHOD、path、组合 id。
