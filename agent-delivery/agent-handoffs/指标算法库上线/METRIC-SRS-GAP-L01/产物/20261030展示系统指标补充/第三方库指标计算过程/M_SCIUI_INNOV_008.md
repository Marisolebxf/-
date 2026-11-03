# 指标趋势预测值（M_SCIUI_INNOV_008）

> **类型**：FORECAST（外推预测值，含置信区间）｜ **域**：科技发展态势·全球创新监测·趋势预测（能力）+ 科技创新评估·科学创造力指标展示＞趋势预测（指标族）｜ **UI 挂载**：全球创新监测能力卡 `globalInnovationMonitor.js:21` + 创新趋势分析图（`realtimeModel.js:29` 前 15 月实测/末 3 月预测）+ 科技创新评估new（`TechInnovationEvaluationNewPage.jsx:97/119` 趋势预测指标卡与 95% 置信区间图）
> **数据支持度**：**部分支持**｜ **公式定义人**：推测定义（Hyndman FPP3 ETS 框架）｜ **口径归属**：UI 推测叶（SRS 未出现该指标名；科技创新评估页 seq 139/145 明写"预测结果和置信区间"但挂另页）
> **复现脚本**：`code/M_SCIUI_INNOV_008.py`｜ **产物**：`code/M_SCIUI_INNOV_008_out.json`
> **四判定摘要**：直接结构 = 部分（久新 forecast_yearly 有预测面但 LLM 情景估计非统计外推）；直接数据 = 部分（4,872 行全带置信区间但 backtest 0 行）；依赖结构 = 是（三源年度序列充足可自建模型）；依赖数据 = 部分（序列短/在途年/统计模型级结果面三源均无）
> **数据源口径**：开发库（gkxlumenx_*，10.50.11.76，禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新库（jiuxin Doris 47.93.119.170:29030，gkx_technology_analysis_dev，只读）

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库 gkx+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 表面上久新库有现成预测结果面（`ads_research_problem_forecast_yearly` 4,872 行，406 问题 × 4 指标 × 2026–2028，且**全部带上下界**），实测其方法列后发现三个硬伤：`forecast_method` 全量为 `LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED`（DeepSeek 情景估计）、`backtest_error` 0/4,872 非空（**零回测**）、`coverage_status` 全量 `AI_ESTIMATED_NOT_BACKTESTED`——久新建库方自己就把这批数据登记为"AI 估计非回测"，与 SRS seq 139 明文要求的"基于历史数据和算法模型，预测……用户可查看**预测结果和置信区间**"（统计模型 + 区间语义）不同族。统计模型级的预测面三源均无（dev 预测表 0 命中；gkx 无预测承载），但自建依赖（年度序列）充足：本件用 gkx 融资 2015–2025 序列跑通 Holt 线性趋势 + ETS(A,A,N) 解析预测区间（2026 点预测 575.25，95% 区间 [0, 2819.84]），证明"建模可行性"没问题，缺的是**已回测的落库结果面**——判部分支持，升档触发器两条（§1.6）。

### 批次通用纪律摘要（20261101 批 S3-01 Lane 6 五件共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 预测对照比的分子分母同池（gkx 序列自派生） |
| B4 | 负结论带探针 | dev forecast/predict 表扫描 absence_probe 留证（含 policy_prediction_indicator 误命中甄别） |
| B5 | 确定性 | Holt α=0.8/β=0.2 固定参数；无随机初始化 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 改脚本→重跑，产物零手改 |
| B8 | 回执不复收 | 硬证据本件实跑（三源连接记录在案） |
| B9 | 单位/日期陷阱 | 训练窗排除在途年；training_end_date 抽样核验 |
| B10 | 口径裁定保守交付 | LLM 情景 vs 统计外推双口径并列 + 升档触发器写死 |
| B11 | 多本账互推 | gkx 融资年度序列与 INNOV_006 同源同值（B11 批内一致） |
| W2-1 | 先读资产再发 SQL | 共享快照 + lane6 探针（forecast 表 4,872 行发现）消费后才写脚本 |
| W2-2 | 引用不漂移 | 快照数字原值引用 |
| W2-3 | 篇幅深度对标 | 13 章节齐全 ≥20KB |
| W2-4 | 三源探针不省略 | dev/gkx/jiuxin 三源逐一留证（§三/附录 B） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 有现成预测结果面吗？ | 有但方法不符 | 久新 forecast_yearly 4,872 行，LLM 情景估计非统计外推（facts.jiuxin_forecast_method_coverage） |
| 现成面可回测吗？ | 不可 | backtest_error 0/4,872（facts.jiuxin_forecast_backtested_rows=0） |
| 自建模型可落吗？ | 序列可、结果面无 | Holt 演示跑通（facts.gkx_holt_* 键）；三源无统计预测落库面 |

