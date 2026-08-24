# metrics/ —— 指标真源目录（D9 数据血缘）

> 模型定义：`../data-lineage-policy.md` §2.1（填齐时序）+ §2.3（四维就绪度，**v1.5**）。  
> 8 件套 = **`D1=aligned` 齐备态**（v1.5 起 **9 项**，含 `algorithm_type`），不是 PACK/OPEN 一次填完。  
> **类型 / 流程 / WBS / 8/25 给人表**（勿在本目录存副本）：[`../agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md`](../agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md)

## 0. 目录地图（先看这张）

身份 YAML 在 `registry/`（FE / API / 镜像脚本只认这里）。文档与口径细稿按桶收口。

```
metrics/
├── registry/                              ← 机器真源（v1.5 起）
│   ├── cfg_metric-{域}-seed.yaml          ← 8 件套（9 项，含 algorithm_type）
│   ├── metric-readiness-matrix-{域}.yaml  ← 四维就绪度
│   └── metric-spec-POLICY.yaml            ← 政策算法定义卡
│
├── calc-logic/                            ← 口径细稿 md（seed 的展开）
│   ├── ENT/     60 × M_ENT_*
│   ├── CHAIN/   63 × M_CHAIN_*
│   └── SVC/     29 × M_SVC_*
│
├── ingest/                                ← B 轨入库过程（指南 / 交接报告 / 批次 xlsx）
├── inventory/                             ← D1 前需规抽取（非正式 TMP_*；展示 112 行）
│
├── algo-results/                          ← A1：算法库 97 叶 + 8/25 ODS 给人表
├── request/                               ← A2 差集 + 九新
│   ├── 专题系统/  展示系统/
│   ├── 九新-技术机构人才/
│   └── _work/                             ← loop/fan-in 底稿，不是给人主表
└── indicator-inventory/                   ← 废作四叶，只读
```

| 问 | 打开 |
|----|------|
| 梳理 vs 血缘各管什么？ | [`给人说明-指标与算法工作类型与流程梳理.md`](./给人说明-指标与算法工作类型与流程梳理.md) |
| 这个指标 8 件套 / 就绪度？ | MCP `metric-registry`（`metric-get` / `metric-query`）；说明见 [`metric-mcp-usage-guide.md`](../metric-mcp-usage-guide.md)。禁止整文件读 `registry/` YAML |
| 指标进度统计 Excel？ | MCP `metric-progress-export`（skill `gkx-metric-progress`）→ `registry/export/指标与数据开发进度.xlsx` |
| 算法类型 `algorithm_type`？ | seed 第 5 项（未填=`UNKNOWN`；会签前可先看 A1 表2） |
| 这条指标填到哪一关？ | 矩阵 `lifecycle_stage`（policy §2.1.1；未填=`unspecified`） |
| 口径怎么算、源表是哪？ | `calc-logic/{ENT,CHAIN,SVC}/` |
| 王惠怎么入仓 / 8/21 交接？ | `ingest/` |
| 展示需规抽了哪些指标（未注册）？ | `inventory/展示系统/` |
| 页面要了库没有？ | `request/{专题系统,展示系统}/` |
| 算法库叶子 ODS 满不满？ | `algo-results/` |
| 九新交 SQL 还是 API？ | `request/九新-技术机构人才/` |

**唯一性铁律**：同一要素域禁止第二份矩阵 / 第二份 seed；禁止用 Excel/Word/散落 md 当平行状态表。FE 与 API 只认 **`registry/`** YAML。旧根路径 `metrics/registry/cfg_metric-*.yaml` 已迁走，不要在根上再放一份。  
`lumen-algo-py/docs/metrics/` **只保留指针**，不再存口径副本。  
仓根 `gkx-orchestration/agent-handoffs/` **已停用**（误放；盘点见 `inventory/`，任务 handoff 见 `agent-delivery/agent-handoffs/`）。

## 1. registry/ YAML Owner

| 文件 | 角色 | Owner |
|------|------|-------|
| `registry/cfg_metric-{域}-seed.yaml` | 指标 8 件套（现网：ENT / POLICY / CHAIN / SYNTH / TNIE / INNOV / TECH / ORG / TALENT / SVC / COMMON） | data-agent |
| `registry/metric-readiness-matrix-{域}.yaml` | 四维就绪度（现网：ENT / CHAIN / SVC / SYNTH / INNOV / TECH / ORG / TALENT / COMMON / POLICY） | data-agent（D2：lineage-subcoord） |
| `registry/metric-spec-POLICY.yaml` | 政策指标 spec / 算法定义卡 | data-agent |

