# Handoff：ENT-JAVA-EVAL

- **时间**：2026-07-28
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`；文档仓 `gkx-orchestration` / `dev`
- **派单包**：`ENT-JAVA-EVAL-派单包.md` v3.2
- **状态**：`review`（代码 commit `7bd6c59`，待 push / coordinator 验收）
- **前置**：Phase 0 Feign D-30 body-only 已 push（`4d8cf0e`）；`ENT-JAVA-ANALYSIS-CORE` done；`ENT-PY-EVAL-TASK` done

## 1. 范围与实现

落仓 **`gkxlumen-topic-async-service`**（与 CORE 同仓、同注释/子目录风格）。

| 能力 | 服务内 | 对外（网关 StripPrefix=1） | 实现 |
|---|---|---|---|
| industries | `POST /topic/v1/evaluation/industries` | `/topicAsync/topic/v1/evaluation/industries` | Feign `evalIndustries` 透传 |
| indicators | `POST /topic/v1/evaluation/indicators` | 同上 | Feign `evalIndicators` |
| precheck | `POST /topic/v1/evaluation/precheck` | 同上 | Feign `evalPrecheck` |
| compare | `POST /topic/v1/evaluation/tasks/compare` | 同上 | 校验归属+success+企业范围后 Feign `evalCompare`（body.`task_id`，D-30） |
| templates* | `/topic/v1/evaluation/templates**` | `/topicAsync/.../templates**` | MySQL `evaluation_template`，不转发 Python |

**不做**：第二套 tasks/status/result/history；不改 Adapter；不写算法；不直连 entan。

## 2. 偏离说明（as-built）

| 项 | 派单 / 旧契约 | As-built | 理由 |
|---|---|---|---|
| 落仓 | 曾写 enterprise | `gkxlumen-topic-async-service` | 与 CORE 同异步编排仓；网关 `/topicAsync` |
| Feign 名 | `RemoteEnterpriseAiPythonClient` | `RemoteTopicAsyncAiPythonClient` | CORE 迁移后真名 |
| compare 路径 | 契约曾写 `/{taskId}/compare` | 前端 body.`taskId`；Feign `/tasks/compare` + body | D-30；与 Python v3.4 对齐 |
| 模板字段 | 临时默认 `industry_code` | DDL 列名 `industry`（派单包骨架） | 🟡 待产品确认命名 |
| 权重单位 | 未定 | 模板存整数 0–100 快照 | 🟡 调 Python 时按契约再转换 |

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| DDL + seed | `db/9x_gkxlumenx_topic_enterprise.sql`（`evaluation_template` + 3 系统模板） |
| DTO / Entity | `api/dto/evaluation/*`、`api/entity/EvaluationTemplateEntity` |
| Controller | `controller/evaluation/EvaluationAssistController`、`EvaluationTemplateController` |
| Service | `service/evaluation/**`、`service/impl/evaluation/**` |
| Mapper | `mapper/evaluation/EvaluationTemplateMapper` |
| 单测 | `EvaluationAssistServiceImplTest`（+既有 Adapter 单测） |
| catalog | `API-ENT-full-catalog.md` #113–121 |
| 本 handoff | `ENT-JAVA-EVAL.md` |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven 单测 | ✅ `EvaluationAssistServiceImplTest` + `AnalysisAdapterValidationTest`（实现会话 12 tests 绿） |
| 无第二套任务中心 | ✅ 无 `/evaluation/tasks` create/status/result/history |
| compare 校验 | ✅ 归属 / `enterprise_eval` / `success` / 企业 ∈ `target_params` |
| 系统模板 seed | ✅ `TPL-SYSTEM-{TECHNOLOGY,BUSINESS,COMPETITIVENESS}` |
| push `origin/dev` | ⏳ 本地 commit `7bd6c59`，待 push |

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 Feign 透传 |
| 2 | 调用链 | ✅ 前端 → Java → `/internal/gkx-ai/**` |
| 3 | 图谱 | N/A |
| 4 | 可观测性 | ✅ 沿用平台 OTel |
| 5 | CI/CD | ⏳ push 后跟 Pipeline |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ async-service 编排门面 |
| 8 | 数据策略 | ✅ 模板表先行 + seed |
| 9 | 前端规范 | N/A |
| 10 | 数据血缘 | ✅ 预览/透传字段不改写；Mock 由 Python 返回 |

## 6. cost 四字段（估计）

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~180000（含 Phase0 联调核对 + Wave A/B/C，粗估） |
| `model_used` | cursor-grok-4.5 / 实现子会话 |
| `actual_cost` | ~$3.5（粗估，&lt;$10） |
| `cost_warn` | green |

## 7. 开放项

1. 对目标库执行 `evaluation_template` DDL + seed
2. 与 AI Python 联调 industries/indicators/precheck/compare（注意 compare 依赖 `_raw_scores`）
3. 🟡 权重单位 / industry 字段名 / precheck 阈值：见实施方案 §4，上线前甲方确认
4. `API-ENT-EVAL-contract.md` v4 路径仍偏旧，以 catalog / as-built 为准（可另开 doc 对齐）
5. commit + push 后由 coordinator 验收转 `done`
