# FE-DISPLAY-SMALL-BATCH-A · 展示小屏批 A：态势/指数类首页

> 目标仓：`lumen-ui-science-mobile`。规范：`Design-mobile.md` **v1.1.2** + 断点规则 + 小屏 AI 出效果备忘。  
> 本文件曾在第二轮写过后未入库，2026-08-28 按第二轮稿恢复，并补第三轮至第十二轮（含科技人才态势、科技数据资源）。2026-09-01 补第十三轮（数据资源对照 demo 补区块与详情）、第十四轮（接入视窗监管人反馈）与第十五轮（人才态势对照 demo：弹窗区分、中国面状图、画像四区、引进评估布局）。人才态势与数据资源均并入本叶，不单开 handoff。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| Owner | `human:孔东` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | 任务 DoD 登记 `lite`；2026-08-28 全景至数据资源第十二轮、2026-09-01 第十三/十四/十五轮按会话默认 `full` |
| 说明 | 未用 YAGNI 跳过 D8 token、D9（镜像空则不传 metric_id）、D10 抽屉、可观测请求头、D12 网关。按页拆布局，不套统一底 Tab / 指标卡 / 地图。全景页用户点名要 ECharts 图谱，未按备忘「缓：知识图谱」跳过。评估页权重只读，未做滑条/推演。全球订阅规则与权重编辑、湾区飞线/报告导出、指数对比/导出/实时刷新留 PC。规划土地为示意数据；报告为本地预览。数据资源未新造指标 / 功能 / mock，只复刻 demo dump 与详情字段。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改 Java/Python 调用链；前端仍 `/api` → 网关 |
| 会签态 | N/A |
| 说明 | 小屏裁剪首页，不改拓扑。全景是 ECharts 预览样例，不直连 Nebula。 |

## 范围与实现

裁自展示 L1「科技发展态势」+「科技人才态势」+「科技数据资源」。`科技全域态势` 沿用 SPIKE，本叶补态势组其余 8 页 + 人才态势 4 页 + 数据资源 4 页。

第二轮（监管人反馈：8 页高度雷同）改为 **一页一布局、一页一 vue**，同一屏内按功能堆叠，不再用三分段 + 地图 + 底 Tab 套版。

| 菜单 | 路由 | 小屏布局（as-built） | 地图 | 底 Tab |
|---|---|---|---|---|
| 科学技术全景 | `/trend/tech-panorama` | 结论条 → ECharts 图谱 → 类型图例 → 关键实体芯片 + 名单 | 无 | 无 |
| 技术发展跟踪 | `/trend/tech-development-tracking` | 底栏三区：结果（得分 + 历史）/ 参数（只读 + 说明）/ 方法（四法详解） | 无 | 有（结果/参数/方法） |
| 全球创新监测 | `/trend/global-innovation-monitor` | 底栏五区对齐 demo：综合展示 / 实时数据 / 载体排行 / 监测分析 / 能力分析 | 有（综合） | 有（综合/实时/排行/监测/能力） |
| 湾区创新监测 | `/trend/bay-area-innovation-monitor` | 底栏四区对齐 demo：成果展示 / 创新能力 / 能力分析 / 指标数据 | 有（成果+指标） | 有（成果/能力/分析/指标） |
| 深圳创新监测 | `/trend/shenzhen-innovation-monitor` | 底栏四区对齐 PC：综合 / 指标 / 领域 / 城市 | 有（综合+领域） | 有（综合/指标/领域/城市） |
| 科技创新评估 | `/trend/tech-innovation-evaluation` | 底栏两区：结果（四维 + 历史）/ 指标（体系预览 + 权重） | 无 | 有（结果/指标） |
| 科技指数 | `/trend/tech-index` | 底栏四区对齐 PC：指标 / 可视化 / 排名 / 评议 | 有（可视化·地图） | 有（指标/可视化/排名/评议） |
| 科技发展规划 | `/trend/tech-development-plan` | 底栏三区对齐 demo：综合规划 / 重点领域 / 研究分析 | 有（重点领域） | 有（综合规划/重点领域/研究分析） |
| 全球领域人才态势 | `/talent/global-talent-situation` | 底栏两区：分布 / 动态 | 有 | 有（分布/动态） |
| 关注地区人才态势 | `/talent/local-talent-situation` | 底栏两区：中国 / 深圳 | 有 | 有（中国/深圳） |
| 重点科技人才画像 | `/talent/key-talent-profile` | 页内 Vant Tabs 七区：基础/关联/分析/成果/网络/领域/荣誉；二级筛选仍为 chip | 无 | 无（一级 `van-tabs` 横滑，避免 7 项底栏挤压） |
| 人才引进推荐评估 | `/talent/talent-introduction-evaluation` | 底栏四区：贡献 / 难度 / 成本 / 尽调 | 无 | 有（贡献/难度/成本/尽调） |
| 总体视窗 | `/data/data-overview` | 底栏四区对齐 SRS：统计 / 中心 / 关联 / 应用 | 无 | 有（统计/中心/关联/应用） |
| 接入视窗 | `/data/data-access` | 底栏五区：概览 / 来源 / 接入 / 历史 / 问题 | 无 | 有（概览/来源/接入/历史/问题） |
| 主题视窗 | `/data/data-theme` | 底栏三区：分类 / 资源 / 关联 | 无 | 有（分类/资源/关联） |
| 应用视窗 | `/data/data-application` | 底栏六区对齐 PC：总览 / 主题 / 供应 / 需求 / 业务 / 使用 | 无 | 有（总览/主题/供应/需求/业务/使用） |

点地图 / 名单 / 卡片 / 图谱节点只开 `ProfileDrawer`，不跳 PC。样例注释「预览样例，非 USE_MOCK fixture」。政策/图谱/成果/服务菜单仍 `PlaceholderView`（BATCH-B）。

### 本叶各模块实现功能（as-built 对照）

| 模块 | 已实现（可点可翻） | 明确不做 |
|---|---|---|
| 科学技术全景 | ECharts 图谱 roam + 类型图例；点节点过滤关键实体 11 条；全屏详情 | G6、路径播放、导出 |
| 技术发展跟踪 | 底栏三区：结果 hero 80 + 4 条历史折线；参数五维只读 + 5 套模板；四方法详解 | 权重编辑、弦线/热力、下载报告 |
| 全球创新监测 | 底栏五区：成果地图、实时 KPI、载体筛选排行、预警+推送、10 城能力雷达 | 订阅规则、权重编辑、知识图谱 |
| 湾区创新监测 | 底栏四区：67 点成果筛选地图、创新能力、SWOT、6 项指标；详情半屏 62% | 飞线、报告/指标导出、权重编辑 |
| 深圳创新监测 | 底栏四区：60 载体筛选地图、10 指标系下钻对比、8 领域集聚、8 城对标；详情半屏 62% | 报告导出、订阅、飞线 |
| 科技创新评估 | 底栏两区：结果 76 + 四大能力 + 4 历史；指标预览 + 权重 25/30/25/20 只读 | 评估过程、权重滑条、PDF |
| 科技指数 | 底栏四区：三级指标树、可视化四视图、33 条成果榜、20 人评议只读；名单半屏 / 权重说明全屏 | 对比可视化、对比篮、导出、实时刷新 |
| 科技发展规划 | 底栏三区：综合规划（预警 5 条+热点 8 项+趋势对比）、重点领域（集群/载体地图/土地/三方案）、研究分析（四档等级/图谱/重叠仪表/情报 Word） | 真用地台账；桑基/热力/四象限留 PC；报告为本地 `.doc` |
| 全球领域人才态势 | 半屏筛选；22 城散点 / 机构落点；KPI；华人占比柱；产学结构；迁徙名单；8 条顶尖机构；动态 16 条 + 月芯片 + 加载更多；分布/动态详情分窗；详情可跳画像/评估 | Excel/Word 导出；迁徙飞线；时间轴自动播放；Treemap |
| 关注地区人才态势 | 共享半屏筛选 50%；中国 ECharts 省级面状图 + 迁徙线 + 领域切换排行表；深圳三级下钻（区→园→主体）+ 排名/流动表 + 多区趋势 | 中国热力层（监管人去掉）；深圳地图+列表切换与热力；报告导出 |
| 重点科技人才画像 | 8 人检索/上下翻；一级 Vant Tabs 七区；基础简历式；关联分组+详情；分析全量图；成果时间轴；网络底栏节点详情；领域研究图谱块；荣誉卡无弹窗 | 管理员导入导出；PDF；服务端订阅；网络详情弹窗 |
| 人才引进推荐评估 | 对象筛选；贡献雷达+学科增益；难度仪表+双列因子；成本三方案 A/B/C；尽调双列推荐卡+详情；尽调本地 Word | 成本滑条推演；热力缩放；批量对比；xlsx |
| 总体视窗 | 底栏四区：KPI 下钻 + 类型/年度/活跃/多源/来源柱饼 + 智能分类 + 五类来源 + 来源表 + 接入名单；中心 28 库 KPI + 增长/热点/更新流 + 11 资源；图谱分类筛选 + 主题簇 + 融合趋势；质量进度条/雷达 + 调用周期 + 主体表 | 仪表盘一键展开全图；导出；G6 |
| 接入视窗 | 底栏五区：概览只留 KPI+完成度+归集趋势；来源渠道时间/业务维度 + 12 明细；分区对齐 demo「接入数据资源详情」（gauge/主题饼/类型/对比/themeDatabases）；历史仪表盘 12 条；问题月度+渠道统计/列表色条 | 批量复现/检索；多 Sheet 导出；概览「接入渠道」「更新周期」（demo 概览没有） |
| 主题视窗 | 底栏三区：demo 六卡 28 / 1,248 / 10.2 亿 / 18.6 TB / 91.2 / 24；7 大类芯片+子领域；主题分布饼（resourceThemeDistribution）；7 库对照表+schema 抽屉；15 节点关联图 | DirectoryTree 三栏；schema 全表导出；禁止用 7 库列表重算 KPI |
| 应用视窗 | 底栏六区：KPI + demo 原文实时监控 QPS 8,520 / 告警 + 趋势 + 7 资产排行 + 基本情况筛选；主题饼/折/排行；5 供应方；8 需求方；6 业务+12 日志；12 字段+8 用户追踪 | 真 QPS 推送 / WebSocket；多 Sheet 报告导出 |

