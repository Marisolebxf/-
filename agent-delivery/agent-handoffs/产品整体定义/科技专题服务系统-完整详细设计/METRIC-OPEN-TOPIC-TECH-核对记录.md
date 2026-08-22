# METRIC-OPEN-TOPIC-TECH-核对记录

> **任务**：TOPIC-TECH-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 3）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 04 + 05.1 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：专题技术链分析 **一整包** `page_id=TOPIC-TECH-05` 的 ④ 指标语义卡 + ⑤ 开放项。覆盖 05.1 **六招标叶子**里进算法差集的那些。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **赋号**：`TEMP_*` 已升正式草稿 `M_TECH_*`（§赋号表）；**非 seed 终态**。与 DS-02 论文/专利计数同口径则共享号，**不**把 DS-02 OPEN 改挂为本页唯一消费。  
> **与九新叶分责**：本叶 = 语义 / 适用性 / 赋号草稿；交付形态（SQL / Python / API）= `JIUXIN-TECH-ORG-TALENT-L01`（郭万迎对北京九新）。本叶不写九新接口清单。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 六招标叶子中：论文/专利计数、热度指数、潜力评分、阶段判定、深圳综合评估、瓶颈清单均有页面统计/评估语义 → **出卡**。正式草稿 ID 见 **§赋号表**（`TEMP_*` 对照保留）。**禁止**写入 seed；**禁止**把 DS-02 OPEN 改挂为本页唯一消费。实现类 **third_party 不伪展开公式**。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 TECH-B01…B06。展示 DS-02 / DS-03 口径 **不改挂**为本页 Q。本叶不改 `客户决策清单跟踪表.md`、不升 🟢。Q068 颠覆标签 = 明确不做，不进卡。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/TOPIC-TECH-05.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | COUNT 类可写演示公式；MODEL/Job 实现类公式 **禁止**把 05 深度分析散文抄成我方公式，一律 `pending_cosign`。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |
| 页面要哪些指标（实现清单） | `human:郭万迎`（对九新；李伟辅助） | 给人说明责任矩阵；**不等于**本叶语义 Owner |
| 功能实现 Owner | 待指定 | 给人说明：技术链未点名；不得猜 Owner |

**结论**：本页 **④ 适用（kit）**，**非整页 N/A**。全景可视化 / 节点下钻清单 / NLP 建图面 / 深圳 ODS 提取 / 子图过滤壳 / 转化流程图 / 历程 CMS / 展示 DS-02 全景 → **N/A + 依据**（§3.8）。甲方 🟡 与 LLM 501 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本页必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `TOPIC-TECH-05` | 专题技术链分析（整包） | **kit** | §赋号表 6 个 `M_TECH_*`（`TEMP_*` 对照） | 写入 seed；把 DS-02 OPEN 改挂为本页唯一；挂 `DS-03-METRIC-OPEN`；用 `M_CHAIN_*` 顶替；把本页 A=0 改成 missing；把 third_party 05 散文抄成公式 |

**展示科学技术全景（A2.2 / DS-02）**：本叶 **不消费**。`DS-02-TECHGRAPH` / `DS-02-ENTITY` / `DS-02-PATH` / `DS-02-MAINTAIN-GRAPH` / `DS-02-MAINTAIN-ENTITY` 与 `DS-02-METRIC-OPEN-L01` **不是**本页语义层（05.1 对象=技术点专题分析；DS-02 是展示全景图壳。同源 05 seq 104/105/130 **不同页**）。

**展示技术发展跟踪（DS-03）**：本叶 **不消费**。热点/潜力/阶段 Job 宿主在专题六叶子，禁止改挂展示跟踪页。

### §1.2 05.1 六招标叶子 × 差集

