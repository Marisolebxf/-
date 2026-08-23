# 智树负责范围与边界说明

> **智树实现范围**：同级 [报价明细表 V2.xlsx](./科技信息展示系统+专题战略4要素以及综合分析+数据处理中台-智树-报价明细表V2.xlsx)（见 [scope-baseline.md](./scope-baseline.md) §0）。  
> **招标 62 叶**：`bid-reference/` MD，用于对照与 ±10%；报价裁掉的周边 **只分析不实现**。

## 0. 范围铁律（2026-08-23）

| 原则 | 说明 |
|------|------|
| **实现真源** | 报价明细表 V2：展示系统 + 战略 4 要素（企业/产业链/产业服务/政策）+ 综合分析 + 数据 Mapping 中台 |
| **只分析不实现** | 科研机构 / 技术链 / 人才深度及对应算法；门户等未报价系统；表内划掉且工作量 0 |
| **招标叶子** | 仍为 **62**（±10% → 56～68）；不把「只分析」当成从 62 删叶 |
| **不可 silent 删报价内实现项** | 删报价内交付须 PM |

## 1. 双根目录

| 根 | 路径 | 用途 |
|---|---|---|
| 代码根 | `${GKX_ROOT}` | lumen 三仓、Python 算法仓、本 `agent-delivery` 编排 |
| 文档根 | `${GKX_DOCS_ROOT}` | V6、时序图、2-1需求分析（澄清台账） |
| 范围 MD | `${GKX_ROOT}/gkx-orchestration/agent-delivery/bid-reference/` | **工作范围出发点**（原始方案 + 核增） |

路径真源：`agent-delivery/paths.yaml`

## 2. 智树主责（与报价表对齐）

### 2.1 科技信息展示系统

中 / 大 / 小屏工作量均在报价表。深度跟列 C：**态势 / 政策 / 成果** 完整链路；**人才 / 数据资源 / 图谱** 界面+对接（他队 API）；**服务全景** 只跳转。

### 2.2 专题战略 4 要素 + 综合分析

实现：**企业、产业链、产业服务机构、政策** + **综合智能分析**（及对应深度模型 1/2/6/7 与综合模型）。  
只分析不实现：**科研机构、技术链、人才**（深度模型 3/4/5）。

### 2.3 数据处理中台

报价「数据 Mapping 过程实施」。智树完成：企业机构/科研机构、市场研究、政策 Mapping。论文/报告：培训与模板，实施他队。

### 2.4 不在智树独立交付

未进报价文件名的系统（门户、智库等）；服务全景他队界面；报价划掉且 0 工作量行。

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

## 6. 与报价表 / MD / 需规 / V6 关系

- **智树实现**：报价明细表 V2（最高）
- **招标对照**：`bid-reference/*.md`（62 叶与 ±10%）
- **澄清与台账**：`2-1需求分析`
- **设计细节**：V6 docx / 时序图
- **禁止**：读招标 PDF

## 7. 当前 Epic 边界（Wave 0–1）

| Epic | 范围 | 不包含 |
|---|---|---|
| E-INNOV-M1 | 全球创新实时数据 EventMap 端到端 | P5 网络x→Nebula、载体排行、城市指数 |
| E-PLATFORM-P0 | 七要素支持层脚手架 P-01~P-07 | 167 指标全量、58 模型全量 |
| E-E7-POLICY-M1 | 政策 5 指标 + 子图 + 3 核心模型 + 专题页 | 政策推演 DEMO（已登记 fallback） |
