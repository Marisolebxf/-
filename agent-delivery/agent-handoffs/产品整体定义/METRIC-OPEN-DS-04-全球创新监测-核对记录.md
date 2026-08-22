# METRIC-OPEN-DS-04-全球创新监测-核对记录

> **任务**：DS-04-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 11）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 全球创新监测 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-04` **全部 6 个** `page_id` 的 ④ 指标语义卡 + ⑤ 开放项。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **预测模型**：可标 **501 / pending**；**禁止**因此把差集改成 mapped（不伪闭合）。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 6 页中 **5 页 kit**、**1 页整页 N/A + 依据**（`DS-04-ACHIEVE-DETAIL`）。SRS 02 / 详设 04 / A2 页 yaml **未挂**任何正式 `metric_id` → 卡面只用 **`TEMP_DS04_*`**。**禁止**发明正式 `M_*` 写入 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 沿用 A2 已写语义债 `AOV-B01` / `MON-B01..B02` / `RT-B01..B02` / `CITY-B01..B03` / `CRK-B01..B02`。**不新建** `Q0xx`（避免与展示企业 Q010～Q019、政策 QPOL、指数 Q-TINDEX-01 撞号）。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 `data-gap-catalog`（文案真源 = 本 §4 + A2 `semantic_debt`）。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/DS-04-*.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | STAT / V1 看板可写演示公式；MODEL（价值 / 发现 / 赋分 / 预测 / 载体指数）公式 `pending_cosign`。CITY 三维 vs 186 四维显式挂 CITY-B03。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：DS-04 **非整包 N/A**。成果详情页整页 N/A；其余五页有统计 / 指数 / 模型 → **出卡**。甲方 🟡 / 公式未签 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。**501 不是覆盖证明。**

### §1.1 本叶必须消费本核对记录（catalog 6 页）

| 页 `page_id` | 中文（需规五级） | ④ | 消费的 ID | 禁止 |
|--------------|------------------|----|-----------|------|
| `DS-04-ACHIEVE-OVERVIEW` | 创新成果综合展示 | **kit** | `TEMP_DS04_ACHIEVE_VALUE` | 挂 seq 182 区域成果指数；消费 `M_CHAIN_*` / `M_SVC_GRAPH_*`；把预测算进本页 |
| `DS-04-ACHIEVE-DETAIL` | 具体创新成果展示 | **N/A + 依据** | 无 TEMP_ | 发明 `M_ACHIEVE_*`；把 OVERVIEW 价值模型 / MONITOR 评估 missing 算进本页 |
| `DS-04-MONITOR` | 创新监测与分析 | **kit** | `TEMP_DS04_MONITOR_DISCOVERY` · `TEMP_DS04_MONITOR_VALUE` | 改挂 seq 134/135/182；`M_SVC_REC_*` 顶替推送；把 501 当发现/评估已覆盖 |
| `DS-04-REALTIME` | 全球创新实时数据 | **kit** | `TEMP_DS04_RT_KPI_BOARD` · `TEMP_DS04_RT_IMPACT_SCORE` · `TEMP_DS04_RT_IMPACT_FORECAST` | 把预测 501 改 mapped；`M_SVC_GRAPH_*` 顶替赋分；also_in `M_SYNTH_ELEM_CONTRIB` / DS-02-PATH |
| `DS-04-CITY` | 城市创新能力分析 | **kit** | `TEMP_DS04_CITY_MONITOR` · `TEMP_DS04_CITY_RANK` · `TEMP_DS04_CITY_BENCHMARK` · `TEMP_DS04_CITY_FACTOR` · `TEMP_DS04_CITY_TALENT_INDEX` | 改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*` / `M_CHAIN_REGION_*`；湾区 DS-05 / 深圳 DS-06 |
| `DS-04-CARRIER-RANK` | 创新载体排行榜 | **kit** | `TEMP_DS04_CARRIER_INDEX` · `TEMP_DS04_CARRIER_RANK` | 改挂 `M_SVC_ORG_TECH_SCORE` / 企业技术力 / CITY 城市排名；深圳 `DS-06-CARRIER`；DS-08 指数顶替 |