## 摘要

「指标趋势预测值」是全球创新监测"趋势预测"能力的核心读数：监测页创新趋势图把 18 个月序列切成"前 15 个月实测 + 末 3 个月预测"（虚线 + 热力图"预测值"标记，`realtimeModel.js:29/110-125`），科技创新评估new 页更给出完整的"历史趋势 + 预测趋势 + 95% 置信区间"三线图（`TechInnovationEvaluationNewPage.jsx:563-580`，预测至 2030E）——UI 对预测的需求语义是**统计外推 + 区间量化**。数据侧实测出本批最重要的发现之一：久新 `ads_research_problem_forecast_yearly` 并非 schema 声明的零行空表，实际有 4,872 行（DeepSeek 情景估计，2026-10-24 生成），全部带上下界与完整 LLM 溯源五件套（provider/model/prompt_version/input_hash/generated_at）——建库方工程纪律良好，但方法登记明示 `NOT_BACKTESTED`（回测误差 0 行覆盖），与需求的统计模型语义不同族。本件以 gkx 融资 2015–2025 年度序列演示 Holt/ETS 统计外推全流程（点预测 575.25、95% 区间 [0, 2819.84]——区间宽即序列波动大的诚实量化），证明建模路径通畅，缺的是回测流水线与落库面。判**部分支持**，两条升档触发器写死。

