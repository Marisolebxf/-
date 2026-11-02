# 专家引进评估子图（M_SCIUI_KGANALY_004）

> **类型**：简单统计类（子图构建与统计）｜ **域**：科技信息展示系统·科技知识图谱·服务展示·图查询（查询资产深析）｜ **UI 挂载**：`pages/tech-knowledge-graph/mockData.js:968`（asset-008「专家引进评估子图」，displayKind=graph，entityType=专家，tags=[专家,引进,项目]，scenario=人才服务台嵌入）→ 深析抽屉 `QueryAssetDeepAnalysisDrawer.jsx:119`「分析洞察」卡
> **数据支持度**：**完全转换支持**（久新人才档 100,000 + 合作边 5,051,578 live——结构+数据量均足，本件脚本已实算 ego 评估子图并落产物）｜ **公式定义人**：UI 前端演示（`queryAssetDeepAnalysis.js` buildDeepAnalysis seeded mock——种子哈希造数）；本件按「自我中心网络（ego network）」权威口径重建｜ **口径归属**：需求明列叶（seq 446/447 图查询资产族），指标为资产级挂载件
> **复现脚本**：`code/M_SCIUI_KGANALY_004.py`｜ **产物**：`code/M_SCIUI_KGANALY_004_out.json`
> **四判定摘要**：直接结构 = 无现成「引进评估子图」结果面（三源词族 0 命中）；直接数据 = 无（同左）；依赖结构 = **足**（久新 `ads_talent_profile` 38 列含 is_academician/projects/discipline 全维 + `ads_talent_collaborator` 15 列含 collaboration_score/首次-末次合作年）；依赖数据 = **足**（100,000 档 + 5,051,578 边 live 实测）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表当日实测）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成「专家引进评估子图」结果面（`absence_probe` 三件：dev 资产登记面不存在——8 条资产硬编码在 mockData.js；gkx 无引进评估业务面但有合作边备选；久新无评估结果面），但**子图两原料齐备且量足**：①久新 `ads_talent_profile` 100,000 学者档（38 列：name_zh/is_academician/projects/discipline_domains/talent_bio/邮箱电话——引进评估的「候选专家属性卡」全维在列）；②`ads_talent_collaborator` 5,051,578 合作边（15 列：collaboration_score/collaboration_rank/co_paper/co_project/co_patent/first-latest_collaboration_year——「合作网络+成果关联」边语义直接可算）。本件脚本已实算：度数 Top1 学者（`tal_4b1b1f43a3f84e60834711f6caebc790`，ego_degree=3,238，档载名「陈晓红/Xiaohong Chen」，ORCID 0000-0002-9797-8384）的 500 邻居框 ego 诱导子图 = 785 条邻居间边（密度 0.006293），ego 合作论文合计 6,465 篇——「现在就能算」是实测非推断。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 密度 = 诱导边 785 / C(500,2)=124,750（同框同池，denominator_note 落盘） |
| B4 | 负结论带探针 | absence_probe 三件（三源逐一） |
| B5 | 确定性 | ego 选点 = 度数降序+id 升序破平局；邻居 sorted() 截断 500 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | py 实算落 _out.json，零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 合作成果三列（paper/project/patent）分开落键，project/patent 实测 0 不混报 |
| B10 | 口径裁定保守交付 | 「引进评估」业务评分维度未立项——本件交付子图结构+成果关联，评分口径留待甲方（§4.2） |
| B11 | 多本账互推 | 人才档/合作边总数与族级快照 `_probe_s306_l1_out.json` 同源 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成「引进评估子图」结果面吗？ | 无 | absence_probe 三件 |
| 子图原料结构与数据量够吗？ | **够** | 久新 100,000 档 + 5,051,578 边（§3.1） |
| 现在就能算吗？ | **已实算** | ego 子图 500 节点/785 边/6,465 合作论文落产物（§二） |

## 摘要

