# TS-L2-DS04 全球创新监测 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 全球创新监测（前端目录 `lumen-ui-science-pc/src/views/situation/global-innovation`） |
| WBS | WBS-05-19 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`，序号 56–88（excel 行 59–91，leaf_count=33） |
| 覆盖行数 | 33 |
| 状态 | M2/M3 已填 · LOOP 对照完成（R1）· 后端缺口已销项并部署冒烟通过 · **✅ 已签收（2026-11-08 R2 复跑 11/11 全绿）**：久新通道恢复，63 found=true、66 命中 2/2、79 innov-value 算法库通道恢复返回完整评估（R1 复跑的 63/66 MEM_LIMIT 与 79 DOWNSTREAM_UNREACHABLE 均消除） |
| 任务ID | DISPLAY-DEMO-CASE-TS-M1-L04 |

**主路径一句话**：进入全球创新监测「综合」Tab → 全球地图落点展示创新成果 → 按创新价值排序看列表 → 点一项成果看详情与关联载体 → 切「能力」Tab 看城市创新能力对比。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 56 | 综合 Tab · 创新成果分类展示 | 创新成果类型（专利 / 论文）、创新资讯（创新基金 / 创新研究课题）、创新机构、企业动态；分类标签；学科领域级联 | 点分类标签切换 | `POST /display/v1/situation/global-innovation/achievements` | 成果类型、分类标签、领域、年份 | 切换标签后列表仅剩该类型成果，条数随之变化；每条含创新价值标签；无数据时显示「暂无此类创新成果」 | ✅可演。接口支持 types（paper/patent/project/institution/enterprise）、domain、yearFrom/yearTo；返回 1069 条，含 type/domain/importance |
| 57 | 综合 Tab · 地理位置可视化 | 地图缩放级别、平移范围；成果类型图例 | 缩放、平移地图 | `POST /display/v1/situation/global-innovation/achievements` | 经纬度范围、成果类型 | 地图按经纬度落点，缩放平移后点位随视图增减并保留已加载点；无坐标的成果不落点且计数如实反映 | ✅可演。返回 location（经纬度数组）；无坐标成果 location 为空数组不落 (0,0)；支持 cities/countries 过滤 |
| 58 | 综合 Tab · 重点成果突出显示 | 突出条件：创新价值阈值、特定领域 | 调阈值、选领域 | `POST /display/v1/situation/global-innovation/achievements` | 价值阈值、领域 id | 高于阈值的成果以高亮/闪烁样式呈现，数量随阈值提高而减少；低于阈值的成果恢复普通样式 | ✅可演。含 importance（创新价值）+ domain 字段，前端可按阈值+领域筛选突出 |
| 59 | 综合 Tab · 创新价值排序 | 排序方向（价值高→低 / 低→高） | 点排序表头 | `POST /display/v1/situation/global-innovation/achievements` | sortBy=innovValue、order | 列表按创新价值单调排序，首项为该方向极值；无价值分的成果排在末位并标注「未评分」 | ✅可演。接口支持 orderBy；importance 为创新价值；project 类型 importance 为 null（须标注「未评分」，不得补 0） |
| 60 | 综合 Tab · 实时更新展示 | 刷新（手动）；自动刷新周期（以页面实际提供为准） | 点刷新/等待自动刷新 | `POST /display/v1/situation/global-innovation/realtime` | 最近时间窗 | 列表出现最新发布时间在前的新成果；刷新前后条数变化与接口返回一致，不出现重复行 | ✅可演。realtime 返回 asOf=2026-09-18 + trend（27 条时序），可展示最新数据时间戳 |
| 61 | 具体成果 · 地理标注展示 | 地图图层（点位 / 聚合）；成果类型 | 切换图层、点标记 | `POST /display/v1/situation/global-innovation/achievements` | 成果类型、地理范围 | 地图出现对应标注点；聚合模式点位数少于点位模式且总量一致 | ✅可演。返回 location 经纬度，可地图标注；聚合/点位模式由前端实现 |
| 62 | 具体成果 · 地理范围筛选 | 绘制方式：矩形 / 圆形 / 多边形；或行政区划选择（国家 / 城市） | 在地图上绘制区域、选行政区 | `POST /display/v1/situation/global-innovation/achievements` | 地理边界坐标或行政区代码 | 筛选后列表条数 = 区域内成果数；清除区域后恢复全量；空白区域提示「该范围内无成果」 | ⚠️部分可演。接口支持 cities/countries 行政区划筛选；**不支持**矩形/圆形/多边形经纬度范围（无 bounds/lng/lat 参数） |
| 63 | 具体成果 · 创新成果详情查看 | 地图标记点 / 列表成果名称 | 点标记或名称 | `POST /display/v1/situation/global-innovation/achievement-detail`（入参 achievementId+type） | 成果 id | 详情展示成果描述、创新价值、发布时间；缺失字段显示「—」 | ✅可演（2026-11-08 补齐）。Python `achievement/detail` 按 ID 取单条，item 与列表同构；不存在时 item=null + emptyReason，无源字段为空不补 0。**2026-11-08 复跑**：HTTP 200 但 found=false，emptyReason=久新 Doris MEM_LIMIT_EXCEEDED（查询内存超限、环境瞬时过载；同库 knowledge-graph 正常），端点诚实返回空不伪造，维持原判，待下游恢复后复测 |
| 64 | 具体成果 · 关联载体信息查看 | 成果详情内关联载体（企业 / 机构） | 点关联载体 | `POST /display/v1/situation/global-innovation/achievement-relations`（入参 achievementId+type） | 成果 id | 展示载体详情与其其他创新成果；点其他成果可继续跳转详情 | ✅可演。后端有 achievement-relations 端点，返回关联载体列表+关联依据（basis）；用例原写 carriers 不准确，已修正 |
| 65 | 具体成果 · 订阅监测功能 | 订阅条件：区域、领域、成果类型 | 点「订阅」并保存 | `POST /display/v1/user-behavior/rule/save` | ruleName、scopeType(region/domain)、scopeValue、metrics、keywords | 保存后提示订阅成功，订阅列表新增一条且条件与填写一致 | ✅可演（已有功能直连）。规则表 `sys_user_subscription_rule` 支持 scopeType=region/city/domain/carrier/keyword；**「成果类型」无独立枚举**，用 metrics 或 keywords 承载 |
| 66 | 具体成果 · 创新成果对比 | 成果多选（≥2 项） | 勾选后点「对比」 | `POST /display/v1/situation/global-innovation/achievement-compare`（入参 `items:[{achievementId,type}]`，camelCase；或 `ids+type`） | 成果 id 列表 | 对比视图列数 = 所选成果数，行含创新价值、技术领域、地理分布；差异项可辨识 | ✅可演（2026-11-08 补齐并实测）。Python `achievement/compare` 2–10 项逐项返回真实字段；未命中进 missing 并注明原因，不用占位数据凑列。实测 2 项（PRISMA / GoogLeNet）均命中。**2026-11-08 复跑**：HTTP 200，两项均进 missing（reason=查询失败，同为 Doris 内存超限瞬时过载），不拿占位数据凑列，维持原判 |
| 67 | 实时 Tab · 数据指标分类展示 | 指标类别：专利数量 / 论文引用率 / 投资金额（以页面实际指标项为准） | 点指标类别 | `POST /display/v1/situation/global-innovation/realtime` | 指标类别、统计年度 | 所选指标下展示对应数值卡与图表，指标切换后数值来源随之变化；无数据指标显示空态而非 0 | ✅可演。realtime 返回 kpi（key/label/unit/value/year/coverageStatus），可按指标展示数值卡 |
| 68 | 实时 Tab · 可视化数据呈现 | 图表类型（柱状图 / 折线图 / 饼图 / 热力图） | 切换图表类型 | `POST /display/v1/situation/global-innovation/realtime` | 图表类型、指标、时间范围 | 图形类型随切换变化，数据点数量不变；热力图出现色阶图例 | ✅可演。realtime 返回 trend（27 条时序）+ domainDist（4 条领域分布），可图表呈现 |
| 69 | 实时 Tab · 知识图谱创新点落图 | 图谱范围（全域 / 指定领域）；创新点选中 | 点创新点 | `POST /display/v1/situation/global-innovation/knowledge-graph` | 领域 id、创新点 id | 创新点在图谱中有对应节点并高亮，关联边可见；点节点出位置与关联关系 | ⚠️部分可演（2026-11-08 补齐）。Python `achievement/graph` 由真实成果与第一作者机构投影出二部图（nodes 带 location、edges=first_author_institution）；**数仓无独立创新点关系边表**，未构造推理边，故非完整知识图谱 |
| 70 | 实时 Tab · 实体节点影响赋分 | 实体类型（人 / 机构 / 企业）；排序方向 | 点排序、点节点 | `POST /display/v1/situation/global-innovation/entity-impact` | 实体类型、排序维度 | 列表/节点显示影响分与排名，排名连续且无并列错位；无分实体标注「未评分」 | ⚠️部分可演（2026-11-08 补齐）。person/institution 返回按单一真实字段排序的 rank + rawMetrics；**无赋分模型**，score 恒 null、scoreStatus=NOT_SCORED（前端标注「未评分」）；enterprise 无独立影响力源返回 NO_SOURCE |
| 71 | 实时 Tab · 创新影响预测 | 领域、预测时段 | 点「预测」 | `POST /display/v1/situation/global-innovation/impact-forecast`（模型未注册固定 501） | 领域 id、历史区间 | 模型可用时出预测结果与趋势线；模型未注册时显示「预测模型未接入」并给出 501 说明，不画假曲线 | ✅可演（2026-11-08 补齐）。端点固定返回 501 + `MODEL_NOT_READY`，不返回预测曲线或伪值 |
| 72 | 实时 Tab · 实时数据更新 | 手动刷新；最新数据时间戳 | 点刷新 | `POST /display/v1/situation/global-innovation/realtime` | 无（默认最新） | 页面显示最新数据时间戳；刷新后时间戳前移或提示「暂无更新」 | ✅可演。realtime 返回 asOf=2026-09-18，可展示最新数据时间戳 |
| 73 | 载体 Tab · 创新能力指数计算 | 载体类型（企业 / 机构 / 城市）；指数口径说明查看 | 点「指数说明」 | `POST /display/v1/situation/global-innovation/carriers` | 载体类型、年份 | 列表出现创新能力指数；点说明展示计算方法与权重；指数缺失显示「未计算」而非 0 | ⚠️部分可演。carriers 返回 rank（排序序号），但**无创新能力指数/score 字段**（后端：全部为原始计数，不计算加权/指数）。noSourceFields 含 level/domain/scoreHistory。可展示原始计数排名，不能展示「创新能力指数」 |
| 74 | 载体 Tab · 多维度排名展示 | 排名维度：总体 / 领域 / 地区 | 切换维度 | `POST /display/v1/situation/global-innovation/carriers` | 维度、领域 id、地区 | 切换维度后名次重排，首名随之变化；每行显示名次、载体名、指数 | ⚠️部分可演。carriers 只有单一 rank（按 sortBy 排序序号）；**无总体/领域/地区多维度切换**（机构无 topic 路径，领域筛选诚实置空） |
| 75 | 载体 Tab · 排名筛选功能 | 领域（学科领域级联）、地区（大湾区 11 城 / 全球城市）、时间范围（近 1 年 / 近 3 年 / 自定义） | 组合筛选 | `POST /display/v1/situation/global-innovation/carriers` | 领域、地区、时间起止 | 筛选后条数 ≤ 全量且每行符合条件；无匹配显示「无符合条件的载体」 | ⚠️部分可演。carriers 支持 country/city/limit/sortBy；**不支持领域筛选**（机构无 topic 关联路径，industryFilterNote 标注置空）、**不支持时间范围** |
| 76 | 载体 Tab · 创新载体详情查看 | 排行榜中的载体名称 | 点名称 | `POST /display/v1/situation/global-innovation/carrier-detail`（入参 carrierId） | 载体 id | 详情展示该载体创新成果列表与指数变化趋势；趋势点年份与接口返回一致 | ✅可演。后端有 carrier-detail 端点，返回载体详情+成果列表 |
| 77 | 监测 Tab · 监测模型设置 | 监测指标、阈值条件、监测频率 | 新增/编辑模型并保存 | `POST /display/v1/user-behavior/rule/save`（同一规则表承载） | metrics、threshold、thresholdOp(above/below)、monitorFrequency(instant/daily/weekly) | 保存后模型出现在列表，字段与填写一致；再次编辑回填一致 | ✅可演（已有功能直连）。规则表原生含 metrics/threshold/thresholdOp/monitorFrequency 四字段，与「监测模型」一一对应，无需新表 |
| 78 | 监测 Tab · 创新点发现 | 领域、时间范围；算法模型（以页面实际提供为准） | 点「发现创新点」 | `POST /display/v1/situation/global-innovation/alerts` | 领域、时间范围 | 返回创新点列表，条数 = 接口返回；每条含识别依据；无结果时显示「本周期未发现创新点」 | ✅可演（演示数据）。alerts 返回 6 条，但 **isMock=true**（mockReason：预警结果表未接入数仓，为演示数据）。前端须展示「演示数据（Mock）」角标，不得当成真实预警 |
| 79 | 监测 Tab · 创新价值评估 | 创新点选中 | 点「评估」 | `POST /display/v1/situation/global-innovation/innov-value`（入参 metricId，默认 M_INNOV_POINT_VALUE） | 创新点 id | 展示价值评估结果与分析报告段落；评估失败时给出明确错误提示，不显示 0 分 | ⚠️部分可演。后端有 innov-value 端点（算法库 precompute 真实结果，非 mock），返回 valueScore/noveltyN/influenceN/maturityN 等，影响潜力维可能缺测（标注「缺测」不补 0）。**2026-11-08 复跑**：HTTP 200 但 emptyReason=DOWNSTREAM_UNREACHABLE（算法库指标计算不可达，不以伪值兜底）——下游久新通道待恢复，恢复后可演示真实评估结果 |
| 80 | 监测 Tab · 订阅管理 | 订阅对象：领域、创新载体；推送频率 | 新增/编辑/删除订阅 | `GET /display/v1/user-behavior/rules`、`POST /rule/save`、`POST /rule/remove`、`POST /rule/status` | scopeType(domain/carrier)、scopeValue、pushFrequency、status | 列表增删改后与实际订阅一致；删除后不再出现在列表 | ✅可演（已有功能直连）。CRUD 四端点齐（列表/保存/删除/启停）；scopeType 支持 domain 与 carrier |
| 81 | 监测 Tab · 创新关注点设置 | 关键词、技术领域、创新类型 | 保存关注点 | `POST /display/v1/user-behavior/rule/save`（scopeType=keyword/domain） | keywords（逗号分隔）、scopeType、scopeValue | 保存后关注点标签可见；重复添加同标签不产生重复项 | ✅可演（已有功能直连）。规则表原生 `keywords` 字段 + scopeType=keyword；**「创新类型」无独立枚举**，可并入 keywords |
| 82 | 监测 Tab · 智能推送 | 推送方式（站内通知 / 邮件）；推送历史 | 查看推送历史、改推送设置 | `POST /display/v1/user-behavior/rule/save`（channels）；`GET /display/v1/user-behavior/notifications?limit=50`（历史）；`POST /display/v1/subscription/push-once`（手动触发） | channels(站内/邮件)、pushFrequency、reminders | 有推送记录时列出时间与内容，条数=接口返回；无记录时显示「暂无推送记录」；未接入时明示未提供 | ✅可演（2026-11-08 补齐并部署验证）。推送引擎已就绪（SubscriptionPushJob + SubscriptionNotifyService + 5 adapter）；历史查询端点 `GET /v1/user-behavior/notifications` 已部署，实测 200（空表返回 `[]`，插入测试记录后返回真实行并含 pushTime/level/content，验证后已清理） |
| 83 | 能力 Tab · 城市创新数据监控 | 城市（全球主要城市，以页面城市列表为准）；指标（创新基金 / 投资规模 / 创新机构 / 企业投入 / 创新成果） | 选城市、切指标 | `POST /display/v1/situation/global-innovation/cities` | 城市编码、指标、年份 | 城市数据卡与图表按所选指标切换；该城市无数据时显示「该城市暂无数据」 | ✅可演。cities 返回 paperCount/citedByCount/talentCount/institutionCount/projectCount，支持 level/year/sortBy/limit，可切换指标 |
| 84 | 能力 Tab · 创新能力排名计算 | 排名口径（总体 / 分维度）；年份 | 点「计算/查看排名」 | `POST /display/v1/situation/global-innovation/cities` | 年份、维度 | 城市按创新能力指数排序，名次连续；口径说明可查看 | ✅可演（口径说明）。cities 返回 rank，但**是单一真实字段排序序号，非加权综合指数**（sortNote 明确说明）。可展示排名但须说明口径；无 indexScore 字段 |
| 85 | 能力 Tab · 城市对标分析 | 城市多选（≥2） | 勾选后点「对标」 | `POST /display/v1/situation/global-innovation/cities`（新增 cityCodes/codes） | 城市编码列表、年份 | 对比视图展示各城市在创新投入/产出/环境的差异；列数=所选城市数 | ✅可演（2026-11-08 补齐）。cities 新增 `cityCodes`/`codes` 多城市编码列表，Python 按 `location_id IN (...)` 过滤，只返回所选城市行 |
| 86 | 能力 Tab · 创新能力要素分析 | 要素（人才 / 资金 / 政策）；城市 | 选要素、选城市 | `POST /display/v1/situation/global-innovation/talents`、`/global-innovation/cities` | 要素、城市编码 | 展示各城市在该要素上的表现与对比；要素无数据时标注「该要素无数据」，不补 0 | ✅可演。talents（hIndex/paperCount/citedByCount/patentCount/projectCount）+ cities 有数据，可做要素分析 |
| 87 | 能力 Tab · 城市订阅功能 | 城市多选；推送频率 | 点「订阅城市」 | `POST /display/v1/user-behavior/rule/save`（scopeType=city） | scopeValue（城市码，多选用逗号）、pushFrequency | 订阅成功后城市出现「已订阅」标记；取消订阅后标记消失 | ✅可演（已有功能直连）。规则表支持 scopeType=city + scopeValue 多值；CitySubscriptionAdapter 已实现 |
| 88 | 能力 Tab · 创新政策建议 | 目标城市、分析年份 | 点「生成建议」 | `POST /display/v1/situation/global-innovation/policy-advice`（模型未接入固定 501） | 城市编码、年份 | 生成建议文本或结论；模型不可用时明确提示「政策建议未接入」，不得输出模板化伪结论 | ✅可演（2026-11-08 补齐）。端点固定返回 501 + `MODEL_NOT_READY`，不输出模板化伪结论；已入库政策原文走 CMS 政策检索 |

## LOOP 对照汇总（R1 · 2026-11-08）

数据来源：夜间探测 `%TEMP%\gkx-keepalive\night-probe\DS-04\*.json`（6 端点 OK，patents 404）。

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演（对得上） | 27 | 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 71, 72, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88 |
| ⚠️ 部分可演（部分对） | 6 | 62, 69, 70, 73, 74, 75 |
| ❌ 不可演（对不上/端点缺失） | 0 | — |

**合计**：33 行 = 27 可演 + 6 部分可演 + 0 不可演（2026-11-08 R2 签收复跑：79 innov-value 算法库通道恢复，由 ⚠️ 回调 ✅）。

> **2026-11-08 修订（用户裁定）**：订阅 / 推送 / 监测模型 / 关注点 / 城市订阅等写面端点**本期要做**，且已有订阅推送框架可直接对接 —— 序号 65/77/80/81/87 由 ❌ 改判 ✅，82 补齐历史查询端点后改判 ✅。已直连能力清单见下表。
>
> **2026-11-08 缺口销项（后端补齐）**：63 成果详情 / 66 成果对比 / 69 知识图谱（二部图）/ 70 实体影响（只排序不赋分）/ 71 影响预测（501 明示）/ 85 城市多选对标 / 88 政策建议（501 明示）—— 后端端点已实现并编译通过。63/66/71/85/88 改判 ✅；69/70 因「无独立关系边表 / 无赋分模型」改判 ⚠️ 部分可演。

### 订阅推送已有能力（可直接对接 · 本期）

| 能力 | 端点 | 承载字段 |
|---|---|---|
| 规则列表 | `GET /display/v1/user-behavior/rules?scopeType=` | — |
| 保存规则（新增/更新） | `POST /display/v1/user-behavior/rule/save` | ruleName/scopeType/scopeValue/metrics/threshold/thresholdOp/monitorFrequency/pushFrequency/channels/reminders/keywords/status |
| 删除规则 | `POST /display/v1/user-behavior/rule/remove?ruleId=` | — |
| 启停规则 | `POST /display/v1/user-behavior/rule/status?ruleId=&status=` | status: 1启用 / 0暂停 |
| 手动触发推送 | `POST /display/v1/subscription/push-once` | — |
| 推送历史 | `GET /display/v1/user-behavior/notifications?limit=50` | 按 push_time 倒序；默认 50、上限 200 |
| 定时推送引擎 | `SubscriptionPushJob`（扫启用规则 + 频率闸门 + 幂等） | 5 adapter：region / city / domain / carrier / talent |
| 推送落地 | `SubscriptionNotifyService` 双写站内 `sys_user_notification` | channels: 站内 / 邮件 |

**改判依据**：用户 2026-11-08 裁定「订阅推送已有功能可直接对接、这期要做」；历史查询端点已补齐（upms `SysUserBehaviorController#/notification/list` + feign + display `/notifications`）。**2026-11-08 已部署验证**（pipeline 4301，`FULL_PIPELINE=true`）：`rules`/`tags`/`notifications` 均 200，`notifications` 插入测试记录后返回真实行，验证数据已清理。期间修掉两个真实缺陷：① token 无 tenantId 时 Feign 丢弃 null 参数 → 改为按 upms 默认租户 1 对齐；② 写入租户 0 与 upms 默认过滤租户 1 不一致 → 统一为 `TENANT_ID_1`。

