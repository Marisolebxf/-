# METRIC-OPEN-DS-07-科技创新评估-核对记录

> **任务**：DS-07-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 14 / 波 B）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 科技创新评估 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-07` **全部 4 个** `page_id` 的 ④ 指标语义卡 + ⑤ 开放项。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **评估四力**：本四级 = 科学创造力 / 技术创新力 / 产业发展潜力 / 政策与条件保障力。**POLICY-GUARD 是四力之一的展示指标页，不是专题 E7 政策工作台，也不是 DS-10/11/12 科技政策跟踪。**

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 4 页 **全部 kit**（无整页 N/A）。页内若干叶 **N/A + 依据**（POLICY 优化建议；TECH 空间热力）。SRS 02 / 详设 04 / A2 页 yaml **未挂**任何正式 `metric_id` → 卡面只用 **`TEMP_DS07_*`**。**禁止**发明正式 `M_*` 写入 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 沿用 A2 已写语义债 `PG-B01..B06` / `POT-B01..B02` / `TINN-B01..B04` / `SCI-B01..B02`。**不新建** `Q0xx`（避免与展示企业 Q010～Q019、政策 QPOL、指数 Q-TINDEX-01 撞号）。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 `data-gap-catalog`（文案真源 = 本 §4 + A2 `semantic_debt`）。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/DS-07-*.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | STAT / V1 看板可写演示公式；MODEL（引导力 / 四力综合 / 质量 / 影响力 / 预测）与 third_party（成熟度 / 市场潜力 / 前沿）公式 `pending_cosign`。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性。DoD 写「淮政瑎」是错字，以本栏为准。 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：DS-07 **非整包 N/A**。四页均有统计 / 评估 / 模型 → **出卡**。甲方 🟡 / 公式未签 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。**501 不是覆盖证明。** 库缺口 **9 行 missing 保持**（POLICY 2 + POTENTIAL 3 + TECH-INNOV 3 + SCI-CREATE 1）。

### §1.1 本叶必须消费本核对记录（catalog 4 页）

| 页 `page_id` | 中文（需规五级） | ④ | 消费的 ID | 禁止 |
|--------------|------------------|----|-----------|------|
| `DS-07-POLICY-GUARD` | 政策与条件保障力指标展示 | **kit** | `TEMP_DS07_PG_GUIDE` · `TEMP_DS07_PG_INTENSITY` · `TEMP_DS07_PG_COUNT_DIST` · `TEMP_DS07_PG_FUND` · `TEMP_DS07_PG_PROJECT` · `TEMP_DS07_PG_EFFECT` · `TEMP_DS07_PG_COMPOSITE` | **消费 `POLICY-METRIC-OPEN-L01` / `METRIC-OPEN-E7-DS10-12` / DS-10～12**；另开 `TOPIC-POLICY-METRIC-OPEN-L01`；改挂 `M_POLICY_*` / seq 185；按号 mapped 科研 152–155 / 人才 156–158 |
| `DS-07-INDUSTRY-POTENTIAL` | 产业发展潜力指标展示 | **kit** | `TEMP_DS07_POT_INPUT` · `TEMP_DS07_POT_MATURITY` · `TEMP_DS07_POT_OUTPUT` · `TEMP_DS07_POT_SCI_INFL` · `TEMP_DS07_POT_TECH_INFL` · `TEMP_DS07_POT_COMPOSITE` | 改挂 `M_SYNTH_*` / seq 183/186；改挂 135 顶综合；`M_CHAIN_*` 成熟度/产值/学术力；DS-01-FACTORS also_in；按号 mapped 企业 146–148 / 科研 149–151 |
| `DS-07-TECH-INNOV` | 技术创新力指标展示 | **kit** | `TEMP_DS07_TINN_PATENT_COUNT` · `TEMP_DS07_TINN_PATENT_QUALITY` · `TEMP_DS07_TINN_MARKET` · `TEMP_DS07_TINN_COMPOSITE` · `TEMP_DS07_TINN_FORECAST` | 改挂 `M_CHAIN_PATENT_COUNT`；按号 mapped 05 seq 140；硬挂 182/186；改挂 SCI seq 139；DS-03 技术跟踪；DS-08 指数 |
| `DS-07-SCI-CREATE` | 科学创造力指标展示 | **kit** | `TEMP_DS07_SCI_PAPER` · `TEMP_DS07_SCI_CENTRALITY` · `TEMP_DS07_SCI_FRONTIER` · `TEMP_DS07_SCI_FORECAST` | 按号 mapped 技术链 136–139；also_in DS-02-PATH / DS-04-REALTIME seq 71；改挂 `M_SVC_GRAPH_*` / `M_CHAIN_REG_PAPERS`；把 134 热点趋势当本页预测 |

**本叶不消费**：`POLICY-METRIC-OPEN-L01`；`METRIC-OPEN-E7-DS10-12-核对记录.md`；展示 DS-10/11/12；专题 TOPIC-POLICY / TOPIC-TECH / TOPIC-ORG / SYNTH OPEN；展示 ENT-MOD-*；DS-03 技术跟踪；DS-08 科技指数。B 轨已有 ID **不得 missing、不得改挂**为本页正式 ID。已 mapped **不得改挂**为本页正式 ID。

### §1.2 需规 23 叶 × 差集（对照 A2；本叶不改判定）

| 五级 | seq | 招标叶子 | A2 差集（保持） | ④ |
|------|-----|----------|-----------------|----|
| 科学创造力 | 136 | 科学论文数量分析 | **mapped** 96 论文项 | **kit** |
| 科学创造力 | 137 | 科学网络中心性评估 | **mapped** 116（5） | **kit** |
| 科学创造力 | 138 | 科学研究前沿性分析 | **third_party** 134 | **kit** |
| 科学创造力 | 139 | 科学创造力趋势预测 | **missing** | **kit**；04 未给本页 501；不伪闭合 |
| 技术创新力 | 140 | 专利数量统计分析 | **mapped** 96（5）（6）（7） | **kit** |
| 技术创新力 | 141 | 专利质量评估 | **missing** | **kit** |
| 技术创新力 | 142 | 技术市场潜力分析 | **third_party** 135 | **kit** |
| 技术创新力 | 143 | 技术创新力综合评估 | **missing** | **kit** |
| 技术创新力 | 144 | 技术创新空间分布 | other_system | **N/A + 依据**（GIS 热力；区域计数宿主 TINN-D01） |
| 技术创新力 | 145 | 技术创新趋势预测 | **missing**（501 通道） | **kit**；**不改 mapped** |
| 产业发展潜力 | 146 | 产业投入分析 | other_system | **kit**（STAT 读面） |
| 产业发展潜力 | 147 | 技术产品成熟度评估 | **third_party** 137 | **kit** |
| 产业发展潜力 | 148 | 产业产值分析 | other_system | **kit**（STAT 读面） |
| 产业发展潜力 | 149 | 科学影响力评估 | **missing** | **kit** |
| 产业发展潜力 | 150 | 技术影响力评估 | **missing** | **kit** |
| 产业发展潜力 | 151 | 产业发展潜力综合评估 | **missing**（对不上 183） | **kit** |
| 政策与条件保障力 | 152 | 发展战略引导力评估 | **missing** | **kit** |
| 政策与条件保障力 | 153 | 政策扶持力度分析 | **mapped** 167 + 100 | **kit** |
| 政策与条件保障力 | 154 | 经费支持分析 | other_system | **kit**（STAT 读面） |
| 政策与条件保障力 | 155 | 项目支持分析 | other_system | **kit**（STAT 读面） |
| 政策与条件保障力 | 156 | 政策实施效果评估 | **mapped** 168 | **kit**（xlsx 行66 同核） |
| 政策与条件保障力 | 157 | 政策与条件保障力综合评估 | **missing** | **kit** |
| 政策与条件保障力 | 158 | 政策优化建议 | other_system | **N/A + 依据**；德尔菲段见 PG-B05，不 missing |

**9/9 库缺口 missing 行保持 missing。** 不得因本 OPEN `present` 改 mapped。已 mapped / third_party 只补 TEMP_ 语义卡，不改差集、不改挂正式 ID。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/DS-07-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml` / `LOOP-state.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-07 四页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-07-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-07-METRIC-OPEN-L01`。**库缺口 `missing` 不动**。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `ds_id=DS-07` 四页 | 现网四页均为 `metric_open_status: missing`；Round 18 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句 |
| TRACE / WF | **无**展示四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-07-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。页面要哪些指标主责（展示）= `human:李伟`（给人说明），**不定**本叶清单、不改挂。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止正式 M_*）

