ponytail: full

# SVC-EXPO-DEMO-ACCEPT-LOOP · 交流/竞赛/传播 EXPO 演示样本循环验收记录

> **验收单**：SVC-EXPO-DEMO-ACCEPT-LOOP（tech_task / qa-agent）　|　**监管人**：human:李伟
> **依据**：`产品实现规程.md` §6.5；计划 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/编排计划/TS-L2-EXPO-LOOP计划.md`；用例真源 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/SVC-L2-EXPO-合规演示用例.md`
> **性质**：只读验收（GET 查询），零代码改动、零 commit/push；token 不落盘、不进本文档。

## 运行 2026-11-07 R1

- **执行**：qa-agent　|　**轮次**：R1（第一轮）
- **探测（第一笔）**：网关 `http://10.50.69.111:30895`，头 `Authorization: Bearer <本机 token>`（读 `%USERPROFILE%\.gkx\display-loop-token`，len=32，内容不记录）+ `systemCode: display`，body `{}`，curl.exe `--max-time 40`。
  - 按计划 §1 先发 **POST** `/display/v1/exchange/overview` → **HTTP 405**（`{"status":405,"error":"Method Not Allowed","path":"/v1/exchange/overview"}`）。405 不属熔断三态（401/424/404），路径存在、映射未缺。
  - 改发 **GET** 同端点 → **HTTP 200**，stats 四卡 252/2282/77/105 与基线一致 → 不熔断，进入 22 行对照。
  - ⚠️ 计划 §1「POST」与端点实现（仅 GET）不符，建议计划文档订正（观察 O1）。
- **判定口径**：22 行可演逐行对照；传播三卡计数 0 与 overview `activityCountByType={}` 为已知空态不判负；覆盖不到 4 行（585/586/588/591）+ 部分可演 1 行（601）按计划不判。

### 22 行逐行对照（计划 §2）

