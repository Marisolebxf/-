# 无人值守批量处理 — 终版台账（2026-11-14）

> 经办：李伟（开发） / MCP 身份：黄敬洲 / 模块白名单：科技发展态势（除科学技术全景/科技发展规划/维护管理）
> 授权：用户「完工即推」+「遇到需要我确定的就跳过」（2026-11-14 01:2x）
> 口径：全部 47 条 = 白名单模块内 OPEN + P1 缺陷（原 45 条 + 复核补入漏项 2525、2545）
> 复核：2026-11-14 逐条查评论，47 条全部有判定评论，无遗漏

## 一、总览

| 结果 | 条数 | 说明 |
|---|---|---|
| **已修复并推送** | **7** | 2548、2537、2540、2568、2558、2545、2533（部分） |
| 已满足（建议关闭，待业务确认） | 12 | 2546、2547、2527、2528、2561、2560、2553、2539、2535、2569、2532、2525 |
| 部分实现（已修可修部分 / 待补数） | 4 | 2529、2534、2567、2574、2531 |
| 数据缺口（BLOCKED） | 20 | 见下表 |
| 需规未定义（待产品裁定） | 5 | 2557、2542、2562、2552、2556 |

> 注：合计按 45 条统计，「已满足」实为 11 条（含 2539/2535/2569/2532），分档以 §三 明细为准。

## 二、代码改动（5 次提交，全部已推 origin/dev）

| commit | 单号 | 改动 |
|---|---|---|
| `a3db6d9` | 2548 | 湾区指标级导出补 Excel（`a-dropdown` 双格式 + `downloadXlsxWorkbook`） |
| `81ce6ff` | 2537 / 2540 | 榜单载体名称可点击 + 详情「创新成果」区块（含空态）；创新价值分析报告弹窗 + Word 导出 |
| `8f72bbc` | 2568 / 2574 | 评估详情页综合评估卡补「自定义权重」入口（复用 `WeightDrawer`） |
| `9fdfe57` | 2558 / 2533 | 深圳对标城市补「其他对标城市」兜底组；技术跟踪历史补完成年份筛选 |
| `50c8e6e` | 2545 | 湾区概况地图补「热力强度」自定义（0.4–2.0 倍率滑块 + 恢复默认，纯展示参数） |

验证：每次改动均 `vue-tsc --noEmit` exit 0；无 lint 报错。

## 三、逐条判定

### 已修复并推送（6）
| 单号 | work_item_id | 状态 |
|---|---|---|
| 2548 | 7167635778 | RESOLVED（已修复） |
| 2537 | 7168142038 | RESOLVED（已修复） |
| 2540 | 7167702355 | RESOLVED（已修复） |
| 2568 | 7167999207 | RESOLVED（已修复） |
| 2558 | 7167764650 | RESOLVED（已修复） |
| 2545 | 7167556830 | RESOLVED（已修复，热力强度自定义；飞线为数据缺口） |
| 2533 | 7167777160 | IN PROGRESS（时间筛选已修，技术类型/原因说明待补数） |

### 已满足（证据评论已发，建议关闭）
2546、2547、2527、2528、2539、2535、2561、2560、2553、2569、2532、2525

### 部分实现
- 2529 科创要素描述列（缺 description 展示）
- 2534 成果发布日期（无 publishDate 字段）
- 2567 权利要求数量（无 claim_count）
- 2574 政策保障力排名（无横截面样本）
- 2531 概览方法选择步（插步会破坏后端进度映射）

### 数据缺口（BLOCKED）
2530（预测/异常）、2559（研发投入/专利/高企）、2554（9 类要素未下发）、2549（创新价值排名）、2551（定期推送）、2556（年份维度）、2562→裁定、2543（资金要素）、2541（基金规模）、2538（自动监测调度）、2536（预测模型）、2506（成果 domain 字段）、2542→裁定、2572（经费来源维度）、2571（战略规划原文）、2566（专利四维）、2565（前沿主题区域）、2563（季度/月/机构）、2564（中心性物化）、2570（SEP）、2573（项目库）

### 需规未定义（待产品裁定）
- 2557 领域口径：20+8 集群 vs 四类学科领域
- 2556 时间范围：需年份维度口径
- 2562 未来预测：是否允许外推
- 2552 创新价值筛选：论文数档位是否合规
- 2542 城市对标三分组：投入/产出/环境如何映射

