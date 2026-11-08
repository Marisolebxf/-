# TS-L2-DS07 科技创新评估 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 科技创新评估（前端目录 `lumen-ui-science-pc/src/views/situation/innovation-evaluation`） |
| WBS | WBS-05-20 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技创新评估.md`，序号 136–158（excel 行 139–161，leaf_count=23） |
| 覆盖行数 | 23 |
| 状态 | M3 复跑重填（2026-11-09）· G7 修复后 17 可演 / 1 部分可演 / 5 覆盖不到 · G1 算法库路由已恢复、G7 趋势预测已透出；剩余 G2–G5 为数据源/模型缺口 |
| 任务ID | DISPLAY-DEMO-CASE-TS-M1-L07 |

**主路径一句话**：进入科技创新评估 → 选评估对象与年份 → 看「科学创造力 / 技术创新力 / 产业发展潜力 / 政策与条件保障力」四组指标 → 点指标卡看定义与数据来源。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 136 | 科学创造力 · 科学论文数量分析 | 领域（学科领域级联）；时间粒度（年 / 季度 / 月）；研究机构；地域（大湾区 11 城 / 深圳市各区县）；图表类型（柱状图 / 折线图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间粒度、机构、地域 | 图表出现且数据点数量与所选时间粒度一致；切柱/折线不改变数值；无数据时显示「该维度暂无论文数据」 | ✅可演。snapshot science 维「论文数量」=68.5（gkx dwd_zh_paper 100,900 篇真实计量）；indicatorIntro.sources 确认数据源；算法库 `M_INNOV_DS_07_SCI_CREATE_004` 直连 200，support_judgment=完全转换支持 |
| 137 | 科学创造力 · 科学网络中心性评估 | 指标（度中心性 / 接近中心性 / 中介中心性）；对象（学者 / 研究机构） | 切指标、点网络节点 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标类型、对象类型、领域 | 出现合作网络图谱与中心性排名表；排名条数=接口返回；无网络数据时显示「暂无合作网络数据」 | ✅可演。snapshot science 维「网络中心性」=57.5（合作网络中心性三维等权合成）；中心性分值在科学维 payload 内，链路通 |
| 138 | 科学创造力 · 科学研究前沿性分析 | 领域；时间范围；前沿主题 | 点前沿主题 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间范围 | 展示前沿主题的时间演变与空间分布；主题条数=接口返回；无结果时提示「未识别到研究前沿」 | ✅可演。snapshot science 维「研究前沿」=68.9（前沿论文占比 min-max 归一）；indicatorIntro.method 确认文献计量+前沿占比算法 |
| 139 | 科学创造力 · 科学创造力趋势预测 | 领域；预测年限 | 点「预测」 | `POST /display/v1/situation/innovation-evaluation/snapshot` + 算法库 `M_INNOV_DS_07_SCI_CREATE_004` | 领域、历史区间、预测年限 | 出预测曲线与置信区间；模型不可用时显示「预测模型未接入」，不画无置信区的假预测线 | ✅可演。snapshot 新增 `sciForecast.domains`（3 领域：医学临床/新材料/电力能源），每域含 series（2015-2026 年序列，composite 0-1）、forecast（Holt 点预测 2024E/2025E）、lo80/hi80（80% 置信区间）；前端 `buildSciForecastOption` 渲染历史实线+预测虚线+CI 区域带，composite 缩放至 0-100；G7 已修复 |
| 140 | 技术创新力 · 专利数量统计分析 | 领域；时间范围（年 / 季度 / 月）；技术类别；地域；申请人；图表类型（柱状图 / 折线图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间粒度、技术类别、地域、申请人 | 专利数量随维度变化，申请量与授权量分列可辨；无数据时显示「该条件暂无专利数据」 | ✅可演。snapshot `techPatent.composite` 200 个 IPC4 技术领域真实数据（patent_count 如 A61K=226,626、C12N=127,804），data_source=jiuxin ads_patent_profile，data_source=real |
| 141 | 技术创新力 · 专利质量评估 | 质量指标（被引次数 / 权利要求数量 / 家族规模）；排序 | 切指标、点排序 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 质量指标、领域 | 展示质量指标分布与排名，识别高质量专利；指标缺失显示「未评估」 | ⚠️部分可演。snapshot `techPatent.quality` 200 领域含四维（家族规模/被引次数/技术宽度/法律状态授权率），rank_top 200 条真实；missing_dimensions=权利要求数（久新无 claims 字段），该单项显示「未评估」 |
| 142 | 技术创新力 · 技术市场潜力分析 | 指标（市场活跃度 / 技术成熟度 / 商业化前景）；领域 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、指标 | 展示对应指标数值与解读；数据源缺位时明示「无市场活动数据」 | ❌覆盖不到。`techPatent.composite` market_score=null，missing_dimensions=市场潜力（转让/许可/质押/诉讼，久新 ads_patent_profile 无 IPC4 归属字段）；G2 数据缺口，链路通但整维缺测 |
| 143 | 技术创新力 · 技术创新力综合评估 | 指标权重（可自定义，各项权重合计 100%） | 调权重后点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、领域 | 权重和不为 100% 时提示校验错误；计算成功后显示综合得分与分项贡献 | ✅可演。snapshot `techPatent.composite` 200 领域含 composite_score（如 A61K=100.0），weights_used={size:0.5, quality:0.5, market:0.0}；snapshot technology 维「综合评估」=15.9；自定义权重前端可调，后端按 size+quality 等权计算 |
| 144 | 技术创新力 · 技术创新空间分布 | 地域层级（大湾区 / 深圳市 / 区县）；展示形式（热力图 / 区域排名） | 切形式、缩放地图 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 地域层级、领域 | 热力图或排名表随层级变化；无数据区域不着色并标「无数据」 | ✅可演。snapshot `spatialByDimension` 四维（industry/policy/science/technology）全有数据；`spatialRegions`/`spatialRows` 各 100 城真实（含经纬度+论文/被引/人才/项目计数+评分），城市级热力/区域排名可演 |
| 145 | 技术创新力 · 技术创新趋势预测 | 领域；预测年限 | 点「预测」 | `POST /display/v1/situation/innovation-evaluation/snapshot` + 算法库 `M_TECH_DS_07_TECH_INNOV_006` | 领域、历史区间 | 出预测结果与置信区间；不可用时明示未接入 | ✅可演。snapshot `techPatent.forecast` 200 领域含 forecast_top、forecast_years=2、window=2015-2026、trend_direction、cagr_3y_pct；前端 `buildForecastOption` 渲染专利申请量历史+预测曲线；维度 metric「趋势预测」delta/trend 取自 forecast_top 趋势；G7 已修复 |
| 146 | 产业发展潜力 · 产业投入分析 | 维度（企业规模 / 地域 / 时间范围）；投入类型（研发投入 / 固定资产投资 / 人才投入）；图表（饼图 / 柱状图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 维度、地域、时间范围 | 投入结构与变化趋势可辨，饼图分项占比合计 100%；无数据时显示空态 | ✅可演。snapshot industry 维「产业投入」=50.0（48 国民经济行业真实计量，投入维=研发强度/载体密度百分位）；indicatorIntro.sources 确认 gkx dwd_org_income_statement 等 |
| 147 | 产业发展潜力 · 技术产品成熟度评估 | 产业；分析对象（技术 / 产品） | 点「成熟度分析」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 产业 id | 展示技术成熟度曲线或市场渗透率变化；无数据时提示「暂无成熟度数据」 | ✅可演。snapshot industry 维「产品成熟度」=50.0（成熟度维=授权率/发明占比百分位）；算法库 `M_INNOV_POT_COMPOSITE` 直连 200 |
| 148 | 产业发展潜力 · 产业产值分析 | 维度（时间范围 / 地域 / 企业类型）；产值口径（总产值 / 增加值 / 利润） | 选维度 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 维度、口径、年份 | 柱/折线展示产值变化，数值单位与口径一致；无数据时显示「暂无产值数据」 | ✅可演。snapshot industry 维「产业产值」=50.0（产值维=主营收入/净利润百分位）；48 行业真实计量 |
| 149 | 产业发展潜力 · 科学影响力评估 | 指标（论文被引次数 / 国际合作论文比例）；产业 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标、产业 id | 展示指标分布与排名；无被引数据时显示「未评估」 | ❌覆盖不到。snapshot industry 维「科学影响力」=N/A；indicatorIntro 明确「科学/技术影响力覆盖不足整维缺测」，缺测维不补 0、按可得维重归一；G3 数据缺口 |
| 150 | 产业发展潜力 · 技术影响力评估 | 指标（专利被引次数 / 标准必要专利数量）；产业 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标、产业 id | 展示指标分布与排名；无数据时明示 | ❌覆盖不到。snapshot industry 维「技术影响力」=N/A；同 G3，48 行业技术影响力覆盖不足整维缺测，标准必要专利无源 |
| 151 | 产业发展潜力 · 产业发展潜力综合评估 | 指标权重（可自定义，合计 100%）；产业 | 调权重、点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、产业 id | 权重校验同序号 143；成功后出综合得分与排名，排名条数=参评产业数 | ✅可演。snapshot industry 维「综合评估」=50.0（投入/成熟度/产值三维百分位加权合成，科学/技术影响力缺测不补 0）；48 行业真实计量，可出排名 |
| 152 | 政策与条件保障力 · 发展战略引导力评估 | 领域；战略/政策文件范围（时间范围） | 点「评估」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间范围 | 展示战略规划关键内容、实施路径、预期目标与引导力评价；无数据时明示未接入 | ✅可演。snapshot policy 维「战略引导力」=50.1（引导力=规划类政策占比）；data_source=gkx dwd_policy_base（20,000 件抽样），四城 panel 真实计量 |
| 153 | 政策与条件保障力 · 政策扶持力度分析 | 政策类型（财税政策 / 人才政策 / 金融政策）；时间范围；地域 | 选类型、时间、地域 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 政策类型、时间范围、地域 | 展示政策数量、类型、覆盖面分布；无数据时显示「该条件暂无政策」 | ✅可演。snapshot policy 维「政策扶持力度」=64.3（扶持力度=类型覆盖/政策件数）；gkx dwd_policy_base 真实 |
| 154 | 政策与条件保障力 · 经费支持分析 | 经费来源；支持方向；时间范围；图表（饼图 / 柱状图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 来源、方向、时间范围 | 展示经费结构与趋势，分项合计 100%；缺源时明示 | ✅可演。snapshot policy 维「经费支持」=89.4（经费=产业基金数）；data_source=gkx dwd_industrial_fund_basic_info（产业基金注册地）真实 |
| 155 | 政策与条件保障力 · 项目支持分析 | 项目类型；资助机构；时间范围 | 选维度 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 项目类型、机构、时间范围 | 展示项目数量、资助金额、实施效果；金额无源时显示「—」 | ❌覆盖不到。snapshot policy 维「项目支持」=N/A；indicatorIntro 明确「项目（缺测）」，funded_province/funded_institution 全空；G4 数据缺口 |
| 156 | 政策与条件保障力 · 政策实施效果评估 | 政策对象；对比时点（政策前 / 政策后）；关键指标 | 选政策与对比时点 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 政策 id、对比时点、指标 | 展示前后关键指标对比与差值；无法归因时须标注「仅相关不构成因果」 | ✅可演。snapshot policy 维「实施效果」=100.0（效果=论文近三年 vs 前五年增幅）；gkx dwd_zh_paper 真实；页面口径为论文增幅代理，须保留「仅相关不构成因果」标注 |
| 157 | 政策与条件保障力 · 政策与条件保障力综合评估 | 指标权重（可自定义，合计 100%）；领域 | 调权重、点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、领域 | 权重校验同序号 143；成功后出综合得分与排名 | ✅可演。snapshot policy 维「综合评估」=63.4（引导力/扶持力度/经费/效果四维加权，项目维缺测不补 0）；四城 panel 真实，深圳视角取深圳市分值 |
| 158 | 政策与条件保障力 · 政策优化建议 | 评估对象；建议方面（政策重点调整 / 支持力度 / 实施路径） | 点「生成建议」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 评估对象、建议方面 | 生成对应建议条目；模型不可用时明确提示未接入，不得用模板套话代替；德尔菲法/系统仿真能力未接入须如实说明 | ❌覆盖不到。snapshot `policySuggestions=[]`、`methodEvidence`（delphi/simulation）空结构（disagreement/conclusion/consensus/optimistic/conservative/scenario/baseline 全空）；无建议生成模型、无专家评议与模拟数据源（缺口 G5） |

## LOOP 对照汇总

> 部署冒烟口径：网关 `http://10.50.69.111:30895`（StripPrefix=1），Headers `Authorization: Bearer <token>` + `systemCode: display`。算法库直连口径：算法调试台 NodePort `http://10.50.69.111:30894/api/innov/**`（nginx 自动加 `X-Apiview-Direct: 1` 直通 `gkxlumen-platform-innov-py:8000`）。

