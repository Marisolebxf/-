# POLICY · Demo 模拟 ETL（模拟 GDF）过程说明

```yaml
---
doc_id: POLICY-ETL-DEMO-MOCK
element: POLICY
role: etl
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: multi
task_id: DATA-POLICY-STORAGE-S2-L01
---
```

> 流图：[`../01-data-flow.md`](../01-data-flow.md)（**approved · 不翻签**）。  
> 列对照：[`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md)。贴源 DDL：[`../sources/ods-ddl.md`](../sources/ods-ddl.md)。  
> **本文件只把「模拟 ETL」过程写清；不灌数、不 APPLY、不改 `polan`。**

## 0. 「模拟 GDF」是什么

| 正式 GDF（工厂） | Demo 模拟（本文件） |
|---|---|
| 供应方 CDC / 贴源作业进正式 ODS | **不写** `gkx` / `gkxlumenx_*` |
| 明细 Mapping 作业推正式 DWD | 在 **Demo MySQL** 上用脚本/SQL **等价复现**「贴源 → 项目 DWD」 |
| 甲方作业平台调度 | 本域用 `run_all_policy` / 另开 SEED 叶触发；本单不执行 |

一句话：模拟 = **同表名、同列语义、同过滤规则**，落库只进 `demo_gkxlumenx_{ods,dwd,ads}`。

## 1. 端到端五步（必须按序）

```text
E0 贴源对照（只读 gkx 或 md-extract）
  → E1 入 Demo ODS（同表名镜像）
  → T2 ODS→DWD（列映射 + 过滤 + 平面标记）
  → L3 polan 写 ADS（指标 + 图镜像）
  → L4 投影 Nebula demo_gkx_chain（B 叶；本单不跑）
```

旁路 as-built（**不替代**上述主链验收）：`polan` 曾直写 ADS + `policy_graph_*`，图谱 API 只扫 MySQL。B 叶后目标态 = Nebula 优先、ADS 镜像兜底。

---

## 2. 分步说明

### E0 · Extract 对照（只读 · 不落 Demo）

| 项 | 值 |
|---|---|
| 读 | 供应库 `gkx.dwd_policy_base` / `gkx.dwd_global_policy_base`；或 `third-party-source/doc/md-extract` 口径 |
| 写 | **无** |
| 目的 | 确认列与 [`ods-ddl.md`](../sources/ods-ddl.md) 一致；估行数/空值；**禁止**当灌数入口 |

无供应库连通时：E0 跳过，E1 用 LLM Mock / 固定 fixture **按同一 DDL** 造 Demo ODS（另单 SEED）。

### E1 · 入 Demo ODS（贴源镜像）

| 项 | 值 |
|---|---|
| 写库 | `demo_gkxlumenx_ods` |
| 表 | **同名** `dwd_policy_base`、`dwd_global_policy_base`（DDL = 贴源真源） |
| 动作 | 全量 replace 或按 `id` upsert；保留供应技术列 |
| 谁 | SEED / Mock 入站（`POLICY-MOCK-INCR-L01` 或等价）；**不是** `polan` 算法职责 |
| 失败 | 本批不进 T2；保留上一成功 ODS |

禁止：改表名回 `dwd_zck_*`；把 ODS 表当项目 DWD。

### T2 · Transform + Load → 项目 DWD（模拟 GDF 核心）

| 项 | 值 |
|---|---|
| 读 | `demo_gkxlumenx_ods.dwd_policy_base` ∪ `dwd_global_policy_base` |
| 写 | `demo_gkxlumenx_dwd.policy_base_info`（**一张表**，国内+国际） |
| 过滤 | `is_deleted=0` **且** `is_history=0`；其余行不进 DWD |
| 映射 | **仅** [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) |
| 平面 | 国内行 `source_plane=domestic`（或等价）；国际行 `source_plane=global` |
| 主键 | ODS `id` → DWD `policy_id`；禁止另造哈希 |
| 国内要点 | `status` 保持「有效/失效」文案；`rank`/`type`/省市区/`policy_support` JSON **不得压扁丢列** |
| 国际要点 | `organ`→`publish_organization`；`category`/`country`/… 进同表或 `ext`；无国内 `rank`/`expire_date` 不强填 |
| OPEN | 国内/国际 `id` 碰撞策略；`vid` 超长（`pol:{id}` vs `vid_length=80`） |
| 失败语义 | **本批失败不晋升 L3**；ADS/图仍读上一成功批次 |

「模拟 GDF」= **这一步**。正式厂是 Mapping 作业；Demo 可用 SQL INSERT…SELECT / 小脚本，语义必须与对照表一致。

### L3 · 算法写出 ADS（指标面）

| 项 | 值 |
|---|---|
| 读 | DWD `policy_base_info`（+ 需要时的 ODS 附件字段） |
| 写 | `demo_gkxlumenx_ads.policy_*`（九张指标）+ `policy_graph_node`/`edge`（镜像） |
| 谁 | `demo-algo-ent-analysis` · `polan` / `scripts/run_all_policy.py` |
| 批次 | `calc_batch_id` 前缀 `mock_`（如历史 `mock_20260623`） |
| 失败 | 半成品不发布；任务 `failed`；禁止前端填数顶替 |

表清单：[`../stores/mysql/ads.md`](../stores/mysql/ads.md)。

### L4 · 投影一张 G（本管线 B 叶）

| 项 | 值 |
|---|---|
| 读 | DWD（点属性）+ 派生边候选（`quote_policy`→`cite`；`policy_support`→`support`/`apply_to`；产业/企业 hang） |
| 写 | Nebula **`demo_gkx_chain` only**；同步可刷 ADS 图镜像 |
| 谁 | `POLICY-NEBULA-PROJECT-CHAIN-L01`（`nebula_loader`） |
| 空态 | 对不齐不上图；API `source` 诚实（禁 ADS 全表扫却标 `nebula`） |

### T+1 · 增量与更新（日常调度，不是首批全量）

首批走 §1 全量。之后 **按日 T+1**：只拉水位以上的贴源变更，再按变更类型落到 DWD / ADS / 图。正式厂 = GDF Wave A CDC + Wave B Mapping + 触发 Python；Demo 模拟必须 **同一语义**。

水位（两表各自一份，禁止混用）：

```text
watermark = max(上次成功批的 ODS.updated_time, created_time)
本批增量集 Δ = (updated_time > watermark) OR (created_time > watermark)
              且跑批窗口通常为 昨日 00:00 ≤ ts < 今日 00:00
```

无 `updated_time` 的行只认 `created_time`。水位失败则 **不推进**（沿用上一成功水位），禁止静默全表重扫当增量。

#### 贴源变更码（`insert_remark`）

| 码 | 含义 | E1 Demo ODS | T2 项目 DWD |
|---|---|---|---|
| `0` | 新增 | `INSERT`（`id` 已存在则当 `1`） | `INSERT` `policy_id`；已存在则 upsert |
| `1` | 修改 | 按 `id` **整行覆盖**业务列 | 按 `policy_id` **整行覆盖**映射列（技术列按 ETL 规则） |
| `2` | 补齐 | 只填目标空值，**已有值不覆盖** | 同：只补 DWD 空列 |
| — | `is_deleted=1` | 镜像删除标记 | DWD 逻辑删（或物理移出当前集）；**不得**再进当日 L3 分子分母 |
| — | `is_history=1` | 可留 ODS | **不进**当前 DWD；当前集只认 `is_history=0` |
| — | 失效文案 | `status` 改为「失效」等 | DWD 同步文案；L3 时效率用更新后快照 |

国内 / 国际两表 **分别**抽 Δ，写入同一张 `policy_base_info`（`source_plane` 不变）。`id` 跨表碰撞仍走 mapping 的 OPEN，增量批不得自行改键。

```text
Δ 抽出（供应 gkx 只读）
  → E1 按码合并进 demo_ods 同表
  → T2 只处理 Δ 触及的 policy_id（删/史/补/改）
  → 当前 DWD 快照 = 全量当前行（is_deleted=0 ∧ is_history=0）
  → L3 用该快照重算指标，新 calc_batch_id；成功后切读新批
  → L4 只对 Δ 的 policy_id upsert 点、按规则重写其边；删除则删点边
```

#### 各层怎么更新

| 层 | T+1 策略 | 失败 |
|---|---|---|
| E1 ODS | 增量 upsert / 补齐 / 打删除标；**禁止**每日 drop+全量当 T+1 | 本批不进 T2 |
| T2 DWD | 按 `policy_id` 合并 Δ；当前查询视图过滤删与史 | 不晋升 L3；昨日 DWD 当前集仍可读 |
| L3 ADS | **按快照重算整批指标**（九张 + 图镜像可全量 replace 本 `calc_batch_id`）。聚合不能只对 Δ 做加减（时效率、占比、分省都会错） | 新批不发布；前端继续读上一 `calc_batch_id` |
| L4 图 | **点边增量**：Δ 内 upsert `pol:{id}`；该点旧边删后按新 `quote_policy` / `policy_support` 重挂；对不齐仍不上图 | fail-soft；API 不得把失败增量标成已投影 |

L3 不是「给昨天的 KPI 行 +1」。是 **新批次快照**；Java 只读最新成功批。

#### 调度顺序（同一自然日）

1. 等供应库 T+1 贴源就绪（或 Demo Mock 写入 Δ）。  
2. E1 → T2 **串行**；T2 行数/删除数对账不过则停。  
3. L3 启动前确认当前 DWD 快照已含本批 Δ。  
4. L3 绿 → 切 `calc_batch_id` → 才允许 L4。  
5. L4 可与读流量并存；禁止半投影当 `source=nebula`。

对账（最小集）：`Δ 条数`、`insert_remark` 分布、DWD 当前行增减、L3 新批 `policy_count` 与 DWD 当前 `COUNT(*)` 同向、L4 Δ 点成功/跳过数。

Demo 攒货追加（`POLICY-MOCK-INCR-L01`）只覆盖 **E1 差集**，须再跑 T2→L3（及需要时 L4），不得只追加 ODS 当「已更新」。

---

## 3. 单批作业清单（SEED / 联调时打勾）

| # | 步骤 | 输入 | 输出 | 本文件状态 |
|---|---|---|---|---|
| 1 | E0 对照 DDL | `gkx` 或 md-extract | 差异笔记 | 文档已齐 |
| 2 | E1 灌 Demo ODS | 供应抽样 / Mock | `demo_…_ods.dwd_*` | **另单 · 未灌** |
| 3 | T2 映射入 DWD | ODS 两表 | `policy_base_info` | 对照 draft · **未跑** |
| 4 | L3 跑指标 | DWD | `ads.policy_*` | 脚本有 · **本单禁跑** |
| 5 | L4 投影 | DWD + 边规则 | `demo_gkx_chain` | **B 叶** |

幂等建议：同 `calc_batch_id` 可重跑 replace；跨批晋升以「整批成功」为准，禁止半批混读。

## 4. 谁写谁读（汇总）

| 步 | 写方 | 读方 |
|---|---|---|
| E1 ODS | SEED / Mock 入站 | T2 |
| T2 DWD | 模拟 GDF 脚本（待 SEED 叶） | `polan`、展示/专题经 Java 只读 ADS 的上游 |
| L3 ADS | `polan` | Java；算法库联调台经网关读图时也可读镜像 |
| L4 图 | `polan` loader | `/v1/policy/graph`（优先 Nebula） |
| 展示原型 | **不写库** | `demo-ui-science` fixture（虚线） |

## 5. 脚本入口（已有 · 本单不执行）

| 用途 | 路径 | 对应步 |
|---|---|---|
| 政策全链路 | `demo-algo-ent-analysis/scripts/run_all_policy.py` | 偏 L3（现网可能跳过 E1/T2） |
| Mock 增量 | `polan/mockgen/` · `POLICY-MOCK-INCR-L01` | E1 / 差集 |
| 图投影 | `polan/graph/nebula_loader.py` | L4 |

现网 `run_all_policy` **不等于**完整 E1→T2；验收「模拟 GDF」必须能指认 **ODS 两表 → `policy_base_info`** 已按对照表落地。缺口另开 SEED，不在本单 silently 用 ADS Mock 冒充。

## 6. MinIO

对象前缀建议 `policy/{task_id}/`（解析附件、图谱快照）。见 [`pipeline-to-minio.md`](./pipeline-to-minio.md)。ETL 主链不依赖 MinIO 才能绿。

## 7. 禁止

- 写正式 `gkxlumenx_*` / 供应库 `gkx`
- `CREATE SPACE gkx_policy`；`DROP SPACE demo_gkx_chain`；写 `gkx_chain`
- 继续用 `dwd_zck_*`；用旧 v1 37 列当贴源
- 跳过 T2、算法直读 ODS 当「已工厂化」
- 用全表 drop+重建冒充 T+1；L3 对 Δ 做加减冒充快照；失败批切读新 `calc_batch_id`
- 本叶灌数 / 改 `polan` / 细表标 approved
