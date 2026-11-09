# TA-L2-DS13 全球领域人才态势 · 合规演示用例

| 项 | 值 |
|---|---|
| 页面 | DS-13 全球领域人才态势（科技人才态势 · 全球领域人才态势） |
| WBS | WBS-05-03a（前端菜单壳）/ WBS-05-03b（后端）；四子页不重做，供数归 WBS-02-01 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` · seq 243–265（excel 行 246–268） |
| 覆盖行数 | 23（seq 243–265 每条一行） |
| 状态 | **R2 完成（2026-11-09 发布后生产实测）**：三端点 200 / `code=0` / 无 `emptyReason`（global 2.5s、profile 1.3s、recommend 1.9s），23 行判 **18 可演 / 5 部分可演 / 0 待开发完成**，**可申请监管人签收**。R1.5 七项服务侧修复与 R1.6 专利口径修复均已在生产生效并逐项复验（representatives 20/20 家 60 人、coreAchievements 20/20、学历三档 20/20、机构专利 20 个不同真值、fieldHotness/hotspotAlignment 15/15、internationalCoop 15/15 共 90 行）→ 250 / 259 / 265 转 ✅；残余 5 条部分可演全为久新供数缺口（G-DS13-01/02/03/05：工程人才维恒 0、动态单 `media` 型、时间窗密度不足、`projects` 分项无源）。**R2.1（2026-11-09 本地实施·待发版）**：G-DS13-02 动态单型已由服务侧改五类并列出数（`paper/job/project/award/event`，本地实测 231 条 = 75/36/45/45/30），待发版后复跑 R2 即 253 转 ✅（预期 19 可演 / 4 部分可演）；时间粒度仍只到年，256 维持部分可演。 |
| 任务ID | DISPLAY-DEMO-CASE-TA-M1-L01 |

**主路径一句话**：进入「人才分布图」→ 领域选「人工智能」、年份 2025 → 散点 / 热力 / 迁徙三图层切换，点击有数据的城市开区域详情 → 导出 XLSX；再切「人才的最新动态」，类型选「学术发布」并播放 1–6 月气泡，点气泡看动态详情。

> 口径说明：本页四页均为「整页一次性 dataset」契约，`GET /display/v1/talent/global/dataset` **无查询参数**，界面上的地区 / 领域 / 类型 / 年份筛选在前端内存生效（`TA-接口字段映射与对接契约-20261106.md` v1.4）。因此「请求」列统一写端点 + 界面值，不编造后端筛选参数。数据情况经 M3 网关实测判定，见文末「LOOP 对照汇总」。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 243 | 全球领域人才态势 · Tab「人才分布图」· 地图 + KPI 3 卡 | 地区（全球 / 大洲 / 国家 / 城市）；产业级联（一级产业 → 二级产业）；行业；人才类型（领军人才 / 青年人才 / 海外人才 / 工程人才）；时间范围（页面年度条 2020–2026）；图层（散点 / 热力 / 迁徙 / 气泡） | 打开 Tab「人才分布图」默认加载，或修改任一筛选 / 切换图层 | `GET /display/v1/talent/global/dataset` | 无查询参数；界面值（例：地区=全球、领域=人工智能、年份=2025）由前端内存过滤 | 散点地图渲染有位置解析的城市点位，KPI 3 卡出值（人才总数 / 博士占比 / 领域覆盖）；点击城市弹出区域详情抽屉（统计 4 卡 / 学历分布 / 人才类型分布）；无位置数据的城市不出现点位、不补 0 | ⚠️ 部分可演（R1 2026-11-09：散点 24/24 城市有坐标，KPI 3 卡真值——人才总数合计 19,102 / phdRatio / fieldStats 领域覆盖；区域抽屉学历与类型分布为富画像子集口径，博士合计 401、类型 leading 10 / young 1,266 / overseas 1,978；工程人才恒 0 须走空态不补 0） |
| 244 | Tab「人才分布图」· 筛选栏 + 图层按钮 + 年份条 | 图层四选一（散点 / 热力 / 迁徙 / 气泡）；地区、产业级联、行业、人才类型、时间范围五项筛选；地图缩放层级（全球 → 国家 → 省州 → 城市） | 点击图层按钮 / 修改筛选 / 滚轮缩放 | `GET /display/v1/talent/global/dataset` | 无查询参数；界面值由前端内存过滤 | 图层互斥切换且图例随图层变化；筛选后点位、热力强度、KPI 同步重算；筛选无命中时地图与 KPI 显示空态占位（不以 0 值画成真实点） | ⚠️ 部分可演（R1：四图层数据齐——regions 24 / heatData 600 / migrationFlows 600 / activityFeed 30；产业与行业筛选仅 `industries` 平铺字符串、无一级→二级层级；人才类型「工程人才」无命中须空态） |
| 245 | Tab「人才分布图」· 地图交互 + 搜索框 | 鼠标滚轮缩放；搜索框候选（城市 / 机构）；点击区域或标签 | 滚轮 / 搜索回车 / 点击标记 | `GET /display/v1/talent/global/dataset` | 无查询参数；搜索关键词仅前端解析 | 命中后地图 flyTo 并高亮（脉冲标注）；点击区域联动右侧面板与抽屉；清空搜索后地图复位到全球视图并清除高亮与抽屉 | ✅ 可演（R1：regions 24 城市名 + topInstitutions 20 机构名均带坐标，搜索 flyTo / 高亮 / 清空复位为前端能力） |
| 246 | Tab「人才分布图」· 迁徙图层 + 年份条 | 迁徙图层；年份（页面年度条 2020–2026）；地区 / 领域筛选 | 切到迁徙图层 / 拖动年份 | `GET /display/v1/talent/global/dataset` | 无查询参数；年份与筛选在前端过滤 `migrationFlows` | 国家间迁徙飞线出现，tooltip 显示流向与人数；净流入热点城市自动标注；迁徙维度固定「全领域」时页面需标口径（久新 FLOW 维度无 FIELD 级） | ✅ 可演（R1：migrationFlowTimeline 11 年 2015–2025，每年 from/to 名称+坐标+value 齐；净流入取 regionTimeSeries；`field` 实测全为 `ALL`，页面须标「全领域」口径——期望本身要求；2026 无边年份走空态不复用邻年） |
| 247 | Tab「人才分布图」· 区域详情 + 导出菜单 | 任一次图层 / 筛选后的视图；导出格式（XLSX / CSV） | 点击分布区域 / 点击「导出」 | 无独立端点（前端本地导出，数据源 `GET /display/v1/talent/global/dataset`） | 无查询参数；导出取当前前端过滤结果 | 弹窗展示该区域人才数量 / 学历 / 主流行业；导出 XLSX 含三张 sheet（区域汇总 / 顶尖机构 / 概览信息），或 CSV（含 BOM）；导出内容与当前筛选结果一致 | ✅ 可演（R1：导出取 regions + topInstitutions 现状结果；前端 `globalTalentExport` 已含三 sheet（区域汇总/顶尖机构/概览信息）与 CSV BOM，须浏览器核导出文件内容） |
| 248 | Tab「人才分布图」· 洞察面板 · 子 Tab「华人占比」 | 子 Tab「华人占比」；地区（国家 / 城市）；机构（顶尖高校 / 研究机构） | 切子 Tab / 点击地区或机构 | `GET /display/v1/talent/global/dataset` | 无查询参数；地区与机构在前端过滤 `chineseRatio` | 按地区展示华人占比堆叠柱；点击机构弹出该机构华人教师 / 研究员统计；无源时该子 Tab 显示空态占位 + 口径说明，不出假比例 | ✅ 可演（空态口径；R1：`chineseRatio` 实测 0 条、20 机构 chineseCount/chineseTeacherCount/chineseResearcherCount 全 0 → 按期望「无源显示空态占位 + 口径说明、不出假比例」演示） |
| 249 | Tab「人才分布图」· 洞察面板 · 子 Tab「地区分布」 | 子 Tab「地区分布」；学科 / 领域筛选；时间段（2020–2026） | 切子 Tab / 修改筛选 / 点击 Treemap 块 | `GET /display/v1/talent/global/dataset` | 无查询参数；筛选在前端过滤 `regions` | Treemap 按城市绘制人才数（面积与颜色），点击块联动地图定位；逐级下钻到国家 / 城市层级时数值随层级重算 | ✅ 可演（R1：`regionTree` 实测非空——全球→12 国→64 城两级，中国 21,611 与 DS-14 31 省合计一致；Treemap 与逐级下钻有源） |
| 250 | Tab「人才分布图」· 右列「顶尖机构洞察」 | 机构 Top20 列表；领域筛选下拉 | 点击机构行 / 切换领域 | `GET /display/v1/talent/global/dataset` | 无查询参数；领域在前端重排 `topInstitutions` | 横向排名柱 + 列表，条数 ≤20；点击机构 flyTo 并打开机构详情抽屉（基础 7 卡 / 学历结构 / 领域分布 / 核心成果 / 关联专家） | ✅ 可演（R2 2026-11-09 发布后实测：20 机构含 lat/lng、fieldDistribution、papers/patents/trend；`representatives` **20/20 家、合计 60 人（每机构 3 人）**；`coreAchievements` **20/20 家（各 2 条）**；机构学历三档 **20/20 家**（doctor/master/bachelor 齐，如浙大 258/18/6）；机构专利真实累计 20 个不同值（浙大 1,085 / 上交 2,106 / 北大 1,001，不再恒 20）。前端已删「×25%/×12%」估算） |
| 251 | Tab「人才分布图」· 洞察面板 · 子 Tab「产研对比」 | 子 Tab「产研对比」；视图切换「产」/「研」 | 切子 Tab / 点击视图切换 | `GET /display/v1/talent/global/dataset` | 无查询参数；视图切换在前端过滤 `irSplit` | 产业与科研两列分组柱并列展示人才数量与比例；切换视图只重排两份序列，不改数值；页面需注明产研口径（机构类型 company 对 education / facility / archive / government） | ✅ 可演（R1：`irSplit` 11 年 labels + industry/research 双序列真值，切换只重排不改数；页面须注明产研口径） |
| 252 | Tab「人才分布图」· 洞察面板 · 子 Tab「热点流入流出」 | 子 Tab「热点流入流出」；年份（2020–2026） | 切子 Tab / 播放或拖动年份 | `GET /display/v1/talent/global/dataset` | 无查询参数；年份在前端取 `migrationFlows` 对应年 | 时间趋势线（总量 + 净流入）、Top10 迁徙横向柱、净流入 / 净流出双列热点卡三块同时出现；无某年边时该年为空态不复用邻年数据 | ✅ 可演（R1：globalTimeSeries 12 点含 total/netInflow/migrationVolume；Top10 迁徙取 timeline 当年 flows；净流入/净流出热点取 regionTimeSeries netInflow；无某年边走空态） |
| 253 | Tab「人才的最新动态」· 气泡图层 + 动态列表 | 城市气泡；动态类型（学术发布 / 职位变动 / 创新项目）；月份（1–6 月） | 点击气泡 / 切换类型 | `GET /display/v1/talent/global/dataset` | 无查询参数；类型与月份在前端过滤 `activityFeed` | 点击气泡弹窗显示人才名称 / 动态类型 / 时间 / 来源；气泡数量随类型筛选变化；无动态城市不出现气泡；页面需标「媒体报道口径、覆盖重点人才」说明 | ⚠️ 部分可演 → **已实施·待发版转 ✅**（2026-11-09 W3-1，用户裁定 A：后端按前端五类枚举出数）。本地函数级实测 `activityFeed` 231 条：`paper` 75（论文题名 / 年份 / 期刊 / 被引 / DOI 链接）、`job` 36（机构·职位 + 在职/曾任）、`project` 45（项目编号 + 资助方，摘要注明「资助论文署名关系」）、`award` 45（荣誉名 + 授予机构）、`event` 30（原媒体流并入，含原文链接）；**类型筛选 5 项均有点位**（前端 `activityTypeOptions` 与本枚举同源，前端零改动）。生产仍为 R2 的 30/30 `media`，待发版后复跑 R2 转 ✅。契约未新增 `source` 字段 → 来源列按期望显「来源待核」，`summary` 提供期刊 / 授予机构可核对；时间仅到年（`time="YYYY"`、`month=0`），不伪造月日 |
| 254 | Tab「人才的最新动态」/ Tab「人才分布图」· 热力图层 | 热力图层；地图缩放层级（全球 → 城市）；领域筛选 | 切到热力图层 / 滚轮缩放 | `GET /display/v1/talent/global/dataset` | 无查询参数；热力强度取 `heatData[].intensity` | 热力层按强度渲染颜色深浅，图例切换为热力图例；放大到城市层级后同一区域热力不重置、不凭空加深 | ✅ 可演（R1：heatData 600 条 lat/lng/intensity 真值；图例切换与缩放不重置为前端能力） |
| 255 | Tab「人才的最新动态」· 地图导航 + 搜索框 | 鼠标滚轮；搜索框（城市关键词）；地区筛选 | 滚轮 / 搜索回车 | `GET /display/v1/talent/global/dataset` | 无查询参数；搜索词前端解析 | 搜索命中后地图自动定位并放大，同屏叠加该区域气泡与热力；搜索未命中有提示文案，不静默失败 | ✅ 可演（R1：24 城市名 + activityFeed 城市气泡 + heatData 热力可同屏叠加；未命中提示为前端能力） |
| 256 | Tab「人才的最新动态」· 筛选区 + 播放器 + 动态列表 | 动态类型（学术发布 / 职位变动 / 创新项目）；时间窗（近一周 / 近一月）；播放 / 暂停 / 拖动 | 选类型 / 点播放 / 拖时间轴 | `GET /display/v1/talent/global/dataset` | 无查询参数；类型与时间窗在前端过滤 `activityFeed` | 气泡与热点按类型过滤；播放按时间窗回放并列出对应动态；动态列表分页显示，点击条目定位城市并联动城市抽屉 | ⚠️ 部分可演（R1 + 2026-11-09 W3-1：类型筛选随五类出数解决（发版后 5 类型均有数据、播放与列表可按类型过滤）；**仍缺「近一周 / 近一月」时间窗**——页面控件为 1–6 月播放器（按 `month` 过滤），且新增四类时间只到年（`month=0`）、媒体流 30 条最新 2026-02-12 → 期望控件未落地、周/月窗密度不足（W3-3 / W3-4，D 类）；动态分页与点击联动可演） |
| 257 | 区域详情 / 机构详情 → 「代表人才」→ 画像页 · 基础信息卡 | 代表人才（区域详情或机构详情中列出）；画像页 Tab「基础画像」 | 点击代表人才 / 打开画像页 | `GET /display/v1/talent/global/dataset`（本页入口）；`GET /display/v1/talent/profile/dataset`（画像页） | 页面间以 `talentId` 传参 | 展示姓名 / 性别 / 国籍 / 出生年份 / 教育背景 / 工作单位 / 职位；无证据字段留空并标注，不推断（出生年份、性别仅少量人 source_confirmed） | ✅ 可演（R1：15 人基础卡有姓名/单位/职位/教育（degree+school+year）/工作经历（position+org+period）；nationality 0/15、gender 0/15、birthYear 仅 3/15（1958/1964/1966）→ 按期望留空并标注、不推断） |
| 258 | 机构详情「核心成果」/ 代表人才 → 画像页成果统计 | 机构；代表人才；成果类型（论文 / 专利 / 项目） | 打开机构详情 / 打开画像页 | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 机构侧展示论文数、专利数、近两年论文趋势；人才侧展示论文 / 专利 / 项目计数与被引用次数；无数据项显示空态，不补 0 | ⚠️ 部分可演（R1 + 探针：机构侧 papers/patents/trend 可演；人才侧 papers.total 232 / citations 21,568 可演，专利 **6/15 人有值**（1/4/3/1/4/6，探针 `ads_talent_patent` 全库 85,069 条 / 6,490 人）；仅 `projects` 的 national/international/fundingWan 无源——`ads_talent_project` 无级别/经费字段且项目关系仅覆盖 15 人 → 空态不补 0） |
| 259 | 机构详情论文 / 专利卡 / 画像页「分析画像」 | 机构；代表人才；指标（h_index / 被引次数 / 学术力分项） | 打开机构详情 / 切到分析画像 Tab | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 展示 h_index、被引次数与学术力分项（人才主画像投影列）；空值处显示空态占位，不以 0 冒充 | ✅ 可演（R2 2026-11-09 发布后实测：hIndex 70 / citations 21,568 有值；学术力分项 `fieldHotness` **15/15 人、0.28–0.96**，`hotspotAlignment` **15/15 人、43.5–83.2**；`impactMetrics.ifAvg` 无影响因子源仍为 0 → 按期望显示空态占位「无源」、不以 0 冒充；机构侧专利卡随 G-DS13-07 已出真实累计值） |
| 260 | 机构详情「领域分布」/ 画像页领域标签 | 机构；代表人才；领域维度 | 打开机构详情 / 打开画像页 | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 机构侧展示领域分布 Top5 图；人才侧展示研究领域标签；无领域字段的人才只显示基础信息，不生成伪标签 | ✅ 可演（R1：20 机构 fieldDistribution 有值；人才 fields/fieldLabels 有值（例：材料科学/化学/工程学），无领域者不生成伪标签） |
| 261 | 机构详情「合作网络与关联专家」/ 画像页「合作网络图谱」 | 机构；代表人才；节点类型（合作者 / 合作机构 / 团队） | 点击「合作网络与关联专家」/ 切到合作网络 Tab | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 展示合作者与合作机构节点图（画像页取 Top12 合作者）；点击节点可下钻；无合作边时显示空态占位 | ✅ 可演（R1：15 人 `collaborationNetwork` 均 13 节点 / 12 边（15/15 一致），Top12 合作者可演） |
| 262 | Tab「人才的最新动态」· 动态列表 / 城市抽屉 feed | 城市；动态类型；分页页码 | 点击动态条目 / 翻页 | `GET /display/v1/talent/global/dataset` | 无查询参数；按 `activityFeed` 前端分页 | 每条动态展示标题 / 时间 / 来源链接；条目总数与 `activityFeed` 一致；条目缺失来源时显示「来源待核」而非假外链 | ✅ 可演（R1：activityFeed 30 条按前端分页；标题/时间齐，来源缺失按期望显「来源待核」而非假外链） |
| 263 | 区域详情 / 机构详情 · 「进入评估」跨页入口 | 代表人才 | 点击评估入口 | 前端路由跳转（携带 `talentId`）→ DS-16 数据源 `GET /display/v1/talent/recommend/dataset` | 目标页无查询参数，`talentId` 用于定位 | 跳转 DS-16 并把「当前评估对象」定位到该人才；该人才不在推荐集时仍可看贡献 / 难度 / 成本 Tab，但推荐卡不出现该人且不静默换人 | ✅ 可演（R1：recommend dataset 200 / 1.9s 可用，跨页携 `talentId` 定位；不在推荐集不静默换人） |
| 264 | 机构详情「核心成果」award / 画像页「荣誉」Tab | 机构；代表人才；荣誉类型（奖项 / Fellow / 院士 / 荣誉称号） | 点击代表人才 → 画像页荣誉 Tab | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 荣誉墙展示正式事实条目（过滤候选态），每条含名称 / 授予机构 / 年份；不在富画像覆盖范围内的人才显示空态，不用机构奖项顶替个人荣誉 | ✅ 可演（R1：honors 合计 93 条正式事实——award 70 / fellow 13 / academy_member 8 / member 2，每条含名称/授予机构/年份） |
| 265 | 画像页「荣誉」Tab · 国际合作表 / 海外出访记录 | 代表人才；合作类型（项目 / 交流）；年份 | 切到荣誉 Tab / 翻表 | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 国际合作表按行展示合作项目 / 对方机构 / 年份；出访与海外交流记录区为空态占位（契约 `overseasVisits` / `overseasExchanges` 无源），不编造行程 | ✅ 可演（R2 2026-11-09 发布后实测：国际合作表 `internationalCoop` **15/15 人、90 行**（每人 6 行，含合作国家/机构/年份/合著篇数，例 US 合著 196 篇 · 2015–2025）；`overseasVisits` / `overseasExchanges` 仍是 15/15 全 0 条 → 按期望走空态占位、不编造行程） |

## LOOP 对照汇总（R1/R2 · 2026-11-09 生产网关实测）

**接口实测清单**（网关 `https://edu.itic-sci.com/tid/api`，StripPrefix=1，请求头 `Authorization: Bearer <token>` + `systemCode: display`）：

