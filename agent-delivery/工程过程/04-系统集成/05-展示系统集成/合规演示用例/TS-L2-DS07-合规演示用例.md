# TS-L2-DS07 科技创新评估 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 科技创新评估（前端目录 `lumen-ui-science-pc/src/views/situation/innovation-evaluation`） |
| WBS | WBS-05-20 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技创新评估.md`，序号 136–158（excel 行 139–161，leaf_count=23） |
| 覆盖行数 | 23 |
| 状态 | R4 复测（2026-11-09）· **13 可演 / 7 部分可演 / 3 覆盖不到** · 149（FIX-09 v2 久新 15 集群）与 155（NSFC 代理）均已上线实测；143/151/157 因无权重模型维持部分可演；剩余 142/150/158 为数据源/模型缺口 |
| 任务ID | DISPLAY-DEMO-CASE-TS-M1-L07 |

**主路径一句话**：进入科技创新评估 → 选评估对象与年份 → 看「科学创造力 / 技术创新力 / 产业发展潜力 / 政策与条件保障力」四组指标 → 点指标卡看定义与数据来源。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 136 | 科学创造力 · 科学论文数量分析 | 领域（学科领域级联）；时间粒度（年 / 季度 / 月）；研究机构；地域（大湾区 11 城 / 深圳市各区县）；图表类型（柱状图 / 折线图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间粒度、机构、地域 | 图表出现且数据点数量与所选时间粒度一致；切柱/折线不改变数值；无数据时显示「该维度暂无论文数据」 | ✅可演。snapshot science 维「论文数量」=68.5（gkx dwd_zh_paper 100,900 篇真实计量）；indicatorIntro.sources 确认数据源；算法库 `M_INNOV_DS_07_SCI_CREATE_004` 直连 200，support_judgment=完全转换支持 |
| 137 | 科学创造力 · 科学网络中心性评估 | 指标（度中心性 / 接近中心性 / 中介中心性）；对象（学者 / 研究机构） | 切指标、点网络节点 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标类型、对象类型、领域 | 出现合作网络图谱与中心性排名表；排名条数=接口返回；无网络数据时显示「暂无合作网络数据」 | ⚠️部分可演（R1 2026-11-09 实测更正）。snapshot science 维「网络中心性」=57.5（合作网络中心性三维合成）有汇总分；但 payload 无中心性排名表、无合作网络图谱字段 → 期望输出中的图谱/排名按空态说明，只演分值 |
| 138 | 科学创造力 · 科学研究前沿性分析 | 领域；时间范围；前沿主题 | 点前沿主题 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间范围 | 展示前沿主题的时间演变与空间分布；主题条数=接口返回；无结果时提示「未识别到研究前沿」 | ⚠️部分可演（R1 2026-11-09 实测更正）。snapshot science 维「研究前沿」=68.9 有汇总分；payload 无前沿主题清单与主题时间演变字段 → 主题下钻按空态说明，只演分值 |
| 139 | 科学创造力 · 科学创造力趋势预测 | 领域；预测年限 | 点「预测」 | `POST /display/v1/situation/innovation-evaluation/snapshot` + 算法库 `M_INNOV_DS_07_SCI_CREATE_004` | 领域、历史区间、预测年限 | 出预测曲线与置信区间；模型不可用时显示「预测模型未接入」，不画无置信区的假预测线 | ✅可演。snapshot 新增 `sciForecast.domains`（3 领域：医学临床/新材料/电力能源），每域含 series（2015-2026 年序列，composite 0-1）、forecast（Holt 点预测 2024E/2025E）、lo80/hi80（80% 置信区间）；前端 `buildSciForecastOption` 渲染历史实线+预测虚线+CI 区域带，composite 缩放至 0-100；G7 已修复 |
| 140 | 技术创新力 · 专利数量统计分析 | 领域；时间范围（年 / 季度 / 月）；技术类别；地域；申请人；图表类型（柱状图 / 折线图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间粒度、技术类别、地域、申请人 | 专利数量随维度变化，申请量与授权量分列可辨；无数据时显示「该条件暂无专利数据」 | ✅可演。snapshot `techPatent.composite` 200 个 IPC4 技术领域真实数据（patent_count 如 A61K=226,626、C12N=127,804），data_source=jiuxin ads_patent_profile，data_source=real |
| 141 | 技术创新力 · 专利质量评估 | 质量指标（被引次数 / 权利要求数量 / 家族规模）；排序 | 切指标、点排序 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 质量指标、领域 | 展示质量指标分布与排名，识别高质量专利；指标缺失显示「未评估」 | ✅可演（降级口径，2026-11-10 M4 复跑）。FIX-01 落地：`techPatent.quality` dimensions 5 维含「权利要求数」（算法解析 `dwd_patent_claim.original_text`），missing_dimensions 空；rank_top 增 `avg_claims`/`claims_covered_count`（A61K avg=15.24、covered=25，覆盖 0.68% 冻结上限如实披露）；quality_score 与旧 4 维重归一值有差异（A61K 72.86→64.75） |
| 142 | 技术创新力 · 技术市场潜力分析 | 指标（市场活跃度 / 技术成熟度 / 商业化前景）；领域 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、指标 | 展示对应指标数值与解读；数据源缺位时明示「无市场活动数据」 | ⚠️部分可演（2026-11-10 M4 复跑，FIX-02 落地）。`composite.market_category_counts` 四类码值出数（转让 19,996/许可 50/质押 104/开放许可 6）+ 诉讼 0 命中如实标注；`market_attributable_counts` 可按 ipc4 归因（78 域）；weights_used 三维等权 market 不再恒 0；覆盖 0.68% 冻结上限 + 2 万样本为近 24 月转移事件集（非全库随机）三处声明；`weights_rule` 缺测维不补 0 |
| 143 | 技术创新力 · 技术创新力综合评估 | 指标权重（可自定义，各项权重合计 100%） | 调权重后点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、领域 | 权重和不为 100% 时提示校验错误；计算成功后显示综合得分与分项贡献 | ⚠️部分可演（R1 2026-11-09 实测更正）。`techPatent.composite` 200 领域含 composite_score（A61K=100.0）、维分 15.9 可演；但四维 `weights` 全 0、无权重合成模型，自定义权重提交后无后端重算 → 权重区按「模型未建」空态，只演固定口径综合分 |
| 144 | 技术创新力 · 技术创新空间分布 | 地域层级（大湾区 / 深圳市 / 区县）；展示形式（热力图 / 区域排名） | 切形式、缩放地图 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 地域层级、领域 | 热力图或排名表随层级变化；无数据区域不着色并标「无数据」 | ⚠️部分可演（R1 2026-11-09 实测更正）。`spatialRows`/`spatialRegions` 各 100 城真实（含经纬度与论文/被引/人才/项目计数，score=null）；但 `spatialByDimension` 四维均为空数组 → 按技术维切换无数据，只演城市计数热力/排名 |
| 145 | 技术创新力 · 技术创新趋势预测 | 领域；预测年限 | 点「预测」 | `POST /display/v1/situation/innovation-evaluation/snapshot` + 算法库 `M_TECH_DS_07_TECH_INNOV_006` | 领域、历史区间 | 出预测结果与置信区间；不可用时明示未接入 | ✅可演。snapshot `techPatent.forecast` 200 领域含 forecast_top、forecast_years=2、window=2015-2026、trend_direction、cagr_3y_pct；前端 `buildForecastOption` 渲染专利申请量历史+预测曲线；维度 metric「趋势预测」delta/trend 取自 forecast_top 趋势；G7 已修复 |
| 146 | 产业发展潜力 · 产业投入分析 | 维度（企业规模 / 地域 / 时间范围）；投入类型（研发投入 / 固定资产投资 / 人才投入）；图表（饼图 / 柱状图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 维度、地域、时间范围 | 投入结构与变化趋势可辨，饼图分项占比合计 100%；无数据时显示空态 | ✅可演。snapshot industry 维「产业投入」=50.0（48 国民经济行业真实计量，投入维=研发强度/载体密度百分位）；indicatorIntro.sources 确认 gkx dwd_org_income_statement 等 |
| 147 | 产业发展潜力 · 技术产品成熟度评估 | 产业；分析对象（技术 / 产品） | 点「成熟度分析」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 产业 id | 展示技术成熟度曲线或市场渗透率变化；无数据时提示「暂无成熟度数据」 | ✅可演。snapshot industry 维「产品成熟度」=50.0（成熟度维=授权率/发明占比百分位）；算法库 `M_INNOV_POT_COMPOSITE` 直连 200 |
| 148 | 产业发展潜力 · 产业产值分析 | 维度（时间范围 / 地域 / 企业类型）；产值口径（总产值 / 增加值 / 利润） | 选维度 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 维度、口径、年份 | 柱/折线展示产值变化，数值单位与口径一致；无数据时显示「暂无产值数据」 | ✅可演。snapshot industry 维「产业产值」=50.0（产值维=主营收入/净利润百分位）；48 行业真实计量 |
| 149 | 产业发展潜力 · 科学影响力评估 | 指标（论文被引次数 / 国际合作论文比例）；产业 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标、产业 id | 展示指标分布与排名；无被引数据时显示「未评估」 | ✅可演（R4 2026-11-09 解除）。FIX-09 v2 部署后 `industrySciInfluence` 出真值：久新 15 大产业集群口径（`ads_sz_gkx_industry_cluster_topic` ⋈ `ads_paper_profile`），score 74.9、15/15 集群齐全；top1 CL-SEI-01 新一代信息技术 612,431 篇 / 12,765,905 被引 / 篇均 20.84 / D1 100.0，合计 5,826,738 篇 / 114,379,101 被引。国际合作论文比例维久新无国别字段整维缺测（`gaps` 已声明，不补 0） |
| 150 | 产业发展潜力 · 技术影响力评估 | 指标（专利被引次数 / 标准必要专利数量）；产业 | 切指标 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 指标、产业 id | 展示指标分布与排名；无数据时明示 | ❌覆盖不到。snapshot industry 维「技术影响力」=N/A；同 G3，48 行业技术影响力覆盖不足整维缺测，标准必要专利无源 |
| 151 | 产业发展潜力 · 产业发展潜力综合评估 | 指标权重（可自定义，合计 100%）；产业 | 调权重、点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、产业 id | 权重校验同序号 143；成功后出综合得分与排名，排名条数=参评产业数 | ⚠️部分可演（R1 2026-11-09 实测更正）。industry 维「综合评估」=50.0（投入/成熟度/产值三维百分位加权，缺测不补 0）可演；但四维 `weights` 全 0、无自定义权重后端重算 → 权重区空态 |
| 152 | 政策与条件保障力 · 发展战略引导力评估 | 领域；战略/政策文件范围（时间范围） | 点「评估」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 领域、时间范围 | 展示战略规划关键内容、实施路径、预期目标与引导力评价；无数据时明示未接入 | ✅可演。snapshot policy 维「战略引导力」=50.1（引导力=规划类政策占比）；data_source=gkx dwd_policy_base（20,000 件抽样），四城 panel 真实计量 |
| 153 | 政策与条件保障力 · 政策扶持力度分析 | 政策类型（财税政策 / 人才政策 / 金融政策）；时间范围；地域 | 选类型、时间、地域 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 政策类型、时间范围、地域 | 展示政策数量、类型、覆盖面分布；无数据时显示「该条件暂无政策」 | ✅可演。snapshot policy 维「政策扶持力度」=64.3（扶持力度=类型覆盖/政策件数）；gkx dwd_policy_base 真实 |
| 154 | 政策与条件保障力 · 经费支持分析 | 经费来源；支持方向；时间范围；图表（饼图 / 柱状图） | 选维度、切图表 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 来源、方向、时间范围 | 展示经费结构与趋势，分项合计 100%；缺源时明示 | ✅可演。snapshot policy 维「经费支持」=89.4（经费=产业基金数）；data_source=gkx dwd_industrial_fund_basic_info（产业基金注册地）真实 |
| 155 | 政策与条件保障力 · 项目支持分析 | 项目类型；资助机构；时间范围 | 选维度 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 项目类型、机构、时间范围 | 展示项目数量、资助金额、实施效果；金额无源时显示「—」 | ✅可演（R3 2026-11-09 解除）。`projectSupport` 出真值：NSFC 代理口径（gkx dwd_zh_project **58,453 项**；approval_year 覆盖 1986–2021，2022 起缺失不按 0 摊入——caliber 诚实声明）score 42.9；资助金额 mean 43.27 万 / median 30 / max 920；类别分布 面上 27,939 / 青年C 23,884 / 地区 2,634 / 专项 1,058 / 重点 962——数量/金额/类别明细结构齐 |
| 156 | 政策与条件保障力 · 政策实施效果评估 | 政策对象；对比时点（政策前 / 政策后）；关键指标 | 选政策与对比时点 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 政策 id、对比时点、指标 | 展示前后关键指标对比与差值；无法归因时须标注「仅相关不构成因果」 | ✅可演。snapshot policy 维「实施效果」=100.0（效果=论文近三年 vs 前五年增幅）；gkx dwd_zh_paper 真实；页面口径为论文增幅代理，须保留「仅相关不构成因果」标注 |
| 157 | 政策与条件保障力 · 政策与条件保障力综合评估 | 指标权重（可自定义，合计 100%）；领域 | 调权重、点「计算」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 权重配置、领域 | 权重校验同序号 143；成功后出综合得分与排名 | ⚠️部分可演（R1 2026-11-09 实测更正）。policy 维「综合评估」=63.4（四维加权，项目维缺测不补 0）可演；但四维 `weights` 全 0、无自定义权重后端重算 → 权重区空态 |
| 158 | 政策与条件保障力 · 政策优化建议 | 评估对象；建议方面（政策重点调整 / 支持力度 / 实施路径） | 点「生成建议」 | `POST /display/v1/situation/innovation-evaluation/snapshot` | 评估对象、建议方面 | 生成对应建议条目；模型不可用时明确提示未接入，不得用模板套话代替；德尔菲法/系统仿真能力未接入须如实说明 | ❌覆盖不到。snapshot `policySuggestions=[]`、`methodEvidence`（delphi/simulation）空结构（disagreement/conclusion/consensus/optimistic/conservative/scenario/baseline 全空）；无建议生成模型、无专家评议与模拟数据源（缺口 G5） |

## LOOP 对照汇总

> 部署冒烟口径：网关 `http://10.50.69.111:30895`（StripPrefix=1），Headers `Authorization: Bearer <token>` + `systemCode: display`。算法库直连口径：算法调试台 NodePort `http://10.50.69.111:30894/api/innov/**`（nginx 自动加 `X-Apiview-Direct: 1` 直通 `gkxlumen-platform-innov-py:8000`）。