SPIKE `科技全域态势`（`/trend/tech-overall-situation`）不在本叶编码范围，沿用已有四底栏（地图/要素/事件/分析）。

### 科学技术全景 · 功能范围（2026-08-28 第三轮）

对照 demo-ui-science 科学技术全景的 **图谱展示 / 关键实体 / 详情** 三块；小屏裁剪，不是中屏全功能。

| 块 | 做了 | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 图谱展示 | ECharts `type: 'graph'` + `layout: 'none'` + roam；类型色点图例；点节点高亮并过滤实体 | `App.jsx` `simulatedGraphNodes` / `simulatedGraphRelations` **核心 7 节点 + 7 边** | G6 / 图谱建模；`graphKeyPathMockStageNodes` 21 个路径叠加节点；路径比较 / 播放；导入 / 手动添加 / 撤销重做；关系类型与深度筛选 |
| 关键实体 | 类型芯片 + `ListCard` 名单；随选中节点 `nodeIds` 过滤；「清除」回到全部 | `graphListData.js` `graphListRecordSeeds` **11 条**（智能机器人、鹏城实验室、北京大学深圳研究生院、具身智能控制专利族、机器视觉论文簇、先进制造企业联合体、机器人平台验证项目、多模态感知论文簇、具身控制子技术、工业机器人场景应用、深圳机器人转化关键路径） | 列表排序 / 地域字段筛选 / 导出 |
| 详情 | 全屏 `ProfileDrawer`，只留关闭。技术点（`technology` / `subTechnology`）走节点详情；机构 / 论文 / 专利 / 项目走实体详情 | `graphObjectDetail.js` `buildGraphNodeDetail` / `buildGraphEntityDetail`（关联强度、成熟度、关联对象芯片、评分、时间线、贡献说明） | demo L6 双按钮「查看关联实体」；点选跳 PC |
| 结论条 | demo `graphMapAnalysis` 口径：「需继续验证关键实体之间的跨区域协同与成果转化支撑。」 | `graphMapAnalysis.js` | — |

要素色对齐 `Design.md` §4.4（科研机构 `#4DD164`、论文 `#A872E2`、专利 `#58A8F9`、项目 `#83DDD3` 等）。实现落在 `src/views/trend/panoramaSamples.ts` + `TechPanoramaView.vue`；`echarts.ts` 已注册 `GraphChart`。

### 技术发展跟踪 · 功能范围（2026-08-28 第四轮）

对照 demo-ui-science 技术发展跟踪的 **评估结果查看 / 历史评估记录 / 评估参数查看与说明 / 评估方法详解（4 种）**。小屏裁剪，不是中屏向导全功能。监管人确认后去掉第一版「跟踪」底栏（话题热力 / 地理分布 / 评估工作流）。

默认进 **结果**。点得分、记录、维度、模板、方法只开全屏 `ProfileDrawer`，不跳 PC。实现：`src/views/trend/trackingSamples.ts` + `TechDevelopmentTrackingView.vue`。

| 块 | 做了 | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 评估结果查看 | 综合得分 hero（80）+ 阶段「综合跃升」+ 趋势「上升」；点 hero 开本次详情（四方法分、成熟度/产业化/活跃度分项、阶段折线） | `App.jsx` `resultSummary*` / `technologyTrackingEvaluationHistoryMatrix.cells.comprehensive.current`（总分 80、阶段综合跃升） | 下载报告 / 重新评估；话题热力图、动态气泡、雷达、弦线图；结果图种切换 |
| 历史评估记录 | 4 条 `ListCard`（2023–2026）+ 综合得分折线；点记录开该方法分与分项 | `App.jsx` `demoEvaluationHistoryTrace` + `techDevelopmentTracking.js` `technologyTrackingEvaluationHistoryMatrix`（四期 × 四方法 cells） | PC「无历史 / 模拟有记录」演示开关；并排对比矩阵、阶段/方法对比宽表 |
| 评估参数查看 | 当前「综合评估默认模板」五维权重条 + 阈值；点维度看说明 | `App.jsx` `technologyEvaluationParameterTemplates[0]` + `defaultTechnologyEvaluationWeights` / `Thresholds` / `DimensionLabels` | 权重滑条编辑、权重合计校验、导入/导出 JSON、应用到评估参数 |
| 评估参数说明 | 标题旁「查看说明」：五维口径 + 权重/阈值/配置建议 | `App.jsx` `TechnologyEvaluationParameterGuideDialog` | — |
| 参数模板 | 5 套系统模板名单，点开权重/阈值/启用维度 | `App.jsx` `technologyEvaluationParameterTemplates`（综合默认 / 产业化落地 / 前沿跟踪 / 政策匹配 / 风险识别） | 保存为模板、自定义模板 |
| 评估方法详解 | 4 张方法卡；点开原理、场景、输入输出、步骤、案例摘要、最佳实践、对参数影响 | `App.jsx` `technologyEvaluationMethods`（专家评估法 / 经济分析法 / 运筹学评价法 / 综合评价法）+ `technologyEvaluationMethodKnowledgeBase.cases` 各 1 条主案例 | 方法横向对比宽表；完整案例库；把方法纳入当前推荐组合 |

### 深圳创新监测 · 功能范围（2026-08-28 第五轮 · as-built）

对照 demo-ui-science `ShenzhenInnovation.tsx` 四个 PC Tab（载体综合 / 科技发展指标 / 领域分布 / 城市分析）。底栏 `PageTabs`（Vant `van-tabbar`）短标签：**综合 / 指标 / 领域 / 城市**。默认进 **综合**。

**点选交互（监管人确认）**：综合 / 指标 / 领域 / 城市内所有详情（地图点、名单、指标说明、领域行、城市 hero/排名）一律半屏 `ProfileDrawer`（高 62%，`full=false`，只留关闭），不跳 PC。筛选另走半屏 `FilterSheet` 50%。

实现：`src/views/trend/shenzhenSamples.ts` + `ShenzhenInnovationMonitorView.vue`。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 综合展示 | ① 半屏筛选 50%：关键词 / 载体类型多选 / 区域多选 / 领域 / 价值档（高≥80 / 中 60–79 / 低&lt;60）。② `CropMapStage` 地图+列表切换，中心深圳、zoom 11、高 300px。③ 聚焦范围五档：区级 / 街道级 / 产业园级 / 园区级 / 主体级，分组或名单排名 Top10。④ 点地图或名单开半屏载体详情（类型、街道、专利/论文/项目/人才、研发投入、领域覆盖、孵化、合作、当前筛选排名） | `generateCarriers()`：20 街道 × 3 载体 = **60 条**（粤海/桃源/福保/香蜜湖/笋岗/东晓/新安/福海/坂田/龙城/民治/观湖/坑梓/坪山/凤凰/玉塘/盐田/梅沙/葵涌/南澳 + 类型/分值公式）。坐标已转 Leaflet `[lat, lng]` | 订阅动态、载体对比雷达表、飞线、脉冲高亮、AMap 显示模式面板 |
| 指标展示 | ① 10 个一级指标系可展开下钻（专家学者含三级）。② 选中指标：柱/折/饼/雷达 + 构成 pill +「说明」半屏（来源/算法/历史序列）。③ 多维度对比：最多 4 个一级指标折线 + 对比判断文案。④ 区间对比：三时段芯片（2021-2023 / 2022-2024 / 2023-2025）；每行展示 **期初→期末 单位 · 区间增量 单位** + 右侧区间增速（对齐 demo 区间表，监管人要求补数值）。无报告/导出入口 | `generateIndicators()`：论文 48200 篇、期刊 950、专利 168000、专家学者 38200（核心/增量 + 高层次/青年骨干/柔性引进）、会议 1180、组织机构 4200、课题项目 2360、资金 152 亿元、政策 436、基础设施 1260。历史按 yoy 回推 2021–2025 | 领导汇报/分析师/简版报告；Word 导出；跨单位标准化指数模式 |
| 领域分布 | ① 8 领域芯片多选（至少保留 1 个）。② 全市 + 10 区芯片。③ 四指标切换：企业数量 / 专利数量 / 研发投入 / 人才数量。④ 空间集聚地图（强度≥70 落点，地图+列表）。⑤ 已选领域对比横柱 + 热度行。⑥ 优/潜/弱判断（全选=全领域结构判断；单选=单领域分析与建议；多选=多领域对比判断）。点地图或行开半屏领域详情 | `generateTechDomains()`：合成生物 / 光载信息 / 量子信息 / 脑科学与脑机工程 / 深地深海 / 智能机器人 / 前沿新材料 / 未来网络与通信。企业 5200…1280、专利 28600…7600。判断口径对齐 `classifyDomainAdviceRows`（按当前指标排序：第 1=优势、第 2=潜力、末位=薄弱） | 领域研判报告生成 / Word |
| 城市分析 | ① hero：深圳综合指数 **92**、全球样本池第 2、潜力极高；点开半屏。② 搜索 + 8 城多选（深圳锁定；默认深圳/北京/上海）。③ 城市排名柱 + 名单。④ 能力雷达（最多 3 城，四维归一）。⑤ 2021–2025 轨迹 + 2026–2027 斜率外推预测。⑥ 缺口对标：选基准城（默认北京），四维深圳 vs 基准数值条。⑦ 缺口来源 3 条 + 结论建议。点城市开半屏（优势/薄弱/建议 + 历史折线） | `generateCompareCities()`：深圳 92 / 北京 90 / 上海 89 / 杭州 87 / 广州 86 / 新加坡 88 / 硅谷 94 / 东京 89。`gapSourceItems`（基础研究投入、顶尖高校资源、国际科研网络）。`compareConclusionSummary` | Word/打印三套报告模板 |
| 点选弹窗 | 全页统一半屏底弹 62%（`ProfileDrawer` 默认 sheet，已去掉 `full`）。筛选半屏 50%。地图工具条全屏仍是地图铺满，不是详情弹窗 | — | 全屏详情抽屉 |

