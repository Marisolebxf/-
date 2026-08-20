# CHAIN-INST-DATA-ANALYSIS-L01 · 产业链和国内机构库数据源分析与更新（收口）

> 日期：2026-08-20  
> Task：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 类型：`spike`（分析探针，不写业务仓代码）  
> 现行存储入口：[`storage/CHAIN/README.md`](../../data/data-design/storage/CHAIN/README.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:李伟` |
| supervised_by | `human:李伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-07-23 认领；分析阶段 07-29 起；08-07 冻结 Q053；08-20 按现行 v5 收口，不改代码。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义 / 数据源分析 spike，不以缩代码为目标。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本单未改存储流图） |
| 图 diff | 无。流图会签在 `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` / `01-data-flow.md` |
| 会签态 | 流图 `approved`（S1，非本单产物） |
| 说明 | 本 spike 产出 DWD v5 目标结构与 ODS 映射，不翻签流图。 |

## 范围与实现

- **范围**：只读分析 `gkx` / Demo ODS 产业链与国内机构库；输出映射报告；把目标 DWD 从旧 7 表 mock 收到 **v5 十四表**；冻结平台主键 **Q053=INB**。
- **对照**：招标产业链叶子、`catalog-topic-industry.yaml` IC-01～IC-43、客户决策清单 §2.y。
- **非范围**：Java `/internal/*`、生产 ETL、灌数验证、lumen 复刻、v5 三方会签、DWD vs demo 对比。

DoD 对照（registry 原文 5 条）：

| # | DoD | 本单 |
|---|-----|------|
| 1 | 产业链数据源分析报告 | ✅ `产业链-ODS到DWD字段映射分析报告(v3).md` + Step2 复核 |
| 2 | 国内机构库数据源分析报告 | ✅ `国内机构库-ODS到DWD字段映射分析报告.md` |
| 3 | 更新数据模型和映射关系 | ✅ DWD v5 + Q053 DEC；细表导航以 `storage/CHAIN` 为准 |
| 4 | 更新 `/internal/*` 接口 | ⏭ 转走，见偏离 |
| 5 | 验证数据接入和处理流程 | ⏭ 转走，见偏离 |

## 偏离说明

| 项 | DoD 原文 | 处理 | 转给 |
|----|---------|------|------|
| DoD-4 | 更新 `/internal/*` 以支持新数据源 | 本 spike 不做接口 | 后续 Java / 算法实现单；Demo 读面已在 `DEMO-CHAIN-SIM-PROCESS-L01` 等 |
| DoD-5 | 验证数据接入和处理流程 | 本 spike 不做灌数验收 | `DEMO-CHAIN-SIM-PROCESS-L01`（integration）；联调台灌数主路径 |
| 旧 7 表 DWD | 07-29 阶段性稿按 `chain_*` 七表写 | 已被 v5 `industry_chain_*` 十四表替代 | `产业链-DWD表设计-业务需求驱动(v5).md`；stores `dwd-chain.md` |

不把 Q054 / Q055 数据未到当作本单未完成。

## 产物清单

| 产物 | 路径 |
|---|---|
| 产业链 ODS→DWD 分析（v3，过程稿） | `agent-delivery/data/data-design/产业链/产业链-ODS到DWD字段映射分析报告(v3).md` |
| 字段对照明细 | `…/ODS-DWD-字段对照与缺失明细.md` |
| 国内机构库分析 | `…/国内机构库-ODS到DWD字段映射分析报告.md` |
| Step1 业务需求符合性 | `…/产业链-DWD表业务需求符合性分析(Step1).md` |
| Step2 ODS 复核 | `…/产业链-ODS到DWD字段映射复核报告(Step2).md` |
| DWD v5 目标结构 | `…/产业链-DWD表设计-业务需求驱动(v5).md` |
| Q053 编码冻结 | `…/DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md` |
| evidence 索引 | `…/CHAIN-INST-DATA-ANALYSIS-L01.md` |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-INST-DATA-ANALYSIS-L01.md` |

## 验收证据

- [x] 产业链四主源已梳理（结构 / tags / product_tags / news）
- [x] 机构库 13 张 ODS 已排查（主体表空；创新载体可灌基础字段）
- [x] 目标结构收到 v5 十四表；Q053 已冻结 INB
- [x] Q053–Q055 已登记 `客户决策清单跟踪表.md` §2.y（Q053 🟢，Q054/Q055 🔴）
- [x] 07-29 阶段性稿与 08-20 收口稿路径一致；冲突以 `storage/CHAIN` 为准
- [x] cicd: skip（无业务仓代码、无 pipeline）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单无算法实现 |
| 2 | 调用链 前端→Java→Python | ✅ 未越层；接口不在本单 |
| 3 | 图谱 NebulaGraph | ✅ 仅评估 institution Tag 可灌性，未写 nGQL |
| 4 | 可观测性 | ✅ N/A（文档 spike） |
| 5 | CI/CD | ✅ skip（无代码） |
| 6 | demo 不 merge 进 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / Java 只读 ADS | ✅ 分析未改 Java |
| 8 | 数据走 ADS（D3/D7） | ✅ 统计类明确不进 DWD |
| 9 | D8 / D10 | ✅ N/A |
| 10 | D12 lumen 不调 demo | ✅ 未改前端调用链 |

## 遗留风险

| 项 | 状态 | 谁接着 |
|---|---|---|
| v5 三方会签（架构 / API / 算法） | `CHAIN-DATA-L01` 仍 `integration` | 该单会签方 |
| DWD vs demo 对比 + D2 | `CHAIN-DATA-L02` `backlog` | 等 L01 会签 |
| 投融资正式源 | Q054 🔴 | 供应方 / 甲方；ADS 不写假金额 |
| 机构主体表空 | Q055 🔴 | 供应方 / 甲方 |
| stores 细表仍 draft | S3 已声明 | 不得仅凭本单标 approved |

## CI/CD

- 分支：编排仓文档（无业务仓 commit 要求）
- commit / pipeline：cicd skip；无 GitLab pipeline
- K8s / 镜像：skip
- 部署：无

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 300000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 1.62 |
| cost_warn | green |
| 说明 | 无 Console 分项；按 registry `estimated_tokens=300_000` 回填。价表 B 主力 Sonnet 4.5（$3 / $15 per M），in/out=80/20。source: estimate_fill |

*handoff · 收口 · [human:李伟] · 2026-08-20 · CHAIN-INST-DATA-ANALYSIS-L01*
