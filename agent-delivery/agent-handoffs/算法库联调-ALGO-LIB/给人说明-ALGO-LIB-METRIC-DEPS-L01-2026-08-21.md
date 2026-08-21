# A1 生产派单说明 · ALGO-LIB-METRIC-DEPS-L01

> **给谁**：监管人 `human:唐绍祖` 新开 **1** 个 Cursor 会话，执行 Agent = `algorithm-agent`  
> **日期**：2026-08-21（DoD 升格：双表；目的：8/25 前交出三方 ODS 缺口清单）  
> **硬截止**：2026-08-25 提出 **三方数据源不满足** 的缺口列表（给人用）  
> **任务状态**：`ready` · `task_type: spike` · Epic `E-ALGO-LIB-DEMO` · P0  
> **本文件角色**：A1 **生产派单真源**。短包 [`ALGO-LIB-METRIC-DEPS-L01-派单包.md`](./ALGO-LIB-METRIC-DEPS-L01-派单包.md)。总图 [`给人说明-算法指标梳理两轨-2026-08-21.md`](./给人说明-算法指标梳理两轨-2026-08-21.md)。  
> **结果落点**：`agent-delivery/metrics/algo-results/`。**不要**把分析结果写到 `agent-handoffs/`。  
> **Schema 真源**：[`metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`](../../metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md)

registry 旧 DoD / 旧 `*-deps.yaml` **以本说明 + schema 为准**。

---

## 1. 这一叶做什么

**为什么做**：8 月 25 日前要拿出「三方数据源（ODS）相对算法库计算需求 **不满足**」的缺口清单，给采购/入站沟通。双表是手段；**8/25 给人看的是缺口清单**。A2（页面 vs 算法库）不在这条 8/25 截止线上。

对科技专题**算法库**八维每一条 SRS 叶子，交付两张表 + 从中抽出的缺口清单（禁止混成一张）：

1. **表1 需规对应**：这条需规对应哪些指标、哪些算法；覆盖 `full | partial | missing | third_party`  
2. **表2 指标依赖**：每个指标的定义、算法类型、计算公式（或步骤）、以及**每一项重要计算输入**的三方 ODS 满足度（`full | partial | none | pending_ods | n/a`）  
3. **表3 三方缺口清单（8/25 主交付）**：只收录表2 中已判定 `none` / `partial` 的输入；`pending_ods` 另附「待核验」不得混进「不满足」

样板（只读，不替代逐条 SRS）：`metrics/calc-logic/ENT/`、`cfg_metric-ENT-seed.yaml`、`metric-readiness-matrix-ENT.yaml`。企业现有输出**没有**「需规叶子 → 指标」逐条对应，本叶必须补上。

对照物：`metrics/indicator-inventory/2026-08-20/` **只读**。缺维在本叶新建 `requirement_id`，不改那份 yaml。

## 2. 这一叶不做什么

| 禁止 | 原因 |
|------|------|
| 改 `cfg_metric-*-seed.yaml` / 就绪度矩阵 | A 轨不入库 |
| 写 Python / Java / 前端 | spike 文档 |
| 把 8/21 产业链·服务链入库报告写入本叶 DoD | B 轨 |
| 改 `inventory.yaml` 对齐正式 metric_id | 对应关系用表1 `metrics[]` |
| 人才/科研机构/技术实现 **伪展开公式** | `coverage_status: third_party`；表2 仍列 inputs |
| 把 `pending_ods` 写进「不满足」清单 | 未核验 ≠ 已确认缺口 |
| 盘专题/展示页面差集 | A2 |
| 再交一张混用的 `*-deps.yaml` | 已作废 |

## 3. 必读（按序）

1. 本文件 + schema  
2. `bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md`（叶子 97）  
3. 八维各层 md  
4. `metrics/indicator-inventory/2026-08-20/`（只读）  
5. `data-lineage-policy.md` §2.3 D3 枚举  
6. 企业样板：`calc-logic/ENT/README.md` + 任选一条简单（`M_ENT_TOTAL_COUNT`）与一条复合（`M_ENT_TECH_POWER_SCORE`）

专题侧同名分析 md 可作语境，不以页面 USM 当算法库全集。

### 八维覆盖

