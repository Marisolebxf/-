# Topic 桥可行性判定 · 久新建议方案的调研结论（SYSINT-CHAIN-ELEM-LINK-02-L01 增补）

> 背景：久新建议用 **Topic（平台统一 Topic，即 OpenAlex Topics 体系）** 做产业链节点 ↔ 三要素的桥。本文档是该建议的可行性判定，作为 [`CHAIN-ELEM-LINK可行性判定记录.md`](./CHAIN-ELEM-LINK可行性判定记录.md) 的增补（原三通路判定不变，Topic 桥列为通路④）。
> 探针：`topic_bridge_probe.py` / `topic_bridge_probe2.py`（2026-11-05 只读实查）。
> 判定三条件沿用：数据在 + 关联有桥 + 口径已确认。

## 一、久新 Topic 体系的实查画像

| 事实 | 数值 | 来源 |
|---|---|---|
| Topic 字典总量 | **4,516 个**（平台 `topic_id` = `top_<hex32>`，含 OpenAlex 映射） | `ads_discipline_topic` |
| Topic → Subfield | 4,516 个 topic 覆盖全部 **252 个子学科**，每个 topic 必属一个 subfield | 同上 |
| 人才×Topic | `ads_talent_topic_profile` **684.7 万行**，9.9 万人才 × 4,516 topic 全覆盖 | 实查 |
| 机构×Topic | `ads_institution_topic_entry` 335.8 万行（64,555 机构）、`ads_institution_discipline_profile` 723.3 万行 | 实查 |
| 论文×Topic | `ads_paper_profile.primary_topic_id` + `topic_ids[]`（400 万行论文） | schema |
| 项目×Topic | `ads_project_profile.primary_topic_id`、`ads_project_topic` | schema |
| 专利×Topic | **新增族** `ads_patent_analysis_topic` 36.5 万行，3,484 个 topic、4,135 万 patent 关联（含中文名） | 实查 |
| 新兴主题×Topic | `ads_emerging_topic_*`（年度指标 5.4 万行） | schema |

**关键性质：Topic 是久新库内唯一一个「四类主体（论文/专利/项目/人才/机构）都带」的学科维度。** Subfield 只有人才/论文带；GB 码只有人才/机构带；技术节点只有技术带。Topic 是交集。

## 二、桥的可行性判定

### 条件一：数据在 —— **满足**

上表全绿。三要素（人才 9.9 万、机构 6.5 万）与四类成果（论文 400 万、专利 4,135 万关联、项目）全部带 `topic_id`。

### 条件二：关联有桥 —— **桥的两岸都有实体，中间一跳需建**

桥的形状：

```text
我方产业链节点（INB 码，1,220 个）
   │ 跳1：node → subfield（我方已有：subfield_topic_map 89 节点直挂 + L0 归并）
   ▼
Subfield（252 个，两侧同码同源，67 个已有久新集群映射背书）
   │ 跳2：subfield → topic（久新自有官方关系：ads_discipline_topic.subfield_id，4516 行字典，零成本）
   ▼
Topic（4,516 个）
   │ 跳3：topic → 三要素/成果（久新自有：talent_topic_profile / institution_topic_entry / paper / patent_analysis_topic）
   ▼
人才 / 机构 / 论文 / 专利 / 项目
```

**跳 2 是久新自有字典（`ads_discipline_topic.subfield_id` 是 NOT NULL 外键关系），不是我方拍的——这正是「用 Topic 做桥」优于「GB 码对照」的地方：GB 桥需要我方人工建 1,220 行对照并承担误报，Topic 桥的中间层是久新已经维护好的官方分类学。**

跳 1 沿用原判定（89 节点直挂、L0 归并兜底 100%）。

### 条件三：口径已确认 —— **部分满足，一项要书面确认**

- Topic 中文名已审核（`ads_discipline_topic.name_zh` NOT NULL，4,516 全有——与 `technology_name_zh` 修复同批）。
- 演示样例抽查：机械工程下「工程结构分析方法」、能源工程下「电力系统与可再生能源」、海洋工程下「海洋与近海工程研究」，命名质量与业务语义正常。
- **待确认一项**：Topic 与 Subfield 的从属关系是否 1:1（`ads_discipline_topic.subfield_id` 无数组形态，是单值外键）——实测每 topic 单 subfield，但需久新书面确认「topic 不跨 subfield」作为口径。另需确认 `ads_patent_analysis_topic` 是久新分析族的正式产物还是过程表（带 `run_id`，有迭代风险）。

