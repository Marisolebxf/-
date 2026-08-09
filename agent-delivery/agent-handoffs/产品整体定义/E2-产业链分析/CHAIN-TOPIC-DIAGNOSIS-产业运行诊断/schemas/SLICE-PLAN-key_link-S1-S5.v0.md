# SLICE PLAN · key_link S1～S5 谁先开工（v0）

> 基于 `GRAPH-key_link.v0.md` §7。  
> **结论先行**：先开工的不是 S5（LLM），而是 **Runtime 竖切 + S1**；算法与 Java/前端可错峰并行。

---

## 1. 推荐总序（依赖）

```text
[并行轨 A] Java Runtime 最小集：Create / Execute / Stage / Complete / GetJob
[并行轨 B] 前端过程壳：processing Steps + succeeded_wait_view（可先接 Mock Job）
        │
        ▼
     S1  Python 图：N1+N2+N5（五环节结构结果可演示）
        │
        ▼
     S2  +N3 高端化指数
        │
        ▼
     S3  +N4a 规则关键（QC02 临时默认）← 业务闭环「像关键识别」
        │
        ▼
     S4  +N4b 代表企业卡（共享抽屉/篮）
        │
        ▼
     S5  +N4c LLM（可最后；全程允许 degraded 空叙述）
```

**为什么不先 S5**：没有 S1 的 Job/Stage/Result 壳，Prompt 无处挂；没有 S3，模型也改不了「谁是关键」。

---

## 2. 谁先动手（角色）

| 优先级 | 谁 | 先做什么 | 阻塞谁 |
| --- | --- | --- | --- |
| **P0 立刻** | **api-agent（Java）** | Job 表 + Create/Get/Withdraw + Stage/Complete 回调落库 + 签发 snapshot | 全体联调 |
| **P0 立刻** | **frontend-agent** | 关键 Tab：配置→过程壳→wait_view→结果壳；先打 **Mock GetJob/Events** | 不堵算法 |
| **P0 紧随** | **algorithm-agent（Python）** | Worker：`Execute` 收单 + S1（N1/N2/N5）+ ReportStage/Complete | S2+ |
| P1 | algorithm | S2 → S3 | 前端结果 KPI/标注 |
| P1 | frontend | 接真 GetJob；结果页绑 `chain_structure` / summary | — |
| P2 | algorithm + frontend | S4 企业卡 ↔ ElementProfile / 企业篮 | — |
| P3 | algorithm | S5 Prompt Pack；前端只展示降级诚实态 | 可与 S4 尾部重叠 |

监管人按任务派单填 `supervised_by`；此处只定**技术开工序**，不改 registry。

---

## 3. 切片 DoD（做完才算「能演示」）

| 切片 | DoD（最短） |
| --- | --- |
| **Runtime 竖切** | Create→Execute→≥1 次 Stage→Complete→GetJob 看到终态；`succeeded` 不自动跳结果 |
| **S1** | 过程五句文案推进；Result 含合法五节点 `chain_structure`；空 annotations/competition/trends 可先占位但 schema 过 |
| **S2** | 每环节 `high_end_index` 非空（允许 mock+gap） |
| **S3** | `is_key_node`+`annotations`+`key_node_count` 三者一致；honesty 含 QC02 |
| **S4** | ≥1 张企业卡可开画像/入篮（权限锁态按现约） |
| **S5** | 通 LLM 或稳定降级；禁止「实时全网检索」假完成态 |

---

## 4. 并行与错峰（防踩脚）

| 可并行 | 须串行 |
| --- | --- |
| Java Runtime ↔ 前端 Mock 过程壳 | S2 依赖 S1 Artifact 形状 |
| S5 的 Prompt 文案打磨 ↔ S3/S4 编码 | S3 依赖 S2 分数或至少 enterprise_count |
| OpenAPI/Schema 小改（契约仓） | Complete schema 大改需三方同周 |

**契约冻结建议**：S1 开工前，把 `openapi-analysis-job.v0.yaml` + `chain_structure` + `result_payload` 当作「讨论冻结」；改字段走小版本，不边写边推翻路径。

---

## 5. 不建议的开工法

1. 先接真 LLM（S5）再补 Job —— 过程页与审计都会空心。  
2. 前端假 setTimeout 推五步冒充 S1 —— 与 GetJob 契约冲突，返工大。  
3. 三端同时改 Result schema 大字段 —— 合并冲突与联调成本高。  
4. 等 QC02 甲方确认再开 S3 —— 可用 temp_default 先跑，honesty 标 🟡。

---

## 6. 一句话排期

> **本周**：Java Runtime 竖切 + 前端 Mock 过程壳 + Python S1。  
> **下周**：S2→S3（关键可演示）。  
> **再下周**：S4；S5 按模型可用性插空或垫底。

---

## 7. 修订

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0 | 2026-08-09 | S1～S5 开工序与角色并行建议 |