### 修改内容（深圳第五轮，相对第二轮首页）

- 按 PC 四 Tab 拆底栏，不再用第二轮「区级地图 + 领域读数 + 对标缺口」单页滚动。
- mock 从 `batchASamples.ts` 抽到 `shenzhenSamples.ts`，与 demo `generateCarriers` / `generateIndicators` / `generateTechDomains` / `generateCompareCities` 同公式同数字。
- 指标 Tab 明确不下发报告与导出；区间对比补期初/期末/增量数值。
- 详情由全屏改为半屏，与筛选半屏同类。

### 科技创新评估 · 功能范围（2026-08-28 第六轮）

对照 demo-ui-science `pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx`。监管人指定功能点：**权重分布 / 指标体系预览 / 历史评估记录 / 结果查看**；随后明确 **去掉评估过程**。小屏裁剪，不是中屏向导全功能。

底栏两区：`结果` / `指标`。默认进 **结果**。点得分、维度、报告、建议、权重说明只开全屏 `ProfileDrawer`，不跳 PC。实现：`src/views/trend/evaluationSamples.ts` + `TechInnovationEvaluationView.vue`。已从 `batchASamples.ts` 删除自造 `EVAL_DIMS` / `EVAL_RESULTS`，避免双真源。

| 功能点 | 做了 | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 结果查看 | 综合得分 hero **76**；范围 pill（南山区 / 综合评估）；四维雷达；四大能力条（科学创造力 83 较强 / 技术创新力 77 稳步提升 / 产业发展潜力 72 具备潜力 / 政策与条件保障力 69 需加强）；4 条政策优化建议。点 hero 开综合详情（四维分 + 范围字段 + 建议）；点维度开分项得分、口径、来源、方法、二级权重 | `dimensionBaseConfigs` 四维分与 `status`/`summary`/`metrics`；综合分按一级权重 25/30/25/20 加权展示为 76；范围对齐 `DEFAULT_FILTERS`（南山区 / `CL-SEI-01` 新一代信息技术 · `INB1303` 集成电路 / 2019年 - 2025年 / 申报量·授权·公开 / 综合评估-系统仿真模型）；`policySuggestions` 4 条；`updatedAt` `2025-06-17 14:35:22` | 重新评估向导、产业/区域/时间筛选编辑、知识关联图谱、趋势预测图、空间分布地图、导出 PDF |
| 历史评估记录 | 4 条 `ListCard`；点开范围/时间/状态。本次（人工智能）抽屉带四维分 + 政策建议，归档三条只读预览 | `reportHistoryItems`：人工智能创新能力综合评估报告（2025-06-17 已生成）/ 智能机器人技术创新力专题报告（2025-05-28 已归档）/ 未来网络产业发展潜力报告（2025-04-16 已归档）/ 政策与条件保障力优化建议报告（2025-03-09 已归档） | 评估报告中心「生成 PDF」；条件变更后重算 snapshot |
| 指标体系预览 | 「指标」Tab：四维一级行，副文案串二级短名；点开定义 / 数据来源 / 计算方法 / 分项权重与得分 | `dimensionBaseConfigs`：科学创造力 4 项（论文数量、网络中心性、研究前沿、趋势预测）；技术创新力 6 项（专利数量、专利质量、市场潜力、空间分布、趋势预测、综合评估）；产业发展潜力 6 项（产业投入、产品成熟度、产业产值、科学影响力、技术影响力、综合评估）；政策与条件保障力 6 项（战略引导力、政策扶持力度、经费支持、项目支持、实施效果、综合评估）+ 各维 `indicatorIntro` | 布尔全树页内展开、指标拖拽排序 |
| 权重分布 | 同「指标」Tab：雷达（一级权重 ×3，对齐 demo 画法）+ 25/30/25/20 条；标题旁「查看说明」出二级权重表。只读 | `DEFAULT_WEIGHTS`：科学 25（二级 25×4）；技术 30（17/17/16/17/16/17）；产业 25（17/17/16/17/16/17）；政策 20（17/17/17/16/16/17）。一级、各维二级合计均为 100% | 管理权重滑条、权重合计校验、应用到评估、导入/导出 JSON |
| 评估过程 | 不下发 | — | 监管人要求去掉：选择评估条件步进、六任务快照（论文合作网络分析…系统仿真预测）、德尔菲/仿真过程解释、五类数据进度、实时发现洞察、「应用并开始评估」跑批动画 |

### 全球创新监测 · 功能范围（2026-08-28 第七轮）

对照 demo-ui-science `pages/global-innovation` 五个 PC Tab。底栏用已有 `PageTabs`（Vant `van-tabbar`），短标签：综合展示 / 实时数据 / 载体排行 / 监测分析 / 能力分析。默认进 **综合展示**。点地图/名单/预警/城市开全屏 `ProfileDrawer`（`full`），不跳 PC。实现：`src/views/trend/globalInnovationSamples.ts` + `GlobalInnovationMonitorView.vue`。`echarts.ts` 已注册 `RadarChart`。

| 块 | 做了 | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 综合展示 | 类型芯片（全部/专利/论文/新闻/机构/企业）+ `CropMapStage` 成果地图 320px + 成果列表；点开详情 | `INNOVATIONS` **10 条**（深圳人工智能企业…柏林光载信息新闻） | 订阅规则配置 |
| 实时数据 | 4 张 KPI（专利 128,456 / 论文 89,234 / 投资 456 亿 / 机构 2,456）+ 趋势折线/柱状 + 领域饼图/柱状 | `REALTIME_KPI` / `REALTIME_TREND` / `DOMAIN_DISTRIBUTION` | 30s 真推送；权重编辑 |
| 载体排行 | 半屏 `FilterSheet`（70%）：关键词 / 总体·领域·地区排名 / 领域 / 城市；分组名单；点开载体详情（含五年分） | `CARRIERS` **10 条**（华为技术、腾讯科技、清华大学、中科院深圳先进院等） | 自定义权重排行 |
| 监测分析 | 创新点发现 3 条；城市创新数据监控预警卡一行一条；智能推送已读/未读。点开评估雷达 | `ALERTS`（量子信息领域突破性进展等）+ `PUSH_RECORDS` 4 条 | 订阅规则、忽略后的服务端同步 |
| 能力分析 | 半屏筛选：中国/国际城市 + 综合/五维方法；10 城排名；点开五维雷达 + 三条政策建议 | `CITIES` **10 城**（深圳 94 … 柏林 68）+ `CITY_METHODS` | 知识图谱、监测模型配置 |

### 湾区创新监测 · 功能范围（2026-08-28 第八轮）

对照 demo-ui-science `BayAreaInnovation.jsx` 四个 PC Tab。底栏短标签：成果展示 / 创新能力 / 能力分析 / 指标数据。默认进 **成果展示**。点成果/城市/SWOT/指标开**半屏** `ProfileDrawer`（高 62%，`full=false`），不跳 PC。实现：`src/views/trend/bayAreaInnovationSamples.ts` + `BayAreaInnovationMonitorView.vue`。时间筛选相对样本日 `2025-09-28`，避免按「今天」把 2025 成果滤空。

