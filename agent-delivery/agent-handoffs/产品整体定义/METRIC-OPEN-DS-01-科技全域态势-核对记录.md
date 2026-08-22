# METRIC-OPEN-DS-01-科技全域态势-核对记录

> **任务**：DS-01-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 8）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01 / FDS；本工作流书面 **SRS 02 科技全域态势.md 顶 PACK**（给人说明 §8.4 甲）。**FDS 不顶 PACK、不顶 OPEN**。详设 `04-功能-科技发展态势.md` 只作读面对照，不顶 PACK。  
> **范围**：展示 catalog `ds_id=DS-01` **全部** `page_id`：`DS-01-FACTORS` / `DS-01-LAYERS` / `DS-01-MAP` / `DS-01-EVENTS`。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **禁止**：发明正式 `M_*` 写入 seed；把图层/地图操作编成统计核；重列专题 7 条 missing；改 A2 catalog / pages 正文；改 `LOOP-state.yaml` 与共享 `METRIC-OPEN-LOOP-a2-patch.yaml` / `METRIC-SEMANTIC-QUESTIONS.md`；消费 `M_ENT_*` / `M_SYNTH_ELEM_*` / `M_CHAIN_ACADEMIC_POWER` / `M_CHAIN_PATENT_COUNT` 顶替本页。  
> **赋号**：`TEMP_*` **非终态**。草稿 `M_*` 见 **§赋号表**；`algorithm_type` 均为 `suggested_unsigned`，未签。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用则出卡；不适用 N/A+依据 | **FACTORS / EVENTS = kit**（有数量、占比、趋势、影响力、关注度/等级等统计核）。**LAYERS / MAP = 整页 N/A**（GIS 配置与相机壳，无独立统计核）。SRS 02 与详设 04 **未挂**任何 `metric_id` → 卡面只用 **`TEMP_DS01_*`**；服务机构影响力允许 `metric_id_impl` 指向已有 B 轨 `M_SVC_ORG_TECH_SCORE`，**不新编**、不改 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 沿用 A2 pages 已写 SD-FACT-01…05、EVT-B01…03。**不新建** `Q0xx`、不改 `客户决策清单跟踪表.md`、不升 🟢。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + 机器卡可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | COUNT 类可写演示公式；第三方维写「不展开」；MODEL/GRAPH 公式 `pending_cosign`。库缺口行保持 A 类 `missing`，不因本叶 present 改 mapped。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：四页 **不是**同一判定。科创要素、科创事件 **④ 适用（kit）**；图层配置、地图操作 **④ 整页 N/A + 依据**（§3.11）。甲方 🟡 / 库 missing **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本叶必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `DS-01-FACTORS` | 科创要素 | **kit** | `TEMP_DS01_FACT_*`（§2）；服务机构影响力 **impl** 可指向已有 `M_SVC_ORG_TECH_SCORE` | 发明 `M_FACT_*`；挂 `M_SYNTH_ELEM_*`；用 `M_CHAIN_ACADEMIC_POWER` / `M_CHAIN_PATENT_COUNT` 顶替；消费 `M_ENT_*`；把本页 A 类 missing 改 mapped |
| `DS-01-LAYERS` | 图层配置 | **N/A** | 无 | 发明 `M_LAYER_*` / `M_GIS_*`；抢 FACTORS 热力/关联；把半成品要素/事件行改挂本页 |
| `DS-01-MAP` | 地图操作 | **N/A** | 无 | 发明 `M_MAP_*`；mapped 综合/图谱API seq 116 实体检索；因「智能匹配」打 missing |
| `DS-01-EVENTS` | 科创事件 | **kit** | `TEMP_DS01_EVT_ATTENTION` / `_INFLUENCE` / `_IMPORTANCE` | 发明 `M_EVENT_*`；用发展路径「重大事件」时间轴或 `M_CHAIN_NEWS_COUNT` 顶替；列表/详情 CMS 打成 missing |

