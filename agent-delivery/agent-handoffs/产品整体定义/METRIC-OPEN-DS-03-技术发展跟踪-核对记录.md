# METRIC-OPEN-DS-03-技术发展跟踪-核对记录

> **任务**：DS-03-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 10 → **METRIC-ID-ASSIGN** 赋号草稿）  
> **角色**：product-agent（口径草稿 + 赋号）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **赋号**：`TEMP_DS03_*` 已升正式草稿 `M_TECH_*`（**类型未签** / 未入 seed）。见 **§赋号表**。WORKFLOW 整页 N/A **不造 ID**。  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-03` **全部** `page_id`（读全 catalog：仅 `DS-03-WORKFLOW` / `DS-03-RESULT`）。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 分页闭合（口径草稿 + 赋号草稿） | **RESULT = kit**（四图读面有统计核）。**WORKFLOW = N/A + 依据**（工作流壳，catalog note：不在本页跑专题技术链 Job）。卡面正式草稿号 = **`M_TECH_*`**（§赋号表）；`TEMP_DS03_*` 仅对照。**禁止**写入 seed；**禁止**消费 `M_CHAIN_*` / `M_SVC_*`。`algorithm_type` = `suggested_unsigned`。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 DS03-B01…B03。无本页专属甲方 Q0xx 需新开（客户决策清单无「技术发展跟踪」专条）。本叶不改 `客户决策清单跟踪表.md`、不升 🟢。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 §赋号表可回指。门 1 完整闭合仍须 seed 入号 + 公式会签。赋号草稿 ≠ aligned。 |
| PDR-06 自检 | ⏳ 有条件 | ADS 读面 STAT 可写演示口径；热点/阶段/成熟度 = 实现类 third_party，公式 `pending_cosign`。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：DS-03 **非整包 N/A**。`DS-03-RESULT` **④ 适用（kit）**；`DS-03-WORKFLOW` **④ 不适用（N/A + 依据）**。甲方未冻权重不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本叶必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `DS-03-WORKFLOW` | 技术评估工作流 | **N/A** | 无（seq 52–55 壳；**不造 ID**） | 挂专题 Job；发明 `M_EVAL_WF_*`；把壳打成 A 类 missing |
| `DS-03-RESULT` | 技术评估结果 | **kit** | §赋号表 7 个 `M_TECH_*` | 把专题 OPEN 当本页语义层；消费 `M_CHAIN_*` / `M_SVC_*` 当本页正式 ID；发明 `M_EVAL_*` / `M_DS03_*`；把草稿号写入 seed |

catalog 本 `ds_id` **只有这两页**。不扩 DS-02 / DS-04。

### §1.2 需规八叶 × 差集（A2 已判定，本叶不改 mapped/missing）

| 招标叶子 | seq | 宿主页 | 差集 | ④ |
|----------|-----|--------|------|----|
| 话题热力图展示 | 48 | RESULT | third_party（05 seq 134） | kit |
| 地理分布图展示 | 49 | RESULT | other_system（GIS+ADS） | N/A（图壳；数走 TEMP_ 投资/综合） |
| 动态气泡图展示 | 50 | RESULT | third_party（位置维 seq 137） | kit（核=阶段/成熟度/规模/投资） |
| 弦线图展示 | 51 | RESULT | mapped（05 seq 105） | kit |
| 评估流程概览 | 52 | WORKFLOW | n/a_ops | N/A |
| 评估方法详解 | 53 | WORKFLOW | n/a_ops | N/A |
| 评估参数配置 | 54 | WORKFLOW | n/a_ops | N/A |
| 评估结果追踪 | 55 | WORKFLOW | other_system（BFF 读 ADS） | N/A |

A 类 missing **两边都是 0**。不得因「无正式 M_* / 未会签」把上表改成 missing。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文，**不改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml`。指针写入本叶独立 patch。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-03 两页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-03-WORKFLOW.yaml` | 应收口：`metric_open_status: present`；`kit_or_na: na_with_reason`；path=本文件。现行 `n/a_documented` 与本叶 N/A **同向**，只补指针。**库缺口 `missing` 不动**（本页 A=0）。 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-03-RESULT.yaml` | 应收口：`metric_open_status: present`；`kit_or_na: kit`；path=本文件。删「无 METRIC-OPEN」句中已被本叶覆盖者（RS-B01 文件级闭合）。A=0 仍 0。 |
| A2 catalog | `ds_id=DS-03` 两行 | 由 `missing`（缺 OPEN 叶）改为 present + 本文件。**禁止**把 third_party/other_system 改成 mapped 来「好看」 |
| TRACE / WF | **无**展示态势四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-03-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。页面要哪些指标：展示 `human:李伟`；技术维九新交付形态 `human:郭万迎`（给人说明责任矩阵）。

