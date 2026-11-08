# TA-L2-DS13 全球领域人才态势 · 合规演示用例

| 项 | 值 |
|---|---|
| 页面 | DS-13 全球领域人才态势（科技人才态势 · 全球领域人才态势） |
| WBS | WBS-05-03a（前端菜单壳）/ WBS-05-03b（后端）；四子页不重做，供数归 WBS-02-01 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` · seq 243–265（excel 行 246–268） |
| 覆盖行数 | 23（seq 243–265 每条一行） |
| 状态 | M3 实测完成 · 整叶 blocked「待开发完成」（2026-11-08：三端点 HTTP 200 但下游久新人才通道 DOWNSTREAM_UNREACHABLE，无数据返回） |
| 任务ID | DISPLAY-DEMO-CASE-TA-M1-L01 |

**主路径一句话**：进入「人才分布图」→ 领域选「人工智能」、年份 2025 → 散点 / 热力 / 迁徙三图层切换，点击有数据的城市开区域详情 → 导出 XLSX；再切「人才的最新动态」，类型选「学术发布」并播放 1–6 月气泡，点气泡看动态详情。

> 口径说明：本页四页均为「整页一次性 dataset」契约，`GET /display/v1/talent/global/dataset` **无查询参数**，界面上的地区 / 领域 / 类型 / 年份筛选在前端内存生效（`TA-接口字段映射与对接契约-20261106.md` v1.4）。因此「请求」列统一写端点 + 界面值，不编造后端筛选参数。数据情况经 M3 网关实测判定，见文末「LOOP 对照汇总」。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 243 | 全球领域人才态势 · Tab「人才分布图」· 地图 + KPI 3 卡 | 地区（全球 / 大洲 / 国家 / 城市）；产业级联（一级产业 → 二级产业）；行业；人才类型（领军人才 / 青年人才 / 海外人才 / 工程人才）；时间范围（页面年度条 2020–2026）；图层（散点 / 热力 / 迁徙 / 气泡） | 打开 Tab「人才分布图」默认加载，或修改任一筛选 / 切换图层 | `GET /display/v1/talent/global/dataset` | 无查询参数；界面值（例：地区=全球、领域=人工智能、年份=2025）由前端内存过滤 | 散点地图渲染有位置解析的城市点位，KPI 3 卡出值（人才总数 / 博士占比 / 领域覆盖）；点击城市弹出区域详情抽屉（统计 4 卡 / 学历分布 / 人才类型分布）；无位置数据的城市不出现点位、不补 0 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 244 | Tab「人才分布图」· 筛选栏 + 图层按钮 + 年份条 | 图层四选一（散点 / 热力 / 迁徙 / 气泡）；地区、产业级联、行业、人才类型、时间范围五项筛选；地图缩放层级（全球 → 国家 → 省州 → 城市） | 点击图层按钮 / 修改筛选 / 滚轮缩放 | `GET /display/v1/talent/global/dataset` | 无查询参数；界面值由前端内存过滤 | 图层互斥切换且图例随图层变化；筛选后点位、热力强度、KPI 同步重算；筛选无命中时地图与 KPI 显示空态占位（不以 0 值画成真实点） | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 245 | Tab「人才分布图」· 地图交互 + 搜索框 | 鼠标滚轮缩放；搜索框候选（城市 / 机构）；点击区域或标签 | 滚轮 / 搜索回车 / 点击标记 | `GET /display/v1/talent/global/dataset` | 无查询参数；搜索关键词仅前端解析 | 命中后地图 flyTo 并高亮（脉冲标注）；点击区域联动右侧面板与抽屉；清空搜索后地图复位到全球视图并清除高亮与抽屉 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 246 | Tab「人才分布图」· 迁徙图层 + 年份条 | 迁徙图层；年份（页面年度条 2020–2026）；地区 / 领域筛选 | 切到迁徙图层 / 拖动年份 | `GET /display/v1/talent/global/dataset` | 无查询参数；年份与筛选在前端过滤 `migrationFlows` | 国家间迁徙飞线出现，tooltip 显示流向与人数；净流入热点城市自动标注；迁徙维度固定「全领域」时页面需标口径（久新 FLOW 维度无 FIELD 级） | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 247 | Tab「人才分布图」· 区域详情 + 导出菜单 | 任一次图层 / 筛选后的视图；导出格式（XLSX / CSV） | 点击分布区域 / 点击「导出」 | 无独立端点（前端本地导出，数据源 `GET /display/v1/talent/global/dataset`） | 无查询参数；导出取当前前端过滤结果 | 弹窗展示该区域人才数量 / 学历 / 主流行业；导出 XLSX 含三张 sheet（区域汇总 / 顶尖机构 / 概览信息），或 CSV（含 BOM）；导出内容与当前筛选结果一致 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 248 | Tab「人才分布图」· 洞察面板 · 子 Tab「华人占比」 | 子 Tab「华人占比」；地区（国家 / 城市）；机构（顶尖高校 / 研究机构） | 切子 Tab / 点击地区或机构 | `GET /display/v1/talent/global/dataset` | 无查询参数；地区与机构在前端过滤 `chineseRatio` | 按地区展示华人占比堆叠柱；点击机构弹出该机构华人教师 / 研究员统计；无源时该子 Tab 显示空态占位 + 口径说明，不出假比例 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 249 | Tab「人才分布图」· 洞察面板 · 子 Tab「地区分布」 | 子 Tab「地区分布」；学科 / 领域筛选；时间段（2020–2026） | 切子 Tab / 修改筛选 / 点击 Treemap 块 | `GET /display/v1/talent/global/dataset` | 无查询参数；筛选在前端过滤 `regions` | Treemap 按城市绘制人才数（面积与颜色），点击块联动地图定位；逐级下钻到国家 / 城市层级时数值随层级重算 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 250 | Tab「人才分布图」· 右列「顶尖机构洞察」 | 机构 Top20 列表；领域筛选下拉 | 点击机构行 / 切换领域 | `GET /display/v1/talent/global/dataset` | 无查询参数；领域在前端重排 `topInstitutions` | 横向排名柱 + 列表，条数 ≤20；点击机构 flyTo 并打开机构详情抽屉（基础 7 卡 / 学历结构 / 领域分布 / 核心成果 / 关联专家） | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 251 | Tab「人才分布图」· 洞察面板 · 子 Tab「产研对比」 | 子 Tab「产研对比」；视图切换「产」/「研」 | 切子 Tab / 点击视图切换 | `GET /display/v1/talent/global/dataset` | 无查询参数；视图切换在前端过滤 `irSplit` | 产业与科研两列分组柱并列展示人才数量与比例；切换视图只重排两份序列，不改数值；页面需注明产研口径（机构类型 company 对 education / facility / archive / government） | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 252 | Tab「人才分布图」· 洞察面板 · 子 Tab「热点流入流出」 | 子 Tab「热点流入流出」；年份（2020–2026） | 切子 Tab / 播放或拖动年份 | `GET /display/v1/talent/global/dataset` | 无查询参数；年份在前端取 `migrationFlows` 对应年 | 时间趋势线（总量 + 净流入）、Top10 迁徙横向柱、净流入 / 净流出双列热点卡三块同时出现；无某年边时该年为空态不复用邻年数据 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 253 | Tab「人才的最新动态」· 气泡图层 + 动态列表 | 城市气泡；动态类型（学术发布 / 职位变动 / 创新项目）；月份（1–6 月） | 点击气泡 / 切换类型 | `GET /display/v1/talent/global/dataset` | 无查询参数；类型与月份在前端过滤 `activityFeed` | 点击气泡弹窗显示人才名称 / 动态类型 / 时间 / 来源；气泡数量随类型筛选变化；无动态城市不出现气泡；页面需标「媒体报道口径、覆盖重点人才」说明 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 254 | Tab「人才的最新动态」/ Tab「人才分布图」· 热力图层 | 热力图层；地图缩放层级（全球 → 城市）；领域筛选 | 切到热力图层 / 滚轮缩放 | `GET /display/v1/talent/global/dataset` | 无查询参数；热力强度取 `heatData[].intensity` | 热力层按强度渲染颜色深浅，图例切换为热力图例；放大到城市层级后同一区域热力不重置、不凭空加深 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 255 | Tab「人才的最新动态」· 地图导航 + 搜索框 | 鼠标滚轮；搜索框（城市关键词）；地区筛选 | 滚轮 / 搜索回车 | `GET /display/v1/talent/global/dataset` | 无查询参数；搜索词前端解析 | 搜索命中后地图自动定位并放大，同屏叠加该区域气泡与热力；搜索未命中有提示文案，不静默失败 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 256 | Tab「人才的最新动态」· 筛选区 + 播放器 + 动态列表 | 动态类型（学术发布 / 职位变动 / 创新项目）；时间窗（近一周 / 近一月）；播放 / 暂停 / 拖动 | 选类型 / 点播放 / 拖时间轴 | `GET /display/v1/talent/global/dataset` | 无查询参数；类型与时间窗在前端过滤 `activityFeed` | 气泡与热点按类型过滤；播放按时间窗回放并列出对应动态；动态列表分页显示，点击条目定位城市并联动城市抽屉 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 257 | 区域详情 / 机构详情 → 「代表人才」→ 画像页 · 基础信息卡 | 代表人才（区域详情或机构详情中列出）；画像页 Tab「基础画像」 | 点击代表人才 / 打开画像页 | `GET /display/v1/talent/global/dataset`（本页入口）；`GET /display/v1/talent/profile/dataset`（画像页） | 页面间以 `talentId` 传参 | 展示姓名 / 性别 / 国籍 / 出生年份 / 教育背景 / 工作单位 / 职位；无证据字段留空并标注，不推断（出生年份、性别仅少量人 source_confirmed） | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 258 | 机构详情「核心成果」/ 代表人才 → 画像页成果统计 | 机构；代表人才；成果类型（论文 / 专利 / 项目） | 打开机构详情 / 打开画像页 | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 机构侧展示论文数、专利数、近两年论文趋势；人才侧展示论文 / 专利 / 项目计数与被引用次数；无数据项显示空态，不补 0 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 259 | 机构详情论文 / 专利卡 / 画像页「分析画像」 | 机构；代表人才；指标（h_index / 被引次数 / 学术力分项） | 打开机构详情 / 切到分析画像 Tab | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 展示 h_index、被引次数与学术力分项（人才主画像投影列）；空值处显示空态占位，不以 0 冒充 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 260 | 机构详情「领域分布」/ 画像页领域标签 | 机构；代表人才；领域维度 | 打开机构详情 / 打开画像页 | `GET /display/v1/talent/global/dataset`；`GET /display/v1/talent/profile/dataset` | 无查询参数 | 机构侧展示领域分布 Top5 图；人才侧展示研究领域标签；无领域字段的人才只显示基础信息，不生成伪标签 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 261 | 机构详情「合作网络与关联专家」/ 画像页「合作网络图谱」 | 机构；代表人才；节点类型（合作者 / 合作机构 / 团队） | 点击「合作网络与关联专家」/ 切到合作网络 Tab | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 展示合作者与合作机构节点图（画像页取 Top12 合作者）；点击节点可下钻；无合作边时显示空态占位 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 262 | Tab「人才的最新动态」· 动态列表 / 城市抽屉 feed | 城市；动态类型；分页页码 | 点击动态条目 / 翻页 | `GET /display/v1/talent/global/dataset` | 无查询参数；按 `activityFeed` 前端分页 | 每条动态展示标题 / 时间 / 来源链接；条目总数与 `activityFeed` 一致；条目缺失来源时显示「来源待核」而非假外链 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 263 | 区域详情 / 机构详情 · 「进入评估」跨页入口 | 代表人才 | 点击评估入口 | 前端路由跳转（携带 `talentId`）→ DS-16 数据源 `GET /display/v1/talent/recommend/dataset` | 目标页无查询参数，`talentId` 用于定位 | 跳转 DS-16 并把「当前评估对象」定位到该人才；该人才不在推荐集时仍可看贡献 / 难度 / 成本 Tab，但推荐卡不出现该人且不静默换人 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 264 | 机构详情「核心成果」award / 画像页「荣誉」Tab | 机构；代表人才；荣誉类型（奖项 / Fellow / 院士 / 荣誉称号） | 点击代表人才 → 画像页荣誉 Tab | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 荣誉墙展示正式事实条目（过滤候选态），每条含名称 / 授予机构 / 年份；不在富画像覆盖范围内的人才显示空态，不用机构奖项顶替个人荣誉 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |
| 265 | 画像页「荣誉」Tab · 国际合作表 / 海外出访记录 | 代表人才；合作类型（项目 / 交流）；年份 | 切到荣誉 Tab / 翻表 | `GET /display/v1/talent/profile/dataset` | 无查询参数 | 国际合作表按行展示合作项目 / 对方机构 / 年份；出访与海外交流记录区为空态占位（契约 `overseasVisits` / `overseasExchanges` 无源），不编造行程 | 待开发完成（M3 实测：接口 200 但返回 `DOWNSTREAM_UNREACHABLE` 空态，无数据；见文末实测汇总） |

## LOOP 对照汇总（M3 · 2026-11-08 网关实测）

**接口实测清单**（网关 `http://10.50.69.111:30895`，StripPrefix=1，请求头 `Authorization: Bearer <token>` + `systemCode: display`）：