**本叶不消费**：专题 TOPIC-ENT / SYNTH / CHAIN / SVC / POLICY OPEN；展示 ENT-MOD-*；DS-05/06/08/25～29。B 轨已有 ID **不得 missing、不得改挂**为本页正式 ID。

### §1.2 需规 33 叶 × 差集（对照 A2；本叶不改判定）

| 五级 | seq | 招标叶子 | A2 差集（保持） | ④ |
|------|-----|----------|-----------------|----|
| 综合展示 | 56 | 分类展示 | other_system | 无独立核（价值分档消费 TEMP_VALUE） |
| 综合展示 | 57 | 地理位置可视化 | other_system | 无独立核 |
| 综合展示 | 58 | 重点成果突出 | n/a_ops | 无独立核（阈值消费 TEMP_VALUE） |
| 综合展示 | 59 | 创新价值排序 | **missing** | **kit** |
| 综合展示 | 60 | 实时更新展示 | other_system | 无独立核 |
| 具体成果 | 61–66 | 标注 / 圈选 / 详情 / 载体 / 订阅 / 对比 | other_system ×4 + n/a_ops ×2 | **整页 N/A** |
| 实时数据 | 67–68 / 72 | 指标分类 / 图表 / 看板刷新 | other_system | kit（V1 看板 TEMP_KPI_BOARD） |
| 实时数据 | 69 | 知识图谱创新点落图 | **mapped** seq 116 | 无独立核 |
| 实时数据 | 70 | 实体节点影响赋分 | **missing** | **kit** |
| 实时数据 | 71 | 创新影响预测 | **missing**（501 pending） | **kit**；不伪闭合 |
| 载体排行 | 73–74 | 指数计算 / 多维排名 | **missing** ×2 | **kit** |
| 载体排行 | 75–76 | 筛选 / 详情 | n/a_ops / other_system | 无独立核 |
| 监测分析 | 77 / 80–82 | 模型设置 / 订阅 / 关注点 / 推送 | n/a_ops ×4 | 无独立核 |
| 监测分析 | 78–79 | 创新点发现 / 创新价值评估 | **missing** ×2 | **kit** |
| 城市 | 83 / 87–88 | 监控 / 订阅 / 政策建议 | other_system / n/a_ops / other_system | 监控有看板数 → kit TEMP_MONITOR；订阅/建议无独立核 |
| 城市 | 84–86 | 排名 / 对标 / 要素 | **mapped** 186 / 186 / 187 | **kit**（TEMP_，不改挂 SYNTH ID） |
| 城市（半成品） | — | 人才创新指数 xlsx 行34 | other_system（智库） | kit TEMP_TALENT_INDEX（不 mapped 184） |