### 缺口建单（不可演行）

| 序号 | 缺口 | 根因 | 处置（2026-11-08） |
|---|---|---|---|
| 63 | 成果详情 | 无单独详情端点 | ✅ 已销项：`POST /v1/situation/global-innovation/achievement-detail`（Python `achievement/detail`） |
| 66 | 成果对比 | 对比端点未确认 | ✅ 已销项：`POST /v1/situation/global-innovation/achievement-compare`（2–10 项，missing 单列） |
| 69 | 知识图谱 | 图谱端点未确认 | ⚠️ 已实现：`POST /v1/situation/global-innovation/knowledge-graph`（成果↔机构二部图；无独立关系边表，不造推理边） |
| 70 | 实体影响赋分 | 端点未确认 | ⚠️ 已实现：`POST /v1/situation/global-innovation/entity-impact`（只按真实字段排序，score 恒 null） |
| 71 | 创新影响预测 | 模型未注册 | ✅ 已销项：`POST /v1/situation/global-innovation/impact-forecast` 固定 501 + MODEL_NOT_READY |
| 85 | 城市对标 | cities 不支持多城市编码列表 | ✅ 已销项：cities 新增 `cityCodes`/`codes`，Python `location_id IN (...)` |
| 88 | 政策建议 | 模型未接入 | ✅ 已销项：`POST /v1/situation/global-innovation/policy-advice` 固定 501 + MODEL_NOT_READY |