> `TEMP_*` ≠ 正式 `M_*`：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。  
> `algorithm_type` 列为 **草稿建议**，未会签。差集列维持 A2 已写判定。

| temp_id | 主落点 | 适用 | 建议 type（未签） | 差集保持 | pending |
|---------|--------|------|-------------------|----------|---------|
| TEMP_DS07_SCI_PAPER | SCI-CREATE seq 136 | ✅ kit | STAT | mapped 96 | SCI-B02；禁 `M_CHAIN_REG_PAPERS`；只消费论文项 |
| TEMP_DS07_SCI_CENTRALITY | SCI-CREATE seq 137 | ✅ kit | MIXED | mapped 116 | 禁 also_in DS-02-PATH；禁 `M_SVC_GRAPH_*` |
| TEMP_DS07_SCI_FRONTIER | SCI-CREATE seq 138 | ✅ kit | MODEL | third_party 134 | 禁伪公式；134 趋势不改挂 seq 139 |
| TEMP_DS07_SCI_FORECAST | SCI-CREATE seq 139 | ✅ kit | MODEL | **missing** | **无本页 501**；禁 also_in DS-04 seq 71 |
| TEMP_DS07_TINN_PATENT_COUNT | TECH-INNOV seq 140 | ✅ kit | STAT | mapped 96 | TINN-B03 申请≠授权；禁 `M_CHAIN_PATENT_COUNT` |
| TEMP_DS07_TINN_PATENT_QUALITY | TECH-INNOV seq 141 | ✅ kit | MODEL | missing | 禁 96（8）/182/186；≠ POT seq 150 |
| TEMP_DS07_TINN_MARKET | TECH-INNOV seq 142 | ✅ kit | MODEL | third_party 135 | 禁伪展开；禁 seq 137 / POT 成熟度顶替 |
| TEMP_DS07_TINN_COMPOSITE | TECH-INNOV seq 143 | ✅ kit | MODEL | missing | 禁硬挂 182/186/190 |
| TEMP_DS07_TINN_FORECAST | TECH-INNOV seq 145 | ✅ kit | MODEL | **missing** | **501 pending**；禁改挂 SCI seq 139 |
| TEMP_DS07_POT_INPUT | POTENTIAL seq 146 | ✅ kit | STAT | other_system | 禁 187 / `M_CHAIN_REG_FINANCING` |
| TEMP_DS07_POT_MATURITY | POTENTIAL seq 147 | ✅ kit | MODEL | third_party 137 | 禁 B 轨成熟度 ID；不重列 TOPIC-TECH missing |
| TEMP_DS07_POT_OUTPUT | POTENTIAL seq 148 | ✅ kit | STAT | other_system | 禁 `M_CHAIN_REG_REVENUE` |
| TEMP_DS07_POT_SCI_INFL | POTENTIAL seq 149 | ✅ kit | MODEL | missing | 禁 mapped 182；禁 DS-01-FACTORS |
| TEMP_DS07_POT_TECH_INFL | POTENTIAL seq 150 | ✅ kit | MODEL | missing | 禁企业 seq 145；≠ TINN 专利质量 |
| TEMP_DS07_POT_COMPOSITE | POTENTIAL seq 151 | ✅ kit | MODEL | missing | 对不上 183；禁改挂 135/186 |
| TEMP_DS07_PG_GUIDE | POLICY-GUARD seq 152 | ✅ kit | MODEL | missing | 禁 166/167/168/185；**不消费政策 OPEN** |
| TEMP_DS07_PG_INTENSITY | POLICY-GUARD seq 153 广度/深度 | ✅ kit | MIXED | mapped 167 | 禁改挂 `M_POLICY_INTENSITY_*` / SUPPORT_STRENGTH |
| TEMP_DS07_PG_COUNT_DIST | POLICY-GUARD seq 153 件数分布 | ✅ kit | STAT | mapped 100 | 覆盖面≠产业适配；禁 `M_POLICY_INDUSTRY_FIT` |
| TEMP_DS07_PG_FUND | POLICY-GUARD seq 154 | ✅ kit | STAT | other_system | 禁 mapped 167 成本维；禁 `M_CHAIN_REG_FINANCING` |
| TEMP_DS07_PG_PROJECT | POLICY-GUARD seq 155 | ✅ kit | STAT | other_system | 项目「实施效果」字段 ≠ seq 156 |
| TEMP_DS07_PG_EFFECT | POLICY-GUARD seq 156 + xlsx 66 | ✅ kit | MIXED | mapped 168 | 禁改挂 `M_POLICY_IMPLEMENTATION_EFFECT`；无 also_in E7 |
| TEMP_DS07_PG_COMPOSITE | POLICY-GUARD seq 157 | ✅ kit | MODEL | missing | 禁 167/168/185/186；≠ SYNTH 政策成果指数 |