| 判定 | 条数 | 序号 |
|---|---|---|
| ✅ 可演 | 17 | 136, 137, 138, 139, 140, 143, 144, 145, 146, 147, 148, 151, 152, 153, 154, 156, 157 |
| ⚠️ 部分可演 | 1 | 141 |
| ❌ 覆盖不到 | 5 | 142, 149, 150, 155, 158 |

实测接口清单（2026-11-09 复跑）：

| 接口 | 结果 |
|---|---|
| `POST /display/v1/situation/innovation-evaluation/meta` | 200，code=0。`regionOptions` 100 城真实（久新 ads_location）；`timeRangeOptions` 3 段真实（近3年/近5年/全区间）；`defaultWeights` 仍为 0 值空结构（无评估模型）；**新增 `dataSourceNote` 字段**：逐维说明数据源（科学=gkx dwd_zh_paper 100,900 篇；技术=久新 ads_patent_profile；产业=gkx 48 行业；政策=gkx 四城 panel），并标注各维缺测项与权重等权代理说明 |
| `POST /display/v1/situation/innovation-evaluation/snapshot` | 200，code=0，`empty=false`。**`dimensions` 四维全有数据**：science(score=36.6, 4 metrics) / technology(score=19.6, 5 metrics) / industry(score=50.0, 6 metrics) / policy(score=63.4, 6 metrics)；`spatialRegions`/`spatialRows` 各 100 城真实；`techPatent` 三键（composite/quality/forecast）各 200 IPC4 领域真实数据；**`sciForecast.domains`** 3 领域（医学临床/新材料/电力能源）含 series+forecast+lo80/hi80（G7）；`spatialByDimension` 四维全有；`methodEvidence`（delphi/simulation）空结构；`policySuggestions=[]`；`evidence.baseFactor=null`、dimensionOffsets 全 null；`updatedAt=2026-11-08T22:00:54` |
| 算法库 `POST /api/innov/v1/innov/metric/{id}/compute`（30894 直连） | **全部 200**：M_INNOV_DS_07_SCI_CREATE_004 / M_TECH_DS_07_TECH_INNOV_002 / _004 / _006 / M_INNOV_POT_COMPOSITE / M_INNOV_PG_COMPOSITE 均返回真实数据；`GET /api/innov/v1/innov/metrics` 200 列出指标清单；G1 路由缺口已解决 |
| 对照：`POST /display/v1/situation/global-innovation/innov-value`（DS04） | 200，`empty=false`（无 emptyReason）；算法链路全局恢复，非本页独有 |