**12/12 库缺口 missing 行保持 missing。** 不得因本 OPEN `present` 改 mapped。CITY 排名/对标/要素已 mapped，本叶只补语义卡，不改差集。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/DS-04-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-04 六页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-04-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-04-METRIC-OPEN-L01`。**库缺口 `missing` 不动**。`DS-04-ACHIEVE-DETAIL` 的 `n/a_documented` 升为 present + 本文件 N/A 依据。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `ds_id=DS-04` 六页 | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句 |
| TRACE / WF | **无**展示四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-04-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。页面要哪些指标主责（展示）= `human:李伟`（给人说明），**不定**本叶清单、不改挂。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止正式 M_*）

> `TEMP_*` ≠ 正式 `M_*`：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。  
> `algorithm_type` 列为 **草稿建议**，未会签。差集列维持 A2 已写判定。

| temp_id | 主落点 | 适用 | 建议 type（未签） | 差集保持 | pending |
|---------|--------|------|-------------------|----------|---------|
| TEMP_DS04_ACHIEVE_VALUE | OVERVIEW seq 59（seq 56/58 消费同一分值） | ✅ kit | MODEL | missing | AOV-B01；禁 seq 182 |
| TEMP_DS04_MONITOR_DISCOVERY | MONITOR seq 78 | ✅ kit | MODEL | missing | MON-B01；禁 seq 134 |
| TEMP_DS04_MONITOR_VALUE | MONITOR seq 79 | ✅ kit | MODEL | missing | MON-B02；≠ OVERVIEW 成果价值 |
| TEMP_DS04_RT_KPI_BOARD | REALTIME seq 67–68 | ✅ kit | STAT | other_system | V1 读 ADS ≠ mapped 05；禁 `M_CHAIN_PATENT_COUNT` |
| TEMP_DS04_RT_IMPACT_SCORE | REALTIME seq 70 | ✅ kit | MODEL | missing | RT-B01；禁 `M_SVC_GRAPH_*` / DS-02-PATH |
| TEMP_DS04_RT_IMPACT_FORECAST | REALTIME seq 71 | ✅ kit | MODEL | **missing** | **501 pending**；RT-B02；**不改 mapped** |
| TEMP_DS04_CITY_MONITOR | CITY seq 83 | ✅ kit | STAT | other_system | 看板读面；禁 mapped 186「实时监控」 |
| TEMP_DS04_CITY_RANK | CITY seq 84 + xlsx 行38 | ✅ kit | MIXED | mapped 186 | CITY-B02；禁 `M_SYNTH_VIT_*` |
| TEMP_DS04_CITY_BENCHMARK | CITY seq 85 | ✅ kit | MIXED | mapped 186 | CITY-B03 三维≠四维 |
| TEMP_DS04_CITY_FACTOR | CITY seq 86 | ✅ kit | MIXED | mapped 187 | 禁 `M_SYNTH_ELEM_*` / CONTRIB |
| TEMP_DS04_CITY_TALENT_INDEX | CITY xlsx 行34 | ✅ kit | STAT | other_system | 智库封装；禁 mapped 184 |
| TEMP_DS04_CARRIER_INDEX | CARRIER seq 73 | ✅ kit | MODEL | missing | CRK-B01；禁 `M_SVC_ORG_TECH_SCORE` / DS-08 |
| TEMP_DS04_CARRIER_RANK | CARRIER seq 74 | ✅ kit | MIXED | missing | CRK-B02；禁 CITY seq 84 |

**13/13 TEMP_ 均 present。** 不得因「口径未冻 / D1 missing / 无正式 M_* / 可 501」把上表改成差集 `mapped` 或把 missing 改成 mapped。

---

## §赋号表（TEMP → M_* · 2026-08-22 · 类型未签）

> 协议：`METRIC-ID-ASSIGN-LOOP-循环工程.md`。ELEMENT=`INNOV`。真源机器卡 `TEMP_DS04_*` → 正式 ID。  
> **reuse=0**：CITY/载体与 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*` / DS-06 不同口径，禁止改挂。  
> **ACHIEVE-DETAIL 整页 N/A，不造 ID。** `M_INNOV_IMPACT_FORECAST` 建议 MODEL **不是** 501 覆盖证明；差集 missing。  
> 身份草稿只在本表 + `id-assign/`；**不写 seed / 展示 catalog / 共享 QUESTIONS。**

