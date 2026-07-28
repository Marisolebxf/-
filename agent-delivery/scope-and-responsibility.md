# 智树负责范围与边界说明

> **工作范围出发点**：`agent-delivery/bid-reference/` 两份 MD（原始招标方案整理）。  
> 所有 Epic、开发、验收以此为准；`2-1需求分析` 为补充澄清，不得突破 MD 功能点总量 **±10%**（见 `scope-baseline.yaml`）。

## 0. 范围铁律（2026-06-16 确认）

| 原则 | 说明 |
|------|------|
| **范围真源** | `科技信息展示系统和科技专题服务系统.md` + `科技专题服务算法库.md` |
| **实现弹性** | 数据供给、算法选型、接口细节可调整；handoff 记录 as-built |
| **功能点上限** | 相对 MD 基线 58 项叶子，活跃功能点 **52~64**（±10%） |
| **不可 silent 删** | 删叶子须 REMOVED 登记 + PM；超 10% 须 PM 批 change_log |

## 1. 双根目录

| 根 | 路径 | 用途 |
|---|---|---|
| 代码根 | `${GKX_ROOT}` | lumen 三仓、Python 算法仓、本 `agent-delivery` 编排 |
| 文档根 | `${GKX_DOCS_ROOT}` | V6、时序图、2-1需求分析（澄清台账） |
| 范围 MD | `${GKX_ROOT}\agent-delivery\bid-reference\` | **工作范围出发点**（原始方案） |

路径真源：`agent-delivery/paths.yaml`

## 2. 智树主责系统

### 2.1 科技信息展示系统（7 模块 34 页）

- **主交付端**：中屏 `lumen-ui-science-pc`
- **模块责任**（见 `system-wbs.yaml#display_modules`）：
  - **zhishu_primary**：M1 科技发展态势、M2 科技政策跟踪 — 全栈主责
  - **zhishu_frontend_only**：M4 科技数据资源 — 前端 + Java BFF，数据三方
  - **co_build**：M5 科技知识图谱 — 与图谱/算法共建
  - **third_party_integrate**：M3 人才、M6 成果、M7 服务全景 — 集成 + 展示绑定

### 2.2 科技专题服务（七要素 E1–E7）

- **算法**：仅 Python（`demo-algo-science`、`demo-algo-ent-analysis` 及后续 topic-*-py）
- **业务 API**：Java `gkxlumen-topic-*`（只读 ADS / 聚合 / Feign 调 Python）
- **专题页**：`/topic/{element}/**`
- **展示绑定**：34 页通过 W6 工作流消费 `/topic` 或 BFF

### 2.3 不在智树独立交付范围

- 智慧服务门户、新型高端智库、科技数据资源库、科技交流等**其他六大系统**的完整后端
- 人才/成果/服务等**第三方主系统**的业务逻辑（智树做 INTEG 层集成与展示）

## 3. 架构铁律

1. **算法只在 Python**；Java 禁止 NLP/模型/图谱计算
2. **调用链**：前端 → Java REST → Python `/internal/*`；前端不直连 Python/DB
3. **图谱统一 NebulaGraph**（禁止 Neo4j）；demo 真源 `demo-algo-ent-analysis`
4. **全栈 OpenTelemetry**（Java Agent / Python instrument / 前端 `observability.ts`）
5. **CI/CD**：每 leaf 任务 push → GitLab Pipeline 绿 → K8s dev rollout（设计类任务除外）

## 4. 验收策略（三级 Tier）

| Tier | 含义 | 要求 |
|---|---|---|
| FULL | 正式实现 | 真实数据 + dev K8s 可演示 + 文档 |
| INTEG | 三方集成 | 对接外部 API/系统，接口与展示可用 |
| DEMO | 演示兜底 | 必须登记 `demo-fallback-registry.yaml` 并说明理由 |

**验收底线**（`acceptance-compliance-policy.md`）：`2-概要设计/2-1需求分析` 功能点台账范围内每条功能点须有 menu/route；DEMO 须登记。Agent **禁止**读取招标 PDF。

## 5. 参考 demo（只读，不 merge）

| 用途 | 路径/URL |
|---|---|
| innov UI | `${GKX_ROOT}/repos/demo-ui-system-test\src\views\innov` |
| innov Java | `${GKX_ROOT}/repos/demo-svc-platform\gkx-innov` |
| innov Python | `${GKX_ROOT}/repos/demo-algo-science` |
| 图谱 Nebula | `${GKX_ROOT}/repos/demo-algo-ent-analysis` |
| demo2 交互真源 | https://skxrules.unicomcn.tech:30999/ |

## 6. 与 MD / 需规 / V6 关系

- **范围与原始方案**：`bid-reference/*.md`（最高）
- **澄清与台账**：`2-1需求分析`（不得使功能点总数超出 MD 基线 ±10%）
- **设计细节**：V6 docx / 时序图
- **禁止**：读招标 PDF

## 7. 当前 Epic 边界（Wave 0–1）

| Epic | 范围 | 不包含 |
|---|---|---|
| E-INNOV-M1 | 全球创新实时数据 EventMap 端到端 | P5 网络x→Nebula、载体排行、城市指数 |
| E-PLATFORM-P0 | 七要素支持层脚手架 P-01~P-07 | 167 指标全量、58 模型全量 |
| E-E7-POLICY-M1 | 政策 5 指标 + 子图 + 3 核心模型 + 专题页 | 政策推演 DEMO（已登记 fallback） |