**22/22 TEMP_ 均 present。** 不得因「口径未冻 / D1 missing / 无正式 M_* / 可 501」把上表改成差集 `mapped` 或把 missing 改成 mapped。

---

## §3 ④ 指标语义卡（按 page_id · 不写 seed）

身份项由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「DS-07 = M · ADS 知产规模分布；评估对象范围【算法补】」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技信息展示系统·科技创新评估 / display；更新频率=未定；version=`draft-open-ds07`；源表=ADS（评估对象范围未冻 → 本叶不填伪 full）。调用链：前端 `/display` → Java REST → 只读 ADS；可选 `graph/view`（仅 SCI 中心性对照 116）。Java 不写 NLP / 不直连 nGQL。**本页不跑专题 Job。**

### §3.1 `DS-07-SCI-CREATE` · kit（seq 136–139）

对象=**特定领域科学论文 / 学者与机构合作网 / 研究前沿 / 科学创造力趋势**。知产规模在本页收口为**论文数量**，专利项归 TECH-INNOV。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS07_SCI_PAPER | 科学论文数量 | 特定领域科学论文发表数量；按年/季/月、研究机构、地域看分布与历史变化趋势（柱/折）。对象≠专利计数。本叶「趋势」=已落库计数的历史图表，**不是** seq 139 预测。只消费 05 seq 96 论文项（1）–（4）；专利/交易额/资讯不进 | 演示：96 论文数量/深圳/区域 + 环比；季度/按机构全量 vs 96 月年+阈值 → SCI-B02，不另开 A | STAT |
| TEMP_DS07_SCI_CENTRALITY | 科学网络中心性 | 合作网络中学者、研究机构的度中心性、接近中心性、中介中心性 + 网络图谱与中心性排名。对照 116（5）中心度 +（3）可视化 +（2）人物关系。104/105 无中心性计算 → 不对上 | 演示：116 中心度排序；三类中心性权重未签 | MIXED |
| TEMP_DS07_SCI_FRONTIER | 科学研究前沿性 | 文献计量与引文网络识别领域研究前沿/热点；主题时间演变与空间分布。对照 seq 134 实现类（TOPIC-TECH-05 同叶 third_party）。96（4）前沿论文机构≠本叶主题识别 | 第三方不展开；禁止把 134 散文抄成我方公式 | MODEL |
| TEMP_DS07_SCI_FORECAST | 科学创造力趋势预测 | 基于历史与算法模型预测特定领域科学创造力未来趋势，展示预测结果与置信区间。05 无专叶。详设 04 **未**给本页 501 | 模型未签。**即使日后给 501 也只是实现通道 ≠ 已覆盖**。差集 **missing** | MODEL |