| temp_id | metric_id | reuse_of | 建议 type | pending_ref |
|---------|-----------|----------|-----------|-------------|
| TEMP_DS04_ACHIEVE_VALUE | M_INNOV_ACHIEVE_VALUE | — | MODEL | — |
| TEMP_DS04_MONITOR_DISCOVERY | M_INNOV_POINT_DISCOVERY | — | MODEL | — |
| TEMP_DS04_MONITOR_VALUE | M_INNOV_POINT_VALUE | — | MODEL | — |
| TEMP_DS04_RT_KPI_BOARD | M_INNOV_KPI_BOARD | — | STAT | — |
| TEMP_DS04_RT_IMPACT_SCORE | M_INNOV_IMPACT_SCORE | — | MODEL | — |
| TEMP_DS04_RT_IMPACT_FORECAST | M_INNOV_IMPACT_FORECAST | — | MODEL | —（501 pending，非覆盖证明） |
| TEMP_DS04_CITY_MONITOR | M_INNOV_CITY_MONITOR_GLOBAL | — | STAT | — |
| TEMP_DS04_CITY_RANK | M_INNOV_CITY_RANK_GLOBAL | 不复用 `M_SYNTH_VIT_RANK` / DS-06 | MIXED | Q-MO-DS04-04 |
| TEMP_DS04_CITY_BENCHMARK | M_INNOV_CITY_BENCHMARK_GLOBAL | 不复用 `M_SYNTH_VIT_*` | MIXED | Q-MO-DS04-01 |
| TEMP_DS04_CITY_FACTOR | M_INNOV_CITY_FACTOR_GLOBAL | 不复用 `M_SYNTH_ELEM_*` | MIXED | Q-MO-DS04-02 |
| TEMP_DS04_CITY_TALENT_INDEX | M_INNOV_CITY_TALENT_INDEX_GLOBAL | 不复用 DS-06 / seq 184 | third_party | Q-MO-DS04-05 |
| TEMP_DS04_CARRIER_INDEX | M_INNOV_CARRIER_INDEX_GLOBAL | 不复用 DS-06 / `M_SVC_*` | MODEL | — |
| TEMP_DS04_CARRIER_RANK | M_INNOV_CARRIER_RANK_GLOBAL | 不复用 CITY / DS-06 | MIXED | Q-MO-DS04-03 |
| （DETAIL 整页） | — | N/A 不造 ID | — | — |

**计数**：赋号 13 / reuse 0 / 新建 13 / Q 5 / DETAIL 不造 ID。类型分布：STAT 2 · MODEL 6 · MIXED 4 · third_party 1（无 UNKNOWN）。叶级卡：`metrics/request/_work/id-assign/DS-04-METRIC-OPEN-L01.yaml`；Q：`…/DS-04-METRIC-OPEN-L01-questions.yaml`。

撞号（`metric-registry-lib`，MCP 本会话未挂载，未整文件读 seed）：库内无 `M_INNOV_*`；`M_SYNTH_VIT_RANK`=区域创新活力四维排名；`M_ENT_CITY_RANK`=企业多城市对标（禁消费）。

---

## §3 ④ 指标语义卡（按 page_id · 不写 seed）

身份项由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「ADS/ES innov · `gkxlumen-innov` / `/innov/v1/**`」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：正式 `metric_id` 见 **§赋号表**（下表仍列 `temp_id` 对照）；源系统=科技信息展示系统·全球创新监测 / innov；更新频率=未定；version=`draft-open-ds04`；源表=ADS/ES innov（A1 表2 未交 → 本叶不填伪 full）。`algorithm_type` 为建议、未签。

### §3.1 `DS-04-ACHIEVE-OVERVIEW` · kit（seq 56–60）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS04_ACHIEVE_VALUE | 创新价值 | 全球创新成果（专利/论文/资讯/机构/企业动态等清单对象）的技术价值、应用价值与潜在影响力分值；供列表按价值排序、分档与重点突出阈值。对象=**成果条目**，不是区域。 | 演示未签；半成品「创新价值分值」。禁止用区域成果综合评价（05 seq 182）公式顶替 | MODEL |

路由 `/innov`（已有 M1）。V1 指标读 ADS **不等于** mapped 05。预测模型 **不进本页**（归 REALTIME seq 71）。

#### 本页 ④ 不适用（N/A + 依据）

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 分类与检索（seq 56） | other_system | innov/ADS/ES 类型字段 + 检索门面；不是 05 分类模型。价值分档消费 TEMP_VALUE |
| 地理位置可视化（seq 57） | other_system | GIS + innov 坐标；圈选详情归 DETAIL |
| 重点成果突出（seq 58） | n/a_ops | 高亮/闪烁/飞线 + 用户阈值；不是重要性识别模型 |
| 实时更新展示（seq 60） | other_system | 按发布时间刷新列表；不是看板刷新、不是预测 |

