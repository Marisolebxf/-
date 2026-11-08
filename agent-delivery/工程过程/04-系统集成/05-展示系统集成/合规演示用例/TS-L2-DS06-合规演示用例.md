# TS-L2-DS06 深圳创新监测 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 深圳创新监测（前端目录 `lumen-ui-science-pc/src/views/situation/shenzhen-innovation`） |
| WBS | WBS-05-19 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/深圳创新监测.md`，序号 112–135（excel 行 115–138，leaf_count=24） |
| 覆盖行数 | 24 |
| 状态 | M2/M3 已填·2026-11-07 |
| 任务ID | DISPLAY-DEMO-CASE-TS-M1-L06 |

**主路径一句话**：进入深圳创新监测「创新载体」→ 按 8 区筛选（南山 17 / 福田 11 / 龙岗 11 / 光明 3 / 罗湖 3 / 宝安 2 / 盐田 2 / 坪山 1）→ 点深圳大学看详情与技术实力全国 rank=35 → 切「指标体系」看 2000–2026 共 27 期论文/被引/人才/机构/项目 5 指标 → 切「领域分布」看 15 个战新/未来产业集群构成 → 切「城市对标」勾选北京/上海看出 2020–2025 论文/被引/人才/机构/项目 5 项对比与逐年曲线。

> **数据情况证据口径（2026-11-07 M2/M3 实测）**：网关 `http://10.50.69.111:30895`（StripPrefix=1），带 `Authorization: Bearer <token>` + `systemCode: display`，工具 curl.exe、只读 POST。8 个后端端点全 200：`carriers` / `carriers/field-coverage` / `carriers/yearly` / `compare/city-yearly` / `city-benchmark` / `operation-timeline` / `field-distribution` / `indicator-systems`。证据 `.tmp/align-DS-06*.json` 共 8 份。
>
> **数据源**：久新 Doris `gkx_technology_analysis_dev`（`ads_institution_profile` 深圳 135 行 / `ads_institution_technology_power` 64,698 行 / `ads_institution_yearly_metrics` 2015–2026 / `ads_geo_yearly_metrics` / `ads_geo_yearly_discipline_metrics`），经 gkx_show_service 只读通道。
>
> **判定规则**：`可演` = 字段实测非空且来自真实库；`部分可演` = 主路径字段真实但 SRS 列举的部分维度/层级在 `noSourceFields`；`覆盖不到` = 后端无端点或整列在 `noSourceFields`。空值一律 NaN 显示「—」，禁止补 0。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 112 | 创新载体 · 多层级地理展示 | 层级：区级 / 街道级 / 产业园级 / 园区级 / 具体主体（高校 / 研究机构 / 企业 / 工作室）；深圳市各区县 | 点地图区域逐级下钻、缩放 | `POST /display/v1/situation/shenzhen-innovation/carriers` | 层级、区县编码、载体类型 | 每级呈现对应粒度载体点位，上级聚合数=下级点位数之和；无下级数据时提示「该区域暂无下级载体」 | **部分可演**（实测 total=50 载体，district 字段含 8 区真实分布：南山 17 / 福田 11 / 龙岗 11 / 光明 3 / 罗湖 3 / 宝安 2 / 盐田 2 / 坪山 1，区级聚合可演；`level` 全空、`street` 在 noSourceFields，街道级/产业园级/园区级下钻**覆盖不到**，按空态讲「该区域暂无下级载体」） |
| 113 | 创新载体 · 载体详情查看 | 地图载体标记点 | 点标记点 | `POST /display/v1/situation/shenzhen-innovation/carriers` | 载体 id | 展示载体基本介绍、创新成果、载体内部创新价值排名；缺失字段显示「—」 | **可演**（50 载体含 name/type/district/paperCount/citedByCount/talentCount/projectCount/establishedYear/collaboratorCount/fundingAmountCny 等真实字段；示例深圳大学 papers=21,482 cited=491,794 talent=3,318 南方科技大学 papers=17,213；`description`/`street` 无源显示「—」；经费注意 fundingRealCoverageRate 仅 1.3%–3.2%，须明示混合口径） |
| 114 | 创新载体 · 创新价值排名展示 | 排序方向（价值高→低 / 低→高）；载体类型 | 点表头排序 | `POST /display/v1/situation/shenzhen-innovation/carriers` | sortBy=innovValue、载体类型 | 排名连续且按价值单调；无价值分的载体排末位并标「未评分」 | **部分可演**（`value`/`rank` 在 noSourceFields，「创新价值」无源；但 `technologyPowerScore`/`technologyPowerRank` 真实存在，示例深圳大学 rank=35、南科大 rank=58、先进院 rank=181、港中文（深圳） rank=252、鹏城实验室 rank=603；按**技术实力排名**可演，按**创新价值排名**覆盖不到） |
| 115 | 创新载体 · 载体订阅功能 | 载体多选；推送频率 | 点「订阅」 | 待定（订阅端点见 SITUATION-IM-API-CONTRACT-01，路径待 M2 核对） | 载体 id、频率 | 订阅后载体显示「已订阅」，取消后标记消失 | **覆盖不到**（后端 ShenzhenInnovationController 8 个端点中无订阅端点；`isSubscribed`/`subscriptionState`/`pushStatus` 均在 noSourceFields；实测确认 grep 无 subscribe/analysis 路径，订阅功能未接入） |
| 116 | 创新载体 · 载体筛选与搜索 | 载体类型（高校 / 研究机构 / 企业 / 工作室）；创新领域（学科领域级联）；创新价值区间；关键词 | 选条件、输入关键词 | `POST /display/v1/situation/shenzhen-innovation/carriers` | 类型、领域、价值区间、keyword | 结果条数 ≤ 全量且每项符合条件；关键词无命中显示「未找到匹配载体」 | **部分可演**（type 实测 8 类真实分布：healthcare 17 / education 11 / facility 9 / company 9 / archive 1 / other 1 / government 1 / nonprofit 1，类型筛选可演；keyword 走 name 字段检索可演；**创新领域级联**`domain` 在 noSourceFields，**创新价值区间**`value` 在 noSourceFields，两个维度覆盖不到） |
| 117 | 创新载体 · 载体对比分析 | 载体多选（≥2） | 勾选后点「对比」 | `POST /display/v1/situation/shenzhen-innovation/carriers` | 载体 id 列表 | 对比表列=所选载体数，行含创新成果、创新价值、发展潜力；差异可辨识 | **可演**（50 载体可任选 ≥2 勾选；对比维度真实字段：paperCount/citedByCount/talentCount/projectCount/collaboratorCount/establishedYear/fundingAmountCny/technologyPowerScore/technologyPowerRank；发展潜力/创新价值无源字段显示「—」） |
| 118 | 指标体系 · 指标体系展示 | 指标层级（一级 / 二级 / 三级） | 展开层级、点指标 | `POST /display/v1/situation/shenzhen-innovation/indicator-systems` | 层级、指标 id | 层级树展开后可见下级指标；点指标显示定义、计算方法、数据来源 | **部分可演**（实测返回 cityCode=CN-4403 nameZh=深圳，baseIndicators 5 项：paperCount/citedByCount/projectCount/talentCount/institutionCount；`三级指标树`/`dimensions`/`unit`/`calcMethod`/`latestRank`/`yoy` 共 6 项在 noSourceFields → 只有扁平指标卡无层级树，定义/计算方法显示「—」，数据来源可显示 sourceTag=`jiuxin:ads_geo_yearly_metrics`） |
| 119 | 指标体系 · 多维度指标展示 | 维度：论文 / 期刊 / 专利 / 专家学者 / 会议 / 组织机构 / 课题 / 项目 / 资金 / 政策 / 基础设施 | 切维度 | `POST /display/v1/situation/shenzhen-innovation/indicator-systems` | 维度键、年份 | 切换维度后指标卡与图表随之变化；无源维度标注「该维度暂无数据」而非 0 | **部分可演**（实测仅 5 维度有数据：论文 paperCount、被引 citedByCount、项目 projectCount、人才 talentCount、机构 institutionCount；**期刊/专利/专家学者/会议/课题/资金/政策/基础设施** 8 个维度无源，按「该维度暂无数据」讲，禁止补 0） |
| 120 | 指标体系 · 指标数据可视化 | 图表类型（柱状图 / 折线图 / 饼图 / 雷达图） | 切图表类型 | 同上 | 图表类型、指标 | 图形随切换变化且数据点数量不变；雷达图维度数=所选指标数 | **可演**（5 个 baseIndicators 各有 27 期时序（2000–2026），periods 数组实测 27 项；切换柱/折/饼/雷达 4 类图形数据点数不变） |
| 121 | 指标体系 · 指标时间趋势分析 | 时间范围（近 3 年 / 近 5 年 / 自定义起止年）；指标 | 选时间范围 | `POST /display/v1/situation/shenzhen-innovation/carriers/yearly` | 指标、起始年-结束年 | 折线横轴年份=所选范围；缺年数据断开而非补 0；无数据段提示「该年无数据」 | **可演**（实测深圳大学 2020–2025 共 6 年序列：papers 1487/1763/2164/2739/3907/5481，cited 67129/71684/59360/51378/19487，talent 492/577/680/819/1056/1336；**caveat**：被引为「当年发布论文截至统计日累计被引」末年偏低，`patentCoverageLastYear=2022`（2023 起 patent_count 恒为 0 是覆盖滞后非产出归零），`projectCountAvailable=false` 年度表无项目数；缺年按断开讲） |
| 122 | 指标体系 · 指标对比分析 | 指标多选（≥2）或多时间段（≥2） | 勾选后点「对比」 | 同上 `POST /display/v1/situation/shenzhen-innovation/carriers/yearly` | 指标列表、时间段列表 | 对比行=指标数或时间段数；差异列直接给出数值差 | **可演**（5 指标间可勾选 ≥2 对比，论文/被引/人才 3 指标 2020–2025 序列齐全；项目数无源按空态讲） |
| 123 | 指标体系 · 指标详情查看 | 具体指标 | 点指标卡 | `POST /display/v1/situation/shenzhen-innovation/indicator-systems` | 指标 id | 展示详细数据、计算方法、数据来源、分析解读；无解读时显示「暂无解读」 | **部分可演**（详细数值与 27 期趋势真实；`calcMethod`/`unit`/`yoy` 在 noSourceFields → 计算方法/单位/同比显示「—」，分析解读无源显示「暂无解读」，数据来源可显示 sourceTag） |
| 124 | 领域分布 · 热力图展示 | 科技领域（全部 / 单一领域）；热力口径（密度） | 选领域、缩放地图 | `POST /display/v1/situation/shenzhen-innovation/field-distribution` | 领域 id、年份 | 热力图出现色阶图例，热点区随所选领域变化；全空时显示「该领域暂无分布数据」 | **部分可演**（实测 15 产业集群：新一代信息技术 papers=6,070 / 生物产业 5,041 / 新材料 5,746 / 未来健康 7,007 / 未来信息 5,403 等，含未归类 30,680 篇 39.47%，集群覆盖率 47,049/77,729 = 60.53%；**clusterPoints/leadDistrict 在 noSourceFields → 无地理点位，热力图不可演**，只能演集群构成柱/饼图） |
| 125 | 领域分布 · 领域筛选功能 | 领域类型：信息技术 / 生物医药 / 新材料 / 新能源（以页面领域树为准） | 点领域筛选 | 同上 | 领域 id | 切换领域后热力图实时更新，图例与领域名一致 | **可演**（15 集群 id/name/groupName 真实：战新 8 项 + 未来 7 项，period=2020-2025；切换集群后 paperCount/citedByCount/percent/topicCount 联动更新可演） |
| 126 | 领域分布 · 空间分布分析 | 领域；分析维度（分布范围 / 中心位置 / 扩散方向） | 点「空间分析」 | `POST /display/v1/situation/shenzhen-innovation/carriers/field-coverage` | 领域 id、维度 | 展示分布范围、中心位置、扩散方向结论；无结论时明示未提供 | **覆盖不到**（field-coverage 是**诊断探针**非业务空间分析，返回 profile/power/yearly 三表的列填充自检，不含分布范围/中心位置/扩散方向；`clusterPoints`/`leadDistrict` 在 noSourceFields，空间分布分析能力未接入） |
| 127 | 领域分布 · 详细数据指标展示 | 领域；指标（企业数量 / 专利数量 / 研发投入 / 人才数量） | 选指标 | `POST /display/v1/situation/shenzhen-innovation/field-distribution` | 领域 id、指标键 | 展示各领域该指标数值；无源指标显示「无数据」 | **部分可演**（实测有源指标：topicCount（命中 Topic 数）/ paperCount / citedByCount / percent；**企业数量 enterprises / 专利数量 patents / 研发投入 rdInvestment / 人才数量 talents 4 项全部在 noSourceFields** → 按「无数据」讲） |
| 128 | 领域分布 · 分析与建议 | 领域 | 点「分析建议」 | 待定（建议生成依赖模型，可能 501） | 领域 id、年份 | 输出优势领域 / 潜力领域 / 薄弱环节与该领域建议；模型不可用时提示「分析建议未接入」，禁止模板化伪结论 | **覆盖不到**（后端 ShenzhenInnovationController 无 analysis/advice 端点，grep 零命中；前端无对应按钮接线；按「分析建议未接入」讲，禁止伪结论） |
| 129 | 城市对标 · 城市选择功能 | 国内主要城市 / 国际创新城市（以页面城市列表为准）；城市搜索词 | 选城市、搜索城市 | `POST /display/v1/situation/shenzhen-innovation/city-benchmark` | 城市编码列表 | 选中城市进入对标集合，最多可选数以页面限制为准；搜索无命中显示「未找到城市」 | **可演**（实测 total=20 城市全部国内：北京/上海/南京/广州/武汉/杭州/西安/成都/深圳/天津等，country=CN；国际创新城市覆盖不到，仅国内主要城市可演） |
| 130 | 城市对标 · 科技发展指标对比 | 指标：研发投入 / 专利数量 / 高新技术企业数量 / 创新人才；年份 | 选指标 | 同上 | 城市列表、指标、年份 | 对比表基城=深圳，列=所选城市；指标数值缺失显示「—」，不补 0 | **部分可演**（实测有源指标 5 项：paperCount/citedByCount/talentCount/institutionCount/projectCount，示例北京 papers=119,285 cited=1,226,158 talent=31,041；**研发投入/专利数量/高新技术企业数量 3 项在 SRS 列举但后端未明确分发，indicators 字段在 noSourceFields** → 按 5 项真实计数对比可演，研发投入等无源指标显示「—」） |
| 131 | 城市对标 · 城市排名展示 | 指标；排名范围（全国 / 全球） | 点「查看排名」 | `POST /display/v1/situation/shenzhen-innovation/city-benchmark` | 指标、排名范围 | 展示深圳在该指标的排名位次与参评城市数（如「第 N 位 / 共 M 城」）；无名次时显示「未排名」 | **覆盖不到**（`score`/`rank` 在 noSourceFields，后端不返回城市排名；按「未排名」讲） |
| 132 | 城市对标 · 竞争力分析 | 对标城市集合；分析年度 | 点「竞争力分析」 | 待定（分析模型端点未在接口清单确认） | 城市列表、年份 | 输出优势领域、薄弱环节、发展潜力；不可用时明确提示未接入 | **覆盖不到**（后端无 competitiveness/analysis 端点；按「竞争力分析未接入」讲） |
| 133 | 城市对标 · 发展建议提供 | 对标城市集合；建议类型（政策 / 资源配置 / 重点方向） | 点「生成建议」 | 待定（同上） | 城市列表、建议类型 | 生成对应类型建议条目；无生成能力时明示，不得输出通用套话冒充 | **覆盖不到**（后端无 advice/suggestion 端点；按「发展建议未接入」讲，禁止套话） |
| 134 | 城市对标 · 趋势分析 | 指标；时间范围；预测开关（待 M2 确认是否提供） | 切时间范围、开预测 | `POST /display/v1/situation/shenzhen-innovation/compare/city-yearly` | 城市列表、指标、年份范围 | 展示深圳与对标城市历史轨迹，年份轴一致；预测段须有明确标注，无预测能力时不得画延伸虚线 | **可演（历史段）**（实测 3 城 × 2020–2025 = 18 点，5 指标齐全：示例深圳 2024 papers=17,596 cited=227,434 talent=4,922，2025 papers=24,904 cited=83,374 talent=6,462；北京/上海同年数据可对比；**预测段**：`外推预测` 在 city-benchmark noSourceFields，无预测端点 → 预测开关不可演，只画历史折线，不画延伸虚线） |
| 135 | 城市对标 · 报告生成与导出 | 报告格式（PDF / Word）；对标城市集合 | 点「生成报告」并下载 | `POST /display/v1/situation/report/generate`、`GET /display/v1/situation/report/{reportId}/download` | reportType=shenzhen-innovation、conditionKey、format | 生成成功后触发下载；报告含对比结果、排名、竞争力分析与建议章节；同条件重复生成提示复用 | **部分可演**（端点在线：HTTP 200；实测当前条件返回业务失败 `{"code":1,"msg":"报告生成失败：报告内容为空"}` → 报告链路可调但当前数据条件下无内容；按「报告生成功能在线但当前条件无内容」讲，不演示成功下载） |

