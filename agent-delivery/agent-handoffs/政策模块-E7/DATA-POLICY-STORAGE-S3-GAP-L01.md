# DATA-POLICY-STORAGE-S3-GAP-L01 · S3 缺口补齐

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-STORAGE-S3-GAP-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |
| depends_on | `DATA-POLICY-STORAGE-ETL-FILL-L01`（≥ ready_to_sign） |

## Ponytail

- ponytail: `full`
- 四张表按既有 ads.md 的「表 + 用途」粒度登记，只对新群补一列关键列；**未**贴原始 DDL、**未**为每张表另开文件。
- `dwd.md` 列清单按用途分群列出，不复制 `db.py` 原始元组，也不重复 `ods-to-dwd-mapping.md` 的列对照。
- **未新建** `stores/mysql/README.md`（`stores/README.md` 已直接索引两份，再加一层是冗余）；**未新建** `dim.md`（政策域 as-built 无维表，不为对齐 ENT/CHAIN 目录形状造空文件）。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **无**。只登记已存在的表结构，未新增表、未改列、未动拓扑，不翻签。 |
| 会签态 | `approved`（`human:淮政玮` · 2026-08-21）维持 |

## 缺口来源

`DATA-POLICY-STORAGE-ETL-FILL-L01` 核查 ADS 写入图时发现 `ads.md` 只登记 9 指标表 + 2 图镜像，与 as-built 15 张不符。补文档时顺带发现 `dwd.md` 只有口径说明、无列清单，而 S3 的职责正是 stores 细表。

## 修改内容

**`stores/mysql/ads.md`**

- 新增「表总览（as-built 15 张）」：按指标 9 / 图镜像 2 / NER 1 / 文本 3 分群，标注各群产出模块，并显式指出旧口径「九张指标表」会漏后 6 张。
- 新增「NER 结果」节：`policy_entity` 用途 + 关键列 + `entity_type` as-built 取值枚举 + `source_field` 的 D9 字段级血缘作用。
- 新增「文本智能处理」节：`policy_text_parse` / `policy_match` / `policy_simulate` 三表用途 + 关键列；标注三表均带 `model_version` 需在 UI 显示；`policy_simulate` 仅单轮，多轮快照属 `OPEN-POLICY-DISP-05` 不得塞入。
- 图镜像节补一句指向 `nebula.md` 的四类边语义。

**`stores/mysql/dwd.md`**

- 新增「as-built 列清单」：`policy_base_info` 按主键/基本信息/时间/分类状态/正文/深度文本/执行口径/其他/审计/扩展位十群列出。
- 五条要点：深度文本五列是算法链燃料不得截断；`ext1` 承载政策类型属 QPOL-01 临时口径；`ext5` 是产业回落位；`is_deleted=0` 是统一过滤条件；国际政策同表切片。

**`stores/README.md`**：索引行同步为「ADS 15 张：指标 9 + 图镜像 2 + NER 1 + 文本 3」与「含 as-built 列清单」。

**`etl/pipeline-dwd-to-ads.md`**：⚠️ 未登记提示改为已补登指引（缺口已闭合，不再挂 `OPEN-POLICY-GRAPH-03`）。

**未改**代码、**未** APPLY DDL、**未**灌数、**未**新建表。

## 边界说明（本叶为何不动 nebula.md 的 DDL）

`OPEN-POLICY-GRAPH-03` 原挂两项：

| 项 | 性质 | 本叶处理 |
|---|---|---|
| ads.md 漏登四表 | **文档落后于 as-built**，登记即闭合，无需裁决 | ✅ 已补 |
| nebula.md 四类边列定义 | **设计与实现分歧**，需决定哪边改 | ❌ 保留，仍待 `human:淮政玮` 裁决 |

第二项若按 as-built 改文档，等于替甲方/架构侧否掉 per-edge 列的设计意图；若按设计改代码，需改 `polan` 并重投影。两者都不是文档叶能拍板的，维持 `stores/nebula.md` 现有 ⚠️ 标注不动。

## 验收证据

| 结论 | 来源 |
|---|---|
| ADS as-built 15 张及分群 | `polan/common/db.py` L52–132 的 schema 定义与分节注释 |
| 四张表关键列 | 同上 L101–132 逐字段核对 |
| `entity_type` 取值枚举 | `polan/graph/entity.py` L98–107 `add_ner` 调用点 |
| `policy_base_info` 列清单 | `polan/common/db.py` L40–51 |
| `ext1` = 政策类型 | `polan/basic/indicators.py` 模块头「A2 … QPOL-01 临时用 ext1」 |
| `ext5` 产业回落 | `polan/graph/entity.py` L113 `rel.get("industry") or [p["ext5"]]` |
| `is_deleted=0` 过滤 | `polan/graph/entity.py` L54 查询条件 |

无 CI（定义叶）。相对链接已按目录层级核对。

## 遗留风险

- `OPEN-POLICY-GRAPH-03` 仍留边列定义一项待裁决。
- `ext1` 承载政策类型是 QPOL-01 临时口径，甲方确认类别体系后 `dwd.md` 与 `policy_type_dist` 需同步改。
- 本叶登记的是 **Demo as-built** 结构；接三方真数据后列集合可能变化，需按 SEED 单复核。
- S3 主单 `DATA-POLICY-STORAGE-S3-L01` 仍 `ready_to_sign`，本补齐叶与之并行待签，建议同批签收避免口径分叉。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓文档叶）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/README.md`
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-dwd-to-ads.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 零代码改动 |
| 调用链 / D12 | ✅ Java 只读 ADS 口径未变 |
| 图谱 Nebula 一张 G | ✅ 未动图结构；边列之争按开放项挂起 |
| 无闸门不写正式库 | ✅ 登记的是 `demo_gkxlumenx_ads`；本叶不建表不灌数 |
| D9 血缘 | ✅ `source_field` 字段级落点与 `model_version` 显示要求已写入 |
| 诚实性 | ✅ 只登记已存在结构，未预登记未建之表 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 34000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.44 |
| cost_warn | green |