`cfg_metric-SVC-seed.yaml` 于 `METRIC-SEED-REGISTER-L01` 只登记 OPEN 身份（`M_SVC_ORG_TECH_SCORE` + `M_SVC_TYPE_DIST_QUERY`）。B 轨 29 条口径细稿仍在 `calc-logic/SVC/`，**不**在本批全量灌入 seed。

CHAIN seed 与 B 轨 63 条 `M_CHAIN_*` **不一定同集**（seed 含 Wave0 Mock）。改口径先改 `calc-logic/CHAIN/`，再同步 seed。

`algorithm_type` 存量未回填；新 OPEN / 公式会签由 data-agent 写入。禁止把未评估写成 `STAT` 充数。

## 2. 口径侧（王惠）派单与提交格式 ⭐

> 背景：口径梳理习惯用 Excel 做工作底稿——**允许**；Excel **不是** 8 件套 / D1–D4 真源（真源仍是 `registry/` YAML）。  
> 决策：2026-08-01 项目负责人（淮政玮）。  
> **进仓（2026-08-22 淮政玮）**：`metrics/` 目录下的 xlsx **可以进 git**（差集给人表、半成品清单、ingest 冻结快照等）。Office 锁文件 `~$*` 仍不进。

### 2.1 派单话术必含（coordinator / PM 派单时逐条带上）

1. 产出物 = 对应要素域 YAML 真源的**增量更新**（矩阵 D1 列 + seed 已有字段；OPEN 阶段允许 `D1=draft`，**不要求** 8 件套齐），**不是** Excel 附件本身；
2. Excel 底稿列结构须与矩阵 schema 字段对得上（至少含：`metric_id` / 中文名 / 口径定义 / `d1_def_status` 判定 / 关联 Q-* 开放项）；无 metric_id 的新指标行须显式标「待注册」；
3. 交付路径 = 发给 data-agent 正式化，**不要**直接改 YAML（避免格式/枚举错漏）；xlsx 可放 `metrics/` 进仓，但**不得**当第二套 seed / 矩阵；
4. 业务口径歧义不得自行拍板 → 登记 `客户决策清单跟踪表.md`（🟡），矩阵对应条目保持 `d1_def_status: draft`。

### 2.2 data-agent 正式化步骤（收到 Excel 后）

1. 逐行核对 metric_id 是否在 `registry/` seed；新指标先注册 seed（已有字段即可，缺公式/源表/类型则 `D1=draft`，`algorithm_type` 可 `UNKNOWN`），再入矩阵；
2. 把口径细稿写成 `calc-logic/{域}/{metric_id}.md`（见 §4）；
3. 更新矩阵对应条目（通常只动 D1 列 + `d1_pending_ref`；D2/D3/D4 不随口径提交联动）；
4. 矩阵头部更新 `updated` 日期 + 在生成任务注释追加来源任务 ID；
5. 枚举校验（`aligned|draft|missing` 等）+ 汇总统计段刷新；
6. commit message 标 `[agent:data-agent]` 并注明「正式化自 王惠 {日期} Excel 底稿」；
7. 同步通知 FE（demo 镜像 `readinessSeed.ts` / Wave 1 catalog API）。

### 2.3 验收标准（handoff 必附）

- [ ] YAML 可被解析（无缩进/枚举错误），统计段与条目一致
- [ ] 每条 `draft` 都挂 `d1_pending_ref`（Q-* / GAP-*），且与 `客户决策清单跟踪表.md` 一致
- [ ] 无第二真源：xlsx 不替代 `registry/` YAML；无平行状态表；`~$*` 未进仓
- [ ] `aligned` 条目有口径定义落在 seed 的 `definition`（≥50 字，policy §2 第 3 项），且 `algorithm_type` ≠ `UNKNOWN`

## 3. 就绪度矩阵维护规则（速查）

- D1 由口径提交驱动（上文）；D2 由架构/data-agent 评估 + lineage-subcoord 核验（`pending→ready/partial/missing`，`provisional→verified`）；D3 由 GDF 映射结论驱动（8/20 后复判）；D4 由数据工厂接入事实驱动
- 任何维度**禁止**在无证据情况下改绿（policy §2.3 诚实性约束）
- 矩阵变更后 demo 侧镜像同步任务：见 `agent-handoffs/ENT-MOD-EVAL-READINESS-UI-L01.md` 模式