- 需求判定：**UI 推测叶**（本页 SRS 未出现「指标趋势预测值」；科技创新评估 seq 139/145 明写预测+置信区间但挂另页，可作语义真源引用）。
- 复现状态：脚本已跑通；久新预测面解剖 + Holt 演示 + dev 缺席探针三组证据落产物。
- 档位结论：**部分支持**（现成面方法不符 + 统计级结果面三源无 + 自建序列充足——差一步建模落库）。
- 关键事实：久新 4,872 行预测面的 `forecast_method` 全量 `LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED`、回测误差 0 行——方法登记诚实但与需求语义错位。
- 升档路径：①自建统计模型 + 回测流水线落库 → 完全转换支持；②甲方接受 LLM 情景估计作预测值 → 久新面直查升档（UI 须标注非统计预测）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/全球创新监测/**趋势预测能力**（SRS bid_desc"利用数据模型开展趋势预测和判断"；UI `globalInnovationMonitor.js:21` 能力卡"跟踪时间序列、阶段变化和未来增长窗口"）。预测读数在监测页有两个具体形态：其一是创新趋势分析图（`InnovationRealtime.jsx` 引 `realtimeModel.js` 的 `buildRealtimeTrendSeries`），18 个月（2025-04 至 2026-09）的专利/论文/投资额三线，`REALTIME_TREND_MEASURED_COUNT=15` 把序列切成实测段与预测段，预测段以虚线渲染、tooltip 标"预测值"——**UI 代码明写了预测的呈现契约（区分实测/预测）**；其二是科技创新评估new 页的 `buildForecastOption`（`TechInnovationEvaluationNewPage.jsx:563-580`）：历史趋势实线 2020–2025 + 预测趋势虚线 2026E–2030E + 95% 置信区间带（stack 面积图），预测 5 年、逐年 +4 到 +11 分——**这是 UI 里最完整的预测可视化规格**。mock 值是 UI 需求证据（演示值，不参与支持度结论）：预测段斜率为正（增长假设）、区间随 horizon 展宽（不确定性递增的视觉表达）、2030E 上界 clamp 至 100（评分体系封顶）。

### 1.2 为什么需要本指标

监测系统的完整闭环是"观察→解释→预判"：前两步由存量指标（专利数/投资额/增长率）承担，第三步需要预测值——用户决策（布局/撤出/加码）的依据不是"现在多少"而是"未来会怎样"。置信区间是预测的诚信组件：Hyndman 教科书原话"点预测若没有预测区间几乎没有价值，因为无法知道预测有多准"（R2 §5）。UI 作者显然理解这一点——评估页的 95% 区间带是三线图的标准配置而非装饰。对全球创新监测场景，预测的典型问法是"这个领域的论文产出明年还会涨吗""投资热度下个季度见底吗"——都要求可回测的方法（能算历史误差），这正是 LLM 情景估计给不了的（无法定义训练集/测试集切分）。

### 1.3 需求文档是否给出定义方法

**需求文档提及了功能但没给出算法。**「指标趋势预测值」全称在三份 SRS 与主文档 rg 未命中（`named_in_srs=false`，检索记录见附录 A）。但语义真源存在于科技创新评估页 SRS：seq 139「科学创造力趋势预测」原文"**基于历史数据和算法模型，预测特定领域科学创造力的未来发展趋势，用户可查看预测结果和置信区间，为长期科研规划提供参考**"——这句话闭合了预测的四要素（历史数据/算法模型/预测结果/置信区间）；seq 145「技术创新趋势预测」同构。全球创新监测页侧，bid_desc（seq 56）"利用数据模型开展趋势预测和判断"给了能力级要求。综合：需求要求的是**算法模型级预测 + 区间**，无具体算法指定（ARIMA/ETS/Prophet/ML 均可满足"算法模型"字面）。

### 1.4 类似指标权威方法可行性分析概要

预测方法论在统计 forecast 领域有标准教科书答案。Hyndman & Athanasopoulos《Forecasting: Principles and Practice》FPP3（R2）：Holt 线性趋势法点预测 ŷ_{T+h|T} = ℓ_T + h·b_T，其 ETS(A,A,N) 状态空间模型的 h 步预测方差 σ_h² = σ²[1+(h−1){α²+αβh+β²h(2h−1)/6}]，95% 区间 ŷ ± 1.96·σ_h。方法族对照：

| 方法族 | 代表 | 点预测 | 区间 | 数据要求 | 与本库匹配 |
|---|---|---|---|---|---|
| ETS 指数平滑（Holt） | Hyndman FPP3 §8（R2） | ℓ_T+hb_T | 解析方差 | 年度序列 ≥8 点 | gkx 11 点/久新 30+ 点序列**够** |
| ARIMA | FPP3 §9 | 差分自回归 | 解析/模拟 | 同上 | 同上 |
| LLM 情景估计 | DeepSeek（久新现状） | 语言模型生成数 | 生成上下界 | 文本描述 | **已存在但非统计外推** |
| 组合预测（ETS+ARIMA 均值） | FPP3 §13 | 组合 | 模拟路径 | 同上 | 可选增强 |

结论：统计路线（ETS/ARIMA）对年度序列完全可行且区间公式现成；本件演示采用 Holt（趋势明显的下行序列最适配线性趋势模型）。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/globalInnovationMonitor.js:21` — 能力卡"innovation-trend：跟踪时间序列、阶段变化和未来增长窗口"；`realtimeModel.js:29` — `/** 创新趋势分析：2025-04 至 2026-09；前 15 个月实测，末 3 个月为预测演示 */`（注释明写预测演示）与 `REALTIME_TREND_MEASURED_COUNT = 15`；`realtimeModel.js:110-125` — 预测虚线 series（`lineStyle: { type: 'dashed' }`）。
- 组件：`repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:97` — 指标卡 `{ name: '趋势预测', fullName: '科学创造力趋势预测', score: 81, delta: '8.3%', trend: 'up' }`；`:119` — 技术创新趋势预测卡；`:563-580` — buildForecastOption 三线图（历史/预测/95% 区间，2026E–2030E，演示值不作数据证据）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/科技创新评估.md` seq 139/145（预测结果和置信区间——语义真源）；`全球创新监测.md`:13 bid_desc（利用数据模型开展趋势预测和判断）；`科技全域态势.md`:206（支持趋势预测功能，通用能力）。

### 1.6 推测定义与降档/升档触发器

**推测定义（双口径并列，B10）**：

- **口径 A（统计外推，主口径——对齐 SRS seq 139 语义）**：ŷ_{T+h} = ℓ_T + h·b_T（Holt），95% 区间 ŷ ± 1.96·σ_h（ETS(A,A,N) 解析方差）；训练窗=全量历史年（排除在途年）；交付前必须过回测（时间切分，报告历史误差）。
- **口径 B（LLM 情景估计，久新现状）**：直接消费 `ads_research_problem_forecast_yearly`（DeepSeek 生成，带区间与溯源）；UI 必须标注"AI 情景估计，非统计预测，未回测"。

