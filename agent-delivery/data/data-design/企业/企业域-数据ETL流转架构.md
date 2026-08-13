# 企业域数据 ETL 流转架构（ODS → DWD → ADS / ES / 图谱）

> **版本**：v0.5-draft  
> **日期**：2026-08-12  
> **作者**：architect-agent（扫描现有仓与规约后起草；**执行归属待人拍板**）  
> **配套图**：同目录 [`企业域-数据ETL流转架构图.html`](./企业域-数据ETL流转架构图.html)（须与本文同步）  
> **状态**：架构草案。文中标 🟡 的项不得由 AI 替甲方/PM 决定。  
> **执行归属约束**：不做「全链路我方落地」；只保留 **混合模式** 与 **三方模式**。  
> **调度约束**：允许**每日多批次**入库；必须**幂等**（业务键 upsert + 水位/游标），支持断点重跑与任意时刻补跑且不重复。

---

## 1. 目的与边界

本文回答企业模块进入「真实数据 ETL」阶段后，数据如何从三方入站层进入我方可读契约面与检索/图谱面，并明确：

1. **数据流分层与职责**（ODS / DWD / ADS / ES / Nebula）
2. **两类加工**：贴源映射 vs 算法指标计算
3. **执行归属双轨（仅此两种）**：**混合模式** vs **三方模式**（我方提供 Mapping **或** SQL/Python 脚本）；**废弃全链路我方落地**
4. **日变更量报告 + 质量报告**（发现漏数 / 代码遗漏的主手段）
5. **与现有仓与文档的对齐点**（as-built）与开放决策

**不在本文范围**：前端页面交互、Java 业务 REST 字段契约细节、非企业域（政策/产业链/服务机构）的表级 Mapping。

---

## 2. 命名词典（必须先读，否则会串层）

| 口头说法 | 实际对象 | 库/表习惯 | 说明 |
|---|---|---|---|
| **入站 ODS（运行时）** | 三方清洗后对项目开放的明细 | 供应侧常为 `dwd_*` 表名 | 供应约束：真正的 `ods_*` **不暴露**；项目侧把「可见的供应明细」当作入站贴源。见 `SUPPLIER-WORK-CONSTRAINTS.md` |
| **项目 DWD** | 我方按业务设计的明细/维度/指标表 | `gkxlumenx_dwd.*`（表名**不带** `dwd_` 前缀，v3.0） | 与供应表**解耦**，不一一同名。真源：`DWD表结构设计-企业模块-MySQL-v3.0.md` |
| **ADS** | 线上只读契约面 | `gkxlumenx_ads.*`（规划/部分已建） | Java **只读 ADS**；算法/ETL 写。本期企业口径：**结构与 DWD 对齐的同步副本**（不做再聚合变形） |
| **ES** | 企业检索索引 | 别名 `gkx_enterprise` → `gkx_enterprise_v1`（国内）+ `gkx_enterprise_global_v1`（国外） | `lumen-etl-es-py`：DWD → ES；搜索/读走别名，ETL 写物理索引 |
| **图谱** | NebulaGraph | space 如 `gkx_ent`（demo/正式对齐中） | 从 DWD 关系表灌 Tag/Edge；禁止 Neo4j 作为生产主存 |
| **DQ 门禁** | Data Quality 检查通过才放行下游 | 作业后钩子 | 主键/空值/枚举/软删等规则；**不通过则不触发**算法、ADS、ES、图谱 |
| **日更报告** | 每日变更与质量汇总 | 报表/飞书/对象存储 | 含推送量、入仓影响量、对账差额，用于发现漏数；**按批次**也可出中间报告 |
| **水位 / 游标** | 增量抽取进度标记 | 时间点或单调 ID | 决定「本批读到哪」；重跑不回退已提交成功区间（除非显式回补窗口） |
| **幂等入库** | 同一批数据跑 N 次结果一致且无重复行 | upsert / 唯一键 | 禁止裸 `INSERT`；业务唯一键冲突则更新 |

> **一句话**：供应库里的 `dwd_*` ≠ 项目 `gkxlumenx_dwd`。前者是入站原料，后者是我方标准明细层。

---

### 2.1 国内外机构分库分索引

