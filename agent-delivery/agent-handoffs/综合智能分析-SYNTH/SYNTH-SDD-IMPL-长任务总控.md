# SYNTH SDD v1.0.4 落地 · 长任务总控（无人值守）

> **日期**：2026-11-05
> **授权**：`human:徐滕强`（本管线监管人；后续认领**不必再问**；用户原话「可以，那开始吧」「中间不要打扰我」）
> **目标**：按 `sdd/`（v1.0.4-draft，已推 origin/dev `8a5378cb`）会签 → 三叶真链代码完成至联调闸门 → 段 E 冒烟
> **模式**：长任务；`claim_type=coordinator_dispatch`；规约：`agent-delivery/长任务执行规约.md`
> **设计真源**：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/`（总册 + 三 L2 + reconciliation）；辅以 `API-SYNTH-INTEL-REPLICA-PLAN.md`、`LUMEN-INTEL-MOCK-INV-L01.md`、`LUMEN-INTEL-实现方案.md`

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| A 会签 | gkx-orchestration | origin/dev | `LUMEN-INTEL-SDD-SIGNOFF-L01` | 四方会签 → done 后解锁 B/C/D DDL |
| B 活力 | lumen-svc-platform | origin/dev | `LUMEN-INTEL-VIT-FP-SNAP-L01`（增量；存量 VIT 五单+BE-1 续跑不重开） | SIGNOFF done |
| C 要素 | lumen-algo-py / lumen-svc-platform / lumen-ui-topic | origin/dev | `ELEM-DDL → ELEM-PY → ELEM-BE → ELEM-FE` | DDL 等 SIGNOFF；下游联调闸门解锁，不等签收 |
| D 协同 | 同上 | origin/dev | `COLLAB-DDL → COLLAB-PY ∥ COLLAB-GRAPH → COLLAB-FE` | 同上；GRAPH 预填即可开工 |
| E 解锁 | 各仓 | origin/dev | `FOURDIM-OPEN → FOURDIM-DDL → FOURDIM-WIRE`；`COLLAB-C05-SRC` | backlog；条件满足由 coordinator 以徐滕玮授权升 ready 领跑 |
| F 段 E | devops + qa | K8s `dev` | `SDD-E0`（发布门）· `SDD-E1`（金路径冒烟） | P0 叶全部联调闸门后；只认已发布前端 |

厚包：本文件 + `sdd/` 全套 · 金路径：本文件 §4 · 缺陷包：`templates/long-task-e-defect-pack.md`

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:徐滕强`，`claim_type=coordinator_dispatch`；升 ready 后直接认领开工。
2. **已拍板不回问**：调用链 FE→gateway→Java→Python `/internal/*`；库 `gkxlumenx_ai` + `gkxlumenx_gapfill`；分支一律 `origin/dev`；`snapshotId` 不可变 ≠ `cache_key`；`legacy_unknown` 禁复用；协同 `batch_meta` 持久；137② 解锁前 `[]+reason`；C-05 真值 blocked、预填先行。
3. **QC / 甲方 🟡**：诚实降级，不停工等纪要（Q-SYNTH-* 全部按临时默认跑，UI 带 ⚠️）。
4. **结构歧义**：该叶 `blocked` + 升级 `human:李伟`；同段其它叶继续。
5. **缺数据**：禁止无闸门写正式 `gkxlumenx_*`；读空则空态；`USE_MOCK=false` 禁 fixture。
6. git：commit `[agent:<role>]`；禁止 force push；`git reset --hard` 禁令（多会话保护）。
7. 每叶 handoff + `ponytail:` + cost 四字段；`ready_to_sign→done` 由 coordinator 以 `actor=human:徐滕强` 代签（本总控授权），可积压不挡主链。
8. **段 E**：禁止逐叶 QA；E0→E1；QA 不改代码；**期望未发生必红**；红了先失败分类 C1–C6；C1 由 coordinator 派修（分诊无提交权）；点名 deploy 绿 = E0 → 复测失败故事。禁止等聊天、禁止等黄敬洲领取。

锁：`lock_hours=24`；lease 过期同监管人续领。

---

## 2. 依赖（联调闸门）

```text
SDD-SIGNOFF(done)
  ├─ VIT-FP-SNAP（活力存量链并行续跑）
  ├─ ELEM-DDL → ELEM-PY → ELEM-BE → ELEM-FE
  └─ COLLAB-DDL → COLLAB-PY ∥ COLLAB-GRAPH → COLLAB-FE
全 P0 叶联调闸门 → E0 → E1
（并行解锁，条件触发）FOURDIM-OPEN → FOURDIM-DDL → FOURDIM-WIRE；C05-SRC 独立
```

废作施工（不要派、不要当依赖）：不为 lumen 平行新开 FE-REPLICA 壳单；不新建 Python 服务；不把 `TOPIC-SYNTH-R3`（demo 闭环）当 lumen 依赖；Java 不写算法；前端不直连 demo 服务。

---

## 3. 开工顺序

1. 建单（16 张）→ commit + push registry。
2. 派 ① 会签（arch）→ done（徐滕强签）→ 升 B/C/D 首叶 ready。
3. 同仓一次只派 1 张 coding；跨仓可并行（algo-py 线与 svc-platform 线互不撞文件）。
4. 每叶：claim → in_progress → 子智能体执行 → handoff → AV-0/AV-1 → 联调闸门 → 下游 ready。
5. 解锁条件出现（唐绍祖 METRIC-OPEN 定稿 / C-05 贴源）→ 对应单升 ready 派工。
6. P0 叶全联调 → E0 → E1 → 失败分类处理。

卡住只允许：真环境不通、正式库误写风险、结构歧义升级、E 超 3 轮、cost 硬闸（>$10 停叶复盘 / >$20 hard stop）。

---

## 4. 金路径（段 E1 · SDD-E1 用）

> **期望未发生必红**。空态只有写进本行才算过。失败分类见规约 §11.4。

| # | 故事 | 已发布路由 | 期望（未发生=红） | 允许的空态 |
|---|------|------------|-------------------|------------|
| 1 | 活力秒开 | `/intelligence/vitality` | 默认三元组快照 200 同构；换 `weight_profile` 不复用他档/legacy 任务 | 404 → 引导「开始分析」 |
| 2 | 活力任务 | vitality 任务过程页 | create→running→succeeded；`resultData` 同构；`snapshotId` 含批次 | failed 显示 reason |
| 3 | 要素三透镜 | `/intelligence/elements` | 类型/层次/领域接真表有数 | — |
| 4 | 要素四维 | 同上 | 解锁前：`[]`+`reason='metric_not_registered'` + 页面红问号，无演示数 | 仅缺失态 |
| 5 | 协同图谱 | `/intelligence/collaboration` | 默认三元组图谱 nodes/edges 非空无重复；带 `snapshotId` | — |
| 6 | 协同坏快照 | 同上 | 指定不存在/无 meta 的 `snapshotId` → 不可用（`batch_meta_missing`），不串最新批 | — |
| 7 | 报告页 | 三叶 report | 前端真快照渲染 PDF，无 fixture | 快照缺失不伪造 |

P1 不挡闭环：136 全景深化、141 策略审核流、`*_report` 任务键。