详设 04 算法映射：**03 技术发展跟踪 · M · ADS 评估结果与工作流 · 不在本页跑专题技术链 Job**。

---

## §2 模块消费矩阵（TEMP_ 对照 · 终态见 §赋号表）

> 差集列维持 A2 已写判定。本表只闭合语义层。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` 不再作页面终态**：正式草稿号见 **§赋号表**；**禁止**写入 `metrics/registry/` seed。  
> 与专题 `TOPIC-TECH-05` **同 05 叶、不同页**：本页是展示读面，不跑 Job，不把专题 OPEN 当本页语义层。同口径才共享 ID（见 Q-MO-DS03-02/03）。

| temp_id | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|------|-------------------|---------|
| TEMP_DS03_TOPIC_HEAT | 热力图：关注度/活跃程度；xlsx 技术话题热度 | ✅ kit | MODEL（third_party · seq 134） | 禁伪展开；禁 mapped seq 96(11)；正式号 `M_TECH_TOPIC_HEAT` |
| TEMP_DS03_TECH_MATURITY | 气泡位置维；xlsx 技术成熟度 | ✅ kit | MODEL（third_party · seq 137） | 禁 `M_CHAIN_TECH_MATURITY_SCORE` |
| TEMP_DS03_TECH_STAGE | 气泡位置维；xlsx 技术发展阶段 | ✅ kit | MODEL（third_party · seq 137） | 禁 `M_CHAIN_PHASE_DETERMINATION` / `CYCLE_STAGE`；禁改挂 seq 132 |
| TEMP_DS03_TECH_SCALE | 气泡大小；xlsx 技术规模 | ✅ kit | STAT（ADS other_system） | seq 96 无「技术规模」专名；禁把论文/专利抄成规模 |
| TEMP_DS03_INVESTMENT | 气泡大小 / 地理投资分布；xlsx 投资额 | ✅ kit | STAT（ADS other_system） | 交易额 ≠ 投资额；禁 mapped seq 96(9)(10)；禁 `M_CHAIN_MARKET_SIZE` |
| TEMP_DS03_REL_STRENGTH | 弦线线粗；xlsx 关联强度 | ✅ kit | GRAPH（mapped · seq 105） | 影响路径 ≠ DS-02-PATH；禁 `M_SVC_GRAPH_*` / `M_SYNTH_ELEM_CONTRIB` |
| TEMP_DS03_COMPOSITE_SCORE | 下钻报告读数；xlsx 综合得分 | ✅ kit | COMPUTE（赋号建议；OPEN 草稿曾写 STAT 读面） | 禁 mapped 综合 182–191；本页不跑综合评价 Job |

**7/7 TEMP_ 均有差集判定 + 本叶 present。** 不得因「口径未冻 / D1 missing / 无正式 M_*」改成差集 `missing`。

## §赋号表

> 协议：`METRIC-ID-ASSIGN-LOOP-循环工程.md`。ELEMENT=`TECH`（本页非监测大盘，不用 `INNOV`）。WORKFLOW **0** 号。建议类型 **未签**（`suggested_unsigned`）。未改 seed / 展示 catalog / 共享 QUESTIONS。

| temp_id | metric_id | 复用 | 建议 type（未签） | Q |
|---------|-----------|------|-------------------|---|
| TEMP_DS03_TOPIC_HEAT | `M_TECH_TOPIC_HEAT` | 新建。禁 `M_CHAIN_HOTSPOT_SCORE` | MODEL | Q-MO-DS03-02 |
| TEMP_DS03_TECH_MATURITY | `M_TECH_MATURITY_LEVEL` | 新建。禁 `M_CHAIN_TECH_MATURITY_SCORE` | MODEL | Q-MO-DS03-05 |
| TEMP_DS03_TECH_STAGE | `M_TECH_LIFE_STAGE` | 新建；**建议专题同口径复用本号**。禁 `M_CHAIN_PHASE_DETERMINATION` / `CYCLE_STAGE` | MODEL | Q-MO-DS03-03 |
| TEMP_DS03_TECH_SCALE | `M_TECH_OUTPUT_SCALE` | 新建。禁 `M_CHAIN_MARKET_SIZE` / `M_SVC_SZ_SCALE` | STAT | Q-MO-DS03-01 |
| TEMP_DS03_INVESTMENT | `M_TECH_INVEST_AMOUNT` | 新建。禁 `M_CHAIN_MARKET_SIZE` | STAT | — |
| TEMP_DS03_REL_STRENGTH | `M_TECH_REL_STRENGTH` | 新建。禁 `M_SYNTH_ELEM_CONTRIB` / `M_SVC_GRAPH_*` / `M_ENT_RELATION_STRENGTH` | GRAPH | Q-MO-DS03-06 |
| TEMP_DS03_COMPOSITE_SCORE | `M_TECH_COMPOSITE_SCORE` | 新建。禁专题 `SZ_ASSESS`、禁抄 seq 182–191 | COMPUTE | Q-MO-DS03-04 |

**计数**：赋号 7 / 复用 0 / 新建 7 / Q 6 / WORKFLOW ID 0。类型：MODEL×3 · STAT×2 · GRAPH×1 · COMPUTE×1。

叶级卡：`metrics/request/_work/id-assign/DS-03-METRIC-OPEN-L01.yaml`；Question：`…/DS-03-METRIC-OPEN-L01-questions.yaml`（**不**写入共享 `METRIC-SEMANTIC-QUESTIONS.md`）。

---

## §3 ④ 指标语义卡（按招标叶子 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「Java `/display/v1/**` 薄 BFF 只读 ADS」为准，**不**把项目 DWD 反推成 ODS `full`（A1 双表未交）。

8 件套草稿字段（共同）：metric_id=§赋号表 `M_TECH_*`（`temp_id` 对照）；源系统=科技信息展示系统·技术发展跟踪（读面）；更新频率=未定；version=`draft-id-assign-ds03`；源表=ADS 评估结果（A1 表未交 → 本叶不填伪 full）。Job 宿主 = 专题技术链 / 第三方，**不在本页跑**。`algorithm_type` = 建议未签。

### §3.1 话题热力图 · kit（Bid seq 48；excel_row 51）

| temp_id / metric_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS03_TOPIC_HEAT → **`M_TECH_TOPIC_HEAT`** | 技术话题热度 | 选定时间窗内，按技术领域关键词/主题聚合的关注度与活跃程度；支撑热力分布与悬停下钻详情 | 实现类：对照 05 seq 134（研究热度 / 关键词权重 / 专家活跃度）。**禁止**本页伪展开。读 ADS 已落库专题/第三方结果 | MODEL |

时间轴、悬停、点击下钻 = 图壳 → §3.6。禁止 mapped seq 96 资讯热点标签。与专题 TECH-D04/D05 **同叶不同页**。

### §3.2 地理分布图 · N/A（Bid seq 49；excel_row 52）

展示 GIS + ADS 图层：区域上的发展水平 / 应用情况 / 投资分布。缩放、图例筛选、点击报告 = 图壳。

- **无独立算法核**（A2 RS-D03 `other_system`）。禁止 mapped 综合 seq 182–191、seq 104「地理位置」抽取、seq 96 区域论文/专利。
- 图上若出现数字：投资分布走 `M_TECH_INVEST_AMOUNT`（TEMP_DS03_INVESTMENT）；综合/发展读数走 `M_TECH_COMPOSITE_SCORE`。**不另造**「区域发展水平 / 区域排名」正式 ID（xlsx 行 33 区域排名不进本五级）。
- 点击「发展建议」**不是** seq 140 深圳布局 Job。

### §3.3 动态气泡图 · kit（Bid seq 50；excel_row 53）

气泡本身是图种，核在四维编码：

| temp_id / metric_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS03_TECH_MATURITY → **`M_TECH_MATURITY_LEVEL`** | 技术成熟度 | 技术从概念到应用转化的成熟水平；气泡**位置**维之一 | 对照 seq 137 成熟度输入；实现类不伪展开 | MODEL |
| TEMP_DS03_TECH_STAGE → **`M_TECH_LIFE_STAGE`** | 技术发展阶段 | 萌芽/成长/成熟等生命周期阶段；气泡**位置**维之一 | 对照 seq 137；禁产业链阶段 ID | MODEL |
| TEMP_DS03_TECH_SCALE → **`M_TECH_OUTPUT_SCALE`** | 技术规模 | 成果/应用体量（默认不含投入）；气泡**大小**编码之一 | ADS 读面字段；seq 96 无专名，禁论文量/专利量冒充 | STAT |
| TEMP_DS03_INVESTMENT → **`M_TECH_INVEST_AMOUNT`** | 技术投资额 | 资金投入规模；气泡大小或地理「投资分布」编码 | ADS 读面；禁技术交易额公式、禁 `M_CHAIN_MARKET_SIZE` | STAT |

调坐标轴 / 时间轴播放 / 点击气泡 = 图壳 → §3.6。禁止改挂 seq 132 历程模型。xlsx 商业化前景 / 市场渗透率 **不进**本五级（§3.6）。

### §3.4 弦线图 · kit（Bid seq 51；excel_row 54）

| temp_id / metric_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS03_REL_STRENGTH → **`M_TECH_REL_STRENGTH`** | 技术关联强度 | 技术–技术边的关联紧密程度；弦线粗细。影响路径=弦上关系流向可视化 | 边权重随 05 seq 105 关系抽取。不伪展开中心度 | GRAPH |

可与 `DS-02-TECHGRAPH` / `TOPIC-TECH-05` **同叶不同页**。禁止：DS-02-PATH 关键路径、seq 116 综合图谱 API、`M_SVC_GRAPH_*`、`M_SYNTH_ELEM_CONTRIB`（专题已 missing，不重列、无 also_in）。旋转/缩放/筛选 = 图壳。

### §3.5 综合得分 · kit（半成品 xlsx 行 32；下钻报告）

| temp_id / metric_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS03_COMPOSITE_SCORE → **`M_TECH_COMPOSITE_SCORE`** | 评估综合得分 | 多项评价指标加权后的综合评价结果，供本页读面/下钻报告展示 | ADS 已落库字段。**禁止**把 seq 182–191 抄成我方公式；本页不跑综合评价 Job | COMPUTE |

### §3.6 ④ 不适用（N/A + 依据）

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| `DS-03-WORKFLOW` seq 52 | 评估流程概览 | n/a_ops | 流程图 + 进度高亮 + 导航。「分析计算」是节点标签，不是本页调用 05 seq 134–140 |
| 同上 seq 53 | 评估方法详解 | n/a_ops | 四类经典评价方法说明/模板。方法推荐 ≠ seq 134–140 Job |
| 同上 seq 54 | 评估参数配置 | n/a_ops | 权重/阈值表单与模板库。禁把 05 散文权重抄成公式；禁发明 `M_EVAL_PARAM_*` |
| 同上 seq 55 | 评估结果追踪 | other_system | display BFF 读 ADS 已落库运行。不是四类结果图。禁 mapped seq 132/136/137 |
| RESULT seq 49 | 地理分布图展示 | other_system | GIS 图壳；无独立算法核。数走 `M_TECH_INVEST_AMOUNT` / `M_TECH_COMPOSITE_SCORE` |
| RESULT 交互 | 时间轴/悬停/下钻/缩放/播放/筛选 | n/a_ops | 图壳；禁改挂 seq 132 |
| 半成品不进本五级 | 市场活跃度 / 商业化前景 / 市场渗透率 / 区域排名（xlsx 29–31、33） | 不进差集 | 无本五级宿主；禁 missing；潜力语义归专题 TECH-D06，不改挂 |
| 本叶范围外 | `TOPIC-TECH-05` 热点/潜力/阶段/瓶颈 **Job 执行** | other_system / 专题页 | **禁止**在 DS-03 跑专题技术链 Job；禁止把那些模型打成本页 missing |
| 本叶范围外 | DS-02 技术点网 / 关键路径；DS-04 全球监测 | other_system | 弦线影响路径 ≠ PATH；地理分布 ≠ 城市创新能力 |
| B 轨形近 | `M_CHAIN_TECH_MATURITY_SCORE` 等 | 禁止消费 | 产业链口径，不得顶替本页技术评估读面 |
| 无独立核 | 发展水平专名、应用情况专名、气泡图种本身 | 语义债 DS03-B02 | 禁止另造区域排名等正式 `M_*` |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| DS03-B01 / RS-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 18 才改指针 | 语义欠账→有指针；非 A 类 missing |
| DS03-B02 / RS-B02 | 热度/阶段/成熟度/关联强度等已赋 `M_TECH_*` 草稿，**未入 seed** | 语义债降为「身份草稿待入 registry」；不把建议类型写入 seed 当已签 |
| DS03-B03 / RS-B03 | PDR-05/06 有条件；公式/权重未签；实现类不伪展开 | ⏳ `pending_cosign: human:唐绍祖`；类型 `suggested_unsigned` |
| WORKFLOW 壳 | 无统计义务；A2 已 `n/a_documented` | 保持 N/A；**不造 ID** |
| 客户决策清单 | 无 DS-03 专条 | **不改共享 QUESTIONS / 跟踪表**；叶级 `Q-MO-DS03-01…06` 待 coordinator 合流 |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未改共享 `METRIC-SEMANTIC-QUESTIONS.md`。未新建 `data-gap-catalog`。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/display/v1/**` 薄 BFF → 只读 ADS。不直连 Python `/internal/*`，不在本页起专题技术链 Job。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。技术维实现类倾向 third_party（九新形态：`JIUXIN-TECH-ORG-TALENT-L01` / 郭万迎）。 |
| 算法库 05 | 热度 134 / 阶段 137 = third_party（库已列叶，不是 missing）。弦线 105 = mapped。地理/规模/投资/综合 = other_system。WORKFLOW 不 mapped 05。 |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不把 B 轨 / 专题 ID 改挂；不新建 gap catalog。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **仍无**本页 ID → 回指 **本记录 §赋号表 `M_TECH_*`**，**禁止**点开 `M_CHAIN_*` / `M_SVC_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 实现类未冻：⚠️「待甲方确认」挂 `Q-MO-DS03-*`（评审模式）；关闭评审 DOM 零泄漏
- 赋号草稿未入 seed：D1 按 `draft` 诚实；**不**标 `aligned`；**不显伪齐备 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner = 展示 `human:李伟`；STAT → GDF ADS + Java 聚合；MODEL/GRAPH/Job 计算仍归唐绍祖监管 Python；九新 third_party 对接 `human:郭万迎`

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/METRIC-OPEN-DS-03-技术发展跟踪-核对记录.md`（含 **§赋号表**） |
| 机器卡 | `metrics/request/_work/open-loop/DS-03-METRIC-OPEN-L01.yaml`（`demands` 已换 `M_TECH_*`） |
| 赋号卡 | `metrics/request/_work/id-assign/DS-03-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/DS-03-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（本叶独立） | `metrics/request/_work/open-loop/DS-03-METRIC-OPEN-L01-a2-patch.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-03-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog / pages 正文；共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml` / `METRIC-SEMANTIC-QUESTIONS.md` / `客户决策清单跟踪表.md` |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _赋号草稿已出：RESULT 7 条 `M_TECH_*` 全新建；WORKFLOW N/A 不造 ID；零消费 `M_CHAIN_*` / `M_SVC_*`；类型未签_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方专属 Q | — | 无本页专条；不新开、不升 🟢 | |