**专题 missing 7 条不重列、无 also_in**：`M_CHAIN_PRODUCT_COUNT` / `M_CHAIN_PATENT_COUNT` / 环节健康度 / 全球成功案例 / `M_POLICY_INDUSTRY_FIT` / `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_COLLAB_OUTPUT_CORR`。

### §1.2 需规五级 × 差集（A2 已裁定，本叶不改判定）

| 五级 | seq / excel | 招标叶子 | 差集要点 | ④ |
|------|-------------|---------|----------|----|
| 地图操作 | 1–4 / 4–7 | 放大缩小、拖动平移、复位、搜索定位 | 全 `n/a_ops` 或 `other_system`；A=0 | **N/A** |
| 图层配置 | 5–8 / 8–11 | 多对象图层、实时监控、分组、数据源 | 全 `n/a_ops` 或 `other_system`；A=0 | **N/A** |
| 科创要素 | 9–13 / 12–16 | 基础信息、统计、分析、监测趋势、地图可视化 | mapped 统计/影响力若干；A 类：会议/项目/专利被引·SEP/期刊/聚类/预测/异常 | **kit** |
| 科创事件 | 14–16 / 17–19 | 时间筛选、重要性分级、详情 | 关注度/影响力/等级 A=3 missing；列表/详情 `other_system` | **kit**（三统计核） |

详设 04：DS-01 标签 **G1**；读面 **A 嵌图 + GIS + ADS**；嵌图可薄、挂接可空。GIS 与图坐标两套。图失败不挡 KPI。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 `pages/DS-01-*.yaml` 正文。指针写入 `_work/open-loop/DS-01-METRIC-OPEN-L01-a2-patch.yaml`（**不**追加共享 `METRIC-OPEN-LOOP-a2-patch.yaml`，由 coordinator 合流）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-01 四页唯一 OPEN 真源 |
| A2 页 yaml | `展示系统/pages/DS-01-{FACTORS,LAYERS,MAP,EVENTS}.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-01-METRIC-OPEN-L01`。**库缺口 `missing` 不动**。LAYERS/MAP 仍 `kit_or_na=na_with_reason`。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 四行 `ds_id=DS-01` | 删「无 METRIC-OPEN」语义；改为 present + 本文件。禁止把 N/A 页写成缺任务。 |
| TRACE / WF | **无** DS-01 四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-01-PACK-L01` | **SRS 02 顶 PACK**；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止新编正式 M_*）

> 差集列维持 A2 已写判定。本表只闭合语义层。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` ≠ 正式 `M_*`**：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。

### §2.1 `DS-01-FACTORS` · kit

