# TA-L2-DS16 人才引进推荐评估 · 合规演示用例

| 项 | 值 |
|---|---|
| 页面 | DS-16 人才引进推荐评估（科技人才态势 · 人才引进推荐评估，4 个 Tab） |
| WBS | WBS-05-03a（前端菜单壳）/ WBS-05-03b（后端）；四子页不重做，供数归 WBS-02-01 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技人才态势/人才引进推荐评估.md` · seq 305–329（excel 行 308–332） |
| 覆盖行数 | 25（seq 305–329 每条一行） |
| 状态 | M3 已填（2026-11-08 网关实测）：接口 200 有真实数据（非 DS-13 实测时的 DOWNSTREAM_UNREACHABLE）· **23 可演（含 14 空态演示）+ 2 部分可演 + 0 覆盖不到**（312/313 已修复升档：后端 `df225ed` + pipeline 4308 全绿；312 机构列已修复升档：后端 `ef1004b` + edu 网关实测 + 前端 `fe497a8` 浏览器实测）· M5 编排完成（`../编排计划/TA-L2-DS16-LOOP计划.md`）· **R1 实跑完成（2026-11-09）→ 已签收（2026-11-09，监管人 human:李伟）** |
| 任务ID | DISPLAY-DEMO-CASE-TA-M1-L01 |

**主路径一句话**：选产业级联 + 评估目标 + 当前评估对象 → 贡献度 Tab 三层视图与指标缩放 → 点「自动深度分析」打开贡献匹配报告 → 切尽调 Tab 按学科方向 / 匹配度阈值筛出推荐卡 → 打开尽调报告并导出 PDF；难度 / 成本两 Tab 只展示「无数据」空态。

> 口径说明：`GET /display/v1/talent/recommend/dataset` **无查询参数**，评估目标、评估对象与筛选均在前端完成；推荐集为 **15 名 MVP 人才内按能力分 Top8**，`aiScore` 与 `matchScore` 为两套口径（`ta_recommend_self_v1`），不得合并成一个分。数据情况已于 M3（2026-11-08）按网关实测逐行回填，实测证据见文末「LOOP 对照汇总」。

## 覆盖表

| 序号 | 界面 | 输入或选择 | 触发 | 接口 | 请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 305 | 人才引进推荐评估 · 筛选行 + 贡献度 Tab | 产业级联（一级产业 → 二级产业）；评估目标（页面下拉枚举）；当前评估对象（可搜索下拉）；贡献层级（概览 / 学者 / 成果）；关系网络节点（专家 / 学科 / 成果 / 合作者） | 选目标与对象 / 切换层级 / 点击节点 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；目标与对象前端匹配 `recommendations` / `talents` | 三层视图互斥切换，关系网络随层级聚焦；点击节点下钻到该专家 / 学科 / 成果；无贡献数据的人才显示空态，不借用他人数据 | ✅可演。实测 200：talents=15（全档真实）、recommendations=8（15 人内能力分 Top8）、contributionScores=15；关系网络节点取 talents[].collaborationNetwork（每人才 13 节点=本人+12 真实合作者含合作次数，links 边未下发、由前端按层级语义构建）；合作者节点姓名未解析时显示 id，现场不点名 |
| 306 | 贡献度 Tab · 多维数据联动 | 指标（论文质量 / 影响因子 / 项目数 / 专利量）；分值区间滑杆；热力图 zoom 模式；贡献图谱 | 调滑杆 / 切 zoom 模式 / 点击图谱 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；按 `contributionScores` 前端重算 | 四类指标条按所选区间重排；热力图放大后高贡献区突出；项目 / 专利「贡献分」无评分源时该维度分值为 0 且另列真实计数，不用计数冒充评分 | ✅可演。scores.papers/impact/network 为真实分；projects/patents 无评分源分=0 且 projectCount/patentCount 真实另给（如李亚栋 456/0）；trend 2015–2025 真实活跃指数；fieldGain 为空，热力值由前端按 avg（真实）+fields 归属规则派生 |
| 307 | 贡献度 Tab · 智能分析与推荐 | 自动深度分析（高潜力 Top1）；预测视图（整体预期 / 局部影响 / 阶段性增长）；缩放与聚焦操作 | 点「自动深度分析」/ 切预测视图 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 自动切到高潜力对象并展开其贡献；贡献匹配报告弹窗出现潜力 / 匹配 / 风险三卡与贡献雷达；预测视图无模型时显示空态，不输出预测数值 | ⚠️部分可演。自动深度分析与贡献匹配报告可演（潜力/匹配真实、贡献雷达五维中 project/social 无源为 0、风险卡 NO_DATA 标注）；预测视图无真源模型，前端按演示规则对真实 trend 投影（系数 1.05/0.85/1.15），现场按「规则投影」讲，不得讲成模型预测 |
| 308 | 学者引进难度预测 Tab · 学者适应性评估 | 难度 Tab；六因子面板（含 activity 活跃度因子）；评估对象 | 切到难度 Tab / 切换评估对象 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；按 `difficultyEstimate.factors` 渲染 | 难度仪表盘显示综合难度；`activity` 因子有真实百分位值（level 标 `PARTIAL_DATA`）；其余 7 因子无源时显示占位并标注「无数据」，不得解释为「难度低」 | ✅可演（2026-11-10 M4 复跑，FIX-08 T7 落地）。15 人 `difficultyEstimate` 全非 null：5 真实因子（activity/mobility/pastCooperation/adaptability/policy，`factorSources` 标 REAL），communication/culture/family 显式 null+NO_SOURCE 非 0 掩码；overall 35.97–84.32 十五人全异值；`weightVersion=v1-demo.t7-2026-11-09` 演示口径披露 |
| 309 | 难度预测 Tab · 沟通障碍智能检测 | 因子 `communication` | 查看该因子 / hover 图标 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号 + 「无数据源（IP-10，owner 待定）」说明；不参与难度总分计算，不以 0 分呈现 | ✅可演（空态演示）。communication=0 无源；前端 FACTOR_MISSING 红问号 +「无数据源（IP-10，owner 待定）」锚点已在（recommendMetrics.ts），不生成检测结论 |
| 310 | 难度预测 Tab · 文化融合风险评估 | 因子 `culture` | 查看该因子 / hover 图标 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号与无源说明；不生成文化适应结论或建议方案 | ✅可演（空态演示）。culture=0 无源；前端红问号 +「无数据源（IP-10，owner 待定）」锚点已在，不生成文化适应结论 |
| 311 | 难度预测 Tab · 国际流动壁垒分析 | 因子 `mobility`；出访 / 流动记录 | 查看该因子 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 该因子显示红问号与无源说明；出访记录为空态（`overseasVisits` 无源），不推测迁徙意愿 | ✅可演（空态演示）。mobility=0 无源；overseasVisits/overseasExchanges 全 15 人空数组（出访无源），空态不推测迁徙意愿 |
| 312 | 难度预测 Tab · 过往合作情况回溯 | 过往合作表（机构 / 项目 / 合作次数 / 时间）；合作网络图 | 打开难度 Tab / 点击表格行 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；取 `talents[].collaboration` 相关表 | 合作表按机构与项目列出真实合作记录，点击行联动网络图高亮；无合作记录时显示空态，不填演示行 | ✅可演（2026-11-09 升档：机构列已修复，后端 `ef1004b` + 前端 `fe497a8`）。`difficultyScores[].pastCooperation` 已下发：每人 12 条真实合作记录（真实合作者姓名 + 真实 co_paper_count 次数，如 176/189）→ 合作表姓名/次数列可演、点行联动网络图高亮可演；**机构列已接真**：collaborator_talent_id join 主档 current_institution_ids→机构名，138/180 实名（南京大学/University of Pennsylvania/南开大学/Duke/Texas A&M 等，反查不到留空不编造），edu 网关实测 + 浏览器实测表格 PASS；`outcome`/`conflict`/项目名仍无源留空（`co_project_count` 久新全空，实探确认真无源），空态为期望行为 |
| 313 | 难度预测 Tab · 个人科研活跃度与合作网络分析 | 合作网络力导向图；活跃度指标 | 打开难度 Tab / 拖动网络 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 网络节点与边为真实合作数据，可缩放与下钻；活跃度指标无源时该指标显示空态，不编造活跃度分 | ✅可演（2026-11-08 升档：已修复，commit `df225ed` + pipeline 4308 全绿）。难度 Tab 网络图取 `difficultyScores[].network`，实测每人 13 节点（本人 + 12 真实合作者）/ 12 边（「论文合作 N 次」，权重=真实 co_paper_count）→ 力导向图真实可演、可缩放下钻；无合作边者返回空交前端空态；活跃度因子 activity=100.0 真实可演 |
| 314 | 难度预测 Tab · 引进阻力量化评分 | 难度面板标题；综合评分 | hover 标题 ⓘ / 查看评分 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 综合难度评分及主要阻力来源；模型未建（T7）时显示空态与「模型未建」说明，禁止用招入推荐匹配度顶替 | ✅可演（2026-11-10 M4 复跑转真实出数）。T7 模型已建：overall 0–100 出数（35.97–84.32，15 人区分度足）；主要阻力来源按 5 真实因子最低项可讲；无源三因子显式 NO_SOURCE；禁止用推荐匹配度顶替综合难度（不变） |
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
| 327 | 尽调 Tab · 动态跟踪与更新 | 刷新按钮；时间戳 | 点刷新 | `GET /display/v1/talent/recommend/dataset?force=1` | `force=1` 强制重取（穿透 dataset 缓存与久新 SQL 缓存） | 推荐卡与画像的更新时间戳刷新；后端无实时推送时标注「页面重取」，不虚构新成果或新履历 | ✅可演（2026-11-09 发布后实测）。`force=1` 全链路已上线：不带 force 的普通请求命中整页缓存 **2.4s**，带 force **32.5–38.3s** → 双缓存穿透成立；真机点「动态跟踪与更新」实测请求 `/talent/recommend/dataset?force=1` → **200 / 32.5s**，按钮期间 loading，成功提示带 `recommendations[].updatedAt`。R1 的「假刷新」判定撤销。**操作前提**：浏览器旧 JS chunk 会让按钮退化为不带 force 的请求，现场演示前须强刷（Ctrl+Shift+R） |
| 328 | 尽调 Tab · 风险与合规性评估 | 风险类型（合作风险 / 学术诚信 / 成果有效性 / IP） | 打开风险区 / 切换风险类型 | `GET /display/v1/talent/recommend/dataset` | 无查询参数；取 `risks` | 四类风险分别展示评估结果与依据；`risks` 无源时该区显示空态并注明「无风险数据」，绝不显示「无风险」结论 | ✅可演（空态演示）。recommendations[].risks 四类（cooperation/integrity/validity/ip）全 NO_DATA、riskLevel=NO_DATA → 风险区空态注明「无风险数据」，绝不显示「无风险」结论 |
| 329 | 尽调 Tab · 团队组合与协同分析 | 对比对象（2 人及以上）；并行尽调队列；团队分析入口 | 点「对比」/ 打开并行队列 | `GET /display/v1/talent/recommend/dataset` | 无查询参数 | 展示协同度评分、学科覆盖缺口、角色互补与两两协同表；团队协同模型未建时显示空态，禁用合作网络边密度顶替协同度 | ✅可演（空态演示）。团队协同模型未建（RECRUIT_025 无源）；前端 teamSynergy 红问号锚点已在（TalentComparePanel），协同度空态，禁用合作网络边密度顶替 |

## LOOP 对照汇总（M3 · 2026-11-08 首次实测）

**接口实测**：`GET /display/v1/talent/recommend/dataset`（网关 `http://10.50.69.111:30895`，StripPrefix=1，headers `Authorization: Bearer <token>` + `systemCode: display`）→ **HTTP 200 / 13.4s / code=0 / 437KB**；响应中**无 emptyReason**（区别于 DS-13 实测时的 DOWNSTREAM_UNREACHABLE，本次 gkx_show_service→久新 Doris 链路连通、数据真实）。数据集规模：`talents=15`、`recommendations=8`、`contributionScores=15`、`difficultyScores=15`、`costEstimates=15`。322/325 无独立端点（前端本地生成），未触发写操作。