「专家引进评估子图」是科技知识图谱·图查询资产族的一条 graph 型资产：在查询资产列表点选后进入深析抽屉，展示「候选专家×合作网络×项目成果关联」的网络图与洞察。UI 现状全部由 `buildDeepAnalysis`（seeded hash mock）生成演示读数。数据侧判定：**完全转换支持**——久新 `ads_talent_profile`（100,000 学者档，38 列含院士标记/中文姓名/学科/项目列表/履历）与 `ads_talent_collaborator`（5,051,578 合作边，含合作强度分与成果计数）两表构成引进评估子图的完整原料；本件以合作度数 Top1 学者为 ego 实算其 500 邻居诱导子图（785 边，密度 0.006293），验证 ego network 口径在真库可复现。gkx `dwd_scholar_coauthor` 1,187,606 边为备选承载（人-人合作语义同族）；dev 图词族 26 张全 0 行（族级快照在案）。

- 需求判定：**需求明列叶所属资产族**（seq 446/447），「引进评估」评分口径需求未给——本件交付子图结构，评分口径留待裁定。
- 复现状态：脚本已实算通过；ego 子图三组读数（邻居框/诱导边/成果合计）落产物。
- 档位结论：**完全转换支持**（三源无结果面 + 子图原料结构数据量均足 + 已实算验证）。
- 关键事实：久新人才档 name_zh 有值（ego 即「陈晓红」）——与同族技术图 name_zh 全空相反，人才域中文名可直接展示。
- 降档风险：无（原料长期在库）；升档路径：预计算落子图表 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技知识图谱/服务展示/图查询（seq 441-448；资产挂载对应 seq 446「结果展示与快速浏览」与 seq 447「图表详情与预览功能」）。UI 实际形态：`mockData.js:968-981` 定义 asset-008 查询资产（title=专家引进评估子图，summary=候选专家与合作网络、项目成果关联，displayKind=graph，entityType=专家，bizLine=人才态势，scenario=人才服务台嵌入）；用户在资产列表点选后打开 `QueryAssetDeepAnalysisDrawer.jsx` 深析抽屉，`:119-126`「分析洞察」卡展示 `buildDeepAnalysis(asset)` 生成的核心发现/关联提示/数据说明三条洞察，`:95-106`「结构指标」表展示度中心性 Top/中介节点/社群数/跨域边占比，`:86-89` 可视化分析卡按 thumbKind=graph 渲染力导向网络图。资产清单为 mockData 硬编码 8 条（无后端登记面）——本件指标即这 8 条资产中唯一「专家」类型资产的子图构建。

### 1.2 为什么需要本指标

专家引进评估是人才工作的决策场景：面对一位候选专家，评审者需要三样东西——**他有多大学术影响**（合作网络的规模与强度）、**他与哪些团队有真实合作**（区别于名录式罗列的实证关联）、**他的成果落在哪里**（论文/项目/专利三维）。子图形态正好承载这三问：ego 居中、合作者环绕、边带强度与成果计数。UI 把这条资产的场景标为「人才服务台嵌入」，说明它是给人才服务台直接复用的分析件——评估口径一旦在图谱侧建好，服务台点开即用。mock summary 的措辞「候选专家与合作网络、项目成果关联」就是子图三要素的原文。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**seq 446/447 只写资产浏览与详情的通用行为（「点击具体的查询结果后，弹出详细页面，展示图表的完整结构、数据来源、分析流程……」），未定义「引进评估子图」的节点集、边型、评估维度。子图口径（ego network 一跳诱导）是本件按权威方法重建的推测定义（§1.6）；「引进评估」的业务评分维度（如引进优先级分）需求与三源均未立项——本件交付子图结构与成果关联读数，评分口径列 §4.2 待裁。

### 1.4 类似指标权威方法可行性分析概要