**降档/升档触发器（B10 模板）**：现状部分支持；若自建 ETS/ARIMA + 回测流水线落库（工程量一次建模脚本）→ **升完全转换支持**；若甲方接受口径 B → **升完全直接支持**（久新面直查，但 UI 标注义务随行）；若要求月度粒度预测 → 久新月度面 PARTIAL、gkx 月度序列需评估后再定档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | 全球创新监测.md（能力级）+ 科技创新评估.md（指标级语义真源） |
| 本件挂靠叶 | 全球创新监测 bid_desc 趋势预测能力；科技创新评估 seq 139/145（跨页同族） |
| 相近叶 | 创新影响预测（seq 71，预测对象为创新影响/贡献度——非指标趋势）；科技全域态势.md:206 趋势预测功能 |
| UI 容器 | `InnovationRealtime.jsx` 趋势图 + `TechInnovationEvaluationNewPage.jsx` 预测三线图 |
| 批内姊妹件 | INNOV_006（增长率=回顾差分，本件=前瞻外推，共享年度序列底座）；INNOV_002（趋势演进=序列本体） |

本件与 INNOV_006 构成时间轴上的对偶件：006 算已发生的变化率，本件外推未发生的值；两件共享"指标所指不闭合"的口径风险（UI 的预测对象分别是专利/论文/投资额月序列与科学创造力得分）。

## 二、计算过程

### 2.1 装载与规模校验

gkx 融资年度序列与 INNOV_006 同源同值（2015–2025 十一年，B11 批内零漂移）；久新预测面 4,872 行（发现过程：ADS_SCHEMA-5.11.0.md §27.4 声明"未来三年预测表在模型训练与回测完成前保持空表"，lane6 第一轮探针实测 4,872 行——**schema 快照（2026-10-22）与实库（2026-11-01）已发生回填漂移**，产物 `jiuxin_forecast_rows=4872` 为准）；dev 预测表扫描 0 命中（`policy_prediction_indicator` 为政策模拟参数表，已甄别排除，见 §3.4）。

### 2.2 久新现成预测面解剖（本件核心证据）

`ads_research_problem_forecast_yearly` 4,872 行 = 406 问题 × 4 指标（PAPER_COUNT/PATENT_COUNT/PROJECT_COUNT/HOTSPOT_SCORE 各 1,218 行）× 预测年 2026–2028。三组关键读数：其一，**全部带区间**（lower_bound/upper_bound 非空 4,872/4,872，confidence_level 0.30–0.35）；其二，**方法全量登记**为 `LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED`，coverage 全量 `AI_ESTIMATED_NOT_BACKTESTED`（`facts.jiuxin_forecast_method_coverage` 单键即全量 4,872）——LLM 情景估计且未回测；其三，**回测误差零覆盖**（backtest_error 0/4,872）。溯源五件套完整：`inference_provider='deepseek-openai-compatible'`、`inference_model='deepseek-flash'`、`inference_prompt_version='research_problem_deepseek_decision_v1'`、`inference_input_hash`、`inference_generated_at`（样例 2026-10-20 07:15:28）。PAPER_COUNT 2026 预测值分布 min 0 / avg 2.17 / max 14（问题粒度的小数值是 LLM 对"问题级论文增量"的估计量级）。

这组证据的判档含义分两层：工程层——久新的表结构就是为统计预测设计的（training_end_date/forecast_horizon/backtest_error 列全在，schema §27.4 明写"在模型训练与回测完成前保持空表"），LLM 填充是过渡态；语义层——现填充内容不满足 SRS seq 139 的"算法模型"语义（LLM 情景估计不可回测、无训练/测试切分概念），**表在而语义不符**，这是"部分支持"而非"直接支持"的精确理由。

### 2.3 gkx 序列外推演示：Holt 点预测

对 gkx 融资年度序列（2015–2025，x = [2602, 3884, 2909, 2257, 1666, 1948, 2019, 1757, 1266, 919, 618]）拟合 Holt 线性趋势（α=0.8, β=0.2，固定参数保证确定性 B5）：终态 level ℓ_T = 687.81、trend b_T = −112.56（`facts.gkx_holt_level_2025`/`gkx_holt_trend_2025`）。2026 点预测 ŷ = 687.81 + 1×(−112.56) = **575.25**（`facts.gkx_holt_forecast_2026_point`）——趋势延续判断为继续下行（与 INNOV_006 的同比序列 −32.75% 方向一致，模型内部一致性互证）。

