# TA-L2-DS16 人才引进推荐评估 · 合规演示用例

| 项 | 值 |
|---|---|
| 页面 | DS-16 人才引进推荐评估（科技人才态势 · 人才引进推荐评估，4 个 Tab） |
| WBS | WBS-05-03a（前端菜单壳）/ WBS-05-03b（后端）；四子页不重做，供数归 WBS-02-01 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技人才态势/人才引进推荐评估.md` · seq 305–329（excel 行 308–332） |
| 覆盖行数 | 25（seq 305–329 每条一行） |
| 状态 | M3 已填（2026-11-08 网关实测）：接口 200 有真实数据（非 DS-13 实测时的 DOWNSTREAM_UNREACHABLE）· 21 可演（含 14 空态演示）+ 4 部分可演 + 0 覆盖不到 · 待签收 |
| 任务ID | DISPLAY-DEMO-CASE-TA-M1-L01 |

**主路径一句话**：选产业级联 + 评估目标 + 当前评估对象 → 贡献度 Tab 三层视图与指标缩放 → 点「自动深度分析」打开贡献匹配报告 → 切尽调 Tab 按学科方向 / 匹配度阈值筛出推荐卡 → 打开尽调报告并导出 PDF；难度 / 成本两 Tab 只展示「无数据」空态。

> 口径说明：`GET /display/v1/talent/recommend/dataset` **无查询参数**，评估目标、评估对象与筛选均在前端完成；推荐集为 **15 名 MVP 人才内按能力分 Top8**，`aiScore` 与 `matchScore` 为两套口径（`ta_recommend_self_v1`），不得合并成一个分。数据情况已于 M3（2026-11-08）按网关实测逐行回填，实测证据见文末「LOOP 对照汇总」。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 305 | 人才引进推荐评估 · 筛选行 + 贡献度 Tab | 产业级联（一级产业 → 二级产业）；评估目标（页面下拉枚举）；当前评估对象（可搜索下拉）；贡献层级（概览 / 学者 / 成果）；关系网络节点（专家 / 学科 / 成果 / 合作者） | 选目标与对象 / 切换层级 / 点击节点 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；目标与对象前端匹配 `recommendations` / `talents` | 三层视图互斥切换，关系网络随层级聚焦；点击节点下钻到该专家 / 学科 / 成果；无贡献数据的人才显示空态，不借用他人数据 | ✅可演。实测 200：talents=15（全档真实）、recommendations=8（15 人内能力分 Top8）、contributionScores=15；关系网络节点取 talents[].collaborationNetwork（每人才 13 节点=本人+12 真实合作者含合作次数，links 边未下发、由前端按层级语义构建）；合作者节点姓名未解析时显示 id，现场不点名 |
| 306 | 贡献度 Tab · 多维数据联动 | 指标（论文质量 / 影响因子 / 项目数 / 专利量）；分值区间滑杆；热力图 zoom 模式；贡献图谱 | 调滑杆 / 切 zoom 模式 / 点击图谱 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；按 `contributionScores` 前端重算 | 四类指标条按所选区间重排；热力图放大后高贡献区突出；项目 / 专利「贡献分」无评分源时该维度分值为 0 且另列真实计数，不用计数冒充评分 | ✅可演。scores.papers/impact/network 为真实分；projects/patents 无评分源分=0 且 projectCount/patentCount 真实另给（如李亚栋 456/0）；trend 2015–2025 真实活跃指数；fieldGain 为空，热力值由前端按 avg（真实）+fields 归属规则派生 |
| 307 | 贡献度 Tab · 智能分析与推荐 | 自动深度分析（高潜力 Top1）；预测视图（整体预期 / 局部影响 / 阶段性增长）；缩放与聚焦操作 | 点「自动深度分析」/ 切预测视图 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 自动切到高潜力对象并展开其贡献；贡献匹配报告弹窗出现潜力 / 匹配 / 风险三卡与贡献雷达；预测视图无模型时显示空态，不输出预测数值 | ⚠️部分可演。自动深度分析与贡献匹配报告可演（潜力/匹配真实、贡献雷达五维中 project/social 无源为 0、风险卡 NO_DATA 标注）；预测视图无真源模型，前端按演示规则对真实 trend 投影（系数 1.05/0.85/1.15），现场按「规则投影」讲，不得讲成模型预测 |
| 308 | 学者引进难度预测 Tab · 学者适应性评估 | 难度 Tab；六因子面板（含 activity 活跃度因子）；评估对象 | 切到难度 Tab / 切换评估对象 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；按 `difficultyEstimate.factors` 渲染 | 难度仪表盘显示综合难度；`activity` 因子有真实百分位值（level 标 `PARTIAL_DATA`）；其余 7 因子无源时显示占位并标注「无数据」，不得解释为「难度低」 | ⚠️部分可演。factors.activity=100.0 真实（99,996 人百分位口径，level=PARTIAL_DATA）；其余 7 因子=0 无源（T7 未建）；overall=0 综合难度无模型，仪表盘按「模型未建」空态讲，不得把 0 分解读为难度低 |
| 309 | 难度预测 Tab · 沟通障碍智能检测 | 因子 `communication` | 查看该因子 / hover 图标 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号 + 「无数据源（IP-10，owner 待定）」说明；不参与难度总分计算，不以 0 分呈现 | ✅可演（空态演示）。communication=0 无源；前端 FACTOR_MISSING 红问号 +「无数据源（IP-10，owner 待定）」锚点已在（recommendMetrics.ts），不生成检测结论 |
| 310 | 难度预测 Tab · 文化融合风险评估 | 因子 `culture` | 查看该因子 / hover 图标 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号与无源说明；不生成文化适应结论或建议方案 | ✅可演（空态演示）。culture=0 无源；前端红问号 +「无数据源（IP-10，owner 待定）」锚点已在，不生成文化适应结论 |
| 311 | 难度预测 Tab · 国际流动壁垒分析 | 因子 `mobility`；出访 / 流动记录 | 查看该因子 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号与无源说明；出访记录为空态（`overseasVisits` 无源），不推测迁徙意愿 | ✅可演（空态演示）。mobility=0 无源；overseasVisits/overseasExchanges 全 15 人空数组（出访无源），空态不推测迁徙意愿 |
| 312 | 难度预测 Tab · 过往合作情况回溯 | 过往合作表（机构 / 项目 / 合作次数 / 时间）；合作网络图 | 打开难度 Tab / 点击表格行 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；取 `talents[].collaboration` 相关表 | 合作表按机构与项目列出真实合作记录，点击行联动网络图高亮；无合作记录时显示空态，不填演示行 | ⚠️部分可演。difficultyScores[].pastCooperation 全 15 人空数组 → 合作表空态（注意文案不能讲「无合作记录」，本组人才有真实合作）；合作事实真实存在于 talents[].collaborationNetwork（12 合作者+真实次数），但非「机构/项目/次数/时间」表结构且未接入难度 Tab（缺口登记候选） |
| 313 | 难度预测 Tab · 个人科研活跃度与合作网络分析 | 合作网络力导向图；活跃度指标 | 打开难度 Tab / 拖动网络 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 网络节点与边为真实合作数据，可缩放与下钻；活跃度指标无源时该指标显示空态，不编造活跃度分 | ⚠️部分可演。难度 Tab 网络图取 difficultyScores[].network（全 15 人空）→ 力导向图空态；活跃度因子 activity=100.0 真实可演；主档 collaborationNetwork 节点真实（合作者+次数），links 边未下发（缺口登记候选） |
| 314 | 难度预测 Tab · 引进阻力量化评分 | 难度面板标题；综合评分 | hover 标题 ⓘ / 查看评分 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 综合难度评分及主要阻力来源；模型未建（T7）时显示空态与「模型未建」说明，禁止用招入推荐匹配度顶替 | ✅可演（空态演示）。overall=0 + level=PARTIAL_DATA（T7 模型未建）；前端 RECOMMEND_MISSING_METRICS.resistance 红问号「无数据源（IP-10）」已在；禁止用推荐匹配度顶替综合难度 |
| 315 | 难度预测 Tab · 策略建议与预警提示 | 预警筛选（高风险 / 中风险 / 全部） | 切换筛选 / 查看预警 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 预警条目与建议按风险等级过滤；无评估结果时显示「演示规则提示」而不生成个性化策略；不出现凭空的预算或方案建议 | ✅可演（空态演示）。difficultyScores[].strategies 全 15 人空数组 → 按「演示规则提示」空态，不生成个性化策略；不出现凭空预算或方案建议 |
| 316 | 引进成本预测 Tab · 多维成本数据采集 | 采集维度（领域权威度 / 职位头衔 / 过往薪酬 / 所获奖项 / 引进难度 / 引才案例 / 薪酬趋势 / 激励政策） | 切到成本 Tab / 展开采集清单 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 各维度显示来源与更新时间；无薪资源时显示「无数据源」占位，不展示金额或薪酬区间 | ✅可演（空态演示）。costEstimates 全 15 人 NO_DATA（8 维采集全 0/空，无薪资源）；前端 costModel 红问号「成本采集来源未拍板（DN-A15-COST）」已在，占位不展示金额 |
| 317 | 成本预测 Tab · 高精度成本模型构建 | 模型维度（学科 / 地区 / 专家类型）；三方案预设（稳健 / 科研倾斜 / 薪酬竞争） | 切换预设 / 点「测算」 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 模型输出引进费用区间与趋势预测；成本模型未建时结果区显示空态，不输出任何金额 | ✅可演（空态演示）。成本模型未建（T12/T13），modelConfidence=0、predictedTotal=0；结果区空态不输出金额，三方案预设控件保留 |
| 318 | 成本预测 Tab · 个性化成本分布分析 | 成本结构（薪酬 / 津贴 / 科研启动经费 / 生活保障） | 切到成本结构视图 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 成本结构条与饼按组成部分展示并可切换专家类型；无源时结构与占比区显示空态，不给出虚构比例 | ✅可演（空态演示）。costs 八项（salary/allowance/research/housing/relocation/other/team/total）全 0 无源 → 结构与占比空态，不给虚构比例 |
| 319 | 成本预测 Tab · 方案模拟与资金测算 | 方案参数滑杆（五档）；方案数量（多方案对比）；成本参数 | 拖动滑杆 / 点「模拟」 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 输出资金投入、投资回报、人员配置与预算差异；成本无源时控件保留但结果区显示空态，不产金额 | ✅可演（空态演示）。成本无源（DN-A15-COST）；滑杆/多方案控件保留，结果区空态不产金额 |
| 320 | 成本预测 Tab · 历史成本趋势追踪 | 年份范围；投入 / 效果两条曲线 | 切换年份 / 缩放趋势图 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 历史投入与效果趋势曲线可放大；无历史成本数据时趋势区显示空态，不用其他指标画替代趋势 | ✅可演（空态演示）。costEstimates[].trend/salaryTrend 全空数组 → 历史趋势区空态，不用其他指标画替代曲线 |
| 321 | 成本预测 Tab · 智能预警与决策建议 | 预警阈值；异常成本区段 | 设置阈值 / 查看预警 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 高风险或异常区段高亮并给出预算优化建议；成本无源时预警区显示空态，不编建议文案 | ✅可演（空态演示）。成本无源 → 预警区空态，不编预算优化建议文案 |
| 322 | 成本预测 Tab · 支持导出和对比分析 | 导出格式（CSV / PDF）；对比对象（历史 / 行业平均 / 典型案例） | 点导出 / 切换对比对象 | 无独立端点（前端本地生成，数据源 `GET /display/v1/talent/recommend/dataset`） | 无查询参数 | 导出成本数据表并带 BOM；对比视图按所选对象并列；成本无源时导出为空模板并提示「无成本数据」，不输出占位金额 | ✅可演（空态演示）。无独立端点（前端本地生成）；成本无源 → 导出空模板并提示「无成本数据」，不输出占位金额 |
| 323 | 人才尽调报告与推荐 Tab · 专家画像智能生成 | 当前评估对象；定制维度（学术背景 / 行业贡献 / 以往合作 / 奖项荣誉 / 风险点）；生成按钮 | 点「生成画像」 | `GET /display/v1/talent/recommend/dataset`（画像主体取 `talents[]`） | 无查询参数 | 画像卡展示基础信息、成果、履历与合作网络，并标注 NLP 融合采集计数；无源维度显示空态；画像对象必须与所选评估对象一致 | ✅可演。talents[] 15 人全档真实：education/workExperience/recentWorks（5 篇）/honors（0–16 条正式事实）/collaborationNetwork（13 节点含真实合作次数）；sources 计数真实（papers/projects/networkNodes+platforms=OpenAlex/久新ADS）；nlpFieldProfile=NOT_BUILT 空态标注；出访等无源维度空态 |
| 324 | 尽调 Tab · 多维综合评价与评分 | 评分维度（权威度 / 创新性 / 项目经验 / 社会影响）；评分雷达 | 打开推荐卡 / 切评分维度 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 展示能力综合分（`aiScore`，口径 `ta_recommend_self_v1`）与学科匹配分（`matchScore`）两项，分列且标注口径；未入推荐集的人才不显示评分 | ✅可演。8 名推荐人 aiScore（能力口径 ta_recommend_self_v1）与 matchScore（最佳问题学科匹配）双列真实（如李亚栋 99.0/76.0）；dimensions 五维中 project/social 无源为 0；未入推荐集不显示评分 |
| 325 | 尽调 Tab · 定制化尽调报告生成 | 定制维度勾选；报告范围（单人或多人） | 点「生成报告」/ 导出 PDF | 无独立端点（前端打印页生成，数据源 `GET /display/v1/talent/recommend/dataset`） | 无查询参数 | PDF 报告含多源画像、AI 评分雷达、成果、履历、合作网络与风险六段；风险段无源时标注「无数据」而非「无风险」；维度勾选变化反映到报告章节 | ✅可演。无独立端点（前端打印页/PDF 落库链路 talent-dd-report，契约 v1.6 本地联调实测）；报告六段数据源真实（talents+recommendations）；风险段 risks 四类全 NO_DATA → 标注「无数据」而非「无风险」 |
| 326 | 尽调 Tab · 专家智能推荐 | 学科方向；匹配方式（随评估目标联动）；匹配度阈值；关键词 | 选择条件 / 拖动阈值 / 关键词回车 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；按 `recommendations` 前端过滤 | 推荐卡网格按匹配度降序，条数 = 阈值内命中数（目录上限为 15 人内 Top8）；每卡显示匹配理由；低于阈值不展示；无命中显示空态文案 | ✅可演。recommendations 8 条按 matchScore 降序真实在册；matchReasons 真实（最佳问题匹配+能力总分，产业力理由 6/15 人有分）；阈值过滤前端完成，低于阈值不展示、无命中空态 |
| 327 | 尽调 Tab · 动态跟踪与更新 | 刷新按钮；时间戳 | 点刷新 | `GET /display/v1/talent/recommend/dataset` | 无查询参数（重新取 dataset） | 推荐卡与画像的更新时间戳刷新；后端无实时推送时标注「页面重取」，不虚构新成果或新履历 | ✅可演。recommendations[].updatedAt=2026-11-06 真实；刷新=重取 dataset（无实时推送，标注「页面重取」），不虚构新成果或新履历 |
| 328 | 尽调 Tab · 风险与合规性评估 | 风险类型（合作风险 / 学术诚信 / 成果有效性 / IP） | 打开风险区 / 切换风险类型 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；取 `risks` | 四类风险分别展示评估结果与依据；`risks` 无源时该区显示空态并注明「无风险数据」，绝不显示「无风险」结论 | ✅可演（空态演示）。recommendations[].risks 四类（cooperation/integrity/validity/ip）全 NO_DATA、riskLevel=NO_DATA → 风险区空态注明「无风险数据」，绝不显示「无风险」结论 |
| 329 | 尽调 Tab · 团队组合与协同分析 | 对比对象（2 人及以上）；并行尽调队列；团队分析入口 | 点「对比」/ 打开并行队列 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 展示协同度评分、学科覆盖缺口、角色互补与两两协同表；团队协同模型未建时显示空态，禁用合作网络边密度顶替协同度 | ✅可演（空态演示）。团队协同模型未建（RECRUIT_025 无源）；前端 teamSynergy 红问号锚点已在（TalentComparePanel），协同度空态，禁用合作网络边密度顶替 |

## LOOP 对照汇总（M3 · 2026-11-08）

**接口实测**：`GET /display/v1/talent/recommend/dataset`（网关 `http://10.50.69.111:30895`，StripPrefix=1，headers `Authorization: Bearer <token>` + `systemCode: display`）→ **HTTP 200 / 13.4s / code=0 / 437KB**；响应中**无 emptyReason**（区别于 DS-13 实测时的 DOWNSTREAM_UNREACHABLE，本次 gkx_show_service→久新 Doris 链路连通、数据真实）。数据集规模：`talents=15`、`recommendations=8`、`contributionScores=15`、`difficultyScores=15`、`costEstimates=15`。322/325 无独立端点（前端本地生成），未触发写操作。