| 招标叶子 | 05.1 算法 | 标签 | 差集 | ④ |
|----------|-----------|------|------|----|
| 全景图谱 | `.4.1` 可视化 + `.4.2` 下钻材料 | G1 读面 A | mapped（TECH-D01/D02）；计数 TECH-D03 mapped | 计数 **kit**；可视化/清单 **N/A** |
| 新技术热点 | `.4.5` | M/G3 **Job** | third_party（TECH-D04/D05；seq 134） | 热度 **kit**（不伪展开）；NER **N/A** |
| 产业化潜力 | `.4.6` | **G3 Job** | third_party（TECH-D06/D07；seq 135） | kit（不伪展开） |
| 阶段研判 | `.4.8` | M/G3 **Job**；LLM 未注册 501 | third_party（TECH-D08/D09；seq 137） | kit（不伪展开） |
| 深圳技术发展 | `.4.2` 过滤 + `.4.4` `.4.9`～`.4.11` | M/G3；A 过滤 + Job | D10 `other_system`；D11 mapped；D12 third_party | 综合评估 **kit**；ODS/过滤壳 **N/A** |
| 转化瓶颈 | `.4.7` | **G3 Job** | third_party（TECH-D13/D14；seq 136） | 瓶颈 **kit**（不伪展开）；流程图 **N/A** |

历程 **不是**六招标叶子：`.4.3` = **CMS/ADS** → `n/a_ops`（TECH-D15；05 seq 132 叶存在禁止 missing）。

### §1.3 TRACE / A2 语义层指针（Round 17 才回写 catalog 正文）

本叶 **不改** `metrics/request/专题系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/TOPIC-TECH-METRIC-OPEN-L01-a2-patch.yaml`（**仅本叶 entries**；不改共享 `METRIC-OPEN-LOOP-a2-patch.yaml` / `LOOP-state.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | `TOPIC-TECH-05` 唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/专题系统/pages/TOPIC-TECH-05.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: TOPIC-TECH-METRIC-OPEN-L01`。**库缺口 `missing` 不动**（本页 A 类本就为空）。仍 **禁止写入 seed**。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `TOPIC-TECH-05` | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（TECH-B01 文件级闭合） |
| TRACE / WF | **无**专题技术链四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 04 叙述发明 `M_*` |
| PACK | 无独立 `TOPIC-TECH-PACK-L01` | SRS 04 + `05.1-技术链.md` 顶 PACK；FDS **不顶** OPEN；九新叶 **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。展示 DS-02/DS-03 **不升**、不改挂。

---

## §2 模块消费矩阵（TEMP_ 对照 · 正式草稿见 §赋号表）