#### 本页 ④ 不适用 / 边界

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 柱折图壳（seq 136 可视化） | 并入 PAPER | 与计数同一读面，不另开 missing |
| 网络图谱读面（seq 137 图） | 并入 CENTRALITY | 116（3）；不是 GIS，不是 DS-21～24 三中心性行 |
| 中心性排名 | 并入 CENTRALITY | 中心度排序，不另 missing |

禁止按号 mapped 技术链 136–139（瓶颈/阶段/问题/机遇）。禁止 also_in DS-02-PATH（路径关键节点≠科学合作网）。禁止 also_in DS-04-REALTIME seq 71。禁止改挂 SCI-CREATE 预测到 TECH-INNOV seq 145。xlsx 157–160 图谱算法展示不进本页。

### §3.2 `DS-07-TECH-INNOV` · kit（seq 140–145）

对象=**特定领域专利 / 技术创新力**（规模、质量、市场潜力、综合、空间、趋势）。不是技术链工作台，不跑 TOPIC-TECH Job。不是 DS-03 技术跟踪。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS07_TINN_PATENT_COUNT | 专利数量 | 特定领域专利申请和授权数量；按时间、技术类别、地域、申请人分布；柱/折看变化。对照 96（5）（6）（7）。**不是**产业链关联专利数 | 演示：96 专利计数 + 环比。招标「申请和授权」vs 96「申请成功」= TINN-B03，不另开 A。禁止 mapped 05 seq 140 深圳重点布局推荐 | STAT |
| TEMP_DS07_TINN_PATENT_QUALITY | 专利质量 | 引文 / 权利要求 / 家族专利分析；被引次数、权利要求数量、家族规模的分布与排名，识别高质量专利。05 无专叶 | 模型未签。禁止 96（8）领先机构 / 182 高价值专利分项 / 186 专利成果质量顶替。≠ POT seq 150 产业技术影响力 | MODEL |
| TEMP_DS07_TINN_MARKET | 技术市场潜力 | 基于专利转让、许可、诉讼等市场活动，看市场活跃度、技术成熟度、商业化前景。对照 seq 135 实现类（专题已 third_party 同叶） | 第三方不展开三维加权。禁止 96 交易额 / seq 137 / POT seq 147 顶替 | MODEL |
| TEMP_DS07_TINN_COMPOSITE | 技术创新力综合评估 | 将本页规模/质量/潜力等按用户自定义权重计算综合得分。05 无「技术创新力综合」专叶 | 权重未签。禁止硬挂 182（会吞 SCI-CREATE）/ 186 / 190。自定义权重是交互壳，不另开 n/a_ops | MODEL |
| TEMP_DS07_TINN_FORECAST | 技术创新趋势预测 | 基于历史与算法模型预测特定领域技术创新力趋势 + 置信区间。详设「趋势预测可 501」= **实现通道**，05 无专叶 | 模型未签。**501 pending，差集保持 missing，禁止改 mapped**。禁止改挂 SCI seq 139 / 134 / 132 / 186 | MODEL |

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 技术创新空间分布（seq 144） | other_system | GIS + ADS 知产落图/热力；区域计数宿主是 TEMP_DS07_TINN_PATENT_COUNT（96（7）），本叶无独立统计核。禁止因 05 无 GIS 专叶而 missing。禁止 mapped 116 |
| 柱折图壳（seq 140） | 并入 PATENT_COUNT | 同一读面 |
| 置信区间读面（seq 145） | 并入 FORECAST | 不另开 missing |

