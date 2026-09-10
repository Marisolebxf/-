# CROSS-VEC-SAD-L01 · 跨系统向量库 SAD 施工关门（非正式双签）

> 格式参考 `templates/handoff-template.md`。本叶是 **definition 施工关门**，不是正式双签完成，也不是生产 OpenAPI。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。特殊授权：不等李伟/徐滕强/唐绍祖正式双签 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；不写 lumen-* / demo-* 业务代码 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只评审已落盘 draft 并写封面/纪要/handoff，未挂载 Headroom 压缩 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | SAD 内嵌：`01` 本体/文档分层 · `02` 建库/消费切面 · `02` D12 调用链（FE→GW→Java→Python→Milvus） |
| 图 diff | 本叶不改图；沿用 v0.3-draft 三图。禁止事项未变：不写 `amcpdp-*`、不把 RAG 画成建图前置、Hang ≠ G3 |
| 会签态 | `draft`（施工授权已开；正式双签 🟡 后补。禁止自填绿） |
| 说明 | 真源仍是三卷 + INDEX；本叶只关门施工授权，不新画 L0–L4 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | 派单/CROSS-VEC-SAD-L01-派单包.md · CROSS-VEC-长任务总控.md §0 |
| 对照 | 跨系统-知识图谱/INDEX.md · 02 §3.1–3.2（Hang ≠ G3） |

## 问题清单

- 正式双签未齐：架构 `李伟` / `徐滕强`、算法 `唐绍祖`、数据 Lead、PM 均为 🟡 后补。
- VEC-Q1 / Q1b / Q2 / Q5 书面结论仍归 `CROSS-VEC-ARCH-SIGN-L01`；本叶不替签、不改口径。
- 01 封面仍写 v0.2-draft、02/03 写 v0.3-draft：内容已按 v0.3 施工面冻结，本叶不改三卷正文。

## 修改内容

- 精读 v0.3-draft 三卷 + INDEX + 导读、知识图谱 INDEX / 02 §3.1–3.2、`architecture-baseline.md` D1–D12、长任务总控 §0、本叶派单包。
- **评审结论**：draft 与冻结十五条一致，可按特殊授权施工关门；**不是**正式会签通过。
- 更新 `INDEX.md` 封面：施工授权 + 后补签；门禁区拆成「施工门已开 / 生产契约门未开」。
- 落盘纪要 `decisions/2026-09-10-sad-施工授权.md`。
- **未改** 01/02/03 口径；**未写** lumen-* / demo-* 业务代码；**未写** 生产 OpenAPI。

### 冻结核对（已拍板，本叶不改）

| # | 冻结项 | 三卷落点 | 结论 |
|---|--------|----------|------|
| 1 | 建库 = 产业链灌数末段一次 `embed/rebuild` | 02 §1.1 · 03 §5 | ✅ 沿用 |
| 2 | 重灌同步 = 仅 L0+L1，不调 Milvus/LLM | 02 §3 · INDEX 纪律封面 | ✅ 沿用 |
| 3 | Job A/B 是 ETL 长任务，不是重灌内步骤 | 02 §3.1–3.2 | ✅ 沿用 |
| 4 | Milvus 共用 `192.168.88.48:19530`；禁止 `amcpdp-*` | 01 §2.1 · 03 §0 | ✅ 沿用 |
| 5 | 数仓 `demo_gkxlumenx_*`；图 `demo_gkx_chain` | 总控 §0 #9–#10 | ✅ 沿用（本 SAD 不另开正式 catalog） |
| 6 | 不把 RAG 写成建图开工条件；不写生产 OpenAPI | INDEX 与图谱分工 · 03 文首 | ✅ 沿用 |

### 与知识图谱 SAD 对齐

- 向量是**用图之后的对齐面**，不替代建图。
- Hang = ETL 上图跑批（FETCH 已有点）；G3 = 只读分析 Job，**不是上图**。
- 夜班建议：灌链 VID 稳定 → rebuild → L0+L1 重灌 → Job A 补槽 → Hang；先槽后边。

## 测试结果

- 本叶无业务仓、无 pytest / 浏览器验收。
- 文档自检：INDEX 封面诚实（施工授权 ≠ 已双签）；三卷「明确不做」含禁止 `amcpdp-*`、禁止假 VID、禁止 Java/前端直连 19530。
- MCP：见文末「MCP 回填」；definition 交卷目标态 = `integration`（会签中/施工关门），**不标 done**。

## 遗留风险