| 判定 | 行数 | 序号 |
| --- | --- | --- |
| ✅ 可演（真实数据支撑） | 7 | 305、306、323、324、325、326、327 |
| ✅ 可演（空态演示，501 档语义） | 14 | 309、310、311、314、315、316、317、318、319、320、321、322、328、329 |
| ⚠️ 部分可演 | 4 | 307、308、312、313 |
| ❌ 覆盖不到 | 0 | — |
| blocked 待开发完成 | 0 | — |

合计 25 行，全部对上。难度 / 成本两 Tab 按 M1 备注 3「结构保留 + 空态」501 档语义演示：控件与面板保留、结果区空态、红问号锚点已在（前端 `recommendMetrics.ts` 的 `FACTOR_MISSING` / `RECOMMEND_MISSING_METRICS`）。

**实测要点**：
- 真实：15 名 MVP 人才全档（教育/履历/近作 5 篇/荣誉/合作网络 13 节点含真实合作次数）；recommendations 双分口径真实（aiScore 能力 `ta_recommend_self_v1`、matchScore 学科匹配，updatedAt=2026-11-06）；contributionScores 论文/影响/网络分真实、trend 2015–2025 真实活跃指数、sources 计数真实。
- 无源（诚实 0/空，演示按空态讲）：难度 7 因子（仅 activity=100.0 真实、level=PARTIAL_DATA、overall=0）、pastCooperation/network/strategies 全空、costEstimate 全族 NO_DATA、risks 四类 NO_DATA、overseasVisits 空、nlpFieldProfile=NOT_BUILT、socialInfluence 仅 mediaMentions 真实。
- 派生（现场需知）：贡献热力 `fieldGain` 为空，热力值由前端按 avg（真实）+ fields 归属规则派生；预测视图为前端演示规则投影（trend×固定系数），非模型产出；`contributionScores[].collaborators` 姓名未解析（显示 tal_xxx id，现场不点名）。