## 四、库侧实测结论（供补数方）

- `demo_gkxlumenx_ads.city_index`：81 城市 × 9 期，`indicator_values` 仅 `orgs/source/policies/scholars/papers_patents` → 无研发投入/高企/独立专利数；9 期为综合分，不能当指标分期值。
- 正式 `gkxlumenx_ads` 相关表 ≈ 全 0 行（city_index / innovation_carrier / carrier_index / point_map / impact_prediction / eval_weight 均 0），demo 库有数 → 正式环境属「未灌数」。
- 久新：`ads_*` 261 张可读，geo_yearly 17.1 万 / topic_yearly 5.4 万 / patent_cross_year 50.2 万 / strategy_scope 1523 / fund_subfield 2.77 万 / collab_edge 1438 万。

## 五、遗留待办（非开发工时）

1. 算法侧：中心性物化、城市能力分预测、SEP 库、载体创新价值分、前沿主题×区域、季度/月论文粒度。
2. 数仓侧：`city_index.indicator_values` 补三键；深圳监测指标×年份宽表；经费来源结构化。
3. 产品侧：5 条裁定（§三末）。
4. 后端：`/snapshot` 多维筛选参数、订阅推送 job、成果 `domain` / `publish_date` 字段。

## 六、收口复核（2026-11-14 01:40）

- 空间内 OPEN+P1 缺陷共 71 条；白名单模块内 40 条（+ 已流转 5 RESOLVED + 1 IN PROGRESS = 46，另 2525/2545 为本轮复核补入）。
- **逐条查评论核实：白名单内 46 条全部有判定评论**（首行署名「[由李伟处理，经黄敬洲 MCP]」），无重复评论、无遗漏。
- 状态：6 条 RESOLVED（2548/2537/2540/2568/2558/2545）、1 条 IN PROGRESS（2533）、其余保持 OPEN（等业务/测试确认或等补数）。
- **非白名单（未处理，31 条）**：科创政策全景、政策分析评价、政策效果推演、科技交流、门户-集群专题/集群服务、全局处理、我的报告任务 —— 不属「科技发展态势（除科学技术全景/科技发展规划/维护管理）」白名单，按口径未纳入。
- 结论：**白名单内已无可执行的开发动作**；剩余全部阻塞在算法补数、数仓补数、后端接口、产品裁定四类外部依赖上。

## 七、下午续作（2026-11-14 13:00，7 单 / 5 commit）

用户裁定口径后补齐「前端可先行」部分，其中 4 条口径确认：2574 排名→区域空间分布；2534 发布日期→源记录公开日；2529 描述→摘要截断（无则「—」）；2570 SEP→专利被引/同族代理。

| commit | 单号 | 改动 |
|---|---|---|
| `db1c17b` | 2556 | 指标趋势「时间范围」下拉（后端 `historyPeriods` 裁剪 + 窗口内同比重算，窗口首期同比置「—」） |
| `53ac81b` | 2532 | 参数模板 localStorage 存档（`gkx:tracking:parameter-templates:v1`）补持久化兜底 |
| `755f4d7` | 2561 | 竞争力分析报告改走 `buildReportDocument` + `downloadReportAsWord`，删造数章节 |
| `81daadc` | 2533 | 结果追踪「评估方法」筛选（`methodKeys`）+ 最早→最新客观差值/变化原因 |
| `0206258` | 2574 / 2570 | 政策综合评估补综合得分/一级权重/权重覆盖率 + 区域政策保障力排名（`policyPanel.dimScores` → `spatialByDimension.policy` → 空态）；技术影响力补 IPC4 被引/同族代理排名（明标非 SEP 口径） |
| `a68f40d` | 2534 | 成果详情「更新时间」→「发布日期」（后端 `time` 实为 `publish_date`，缺失退化 `publish_year`），评审模式补口径项 |
| `f436883` | 2529 | 地图对象基础信息补「描述」（摘要 120 字截断）/「学科领域」行（别名 domain/subject/field/discipline），无源文本给「—」，不再用 `region.trend` 冒充描述 |

状态：2574 RESOLVED；2532/2556/2561 RESOLVED；2533/2529/2534/2570 保持 IN PROGRESS（余缺：技术类型字段、要素级 description/domain、成果摘要、SEP 库）。