| 块 | 做了 | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 成果综合展示 | 半屏 `FilterSheet`（70%）：城市多选 / 成果类型多选 / 领域 / 近 30 天·90 天·一年；6 类统计；地图+下方列表联动高亮；点开半屏详情 | `generateInnovationPoints` 同算法 **67 点 / 11 城**（鹏城实验室、南沙实验室等） | 飞线、脉冲高亮 |
| 创新能力 | 综合分 hero + 四维 pill；「计算方法」弹窗（公式与四维权重）；深/穗/港趋势折线；11 城柱状；点城市开子指标雷达 | `CITY_SEEDS` 四维指数 + `history` 2020–2025；默认短板维按均值最低 | 权重滑条编辑 |
| 创新能力分析 | SWOT 雷达 + 2×2 卡 + 因素列表；默认优先短板（W，与 demo `getDefaultSwotItem` 一致）；点卡/因素开诊断弹窗 | `generateSwotData` 四象限全文（优势 82 / 短板 58 / 机会 76 / 威胁 64） | 报告导出、生成报告 |
| 创新指标数据 | 搜索 + 4 类名单（产出/投入/转化/知识产权）；「指标口径」弹窗；GIS 落点；对比柱；点城市看构成项 | `INDICATORS` **6 项**（创新产值、创新比例、创新投入、技术合同交易额、专利及论文数量、专利授权量）+ 11 城构成 | 指标导出、常用星标 |

### 科技指数 · 功能范围（2026-08-28 第九轮 · as-built）

对照 demo-ui-science `pages/tech-index/index.jsx` 四个 PC Tab（指标展示 / 指数可视化展示 / 科技成果综合排名 / 专家评议）。底栏 `PageTabs` 短标签：**指标 / 可视化 / 排名 / 评议**。默认进 **指标**。

监管人指定：除 **对比、导出、实时刷新开关** 外对齐 4 Tab；筛选项多的走半屏 `FilterSheet`（50%，底栏「重置/筛选」固定不随字段滚动）。

**点选交互（监管人确认）**：区域排行、专家名单、成果榜点开一律半屏 `ProfileDrawer`（高 62%，`full=false`，只留关闭）。指标树「查看详情」与「查看指标权重展示」仍全屏。不跳 PC。

实现：`src/views/trend/techIndexSamples.ts` + `TechIndexView.vue`。已从 `batchASamples.ts` 删除自造 `INDEX_*`，避免双真源。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 指标展示 | ① 三级缩进树：一级蓝 / 二级绿 / 三级橙 + 左竖线；默认展开四个一级、三级收起。② 点一级/二级展开子级并选中；点三级开半屏详情。③ 选中节点摘要 +「查看详情」全屏（口径、公式、赋权依据、同级权重、版本折线）。④「查看指标权重展示」全屏：AHP+德尔菲方法、四步、一级权重 40/30/20/10 | `indicatorTreeData`：科技创新能力 40%（科研投入/创新产出）· 科技影响力 30%（学术/产业）· 科技发展潜力 20%（人才/技术储备）· 科技保障能力 10%（政策/资金）。`indicatorWeightSetting`（层次分析法结合德尔菲）。`indicatorWeightBasisById`。`indicatorVersionHistory`（如 2024-v1 创新能力 40%） | 权重树编辑、判断矩阵录入 |
| 指数可视化 | ① 半屏筛选 50%：科技领域 / 机构类型 / 地域 / 时间 / 指标维；底栏重置/筛选固定。② 四视图芯片（无对比）：地图、专家、趋势、活跃度。③ 地图：34 省 `CropMapStage` + 区域排名行，点开半屏（指数/排行/五年趋势，北京有 2020–2024 序列）。④ 专家：H 指数横柱 Top12 + 名单，点开半屏（H/被引/论文/活跃度）。⑤ 趋势：四维折线，可按领域微调。⑥ 活跃度：最多 3 人雷达（论文产出/引用/项目/合作/活跃/转化） | `regionIndexData` 34 条（北京 95.8 第 1 … 西藏 52.1）。`expertData` **20 人**（张浩然中科院 H92 活跃度 95 等）。`trendData` 2020-01～2024-06 四维。`expertRadarData` 6 轴 | **综合对比可视化**；可视化结果导出；模拟实时刷新开关；大屏导航链接 |
| 科技成果综合排名 | ① 综合榜 / 高校榜 / 企业榜 / 科研机构芯片。② 半屏筛选 50%：关键词 / 领域 / 成果类型 / 机构 / 地域 / 近 1·2·5 年 / TOP10·50·100 / 得分档。③ 名单点开半屏：综合得分、上期排名、四维贡献、数据来源芯片、2021–2024 得分折线 | `rankingData` **33 条**成果。综合分派生：创新 40% + 影响 30% + 潜力 20% + 保障 10%（禁止手写总分）。例：智能机器人柔性装配关键技术及产业化 | **排名对比分析** / 对比篮；排名结果导出 |
| 专家评议 | 只读：AI 辅助建议条（Mock，不接真模型）+ 说明「新增/停用请到维护管理」+ 20 人按活跃度降序。点开半屏同可视化专家详情 | `expertData` 20 人 | 评议管理后台（新增/停用专家） |
| 点选弹窗 | 名单/地图/排行：半屏 62%。指标详情与权重说明：全屏。筛选：半屏 50%，`QuickFilter` 字段区滚动、`quick-filter__actions` 底栏固定 | — | 对比抽屉 |

### 修改内容（科技指数第九轮，相对第二轮首页）

- 按 PC 四 Tab 拆底栏，不再用第二轮「hero + 扁平指标条 + 5 省地图 + 5 条成果」单页滚动。
- mock 抽到 `techIndexSamples.ts`，与 demo `indicatorTreeData` / `regionIndexData` / `expertData` / `rankingData` / `trendData` 同数字同口径。
- 监管人点选后：筛选底栏固定；广东省/张浩然等名单改半屏；指标树改为一级/二级/三级缩进色标，不再用与二级同外观的 `ListCard` 铺平三级。

### 科技发展规划 · 功能范围（2026-08-28 第十轮 · as-built）

对照 demo-ui-science `TechDevelopmentPlan.tsx` 三个 PC Tab（综合发展规划 / 重点领域规划 / 研究领域分析）。底栏 `PageTabs` 短标签：**综合规划 / 重点领域 / 研究分析**。默认进 **综合规划**。

监管人指定：全功能复刻 demo mock；小屏按底栏分区堆叠，不另起一套 UI。点预警/热点/人才/资源/载体/方案/情报开 `ProfileDrawer`（默认半屏 62%；「生成报告」全屏并可本地下载 `.doc`）。不跳 PC。

实现：`src/views/trend/planSamples.ts` + `TechDevelopmentPlanView.vue`。已从 `batchASamples.ts` 删除自造 `PLAN_*` / `TREND_YEARS`，避免双真源。`echarts.ts` 已注册 `GaugeChart`。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 综合规划 | ① 半屏筛选：时间 3/6/12 个月、规划区域（深圳/湾区/全国/全球）、人才流动（全部/学术→产业/产业→学术/预警）。② 潜在方向预警：6 源均分 KPI + 5 条预警卡一行一条（具身智能高预警、大模型安全高预警、量子工程化关注、合成生物关注、光载信息观察）；点卡开半屏；「生成报告」全屏 + 下载 Word。③ 全球热点技术捕捉 8 行（人工智能大模型热 98 … 可控核聚变 76）；默认 Top3 对比高亮（大模型/量子/合成生物），选中只留浅蓝底无描边。④ 热点动态跟踪：chip 最多 5 项对比 + 时间趋势折线 / 空间分布柱（南山…龙岗）；「口径」弹窗（热度公式 40/30/20/10）。⑤ 7 类指标 pill（技术发展/产业/机构/课题/成果/统计/人才）。⑥ 本地优势：领域/能力/产出三视图，深圳 vs 全球平均横柱。⑦ 人才：TOPS 净流入（华为 +1,248 … 中山大学深圳 −276）+ 5 条流动名单。⑧ 资源推送 5 条 + 推送设置半屏（领域多选 / 每日·每周） | `HOT_TECHS` 8 项（专利/论文与 demo 同数，如合成生物学 5,890 / 1,860）。`MONITOR_ITEMS` 5 条 + 六源分。`TALENT_FLOWS` 5 人。`RESOURCES` 5 条。`TREND_SERIES` 3m/6m/12m | 真预警推送；人才桑基图 |
| 重点领域 | ① 半屏筛选：规划区域（深圳市/南山/福田/光明/坪山）、载体类型、土地用途、对标区域。② 3 产业集群芯片（人工智能/生物医药/新能源）+ 4 图层（科技载体/土地效益/资源缺口/产业热度）。③ `CropMapStage` 载体地图 280px，点开半屏（鹏城实验室等 **22** 点）。④ 竞争力 5 pill（综合 78.5 / 创新 88 / 产业 85 / 开放 62 / 潜力 82）+ 五维条 + 5 城对标。⑤ 载体三视图：按类型条 / 按行政区 / 列表。⑥ 土地用途效益柱，文案标明示意数据。⑦ 三套配置方案（A 策源 / B 转化 / C 空间），点开半屏 | `CARRIERS` 22 条（L/C/P/I/A）。`CLUSTERS` 3。`SCENARIOS` 3。`LAND_USE` 6 条效率 | 真用地台账核算；AMap |
| 研究分析 | ① 半屏筛选：目标主体 / 对比主体 / 领域 / 近 1·3·5 年 / 情报等级 / 重叠规则（严格/均衡/宽松）。② 四档等级（领先 92 / 优势 76 / 追赶 58 / 潜力 34）。③ ECharts `graph` roam（先进院为中心，企业/机构/领域/文献/专利）。④ 重叠度仪表 + 华为 82 / 腾讯 67 / 大疆 48 条。⑤ 6 企竞争等级（华为/腾讯 S … 小米 B）。⑥ 情报 4 条；「生成报告」全屏 + 下载 Word | `GRAPH_NODES`、`OVERLAP_BARS`、`COMPANIES`、`INSIGHTS`；重叠随时间窗 `TIME_SCOPE_FACTOR` 缩放 | G6 建模；重叠热力 / 四象限 |
| 点选弹窗 | 名单/预警/热点/载体/方案：半屏 62%。生成报告：全屏 + 页内「下载 Word」（blob，非服务端） | `downloadWord` | PDF 打印；跳 PC |