## 缺口建单（M3 · 2026-11-08）

| 关联行 | 缺口 | 根因 | 处置建议 |
| --- | --- | --- | --- |
| 307 | 预测视图无真源预测模型 | 无预测模型数据源；前端按演示规则对真实 trend 投影 | 引用既有缺口口径登记；演示按「规则投影」讲，不得讲成模型预测 |
| 308、314 | 综合难度模型 T7 未建 | difficultyEstimate 仅 activity 有源（PARTIAL_DATA），其余 7 因子=0、overall=0 | 引用既有 T7 / IP-10；模型未建前按「模型未建」空态演示，禁止把仪表盘 0 分讲成难度低 |
| 312 | 过往合作表无源 | `difficultyScores[].pastCooperation` 全 15 人空数组（机构/项目/次数/时间表结构无源） | **新登记候选**：合作事实在 talents[].collaborationNetwork（12 合作者+真实次数），需后端补表结构切面或难度 Tab 改接主档——交 M4 / 授权人裁定 |
| 313 | 难度 Tab 合作网络空 | `difficultyScores[].network` 全空；主档 collaborationNetwork 节点真实但 links 边未下发 | **新登记候选**（同上，后端 dataset 组装缺口）——交 M4 / 授权人裁定 |
| 316–322 | 成本全族 NO_DATA | 无薪资源（dwd_org_recruit_info 未入久新），T12/T13 成本模型未建 | 引用既有 DN-A15-COST；501 档空态演示 |
| 328 | 风险四类无源 | risks 全 NO_DATA（合作/诚信/有效性/IP 评估未建） | 引用既有 IP-10；空态注明「无风险数据」，绝不显示「无风险」 |
| 329 | 团队协同无源 | RECRUIT_025 协同度模型未建 | 引用既有；协同度空态，禁用合作网络边密度顶替 |