| 判定 | 行数 | 序号 |
| --- | --- | --- |
| ✅ 可演（真实数据支撑） | 9 | 305、306、312、313、323、324、325、326、327 |
| ✅ 可演（空态演示，501 档语义） | 14 | 309、310、311、314、315、316、317、318、319、320、321、322、328、329 |
| ⚠️ 部分可演 | 2 | 307、308 |
| ❌ 覆盖不到 | 0 | — |
| blocked 待开发完成 | 0 | — |

合计 25 行，全部对上（2026-11-08 升档：313 随 network nodes+links 修复由 ⚠️ 升 ✅，后端 `df225ed` + pipeline 4308 全绿实测 13 节点/12 边；2026-11-09 升档：312 随机构列修复由 ⚠️ 升 ✅，后端 `ef1004b` + edu 网关实测机构 138/180 实名 + 前端 `fe497a8` 浏览器实测表格 PASS）。难度 / 成本两 Tab 按 M1 备注 3「结构保留 + 空态」501 档语义演示：控件与面板保留、结果区空态、红问号锚点已在（前端 `recommendMetrics.ts` 的 `FACTOR_MISSING` / `RECOMMEND_MISSING_METRICS`）。

**2026-11-09 327 复核（发布后实测，R1「假刷新」判定撤销）**