| temp_id / 已有 ID | 主落点 | 适用 | 建议 type（未签） | 差集 | pending |
|-------------------|--------|------|-------------------|------|---------|
| TEMP_DS01_FACT_COUNT | 数量统计 | ✅ kit | STAT | mapped | 会议/期刊/项目/成果计数走 ADS（SD-FACT-01），不改 missing |
| TEMP_DS01_FACT_DIST | 分布比例 | ✅ kit | STAT | mapped | 半成品行 4；第三方不展开 |
| TEMP_DS01_FACT_GROWTH | 增长趋势 | ✅ kit | STAT | mapped | 历史趋势；预测另卡 FORECAST |
| TEMP_DS01_FACT_INFLUENCE_DEGREE | 要素间影响程度 | ✅ kit | GRAPH | mapped | seq 116 关系权重；禁 `M_SYNTH_ELEM_CONTRIB` / seq 187 |
| TEMP_DS01_FACT_ASSOC | 要素关联关系 | ✅ kit | GRAPH | mapped | 关系查询 API；禁 `M_SVC_GRAPH_*` 改挂、禁 missing B 轨 |
| TEMP_DS01_FACT_SCHOLAR | 专家学者影响力 | ✅ kit | MODEL | mapped | seq 162；第三方不展开；禁 `M_CHAIN_ACADEMIC_POWER` |
| TEMP_DS01_FACT_CONF | 会议影响力 | ✅ kit | MODEL | **missing** | 05 无会议专叶；不新造 `M_*` |
| TEMP_DS01_FACT_ORG | 科研机构影响力 | ✅ kit | MODEL | mapped | seq 99；禁 `M_SVC_ORG_TECH_SCORE` 顶替科研机构 |
| TEMP_DS01_FACT_ENT | 企业影响力 | ✅ kit | MODEL | mapped | seq 145；**禁** `M_ENT_*` |
| TEMP_DS01_FACT_SVC | 服务机构影响力 | ✅ kit | MODEL | mapped | **impl** 已有 `M_SVC_ORG_TECH_SCORE`；本页不新编、不改 seed |
| TEMP_DS01_FACT_PROJECT | 项目/课题影响力 | ✅ kit | MODEL | **missing** | 05 无项目评价专叶 |
| TEMP_DS01_FACT_PAPER | 论文影响力 | ✅ kit | STAT | mapped | seq 96 被引/影响因子；国际合作比例 SD-FACT-03 |
| TEMP_DS01_FACT_PATENT | 专利影响力 | ✅ kit | MODEL | **missing** | 被引/SEP 无专叶；禁 `M_CHAIN_PATENT_COUNT` 顶替、不重列 |
| TEMP_DS01_FACT_JOURNAL | 期刊影响力 | ✅ kit | MODEL | **missing** | 05 无期刊评价专叶 |
| TEMP_DS01_FACT_CLUSTER | 要素聚类 | ✅ kit | MODEL | **missing** | seq 96「聚类」是区域论文清洗句，不是本核 |
| TEMP_DS01_FACT_FORECAST | 监测趋势预测 | ✅ kit | MODEL | **missing** | 禁用 `M_SYNTH_ELEM_INDEX` 区域趋势顶替 |
| TEMP_DS01_FACT_ANOMALY | 监测异常点 | ✅ kit | MODEL | **missing** | 清洗≠监测异常检测 |

**17/17 统计核均有 TEMP_（或已有 impl 指针）+ 本叶 present。** 不得因「口径未冻 / D1 missing / 无正式 M_*」把上表改成「缺 OPEN」。**库 missing 七行保持 missing。**

### §2.2 `DS-01-EVENTS` · kit

| temp_id | 主落点 | 适用 | 建议 type（未签） | 差集 | pending |
|---------|--------|------|-------------------|------|---------|
| TEMP_DS01_EVT_ATTENTION | 事件关注度 | ✅ kit | MODEL | **missing** | 半成品行 2；口径需确认 EVT-B01 |
| TEMP_DS01_EVT_INFLUENCE | 事件影响力 | ✅ kit | MODEL | **missing** | 半成品行 3；禁把要素影响力九子项算进本页 |
| TEMP_DS01_EVT_IMPORTANCE | 重要性等级 | ✅ kit | MODEL | **missing** | SRS L6-2 点名自动分级；高/中/低 |

**3/3 统计核 kit + present。库缺口仍 missing。** 时间筛选/详情/关联展示/导出走 §3.11 N/A。

### §2.3 `DS-01-LAYERS` / `DS-01-MAP` · 整页 N/A

无 `demands[]` 统计 ID。见 §3.11。

---

## §3 ④ 指标语义卡（不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「display BFF 只读 ADS / GIS 配置+坐标」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技信息展示系统·科技全域态势；更新频率=未定；version=`draft-open-ds01`；源表=ADS 展示科创要素/资讯（A1 表2 未交 → 本叶不填伪 full）。

### §3.1 科创要素 · 基础统计 · kit（seq 10；半成品行 4–5）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS01_FACT_COUNT | 科创要素数量统计 | 选定范围下论文/专利/人才/企业/科研机构/服务机构等去重存量。会议/期刊/项目/成果无基础指标叶 → ADS 列表计数（SD-FACT-01），不另造 CNT ID | `COUNT(DISTINCT entity_id) GROUP BY factor_type`；第三方维不展开 | STAT |
| TEMP_DS01_FACT_DIST | 科创要素分布比例 | 对象在分类、区域或层级中的占比 | 占比=该类计数/当期集合；第三方不展开 | STAT |
| TEMP_DS01_FACT_GROWTH | 科创要素增长趋势 | 日/周/月/季/年历史增长率与趋势曲线。预测见 FORECAST，不混进本条 | 环比/同比未签；第三方基础指标含环比叙事 | STAT |