| 层 | 国内 | 国外 |
|---|---|---|
| **DWD** | `enterprise_*`（如 `enterprise_base`、`enterprise_invest`） | `enterprise_forg_*`（如 `enterprise_forg_base`、`enterprise_forg_invest`） |
| **ES 物理索引** | `gkx_enterprise_v1` | `gkx_enterprise_global_v1` |
| **ES 别名** | `gkx_enterprise`（共用） | `gkx_enterprise`（共用） |
| **写路径** | ETL 写 `gkx_enterprise_v1` | ETL 写 `gkx_enterprise_global_v1` |

- 两个物理索引 mapping 结构一致，分词器可不同：国内 `name_cn` 用 IK + 拼音、`name_en` 存英文/别名；国外 `name_cn` 存 `name_alias`（本地名称，可能中文）、`name_en` 存 `enterprise_name`（英文名），均用 `standard`。
- 搜索/读统一走别名 `gkx_enterprise`，ES 自动 fan-out；别名指向多索引时**不能用于写**，ETL 必须写物理索引。
- 混合查询使用 `country_code`（统一 alpha-3）过滤国内/国外范围。
- 国内、国外 ETL 模块独立调度，互不阻塞；国外模块名统一为 `forg_reg_info` / `forg_executive` / `forg_finance` / `forg_relations`。

## 3. 目标数据流（企业）

与 HTML 流程图节点一一对应（T0–T8）。

```text
T0  三方源业务库
      │  推送 / 同步（供应方）
      ▼
T0' 【入站 ODS】供应开放明细（常称 dwd_*）
      │  Mapping / SQL / Python 脚本
      │  清洗 · 主键对齐 · is_deleted=0
      ▼
T1  【项目 DWD】贴源明细/维度表  gkxlumenx_dwd
      │
      ├─► T2  DQ 门禁（失败则阻断下游，写失败报告）
      │         │ 通过
      │         ▼
      │    T3  算法指标作业（Python）→ 指标表写回 DWD（或再同步 ADS）
      │         │
      │         ├─► T4  DWD → ADS 同构同步（本期不改结构）
      │         ├─► T5  DWD → Elasticsearch（日更增量：国内模块 + 国外模块独立调度）
      │         └─► T6  DWD → NebulaGraph（日更增量/全量）
      │
      └─► T7  日更变更报告 + 质量报告（每步写计数；日终汇总）
              │
              ▼
         T8  线上：前端 → Java REST →（只读 ADS）+ ES + 图谱（经 Python /internal）
```

### 3.1 加工语义

| 步骤 | 输入 | 输出 | 是否改结构 | 业务逻辑载体 |
|---|---|---|---|---|
| **A. ODS→DWD 贴源映射** | 入站 ODS | DWD 明细/维度表 | 有：字段映射、枚举归一、拆合表 | Mapping 说明 **或** 可执行 SQL/Python |
| **B. DWD 算法指标** | DWD 明细（+ 配置权重） | 指标结果表 | 有：新指标列/表 | **算法只在 Python**（铁律） |
| **C. DWD→ADS 同步** | DWD | ADS | **本期无**：同构同步 | 同步作业（平台或脚本） |
| **D. DWD→ES** | DWD | ES 文档 | 有：检索模型 | `lumen-etl-es-py`（国内 `enterprise_*` 模块 + 国外 `enterprise_forg_*` 模块独立调度） |
| **E. DWD→图谱** | DWD 实体/关系 | Nebula Tag/Edge | 有：图模型 | Python `nebula_loader` / 增量 |
| **F. 日更报告** | 各步计数与 DQ 结果 | 日报 / 告警 | — | 报表作业（必做） |

### 3.2 入库频率与幂等（必提示）

**结论：需要在架构与作业规范里明确提示频率与幂等，不能默认「一天只跑一次、失败整日重跑」。**

| 原则 | 要求 |
|---|---|
| **频率** | 允许 **每日多批次** 执行 ODS→DWD（及下游扇出）；批次间隔由 SLA / 供应推数节奏决定（如每小时、固定窗口、有数即跑）🟡 |
| **不重复** | 同一业务实体多次跑不得堆出重复行；写入必须 **按业务唯一键 upsert**（`INSERT … ON DUPLICATE KEY UPDATE` / `REPLACE` 等价语义，或先删后插仅限明确分区） |
| **断点重跑** | 每表（或每 Mapping 任务）维护 **水位**：优先 `update_time`（+ 并列键防同秒丢数），或单调递增业务/`id`；失败从**上次成功提交的水位**续跑，不要每次从日初全扫除非回补任务 |
| **随便跑（任意时刻补跑）** | 允许人工/平台对任意时间窗 `[t0, t1]` 或 ID 区间重放；重放仍走 upsert，结果与首次成功写入一致 |
| **批次元数据** | 每批记录 `batch_id`、水位起止、行数、成功/失败；报告与告警按批累加，日终再汇总 |