| 判定 | 条数 | 序号 |
|---|---|---|
| ✅ 可演 | 13 | 136, 139, 140, 145, 146, 147, 148, 149, 152, 153, 154, 155, 156 |
| ⚠️ 部分可演 | 7 | 137, 138, 141, 143, 144, 151, 157 |
| ❌ 覆盖不到 | 3 | 142, 150, 158 |

> **R1→R4 演进说明（2026-11-09 生产网关实测）**：原 19/1/3 为「有汇总分即记可演」口径。R1 按各行「期望输出」重判为 11/7/5：①137/138 只有维内汇总分，无图谱/排名表/主题清单字段；②143/151/157 综合分有值但四维 `weights` 全 0、无权重合成模型；③144 `spatialByDimension` 四维均为空数组（城市计数可用）；④149/155 生产响应缺 `industrySciInfluence`/`projectSupport` 两块。**R3：`projectSupport` 出真值（155 转 ✅）→ 12/7/4；R4：FIX-09 v2 部署后 `industrySciInfluence` 出真值（149 转 ✅）→ 13/7/3**。`noSourceFields` 10 项为设计空态（诚实性声明），不计缺陷。

实测接口清单（2026-11-09 复跑）：

| 接口 | 结果 |
|---|---|
| `POST /display/v1/situation/innovation-evaluation/meta` | 200，code=0。`regionOptions` 100 城真实（久新 ads_location）；`timeRangeOptions` 3 段真实（近3年/近5年/全区间）；`defaultWeights` 仍为 0 值空结构（无评估模型）；**新增 `dataSourceNote` 字段**：逐维说明数据源（科学=gkx dwd_zh_paper 100,900 篇；技术=久新 ads_patent_profile；产业=gkx 48 行业；政策=gkx 四城 panel），并标注各维缺测项与权重等权代理说明 |
| `POST /display/v1/situation/innovation-evaluation/snapshot` | 200，code=0，`empty=false`，**214.8KB（2026-11-09 R4 实测）**。`dimensions` 四维出分：science=36.6（论文数量 68.5 / 网络中心性 57.5 / 研究前沿 68.9 / 综合 36.6）/ technology=19.6 / industry=50.0 / policy=63.4；`weights` 四维全 0；`spatialRegions`/`spatialRows` 各 100 城真实但 `score=null`、**`spatialByDimension` 四维均为空数组**；`techPatent` 三键（composite/quality/forecast）各 200 IPC4 真实；`sciForecast.domains` 3 领域含 series+forecast+lo80/hi80；**`industrySciInfluence`（15 集群 / score 74.9 / 合计 5,826,738 篇）与 `projectSupport`（NSFC 58,453 项 / score 42.9）两块均已出真值**；`methodEvidence` 空结构、`policySuggestions=[]` |
| 算法库 `POST /api/innov/v1/innov/metric/{id}/compute`（30894 直连） | **全部 200**：M_INNOV_DS_07_SCI_CREATE_004 / M_TECH_DS_07_TECH_INNOV_002 / _004 / _006 / M_INNOV_POT_COMPOSITE / M_INNOV_PG_COMPOSITE 均返回真实数据；`GET /api/innov/v1/innov/metrics` 200 列出指标清单；G1 路由缺口已解决 |
| 对照：`POST /display/v1/situation/global-innovation/innov-value`（DS04） | 200，`empty=false`（无 emptyReason）；算法链路全局恢复，非本页独有 |