| 接口 | HTTP | 返回 | 判定 |
|---|---|---|---|
| `GET /display/v1/talent/global/dataset` | 200 | `code=0`，`data.emptyReason=「DOWNSTREAM_UNREACHABLE：久新人才通道不可达，全球人才态势暂不可用（不以演示数据兜底）」`；实测 2 次（60.2s / 10.7s）结论一致，非瞬态 | 可调但无数据 |
| `GET /display/v1/talent/profile/dataset` | 200 | `code=0`，`data.emptyReason=「DOWNSTREAM_UNREACHABLE：…人才画像暂不可用（不以演示数据兜底）」`（9.4s） | 可调但无数据 |
| `GET /display/v1/talent/recommend/dataset` | 200 | `code=0`，`data.emptyReason=「DOWNSTREAM_UNREACHABLE：…人才引进推荐评估暂不可用（不以演示数据兜底）」`（0.45s） | 可调但无数据 |

**判定口径**：网关与 `gkxlumen-display` BFF 可达，且按诚实口径返回空态信封（`code=0` + `emptyReason`，不兜底造数）；但下游 `gkx_show_service`（lumen-topic-py）→ 久新 Doris 通道不可达，**库中数据无法经接口取出**，不满足总控 §1-12 的 M3 前置「接口实测可调（200）+ 库中有数据」。据此本页整叶 `blocked`，23 行一律填「待开发完成」，不填「可演」，也不以「覆盖不到」充数。

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演 | 0 | — |
| ⚠️ 部分可演 | 0 | — |
| ⛔ 待开发完成（整叶 blocked） | 23 | 243–265 全部 |