禁止 `M_CHAIN_PATENT_COUNT` 顶替（对象=链关联专利，专题已 missing，不重列）。禁止 DS-08 / Q-TINDEX-01 顶替综合。禁止 INDUSTRY-POTENTIAL 成熟度/技术影响力混挂。

### §3.3 `DS-07-INDUSTRY-POTENTIAL` · kit（seq 146–151）

对象=**特定产业的发展潜力**（投入、成熟度、产值、科学影响力、技术影响力、综合）。不是 TOPIC-TECH 技术点潜力 Job 页，不是 SYNTH 区域活力页。父句「知产规模和地域分布」不单独开本页行。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS07_POT_INPUT | 产业投入 | 产业内企业研发投入、固定资产投资、人才投入；按规模/地域/时间看结构与趋势。ADS 统计读面 | 演示：ADS 金额/强度聚合。禁止 mapped 05 seq 146 企业商业力 / 187 资金要素 | STAT |
| TEMP_DS07_POT_MATURITY | 技术产品成熟度 | 技术生命周期 / 市场渗透率，评估产业内技术或产品成熟度；成熟度曲线。对照 seq 137 实现类（TOPIC-TECH-05 同叶 third_party） | 第三方不展开。禁止 B 轨 `M_CHAIN_*` 成熟度/阶段 ID 顶替。禁止 mapped 05 seq 147 | MODEL |
| TEMP_DS07_POT_OUTPUT | 产业产值 | 总产值、增加值、利润；按时间/地域/企业类型看趋势。ADS 经济统计读面 | 演示：ADS 聚合。禁止 mapped 05 seq 148；禁 `M_CHAIN_REG_REVENUE` / MARKET_SIZE | STAT |
| TEMP_DS07_POT_SCI_INFL | 产业科学影响力 | 基于论文引用、国际合作评估**产业**科学影响力；被引次数、国际合作论文比例的分布与排名。05 无专叶。182「学术影响力」是区域科技成果分项，对象不符 | 模型未签。禁止 also_in DS-01-FACTORS。禁止 `M_CHAIN_ACADEMIC_POWER` / `M_SVC_GRAPH_INFLUENCE` | MODEL |
| TEMP_DS07_POT_TECH_INFL | 产业技术影响力 | 基于专利引用、技术标准评估**产业**技术影响力；专利被引、标准必要专利数量分布与排名。05 无专叶。企业技术力 seq 145 对象=企业 | 模型未签。≠ TINN 专利质量（单件专利质量 vs 产业影响力）。禁 `M_CHAIN_TECH_POWER` / HIGH_VALUE_RATIO | MODEL |
| TEMP_DS07_POT_COMPOSITE | 产业发展潜力综合评估 | 将投入/成熟度/产值/科学影响力/技术影响力按自定义权重计算综合得分与排名。对照 183：成果三维（产品服务/企业/服务机构）≠ 本页潜力五项，对象不对 → **对不上** | 权重未签。禁止伪 mapped 183。禁止改挂 135（技术点潜力，专题已 third_party，不重列）。禁止 mapped 186 | MODEL |

禁止按号 mapped 企业 146–148 / 科研 149–151。seq 135 可与专题同叶但不列为本页综合的覆盖、不 missing 重列。

### §3.4 `DS-07-POLICY-GUARD` · kit（seq 152–158）

对象=**科技创新评估四力之一：政策与条件保障力**（引导力 / 扶持力度 / 经费 / 项目 / 实施效果 / 综合）。**不是**专题 E7 政策分析工作台，**不是**展示 DS-10 政策全景 / DS-11 政策评价 / DS-12 政策推演。