## 4. calc-logic/ · 指标计算逻辑真源（md 文件）

> 背景：口径侧（王惠）Excel 底稿含多级子指标（L1/L2/L3）的详细口径定义、计算逻辑、源表字段等信息，超出 seed yaml 8 件套的摘要粒度。  
> 决策：2026-08-18 项目负责人（淮政玮）确认入仓方案。2026-08-22 CHAIN/SVC 从 `lumen-algo-py/docs/metrics/` 汇总到本仓，与 ENT 同级。

### 4.1 目录结构

```
metrics/calc-logic/{域}/
├── README.md          ← 索引
├── M_{域}_*.md        ← 每个指标 ID 一个 md 文件
└── ...                ← 多级子指标合并为单文件（文件内按 L1→L2→L3 分节）
```

| 域 | 条数 | 过程件 |
|----|------|--------|
| ENT | 60 | 企业批次过程不在 `ingest/`（早于该目录） |
| CHAIN | 63 | `ingest/CHAIN/` |
| SVC | 29 | `ingest/SVC/` |

### 4.2 md 文件规格

**单行指标（仅 L1）**：
- 元数据（指标ID / 名称 / 模块 / 频率 / 对齐状态 / 是否在数据库 / 关联Q编号）
- 口径定义、计算逻辑说明、源表字段、待建表字段、备注

**多级子指标（L1 + L2/L3）**：
- L1 节：指标一级的元数据 + 口径定义 + 计算逻辑 + 源表字段
- 子指标详情节：按 L2 维度分小节，每个 L3 子指标列出独立的口径定义、计算逻辑、源表字段、对齐状态、数据库支持
- 同一 `metric_id` 的所有行合并为单文件，文件内按层级嵌套

### 4.3 与 seed yaml 的关系

- seed yaml 的 `calc_logic_ref` 字段指向本目录下的 md 文件路径（如 `metrics/calc-logic/ENT/M_ENT_TOTAL_COUNT.md`）
- seed yaml 保持 8 件套摘要级信息；md 文件提供完整口径细节（含子指标）
- 口径变更时：先更新 md 文件，再同步 seed yaml 的 `definition` / `formula` 等字段
- CHAIN seed 目前无 `calc_logic_ref`；先以 `calc-logic/CHAIN/*.md` 为准

### 4.4 维护规则

1. 口径变更流程：王惠更新 Excel 底稿 → data-agent 重新生成对应 md 文件 → commit message 标 `[agent:data-agent]` 并注明「正式化自 王惠 {日期} Excel 底稿」
2. `metrics/` 下 xlsx 可进 git（§2）；口径变更仍先改 md / seed，不要只改表；`ingest/` 冻结快照不改口径
3. 文件命名：`{metric_id}.md`，与 `metric_id` 一一对应
4. 多级指标合并：同一 `metric_id` 的所有 L1/L2/L3 行合并为单文件
5. 新增域时在 `calc-logic/` 下新建子目录（如 `calc-logic/POLICY/`），并生成对应的 README.md 索引

## 5. 算法任务结果落点

分析表 / 差集表落本目录；**派单包与给人流程说明**仍在 `agent-handoffs/算法库联调-ALGO-LIB/`。

| 路径 | 用途 |
|------|------|
| `algo-results/` | A1：schema + 双表 + **8/25** `-ods-status.xlsx` + `-ods-gaps.*` |
| `request/` | A2 四件套（`专题系统/`、`展示系统/`）+ 半成品 xlsx；九新表；`_work/` 底稿 |
| `ingest/` | B 轨入库指南 / 交接报告 / 20260821 xlsx 快照 |
| `inventory/` | D1 前需规抽取（展示 `SCI-DISPLAY-METRIC-L123-INV`） |
| `calc-logic/` | ENT / CHAIN / SVC 口径细稿 |
| `registry/` | 8 件套 seed / 就绪度矩阵 / 政策定义卡 |
| `indicator-inventory/` | 废作四叶，只读 |

`metrics/` 下 xlsx **可以进仓**（2026-08-22 淮政玮）。`~$*.xlsx`、`_tmp*` **不进 git**。
