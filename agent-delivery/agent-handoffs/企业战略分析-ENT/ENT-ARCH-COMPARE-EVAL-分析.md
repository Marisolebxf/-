# 架构师分析：对比篮（COMPARE）+ 企业评估（EVAL）功能拆解

- **分析人**：architect-agent（[human:徐滕强] 监管）
- **时间**：2026-07-21
- **输入**：原型截图 3 张（`/enterprise-center/basket`）、Wireframe-ENT-COMPARE v1.5、Wireframe-ENT-EVAL v1.6、IA-ENT-COMPARE、IA-ENT-EVAL、企业维度-Python微服务架构预设计 v1.3、现有 Python/Java 代码
- **目的**：拆解对比篮 + 企业评估两个功能的数据层/接口层/业务层职责，明确 data-agent / algorithm-agent / api-agent 各自任务范围

---

## 1. 两条铁律前置

1. **数据侧项目 ≠ 算法侧项目**：
   - 数据侧（`demo-svc-topic-py` / `gkx_search_service`）：数据组负责，纯读 ES/Nebula/PG，`/internal/*` 供 Java Feign
   - 算法侧（`demo-algo-ent-analysis` / `entan`）：算法组负责，独立算法 demo，含 task_manager / eval 模块 / `/v1/*` API
   - 架构预设计 §13 的"entan/eval → search 模块"是**未来演进映射**，非现状；data-agent **不碰** entan 仓代码
2. **Java 只通过数据侧 Python 触达算法**：
   - 调用链：前端 → Java → gkx_search_service(`/internal/*`) →（必要时 HTTP 调）entan(`/v1/*`)
   - gkx_search_service 是算法服务的**屏蔽层**；Java 不直连 entan

---

## 2. 对比篮（COMPARE）分析

### 2.1 功能定位（Wireframe v1.5 + Decision 088）

对比篮是**派生暂存/分发容器**：
- 暂存企业对象（≤50 家）、篮内搜索/筛选/勾选
- 发起分析（分发到企业评估/风险洞察，携 `enterprise_codes[]` + `analysis_type` + `return_context_id`）
- 加入招引/培育候选名单
- **不展示分析结果、不拥有统计 metric**（metrics_required=0）

### 2.2 字段需求 × 数据来源矩阵

| Wireframe 字段 | 来源层 | Python 现有接口 | 缺口 |
|---|---|---|---|
| enterprise_code / 统一社会信用代码 | 企业主数据 | ✅ `/enterprises/compare` org_id | 无 |
| 名称、地区、产业领域、企业类型 | 企业主数据 | ✅ `/enterprises/compare` name_cn/province/industry_class_name | 无 |
| 风险等级 | 企业摘要 | ✅ `/enterprises/compare` risk_level | 无 |
| 引育标签 | 已授权摘要 | ✅ `/enterprises/compare` tags/tags_flat | 无 |
| 最近操作时间 | **篮状态** | ❌ | Java 业务层 |
| 数据更新时间 | 企业数据 | ⚠️ ES 文档 updated_at（待确认） | 可能需补 |
| source_routes[] | 加入动作记录 | ❌ | Java 业务层 |
| basket_count / 50 | 单用户单篮状态 | ❌ | Java 业务层 |
| 篮持久化 / 恢复 / return_context | 篮状态 | ❌ | Java 业务层 |
| 候选名单（招引/培育） | 名单管理 | ❌ | Java 业务层 |

### 2.3 结论

- **Python 数据侧（data-agent）：无新增任务**。`/enterprises/compare`（ES mget）已覆盖对比篮卡片所需的全部企业摘要字段。
- **Java 业务层（api-agent）：需新增任务**。篮持久化、篮内搜索/筛选、勾选状态、return_context、候选名单管理，全部是 Java 应用层职责（与已派发的 `ENT-JAVA-SEARCH-BIZ` 同类）。

---

## 3. 企业评估（EVAL）分析

### 3.1 功能定位（Wireframe v1.6）

企业评估是**任务驱动型**评估系统：
1. **配置工作区 F-EVAL-01**：从对比篮带入企业 → 选模式（技术力/商业力/综合竞争力）→ 选指标 + 配权重 → 数据覆盖预检 → 生成评估
2. **生成过程 F-EVAL-06**：六阶段异步任务（提交→校验→数据汇聚→指标计算→可信校验→结果组装）
3. **结果工作区 F-EVAL-02**：KPI 卡 + 雷达/排名/诊断 + 单企诊断/双企对比 + 报告
4. **最近评估 F-EVAL-03**：历史任务列表 + 恢复结果 / 按此配置新建
5. **指标说明抽屉 F-EVAL-07**：业务口径 + 评审追加 metric_id/公式/源表

### 3.2 现状盘点

| 层 | 仓 | 现状 | 缺口 |
|---|---|---|---|
| 算法侧 | `demo-algo-ent-analysis` | `/v1/score` `/v1/ranking` `/v1/diagnosis` `/v1/centrality` `/v1/risk`——**列表查询型**（level/chain/keyword 过滤全表，权重写死 settings.yaml）；task_manager 是 GDF 批量灌数，非交互式评估 | **缺**：按企业集合 + 自定义权重的交互式评估计算接口 |
| 数据侧 | `demo-svc-topic-py` | **无任何评估端点**；现有 `gkx_search_service` 子项目是检索+详情（ES 主导），不含模型编排；预设计的 `gkx-ai-service`（推理+推荐+推演）尚未落地 | **缺**：新建 `gkx_ai_service` 子项目（与 gkx_search_service 平级，共用 gkx_common），承担评估任务编排层 |
| Java 侧 | `lumen-svc-platform` | **无任何评估端点** | **缺**：Feign 对接 + 对外 `/topic/v1/evaluation/*` |
| 产品定义 | agent-handoffs | EVAL 四件套齐（IA/USM/TRACE/Wireframe v1.6）；METRIC-OPEN/PDR 任务已 ready | 定义层不阻塞实现层 |