根因定性（更新）：G1、G7 已解决——G1 生产镜像 `gkxlumen-innov-py` 已挂 `/v1/innov/metric/{id}/compute` 路由，四维评分链路通；G7 后端 `InnovationEvaluationController` 新增 `sciForecast` 透出科学创造力预测曲线+80% CI，`techPatent.forecast` 技术趋势数据已在快照内，前端路由修正。剩余 G2–G5 为数据源/模型缺口。2026-11-09 双路线复核（久新 ads_* + 王慧口径 gkx `dwd_*` 探针，探针产物 `lumen-algo-py/vendor/innov-py/data/precompute/*.json`）：G2 两边均无源（gkx 转让表无法归属 IPC4、legal 覆盖 0.68%）；G3 科学 gkx 仅机构级可出榜（产业级 127 篇 < 100 篇门槛不排名）、久新 15 集群口径可做（覆盖 63.3%）；G3 技术 gkx 完全不支持（被引回连 0.0162%）、久新仅离线 precompute 理论可行；G4 gkx `dwd_zh_project` 部分支持（金额 100% 填充、结题摘要 81.1%，但 100% 国自然、 funded_institution/funded_province 空）、久新金额覆盖 1.3%~3.2% 不可用；G5 两边均无模型（王慧资料亦无对应指标文件）。需规核对结论：149/150 需规写死「特定产业」粒度+排名，机构级榜单不满足需规，149 唯一可行路线=久新 15 集群口径（待产品裁定）；155 需规未要求区域维、未限项目来源，gkx 国自然代理为最近路线（须标注口径）；142/150/158 无可用路线，维持缺口。**2026-11-08 产品裁定落地：149 走久新 15 深圳产业集群口径（产业粒度排名）、155 走 gkx 国自然代理口径（类型/机构/时间三维切片），源码已实现（snapshot `industrySciInfluence` / `projectSupport` 块 + 前端 IndustrySciInfluencePanel / ProjectSupportPanel）；2026-11-09 R3/R4 复测：display 与 innov-py（FIX-09 v2，commit `84ff427`）均已发布，`projectSupport` 与 `industrySciInfluence` 均出真值（149 score 74.9 / 15 集群 / 5,826,738 篇；155 score 42.9 / 58,453 项），两行升档可演。**142/150/158 维持缺口。**

