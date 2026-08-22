# METRIC 赋号 + Question · 循环工程

> **日期**：2026-08-22  
> **拍板**：`human:淮政玮`（口径 / `metric_id` / 适用性 / 内部默认）  
> **公式仍未签**：`human:唐绍祖`（8/25 前不派他开工本 loop）  
> **状态机**：[`metrics/request/_work/METRIC-ID-ASSIGN-LOOP-state.yaml`](../../metrics/request/_work/METRIC-ID-ASSIGN-LOOP-state.yaml)  
> **上游**：16 张 OPEN 核对记录（`TEMP_*` 占位）已齐。本 loop **不再把 `TEMP_*` 当终态**。

**一句话**：把 OPEN 卡面上的 `TEMP_*` 升成正式 `M_*`（或复用已有同口径 ID），每条带 **建议 `algorithm_type`（未签）**；口径有歧义则推理并写默认，进 Question 表（🟡）。然后整包交给算法轨签公式。

```text
Wave A   专题 5 叶（ENT/TECH/ORG/TALENT/QUERY）+ 态势 DS-01…05
Wave B   DS-06…09 + ZHIKU（非 🔴）
Skip     SVCCHAIN（已是 M_SVC_*）；CHAIN / SYNTH / POLICY / 展示 ENT 已有正式 ID 的不重赋
```

并行：一叶一智能体，最多 10。**禁止**并行写共享 `LOOP-state`、总赋号 catalog、`METRIC-SEMANTIC-QUESTIONS.md`、`客户决策清单跟踪表.md`（coordinator 合流）。

Round 18 `DS-ALGO-GAP-L01` 若仍在改 `展示系统/` catalog，本 loop **禁止**写展示 catalog / pages 正文（只改核对记录、机器卡、`id-assign/`）。

---

## 0. 铁律

| 做 | 不做 |
|----|------|
| `TEMP_*` → 正式 `M_*` 或 **复用**已有同口径 `M_*` | 把 `TEMP_*` 留作页面终态 |
| 建议 `algorithm_type` 写在赋号卡里，标 `suggested_unsigned` | 替唐绍祖签类型；标 `D1=aligned` |
| 歧义：检索/推理 → **选一个默认** → Question 🟡 | 把歧义留成「语义债」不赋号 |
| 先 MCP `metric-query` 防撞号 | 与 seed 已有 ID 撞名却不同口径 |
| 专题企业：**同口径才**复用 `M_ENT_*`；不同口径用 `VARIANT=TOPIC` | 把展示企业门户 60 个 ID **整页改挂**为本页唯一消费 |
| 专题人才 **不**改挂展示 DS-13～16（本批无 OPEN） | 混 `TOPIC-TALENT` 与 `DS-13*` |
| 库缺口 `missing` 保持 | 因赋号把 A2 列 11 改 mapped |
| 身份草稿可写核对记录 / `id-assign/` | **改 seed 口径/公式/源表**（8/25 A1 窗口）；把建议类型写入 seed 当已签 |

---

## 1. 命名（`data-lineage-policy.md` §3）

```
M_{ELEMENT}_{INDICATOR}_{PERIOD?}_{VARIANT?}
```

ELEMENT：`ENT` / `CHAIN` / `ORG` / `TECH` / `TALENT` / `SVC` / `POLICY` / `SS` / `IC` / `INNOV` / `COMMON`。

本 loop 默认：

| 叶 | ELEMENT | 备注 |
|----|---------|------|
| TOPIC-ENT | `ENT` | 同口径复用展示 `M_ENT_*`；不同口径 `…_TOPIC` |
| TOPIC-TECH | `TECH` | 与 DS-02 同口径则复用，不另造 |
| TOPIC-ORG | `ORG` | 禁止改挂 `M_SVC_ORG_*` 顶替专题科研机构 |
| TOPIC-TALENT | `TALENT` | 不混 DS-13～16 |
| TOPIC-QUERY | `COMMON` 或按图种要素 | BI 聚合在当前结果集上，差集仍 other_system |
| DS-01…09 态势 | `INNOV`（监测/指数/规划）或 `TECH`/`IC`（全景/路径） | 城市/湾区/深圳排名与 `M_SYNTH_*` 同口径才复用，禁止改挂 |
| ZHIKU 非 🔴 | `COMMON` 或保持可追溯前缀 | 四枚 🔴 **不得转正** |