### §3.2 `DS-04-ACHIEVE-DETAIL` · **整页 N/A**（seq 61–66）

A2 已记 `metric_open_status: n/a_documented`（本叶升 present，④ 仍 N/A）。六叶均为 innov/GIS 读面或订阅/并排壳，**无独立统计核 / 无模型产出义务**。

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 地理标注 / 范围筛选（seq 61–62） | other_system | GIS 落点与空间过滤；05 无地图维 ≠ missing |
| 成果详情（seq 63） | other_system | 只读已落库字段（含创新价值字段）；计算归 OVERVIEW / 评估归 MONITOR |
| 关联载体（seq 64） | other_system | ADS 关联下钻；不抢 CARRIER-RANK；禁 mapped seq 116 |
| 从详情订阅（seq 65） | n/a_ops | 本页只消费单条订阅开关；条件订阅/推送归 MONITOR |
| 创新成果对比（seq 66） | n/a_ops | 并排已有字段，不是相似度/案例匹配；禁 also_in CHAIN-TOPIC-SHENZHEN |

禁止发明 `M_ACHIEVE_*` / `M_INNOV_DETAIL_*`。禁止把半成品行 35–40 算进本页 missing。

### §3.3 `DS-04-MONITOR` · kit（seq 77–82）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS04_MONITOR_DISCOVERY | 创新点发现 | 用算法模型从全球创新监测对象中自动识别「创新点」，产出识别列表与详情。对象≠技术链热点领域（seq 134）、≠区域综合评价（182–191） | 模型未签；05 无专叶 | MODEL |
| TEMP_DS04_MONITOR_VALUE | 创新点价值评估 | 对**已发现的创新点**做价值评估，产出评估分值与价值分析报告。对象≠ OVERVIEW 成果清单创新价值（行35） | 演示未签；半成品行40「创新价值评估分值」；05 无专叶 | MODEL |

**不得**把详设「预测模型可 501」改挂为本页发现/评估已覆盖。`/innov` M1 as-built 是成果地图/事件读面，**不是**发现-评估管线。

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 监测模型设置（seq 77） | n/a_ops | 指标/阈值/频率配置表单 + 规则调度 |
| 订阅管理（seq 80） | n/a_ops | 领域/载体订阅配置；≠ seq 65 |
| 创新关注点设置（seq 81） | n/a_ops | 关键词/领域/类型表单 |
| 智能推送（seq 82） | n/a_ops | 通知/邮件通道；未点名推荐算法；禁 `M_SVC_REC_*` |

### §3.4 `DS-04-REALTIME` · kit（seq 67–72）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS04_RT_KPI_BOARD | 全球创新实时看板指标 | 按专利数量、论文引用率、投资金额等类别切换查看的全球创新看板计数/比率；图表（柱/折/饼/热力）为同一套数的读面 | 演示：innov/ADS V1 字段聚合；**不是** 05 seq 96 论文/专利公式 | STAT |
| TEMP_DS04_RT_IMPACT_SCORE | 创新影响分数 | 对领域知识图谱**实体节点**做创新影响赋分，展示分数与排名。不是网络密度/中心度（seq 116（5）），不是服务链图指标 | 模型未签；半成品行36 | MODEL |
| TEMP_DS04_RT_IMPACT_FORECAST | 创新影响预测 | 基于图谱与影响分数，预测科技创新对领域创新的积极影响及贡献度（含趋势）。招标父句「趋势预测和判断」落本叶 | 模型未签；半成品行39。**实现通道可 501 / pending**。05 无专叶 → **差集保持 missing**，**禁止**因 501 改 mapped | MODEL |

知识图谱创新点落图（seq 69）= mapped seq 116 可视化 + 关系查询；**④ 无独立统计核**（不另造 TEMP_）。不是 GIS 地理落点。

