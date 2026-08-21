# LUMEN-SVC-P-FE-US-REC-03 · US-SVC-REC-03 培育模型与筛选

> 日期：2026-08-22  
> Task：`LUMEN-SVC-P-FE-US-REC-03`  
> 总控：[`LUMEN-SVC-P-长任务总控.md`](./LUMEN-SVC-P-长任务总控.md)（§7 已生效；金路径培育配置）  
> 仓：`lumen-ui-topic` · `origin/dev`  
> 复刻真源：`demo-ui-topic` CultivateTab 配置交互（只读对照，未贴 JSX、未改 demo、未搬 `computeCultivateList` 本地 Σ）  
> 本仓前置：REC-01 `9f58610` · REC-02 `33141a9` · WAITVIEW `7f83a82`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务 24h 锁；本叶不标 `done`。coordinator 已 MCP `in_progress`。本会话未挂载 task-registry MCP，未手改 yaml。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 抽出 `svcRecWeightGate` 复用招引合计/归一门控；cultivate 接 WAITVIEW + 四卡/筛选。未用 YAGNI 跳过 D8 页底 token、D9 GAP 红问号、D10 评审自闸、可观测 X-Trace-Id、handoff、图即契约、五维复刻、附录 E。未自造 `M_SVC_REC_CULTIVATE_SCORE` 进 seed，未挪用 `M_SVC_REC_ATTRACT_SCORE`，未本地 Σ，未打 rec-list。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，不改工厂边）；`LUMEN-SVC-P-FE-US-REC-03-SEQ`（本叶） |
| 图 diff | LINEAGE 边未改。本叶把 `workspace=cultivate` 从 REC-02 占位改成实线配置：WAITVIEW + 四维度可调 + 机构类型/服务环节筛选。结果区诚实空位，不打 rec-list。禁止事项未变：权重/筛选/产业不进 `analysis_fp`、不写入 CREATE params、不本地 Σ、不打 `demo-*`、招引 REC-01/02 契约未改。 |
| 会签态 | `SVC-STORAGE-LINEAGE` 随 `storage/SVC/01-data-flow.md` frontmatter：`approved`（`human:淮政玮` · 2026-08-19 流图；2026-08-20 选 B 增补 LINEAGE，**不改** §1 工厂边）。本叶 SEQ 为 `draft`，禁止自填绿。 |

### L2 消费（不改边）

本叶只读消费 [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) §1.1 `SVC-STORAGE-LINEAGE`：培育名单 ADS `svc_cultivation_recommend` 仍由后续 REC-04 消费。本叶不扫表、不直连 nGQL、不改工厂边、不新 Java 路径。

### L4 本叶 SEQ · `LUMEN-SVC-P-FE-US-REC-03-SEQ`

