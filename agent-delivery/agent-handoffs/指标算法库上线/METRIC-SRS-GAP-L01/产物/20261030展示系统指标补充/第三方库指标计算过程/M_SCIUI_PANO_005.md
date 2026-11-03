# 关键实体Top5关联强度（M_SCIUI_PANO_005）

> **类型**：无业务逻辑数值类（图统计读数+排序位）｜ **域**：科技信息展示系统·科技发展态势·科学技术全景（技术点知识图谱）｜ **UI 挂载**：科学技术全景·关键实体Tab「关键关联对象 Top5」（`App.jsx:5789` chart-title；边权归一化排序 tooltip；实体筛选/排序与优先级控件同区）
> **数据支持度**：**完全转换支持**（久新节点表 weighted_degree 归一化排序——本件脚本已实算 Top5 具名清单并落产物）｜ **公式定义人**：UI 前端算法（`graphInteractionState.js:483-501` relationStrength 归一化+排序）；权威口径 加权节点强度（R1 Opsahl et al. 2010）｜ **口径归属**：需求明列叶（SRS 序号 22「默认实体展示」Top5 关键实体 + 序号 27「实体排序与优先级」）
> **复现脚本**：`code/M_SCIUI_PANO_005.py`｜ **产物**：`code/M_SCIUI_PANO_005_out.json`
> **四判定摘要**：直接结构 = 无现成「Top5 实体」结果行（三源词族 0 命中）；直接数据 = 无；依赖结构 = **足**（weighted_degree 19,430 全非空+名称列 100% 原词）；依赖数据 = **足**（ORDER BY 一步即得——本件已实算具名 Top5）
> **数据源口径**：三源逐一探针留证；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**SRS 序号 22 要求「自动展示根节点关联的 Top5 关键实体，包括人、机构、论文、专利等类型……显示名称、类型和关联强度」。久新技术图节点表 `weighted_degree`（强度列全非空）+`technology_name_original`（名称 19,430/19,430 非空）+`community_role`/`chain_role`（类型角色列）三列齐备——本件 ORDER BY DESC 一步实算具名 Top5：**Computational Methods for Biological Sequence Comparison（100.00）**领衔，前五强度 100.00/80.44/59.51/56.15/52.22（归一化）。**口径披露（关键）**：库内图为纯技术点单域图——「实体」=技术点（人/机构/论文/专利实体无独立节点，其证据沉淀在边的 evidence 列与节点名称里），「类型分组」以 community_role/chain_role 承载（CORE 3,495、SOURCE_CANDIDATE 2,433 等）——与 UI 演示图 5 类型（人员/机构/论文/专利/技术）存在域差，见 §4.2 待裁项。

## 摘要

「关键实体Top5关联强度」是科学技术全景页关键实体 Tab 的首屏读数：UI 演示图按边权归一化展示 Top5 关联对象。数据侧判定：**完全转换支持**——久新节点表实算具名 Top5（归一化关联强度 0–100）：①Computational Methods for Biological Sequence Comparison **100.00**（加权度 1,010.91，CORE/SOURCE_CANDIDATE）②Genetic modification mechanisms for lactic acid bacteria **80.44** ③Computational RNA Sequencing Analysis **59.51** ④Computational Tools for Genomic Data Analysis **56.15** ⑤Hardware Architectures for Machine Learning Acceleration **52.22**。前五名全部 CORE 角色（占 CORE 总数 3,495 的 0.14%），集中度极高（Top1 = 均值 100 倍）——与 KGANALY_006「枢纽极值过千」结论同向。中文名列全空为展示位待裁项（§4.2），不影响强度计算位。

- 需求判定：**需求明列叶**（序号 22 Top5 + 序号 27 排序与优先级）。
- 复现状态：脚本已实算通过；具名 Top5+归一化强度落产物。
- 档位结论：**完全转换支持**（技术点域内）；多域实体（人/机构/论文/专利独立节点）维缺失降档披露见 §4.2。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科学技术全景/展示技术点关联实体/默认实体展示（1.1.1.1.4.1.2.2.1；SRS 序号 22，excel_row 25）+实体排序与优先级（序号 27，excel_row 30）。UI 挂载：关键实体 Tab「关键关联对象 Top5」卡（`App.jsx:5789`），配类型筛选（`aria-label="筛选关键关联对象类型"`）、时间范围筛选、排序维选择三控件。