## 备注与风险

- **模块目录缺 `FE-TS-06A.md`**：WBS 已注明「模块目录无同名 FE-TS-06A.md」，本页实现口径只能从 WBS 摘要与前端代码反推；序号 118–135 的页面归属需 M2 对照实际 Tab 校正。
- **分析/建议类（128、132、133）后端无端点**：grep `shenzhen-innovation/subscribe|analysis|advice|forecast` 在 lumen-svc-platform 零命中，确认未接入，按「未接入」口径讲，不建子任务（属需求未排期，非缺陷）。
- **趋势预测（134）**：`外推预测` 在 city-benchmark noSourceFields，前端无预测开关接线，只演历史段。
- **订阅（115）**：`isSubscribed`/`subscriptionState`/`pushStatus` 均在 noSourceFields，订阅服务整体未接入。
- **载体五级下钻（112）**：`level`/`street` 在 noSourceFields，只有区一级 district 真实；下钻到街道/产业园/园区/主体按空态讲，不合并层级冒充完整。
- **热力图（124）/空间分布（126）**：`clusterPoints`/`leadDistrict` 在 noSourceFields，无地理点位数据，热力图形态不可演，只能演集群构成（柱/饼）。
- **报告链路**：`/display/v1/situation/report/*` 端点在线但当前条件返回「报告内容为空」业务失败；同条件命中会复用旧报告。
- **operation-timeline**：实测返回 `total=0, list=[]`，emptyReason 明确「久新无创新事件流对应能力；原 innov 通道数据源为 benchmark_manual_pack（演示基准包），按『不展示假数据』已停用」→ 后端已诚实置空，前端不渲染，本用例未列入 24 行（SRS 也未要求）。
- **经费字段**：`fundingAmountCny` 全额 = 真实 + 模拟混合，`fundingRealCoverageRate` 实测仅 1.3%–3.2%，演示时必须明示混合口径（参照「诚实三条」）。

## M3 判定摘要（2026-11-07）

| 判定 | 行数 | 序号 |
|---|---|---|
| 可演 | 8 | 113, 117, 120, 121, 122, 125, 129, 134 |
| 部分可演 | 10 | 112, 114, 116, 118, 119, 123, 124, 127, 130, 135 |
| 覆盖不到 | 6 | 115, 126, 128, 131, 132, 133 |

> 主路径（载体列表→详情→指标→领域→对标）全程可演；6 行覆盖不到的全部按「未接入/未排名/无数据」空态口径讲，不建子任务（属需求未排期或数据无源，非实现缺陷）。
