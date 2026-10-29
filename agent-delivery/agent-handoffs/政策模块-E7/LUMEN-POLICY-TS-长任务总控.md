# 政策时序分析口径与关联闭环 · 长任务总控（无人值守）

> **日期**：2026-10-24  
> **授权**：2026-10-24 对话确认本段表（回复「确认」）。监管人 `human:淮政玮`。授权句：后续认领 **不必再问**。  
> **目标**：`/policy/overview` 的时序结果与过程页按本文件口径可复核。样本锚点「高性能与前沿新材料」（`chain:INB170401`），对照任务 `POLICY-20261024-005`。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **不重开**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)、[`POLICY-GRAPH-CHAIN-长任务总控.md`](./POLICY-GRAPH-CHAIN-长任务总控.md)  
> **执行 agent 按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| A | `gkx-orchestration` | `origin/dev` | `LUMEN-POLICY-TS-CALIBER-L01` | 口径以本文 §0 为准。本叶只核对差异表无遗漏并写 handoff |
| B1 | `lumen-algo-py` | `origin/dev` | `LUMEN-POLICY-TS-BOARD-L01` | A 有 handoff 且 ≥ integration |
| B2 | `demo-algo-ent-analysis` | `origin/dev` | `LUMEN-POLICY-TS-REL-L01` | 与 B1 并行。只抽样校准，不重跑 2 万条 |
| C | `lumen-svc-platform` | `origin/dev` | `LUMEN-POLICY-TS-NAME-L01` | B1 联调闸门后 |
| D | `lumen-ui-topic` | `origin/dev` | `LUMEN-POLICY-TS-FE-L01` | C 联调闸门后。同仓同时只派一张；`LUMEN-POLICY-D-POL-01-L01` 过期锁未释放前本叶不认领 |
| E | qa（只点已发布前端） | K8s `dev` | `LUMEN-POLICY-TS-E-QA-L01` | D 与 B2 都达联调闸门。B2 仍有明显错配则本叶记关联未过，不得改时序公式掩盖 |