### 修改内容（科技发展规划第十轮，相对第二轮首页）

- 按 PC 三 Tab 拆底栏，不再用第二轮「预警卡 + 本地 vs 全球折线」单页滚动。
- mock 抽到 `planSamples.ts`，与 demo `TechDevelopmentPlan.tsx` 同数字同口径（热点 8 项、预警 5 条、载体 22、人才 5、方案 3）。
- 热点行 `heat-row.active`：保留 `--sci-primary-soft` 底色，去掉主色描边与 outline（键盘 `:focus-visible` 仍保留描边）。对比切换走上方 chip（最多 5），点行开详情。
- 详情默认半屏；预警/情报「生成报告」全屏并可本地下载 `.doc`。知识图谱用 ECharts，不接 G6。
- 小屏取舍：人才桑基→机构净流入 + 名单；重叠热力/四象限→仪表 + 条；高德→Leaflet；PDF→报告预览 + 本地 Word。

### 科技人才态势 · 功能范围（2026-08-28 第十一轮 · as-built）

对照 demo-ui-science `pages/talent-trend`。人才态势属展示「态势」族，并入本叶，不单开 handoff。布局同批 A：一页一 vue、PC Tab→底栏/chip、FilterSheet、ProfileDrawer、CropMapStage。

点地图 / 名单 / 卡片开 `ProfileDrawer`（默认半屏 62%）。画像 ↔ 评估用路由 `?id=`，不跳 PC。实现：`src/views/talent/*.vue` + `talentSamples.ts` + `talentDump.ts`（冻结 demo `data.js` 种子 `20260821`：22 城 / 20 机构 / 16 动态 / 31 省 / 10 区 / 8 人）。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 全球领域人才态势 | 底栏两区默认 **分布**。半屏筛选；`CropMapStage` 22 城散点 / 机构落点；KPI；华人占比柱；产学结构；迁徙名单；8 条顶尖机构。动态 16 条 + 月芯片。详情可跳画像/评估 | demo `talent-trend` 全球页种子 | Excel/Word 导出；迁徙飞线；时间轴自动播放；Treemap |
| 关注地区人才态势 | 底栏两区：中国 / 深圳。共享半屏筛选 50%。中国：31 省落点+排名+8 条省际流动。深圳：10 区落点+趋势/流动/结构+园区 | 同上中国/深圳页 | china.json 色斑图；园区下钻热力；报告导出 |
| 重点科技人才画像 | 8 人检索/上下翻。chip 七区：基础/关联/分析雷达/成果/ECharts 合作图/关键词/荣誉。本地订阅开关 | 8 人冻结样例（首条张明远 / MIT） | 管理员导入导出；PDF；服务端订阅 |
| 人才引进推荐评估 | 底栏四区默认 **贡献**。贡献雷达+学科增益；候选学者对照表（姓名/单位/贡献）。难度仪表+6 因子；策略行左侧圆角色条（红/黄/绿），无箭头、不写 red/green。成本三方案 A/B/C；政策条目无点击无箭头。尽调对照表 + 本地 Word | `CONTRIBUTION` / `DIFFICULTY` / `COST` / `RECOMMENDATIONS` | 成本滑条推演；热力缩放；批量对比；xlsx |

### 修改内容（科技人才态势第十一轮）

- 4 页从 `PlaceholderView` 改为独立 vue；mock 抽到 `talentDump.ts`，不进 BATCH-B。
- 画像七区用 chip 换行，避免 7 项底栏挤压；评估成本用三方案卡，不用滑条。
- 中国地图用 Leaflet 省点，不用 echarts geoJSON。
- 评估名单由 `ListCard` 改为 `.data-table`；无点击的 `ListCard` 加 `plain` 去 `›`；策略用 `.tone-note` 左侧弧形色条。

### 科技数据资源 · 功能范围（2026-08-28 第十二轮 · 首版 as-built）

对照 demo-ui-science `pages/data-resources` 四视窗。PC 为长滚动/三栏/六 Tab，小屏按 SRS 与 PC Tab 拆底栏 + 半屏抽屉，避免单页过厚。无地图。实现：`src/views/data/*.vue` + `dataSamples.ts` + `dataDump.ts`（冻结 `mockData.js` 全量 49 个 export）。

第十二轮首版只铺了底栏骨架与主表；自造主题 KPI、缺 demo 区块与详情字段。以第十三 / 十四轮 as-built 为准。

### 科技数据资源 · 第十三轮（2026-09-01 · 对照 demo 补区块，不新造）

监管人要求：重新对照 `demo-ui-science/src/pages/data-resources/`，调整 `lumen-ui-science-mobile` 科技数据资源；**不新造指标、不新造功能、不新造 mock**；复刻 demo mock；详情弹窗内容也要复刻。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 去掉自造口径 | 主题视窗不再用 7 条 `themeDatabases` 算出「主题库 / 数据表 / 来源 / 均质」；主题分布饼不再用表数重算 | `THEME_OVERVIEW_KPIS` 对齐 `ThemeWindow` 六卡：28 / 1,248 / 10.2 亿 / 18.6 TB / 91.2 / 24（主题库总数读 `bigDataCenterStats.overview.totalDatabases`）；饼图用 `resourceThemeDistribution` | 禁止另起一套 KPI |
| 总体视窗 | 补回：多源整合横柱、来源柱/饼、智能分类四卡、五类来源表、来源明细筛选、KPI 下钻（来源/主题）、图谱分类芯片、融合趋势、中心近 7 日增长 / 热点 / 更新流；应用区质量进度条 ↔ 雷达 | dump 已有字段；`dataSamples.check.mjs` 断言无「均质」、有「资源总量」、7 库 / 28 主题库 / schema / provider / relatedProject / deployLocation | 导出；宽表；一键展开仪表盘 |
| 接入视窗 | 来源：渠道 / 时间细分 / 业务类型 + 月/季；历史：`historyAccessDashboard` 归档/渠道/成功率/异常 + 趋势；问题：类型饼 + 集群柱 + 月度折 + 渠道柱 | `accessSourceAnalysis` / `historyAccessDashboard` / `problemResourceStats` | 批量复现/检索；多 Sheet |
| 主题视窗 | 分类区六卡 + 7 大类芯片；资源区分布饼 + 7 库表；点开走 `buildThemeDetail`（含全部 `tableSchemas`：字段名 / 类型 / 含义 / 必填） | `THEME_TREE` / `themeDatabases` / `resourceThemeDistribution` | DirectoryTree；三栏并排；Export |
| 应用视窗 | 总览补 demo `RealtimeMonitor` 原文：QPS **8,520**、平均响应、成功率、2 条告警；资产基本情况筛选；主题排行；供应部门归集；需求/业务/使用筛选与明细 | `APP_MONITOR` 文案来自 demo；数来自 `resourceUsageStats` + dump；`assetRanking` / `supplierRegionGroups` / `businessApplicationCallLogs` / `callUserTracking` | 真推送；RangePicker；多 Sheet |
| 详情弹窗 | `buildOverviewSourceDetail` / `buildAccessSourceDetail` / `buildResourceDetail` / `buildCenterDetail` / `buildThemeDetail` / `buildAssetDetail` / `buildHistoryDetail` / `buildProblemDetail` / `buildSupplierDetail` / `buildDemanderDetail` / `buildBusinessDetail` / `buildUsageDetail` / `buildUserTrackDetail` / `buildLogDetail`，字段对齐 demo `Descriptions` | 全部读 dump，不手写新行 | 导出、批量勾选、日期 RangePicker 留 PC |

### 修改内容（科技数据资源第十三轮）

- 只改 `dataSamples.ts` + 四视窗 + `dataSamples.check.mjs`；`dataDump.ts` 不扩行、不加新 mock。
- 主题 KPI 改回 demo 原值；自造「均质」删除。
- 详情抽屉补齐 demo 字段（主题库表结构整表展开）。
- 导出 / 批量 / RangePicker 仍留 PC，未另做移动端套件。

### 科技数据资源 · 第十四轮（2026-09-01 · 接入视窗监管人反馈）

三处按 demo 改，不新造：