- 接口侧（edu 网关，`GET /display/v1/talent/recommend/dataset`）：普通请求 **2.4s**（命中整页 TTL 缓存）vs `?force=1` **38.3s**（穿透 dataset + 久新 SQL 双层缓存）→ force 语义真实生效。
- 页面侧（`/tid/talent/talent-introduction-evaluation` → 第 4 Tab「人才尽调报告与推荐」→「动态跟踪与更新」）：强刷后点击，实际请求 `/talent/recommend/dataset?force=1` → **200 / 32.5s**，按钮期间 disabled+loading，成功后由父级回填并提示画像时间。
- 首轮未强刷时实测请求**不带** force=1（旧 JS chunk）→ 现场演示前置条件：强刷一次或确认 `index.html` 不缓存。
- 判定维持 25 行 **23 可演 / 2 部分 / 0 覆盖不到**；327 由「⚠ 待发布复核」转 **✅**（下方汇总表此前已将其计入可演，本次补齐发布后判定依据）。

**实测要点**：
- 真实：15 名 MVP 人才全档（教育/履历/近作 5 篇/荣誉/合作网络 13 节点含真实合作次数）；recommendations 双分口径真实（aiScore 能力 `ta_recommend_self_v1`、matchScore 学科匹配，updatedAt=2026-11-06）；contributionScores 论文/影响/网络分真实、trend 2015–2025 真实活跃指数、sources 计数真实。
- 无源（诚实 0/空，演示按空态讲）：难度 7 因子（仅 activity=100.0 真实、level=PARTIAL_DATA、overall=0）、strategies 全空、costEstimate 全族 NO_DATA、risks 四类 NO_DATA、overseasVisits 空、nlpFieldProfile=NOT_BUILT、socialInfluence 仅 mediaMentions 真实。（pastCooperation / network 已于 2026-11-08 修复下发，`df225ed`）
- 派生（现场需知）：贡献热力 `fieldGain` 为空，热力值由前端按 avg（真实）+ fields 归属规则派生；预测视图为前端演示规则投影（trend×固定系数），非模型产出；`contributionScores[].collaborators` 姓名未解析（显示 tal_xxx id，现场不点名）。