未做：2530（趋势预测/异常监测需算法模型与规则口径）、2538（监测模型设置需后端模型服务）。二者不是前端可独立闭合，需产品定规则项与阈值默认值。

## 八、2530 / 2538 按裁定落地（2026-11-14 13:20，规则法 + 趋势外推，口径只进角标）

用户裁定：**现在做，但不在页面标明，在角标写清楚**（即口径说明只走 ⓘ 角标 tooltip，正文不铺说明文字）。

| commit | 单号 | 改动 |
|---|---|---|
| `7820d3b` | 2530 | 新增 `src/utils/monitorRules.ts`（规则配置读写 + 阈值判定 + 角标文案）；科创事件画布补「事件数量趋势与预测」条（触发年份真实计数聚合 6 年 + 末 2 期线性外推，虚框柱区分推算）；命中规则显示「异常 N 期」角标，tooltip 列年份与命中原因；抽屉趋势段改历史实线/预测虚线、删「稳步上行」无源结论 |
| `7860b5b` | 2538 | 监测模型设置补「自动监测规则」分组（总开关 / 低分阈值 / 环比降幅阈值 / 缺测提示），保存写 `gkx:monitor:rules:v1` 并与订阅解耦；规则说明走 ⓘ 角标 |

状态：2530 RESOLVED；2538 保持 IN PROGRESS（规则法非模型，等产品确认口径；要模型需算法侧提供监测模型与打分接口）。

口径边界（写进评论）：趋势预测 = 事件计数线性外推，非模型预测；异常监测 = 阈值规则判定，推算值不参与判定；两处规则共用同一本机存储，改一处同时生效。

## 九、2570 流程冲突纠偏（2026-11-14 13:25）

徐滕强 12:37 已将 2570 处理人划至其名下并按 `[agent-blocked]` 处置（恢复条件：接入 ETSI/信通院 SEP 声明数据，或产品书面批准替代口径）；我们 13:07 不知情按会话内裁定改了前端（`0206258`）并填了解决结果，撞处置。李伟裁定**回滚代码**。

- 纠偏：2570 解决结果/问题归类已清空，状态与处理人不动（留徐滕强名下）；评论说明时间线与处置。
- 回滚：`7e20822`（origin/dev）撤销 `0206258` 中技术影响力代理排名表，页面回「标准必要专利：未测」；2574 不受影响；`vue-tsc` 通过。
- 教训（后续铁律）：**动任何飞书单前必须先查操作记录/处理人最新归属**，他人划走的单不再单方面改字段、改状态、改代码口径；替代口径须经产品书面批准，开发会话内裁定不算数。

## 十、reopen 单处理：2575 指标概述三词字面化（2026-11-14 14:35）

用户 13:20 自己 reopen 2575（科技指数-指标概述查看，7167977167），原因：需规原文三词「指标定义 / 评价目的 / 适用范围」没有字面出现在页面上（此前标签是「指标概述查看 / 计算方法 / 意义解读」这套换说法）。

- 修复：`IndicatorDetailPanel.vue` 指标概述卡改三小节——指标定义=`description`、评价目的=`significance` 原文、适用范围=配置字段事实组合（领域/频率/单位/版本，无独立字段不推断），缺数走空态；`70280eb` 已推 origin/dev。
- 不动「指标意义解读」卡（7167984756 三要素需规的标题字样保留）。
- 状态：REOPENED → RESOLVED（35119342），解决结果=已修复、问题归类=功能逻辑，评论已发。
- 处理原则：需规验收词必须字面出现在页面文案里，标签不得自创同义替换；数据无独立字段时用配置事实组合 + 空态，不造适用范围文案。

## 十一、reopen 单处理：2576 计算方法三词字面化（2026-11-14 14:35）

用户 13:28 自行 reopen 2576（科技指数-指标计算方法说明，7168333574），评论「计算方法OK，现在『计算公式、数据来源、统计口径』在页面上没有明确文案显示」——与 2575 同一类：内容对但需规词未字面出现。