```python
# Holt 线性趋势（固定 α/β，B5 确定性；训练窗排除在途年 2026）
alpha, beta = 0.8, 0.2
l, b = vals[0], vals[1] - vals[0]
for v in vals[1:]:
    l_new = alpha * v + (1 - alpha) * (l + b)
    b = beta * (l_new - l) + (1 - beta) * b
    l = l_new
point_2026 = l + 1 * b  # → 575.25
```

### 2.4 ETS(A,A,N) 解析预测区间

残差方差 σ² 由拟合残差估计（σ = 1,145.20，`facts.gkx_holt_residual_sigma`）；h=1 步预测方差 σ_h² = σ²[1+(h−1){…}] 退化为 σ²。95% 区间 = 575.25 ± 1.96×1145.20 = [−1671.4, 2819.8]，下界截 0 后 **[0, 2819.84]**（`facts.gkx_holt_forecast_2026_lo95/hi95`）。区间宽度占点预测 **489.9%**（`derived.gkx_holt_2026_ci_width_pct`）——这个"难看"的数字恰是本件方法论论证的价值所在：融资事件序列波动剧烈（2016→2019 三年腰斩再反弹），任何诚实的外推都必须给出这么宽的区间；UI mock 的窄区间带（±7 分）只适用于平滑评分序列，不适用于事件计数序列。**区间宽度是数据面的诚实属性，不是模型缺陷**——交付时若甲方嫌区间宽，正解是换平滑指标（如移动平均序列）而非压缩区间。

### 2.5 稳健性与口径敏感性

三个敏感性披露：**参数选择**——α/β 固定为经典值 0.8/0.2 未做网格优化，正式建模应按 AICc 选参（FPP3 §8.5），点预测会随参数小幅漂移（方向判断稳定）；**训练窗**——2015 起算 vs 2018 起算的 trend 估计不同（序列前段是爬坡、后段是下行），窗口敏感性需在回测中量化；**在途年排除**——2026 的 238 事件是部分年度读数，混入训练会把 trend 拉向深负（假信号），全程排除（B9）。

### 2.6 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_008.py`（gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读；Holt+ETS 区间纯 Python 实现无第三方依赖；运行 `python3 code/M_SCIUI_INNOV_008.py`）。
- 产物：`code/M_SCIUI_INNOV_008_out.json`。正文数字与产物键逐一对应：`jiuxin_forecast_rows=4872` / `jiuxin_forecast_by_metric`（§2.2 四指标分布）/ `jiuxin_forecast_method_coverage`（§2.2 全量 LLM）/ `jiuxin_forecast_backtested_rows=0`（§2.2）/ `jiuxin_forecast_paper_2026_min_avg_max=[0,2.17,14]`（§2.2）/ `gkx_financing_yearly_2015_2025`（§2.3 序列）/ `gkx_holt_level_2025=687.81` / `gkx_holt_trend_2025=-112.56` / `gkx_holt_forecast_2026_point=575.25` / `gkx_holt_forecast_2026_lo95=0` / `gkx_holt_forecast_2026_hi95=2819.84` / `gkx_holt_residual_sigma=1145.2`（§2.3/§2.4）/ `dev_forecast_tables=0` / `dev_predict_table_names`（§2.1/§3.4）/ 派生键 `gkx_holt_2026_vs_2025_actual_pct=-6.94`（§2.3 对照）/ `gkx_holt_2026_ci_width_pct=489.9`（§2.4）。
- 结果解读：久新面解剖（表在语义不符）+ 统计演示（跑通且区间诚实）双证据链闭合；差的一步是"回测流水线 + 落库"。
- 对照需求功能要求的评审：预测结果+置信区间（seq 139）——统计口径可满足但需建模落库；LLM 口径立即可用但语义错位需甲方裁定（触发器 §1.6）。

