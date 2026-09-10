# CROSS-VEC-ARCH-SIGN-L01 · 向量库会签建议（非正式双签）

> 格式对齐 `templates/handoff-template.md` + AV-1 必检标题。本叶是 **架构建议 + 施工默认**，**不是**已会签通过。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。公约 §3.1：不能替李伟/徐滕强拍板 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；不写 pymilvus、不改 helm、不实现 Job A |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只写会签建议页与 handoff，未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 沿用 SAD `02` 调用链（FE→GW→Java→Python→`192.168.88.48:19530`） |
| 图 diff | 无新边。禁止事项未变：不写 `amcpdp-*`、不采购第二套云、Java 不直连 19530 |
| 会签态 | `draft`（建议已落盘；正式双签 🟡。禁止自填绿） |
| 说明 | 本叶不新画 L0–L4 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md · AV-1 REQUIRED_SECTIONS |
| 范围边界 | 派单/CROSS-VEC-ARCH-SIGN-L01-派单包.md · 总控 §0 #4–#6 #11–#12 |

## 问题清单

- 正式模型名未定（VEC-Q2）：仓内无已装产业文本 embedding 实现，禁止编造。
- 四题均 🟡 待 `human:李伟` / `human:徐滕强`；算法 `human:唐绍祖` 知情。
- 账号 / 网段 ACL 细节交 DEVOPS-NET，本叶不改 helm。

## 范围与实现

对照派单包：书面结论四题（Q1 / Q1b / Q2 / Q5）。对照 bid-reference：不扩招标、不采购向量云、不写生产 OpenAPI。

落盘：[decisions/2026-09-10-vec-q1-q2-q5-会签建议.md](./decisions/2026-09-10-vec-q1-q2-q5-会签建议.md)。INDEX + 03 §0 加指针。**未改** draft 为已会签。

| 题 | 建议值（施工默认） | 待确认 |
|----|-------------------|--------|
| VEC-Q1 | 共用 `192.168.88.48:19530`；仅 Python 连；产业账号禁止 drop/insert `amcpdp-*` | 🟡 李伟 / 徐滕强 |
| VEC-Q1b | 接受 standalone 单点；默认**不采购**第二套 | 🟡 李伟 / 徐滕强 |
| VEC-Q2 | collection 建议 `gkxlumen-industry-anchor`；度量建议 COSINE；**模型名不编造**；PY-INDEX 先内存回退 | 🟡 李伟 / 徐滕强（模型名+dim）；唐绍祖知情 |
| VEC-Q5 | Job A 增量默认可调度、全量须审批；Job B 默认关（`enable_llm=true` 才跑） | 🟡 李伟 / 徐滕强 |

## 偏离说明

**无偏离。** 建议值对齐总控 §0 #4–#6 #11–#12 与 SAD 03 §0。未改 bid-reference、未另起向量云、未把 RAG 写成建图开工条件。按 draft 给施工默认 ≠ 正式双签，也不算偏离。

## 验收证据

- 定义叶无 pytest / K8s。证据 = 建议页 + INDEX/03 指针 + 本 handoff。
- 仓内检索：`lumen-algo-py` 无 `pymilvus` / `bge-*` / `sentence-transformers` 产业锚点实现 → VEC-Q2 不编模型名。
- MCP：`integration`（会签中）。**禁止** note 写「会签通过」。**禁止** `done` / `ready_to_sign`。

## 遗留风险

- 后补签改模型名 / dim → PY-INDEX 改 `model_version` 并重建本前缀；内存单测不必返工。
- 19530 不通 → 内存回退 / degraded，禁止假 VID。
- ACL 未落地前，DEVOPS-NET 只探测、不 insert 业务向量。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev` → `origin/dev`
- commit：本叶提交后回填 SHA
- pipeline URL / ID：`cicd: skip`（定义叶）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- Tempo / Loki：无
- Job A/B 进度仍按 02 §3.2：已处理/跳过/对码/失败，禁止假百分比

## 产物清单

- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/decisions/2026-09-10-vec-q1-q2-q5-会签建议.md`（新建）
- `…/跨系统-向量库/INDEX.md`（加会签建议指针，状态仍为 draft）
- `…/跨系统-向量库/03-详细设计.md`（§0 加指针，仍标非生产契约）
- `…/跨系统-向量库/CROSS-VEC-ARCH-SIGN-L01.md`（本 handoff）
- 顺带：`CROSS-VEC-SAD-L01.md` AV-1 标题对齐（状态保持 `integration`）

## 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python | ✅ 仅 `lumen-algo-py` `/internal/*` 连 19530；Java 禁 NLP / 禁直连 |
| 2 | 调用链 / **D12** | ✅ 前端 → 网关 → `gkxlumen-*` → Python；禁止 lumen 回落 `demo-*` |
| 3 | 图谱 = NebulaGraph | ✅ 定码仍走 VID + FETCH；向量不替代建图 |
| 4 | 可观测 | ✅ 设计叶；Job 阶段计数约定不变 |
| 5 | CI/CD | ✅ 定义叶 `cicd: skip` |
| 6 | demo 不污染 lumen | ✅ 不改业务仓、不 merge demo→lumen |
| 7 | 方案 A | ✅ 展示+专题共用产业锚点 |
| 8 | 禁止 `amcpdp-*` | ✅ Q1 最小权限 + Q2 另前缀 |
| 9 | 不采购第二套云 | ✅ Q1b 默认不采购 |
| 10 | RAG ≠ 建图开工 | ✅ 未改 SAD 分层 |

决议：**建议落盘、施工默认可用；正式双签 🟡 后补。** 不挡 POLICY-L0 / PY-INDEX 内存回退。

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | `38000` |
| model_used | `cursor-grok-4.6`（预算档按 architect 评审 · C 旗舰口径折算） |
| actual_cost | `0.91` |
| cost_warn | `green` |

口径：`38000 × 0.85 × 15 / 1e6 + 38000 × 0.15 × 75 / 1e6 = 0.4845 + 0.4275 = 0.912 ≈ 0.91`。单任务 < $5 → `green`。

## 开放项

| 人 | 要补 | 挡主链？ |
|----|------|----------|
| `李伟` / `徐滕强` | 四题书面确认 | 否 |
| `唐绍祖` | VEC-Q2 模型知情 | 否 |
| DEVOPS-NET | 账号 / 网段 ACL | 否（先探测） |

## MCP 回填

- `evidence` = 本文件路径。
- 目标状态：`integration`（会签中）。禁止 `done` / `ready_to_sign`。禁止 note 写「会签通过」。