- 修复：`IndicatorDetailPanel.vue` 计算方法卡拆三小节——计算公式=`calculation` 含「=」段；统计口径=同一字段口径段（按原文「；」分段归位，不改写）；数据来源=`source_systems`（走 toPublicCopy，源表名不向客户暴露）。`777397f` 已推 origin/dev。
- 单句配置时口径显示「未单列，已含于上方公式说明」，不复制同一段两次。
- 需规末尾「示例」（逐指标算例）配置无字段，评论中明确不在本单范围、需另提。
- 状态：REOPENED → RESOLVED（35119342），评论已发。
- 规律：科技指数同批需规验收单（2575/2576）都是「要素未逐项显式化」，后续同类单先按此模板自查三要素是否逐字可见。

## 十二、深圳创新监测 3 单收口 + 模拟类文案清理（2026-11-14 18:24）

用户 18:23 发现载体详情仍显示「模拟推算，非真实成交额」，随后裁定：深圳创新监测全模块清掉界面上的「模拟 / 推算 / 非真实 / 估算」类文案，代码注释与 mock 台账保留留痕。

- `f151486`：载体详情 `description` 补映射（后端 `toCarrierFromJiuxin` 已下发 gapfill description，前端 `mapCarriers` 未接，导致「基本介绍/载体描述」恒为「—」）。
- `9216e39`：CarrierTab 删「模拟推算，非真实成交额」「TOP20 模拟推算」标识、「其余为模拟额」，经费构成枚举改「真实额 + 口径补足混合 / 全部为口径补足 / 无项目证据」，tooltip 去掉「授权演示 gapfill」。
- CompareTab 的「估算/模拟」角标与 caveat 说明段已从工作区删除，但该表格属另一会话未提交的「城市官方指标」功能，尚未上线，随其提交生效。
- dev 复测（bundle `index-RjTyedCz.js`）：罗湖区创新载体详情「载体描述」有正文，三处模拟类文案全部消失，PASS。
- 状态：7165910425 / 7166709715 / 7166852615 均 IN PROGRESS → RESOLVED（35119339），解决结果=已修复，负责人自动转测试吕宇翔，评论已发。
- 口径提醒：上述 description / 计算方法 / 数据来源 / 单位均为 Java D4=mock 冻结种子，合规后需按 gapfill DROP 清单回收。

## 十三、7167864981 科创要素趋势预测/异常监测（REOPEN 返工，2026-11-14 20:19）

黄敬洲 16:51 REOPEN：需规要的是科创要素，上一版却改在科创事件页（GlobalEventSection），事件页「事件数量趋势与预测」被判「没法看」。

- 需规依据：趋势预测/异常监测仅见 §1.1.1.1.4.1.1.3.4 科创要素「监测数据趋势变化查看功能」；科创事件章节只有时间筛选/重要性分级/详情查看，**无**趋势预测。
- `276221f`：`buildTrendMultiLineOption` 新增可选叠加参数（推算段虚线+空心菱形、异常点），科创要素「增长趋势」末尾追加 2 期线性外推（末 6 期斜率，负值截断 0），ⓘ 标明「推算示意、非真实值」。
- `95e46d0`：修 CI 类型门 `vue-tsc --build` 报的 TS2532（`window[0]` 可能 undefined）。
- `14a4abd`：异常点改独立 scatter（markPoint.coord 在类目轴+末端 null 下不落点），图例收敛为「异常点（N）」，并回退 GlobalEventSection 超范围改动（-173 行）。
- `f9e5dc3`：异常原因并入轴级 tooltip（series 的 item 级 tooltip 被 axis 触发覆盖）。
- `2f2cac7`：异常判定只喂完整年度，跳过进行中年份（2026 截至当前月）。
- dev 复测（bundle `index-CxJZKAb2.js`）：X 轴延至 2028、末端虚线菱形；图例「异常点（4）」；悬停 2018/2022/2024/2025 均出「环比下降 x%，超过阈值 10%」。
- 状态：REOPENED → RESOLVED（35119342），解决结果=已修复，评论已发。
- 教训：本仓类型门必须用 `vue-tsc --build`（`--noEmit` 漏 `noUncheckedIndexedAccess`）；异常点选 `markPoint` 不可靠，统一用 scatter 叠加。

## 十四、4 条「部分完成」单 dev 复测（2026-11-14 20:5x）

用户选定「继续 4 条部分完成」，逐条 dev 实测：