自定义统计维度、柱饼折线、导出 = 展示壳（FACT-D21），无独立核。

### §3.2 科创要素 · 关联与影响程度 · kit（seq 11；半成品行 6；05 seq 116）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS01_FACT_INFLUENCE_DEGREE | 要素间影响程度 | 实体间关系权重 / 网络指标，衡量相互作用强弱 | 图指标未签。禁止用七要素贡献路径或 seq 187 作用强度顶替 | GRAPH |
| TEMP_DS01_FACT_ASSOC | 要素关联关系 | 要素间关系查询与可视化；图失败不挡 KPI（详设 04 §6） | 关系查询 API；不另造协同指数（禁 `M_SYNTH_COLLAB_*`） | GRAPH |

B 轨 `M_SVC_GRAPH_INFLUENCE` / `CENTRALITY` / `DENSITY` **不改挂本页、不得 missing**。

### §3.3 科创要素 · 分类型影响力 · kit（seq 11；半成品行 7–15）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS01_FACT_SCHOLAR | 专家学者影响力 | 学术活动/成果/合作网络中的影响程度。半成品叙事 H 指数/引用/论文数 | 第三方不展开（seq 162 学术力）；维差 SD-FACT-02 | MODEL |
| TEMP_DS01_FACT_CONF | 会议影响力 | 投稿数/参与人数/会议热度等（半成品行 8） | **库无专叶**；禁止伪热度公式进 seed | MODEL |
| TEMP_DS01_FACT_ORG | 科研机构影响力 | 科研产出/合作/领域布局。半成品论文数/专利数/科研人数 | 第三方不展开（seq 99 综合科研实力）。禁止用服务机构技术力顶替 | MODEL |
| TEMP_DS01_FACT_ENT | 企业影响力 | 科技创新、成果转化、产业带动。半成品专利数/技术交易额/科研人数 | 对照 seq 145 技术力（辅 146/97）。**禁止消费 `M_ENT_*`** | MODEL |
| TEMP_DS01_FACT_SVC | 服务机构影响力 | 科技服务供给、资源连接、生态支撑 | impl 指向已有 `M_SVC_ORG_TECH_SCORE`（seq 179）；本页 `metric_id` 不新编 | MODEL |
| TEMP_DS01_FACT_PROJECT | 项目（含课题）影响力 | 项目数量/资助金额/实施效果；02「课题」按半成品并入项目（SD-FACT-05，待甲方确认） | **库无专叶**；seq 145 仅把项目库当企业技术力输入，不是本核 | MODEL |
| TEMP_DS01_FACT_PAPER | 论文影响力 | 被引 / 影响因子；国际合作比例无专核（SD-FACT-03） | 第三方不展开（seq 96）；不新造国际合作 ID | STAT |
| TEMP_DS01_FACT_PATENT | 专利影响力 | 专利被引次数 / 标准必要专利数量（半成品行 14） | **库无专叶**（05 仅有专利数量与领先主体）。禁止用专题 `M_CHAIN_PATENT_COUNT` 顶替，不重列 | MODEL |
| TEMP_DS01_FACT_JOURNAL | 期刊影响力 | 影响因子/发文量/高被引论文数 | **库无专叶**；seq 96 影响因子仅为机构筛选输入 | MODEL |

### §3.4 科创要素 · 分析/监测模型核 · kit（seq 11–12）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS01_FACT_CLUSTER | 要素聚类 | 将相似科创要素自动分类归纳 | **库无专叶**；禁止把区域论文「数据处理」一句写成 mapped | MODEL |
| TEMP_DS01_FACT_FORECAST | 监测趋势预测 | 基于历史数据预测特定要素未来趋势 | **库无要素实体时序预测**；综合 182/186/189/190 是区域指数报告，禁止顶替 | MODEL |
| TEMP_DS01_FACT_ANOMALY | 监测异常点识别 | 自动识别标记异常点与突变点 | **库无监测异常检测专叶**；异常值剔除=清洗，不是本核 | MODEL |