## LOOP 对照汇总（R1 · 2026-11-09 生产实测）

同一端点生产复跑（同一网关 / token / 头），**HTTP 200 / 21.7s / 466.6KB / `code=0`**，无 `emptyReason`。25 行全量对照结论与 M3 一致：**9 真实可演 + 14 空态可演 + 2 部分可演 + 0 覆盖不到**，无新增缺口。

| 维度 | R1 实测 | 与 M3 对比 |
|---|---|---|
| 数据集规模 | talents=15、recommendations=8、contributionScores=15、difficultyScores=15、costEstimates=15 | 一致 |
| 313 合作网络 | `difficultyScores[].network` 键为 `nodes`/`links`；**15 人逐人 13 节点 / 12 links**，link 名如「论文合作 176 次」 | R1 首次逐人核，15/15 全一致 → 升档成立 |
| 312 过往合作 | pastCooperation 共 **180 条**；机构名 **138/180 实名**；`co_project_count` **0/180**；样本 `{year:2025, partner:"Dingsheng Wang", institution:"清华大学", times:176, output:"联合论文 176 篇"}` | 机构列已接真；项目名/成果/冲突确认真无源（0/180，不编造） |
| 评分口径 | rec[0] 李亚栋 aiScore 99.0054 / matchScore 75.98171；updatedAt=2026-11-06 | 一致 |
| 难度 / 成本 / 风险 | activity=100.0 ×15；risks NO_DATA 8/8；strategies 全空；cost 全 0（15/15） | 一致（空态语义维持） |

