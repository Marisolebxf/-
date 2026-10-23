# 智能服务集群-科技专题服务算法库测试用例（区域创新协同分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.synergy` · `catalog_page_id=comp.synergy` · path `#/industry-comp/synergy`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.synergy`  
> **A 线对照**：`fp-split-by-api-run/work/L60.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；双 endpoint 仅 region；金样主流程 SYN-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 创新协同 | comp.synergy.main | GET | unavailable |
| 2 | 区域创新协同分析模型 | comp.synergy.m_synth_191_1 | POST | available |

两个接口都只有可选参数 `region`（区域编码，string，required=false，example `440300`）。`sampleRequest` 均传 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。每个接口反向恰好 1 条：`region=__invalid__`。`创新协同` 的 catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。`GET /comp/v1/comp/innov-synergy` 为本页独占，与同模块 `region-vitality`、`element-synthesis` 等 path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute` 只挂 title「区域创新协同分析模型」。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01078**～**FUNC-01085**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.synergy`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01078 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 创新协同 | 验证创新协同功能，检查填写 region=440300 传 region=440300 后返回与 sampleResponse 同层字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「创新协同」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 协同指数，示例 68.5）、link（number，示例 214）、cross（number，示例 37）、effect（number，示例 71）；2、radar 为数组，元素含产学研（number，示例 74）、供应链（number，示例 70）、资本协同（number，示例 65）、跨城协同（number，示例 62）；3、bar_items 为数组，元素含 name（string）、value（number），示例深港 88、深莞 81、深惠 74、深珠 66、深汕 58；4、pie_items 为数组，元素含 name（string）、value（number），示例产学研 40、供应链 35、资本协同 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深港协同/88/1/高/跨境创新走廊、深莞协同/81/2/高/制造互补、深惠协同/74/3/中/产业外溢；6、nodes 为数组（responseFields 协同网络节点），元素含 id（string）、node_key（string）、name（string）、node_type（string）、weight（number），示例 e1/e1/深圳链主A/企业/48、e2/e2/莞制造B/企业/36、e3/e3/港科创C/企业/34、r1/r1/深研院/科研机构/42、r2/r2/港大联合/科研机构/38、t1/t1/领军人才X/人才/30、t2/t2/青年人才Y/人才/26、c1/c1/深圳/城市/44、c2/c2/东莞/城市/32、c3/c3/香港/城市/36；7、edges 为数组（responseFields 协同关系边），元素含 source（string）、target（string）、src_key（string）、dst_key（string）、relation（string），示例 e1/r1/e1/r1/产学研、e1/e2/e1/e2/供应链、e1/c1/e1/c1/属地、e2/c2/e2/c2/属地、e3/c3/e3/c3/属地、r1/t1/r1/t1/人才、r2/t2/r2/t2/人才、r1/r2/r1/r2/合作、e3/r2/e3/r2/产学研、c1/c2/c1/c2/跨城、c1/c3/c1/c3/跨城、e1/t1/e1/t1/聘用 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy | M_SYNTH_COLLAB_INDEX | INTEG |  | FUNC-01078 | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01079 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 创新协同 | 验证创新协同功能，检查不传可选 region 不传 region 后仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「创新协同」；4.不传 region，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，responseFields 协同指数，示例 68.5）、link（number，示例 214）、cross（number，示例 37）、effect（number，示例 71）；2、radar 为数组，元素含产学研（number，示例 74）、供应链（number，示例 70）、资本协同（number，示例 65）、跨城协同（number，示例 62）；3、bar_items 为数组，元素含 name（string）、value（number），示例深港 88、深莞 81、深惠 74、深珠 66、深汕 58；4、pie_items 为数组，元素含 name（string）、value（number），示例产学研 40、供应链 35、资本协同 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深港协同/88/1/高/跨境创新走廊、深莞协同/81/2/高/制造互补、深惠协同/74/3/中/产业外溢；6、nodes 为数组（responseFields 协同网络节点），元素含 id（string）、node_key（string）、name（string）、node_type（string）、weight（number），示例 e1/e1/深圳链主A/企业/48、e2/e2/莞制造B/企业/36、e3/e3/港科创C/企业/34、r1/r1/深研院/科研机构/42、r2/r2/港大联合/科研机构/38、t1/t1/领军人才X/人才/30、t2/t2/青年人才Y/人才/26、c1/c1/深圳/城市/44、c2/c2/东莞/城市/32、c3/c3/香港/城市/36；7、edges 为数组（responseFields 协同关系边），元素含 source（string）、target（string）、src_key（string）、dst_key（string）、relation（string），示例 e1/r1/e1/r1/产学研、e1/e2/e1/e2/供应链、e1/c1/e1/c1/属地、e2/c2/e2/c2/属地、e3/c3/e3/c3/属地、r1/t1/r1/t1/人才、r2/t2/r2/t2/人才、r1/r2/r1/r2/合作、e3/r2/e3/r2/产学研、c1/c2/c1/c2/跨城、c1/c3/c1/c3/跨城、e1/t1/e1/t1/聘用 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy | M_SYNTH_COLLAB_INDEX | INTEG |  | FUNC-01079 | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01080 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 创新协同 | 验证创新协同功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值 | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「创新协同」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 或 nodes 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/innov-synergy |  | INTEG |  | FUNC-01080 | endpoint_id=comp.synergy.main catalog_page_id=comp.synergy 组合=SYN-03 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01081 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 区域创新协同分析模型 | 验证区域创新协同分析模型功能，检查填写 region=440300 传 region=440300 后返回 metric_id、hint 与 responseFields 声明字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「区域创新协同分析模型」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_191_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 index（number，协同指数）、nodes（array，协同网络节点）、edges（array，协同关系边），sampleResponse 未给出这三字段的示例值，返回中应含 index、nodes、edges 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | M_SYNTH_191_1 | INTEG |  | FUNC-01081 | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01082 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 区域创新协同分析模型 | 验证区域创新协同分析模型功能，检查不传可选 region 不传 region 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「区域创新协同分析模型」；4.不传 region，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_191_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 index（number，协同指数）、nodes（array，协同网络节点）、edges（array，协同关系边）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | M_SYNTH_191_1 | INTEG |  | FUNC-01082 | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01083 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 区域创新协同分析模型 | 验证区域创新协同分析模型功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值 | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换至「算法测试」tab；3.接口下拉选择「区域创新协同分析模型」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute |  | INTEG |  | FUNC-01083 | endpoint_id=comp.synergy.m_synth_191_1 catalog_page_id=comp.synergy 组合=M191-03 场景=异常-入参-非法region catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01084 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 接口信息 | 验证区域创新协同分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（创新协同、区域创新协同分析模型）；3、默认项概览 method=GET、path=/comp/v1/comp/innov-synergy；4、切换后概览对应区域创新协同分析模型 POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01084 | catalog_page_id=comp.synergy 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01085 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新协同分析模型 | 区域创新协同分析 | 算法测试 | 验证区域创新协同分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新协同分析」；2.切换到「算法测试」tab；3.下拉切换到「区域创新协同分析模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「区域创新协同分析模型」；3、调用区 method 为 POST、path 为 /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01085 | catalog_page_id=comp.synergy 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| comp.synergy.main | FUNC-01078、01079、01080 |
| comp.synergy.m_synth_191_1 | FUNC-01081、01082、01083 |
| （页面清单） | FUNC-01084、01085 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-01078 创新协同、FUNC-01081 区域创新协同分析模型）
- [x] 各接口：sampleRequest 主流程 1 条 + 与 sample 相反不传 region 1 条备选 + region 1 条非法反向，各恰好 3 条
- [x] unavailable（创新协同）仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L60：`产业综合分析模型构建` / `区域创新协同分析模型`
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01078～01085

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **8** 条；主流程 **2**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-01078**～**FUNC-01085**（R3 返工 · comp.synergy）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **8** |
| 编号闭区间 | **FUNC-01078**～**FUNC-01085** |
| 接口向（不含清单） | **6** |
| 清单 | **2** |
| 主流程 | **2**（FUNC-01078、FUNC-01081） |
| 备选-参数组合 | **2**（01079、01082） |
| 反向 | **2**（01080、01083） |
| catalog_page_id | `comp.synergy` |
| endpoint 数 | **2** |
| 已删 API 册 | `API-区域创新协同分析-用例.md`（API-01820～01825 作废，不复用） |
| 鉴权用例 | **0** |