根因定性（更新）：G1、G7 已解决——G1 生产镜像 `gkxlumen-innov-py` 已挂 `/v1/innov/metric/{id}/compute` 路由，四维评分链路通；G7 后端 `InnovationEvaluationController` 新增 `sciForecast` 透出科学创造力预测曲线+80% CI，`techPatent.forecast` 技术趋势数据已在快照内，前端路由修正。剩余 G2–G5 为数据源/模型缺口：G2 久新无专利转让/许可/质押/诉讼 IPC4 归属字段；G3 48 行业科学/技术影响力覆盖不足；G4 政策项目维 funded_province/funded_institution 全空；G5 政策建议与德尔菲/系统仿真无模型与数据源。

## 缺口建单

| 缺口 | 影响序号 | 处置建议 |
|---|---|---|
| ~~G1 算法库指标路由未上生产~~ **已解决** | — | 路由 `/api/innov/v1/innov/metric/{id}/compute` 已上线，6 个 DS-07 指标全部 200；四维评分链路通 |
| G2 技术市场潜力数据源缺失：久新 `ads_patent_profile` 无转让/许可/质押/诉讼 IPC4 归属字段 | 142 | 数据补源；未补前即使链路通该维仍整维缺测（market_score=null） |
| G3 产业科学/技术影响力覆盖不足：48 行业两维覆盖不足整维缺测（missing_dims） | 149, 150 | 数据补源；恢复链路后仍缺（科学影响力/技术影响力=N/A） |
| G4 政策项目维无源：funded_province / funded_institution 全空 | 155 | 数据补源；项目维整维缺测（项目支持=N/A） |
| G5 政策建议与方法论模型无源：`policySuggestions=[]`、`methodEvidence`（德尔菲共识/情景模拟）空结构，无评估模型与专家评议数据源 | 158 | 模型接入；未接前页面须如实「未接入」，不得模板套话 |
| G6 历史报告 0 条：report 表 report_type=innovation-evaluation 无记录 | 页面「历史报告」抽屉（无独立 case 行） | 依赖跑通一次完整评估落库生成 |
| ~~G7 趋势预测分值未在快照维度层透出~~ **已解决** | — | 后端 `InnovationEvaluationController` 新增 `sciForecast` 字段（科学创造力 3 领域 Holt 点预测+80% CI），`techPatent.forecast` 200 领域趋势数据已在快照内；前端 `getDetailPanelOption` 科学维走 `buildSciForecastOption(sciForecast)`、技术维走 `buildForecastOption(techPatent.forecast)`；139/145 均升为 ✅可演 |