## 缺口建单

| 缺口 | 影响序号 | 处置建议 |
|---|---|---|
| ~~G1 算法库指标路由未上生产~~ **已解决** | — | 路由 `/api/innov/v1/innov/metric/{id}/compute` 已上线，6 个 DS-07 指标全部 200；四维评分链路通 |
| G2 技术市场潜力数据源缺失（双路线取证 2026-11-09）：久新 `ads_patent_profile` 无转让/许可/质押/诉讼 IPC4 归属字段；王慧口径（gkx `dwd_patent_transfer`/`dwd_patent_legal`/`dwd_patent`，V2.0-20261108）探针=`完全不支持`——转让表 22,809 行仅 pn 无 patent_id/IPC4、主表 pn 无索引（3 条回连查询各 60s 超时）、legal_events 仅 20,000 行（0.68%）且诉讼命中 0/许可 56/质押 104/开放许可 6、`dwd_market` 15 行度量全空 | 142 | 数据补源（修复前置：transfer 加 patent_id+ipc4+apdt_year 或主表 pn 建索引；legal 扩全量并冗余 ipc4）。需规仅要求「转让、许可、诉讼等市场活动数据」未限定粒度，王慧口径与需规兼容但源缺；未补前该维整维缺测（market_score=null） |
| ~~G3 产业科学影响力~~ **149 已裁定落地并上线实测**（产品裁定 2026-11-08；R4 2026-11-09 复测通过）：149 科学——走久新 15 深圳产业集群口径（ads_sz_gkx_industry_cluster_topic ⋈ ads_paper_profile，topic 桥归属集群，按被引总次数百分位排名，15 集群论文数加权 D1 均值出分 score=74.9；国际合作论文比例维久新无国别字段整维缺测、不参与合成）；150 技术——gkx 探针=`完全不支持`（被引回连率 475/2,939,895=0.0162%、other_Versions 空壳、family 无申请人字段）；久新仅离线 precompute 理论可行。另需规举例含「标准必要专利数量」，王慧口径明确不用该字段，存在口径偏差 | ~~149~~, 150 | 149：**已上线**（M_INNOV_POT_SCI_INFL v2 久新集群口径，commit `84ff427`；snapshot `industrySciInfluence` 15 集群 / score 74.9 实测非 null，前端 IndustrySciInfluencePanel 渲染产业粒度排名表）；150：数据补源（patent_cited 补全量+统一 ID、加申请人字段、主表 pn 建索引），未补前技术影响力整维缺测（=N/A） |
| ~~G4 政策项目维~~ **155 已裁定落地**（产品裁定 2026-11-08）：走 gkx `dwd_zh_project` 国自然代理口径——58,453 项中文项目（funded_amount 100% 填充、结题摘要 81.1%、approval_year 1986–2021 连续、2022 起缺失不按 0 摊入），类型/机构/时间三维切片可算；资助机构维走依托单位（institution_top_zh）；代表性受限（100% 国自然）在 caliber/gaps 如实标注；v2 缺测维重归一 S=100×(0.5×资助金额归一+0.5×结题完备) | ~~155~~ | 已实现（M_INNOV_PROJECT_INFLUENCE precompute，snapshot `projectSupport` 透出三维切片，policy 维「项目支持」出分但不纳入综合分；前端 ProjectSupportPanel 渲染类型/机构/时间三维） |
| G5 政策建议与方法论模型无源：`policySuggestions=[]`、`methodEvidence`（德尔菲共识/情景模拟）空结构，无评估模型与专家评议数据源；王慧资料目录亦无政策建议/德尔菲对应指标文件（仅 GUIDE/INTENSITY/EFFECT/COMPOSITE 评估类）；久新侧无模型 | 158 | 模型接入；未接前页面须如实「未接入」，不得模板套话 |
| G6 历史报告 0 条：report 表 report_type=innovation-evaluation 无记录 | 页面「历史报告」抽屉（无独立 case 行） | 依赖跑通一次完整评估落库生成 |
| ~~G7 趋势预测分值未在快照维度层透出~~ **已解决** | — | 后端 `InnovationEvaluationController` 新增 `sciForecast` 字段（科学创造力 3 领域 Holt 点预测+80% CI），`techPatent.forecast` 200 领域趋势数据已在快照内；前端 `getDetailPanelOption` 科学维走 `buildSciForecastOption(sciForecast)`、技术维走 `buildForecastOption(techPatent.forecast)`；139/145 均升为 ✅可演 |

