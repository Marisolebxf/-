# 智能服务集群-科技专题服务算法库测试用例（产业链全景 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 产业链全景  
> **catalog**：`entry_id=chain.panorama` · `catalog_page_id=chain.panorama` · path `/chain/panorama`  
> **调试台**：50897（文档位置，不写入用例步骤）  
> **A 线对照**：`fp-split-by-api-run/work/L05.md`、`L06.md`、`L14.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批5）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | A/B/C 按 op_id 写入 | chain.panorama.ops | running |
| 2 | 全景图谱 | chain.panorama.main | running |
| 3 | 产业链全景模型 | chain.panorama.m_chain_deep_117_1 | available |

**sampleRequest 取值**：写入类 path/body `op_id=CHAIN_NER_INDUSTRY`，body `scope=one`、`id=INB13`、`mode=rule`、`dry_run=true`（不含 filter、relation_whitelist、dest_types）。全景图谱 path `chainId=INB13`。产业链全景模型 body 按 sampleRequest 使用键 `chain_id=INB1701`（params.name 为 `chainId`，example 为 `INB170101`）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01220**～**API-01238**，闭区间 19 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.panorama`、组合 id。旧号 API-00001～00888 作废，本册不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01220 | 图谱 | 产业链全景 | 主流程 | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入按文档 sampleRequest（op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true）请求 | 1、path 与 body 使用文档 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-01 catalog_status=running 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01221 | 图谱 | 产业链全景 | 备选-参数组合 | 省略 id | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入省略 sampleRequest 中的可选参数 id，其余保持 sample 合法值 | 1、不传 id，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-02 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01222 | 图谱 | 产业链全景 | 备选-参数组合 | 传入 filter | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入在 sampleRequest 之外传入可选参数 filter，其余保持 sample 合法值 | 1、filter={"all":true}，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-03 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-03 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01223 | 图谱 | 产业链全景 | 备选-参数组合 | 省略 mode | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入省略 sampleRequest 中的可选参数 mode，其余保持 sample 合法值 | 1、不传 mode，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-04 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-04 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01224 | 图谱 | 产业链全景 | 备选-参数组合 | 省略 dry_run | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入省略 sampleRequest 中的可选参数 dry_run，其余保持 sample 合法值 | 1、不传 dry_run，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-05 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-05 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01225 | 图谱 | 产业链全景 | 备选-参数组合 | 传入 relation_whitelist | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入在 sampleRequest 之外传入可选参数 relation_whitelist，其余保持 sample 合法值 | 1、relation_whitelist=["depends_on"]，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-06 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-06 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01226 | 图谱 | 产业链全景 | 备选-参数组合 | 传入 dest_types | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入在 sampleRequest 之外传入可选参数 dest_types，其余保持 sample 合法值 | 1、dest_types=["enterprise"]，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-07 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，sampleResponse 多出字段，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组，无元素嵌套字段）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组，无元素嵌套字段）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组，无元素嵌套字段）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，sampleResponse 多出字段，示例 rule）；llm_fallback（boolean，sampleResponse 多出字段，示例 false）；calc_batch_id（string，sampleResponse 多出字段，示例空串） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-07 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01227 | 图谱 | 产业链全景 | 异常-入参-缺op_id | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传必填参数 op_id | 1、path 与 body 均不传 op_id，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-08 | 1、返回 body 的 message 或 msg 指出 op_id 缺失；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-08 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01228 | 图谱 | 产业链全景 | 异常-入参-缺scope | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入不传必填参数 scope | 1、不传 scope，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-09 | 1、返回 body 的 message 或 msg 指出 scope 缺失；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-09 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01229 | 图谱 | 产业链全景 | 异常-入参-非法id | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 id 取非法值 | 1、id=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-10 | 1、返回 body 的 message 或 msg 指出 id 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-10 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01230 | 图谱 | 产业链全景 | 异常-入参-非法filter | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 filter 取非法值 | 1、filter=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-11 | 1、返回 body 的 message 或 msg 指出 filter 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-11 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01231 | 图谱 | 产业链全景 | 异常-入参-非法mode | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 mode 取非法值 | 1、mode=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-12 | 1、返回 body 的 message 或 msg 指出 mode 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-12 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01232 | 图谱 | 产业链全景 | 异常-入参-非法dry_run | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 dry_run 取非法值 | 1、dry_run=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-13 | 1、返回 body 的 message 或 msg 指出 dry_run 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-13 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01233 | 图谱 | 产业链全景 | 异常-入参-非法relation_whitelist | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 relation_whitelist 取非法值 | 1、relation_whitelist=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-14 | 1、返回 body 的 message 或 msg 指出 relation_whitelist 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-14 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01234 | 图谱 | 产业链全景 | 异常-入参-非法dest_types | — | 产业链全景 | A/B/C 按 op_id 写入 | A/B/C 按 op_id 写入可选参数 dest_types 取非法值 | 1、dest_types=__invalid__，其余保持 sampleRequest | 1.POST /chain/v1/chain/graph/ops/{op_id}，组合 OPS-15 | 1、返回 body 的 message 或 msg 指出 dest_types 非法；2、不返回含 written_nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | | INTEG | | | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-15 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01235 | 图谱 | 产业链全景 | 主流程 | — | 产业链全景 | 全景图谱 | 全景图谱按文档 sampleRequest chainId=INB13 查询 | 1、path chainId 使用文档示例 INB13 | 1.GET /chain/v1/chain/{chainId}/panorama，组合 PAN-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：nodes（array，responseFields 环节节点，示例为空数组，无元素嵌套字段）；edges（array，responseFields 上下游关系，示例为空数组，无元素嵌套字段）；source（string，sampleResponse 多出字段，示例 demo_gkx_chain）；space（string，sampleResponse 多出字段，示例 demo_gkx_chain） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama | M_CHAIN_NODE_COUNT | INTEG | | | endpoint_id=chain.panorama.main catalog_page_id=chain.panorama 组合=PAN-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01236 | 图谱 | 产业链全景 | 异常-入参-缺chainId | — | 产业链全景 | 全景图谱 | 全景图谱不传必填参数 chainId | 1、path 不传 chainId | 1.GET /chain/v1/chain/{chainId}/panorama，组合 PAN-02 | 1、返回 body 的 message 或 msg 指出 chainId 缺失；2、不返回含 nodes 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama | | INTEG | | | endpoint_id=chain.panorama.main catalog_page_id=chain.panorama 组合=PAN-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01237 | 图谱 | 产业链全景 | 主流程 | — | 产业链全景 | 产业链全景模型 | 产业链全景模型按文档 sampleRequest 传 chain_id=INB1701 | 1、body 使用 sampleRequest 键 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute，组合 DEEP-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_117_1）；hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute | M_CHAIN_DEEP_117_1 | INTEG | | | endpoint_id=chain.panorama.m_chain_deep_117_1 catalog_page_id=chain.panorama 组合=DEEP-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01238 | 图谱 | 产业链全景 | 异常-入参-缺chainId | — | 产业链全景 | 产业链全景模型 | 产业链全景模型不传必填参数 chainId | 1、body 不传 chainId，也不传 sampleRequest 的 chain_id | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute，组合 DEEP-02 | 1、返回 body 的 message 或 msg 指出 chainId 缺失；2、不返回含 metric_id 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute | | INTEG | | | endpoint_id=chain.panorama.m_chain_deep_117_1 catalog_page_id=chain.panorama 组合=DEEP-02 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| OPS-01 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 sampleRequest：op_id=CHAIN_NER_INDUSTRY；scope=one；id=INB13；mode=rule；dry_run=true | 主路径（sampleRequest） |
| OPS-02 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body：op_id=CHAIN_NER_INDUSTRY；scope=one；不传 id；mode=rule；dry_run=true | 省略可选 id |
| OPS-03 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，另传 filter={"all":true} | 传入可选 filter |
| OPS-04 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body：op_id=CHAIN_NER_INDUSTRY；scope=one；id=INB13；不传 mode；dry_run=true | 省略可选 mode |
| OPS-05 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body：op_id=CHAIN_NER_INDUSTRY；scope=one；id=INB13；mode=rule；不传 dry_run | 省略可选 dry_run |
| OPS-06 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，另传 relation_whitelist=["depends_on"] | 传入可选 relation_whitelist |
| OPS-07 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，另传 dest_types=["enterprise"] | 传入可选 dest_types |
| OPS-08 | chain.panorama.ops | path 不传 op_id（POST /chain/v1/chain/graph/ops，无 op_id 段）；body 不传 op_id；scope=one；id=INB13；mode=rule；dry_run=true | 缺必填 op_id |
| OPS-09 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body：op_id=CHAIN_NER_INDUSTRY；不传 scope；id=INB13；mode=rule；dry_run=true | 缺必填 scope |
| OPS-10 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 id=__invalid__ | 非法 id |
| OPS-11 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 filter=__invalid__ | 非法 filter |
| OPS-12 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 mode=__invalid__ | 非法 mode |
| OPS-13 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 dry_run=__invalid__ | 非法 dry_run |
| OPS-14 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 relation_whitelist=__invalid__ | 非法 relation_whitelist |
| OPS-15 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body 同 OPS-01，仅 dest_types=__invalid__ | 非法 dest_types |
| PAN-01 | chain.panorama.main | path chainId=INB13 | 主路径（sampleRequest） |
| PAN-02 | chain.panorama.main | path 不传 chainId（GET /chain/v1/chain//panorama，chainId 段缺省） | 缺必填 chainId |
| DEEP-01 | chain.panorama.m_chain_deep_117_1 | body 同 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101） | 主路径（sampleRequest） |
| DEEP-02 | chain.panorama.m_chain_deep_117_1 | body 为空对象：不传 chainId，也不传 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| A/B/C 按 op_id 写入 | chain.panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | op_id*；scope*；id?；filter?；mode?；dry_run?；relation_whitelist?；dest_types? | running |
| 全景图谱 | chain.panorama.main | GET | /chain/v1/chain/{chainId}/panorama | chainId* | running |
| 产业链全景模型 | chain.panorama.m_chain_deep_117_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.panorama.ops | API-01220～01234 |
| chain.panorama.main | API-01235、01236 |
| chain.panorama.m_chain_deep_117_1 | API-01237、01238 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现且各有 1 条主流程（API-01220、API-01235、API-01237）
- [x] 写入接口：sampleRequest 主流程 1 + 可选参数与 sample 相反的传/不传 6 + 每参数反向 8 = 15
- [x] 全景图谱、产业链全景模型：各 1 条主流程 + 必填 chainId 缺省反向 1 条
- [x] 正向预期逐字段写 sampleResponse（含 responseFields；数组示例为空，无元素嵌套）
- [x] 反向预期写 message 或 msg 指出该参数
- [x] 未写鉴权类用例，反向预期只写参数错误说明
- [x] status 以 catalog JSON 为准（running / running / available）
- [x] `coverage-fp.md` 已同步 API-01220～01238

**统计**：用例 **19** 条；主流程 **3**、备选 **6**、反向 **10**；编号闭区间 **API-01220**～**API-01238**（父控 R2-批5 分配）。