**水位选型建议**：

1. **有可靠 `update_time`（供应约束已要求）**：水位 = `max(update_time)`，同秒追加 `id` / 业务键并列游标，避免同时间戳漏数。  
2. **时间不可靠、有单调 ID**：水位 = 已处理最大 `id`（或供应侧变更流水号）。  
3. **全量维表 / 小表**：可按日全量 upsert，仍靠唯一键防重，不依赖水位，但报告仍要记「本批影响行数」。

**禁止**：无唯一键的盲插；依赖「作业互斥锁」代替幂等；多批并行写同一表却无分区/无锁且无 upsert（易乱序覆盖，须在作业规范里写清并行边界 🟡）。

---

## 4. 日更变更报告与质量报告（必做）

目的：用**可对账的数量**判断「ODS 有推、DWD 没进 / 进少了」是否由 Mapping/脚本遗漏或过滤过严引起，而不是只看作业成功/失败。

### 4.1 日变更量报告（Volume / Delta）

按**表**（或 Mapping 任务）输出，建议字段：

| 指标 | 含义 | 用途 |
|---|---|---|
| `batch_id` / `batch_start` / `batch_end` | 本批标识与水位窗口 | 多批对账、断点续跑 |
| `watermark_before` / `watermark_after` | 批前/批后水位（时间或 ID） | 证明增量区间 |
| `ods_push_rows` | 本批 ODS 推送/可见变更行数（insert+update，按水位） | 供应是否有数 |
| `ods_active_rows` | 本批参与映射的有效行（如 `is_deleted=0`） | 过滤后原料量 |
| `dwd_insert_rows` | 入 DWD 新增行数 | 映射产出 |
| `dwd_update_rows` | 入 DWD 更新行数（含幂等重跑命中更新） | 映射产出；重跑时 insert≈0、update↑ 属正常 |
| `dwd_soft_delete_rows` | DWD 置历史/失效行数 | 与 ODS 删除/失效对齐 |
| `dwd_affected_orgs` | 受影响企业数（`org_id` distinct） | 业务影响面 |
| `dwd_dup_reject_rows` | 因唯一键冲突被规范化为 update 的行（可选） | 观察重跑/乱序 |
| `ads_sync_rows` | ADS 同步行数 | 与 DWD 对账 |
| `es_upsert_docs` / `es_fail` | ES 写入成功/失败文档数 | 检索面 |
| `graph_nodes` / `graph_edges` | 图谱写入节点/边数 | 图谱面 |
| `algo_metric_rows` | 算法指标写出行数 | 指标面 |

**漏数告警规则（草案）**：

1. `ods_active_rows > 0` 且 `dwd_insert_rows + dwd_update_rows = 0` → **疑似 Mapping/脚本未跑或全过滤**（P0）
2. `|ods_active_rows − (dwd_insert+dwd_update+预期拒绝)| / ods_active_rows > 阈值` → **转化率异常**（P1）
3. `dwd_affected` 与 `ads_sync` / `es_upsert` 差额超阈值 → **下游漏同步**（P1）
4. 与昨日/近 7 日均值偏离超阈值 → **突增突降**（P2，需人工确认是否业务日）

### 4.2 质量报告（DQ Report）

在「变更量」之外，每日输出质量切片（可与 DQ 门禁共用同一套规则引擎）：

| 类别 | 检查项（示例） | 失败动作 |
|---|---|---|
| **完整性** | 主键/业务键空值率；必填字段空值率 | 门禁阻断或标红 |
| **唯一性** | 业务唯一键重复数；幂等重跑后行数不膨胀 | 阻断该表下游 |
| **合法性** | 枚举越界、日期非法、金额负数 | 记入拒绝明细 |
| **参照完整性** | `org_id` 能否关联企业主表 | 告警 / 隔离脏行 |
| **软删一致性** | ODS `is_deleted=1` 是否在 DWD 正确失效 | 对账项 |
| **时效性** | ODS 最新 `update_time`、本批水位推进、相对 SLA 延迟 | 延迟告警；水位停滞告警 |
| **水位健康** | `watermark_after >= watermark_before`；无回退（回补任务除外） | 防止漏扫或乱序 |
| **跨层对账** | 抽样 N 家企业：ODS ↔ DWD ↔ ADS ↔ ES ↔ 图 | D4 `verified` |
| **拒绝明细** | 被过滤/转换失败的行（键 + 原因码） | 排查 Mapping 遗漏 |