| 接口 | HTTP | 耗时 / 载荷 | 返回 | 判定 |
|---|---|---|---|---|
| `GET /display/v1/talent/global/dataset` | 200 | **3.3s / 454.9KB** | `code=0`，无 `emptyReason`；`regions` 24 / `heatData` 600 / `migrationFlows` 600 / `activityFeed` 30 / `topInstitutions` 20 | 有数据 |
| `GET /display/v1/talent/profile/dataset` | 200 | **1.5s / 380.4KB** | `code=0`；`talents` 15，honors 合计 93、collaborationNetwork 13 节点 / 12 边 | 有数据 |
| `GET /display/v1/talent/recommend/dataset` | 200 | **1.9s / 508.9KB** | `code=0`；推荐集可用（DS-16 已签收） | 有数据 |

> 较 R0b（61.1s / 110B / `DOWNSTREAM_UNREACHABLE`）：整页 TTL 缓存 + 启动预热（`lumen-topic-py` `dataset_cache.py`，2026-11-09 发布）生效，三端点均 <4s；M3「整叶 blocked」结论解除，转常规 LOOP R1。

**global 字段级事实**：`regions` 24（24/24 有 lat/lng、phdRatio、topFields、fieldStats、universities、industries、breakdown），`value` 合计 19,102；类型分布合计 leading 10 / young 1,266 / overseas 1,978 / **engineer 0**；`migrationFlowTimeline` 11 年（2015–2025，`migrationFlows[].field` 全 `ALL`）；`regionTimeSeries` 10 地区（2015–2026）；`globalTimeSeries` 12 点；`heatData` 600（lat/lng/intensity）；`activityFeed` 30（`type` 30/30 = `media`，最新 2026-02-12）；`chineseRatio` 0 条；`regionTree` 全球→12 国→64 城；`topInstitutions` 20（`coreAchievements` 0/20、`representatives` 0/20 非空，华人数全 0）；`irSplit` 11 年。
**profile 字段级事实**：15 人 `papers` 聚合（total 232 / citations 21,568 / hIndex 70）、`honors` 合计 93（award 70 / fellow 13 / academy_member 8 / member 2）、`collaborationNetwork` 13 节点 / 12 边（15/15 一致）、`recentWorks` 5/人；`patents.total` 0、`projects` 分项 national/international 0（total 366）、`nationality` / `gender` 0/15、`birthYear` 3/15、`academicInfluence.fieldHotness` / `hotspotAlignment` 恒 0、`internationalCoop` / `overseasVisits` / `overseasExchanges` 0 条。

