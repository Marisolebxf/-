# 智能服务集群-科技专题服务算法库测试用例（深圳产业链 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 深圳产业链  
> **catalog**：`entry_id=chain.topic-panorama` · `catalog_page_id=chain.topic-panorama` · path `/chain/topic-panorama`  
> **A 线对照**：`fp-split-by-api-run/work/L15.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批5）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | A/B/C 按 op_id 写入 | chain.topic-panorama.ops |
| 2 | 专题全景图谱 | chain.topic-panorama.main |
| 3 | 深圳产业链模型 | chain.topic-panorama.m_chain_deep_118_1 |

**试调取值**：写入 `op_id` 用文档示例 `CHAIN_NER_INDUSTRY`，`id` 用 `INB13`；全景 path `chainId` 用 `INB13`。深圳产业链模型 `sampleRequest` 键为 `chain_id=INB1701`（`params.name` 为 `chainId`，`params.example` 为 `INB170101`）。`sampleRequest` 已含可选 `id`、`mode`、`dry_run`，备选为不传；未含可选 `filter`、`relation_whitelist`、`dest_types`，备选为按 `params.example` 传入。必填反向缺省，可选反向非法值。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01239**～**API-01257**，闭区间 19 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.topic-panorama`、组合 id。旧号 API-00326～00339 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01239 | 图谱 | 深圳产业链 | 主流程 | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入按文档 sampleRequest（op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true）返回写入字段 | 1、path 与 body 取文档 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01240 | 图谱 | 深圳产业链 | 备选-参数组合 | 省略 id | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传可选 id，其余保持 sampleRequest | 1、不传 id，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-02 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01241 | 图谱 | 深圳产业链 | 备选-参数组合 | 传入 filter | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入传入可选 filter，其余保持 sampleRequest | 1、传入 filter 为空对象，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-03 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-03 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01242 | 图谱 | 深圳产业链 | 备选-参数组合 | 省略 mode | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传可选 mode，其余保持 sampleRequest | 1、不传 mode，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-04 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-04 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01243 | 图谱 | 深圳产业链 | 备选-参数组合 | 省略 dry_run | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传可选 dry_run，其余保持 sampleRequest | 1、不传 dry_run，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-05 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-05 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01244 | 图谱 | 深圳产业链 | 备选-参数组合 | 传入 relation_whitelist | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入传入可选 relation_whitelist，其余保持 sampleRequest | 1、传入 relation_whitelist 为空数组，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-06 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-06 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01245 | 图谱 | 深圳产业链 | 备选-参数组合 | 传入 dest_types | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入传入可选 dest_types，其余保持 sampleRequest | 1、传入 dest_types 为空数组，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-07 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 写入或计划写入节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 写入或计划写入边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields 跳过项及原因，示例为空数组，无元素嵌套字段）；source（string，responseFields 写入来源，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-07 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01246 | 图谱 | 深圳产业链 | 异常-入参-缺op_id | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传必填参数 op_id | 1、不传 path op_id，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-08 | 1、返回 body 的 message 或 msg 指出 op_id 缺失；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-08 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01247 | 图谱 | 深圳产业链 | 异常-入参-缺scope | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传必填参数 scope | 1、不传 scope，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-09 | 1、返回 body 的 message 或 msg 指出 scope 缺失；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-09 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01248 | 图谱 | 深圳产业链 | 异常-入参-非法id | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 id 换成非法值 | 1、仅 id 取非法值，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-10 | 1、返回 body 的 message 或 msg 指出 id 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-10 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01249 | 图谱 | 深圳产业链 | 异常-入参-非法filter | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 filter 换成非法值 | 1、仅 filter 取非法值，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-11 | 1、返回 body 的 message 或 msg 指出 filter 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-11 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01250 | 图谱 | 深圳产业链 | 异常-入参-非法mode | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 mode 换成非法值 | 1、仅 mode 取非法值，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-12 | 1、返回 body 的 message 或 msg 指出 mode 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-12 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01251 | 图谱 | 深圳产业链 | 异常-入参-非法dry_run | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 dry_run 换成非法值 | 1、仅 dry_run 取非法值，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-13 | 1、返回 body 的 message 或 msg 指出 dry_run 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-13 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01252 | 图谱 | 深圳产业链 | 异常-入参-非法relation_whitelist | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 relation_whitelist 换成非法值 | 1、仅 relation_whitelist 取非法值，其余保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-14 | 1、返回 body 的 message 或 msg 指出 relation_whitelist 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-14 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01253 | 图谱 | 深圳产业链 | 异常-入参-非法dest_types | — | 深圳产业链 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入将可选参数 dest_types 换成非法值 | 1、仅 dest_types 取非法值，其余参数保持 sampleRequest 合法值 | 1.POST /chain/v1/chain/graph/ops/{op_id}，path 与请求体取组合 OPS-15 | 1、返回 body 的 message 或 msg 指出 dest_types 非法或无法解析；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-15 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01254 | 图谱 | 深圳产业链 | 主流程 | — | 深圳产业链 | 专题全景图谱 | 专题全景图谱按文档 sampleRequest 的 chainId=INB13 返回全景字段 | 1、chainId 使用文档示例 INB13 | 1.GET /chain/v1/chain/{chainId}/panorama，path 取组合 PAN-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：nodes（array，responseFields 专题节点，示例为空数组，无元素嵌套字段）；edges（array，responseFields 结构边，示例为空数组，无元素嵌套字段）；source（string，sampleResponse 多出字段，示例 demo_gkx_chain）；space（string，sampleResponse 多出字段，示例 demo_gkx_chain） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama | M_CHAIN_NODE_COUNT | INTEG |  |  | endpoint_id=chain.topic-panorama.main catalog_page_id=chain.topic-panorama 组合=PAN-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01255 | 图谱 | 深圳产业链 | 异常-入参-缺chainId | — | 深圳产业链 | 专题全景图谱 | 专题全景图谱不传必填参数 chainId | 1、不传 path chainId | 1.GET /chain/v1/chain/{chainId}/panorama，path 取组合 PAN-02 | 1、返回 body 的 message 或 msg 指出 chainId 缺失；2、不返回含 nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama |  | INTEG |  |  | endpoint_id=chain.topic-panorama.main catalog_page_id=chain.topic-panorama 组合=PAN-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01256 | 图谱 | 深圳产业链 | 主流程 | — | 深圳产业链 | 深圳产业链模型 | 深圳产业链模型按文档 sampleRequest 的 chain_id=INB1701 返回指标字段 | 1、请求体按 sampleRequest，键 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute，请求体取组合 DEEP-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_118_1）；hint（string，sampleResponse 多出字段，示例为真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute | M_CHAIN_DEEP_118_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.m_chain_deep_118_1 catalog_page_id=chain.topic-panorama 组合=DEEP-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01257 | 图谱 | 深圳产业链 | 异常-入参-缺chainId | — | 深圳产业链 | 深圳产业链模型 | 深圳产业链模型不传必填参数 chainId | 1、不传 chainId，请求体不含 chain_id | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute，请求体取组合 DEEP-02 | 1、返回 body 的 message 或 msg 指出 chainId 缺失；2、不返回含 metric_id 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute |  | INTEG |  |  | endpoint_id=chain.topic-panorama.m_chain_deep_118_1 catalog_page_id=chain.topic-panorama 组合=DEEP-02 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| OPS-01 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=true | 主路径 sampleRequest |
| OPS-02 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；不传 id；mode=rule；dry_run=true | 省略可选 id（sample 已含） |
| OPS-03 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；filter={}；mode=rule；dry_run=true | 传入可选 filter（sample 未含，params.example 空对象） |
| OPS-04 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；不传 mode；dry_run=true | 省略可选 mode（sample 已含） |
| OPS-05 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；不传 dry_run | 省略可选 dry_run（sample 已含） |
| OPS-06 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=true；relation_whitelist=[] | 传入可选 relation_whitelist（sample 未含，params.example 空数组） |
| OPS-07 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=true；dest_types=[] | 传入可选 dest_types（sample 未含，params.example 空数组） |
| OPS-08 | chain.topic-panorama.ops | 不传 path op_id；body scope=one；id=INB13；mode=rule；dry_run=true | 缺必填 op_id |
| OPS-09 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 不传 scope；id=INB13；mode=rule；dry_run=true | 缺必填 scope |
| OPS-10 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=__invalid__；mode=rule；dry_run=true | 非法 id |
| OPS-11 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；filter=not-json；mode=rule；dry_run=true | 非法 filter |
| OPS-12 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=not-a-mode；dry_run=true | 非法 mode |
| OPS-13 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=not-a-bool | 非法 dry_run |
| OPS-14 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=true；relation_whitelist=not-a-list | 非法 relation_whitelist |
| OPS-15 | chain.topic-panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body scope=one；id=INB13；mode=rule；dry_run=true；dest_types=not-a-list | 非法 dest_types |
| PAN-01 | chain.topic-panorama.main | path chainId=INB13 | 主路径 sampleRequest |
| PAN-02 | chain.topic-panorama.main | 不传 path chainId | 缺必填 chainId |
| DEEP-01 | chain.topic-panorama.m_chain_deep_118_1 | body chain_id=INB1701（sampleRequest；params.name=chainId） | 主路径 sampleRequest |
| DEEP-02 | chain.topic-panorama.m_chain_deep_118_1 | 不传 chainId，body 不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| A/B/C 按 op_id 写入 | chain.topic-panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | op_id*；scope*；id?；filter?；mode?；dry_run?；relation_whitelist?；dest_types? | running |
| 专题全景图谱 | chain.topic-panorama.main | GET | /chain/v1/chain/{chainId}/panorama | chainId* | running |
| 深圳产业链模型 | chain.topic-panorama.m_chain_deep_118_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.topic-panorama.ops | API-01239～01253 |
| chain.topic-panorama.main | API-01254、01255 |
| chain.topic-panorama.m_chain_deep_118_1 | API-01256、01257 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现且各有 1 条主流程（API-01239、API-01254、API-01256）
- [x] 写入接口：sampleRequest 主流程 1 条；与 sample 相反的可选传/不传 6 条；8 个参数各 1 条反向（必填缺省、可选非法）
- [x] 专题全景图谱、深圳产业链模型：仅必填 chainId，各 1 条主流程 + 1 条缺省反向
- [x] 正向预期逐字段写 sampleResponse（含 responseFields；示例数组无元素嵌套）
- [x] 反向预期写 message 或 msg 指出该参数
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01239～01257
- [x] 本子任务不改 `code-registry.yaml`（父控回写）

**统计**：用例 **19** 条（主流程 3、备选 6、反向 10）；编号闭区间 **API-01239**～**API-01257**。