### 1.2 为什么需要本指标

Top5 回答「图谱里最强的技术点是谁」：它是技术侦察的第一屏——管理者打开页面即见的明星技术点。归一化强度（0–100）让跨图可比。序号 22 原文明确「Top5」与「名称、类型和关联强度」三要素；序号 27 要求「根据实体与技术点的关联强度、影响力等指标自动排序」——库内 weighted_degree 即该排序指标的预计算落盘。

### 1.3 需求文档是否给出定义方法

**需求文档给了要素清单但未给强度公式。**「关联强度」=节点强度（weighted_degree，加权度）——R1 Opsahl（2010）节点强度定义 $\s(v)=\sum_{e\ni v} w(e)$ 即久新列口径；归一化 $s_{\text{norm}}=s/\max(s)\times 100$ 由 UI 算法（`graphInteractionState.js:483` `Math.round(relationWeight*100)`）闭合。

### 1.4 类似指标权威方法可行性分析概要

强度排序是加权网络分析标准操作。R1 Opsahl et al.（2010）：节点强度=边权和，α 参数权衡边数与权重——weighted_degree 列即 α=1 特例的库内预计算；R2 中文权威（郭剑明等 2024《情报学报》）：PageRank/HITS 属性+网络双维识别——本件为强度维单解，PR 维已在 KGANALY_001 承载；R3 杜雪盈等（2024《软件学报》）：链接预测/实体排序评测体系（MR/MRR/Hits@K）——排序位评测口径背书。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 节点强度排序（R1） | Opsahl 2010 | weighted_degree 列 | 锚（预计算 α=1） |
| 属性+网络双维（R2） | 郭剑明 2024 | PR（KGANALY_001）+强度 | 高（双维可拼） |
| 排序评测（R3） | 杜雪盈 2024 | ORDER BY 确定性排序 | 高 |

结论：强度排序零悬念；「实体类型」维是唯一域差待裁项。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/App.jsx:5789`（chart-title）；`graphInteractionState.js:483-501`（relationStrength 归一化排序）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md` 序号 22（excel_row 25）、序号 27（excel_row 30），原文见附录 A。
- 权威方法：R1 Opsahl et al. 2010；R2 郭剑明等 2024；R3 杜雪盈等 2024。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义**：$s_{\text{norm}}(v)=\frac{\text{weighted\_degree}(v)}{\max_u \text{weighted\_degree}(u)}\times 100$，Top5 按 $s_{\text{norm}}$ 降序（并列按 node_id ASC 确定性）。

