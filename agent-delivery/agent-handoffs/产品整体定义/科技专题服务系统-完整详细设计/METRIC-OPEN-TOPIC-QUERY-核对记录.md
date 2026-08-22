# METRIC-OPEN-TOPIC-QUERY-核对记录

> **任务**：TOPIC-QUERY-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 6）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 04「科技专题数据查询」+ 详细设计 `04-功能-数据查询.md` 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：专题查询 **一整包** `page_id=TOPIC-QUERY` 的 ④ 指标语义卡 + ⑤ 开放项。覆盖 04 三级 I 十二招标叶子（呈现 seq 1–5 + 分析 seq 6–12）。**不对 05 八维 97 叶打 mapped / missing。** 不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ **混页**：有统计则 kit；壳/检索 N/A+依据 | 十二叶子里 **仅 seq 6–7 推荐图表**在页上给出产品定义的统计数字（人才结构、科研绩效、技术/服务/资讯热度）→ **出卡**。正式 ID 见 **§赋号表**（`TEMP_*` 对照保留）。**禁止** `M_QUERY_*` / `M_SEARCH_*` / `M_HEAT_*` / `M_WORDCLOUD_*`，**禁止写入 seed**。检索/结果壳/自定义图表工作区 **禁止口头 N/A**，一律 **N/A + 依据**（§3.3）。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 QRY-B01…B07。展示 E1 / 八维 OPEN **不改挂**为本页。本叶不改 `客户决策清单跟踪表.md`、不升 🟢。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/TOPIC-QUERY.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签。 |
| PDR-06 自检 | ⏳ 有条件 | 推荐图表 STAT 可写演示公式（当前结果集聚合）；公式 `pending_cosign`。人才分箱 / 绩效核 / 热度分母未冻 → QRY-B03/B06/B07。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：本页 **非整页 N/A**。给人说明「专题 · 查询走 n/a_ops、不进九新清单」指的是 **不把查询页指标列入九新三方交付、功能 Owner 待指定**，**不是**允许对页上统计数字口头 N/A。§8.4 甲对本叶写明「有统计数字就不能口头 N/A」。

- **④ kit**：seq 6–7 推荐图表上的 5 个产品定义统计核（§2）。
- **④ N/A + 依据**：seq 1–5 检索/呈现壳、seq 8–12 自定义图表工作区壳、命中条数、八维战略页、展示 E1（§3.3）。
- 甲方未冻分箱/绩效/热度分母 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本页必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `TOPIC-QUERY` | 科技专题数据查询（整包） | **kit**（仅推荐图表）+ 壳 **N/A+依据** | §赋号表 5×`M_*_QUERY`（TEMP 对照） | 对 05 八维打 missing/mapped；reuse 05 模型 ID / `M_ENT_*` / `M_CHAIN_*` / `M_SVC_ORG_CNT`；发明 `M_QUERY_*`；写入 seed；用展示 `ENT-MOD-SEARCH` / 图谱API seq 116 顶替 |

**展示企业查询（E1 / A2.2）**：本叶 **不消费**。`ENT-MOD-SEARCH-METRIC-OPEN` 与全部 `M_ENT_*` **不是**本页语义层。

**八维战略分析（W1–W4）**：本叶 **不消费**。`TOPIC-ENT-05` / `TOPIC-TECH-05` / `TOPIC-ORG-05` / `TOPIC-TALENT-05` / `SVCCHAIN-*` / `E7-POLICY` / `SYNTH-*` 的 OPEN 与 B 轨 ID **禁止**改挂为本页。

### §1.2 04 十二招标叶子 × 差集 × ④

> 差集列维持 A2 已写判定（本页 A=0、C(算法叶)=0）。④ 是语义层，**不等于**把 other_system 改成 mapped。