### 3.3 调用链设计（屏蔽层模式）

```
前端 → Java(gkxlumen-topic) /topic/v1/evaluation/*
         → 数据侧Python(gkx_ai_service) /internal/gkx-ai/evaluation/*   ← 新建子项目，与 gkx_search_service 平级
              ├─ 任务创建/状态/结果/历史/模板（gkx_ai_service 自管 PG 表）
              ├─ 数据预检（调 gkx_search_service 既有企业数据 /internal/gkx-search/* + ES 覆盖度）
              └─ 评估计算（HTTP 调 算法侧 entan /v1/evaluation/*  ← 需算法组先扩展）
```

> **服务归属**：评估 = 调基础数据 + 模型计算 + 任务编排，按架构预设计 §8 归 `gkx-ai-service`（推理+推荐+推演，调①②③+模型），**不属于** gkx-search-service（检索+详情）。当前 `demo-svc-topic-py` 仓采用 monorepo 多子项目结构（`gkx_search_service/` + `gkx_common/` 平级），评估编排层新建 `gkx_ai_service/` 子项目，与 `gkx_search_service/` 平级，共用 `gkx_common/`。

### 3.4 三层任务拆解

| 任务 ID | Agent | 仓 | 范围 | 依赖 |
|---|---|---|---|---|
| `ENT-ALGO-EVAL-INTERACTIVE` | algorithm-agent | demo-algo-ent-analysis | entan 扩展交互式评估接口（按企业集合+自定义权重计算 score/ranking/diagnosis/radar） | 无（算法组独立） |
| `ENT-PY-EVAL-TASK` | data-agent | demo-svc-topic-py | **新建 `gkx_ai_service/` 子项目**（与 gkx_search_service 平级，共用 gkx_common）+ 评估任务编排层（7 端点 `/internal/gkx-ai/evaluation/*`）+ 屏蔽 entan + 数据预检 + Mock 兜底 | **硬依赖** ENT-ALGO-EVAL-INTERACTIVE（算法接口就绪后才能联调；Mock 模式可先行） |
| `ENT-JAVA-EVAL` | api-agent | lumen-svc-platform | Java Feign 对接 gkx_ai_service 评估端点 + 对外 `/topic/v1/evaluation/*` | **硬依赖** ENT-PY-EVAL-TASK |

> **分阶段策略**：ENT-PY-EVAL-TASK 可先以 **Mock 模式**开发（gkx_ai_service 自造评估结果 Mock），不阻塞前端联调；待 ENT-ALGO-EVAL-INTERACTIVE 就绪后切换为 HTTP 调 entan。这样三层可并行起步。

---

## 4. 本次派单范围

用户要求"给 data-agent 创建任务并派发"。本次派发：

| 任务 | Agent | 说明 |
|---|---|---|
| `ENT-PY-EVAL-TASK` | data-agent | 企业评估任务编排层（gkx_search_service，7 端点，Mock 优先） |
| `ENT-JAVA-COMPARE-BASKET` | api-agent | 对比篮 Java 业务层（篮持久化/候选名单/return_context，无 Python 依赖） |

**未派（登记待后续）**：
- `ENT-ALGO-EVAL-INTERACTIVE`（algorithm-agent）—— 本次用户未要求派算法组；在 task-registry 登记 backlog，标注为 ENT-PY-EVAL-TASK 的硬依赖
- `ENT-JAVA-EVAL`（api-agent）—— 依赖 ENT-PY-EVAL-TASK，待 data-agent 产出 API 契约后派

---

## 5. 架构合规自检（铁律 9 条）

| # | 铁律 | 本次 | 说明 |
|---|---|---|---|
| 1 | 算法只在 Python | ✅ | 评估计算归 entan（Python）；Java 不写算法 |
| 2 | 调用链前端→Java→Python `/internal/*` | ✅ | 评估经 Java→gkx_search_service→entan；对比篮经 Java 业务层 |
| 3 | 图谱 NebulaGraph | N/A | 本次不涉图 |
| 4 | 可观测性全栈 | ✅ | gkx_search_service 已有 OTel；新端点继承；Java 透传 trace 头 |
| 5 | CI/CD push→Pipeline→K8s | ✅ | demo-svc-topic-py / lumen-svc-platform 均有 CI |
| 6 | demo2 不 merge lumen | ✅ | 本次在 demo-svc-topic-py（数据侧）+ lumen-svc-platform（Java 侧），无 demo→lumen 直 merge |
| 7 | 方案 A 共享 gkxlumen-topic | ✅ | 评估/对比篮均经 gkxlumen-topic |
| 8 | 数据走 ADS / Java 只读 | ✅ | gkx_search_service 读 ES/PG；Java 不直读库 |
| 9 | D8 前端规范 | N/A | 本次不涉前端 |

---

## 6. 风险

| 风险 | 等级 | 缓解 |
|---|---|---|
| ENT-ALGO-EVAL-INTERACTIVE 未就绪，ENT-PY-EVAL-TASK 无法联调真实算法 | 中 | Mock 优先，三层并行起步；切换 entan 时仅改 gkx_search_service 内部 HTTP 客户端 |
| EVAL Wireframe 指标受 Q014（权重）/K-O7（数据源）阻断 | 中 | Mock 阶段用临时默认权重 + ⚠️ 待确认角标；不替甲方拍板 |
| 对比篮 GAP-IMPL-02（正式持久化契约）未闭合 | 低 | demo 阶段浏览器存储 + 🟡；Java 任务范围内实现 PG 持久化即可闭合 |
