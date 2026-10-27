# SYSINT-SCHEME-07-L02 · 七要素与需求清单对齐轴

> **任务**：`SYSINT-SCHEME-07-L02`（WBS-07-00A）
> **监管人**：human:郭万迎
> **完成日期要求**：2026-11-09（WBS-07-00 出门日）
> **创建时间**：2026-10-27

## 一、目的与口径

### 1.1 本文件是什么

本文件是一张**中间对齐表**，不做差集分析。它把两个不同视角的清单逐行对到同一行，为后续 L03（算法中台上图台账）和 L04（燕大七要素上图对照）提供减数基准。

| 视角 | 来源 | 实体数 | 关系数 | 命名风格 |
|---|---|---:|---:|---|
| **需求侧**（展示系统要什么） | 致燕大知识图谱接口需求清单 v1.0 | 14 | 17 | 业务功能名（enterprise、policy、cooperate） |
| **燕大侧**（图谱已有什么） | 七要素数据维度与上图逻辑现状快照（2026-10-26） | 17 TAG | 33 EDGE | 图工程名（Organization、AUTHORED_BY） |

### 1.2 硬约束（来自 task DoD）

1. **不改燕大快照原文，不改需求清单原文**——本文件只对齐，不修订上游
2. **对不上的行单独留下**，不强行并进「产业」或「企业」
3. `dataset`、`topic`、`event`、`activity`、`innovation_carrier`、`field` **不并进七要素**，在对齐表中单独留行

### 1.3 对齐判定符号

| 符号 | 含义 |
|---|---|
| ✅ | 直接对齐：1:1 或多:1 清晰映射 |
| 🔶 | 部分对齐：边界不同、语义缩小、多 TAG 混装 |
| 🔴 | 无对应：需求侧有，燕大侧完全不存在 |

---

## 二、七要素归属总表

> 先把 14 个需求实体归入七个要素框架，作为后续对齐的宏观锚点。

| # | 七要素 | 需求实体 | 对齐判定 | 燕大侧现状（见快照 1.2 节） |
|---|---|---|---|---|
| 1 | 产业 | — | — | ✅ 已实现（IndustryChain、IndustryNode） |
| 2 | 企业 | `enterprise` | 🔶 | ✅ 已实现但无专属枚举（Organization 默认桶混装） |
| 3 | 技术（论文） | `paper`、`patent`、`project` | ✅ | ✅ 已实现（Paper、Journal、Patent、PatentFamily、Report、Keyword、Project） |
| 4 | 人才 | `person` | ✅ | ✅ 已实现（Person、ScholarOrganization） |
| 5 | 科研机构 | `institution` | ✅ | ✅ 已实现（Organization org_kind=domestic_university / domestic_research_institute） |
| 6 | 政策 | `policy` | 🔴 | ⚠ 未实现（蓝图+源表已备，无 TAG） |
| 7 | 服务机构 | — | — | ⚠ 无独立口径（Organization 默认桶混装，无专属 org_kind 值） |
| — | **不并进七要素** | `technology`、`field`、`topic`、`event`、`dataset`、`activity`、`innovation_carrier` | 各自判定 | 见下表 |

---

## 三、实体对齐表（需求侧 14 实体 ↔ 燕大侧 17 TAG）

> 逐行对齐，共 14 行。最后 6 行标记「不并进七要素」。