### §3.5 科创事件 · 三统计核 · kit（seq 15；半成品行 2–3、16）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS01_EVT_ATTENTION | 事件关注度 | 科技事件被关注和讨论的程度；作为重要性分级输入 | 未签；半成品「需确认」。05 无专叶 | MODEL |
| TEMP_DS01_EVT_INFLUENCE | 事件影响力 | 对行业、区域或舆情的影响强度；作为分级输入 | 演示「影响力分值」未签。禁止把要素影响力九子项算进本页 | MODEL |
| TEMP_DS01_EVT_IMPORTANCE | 事件重要性等级 | 基于影响力、关注度 **自动** 计算高/中/低，供筛选排序并随动态更新 | 分级规则未签。点名计算 → 差集 missing，不是 CMS 手工打标 | MODEL |

禁止 mapped 产业/企业/技术/机构发展路径里的「重大事件」时间轴（05 seq 119/142/132/150）。禁止 `M_CHAIN_NEWS_COUNT` 顶替关注度。

### §3.11 ④ 不适用（N/A + 依据）

整包 N/A：**无**（FACTORS / EVENTS 有统计核）。**LAYERS / MAP 整页 N/A。**

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| `DS-01-MAP` 整页 | 放大/缩小、拖动平移、复位 | `n/a_ops` | SRS seq 1–3：GIS 相机/控件。05 无地图维。不发明 `M_MAP_*`。分布数据归 FACTORS。 |
| `DS-01-MAP` | 搜索要素定位 | `other_system` | SRS seq 4：检索门面 + GIS 飞点。禁止 mapped seq 116 实体检索；禁止因「智能匹配」missing。 |
| `DS-01-LAYERS` 整页 | 多对象图层、分组组织 | `n/a_ops` | SRS seq 5/7：图层开关/目录/颜色。不进算法库。不发明 `M_LAYER_*`。 |
| `DS-01-LAYERS` | 实时数据监控 | `other_system` | SRS seq 6：GIS 图层读 ADS 坐标。密度/关联差集权在 FACTORS，本页不抢、不 missing。 |
| `DS-01-LAYERS` | 数据源灵活配置 | `other_system` | SRS seq 8：API/库表/填报绑定。禁止当 ODS 缺口写成 missing。 |
| FACTORS | 基础信息查看（FACT-D01） | `other_system` | seq 9 浏览/详情/筛选/收藏。展示前端 + ADS/ES，筛选壳无独立核。 |
| FACTORS | 要素比较分析（FACT-D17） | `other_system` | 用户多选横向对比，拼装已有指标。禁用 seq 188/190 区域要素排名冒充。 |
| FACTORS | 要素地图可视化（FACT-D20） | `other_system` | seq 13 GIS 分布/热力/图列联动。取数复用 COUNT/DIST；缩放图层归 MAP/LAYERS。 |
| FACTORS | 统计图表与导出（FACT-D21） | `n/a_ops` | 柱饼折线/导出/收藏。展示壳。 |
| EVENTS | 时间筛选与事件列表（EVT-D04） | `other_system` | seq 14 CMS/资讯库时间戳过滤。 |
| EVENTS | 时段分布对比（EVT-D05） | `other_system` | 同一事件库区间计数，未点名 05 模型。 |
| EVENTS | 事件详情字段（EVT-D06） | `other_system` | seq 16 标题/时间/地点/描述/主体；地图弹出是 GIS 宿主。 |
| EVENTS | 事件关联展示（EVT-D07） | `other_system` | 展示关联，未点名构图。禁 mapped seq 116；禁因无「事件关联」叶而 missing。 |
| EVENTS | 导出与分享（EVT-D08） | `n/a_ops` | 运营/前端。 |
| 本叶范围外 | 专题 SYNTH-ELEMENT 七要素指数 | — | 禁止消费 `M_SYNTH_ELEM_*`；不重列其 missing。 |
| 本叶范围外 | 展示企业包 / 专题企业 | — | 禁止 `M_ENT_*` 与 `TOPIC-ENT` / `ENT-MOD-*` OPEN。 |
| 本叶范围外 | DS-02…09 及其他展示 OPEN | — | 本叶只覆盖 DS-01 四页。 |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢 · 不新建 Q0xx）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| SD-FACT-01 | 会议/期刊/项目/成果无基础指标叶；计数走 ADS | 语义债；不把 COUNT 改 missing |
| SD-FACT-02 | 学术力维名 ≠ 半成品 H 指数 | 语义债；FACT-D07 保持 mapped |
| SD-FACT-03 | 国际合作论文比例无专核 | 语义债；PAPER 保持 mapped |
| SD-FACT-04 | 本叶闭合文件级：核对记录 present；正式 `M_*` 仍不发明 | 有统计无正式 ID = B 类，不是缺 OPEN |
| SD-FACT-05 | 组织机构拆科研/企业/服务；课题并入项目 | 待甲方确认；不改差集 |
| EVT-B01 | 事件关注度无正式 ID、口径需确认 | 语义债；库缺口仍 EVT-D01 missing |
| EVT-B02 | 事件影响力无正式 ID | 语义债 |
| EVT-B03 | 重要性等级无正式 ID | 语义债 |
| 专题 7 missing | **不重列、无 also_in** | 真源仍专题 A2 summary |
| Q0xx | **N/A**：本叶不新建客户决策号、不改跟踪表 | — |

