# 智能服务集群-科技专题服务算法库测试用例（风险洞察（异步） FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.risk` · `catalog_page_id=innov.risk` · path `/innov/risk`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.risk`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 SUP-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 供应链风险图谱契约 | innov.risk.supply | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | sub_type*；enterprise_codes? | 2 |
| 2 | 发展痛难点契约 | innov.risk.pain | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | sub_type*；enterprise_codes? | 2 |

两个 title 的 catalog `status=running`。每个接口只有必填 `sub_type` 与可选 `enterprise_codes`，无其它参数。主流程跟 `sampleRequest` 全参：供应链 `sub_type=supply_chain` 且 `enterprise_codes` 为文档示例 `91440300MA5DA8YX7E`、`91440300752531479N`；痛难点 `sub_type=pain_points` 且 `enterprise_codes` 同上。反向恰好 1 条：省略 `sub_type`（不写备选、不写非法 sub_type）。合计 **4** 条接口调用 + §6.1 清单 **2** 条 = **6** 条。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01164**～**FUNC-01169**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.risk`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01164 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 供应链风险图谱契约 | 验证供应链风险图谱契约功能，检查填写 sub_type=supply_chain、enterprise_codes=[91440300MA5DA8YX7E,91440300752531479N] 传 sub_type=supply_chain 与文档示例 enterprise_codes 后返回图谱与风险字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、sub_type=supply_chain；enterprise_codes 使用 sampleRequest 双码 | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「供应链风险图谱契约」；4.填写 sub_type=supply_chain、enterprise_codes=[91440300MA5DA8YX7E,91440300752531479N]，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：summary.display_mode（string，示例 graph）、summary.data_time（string，示例 2026-07-30）、summary.enterprises（string 数组，示例 智芯科技、绿能装备）；2、nodes 为数组，元素含 id（string）、name（string）、relation_type（string）、influence_score（number）、is_key（boolean），示例 N1/智芯科技/core/86/true、N2/关键芯片供应商/supply/74/true；3、edges 为数组，元素含 src（string）、dst（string）、relation_type（string），示例 src=N2、dst=N1、relation_type=supply；4、key_nodes 为数组（responseFields 关键节点），元素含 name（string）、relation_type（string）、influence_score（number）、is_key（boolean）、suggestion（string），示例 关键芯片供应商/supply/74/true/备选供应商不足；5、break_risks 为数组（responseFields 断链风险），元素含 name（string）、risk_level（string）、impact（string）、suggestion（string），示例 关键芯片供应商/高/核心器件断供/引入第二货源 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | M_ENT_SUPPLY_CHAIN_RISK | INTEG |  | FUNC-01164 | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=SUP-01 场景=主流程 catalog_status=running 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01165 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 供应链风险图谱契约 | 验证供应链风险图谱契约功能，检查不传必填 sub_type 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 sub_type | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「供应链风险图谱契约」；4.不传 sub_type（请求体 {} 或不含 sub_type 字段），点击调用 | 1、返回面板 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 key_nodes 或 break_risks 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute |  | INTEG |  | FUNC-01165 | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=SUP-02 场景=异常-入参-缺sub_type catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01166 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 发展痛难点契约 | 验证发展痛难点契约功能，检查填写 sub_type=pain_points、enterprise_codes=[91440300MA5DA8YX7E,91440300752531479N] 传 sub_type=pain_points 与文档示例 enterprise_codes 后返回诊断与问题字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、sub_type=pain_points；enterprise_codes 使用 sampleRequest 双码 | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「发展痛难点契约」；4.填写 sub_type=pain_points、enterprise_codes=[91440300MA5DA8YX7E,91440300752531479N]，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：summary.diagnosis_method（string，示例 四维共性）、summary.data_time（string，示例 2026-07-30）；2、dimension_cards 为数组，元素含 dimension（string）、priority（string）、issue_count（number）、affected_enterprise_count（number），示例 tech_rd/高/3/4、financing/中/2/3；3、issues 为数组（responseFields 共性问题），元素含 title（string）、priority（string）、dimension（string）、affected_enterprise_count（number）、evidence（string），示例 高端人才招聘难/高/tech_rd/4/研发岗位空缺率高、融资渠道单一/中/financing/3/银行贷款占比过高 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | M_ENT_PAINPOINT_GAP | INTEG |  | FUNC-01166 | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=PAIN-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01167 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 发展痛难点契约 | 验证发展痛难点契约功能，检查不传必填 sub_type 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 sub_type | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「发展痛难点契约」；4.不传 sub_type（请求体 {} 或不含 sub_type 字段），点击调用 | 1、返回面板 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 issues 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute |  | INTEG |  | FUNC-01167 | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=PAIN-02 场景=异常-入参-缺sub_type catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01168 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 接口信息 | 验证风险洞察（异步）的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（供应链风险图谱契约、发展痛难点契约）；3、默认项概览 method=POST、path=/entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute；4、切换后概览对应发展痛难点契约 POST /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01168 | catalog_page_id=innov.risk 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01169 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险洞察（异步） | 算法测试 | 验证风险洞察（异步）的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「风险洞察（异步）」；2.切换至「算法测试」tab；3.接口下拉切换到「发展痛难点契约」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 2 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01169 | catalog_page_id=innov.risk 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SUP-01 | innov.risk.supply | sub_type=supply_chain；enterprise_codes=[91440300MA5DA8YX7E, 91440300752531479N] | 主路径全参（sampleRequest） |
| SUP-02 | innov.risk.supply | 不传 sub_type（请求体 {} 或不含 sub_type 字段） | 缺必填 sub_type |
| PAIN-01 | innov.risk.pain | sub_type=pain_points；enterprise_codes=[91440300MA5DA8YX7E, 91440300752531479N] | 主路径全参（sampleRequest） |
| PAIN-02 | innov.risk.pain | 不传 sub_type（请求体 {} 或不含 sub_type 字段） | 缺必填 sub_type |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 供应链风险图谱契约 | innov.risk.supply | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | sub_type*；enterprise_codes? | running |
| 发展痛难点契约 | innov.risk.pain | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | sub_type*；enterprise_codes? | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.risk.supply | FUNC-01164、01165 |
| innov.risk.pain | FUNC-01166、01167 |
| （页面清单） | FUNC-01168、01169 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title（供应链风险图谱契约、发展痛难点契约）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest 全参：supply_chain / pain_points + 文档示例 enterprise_codes 双码
- [x] 无其它参数，无备选；每个接口反向恰好 1 条，只省略 sub_type，不另写非法值
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的 summary、nodes、edges、dimension_cards）；反向预期为 message 或 msg 指出 sub_type 缺失或非法
- [x] 无登录 / Token / 401 / 424
- [x] A 线无对应 Lxx；未改 work
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01168、01169）
- [x] `coverage-fp.md` 已同步 FUNC-01164～01169；旧 API-01894～01897 作废

**统计**：合计 **6** 条（主流程 2、反向 2、清单 2）；编号闭区间 **FUNC-01164**～**FUNC-01169**（R3 · innov.risk）。金样 **FUNC-01164**（SUP-01）。