| 维度 | SRS | L01 草稿 | 本叶 |
|------|-----|----------|------|
| 产业链 | `…/产业链/` | 仅基础 | 图谱+深度；基础对照草稿 |
| 技术链 | `…/技术链/` | 无 | 全量；实现类 `third_party` |
| 企业 | `…/企业/` | 仅基础 | 图谱+深度；可对照 ENT 样板，仍须表1 挂 SRS seq |
| 科研机构 | `…/科研机构/` | 无 | 全量；不伪展开公式 |
| 人才 | `…/人才/` | 无 | 全量；不伪展开公式 |
| 政策 | `…/政策/` | 有 | 表1+表2 补全 |
| 产业服务 | `…/产业服务/` | 有 | 不要把 29 个 `M_SVC_*` 当本叶验收 |
| 综合 | `…/综合/` | 有 | 图谱 API + 综合分析 |

## 4. 交付文件

见 schema。字段与枚举**不要在本说明另写一套**，以 schema 为准。

无正式 `metric_id` 时用 `TEMP_ALGO_{requirement_id}_{n}`，禁止为缺口编造 `M_*` 并写入 seed。

## 5. 认领与收口

1. 唐绍祖确认后 MCP `task-claim`（`algorithm-agent` / `human:唐绍祖` / `pull`）→ `in_progress`。  
2. 未确认前不要替他认领。  
3. 交卷：schema 五件套齐（含 8/25 缺口清单）→ evidence 指向 handoff → `review`。硬截止 **2026-08-25**。  
4. handoff：`claimed_by` / `supervised_by` / `ponytail: N/A` / 架构自检 / 开放项。

## 6. `/goal`

```text
/goal
task: ALGO-LIB-METRIC-DEPS-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
claim_type: pull
repo: gkx-orchestration
task_type: spike
强度：ponytail off
理由：本叶纯文档分析，禁止砍 97 条需规对应或表2 逐输入 ODS 判定。不写业务代码。
截止：2026-08-25 必须交出三方 ODS 不满足缺口清单（confirmed none/partial）；pending_ods 不得混入该清单。
备注：必须使用 loop 工程，禁止一个提示词来做整体任务。

先读：
- 给人说明-ALGO-LIB-METRIC-DEPS-L01-2026-08-21.md
- metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md
- bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md
- metrics/indicator-inventory/2026-08-20/（只读）
- data-lineage-policy.md §2.3 D3
- calc-logic/ENT/ 仅作样板

交付（metrics/algo-results/）：
1. ALGO-LIB-METRIC-DEPS-L01-requirements.yaml
2. ALGO-LIB-METRIC-DEPS-L01-metrics.yaml
3. ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml + -ods-gaps.md  （8/25 主交付：三方不满足）
4. ALGO-LIB-METRIC-DEPS-L01-summary.md
5. ALGO-LIB-METRIC-DEPS-L01.md handoff
禁止：改 seed；写代码；混表 deps.yaml；凭 DWD 标 ODS full；把 pending_ods 写进「不满足」清单；伪展开第三方公式；做 A2；一个提示词包办整叶。
```

## 7. DoD 勾选（唐绍祖会签）

- [ ] 表1 叶子数 = 八维 README 97，无漏维  
- [ ] 每条需规有 `coverage_status` 与 `metrics[]`（0～N）  
- [ ] 每项指标有 definition、algorithm.type、formula 或 steps  
- [ ] MODEL/GRAPH 有 steps；不得只写「模型计算」  
- [ ] 每项重要输入单独有 `ods_mapping_status` + evidence  
- [ ] 指标级 `dependency_rollup` 符合 schema 汇总规则  
- [ ] 未核三方入站的输入不得标 `full`  
- [ ] 第三方行公式不伪造，inputs 仍在  
- [ ] 未改 seed、未写业务代码、未交 `*-deps.yaml`  
- [ ] summary 含八维覆盖率与 ODS 五档计数  
- [ ] **8/25**：`*-ods-gaps.yaml` + `*-ods-gaps.md` 只含已确认 `none`/`partial`；`pending_ods` 另节「待核验」  
- [ ] 每条已确认缺口写清：缺什么字段/粒度、影响哪条需规/指标、对公式的影响  

A1 通过后才 A2.1 `TOPIC-ALGO-GAP-L01`。见 [`给人说明-A2差集拆解-2026-08-21.md`](./给人说明-A2差集拆解-2026-08-21.md)。