未关闭任何甲方项。门 1 有条件闭合：OPEN 文件级 present ≠ 口径 FULL。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/display/v1/**` 薄 BFF → 只读 ADS；GIS = 配置 + ADS 坐标。可选 `graph/view` 嵌图可空。Java 不写 NLP / 不直连 nGQL。 |
| 读面（详设 04） | G1；A 嵌图 + GIS + ADS；嵌图可薄。GIS 与图坐标两套，不以切面冻坐标驱动态势地图。图失败不挡 KPI。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。人才/科研机构/技术链基础指标：差集 mapped、公式「第三方不展开」（郭万迎对九新；李伟辅助抽清单）。 |
| 算法库 05 | 能对上的基础指标/学术力/技术力/图谱 API/服务机构技术力 → mapped。会议/项目/专利被引·SEP/期刊/聚类/要素预测/监测异常/事件三核 → **保持 missing**。 |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不把 B 轨 `M_SVC_GRAPH_*` / 63 个 `M_CHAIN_*` 打 missing；不新建 `data-gap-catalog`（文案真源仍 A2 `semantic_debt` + 本 §4）。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_**；服务机构影响力可回指已有 `M_SVC_ORG_TECH_SCORE`，**禁止**点开展示 `M_ENT_*` / 七要素 `M_SYNTH_ELEM_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/课题并入口径未冻：⚠️「待甲方确认」（SD-FACT-05）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 图层开关 / 地图缩放平移复位：**无 ⓘ 数字义务**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 页面要哪些指标 Owner = `human:李伟`（展示系统）；依赖九新的人才/机构/技术 → `human:郭万迎`。STAT → GDF ADS + Java 聚合；MODEL/GRAPH 计算仍归唐绍祖监管 Python

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-01-科技全域态势-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-01-METRIC-OPEN-L01.yaml` |
| A2 指针补丁（本叶） | `metrics/request/_work/open-loop/DS-01-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-01-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/DS-01-METRIC-OPEN-L01-questions.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-01-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文；`pages/DS-01-*.yaml`；`LOOP-state.yaml`；共享 `METRIC-OPEN-LOOP-a2-patch.yaml`；`METRIC-SEMANTIC-QUESTIONS.md`；其它 DS OPEN |

---

## §赋号表（ID-ASSIGN 草稿 · 类型未签 · 2026-08-22）

> ELEMENT 默认 `INNOV`（监测）。不用 `IC`，避免与 SYNTH 七要素创新生态混淆。  
> 20/20 `TEMP_DS01_*` 已升正式草稿 ID（或 reuse）。`algorithm_type` = `suggested_unsigned`。未写 seed。LAYERS/MAP 无行。

| temp_id | metric_id | reuse | 建议类型 | Q |
|---------|-----------|-------|----------|---|
| TEMP_DS01_FACT_COUNT | M_INNOV_FACTOR_COUNT | — | STAT | Q-MO-DS01-01 |
| TEMP_DS01_FACT_DIST | M_INNOV_FACTOR_DIST | — | STAT | — |
| TEMP_DS01_FACT_GROWTH | M_INNOV_FACTOR_GROWTH | — | STAT | — |
| TEMP_DS01_FACT_INFLUENCE_DEGREE | M_INNOV_FACTOR_EDGE_WEIGHT | — | GRAPH | — |
| TEMP_DS01_FACT_ASSOC | M_INNOV_FACTOR_RELATION | — | GRAPH | — |
| TEMP_DS01_FACT_SCHOLAR | M_INNOV_SCHOLAR_INFLUENCE | — | MODEL | Q-MO-DS01-02 |
| TEMP_DS01_FACT_CONF | M_INNOV_CONFERENCE_INFLUENCE | — | MODEL | — |
| TEMP_DS01_FACT_ORG | M_INNOV_ORG_INFLUENCE | — | MODEL | — |
| TEMP_DS01_FACT_ENT | M_INNOV_ENTERPRISE_INFLUENCE | — | MODEL | — |
| TEMP_DS01_FACT_SVC | M_SVC_ORG_TECH_SCORE | **reuse** B 轨（seed miss） | MODEL | Q-MO-DS01-04 |
| TEMP_DS01_FACT_PROJECT | M_INNOV_PROJECT_INFLUENCE | — | MODEL | Q-MO-DS01-03 |
| TEMP_DS01_FACT_PAPER | M_INNOV_PAPER_INFLUENCE | — | STAT | — |
| TEMP_DS01_FACT_PATENT | M_INNOV_PATENT_INFLUENCE | — | MODEL | Q-MO-DS01-05 |
| TEMP_DS01_FACT_JOURNAL | M_INNOV_JOURNAL_INFLUENCE | — | MODEL | — |
| TEMP_DS01_FACT_CLUSTER | M_INNOV_FACTOR_CLUSTER | — | MODEL | — |
| TEMP_DS01_FACT_FORECAST | M_INNOV_FACTOR_FORECAST | — | MODEL | — |
| TEMP_DS01_FACT_ANOMALY | M_INNOV_FACTOR_ANOMALY | — | MODEL | — |
| TEMP_DS01_EVT_ATTENTION | M_INNOV_EVENT_ATTENTION | — | MODEL | Q-MO-DS01-06 |
| TEMP_DS01_EVT_INFLUENCE | M_INNOV_EVENT_INFLUENCE | — | MODEL | Q-MO-DS01-07 |
| TEMP_DS01_EVT_IMPORTANCE | M_INNOV_EVENT_IMPORTANCE | — | MODEL | Q-MO-DS01-08 |

**计数**：赋号 20 · reuse 1 · 新编 19 · Q 8 · STAT 4 / GRAPH 2 / MODEL 14。  
**禁止改挂**：`M_ENT_*` / `M_SYNTH_ELEM_*` / `M_CHAIN_ACADEMIC_POWER` / `M_CHAIN_PATENT_COUNT` / `M_SVC_GRAPH_*`。科研机构影响力 **不** reuse `M_SVC_ORG_TECH_SCORE`。

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _赋号草稿已出：20 条（reuse 1）；类型未签；TEMP 非终态；未写 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方 SD-FACT-05 / 事件口径 | — | 保持待确认；不新建 Q0xx、不升 🟢 | |