| 单号 | work_item_id | 复测结论 | 证据 |
|---|---|---|---|
| 2529 | 7168047201 | **PASS** | 科技全域态势 → 东莞忆联信息系统有限公司 → 详情抽屉「基础信息查看功能」：描述「东莞忆联信息系统有限公司（东莞市）企业创新主体点位，enterprise_score 评分 61.1」；学科领域「暂无数据」 |
| 2533 | 7167777160 | **PASS（补测）** | 首次进入受阻（步骤 3 `is-pending`）。按方案 A 在 dev 用默认条件触发一次评估跑批（20:32:10 完成，10 条技术排名）后进入结果页：「完成时间」下拉（全部年份）/「评估方法」下拉（全部方法）/「显示 20 / 20 条」/「差异分析（11-13 02:03 → 11-14 20:32）综合潜力 0 · 技术数 0 · 关联数 0；变化原因：持平」 |
| 2534 | 7167783660 | **PASS** | 全球创新监测（`/tid/trend/global-innovation-monitor`）→ 创新成果综合展示 → 中国科学院详情：元信息四卡为「创新价值 4781335 / 所在区域 北京市 / 国家/地区 CN / **发布日期 2026-09-18**」，无「更新时间」 |
| 2538 | 7168059694 | **PASS** | 同页 → 创新监测与分析 → 「监测模型设置」面板：「自动监测规则」分组（总开关已勾选 / 低分阈值 60 分 / 环比降幅阈值 10%）；「智能推送」空态「暂无推送记录：订阅规则暂不产生推送记录」 |

- 2533 补测闭环：方案 A 跑批成功后，三处元素全部实测可见，不再依赖源码证据。
- 4 条全部 PASS，收口（转 RESOLVED）待用户「已修复待验证」口令。

## 十五、2529 期刊/会议「描述」口径裁定：结构化事实拼接（2026-11-14 21:0x）

用户裁定（human:李伟）：期刊、会议在久新库无任何简介文本字段，其详情「描述」采用**结构化事实拼接**，不写空态、不自造文案。

**依据（live 实测 + 文档）**

- `ads_paper_profile` 来源元数据仅 7 字段：`primary_source_id / name / name_zh / type / issn_l / publisher / is_core`，无 description / abstract / summary。
- 唯一 source 表 `ads_media_source_profile`（36 行）为新闻媒体源，非学术期刊，同样无描述字段。
- `ADS_SCHEMA.md:2393-2396`：六个 `primary_source_*` 只从 `dwd_source` Snapshot 投影，缺失保持 NULL；`is_core` 只表示 CWTS Core Sources 覆盖，**不含 JCR 分区、影响因子、期刊等级**。
- 会议无独立实体表，仅为论文 `primary_source_type='conference'`；学科只能按发文 Topic 聚合代理。

**拼接模板（只允许真实字段；字段缺失时分句整段省略，不编造）**

- 期刊：`《{name_zh 或 name}》，期刊，ISSN-L {issn_l}，{publisher} 出版，{CWTS 核心源 / 非核心源}；{统计年} 年发文 {n} 篇，主要方向：{Topic 中文名 Top3}。`
- 会议：`《{name}》，会议，{publisher} 出版；{统计年} 年发文 {n} 篇，主要方向：{Topic 中文名 Top3}。`
- 学科方向统一标注「按发文聚合」；统计年取 `statYearOf(scope)`（区间内最近完整年），不跨年累加。

**禁用字段**：影响因子、JCR 分区、期刊等级、主办单位、创刊年、简介原文——久新无源。

**影响**：2529 处理结论与「要素对象级详情」接口契约按此实现；前端描述区直接渲染拼接文本，不走「暂无数据」空态。

---

## 十六、2529 对象级科创要素浏览/详情（三端实现，待部署复测）

**根因**：`/display/v1/situation/map` 仅企业下发对象级点位，其余 8 类只有城市聚合 → 前端在「科创要素」里点不到「某个会议 / 某篇论文」，`detail.description` 与 `detail.properties.domain` 必然为空，需规的「描述 / 学科领域」只能显示「—」。

**改动（三仓均停在本地工作区，未提交未推送）**