### 裁定回写（M4 裁定单 · 授权人李伟，2026-11-09）

> 以下为最终裁定，与本页「处置建议」冲突时以本表为准。编号 `M4-Gxx` 对应裁定单 G7–G10（本页原 G7 为另一事项，故加前缀以免混淆）。

| 缺口 | 裁定 |
|---|---|
| G1 算法库路由 | ✅ 已修复并发布（2026-11-08，pipeline 4305/4306 全绿；生产实测四维出分 19.6/36.6/50.0/63.4） |
| G2 技术市场潜力（142） | ⏳ 数据补源（transfer 加 patent_id+ipc4+apdt_year、legal 扩全量）；未补前整维缺测 `market_score=null`，不演空态，不得以转让计数顶替评分 |
| G3 产业科学影响力（149） | ✅ 已落地（久新 15 集群口径），可演 |
| G3 产业技术影响力（150） | ⏳ 数据补源；整维缺测 = N/A，不演 |
| G4 政策项目维（155） | ✅ 已落地（gkx 国自然代理三维切片），可演 |
| G5 政策建议与方法论（158） | ✅ 不演（接受空态，禁模板套话）——裁定单 A01 |
| G6 历史报告 0 条 | ⏳ G1 已发布，需跑一次完整评估落库生成 |
| G7 趋势预测透出（139/145） | ✅ 已解决 |
| M4-G7 `claim_count` | ✏️ 修复（数仓：建字段 + 回填）；专利质量按 4/5 维重归一 |
| M4-G8 `legal_event_code` 4 类码值 | ✏️ 修复（数仓：补许可/诉讼/质押/开放许可码值）；未补前不参与市场潜力计分 |
| M4-G9 国别映射表 | ✏️ 修复（后端：`country_alias` 映射表） |
| M4-G10 政策前瞻词表 | ✏️ 修复（算法：config 词表） |
| 评估对象范围 | ⏳ SRS 未给「评估对象」枚举，产品需补，否则 P2 复刻无法排 LOOP |