```mermaid
sequenceDiagram
  actor User
  participant FE as lumen-ui-topic
  participant GW as gkxlumen-platform-gateway
  participant ASYNC as gkxlumen-topic-async-service
  Note over FE,GW: 不对前端暴露 /internal；禁止 /api/svc；D12 不打 demo-*
  User->>FE: 调四维度权重（默认 25/30/25/20）+ 机构类型/服务环节筛选
  FE->>FE: URL cw/cot/cseg + localStorage；合计≠100 或筛选全空禁用开始分析
  User->>FE: 门控通过后点「开始分析」
  Note over FE: 产业/权重/筛选不进 analysis_fp=svc\|cultivate|*；不写入 CREATE params
  FE->>GW: POST /topicAsync/topic/v1/analysis/tasks (analysisType=cultivate)
  GW->>ASYNC: CREATE + poll GET
  ASYNC-->>FE: success 停 wait_view（过程页）
  User->>FE: 「查看结果」
  Note over FE: 本叶不打 rec-list；不本地 Σ；不展示招引名单或 Demo 本土机构
  FE-->>User: 诚实空位「培育名单由后续叶交付」
  alt Job failed
    FE-->>User: WAITVIEW 红 alert ≠ 空位 5xx
  end
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| 页面权重/筛选编辑器 | 配置区门控 | 改 `cw`/`cot`/`cseg` / 归一 / 恢复默认 | 损坏回落 25/30/25/20 与全选 + Message | 权重/筛选进 fingerprint；写入 CREATE params；本地 Σ |
| Java `POST\|GET /topicAsync/.../tasks*` | WAITVIEW | 「开始分析」/「重新分析」且门控通过 | 失败红 alert ≠ 空位 | 切权重/筛选/产业自动 CREATE；打 rec-list |
| `GAP-SVC-REC-CULTIVATE-SCORE` | 模型头红问号 | 评审开 | Q063 / Q-SVCCHAIN-05 待核验，不改绿 | 自造 `M_SVC_REC_CULTIVATE_SCORE` 进 seed；挪用 `M_SVC_REC_ATTRACT_SCORE` |

## 范围与实现

落地 `US-SVC-REC-03` 培育模型与筛选，挂 `/service/institution-decision?workspace=cultivate`，替换 REC-02 占位：

1. 配置区 / 过程壳 / 记录 Tab 复用招引 WAITVIEW 骨架。CREATE 白名单裸键 `cultivate`。指纹 `svc|cultivate|*`。切条件不自动 CREATE。
2. 四维度卡：现有规模 / 技术创新能力 / 服务成效 / 市场缺口。默认 **25/30/25/20**（切法 A 冻结）。0–100 整数；合计 ≠100 禁用「开始分析」；「按比例归一」；「恢复默认」。
3. 筛选：机构类型多选、服务环节多选（默认全选）；全不选禁用开始并解释。权重+筛选持久化 URL `cw`/`cot`/`cseg` 与 localStorage；损坏回落默认 + Message。
4. 本叶不打 rec-list、不本地 Σ、不发明培育名单。结果区诚实空位「培育名单由后续叶交付」。
5. 模型区 🧪 + 业务态「演示模型口径」。评审 ⚠️ `Q-SVCCHAIN-05` / `Q063` 不改绿。D1 missing 走 `GAP-SVC-REC-CULTIVATE-SCORE` 红问号。关评审零泄漏。
6. 页底 `--sci-bg-page`。Mock 关：页面不引 `@/mock/**`。

**非范围**：US-SVC-REC-04 培育名单 / 建议标签 / 入篮 / CSV；改招引 REC-01/02 契约；派 Python 改培育模型；把 TECH ranking 落到 cultivate；宣称 K8s 绿；改 `industry-center` / `demo-ui-topic`。

## 偏离说明

- 默认权重用冻结清单 **25/30/25/20**。USM 若写 20/30/25/25，以冻结为准。
- 本叶不做培育名单。Demo CultivateTab 用 `computeCultivateList` 本地 Σ 出名单与建议；本叶按 `/goal` **禁止**搬本地 Σ、禁止打 rec-list。
- 权重与筛选 **不进** 指纹（与招引同一原则）。改筛选会复用当天同指纹任务；须「重新分析」才新建 Job。
- Demo 权重在 ALIGN-L01 后为内置只读 Tag。本叶按 `/goal` 做成可调四卡（与招引 REC-01 同一门控）。
- Q063 / Q-SVCCHAIN-05 **不改绿**。仓内无 `M_SVC_REC_CULTIVATE_SCORE` 种子，不自造、不挪用招引综合分。
- 未做报告阅读器（W3 N/A）。模板 W2 关系图 N/A。
- 按钮文案沿用 WAITVIEW「开始分析」，无单独「生成培育名单」。

## 复刻五维（R1–R5）

| # | 项 | 结果 |
|---|---|---|
| R1 布局 | 配置区四卡+筛选 + 过程壳 + 记录 Tab + 结果空位；招引仍独立名单页 | ✅ |
| R2 交互 | 合计/筛选门控；损坏回落；不自动 CREATE；查看结果才进空位；Job failed 走 WAITVIEW | ✅ |
| R3 样式 | `--sci-bg-page` / `#D8E7FC`；主色 `#165DFF`；四卡网格沿招引 | ✅ |
| R4 评审 | 只从 `@/review`（`SVC-REC-03-*`）；关评审不泄漏 metric_id / GAP-* / Q063 | ✅ |
| R5 Mock | 关：页面不引 `@/mock/**`、无页内 `MOCK_`、无华大基因填数 | ✅ |

### 检索皮肤（V1–V7）

本叶是分析工作区配置，不是检索 Hub。V1 页底必过；V2–V7 N/A。

| # | 结果 |
|---|---|
| V1 页底 `--sci-bg-page` / `#D8E7FC` | ✅ |
| V2–V7 | N/A（查询页） |

### 工作区（W1 / W4）

| # | 项 | 结果 |
|---|---|---|
| W1 | 配置区（可调四卡+筛选）/ 过程壳 / 结果空位 / 记录 Tab | ✅ |
| W2 | 关系图 | N/A |
| W3 | 报告阅读器 | N/A |
| W4 | 切条件/改权重/筛选不自动 create；「开始分析」；同指纹一条在跑；当天成功可恢复；「重新分析」可 force | ✅ |

## 附录 E（I2-12）

| # | 项 | 结果 |
|---|---|---|
| E.1 页清单 | `/service/institution-decision?workspace=cultivate`（本叶） | ✅ |
| E.2 CTA | 配置区「开始分析」（合计=100 且筛选非空才可点） | ✅ |
| E.3 禁自动 create | 无 `watch → create`；改权重/筛选/产业只改 query | ✅ |
| E.4 单飞 | `decideAnalysisTaskGate` + `svc\|cultivate\|*`；产业/权重/筛选不进指纹 | ✅ |
| E.5 当天复用 | `forceCreate=false` restore 过程页；`重新分析` `force=true` | ✅ |
| failed | 过程壳红 alert ≠ 空位 | ✅ |

## Design.md §14

页底 token `--sci-bg-page`；主色 `#165DFF`；控件高走 Arco InputNumber / Checkbox / Select 默认 32px。筛选 Select 受 `--sci-filter-control-max`。无 `.ant-` / vendor-antd token。无新地图。模型综合分走 `@/review` GAP 红问号，不自造 ⓘ / emoji 角标。权重警告色用 `#FF7D00`（待核验橙，不是涨跌方向色）。

## 测试结果

- `node src/views/service/serviceRecCultivate.selfcheck.mjs` → `serviceRecCultivate.selfcheck ok`
- `node src/views/service/serviceRecAttractWeight.selfcheck.mjs` → `serviceRecAttractWeight.selfcheck ok`
- `node src/views/service/serviceRecommendAttract.selfcheck.mjs` → `serviceRecommendAttract.selfcheck rec-list ok`
- `node src/router/menu.selfcheck.mjs` → `menu.selfcheck svc-shell ok`
- `npx vue-tsc --build` → 通过（exit 0）
- 本叶未等 K8s rollout

## 遗留风险

- 培育名单 / 建议标签 / 入篮 / CSV 由 REC-04 交付；50892 上本叶结果区会看到诚实空位，这不是 5xx。
- 改筛选不换指纹：当天已成功任务会 restore 过程页，须点「重新分析」才新建 Job。
- Q063 / Q-SVCCHAIN-05 闭合前不得把演示权重当正式模型。
- 金路径仍须 E0 滚出后在 50892 点过一遍（调权重 → 筛选门控 → 开始分析 → 查看结果 → 空位）。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`（push `9f58610..bccdd98`，未 force）
- commit：`bccdd98` `feat(svc): add US-SVC-REC-03 cultivate model and filters [agent:frontend-agent]`
- pipeline URL / ID：GitLab 对 dev 自动建管线（本叶未等绿、未宣称 K8s 已滚出）
- 部署 namespace / 镜像 tag：待 E0 / CI
- K8s rollout：本叶未等
- dev 测试 URL：http://111.198.38.90:50892/service/institution-decision?workspace=cultivate （需 CI 滚出后可见本叶）
- 本地：`node src/views/service/serviceRecCultivate.selfcheck.mjs`

## 可观测性

- CREATE / GET / RESULT 均走 `src/utils/request.ts`：`X-Trace-Id` + `traceparent`
- Job 失败展示 `traceId`
- OTEL_SERVICE_NAME：N/A（前端）
- Tempo / Loki：有（平台已有）；本叶无新 span 名

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 前端无排名算法；不本地 Σ；不打 rec-list |
| 2 调用链 FE→Java→Python `/internal` | ✅ 只调已有 tasks；无第二张 Java/Python 单 |
| 3 Nebula 非 Neo4j | ✅ 未碰图 |
| 4 可观测 | ✅ request 拦截器 X-Trace-Id |
| 5 CI | ⏳ push 后 |
| 6 demo2 不 merge 进 lumen | ✅ 只读对照 demo-ui-topic |
| 7 共享聚合 / 只调 Java | ✅ 未直连 Python |
| 8 数据 ADS / 无硬 mock | ✅ `USE_MOCK=false` 不填 fixture |
| 9 D8 Design token | ✅ `--sci-bg-page` |
| 10 D9 八件套 / 不自造 ⓘ | ✅ `GAP-SVC-REC-CULTIVATE-SCORE`；未造 `M_SVC_REC_CULTIVATE_SCORE`；Q063 不改绿 |
| 11 D10 `@/review` | ✅ |
| 12 D12 不打 demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 245000 |
| `model_used` | `claude-sonnet-4.5`（registry 合法枚举；本会话为 Cursor Grok 4.6，按 Sonnet 价表回填） |
| `actual_cost` | 1.32 |
| `cost_warn` | green |
| 口径 | frontend-agent 80/20；`245000×0.8×3/1e6 + 245000×0.2×15/1e6 = 1.323` 取 `1.32`；`source: session_estimate` |

## 涉及文件

- `lumen-ui-topic` `src/views/service/ServiceRecommendCultivateWorkspace.vue`
- `lumen-ui-topic` `src/views/service/svcRecommendCultivateModel.ts`
- `lumen-ui-topic` `src/views/service/svcRecWeightGate.ts`
- `lumen-ui-topic` `src/views/service/ServiceRecommendAttractWorkspace.vue`（占位改挂子页）
- `lumen-ui-topic` `src/views/service/svcRecommendAttractModel.ts`（权重门控抽到 gate）
- `lumen-ui-topic` `src/views/service/svcRecommendAttractWorkspace.ts`
- `lumen-ui-topic` `src/views/service/serviceRecommendAttract.css`
- `lumen-ui-topic` `src/views/service/serviceRecCultivate.selfcheck.mjs`
- `lumen-ui-topic` `src/views/service/ServiceReviewMount.vue`
- `lumen-ui-topic` `src/mock/service/svcGapCatalog.ts`（仅 GAP 文案，未写 CULTIVATE_SCORE seed）
- 本 handoff

## 产物清单

- 代码：`bccdd98`（`lumen-ui-topic` `dev`）
- 文档：本文件
- 未改：`DefaultLayout.vue`、`industry-center`、`demo-ui-topic`、Java / Python、招引 rec-list 契约、WAITVIEW 过程壳实现

## 联调确认

联调通过（代码侧）：`workspace=cultivate` 经 WAITVIEW；四卡默认 25/30/25/20 且合计/筛选门控；权重与筛选不进指纹、不写入 CREATE；不打 rec-list；不本地 Σ；结果区诚实空位；Q063 / Q-SVCCHAIN-05 不改绿；招引 REC-01/02 自检仍绿。请 coordinator AV-0，**本叶不自行标 done**。

## Registry（MCP）

本会话未挂载 `task-registry` MCP。`status` 仍为 `in_progress`（未改 done）。禁止手改 `task-registry.yaml`。请 coordinator 代写 evidence / note / cost 四字段。