1. `lumen-topic-py`（新增 `gkx_show_service/views/element_browse.py`，`main.py` 注册路由）
   - `POST /internal/gkx-show/element/browse`：9 类 factor（paper/journal/patent/scholar/meeting/institution/topic/project/result），分页 + keyword/yearFrom/yearTo/subfieldIds/region。
   - `POST /internal/gkx-show/element/detail`：按 `<factor>:<主键>` 取完整基础信息。
   - 数据源（久新只读，全部 live 实测）：`ads_paper_profile` / `ads_patent_profile`(+`ads_patent_analysis_ipc_topic`) / `ads_project_profile` / `ads_research_outcome_profile` / `ads_research_problem_profile` / `ads_talent_profile` / `ads_institution_profile`(+`ads_institution_topic_entry`)；期刊/会议按 `primary_source_*` 聚合（统计年取 yearTo，默认 2024）。
   - 描述优先级：源摘要/说明 → 结构化事实拼接（字段缺失整句省略）；学科领域：主题/学科/领域维度解析，专利按 IPC 主分类主题映射（接口 note 明示）；无维度筛选如实提示「未参与」，不伪造。
2. `lumen-svc-platform`（`gkxlumen-display`）
   - `feign/RemoteShowPythonClient` 增 `elementBrowse` / `elementDetail`（@NoToken）。
   - 新增 `controller/SituationElementController`：`POST /v1/situation/element/browse|detail`，9 类白名单 + 参数白名单透传；下游异常返回 `degraded=true + reason`，不回落 Mock。
3. `lumen-ui-science-pc`
   - `api/situation/index.ts`、`types/situation.ts`：新增对象级浏览/详情类型与请求。
   - `overview/index.vue`：仅在「列表视图 + 科创要素 Tab」按需拉取（并发 9 类、每类 10 条），结果通过 `elementItems` 下发；筛选（时间/子学科）变化重拉。
   - `FactorMapSection.vue`：列表视图把对象行置顶（类型/名称/区域/年份/描述入口），点击「查看」复用既有详情抽屉；对象行隐藏「在地图中查看」（无坐标，不伪造点位）。
   - `detailModel.ts`：对象级详情描述上限放宽到 600 字（城市聚合仍 120 字）；9 类要素补「要素类型」文案。

**验证**

- Python：真实连久新跑通 browse+detail ×9 类，均有描述与学科领域；耗时 paper 0.8s / patent 0.4s / meeting 2.3s / journal 8.8s（首次，SQL 缓存 120s）/ 其余 <3.5s。
- Java：`mvn -o -pl gkxlumen-display -am compile` BUILD SUCCESS。
- 前端：`pnpm --config.engine-strict=false type-check`（vue-tsc --build）通过；本机 Node 20.18.0 低于仓要求 20.19，仅绕过引擎校验，未改仓配置。

**成果（result）子学科筛选核实**（2026-11-14 21:2x，真实库 SQL）：`ads_research_outcome_profile` 共 342 行、`primary_topic_id` 无空值、238 个 distinct topic **全部**能在 `ads_discipline_topic` 命中（编码空间一致），覆盖 99 个子学科；此前测得的「流行病学子学科 0 条」属该子学科确无成果对象，不是映射断裂。结论：`_FILTER_CAPS["result"]` 保留 `{year, subfield}`，空态按真实无数据返回，不改口径、不做兜底造数。

**已推送 origin/dev**（2026-11-14 21:4x）

| 仓 | commit | 说明 |
|---|---|---|
| `lumen-topic-py` | `4683df4` | `element_browse.py` + `main.py` 注册 |
| `lumen-svc-platform` | `5dce818f` | `SituationElementController` + `RemoteShowPythonClient` 两端点 |
| `lumen-ui-science-pc` | `8e6d50d` | 列表视图对象行 + 详情描述/学科领域 |

> 三仓推送前均 rebase 到最新 origin/dev；`lumen-topic-py` 的 autostash 在他人在改的 `innovation_evaluation.py` docstring 上冲突，已按「上游出参列表 + 本地 topN 说明」合并解冲突（未提交该文件，改动仍留在工作区），stash 备份保留。

**dev 部署与复测**（2026-11-14 21:5x–22:1x，PASS）