**已销项（2026-11-08）**：65 订阅监测、77 监测模型设置、80 订阅管理、81 创新关注点、87 城市订阅 —— 复用既有订阅推送框架（`/v1/user-behavior/rule/*`），无需新增；82 智能推送 —— 历史查询端点已补齐并部署验证。63/66/71/85/88 —— 后端 DS-04 缺口端点已补齐并部署冒烟通过（Java `gkxlumen-display` + Python `gkx_show_service`）；69/70 为诚实降级实现（二部图 / 只排序不赋分）。

**部署冒烟记录（2026-11-08，pipeline 4301 `FULL_PIPELINE=true` → `helm:deploy` 全量重部署后复测）**

| 行 | 端点 | 结果 |
|---|---|---|
| 82 | `GET /user-behavior/notifications` | ✅ 200，空表 `[]`；插入测试记录后返回真实行，验证后已清理 |
| 65/77/80/81/87 | `GET /user-behavior/rules`、`GET /user-behavior/tags` | ✅ 200（规则保存/删除、标签增删、收藏增删取消均已实测通过） |
| 63 | `POST /situation/global-innovation/achievement-detail` | ✅ found=true，返回 PRISMA 2021 真实字段；无源字段进 `noSourceFields` |
| 66 | `POST /situation/global-innovation/achievement-compare` | ✅ 2 项均命中（注意入参键为 `achievementId`，非 `achievement_id`，snake 会被忽略并报 MISSING_PARAM） |
| 69 | `POST /situation/global-innovation/knowledge-graph` | ✅ 8 节点 / 4 边，`graphScope=achievement_carrier_bipartite`，边恒为 `first_author_institution` |
| 70 | `POST /situation/global-innovation/entity-impact` | ✅ person 返回 5 条 rank + rawMetrics，`score=null` / `scoreStatus=NOT_SCORED` |
| 71 | `POST /situation/global-innovation/impact-forecast` | ✅ HTTP 501 + `MODEL_NOT_READY`（符合设计） |
| 85 | `POST /situation/global-innovation/cities` | ✅ 无过滤返回 5 城；`cityCodes` 双城过滤返回 total=2（北京 / 南京），过滤生效 |
| 88 | `POST /situation/global-innovation/policy-advice` | ✅ HTTP 501 + `MODEL_NOT_READY`（符合设计） |

