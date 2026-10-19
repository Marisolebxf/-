# 智能服务集群-科技专题服务算法库测试用例（企业发展痛难点识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业发展痛难点识别  
> **catalog**：`entry_id=entan.pain-points` · `catalog_page_id=entan.pain-points` · path `/entan/pain-points`  
> **A 线对照**：`fp-split-by-api-run/work/L29.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业发展痛难点反映企业数（企业集合） | entan.pain-points.count |
| 2 | 企业发展痛难点严重度（企业集合） | entan.pain-points.severity |
| 3 | 痛难点改进差距 | entan.pain-points.count.m_ent_painpoint_gap |
| 4 | 发展痛难点诊断 | entan.pain-points.count.m_ent_painpoint_topic |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（执行期可替换为环境有效企业标识，组合表引用该组）。

本页 4 个接口均只有必填 `enterprise_codes`，无可选参数。每接口 1 条主流程（sampleRequest 全参）+ 1 条反向（缺 `enterprise_codes`）。`count` / `severity` 的 catalog `status=unavailable`，仍按文档返回体写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00956**～**API-00963**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.pain-points`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00956 | 企业分析 | 企业发展痛难点识别 | 主流程 | — | 企业发展痛难点识别 | 企业发展痛难点反映企业数（企业集合） | 企业发展痛难点反映企业数（企业集合）按文档示例 enterprise_codes 查询 | 1、enterprise_codes 使用文档示例四元组 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，组合 CNT-01 | 1、返回 body 含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_COUNT）、metric_name_zh（string，样例痛难点反映企业数）；2、value 为 object，含 value.count（number，样例 12）；3、value.dimension_cards 为 array（responseFields 名 dimension_cards，样例位于 value 下）；4、dimension_cards 元素含 dimension（string）、issue_count（number）、priority（string）、affected_enterprise_count（number）；5、另含 data_source（string）、confidence（string）；6、calc_process 为 object，含 definition（string）、formula（string）、source_tables（array）、model_version（string） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | M_ENT_PAINPOINT_COUNT | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=CNT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00957 | 企业分析 | 企业发展痛难点识别 | 异常-入参-缺enterprise_codes | — | 企业发展痛难点识别 | 企业发展痛难点反映企业数（企业集合） | 企业发展痛难点反映企业数（企业集合）不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，组合 CNT-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 value.count 与 dimension_cards 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=CNT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00958 | 企业分析 | 企业发展痛难点识别 | 主流程 | — | 企业发展痛难点识别 | 企业发展痛难点严重度（企业集合） | 企业发展痛难点严重度（企业集合）按文档示例 enterprise_codes 查询 | 1、enterprise_codes 使用文档示例四元组 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，组合 SEV-01 | 1、返回 body 含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_SEVERITY）、metric_name_zh（string，样例痛难点严重度）；2、value 为 object，含 value.severity（object，样例键为技术、人才、资金、供应链，值为严重度文案）；3、value.dimension_cards 为 array（responseFields 名 dimension_cards）；4、dimension_cards 元素含 dimension（string）、issue_count（number）、priority（string）、affected_enterprise_count（number）；5、另含 data_source（string）、confidence（string）；6、calc_process 为 object，含 definition（string）、formula（string）、source_tables（array）、model_version（string） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | M_ENT_PAINPOINT_SEVERITY | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=SEV-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00959 | 企业分析 | 企业发展痛难点识别 | 异常-入参-缺enterprise_codes | — | 企业发展痛难点识别 | 企业发展痛难点严重度（企业集合） | 企业发展痛难点严重度（企业集合）不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，组合 SEV-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 value.severity 与 dimension_cards 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=SEV-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00960 | 企业分析 | 企业发展痛难点识别 | 主流程 | — | 企业发展痛难点识别 | 痛难点改进差距 | 痛难点改进差距按文档示例 enterprise_codes 查询 | 1、enterprise_codes 使用文档示例四元组 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute，组合 GAP-01 | 1、返回 body 含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_GAP）；2、含 hint（string，样例为 compute 响应说明，以实际调用为准）；3、responseFields 声明的 dimension_cards（array）应在返回体中可定位；样例未给出该数组元素子字段，不断言未列出的嵌套值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | M_ENT_PAINPOINT_GAP | INTEG | | | endpoint_id=entan.pain-points.count.m_ent_painpoint_gap catalog_page_id=entan.pain-points 组合=GAP-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00961 | 企业分析 | 企业发展痛难点识别 | 异常-入参-缺enterprise_codes | — | 企业发展痛难点识别 | 痛难点改进差距 | 痛难点改进差距不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute，组合 GAP-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 与 dimension_cards 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | | INTEG | | | endpoint_id=entan.pain-points.count.m_ent_painpoint_gap catalog_page_id=entan.pain-points 组合=GAP-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00962 | 企业分析 | 企业发展痛难点识别 | 主流程 | — | 企业发展痛难点识别 | 发展痛难点诊断 | 发展痛难点诊断按文档示例 enterprise_codes 查询 | 1、enterprise_codes 使用文档示例四元组 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute，组合 TPC-01 | 1、返回 body 含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_TOPIC）；2、含 hint（string，样例为 compute 响应说明，以实际调用为准）；3、responseFields 声明的 dimension_cards（array）应在返回体中可定位；样例未给出该数组元素子字段，不断言未列出的嵌套值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | M_ENT_PAINPOINT_TOPIC | INTEG | | | endpoint_id=entan.pain-points.count.m_ent_painpoint_topic catalog_page_id=entan.pain-points 组合=TPC-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00963 | 企业分析 | 企业发展痛难点识别 | 异常-入参-缺enterprise_codes | — | 企业发展痛难点识别 | 发展痛难点诊断 | 发展痛难点诊断不传 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute，组合 TPC-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 与 dimension_cards 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | | INTEG | | | endpoint_id=entan.pain-points.count.m_ent_painpoint_topic catalog_page_id=entan.pain-points 组合=TPC-02 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CNT-01 | entan.pain-points.count | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| CNT-02 | entan.pain-points.count | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| SEV-01 | entan.pain-points.severity | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| SEV-02 | entan.pain-points.severity | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| GAP-01 | entan.pain-points.count.m_ent_painpoint_gap | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| GAP-02 | entan.pain-points.count.m_ent_painpoint_gap | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |
| TPC-01 | entan.pain-points.count.m_ent_painpoint_topic | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| TPC-02 | entan.pain-points.count.m_ent_painpoint_topic | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页接口清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业发展痛难点反映企业数（企业集合） | entan.pain-points.count | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | enterprise_codes* | unavailable |
| 企业发展痛难点严重度（企业集合） | entan.pain-points.severity | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | enterprise_codes* | unavailable |
| 痛难点改进差距 | entan.pain-points.count.m_ent_painpoint_gap | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | enterprise_codes* | available |
| 发展痛难点诊断 | entan.pain-points.count.m_ent_painpoint_topic | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.pain-points.count | API-00956、00957 |
| entan.pain-points.severity | API-00958、00959 |
| entan.pain-points.count.m_ent_painpoint_gap | API-00960、00961 |
| entan.pain-points.count.m_ent_painpoint_topic | API-00962、00963 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例全参正向；每参数恰好 1 条反向（缺 enterprise_codes）；无可选参数，无备选-参数组合
- [x] unavailable（反映企业数、严重度）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 无鉴权类功能项、无纯状态码预期；反向预期为 message 或 msg 指出缺少 enterprise_codes
- [x] `coverage-fp.md` 已同步 API-00956～00963
- [ ] `code-registry` 回写：本子任务禁止改 registry，编号由父控闭区间分配

**统计**：接口 **4**；用例 **8** 条（主流程 **4**、反向 **4**）；编号闭区间 **API-00956**～**API-00963**（父控 R2-批2 分配，连续无跳号）。