- 三仓 CI 均按 dev 自动发布：`deploy:show-py`（topic-py，镜像 `gkxlumen-show-service`）、`deploy:display`（svc-platform，`gkxlumen-platform-display`）、前端 `deploy:k8s`（22:03 产出新包 `index-Dmdhql4f.js`）。
- 网关 `http://10.50.69.111:30895/display/v1/situation/element/{browse,detail}` 实测：9 类全部返回真实对象，description 44–601 字、disciplines 非空；detail 9 类均 OK；非法/缺 id 返回 `degraded=true + reason`，不造对象。
- 前端包校验：`index-DRb6O3mm.js`（overview 页 chunk）含 `elementItems`，`useIndustryDomains-*.js`（api chunk）含 `element/browse`，确认新代码已上线。
- 浏览器复测（https://edu.itic-sci.com/tid/trend/tech-overall-situation）：列表视图出现论文/会议/成果/企业对象行；论文详情「描述」为摘要正文、「学科领域 = 荟萃分析与系统综述、决策科学、社会科学」、「要素类型 = 论文」；企业行学科领域「暂无数据」符合预期。

**收口**（2026-11-14 22:15）：用户口令「已修复待验证」→ 已发评论（首行 `[由李伟处理，经黄敬洲 MCP]`，含三端改动、描述/学科领域口径、9 类实测证据）+ `transition_state` 35119339 → **RESOLVED**；阶段分类=开发测试阶段、解决结果=已修复、问题归类=功能逻辑问题。

---

## 十七、2534 成果描述补齐（2026-11-14 23:0x，待推送）

用户裁定口径：**论文/专利中文摘要优先、英文原文兜底**；**项目/机构无原文时用结构化事实拼接**；**中文摘要缺口挂数据侧**。

**久新实测（只读，抽样 5 万行）**

| 表.字段 | 填充率 | 用途 |
|---|---|---|
| `ads_paper_profile.abstract_zh` / `abstract_en` | 0.11% / 62.9% | 论文描述（英文兜底） |
| `ads_patent_profile.abstract_zh` / `abstract_en` | 0% / 93.0% | 专利描述（英文兜底） |
| `ads_project_profile.description` / `description_zh` / `description_en` | 3.6% / 0% / 0% | 项目描述（拼接兜底） |
| `ads_project_profile.funder_name` / `funded_paper_count` / `observed_start_year` | 100% / 100% / ~100% | 项目拼接素材 |
| `ads_institution_profile.description` | 26 / 83,745（0.03%） | 机构描述（拼接兜底） |

**代码改动（3 仓，本地待推）**

- `lumen-topic-py`：`achievement_indicator.py` — 论文摘要按「中→英→原文」取值并回 `description_lang`；专利补 `ads_patent_profile` 主键点查 + 无摘要时「名称/公开号/受理局/公开年」拼接；项目补 `funder_name/end_year/funded_paper_count` 并拼接；机构补 `description/province_name/established_year` 并拼接。
- `lumen-svc-platform`：`GlobalInnovationController.achievementItem` 透传 `descriptionLang`。
- `lumen-ui-science-pc`：`AchievementRow.descriptionLang`；`InnovationDetail.vue` 抽屉描述改「详情接口优先、列表兜底」，评审模式对英文摘要标注「摘要语种：英文原文（中文摘要未入仓）」。

**数据侧缺口（挂数据侧，不阻塞 2534 收口）**

- 论文中文摘要近乎未入仓（0.11%）、专利中文摘要 0%、项目 `description_zh/en` 0%：需久新补中文摘要，或另行评估机器翻译（派生数据须标注）。
- 项目/机构原始简介长期缺失：当前用结构化事实拼接（同 2529 期刊/会议口径），字段全真实、缺项整句省略，不编造。

**dev 复测（2026-11-14 23:23，接口层）**

| 类型 | 结果 | 证据 |
|---|---|---|
| 论文 | PASS | `wrk_417d…`：`descriptionLang=en`，597 字符 PRISMA 摘要 |
| 专利 | PASS | `pat_59c2…`：`descriptionLang=en`，770 字符英文摘要 |
| 项目（无原文） | PASS | `prj_096f…`：`《Management and Operations of the National Optical Astronomy Observatory》，National Science Foundation资助项目，2016 年立项，2019 年结项，关联论文 23 篇。研究方向：星系的形成、演化与现象。` |
| 机构 | PASS | `ins_782f…`（中国科学院）：`中国科学院，政府机构，位于北京市，1949 年成立。累计发文 177917 篇，被引 4781335 次，人才 19241 人。` |
| 项目（有原文） | 发现并修复 | 原文英文被判为 `zh` → 增加 CJK 判定，英文原文标 `en` |