## 备注与风险

- **G1、G7 已解决，149/155 裁定落地并上线后演示覆盖率为 13/23 可演 + 7 项部分可演**：四维评分链路通，科学/技术/产业/政策各有真实分值与指标卡；趋势预测（139 科学创造力、145 技术创新力）曲线+置信区间已透出；149 产业科学影响力（久新 15 集群粒度排名，score 74.9）与 155 项目支持分析（gkx 国自然代理三维切片，score 42.9）均已实测出真值。现场讲解以四维综合评估卡 + 可演 13 项为主线。
- **3 项覆盖不到为数据源/模型缺口（G2–G5 残余）**：142 市场潜力、150 技术影响力、158 政策建议——均为缺源/缺模型，非链路问题。现场须如实说明「数据源未接入」，不得前端补算。149/155 已于 2026-11-08 产品裁定口径落地，并于 2026-11-09 R3/R4 实测出真值（149 score 74.9 / 155 score 42.9），不再属缺口。
- **7 项部分可演**：137 网络中心性（有维分无图谱/排名表）、138 技术前沿性（有维分无前沿主题清单）、141 专利质量（4/5 维可演，权利要求数缺测）、143/151/157 三处权重合成（综合分有值但 `weights` 全 0、无权重模型）、144 空间分布（城市计数真实但 `spatialByDimension` 四维空）。
- **评估对象范围未定**：SRS 未给「评估对象」枚举（领域/产业/区域/机构何者为主），页面选择项无法列全集，M2 前需产品补齐。
- **权重为等权代理**：四维 indicatorIntro 均注明「权重等权代理（甲方签认前不作正式口径）」，`defaultWeights` 为 0 值空结构。演示时须说明权重为临时等权，正式口径待甲方签认。
- **预测与建议类（139、145、158）**：139/145 趋势预测已可演（G7 修复，sciForecast + techPatent.forecast 透出）；158 建议生成模型未接入，须按不可用讲。
- **序号 158 附加的德尔菲法/系统仿真**：SRS 明确要求，`methodEvidence` 空结构，须在演示口径中列为「未提供」。
- **四组指标与页面 Tab 的对应关系**：本文件按 SRS 四个分组归位（科学创造力 / 技术创新力 / 产业发展潜力 / 政策与条件保障力），与 snapshot dimensions 的 key（science/technology/industry/policy）一一对应。
