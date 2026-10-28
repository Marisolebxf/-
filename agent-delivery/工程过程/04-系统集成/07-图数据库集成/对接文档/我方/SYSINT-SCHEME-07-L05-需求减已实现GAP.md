# SYSINT-SCHEME-07-L05 · 需求减去已实现的图谱 GAP

## 一、差集公式与口径

### 1.1 差集公式

```
GAP = 需求清单 v1.0 − (L03 算法中台 ✅已实现 ∪ L04 燕大侧 ✅已实现)
```

### 1.2 减数范围（严格 DoD）

| 项 | L03（算法中台） | L04（燕大侧） | 说明 |
|---|---|---|---|
| **实体 TAG** | 3 要素 ✅ | 5 要素 ✅ | L03 产业/企业/服务机构；L04 产业/企业/技术/人才/科研机构 |
| **关系 EDGE** | 产业 4 + 企业 7 + 服务机构 2 条 | 33 条（17 TAG 配套） | L04 燕大 EDGE 覆盖更广 |
| **属性** | ❌ L03 不覆盖 | ⚠️ L04 快照有 867 属性定义但需求清单属性未逐条映射 | 属性层 GAP 主要在"需求字段 vs 燕大属性是否能对上" |
| **计算能力** | ❌ L03 不覆盖（cfg_metric 全 mock） | ⚠️ L04 有 9 推理服务接口 + nGQL 控制台 + PageRank/Louvain/Degree 真实已跑通 | 计算能力 GAP 主要看燕大 31 项能否覆盖 |
| **写入接口** | ✅ nebula_loader.py 有 ensure_schema + _insert_vertices/_insert_edges | ✅ Schema 管理 API + 动态置信度 + 人工审核队列 + 版本隔离 | 写入接口是唯一可能 100% 覆盖的层 |

### 1.3 关键边界

| 边界 | 处理 |
|---|---|
| 人才/科研机构 L03 侧 | 🔶 代码路径存在但**久新数据是否灌入 PG 未验证**，**暂不入减数** |
| `technology`（技术点）与七要素「技术」区分 | 需求实体 `technology` 是**技术点/技术方向/技术领域下的具体技术**（含层级关系与发展状态），与七要素「技术」=论文/专利/项目**不是同一事物**；数据由**久新供数**；L03/L04 均无该 TAG，**不入减数** |
| 两侧 TAG/EDGE 命名不同 | 通过 L02 对齐轴统一到需求清单口径再做差 |
| 不沿用 KG-YANDA-GAP-L01 v1.1 | v1.1 只作草稿，本文件独立判定 |
| 每行归堆 | 必填列：对端缺口 / 第06项 Graph / 第07项读图 / 在途 |

### 1.4 三系统命名统一映射表

| 需求实体 | 七要素 | 算法中台 TAG（L03） | 燕大 TAG（L04） | L02 对齐判定 |
|---|---|---|---|---|
| `enterprise` | 企业 | `enterprise`（nebula_loader） | `Organization`（默认桶混装） | 🔶 |
| `institution` | 科研机构 | `institution`（graph_project 端点）+ `research`（nebula_loader） | `Organization`（org_kind 枚举区分） | ✅ |
| `person` | 人才 | `talent`（nebula_loader，🔶暂不入） | `Person` + `ScholarOrganization` | ✅ |
| `paper` | 技术 | ❌ 无（燕大侧负责） | `Paper` + `Journal` | ✅ |
| `patent` | 技术 | ❌ 无 | `Patent` + `PatentFamily` | ✅ |
| `project` | 技术 | ❌ 无 | `Project` | ✅ |
| `technology` | 技术点/技术方向（≠七要素「技术」=论文；久新供数） | ❌ 无 | ❌ 无 `Technology` TAG（最接近 `Keyword`，语义不同） | 🔶 |
| `field` | 不并进七要素 | ❌ 无 | 最接近 `Keyword`（语义不同） | 🔶 |
| `topic` | 不并进七要素 | ❌ 无 | 最接近 `Keyword`（语义不同） | 🔶 |
| `policy` | 政策 | ❌ 两侧都不写 | ❌ 无（蓝图已备） | 🔴 |
| `dataset` | 不并进七要素 | ❌ 无 | ❌ 无（DataSource 是治理占位） | 🔴 |
| `event` | 不并进七要素 | ❌ 无 | `Event`（工商风险事件，语义错位） | 🔶 |
| `activity` | 不并进七要素 | ❌ 无 | ❌ 无 | 🔴 |
| `innovation_carrier` | 不并进七要素 | ❌ 无 | ❌ 无 | 🔴 |

### 1.5 归堆分类定义