- 正式双签未齐：若后补签改 VEC-Q2 模型名 / dim，PY-INDEX 须改 `model_version`，不回滚本叶施工授权。
- 01 文首版本号滞后（v0.2 vs v0.3）：不挡施工；ARCH-SIGN 可顺手对齐封面版本号。
- 19530 不通：PY-INDEX 走内存回退 / degraded，禁止假 VID（总控 §1.5）。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev` → `origin/dev`
- commit：本叶提交后回填 SHA（见 coordinator 回报）
- pipeline URL / ID：`cicd: skip`（定义叶，仅编排文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A（无业务部署）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（本叶无进程）
- traceId（dev 抽样）：N/A
- Tempo / Loki：无
- 后续实现叶：Job A/B 进度只报已处理/跳过/对码/失败，禁止假百分比（02 §3.2）

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/INDEX.md`（封面 + 门禁）
- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/decisions/2026-09-10-sad-施工授权.md`（新建）
- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/CROSS-VEC-SAD-L01.md`（本 handoff）
- 只读、未改：`01-系统分析.md` · `02-概要设计.md` · `03-详细设计.md` · 导读三件 · `architecture-baseline.md`

## 架构合规自检（D1–D12）

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python | ✅ SAD 规定仅 `lumen-algo-py` `/internal/*` embed/search/L2；Java 禁 NLP / 禁直连 19530 |
| 2 | 调用链 / **D12** | ✅ 前端 → 网关 → `gkxlumen-*` Feign → Python；lumen **禁止**回落任何 `demo-*` 服务 |
| 3 | 图谱 = NebulaGraph | ✅ 定码走图 VID + FETCH；一张 G = `demo_gkx_chain`；禁止 Neo4j |
| 4 | 可观测 | ✅ 设计约定 Job 阶段计数；实现叶补 OTel。本叶无进程 |
| 5 | CI/CD | ✅ 定义叶 `cicd: skip`；实现叶仍须 push → Pipeline |
| 6 | demo 不污染 lumen | ✅ 对照可读；禁止 merge demo→lumen；数仓本轮 `demo_gkxlumenx_*` |
| 7 | 方案 A | ✅ 展示+专题共用产业锚点；前端不直调 Python / Milvus |
| 8 | 数据走 ADS/DWD 纪律 | ✅ 建库读 DWD 链表 + 图点；Java 不写算法、不直连 nGQL |
| 9 | D8 前端规范 | N/A 本叶无页面 |
| 10 | D9 指标 8 件套 | N/A 本叶不落统计数字 |
| 11 | D10 交互 | N/A 本叶无交互稿 |
| 12 | **禁止 `amcpdp-*`** | ✅ collection 前缀 `gkxlumen-industry-*`；只读不改多媒体帧库 |
| 13 | RAG ≠ 建图开工 | ✅ 与知识图谱 SAD 一致；向量不替代建图 |
| 14 | Hang ≠ G3 | ✅ Job A/B 补 DWD 槽；Hang 上图；G3 只读分析、不上图 |

决议：**施工关门通过（draft + 特殊授权）**。正式会签后补，**不挡** `CROSS-VEC-POLICY-L0-L01` / 后续叶。

## 成本（必填四字段）

| 字段 | 值 |
|------|-----|
| actual_tokens | `72000` |
| model_used | `cursor-grok-4.6`（预算档按 architect 评审 · C 旗舰口径折算） |
| actual_cost | `1.73` |
| cost_warn | `green` |

口径：`actual_tokens` ≈ in+out；architect 默认比 85/15；C 旗舰 `$15` / `$75` per M。  
`72000 × 0.85 × 15 / 1e6 + 72000 × 0.15 × 75 / 1e6 = 0.918 + 0.810 = 1.728 ≈ 1.73`。  
单任务 < $5 → `green`。未超 $10 暂停线。

## 开放项（后补签名单）

| 人 / 叶 | 要补什么 | 挡主链？ |
|---------|----------|----------|
| `李伟` / `徐滕强` | 架构正式双签 | 否 |
| `唐绍祖` | 算法知情 / 会签 | 否 |
| 数据 Lead / PM | 知情 | 否 |
| `CROSS-VEC-ARCH-SIGN-L01` | VEC-Q1 / Q1b / Q2 / Q5 书面结论 | 否（总控：不挡 L0；NET/INDEX 可按施工默认） |

## MCP 回填

- `evidence` = 本文件相对编排仓路径（见下）。
- 目标状态：`integration`（definition = 会签中 / 施工关门）。
- **禁止** `done`。正式双签完成后由 ARCH-SIGN / 签收路径处理。
