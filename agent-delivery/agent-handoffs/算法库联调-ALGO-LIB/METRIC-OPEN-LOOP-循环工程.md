# METRIC-OPEN ×16 + A2 返工 · 循环工程

> **日期**：2026-08-22  
> **监管 / 认领**：`human:淮政玮`（16 叶已 `claimed`，锁 72h）  
> **模式**：与 A1 相同 — **一叶一智能体**，禁止一个提示词包办 16 份核对记录。可 **5～10 叶并行**（各写各的核对记录 / 机器卡 / `{ID}-a2-patch.yaml`）。**禁止**并行写共享的 `LOOP-state.yaml` 与 `METRIC-OPEN-LOOP-a2-patch.yaml`（由 coordinator 合流）。A2 返工仍必须等 OPEN 齐。  
> **状态机**：[`metrics/request/_work/METRIC-OPEN-LOOP-state.yaml`](../../metrics/request/_work/METRIC-OPEN-LOOP-state.yaml)

**一句话**：先用 SRS/详细设计顶 PACK 把 16 张 OPEN 的 ④⑤ 写齐（OPEN 阶段可用 `TEMP_*` 占位），再用这些路径把 A2 两叶从「缺 OPEN 叶」改成「语义层已挂上」；库未覆盖的 `missing` **保持**。**2026-08-22 淮政玮：`TEMP_*` 不是终态** — 紧接着跑 [`METRIC-ID-ASSIGN-LOOP-循环工程.md`](./METRIC-ID-ASSIGN-LOOP-循环工程.md) 赋正式 `M_*` + 建议 `algorithm_type` + Question。

```text
Round 1–7   专题 OPEN（含 ZHIKU 补登记）
Round 8–16  展示态势 DS-01…09
Round 17    返工 TOPIC-ALGO-GAP-L01   ← 必须等 1–7 全 done
Round 18    返工 DS-ALGO-GAP-L01      ← 必须等 8–16 + Round 17
```

POLICY **不在这 16 张里**。A2 `E7-POLICY` 返工时直接挂已有 `METRIC-OPEN-E7-DS10-12-核对记录.md`（DEBT 已写指针）。SYNTH 三兄弟已有 OPEN，catalog 只改挂，不新写。

---

## 0. 铁律

| 做 | 不做 |
|----|------|
| 每轮只碰 **一张** OPEN 叶 | 一轮写 16 份 md |
| 每轮结束更新 `LOOP-state.yaml` 该 round = `done` | 攒到最后才落盘 |
| ④ 适用则语义卡；不适用 **N/A+依据** | 口头 N/A；编造正式 `M_*` 进 seed |
| `owner_semantic=human:淮政玮`；公式/`algorithm_type` 标 `pending_cosign: human:唐绍祖` | 替唐绍祖签公式；8/25 前派唐绍祖开工本 loop |
| A2 返工只改 **指针 + 分类**（缺 OPEN → present） | 把 A2 `missing`（库缺口）改成 mapped 来「好看」 |
| 专题企业 **禁止**消费 `M_ENT_*` / `ENT-MOD-*` OPEN | 另开 `TOPIC-POLICY-METRIC-OPEN-L01` |
| `cicd: skip`；不改 `metrics/registry/` seed | 复活 INVENTORY/CLASSIFY；挡 A1 |

---

## 1. 一轮（OPEN）标准动作

对 `state.yaml` 里 **第一个 `status: pending` 的 OPEN round**：

