# SVC-L2-ZHIKU 智库服务 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 科技服务全景 · 智库服务（子菜单，`service/think-tank`） |
| WBS | WBS-05-07（对端仅提供接口，本仓只做对接不做后台；不建表、不入库） |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技服务全景/智库服务.md` 序号 566–574（excel_row 569–577；数据梳理分析 566–568 / 专题功能实现 569–571 / 接口开发设计 572–574）；接口契约见 `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/05-展示五大模块-第三方API接口清单.md` §六 ZK-01～ZK-09 与 `对接文档/对端/智库门户对接-API接口文档-v1.1.md` |
| 覆盖行数 | 9 行（566、567、568、569、570、571、572、573、574），SRS 本四级 9 条全覆盖 |
| 状态 | **R1 已解除阻塞（2026-11-13 记录）** · 对端 `EXT-B4-ZHIKU` 已配置，9 端点业务码全 0 且有数；判定 **4 可演 / 5 部分可演 / 0 覆盖不到 / 0 blocked**；余对端 `industry` 过滤失效（ZK-GAP-01）、测试库数据（ZK-GAP-02）、iframe 放行（ZK-GAP-03）+ 本侧 G-01~G-05 |
| 任务ID | DISPLAY-DEMO-CASE-SVC-M1-L01 |

## 主路径一句话

进科技服务全景 → 智库服务 → 服务类型选「战略咨询」→ 切「智库报告」页签 → 主题选「人工智能」、时间范围选「近一年」→ 列表出现该主题报告卡（标题 / 类型 / 摘要 / 发布单位 / 日期）→ 点卡片在本系统 iframe 弹框内打开详情，关闭后回到原筛选；对端未配置时页面顶部显示「接口待接入」、各页签显示对应空态。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 566 | 智库服务 · 「服务类型」页签（5 张卡） | 服务类型：全部 / 政策研究 / 战略咨询 / 评估评价 / 人才培训 / 学术交流 | 打开页面；点服务类型卡 | GET `/display/v1/think-tank/enums` → ZK-03 GET `/admin-api/v1/enums` | `tab=report`（报告页枚举）/ 不传（全量） | 固定 5 张服务类型卡；每卡显示「N 项关联」，N 由列表数据前端派生（D5：不作指标、不挂四维就绪度）；点卡后服务类型下拉同步、列表仅保留该类型条目；对端未配置时卡片计数为 0 且顶部提示「接口待接入」 | ⚠️ 部分可演（R1）。BFF `GET /think-tank/enums` 实测 code=0，4 组枚举有值（report_type 4 / sub_type 3 / industry 13 / theme_class 6），「按服务类型」柱图与派生计数有源；但页面**无 5 张服务类型卡**（仅顶部一行文字 + 柱图，`matchService` 为死代码 = G-01），5 类中评估评价/人才培训/学术交流无对端映射源；服务类型主档 B1 仍缺（对端未提供）。 |
| 567 | 顶部筛选栏（主题 / 时间范围 / 时间标签） | 主题：全部 + ZK-03 下发的 industry / theme_class（12 项行业：传感器、低空经济、合成生物、机器人、集成电路、具身智能、人工智能、软件与信息服务、生物医药、数字创意、智能网联汽车、智能终端，实际以接口实时返回为准）；时间范围：全部 / 近一周 / 近一月 / 近一季 / 近一年；时间标签：全部 + 数据中存在的 yyyy-MM | 改任一筛选 | GET `/display/v1/think-tank/enums` → ZK-03；列表 GET `/display/v1/think-tank/reports` → ZK-01 | `status=published&page=1&page_size=100&industry=<主题值>`（外部研报按 entry_mode=external 分发） | 主题下拉取 ZK-03 实时值、不硬编码；切换后列表 total 与过滤结果一致；切「时间标签」不改右侧时间趋势曲线（原型既定行为）；专家页签下时间范围与时间标签置灰 | ⚠️ 部分可演（R1）。主题下拉有源：ZK-03 `industry` 实测 13 项、`theme_class` 6 项，非硬编码；但**切换主题后列表 total=0**——`reports?industry=人工智能`（库内 7 条同值记录）实测 0 条，`低空经济`/`传感器`/`其他` 同为 0，而 `reportType=1` 正常返 14 → 对端 reports 的 `industry` 列未回填（值只在 `industry_tags` 数组内），精确匹配失效。时间范围 / 时间标签为前端派生，可用。 |
| 568 | 右侧统计卡（成果 / 案例 / 建议 饼图 + 时间趋势） | 无（跟随当前页签数据） | 打开页面 / 切换页签 | GET `/display/v1/think-tank/achievements/stats` → ZK-04 GET `/admin-api/v1/achievements/stats` | 不传 industry 返回全部领域，按 total 倒序 | 饼图三类计数 = `achievement_count` / `suggestion_count` / `case_count` 之和；领域值「其他」可出现但不在枚举下发；服务类型关联计数不挂就绪度角标（D5）；时间段无数据显示 0 或空态，不补造曲线 | ⚠️ 部分可演（R1）。ZK-04 实测 code=0 返 5 个领域（人工智能 4 / 其他 2 / 传感器 …），饼图与时间趋势有源；但同页两套分类口径并存（G-03）、4 张图无空态覆层（G-04）、分页 total 取本地数组长度（G-02，当前 56<100 尚未暴露）。ZK-04 多领域重复计数，禁止与列表 total 直接相等。 |
| 569 | 5 个页签：服务类型 / 智库报告 / 智库活动 / 智库专家 / 智库成果；活动内「列表 / 活动历程」 | 页签切换；活动视图：列表 / 活动历程 | 点页签；切活动视图 | 报告 ZK-01 GET `/admin-api/v1/reports`；活动 ZK-05 POST `/delphi-questionnaire/page`；专家 ZK-07 POST `/expert/page`；成果 ZK-02 GET `/admin-api/v1/achievements` | 活动 `{"current":1,"size":100}`；专家 `{"current":1,"size":100}`；成果 `page=1&page_size=100` | 四类页签各有独立请求与独立空态：暂无智库报告 / 暂无智库活动 / 暂无智库专家 / 暂无智库成果；「活动历程」按 startDate 升序时间轴且与列表同批数据；活动仅德尔菲问卷一类（B2 口径） | ✅ 可演（R1）。四类页签请求独立、空态独立，实测全出数：报告 56 / 活动 16 / 专家 900 / 成果 9；活动「列表 / 活动历程」同批数据按 `startDate` 升序。「服务类」模块缺失归 566 的 G-01，不在本行重复计。 |
| 570 | 筛选栏 + 报告 / 成果卡片 + 详情弹框 | 服务类型 5 类；主题；时间范围；时间标签；卡片点击 | 改筛选；点卡片 | 列表 ZK-01 / ZK-02；详情走记录 `detail_url` 的 iframe（无字段级详情接口） | `status=published&page=1&page_size=100&industry=<值>&time_from=&time_to=` | 点卡片打开本系统内 iframe 弹框，URL = `detail_url`；`detail_url` 为空时回落详情抽屉；对端禁嵌时弹框右上「在新窗口打开」可降级；无地址时弹框显示「该条目未提供详情地址」；活动详情只显示 7 项汇总（名称 / 领域 / 起止日期 / 描述 / 预计专家数 / 参与专家数 / 完成率），不显示问答正文 | ⚠️ 部分可演（R1）。`detailUrl` 实测 20/20 非空（形如 `https://edu.itic-sci.com/zp-tts/zw/gallery/detail/{id}`），iframe 弹框路径成立、为空时回落详情抽屉；但服务类型不可筛（G-01），对端 `X-Frame-Options` / CSP 放行仍未书面确认（`SYSINT-05-07-04-L01`），禁嵌时只能「在新窗口打开」降级。 |
| 571 | 右侧「重大事件」侧栏 + 成果「建议」类 | 无；点击事件条 | 打开页面；点事件 | POST `/display/v1/think-tank/major-events/page` → ZK-09 POST `/major-event/page` | `{"current":1,"size":100}` | 侧栏列出 title + newsTypeName；点击按 `sourceUrl` 打开 iframe；`sourceUrl` 为空显示「该条目未提供详情地址」；无数据显示「暂无重大事件」；成果发布与政策建议由成果页签 strategySubType = 成果 / 建议 承载 | ✅ 可演（R1）。ZK-09 实测 code=0、total=7，`title` + `newsTypeName` 均非空、`sourceUrl` 有值可开 iframe；无数据时「暂无重大事件」空态不变。 |
| 572 | 分项查询（报告 / 成果 / 活动 / 专家） | 专家 Field（ZK-08 下发值）；分页 page / page_size（≤100） | 打开相应页签；选 Field | ZK-01 GET `/admin-api/v1/reports`；ZK-02 GET `/admin-api/v1/achievements`；ZK-03 GET `/admin-api/v1/enums`；ZK-04 GET `/admin-api/v1/achievements/stats`；ZK-05 POST `/delphi-questionnaire/page`；ZK-06 POST `/delphi-questionnaire/detail`；ZK-07 POST `/expert/page`；ZK-08 POST `/expert/field/options` | 例：ZK-07 `{"current":1,"size":100,"fieldId":"<Field ID>"}`；ZK-08 body `{}` | 四类对象各有独立端点且可分别调通；报告固定 `status=published`；分页越界按默认（page 默认 1、page_size 默认 20）；Field 下拉取 ZK-08，不硬编码 | ✅ 可演（R1）。8 个 BFF 端点实测业务码全 0（reports 56 / achievements 9 / enums 4 组 / stats 5 域 / activities 16 / experts 900 / field-options 13 项 / major-events 7）；`page_size≤100` 生效；Field 下拉取 ZK-08 实时值 13 项，非硬编码。 |
| 573 | 列表 ↔ 详情弹框 | 任一条目 | 点条目；关闭弹框 | ZK-01 / ZK-02 / ZK-05 / ZK-07（列表）+ `detail_url` iframe | 同序号 570 | 列表到详情传 `detail_url`（或 `questionnaireId` 调 ZK-06）；关闭弹框后回到原页签、原筛选与原页码；详情媒资由对端页面承载，本仓不聚合；活动缺 `questionnaireId` 时不发 ZK-06 | ✅ 可演（R1）。活动详情实测：传 `questionnaireId` → code=0 出 7 项汇总；传 `id` 被对端拒（`ZK_BAD_REQUEST`：questionnaireId 必填）。前端 `index.vue:794-796` 已按 questionnaireId 判空后调用，口径一致；报告 / 成果走 `detailUrl`。媒体资料仍无字段（D3 既定）。 |
| 574 | 跨页签口径一致性 | 同一服务类型 + 同一主题 | 依次查看服务类型卡 / 报告 / 成果 / 统计卡 | ZK-01 / ZK-02 / ZK-03 / ZK-04 | 同一 `industry=<值>` 分别下发给 ZK-01、ZK-02、ZK-04 | 同一主题在报告与成果列表的过滤结果可复现；ZK-04 按「多领域重复计数」口径，其合计不得与成果列表 total 直接相等比较；服务类型卡的「N 项关联」= 按该类型过滤后的列表 total（在 page_size 覆盖范围内）；不符时以对端口径为准并记录差异 | ⚠️ 部分可演（R1）。同一 `industry` 值可分别下发 ZK-01 / ZK-02 / ZK-04，但 ZK-01、ZK-02 实测过滤后 total 均为 0（同 567 根因），跨页签一致性无法校验；ZK-04 按多领域重复计数（人工智能 4 + 其他 2 + … ≠ 成果 total 9），符合既定口径但需在演示中说明。 |