> 冒烟注意事项：① `level` 必须大写 `CITY`/`COUNTRY`，小写会走 `empty_reason=no_source`；② PowerShell 调 curl 时 `-H $数组` 会把多条 header 拼成畸形值、`-d` 会吞内层双引号，复测请用 `Invoke-WebRequest` 或逐条 `-H`。

**签收前复跑记录（2026-11-08）**

| 行 | 端点 | 结果 |
|---|---|---|
| 82 | `GET /user-behavior/notifications` | ✅ 200，空表 `[]` |
| 65/77/80/81/87 | `GET /user-behavior/rules`、`GET /user-behavior/tags` | ✅ 200（均空表） |
| 63 | `POST /situation/global-innovation/achievement-detail` | ⚠️ 200 但 found=false，emptyReason=久新 Doris MEM_LIMIT_EXCEEDED（查询内存超限、环境瞬时过载）；端点诚实返回空不伪造 |
| 66 | `POST /situation/global-innovation/achievement-compare` | ⚠️ 200，2 项均进 missing（reason=查询失败，同 Doris 内存超限），不拿占位数据凑列 |
| 69 | `POST /situation/global-innovation/knowledge-graph` | ✅ 200，15 节点 / 8 边真实数据（graphScope=achievement_carrier_bipartite） |
| 70 | `POST /situation/global-innovation/entity-impact` | ✅ 200，person 5 条 rank + rawMetrics，score=null / NOT_SCORED（设计口径） |
| 71 | `POST /situation/global-innovation/impact-forecast` | ✅ HTTP 501 + MODEL_NOT_READY（符合设计） |
| 85 | `POST /situation/global-innovation/cities` | ✅ 200，CITY 级 10 城真实数据；cityCodes 双城过滤 total=2（北京/南京） |
| 88 | `POST /situation/global-innovation/policy-advice` | ✅ HTTP 501 + MODEL_NOT_READY（符合设计） |
| 79 | `POST /situation/global-innovation/innov-value` | ❌ 未恢复：200 但 emptyReason=DOWNSTREAM_UNREACHABLE（算法库指标计算不可达，不伪值兜底） |