**合计**：23 行 = 0 可演 + 0 部分可演 + 23 待开发完成。

### 缺口建单

| 缺口 | 性质 | 处置建议 | 责任方 |
|---|---|---|---|
| 久新人才通道不可达（`DOWNSTREAM_UNREACHABLE`） | 部署/环境类缺口：display BFF 在线，下游 `gkx_show_service` 或久新 Doris 连接在网关侧集群环境未就绪；**非数据缺口、非契约缺口**（契约 v1.4 记录 2026-11-07 本地四层联调曾全绿） | 恢复 `gkx_show_service` 与久新 Doris 连通后复测本页三端点；复测 200 且有数据后按契约 v1.3–v1.5 逐行重判（预期 `heatData`/`activityFeed` 已补真，`chineseRatio`/`engineer`/全球 `industries`/`overseasVisits` 等维持空态口径；256 行「近一周」窗按备注 6 复核是否降级） | 部署运维 + TA 后端 |

## 备注与风险

1. **久新实探结论（2026-11-06，只读实测）**：库内 252 表、schema 9.14.0。本页依赖的主表：`ads_talent_profile` 100,000 行（137 列）、`ads_talent_experience` 140,893 行、`ads_geo_yearly_metrics` 171,736 行、`ads_talent_mobility_yearly_flow` 51,489 行、`ads_geo_yearly_discipline_metrics` 10,151,653 行（久新明令禁跨 Topic 相加）、`ads_institution_profile`、`ads_talent_honor_detail`（93 条正式事实）、`ads_talent_media_report`（30 条）。**双档事实**：结构化指标覆盖 10 万人，富画像（荣誉 / 媒体报道 / 简介 / 情感）只覆盖 15 名 MVP 重点人才，UI 必须按两档处理。
2. **两套人数口径并存，禁混读**：地图 / 榜单 / 区域树 = 人才当前主机构位置聚合口径；时间轴（`globalTimeSeries` / `regionTimeSeries`）= 年度论文署名活跃人才口径（2025 全城加总远大于 10 万存量）。验收按图区口径分别核对，不互相校验。
3. **契约未闭合 / 无源字段**：`chineseRatio`（无国籍、族裔列 → 空态）、`engineer`（工程人才分类久新未发布 → 0，需标口径）、全球页 `industries`（无源）、`overseasVisits` / `overseasExchanges`（无源）、`nlpFieldProfile`（无 NLP 产出）、`risks`（无源）、`difficultyEstimate` / `costEstimate`（T7 / T12 / T13 未建）。`heatData`、`activityFeed`、省卡 `industries`、`difficultyEstimate.factors.activity` 已在契约 v1.3 补为真实数据，M3 需按 v1.3 复核，勿按 v1 旧结论记空态。
4. **契约未闭合项**：本页无独立导出 / 弹窗 / 搜索接口，导出为前端本地生成；跨页跳转仅靠 `talentId` query，路由路径以 `lumen-ui-science-pc` 路由配置为准，M1 不写死。四子页供数归 WBS-02-01；技术方案 §1.2 明确「非三要素区块的对接对象清单：还没有」。
5. **页面不重做**：WBS-05-03a / 03b 只做菜单壳与非三要素区块，四子页不重做、不在本叶填数；本文件只整理可演示路径与条件。
6. **准入限制**：媒体事件流仅 30 条（15 人档、2013–2026 跨度），「近一周」时间窗的密度演示存在明显不足，M3 需判定 256 行是否降级为「近一月 / 全部」。