| 反馈 | as-built | 不做 |
|---|---|---|
| 环状图底部残留横坐标 | `pieOption` 显式 `xAxis/yAxis/grid.show=false`、图例沉底、`label.show=false`；数据四页 `VChart` 一律 `:update-options="{ notMerge: true }"`，避免 tab 切回时合并折线轴 | 不换图库 |
| 分区接入应对齐 demo | 「接入」Tab 对齐 `AccessDataResourceDetail`：标题「接入数据资源详情」；统计（分区接入总量 / 检索命中 / 优质≥90）；平均质量 gauge；主题结构饼；选中分区类型分布；按区域 / 按分库 / 按来源机构明细（含类型占比）；接入数量对比、类型堆叠；资源列表改用 **`themeDatabases`**（`filterPartitionResources`），点开走 `buildThemeDetail`；筛选主题 / 时间(2026-05\|04) / 来源 / 质量 | 不再用 `resourceAccessDetailList` 当分区清单 |
| 概览「接入渠道」「更新周期」demo 没有 | 概览只留 KPI + 完成度 142/23/8 + 归集数据量月周日趋势；`accessChannelStats` / `updateCycleStats` 仍在 dump，页面不再渲染 | 不把渠道/周期加回概览 |

### 修改内容（科技数据资源第十四轮）

- `PARTITION_MODES` 文案改为「按区域 / 按分库 / 按来源机构」。
- 新增 `filterPartitionResources` / `partitionOverview` / `partitionCountBar` / `partitionTypeStack` / `qualityGaugeOption` / `partitionTypePie` / `PARTITION_TYPE_KEYS`。
- 概览删除渠道列表与更新周期列表。

### 科技人才态势 · 第十五轮（2026-09-01 · 对照 demo 补交互与详情）

监管人要求：对照 `demo-ui-science/src/pages/talent-trend` 补人才四页遗漏，且**不能出现 demo 没有的功能和数据**。`talentDump.ts` 无 `recentWorks` / `collaborationNetwork` / `nlpFieldProfile` / `researchEvolution`，一律从 `relations` / `honors` / `fieldKeywords` / `similarScholars` 推导，不另造种子。

点地图 / 名单 / 卡片开 `ProfileDrawer`（默认半屏 62%）。画像网络节点详情**不弹窗**，固定在图谱底部。实现仍落 `src/views/talent/*.vue` + `talentSamples.ts`；`echarts.ts` 补 `MapChart` / `LinesChart` / `GeoComponent` / `VisualMapComponent`。中国面状图用仓内 `src/assets/geo/china.json`。

| 块 | 完成内容（as-built） | 数据真源（复刻，非自造） | 不做 / 缓 |
|---|---|---|---|
| 全球领域 · 分布/动态弹窗 | 分布：区域走 `buildRegionDetail`（学历/类型条、领域饼、院校、华人研究员占比）；机构走 `buildInstitutionDetail`。动态：城市聚合走 `buildCityActivityDetail`（实时动态详情），单条动态走 `buildActivityDetail`。地图点色区分机构 | dump `regions` / `institutions` / `activities` | 不混用同一套弹窗文案 |
| 全球领域 · 动态分页 | 地图/列表共用「加载更多」（`PAGE_SIZE`），适合小屏长列表；不另做页码条或上拉插件 | dump 16 条动态 | 时间轴自动播放 |
| 关注地区 · 中国 | ECharts `type: 'map'` 省级面状 + `lines` 迁徙；排行领域切换联动地图；排名/净流入用 table；点省开 `buildProvinceDetail`。人才分布迁徙：年芯片 + 原因饼 + 路线柱 + 净流表 | dump `provinces` / `chinaMigration`；`china.json` | **热力层已按监管人去掉**；Excel/Word |
| 关注地区 · 深圳 | 三级下钻：区 → 园区 → 主体；`lock-fit` + `hide-switch` + `hide-heat`；`flyTo` 定位。排名/流动 table；趋势折线多区 | dump `districts` / `trends` / `structure` / `flows` | 地图+列表切换；热力；园区热力下钻 |
| 画像 · 基础 | 简历卡（姓名/职称/单位/性别国籍出生年）+ 领域/技术标签 + 教育/工作时间轴 + 贡献条 | dump `education` / `workExperience` / `fieldLabels` / `techTags` | PDF / 导入 |
| 画像 · 关联 | 论文/专利/项目分组；高被引/重大项目/核心技术/NEW；二级 chip 筛选。弹窗对齐 demo：来源/年份/引用/关联人才/原文链接/技术标签/变更记录/隐含关系 | dump `relations.*`（含 `changeLog` / `latentLinks` / `sourceUrl`） | 列表/树/图谱/标签四视图工具栏（中屏） |
| 画像 · 分析 | 综合 gauge + 贡献雷达 + 五维条 + 领域柱 + 难度因子柱 + 成本构成柱 + 相似学者卡 | dump `contributionScore` / `academicInfluence` / `difficultyEstimate` / `costEstimate` / `similarScholars` | — |
| 画像 · 成果 | 按年时间轴；二级 chip：全部/论文/专利/项目/获奖；点击走同一套 `buildRelationDetail` | `flattenWorks` = `relations` + `honors`（dump 无 `recentWorks`，不造 award/event 种子） | 多级展开 / 分类聚合 / 缩放全屏 |
| 画像 · 网络 | ECharts force；点击节点**底部**「合作详情与溯源」：机构、关系类型、合作次数、领域、主题、路径强度、代表成果；相似学者可跳画像 | `buildCollabNetwork` 从合作者 + `similarScholars` 推导 | 节点弹窗；直播同步；算法推荐抖动；师承/技术转移伪节点 |
| 画像 · 领域 | 对齐 demo「领域研究图谱」：主要研究领域覆盖条、专业方向、技术标签、主题演化面积图、关键词云、关系图、团队合作匹配。点词开代表性论文/项目 | `deriveFieldProfile` 从 `fieldKeywords` / `fieldLabels` / `techTags` / 成果年份聚合 | 不写伪 NLP 置信度 / 机构需求卡（dump 无 `nlpFieldProfile`） |
| 画像 · 荣誉 | 卡片展示类别/级别/机构/年份/影响说明 | dump `honors` | **点击弹窗已按监管人去掉** |
| 画像 · 一级/二级 Tab | 一级七区改 `van-tabs`（`inline-tabs`，下划线+横滑）；关联/成果二级筛选仍为胶囊 chip | — | 七项不进底栏 `PageTabs` |
| 画像 · 变更记录 | 抽屉 `sections.timeline` 复用 `.step-list`（圆点+竖线，按日期升序） | `changeLog` | — |
| 引进评估 | 难度因子由三行 `gap-row` 改为双列 `factor-grid`；尽调推荐双列 `rec-card`，点开走 `buildDueDiligence`（含社会影响维） | dump `difficultyEstimate.factors` / `recommendations` | 成本滑条；xlsx |

### 修改内容（科技人才态势第十五轮）

- 全球：区域/机构/城市动态三套抽屉；动态「加载更多」。
- 中国：Leaflet 省点改为 ECharts 面状图 + 迁徙线；排行领域联动；监管人去掉热力。
- 深圳：三级下钻，关掉地图/列表切换与热力；排名与流动改 table。
- 画像：基础简历式；关联/成果详情对齐 demo；成果时间轴；网络底栏详情；领域块对齐研究图谱 Tab；荣誉去弹窗；一级 Tab 改 Vant Tabs。
- 引进：难度因子紧凑双列；尽调推荐卡 + 详情。
- `ProfileDrawer` 增 `bars` / `chart` / `people` / `list` / `timeline`。`CropMapStage` / `UnifiedLeafletMap` 增 `hideSwitch` / `hideHeat` / `lockFit` / `flyTo` / 点色。
- 断言：`scripts/talent-situation.test.mjs`。`talentDump.ts` 未扩行。

## 偏离说明