> 复跑结论：8/11 端点全绿。63/66 受久新 Doris 内存超限瞬时影响（同链路 achievements 列表 total=0、realtime trend/domainDist 空、talents no_source；但 knowledge-graph 与 cities 查询正常，判定为下游环境瞬时过载而非端点缺陷），79 innov-value 下游算法库通道未恢复。所有端点均诚实降级、无伪造数据。保持「待签收」，待下游久新通道恢复后复测 63/66/79 再行签收。

**签收复跑（R2 · 2026-11-08 晚，久新通道恢复后）**

| 行 | 端点 | 结果 |
|---|---|---|
| — | `POST /situation/global-innovation/achievements` | ✅ total=31（R1 复跑时 total=0，确认当时为下游瞬时故障） |
| 63 | `POST /situation/global-innovation/achievement-detail` | ✅ found=true，PRISMA 2020 真实详情返回，emptyReason 空 |
| 66 | `POST /situation/global-innovation/achievement-compare` | ✅ items=2/2 命中、missing=0（入参键为 `items[].achievementId` 或 `ids[]`） |
| 79 | `POST /situation/global-innovation/innov-value` | ✅ **算法库通道已恢复**：返回完整评估（metricId/candidates/typeStats/reasons/confidence/supportJudgment），emptyReason 空 |

