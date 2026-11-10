# POL-PC1 · 智能政策库构建（政策数据治理）· 长任务总控

> **日期**：2026-11-08  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**；**中间不要打扰**）  
> **目标**：PC-1（SRS 602–605）按 §4.1 补齐二级四单并会签收口 → 实现可调 → §6.4 用例可演行齐 → §6.5 LOOP 自动跑至样本满足  
> **模式**：长任务。规约：`agent-delivery/长任务执行规约.md` · 过程：`产品实现规程.md` §4.1 / §6.4 / §6.5  
> **锁**：`lock_hours=24`。`claim_type=coordinator_dispatch`。`supervised_by=human:淮政玮`

聊天授权原文要点：范围仅 PC-1；会签 A；604/605 跟已落盘 ARCH（D18 gapfill）；前端纳入接线并完工即推；LOOP 总控收口自动建验收+自动派 FIX+授权人代签；token 已写入本机 `%USERPROFILE%\.gkx\display-loop-token`（不进 git）；registry 本管线可 push；升级人 `human:淮政玮`。  
未在 A/B 间划掉一侧的选项，按上轮「直至所有工作完成」收口为完整管线默认值，记入本表，执行中不回问。

| 段 | 仓 | 分支 | 任务簇 | 状态门 |
|----|-----|------|--------|--------|
| S0 会签 | gkx-orchestration | origin/dev | `POL-L2-PC1-*-ARCH`×4 代签收口 | 四角色会签由授权人代签；ARCH≥integration+稿落盘 → 可升下游 ready |
| S1 二级三单 | gkx-orchestration | origin/dev | 每叶 `*-API` / `*-METRIC` / `*-DATA`×4 | 硬依赖本叶 ARCH 稿；联调闸门解锁，不等签收 |
| S2 实现 | lumen-svc-platform ·（gapfill）data · lumen-ui-science-pc | origin/dev | 门面 + gapfill 灌数 + FE 接线 | 该叶四单会签收口后；同仓串行 |
| S3 用例 | gkx-orchestration | origin/dev | 四份合规演示用例可演行 | 接口可调且库有数据后 |
| S4 LOOP | 编排+探测 | — | `POL-L2-PC1-*-DEMO-ACCEPT-LOOP` | 覆盖表无空行后自动建；自动派 FIX；授权人代签 |
| S5 段 E | devops + qa | K8s `dev` | E0 发布门 · E1 金路径 | S2 FE 联调闸门后；只认已发布前端 |

厚包：`POL-PC1-SDD-IMPL-LOOP-总派单.md` · 金路径：本文件 §4 · 缺陷包：`templates/long-task-e-defect-pack.md`

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工。  
2. **已拍板不回问**：见 §1.1。  
3. **QC / 甲方 🟡**：诚实降级，不停工等纪要。  
4. **结构歧义**（新表主键/正式库误写风险）：该叶 `blocked` + 升级 `human:淮政玮`；同段其它叶继续。  
5. **缺数据**：602/603 只读第 6 项已有结果，禁止重开 GDF；604/605 只写 `gkxlumenx_gapfill` 的 `gapfill_policy_*`，禁止写 ODS/DWD/ADS/供应方库。  
6. git：lumen / orchestration 推 `origin/dev`；禁止 force；commit `[agent:<role>]`。前端本管线 **完工即推**（废止人工确认闸，仅本管线）。  
7. 每叶 handoff + `ponytail:` + cost 四字段。`ready_to_sign→done` 由 `actor=human:淮政玮` 代签，可积压不挡主链。  
8. **会签 A**：架构/算法/数据/产品四角色会签由授权人书面代签收口；不逐人等聊天。  
9. **LOOP 收口**：覆盖核对通过后自动建验收单（视为「按 LOOP 跑」）；缺口单 ready 后自动认领派 DATA/QUERY/ALGO（视为「可以派了」）；FIX 到 ready_to_sign 后授权人代签并续轮；样本满足后代签验收单 done。注册表本管线可 commit+push。  
10. **段 E**：禁止逐叶 QA；期望未发生必红；失败分类 C1–C6；C1 派修；禁止等黄敬洲领取。  
11. token：只读本机 `display-loop-token`；401/424 → 验收单 `blocked`，停 LOOP，不自动重登（唯一允许事后找授权人的情况）。禁止把 token 写入 git / handoff / 聊天复述。

锁：`lock_hours=24`。lease 过期同监管人续领。

### 1.1 已拍板