**明确不消费**：`POLICY-METRIC-OPEN-L01`；`METRIC-OPEN-E7-DS10-12-核对记录.md`；E7 TRACE 的 `M_POLICY_INTENSITY_*` / `SUPPORT_STRENGTH` / `IMPLEMENTATION_EFFECT` / `INDUSTRY_FIT` / `LAYOUT_REC_COUNT`（力度/效果可 **同叶对照 167/168**，不改挂 TRACE 8 枚、不复制 E7 行、无 also_in）。禁止另开 `TOPIC-POLICY-METRIC-OPEN-L01`。E7 missing 仅 `M_POLICY_INDUSTRY_FIT`；本页无产业适配性 → 不重列。

知产规模/地域分布 → SCI-CREATE / TECH-INNOV，不进本页。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS07_PG_GUIDE | 发展战略引导力 | 收集领域发展战略规划、产业政策文件，评估战略规划的前瞻性、系统性、针对性；查看关键内容、实施路径、预期目标。政策 9 叶无引导力专叶 | 模型未签；三性口径未冻（PG-B03）。禁止 mapped 166/167/168/185。禁止按号 mapped 科研机构 152 | MODEL |
| TEMP_DS07_PG_INTENSITY | 政策扶持力度 | 评估政策扶持的广度与深度。对照 05 seq 167 力度指数（覆盖≈广度，效果/成本≈深度） | 演示：167 指数；不伪展开。禁止改挂 `M_POLICY_SUPPORT_STRENGTH` / `INTENSITY_*`。xlsx 行85「资金支持强度」归 FUND，不把 153 改打 other_system | MIXED |
| TEMP_DS07_PG_COUNT_DIST | 政策数量类型与覆盖分布 | 政策数量、类型、覆盖面；按财税/人才/金融、时间、地域看分布。对照 seq 100 基础指标。覆盖面≠产业适配 | 演示：100 级别/类型/时序/全国/深圳件数。不改挂 `M_POLICY_TOTAL_COUNT` | STAT |
| TEMP_DS07_PG_FUND | 经费支持 | 科研经费、产业基金、补贴资金；按来源/方向/时间看结构与趋势。原文是计数可视化，未点名评估模型 | ADS 聚合。05 力度成本维≠经费台账。禁止 missing「库无经费叶」。禁止 mapped 167/185 | STAT |
| TEMP_DS07_PG_PROJECT | 项目支持 | 科技项目、产业项目数量与资助金额分布。原文并列的「实施效果」当**项目记录字段**，不是 seq 156 政策效果模型 | ADS 聚合。禁止 mapped 168 / 科研机构 155 | STAT |
| TEMP_DS07_PG_EFFECT | 政策实施效果 | 基于实施后数据变化评估实际效果；实施前后关键指标对比。对照 seq 168。半成品行66「政策效果评估值」同核 | 演示：168 效果指数。不改挂 `M_POLICY_IMPLEMENTATION_EFFECT`。E7 已 mapped 同叶 → 不重列、无 also_in。禁止 mapped 185 | MIXED |
| TEMP_DS07_PG_COMPOSITE | 政策与条件保障力综合评估 | 将引导力、扶持力度、经费、项目、效果按自定义权重计算综合得分与排名。政策 9 叶无保障力综合专叶。185=区域政策创新成果指数（数量/类型/效果），对象不符 | 权重未签（PG-B03）。禁止 mapped 167/168/185/186。禁止用前端加权冲成 n/a_ops | MODEL |

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 政策优化建议（seq 158） | other_system | 建议报告读面，原文未点名必须跑生成模型。禁止 missing「库无建议生成叶」。禁止硬挂 166/169/171。禁止 also_in `M_POLICY_LAYOUT_REC_COUNT` |
| seq 158 文末德尔菲 / 系统仿真 / 学术及科技创新系统评估模型 | 见 PG-B05 | 四级评估总述残留，挂在末叶。不升格为本页 A 类，不派给另外三评估五级，不 missing 仿真模型 |

禁止按号 mapped 科研机构 152–155 / 人才 156–158。点选本页指标禁止跳转 DS-10/11/12。

---