**R2 复测字段级事实（2026-11-09 发布后，替代上述 R1 对应项）**：`global` 2.5s / `profile` 1.3s，均 `code=0` 无 `emptyReason`；`regions` 24 / `heatData` 600 / `migrationFlows` 600 / `activityFeed` 30（仍 30/30 `media`）/ `migrationFlowTimeline` 11 年 / `regionTimeSeries` 10 地区 / `irSplit` 11 年 / `chineseRatio` 仍 0 条；`topInstitutions` 20 家 **`representatives` 20/20（合计 60 人）、`coreAchievements` 20/20（各 2 条）、学历三档 20/20、专利 20 个不同真值**。`profile` 15 人：`fieldHotness` 15/15（0.28–0.96）、`hotspotAlignment` 15/15（43.5–83.2）、`internationalCoop` 15/15 共 90 行、`patents.total` **6/15 有值**（0/1/3/4/4/6，其余为探针证实的真实 0）、`projects.total` 15/15 有计数但 national/international/fundingWan 仍 0、`overseasVisits`/`overseasExchanges` 仍 0 条、`collaborationNetwork` 仍 13 节点 / 12 边。
**R2.1 本地实测（2026-11-09，未发版）**：`activityFeed` 由 30 条单一 `media` 改为 231 条五类并列出数（`paper` 75 / `job` 36 / `project` 45 / `award` 45 / `event` 30），前端 `fieldConfig.ts` 的 `activityTypeOptions` 与之逐值对齐、前端零改动；四类新增事件时间只到年（`time="YYYY"`、`month=0`），`event` 保留原日粒度。生产环境需待本次发版后才有上述数据。