修复提交：`lumen-topic-py 2e9fd5f`（语种判定）、`lumen-ui-science-pc 441b3f0`（文案「描述语种：英文原文（中文摘要/简介未入仓）」）、`lumen-ui-science-pc d368961`（修正 policy 模块 `@arco-design/web-vue/icon` 无效导入，恢复 CI 构建；本地 `vite build` 已验证通过），均触发 CI 重新发布。

**收口（2026-11-15 00:00）**：7167783660 IN PROGRESS → **RESOLVED**（阶段分类=开发测试阶段、解决结果=已修复、问题归类=功能逻辑问题），评论已附完整验证过程与库侧证据。中文摘要缺口转久新数据侧，不阻塞本单。

## 十八、7166676321 领先区县/扩散方向（D 档：库 + 算法 + 需规，2026-11-15，本地待推）

**结论**：不是前端漏渲染。`leadDistrict` 全链路从未接（Python 未算 → Java 未透传 → 前端未映射），`diffusion` 恒 `'—'`。

**三方对齐**

| 来源 | 结论 |
|---|---|
| 需规 DS-06-DOMAIN `DOM-D03` | 空间分布分析（分布范围/中心位置/扩散方向）判 `other_system`（GIS 空间聚合），不定义 M_* |
| 算法 `M_SCIUI_SZINNOV_011` | 部分支持：v1 只承认区级计数；中心位置/扩散方向属 v2 形态学，未定义 |
| 久新 `ads_geo_yearly_discipline_metrics` | 实测 `GROUP BY location_level` **无 DISTRICT 级行（0）**，领域×区县不可直取 |
| 久新 `ads_institution_profile` | 深圳 136 家机构，**124 家有 `district_name`**，坐标 100% |
| 久新 `ads_institution_topic_entry` ⋈ `cluster_topic` | 单条 SQL 1.01s 出 15 集群 × 7~9 区分布，**各集群领先区县均为南山区** |
| 我方 `gkxlumenx_ads.chain_sz_dist` / `innovation_point_map` | 均 0 行，无现成区级数据可复用 |

**口径（写入代码注释 + 接口 note + 报告脚注）**：区县分布 = 机构属地区县 × 主题加权论文计数（全时段累计，跨机构共著重复计），与城市级 Topic 论文数**不同分母、不可相加**；未解析到区的 12 家不计入；数据源无时序区县/街道级记录，**扩散方向只呈现静态分布梯度（Top3 区县），不构成时序扩散结论**（禁止恢复 mock「向相邻行政区扩散」）。

**代码改动（本地未提交）**

- `lumen-topic-py`：`monitor_indicator.py::cluster_distribution` 增区县聚合（独立 try 降级），items 增 `lead_district` / `lead_district_percent` / `district_distribution`，顶层增 `district_analysis`（全领域分布 + 口径 note）。
- `lumen-svc-platform`：`ShenzhenInnovationController.fieldDistribution` 透传上述字段；`noSourceFields` 移除 `leadDistrict`（保留 `clusterPoints`）；`fieldDeviations` 增区县口径条目。
- `lumen-ui-science-pc`：`SzDomainDistrictShare` / `SzDomainDistrictAnalysis` 类型；`mapDomains` 接区县分布；`index.vue` 下传 `district-analysis`；`DomainTab.vue` 报告「领先区县：南山区（占比 xx.x%）」、「扩散方向：南山区 → 龙岗区 → 福田区（静态分布梯度，非时序扩散）」，并加口径脚注；自检补 4 条断言。

**验证（本机）**：`py_compile` 0；Python 实跑 `cluster-distribution` 返回 15 集群全部有 `lead_district=南山区`（53.7%~81.0%），全领域 67.0%；`mvn -pl gkxlumen-display -am compile` 0；`pnpm type-check` 0；`node szDomainTabFixes.selfcheck.mjs` PASS（顺带修正 CarrierTab 雷达断言：中层已改消费后端 value，旧断言 `[0,0,0]` 失效）；`pnpm build-only` 2m07s 0。

**待办**：人工确认后推 3 仓 → 部署 → dev 复测报告抽屉 → 7166676321 收口。7166799221 的「领域/领域分布/领域覆盖数」待需规确认派生口径；7166773230 已修待验证。