| # | 需求实体ID | 中文名 | 七要素归属 | 对应燕大 TAG | 对齐判定 | 燕大现状 | 对齐说明 |
|---|---|---|---|---|---|---|---|
| 1 | `institution` | 机构 | 科研机构 | `Organization`（org_kind=domestic_university / domestic_research_institute）+ `ScholarOrganization` | ✅ | ✅ 已实现 | 燕大靠 org_kind 枚举两值（高校 / 科研院所）区分科研机构要素；ScholarOrganization 是 2026-10-15 新增的轻量任职机构 TAG，用于修复 AFFILIATED_WITH 悬挂端点。两个 TAG 共同覆盖需求侧 institution |
| 2 | `enterprise` | 企业 | 企业 | `Organization`（org_kind=默认桶 domestic_organization）+ `Product` + `Event` + `News` | 🔶 | ✅ 已实现（无专属枚举） | **核心难点**：燕大无「企业」专属 org_kind 值。内地企业主体全落 `domestic_organization` 默认桶；`org_type` 本地实测基本为空（3689 行中 3639 NULL），连文本区分都不可用。Product / Event / News 是企业要素下的子实体，依附 Organization 存在 |
| 3 | `paper` | 论文 | 技术 | `Paper` + `Journal` + `Report` | ✅ | ✅ 已实现 | 需求侧 paper 涵盖学术论文 + 期刊论文；燕大 Paper + Journal 精确覆盖；Report 是科技成果（软科学报告），需求侧未单列但属性上可并入 paper |
| 4 | `patent` | 专利 | 技术 | `Patent` + `PatentFamily` | ✅ | ✅ 已实现 | Patent 覆盖单体专利，PatentFamily 覆盖同族聚合。需求侧 patent 未明确同族概念，但 PatentFamily 是自然扩展 |
| 5 | `project` | 项目 | 技术 | `Project` | ✅ | ✅ 已实现 | 需求侧涵盖科研项目、软科学课题、联合研发项目；燕大 Project 一表覆盖 |
| 6 | `person` | 人员/专家 | 人才 | `Person` + `ScholarOrganization` | ✅ | ✅ 已实现 | 需求侧 person 涵盖专家、学者、科研人员、团队负责人；燕大 Person 覆盖 scholar + author + 机构角色人员三类，ScholarOrganization 作为任职机构端点补齐边 |
| 7 | **`policy`** | **政策** | **政策** | **—** | **🔴** | **⚠ 未实现（蓝图+源表已备）** | 燕大快照明确标注政策要素无 TAG，源表和蓝图已准备好但尚未上图。这是 **P0 GAP** |
| 8 | — | 产业 | 产业 | `IndustryChain` + `IndustryNode` | ✅ | ✅ 已实现 | 需求清单未单列产业实体（产业是展示系统的模块而非实体），但燕大侧产业要素是完整的——7 位链行 + 9-21 位节点行，IndustryNode 1261 节点有父子层级和上下游字段 |
| 9 | — | 服务机构 | 服务机构 | `Organization`（默认桶混装，无专属 org_kind） | 🔶 | ⚠ 无独立口径 | 与 enterprise 同困境：燕大 Organization 默认桶同时装企业和服务机构，无 org_kind 枚举值可区分。需求清单未单列服务机构实体（七要素之一），但展示系统科技服务全景模块隐含需要 |
| --- | **以下 6 行不并进七要素** | | | | | | |
| 10 | `technology` | 技术 | — | 最接近 `Keyword` | 🔶 | ✅ Keyword 已实现 | **边界不同**：需求侧 technology = 技术点/技术方向/技术领域下的具体技术，还要有层级关系（technology_hierarchy）和技术影响（technology_influence）。燕大 Keyword = 论文/专利/项目关键词本体（中英归一化，237,552 词），覆盖面远广但语义粒度不同 |
| 11 | `field` | 领域 | — | 无显式 TAG | 🔶 | — | 燕大无独立「学科领域/技术领域」TAG。Keyword 部分覆盖，但领域是更高层级的分类体系（人工智能、量子计算、生物医药…），与关键词不等价 |
| 12 | `topic` | 主题 | — | 最接近 `Keyword` | 🔶 | ✅ Keyword 已实现 | **边界不同**：需求侧 topic = 研究主题/技术主题，是「主题库与主题分类」的载体，有主题交叉关系（dataset_link）。燕大 Keyword 是关键词本体，没有主题分类层级和主题库概念 |
| 13 | `event` | 科技事件 | — | `Event` | 🔶 | ✅ Event 已实现 | **语义不同**：需求侧 event = 科创事件（论坛、发布会、签约）。燕大 Event = 企业工商风险事件（17 张表：融资、处罚、诉讼、失信、破产…），量级 16M 行封顶 124,999。**同一个 TAG 名但覆盖范围几乎无交集** |
| 14 | **`activity`** | **科技活动** | — | **—** | **🔴** | **—** | 无任何对应 TAG。科技交流活动/赛事/专家讲座在燕大侧完全不存在。**P1 GAP** |
| 15 | **`innovation_carrier`** | **创新载体** | — | **—** | **🔴** | **—** | 无任何对应 TAG。孵化器/创新平台/园区在燕大侧无独立实体（可能隐含在 Organization 中但无口径区分）。**P1 GAP** |
| 16 | **`dataset`** | **数据集** | — | `DataSource`（治理占位 TAG） | **🔴** | **—** | 燕大 `DataSource` 是 Schema 治理层的**占位 TAG**（id / 表中文名 / tier / library），用于溯源元数据，不是业务实体「科技数据资源/主题库/专题数据」。两者不等价 |