## §4 ⑤ 开放项（已登记 · 不升 🟢 · 不新建 Q0xx）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| 文件级 OPEN | **本叶闭合**：四页 `metric_open_status: present` | 语义欠账→有指针；非把 missing 改 mapped |
| PG-B01 | 本页无 TRACE ID / 无四件套 | 本叶补指针后文件级闭合；不发明 `M_POLICY_GUIDE_*` / `M_POLICY_GUARD_*` |
| PG-B02 | 评估对象范围未冻（详设【算法补】） | 语义债；不另开 A |
| PG-B03 | 引导力三性口径与综合权重未确认 | 语义债；库缺口仍 PG-D01 / PG-D07 missing |
| PG-B04 | 半成品力度行混入资金支持强度 | 力度走 167；资金走 FUND |
| PG-B05 | seq 158 德尔菲与系统仿真不进 A 类 | 建议叶保持 other_system |
| PG-B06 | 项目「实施效果」字段 ≠ 政策效果模型 | D05 other_system vs D06 mapped 168 |
| POT-B01 / POT-B02 | 无四件套；六叶无正式 metric_id | 本叶补 TEMP_；不改挂 B 轨 |
| TINN-B01 / TINN-B02 | 无四件套；无正式 metric_id | 同上 |
| TINN-B03 | 「申请和授权」vs 96「申请成功」 | 已 mapped，不另开 A |
| TINN-B04 | 潜力不伪展开；预测 501 未注册 | **missing + 501 pending**；不伪闭合 |
| SCI-B01 / SCI-B02 | 无四件套；论文/中心性/前沿无正式 ID | 本叶补 TEMP_；seq 139 不靠本条翻成有 ID |
| QPOL-* / Q-TINDEX-01 / Q010～Q019 | 政策跟踪 / 指数后台 / 展示企业 | **本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未新建 `data-gap-catalog`（⑤ = 本表 + A2 `semantic_debt`，**N/A 于新 Q0xx**）。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 `/display` → Java display/metrics BFF → 只读 ADS；SCI 中心性可选 `graph/view`（116）。**不**经专题 E7 政策链，**不**调 DS-10/11/12。Java 不写 NLP / 不直连 nGQL。对照 05 叶 **不在本页跑专题 Job**。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。V1 知产规模 ADS **不等于** mapped 05 全叶。评估对象范围【算法补】= B 类。 |
| 预测 / 501 | **仅** TECH-INNOV seq 145 可标 501 实现通道；**未注册 metric_id**；差集 **missing**。SCI-CREATE seq 139：**04 未给 501**，保持 missing，禁止借 DS-04/DS-09 的 501 伪覆盖。 |
| 算法库 05 | 论文/专利计数 mapped 96；中心性 mapped 116；扶持力度 mapped 167；件数 mapped 100；效果 mapped 168。前沿 third_party 134；市场潜力 third_party 135；成熟度 third_party 137。引导力 / 保障力综合 / 专利质量 / 创新力综合 / 技术趋势 / 产业科学·技术影响力 / 潜力综合 / 科学创造力预测 → **missing 保持**。 |
| 本叶不做 | 不写任何 `cfg_metric-*-seed.yaml`；不发明 `M_SCI_*` / `M_TECH_INNOV_*` / `M_INDUSTRY_*` / `M_POLICY_GUIDE_*` / `M_POLICY_GUARD_*`；不改挂 B 轨 / SYNTH / CHAIN / SVC / ENT / `M_POLICY_*`；**不消费政策 OPEN**；不改 A2 catalog 正文；不写共享 LOOP 文件。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_**，**禁止**点开 `M_POLICY_*` / `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重/501/评估对象未冻：⚠️「待甲方确认」（文案走 PG/POT/TINN/SCI-B*，不要把 QPOL / Q-TINDEX-01 写进 `/display` DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样
- 功能实现 Owner（展示页要哪些指标）= `human:李伟`；STAT → GDF ADS + Java 聚合；MODEL 计算仍归唐绍祖监管 Python
- POLICY-GUARD 与 DS-10/11/12 / E7 政策工作台 **分路由**，禁止「政策」二字跳转混页

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-07-科技创新评估-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-07-METRIC-OPEN-L01.yaml` |
| A2 指针补丁（分叶） | `metrics/request/_work/open-loop/DS-07-METRIC-OPEN-L01-a2-patch.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-07-METRIC-OPEN-L01.md` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-07-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-07-METRIC-OPEN-L01-questions.yaml` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 18）；共享 `LOOP-state.yaml` / `METRIC-SEMANTIC-QUESTIONS.md` / `METRIC-OPEN-LOOP-a2-patch.yaml`；`POLICY-METRIC-OPEN-L01` 产物 |

---

## §赋号表（ID-ASSIGN 草稿 · 类型未签 · 2026-08-22）

> ELEMENT 默认 `INNOV`。POLICY-GUARD **不是** E7 政策 OPEN：不改挂 `M_POLICY_*` / `TOPIC-POLICY` / `POLICY-METRIC-OPEN-L01` 为本页唯一消费（Q-MO-DS07-01 默认仍 INNOV）。  
> 22/22 `TEMP_DS07_*` 已升正式草稿 ID。`algorithm_type` = `suggested_unsigned`。reuse = 0。未写 seed。  
> 预测：`M_INNOV_TINN_FORECAST` 可赋号 + 建议 MODEL，**501 pending 不是覆盖证明**，差集 missing 保持；`M_INNOV_SCI_FORECAST` 无 501，同样 missing。

| temp_id | metric_id | reuse | 建议类型 | Q |
|---------|-----------|-------|----------|---|
| TEMP_DS07_SCI_PAPER | M_INNOV_SCI_PAPER | — | STAT | — |
| TEMP_DS07_SCI_CENTRALITY | M_INNOV_SCI_CENTRALITY | — | MIXED | Q-MO-DS07-02 |
| TEMP_DS07_SCI_FRONTIER | M_INNOV_SCI_FRONTIER | — | MODEL | — |
| TEMP_DS07_SCI_FORECAST | M_INNOV_SCI_FORECAST | — | MODEL | — |
| TEMP_DS07_TINN_PATENT_COUNT | M_INNOV_TINN_PATENT_COUNT | — | STAT | Q-MO-DS07-03 |
| TEMP_DS07_TINN_PATENT_QUALITY | M_INNOV_TINN_PATENT_QUALITY | — | MODEL | — |
| TEMP_DS07_TINN_MARKET | M_INNOV_TINN_MARKET | — | MODEL | — |
| TEMP_DS07_TINN_COMPOSITE | M_INNOV_TINN_COMPOSITE | — | MODEL | — |
| TEMP_DS07_TINN_FORECAST | M_INNOV_TINN_FORECAST | — | MODEL | — |
| TEMP_DS07_POT_INPUT | M_INNOV_POT_INPUT | — | STAT | — |
| TEMP_DS07_POT_MATURITY | M_INNOV_POT_MATURITY | — | MODEL | — |
| TEMP_DS07_POT_OUTPUT | M_INNOV_POT_OUTPUT | — | STAT | — |
| TEMP_DS07_POT_SCI_INFL | M_INNOV_POT_SCI_INFL | — | MODEL | — |
| TEMP_DS07_POT_TECH_INFL | M_INNOV_POT_TECH_INFL | — | MODEL | — |
| TEMP_DS07_POT_COMPOSITE | M_INNOV_POT_COMPOSITE | — | MODEL | — |
| TEMP_DS07_PG_GUIDE | M_INNOV_PG_GUIDE | — | MODEL | Q-MO-DS07-05 |
| TEMP_DS07_PG_INTENSITY | M_INNOV_PG_INTENSITY | — | MIXED | Q-MO-DS07-04 |
| TEMP_DS07_PG_COUNT_DIST | M_INNOV_PG_COUNT_DIST | — | STAT | Q-MO-DS07-01 |
| TEMP_DS07_PG_FUND | M_INNOV_PG_FUND | — | STAT | Q-MO-DS07-01 |
| TEMP_DS07_PG_PROJECT | M_INNOV_PG_PROJECT | — | STAT | Q-MO-DS07-01 |
| TEMP_DS07_PG_EFFECT | M_INNOV_PG_EFFECT | — | MIXED | Q-MO-DS07-06 |
| TEMP_DS07_PG_COMPOSITE | M_INNOV_PG_COMPOSITE | — | MODEL | Q-MO-DS07-01 |

**计数**：赋号 22 · reuse 0 · 新编 22 · Q 6 · STAT 7 / MIXED 3 / MODEL 12。  
**禁止改挂**：`M_POLICY_*` / `M_SYNTH_*` / `M_CHAIN_*` / `M_SVC_*` / `M_ENT_*`；形近 `M_INNOV_PAPER_INFLUENCE` / `M_INNOV_PATENT_INFLUENCE` / `M_INNOV_FACTOR_FORECAST` / `M_TECH_HEAT_INDEX` / `M_TECH_POTENTIAL_SCORE` / `M_TECH_PATH_CENTRALITY` 不同口径，不 reuse。  
**N/A 不赋号**：seq 144 空间分布；seq 158 政策优化建议。  
**9/9 库 missing 保持**。

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _赋号草稿已出：22 条（reuse 0）；类型未签；TEMP 非终态；POLICY-GUARD 未改挂 `M_POLICY_*`；预测 501 pending ≠ 覆盖；9 行库 missing 保持；未写 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 展示页指标清单（李伟） | — | 本叶不定清单、不改挂 | |
| 甲方既有 Q 项 | — | 不改挂、不升 🟢；叶级 Q-MO-DS07-01…06 待合流 | |