## LOOP 对照汇总（M3 · 2026-11-08）

探测方式：网关 `http://10.50.69.111:30895`（StripPrefix=1），请求头 `Authorization: Bearer <display-loop-token>` + `systemCode: display`，逐条 curl 实测；POST body 以 `--data-binary @file` 提交。对端（智谱 zwrite-backend / topic-system）直连接口因 BASE_URL + 双凭证未给**未探**，按契约登记状态判定，不伪造 200。

**接口实测清单（BFF 侧，9 端点全调通）**

| BFF 端点（`/display/v1/think-tank`） | 对位 | 方法 | HTTP | body 判定 |
|---|---|---|---|---|
| `/enums` | ZK-03 | GET | 200 | `_error=ZK_NOT_CONFIGURED`，`enums=[]` |
| `/reports?page=1&pageSize=100` | ZK-01 | GET | 200 | `ZK_NOT_CONFIGURED`，`items=[]`、`total=0` |
| `/achievements?page=1&pageSize=100` | ZK-02 | GET | 200 | `ZK_NOT_CONFIGURED`，`items=[]`、`total=0` |
| `/achievements/stats` | ZK-04 | GET | 200 | `ZK_NOT_CONFIGURED`，`items=[]` |
| `/activities/page` `{current:1,size:100}` | ZK-05 | POST | 200 | `ZK_NOT_CONFIGURED`，`records=[]`、`total=0` |
| `/activities/detail` `{questionnaireId}` | ZK-06 | POST | 200 | `ZK_NOT_CONFIGURED`，`detail=null` |
| `/experts/page` `{current:1,size:100}` | ZK-07 | POST | 200 | `ZK_NOT_CONFIGURED`，`records=[]`、`total=0` |
| `/experts/field-options` `{}` | ZK-08 | POST | 200 | `ZK_NOT_CONFIGURED`，`options=[]` |
| `/major-events/page` `{current:1,size:100}` | ZK-09 | POST | 200 | `ZK_NOT_CONFIGURED`，`records=[]`、`total=0` |