---

## 四、关系对齐表（需求侧 17 关系 ↔ 燕大侧 33 EDGE）

> 逐行对齐，共 17 行。燕大侧 33 EDGE 分布：论文域 9 + 人才域 8 + 产业域 5 + 机构工商治理域 11。

| # | 需求关系ID | 关系名 | 起点 → 终点 | 对应燕大 EDGE | 对齐判定 | 燕大侧现状 | 对齐说明 |
|---|---|---|---|---|---|---|---|
| 1 | `cooperate` | 合作 | person↔person；institution↔institution；person↔institution | `COAUTHOR_WITH`（仅 person↔person） | 🔶 | ✅ 已实现（Person-Person 合著 ≈1.19M 边） | **语义缩小**：需求侧 cooperate 是三端点全方向的合作网络（合著、项目合作、师承、技术交流），燕大只有 COAUTHOR_WITH（Person-Person 合著）一种，且是无向边 |
| 2 | `belong` | 隶属 | person→institution；institution→institution（上级） | `AFFILIATED_WITH`（person→Organization）、`STUDIED_AT`（person→Organization） | 🔶 | ✅ 已实现 | **有两段但覆盖不全**：AFFILIATED_WITH + STUDIED_AT 覆盖了 person→institution（任职 + 就读），但需求侧还需要 institution→institution 的**上级隶属**（如院所→上级主管部门、子机构→总部），燕大全无 |
| 3 | `research` | 研究 | person→field/topic；institution→field；enterprise→field | — | 🔴 | — | 燕大无任何「人/机构研究某领域/主题」的边。Keyword 是被动的「论文有某关键词」（HAS_KEYWORD），不是主动的「人研究某技术」 |
| 4 | `cite` | 引用 | paper→paper；patent→paper；patent→patent | `CITES`（Paper→Paper） | 🔶 | ✅ 已实现 | **仅覆盖一段**：燕大 CITES 是 Paper→Paper 引用（含 DOI 桩点 + SAME_AS 对齐），但需求侧还要 patent→paper 和 patent→patent，燕大全无 |
| 5 | `participate` | 参与 | person→project；institution→project | `LEADS`（Project→Person）、`HAS_PARTICIPANT`（Project→Person）、`FUNDED_BY`（Project→Organization） | 🔶 | ✅ 已实现 | Person→Project 基本覆盖（LEADS 负责人 + HAS_PARTICIPANT 参加人），但 Institution→Project 只有 FUNDED_BY（资助方），**参加机构/合作机构无对应** |
| 6 | `belong_to` | 属于 | paper/patent/project/technology→field | — | 🔴 | — | 燕大无「成果/技术归属学科领域」的边。HAS_KEYWORD 是关键词关联不是领域归属 |
| 7 | `author_of` | 著作 | person→paper/patent | `AUTHORED_BY`（Paper→Person）、`INVENTED_BY`（Patent→Person） | ✅ | ✅ 已实现 | 需求侧 author_of 有向 `person→paper/patent`，燕大两条边方向相反（`Paper→Person`、`Patent→Person`），但语义等价。注意 INVENTED_BY 走挂实体改道（pendingReview + 人裁后补写），不是实时直写 |
| 8 | `technology_hierarchy` | 技术层级 | technology→technology | — | 🔴 | — | 燕大无 technology TAG，自然无技术层级边。**P1 GAP** |
| 9 | `technology_influence` | 技术影响 | technology→technology | — | 🔴 | — | 同上。**P1 GAP** |
| 10 | **`publish`** | **发布** | **institution→policy** | **—** | **🔴** | **政策未实现** | 政策 TAG 不存在，所有政策相关边均无对应。**P0 GAP** |
| 11 | **`policy_relate`** | **政策关联** | **policy↔policy** | **—** | **🔴** | **政策未实现** | 同上。**P0 GAP** |
| 12 | **`policy_apply_to`** | **政策适用** | **policy→field/enterprise/person/institution** | **—** | **🔴** | **政策未实现** | 同上。**P0 GAP** |
| 13 | `dataset_link` | 数据集关联 | dataset↔dataset | — | 🔴 | — | dataset TAG 不存在，自然无数据集间关系。DataSource 是治理占位不是业务实体 |
| 14 | `about_topic` | 主题相关 | paper/patent/project/dataset→topic | `HAS_KEYWORD`（Paper→Keyword） | 🔶 | ✅ 已实现 | **仅覆盖 Paper**：HAS_KEYWORD 是 Paper→Keyword 的边（论文主题），但需求侧还要 patent→topic、project→topic、dataset→topic。Keyword ≠ topic 但语义最接近 |
| 15 | `event_link` | 事件关联 | event↔event；event→institution/person | — | 🔴 | — | 燕大 Event TAG 覆盖工商风险事件，且只有 INVOLVED_IN（Organization→Event）一条边，无事件间关联，无 Event→Person。需求侧的科创事件 + 事件关联完全不存在 |
| 16 | **`activity_link`** | **活动关联** | **activity→person/institution/dataset** | **—** | **🔴** | **activity TAG 不存在** | activity TAG 不存在，相关边自然全无。**P1 GAP** |
| 17 | `carrier_cooperate` | 载体协同 | innovation_carrier↔innovation_carrier；innovation_carrier→person/institution | — | 🔴 | innovation_carrier TAG 不存在 | 创新载体无独立 TAG，相关边自然全无。**P1 GAP** |