**判定口径**：以每行「期望输出」为准——明细结构有真实字段 ✅；部分要素无源但可按期望走空态 / 降级 ⚠️；整维无源 ❌；设计内空态若期望输出即空态则计可演。

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演 | 18 | 245、246、247、248、249、250、251、252、254、255、257、259、260、261、262、263、264、265 |
| ⚠️ 部分可演 | 5 | 243、244、253、256、258 |
| ⛔ 待开发完成 | 0 | — |

**合计**：23 行 = 18 可演 + 5 部分可演 + 0 待开发完成（R2，2026-11-09 发布后实测；R1 为 15/8/0）。
> **R2.1（2026-11-09 待发版）**：253 已于服务侧实施五类并列出数（本地实测 231 条），发版并复跑 R2 后预期 **19 可演 / 4 部分可演 / 0 待开发**（残余 243、244、256、258）。

### 缺口建单

> 处置细则见 `../编排计划/TA-L2-DS13-供数修复方案.md`（W1–W5 分工：S 类服务侧可算 / D 类久新补采 / C 类契约缺口；含探针 SQL、字段级验收与复验脚本）。

| 缺口 | 性质 | 处置建议 | 责任方 |
|---|---|---|---|
| G-DS13-01 工程人才维恒 0（`breakdown.types.engineer` 24/24 = 0） | 供数缺口（工程人才分类未发布） | 页面按空态 + 口径说明，不补 0；久新发布分类后复判 243 / 244 | 久新 + TA 后端 |
| G-DS13-02 动态类型仅 `media` 单一型（`activityFeed` 30/30） | ~~供数缺口~~ **S 类，已实施·待发版** | **2026-11-09 W3-1（用户裁定 A）**：服务侧按前端 `activityTypeOptions` 五类并列出数 —— `paper`←代表成果、`job`←工作经历、`project`←项目概况（资助论文署名关系）、`award`←荣誉明细、`event`←原媒体流；本地实测 231 条（75/36/45/45/30），时间只到年不伪造月日。发版后复跑 R2 → 253 转 ✅、256 的类型筛选部分解除（仍缺周/月窗） | TA 后端（已完成，待发版） |
| G-DS13-03 动态时间窗密度不足（最新 2026-02-12，30 条 / 15 人档） | 供数缺口 | 256 行按备注 6 降级为「全部」并声明；媒体流扩量后复判 | 久新 + TA 后端 |
| G-DS13-04 机构 `coreAchievements` / `representatives` 空（0/20） | ~~供数缺口~~ **S 类，已修并发布生效** | 2026-11-09 服务侧修复：代表改全量人才按 h_index Top3（20/20 家、合计 60 人）、成果改事实统计 2 条（20/20 家非空）；**R2 复判通过，250 转 ✅** | TA 后端（已完成） |
| G-DS13-05 画像 `projects` 级别/类型/经费分项无源（国际合作表已修；专利经探针已排除） | 供数缺口（仅项目分项） | 国际合作表 2026-11-09 已由 `ads_talent_collaborator` 接通并发布生效（R2 实测 15/15 人、90 行），**265 转 ✅**；`projects` 的 national/international/fundingWan 仍无源 → 空态不补 0，补字段后复判 258 | 久新 + TA 后端 |
| G-DS13-06 学术力分项（`fieldHotness` / `hotspotAlignment` 已修；`ifAvg` 无源） | ~~供数缺口~~ **S 类，已修并发布生效** | 2026-11-09 服务侧按「学科热度分位 0–1 × 论文占比」出数（R2 实测 15/15 人：hot 0.28–0.96 / align 43.5–83.2）；`ifAvg` 无影响因子源，维持空态并标「无源」；**R2 复判通过，259 转 ✅** | TA 后端（已完成）；`ifAvg` 仍属久新 |
| G-DS13-07 机构专利数为采样截断（`ads_institution_patent` 每机构 ≤20 条，2,861 家恰为 20） | 供数缺口（D 类→**已修并发布生效**） | **用户裁定 2026-11-09：去「近3年」口径、显示统计总数**。后端 `topInstitutions[].patents` 改 `ads_institution_yearly_metrics` 的 `SUM(patent_count)`；**R2 实测 20 家出 20 个不同真值**（浙大 1,085 / 清华 770 / 北大 1,001 / 上交 2,106，不再同值 20）；前端抽屉标签「近3年论文/近3年专利」→「论文数量/专利数量」（demo 同步）。⚠️ 残余：年度表真实值仅覆盖 2015–2022，2023+ 缺采（2015–2020 每年 2.5–4.1 万件、2021 1.3 万、2023–2026 全 0），现为「截至 2022 的已观测累计」，2023+ 回补仍挂久新 | TA 后端 + 前端（已完成）；久新（2023+ 补采） |

