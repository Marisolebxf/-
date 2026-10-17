# 智能服务集群-科技专题服务算法库测试用例（载体分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 载体分析  
> **catalog**：`entry_id=innov.carriers` · `catalog_page_id=innov.carriers` · path `/innov/carriers`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.carriers`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.carriers` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/carriers/rank` · `GET /innov/v1/carriers/{carrierId}` · `GET /innov/v1/carriers/index-method` |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00769（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析 `data`）；同册其余用例在前置写「信封规则见 §0，金样见 API-00769」后，可只断言 `data` 载荷或失败态 |
| catalog 状态 | 本页 **3** 个 endpoint 均为 catalog `status=running`、`runtime=java_api`；**禁止**将 `sampleResponse` 中载体名称、indexScore、rankTotal、权重 w 或子指数分值作为通过条件 |
| 页内语义 | 载体类型仅 `university` / `research` / `incubator`（catalog 页 summary）；本册不对类型枚举单独造 REST 入参 |
| 样例与契约差 | rank/detail 样例含 `total`、`period`、`subScores`、`radar` 等；契约 `responseFields` 对 rank 仅声明 `list`，对 detail 仅 `info`、`trend`，对 method 仅 `methodDesc`、`weights`。断言 **只强制 responseFields** |
| 依赖链 | 详情合法 `carrierId` 默认 `CAR-01`（catalog example）；执行期可先调 API-00769，若 `list` 非空则取首条 `carrierId` 替换，须在执行记录注明 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **3** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00769`～`00783`。`路由route` = catalog path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.carriers`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00769 | 创新监测 | 载体分析 | 主流程-排行成功 | 载体排行 | 载体分析 | 载体排行 | 载体排行在合法分页下返回成功信封与 list 字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RANK-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.list 存在且为 array；5、禁止将 sample 中 indexScore 或 rankTotal 具体值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RANK-01 金样 §0未试调 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00770 | 创新监测 | 载体分析 | 异常-鉴权 | 载体排行 | 载体分析 | 载体排行 | 载体排行缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/carriers/rank，查询参数取组合 RANK-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 list 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RANK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00771 | 创新监测 | 载体分析 | 异常-pageSize越界 | 载体排行 | 载体分析 | 载体排行 | 载体排行 pageSize 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RANK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 list 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RANK-02；矩阵挂 pageSize、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00772 | 创新监测 | 载体分析 | 异常-pageNum非法 | 载体排行 | 载体分析 | 载体排行 | 载体排行 pageNum 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/carriers/rank，查询参数取组合 RANK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RANK-03；矩阵挂 pageNum、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00773 | 创新监测 | 载体分析 | 备选-省略分页 | 载体排行 | 载体分析 | 载体排行 | 载体排行省略可选分页参数时响应可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/rank（无查询参数，组合 RANK-04） | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.list 为 array；4、禁止将 sample 条数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RANK-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00774 | 创新监测 | 载体分析 | 主流程-详情成功 | 载体详情 | 载体分析 | 载体详情 | 载体详情在合法 carrierId 下返回 info 与 trend | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/CAR-01（path 取组合 DET-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.info 存在且为 object；5、data.trend 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00775 | 创新监测 | 载体分析 | 异常-鉴权 | 载体详情 | 载体分析 | 载体详情 | 载体详情缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/carriers/CAR-01，组合 DET-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 info/trend 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00776 | 创新监测 | 载体分析 | 异常-非法carrierId | 载体详情 | 载体分析 | 载体详情 | 载体详情在非法 carrierId 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/carriers/__invalid__（组合 DET-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 info/trend 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-02；矩阵挂 carrierId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00777 | 创新监测 | 载体分析 | 异常-空carrierId | 载体详情 | 载体分析 | 载体详情 | 载体详情 path 段 carrierId 为空占位时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/carriers/%20（组合 DET-03，path 为空白编码） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与合法 CAR-01 成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-03；矩阵挂 carrierId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00778 | 创新监测 | 载体分析 | 备选-依赖排行id | 载体详情 | 载体分析 | 载体详情 | 载体详情使用排行接口取得的 carrierId 时契约字段可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、已调用 API-00769 且 data.list 非空并记录首条 carrierId，或沿用 §0 默认 CAR-01 | 1.GET /innov/v1/carriers/{carrierId}，path 取组合 DET-04 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.info 为 object且 data.trend 为 array | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00779 | 创新监测 | 载体分析 | 主流程-方法成功 | 指数方法与权重 | 载体分析 | 指数方法与权重 | 指数方法接口在有效鉴权下返回 methodDesc 与 weights | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/index-method（无查询参数，组合 METH-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.methodDesc 存在且为 string；5、data.weights 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=METH-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00780 | 创新监测 | 载体分析 | 异常-鉴权 | 指数方法与权重 | 载体分析 | 指数方法与权重 | 指数方法接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/carriers/index-method，组合 METH-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 methodDesc/weights 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=METH-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00781 | 创新监测 | 载体分析 | 异常-非法查询参数 | 指数方法与权重 | 载体分析 | 指数方法与权重 | 指数方法接口携带未登记查询参数时不得误判为契约失败以外的成功形态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/carriers/index-method，查询参数取组合 METH-02 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 非成功集合则为可识别失败；4、若 code 成功则仍须满足 data.weights 为 array（忽略未知查询键，不设权重数值断言） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=METH-02；矩阵挂 _fail（网关忽略或拒绝 observed） |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00782 | 创新监测 | 载体分析 | 备选-权重形态 | 指数方法与权重 | 载体分析 | 指数方法与权重 | 成功信封下 weights 元素形态可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/index-method，组合 METH-01 | 1、若 code 属成功集合且 data.weights 非空，则首条元素为 object；2、禁止将 sample 中 w=0.28 等具体权重作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=METH-01；矩阵挂 weights |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00783 | 创新监测 | 载体分析 | 备选-重复请求 | 指数方法与权重 | 载体分析 | 指数方法与权重 | 连续两次无参请求指数方法接口响应均可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00769 | 1.GET /innov/v1/carriers/index-method，组合 METH-01；2.立即重复步骤 1 一次 | 1、两次响应均含可解析 code；2、若两次 code 均成功则 data.methodDesc 均为 string 且 data.weights 均为 array；3、禁止要求两次 weights 内容完全一致 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M3 创新载体排行 | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=METH-01 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RANK-01 | innov.carriers.rank | `pageNum`: 1；`pageSize`: 20（对齐 catalog example） | 排行主路径 |
| RANK-02 | innov.carriers.rank | `pageNum`: 1；`pageSize`: -1 | pageSize 越界 |
| RANK-03 | innov.carriers.rank | `pageNum`: `not-a-number`；`pageSize`: 20 | pageNum 非法类型 |
| RANK-04 | innov.carriers.rank | 不传 pageNum、pageSize | 省略可选分页 |
| DET-01 | innov.carriers.detail | path `carrierId`: `CAR-01`（catalog example） | 详情主路径 |
| DET-02 | innov.carriers.detail | path `carrierId`: `__invalid__` | 非法 id |
| DET-03 | innov.carriers.detail | path `carrierId`: 空白（URL 编码 `%20`） | 空占位 id |
| DET-04 | innov.carriers.detail | path `carrierId`: 取自 API-00769 首条 `carrierId`，缺省 `CAR-01` | 列表→详情依赖 |
| METH-01 | innov.carriers.method | 无查询参数 | 方法主路径 |
| METH-02 | innov.carriers.method | 未登记查询键 `debug`: `1` | 未知查询参数 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| innov.carriers.rank | GET | /innov/v1/carriers/rank | running | 无（pageNum、pageSize 可选） |
| innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | running | path carrierId |
| innov.carriers.method | GET | /innov/v1/carriers/index-method | running | 无 |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.carriers.rank | API-00769、00770、00771、00772、00773 |
| innov.carriers.detail | API-00774、00775、00776、00777、00778 |
| innov.carriers.method | API-00779、00780、00781、00782、00783 |

---

## 3. 覆盖自检（§S1）

- [x] 3 个 running endpoint 各 1 条主路径（API-00769、00774、00779），未写 sample 数值通过条件
- [x] 异常-鉴权 3 条（00770、00775、00780）
- [x] rank 入参单缺陷 2 条 + 省略可选 1 条；detail 非法/空 id + 依赖链；method 未知查询 + 形态/重复
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（§0 未试调）
- [x] 金样 1 条且断言完整信封（API-00769）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` / `run-log.md` 由父控回写（本子任务 **未改** registry / run-log）

**统计**：用例 **15** 条；编号 **API-00769**～**API-00783**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **15**（00769～00783） |
| 金样（完整信封） | **1**（00769） |
| live 主路径 | **3**（rank/detail/method 各 1） |
| 异常-鉴权 | **3** |
| `_empty` 矩阵 | **3** 行 **未覆盖** |
| `_fail` 矩阵 | **3** 行 **已覆盖**（入参/鉴权哨兵） |
| 步骤以 GET+path 开头（抽检 00769、00776、00781） | **通过** |
| 预期无页面/图表表述（抽检 00770、00774、00782） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| A 线 `work` 检索 `innov.carriers` | **0 命中** |