#### 本页 ④ 不适用 / 无独立核

| 项 | 差集 | 依据 |
|----|------|------|
| 图表切换（seq 68） | other_system | 与 KPI_BOARD 同一读面；热力≠话题热力 seq 134、≠ GIS |
| 知识图谱落图（seq 69） | mapped | 无独立 metric_id；116（5）不覆盖赋分 |
| 实时数据更新（seq 72） | other_system | 看板刷新；≠ OVERVIEW seq 60 最新成果列表 |

**501 纪律**：只给 seq 71 一条实现通道注释。未注册本页正式 ID。不把 DS-07 趋势预测行、seq 182–191、`M_SYNTH_ELEM_CONTRIB` 当已覆盖。

### §3.5 `DS-04-CITY` · kit（seq 83–88）

catalog `algo_srs` = 专题算法库/综合。本页是**全球城市读面**，不跑专题 SYNTH Job，**禁止**改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*` 为本页正式 ID。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS04_CITY_MONITOR | 城市创新数据监控 | 全球主要城市的创新基金/投资规模、机构与企业投入、创新成果等看板详情 | innov/ADS 字段展示；不是 186「实时监控」 | STAT |
| TEMP_DS04_CITY_RANK | 城市创新能力排名 | 基于数据模型计算各大城市创新能力排名（名次 + 可查看计算方法）。对照 05 seq 186 活力指数排序；与专题 SYNTH-VITALITY **同叶不同页** | 演示：186 指数排序；权重未签 | MIXED |
| TEMP_DS04_CITY_BENCHMARK | 城市对标分析 | 多城对比：招标三维=投入/产出/环境；186 四维=科技/产业/人才/政策 → CITY-B03，不另开 A | 随 186 横向对比 + 单维评分 | MIXED |
| TEMP_DS04_CITY_FACTOR | 城市创新能力要素表现 | 各城在人才/资金/政策等要素上的量化表现。对照 seq 187 类型综合评价；例示三要素 ⊂ 七要素 | 随 187 要素维评分；不伪展开 | MIXED |
| TEMP_DS04_CITY_TALENT_INDEX | 人才创新指数 | 综合反映人才在创新活动中的贡献度、影响力与活跃度。调用系统=新型高端智库 / 科技人才智慧服务 | 智库封装读数；禁止挂 seq 184 | STAT |

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 城市订阅（seq 87） | n/a_ops | 订阅 + 推送通道；禁 `M_SVC_REC_*` |
| 创新政策建议（seq 88） | other_system | 报告/文案读面，未点名生成模型；禁硬挂 seq 185 |

禁止湾区 DS-05、深圳 DS-06-CITY 混挂。xlsx 行37 载体指数 **不进本页**。

### §3.6 `DS-04-CARRIER-RANK` · kit（seq 73–76）

对象=**创新载体（企业/机构）**，不是城市、不是区域。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS04_CARRIER_INDEX | 创新载体创新能力指数 | 按各载体创新成果数据计算的综合指数（资源/产出/能力），可查看方法与权重 | 模型未签；半成品行37。05 无载体指数专叶。上层封装「科技指数计算」≠ mapped 05、≠ DS-08 | MODEL |
| TEMP_DS04_CARRIER_RANK | 创新载体多维度排名 | 总体 / 领域 / 地区三维度排名；名次依赖同一指数 | 未签；05 无载体排行专叶。禁止用 CITY seq 84 城市排名顶替 | MIXED |

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 排名筛选（seq 75） | n/a_ops | 领域/地区/时间过滤壳 |
| 载体详情（seq 76） | other_system | innov/ADS 详情；指数趋势消费 TEMP_INDEX，不另开 missing；不抢 DETAIL seq 64 |

禁止 `M_SVC_ORG_TECH_SCORE`、企业 seq 141/145、机构 seq 99/149/154/155、综合 182–191、`DS-06-CARRIER`、DS-08 / Q-TINDEX-01 顶替。

---

## §4 ⑤ 开放项（已登记 · 不升 🟢 · 不新建 Q0xx）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| 文件级 OPEN | **本叶闭合**：六页 `metric_open_status: present`（DETAIL 为 present + N/A 依据） | 语义欠账→有指针；非把 missing 改 mapped |
| AOV-B01 | 成果创新价值无正式 ID | 语义债；库缺口 AOV-D01 保持 missing |
| MON-B01 / MON-B02 | 创新点发现 / 创新点价值评估无正式 ID | 语义债；missing 保持 |
| RT-B01 | 创新影响分数无正式 ID | 语义债；missing 保持 |
| RT-B02 | 创新影响预测 / 贡献度；**501 未注册本页 ID** | 语义债；**missing + 501 pending**；不伪闭合 |
| CITY-B01 | 无四件套 / TRACE | 本叶补指针后文件级闭合；不发明 M_* |
| CITY-B02 | 排名/对标/要素无正式 metric_id | 语义债；差集 mapped 186/187 不动 |
| CITY-B03 | 「城市创新能力」vs「区域创新活力」；对标三维 vs 四维 | 语义债；不另开 A、不发明三维 M_* |
| CRK-B01 / CRK-B02 | 载体指数 / 多维排名无正式 ID | 语义债；missing 保持 |
| Q-TINDEX-01 | 智库指数后台（DS-08） | **本页不改挂** |
| Q010～Q019 / QPOL-* | 展示企业 / 政策口径族 | **本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未新建 `data-gap-catalog`（⑤ = 本表 + A2 `semantic_debt`，**N/A 于新 Q0xx**）。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 `/innov` → Java `gkxlumen-innov` `/innov/v1/**` → 只读 ADS/ES innov；可选 `graph/view`（seq 69）。Java 不写 NLP / 不直连 nGQL。CITY 对照 186/187 **不在本页跑专题 Job**。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。V1 看板字段走 innov ADS，不自动等于 05 技术链基础指标。 |
| 预测 / 501 | 仅 REALTIME seq 71 可走 501 实现通道；**未注册 metric_id**；差集 **missing**。MONITOR 发现/评估 **不得**借 501 伪覆盖。 |
| 算法库 05 | 落图 mapped 116；CITY 排名/对标 mapped 186、要素 mapped 187。价值 / 发现 / 评估 / 赋分 / 预测 / 载体指数 **无对口叶** → missing 保持。 |
| 本叶不做 | 不写任何 `cfg_metric-*-seed.yaml`；不发明 `M_INNOV_*` / `M_ACHIEVE_*` / `M_CITY_*` / `M_CARRIER_*` / `M_REALTIME_*` / `M_MONITOR_*`；不改挂 B 轨 / SYNTH / CHAIN / SVC / ENT；不改 A2 catalog 正文。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_**，**禁止**点开 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重/501 未冻：⚠️「待甲方确认」（文案走 AOV/MON/RT/CITY/CRK-B*，不要把 Q-TINDEX-01 写进 `/innov` DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样
- 功能实现 Owner（展示页要哪些指标）= `human:李伟`；STAT → GDF ADS + Java 聚合；MODEL 计算仍归唐绍祖监管 Python

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-04-全球创新监测-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/DS-04-METRIC-OPEN-L01.yaml`（demands 已换 `M_*`，保留 temp_id_map） |
| A2 指针补丁（分叶） | `metrics/request/_work/open-loop/DS-04-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-04-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-04-METRIC-OPEN-L01-questions.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-04-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 18）；共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml` / `METRIC-SEMANTIC-QUESTIONS.md` / 客户决策清单 |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；六页：OVERVIEW/MONITOR/REALTIME/CITY/CARRIER-RANK **kit**；ACHIEVE-DETAIL **N/A**；预测 **501 pending、差集 missing**；**零**正式 `M_*` 入 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 展示页指标清单（李伟） | — | 本叶不定清单、不改挂 | |
| 甲方既有 Q 项 | — | 不改挂、不升 🟢 | |