1. MCP `task-update-status` → `in_progress`（仅本叶）。
2. 读本叶 `design_refs` + 对应 `metrics/request/{专题\|展示系统}/pages/{page_id}.yaml` + SRS/05.x。
3. 写 **核对记录**（路径见下表）。样板：`METRIC-OPEN-E7-DS10-12-核对记录.md` 的 §1 适用性表 + 消费矩阵。ZHIKU 只补会签栏，不从零写。
4. 写机器卡 `metrics/request/_work/open-loop/{TASK_ID}.yaml`（schema 见 §3）。
5. 把本叶将回写 A2 的指针 **追加**到 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`（只追加，不改 A2 正文，直到 Round 17/18）。
6. 薄 handoff：`agent-handoffs/算法库联调-ALGO-LIB/{TASK_ID}.md`（认领淮政玮 / ponytail N/A / cicd skip / cost 估）。
7. MCP：`task-update-fields` evidence；`note` 含 `会签通过`（口径草稿；公式 pending）；状态先留 `in_progress`（coordinator AV）。`LOOP-state` 本 round → `done`，`current` → 下一 id。

**本轮退出**：核对记录存在 + 机器卡 `pages[]` 非空 + patch 行已追加 + 未改 seed。缺一项不准进下一 round。

---

## 2. 16 叶顺序（禁止打乱：先专题后态势）

| Round | Task ID | 核对记录路径 | 消费的 A2 `page_id` |
|------|---------|--------------|---------------------|
| 1 | `SVCCHAIN-METRIC-OPEN-L01` | `agent-handoffs/产品整体定义/E7-产业服务链分析/METRIC-OPEN-SVCCHAIN-核对记录.md` | `SVCCHAIN-ORG-ANALYSIS` / `ECOSYSTEM` / `RECOMMEND` / `PORTAL` |
| 2 | `TOPIC-ENT-METRIC-OPEN-L01` | `…/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-ENT-核对记录.md` | `TOPIC-ENT-05`（禁挂展示 ENT） |
| 3 | `TOPIC-TECH-METRIC-OPEN-L01` | `…/METRIC-OPEN-TOPIC-TECH-核对记录.md` | `TOPIC-TECH-05` |
| 4 | `TOPIC-ORG-METRIC-OPEN-L01` | `…/METRIC-OPEN-TOPIC-ORG-核对记录.md` | `TOPIC-ORG-05` |
| 5 | `TOPIC-TALENT-METRIC-OPEN-L01` | `…/METRIC-OPEN-TOPIC-TALENT-核对记录.md` | `TOPIC-TALENT-05`（勿混 DS-13～16） |
| 6 | `TOPIC-QUERY-METRIC-OPEN-L01` | `…/METRIC-OPEN-TOPIC-QUERY-核对记录.md` | `TOPIC-QUERY` |
| 7 | `ZHIKU-METRIC-OPEN-L01` | 已有 `…/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md`（补栏） | 智库页若在 A2.2 catalog 则挂；无则只补登记 |
| 8–16 | `DS-0N-METRIC-OPEN-L01` | `…/产品整体定义/METRIC-OPEN-DS-0N-{短名}-核对记录.md` | 展示 catalog `ds_id=DS-0N` 全部 `page_id` |

态势短名：01 全域态势 / 02 科学技术全景 / 03 技术发展跟踪 / 04 全球创新监测 / 05 湾区 / 06 深圳创新监测 / 07 科技创新评估 / 08 科技指数 / 09 科技发展规划。

---

## 3. 机器卡 schema（每叶一份）

```yaml
task_id: SVCCHAIN-METRIC-OPEN-L01
owner_semantic: human:淮政玮
formula_cosign: pending   # human:唐绍祖
srs_tops_pack: true
pages:
  - page_id: SVCCHAIN-ORG-ANALYSIS
    metric_open_status: present   # 禁止再写 missing 表示「缺 OPEN 叶」
    metric_open_path: agent-handoffs/产品整体定义/E7-产业服务链分析/METRIC-OPEN-SVCCHAIN-核对记录.md
    metric_open_task: SVCCHAIN-METRIC-OPEN-L01
    kit_or_na: kit | na_with_reason
    demands: []   # 有统计则列 TEMP_ 或已有 M_*；禁止新编正式 M_*
a2_gap_note: >
  本叶闭合的是语义层。库未覆盖的行仍 missing，不得因 OPEN 存在而改 mapped。
```

---

## 4. Round 17–18 · A2 返工（在 OPEN 结果之上）

两叶现网已 `needs-revision`（淮政玮指定不签收旧版）。

**Round 17 `TOPIC-ALGO-GAP-L01`**

读 `_work/METRIC-OPEN-LOOP-a2-patch.yaml` + `专题系统/A2-GAP-page-catalog.yaml` + 各 `pages/*.yaml`。

只改这些：

1. catalog：`metric_open_status: present`；填 `metric_open` / `metric_open_task`；删「无 METRIC-OPEN → 只记语义欠账」中已被 16 叶覆盖的句。
2. `E7-POLICY`：挂 `METRIC-OPEN-E7-DS10-12-核对记录.md` + `POLICY-METRIC-OPEN-L01`（DEBT §1.2）。**禁止**再写「勿用展示政策 OPEN」。
3. `SYNTH-REGION`：注明父索引，三兄弟已有 OPEN，不另建叶。
4. 页 yaml `semantic_layer`：与 catalog 同指针。`TOPIC-ENT-05` 仍 **禁止** `M_ENT_*`。
5. 差集列 11：`semantic_debt` 里「缺 OPEN 叶」→ 改为有指针；**库缺口 `missing` 不动**。
6. 重写 `专题系统/` summary 计数：缺 OPEN 叶 vs 库 missing 分开。
7. 不覆盖根目录半成品 xlsx；yaml 为机器真源，xlsx 能改则改（给人）。

**Round 18 `DS-ALGO-GAP-L01`**

1. 必须先有 Round 17 `done`。
2. 展示 catalog DS-01…09 挂 9 份态势核对记录。
3. 专题已记的 `missing` **不重列**。
4. 人才 DS-13～16 **仍缺 OPEN 叶**（本批未建）→ 继续诚实 `missing`/欠账，勿跟 `TOPIC-TALENT` 混。
5. 不签收；handoff 写清「相对旧版 diff：指针 / 计数」。

---

## 5. 会话怎么开（一气呵成）

同一 product-agent 会话，系统提示只固定本文件 + state。每轮用户或 coordinator 只说：

```text
LOOP-NEXT
```

执行体读 `current`，做完一轮停 30 秒自检退出标准，再自己 `LOOP-NEXT`，直到 Round 18。  
**禁止**第一轮就把 16 份核对记录一起生成。卡死就写 `LOOP-state` 该 round = `blocked` 原因，停。

完成后 coordinator：16 OPEN AV-0；A2 两叶仍 `needs-revision` 直到你再签。
