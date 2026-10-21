# 智能服务集群-科技专题服务算法库测试用例（城市对标 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.cities` · `catalog_page_id=innov.cities` · path `/innov/cities`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.cities`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 城市排名 | innov.cities.rank | GET | /innov/v1/cities/rank | scope? | 3 |
| 2 | 城市对标 | innov.cities.compare | GET | /innov/v1/cities/compare | cityCodes* | 2 |
| 3 | 政策建议 | innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | cityCode* | 2 |
| 4 | 指数方法与权重 | innov.cities.method | GET | /innov/v1/cities/index-method | 无 | 1 |

四个 title 均为 catalog `status=running`。合计 **8** 条接口调用 + §6.1 清单 **2** 条 = **10** 条。无参 1 条主流程；有参为 1 条主流程（跟 `sampleRequest`）+ 每个可选参数与 sample 相反的传/不传 1 条 + 每个参数 1 条反向。必填反向只省略该参数。

`城市排名` 的 `scope` 可选，`sampleRequest` 传 `scope=global`；与 sample 相反为不传 `scope`；反向为枚举外非法值。`城市对标` 必填 `cityCodes`，主流程用 `sampleRequest` 的 `440300,110000`（params.example 三城不单列）。`政策建议` 必填 path `cityCode`，主流程 `440300`，反向省略 path 段。`指数方法与权重` 无参，仅 1 条主流程。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01141`～`01150`（闭区间 **10** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.cities`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01141 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 城市排名 | 验证城市排名功能，检查填写 sampleRequest 所示参数 传 scope=global 后返回 period 与 list 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope=global | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「城市排名」；4.填写 scope=global，点击调用 | 1、返回面板 body 的 data 含 period（string，示例 2025）、list（array，responseFields 城市排名）；2、list 元素含 cityCode（string）、nameZh（string）、indexScore（number）、rankGlobal（number）、rankDomestic（number）、isBenchmark（number）、subScores（object，含 resource、institution、output、environment，均为 number）；3、示例三行：cityCode=US-BOS、nameZh=波士顿、indexScore=94.1、rankGlobal=1、rankDomestic=99、isBenchmark=1、subScores resource=95/institution=92/output=94/environment=90；cityCode=440300、nameZh=深圳、indexScore=88.6、rankGlobal=6、rankDomestic=1、isBenchmark=0、subScores resource=86/institution=84/output=92/environment=88；cityCode=110000、nameZh=北京、indexScore=87.2、rankGlobal=7、rankDomestic=2、isBenchmark=0、subScores resource=90/institution=88/output=85/environment=82 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG |  |  | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01142 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 城市排名 | 验证城市排名功能，检查不传可选 scope（与 sampleRequest 相反）后仍返回排名列表结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「城市排名」；4.不传 scope，点击调用（不传 scope），点击调用 | 1、返回面板 body 的 data 仍含 period（string）、list（array）；2、list 元素仍含 cityCode、nameZh、indexScore、rankGlobal、rankDomestic、isBenchmark、subScores（resource、institution、output、environment）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG |  |  | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01143 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 城市排名 | 验证城市排名功能，检查 scope 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope 取枚举外值 | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「城市排名」；4.填写 scope=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 scope 非法；2、不返回含 list 城市排名的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank |  | INTEG |  |  | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-03 场景=异常-入参-非法scope catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01144 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 城市对标 | 验证城市对标功能，检查填写 sampleRequest 所示参数 传 cityCodes=440300,110000 后返回 list 与 radar 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、cityCodes 使用 sampleRequest 440300,110000 | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「城市对标」；4.填写 cityCodes=440300,110000，点击调用 | 1、返回面板 body 的 data 含 list（array，responseFields 对标城市）、radar（array，sampleResponse 多出）；2、list 元素含 cityCode（string）、nameZh（string）、indexScore（number）、rankGlobal（number）、resource（number）、institution（number）、output（number）、environment（number）；3、示例两行：cityCode=440300、nameZh=深圳、indexScore=88.6、rankGlobal=6、resource=86、institution=84、output=92、environment=88；cityCode=110000、nameZh=北京、indexScore=87.2、rankGlobal=7、resource=90、institution=88、output=85、environment=82；4、radar 元素含创新资源、制度环境、创新产出、产业环境（number）；5、示例两行：创新资源=86、制度环境=84、创新产出=92、产业环境=88；创新资源=90、制度环境=88、创新产出=85、产业环境=82 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/compare |  | INTEG |  |  | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CMP-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01145 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 城市对标 | 验证城市对标功能，检查不传必填 cityCodes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 cityCodes | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「城市对标」；4.不传 cityCodes，点击调用（不传 cityCodes），点击调用 | 1、返回面板 body 的 message 或 msg 指出 cityCodes 缺失；2、不返回含 list、radar 的成功对标 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/compare |  | INTEG |  |  | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CMP-02 场景=异常-入参-缺cityCodes catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01146 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 政策建议 | 验证政策建议功能，检查按 sampleRequest 传 path cityCode=440300 后返回 title、contentMd 及 sampleResponse 扩展字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、cityCode=440300 | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「政策建议」；4.填写 pathcityCode=440300，点击调用 | 1、返回面板 body 的 data 含 title（string，responseFields 标题）、contentMd（string，responseFields Markdown 正文）；2、sampleResponse 还含 reportId（string）、generateMode（string）；3、示例 reportId=RPT-SZ-01、title=深圳城市创新能力政策建议、generateMode=rule、contentMd 为「## 建议」及两条「加强基础研究投入」「补齐制度环境短板」 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice |  | INTEG |  |  | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=ADV-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01147 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 政策建议 | 验证政策建议功能，检查不传必填 cityCode 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 cityCode | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「政策建议」；4.不传 path cityCode（请求 `/innov/v1/cities//advice`，path 段为空），点击调用 | 1、返回面板 body 的 message 或 msg 指出 cityCode 缺失；2、不返回含 title、contentMd 的成功建议 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice |  | INTEG |  |  | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=ADV-02 场景=异常-入参-缺cityCode catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01148 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 指数方法与权重 | 验证指数方法与权重功能，检查无参调用后返回文档示例中的 weightVersion、methodDesc、weights 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉选择「指数方法与权重」；4.不填写业务参数，点击调用 | 1、返回面板 body 的 data 含 weightVersion（string，示例 city-v1）、methodDesc（string，示例 四要素加权合成。）、weights（array，responseFields 权重展平）；2、weights 元素含 k（string）、desc（string）、w（number）；3、示例四行：k=创新资源、desc=人才与资金、w=0.28；k=制度环境、desc=政策与治理、w=0.22；k=创新产出、desc=论文专利、w=0.3；k=产业环境、desc=产业配套、w=0.2 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/index-method |  | INTEG |  |  | endpoint_id=innov.cities.method catalog_page_id=innov.cities 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01149 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 接口信息 | 验证M4 城市创新能力的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致（城市排名、城市对标、政策建议、指数方法与权重）；3、默认项概览 method=GET、path=/innov/v1/cities/rank；4、切换后概览对应城市对标 GET /innov/v1/cities/compare，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.cities 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01150 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M4 城市创新能力 | 算法测试 | 验证M4 城市创新能力的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M4 城市创新能力」；2.切换至「算法测试」tab；3.接口下拉切换到「指数方法与权重」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 GET、path 为 /innov/v1/cities/index-method；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 4 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.cities 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | innov.cities.rank | scope=global | 主路径（sampleRequest） |
| RNK-02 | innov.cities.rank | 不传 scope | 省略可选 scope（与 sample 相反） |
| RNK-03 | innov.cities.rank | scope=__invalid__ | 只破坏 scope |
| CMP-01 | innov.cities.compare | cityCodes=440300,110000 | 主路径（sampleRequest） |
| CMP-02 | innov.cities.compare | 不传 cityCodes | 缺必填 cityCodes |
| ADV-01 | innov.cities.advice | path cityCode=440300 | 主路径（sampleRequest） |
| ADV-02 | innov.cities.advice | 不传 path cityCode（请求 `/innov/v1/cities//advice`，path 段为空） | 缺必填 cityCode |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 城市排名 | innov.cities.rank | GET | /innov/v1/cities/rank | scope? | running |
| 城市对标 | innov.cities.compare | GET | /innov/v1/cities/compare | cityCodes* | running |
| 政策建议 | innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | cityCode* | running |
| 指数方法与权重 | innov.cities.method | GET | /innov/v1/cities/index-method | — | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.cities.rank | FUNC-01141、01142、01143 |
| innov.cities.compare | FUNC-01144、01145 |
| innov.cities.advice | FUNC-01146、01147 |
| innov.cities.method | FUNC-01148 |
| （页面清单） | FUNC-01149、01150 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-01141、01144、01146、01148）
- [x] 无参指数方法与权重仅 1 条主流程；城市排名 1 主流程 + 省略 scope 1 条 + 非法 scope 1 条；城市对标、政策建议各 1 主流程 + 省略必填 1 条
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 无对应 Lxx：功能项/子功能项写待挂需规
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 四接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01149、01150）
- [x] `coverage-fp.md` 已同步 FUNC-01141～01150

**统计**：catalog endpoint **4**；title **4**；FUNC 用例 **10** 条；主流程 **4**、备选 **1**、反向 **3**、清单 **2**；编号闭区间 **FUNC-01141**～**FUNC-01150**（R3 innov.cities）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **FUNC-01141**～**FUNC-01150** |
| 接口向（不含清单） | **8** |
| 主流程 | **4** |
| 备选-参数组合 | **1** |
| 反向 | **3** |
| 清单 | **2** |
| 已删 API 册 | `API-城市对标-用例.md`（API-01875～01882 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