| 行（序号） | 条件 | 端点 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|
| 575 | activityType=exchange/reasoning/live/course，page=1&pageSize=100 | `/exchange/list` | 200 | 四类 total 22/135/32/63，合计 252 与 overview 一致；exchange 列表类型纯度 22/22；卡片字段（title/activityTypeName/startTime/nested venueAddress·subjectAreaName）齐；漏参复测 HTTP 400（已知坑确认） | 对得上 |
| 576 | page=1&pageSize=6&expertLimit=4 | `/exchange/recommendation` | 200 | experts=4（首位 zyg·北京大学·关联活动 58）；resources=6（fileName/viewCount/activityTitle 齐） | 对得上 |
| 577 | 四类可点 ID：604/612/609/3171172762 | `/exchange/detail` | 200 | detailUrl 四路径与用例登记一致：sci-comm/detail/604、science-thinking/ended?activityId=612、technology-live-streaming/details?activityId=609、courses/3171172762?tab=courses | 对得上 |
| 578 | status/timeRange/subjectAreaId/categoryId/liveType/keyword 及组合 | `/exchange/list` | 200 | exchange ended 22 / ongoing 0；thisQuarter 4；categoryId=1→12；subjectAreaId=9→1；live liveType=seminar→13；reasoning keyword=科技→2；组合 ongoing+thisMonth+subj8→0（筛选生效） | 对得上 |
| 579 | 同 576 | `/exchange/recommendation` | 200 | resources 6 条含 viewCount（首条 31）与所属活动 activityTitle | 对得上 |
| 580 | 同 576 | `/exchange/recommendation` | 200 | 专家卡字段 name/organization/school/domain/researchFields/relatedActivityCount 齐（58/17 口径保持） | 对得上 |
| 581 | 无参（overview/dictionaries）；sync 带 activityType=exchange | `/exchange/overview`、`/exchange/dictionaries`、`/exchange/sync` | 200 | stats 252/2282/77/105 ✓；`activityCountByType={}`（已知空态）；deepShiReachable=true、enumerations=embedding-via-bff；字典 activityType 4 / subjectArea 13 / categoryId 6 / liveType 6 / sortType 2；sync total=25、nextUpdatedSince=2026-10-28T14:49:21+08:00 | 对得上 |
| 582 | page/pageSize/expertLimit | `/exchange/recommendation` | 200 | experts[]=4、resources[]=6，分页与 expertLimit 生效，无 mock 痕迹 | 对得上 |
| 583 | 同 575/577 条件串行 | `/exchange/list` + `/exchange/detail` | 200 | 四类计数（22/135/32/63）与 detail 同源一致，list/detail 均 200 | 对得上 |
| 584 | page=1&pageSize=100 | `/competition/list` | 200 | total=37；stats 年度赛事 37 场 / 参赛团队 17 支 / 参赛人数 79 人；publishUrl=…/tics/competitions/create | 对得上 |
| 587 | competitionLevel=1/2/3/5/6；stage 五档；registrationDeadline=thisWeek/thisMonth | `/competition/list` | 200 | level→21/4/3/5/2（合计 39>37，级别多标签已知口径）；stage registering 4 / processing 3 / reviewing 2 / coming 0 / completed 28，与页签分组一致；deadline 1/1 | 对得上 |
| 589 | competitionId=11048（有榜）/ 11055（无榜），page=1&pageSize=10 | `/competition/ranking` | 200 | 11048 total=3，榜首 rank=1「我要发发发」清华大学 97 分、members=2；11055 total=0、items=[]（空态可演） | 对得上 |
| 590 | keyword=科技；theme=人工智能；level/stage/deadline 同 587 | `/competition/list` | 200 | keyword→7；theme→0（诚实空态）；各筛选生效；items 字段（competitionId/name/sponsor/organizer/overview/startTime/endTime/detailUrl 等）齐 | 对得上 |
| 592 | competitionId=11048，page=1&pageSize=10 | `/competition/ranking` | 200 | 字段 rank/teamName/institution/score/submissionCount/submissionTime/awardName/members 齐；未用其它榜单替代 | 对得上 |
| 593 | contentTypes=1/2/3/4/5/6/7（单值） | `/communication/content/list` | 200 | total=47；七类计数 22/10/3/3/2/4/3，之和=47 与 total 一致 | 对得上 |
| 594 | page=1&pageSize=8&sortType=LATEST | `/communication/content/list` | 200 | items 字段 contentId/title/summary/coverImageUrl/contentTypeName/subjectAreaName/institutionName/publishTime/viewCount/detailUrl 等 19 字段齐 | 对得上 |
| 595 | 同 594（stats 随列表） | `/communication/content/list` | 200 | totalContentCount=47；monthlyViewCount=1 / activeUserCount=0 / newContentCount=0（三卡已知空态口径照实；月浏览由基线 0 变 1 系对端数据自然变化，见观察 O2） | 对得上 |
| 596 | 同 594 | `/communication/content/list` | 200 | publishTime 跨度 2026-06-08 ~ 2026-10-23，时间轴分组数据源充足，两视图同源 | 对得上 |
| 597 | keyword=科技；sortType=LATEST / HOTTEST | `/communication/content/list` | 200 | keyword→total 7；LATEST 首条 publishTime=2026-10-23、HOTTEST 首条 viewCount=140，排序切换生效 | 对得上 |
| 598 | contentId=17（取自 list.detailUrl） | `/communication/content/list` | 200 | detailUrl=https://szc.test.dp.tech/tics/sci-comm/hot-spot/detail/17 存在（页面 iframe 口径维持） | 对得上 |
| 599 | subjectAreaIds=2 / institutionTypeIds=1 / subjectCategoryId=1 / publishStartTime=2026-10-01&publishEndTime=2026-11-07 / publishTimeOrder=ASC | `/communication/content/list` | 200 | 分别 →13/16/13/5/47（ASC 首条 2026-06-08 升序生效）；contentTypes 多值组合与 DESC 不演（用例已登记对端空壳行为） | 对得上 |
| 600 | contentId=17 | `/communication/content/detail` | 200 | 28 字段含 content 正文/authorName/datasetUrl/codeRepoUrl/references/averageScore/ratingCount | 对得上 |

- **对得上 22/22**；**对不上 0/22**。
- **结论**：**样本满足**。本轮无新增缺口，不做 DATA/QUERY/ALGO 分类、不建子任务；验收单等监管人 human:李伟「签收」后再校验一次通过即 done。

### 观察项（不判对不上）

- O1【计划文档订正建议】：计划 §1 探测写法为 POST，实测端点仅支持 GET（POST 405）；GET 200 完成探测且当日 CASE-FILL 亦记 GET。建议把计划与验收单派单口径订正为 GET，避免下轮误判。
- O2【数据自然变化】：传播 stats `monthlyViewCount` 由基线 0 变为 1（activeUserCount/newContentCount 仍 0），属对端真实浏览计数变化，非缺口；三卡空态口径维持照实讲。

### 覆盖不到 5 行（585/586/588/591 + 部分可演 601）

585/586/591 接口有数页面未渲染、588 发布组织口径冲突——均属待开发完成，本轮不判、不建补数单；601 PC 端 list/detail 同 contentId=17 均 200（可演部分通过），移动端不在本仓验收维持待定。上述行若连续两轮仍在，交监管人裁定（§6.5.7 步 9）。

- **工程纪律**：全程只读 GET 查询（34 笔），响应暂存 `$env:TEMP\svc-expo-r1\` 未入库；token 不落盘、不进本文档；零代码改动、零 commit/push。