> 历史（M3 · 2026-11-08）：三端点 HTTP 200 但信封 `emptyReason=DOWNSTREAM_UNREACHABLE`，23 行整叶 blocked。R0b 根因修正后确认实为实时全表聚合越过 Feign 读超时 + 无缓存，2026-11-09 整页 TTL 缓存 + 启动预热发布后解除。

## 备注与风险

1. **久新实探结论（2026-11-06，只读实测）**：库内 252 表、schema 9.14.0。本页依赖的主表：`ads_talent_profile` 100,000 行（137 列）、`ads_talent_experience` 140,893 行、`ads_geo_yearly_metrics` 171,736 行、`ads_talent_mobility_yearly_flow` 51,489 行、`ads_geo_yearly_discipline_metrics` 10,151,653 行（久新明令禁跨 Topic 相加）、`ads_institution_profile`、`ads_talent_honor_detail`（93 条正式事实）、`ads_talent_media_report`（30 条）。**双档事实**：结构化指标覆盖 10 万人，富画像（荣誉 / 媒体报道 / 简介 / 情感）只覆盖 15 名 MVP 重点人才，UI 必须按两档处理。
2. **两套人数口径并存，禁混读**：地图 / 榜单 / 区域树 = 人才当前主机构位置聚合口径；时间轴（`globalTimeSeries` / `regionTimeSeries`）= 年度论文署名活跃人才口径（2025 全城加总远大于 10 万存量）。验收按图区口径分别核对，不互相校验。
3. **契约未闭合 / 无源字段**：`chineseRatio`（无国籍、族裔列 → 空态）、`engineer`（工程人才分类久新未发布 → 0，需标口径）、全球页 `industries`（无源）、`overseasVisits` / `overseasExchanges`（无源）、`nlpFieldProfile`（无 NLP 产出）、`risks`（无源）、`difficultyEstimate` / `costEstimate`（T7 / T12 / T13 未建）。`heatData`、`activityFeed`、省卡 `industries`、`difficultyEstimate.factors.activity` 已在契约 v1.3 补为真实数据，M3 需按 v1.3 复核，勿按 v1 旧结论记空态。
4. **契约未闭合项**：本页无独立导出 / 弹窗 / 搜索接口，导出为前端本地生成；跨页跳转仅靠 `talentId` query，路由路径以 `lumen-ui-science-pc` 路由配置为准，M1 不写死。四子页供数归 WBS-02-01；技术方案 §1.2 明确「非三要素区块的对接对象清单：还没有」。
5. **页面不重做**：WBS-05-03a / 03b 只做菜单壳与非三要素区块，四子页不重做、不在本叶填数；本文件只整理可演示路径与条件。
6. **准入限制**：媒体事件流仅 30 条（15 人档、2013–2026 跨度），「近一周」时间窗的密度演示存在明显不足，M3 需判定 256 行是否降级为「近一月 / 全部」。