### 判定结论

**Topic 桥可行，且优于原方案二的 GB 码桥（针对学科型挂接）。** 定级从「黄（我方建桥）」改为：

| 挂接 | 原通路 | 现判定 |
|---|---|---|
| 人才按链节点 | GB 桥（我方建 1,220 行对照） | **Topic 桥（跳2 用久新官方字典，零建桥成本）** |
| 机构按链节点 | GB 桥 | **Topic 桥** |
| 专利/论文/项目按链节点 | 无 | **Topic 桥新增能力**（GB 桥做不了这三类） |
| 技术按链节点 | tech_node_industry_map | 不变（Topic 桥不覆盖技术节点） |

**边界**：GB 码桥不废弃——「企业按产业」的场景（招投标、财务域）仍走 GB/INB 侧；Topic 桥覆盖的是**学术型主体**（人才、机构、论文、专利、项目）。两类桥互补，不是替代。

## 三、落地方案（给久新的确认稿 + 我方实施路径）

### 方案（一句话版）

**链节点 →(我方 `subfield_topic_map`)→ Subfield →(久新 `ads_discipline_topic` 官方字典)→ Topic →(久新各 *_topic 表)→ 人才/机构/论文/专利/项目。**

### 我方要做的

1. **镜像一张字典**：`ads_discipline_topic`（4,516 行，很小）进我方 DIM，作为 topic↔subfield 官方关系的只读快照（含 release 版本管理，随久新发版刷新）。
2. **链节点→topic 展开查询**：`subfield_topic_map`（已有）JOIN `discipline_topic` 镜像 → 得到每个链节点（直挂或 L0 归并）的 topic 集合。预计展开规模：89 直挂节点 × 平均 18 topic/subfield + 12 L0 全量，约 4,500–6,000 行预计算结果，可物化成 `chain_node_topic_map` 本侧表（我方算，非久新供）。
3. **消费端**：展示/专题按链节点过滤人才/机构/专利/项目时，先查 `chain_node_topic_map` 得 topic 集合，再对久新镜像表（阶段二 TDSQL 同步后的我方库）按 `topic_id IN (...)` 过滤。请求链不跨库，全部同域化后完成。

### 请久新确认的三点（并入 51 行回复或书面回函）

1. **Topic↔Subfield 1:1 口径**：`ads_discipline_topic.subfield_id` 单值外键，确认 topic 不跨 subfield、且该从属关系纳入变更管理（改了要通知）。
2. **`ads_patent_analysis_*` 表的稳定性**：带 `run_id`，确认是正式产物、随分析运行如何版本化；进圈表清单时按 release 还是按 run 选取。
3. **`ads_talent_topic_profile` / `ads_institution_topic_entry` 的更新频率与水位字段**（作为这两张表进圈表的增量依据）。

### 我方不做的

- 不要求久新建任何新表/新映射——Topic 桥的全部中间层久新已建好，我方只需镜像字典 + 物化展开表。
- 不把 Topic 桥用于企业侧（企业无 Topic 维度），企业走 INB/GB 侧不变。

## 四、对既有判定的更正与圈表增补

- **更正 CHAIN-ELEM-LINK 判定**：人才/机构挂链从「黄（GB 桥我方建）」改为「**绿→Topic 桥**（中间层久新官方字典，我方零建桥）」；新增专利/论文/项目按链节点过滤能力（原无通路）。
- **圈表增补（附页 A 建议项）**：`ads_discipline_topic`（字典，4,516 行）、`ads_talent_topic_profile`（684.7 万行）、`ads_institution_topic_entry`（335.8 万行）、`ads_patent_analysis_topic`（36.5 万行）——四张表是 Topic 桥的最小集，建议纳入阶段二第一批。
- 保守起见 GB 码桥保留为**降级预案**：若久新对 Topic 口径确认拖延，先建 GB 桥保人才/机构演示（原方案不变）。

## 诚实性红线

- Topic 展开后的「链节点粒度」仍是 subfield 级聚合（一个 subfield 平均 18 个 topic，粒度介于节点与产业之间），界面标注规则与 L0 回退相同。
- 未确认「topic 不跨 subfield」前，展开查询不得按 1:1 假设写死。
- `chain_node_topic_map` 物化表属我方派生数据，血缘标注来源=我方加工（输入：subfield_topic_map + discipline_topic 镜像），不冒充久新原表。