**新观察：性能**。21.7s 较 M3 13.4s 变慢约 60%，仍在 60s 阈值内，演示前须预热。

**R1 浏览器实测（2026-11-09 前端，lumen-ui-science-pc）**：305–329 逐行实测通过（贡献度三层互斥/真实指标条；尽调李亚栋 aiScore 99.0/岗位匹配 76%、报告六段、风险「无风险评估数据源」、推荐卡 matchScore 降序、updatedAt=2026-11-06；307 自动深度分析弹窗；315 演示规则提示通用文案）。发现 3 处前端与用例承诺不符并已修根因（修复后 type-check/自检/build 三绿 + 浏览器复验 PASS，commit 待推）：

1. **难度 Tab（308/314/309–311/312）**：`level=PARTIAL_DATA` 绿标+仪表盘 0 分（违反 314「模型未建」承诺）→ 灰标「模型未建」+仪表盘「—」；communication/culture/mobility 无源因子以 0 分红「需关注」条呈现（违反 309–311「不以 0 分呈现」）→ 「—」+「无数据」灰态；312 点行联动网络高亮补齐（合作者节点蓝框+相连边加粗变蓝，数据层复验 PASS）；合作表 row-key 由 year（12 行同 2025 键重复）改 partner。
2. **成本 Tab（316–322）**：真机全 0 以「¥0 万」当真实成本展示、导出按钮未拦截（违反 316「不展示金额」/322「导出空模板并提示无成本数据」）→ 整页「模型未建」空态（`predictedTotal>0` 为有数据信号，全 15 人全 0 故恒空态），空态页无导出按钮。
3. **329 团队协同**：`synergyScore=60+n*8`、`pairScore=55+互补*40` 演示公式分顶替协同度（违反 A18「禁用任何口径顶替」）、角色按数组下标派名、aiScore `||70` 兜底 → 协同度灰标「模型未建」（面板+报告弹窗），两两只列真实 fieldLabels 共享方向不出分，未入推荐集不显评分（324）。

**结论**：25 行零阻断，307/308 部分可演与 14 行空态均属 M4 裁定口径 → **已签收（2026-11-09，监管人 human:李伟；验收单 TA-DS16-DEMO-ACCEPT-LOOP → done）**。遗留口径：风险/成本/专利/论文全族无源走空态（co_project_count 0/180 确认真无源），演示前预热（冷跑 21.7s）。

## 缺口建单（M3 · 2026-11-08）

| 关联行 | 缺口 | 根因 | 处置建议 |
| --- | --- | --- | --- |
| 307 | 预测视图无真源预测模型 | 无预测模型数据源；前端按演示规则对真实 trend 投影 | 引用既有缺口口径登记；演示按「规则投影」讲，不得讲成模型预测 |
| 308、314 | 综合难度模型 T7 未建 | difficultyEstimate 仅 activity 有源（PARTIAL_DATA），其余 7 因子=0、overall=0 | 引用既有 T7 / IP-10；模型未建前按「模型未建」空态演示，禁止把仪表盘 0 分讲成难度低 |
| 312 | 过往合作表无源 | `difficultyScores[].pastCooperation` 全 15 人空数组（机构/项目/次数/时间表结构无源） | **✅ 已修复（2026-11-08，commit `df225ed`，pipeline 4308 全绿）**：pastCooperation 从主档 collaborationNetwork 真实合作边组装，实测每人 12 条（真实合作者姓名 + 真实 co_paper_count 次数，如 176/189）；**机构列 2026-11-09 已修复（commit `ef1004b`）**：collaborator_talent_id join 主档 current_institution_ids→机构名，edu 网关实测 138/180 实名（反查不到留空），前端 `fe497a8` 浏览器实测表格 PASS → 312 升 ✅可演；`outcome`/`conflict`/项目名仍无源留空（`co_project_count` 久新实探全空，真无源），不编造 |
| 313 | 难度 Tab 合作网络空 | `difficultyScores[].network` 全空；主档 collaborationNetwork 节点真实但 links 边未下发 | **✅ 已修复（2026-11-08，同上 commit）**：network 下发 nodes（本人+合作者）+ links（「论文合作 N 次」，权重=真实合作次数），实测 13 节点/12 边；无合作边者返回空交前端空态 |
| 316–322 | 成本全族 NO_DATA | 无薪资源（dwd_org_recruit_info 未入久新），T12/T13 成本模型未建 | 引用既有 DN-A15-COST；501 档空态演示 |
| 328 | 风险四类无源 | risks 全 NO_DATA（合作/诚信/有效性/IP 评估未建） | 引用既有 IP-10；空态注明「无风险数据」，绝不显示「无风险」 |
| 329 | 团队协同无源 | RECRUIT_025 协同度模型未建 | 引用既有；协同度空态，禁用合作网络边密度顶替 |