厚包：本文件即各段派单依据（不另写六份总派单）。金路径：§4。缺陷包：[`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)

---

## 0. 已拍板（落盘即生效 · 执行勿问）

| # | 议题 | 决定 |
|---|------|------|
| 1 | 范围 | 只改政策时序 `/policy/overview`。不改区域对比、深圳三维、政策查询、入图 |
| 2 | 调用链 | 前端 → Java `gkxlumen-topic-async-service` → Python `/internal/policy/jobs/execute`。时序不在 Job 里做第二次产业匹配 |
| 3 | 数仓 | 继续 `demo_gkxlumenx_*`。禁止为本轮改正式 `gkxlumenx_*` |
| 4 | 关联集合 | `ads.policy_industry_rel`：`is_deleted=0` 且 `industry_link_code` 等于锚点 VID。条数即政策总数 |
| 5 | 错配 | 甘肃新型研发机构、安康创新挑战赛进「高性能与前沿新材料」属抽取产业错配。B1 禁止用标题关键词把它们滤掉。B2 只按 [`industry-match-optimize.md`](../../data/data-design/storage/POLICY/etl/industry-match-optimize.md) 抽约 50 条校准 0.55 / 0.45，并复核对账 `chain:INB170401` |
| 6 | 密度 | `M_POLICY_TIMESERIES` 的正式含义是各年发布量 + 环比 + 连续性，不是一个末年条数。卡片改名为「最近一年发布量」，值 = 跨度最后一年的 `publish_count`（无跨度则空）。趋势图仍展示各年发布量。禁止再标「政策密度指数」 |
| 7 | 增长率 | `(本期-上期)/上期×100`。取最近一个发布量 > 0 的年份相对上一日历年。上一年为 0 或没有上一年时，值为空，界面「—」。禁止显示成 0 |
| 8 | 有效占比 | `status=1` 且（`expire_date` 为空或 ≥ 今天）的条数 / 总数 × 100，保留两位。`status` 为空不算有效。总数为 0 时卡片为空 |
| 9 | 匹配对象 | 结果包 `match_object` 用产业中文名。创建参数带 `industry_name`。没有中文名才退回 VID |
| 10 | 渠道 | 「国家部委、地方政府」仍是页面说明，本轮不做 SQL 过滤。省级科技厅保留在结果里 |
| 11 | 过程页 | 「分析类型」显示「政策时序分析」。四步是能力说明，不是四个已执行节点。不把 Java `totalNodes` 改成 4。任务名继续等于任务 ID |
| 12 | 算子 | 不改 `polan/basic/indicators.py` 的 `run()`。只改在线结果板 `timeseries_board`。窗口期规则、支持力度关键词本轮不改 |
| 13 | 监管 | `supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`，`lock_hours=24` |
| 14 | 抽取写入方 | B2 先确认 `chain:INB170401` 的关联行是 demo 抽取写入。若发现 lumen 侧还有第二套写入，该叶 `blocked`，不猜着改 |

临时口径与正式 8 件套不一致处（密度卡片改名、有效判定收紧到 `status=1`）界面保持 ⓘ，不改 seed、不把口径改绿。QPOL-02 权重本轮不动。

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工。  
2. **已拍板不回问**：§0。  
3. **甲方 🟡**：密度指数的归一化定义未拍板。本轮用「最近一年发布量」诚实展示，不停工等纪要。  
4. **结构歧义**（给 `policy_industry_rel` 加列、改门槛以外的新表）：该叶 `blocked` + 升级 `human:李伟`。  
5. **缺数据**：读空则结果空态。禁止无闸门写正式库。B2 不重跑 2 万条。  
6. git：`origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 每叶 handoff + `ponytail: full`（A 为定义叶，`ponytail: N/A`）+ cost 四字段。签收可积压。  
8. **段 E**：QA 不改代码。只点已发布 `http://10.50.69.111:30892`。期望未发生必红。失败先 C1–C6。不等黄敬洲领取。

锁：`lock_hours=24`。lease 过期则同一监管人续领，不改 §0。

---

## 2. 依赖（联调闸门，不等签收 `done`）

```text
A CALIBER（本文 §0 差异表核对）
  ├→ B1 BOARD（timeseries_board）
  │    → C NAME（industry_name → match_object）
  │         → D FE（过程页类型名、匹配对象、KPI 文案）
  └→ B2 REL（50 条抽样 + INB170401 对账）──┐
                                          ├→ E QA
                         D 联调闸门 ──────┘
```

废作施工（不要派、不要当依赖）：

| ID / 路径 | 原因 |
|-----------|------|
| `E-E7-POLICY-M1-L03`～`L07` | ABCDE 总控已废 |
| `LUMEN-POLICY-D-POL-02-L01` | 结果板骨架已在仓内。registry 无此 ID。本轮不补登记、不重做骨架 |
| 重跑 2 万条抽取 | B2 只抽样 |
| 改 `indicators.run()` | §0 #12 |
| 把错配标题在时序 SQL 里滤掉 | 掩盖关联质量 |

`LUMEN-POLICY-D-POL-01-L01` 仍是 `in_progress`，锁到 2026-09-03 已过期。本轮不改它的范围。段 D 认领前由 coordinator 释放该过期锁或确认同仓无在途提交。未处理前不派 `LUMEN-POLICY-TS-FE-L01`。

---

## 3. 开工顺序

1. A 升 ready 后认领。对照 §0 写差异表 handoff，不改公式。  
2. A 达联调闸门 → 同时派 B1、B2（不同仓）。  
3. B1 闸门 → C → D。D 受 §2 的同仓锁约束。  
4. D 与 B2 都达联调闸门 → 点名相关部署绿 → E。  
5. E 用「高性能与前沿新材料」手跑 §4。B2 对账仍有明显错配：金路径第 3 条红，不回改 B1 公式。

卡住只允许：demo 与 lumen 两套写入对不上、正式库误写风险、给关联表加列、E 超 3 轮 / cost 硬闸。

---

## 4. 金路径（段 E1 · 只点已发布前端）

已发布前端：`http://10.50.69.111:30892`。路由 `/policy/overview`。环境禁止 localhost。QA 不改代码。

锚点：产业集群下的 L0「高性能与前沿新材料」，VID `chain:INB170401`。点「开始分析」。成功后必须点「查看分析结果」才进结果。

| # | 故事 ID | 期望（未发生=红） | 允许的空态 |
|---|---------|-------------------|------------|
| 1 | `US-E7-POL-02` | 进入过程页。分析类型是「政策时序分析」，不是 `POLICY-*` 编号。成功后不自动跳结果 | 无 |
| 2 | `US-E7-POL-02` | 关联条数等于该 VID 在 `policy_industry_rel` 的有效行数。匹配对象列是中文名 | 关联 0 条时列表空态，且总数卡片为 0 |
| 3 | `US-E7-POL-02` | 抽查标题不得再把与该产业无关的规章算进结果。B2 对账仍错则本条红 | 无 |
| 4 | `US-E7-POL-02` | 四张卡为：政策总数、最近一年发布量、年度增长率、有效政策占比。值能按 §0 #6–#8 用结果列表手算复核。上一年发布量为 0 时增长率是「—」 | 无跨度时「最近一年发布量」为空 |

P1 不挡：报告导出、窗口期阈值、支持力度关键词、渠道 SQL。