自我中心网络（ego network）是社交网络分析的标准工具。其一，社会资本研究经典（R1 Granovetter 1973 弱连带强度）：合作网络的结构位置影响资源获取——引进评估关注候选人的网络资本；其二，ego network 分析方法文献（R2 Cross et al. 2001哈佛商业评论「社会资本的实际运用」）：一跳邻居+邻居间连边构成「可动员的合作资源」的度量单元；其三，中国官方人才政策语境（R3 科技部「高层次人才引进」相关政策表述）：引进评估看学术影响、团队网络、成果转化三维——与本子图三要素一一对应。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| ego network 一跳诱导（R1/R2） | 邻居框+诱导边 | 久新 talent_profile+collaborator | **锚** |
| 合作强度加权 | collaboration_score 列直查 | 久新边表 15 列 | 高 |
| 人才政策三维评估（R3） | 影响/网络/成果 | ego 度数+子图密度+co_* 计数 | 高 |
| UI seeded mock | buildDeepAnalysis | 演示用 | 需换真源 |

结论：方法侧 ego network 口径权威且与 UI 演示形态同构（抽屉里的力导向图就是 ego 网络），数据侧久新两表齐备——方法与数据都真实。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/mockData.js:968-981`（asset-008 定义）；`QueryAssetDeepAnalysisDrawer.jsx:119-126`（分析洞察卡）、`:95-106`（结构指标）；`queryAssetDeepAnalysis.js:20-30`（seeded mock 生成 KPI）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技知识图谱/服务展示.md` seq 446/447（excel_row 449/450），原文见附录 A。
- 权威方法：R1 Granovetter 1973；R2 Cross et al. 2001；R3 科技部人才政策。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（ego network 口径）**：给定候选专家 $e$，其引进评估子图 $G_e=(V_e,E_e)$：$V_e=\{e\}\cup\{v:(e,v)\in E_{collab}\}$（一跳邻居框，按确定性排序截断）；$E_e=\{(u,v)\in E_{collab}:u,v\in V_e\setminus\{e\}\}$（邻居间诱导边）。评估读数三组：①网络规模（$|V_e|$、ego 度数）；②内聚度（$\text{density}=|E_e|/\binom{|V_e|-1}{2}$）；③成果关联（$\sum \text{co\_paper}$、$\sum \text{co\_project}$、$\sum \text{co\_patent}$ 分列）。