| seq | 招标叶子 | A2 差集 | ④ |
|-----|----------|---------|----|
| 1 | 关键词与语义融合探查 | `other_system` | **N/A + 依据**（检索门面） |
| 2 | 结构化条件与图谱联动探查 | `other_system` | **N/A + 依据**（查询壳 + 结果子图浏览） |
| 3 | 多模态结果展示与交互 | `n/a_ops` | **N/A + 依据**（UI 壳；命中条数同此） |
| 4 | 专业术语与主体详情呈现 | `other_system` | **N/A + 依据**（知识库/主数据直读） |
| 5 | 查询结果智能导出 | `n/a_ops` | **N/A + 依据**（导出壳） |
| 6 | 人才与科研产出分析视图 | `other_system`（BI，非 05 人才/机构模型） | **kit**（TEMP_ TALENT_STRUCT / ORG_PERF） |
| 7 | 技术、服务与资讯热度视图 | `other_system`（可视化，非 05 技术热点叶） | **kit**（TEMP_ TECH_HEAT / SVC_DIVERSITY / INFO_TREND） |
| 8 | 多维数据筛选与组合 | `n/a_ops` | **N/A + 依据**（自定义图表交互壳） |
| 9 | 图表类型与坐标配置 | `n/a_ops` | **N/A + 依据** |
| 10 | 多图表集成与模板应用 | `n/a_ops` | **N/A + 依据** |
| 11 | 可视化布局与对齐控制 | `n/a_ops` | **N/A + 依据** |
| 12 | 面板保存与多格式导出 | `n/a_ops` | **N/A + 依据** |

「智能分析」= **当前查询结果集上的 BI/图表工作区**，不是八维战略分析模型、不是 05 综合 11 叶。禁止因「库无查询维」把 05 97 叶打成 A 类 `missing`。

### §1.3 TRACE / A2 语义层指针（Round 17 才回写 catalog 正文）