### 2.7 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 发现 | 久新预测面行数 | `jiuxin_forecast_rows` | 4,872（schema 声明 0 已漂移） |
| 解剖 | 四指标分布 | `jiuxin_forecast_by_metric` | 各 1,218 行 × 406 问题 × 2026–2028 |
| 解剖 | 区间覆盖 | `jiuxin_forecast_by_metric[*].with_ci` | 4,872/4,872（100%） |
| 解剖 | 方法登记 | `jiuxin_forecast_method_coverage` | LLM_SCENARIO…NOT_BACKTESTED 全量 |
| 解剖 | 回测覆盖 | `jiuxin_forecast_backtested_rows` | **0**/4,872 |
| 演示 | Holt 终态 | `gkx_holt_level_2025` / `trend_2025` | 687.81 / −112.56 |
| 演示 | 2026 点预测 | `gkx_holt_forecast_2026_point` | 575.25 |
| 演示 | 95% 区间 | `gkx_holt_forecast_2026_lo95/hi95` | [0, 2819.84] |
| 演示 | 区间宽占比 | derived `gkx_holt_2026_ci_width_pct` | 489.9% |
| absence | dev 预测表 | `absence_probe[0]` | forecast 0 命中；predict 误命中已甄别 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 现成预测结果面 | jiuxin | `ads_research_problem_forecast_yearly` | 4,872 | 直查 | **有但方法不符（LLM 非回测）** |
| D2 | 年度序列（训练数据） | gkx | `dwd_org_financing_info` 按年 | 2015–2025 连续 | 直查 | **足** |
| D3 | 年度序列（长序列） | jiuxin | `ads_technology_yearly_metrics` | 1990–2026 | 直查 | 足 |
| D4 | 统计预测落库面 | 三源 | — | — | **不存在** | **缺（升档工程项）** |
| D5 | 预测承载表 | dev | forecast/predict LIKE | 0（1 误命中甄别） | **不存在** | 缺（两源已兜） |

`support_judgment="部分支持"`，与文首同档（闸 6 对齐）。

### 3.2 D1 久新预测面：表在、语义错位

§2.2 已详述。补充一点工程判断：久新的表设计（training_end_date/backtest_error 列预留）说明建库方本来就规划了统计模型路径，LLM 填充是"先有数"的过渡方案——`forecast_method` 列的枚举值设计（LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED）为将来接入统计模型（如 ETS_BACKTESTED）留了同一列的扩展位。本项目若自建预测落库，**直接沿用该表结构**是最省路径（升档工程量集中在建模脚本与回测流水线，不在 DDL）。

### 3.3 D2/D3 训练序列：三源充足

gkx 融资 11 点年度序列（本件演示已用）；久新 `ads_technology_yearly_metrics` 全库论文合计 1990–2026 三十多年序列（`_probe_lane6_jiuxin_out.json` 年份全分布键，与 lane1 探针一致）；`ads_emerging_topic_yearly_metrics` 4,496 主题 × 多年。序列长度对 ETS/ARIMA 均够（教科书建议 ≥8 点，FPP3）；唯一注意点是久新序列在 2020–2021 有观察池扩容跳变（论文数 4,450→9,795→23,719），外推前需做结构性断点检验或取 2021 后子窗。

### 3.4 D5 dev 缺席：absence_probe 全记录

否定性证据三件套：**查了什么**——`SHOW TABLES LIKE '%forecast%'` 与 `'%predict%'`（gkxlumenx_dwd）；**条件**——表名 LIKE 扫描；**命中**——forecast 0；predict 1（`policy_prediction_indicator`，列结构为政策模拟参数，已甄别为误命中并在探针 hit_detail 注明）。缺失情形归属：**表不存在**。dev 侧无预测承载，两源（gkx 序列 + 久新面）承担本件全部证据义务。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| schema-实库漂移 | forecast 表 schema 声明 0 行 → 实测 4,872（2026-10-24 回填，产物留证） |
| LLM 溯源五件套 | 样例行 provider/model/prompt_version/input_hash/generated_at 齐全 |
| Holt 确定性 | 固定 α/β，重跑同值 |
| 在途年排除 | 训练窗 2015–2025，2026 仅作预测目标年 |
| 区间下界截断 | 负值截 0 并在 facts 落原值轨迹 |
| 脚本形态 | 三源只读；无 demo_*；无耗时键 |

## 四、数据缺失情况

### 4.1 统计模型级预测落库面缺失（结果面级，主降档因）

三源无"已回测的统计预测结果表"：久新有表但内容为 LLM 情景估计（backtest 0 行）；gkx/dev 无预测承载。修复路径：自建 ETS/ARIMA 流水线（训练→回测→落库，沿用久新 forecast_yearly 表结构），工程量一次建模脚本 + 调度——这是升完全转换支持的全部缺口。影响面：本件 + 未来所有预测类指标（评估页 seq 139/145 同族）。

