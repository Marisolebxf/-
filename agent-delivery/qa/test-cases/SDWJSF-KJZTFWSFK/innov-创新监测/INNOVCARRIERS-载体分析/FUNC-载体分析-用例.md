# 智能服务集群-科技专题服务算法库测试用例（载体分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.carriers` · `catalog_page_id=innov.carriers` · path `/innov/carriers`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.carriers`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 RNK-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 载体排行 | innov.carriers.rank | GET | /innov/v1/carriers/rank | pageNum? pageSize? | 5 |
| 2 | 载体详情 | innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | carrierId* | 2 |
| 3 | 指数方法与权重 | innov.carriers.method | GET | /innov/v1/carriers/index-method | 无 | 1 |

三个 title 均为 catalog `status=running`。合计 **8** 条接口调用 + 清单 **2** 条 = **10** 条。载体排行：`sampleRequest` 为 `pageNum=1`、`pageSize=20`；与 sample 相反为不传 `pageNum`、不传 `pageSize`；`pageNum`、`pageSize` 各 1 条非法。载体详情：主流程 `carrierId=CAR-01`；必填反向为省略 `carrierId`。指数方法与权重无参，仅 1 条主流程。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01131**～**FUNC-01140**，共 **10** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.carriers`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01131 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体排行 | 验证载体排行功能，检查填写 pageNum=1、pageSize=20调用后返回 total、period 与 list 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1、pageSize=20 取自 sampleRequest | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体排行」；4.填写 pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 含 total（number，示例 3）、period（string，示例 2025）、list（array，responseFields 排行）；2、list 元素含 carrierId（string）、name（string）、carrierType（string）、indexScore（number）、rankTotal（number）、subScores（object）；3、subScores 含 output、quality、activity、performance（number）；4、示例三行：carrierId=CAR-01、name=清华大学、carrierType=university、indexScore=91.2、rankTotal=1、subScores output=88/quality=93/activity=86/performance=90；carrierId=CAR-02、name=中科院计算所、carrierType=research、indexScore=87.4、rankTotal=2、subScores output=84/quality=90/activity=82/performance=86；carrierId=CAR-03、name=南山孵化器、carrierType=incubator、indexScore=72.8、rankTotal=3、subScores output=70/quality=68/activity=80/performance=74 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG |  | FUNC-01131 | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-01 场景=主流程 catalog_status=running 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01132 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体排行 | 验证载体排行功能，检查不传可选 pageNum（与 sampleRequest 相反）且 pageSize=20 时仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 pageNum；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体排行」；4.不传 pageNum，填写 pageSize=20，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 carrierId、name、carrierType、indexScore、rankTotal、subScores；3、subScores 仍含 output、quality、activity、performance；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG |  | FUNC-01132 | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01133 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体排行 | 验证载体排行功能，检查不传可选 pageSize（与 sampleRequest 相反）且 pageNum=1 时仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；不传 pageSize | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体排行」；4.不传 pageSize，填写 pageNum=1，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 carrierId、name、carrierType、indexScore、rankTotal、subScores；3、subScores 仍含 output、quality、activity、performance；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG |  | FUNC-01133 | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-03 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01134 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体排行 | 验证载体排行功能，检查 pageNum 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum 取非法值；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体排行」；4.填写 pageNum=not-a-page、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank |  | INTEG |  | FUNC-01134 | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-04 场景=异常-入参-非法pageNum catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01135 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体排行 | 验证载体排行功能，检查 pageSize 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；pageSize 取非法值 | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体排行」；4.填写 pageNum=1、pageSize=not-a-size，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank |  | INTEG |  | FUNC-01135 | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-05 场景=异常-入参-非法pageSize catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01136 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体详情 | 验证载体详情功能，检查填写 pathcarrierId=CAR-01 传 carrierId=CAR-01 后返回 info、trend 与 radar 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、carrierId=CAR-01 | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体详情」；4.填写 pathcarrierId=CAR-01，点击调用 | 1、返回面板 body 的 data 含 info（object，responseFields 基本信息）、trend（array，responseFields 多期指数）、radar（array，sampleResponse 多出字段）；2、info 含 carrierId（string，示例 CAR-01）、name（string，示例 清华大学）、carrierType（string，示例 university）；3、trend 元素含 statPeriod（string）、indexScore（number）、rankTotal（number）；示例三期：statPeriod=2023、indexScore=86.1、rankTotal=2；statPeriod=2024、indexScore=88.7、rankTotal=1；statPeriod=2025、indexScore=91.2、rankTotal=1；4、radar 元素含 成果产出、成果质量、创新活跃、转化绩效（number）；示例 成果产出=88、成果质量=93、创新活跃=86、转化绩效=90 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} |  | INTEG |  | FUNC-01136 | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01137 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 载体详情 | 验证载体详情功能，检查不传必填 carrierId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 carrierId | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「载体详情」；4.不传 path carrierId（请求 `/innov/v1/carriers/`，path 段为空），点击调用 | 1、返回面板 body 的 message 或 msg 指出 carrierId 缺失或非法；2、不返回含 info、trend 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} |  | INTEG |  | FUNC-01137 | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-02 场景=异常-入参-缺carrierId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01138 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 指数方法与权重 | 验证指数方法与权重功能，检查无参调用后返回 weightVersion、methodDesc 与 weights 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无查询参数 | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.接口下拉选择「指数方法与权重」；4.保持请求参数为空，点击调用 | 1、返回面板 body 的 data 含 weightVersion（string，示例 carrier-v1，sampleResponse 多出字段）、methodDesc（string，responseFields 方法说明，示例 AHP 先验 × 熵权客观权重。）、weights（array，responseFields 权重）；2、weights 元素含 k（string）、desc（string）、w（number）；3、示例四行：k=成果产出、desc=论文/专利数量、w=0.28；k=成果质量、desc=高被引与授权、w=0.27；k=创新活跃、desc=近三年增量、w=0.22；k=转化绩效、desc=成果落地、w=0.23 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/index-method |  | INTEG |  | FUNC-01138 | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01139 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 接口信息 | 验证 M3 创新载体排行的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致（载体排行、载体详情、指数方法与权重）；3、默认项概览 method=GET、path=/innov/v1/carriers/rank；4、切换后概览对应载体详情 GET /innov/v1/carriers/{carrierId}，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01139 | catalog_page_id=innov.carriers 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01140 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M3 创新载体排行 | 算法测试 | 验证 M3 创新载体排行的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M3 创新载体排行」；2.切换至「算法测试」tab；3.下拉切换到「指数方法与权重」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「指数方法与权重」；3、调用区 method 为 GET、path 为 /innov/v1/carriers/index-method；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01140 | catalog_page_id=innov.carriers 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | innov.carriers.rank | pageNum=1；pageSize=20 | 主路径（sampleRequest） |
| RNK-02 | innov.carriers.rank | 不传 pageNum；pageSize=20 | 省略可选 pageNum（与 sample 相反） |
| RNK-03 | innov.carriers.rank | pageNum=1；不传 pageSize | 省略可选 pageSize（与 sample 相反） |
| RNK-04 | innov.carriers.rank | pageNum=not-a-page；pageSize=20 | 只破坏 pageNum |
| RNK-05 | innov.carriers.rank | pageNum=1；pageSize=not-a-size | 只破坏 pageSize |
| DET-01 | innov.carriers.detail | path carrierId=CAR-01 | 主路径（sampleRequest） |
| DET-02 | innov.carriers.detail | 不传 path carrierId（请求 `/innov/v1/carriers/`，path 段为空） | 缺必填 carrierId |

指数方法与权重无查询参数，不设组合 id。

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 载体排行 | innov.carriers.rank | GET | /innov/v1/carriers/rank | pageNum?；pageSize? | running |
| 载体详情 | innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | carrierId* | running |
| 指数方法与权重 | innov.carriers.method | GET | /innov/v1/carriers/index-method | — | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.carriers.rank | FUNC-01131、01132、01133、01134、01135 |
| innov.carriers.detail | FUNC-01136、01137 |
| innov.carriers.method | FUNC-01138 |
| （页面清单） | FUNC-01139、01140 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-01131 载体排行、FUNC-01136 载体详情、FUNC-01138 指数方法与权重）
- [x] 载体排行 1 主流程 + 省略 pageNum 1 条 + 省略 pageSize 1 条 + 非法 pageNum 1 条 + 非法 pageSize 1 条；载体详情 1 主流程 + 省略 carrierId 1 条；指数方法与权重仅 1 条主流程
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级为 `待挂需规` / `待挂需规`（innov.* 无 Lxx）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 三接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01131～01140；A 线 `work/` 未改
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：catalog endpoint **3**；title **3**；FUNC 用例 **10** 条；主流程 **3**、备选 **2**、反向 **3**、清单 **2**；编号闭区间 **FUNC-01131**～**FUNC-01140**（父控 R3 返工 · innov.carriers）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **FUNC-01131**～**FUNC-01140** |
| 接口向（不含清单） | **8** |
| 主流程 | **3**（FUNC-01131、01136、01138） |
| 备选-参数组合 | **2**（01132、01133） |
| 反向 | **3**（01134、01135、01137） |
| 清单 | **2**（01139、01140） |
| catalog_page_id | `innov.carriers` |
| endpoint 数 | **3** |
| 已删 API 册 | `API-载体分析-用例.md`（API-01867～01874 作废，不复用） |
| 鉴权用例 | **0** |
