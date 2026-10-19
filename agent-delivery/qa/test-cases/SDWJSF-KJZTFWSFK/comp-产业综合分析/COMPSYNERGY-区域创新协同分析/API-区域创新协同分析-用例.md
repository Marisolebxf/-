# 智能服务集群-科技专题服务算法库测试用例（区域创新协同分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域创新协同分析  
> **catalog**：`entry_id=comp.synergy` · `catalog_page_id=comp.synergy` · path `/industry-comp/synergy`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.synergy`  
> **A 线对照**：`fp-split-by-api-run/work/L60.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.synergy`；本册不访问）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批19）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 创新协同 | comp.synergy.main | GET | unavailable |
| 2 | 区域创新协同分析模型 | comp.synergy.m_synth_191_1 | POST | available |

两个接口都只有可选参数 `region`（区域编码，string，required=false，example `440300`）。`sampleRequest` 均传 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。每个接口反向恰好 1 条：`region=__invalid__`。`创新协同` 的 catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。`GET /comp/v1/comp/innov-synergy` 为本页独占，与同模块 `region-vitality`、`element-synthesis` 等 path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute` 只挂 title「区域创新协同分析模型」。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01820**～**API-01825**，连续用满；禁止复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.synergy`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01820 | 产业综合分析 | 区域创新协同分析 | 主流程 | — | 区域创新协同分析 | 创新协同 | 创新协同按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.GET /comp/v1/comp/innov-synergy，查询参数取组合 SYN-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 协同指数，示例 68.5）、link（number，示例 214）、cross（number，示例 37）、effect（number，示例 71）；2、radar 为数组，元素含产学研（number，示例 74）、供应链（number，示例 70）、资本协同（number，示例 65）、跨城协同（number，示例 62）；3、bar_items 为数组，元素含 name（string）、value（number），示例深港 88、深莞 81、深惠 74、深珠 66、深汕 58；4、pie_items 为数组，元素含 name（string）、value（number），示例产学研 40、供应链 35、资本协同 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深港协同/88/1/高/跨境创新走廊、深莞协同/81/2/高/制造互补、深惠协同/74/3/中/产业外溢；6、nodes 为数组（responseFields 协同网络节点），元素含 id（string）、node_key（string）、name（string）、node_type（string）、weight（number），示例 e1/e1/深圳链主A/企业/48、e2/e2/莞制造B/企业/36、e3/e3/港科创C/企业/34、r1/r1/深研院/科研机构/42、r2/r2/港大联合/科研机构/38、t1/t1/领军人才X/人才/30、t2/t2/青年人才Y/人才/26、c1/c1/深圳/城市/44、c2/c2/东莞/城市/32、c3/c3/香港/城市/36；7、edges 为数组（responseFields 协同关系边），元素含 source（string）、target（string）、src_key（string）、dst_key（string）、relation（string），示例 e1/r1/e1/r1/产学研、e1/e2/e1/e2/供应链、e1/c1/e1/c1/属地、e2/c2/e2/c2/属地、e3/c3/e3/c3/属地、r1/t1/r1/t1/人才、r2/t2/r2/t2/人才、r1/r2/r1/r2/合作、e3/r2/e3/r2/产学研、c1/c2/c1/c2/跨城、c1/c3/c1/c3/跨城、e1/t1/e1/t1/聘用 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy | M_SYNTH_COLLAB_INDEX | INTEG | | | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01821 | 产业综合分析 | 区域创新协同分析 | 备选-参数组合 | 省略 region | 区域创新协同分析 | 创新协同 | 创新协同不传可选 region（与 sample 相反） | 1、不传 region | 1.GET /comp/v1/comp/innov-synergy，查询参数取组合 SYN-02 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，responseFields 协同指数，示例 68.5）、link（number，示例 214）、cross（number，示例 37）、effect（number，示例 71）；2、radar 为数组，元素含产学研（number，示例 74）、供应链（number，示例 70）、资本协同（number，示例 65）、跨城协同（number，示例 62）；3、bar_items 为数组，元素含 name（string）、value（number），示例深港 88、深莞 81、深惠 74、深珠 66、深汕 58；4、pie_items 为数组，元素含 name（string）、value（number），示例产学研 40、供应链 35、资本协同 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深港协同/88/1/高/跨境创新走廊、深莞协同/81/2/高/制造互补、深惠协同/74/3/中/产业外溢；6、nodes 为数组（responseFields 协同网络节点），元素含 id（string）、node_key（string）、name（string）、node_type（string）、weight（number），示例 e1/e1/深圳链主A/企业/48、e2/e2/莞制造B/企业/36、e3/e3/港科创C/企业/34、r1/r1/深研院/科研机构/42、r2/r2/港大联合/科研机构/38、t1/t1/领军人才X/人才/30、t2/t2/青年人才Y/人才/26、c1/c1/深圳/城市/44、c2/c2/东莞/城市/32、c3/c3/香港/城市/36；7、edges 为数组（responseFields 协同关系边），元素含 source（string）、target（string）、src_key（string）、dst_key（string）、relation（string），示例 e1/r1/e1/r1/产学研、e1/e2/e1/e2/供应链、e1/c1/e1/c1/属地、e2/c2/e2/c2/属地、e3/c3/e3/c3/属地、r1/t1/r1/t1/人才、r2/t2/r2/t2/人才、r1/r2/r1/r2/合作、e3/r2/e3/r2/产学研、c1/c2/c1/c2/跨城、c1/c3/c1/c3/跨城、e1/t1/e1/t1/聘用 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy | M_SYNTH_COLLAB_INDEX | INTEG | | | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01822 | 产业综合分析 | 区域创新协同分析 | 异常-入参-非法region | — | 区域创新协同分析 | 创新协同 | 创新协同的 region 非法 | 1、region 取非法值 | 1.GET /comp/v1/comp/innov-synergy，查询参数取组合 SYN-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 或 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy | | INTEG | | | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01823 | 产业综合分析 | 区域创新协同分析 | 主流程 | — | 区域创新协同分析 | 区域创新协同分析模型 | 区域创新协同分析模型按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute，请求体取组合 M191-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_191_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 index（number，协同指数）、nodes（array，协同网络节点）、edges（array，协同关系边），sampleResponse 未给出这三字段的示例值，返回中应含 index、nodes、edges 且类型与声明一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | M_SYNTH_191_1 | INTEG | | | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01824 | 产业综合分析 | 区域创新协同分析 | 备选-参数组合 | 省略 region | 区域创新协同分析 | 区域创新协同分析模型 | 区域创新协同分析模型不传可选 region（与 sample 相反） | 1、不传 region | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute，请求体取组合 M191-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_191_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 index（number，协同指数）、nodes（array，协同网络节点）、edges（array，协同关系边）仍应出现，类型与主流程一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | M_SYNTH_191_1 | INTEG | | | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01825 | 产业综合分析 | 区域创新协同分析 | 异常-入参-非法region | — | 区域创新协同分析 | 区域创新协同分析模型 | 区域创新协同分析模型的 region 非法 | 1、region 取非法值 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute，请求体取组合 M191-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | | INTEG | | | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SYN-01 | comp.synergy.main | region=440300 | 主路径（sampleRequest） |
| SYN-02 | comp.synergy.main | 不传 region | 省略可选 region（与 sample 相反） |
| SYN-03 | comp.synergy.main | region=__invalid__ | 只破坏 region |
| M191-01 | comp.synergy.m_synth_191_1 | region=440300 | 主路径（sampleRequest，请求体） |
| M191-02 | comp.synergy.m_synth_191_1 | 不传 region | 省略可选 region（与 sample 相反） |
| M191-03 | comp.synergy.m_synth_191_1 | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 创新协同 | comp.synergy.main | GET | /comp/v1/comp/innov-synergy | region? | unavailable |
| 区域创新协同分析模型 | comp.synergy.m_synth_191_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | region? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.synergy.main | API-01820、01821、01822 |
| comp.synergy.m_synth_191_1 | API-01823、01824、01825 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01820 创新协同、01823 区域创新协同分析模型）
- [x] 每个接口：sampleRequest 主流程 + 与 sample 相反的不传 region 备选 + region 1 条非法反向
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 region 非法
- [x] unavailable（创新协同）仍按 sampleResponse 写主流程与备选，备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01820～01825；field_key 挂到本页 API 号，未一字段一条用例；未改 A 线 work

**步骤字数**：GET 步骤为 METHOD + path + 组合 id，49 字。POST 步骤保留同样句式后为 73 字：path `/entan/v1/synth-metric/metric/M_SYNTH_191_1/compute` 单独已 51 字，加上 `1.POST ` 为 58 字，再写组合 id 即超过 60。按金样保留完整 path 与组合 id。

**预期字数**：正向按 sampleResponse 逐字段展开，单条超过 60 字（本页条数锁定 6，不再拆条）。反向各 2 点，指出 region 非法。

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01820**～**API-01825**（父控 R2-批19，连续用满）。