### 4.2 预测对象口径不闭合（口径级，与 INNOV_006 共享）

UI 三处预测对象各不同（监测页=专利/论文/投资额月序列；评估页=科学创造力/技术创新得分；能力卡=趋势预测功能）。若预测必须挂"得分"类指标，得分本体先要建模（INNOV_014 同族）——预测的口径依赖链比增长率更长。B10 触发器已含此分支。

### 4.3 月度粒度预测的数据缺口（粒度级，披露项）

UI 监测页的预测段是月粒度（末 3 个月）；久新月度面 `ads_research_problem_monthly_metrics` 91,520 行实测有数（coverage PARTIAL_REAL_MONTHLY_FACT，引文月度资金不可得），gkx 月度序列可从 completion_date 聚合——月粒度可做但覆盖率与断点需逐序列评估，正式立项前不给档位承诺。

### 4.4 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 自建统计预测流水线（建模+回测+落库） | 工程 | 本件 + seq 139/145 族 | 升完全转换支持；沿用久新表结构 |
| 口径裁定（统计 vs LLM 情景） | 口径裁定 | 本件 | B10 触发器；LLM 口径 UI 须标注非统计预测 |
| 序列断点检验（久新 2020–2021 跳变） | 建模前置 | 本件 | 扩容跳变误当趋势的风险 |
| 月粒度预测专项评估 | 立项评估 | 本件 | UI 月粒度需求的数据面适配性 |

## 参考文献

1. Forecasting: Principles and Practice (3rd ed) §8 Exponential smoothing[EB/OL]. Hyndman & Athanasopoulos. https://otexts.com/fpp3/exponential-smoothing.html （R2，Holt 线性趋势与 ETS 框架，2026-11-01 WebSearch 核验可达）
2. Forecasting: Principles and Practice (3rd ed) §8.7 Forecasting with ETS models[EB/OL]. https://otexts.com/fpp3/ets-forecasting.html （R2b，预测区间公式与模拟路径，2026-11-01 WebSearch 核验可达）
3. Forecasting: Principles and Practice (3rd ed) §5 The forecaster's toolbox[EB/OL]. https://otexts.com/fpp3/toolbox.html （R2c，"点预测无区间几乎无价值"方法论，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「指标趋势预测值」在三份 SRS 与主文档均未出现（`named_in_srs=false`）。语义真源（科技创新评估页，跨页同族）：

SRS《02-科技信息展示系统/科技发展态势/科技创新评估.md》seq 139（excel_row 142）：

> 基于历史数据和算法模型，预测特定领域科学创造力的未来发展趋势，用户可查看预测结果和置信区间，为长期科研规划提供参考。

seq 145（技术创新趋势预测）同构。全球创新监测页能力级（`全球创新监测.md`:13 bid_desc）：

> 支持全球创新成果与热点的检索分析、展示最新的创新动态、利用数据模型开展趋势预测和判断、对全球城市进行创新能力分析。

`科技全域态势.md`:206（通用能力）：「支持趋势预测功能，基于历史数据预测未来发展趋势」。