> 九条响应 `_vendor` 一致：`source=not-configured`、`vendorMessage="智库接口未配置（地址或令牌为空）"`、`attempts=0`——BFF（`BE-DISPLAY-SVC-THINKTANK-API-L01`）已部署且信封/错误码透传正常，**阻塞点只剩对端配置**（段 A `Authorization: Bearer`、段 B `X-Portal-Access-Token` 两套凭证 + BASE_URL）。

**判定计数（M3 历史，已被 R1 取代）**

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演 | 0 | — |
| ⚠️ 部分可演 | 0 | — |
| ⛔ 待开发完成（接口待接入） | 9 | 566, 567, 568, 569, 570, 571, 572, 573, 574 |

**合计**：9 行 = 0 可演 + 0 部分可演 + 9 待开发完成。按总控 §1 拍板 12（开发就绪门）：对端未配置、库（对端）零供数，整叶 `blocked` 写「待开发完成」，不填可演、不拿「覆盖不到」充数；页面当前只能演示「接口待接入」顶部提示 + 各页签空态（属设计既定空态，不计可演行）。M5 LOOP 计划暂不编排本页，待对端配置到位后重测改判。

## R1 实测与判定（2026-11-13）

> 触发：对端 `EXT-B4-ZHIKU` 已配置（BASE_URL + 双凭证到位），`ZK_NOT_CONFIGURED` 消失。
> 实测时点：**2026-11-12 22:40–23:10**（`display-loop-token` 于 11-13 失效，401 `sso check-token failed`，本轮数字取自该次实测；复测需重新登录公网页面取 token 写入 `C:\Users\35197\.gkx\display-loop-token`）。
> 方法：内网网关 `http://10.50.69.111:30895`（StripPrefix=1），头 `Authorization: Bearer <token>` + `systemCode: display`，参数按用例口径（`page_size=100` / `{current:1,size:100}`）。