报告形态建议：日终一份 **汇总 JSON/Markdown**（表级计数）+ **失败明细 CSV**；推送飞书/邮件；归档对象存储便于回溯。

### 4.3 与调度的关系

```text
任意批次（日可多批）：
  T0' 按水位拉取 ODS 增量 → 写 ods_* 计数 + watermark
  T1  upsert 入 DWD → 写 dwd_* 计数（insert/update 分开）
  T2  DQ 门禁 → 写质量项；失败则阻断本批 T3–T6，仍出批报告
  T3–T6 各步结束 → 写 ads/es/graph/algo 计数；推进已提交水位
  T7  批报告累加；日终再出汇总日报 + 告警
重跑 / 补跑：指定 [t0,t1] 或 ID 区间，仍 upsert，水位策略见 §3.2
```

---

## 5. 执行归属双轨（仅混合 / 三方）

> **已废弃**：全链路「我方落地 ETL」（原模式 α）。批处理与贴源调度不以我方自建全链路为目标。

两种可选模式**数据流与报告口径相同**，差异在算法 / ES / 图谱是否仍由我方服务承接。业务语义、DQ、报告阈值由我方冻结。

### 5.1 混合模式（推荐默认）

| 段 | 执行方 | 我方交付 / 保留 |
|---|---|---|
| ODS→DWD | **三方平台** | Mapping **或** SQL/Python + DQ 规则 |
| 算法指标 | **我方 Python**（平台可触发） | `/internal/*` 任务 API |
| DWD→ADS | **三方平台** | 表清单、同构规范、SLA |
| DWD→ES | **我方** `lumen-etl-es-py`（平台触发） | 索引 mapping；平台直写需双签 🟡 |
| DWD→图谱 | **我方** 灌图服务（平台触发） | Tag/Edge 契约；平台直写需双签 🟡 |
| 日更报告 | 平台出数或我方汇总 | **报告指标字典由我方定**（§4） |

### 5.2 三方模式

| 段 | 执行方 | **我方交付物（任选或组合）** |
|---|---|---|
| ODS→DWD | 三方平台 | ① Mapping 说明 ② 可执行 SQL ③ Python 脚本；+ DQ SQL、验收用例、报告字段定义 |
| 算法指标 | 平台调度；**计算仍须走我方 Python**（铁律）或经双签例外 🟡 | `/internal/*` 契约；禁止在平台用非 Python 重写算法逻辑 |
| DWD→ADS | 三方平台 | 表清单、同构同步规范、SLA、对账字段 |
| DWD→ES | 三方调度（优先调我方 ETL API；直写需双签 🟡） | 索引 mapping + 局部更新规范 |
| DWD→图谱 | 三方调度（优先调我方灌图 API；直写需双签 🟡） | Tag/Edge 契约 + 增量策略 |
| 日更报告 | 三方平台按我方字典出数 | 指标字典、漏数告警阈值由我方定 |

> 无论混合还是三方：我方可只给 Mapping，也可直接给 **SQL/Python**；**日变更量 + DQ 报告口径不变**。

### 5.3 二者怎么选（供人拍板）

| | 混合模式 | 三方模式 |
|---|---|---|
| 贴源 / ADS | 三方跑 | 三方跑 |
| 算法 / ES / 图谱 | **我方服务必经**（平台只触发） | 平台调度为主，仍优先调我方 API |
| 适用 | 默认；保护检索局部更新与图谱契约 | 供应方平台能力强、愿接调度与出报 |

> **拍板结论待填**：当前文档默认推荐 **混合模式**；若选纯三方模式，须确认 ES/图谱写路径与算法触发方式（Q-ETL-ENT-01/03）。

---

## 6. 与现有项目 as-built 对齐