UI 代码证据：`realtimeModel.js:29` 注释「前 15 个月实测，末 3 个月为预测演示」；`TechInnovationEvaluationNewPage.jsx:563-580` buildForecastOption（历史/预测/95% 置信区间三线，2026E–2030E，演示值不作数据证据）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 指标趋势预测值 / 趋势预测值 | 三份 SRS + 主文档 | 0 |
| 趋势预测 | 科技创新评估.md:50/140（seq 139/145）；科技全域态势.md:206；全球创新监测.md:13（bid_desc） | 语义真源族 |
| 置信区间 | 科技创新评估.md seq 139 | 1（预测区间明文） |
| 预测 | 主文档 | 命中均为政策模拟/评估语境（附录 A 固定句式适用本件全称） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_008_out.json`（20261101 实跑：久新预测面解剖、Holt/ETS 演示、dev 缺席探针）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx 融资基数，零漂移引用）。
- lane 级探针：`code/_probe_lane6_jiuxin_out.json`（forecast 表 4,872 行首发现 + target_metric 分布）/`_probe_lane6_jiuxin2_out.json`（DESC 列清单 + 样例 + 回测覆盖）/`_probe_lane6_jiuxin3_out.json`（method/coverage 分布）；`_probe_lane6_gkx_fin2_out.json`（年度序列）。
- schema 快照：`gkx-orchestration/agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA-5.11.0.md` §27.4（声明零行——与实库漂移已登记）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_008 | 文首 |
| `ui_evidence` | 证据 | 4 条组件行号 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.dev_forecast_tables` / `dev_predict_table_names` | 计数/清单 | 0 / [policy_prediction_indicator] | §2.1/§3.4 |
| `facts.gkx_financing_yearly_2015_2025` | 序列 | 11 点 | §2.3 |
| `facts.gkx_holt_params` | 参数 | α=0.8, β=0.2 | §2.3 |
| `facts.gkx_holt_level_2025` / `trend_2025` | 状态 | 687.81 / −112.56 | §2.3 |
| `facts.gkx_holt_forecast_2026_point` | 预测 | 575.25 | §2.3 |
| `facts.gkx_holt_forecast_2026_lo95/hi95` | 区间 | 0 / 2819.84 | §2.4 |
| `facts.gkx_holt_residual_sigma` | 残差 | 1145.2 | §2.4 |
| `facts.jiuxin_forecast_rows` | 计数 | 4,872 | §2.2 |
| `facts.jiuxin_forecast_by_metric` | 分布 | 4 指标 × 1,218 | §2.2 |
| `facts.jiuxin_forecast_method_coverage` | 登记 | LLM 全量 | §2.2 |
| `facts.jiuxin_forecast_backtested_rows` | 计数 | **0** | §2.2 |
| `facts.jiuxin_forecast_paper_2026_min_avg_max` | 分布 | [0, 2.17, 14] | §2.2 |
| `derived[0]` | 派生比 | gkx_holt_2026_vs_2025_actual_pct = −6.94 | §2.6 |
| `derived[1]` | 派生比 | gkx_holt_2026_ci_width_pct = 489.9 | §2.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 四条（降档因/升档路径/演示性质/口径风险） | §1.6/§四 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 区间能力 | 可回测 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| ETS/Holt 统计外推 | FPP3（R2） | 解析方差 | **是** | 序列够、结果面无 | **最高（口径 A）** |
| ARIMA | FPP3 §9 | 解析/模拟 | 是 | 同上 | 高 |
| LLM 情景估计 | DeepSeek（久新现状） | 生成上下界 | **否** | **现成 4,872 行** | 中（口径 B，语义错位） |
| 组合预测 | FPP3 §13 | 模拟 | 是 | 可自建 | 中（增强项） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| 久新预测面 | 4,872 | 区间 100%、溯源完整 | LLM 非回测（方法错位） |
| gkx 年度序列 | 2015–2025 | 连续 11 点 | 波动大（区间宽） |
| 久新长序列 | 1990–2026 | 30+ 点 | 2020–2021 扩容跳变 |
| 统计落库面 | 三源无 | — | 升档工程项 |
| dev 预测表 | 0 | — | 表不存在 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径裁定：LLM 面直查（带标注）或暂缓 | 甲方裁定 |
| v2 | ETS/ARIMA 建模 + 回测流水线 + 落库（沿用久新表结构） | 建模脚本 + 调度 |
| v3 | 月粒度预测 + 组合模型 | 月度面评估 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| LLM 预测被当统计预测展示 | **高** | UI 标注义务（NOT_BACKTESTED 随行） |
| 区间宽被误读为模型差 | 中 | 方法论文案（区间=数据波动诚实量化） |
| 序列断点误当趋势 | 中 | 断点检验前置 |
| schema-实库漂移复发 | 中 | 探针以实库为准，schema 仅参考 |

### C.5 总判

**部分支持**：现成面方法不符（LLM 非回测）+ 统计级结果面三源无 + 自建序列充足——差一步"建模+回测+落库"即可升完全转换支持；口径 B（LLM 直查）是零工程量的备选，但语义错位须甲方显式接受。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_008.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读 | demo_* 直接 raise |
| Holt 确定性 | 固定参数重跑 | 点预测 575.25 同值 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 部分支持 |
| 负证据探针 | `absence_probe[0]`（dev forecast 0/predict 误命中甄别） | 留证 |
| 共享快照对账 | 序列与 INNOV_006 同源同值 | B11 批内零漂移 |
| schema 漂移登记 | jiuxin_forecast_rows=4872 vs schema 声明 0 | 已登记回执 |
| mock 残留检查 | `rg "buildForecastOption" repos/demo-ui-science/src` | 正式版替换后无引用 |