**9 端点实测（业务码全 0，无一 `ZK_NOT_CONFIGURED`）**

| BFF 端点 | 对位 | HTTP | 业务码 | 实测数据量 |
|---|---|---|---|---|
| `/reports?status=published&page=1&page_size=100` | ZK-01 | 200 | 0 | total=56（单次拉回 20，对端单页上限 20） |
| `/achievements?page=1&page_size=100` | ZK-02 | 200 | 0 | total=9 |
| `/enums` | ZK-03 | 200 | 0 | 4 组：report_type 4 / sub_type 3 / industry 13 / theme_class 6 |
| `/achievements/stats` | ZK-04 | 200 | 0 | 5 个领域（人工智能 4 / 其他 2 / 传感器 …） |
| `/activities/page` | ZK-05 | 200 | 0 | total=16 |
| `/activities/detail` | ZK-06 | 200 | 0 | 传 `questionnaireId` 出 7 项汇总；传 `id` → `ZK_BAD_REQUEST` |
| `/experts/page` | ZK-07 | 200 | 0 | total=900 |
| `/experts/field-options` | ZK-08 | 200 | 0 | 13 个领域选项 |
| `/major-events/page` | ZK-09 | 200 | 0 | total=7 |

**判定计数（R1）**

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演 | 4 | 569, 571, 572, 573 |
| ⚠️ 部分可演 | 5 | 566, 567, 568, 570, 574 |
| ⛔ 待开发完成 | 0 | — |
| 覆盖不到 | 0 | — |

**R1 缺口**

| 编号 | 缺口 | 责任方 | 处置 |
|---|---|---|---|
| ZK-GAP-01 | ZK-01 / ZK-02 的 `industry` 精确匹配失效：库内 `industry_tags` 有值、`industry` 列未回填（`人工智能` 7 条同值却过滤出 0） | 对端（智谱） | 回填 `industry` 列或下发正确过滤参数名；我方 BFF 按接口文档原样透传（`ThinkTankController:42/53/66/74`），不改口径 |
| ZK-GAP-02 | 对端为测试库：报告含「【测试】…」「ai」「电竞椅」「python大叔」，成果 9 条全「测试项目」，活动「test问卷2（第一轮）」，重大事件「马化腾的第一个标题」 | 对端（智谱） | 换正式库或清洗造数；否则业务演示会被现场看穿 |
| ZK-GAP-03 | 门户 `X-Frame-Options` / CSP `frame-ancestors` 放行未书面确认 | 对端 / `SYSINT-05-07-04-L01` | 联调时抓响应头确认；禁嵌走「在新窗口打开」降级 |
| G-01~G-05 | 本侧页面缺口（服务类型维度缺失、分页 total 取本地长度、两套分类口径、图表空态、顶部文案） | 我方 FE | 见 `agent-handoffs/展示对齐-DISPLAY/real-data-audit/2026-11-12-13-智库服务-逐屏核对与缺口验收单.md`；G-01 需 human 裁定「接 `matchService`」还是「立偏差单」 |