---

## 五、整体对齐判定汇总

### 5.1 实体对齐汇总

| 判定 | 数量 | 占比 | 详情 |
|---|---:|---:|---|
| ✅ 已对齐 | 7 | 50% | institution、paper、patent、project、person + 产业（隐式）+ 科研机构（隐式） |
| 🔶 部分对齐 | 5 | 36% | enterprise（混装无枚举）、technology、field、topic、event（语义不同） |
| 🔴 无对应 | 4 | 29% | **policy、activity、innovation_carrier、dataset** |

> 注：需求清单 14 实体中，7 个并入七要素，6 个不并入。上表按需求实体计 14 行。

### 5.2 关系对齐汇总

| 判定 | 数量 | 占比 | 详情 |
|---|---:|---:|---|
| ✅ 已对齐 | 1 | 6% | author_of |
| 🔶 部分对齐 | 6 | 35% | cooperate、belong、cite、participate、about_topic + service机构隶属（隐式） |
| 🔴 无对应 | 10 | 59% | **research、belong_to、technology_hierarchy、technology_influence、publish、policy_relate、policy_apply_to、dataset_link、event_link、activity_link、carrier_cooperate** |

### 5.3 燕大侧 33 EDGE 反向覆盖情况

> 燕大有的 33 条边中，需求侧直接用到的很少，大量边是燕大业务逻辑自带但需求清单未显式要求：

| 燕大边 | 需求侧映射 | 判定 |
|---|---|---|
| AUTHORED_BY | author_of | ✅ |
| COAUTHOR_WITH | cooperate | 🔶（缩小） |
| CITES | cite | 🔶（缩小） |
| HAS_KEYWORD | about_topic | 🔶（缩小） |
| AFFILIATED_WITH + STUDIED_AT | belong | 🔶（缩小） |
| LEADS + HAS_PARTICIPANT | participate | 🔶（覆盖 Person 段） |
| PUBLISHED_IN | —（需求侧无论文→期刊关系） | 燕大独有 |
| REFERENCED_BY | —（需求侧无论文→报告关系） | 燕大独有 |
| MEMBER_OF_FAMILY | —（需求侧无专利同族） | 燕大独有 |
| INVENTED_BY / APPLIED_BY / OWNED_BY | author_of 覆盖了 INVENTED_BY | 部分覆盖 |
| OUTPUT_OF / HAS_OUTPUT | —（需求侧无项目→成果关系） | 燕大独有 |
| CHILD_OF / HAS_NODE / COVERS_CHAIN | —（产业域边，需求清单未涉及） | 燕大独有 |
| BELONGS_TO_NODE | —（企业→产业节点，需求清单未涉及） | 燕大独有 |
| SUBSIDIARY_OF / INVESTS_IN / ACQUIRES | —（企业工商治理边） | 燕大独有 |
| LEGAL_REP_OF / EXECUTIVE_OF / SHAREHOLDER_OF | —（企业治理边） | 燕大独有 |
| PRODUCES / HAS_NEWS / INVOLVED_IN | —（企业运营/事件边） | 燕大独有 |
| 其余 | — | 燕大独有 |