**演示诚实性红线（现场不得改口）**：aiScore ≠ matchScore 两套口径不得合并；projects/patents 贡献分=0 是无评分源、计数另列真实值；难度 overall=0 是「模型未建」不是「难度低」；成本全 0 是「无数据源」不是「免费」；risks NO_DATA 不是「无风险」；预测视图为前端规则投影非模型产出。

## 备注与风险

1. **久新实探结论与契约口径**：推荐集 = 15 名 MVP 人才内按能力分 Top8（每个推荐项在 `talents[]` 有完整主档）；`aiScore` = `ads_talent_capability_assessment` 学术能力分（口径 `ta_recommend_self_v1`），`matchScore` = `ads_talent_research_problem_discipline_match` 最佳问题学科匹配分（1,142,501 行）；`matchReasons` 产业力理由来自 `industrial_capability_industry_score`（6/15 人有分）+ `ads_industry` 主行业名；`sources` 计数全部真实；`contributionScores` 五维中 projects / patents 无评分源（分值为 0，计数真实另给）。
2. **明确无源 / 空态项**：`difficultyEstimate` 仅 `factors.activity` 有真实百分位（其余 7 因子 0，T7 未建）；`costEstimate` 全部 NO_DATA（无薪资源，`dwd_org_recruit_info` 未入久新，T12 / T13 未建）；`risks`（合作 / 诚信 / 有效性 / IP）无源 → null；团队协同（`RECRUIT_025`）无源；出访与海外交流无源。对应行（308–311、314–322、328、329）**不得写成可演金额或风险结论**。
3. **演示语义约束**：难度 / 成本 Tab 按「501 档语义」处理（页面保留结构与控件，结果区空态）；诚信 / 政治 / 情感类演示分带 `nature` 字段，禁止裸展示分数，禁止用于筛选决策。307 的「预测视图」与 321 的「决策建议」无模型时必须空态。
4. **契约未闭合项**：评估目标下拉、当前评估对象候选、定制尽调维度选项的枚举未在 SRS 或契约中固定（由 `talentRecommendSpec` 与页面枚举提供），M2 需补全集；`326` 的「匹配方式」随评估目标联动映射（`EVALUATE_TARGET_TAB` / `TARGET_TO_ORG_NEED`）属前端冻结语义，需在 M3 核对口径；导出 / 报告均无后端端点，为前端打印页或 CSV 本地生成。
5. **页面不重做**：WBS-05-03a / 03b 只做菜单壳与非三要素区块，四子页不重做；供数归 WBS-02-01，技术方案 §1.2 记「非三要素区块的对接对象清单：还没有」。
