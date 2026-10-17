# 智能服务集群-科技专题服务算法库测试用例（产业热点领域识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业热点领域识别  
> **catalog**：`entry_id=chain.hotspot` · `catalog_page_id=chain.hotspot` · path `/chain/hotspot`  
> **A 线对照**：`fp-split-by-api-run/work/L17.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（50897 试调 2026-10-17）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView 默认 `admin` / `gkx@2026`，密码经 AES-CFB 加密提交）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message`（试调无 token：`HTTP 424`，`code=1`，`msg=token expired`） |
| 断言分工 | **API-00059（金样）**断言**完整原始信封**（HTTP + `code` + `data` 类型）；同册其余用例断言 HTTP/`code` 或 **data 载荷**，前置写「信封成功规则见 §0，金样见 API-00059」 |
| catalog 与现场 | `chain.hotspot.hot` 在 catalog 为 `status=unavailable`；50897 试调在有效鉴权下 **仍返回 200 成功信封 + mock 载荷**（`data.honesty=mock`），以本条 as-built 为准，不得将 sample 数值写入预期 |
| 试调 observed（仅记录，非预期） | `GET /innov/v1/industry/INB1702/hotspot` → `code=0`，`data` 为对象，含 `number` 型 `hotspot_score`、`array` 型 `hot_news`（元素含 `title`、`views`）；非法 id `__invalid__` → `code=1`，`data=null`，`msg` 提示 chainId 格式 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id（如有）。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00059 | 产业链分析 | 产业热点领域识别 | 主流程-热点成功 | 金样信封 | 产业热点领域识别 | M4 热点识别 | 热点识别在有效鉴权下返回成功信封与契约字段 | 1、已按 §0 取得有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/industry/INB1702/hotspot（path 参数取组合 HOT-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data 中 hotspot_score 存在且为 number；5、data 中 hot_news 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.4 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/hotspot | | FULL | | | endpoint_id=chain.hotspot.hot catalog_page_id=chain.hotspot 组合=HOT-01 金样 50897试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00060 | 产业链分析 | 产业热点领域识别 | 异常-非法chainId | 入参校验 | 产业热点领域识别 | M4 热点识别 | 非法 chainId 时热点接口返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/__invalid__/hotspot（path 参数取组合 HOT-02） | 1、响应 code 不属于成功集合或 HTTP 为 4xx；2、message 或 msg 非空；3、不得将失败当作空热点或正常 hotspot_score/hot_news 业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.4 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/hotspot | | FULL | | | endpoint_id=chain.hotspot.hot catalog_page_id=chain.hotspot 组合=HOT-02 矩阵覆盖_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00061 | 产业链分析 | 产业热点领域识别 | 异常-鉴权 | 缺Token | 产业热点领域识别 | M4 热点识别 | 缺有效 token 时热点接口拒绝访问 | 1、请求不携带 Authorization 与 TENANT-ID（或 token 已失效） | 1.GET /innov/v1/industry/INB1702/hotspot（path 参数取组合 HOT-01），skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务热点载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.4 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/hotspot | | FULL | | | endpoint_id=chain.hotspot.hot catalog_page_id=chain.hotspot 组合=HOT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00062 | 产业链分析 | 产业热点领域识别 | 契约-不可用 | catalog占位 | 产业热点领域识别 | M4 热点识别 | catalog 标记 unavailable 时契约未交付态可识别 | 1、已确认 catalog `chain.hotspot.hot` 为 unavailable；2、已读 §0 as-built（50897 可能仍 mock） | 1.对照 catalog 与 A 线 L17 不可用口径；2.若环境为契约未交付网关，GET /innov/v1/industry/INB1702/hotspot（组合 HOT-01） | 1、不得将「契约未交付/不可用」当作含可信 hotspot_score 与 hot_news 的成功业务结果验收；2、未交付时应为可识别错误、占位或明确不可用语义（非伪高分）；3、若 50897 仍返回 mock 成功，记录 as-built 偏差，不以 sample 数值判绿 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.4 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/hotspot | | FULL | | | endpoint_id=chain.hotspot.hot catalog_page_id=chain.hotspot 组合=HOT-01 catalog_status=unavailable |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| HOT-01 | chain.hotspot.hot | path `chainId=INB1702`（catalog example，§0 试调有效，可替换） | 主路径合法产业 id |
| HOT-02 | chain.hotspot.hot | path `chainId=__invalid__` | 非法 id（单缺陷） |
| HOT-03 | chain.hotspot.hot | path `chainId=INB1701`（catalog 描述示例「无热点」） | 文档空态参考；**本轮无稳定空态构造**，见矩阵 `_empty` |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.hotspot.hot | GET | /innov/v1/industry/{chainId}/hotspot | unavailable | chainId |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.hotspot.hot | API-00059、API-00060、API-00061、API-00062 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-00062）+ 50897 主路径金样（API-00059）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（试调 INB1701 仍非空 mock）
- [x] 金样 1 条且断言完整信封（API-00059）
- [x] 50897 试调 1 条（§0 + API-00059 备注）
- [x] `coverage-fp.md` 已更新
- [x] `code-registry.yaml` 已回写 API-00059～00062