| 能力 | 现状 | 仓 / 文档 |
|---|---|---|
| 架构铁律 | 前端→Java→Python `/internal/*`；Java 只读 ADS；图谱=Nebula | `architecture-baseline.md` |
| 入站约束 | 供应 `ods_*` 不暴露；工作面=`dwd_*` | `SUPPLIER-WORK-CONSTRAINTS.md` |
| 项目 DWD | 企业 36 表 v3.0 已迁库 | `DWD表结构设计-企业模块-MySQL-v3.0.md` |
| ODS→DWD Mapping | GDF 企业工作包 + Mapping v3 | `GDF/派单包/企业/GDF-ENT-WORKPACK-v1/` |
| DWD→ES（国内） | `lumen-etl-es-py` 国内模块（reg_info/tag_info/.../statistics，13 个） | `企业搜索-ES更新机制.md` |
| DWD→ES（国外） | `lumen-etl-es-py` 国外模块：`forg_reg_info` / `forg_executive` / `forg_finance` / `forg_relations` | `企业搜索-ES更新机制.md` |
| DWD→图谱 | `entan/graph` | `demo-algo-ent-analysis` |
| 血缘 D4 | `ods_synced → dwd_loaded → es_indexed → graph_loaded → verified` | `data-lineage-policy.md` |

**缺口**：生产级 ODS→DWD 日更流水线、DWD→ADS 统一同步、**日变更/质量报告**、执行归属（混合 vs 三方）双签。

---

## 7. 开放决策清单（🟡）

| ID | 决策项 | 选项 |
|---|---|---|
| Q-ETL-ENT-01 | 执行归属选哪种 | 混合模式 / 三方模式（**不含**全链路我方落地） |
| Q-ETL-ENT-02 | 三方承接时我方主交付形态 | Mapping / SQL / Python / 组合 |
| Q-ETL-ENT-03 | ES / 图谱是否允许平台直写 | 否（调我方服务）/ 是（需双签） |
| Q-ETL-ENT-04 | DWD→ADS 是否严格同构 | 是（本期）/ 后续引入聚合层 |
| Q-ETL-ENT-05 | 算法指标落 DWD 还是 ADS | 双写 / 只 ADS / 只 DWD 再同步 |
| Q-ETL-ENT-06 | 日更报告推送渠道与留存 | 飞书 / 邮件 / 对象存储；保留天数 |
| Q-ETL-ENT-07 | 漏数告警阈值（转化率、突增突降） | 百分比与基线窗口 |
| Q-ETL-ENT-08 | 日多批默认节奏 | 例如每小时 / 供应推完即跑 / 固定 2～4 窗 |
| Q-ETL-ENT-09 | 各表水位字段 | `update_time(+id)` / 单调 ID / 仅全量 upsert |

---

## 8. 下一步建议

1. 拍板 Q-ETL-ENT-01～03（混合 vs 三方 + 交付形态 + ES/图写权限）。  
2. 冻结企业域表级 Mapping/脚本清单 + **报告指标字典**（§4）。  
3. 先落「日变更量报告」MVP（ODS 推送量 vs DWD 影响量对账），再扩 DQ 明细。  
4. 将 ES / 图谱灌数纳入统一日更编排与报告计数。  
5. 抽样 5 家企业做 ODS↔DWD↔ADS↔ES↔图端到端核验模板。

---

## 9. 参考索引

| 文档 / 仓 | 用途 |
|---|---|
| `architecture-baseline.md` | 方案 A、调用链铁律 |
| `数据库设计.md` §12 | 数据工厂与契约面 |
| `data-lineage-policy.md` | 血缘与 D4 阶段 |
| `DWD表结构设计-企业模块-MySQL-v3.0.md` | 项目 DWD 真源 |
| `企业搜索-ES更新机制.md` / `lumen-etl-es-py` | DWD→ES |
| `graph-engine.md` / `entan/graph` | DWD→图谱 |
| `GDF/派单包/企业/GDF-ENT-WORKPACK-v1` | Mapping 工作包 |

---

## 附录 A · 版本历史

| 版本 | 日期 | 说明 |
|---|---|---|
| v0.1-draft | 2026-08-10 | 首版：双轨执行归属 |
| v0.2-draft | 2026-08-10 | 补日变更/质量报告；三方交付 Mapping 或 SQL/Python；与 HTML 流程图对齐 T0–T8 |
| v0.3-draft | 2026-08-10 | 废弃「全链路我方落地」；执行归属仅保留混合模式与三方模式 |
| v0.4-draft | 2026-08-10 | 补入库频率提示：日多批、幂等 upsert、水位断点重跑与任意补跑 |
| v0.5-draft | 2026-08-12 | 补国内外机构分库分索引：`gkx_enterprise_v1` + `gkx_enterprise_global_v1` 共用别名，搜索读别名、ETL 写物理索引；T5/as-built 补充国外模块独立调度 |