**与 M3 的差异**：M3（2026-11-08）因对端零供数判 9 行「待开发完成」并整叶 blocked；R1 对端已供数，按实证改判 **4 可演 + 5 部分可演**，**blocked 解除**。M3 的 9 行「数据情况」列已就地更新为 R1 结论，其判定计数表按历史保留。

### 缺口建单（M3 记录 · 整页 `EXT-B4-ZHIKU` 缺失已于 R1 解除，余 B1 主档与详情/iframe 项仍有效）

| 序号 | 缺口 | 根因 | 处置建议 | 责任方 |
|---|---|---|---|---|
| 566–574（整页） | `EXT-B4-ZHIKU` 未配置：对端测试环境 BASE_URL + 段 A `access_token` + 段 B `UC_ACCESS_TOKEN` 三件套未到 | 契约已登记（接口清单 §六）但凭证未交付；我方已发 `对接文档/我方/2026-11-06-智库服务-鉴权与联调申请.md` | 拿到三件套后配置 BFF（`ThinkTankProperties`），重测 9 端点；段 B 注意 HTTP 200 + body `code` 二次判码 | 对端（智谱）/ 对接人；升级 `human:李伟` |
| 566 | 服务类型主档无接口（B1） | 对端未提供主档，前端临时目录承载 | 等对端补主档后换映射；演示时说明为运营目录 | 对端（接口清单 §6.4 已登记，不新造编号） |
| 570 / 573 | 报告/成果/专家详情无字段级接口，仅 `detail_url`/外链走 iframe | 契约既定（§6.4）；`X-Frame-Options`/CSP `frame-ancestors` 放行未书面确认（`SYSINT-05-07-04-L01`） | 对端配置到位后连白名单一并验证；禁嵌时按「在新窗口打开」降级口径讲解 | 对端 / `SYSINT-05-07-04-L01` |
| 569 / 570 | 活动仅德尔菲问卷一类（B2）、问答正文不公开（D3） | 对端口径已裁定，属设计边界非新缺口 | 演示按既定口径讲解，不补造 | —（已裁定，不建单） |

## 备注与风险

1. **接口已联调（R1 实测）**：对端 `EXT-B4-ZHIKU` 已配置，9 端点业务码全 0 且有数（2026-11-12 22:40 实测，明细见本文 R1 段）。仍待人工确认两件：①对端给的是**测试库**（`ZK-GAP-02`）；②门户 iframe 放行未书面确认（`ZK-GAP-03`）。复测需重新登录公网页面刷新 `display-loop-token`（11-13 该 token 已过期，返回 401 `sso check-token failed`）。
2. **两套鉴权不能混**：段 A 四个 GET 用 `Authorization: Bearer`；段 B 五个 POST 用 `X-Portal-Access-Token`，且业务错误仍返回 HTTP 200 + body `code`，BFF 必须二次判码，不能只看 HTTP 状态。
3. **详情无字段级接口**：报告 / 成果只有 `detail_url`，专家只有外链，重大事件只有 `sourceUrl`，全部走 iframe。需对端放行 `X-Frame-Options` / CSP `frame-ancestors`（`SYSINT-05-07-04-L01` 尚未书面确认）；被禁嵌时只能靠「在新窗口打开」降级，不满足「弹框内正常展示」。
4. **口径约束**：ZK-04 多领域重复计数，禁止与列表 total 简单相等；服务类型计数为前端派生（D5），不作指标、不挂就绪度；H 指数不展示（D2 `provisional`）；成果敏感字段 `actual_investment` / `roi_percent` / `satisfaction` 在裁定前不展示。
5. **能力缺口**：服务类型主档对端未提供（仅前端临时目录）；活动类型只有德尔菲问卷；问卷问答正文不公开（只给 7 项汇总）。
6. **供数与边界**：智库不做后台，本仓不建表、不入库（技术方案 §3.2）；对端已供数，页面按真实数据渲染。主题筛选路径当前不可演（`ZK-GAP-01` 过滤恒 0），演示应避开或先说明；数据为对端测试库时须当场说明来源。
7. **兜底数据**：ZK-03 失败时前端有内置的 12 项行业 / 5 类服务类型兜底；演示时若出现兜底值，必须如实说明是前端兜底而非对端实时下发。