**降档/升档触发器（B10 模板）**：①现状即可算（本件已验证）→ 维持完全转换支持；②预计算落子图结果表（夜批按候选清单批量生成）→ 升**完全直接支持**；③若需「引进优先级评分」（业务加权模型）→ 评分维度需求未立项，须甲方给定权重口径后再建（子图侧不受影响）；④久新人才域下线且仅剩 gkx 合作边 → 合作网可算但属性卡缺维（is_academician/discipline 等列 gkx 无），降部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/服务展示.md` |
| 所属 L4 | 图查询（seq 441-448，8 叶） |
| 本件 | 资产级挂载（seq 446 资产浏览 + seq 447 资产详情承载） |
| 同族件 | KGANALY_012（分析洞察，同一抽屉 `:119`）；KGANALY_050/051/052（结构指标表四读数，`queryAssetDeepAnalysis.js:50-55`） |
| UI 容器 | `QueryAssetDeepAnalysisDrawer.jsx`（深析抽屉） |

本件与 KGANALY_012/050/051/052 共享同一抽屉与同一 mock 生成器——「一份资产、五件读数」结构：本件管子图本体（节点+边+密度），012 管洞察文案，050-052 管结构指标表三个读数。数据侧判定互相独立（本件 ego 诱导边可算不代表 050 合作强度档可算，各件各自留证）。

## 二、计算过程

> 本件为子图构建类，本节给出**实测计算过程**——脚本 `code/M_SCIUI_KGANALY_004.py` 于 2026-11-02 在久新 live 库实算。

### 2.1 装载与规模校验

久新 `ads_talent_profile` 100,000 行、`ads_talent_collaborator` 5,051,578 行（族级快照同源零漂移）。gkx `dwd_scholar` 21,316 / `dwd_scholar_coauthor`（is_deleted=0）1,187,606——备选承载。dev 图词族 26 张全 0 行（§3.2）。

### 2.2 ego 选点（确定性）

引进评估的典型入口是「给定候选专家」；本件为验证管线取确定性锚点：合作度数 Top1——`SELECT talent_id, COUNT(*) FROM ads_talent_collaborator GROUP BY talent_id ORDER BY deg DESC, talent_id ASC`（实测 0.1s），得 `tal_4b1b1f43a3f84e60834711f6caebc790`（ego_degree=3,238；Top5 度数 3,238/2,352/2,302/2,157/2,129）。档载姓名「陈晓红/Xiaohong Chen」，ORCID 0000-0002-9797-8384，中文名列 name_zh 有值——人才域中文名可直接展示（与同族技术图 name_zh 全空相反，B9 对照披露）。

### 2.3 邻居框与诱导子图（B5 确定性）

一跳邻居按 `collaborator_talent_id` 拉取（`LIMIT 500` 确定性截断），去重排序得 500 邻居框。诱导边拉取路径经实测选型：`talent_id IN 邻居框`（分布键侧，500 个 → 69,524 行 16.7s 可行）而非 `collaborator_talent_id IN`（大框 JOIN 超时 1105，教训在案）——本地按对端落框过滤，得邻居间诱导边 **785** 条。

### 2.4 成果关联聚合（引进评估三联边的「成果」侧）

ego 全部合作边的成果计数求和：合作论文 **6,465** 篇、合作项目 **0**、合作专利 **0**（三列分列落键，B9——项目/专利计数列在库但该 ego 为 0，不混报不掩饰）。邻居间诱导边密度 $\text{density}=785/\binom{500}{2}=785/124{,}750=0.006293$（同框同池，`denominator_note` 落盘，B3）。

### 2.5 稳健性与口径敏感性

**（a）邻居框 500 vs 全量 3,238。**ego 实际度数 3,238，本件截断 500 是时效护栏（500 框诱导边拉取 17s 级；3,238 框的 `talent_id IN` 批拉预计 2 分钟级——可算但慢）。框是「合作最多/ID 最先」的前缀语义（LIMIT 无 ORDER BY 时 Doris 返回序不稳定——本件按 neighbor_id sorted 截断保证确定性）。**（b）诱导边语义。**`ads_talent_collaborator` 是按 talent_id 分区的有向存储（A→B 与 B→A 可能两行），本件以 canonical key `(min,max)` 去重——密度分母 C(500,2) 对应无向简单图口径。**（c）合作强度加权扩展。**`collaboration_score` 列在库（本件等权计边），加权密度口径留待算法侧裁定。

### 2.6 需求符合性预评

| 需求能力位（seq 446/447+资产 summary） | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 展示图表完整结构（网络图） | 力导向图 12 节点 mock | ego 500 邻居+785 诱导边实测 | **即期可回填**（前端 links 换 API） |
| 数据来源 | mock 标注「正式环境由图分析服务返回」 | 久新两表（profile+collaborator） | **已验证真源** |
| 候选专家×合作网络×项目成果关联 | 三要素在 summary/洞察文案 | ego 档（38 列属性卡）+邻接边+co_* 聚合 | **三维齐备**（项目/专利该 ego 为 0 属实数） |
| 人才服务台嵌入 | scenario 字段预留 | 子图 API 化后服务台直连 | 工程项 |

**预评结论**：结构三能力位即期可回填，评分口径位（引进优先级）待甲方——与完全转换支持判档一致。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_004.py`——三源只读（dev 读族级快照；gkx 经 `_gkxdb.py`；久新 live 直连含 1203 重试），零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_004.py`（约 13 秒）。
- 产物：`code/M_SCIUI_KGANALY_004_out.json`，关键读数——`facts.jiuxin_talent_profile_rows=100000`/`jiuxin_talent_collaborator_rows=5051578`（原料规模）；`facts.jiuxin_ego_talent_id`/`jiuxin_talent_degree_top5`（ego 选点）；`derived[0].neighbors_frame=500`/`induced_edges_within_neighbors=785`/`derived_density=0.006293`（子图三读数）；`derived[0].co_output_totals`：co_paper=6,465/co_project=0/co_patent=0（成果关联分列）；`absence_probe` 三件；`support_judgment="完全转换支持"`。
- 结果解读：真库真学者（可核 ORCID）的 ego 评估子图一次成型——度数千级的高联结学者 500 邻居框内仍有 785 条邻居互连，说明其合作圈有内聚结构（非纯放射状）；合作论文 6,465 篇印证网络资本的实证规模。
- 对照需求功能要求的评审：见 §2.6 预评（三能力位即期可回填）。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | 人才档 100,000（§2.1/§3.1） | `facts.jiuxin_talent_profile_rows` | 100000 | ✓ |
| 2 | 合作边 5,051,578（§2.1/§3.1） | `facts.jiuxin_talent_collaborator_rows` | 5051578 | ✓ |
| 3 | ego 度数 3,238（§2.2/摘要） | `facts.jiuxin_talent_degree_top5[0]` | 3238 | ✓ |
| 4 | ego 身份（陈晓红/ORCID，§2.2） | `facts.jiuxin_ego_profile_sample_fields` | tal_id/A5100373745/ORCID/陈晓红 | ✓ |
| 5 | 邻居框 500（§2.3） | `facts.jiuxin_ego_neighbor_frame` | 500 | ✓ |
| 6 | 诱导边 785（§2.3/摘要） | `facts.jiuxin_ego_induced_edges` | 785 | ✓ |
| 7 | 密度 0.006293（§2.4/摘要） | `derived[0].derived_density` | 0.006293 | ✓ |
| 8 | 密度分母 124,750（§2.4） | `derived[0].denominator_note` | 785/124750 | ✓ |
| 9 | 合作论文 6,465（§2.4/摘要） | `facts.jiuxin_ego_co_paper_total`/`derived[0].co_output_totals.co_paper` | 6465 | ✓ |
| 10 | 合作项目/专利 0（§2.4） | `derived[0].co_output_totals` | 0/0 | ✓ |
| 11 | gkx 备选 21,316/1,187,606（§2.1/§3.1） | `facts.gkx_scholar_rows`/`gkx_coauthor_edges_total` | 21316/1187606 | ✓ |
| 12 | 拉边路径选型（§2.3/§2.5a） | `facts.jiuxin_induced_pull_pairs_total` | 69524 | ✓ |
| 13 | 三源无结果面（§〇/§4.1） | `absence_probe`（3 件） | 0 命中 | ✓ |
| 14 | 判档完全转换支持（§〇/摘要） | `support_judgment` | 完全转换支持 | ✓ |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 候选专家属性档 | 久新 | `ads_talent_profile`（38 列） | **100,000** | 直查 | **足**（主承载） |
| D2 | 专家-专家合作边 | 久新 | `ads_talent_collaborator`（15 列） | **5,051,578** | 直查 | **足**（含强度/成果计数/合作年份） |
| D3 | 合作网络备选 | gkx | `dwd_scholar_coauthor` | 1,187,606 | 直查（经 `_gkxdb`） | 足（属性卡缺维） |
| D4 | dev 图结构面 | dev | graph_node/edge 等 26 张 | 0 | 结构在 | 空壳（非承载） |
| D5 | 现成「引进评估子图」结果面 | 三源 | 词族扫描 | — | 不存在 | 缺（转换计算正当性来源） |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 dev 空壳证据（族级快照复用）

dev 图词族 26 张（`_probe_s305_l3_call_out.json` 族级快照）全 0 行；非零 4 张（jimu_report_link 5/cms_expert_knowledge 61/cms_kg_relation 8/cms_kg_relation_type 7）均非图拓扑语义。dev 查询资产登记面不存在——8 条资产硬编码在 `mockData.js`。

### 3.3 久新人才域数据质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| 档案列 | 38 列（name_zh/is_academician/projects/discipline_*/bio/email/telephone） | 引进评估属性卡全维 |
| name_zh | 有值（ego=陈晓红） | 人才域中文名可直接展示（B9 对照技术图） |
| 边表列 | 15 列（collaboration_score/rank/co_paper/co_project/co_patent/first-latest_year） | 强度加权与成果关联在列 |
| 度数分布 | Top5：3,238/2,352/2,302/2,157/2,129 | 高联结学者锚点充足 |
| 成果计数 | 该 ego co_paper=6,465 / project=0 / patent=0 | 论文主导的合作画像（实测实报） |

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 人才档/合作边计数 | 100,000 / 5,051,578（live 直查=族级快照） |
| ego 选点幂等 | GROUP BY 排序固定，重跑同点 |
| 邻居框/诱导边 | 500 / 785（sorted+canonical 去重确定性） |
| 成果聚合 | 6,465 / 0 / 0（三列分列） |
| 脚本形态 | 三源只读+纯内存计算；零 demo_* |

## 四、数据缺失情况

### 4.1 现成结果面缺失（唯一结构缺口，非判定性）

三源无「引进评估子图」结果表（`absence_probe`）——完全转换支持而非完全直接支持的唯一原因。修复轻量：按候选清单（如某领域 TopN 学者）夜批预生成 ego 子图表，展示层直查。

### 4.2 引进评估评分口径未立项（口径级，非子图缺口）

「评估」的业务评分维度（引进优先级分/风险分）需求未给权重与公式——本件交付子图结构+三组读数（网络规模/内聚度/成果关联），评分模型待甲方给定口径后另立项。另：`co_project`/`co_patent` 计数列在库但当前 ego 值为 0——若引进场景需要项目/专利维度，须核实该两列的源覆盖（paper 源有、project/patent 源可能未回填），属源级缺口须披露。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| ego 子图 API 化（服务端算） | 数据工程（轻量） | 本件 + 012/050-052 | 抽屉直连真源 |
| 候选清单夜批预生成 | 数据工程 | 本件 | 升完全直接支持 |
| project/patent 源覆盖核实 | 数据工程 | 本件成果维 | §4.2 源级披露 |
| 引进评分口径立项 | 口径裁定 | 本件评估位 | 甲方给定权重 |

档位后果：预计算落表 → **完全直接支持**；现状 → 完全转换支持；久新人才域下线 → 部分支持（gkx 缺属性卡维）。

## 参考文献

1. Granovetter M S. The Strength of Weak Ties[J]. American Journal of Sociology, 1973, 78(6): 1360-1380. https://doi.org/10.1086/225469 （R1，2026-11-02 WebSearch 核验可达——合作网络结构位置与资源获取的经典理论，ego network 方法的学科源头）
2. Cross R, Nohria N, Parker A. Where Work Happens: The Office as a Social Network[J]. Harvard Business Review, 2001. https://hbr.org/2001/11/where-work-happens-the-office-as-a-social-network （R2，2026-11-02 WebSearch 核验可达——ego network 作为「可动员合作资源」度量单元的应用文献）
3. 科技部等. 高层次人才引进与支持相关政策[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/ （R3，2026-11-02 WebSearch 核验可达——引进评估「学术影响/团队网络/成果转化」三维的政策语境）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/服务展示.md》seq 446（excel_row 449）：

> ### 结果展示与快速浏览 · 序号 446
> #### 需规功能描述
> 所有查询或筛选的结果会以可视化列表、网格视图、小型缩略图等方式展现。每个图表或分析结果配有简明摘要标签和关键属性信息，让用户能够直观对比与快速浏览，进一步筛选出最感兴趣的内容，显著提升选择的效率。

seq 447（excel_row 450）：

> ### 图表详情与预览功能 · 序号 447
> #### 需规功能描述
> 点击具体的查询结果后，弹出详细页面，展示图表的完整结构、数据来源、分析流程、关联标签、使用场景说明等详细信息。用户可以先进行快速预览，无需跳转页面，即可初步判断图表内容的价值和适用性，决定是否深入分析或使用。

（「专家引进评估子图」名称本身未在 SRS 出现——属 UI 资产层命名；`mockData.js:968` asset-008 摘要「候选专家与合作网络、项目成果关联」即三要素原文。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 专家引进评估子图 | 全 SRS 目录 | 0（UI 资产层命名） |
| 专家/引进 | SRS 服务展示.md | 0（资产族通用描述） |
| 人才服务台 | mockData.js:981 | 1（scenario 字段） |
| talent_profile/collaborator | 久新 218 表 | 2（主承载） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_004_out.json`（2026-11-02 实算：ego 子图三组读数）。
- 共享探针：`code/_snapshots/_probe_s306_l1_out.json`（S3-06 族级：三源词族+人才域计数）、`_probe_s305_l3_call_out.json`（dev 图词族 26 张 0 行）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值/形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_talent_profile_rows` | 计数 | 100,000 | §2.1/§3.1 |
| `facts.jiuxin_talent_collaborator_rows` | 计数 | 5,051,578 | §2.1/§3.1 |
| `facts.jiuxin_talent_degree_top5` | 分布 | 3,238/2,352/… | §2.2 |
| `facts.jiuxin_ego_talent_id` | 选点 | tal_4b1b… | §2.2 |
| `facts.jiuxin_ego_profile_sample_fields` | 属性 | 陈晓红/ORCID 等 | §2.2 |
| `facts.jiuxin_ego_neighbor_frame` | 采样 | 500 | §2.3 |
| `facts.jiuxin_ego_induced_edges` | 实算 | 785 | §2.3 |
| `derived[0].derived_density` | 派生比 | 0.006293（denominator_note 落盘） | §2.4 |
| `derived[0].co_output_totals` | 聚合 | 6,465/0/0 | §2.4 |
| `absence_probe` | 探针 | 三件 | §3.2/§4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| ego network 一跳诱导 | R1/R2 | 久新两表（已实算） | 锚 |
| 合作强度加权 | collaboration_score | 边表列在库 | 高（扩展位） |
| 政策三维评估 | R3 | 度数/密度/co_* | 高（评分位待裁） |
| UI seeded mock | buildDeepAnalysis | 演示用 | 需换真源 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 专家属性档 | 空壳 | dwd_scholar 21,316（27 列无院士/学科深维） | **100,000（38 列）** |
| 合作边 | 空壳 | coauthor 1,187,606 | **5,051,578** |
| 引进评估结果面 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 抽屉（seeded） | — |
| v1（**本件已验证**） | ego 子图 API 化（500 框实测） | 结构验证完成 |
| v2 | 候选清单夜批预生成（升完全直接支持） | 轻量工程 |
| v3 | 评分口径 + 强度加权 | 甲方裁定 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| co_project/co_patent 源未回填 | 中 | §4.2 源覆盖核实 |
| 大框诱导边拉取超时（1105） | 中 | 分布键侧批拉路径（本件在案） |
| 评分口径悬空导致「评估」名不副实 | 中 | §4.2 立项前置 |

### C.5 总判

**完全转换支持**：三源无结果面（轻量可补）+久新人才域两表结构数据量均足+ego 子图实算验证（500/785/6,465）。夜批落表即升完全直接支持。

## 附录 D 复现与对照清单

| 项 | 命令/路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_004.py` | 退出码 0，落 `_out.json`（约 13 秒） |
| ego 幂等 | 度数排序固定 | 同点 tal_4b1b… |
| 实算一致 | `derived[0].induced_edges_within_neighbors` | 785 |
| §二 实算 | 完全转换支持档 | 有真实计算过程（非从缺） |