---

## 六、已知对齐难点备忘

> 这些难点在 L03/L04/L05 中必须诚实保留，不得强行对齐。

| # | 难点 | 影响范围 | 应对策略 |
|---|---|---|---|
| 1 | **Organization 三要素混装** | enterprise / institution / 服务机构 | institution 靠 org_kind 两值枚举区分（有效）；enterprise 和服务机构无法区分（org_kind 无专属值）。L03/L04 中必须分别标注「有效 / 无效」 |
| 2 | **Policy 完全空白** | policy 实体 + publish / policy_relate / policy_apply_to 三条关系 | 燕大快照明确标注「蓝图+源表已备」。**P0 GAP**，需要燕大补建 Policy TAG |
| 3 | **Event 语义错位** | event 实体 | 燕大 Event TAG = 工商风险事件（融资、处罚、诉讼、失信）。需求侧 event = 科创事件（论坛、发布会、签约）。**同名异义** |
| 4 | **technology ↔ Keyword 边界不同** | technology / field / topic 三实体 + technology_hierarchy / technology_influence / belong_to 三条关系 | Keyword 覆盖论文/专利/项目关键词（237,552 词），但不等价于技术点/技术领域/研究主题。L03 中不能把 Keyword 当成 technology 已覆盖 |
| 5 | **activity / innovation_carrier 不存在** | 2 实体 + 2 关系（activity_link / carrier_cooperate） | 完全空白，**P1 GAP** |
| 6 | **燕大 33 EDGE 中大量是业务逻辑自带** | 整个关系域 | 需求侧 17 关系 vs 燕大 33 EDGE 不是 1:1 映射关系。燕大的工商治理边、产业域边、论文域细节边（PUBLISHED_IN / REFERENCED_BY / MEMBER_OF_FAMILY 等）需求清单未要求，但这些边在展示系统侧可能被隐式使用（如企业页展示法律代表人、股东等） |

---

## 七、与 KG-YANDA-GAP-L01 v1.1 的关系

> **重要**：本文件与 `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/GAP-展示系统图谱需求GAP差集分析.md`（v1.1）是**两份独立文档**。

| 维度 | KG-YANDA-GAP-L01 v1.1（旧） | 本文件（L02 对齐轴） |
|---|---|---|
| 用途 | 算法中台 + 燕大已有 vs 需求清单的 GAP 差集 | 纯对齐，不做差集 |
| 减数来源 | 算法中台 cfg_metric seed 文件 + 燕大快照 | 仅燕大快照 |
| 粒度 | 实体/关系/属性/计算能力/写入接口 全五级 | 仅实体 + 关系 |
| 后续影响 | 独立文档，不被 L03/L04/L05 引用 | L03/L04/L05 的前置依赖 |
| 任务声明 | — | L05 note 明确：「**GAP = 需求清单 −（L03 已实现 ∪ L04 已实现）。KG-YANDA-GAP-L01 的 v1.1 只作草稿，不沿用其覆盖结论**」 |

---

## 八、后续依赖链

```
本文件 (L02 对齐轴) ── 已完成
  │
  ├──→ L03 算法中台各要素上图台账 (depends_on L02, status: backlog)
  │     用本对齐轴的实体/关系做减数基准
  │     注意：L03 只认「已实现」(代码入口)，指标 seed 与 D4 mock 不算已实现
  │
  └──→ L04 燕大七要素上图对照 (depends_on L02, 可与 L03 并行, status: backlog)
        用本对齐轴的实体/关系做对照表基准
        注意：L04 只对照 2026-10-26 燕大快照，不改快照原文
        │
        └──→ L05 需求减去已实现的 GAP (depends_on L03 + L04, status: backlog)
              ⚠ 明确声明：不沿用 KG-YANDA-GAP-L01 v1.1 的覆盖结论
              输出路径：对接文档/我方/SYSINT-SCHEME-07-L05-需求减已实现GAP.md
```

---

## 九、输入材料索引

| 材料 | 路径 | 版本 |
|---|---|---|
| 燕大七要素现状快照 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/对端/2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md` | 2026-10-26 |
| 致燕大需求清单 v1.0 | `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` | v1.0（发燕大版） |
| WBS-07 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS.md` | 2026-10-26 |
| GAP v1.1（仅作草稿不沿用） | `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/GAP-展示系统图谱需求GAP差集分析.md` | v1.1 |
