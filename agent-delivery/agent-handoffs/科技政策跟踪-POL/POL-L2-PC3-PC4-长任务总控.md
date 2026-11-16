# POL-L2-PC3-PC4 · 运行对比与智能研报 · 长任务总控

> **日期**：2026-11-17  
> **授权人**：`human:淮政玮`（本管线 `supervised_by`）  
> **授权状态**：编排已落盘。**还没有**「后续认领不必再问」。会签签收前不升 `ready`、不认领、不改代码。签收并写下该句之后，才按本 DAG 无人值守。  
> **目标**：广东省、市级下的珠海固态电池行动方案与深圳新型储能规划，点「运行对比」有数据，点「查看报告」是完整研报。  
> **模式**：长任务。规约：`agent-delivery/长任务执行规约.md`  
> **锁**：`lock_hours=24`。开工后 `claim_type=coordinator_dispatch`。  
> **设计**：`sdd/科技政策跟踪-系统详细设计说明书.md` #### 610

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| S0 会签 | gkx-orchestration | origin/dev | `POL-L2-PC3-PC4-FDE-L01` | 现为 `ready`。波次 A 已写入 #### 610。监管人签收前停在这里 |
| A 建表 | lumen-algo-py | origin/dev | `POL-L2-PC3-PC4-ADS-L01` | 会签签收后。现 `backlog` |
| B 写入 | lumen-algo-py | origin/dev | `POL-L2-PC3-PC4-WRITE-L01` | A 有 handoff 且 ≥ integration。同仓，排在 A 后面 |
| C 门面 | lumen-svc-platform | origin/dev | `POL-L2-PC3-PC4-API-L01` | B 满足联调闸门。不等签收 |
| D 页面 | lumen-ui-science-pc | origin/dev | `POL-L2-PC3-PC4-FE-L01` | C 满足联调闸门 |
| E 金路径 | 已发布展示 dev | — | `POL-L2-PC3-PC4-E01` | D 满足联调闸门。QA 不改代码 |

厚包：`POL-L2-PC3-PC4-总派单.md`。金路径：本文件 §4。

---

## 0. 2026-11-17 核对

能走的实现只有上面五张，外加会签这一张。各叶四单（`POL-L2-PC3-*-ARCH/API/METRIC/DATA`、`POL-L2-PC4-*` 同名）仍是 backlog，完成标准里还留着 11 月 3 日的「501」句子。备注已改为按 #### 610，**不派**。工具改不了那些完成标准原文，执行时以本总控和 #### 610 为准。

七张 `*-GAPFILL-L01` 保持 blocked。它们灌的是 `gapfill_policy_*`，不是这一行 ADS。`POL-MOCK-BTN-B06`、`B07` 也不拿来充本样本。

---

## 1. 无人值守（写下「不必再问」之后才生效）

1. `supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`，`lock_hours=24`。  
2. 已拍板不回问，见 §1.1。  
3. 结构再变（再拆表、改主键、改回 gapfill）：该叶 `blocked`，升级 `human:淮政玮`。  
4. 所选政策还没结构化或还没拆解：先走已有抽取和四个拆解 Job，再写对比行。写完仍空的那一维，页面写「这次对比没有识别出」加名字。不回退种子，不改回 501。  
5. git：只推 `origin/dev`；禁止 force；commit `[agent:<role>]`。本管线前端 `lumen-ui-science-pc` **完工即推**。  
6. 每叶 handoff、`ponytail: full`、cost 四字段。`ready_to_sign→done` 只由 `human:淮政玮` 点，积压不挡下一叶。  
7. 段 E：一张 `E01`。QA 不改代码。期望未发生必红。不逐叶派 QA，不等黄敬洲领取。  
8. 不重发 Nacos。

### 1.1 已拍板

| 项 | 结论 |
|---|---|
| 库 | `gkxlumenx_ads.ads_policy_compare_report` 一行。`utf8mb4` / `utf8mb4_general_ci`。不写 ODS、DWD、供应方库，不建 `gapfill_policy_*` |
| 调用链 | 浏览器只打 `POST/GET /display/v1/policy/compare/runs`。display 委托 Python `/internal/policy/compare-report` 写表。Java 只读 |
| 材料 | 智能政策库构建：检索、603 结构化、604「原文 → 条款 → 结论」。智能政策拆解：606 语义、607 条款、608 指标与力度、609 实体。不新注册模型，不标 501 |
| 样本 | 地区广东省，效力级别市级。珠海市固态电池产业发展行动方案（2025-2030年）；深圳市新型储能产业发展规划（2026—2030年） |
| 研报 | 同一行。深度四块、四类洞察、各章、双向溯源。PDF 与 Word 带这些正文和柱状图、雷达图、知识图谱 |
| 菜单 | 智能研报生成不加回侧栏。入口是对比记录的「查看报告」 |
| D4 | 仍是 mock。不把 D4 改绿 |
| 强度 | ponytail full |

---

## 2. 依赖

```text
FDE-L01 会签签收
  → ADS-L01 → WRITE-L01 → API-L01 → FE-L01 → E01
```

同仓一次只派一张。A 与 B 都在 `lumen-algo-py`，必须串行。解锁按规约 §6.2：前序有 handoff 且 ≥ integration，不等 `done`。

---

## 3. 开工顺序

1. 监管人签收 #### 610，并写下「后续认领不必再问」。在这之前 coordinator 停。  
2. ADS-L01 建表。  
3. WRITE-L01 对样本两份政策：缺结构化先抽，缺拆解先跑四个已有 Job，再写入完成行。  
4. API-L01 只读该行。  
5. FE-L01 运行对比和查看报告改读该行，关 mock 不留种子。  
6. E01 打已发布页面。红了按规约分类，C1 另开修单，QA 不改代码。

---

## 4. 金路径（E01）

期望未发生必红。

| # | 操作 | 期望 | 允许的空态 |
|---|---|---|---|
| 1 | 多维政策对比：广东省、市级，选中样本两份，点「运行对比」 | 四类识别、对比表、柱状图、雷达图、知识图谱、摘要、结论都有内容，对得上这两份政策 | 无。种子句算红 |
| 2 | 该行点「查看报告」 | 深度四块、四类洞察、各章正文、双向溯源都有内容，原文落在这两份政策 | 无 |
| 3 | 导出 PDF、Word | 两份文件章节相同，含上述正文和三张图。正文不出现「演示」「mock」 | 无 |
| 4 | 侧栏 | 没有「智能研报生成」菜单。停在研报页时高亮「多维政策对比」 | 无 |