- 已删除第一版 `TrendBatchAView` 配置驱动模板；态势 8 页 + 人才 4 页 + 数据 4 页独立 vue。
- 科技指数第九轮对齐 PC 四 Tab，**评议只读展示**（名单 + 活跃度）；评议管理后台仍不下发。名单/排行点开半屏抽屉。对比可视化、对比篮、导出、实时刷新开关留 PC。
- **科技创新评估**：第二轮为四维雷达 + 自造「最近评估」。第六轮按监管人功能点改为 **结果 / 指标** 两底栏（结果查看 + 历史评估记录 / 指标体系预览 + 权重分布）；mock 对齐 `tech-innovation-evaluation-new`，不是旧页 `baseRecords`。监管人明确去掉「评估过程」。权重只读，跑批/地图/图谱/导出留 PC。
- **科学技术全景**：第二轮用列表/路径步骤代替图谱；第三轮按监管人要求改为 **ECharts 图谱 + 关键实体 + 详情**，数据对齐 demo 核心 mock。仍禁止 G6。路径叠加 21 节点与路径播放仍缓。
- **技术发展跟踪**：第二轮为话题热力 + 地图 + 工作流、无底 Tab。第四轮按监管人范围改为 **结果 / 参数 / 方法** 三底栏；去掉「跟踪」Tab 及热力/地图/工作流。参数只读，编辑与弦线图留 PC。
- **深圳创新监测**：第二轮为区级地图 + 领域读数 + 对标缺口、无底 Tab。第五轮按监管人对齐 PC 四 Tab；筛选 50% 半屏；**所有点选详情半屏 62%**（不再全屏）；区间对比补期初/期末/增量；指标不做报告导出；城市分析可看结论，Word 导出留 PC。
- **全球创新监测**：第二轮为类型芯片 + 地图 + 载体排行 + 预警卡、无底 Tab。第七轮按监管人对齐 PC 五 Tab；筛选用半屏 `FilterSheet`（70%）；详情全屏抽屉。订阅规则、权重编辑、知识图谱、监测模型配置留 PC。
- **湾区创新监测**：第二轮为城市芯片 + 地图 + 雷达 + SWOT 2×2、无底 Tab。第八轮按监管人对齐 PC 四 Tab；成果详情半屏抽屉（62%）；时间窗相对样本日 `2025-09-28`。飞线、报告/指标导出、常用星标、权重编辑留 PC。
- **科技指数**：第二轮为 hero + 指标树 + 地图 + 成果榜、无底 Tab。第九轮按监管人对齐 PC 四 Tab；可视化/排名筛选走半屏 `FilterSheet`（50%，底栏固定）；名单/排行半屏抽屉；指标树三级缩进色标。对比、导出、实时刷新留 PC。
- **科技发展规划**：第二轮为预警卡 + 本地 vs 全球折线、无底 Tab。第十轮按监管人对齐 PC 三 Tab；筛选半屏；详情半屏、生成报告全屏可下 Word。图谱用 ECharts 非 G6；土地效益标明示意数据；热点选中只留底色去边框。桑基/热力/四象限/PDF/AMap 留 PC。
- **科技人才态势**：并入本叶第十一轮，第十五轮按 demo 纠偏，不单开 `FE-DISPLAY-SMALL-TALENT`。相对 demo 中屏：无全球迁徙飞线、无播放器、无导入 PDF、无成本滑条。中国已用仓内 `china.json` 面状图但**无热力**（监管人去掉）。深圳三级下钻但不做地图+列表切换。画像七区改页内 `van-tabs`，不做 7 项底栏；网络详情在底部不弹窗；成果时间轴由 `relations`+`honors` 推导，不造 `recentWorks`。人才对象 20→8，动态 50→16。评估难度双列、尽调推荐卡。
- **科技数据资源**：并入本叶第十二轮，第十三/十四轮按 demo 纠偏。PC 长滚动/三栏拆成底栏；无导出、无批量复现、无 DirectoryTree。第十二轮自造主题 KPI（均质）已删，改回 `ThemeWindow` 六卡。应用区按 demo 复刻监控文案（QPS 8,520），不做真推送。接入概览不渲染 dump 里的渠道/更新周期（demo 概览没有）。分区清单用 `themeDatabases` 不对 `resourceAccessDetailList`。图谱 ECharts force 非 G6。
- 跟踪/全球/湾区/深圳/评估/指数/规划/人才/数据底 Tab 是本页功能分区，不是统一套版。
- 镜像 `readiness.generated.ts` 为空，不传 `metric_id`（备忘：没有 id 就不要传）。
- 本会话无浏览器 MCP；以 `node --test` + `vue-tsc` 为准。业务仓已 push `origin/dev` `699f280`。任务已转 `ready_to_sign`（待签收）。

## 产物清单

- `repos/lumen-ui-science-mobile/src/views/trend/TechPanoramaView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/panoramaSamples.ts`（第三轮新增；全景 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/TechDevelopmentTrackingView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/trackingSamples.ts`（第四轮新增；跟踪评估 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/GlobalInnovationMonitorView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/globalInnovationSamples.ts`（第七轮新增；全球监测 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/BayAreaInnovationMonitorView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/bayAreaInnovationSamples.ts`（第八轮新增；湾区监测 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/ShenzhenInnovationMonitorView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/shenzhenSamples.ts`（第五轮新增；深圳监测 mock 单真源）
- `repos/lumen-ui-science-mobile/src/components/FilterSheet.vue`（默认 `height: 70%`；深圳综合与科技指数可视化/排名可配 50%；`quick-filter__actions` 底栏固定）
- `repos/lumen-ui-science-mobile/src/components/QuickFilter.vue`（字段区 `quick-filter__fields` 可滚，操作区不滚）
- `repos/lumen-ui-science-mobile/src/views/trend/TechInnovationEvaluationView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/evaluationSamples.ts`（第六轮新增；评估 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/TechIndexView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/techIndexSamples.ts`（第九轮新增；科技指数 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/trend/TechDevelopmentPlanView.vue`
- `repos/lumen-ui-science-mobile/src/views/trend/planSamples.ts`（第十轮新增；规划 mock 单真源）
- `repos/lumen-ui-science-mobile/src/views/talent/GlobalTalentSituationView.vue`
- `repos/lumen-ui-science-mobile/src/views/talent/LocalTalentSituationView.vue`
- `repos/lumen-ui-science-mobile/src/views/talent/KeyTalentProfileView.vue`
- `repos/lumen-ui-science-mobile/src/views/talent/TalentIntroductionEvaluationView.vue`
- `repos/lumen-ui-science-mobile/src/views/talent/talentSamples.ts`
- `repos/lumen-ui-science-mobile/src/views/talent/talentDump.ts`（第十一轮；demo 种子 `20260821` 冻结；第十五轮未扩行）
- `repos/lumen-ui-science-mobile/src/assets/geo/china.json`（第十五轮；中国面状图）
- `repos/lumen-ui-science-mobile/scripts/talent-situation.test.mjs`（第十五轮：全球分窗/中国无热力/画像时间轴与 van-tabs）
- `repos/lumen-ui-science-mobile/src/views/data/DataOverviewView.vue`
- `repos/lumen-ui-science-mobile/src/views/data/DataAccessView.vue`
- `repos/lumen-ui-science-mobile/src/views/data/DataThemeView.vue`
- `repos/lumen-ui-science-mobile/src/views/data/DataApplicationView.vue`
- `repos/lumen-ui-science-mobile/src/views/data/dataSamples.ts`（第十三/十四轮：主题六卡、详情 builder、分区 helper、`pieOption` 去轴）
- `repos/lumen-ui-science-mobile/src/views/data/dataDump.ts`（第十二轮冻结 demo `mockData.js`；十三/十四轮未扩行）
- `repos/lumen-ui-science-mobile/src/views/data/dataSamples.check.mjs`（第十三轮：dump 口径断言）
- `repos/lumen-ui-science-mobile/src/components/ListCard.vue`（`plain`：无点击不去箭头）
- `repos/lumen-ui-science-mobile/src/views/trend/batchASamples.ts`（已删 `PANORAMA_*` / `EVAL_DIMS` / `WORLD_*` / `GBA_CITIES` / `GBA_SWOT` / `INDEX_*` / `PLAN_*` / `TREND_YEARS`，避免双真源；深圳页仍用 `GBA_CENTER`）
- `repos/lumen-ui-science-mobile/src/config/echarts.ts`（`GraphChart` + `RadarChart` + `GaugeChart` + `MapChart` + `LinesChart` + `Geo` + `VisualMap`；无 Heatmap）
- `repos/lumen-ui-science-mobile/src/assets/main.css`（`.heat-row.active` 留底去边；`.alert-grid--stack`；`.data-table`；`.tone-note`；`.work-timeline` / `.node-panel` / `.inline-tabs` / `.factor-grid` / `.rec-grid`）
- `repos/lumen-ui-science-mobile/src/components/ProfileDrawer.vue`（`sections.chips` / `bars` / `chart` / `people` / `list` / `timeline`→`.step-list`；趋势图 y 轴自适应）
- `repos/lumen-ui-science-mobile/src/components/map/CropMapStage.vue`（`hideSwitch` / `hideHeat` / `lockFit` / `flyTo` / `#extra`）
- `repos/lumen-ui-science-mobile/src/components/map/UnifiedLeafletMap.vue`（点色 / `lockFit` / `flyTo`）
- `src/router/index.ts`（`TREND_PAGES` 含 SPIKE + 态势 8 + 人才 4 + 数据 4）
- `scripts/breakpoints.test.mjs`（……；人才 4 页 + `data-table` / `tone-note`；数据 4 页 + 禁 xlsx/ExportButton/DirectoryTree/Slider）

## 验收证据（DoD）

| 条 | 结果 |
|---|---|
| 态势/指数类小屏 Mock 可翻 | ✅ 态势组 9 菜单 + 人才 4 页 + 数据 4 页均可进真页 |
| 核心 CTA 可达；不做中屏全功能 | ✅ 见上文表。无导出/批量复现/G6/滑条。底 Tab 另含数据统计四区 / 接入五区 / 主题三区 / 应用六区。数据第十三/十四轮补 demo 区块与详情，仍裁剪导出/批量/RangePicker |
| 对齐小屏壳断点与裁剪规则 | ✅ 仍只认 `PHONE_MAX_PX=767`；未改 `src/shell/` / `breakpoints.ts` |
| 主执行 human:孔东；ponytail lite | ✅ 任务登记仍 lite；全景第三轮至人才第十五轮按 full 交付 |