## 备注与风险

- **G1、G7 已解决，演示覆盖率从 0/23 提升至 17/23 可演**：四维评分链路通，科学/技术/产业/政策各有真实分值与指标卡；趋势预测（139 科学创造力、145 技术创新力）曲线+置信区间已透出。现场讲解以四维综合评估卡 + 可演 17 项为主线。
- **5 项覆盖不到为数据源/模型缺口（G2–G5）**：142 市场潜力、149/150 产业影响力、155 项目支持、158 政策建议——均为缺源/缺模型，非链路问题。现场须如实说明「数据源未接入」，不得前端补算。
- **1 项部分可演**：141 专利质量（4/5 维可演，权利要求数缺测）。
- **评估对象范围未定**：SRS 未给「评估对象」枚举（领域/产业/区域/机构何者为主），页面选择项无法列全集，M2 前需产品补齐。
- **权重为等权代理**：四维 indicatorIntro 均注明「权重等权代理（甲方签认前不作正式口径）」，`defaultWeights` 为 0 值空结构。演示时须说明权重为临时等权，正式口径待甲方签认。
- **预测与建议类（139、145、158）**：139/145 趋势预测已可演（G7 修复，sciForecast + techPatent.forecast 透出）；158 建议生成模型未接入，须按不可用讲。
- **序号 158 附加的德尔菲法/系统仿真**：SRS 明确要求，`methodEvidence` 空结构，须在演示口径中列为「未提供」。
- **四组指标与页面 Tab 的对应关系**：本文件按 SRS 四个分组归位（科学创造力 / 技术创新力 / 产业发展潜力 / 政策与条件保障力），与 snapshot dimensions 的 key（science/technology/industry/policy）一一对应。