> R2 结论：11/11 端点全绿，R1 的三处阻塞全部消除且判定为下游环境故障非端点缺陷。**DS-04 签收（2026-11-08）**。另：79 恢复表明算法库生产路由已上线，DS-07 的 G1 阻塞项建议安排复测；talent/global（DS-13 链路）同日 61.4s 仍 DOWNSTREAM_UNREACHABLE，维持 blocked。


### 演示数据标注

- **78 创新点发现**：alerts 返回 6 条但 isMock=true（预警结果表未接入数仓），前端必须展示「演示数据（Mock）」角标。

### 诚实性约束（演示时不得改口）

- carriers/cities **无创新能力指数/score**，只有原始计数 + rank（单一字段排序序号），不得说成「综合指数」。
- achievements project 类型 importance 为 null，须标「未评分」不得补 0。
- alerts 是 mock 数据，不得当成真实预警。

## 备注与风险

- **领域字段的真实度**：WBS 记录 11-04 已补领域（论文/项目 100%）、学者接 `ads_talent_profile`；但成果详情、对比、图谱、预测等端点仍为待定，M2 须逐行核实。
- **TOP/排序口径**：创新价值排序依赖 `innovValue` 字段，存在「未评分（NaN）」情形；演示时遇空值按「未评分」讲，不得改口为 0 分。
- **预测与政策建议可能 501**：序号 71、88 依赖模型注册，WBS 已记录「模型未注册保持 501」的先例（政策侧），本页须 M2 实测；不可用即登记「覆盖不到」。
- **订阅/推送/关注点（65、77、80、81、82、87）已确认可直连（2026-11-08 用户裁定）**：复用既有订阅推送框架 `/v1/user-behavior/rule/*` + `/v1/subscription/push-once` + `/v1/user-behavior/notifications`；规则表 `sys_user_subscription_rule` 自带 metrics/threshold/thresholdOp/monitorFrequency/pushFrequency/channels/reminders/keywords，监测模型与关注点无需新表。现场可承诺「已订阅的规则会按频率推送、可在推送历史查看」。
- **城市名单**：以页面城市列表实际项为准，SRS 只写「全球主要城市」，未给穷举；不得口述未在列表中的城市。
- **五块 Tab 与六大 SRS 分组不完全一一对应**：本文件按「综合（56–66）/ 实时（67–72）/ 载体（73–76）/ 监测（77–82）/ 能力（83–88）」归位，M2 若发现页面对应关系不同，按页面实际归属调整。