复刻五维：本叶是裁剪首页不是 Demo 1:1。R3 token `#D8E7FC`/`#165DFF`；R5 `USE_MOCK` 默认 false、无 fixture 填数。各模块实现功能以上表与分节 as-built 为准，交互按小屏抽屉裁剪。

## 测试结果

- `pnpm test`（`scripts/*.test.mjs`）：人才断言 3 passed（`talent-situation.test.mjs`：全球分窗+加载更多、中国无 heatmap、画像 van-tabs/时间轴/node-panel）。全量套件另有既有数据页断言失败（`资产排行` 文案，非本轮改动）
- `node src/views/data/dataSamples.check.mjs`：`dataSamples.check ok`（7 库 / 28 主题库 / 无「均质」）
- `pnpm type-check`：`vue-tsc --build` 通过（exit 0）
- 浏览器：本会话无浏览器 MCP。请本机 `pnpm dev` → `/talent/global-talent-situation|local-talent-situation|key-talent-profile|talent-introduction-evaluation`。第十五轮请点：全球分布/动态分窗与加载更多；中国面状图无热力；深圳三级下钻；画像一级 Tabs / 成果时间轴 / 网络底栏详情 / 关联变更记录时间轴；引进双列因子与推荐卡

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 1050000（in+out 估算；source: session_estimate；含第二轮至第十五轮人才对照） |
| model_used | `claude-sonnet-4.5`（registry 枚举按 B 档口径） |
| actual_cost | 5.67（frontend 默认 80/20 × B 档 $3/$15 per M） |
| cost_warn | green |

## 遗留风险

- 指标镜像仍空，评审开时无 ⓘ 8 件套（不传 id，避免伪闭合）
- 第十三至十五轮已入库 `lumen-ui-science-mobile` `699f280`；K8s 等 CI rollout
- 监管人需本机点选全景：图谱 roam、点节点过滤实体、抽屉关闭后名单仍按选中节点过滤
- 监管人需本机点选跟踪：结果 hero / 4 条历史 / 查看说明 / 5 套模板 / 4 种方法抽屉
- 监管人需本机点选深圳：综合筛选半屏、点选详情半屏 62%、指标下钻与对比、领域地图、城市对标
- 监管人需本机点选评估：`/trend/tech-innovation-evaluation` 结果 hero / 四大能力 / 4 条历史 / 指标 Tab 体系预览与权重说明；确认无「过程」底栏
- 监管人需本机点选全球：五底栏、类型芯片+地图、载体筛选、预警一行一条、城市雷达
- 监管人需本机点选湾区：四底栏、成果半屏筛选/地图列表联动、计算方法与子指标、SWOT 因素、指标口径与城市构成
- 监管人需本机点选指数：四底栏、三级指标树展开、可视化半屏筛选底栏固定（地图/专家/趋势/活跃度）、成果榜筛选、评议名单半屏
- 监管人需本机点选规划：三底栏、预警生成报告与 Word、热点 8 行选中留底去边、chip 对比最多 5、载体地图、研究重叠仪表与情报
- 监管人需本机点选人才：全球分布/动态分窗与加载更多；中国面状图+迁徙线（无热力）+ 排行领域联动；深圳三级下钻；画像一级 Vant Tabs、成果时间轴、网络底栏详情、关联变更记录时间轴、荣誉无弹窗；评估双列因子、尽调推荐卡与 Word
- 监管人需本机点选数据：总体四底栏（含多源/智能分类/质量雷达）；接入概览无渠道与更新周期、分区对齐 demo、环状图无残留横轴；主题六卡 28/1,248/10.2 亿；应用 QPS 8,520 与告警；点开主题库抽屉核表结构字段
- 路径叠加节点 / 路径播放仍缓，与 demo 中屏不完全同构
- 跟踪未做热力/气泡/弦线与参数编辑，与 demo 中屏不完全同构
- 评估未做跑批过程、地图、知识图谱与权重编辑，与 demo 中屏不完全同构。功能点以本叶第六轮表为准：做了结果查看 / 历史评估记录 / 指标体系预览 / 权重分布；评估过程明确不下发。
- 全球未做订阅规则 / 权重编辑 / 知识图谱 / 监测模型配置，与 demo 中屏不完全同构
- 湾区未做飞线 / 报告导出 / 指标导出 / 常用星标 / 权重编辑，与 demo 中屏不完全同构
- 指数未做综合对比可视化、排名对比篮、导出与实时刷新，与 demo 中屏不完全同构
- 规划未做人才桑基、重叠热力/四象限、AMap、PDF 打印；土地效益为示意数据；「生成报告」为本地 blob `.doc`，非服务端 Word。功能点以本叶第十轮表为准。
- 人才未做全球迁徙飞线 / 播放器 / 导入 PDF / 成本滑条；中国无热力；深圳无地图+列表切换；合作网络为 ECharts graph 非 G6。功能点以本叶第十五轮表为准（第十一轮骨架已纠偏）。
- 数据未做导出、批量复现、DirectoryTree、真 QPS 推送；图谱为 ECharts force。功能点以本叶第十三/十四轮表为准（第十二轮骨架已纠偏）。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`lumen-ui-science-mobile` `699f280`（第十三至十五轮）；前序 `d4f69da`（第十二轮）
- pipeline URL / ID：push 后看 GitLab CI
- 部署 namespace / 镜像 tag：CI 触发 K8s dev
- K8s rollout：待 pipeline
- dev 测试 URL / 命令与结果：`node --test scripts/talent-situation.test.mjs` 3 passed；`pnpm type-check` 通过；`node src/views/data/dataSamples.check.mjs` ok；本地 `pnpm dev` → `/talent/key-talent-profile`、`/data/data-overview` 等路径

## 可观测性

- 请求拦截器仍写 `X-Trace-Id` + `traceparent`（`src/utils/request.ts`）
- 本叶未加新埋点事件
- Tempo / Loki：无本叶新配置

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 未写算法 |
| 2 调用链 前端→Java→Python | ✅ 无越层 |
| 3 Nebula 禁止 Neo4j | ✅ 未碰图谱库；可视化用 ECharts |
| 4 可观测 | ✅ 保留 request 头 |
| 5 CI | ✅ 已 push `origin/dev` `699f280`；等 pipeline |
| 6 demo2 不 merge lumen | ✅ 对照 demo 重写，未 merge |
| 7 共享聚合 / 只调 Java | ✅ |
| 8 ADS / Mock 策略 | ✅ 页内预览样例，非 USE_MOCK fixture |
| 9 D8 Design | ✅ token / 主色 / 要素色；小屏骨架按页选用 |
| 10 D9 血缘 | ✅ 不传空镜像 id；不手改 generated |
| 11 D10 交互 | ✅ 抽屉只留关闭；数据/人才/湾区/深圳/指数/规划名单半屏 62%；筛选半屏。无 hover 依赖。数据底 Tab = 总体四区 / 接入五区 / 主题三区 / 应用六区 |
| 12 D12 禁 demo 服务 | ✅ 未改网关 |

## 涉及文件

- `lumen-ui-science-mobile/src/views/trend/Tech*View.vue`（8 页）
- `lumen-ui-science-mobile/src/views/trend/panoramaSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/trackingSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/globalInnovationSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/bayAreaInnovationSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/shenzhenSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/evaluationSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/techIndexSamples.ts`
- `lumen-ui-science-mobile/src/views/trend/planSamples.ts`
- `lumen-ui-science-mobile/src/views/talent/*.vue`（4 页）
- `lumen-ui-science-mobile/src/views/data/*.vue`（4 页）
- `lumen-ui-science-mobile/src/views/data/dataSamples.ts`
- `lumen-ui-science-mobile/src/views/data/dataDump.ts`
- `lumen-ui-science-mobile/src/views/data/dataSamples.check.mjs`
- `lumen-ui-science-mobile/src/views/talent/talentSamples.ts`
- `lumen-ui-science-mobile/src/views/talent/talentDump.ts`
- `lumen-ui-science-mobile/src/assets/geo/china.json`
- `lumen-ui-science-mobile/scripts/talent-situation.test.mjs`
- `lumen-ui-science-mobile/src/components/map/UnifiedLeafletMap.vue`
- `lumen-ui-science-mobile/src/components/ListCard.vue`
- `lumen-ui-science-mobile/src/views/trend/batchASamples.ts`
- `lumen-ui-science-mobile/src/config/echarts.ts`
- `lumen-ui-science-mobile/src/components/FilterSheet.vue`
- `lumen-ui-science-mobile/src/components/QuickFilter.vue`
- `lumen-ui-science-mobile/src/components/PageTabs.vue`
- `lumen-ui-science-mobile/src/components/ProfileDrawer.vue`
- `lumen-ui-science-mobile/src/components/map/CropMapStage.vue`
- `lumen-ui-science-mobile/src/assets/main.css`
- `lumen-ui-science-mobile/src/router/index.ts`
- `lumen-ui-science-mobile/scripts/breakpoints.test.mjs`
- `gkx-orchestration/agent-delivery/agent-handoffs/FE-DISPLAY-SMALL-BATCH-A.md`