本叶 **不改** `metrics/request/专题系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml`，由 coordinator 合流）。**不改** `LOOP-state.yaml`。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | `TOPIC-QUERY` 唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/专题系统/pages/TOPIC-QUERY.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: TOPIC-QUERY-METRIC-OPEN-L01`。**库缺口 `missing` 不动**（本页 A 类本就为空）。差集 `other_system` / `n/a_ops` **不**因 OPEN 存在而改 mapped。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `TOPIC-QUERY` | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（QRY-B01 文件级闭合） |
| TRACE / WF | **无**专题查询四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 04 叙述发明 `M_*` |
| PACK | 无独立 `TOPIC-QUERY-PACK-L01` | SRS 04 查询目录 + `04-功能-数据查询.md` 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。

---

## §2 模块消费矩阵（TEMP 对照 · 正式 ID 见 §赋号表）

> 差集列维持 A2：**seq 6–7 = `other_system`**（不是 05 模型输出）。本表只闭合语义层：页上有统计数字 → 身份卡。`algorithm_type` 列为 **草稿建议**，未会签。  
> 正式 `M_*` 见 **§赋号表**；`TEMP_*` 仅作对照。**禁止**写入 `metrics/registry/` seed。  
> 聚合域 = **当前查询结果集**（ES 命中 ∪ 可选 ADS 字段），**不是**八维分析页的全量切片。

| temp_id | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|------|-------------------|---------|
| TEMP_TOPIC_QUERY_TALENT_STRUCT | seq 6：人才结构饼图/柱状 | ✅ kit | STAT | Q-MO-QUERY-01；禁消费 TOPIC-TALENT-05 / 综合 seq 184 |
| TEMP_TOPIC_QUERY_ORG_PERF | seq 6：科研机构绩效饼图/柱状 | ✅ kit | STAT | Q-MO-QUERY-02；禁消费 TOPIC-ORG-05 |
| TEMP_TOPIC_QUERY_TECH_HEAT | seq 7：技术热点热力图/词云 | ✅ kit | STAT | Q-MO-QUERY-03；禁 mapped seq 134 / TOPIC-TECH-05 |
| TEMP_TOPIC_QUERY_SVC_DIVERSITY | seq 7：服务类型/生态多样性 | ✅ kit | STAT | Q-MO-QUERY-04；禁消费 SVCCHAIN-* / `M_SVC_ORG_CNT` |
| TEMP_TOPIC_QUERY_INFO_TREND | seq 7：资讯传播趋势 | ✅ kit | STAT | Q-MO-QUERY-05；不发明 `M_HEAT_*` / `M_WORDCLOUD_*` |

**5/5 均 other_system + 本叶 present。** 不得因「口径未冻 / D1 draft / 类型未签」把上表改成差集 `missing`。不得因赋号把差集改成 mapped。不得对 05 八维打 missing。正式 ID **禁止写入 seed**。

---

## §赋号表（METRIC-ID-ASSIGN-LOOP · 2026-08-22）

> 本工作流把 `TEMP_*` 升成正式 `M_*`（新号，0 reuse）。建议类型 `suggested_unsigned`，**未签**（`human:唐绍祖`）。叶级 Question = `Q-MO-QUERY-nn`（🟡）；**未写**共享 `METRIC-SEMANTIC-QUESTIONS.md` / 客户决策清单 / seed / 展示 catalog。
>
> **防撞（只读 query）**：seed 无 `M_TALENT_*` / `M_ORG_*` / `M_TECH_*` / `M_COMMON_*`；五候选号均不存在。近义不 reuse：`M_CHAIN_HOTSPOT_*`、`M_CHAIN_NEWS_COUNT` / `M_CHAIN_HOT_NEWS_COUNT`、`M_SVC_ORG_CNT`、`M_POLICY_TYPE_DIST`。05 的 `TEMP_TOPIC_TECH_HEAT_INDEX` / 人才·机构模型 **口径不同**（战略切片或 G3 Job ≠ 当前结果集 BI）。
>
> 命名：`M_{ELEMENT}_{INDICATOR}_QUERY`；资讯无七要素助记码 → `COMMON`。VARIANT=`QUERY` 表示口径=当次查询结果集，不是展示位置。

| temp_id | metric_id | reuse_of | 中文名 | 建议 type（未签） | pending_ref |
|---------|-----------|----------|--------|-------------------|-------------|
| TEMP_TOPIC_QUERY_TALENT_STRUCT | M_TALENT_STRUCT_QUERY | — | 查询结果·人才结构 | STAT | Q-MO-QUERY-01 |
| TEMP_TOPIC_QUERY_ORG_PERF | M_ORG_PERF_QUERY | — | 查询结果·科研机构绩效 | STAT | Q-MO-QUERY-02 |
| TEMP_TOPIC_QUERY_TECH_HEAT | M_TECH_HEAT_QUERY | — | 查询结果·技术热度 | STAT | Q-MO-QUERY-03 |
| TEMP_TOPIC_QUERY_SVC_DIVERSITY | M_SVC_TYPE_DIST_QUERY | — | 查询结果·服务类型分布 | STAT | Q-MO-QUERY-04 |
| TEMP_TOPIC_QUERY_INFO_TREND | M_COMMON_INFO_TREND_QUERY | — | 查询结果·资讯传播趋势 | STAT | Q-MO-QUERY-05 |

**汇总**：赋号 5 / 复用 0 / 新号 5 / Q 5 / 建议类型 STAT×5。

内部默认（待甲方，不升 🟢）：

| Q | 默认 | 一句话 |
|---|------|--------|
| Q-MO-QUERY-01 | 学历为主分箱，职称/年龄可切换 | 招标未冻维；STAT 第一刀用学历 |
| Q-MO-QUERY-02 | 结果集内关联论文数 COUNT | 保持 STAT；禁滑向 05 机构评价 MODEL |
| Q-MO-QUERY-03 | 结果集内 term TF | 禁套 seq 134 / `M_CHAIN_HOTSPOT_*` |
| Q-MO-QUERY-04 | 主数据 `svc_type`/`org_type` | 禁改挂 SVCCHAIN / `M_SVC_ORG_CNT` |
| Q-MO-QUERY-05 | 自然月 × 资讯条数 | 不 reuse 链域 `M_CHAIN_NEWS_*` |

机器卡：`metrics/request/_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01.yaml`（`demands` 已换 `M_*`，保留 `temp_id`）。叶级 yaml：`metrics/request/_work/id-assign/TOPIC-QUERY-METRIC-OPEN-L01.yaml` + `-questions.yaml`。

---

## §3 ④ 指标语义卡（仅推荐图表 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 分箱 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以「查询结果集 + 可选 ADS 字段」为准，**不**把项目 DWD 反推成 ODS `full`。A1 双表未交 → `A1需规ID` 空。

8 件套草稿字段（TEMP 对照 + 正式 ID）：metric_id=§赋号表 `M_*`；源系统=科技专题服务系统·查询工作台；更新频率=随查询即时；version=`draft-assign-r1`；源表=当前结果集（ES 命中；字段级 ADS 可选，A1 表2 未交 → 本叶不填伪 full）。`algorithm_type` 建议 STAT，**未签**。

详细设计 `04-功能-数据查询.md` §4「推荐图表 = 规则匹配字段类型」支持本页 STAT，**不是** 05 深度模型。同节「热度词云 · `.1` 资讯/论文类指标」仅表示 **可消费 ADS 字段**，**禁止**据此把 05 基础指标叶 mapped 进本页。

### §3.1 人才与科研产出分析视图 · kit（Bid seq 6；excel_row 9；QRY-D06）

| metric_id | temp_id | 中文名 | 口径（适用性已认 + 内部默认） | 公式（未签） | 建议 type |
|-----------|---------|--------|------------------------------|--------------|-----------|
| M_TALENT_STRUCT_QUERY | TEMP_TOPIC_QUERY_TALENT_STRUCT | 查询结果·人才结构 | 对 **当前查询命中** 中的人才实体（talent_id 去重），按结构分箱统计数量与占比。默认分箱=最高学历，职称/年龄可切换（Q-MO-QUERY-01）。不是 05 人才 13 叶综合评价。 | 演示：`COUNT(talent_id) GROUP BY struct_bin`；占比=箱内数/结果集人才数 | STAT |
| M_ORG_PERF_QUERY | TEMP_TOPIC_QUERY_ORG_PERF | 查询结果·科研机构绩效 | 对 **当前查询命中** 中的科研机构（org_id 去重），默认按关联论文数 COUNT 聚合（Q-MO-QUERY-02），匹配饼图或柱状。不是 05 科研机构 10 叶模型输出。 | 演示：`COUNT(paper) GROUP BY org_id\|org_type`；核 pending 会签 | STAT |

筛选壳、字段勾选本身见 §3.3（seq 8）。不另造「推荐图表张数」ID。

### §3.2 技术、服务与资讯热度视图 · kit（Bid seq 7；excel_row 10；QRY-D07）

| metric_id | temp_id | 中文名 | 口径（适用性已认 + 内部默认） | 公式（未签） | 建议 type |
|-----------|---------|--------|------------------------------|--------------|-----------|
| M_TECH_HEAT_QUERY | TEMP_TOPIC_QUERY_TECH_HEAT | 查询结果·技术热度 | 对当前结果集中的技术术语/主题做词频，以热力图或词云呈现。默认分母=结果集内 TF（Q-MO-QUERY-03）。**不是** 05 技术链热点识别（seq 134），也 **不 mapped** seq 116，不 reuse `M_CHAIN_HOTSPOT_*`。 | 演示：结果集内 term TF；分母默认当前结果 | STAT |
| M_SVC_TYPE_DIST_QUERY | TEMP_TOPIC_QUERY_SVC_DIVERSITY | 查询结果·服务类型分布 | 对当前结果集中的服务机构按主数据类型计数。字典默认=`svc_type`/`org_type`（Q-MO-QUERY-04）。不是产业服务深度分析 / SVCCHAIN 门户规模核，不 reuse `M_SVC_ORG_CNT`。 | 演示：`COUNT(org_id) GROUP BY svc_type` | STAT |
| M_COMMON_INFO_TREND_QUERY | TEMP_TOPIC_QUERY_INFO_TREND | 查询结果·资讯传播趋势 | 对当前结果集中的资讯按自然月桶计数（Q-MO-QUERY-05）。不 reuse `M_CHAIN_NEWS_COUNT`。资讯 CMS 喂数无独立核。 | 演示：`COUNT(info_id) GROUP BY month` | STAT |

词云/热力图是 **可视化形态**，无独立第三核 → 不另造 `TEMP_…_WORDCLOUD` / `M_HEAT_*` / `M_WORDCLOUD_*`。QRY-B05 记形态无核，统计走本表三枚正式 ID。

### §3.3 ④ 不适用（N/A + 依据）

整页 N/A：**无**（seq 6–7 有统计数字，已出卡）。下列项 **禁止口头 N/A**。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| seq 1 / QRY-D01 | 关键词与语义融合探查 | **`other_system`** | 检索门面（架构：`lumen-etl-es-py` / ES；禁止并进 `lumen-algo-py` 当算法库叶）。意图/实体探查无独立统计核。**不 mapped** 综合/图谱API seq 116 实体检索。无 `metric_id`，不发明 `M_*`。语义欠账 QRY-B04。 |
| seq 2 / QRY-D02 | 结构化条件与图谱联动探查 | **`other_system`** | 多字段筛选 + 结果子图 **浏览**。不调用八维图谱构建/关系抽取叶。详细设计 `.2.15` 是实现接线提示，**不**构成本页对 05 的 mapped，也 **禁止**把 seq 116 打成 A 类 missing。 |
| seq 3 / QRY-D03 | 多模态结果展示与交互 | **`n/a_ops`** | 列表/图谱切换、排序、筛选、批量。UI 壳。**命中条数**（「共 N 条」）= 检索壳结果计数，无独立口径核，不另造 `TEMP_ HIT_CNT`。 |
| seq 4 / QRY-D04 | 专业术语与主体详情 | **`other_system`** | 知识库术语解释 + 产业/技术/企业详情页。主数据直读。禁止 mapped 05 实体识别叶。 |
| seq 5 / QRY-D05 | 查询结果智能导出 | **`n/a_ops`** | Excel/JSON 导出、自定义字段、分表、批量下载。导出壳。 |
| seq 8 / QRY-D08 | 多维数据筛选与组合 | **`n/a_ops`** | 用户从结果勾选字段、过滤时间/地区、交叉。自定义图表 **交互壳**。用户自选聚合无产品定义核；推荐图表固定核走 §3.1–3.2。 |
| seq 9 / QRY-D09 | 图表类型与坐标配置 | **`n/a_ops`** | 图表类型库与标签/刻度。前端可视化配置。 |
| seq 10 / QRY-D10 | 多图表集成与模板应用 | **`n/a_ops`** | 多图组面板 + 行业/趋势模板。看板编排。 |
| seq 11 / QRY-D11 | 可视化布局与对齐控制 | **`n/a_ops`** | 拖拽位置/大小 + 网格。纯布局。 |
| seq 12 / QRY-D12 | 面板保存与多格式导出 | **`n/a_ops`** | 面板落个人/团队空间并导出。工作区持久化。 |
| QRY-D13 | 八维战略分析页（W1–W4） | **`other_system`** | 05 全部 97 叶归那些 `page_id`。本查询页 **不得 mapped、不得 missing、不得消费** 其 METRIC-OPEN / B 轨 ID。 |
| QRY-D14 | 展示系统企业查询（E1） | **`other_system`** | A2.2 / `DS-ALGO-GAP-L01`。**禁止** `ENT-MOD-SEARCH-METRIC-OPEN` 与全部 `M_ENT_*`。 |
| 范围外 | `TOPIC-OPS` / `TOPIC-DATAREQ` | `n/a_ops` / `other_system` | 给人说明 §8.4：运营/需求面走 N/A，不算缺 OPEN 任务。 |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| QRY-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 17 才改指针 | 语义欠账→有指针；非 A 类 missing |
| QRY-B02 | PDR-05/06 有条件；公式未签 | ⏳ |
| QRY-B03 | 推荐图表统计已赋正式 ID（§赋号表）；科研「绩效」核仍待甲方（Q-MO-QUERY-02） | 语义债转叶级 Q；禁止改挂八维指标；禁止写入 seed |
| QRY-B04 | 语义检索/意图/实体探查无正式 ID | 保持；④ 已 N/A+依据；不 mapped seq 116，不 missing |
| QRY-B05 | 热力图/词云无独立形态核 | 统计走 M_TECH_HEAT_QUERY / M_SVC_TYPE_DIST_QUERY / M_COMMON_INFO_TREND_QUERY；不发明 `M_HEAT_*` / `M_WORDCLOUD_*` |
| QRY-B06 | 人才结构分箱字典未冻 | **收口到 Q-MO-QUERY-01**（内部默认学历为主）；不消费展示人才 Q 或 TOPIC-TALENT-05 |
| QRY-B07 | 热度分母与资讯时间桶未冻 | **收口到 Q-MO-QUERY-03 / Q-MO-QUERY-05** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未 append 共享 `METRIC-SEMANTIC-QUESTIONS.md`。叶级 Q 见 `id-assign/TOPIC-QUERY-METRIC-OPEN-L01-questions.yaml`。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/topic/v1/.../search\|graph\|metrics` → 检索走 ES / `lumen-etl-es-py`；推荐图表 = 结果集字段 STAT 聚合（详细设计：规则匹配字段类型）。Java 不写 NLP / 不直连 nGQL。禁止把查询检索并进 `lumen-algo-py` 冒充 05 叶。 |
| 准入 / ODS | 查询结果来自 ES 索引 + 可选 ADS。A1 双表未交 → 本叶 D3 不得伪 `full`。 |
| 算法库 05 | **本页不拥有 05 任何叶。** 不 mapped、不 missing。图谱API seq 116 归综合维；本页图谱是检索结果可视化。 |
| 本叶不做 | 不写任何 `cfg_metric-*-seed.yaml`；正式 ID 只在核对记录 / id-assign；不把八维 / 展示 E1 / B 轨 63+29 改挂；不对 05 打 missing；不改共享 QUESTIONS / LOOP-state。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡 **推荐图表**上的统计数字：ⓘ MetricSpecCard。seed **仍无**本页行 → 回指 **本记录 §赋号表 `M_*` + TEMP 对照**，**禁止**点开 `M_ENT_*` / `M_CHAIN_HOTSPOT_*` / `M_CHAIN_NEWS_*` / `M_SVC_ORG_CNT` / 八维页指标伪 8 件套
- 检索命中条数、导出、布局、自定义图表：无 ⓘ 指标卡（N/A+依据）
- Wave 0：🧪 MockBadge（推荐图表演示数）
- 分箱/绩效核/热度分母/类型字典/时间桶未冻：⚠️「待甲方确认」（文案走 Q-MO-QUERY-nn，不要写展示 Q 字样到专题 DOM）
- 正式 ID 未入 seed：D1 按 `draft` 诚实；draft ⓘ，**不把类型写成已签、不标 D1=aligned**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner = **待指定**（给人说明：专题 · 查询；STAT 仍走 GDF ADS + Java 聚合，公式共签唐绍祖）

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-QUERY-核对记录.md`（含 **§赋号表**） |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01.yaml`（demands=`M_*` + temp_id） |
| 叶级赋号卡 | `metrics/request/_work/id-assign/TOPIC-QUERY-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-QUERY-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（本叶） | `metrics/request/_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01-a2-patch.yaml`（OPEN 指针；本轮未改） |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-QUERY-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；展示 catalog / pages；共享 `METRIC-SEMANTIC-QUESTIONS.md`；`LOOP-state.yaml`；客户决策清单 |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；赋号草稿 5/5 新号（§赋号表）；类型未签；适用性：TOPIC-QUERY **混页** — seq 6–7 **kit**；seq 1–5 / 8–12 **N/A+依据**；**不对 05 打 missing**_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方分箱/绩效/热度分母 | — | 保持未冻；不升 🟢 | |