| 项 | 结论 |
|---|---|
| 范围 | 仅 PC-1 智能政策库构建 / 政策数据治理，SRS 602–605。不含 PC-2/3/4 |
| 菜单名 | 智能政策库构建；产品名政策数据治理 |
| 调用链 | 浏览器只打 `/display/v1/policy/**` → `gkxlumen-display` → `gkxlumen-element` 读 ADS/DWD 已有结果或 gapfill。禁止浏览器打 `/topic/v1/policy`。禁止 `E-E7-POLICY-M1-L06` 当展示路径 |
| 602/603 | 跨项索引：只读第 6 项已有加工结果；资源 `GET …/governance/results`；零建表零灌数零重开 GDF |
| 604/605 | 按已落盘 ARCH：**D18 gapfill**。`gapfill_policy_lineage_index` / `gapfill_policy_indicator_lib`；接口只读表；D4 仍 mock |
| 会签 | 方案 A：授权人代签四角色收口 |
| 前端 | 纳入接线；`FE-POL-04A` 基线复用；本管线完工即推 `lumen-ui-science-pc` `origin/dev` |
| **政策选择（2026-11-08 授权人口径）** | 现实现偏全局看板，**不合理**。须**酌情增加政策选择**以体现能力，不得整页只甩规则/批次/标签树。口径见 §1.2 |
| 废作 | 不新建第二套 `FE-POL-*`；不重开政策 GDF；不把门户扶持十条当本页；不新造 `metric_id`；不把 D4 从 mock 改绿 |
| registry | 本管线 MCP 改后可 commit+push `origin/dev` |

### 1.2 政策选择（酌情 = 够核增 SRS 演示即可）

> 授权人 2026-11-08：「酌情」= **只要满足 SRS 核增部分的需求展示**；不是处处加选择器、不是重做治理工作台。对照现页（结构化 Tab 只有标签体系 + 字段映射、看不到「某份政策」）——**应加上政策的具体选择，用来体现能力已达合规水平**。

原则（少改）：

1. **保留**现有全库看板：页眉 KPI、清洗规则/批次、标签体系树、字段映射总表——这些继续证明「库级治理」。  
2. **只在需要证明「对单份政策生效」的地方**加一处政策选择（搜索下拉即可），选定后多一块「该政策结果」面板；默认带一条可演政策，避免空白。  
3. **优先落点（授权人截图标出的结构化 Tab）**：在「政策库结构化」Tab 条件栏加政策选择 → 展示该政策的结构化摘要（是否已结构化、`auto_tags`、关键标准字段取值）。**不是**拆解页条款树，**不**取代左侧标签树/右侧映射总表。  
4. **604 溯源 / 605 指标库**：同理各加一处选择（或与结构化共用同一选中政策），否则无法演示「原文—条款—结论」「该政策四维条目」。  
5. **602 清洗**：~~库级规则/批次已够核增展示则可不加~~。**已被说明书 PC-1「602」2026-11-10 取代**：选择政策多选必选，候选读 ODS 贴源，规则可启停；按《产品实现规程》§4.2 中档，架构裁定读法前不派实现。  
6. 候选来自已有政策目录读面，禁硬编码标题；参数倾向 `policyId`；同步过滤，不新开 Job。  
7. 合规用例可演行：凡依赖单政策结果的行，写明选定政策标题与 id。

---

## 2. 依赖（联调闸门）

```text
PC1-*-ARCH（稿落盘 ≥ integration）
  → 同叶 API ∥ METRIC ∥ DATA（handoff 后）
  → 会签代签收口（授权人）
  → 实现：CLEAN/STRUCT 门面读 results；LINEAGE/INDLIB gapfill+门面；FE 接线
  → §6.4 用例可演行齐
  → §6.5 LOOP（自动）
  → 段 E0 → E1
```

废作施工：不为 604 等 `GDF-POLICY-LINEAGE-L01`；不把 `M_POLICY_VALIDITY_RATE` / `M_POLICY_BASE_100_1` 改挂治理 KPI；不复用研报 617 表。

---

## 3. 开工顺序

1. 落盘本总控 + 总派单；token 本机就位。  
2. ARCH×4 会签包代签 → 升 API/METRIC/DATA ready 并派写（可与会签文书并行，稿齐即写）。  
3. 四叶三单 handoff 齐 → 代签 → 拆/升实现叶。  
4. 同仓一次一张 coding；跨仓可并行。  
5. 接口可调后写/补四份合规演示用例；覆盖无空行 → 自动 LOOP。  
6. FE 联调闸门 → E0 → E1。

卡住只允许：真环境不通、token 失效、正式库误写风险、结构升级、E/LOOP 超 3 轮同缺口、cost 硬闸。

---

## 4. 金路径（段 E1）

> **期望未发生必红**。空态只有写进本行才算过。

| # | 故事 | 已发布路由 | 期望（未发生=红） | 允许的空态 |
|---|------|------------|-------------------|------------|
| 1 | 602 清洗看板 | 智能政策库构建 · 清洗 Tab | `GET …/governance/results` 200；规则/批次全库可见即可（政策选择非强制） | 无加工结果 → 空，不造 0 |
| 2 | 603 结构化（核增演示主点） | 同上 · 结构化 Tab | 保留标签树+映射总表；**加政策选择**后出现该政策结构化摘要（达合规水平的体现） | 无该政策结构化 → 摘要空 |
| 3 | 604 溯源 | 同上 · 溯源 Tab | 政策选择（可与 603 共用选中项）；`lineage-index` 200 | 该政策无行 → 空 |
| 4 | 605 指标库 | 同上 · 指标库 Tab | 同上；`indicator-library` 200 | 该政策无行 → 空 |
| 5 | 页眉件数 | 治理页眉 | `M_POLICY_TOTAL_COUNT`；不随选择改口径 | 无数则附卡空 |

P1 不挡闭环：基库构建开关演示态、批次窗口外提示、与专题/门户分轨横幅文案微调。