| 归堆 | 含义 | 典型触发条件 |
|---|---|---|
| **对端缺口** | 燕大侧明确不覆盖、未实现或接口形态不匹配 | Policy TAG 未建、11 条关系无对应、31 计算能力中部分未提供 |
| **第06项 Graph** | 智树算法中台侧的图能力可补齐 | 产业/企业/服务机构已有写图路径可复用扩写；cfg_metric 指标可对接图计算 |
| **第07项读图** | 数据供给层缺失（不在图谱侧） | 久新人才/科研机构/**技术点**数据未灌入 PG；主题库/数据集/事件数据需数据接入 |
| **在途** | 已知在排期、有明确依赖未满足、或状态不明确 | 久新数据供给排期未给、燕大清单回复未收到、时序快照可行性未评估 |

---

## 二、实体类型 GAP（14 类）

| # | 需求实体 | 七要素 | L03 ✅ | L04 ✅ | GAP 判定 | 归堆 | 说明 |
|---|---|---|---|---|---|---|---|
| 1 | `enterprise` | 企业 | ✅ enterprise TAG | ✅ Organization 默认桶 | ⚠️ 部分覆盖 | 第06项Graph | 两侧都写，但燕大混装无专属枚举；智树 TAG 独立 |
| 2 | `institution` | 科研机构 | 🔶暂不入（代码有但数据未验证） | ✅ Organization + org_kind | ⚠️ 燕大侧覆盖 | 在途 | 智树侧是否独立写 institution 端点取决于产业链数据供给 |
| 3 | `person` | 人才 | 🔶暂不入（代码有但数据未验证） | ✅ Person + ScholarOrganization | ⚠️ 燕大侧覆盖 | 在途 | 智树 nebula_loader TAG 含 talent，但久新数据未灌入 PG |
| 4 | `paper` | 技术 | ❌ | ✅ Paper + Journal | ✅ 已覆盖 | — | 燕大侧完全覆盖 |
| 5 | `patent` | 技术 | ❌ | ✅ Patent + PatentFamily | ✅ 已覆盖 | — | 燕大侧完全覆盖 |
| 6 | `project` | 技术 | ❌ | ✅ Project | ✅ 已覆盖 | — | 燕大侧完全覆盖 |
| 7 | `technology` | 技术点/技术方向 | ❌ | ❌（Keyword 语义不同） | 🔴 **GAP** | 第07项读图 | 技术点、技术方向、技术领域下的具体技术，含层级关系与发展状态；数据由**久新供数**，供给层未到位；燕大无 Technology TAG，智树亦无该 TAG |
| 8 | `field` | 不并进七要素 | ❌ | ❌（Keyword 语义不同） | 🔴 **GAP** | 对端缺口 | 学科领域 vs 关键词；燕大无 Field TAG |
| 9 | `topic` | 不并进七要素 | ❌ | ❌（Keyword 语义不同） | 🔴 **GAP** | 对端缺口 | 主题库/主题分类 vs 论文关键词；边界不同 |
| 10 | `policy` | 政策 | ❌ | ❌（蓝图已备无 TAG） | 🔴 **GAP** | 对端缺口 | **P0 GAP**：两侧都不写，燕大蓝图+源表已备但 Policy TAG 未建 |
| 11 | `dataset` | 不并进七要素 | ❌ | ❌（DataSource 是治理占位） | 🔴 **GAP** | 对端缺口 | 无业务实体 TAG |
| 12 | `event` | 不并进七要素 | ❌ | ❌（Event 是工商风险事件，语义错位） | 🔴 **GAP** | 对端缺口 | 科创事件 vs 工商风险事件；同名异义 |
| 13 | `activity` | 不并进七要素 | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 完全不存在 |
| 14 | `innovation_carrier` | 不并进七要素 | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 完全不存在 |

### 实体 GAP 汇总

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 两侧覆盖（含一侧明确覆盖） | 7 | enterprise、institution、person、paper、patent、project + 隐式产业（chain/segment） |
| 🔴 **GAP（L03/L04 两侧都不写）** | **7** | policy（P0）、technology（久新供数）、field、topic、dataset、event（语义错位）、activity、innovation_carrier |

> **注**：enterprise/institution/person 虽两侧都写，但 TAG 命名/属性覆盖/枚举区分各有差距，未完全等价覆盖。

---

## 三、关系类型 GAP（17 类）

| # | 需求关系 | 起→终 | L03 ✅ | L04 ✅ | GAP 判定 | 归堆 | 说明 |
|---|---|---|---|---|---|---|---|
| 1 | `cooperate` | person↔person；institution↔institution；person↔institution | ❌ | ❌（需三态回复） | 🔴 **GAP** | 对端缺口 | 燕大 17 种 EDGE 无 cooperate；智树 nebula_loader 有 research_coop（科研机构内）和 talent_coop（人才内），但需求跨三类主体 |
| 2 | `belong` | person→institution；institution→institution（上级） | ❌ | ⚠️ 近似 AFFILIATED_WITH | 🔶 **部分覆盖** | 第06项Graph | 燕大 AFFILIATED_WITH 只覆盖 person→org；智树无直接 belong |
| 3 | `research` | person→field；person→topic；institution→field；enterprise→field | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 两侧都无研究关系 EDGE；依赖 technology/field/topic 实体先存在 |
| 4 | `cite` | paper→paper；patent→paper；patent→patent | ❌ | ✅ CITES | ✅ 已覆盖 | — | 燕大 CITES EDGE 完全覆盖 |
| 5 | `participate` | person→project；institution→project | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 两侧都无参与 EDGE；依赖 project + person/institution 实体先存在 |
| 6 | `belong_to` | paper/patent/project/technology→field | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 两侧都无归属到领域的 EDGE；依赖 field 实体先存在 |
| 7 | `author_of` | person→paper/patent | ❌ | ✅ AUTHORED_BY | ✅ 已覆盖 | — | 燕大 AUTHORED_BY 完全覆盖 |
| 8 | `technology_hierarchy` | technology→technology | ❌ | ❌ | 🔴 **GAP** | 第07项读图 | 依赖 technology 实体先存在（GAP #7）；层级关系由**久新供数**随技术点本体下发，不由图谱侧计算 |
| 9 | `technology_influence` | technology→technology | ❌ | ❌ | 🔴 **GAP** | 第06项Graph | 依赖 technology 实体先存在；影响关系需由引文/专利共现计算，智树图能力可承接 |
| 10 | `publish` | institution→policy | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 policy 实体先存在（P0 GAP） |
| 11 | `policy_relate` | policy↔policy | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 policy 实体先存在 |
| 12 | `policy_apply_to` | policy→field/enterprise/person/institution | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 policy 实体先存在 |
| 13 | `dataset_link` | dataset↔dataset | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 dataset 实体先存在 |
| 14 | `about_topic` | paper/patent/project/dataset→topic | ❌ | ❌（近似关键词挂载） | 🔶 **部分覆盖** | 第06项Graph | 燕大 INVENTED_BY/APPLIED_BY/OWNED_BY 挂实体改道近似，但语义不同 |
| 15 | `event_link` | event↔event；event→institution/person | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 event 实体先存在 |
| 16 | `activity_link` | activity→person/institution/dataset | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 activity 实体先存在 |
| 17 | `carrier_cooperate` | innovation_carrier↔innovation_carrier；carrier→person/institution | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 innovation_carrier 实体先存在 |

### 关系 GAP 汇总

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 两侧覆盖 | **2** | cite（CITES）、author_of（AUTHORED_BY） |
| 🔶 部分覆盖 | **2** | belong（近似 AFFILIATED_WITH）、about_topic（近似关键词挂载） |
| 🔴 **GAP** | **13** | cooperate、research、participate、belong_to、technology_hierarchy、technology_influence、publish、policy_relate、policy_apply_to、dataset_link、event_link、activity_link、carrier_cooperate |

---

## 四、属性 GAP（99 条）

> **方法说明**：属性层 GAP 判定比实体/关系更复杂——需要同时匹配「字段名/类型/必选/语义」四个维度。L04 快照记录了 867 条属性定义，但未与需求清单逐条映射。以下判定基于 L02 对齐轴的实体匹配 + L04 属性概述进行。

### 4.1 公共属性（10 条，适用全部实体）

| 属性 | 中文名 | 燕大是否覆盖 | 判定 | 归堆 |
|---|---|---|---|---|
| `entity_id` | 实体唯一标识 | ✅ 燕大 vid 稳定可关联 | ✅ | — |
| `name` | 实体名称 | ✅ | ✅ | — |
| `type` | 实体类型编码 | ✅ | ✅ | — |
| `field` | 所属领域 | ⚠️ 部分实体有，部分无 | 🔶 | 对端缺口 |
| `region` | 所属地域 | ⚠️ 部分实体有 | 🔶 | 对端缺口 |
| `institution` | 所属机构 | ⚠️ 取决于实体 | 🔶 | 对端缺口 |
| `author` | 作者/负责人 | ⚠️ | 🔶 | 对端缺口 |
| `year` | 实体年份 | ✅ | ✅ | — |
| `value` | 实体度量值 | ❌ 燕大无通用 value 属性 | 🔴 | 对端缺口 |
| `updated_at` | 数据更新时间 | ✅ | ✅ | — |

**公共属性小结**：5✅ / 4🔶 / 1🔴（精确映射见附录 A.1）

### 4.2 实体专有属性（68 条）

> 按实体 GAP 状态分组统计。**🔴 GAP 实体**的属性天然继承 GAP（实体不存在则属性无从挂载）。覆盖实体属性需逐条映射，括号内数字为 ✅/🔶/🔴。

| 实体 | 属性数 | 实体状态 | 属性 GAP 判定 | 归堆 | 详细映射 |
|---|---:|---|---|---|---|
| `technology` | 9 | 🔴 GAP | 🔴 **9/9 全 GAP** | 第07项读图 6（展示类）/ 第06项Graph 3（计算类） | 附录 A.3 |
| `field` | 7 | 🔴 GAP | 🔴 **7/7 全 GAP** | 对端缺口 | — |
| `topic` | 7 | 🔴 GAP | 🔴 **7/7 全 GAP** | 对端缺口 | — |
| `policy` | 6 | 🔴 GAP | 🔴 **6/6 全 GAP** | 对端缺口 | — |
| `enterprise` | 3 | ⚠️ 部分覆盖 | ✅1 / 🔶2（research_fields ✅；overlap_score/overlap_peer_id 需图谱计算） | 第06项Graph | 附录 A.2.1 |
| `institution` | 2 | ⚠️ 部分覆盖 | ✅1 / 🔶1（institution_type ✅；centrality_score 需图谱计算） | 第06项Graph | 附录 A.2.2 |
| `person` | 6 | ⚠️ 燕大侧覆盖 | ✅1 / 🔶4 / 🔴1（research_fields ✅；team 完全不存在；其余需图谱计算或反向聚合） | 对端缺口+第06项Graph | 附录 A.2.3 |
| `paper` | 3 | ✅ 已覆盖 | ✅1 / 🔶2（topic_keywords ✅；citation_count/reference_count 需遍历 CITES 计算） | 对端缺口 | 附录 A.2.4 |
| `patent` | 2 | ✅ 已覆盖 | ✅2（citation_count ✅ 有 citation_nums+cited_by_nums；topic_keywords ✅ 有 keywords 列） | — | 附录 A.2.5 |
| `project` | 3 | ✅ 已覆盖 | ✅1 / 🔶2（project_type ✅ 可由 project_source+level 映射；fusion_score/rank 需图谱计算） | 第06项Graph | 附录 A.2.6 |
| `dataset` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 | — |
| `event` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 | — |
| `activity` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 | — |
| `innovation_carrier` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 | — |

### 4.3 关系属性（21 条）

> 映射结果见附录 A.4。

| 分类 | 属性数 | ✅ | 🔶 | 🔴 | 归堆 | 说明 |
|---|---:|---:|---:|---:|---|---|
| 全部关系通用 | 11 | 6 | 5 | 0 | 对端缺口 | relation_id/source/target/type/updated_at/confidence ✅；weight/year/start_time/end_time/evidence_refs 🔶 |
| 关系专属 | 10 | 0 | 0 | 10 | 对端缺口 | 9 条因关系本身 GAP 天然 GAP；1 条 cite.citation_context 关系存在但属性不存在 |

### 4.4 属性 GAP 汇总（精确值 · 附录 A 映射结果）

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 完全覆盖 | **18** | 公共 5（entity_id/name/type/year/updated_at）+ 覆盖实体专有 7（enterprise.research_fields / institution.institution_type / person.research_fields / paper.topic_keywords / patent.citation_count+topic_keywords / project.project_type）+ 关系通用 6（relation_id/source/target/type/updated_at/confidence） |
| 🔶 部分覆盖 | **20** | 公共 4（field/region/institution/author）+ 覆盖实体专有 11（enterprise 2 + institution 1 + person 4 + paper 2 + project 2）+ 关系通用 5（weight/year/start_time/end_time/evidence_refs） |
| 🔴 **GAP** | **61** | 公共 1（value）+ 覆盖实体专有 1（person.team）+ GAP 实体全部 49（technology 9/field 7/topic 7/policy 6/dataset 5/event 5/activity 5/innovation_carrier 5）+ 关系专属 10（9 条因关系 GAP、cite.citation_context 关系存在但属性不存在） |

> **映射方法**：逐条对照燕大快照第二章实体属性清单 + 第三章关系属性，与需求清单第四章属性定义做字段级匹配。「需图谱侧计算」属性若燕大未预置则判 🔶（可通过第06项 Graph 能力补齐）。详见附录 A。

---

## 五、计算能力 GAP（31 项）

> **方法说明**：计算能力全部是图谱侧产物。L04 燕大快照记录有 9 推理服务接口 + nGQL 控制台 + PageRank/Louvain/Degree 真实已跑通。L03 cfg_metric 580 条全 mock。以下判定基于 L04 概述 + 需求清单接口描述。

| # | 能力ID | 能力名 | 燕大侧覆盖 | 判定 | 归堆 | 说明 |
|---|---|---|---|---|---|---|
| 1 | C-01 | 图谱动态查询与切片 | ✅ nGQL 控制台 | ✅ | — | 基础查询 |
| 2 | C-02 | 实体详情查询 | ✅ FETCH PROP ON | ✅ | — | 基础查询 |
| 3 | C-03 | 邻接实体 TopN | ✅ 展开函数 + ORDER BY | ✅ | — | 基础查询 |
| 4 | C-04 | 多条件图过滤 | ✅ WHERE + FILTER | ✅ | — | 基础查询 |
| 5 | C-05 | 子图切片与聚合 | ⚠️ 需组合 | 🔶 | 对端缺口 | 无现成聚合接口 |
| 6 | C-06 | 路径搜索（BFS/DFS/Dijkstra/…） | ✅ nGQL 路径函数 | ✅ | — | 基础查询 |
| 7 | C-07 | 关键路径与关键节点识别 | ⚠️ 需 PageRank + 路径 | 🔶 | 第06项Graph | 智树算法中台 PageRank 已跑通，可对接 |
| 8 | C-08 | 度中心性 | ✅ Degree 真实已跑通 | ✅ | — | 燕大已跑通 |
| 9 | C-09 | 紧密中心性 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 10 | C-10 | 中介中心性 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 11 | C-11 | PageRank | ✅ 真实已跑通 | ✅ | — | 燕大已跑通 |
| 12 | C-12 | 中心性综合评分与相关分析 | ⚠️ 需 C-09/C-10 | 🔴 | 对端缺口 | 依赖未实现的中心性 |
| 13 | C-13 | 中心性时序趋势 | ❌ 无快照能力 | 🔴 | 对端缺口 | **P0 GAP**：依赖图谱时序快照 |
| 14 | C-14 | 社群发现（Louvain/模块度/…） | ✅ Louvain 真实已跑通 | ✅ | — | 燕大已跑通 |
| 15 | C-15 | 社群属性与社群间矩阵 | ⚠️ 需 C-14 产物后处理 | 🔶 | 对端缺口 | — |
| 16 | C-16 | 社群动态演化追踪 | ❌ 无时序快照 | 🔴 | 对端缺口 | **P0 GAP**：依赖图谱时序快照 |
| 17 | C-17 | 图模式识别与异常点检测 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 18 | C-18 | 图聚类 | ⚠️ Louvain 近似 | 🔶 | 对端缺口 | — |
| 19 | C-19 | 图推荐与链路预测 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 20 | C-20 | 趋势预测 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 21 | C-21 | 实体影响力赋分与传播 | ⚠️ PageRank + 自实现 | 🔶 | 第06项Graph | 可基于 PageRank 扩展 |
| 22 | C-22 | 图谱指标监测与风险链 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 23 | C-23 | 指标融合、综合评分与一致性检验 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 24 | C-24 | 动态指标学习与模型迭代 | ❌ 未提及 | 🔴 | 对端缺口 | — |
| 25 | C-25 | 企业研究领域重叠度 | ❌ 未提及 | 🔴 | 第06项Graph | 可基于智树算法中台企业域能力扩展 |
| 26 | C-26 | 主题演化分析 | ❌ 无时序快照 | 🔴 | 对端缺口 | **P0 GAP**：依赖图谱时序快照 |
| 27 | C-27 | 协同网络绩效与影响力评估 | ⚠️ 需多能力组合 | 🔶 | 第06项Graph | — |
| 28 | C-28 | 数据集关联分析 | ❌ dataset 实体 GAP | 🔴 | 对端缺口 | dataset 实体不存在 → 天然 GAP |
| 29 | C-29 | 活动-资源-专家关联与推荐 | ❌ activity 实体 GAP | 🔴 | 对端缺口 | activity 实体不存在 → 天然 GAP |
| 30 | C-30 | 图快照与多格式导出 | ✅ 燕大可视化 + 子图探索 | ✅ | — | 燕大独有能力 |
| 31 | C-31 | 自定义实体/关系建模 | ✅ Schema 管理 API | ✅ | — | 燕大独有能力 |

### 计算能力 GAP 汇总

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 已覆盖 | **10** | C-01/02/03/04/06/08/11/14/30/31 |
| 🔶 部分覆盖 | **6** | C-05/07/15/18/21/27 |
| 🔴 **GAP** | **15** | C-09/10/12/13/16/17/19/20/22/23/24/25/26/28/29 |

---

## 六、写入接口 GAP（10 项）

> **方法说明**：写入接口是唯一可能 100% 覆盖的层。燕大 Schema 管理 API + 图谱构建编排 + 动态置信度 + 人工审核队列已就绪。L03 nebula_loader.py 有 ensure_schema + 批量写入能力。

| # | 接口 | 方法 | L03 ✅ | L04 ✅ | 判定 | 归堆 |
|---|---|---|---|---|---|---|
| 1 | `/v1/graph/entities` POST | 实体新增（支持批量） | ✅ `_insert_vertices` 批量 | ✅ Schema 管理 API | ✅ 已覆盖 | — |
| 2 | `/v1/graph/entities` PUT | 实体属性更新 | ✅ upsert 覆盖 | ✅ Schema 管理 API | ✅ 已覆盖 | — |
| 3 | `/v1/graph/entities` DELETE | 实体删除（级联删关系） | ✅ `DELETE VERTEX WITH EDGE`（incremental.py） | ⚠️ 未确认级联 | 🔶 部分覆盖 | 在途 |
| 4 | `/v1/graph/relations` POST | 关系新增 | ✅ `_insert_edges` | ✅ Schema 管理 API | ✅ 已覆盖 | — |
| 5 | `/v1/graph/relations` PUT | 关系属性更新 | ✅ upsert 覆盖 | ✅ Schema 管理 API | ✅ 已覆盖 | — |
| 6 | `/v1/graph/relations` DELETE | 关系删除 | ⚠️ 未确认 | ⚠️ 未确认 | 🔶 部分覆盖 | 在途 |
| 7 | `/v1/graph/entities:batch-import` | 多源数据批量导入 | ✅ nebula_loader run() | ✅ 图谱构建编排 | ✅ 已覆盖 | — |
| 8 | `/v1/graph/versions` POST | 图谱版本创建 | ❌ | ✅ 多 graph-space 版本隔离（18 个） | ✅ 已覆盖 | — |
| 9 | `/v1/graph/versions` GET | 图谱版本列表/回滚 | ❌ | ✅ 版本隔离 | ✅ 已覆盖 | — |
| 10 | `/v1/graph/audit-logs` GET | 写操作日志/撤销重做 | ❌ | ✅ 人工审核队列 + 动态置信度 | ✅ 已覆盖 | — |

### 写入接口 GAP 汇总

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 已覆盖 | **8** | 新增/更新/关系新增/关系更新/批量导入/版本创建/版本列表/审计日志 |
| 🔶 部分覆盖 | **2** | 实体删除（级联）、关系删除（待确认） |
| 🔴 GAP | **0** | — |

---

## 七、全局 GAP 总览

### 7.1 五类 GAP 数字（属性已精确化）

| 类 | 需求侧 | ✅ 两侧覆盖 | 🔶 部分覆盖 | 🔴 GAP |
|---|---:|---:|---:|---:|
| 实体类型 | 14 | 7 | 0 | **7** |
| 关系类型 | 17 | 2 | 2 | **13** |
| 属性 | 99 | **18** | **20** | **61** |
| 计算能力 | 31 | **10** | **6** | **15** |
| 写入接口 | 10 | 8 | 2 | 0 |
| **合计** | **171** | **45** | **30** | **96** |

> **注**：属性层从粗估 ≈4/≈25/≈60 精确化为 18/20/61，详见第四章 4.4 和附录 A。

### 7.2 P0 / P1 GAP 分级

| 优先级 | 项 | GAP 内容 | 根因 | 归堆 |
|---|---|---|---|---|
| **P0** | Policy TAG | 燕大未建 Policy TAG，两侧都不写 | 燕大蓝图+源表已备但无代码 | 对端缺口 |
| **P0** | 政策 3 条关系 | publish / policy_relate / policy_apply_to | Policy TAG 不存在 → 依赖链断 | 对端缺口 |
| **P0** | 图谱时序快照 | C-13/C-16/C-26 三项计算能力依赖时序快照 | 燕大无快照能力 | 对端缺口 |
| **P1** | Activity TAG + activity_link | 燕大无 Activity TAG + 无关联关系 | 完全不存在 | 对端缺口 |
| **P1** | 图推荐 C-19 | 链路预测能力未提供 | — | 对端缺口 |
| **P1** | 13 条关系中除 2 已覆盖外的剩余 | cooperate / research / participate / belong_to / technology_hierarchy / technology_influence / dataset_link / event_link / carrier_cooperate | 依赖对应实体先存在 | 对端缺口 + 第06项Graph + 第07项读图 |
| **P1** | 6 个非七要素实体 | field / topic / dataset / event / innovation_carrier（**technology 另计**：久新供数 → 第07项读图 + 第06项Graph） | 部分语义错位、部分完全不存在 | 对端缺口 + 第07项读图 |

### 7.3 燕大独有能力（L03/L05 可直接复用）

| 能力 | 来源 | 说明 |
|---|---|---|
| Schema 管理 API | L04 | 实体/关系增删改的完整 API 契约 |
| 动态置信度规约 | L04 | 0.40（源）+0.20（权威）+0.10（时效）+0.20（证据）+0.10（人工） |
| 13 条溯源属性 | L04 | 所有实体带 source/source_chain/source_confidence |
| 人工审核队列 | L04 | 图谱写入审核流 |
| 多 graph-space 版本隔离 | L04 | 18 个 graph-space，支持版本快照 |
| 9 推理服务接口 | L04 | 独立图谱推理 API |
| nGQL 控制台 + 图算法作业 | L04 | PageRank/Louvain/Degree 真实已跑通 |
| 图谱可视化 + 子图探索 | L04 | C-30 图快照导出 |

### 7.4 智树算法中台独有能力（L03 可直接扩写）

| 能力 | 来源 | 说明 |
|---|---|---|
| graph_project.py 产业链灌链 | L03 | 4 TAG + 4 EDGE，DWD 自产 |
| nebula_loader.py 通用灌图 | L03 | 5 TAG + 7 EDGE，PG→Nebula 批量 |
| incremental.py 增量双写 | L03 | PG+Nebula 幂等覆盖 |
| svcgraph.py 服务机构增量 | L03 | institution TAG + participates/belongs_to |

---

## 八、与 KG-YANDA-GAP-L01 v1.1 的关系

| 维度 | v1.1（前序草稿） | 本文件（L05） |
|---|---|---|
| 被减数 | 14 实体 + 17 关系 | 14 实体 + 17 关系 + 99 属性 + 31 计算 + 10 写入（五类全做） |
| 减数 | 仅燕大侧 + cfg_metric seed | L03（智树 ✅）∪ L04（燕大 ✅），两层都算 |
| 算法中台就绪度 | D4 全部 mock，定义存在但无真实代码 | 3 要素真实已跑通（产业/企业/服务机构），5 TAG 硬编码证据 |
| 人才/科研机构判定 | ❌ 未分析算法中台覆盖 | 🔶 代码路径存在但久新数据未验证，暂不入减数 |
| 政策判定 | 两侧都不写 | ✅ 一致确认（P0 GAP） |
| 不沿用 v1.1 覆盖结论 | — | ✅ 本文件独立判定 |

---

## 九、输入材料索引

| 材料 | 路径 | 版本 |
|---|---|---|
| 需求清单 v1.0 | `外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` | 2026-10-26 |
| L02 对齐轴 | `对接文档/我方/SYSINT-SCHEME-07-L02-对齐轴.md` | v1.0 |
| L03 算法中台上图台账 | `对接文档/我方/SYSINT-SCHEME-07-L03-算法中台上图台账.md` | v1.0（复核修正后） |
| L04 燕大七要素上图对照 | `对接文档/我方/SYSINT-SCHEME-07-L04-燕大七要素上图对照.md` | v1.0 |
| 七要素现状快照 | `对接文档/对端/2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md` | 2026-10-26 |
| KG-YANDA-GAP-L01 v1.1（不沿用） | `外部接口依赖/KG-YANDA-SCHEMA-REQ/GAP-展示系统图谱需求GAP差集分析.md` | v1.1（草稿） |
| WBS-07 | `WBS.md` | 2026-10-26 |

---

## 附录 A · 属性层精细映射（99 条逐条对照）

> **映射方法**：以「需求清单 v1.0 第四章属性定义」为被减数，逐条对照「燕大快照第二章实体属性清单 + 第三章关系属性」。判定规则：
> - ✅ 燕大有直接对应字段或可由 EDGE 聚合得到
> - 🔶 近似但有差距（需图谱计算、需反向聚合、非直取）
> - 🔴 完全找不到
> - 归堆列按 1.5 定义填写
> - **「需图谱侧计算」标记**：需求清单标注了约 17 条需图谱计算的属性，燕大未预置但可通过第06项 Graph 能力补齐 → 判 🔶

### A.1 公共属性（10 条，适用全部实体）

| # | 属性名 | 中文名 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|
| 1 | `entity_id` | 实体唯一标识 | 各 TAG 原生 vid | ✅ | — | 快照第二章每个实体显式 vid=xxx_{主键} |
| 2 | `name` | 实体名称 | name_cn/name_en（Organization）、name_zh/name_en（Person）、title_zh（Paper）、title（Project/Patent）、chain_name（IndustryChain）、node_name（IndustryNode） | ✅ | — | 每个实体 TAG 都有名称列 |
| 3 | `type` | 实体类型编码 | org_kind（Organization）、person_kind（Person）、edge_type（关系） | ✅ | — | org_kind 7 值枚举覆盖机构类型；person_kind 区分人员类型 |
| 4 | `field` | 所属领域 | organization.industry_class；person.research_fields；paper/patent/project.keywords | 🔶 | 对端缺口 | 部分实体有但非统一属性；Organization 有 industry_class，Person 有 research_fields，成果类可从关键词反向聚合 |
| 5 | `region` | 所属地域 | organization.province/city/country；person 国籍列 | 🔶 | 对端缺口 | 机构地域全，人员部分，成果类无 |
| 6 | `institution` | 所属机构 | person.scholar_org_id；organization 内联；论文域机构桩 | 🔶 | 对端缺口 | Person 有 scholar_org_id，其他实体需反向匹配 |
| 7 | `author` | 作者/负责人 | paper 作者表；patent.inventors/applicants；project.project_host | 🔶 | 对端缺口 | 仅成果类有，非通用 |
| 8 | `year` | 实体年份 | paper.publication_year；patent.publication_date→年份；project.approval_year | ✅ | — | 主要实体都有年份字段 |
| 9 | `value` | 实体度量值 | ❌ 无通用 value 属性 | 🔴 | 对端缺口 | 燕大属性都是具体业务字段，没有通用度量占位 |
| 10 | `updated_at` | 数据更新时间 | 平台公共治理列 updatetime | ✅ | — | 快照 1.3-② 说全部实体附 15 条公共治理列含 updatetime |

**公共属性小计**：✅5 / 🔶4 / 🔴1

---

### A.2 覆盖实体专有属性（7 个实体，19 条）

> 以下实体在第二章实体 GAP 判定为 ✅ 已覆盖或 ⚠️ 部分覆盖，逐条映射其需求属性。

#### A.2.1 enterprise · 企业（3 条）

> 燕大承载：Organization（默认桶混装，org_kind=domestic_organization 无专属枚举）

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `research_fields` | 研究领域列表 | 否 | Organization.industry_class | ✅ | — | 工商域 industry_class 列直接映射 |
| 2 | `overlap_score` | 研究领域重叠度 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 需基于两家企业的 industry_class/关键词集合计算 Jaccard/Dice 相似度；燕大无此预置但智树算法中台可扩展 |
| 3 | `overlap_peer_id` | 对比企业 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 依赖 overlap_score 排序选出对比对象；燕大无此属性 |

**enterprise 小计**：✅1 / 🔶2 / 🔴0

#### A.2.2 institution · 机构/科研机构（2 条）

> 燕大承载：Organization + org_kind（domestic_university / domestic_research_institute）

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `institution_type` | 机构类型 | 否 | Organization.org_kind | ✅ | — | org_kind 枚举可直接映射 institution_type |
| 2 | `centrality_score` | 中心性综合分 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 需 PageRank + 度 + 中介等合成；燕大 PageRank/Degree 已跑通可对接 |

**institution 小计**：✅1 / 🔶1 / 🔴0

#### A.2.3 person · 人员/专家（6 条）

> 燕大承载：Person + ScholarOrganization

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `research_fields` | 研究领域列表 | 否 | Person.research_fields | ✅ | — | 快照行 64 明确有 research_fields 列 |
| 2 | `research_topics` | 研究主题列表 | 否 | ❌ 无直取 | 🔶 | 对端缺口 | Person 有 research_fields 但无 research_topics；可从论文/专利/项目关键词反向聚合但非直取字段 |
| 3 | `team` | 所属团队 | 否 | ❌ 完全不存在 | 🔴 | 对端缺口 | Person TAG 无 team/研究团队相关字段 |
| 4 | `cooperation_degree` | 合作度 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 需基于 COAUTHOR_WITH + AFFILIATED_WITH 边数/合著篇数计算；燕大 COAUTHOR_WITH 有 co_paper_count 可复用 |
| 5 | `centrality_score` | 中心性综合分 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 需 PageRank + 度等合成；燕大 PageRank/Degree 已跑通 |
| 6 | `active_years` | 活跃年份区间 | 否 | ⚠️ 可从成果年份聚合 | 🔶 | 对端缺口 | 无直取属性；可从 Person 关联的 Paper.publication_year / Project.approval_year 取 min–max 推断 |

**person 小计**：✅1 / 🔶4 / 🔴1

#### A.2.4 paper · 论文（3 条）

> 燕大承载：Paper + Journal + Report

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `citation_count` | 被引次数 | **是** | ❌ 无预置 | 🔶 | 对端缺口 | CITES EDGE 存在（快照行 98）但 Paper TAG 无 citation_count 属性；需实时或离线遍历 CITES 边反向统计 |
| 2 | `reference_count` | 参考文献数 | **是** | ❌ 无预置 | 🔶 | 对端缺口 | 同上，需遍历 CITES 正向统计 |
| 3 | `topic_keywords` | 主题关键词 | 否 | HAS_KEYWORD EDGE 聚合 | ✅ | — | 快照行 99，论文-关键词边 HAS_KEYWORD 存在，可聚合为 topic_keywords 数组 |

**paper 小计**：✅1 / 🔶2 / 🔴0

#### A.2.5 patent · 专利（2 条）

> 燕大承载：Patent + PatentFamily

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `citation_count` | 被引次数 | **是** | Patent.citation_nums + cited_by_nums | ✅ | — | 快照行 72 富集绑定有 citation_nums（被引数）和 cited_by_nums（他引数）两字段 |
| 2 | `topic_keywords` | 主题关键词 | 否 | Patent.keywords | ✅ | — | 快照行 71 Patent A 基础绑定有 keywords 列 |

**patent 小计**：✅2 / 🔶0 / 🔴0

#### A.2.6 project · 项目（3 条）

> 燕大承载：Project

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `project_type` | 项目类型 | 否 | Project.project_source + project_level | ✅ | — | 快照行 75 有 project_source（项目来源）和 project_level（项目级别），可组合映射 project_type |
| 2 | `fusion_score` | 综合评分 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 需基于 funded_amount + 产出计数（10 类）+ evaluation 等多因子合成；燕大 Project 有 total_outputs 及 10 类产出计数可复用 |
| 3 | `rank` | 综合排名 | **是** | ❌ 无预置 | 🔶 | 第06项Graph | 依赖 fusion_score 排序；燕大无预置排名 |

**project 小计**：✅1 / 🔶2 / 🔴0

#### A.2.7 隐式产业（IndustryChain + IndustryNode）

> 需求清单无独立 industry 实体定义，L05 实体汇总中作为「隐式产业」入 ✅ 覆盖计数。燕大 IndustryChain 仅 2 属性（chain_code/chain_name）、IndustryNode 8 属性（node_id/node_name/node_type/level/node_seq/node_imp_level/node_stage/node_path），无需求侧属性映射需求。

**覆盖实体专有属性总计**：✅7 / 🔶11 / 🔴1

---

### A.3 GAP 实体专有属性（49 条，全部 🔴）

> 以下 8 个实体在第二章实体 GAP 判定为 🔴 GAP（两侧都不写或语义错位），实体不存在 → 属性无从挂载，全部 🔴。

| 实体 | 属性数 | 燕大承载 | 判定 | 归堆 | 说明 |
|---|---:|---|---|---|---|
| `technology` 技术点 | 9 | ❌ 无 Technology TAG（最接近 Keyword 语义不同） | 🔴 9/9 | 第07项读图 6 / 第06项Graph 3 | 数据由**久新供给**（同人才/科研机构）；`hierarchy_level`、`development_status`、`category`、`importance_level` 随本体下发；`innovation_score`/`innovation_rank`/`hotspot_flag` 需图谱计算 |
| `field` 领域 | 7 | ❌ 无 Field TAG（最接近 Keyword） | 🔴 7/7 | 对端缺口 | 学科领域分类体系未建模 |
| `topic` 主题 | 7 | ❌ 无 Topic TAG（最接近 Keyword） | 🔴 7/7 | 对端缺口 | 主题库 vs 关键词本体边界不同 |
| `policy` 政策 | 6 | ❌ Policy TAG 未建（蓝图+源表已备） | 🔴 6/6 | 对端缺口 | **P0 GAP**，两侧都不写 |
| `dataset` 数据集 | 5 | ❌ DataSource 是治理占位 | 🔴 5/5 | 对端缺口 | 无业务实体 TAG |
| `event` 科技事件 | 5 | ❌ Event TAG 存在但语义为工商风险事件 | 🔴 5/5 | 对端缺口 | 科创事件 vs 工商风险事件同名异义 |
| `activity` 科技活动 | 5 | ❌ 完全不存在 | 🔴 5/5 | 对端缺口 | 无活动类 TAG |
| `innovation_carrier` 创新载体 | 5 | ❌ 完全不存在 | 🔴 5/5 | 对端缺口 | 无载体类 TAG |

**GAP 实体专有属性总计**：🔴49

---

### A.4 关系属性（21 条）

#### A.4.1 通用关系属性（11 条，全部关系适用）

| # | 需求属性 | 中文名 | 需图谱计算 | 燕大对应字段 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | `relation_id` | 关系唯一标识 | 否 | Nebula EDGE src_vid + dst_vid + edge_type 组合 | ✅ | — | Nebula EDGE 三字段组唯一标识 |
| 2 | `source_entity_id` | 源实体 | 否 | Nebula 原生 src_vid | ✅ | — | EDGE 原生字段 |
| 3 | `target_entity_id` | 目标实体 | 否 | Nebula 原生 dst_vid | ✅ | — | EDGE 原生字段 |
| 4 | `type` | 关系类型编码 | 否 | edge_type | ✅ | — | Nebula EDGE 原生字段 |
| 5 | `weight` | 关系权重/强度 | **是** | 部分 EDGE 有（co_paper_count/ownership_percentage/inv_amount 等） | 🔶 | 对端缺口 | 不是所有 EDGE 都有 weight；需各 EDGE 单独适配或统一从置信度派生 |
| 6 | `year` | 关系年份 | 否 | 部分可从起止端点年份推断 | 🔶 | 对端缺口 | 无通用 year 属性；如 CITES 可从被引论文 publication_year 取 |
| 7 | `start_time` | 关系开始时间 | 否 | AFFILIATED_WITH 有 start_time；其他部分 EDGE 有 | 🔶 | 对端缺口 | 仅任职/教育类有显式时间；工商治理域部分有 |
| 8 | `end_time` | 关系结束时间 | 否 | AFFILIATED_WITH 有 end_time；其他部分有 | 🔶 | 对端缺口 | 同上 |
| 9 | `updated_at` | 关系更新时间 | 否 | 平台公共治理列 updatetime | ✅ | — | 快照 1.3-② 全部边附公共治理列 |
| 10 | `confidence` | 置信度 | **是** | ✅ 动态置信度规约 | ✅ | — | L05 7.3 确认 0.40+0.20+0.10+0.20+0.10 五维置信度模型 |
| 11 | `evidence_refs` | 证据引用 | 否 | ⚠️ 有 source/source_chain 但非标准 evidence_refs 数组 | 🔶 | 对端缺口 | 溯源属性存在但名称和结构不同；需适配转换 |

**通用关系属性小计**：✅6 / 🔶5 / 🔴0

#### A.4.2 关系专属属性（10 条，绑定到特定关系类型）

> 专属属性的存在前提是**对应关系先存在**。关系不存在 → 属性天然 GAP。

| # | 需求属性 | 绑定关系 | 中文名 | 关系状态 | 需图谱计算 | 判定 | 归堆 | 证据 |
|---|---|---|---|---|---|---|---|---|
| 1 | `cooperation_type` | `cooperate` | 合作类型 | 🔴 GAP | 否 | 🔴 | 对端缺口 | cooperate 关系两侧都不写（第二章关系 GAP #1），属性无从挂载 |
| 2 | `role` | `participate` | 参与角色 | 🔴 GAP | 否 | 🔴 | 对端缺口 | participate 关系 GAP（关系 GAP #5） |
| 3 | `citation_context` | `cite` | 引用语境 | ✅ CITES | 否 | 🔴 | 对端缺口 | CITES EDGE 存在但无 citation_context 属性；燕大引文只取 DOI/题名等标识，不存引用上下文 |
| 4 | `influence_type` | `technology_influence` | 影响类型 | 🔴 GAP | 否 | 🔴 | 第06项Graph | technology_influence 关系 GAP（关系 GAP #9）；影响类型随图谱计算侧一并产出 |
| 5 | `relation_type` | `policy_relate` | 政策关联类型 | 🔴 GAP | 否 | 🔴 | 对端缺口 | policy_relate 关系 GAP（关系 GAP #11） |
| 6 | `target_role` | `policy_apply_to` | 作用角色 | 🔴 GAP | 否 | 🔴 | 对端缺口 | policy_apply_to 关系 GAP（关系 GAP #12） |
| 7 | `link_type` | `dataset_link` | 数据集关联类型 | 🔴 GAP | 否 | 🔴 | 对端缺口 | dataset_link 关系 GAP（关系 GAP #13） |
| 8 | `read_count` | `activity_link` | 阅读量 | 🔴 GAP | 否 | 🔴 | 对端缺口 | activity_link 关系 GAP（关系 GAP #16） |
| 9 | `importance` | `activity_link` | 重要程度 | 🔴 GAP | **是** | 🔴 | 对端缺口 | activity_link 关系 GAP + 属性需图谱计算 |
| 10 | `relevance` | `activity_link` | 关联性 | 🔴 GAP | **是** | 🔴 | 对端缺口 | activity_link 关系 GAP + 属性需图谱计算 |

**专属关系属性小计**：🔴10（其中 9 条因关系不存在天然 GAP，1 条 cite.citation_context 关系存在但属性缺失）

**关系属性总计**：✅6 / 🔶5 / 🔴10

---

### A.5 属性层全局精确 GAP 总表

| 分类 | 条数 | ✅ | 🔶 | 🔴 |
|---|---:|---:|---:|---:|
| 公共属性 | 10 | 5 | 4 | 1 |
| 实体专有 · 覆盖实体 | 19 | 7 | 11 | 1 |
| 实体专有 · GAP 实体 | 49 | 0 | 0 | 49 |
| 关系属性 · 通用 | 11 | 6 | 5 | 0 |
| 关系属性 · 专属 | 10 | 0 | 0 | 10 |
| **合计** | **99** | **18** | **20** | **61** |

### A.6 需图谱侧计算属性汇总（≈17 条 · 全部 🔶 可补齐）

> 需求清单标注「需图谱侧计算」的属性，燕大未预置但可通过第06项 Graph 计算能力（PageRank / Louvain / Degree / 图匹配 / 相似度等）补齐。

| # | 需求属性 | 所属实体/关系 | 需计算的能力 | 燕大是否有底层能力 | 归堆 |
|---|---|---|---|---|---|
| 1 | `innovation_score` | technology | 多因子合成（被引、专利、合作） | 有 CITES + AUTHORED_BY 边 | 第06项Graph |
| 2 | `innovation_rank` | technology | innovation_score 排名 | 需 innovation_score 先有 | 第06项Graph |
| 3 | `hotspot_flag` | technology / field | 热度阈值判断 | 需热度计算 | 第06项Graph |
| 4 | `trend` | field / topic | 时序变化率 | ⚠️ 无时序快照（P0 GAP） | 对端缺口 |
| 5 | `cooperation_degree` | person | 合著/合作边数 + 合作强度 | 有 COAUTHOR_WITH 边含 co_paper_count | 第06项Graph |
| 6 | `centrality_score` | person / institution | PageRank + Degree + 中介合成 | PageRank/Degree 已跑通 | 第06项Graph |
| 7 | `citation_count` | paper / patent | 遍历 CITES 边反向计数 | CITES EDGE 存在；Patent 有预置 citation_nums | 第06项Graph |
| 8 | `reference_count` | paper | 遍历 CITES 正向计数 | CITES EDGE 存在 | 第06项Graph |
| 9 | `fusion_score` | project | funded_amount + 10类产出计数 + evaluation 合成 | Project 有 total_outputs + 10类产出计数 | 第06项Graph |
| 10 | `rank` | project | fusion_score 排名 | 需 fusion_score 先有 | 第06项Graph |
| 11 | `overlap_score` | enterprise | 两家企业行业标签 Jaccard/Dice 相似度 | 智树算法中台企业域可扩展 | 第06项Graph |
| 12 | `overlap_peer_id` | enterprise | overlap_score 排序选出 top-1 | 需 overlap_score 先有 | 第06项Graph |
| 13 | `heat` | topic | 提及频次 + 时间衰减 | 需 topic 实体先存在（🔴 GAP） | 对端缺口 |
| 14 | `related_policy_count` | policy | policy_relate 边数 | policy 实体 🔴 GAP | 对端缺口 |
| 15 | `joint_project_count` / `cooperation_density` / `synergy_score` / `talent_count` | innovation_carrier | 多因子合成 | carrier 实体 🔴 GAP | 对端缺口 |
| 16 | `weight`（通用关系） | 全部关系 | 各 EDGE 独立计算（合著篇数/持股比例等） | 部分 EDGE 已有 weight-like 属性 | 对端缺口 |
| 17 | `confidence`（通用关系） | 全部关系 | 动态置信度五维计算 | ✅ 燕大已有置信度模型 | — |
| 18 | `importance` / `relevance` | activity_link | 活动-专家关联度 | activity 实体 🔴 GAP | 对端缺口 |

### A.7 映射证据索引

| 证据 | 路径 | 用途 |
|---|---|---|
| 燕大实体属性清单 | `对接文档/对端/2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md` 第二章行 54-81 | A.2 各实体燕大对应字段判定 |
| 燕大关系属性清单 | 同上 第三章行 84-154 | A.4 关系属性判定 |
| 燕大公共治理列 | 同上 1.3-② 行 27 | entity_id/updated_at/confidence 等公共属性 |
| 燕大置信度模型 | L05 7.3 | confidence 属性来源 |
| 需求属性定义 | `外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` 第四章行 104-285 | 被减数基准 |