**演示诚实性红线（现场不得改口）**：aiScore ≠ matchScore 两套口径不得合并；projects/patents 贡献分=0 是无评分源、计数另列真实值；难度 overall=0 是「模型未建」不是「难度低」；成本全 0 是「无数据源」不是「免费」；risks NO_DATA 不是「无风险」；预测视图为前端规则投影非模型产出。

### 裁定回写（M4 裁定单 · 授权人李伟，2026-11-09）

> 以下为最终裁定，与本页「处置建议」冲突时以本表为准；`A1x` 对应裁定单附录 A。

| 关联行 | 裁定 |
|---|---|
| 312 过往合作表 | ✅ 已修复并实测通过（每人 12 条真实合作记录、机构列 138/180 实名）→ 可演；项目名/成果/冲突仍无源留空 |
| 313 难度 Tab 合作网络 | ✅ 已修复并实测通过（13 节点 / 12 真实权重边）→ 可演 |
| 308/314 综合难度模型 T7 | ✏️ **改为修复**（A15，算法建 T7 综合难度模型，activity 已有源）；未建成前维持 501 空态，`overall=0` 禁讲「难度低」 |
| 307 预测视图 | ✅ 不演（A14）：按「规则投影」讲，禁说模型预测 |
| 316–322 成本全族 | ✅ 不演（A16）：无薪资源，成本空态，禁讲「免费」 |
| 328 风险四类 | ✅ 不演（A17）：无风险数据 ≠ 无风险，须原话注明 |
| 329 团队协同 | ✅ 不演（A18）：RECRUIT_025 未建，禁用合作网络边密度顶替 |

## 备注与风险

1. **久新实探结论与契约口径**：推荐集 = 15 名 MVP 人才内按能力分 Top8（每个推荐项在 `talents[]` 有完整主档）；`aiScore` = `ads_talent_capability_assessment` 学术能力分（口径 `ta_recommend_self_v1`），`matchScore` = `ads_talent_research_problem_discipline_match` 最佳问题学科匹配分（1,142,501 行）；`matchReasons` 产业力理由来自 `industrial_capability_industry_score`（6/15 人有分）+ `ads_industry` 主行业名；`sources` 计数全部真实；`contributionScores` 五维中 projects / patents 无评分源（分值为 0，计数真实另给）。
2. **明确无源 / 空态项**：`difficultyEstimate` 仅 `factors.activity` 有真实百分位（其余 7 因子 0，T7 未建）；`costEstimate` 全部 NO_DATA（无薪资源，`dwd_org_recruit_info` 未入久新，T12 / T13 未建）；`risks`（合作 / 诚信 / 有效性 / IP）无源 → null；团队协同（`RECRUIT_025`）无源；出访与海外交流无源。对应行（308–311、314–322、328、329）**不得写成可演金额或风险结论**。
3. **演示语义约束**：难度 / 成本 Tab 按「501 档语义」处理（页面保留结构与控件，结果区空态）；诚信 / 政治 / 情感类演示分带 `nature` 字段，禁止裸展示分数，禁止用于筛选决策。307 的「预测视图」与 321 的「决策建议」无模型时必须空态。
4. **契约未闭合项**：评估目标下拉、当前评估对象候选、定制尽调维度选项的枚举未在 SRS 或契约中固定（由 `talentRecommendSpec` 与页面枚举提供），M2 需补全集；`326` 的「匹配方式」随评估目标联动映射（`EVALUATE_TARGET_TAB` / `TARGET_TO_ORG_NEED`）属前端冻结语义，需在 M3 核对口径；导出 / 报告均无后端端点，为前端打印页或 CSV 本地生成。
5. **页面不重做**：WBS-05-03a / 03b 只做菜单壳与非三要素区块，四子页不重做；供数归 WBS-02-01，技术方案 §1.2 记「非三要素区块的对接对象清单：还没有」。