> 差集列维持 A2 已写 **mapped / third_party / other_system / n/a_ops**（A=0）。本表只闭合语义层：落点 + 适用性 + 开放项。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` 非页面终态**：正式草稿 ID = §赋号表 `M_TECH_*`；**禁止**写入 `metrics/registry/` seed。  
> **third_party 行**：卡面给身份与适用性；公式栏只写「实现类 / 第三方，不伪展开」，**禁止**把 seq 134/135/136/137/133/138/139/140 散文中的加权/阈值抄进本卡。

| temp_id | metric_id（草稿） | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|-------------------|------|-------------------|---------|
| TEMP_TOPIC_TECH_PAPER_PATENT_CNT | M_TECH_PAPER_PATENT_CNT | 全景下钻：技术点论文量 / 专利量 | ✅ kit | STAT | 与 DS-02 `TEMP_DS02_ENT_PAPER_PATENT` 同口径共享本号，不改挂 DS-02 OPEN；禁 `M_CHAIN_SZ_PATENT` / `REG_PAPERS` / `REG_PATENT` |
| TEMP_TOPIC_TECH_HEAT_INDEX | M_TECH_HEAT_INDEX | 热点：热度指数 / 增长曲线 | ✅ kit | third_party | G3 **Job**；不伪展开；NER → §3.8；类型见 Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_POTENTIAL_SCORE | M_TECH_POTENTIAL_SCORE | 潜力评分 + 多技术对比面 | ✅ kit | third_party | G3 **Job**；seq 135 三维散文不抄；禁 `M_CHAIN_HIGH_VALUE_RATIO`；Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_STAGE | M_TECH_STAGE_JUDGE | 阶段自动判定 + 用户参数研判 | ✅ kit | third_party | G3 **Job** + LLM **未注册 501**（TECH-B03）；禁 `M_CHAIN_PHASE_DETERMINATION` / `CYCLE_STAGE`；Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_SZ_ASSESS | M_TECH_SZ_ASSESS | 深圳潜力与阶段综合评估 | ✅ kit | third_party | G3 **Job**；seq 133/138/139/140 同层；独立号 vs 切片见 Q-MO-TECH-01；禁 `M_CHAIN_SZ_*` |
| TEMP_TOPIC_TECH_BOTTLENECK | M_TECH_CONVERT_BOTTLENECK | 瓶颈自动识别与归因 | ✅ kit | third_party | G3 **Job**；禁 `M_CHAIN_BOTTLENECK_*`；Q-MO-TECH-02 |

**6/6 TEMP_ → 6 个 `M_TECH_*` 草稿。** 不得因「口径未冻 / D1 missing / 类型未签 / 实现类」把上表改成差集 `missing`。third_party **不是**库未列叶，禁止打 A 类 missing。仍禁止写入 seed。

---

## §3 ④ 指标语义卡（按招标叶子 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以 05.1「Java `/topic/v1/technology/**` 只读 ADS」+ A1 技术链维 ODS 判定为准，**不**把项目 DWD 反推成 ODS `full`。A1 技术链维排期 8/24 晚–8/25，本叶双表未交。

8 件套草稿字段：metric_id=**§赋号表**（`TEMP_*` 对照）；源系统=科技专题服务系统·技术链维；更新频率=未定；version=`draft-id-assign-r1`；源表=ADS 专题技术点（A1 表2 未交 → 本叶不填伪 full）。对象 = **技术点**（`entity_type=technology`）；论文/专利 = 材料 + 清单 + 计数。`algorithm_type` = suggested_unsigned。

### §3.1 全景图谱 · 计数 kit / 可视化 N/A（Bid seq 13–14；05 `.4.1` / seq 130、105、104、96）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_PAPER_PATENT_CNT | 技术点论文量 / 专利量 | 选定技术点关联的论文去重数量、专利去重数量（材料+清单上的计数面）。下钻定义/应用/关联企业是清单，无独立核 | 演示：`COUNT(DISTINCT paper_id)` / `COUNT(DISTINCT patent_id) WHERE technology_id=?`。不伪展开增长率。交易额/资讯无招标宿主 → TECH-B04，**不新造 TEMP_** | STAT |

可视化本身（TECH-D01）与节点下钻清单（TECH-D02）见 §3.8。正式草稿 `M_TECH_PAPER_PATENT_CNT`（与 DS-02 ENTITY 论文/专利计数同口径共享，不改挂 DS-02 OPEN）。禁止用引用网冒充技术链。不消费 `M_CHAIN_NODE_COUNT` / `M_CHAIN_EDGE_COUNT`。关联企业是技术点边，**不是** `TOPIC-ENT-05`。

### §3.2 新技术热点 · kit（Bid seq 15–16；05 `.4.5` **G3 Job** / seq 134）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_HEAT_INDEX | 技术热点热度指数 | 对已对齐技术点做频次/聚类后的热度与趋势（热度指数、增长曲线、热点报告）。判断短期热点 vs 长期趋势 | **实现类 / 第三方 Job，不伪展开热度公式**。05 seq 134 散文不得抄进本卡。页上 **不做 NER**（建图面抽技术点，TECH-D04 → §3.8） | third_party |

**Job，不是全景 G1 图算。** 正式草稿 `M_TECH_HEAT_INDEX`（§赋号表）。不是 missing（库已列叶）。类型见 Q-MO-TECH-02。

### §3.3 产业化潜力 · kit（Bid seq 17–18；05 `.4.6` **G3 Job** / seq 135）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_POTENTIAL_SCORE | 技术产业化潜力评分 | 按 `technology_id` 输出产业化潜力综合分；支撑多技术雷达/排名/对比报告（对比面同核，不另造 ID） | **实现类 / 第三方，不把 seq 135「科研/转化/市场三维加权」抄成我方公式**。输入含论文量/专利量特征（M）+ A 面子图结构，特征口径未签 | third_party |

特征用 `M_TECH_PAPER_PATENT_CNT` 作 **输入材料**，不把潜力分改挂为 STAT。正式草稿 `M_TECH_POTENTIAL_SCORE`。不消费 `M_CHAIN_HIGH_VALUE_RATIO`。

### §3.4 阶段研判 · kit（Bid seq 19–20；05 `.4.8` **G3 Job** / seq 137）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_STAGE | 技术阶段判定 | 输出技术所处阶段及简要说明（状态、关键瓶颈、发展潜力）。用户参数嵌入提示词后重跑为同核定制面，不另造 ID | **实现类 / 第三方 + LLM 未注册 501**（TECH-B03）。不伪展开阶段公式。禁止用联网检索散文冒充已注册模型 | third_party |

**Job。** 正式草稿 `M_TECH_STAGE_JUDGE`。禁止 `M_CHAIN_PHASE_DETERMINATION` / `M_CHAIN_CYCLE_STAGE`。501 不写成 A 类 missing。

### §3.5 深圳技术发展 · kit（Bid seq 21–22；05 `.4.2` + `.4.4` `.4.9`～`.4.11`）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_SZ_ASSESS | 深圳技术潜力与阶段综合评估 | 基于深圳切片输出潜力评分、发展阶段、优劣势与建议（问题/机遇/布局/细分同层 Job，不另造 ID）。潜力/阶段计算复用 §3.3 / §3.4 核，不发明第二套公式 | **实现类 / 第三方 Job，不伪展开**。seq 133/138/139/140 已列叶，不算库缺失 | third_party |

公开数据提取（TECH-D10）与子图 A 过滤（TECH-D11）见 §3.8。正式草稿 `M_TECH_SZ_ASSESS`（独立号 vs 切片 → Q-MO-TECH-01）。不消费 `M_CHAIN_SZ_*` / `M_CHAIN_SZ_PATENT`。

### §3.6 转化瓶颈 · kit（Bid seq 23–24；05 `.4.7` **G3 Job** / seq 136）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TECH_BOTTLENECK | 技术转化瓶颈识别 | 标识转化堵点并给原因与改进建议（清单/报告）。输入 `technology_id` | **实现类 / 第三方，不伪展开归因公式**。专家知识库步骤未签 | third_party |

流程图/时间轴展示转化阶段（TECH-D13）无独立统计核 → §3.8；**不是**历程 CMS（D15）。正式草稿 `M_TECH_CONVERT_BOTTLENECK`。禁止 `M_CHAIN_BOTTLENECK_TECH` / `M_CHAIN_BOTTLENECK_COUNT`。

### §3.7 ④ 明确不做（不进卡、不 missing）

| 项 | 依据 |
|----|------|
| Q068 颠覆标签 / 颠覆指数 | 05.1 §2/§7：`substitutes` 边不得对外写成颠覆指数。不发明 `TEMP_…_DISRUPT` |
| 论文点类型；引用网冒充技术链 | 05.1 §7；子图必须 `entity_type=technology` + 技术链边（演进/依赖/掌握/应用/产业化） |
| seq 96 技术交易额 / 区域交易额 / 技术动态资讯 | 04 十二叶与 05.1 主视图未挂 → TECH-B04；库叶已在，禁止本页 missing，不新造 TEMP_ |

### §3.8 ④ 不适用（N/A + 依据）

整页 N/A：**无**（六招标叶子均有至少一处统计/评估核，见 §2）。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| 全景 `.4.1` | 技术网络可视化（TECH-D01 / seq 13 / seq 130+105） | **mapped**（差集）/ ④ **无独立核** | G1 读面 A 子图。禁止用节点数/边数 KPI 顶替（不消费 `M_CHAIN_NODE_COUNT` / `EDGE_COUNT`）。不发明图谱统计 `M_*` |
| 全景下钻 | 技术节点深度下钻清单（TECH-D02 / seq 14 / seq 104） | **mapped** / ④ **无独立核** | 定义/代表论文/核心专利/典型应用/关联企业 = 材料+清单；计数走 `M_TECH_PAPER_PATENT_CNT`。不把 `TOPIC-ENT-05` 算进本页 |
| 热点 `.4.5` | 智能语义热点提取 NER（TECH-D04 / seq 15） | **third_party** / ④ **无独立核** | 建图面抽技术点，**不在页上 NER**（05.1 §5）。热度指数走 `M_TECH_HEAT_INDEX` |
| 深圳提取 | 深圳区域数据专项提取（TECH-D10 / seq 21） | **`other_system`** | 数据工厂/ODS，不是深度挖掘算法叶。禁止 missing、禁止改挂 seq 131 |
| 深圳过滤 | 深圳技术链子图 A 过滤（TECH-D11 / seq 131） | **mapped** / ④ **无独立核** | 读面 A 产品过滤；无独立 metric_id。不消费 `M_CHAIN_SZ_*` |
| 转化 `.4.7` | 技术转化流程可视化（TECH-D13 / seq 23） | **third_party** / ④ **无独立核** | 流程图/时间轴；与 D14 同叶流程面。不是历程 CMS |
| 历程 `.4.3` | 技术发展历程（TECH-D15 / seq 132） | **`n/a_ops`** | 05.1 明文 CMS/ADS，不用 B 面时间轴。seq 132 叶存在 → **禁止 missing**，也不把 CMS 改判 mapped |
| 本叶范围外 | 展示 DS-02 科学技术全景五页 | **`other_system`** | **禁止**把 `DS-02-METRIC-OPEN-L01` 改挂为本页唯一消费。仅论文/专利计数与 `TEMP_DS02_ENT_PAPER_PATENT` 同口径共享 `M_TECH_PAPER_PATENT_CNT`。同源 05 叶 **不同页** |
| 本叶范围外 | 展示 DS-03 技术发展跟踪 | **`other_system`** | 禁止把专题热点/潜力/阶段 Job 改挂展示跟踪；热度/阶段口径不同，不 reuse DS-03 TEMP |
| 本叶范围外 | 产业链形近 ID（`CHAIN-TOPIC-*`） | 他页 mapped | 禁止 `M_CHAIN_TECH_POWER` / `M_CHAIN_TECH_MATURITY_SCORE` / `M_CHAIN_TECH_BARRIER_INDEX` / `M_CHAIN_BOTTLENECK_TECH` / `M_CHAIN_SZ_PATENT` / `M_CHAIN_REG_PATENT` / `M_CHAIN_REG_PAPERS` / `M_CHAIN_REG_TECH_MATURITY` / `M_CHAIN_REG_TECH_BARRIER` / `M_CHAIN_PHASE_DETERMINATION` / `M_CHAIN_CYCLE_STAGE` |
| 本叶范围外 | `TOPIC-ENT-05` / `TOPIC-ORG-05` / `TOPIC-TALENT-05` | 兄弟页 | 下钻「关联企业 / 代表论文」是技术点材料，不把企业/科研/人才分析模型算进本页 |
| 本叶范围外 | `TOPIC-OPS` / `TOPIC-DATAREQ` | `n/a_ops` | 给人说明 §8.4：运营/需求面走 N/A，不算缺 OPEN 任务 |
| 无独立核的分项 | 交易额/资讯、颠覆指数、用户参数分项、深圳四 Job 分维、增长曲线独立核 | 语义债 TECH-B02/B04/B06 + Q068 | **禁止**另造 ID 或把草稿写入 seed |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| TECH-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 17 才改指针 | 语义欠账→有指针；非 A 类 missing |
| TECH-B02 | 页上统计/评估已有赋号草稿（§赋号表）；**仍未入 seed** | 语义债；覆盖判定仍 mapped/third_party |
| TECH-B03 | 阶段研判 LLM 未注册 501；D08/D09 已 third_party 对上 seq 137 | 语义债；不写成 A 类 missing |
| TECH-B04 | 基础指标交易额/资讯无招标宿主；不新造 TEMP_ | 语义债；seq 96 叶禁止 missing |
| TECH-B05 | PDR-05/06 有条件；公式未签 | ⏳ |
| TECH-B06 | 实现类权重/阈值不伪展开 | 语义债；口径待算法定义卡 + 甲方 |
| Q068 | 颠覆标签 | 明确不做；不进本页卡、不 missing |
| DS-02 / DS-03 展示口径 | **展示**科学技术全景 / 技术发展跟踪 | 保持独立叶；**本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。叶级 Question：`Q-MO-TECH-01` / `Q-MO-TECH-02`（`id-assign/TOPIC-TECH-METRIC-OPEN-L01-questions.yaml`，一律 🟡）。不写共享 `METRIC-SEMANTIC-QUESTIONS.md`。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/topic/v1/technology/**`（门面名以实现叶为准）→ 只读 ADS。热点/潜力/阶段/瓶颈/深圳综合 = **Job**；全景/深圳子图 = A 面 G1（Nebula 当前图，`entity_type=technology`）。Java 不写 NLP / 不直连 nGQL。 |
| 准入 / ODS | 技术点主数据走要素库；A1 技术链维 14 叶表2 未交 → 本叶 D3 不得伪 `full`。展示 DS-02 图壳 **不**自动当作专题分析核。 |
| 算法库 05 | 基础计数 / 图谱×2 / 全景 / 深圳子图 mapped；热点/潜力/阶段/瓶颈/深圳四 Job = third_party（库已列实现类，不算我方库缺失）；历程 CMS = n/a_ops。A1 双表未交 → `A1需规ID` 空。 |
| 实现类红线 | algo-catalog default_hint：技术链实现类倾向 third_party，**禁止伪展开公式**。 |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不把 DS-02 OPEN 改挂为本页唯一；不新建 `data-gap-catalog`；不写共享 QUESTIONS.md / LOOP-state / 展示 catalog。 |
| 九新叶 | `JIUXIN-TECH-ORG-TALENT-L01` 交 SQL/Python/API 形态；本叶不代替郭万迎对九新谈交付。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **仍无**本页 ID → 回指 **本记录 §赋号表草稿**，**禁止**点开展示 DS-02 伪 8 件套，**禁止**点开 `M_CHAIN_*` 形近 ID
- Wave 0：🧪 MockBadge
- 维名/权重/501 未冻：⚠️「待甲方确认」（文案走 TECH-B* / Q-MO-TECH-*，不要写展示 DS-02 字样到专题 DOM）
- 草稿未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 页面要哪些指标 Owner = `human:郭万迎`（对九新）；功能实现 Owner **待指定**（给人说明）。STAT → GDF ADS + Java 聚合（Owner 指定后）；Job / third_party 计算仍归唐绍祖监管类型会签（给人说明 §2.3）
- 热点 Job **禁止同步卡死页面**（05.1 §6）

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-TECH-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-TECH-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-TECH-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-TECH-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（仅本叶） | `metrics/request/_work/open-loop/TOPIC-TECH-METRIC-OPEN-L01-a2-patch.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-TECH-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文；展示 catalog / pages；共享 `METRIC-OPEN-LOOP-a2-patch.yaml`；`LOOP-state.yaml`；`METRIC-SEMANTIC-QUESTIONS.md`；其它 OPEN 叶；DS-02 OPEN |

---

## §8 赋号表（TEMP → M_* · 类型未签）

> 真源：`metrics/request/_work/id-assign/TOPIC-TECH-METRIC-OPEN-L01.yaml`。`TEMP_*` **非终态**。未写 seed。类型 = `suggested_unsigned`。

| temp_id | metric_id | reuse | 建议 type | Q |
|---------|-----------|-------|-----------|---|
| TEMP_TOPIC_TECH_PAPER_PATENT_CNT | M_TECH_PAPER_PATENT_CNT | 同口径共享（DS-02 `TEMP_DS02_ENT_PAPER_PATENT`；seed 无号，`reuse_of=null`） | STAT | — |
| TEMP_TOPIC_TECH_HEAT_INDEX | M_TECH_HEAT_INDEX | 新号（不 reuse DS-02/DS-03 热度） | third_party | Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_POTENTIAL_SCORE | M_TECH_POTENTIAL_SCORE | 新号 | third_party | Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_STAGE | M_TECH_STAGE_JUDGE | 新号（不 reuse `M_CHAIN_PHASE_*` / DS-03 阶段维） | third_party | Q-MO-TECH-02 |
| TEMP_TOPIC_TECH_SZ_ASSESS | M_TECH_SZ_ASSESS | 新号（独立综合包 vs 切片 → Q） | third_party | Q-MO-TECH-01 |
| TEMP_TOPIC_TECH_BOTTLENECK | M_TECH_CONVERT_BOTTLENECK | 新号 | third_party | Q-MO-TECH-02 |

**计数**：赋号 6 / seed reuse 0 / 同口径共享 1 / Q 2。类型分布：STAT 1、third_party 5。

---

## §9 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；适用性：TOPIC-TECH-05 **kit**；可视化/NER/ODS/过滤壳/流程图/历程 CMS / 展示 DS-02 N/A 见 §3.8；**零**写入 seed；**不**把 DS-02 OPEN 改挂为本页唯一；third_party **不伪展开**_ | 2026-08-22 |
| 赋号草稿 | 淮政玮（product-agent 代拟） | _6 条 `M_TECH_*`；1 条与 DS-02 论文专利同口径共享；类型 suggested_unsigned；Q-MO-TECH-01/02 🟡_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 页面清单 / 九新交付形态 | 郭万迎 | _本叶不代替；见 `JIUXIN-TECH-ORG-TALENT-L01`_ | |
| 甲方 Q068 / 展示 DS-02 | — | Q068 不做；DS-02 不改挂为本页唯一 | |
