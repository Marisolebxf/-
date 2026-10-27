# SYSINT-SCHEME-07-L05 · 需求减去已实现的图谱 GAP

> **任务**：`SYSINT-SCHEME-07-L05`（WBS-07-00D）
> **监管人 / 认领人**：human:郭万迎
> **完成日期要求**：2026-11-09（WBS-07-00 出门日）
> **创建时间**：2026-10-27

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
| `technology` | 不并进七要素 | ❌ 无 | 最接近 `Keyword`（语义不同） | 🔶 |
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
| **第07项读图** | 数据供给层缺失（不在图谱侧） | 久新人才/科研机构数据未灌入 PG；主题库/数据集/事件数据需数据接入 |
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
| 7 | `technology` | 不并进七要素 | ❌ | ❌（Keyword 语义不同） | 🔴 **GAP** | 对端缺口 | 技术点 vs 关键词是不同语义；燕大无 Technology TAG |
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
| 🔴 **GAP（两侧都不写）** | **7** | policy（P0）、technology、field、topic、dataset、event（语义错位）、activity、innovation_carrier |

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
| 8 | `technology_hierarchy` | technology→technology | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 technology 实体先存在（GAP #7） |
| 9 | `technology_influence` | technology→technology | ❌ | ❌ | 🔴 **GAP** | 对端缺口 | 依赖 technology 实体先存在 |
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

**公共属性小结**：4✅ / 4🔶 / 1🔴

### 4.2 实体专有属性（68 条）

> 按实体 GAP 状态分组统计。**🔴 GAP 实体**的属性天然继承 GAP（实体不存在则属性无从挂载）。

| 实体 | 属性数 | 实体状态 | 属性 GAP 判定 | 归堆 |
|---|---:|---|---|---|
| `technology` | 9 | 🔴 GAP | 🔴 **9/9 全 GAP** | 对端缺口 |
| `field` | 7 | 🔴 GAP | 🔴 **7/7 全 GAP** | 对端缺口 |
| `topic` | 7 | 🔴 GAP | 🔴 **7/7 全 GAP** | 对端缺口 |
| `policy` | 6 | 🔴 GAP | 🔴 **6/6 全 GAP** | 对端缺口 |
| `enterprise` | 3 | ⚠️ 部分覆盖 | 🔶 2/3 覆盖（overlap_score/overlap_peer_id 需图谱计算） | 对端缺口 |
| `institution` | 2 | ⚠️ 部分覆盖 | 🔶 1/2 覆盖（centrality_score 需图谱计算） | 对端缺口 |
| `person` | 6 | ⚠️ 燕大侧覆盖 | 🔶 3/6 覆盖（cooperation_degree/centrality_score 需图谱计算） | 对端缺口 |
| `paper` | 3 | ✅ 已覆盖 | 🔶 2/3 覆盖（citation_count/reference_count 需图谱计算） | 对端缺口 |
| `patent` | 2 | ✅ 已覆盖 | 🔶 1/2 覆盖（citation_count 需图谱计算） | 对端缺口 |
| `project` | 3 | ✅ 已覆盖 | 🔶 1/3 覆盖（fusion_score/rank 需图谱计算） | 对端缺口 |
| `dataset` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 |
| `event` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 |
| `activity` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 |
| `innovation_carrier` | 5 | 🔴 GAP | 🔴 **5/5 全 GAP** | 对端缺口 |

### 4.3 关系属性（21 条）

| 分类 | 属性数 | 判定 | 归堆 |
|---|---:|---|---|
| 全部关系通用（11 条） | 11 | 🔶 部分覆盖（燕大 EDGE 有 type/weight/start_time/end_time，但 relation_id/source/target/confidence/evidence_refs 是否全有未确认） | 在途 |
| 关系专属（10 条） | 10 | 🔶 部分覆盖（依赖关系 EDGE 先存在；如 cooperate 本身就是 GAP 则 cooperation_type 自然 GAP） | 对端缺口 |

### 4.4 属性 GAP 汇总

| 状态 | 数量 | 详情 |
|---|---:|---|
| ✅ 完全覆盖 | 4 | entity_id、name、type、year、updated_at（公共）+ 部分实体基础属性 |
| 🔶 部分覆盖 | ≈25 | 需图谱计算的指标属性（centrality_score/citation_count/overlap_score 等）+ 需映射的公共属性 |
| 🔴 **GAP** | **≈60** | 🔴 GAP 实体的全部属性（technology 9/field 7/topic 7/policy 6/dataset 5/event 5/activity 5/innovation_carrier 5 + value 公共属性） |

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
| ✅ 已覆盖 | **9** | C-01/02/03/04/06/08/11/14/30/31 |
| 🔶 部分覆盖 | **6** | C-05/07/15/18/21/27 |
| 🔴 **GAP** | **16** | C-09/10/12/13/16/17/19/20/22/23/24/25/26/28/29 |

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

### 7.1 五类 GAP 数字

| 类 | 需求侧 | ✅ 两侧覆盖 | 🔶 部分覆盖 | 🔴 GAP |
|---|---:|---:|---:|---:|
| 实体类型 | 14 | 7 | 0 | **7** |
| 关系类型 | 17 | 2 | 2 | **13** |
| 属性 | 99 | ≈4 | ≈25 | **≈60** |
| 计算能力 | 31 | 9 | 6 | **16** |
| 写入接口 | 10 | 8 | 2 | 0 |
| **合计** | **171** | **≈30** | **≈35** | **≈96** |

### 7.2 P0 / P1 GAP 分级

| 优先级 | 项 | GAP 内容 | 根因 | 归堆 |
|---|---|---|---|---|
| **P0** | Policy TAG | 燕大未建 Policy TAG，两侧都不写 | 燕大蓝图+源表已备但无代码 | 对端缺口 |
| **P0** | 政策 3 条关系 | publish / policy_relate / policy_apply_to | Policy TAG 不存在 → 依赖链断 | 对端缺口 |
| **P0** | 图谱时序快照 | C-13/C-16/C-26 三项计算能力依赖时序快照 | 燕大无快照能力 | 对端缺口 |
| **P1** | Activity TAG + activity_link | 燕大无 Activity TAG + 无关联关系 | 完全不存在 | 对端缺口 |
| **P1** | 图推荐 C-19 | 链路预测能力未提供 | — | 对端缺口 |
| **P1** | 13 条关系中除 2 已覆盖外的剩余 | cooperate / research / participate / belong_to / technology_hierarchy / technology_influence / dataset_link / event_link / carrier_cooperate | 依赖对应实体先存在 | 对端缺口 + 第06项Graph |
| **P1** | 6 个非七要素实体 | technology / field / topic / dataset / event / innovation_carrier | 部分语义错位、部分完全不存在 | 对端缺口 |

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