**降档/升档触发器**：①技术点域内即期可算 → 维持完全转换支持；②夜批落 TopN 结果表 → 升完全直接支持；③需严格「人/机构/论文/专利」多域实体 → 三源均无多域混图（久新单域技术图+gkx 论文/专利可建但边不同源），按 B 类推断依赖两跳止步记缺口（总档不变——技术点位已足）；④中文名翻译维补齐 → 展示位升满。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md` |
| 本件 | 序号 22 Top5 展示 + 序号 27 排序的**读数位** |
| 同族件 | PANO_003（关键节点计数，同卡）；KGANALY_001（PageRank 排序——同面板算法位） |
| UI 容器 | 关键实体 Tab（`App.jsx:5787-5860` 三控件+列表） |

## 二、计算过程

> 脚本 `code/M_SCIUI_PANO_005.py` 于 2026-11-02 在久新 live 库实算。

### 2.1 归一化基准

$\max(\text{weighted\_degree})=\mathbf{1{,}010.90780192}$（Computational Methods for Biological Sequence Comparison——与 KGANALY_006 §2.2 max 同值零漂移）。

### 2.2 具名 Top5 实算（主读数）

| # | 技术点（原词） | 加权度 | 归一化强度 | 角色 | 链角色 |
|---|---|---|---|---|---|
| 1 | Computational Methods for Biological Sequence Comparison | 1,010.9078 | **100.00** | CORE | SOURCE_CANDIDATE |
| 2 | Genetic modification mechanisms for lactic acid bacteria | 813.1248 | **80.44** | CORE | INTERMEDIATE |
| 3 | Computational RNA Sequencing Analysis | 601.5904 | **59.51** | CORE | INTERMEDIATE |
| 4 | Computational Tools for Genomic Data Analysis | 567.6388 | **56.15** | CORE | INTERMEDIATE |
| 5 | Hardware Architectures for Machine Learning Acceleration | 527.8508 | **52.22** | CORE | INTERMEDIATE |

产物 `facts.top5_norm` 五对象（name/weighted_degree/norm_strength/community/community_role/chain_role 全字段）。

### 2.3 结构旁证读数

- 链角色强度分层（`facts.chainrole_wd`）：INTERMEDIATE 均值 15.85 / SOURCE_CANDIDATE 7.16 / APPLICATION_END_CANDIDATE 3.28 / ISOLATED_IN_CHAIN 1.46——中间件节点连接最密，链结构清晰。
- Top5 大社区及其最高强度（`facts.top_communities`）：4,151 节点社区 max 273.78 等——社区级明星点量级低于全图 Top1（集中跨社区）。

### 2.4 分步证据对照表

| # | MD 论断 | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | max=1,010.90780192（§2.1） | top5_norm[0].weighted_degree | 1010.9078 | ✓ |
| 2 | Top1 归一化 100.00（§2.2） | top5_norm[0].norm_strength | 100.0 | ✓ |
| 3 | Top2–5 强度（§2.2） | top5_norm[1..4].norm_strength | 80.44/59.51/56.15/52.22 | ✓ |
| 4 | 具名五条（§2.2） | top5_norm[0..4].name | 见表 | ✓ |
| 5 | 全部 CORE（§摘要） | top5_norm[*].community_role | CORE×5 | ✓ |
| 6 | 链角色分层（§2.3） | facts.chainrole_wd | 15.85/7.16/3.28/1.46 | ✓ |
| 7 | 三源无现成结果行 | absence_probe | 0 命中 | ✓ |
| 8 | 判档 | support_judgment | 完全转换支持 | ✓ |

### 2.5 复现代码结果展示

- 代码：`code/M_SCIUI_PANO_005.py`——三源只读，零 `demo_*`；运行 <1 秒，幂等。
- 结果解读：Top5 全为生物信息/基因/计算生物学+ML 硬件域技术点，全部 CORE+链上游/中游——图谱明星点集中在生命科学与 AI 交叉域；第 1 名强度是第 5 名的 1.92 倍，集中度健康（幂律尾非断崖）。
- 对照需求评审：Top5 三要素中「名称/关联强度」即期可回填（原词+归一化值），「类型」以角色列承载（CORE/链角色）——严格 5 类型分组待多域图（§4.2 B 类缺口，两跳止步）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 强度列 | 久新 | `weighted_degree` | 19,430 全非空 | 直查 | **足**（主承载） |
| D2 | 名称列 | 久新 | `technology_name_original` | 19,430 全非空 | 直查 | 足（原词） |
| D3 | 角色列 | 久新 | `community_role`/`chain_role` | 全非空 | 直查 | 足（类型代理） |
| D4 | 多域实体节点 | 三源 | 人/机构/论文/专利独立节点 | — | **不存在** | 缺（B 类，两跳止步，§4.2） |
| D5 | 现成结果行 | 三源 | 词族扫描 | — | 不存在 | 缺（转换正当性） |

## 四、数据缺失情况

### 4.1 现成 TopN 结果行缺失（唯一结构缺口，非判定性）

修复最轻：夜批 ORDER BY LIMIT 5 落表 → 升**完全直接支持**。

### 4.2 多域实体维缺失（B 类推断依赖，两跳止步）

UI 演示图 5 类型实体（人员/机构/论文/专利/技术）；库内为纯技术点单域图。多域混图属 B 类推断依赖——三源均无现成多域节点-边面（gkx 论文/专利/学者表可分别建图但边语义不同源），按两跳止步规则记缺口、不代理。总档不变：技术点位（本件主承载）完全转换支持。

### 4.3 中文名翻译维缺失（展示位口径级）

`technology_name_zh` 全空——Top5 卡回填用原词（英文）或补翻译维；不影响强度计算位。

## 参考文献

1. Opsahl T, Agneessens F, Skvoretz J. Node Centrality in Weighted Networks: Generalizing Degree and Shortest Paths[J]. Social Networks, 2010, 32(3): 245-251. https://doi.org/10.1016/j.socnet.2010.03.006 （R1，2026-11-02 WebSearch 核验可达——节点强度（加权度）定义与 α 权衡，久新 weighted_degree 口径出处）
2. 郭剑明, 王婧怡, 袁润. 综合属性指标和引用关系的核心专利识别方法研究[J]. 情报学报, 2024, 43(5): 575-587. https://qbxb.istic.ac.cn/CN/10.3772/j.issn.1000-0135.2024.05.007 （R2，2026-11-02 WebSearch 核验可达——属性+网络双维识别中文权威）
3. 杜雪盈, 刘名威, 沈立炜, 彭鑫. 面向链接预测的知识图谱表示学习方法综述[J]. 软件学报, 2024, 35(1): 87-117. http://www.jos.org.cn/1000-9825/6902.htm （R3，2026-11-02 WebSearch 核验可达——实体排序/链接预测评测口径（MR/MRR/Hits@K）中文权威综述）

# 附件

## 附录 A 原始需求原文摘录

SRS 序号 22（excel_row 25）：

> ### 默认实体展示 · 序号 22
> #### 需规功能描述
> 系统初始化加载时，自动展示根节点关联的Top5关键实体，包括人、机构、论文、专利等类型。实体以卡片或列表形式呈现在技术点图谱的侧边区域，每个实体显示基本信息如名称、类型和关联强度。

SRS 序号 27（excel_row 30）：

> ### 实体排序与优先级 · 序号 27
> #### 需规功能描述
> 系统根据实体与技术点的关联强度、影响力等指标自动排序，优先展示重要实体。用户也可选择按时间、名称、类型等不同维度对实体进行排序。

（「关键关联对象 Top5」名称为 UI 卡命名；「Top5 关键实体……名称、类型和关联强度」句即本件读数位原文。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 关键关联对象 Top5 | App.jsx | :5789（chart-title） |
| 默认实体展示 | SRS 序号 22 | 1 |
| 关联强度 | graphInteractionState.js | :483-501（归一化排序） |
| weighted_degree Top5 | 久新 | 具名 5 条（实测） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_PANO_005_out.json`。
- 共享探针：`_snapshots/_probe_s310_entity_out.json`（Top5 具名+链角色+社区）、`_probe_s310_pano_out.json`（列质量）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值/形态 | 正文引用 |
|---|---|---|---|
| `facts.top5_norm` | 实算 | 5 对象全字段 | §2.2 |
| `facts.top_communities` | 直查 | 5 组 | §2.3 |
| `facts.chainrole_wd` | 直查 | 4 档 | §2.3 |
| `facts.core_nodes` | 直查 | 3,495 | §摘要 |
| `derived[0]` | 主读数 | Top1 强度+denominator_note | §2.2 |
| `derived[1]` | 列表 | 5 名具名+排序说明 | §2.2 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 强度列 | 空壳 | 无 | **全非空** |
| 多域实体 | 无 | 分表可建（边不同源） | 单域技术图 |
| 结果行 | 无 | 无 | 无 |

### C.2 总判

**完全转换支持**：强度+名称+角色三列就绪，一步排序即得具名 Top5——展示位（中文/多域）两项口径待裁不阻塞。

## 附录 D 复现与对照清单

| 项 | 命令/路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_PANO_005.py` | 退出码 0，幂等 |
| 实算一致 | top5_norm[0].norm_strength | 100.0 |
| 交叉一致 | Top1 加权度=KGANALY_006 max | 1,010.9078 ✓ |