禁止：中文 ID、拼音业务名、同一口径两套 ID（policy §3.4）。

---

## 2. `algorithm_type` 建议规则（未签）

枚举：`STAT` / `COMPUTE` / `MODEL` / `GRAPH` / `third_party` / `MIXED` / `LITERATURE`。本 loop **禁止**写 `UNKNOWN` 当建议（给不出建议就标 `MIXED` + Question）。

| 页上实际在算什么 | 建议 |
|------------------|------|
| 计数、占比、排名、简单分布 | `STAT` |
| 加权 / 标准化 / 阈值 / 指数合成（无训练） | `COMPUTE` |
| 评分、预测、聚类、适配、潜力、痛难点 | `MODEL` |
| 中心性、路径、子图、关系网 | `GRAPH` |
| 九新/外采人才机构技术 | `third_party` |
| 上列组合且拆不开一条 ID | `MIXED` + 拆子项进 Question |
| 文献指数、无现成公式 | `LITERATURE` |

字段名：`algorithm_type_suggested`。另写 `algorithm_type_reason`（一句话）。**不得**写成已会签。

---

## 3. Question

- 工作底稿（本 loop 真源）：[`metrics/request/_work/METRIC-SEMANTIC-QUESTIONS.md`](../../metrics/request/_work/METRIC-SEMANTIC-QUESTIONS.md)
- 叶级：`metrics/request/_work/id-assign/{TASK_ID}-questions.yaml`（并行只写这个）
- 合流后 coordinator 再 append 进 `客户决策清单跟踪表.md`（Q072+；叶级先用 `Q-MO-{短码}-{nn}`）
- 状态一律 🟡（内部默认，待甲方）。禁止升 🟢。
- 无歧义（计数窗口=自然年、对象=名录去重等常识）**不必**造 Q，在赋号卡 `pending_ref: null`。

短码：`ENT` `TECH` `ORG` `TALENT` `QUERY` `DS01`…`DS09` `ZHIKU`。

---

## 4. 一轮标准动作

1. 读本叶 OPEN 核对记录 + `open-loop/{TASK_ID}.yaml` 的 `TEMP_*`。
2. MCP `metric-query`：同中文名 / 近义是否已有 `M_*`。
3. 逐条赋号：复用或新建；写口径草稿（内部默认）；写建议类型。
4. 有歧义 → 叶级 questions.yaml（选项 + 默认 + 推理依据，可检索）。
5. 回写核对记录 **§赋号表**（TEMP → M_* → 建议类型 → Q 或 —）。机器卡 `demands:` 换成 `M_*`（可保留 `temp_id` 对照字段）。
6. 写 `metrics/request/_work/id-assign/{TASK_ID}.yaml`（schema 见下）。
7. 薄 handoff 追加段：赋号份数 / 复用份数 / Q 份数 / 建议类型分布。
8. MCP `task-update-fields` note 含「赋号草稿；类型未签」。**不**改 OPEN 叶为 done。不写 seed。

---

## 5. 叶级赋号卡 schema

```yaml
task_id: TOPIC-ENT-METRIC-OPEN-L01
owner_semantic: human:淮政玮
formula_cosign: pending
algorithm_type_status: suggested_unsigned
items:
  - temp_id: TEMP_TOPIC_ENT_TYPE_DIST
    metric_id: M_ENT_TYPE_COUNT          # 复用或新号
    reuse_of: M_ENT_TYPE_COUNT           # 无则 null
    metric_name_zh: 企业类型分布计数
    definition_draft: "…"                # 内部默认口径
    algorithm_type_suggested: STAT
    algorithm_type_reason: 名录去重计数
    page_ids: [TOPIC-ENT-05]
    pending_ref: null                    # 或 Q-MO-ENT-01
```

---

## 6. 交给算法轨的包（loop 齐后 coordinator 汇编）

`metrics/request/_work/METRIC-ID-ASSIGN-handoff-to-algo.md`：

- 全量 `M_*` + 中文名 + 口径默认 + `algorithm_type_suggested` + `pending_ref`
- 明确：**类型与公式均未签**；唐绍祖可改类型
- 不替代 A1 97 叶；A1 仍 8/25 硬路径

---

## 7. 退出标准（一叶）

核对记录有赋号表 + 叶级 `id-assign/{ID}.yaml` 条数 = 原 `TEMP_*` 数（或明示废弃）+ 每条有建议类型 + 未改 seed + 未改展示 catalog。
