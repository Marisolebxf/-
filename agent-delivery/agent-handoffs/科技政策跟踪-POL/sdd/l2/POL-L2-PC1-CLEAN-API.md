# POL-L2-PC1-CLEAN-API · 政策数据治理 · 系统引用政策源数据清洗 · 后台接口设计

- 任务：`POL-L2-PC1-CLEAN-API`
- 日期：2026-11-08
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-07`
- 上游：`sdd/l2/POL-L2-PC1-CLEAN-ARCH.md`（本分册以它为准）；总控 `POL-PC1-SDD-IMPL-LOOP-长任务总控.md` §1.2 政策选择
- SRS 序号：**602**

本分册只定政策数据治理二级「系统引用政策源数据清洗」的后台接口。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、查询参数要点、同步、空态。不写 OpenAPI 字段表，不写实现代码。

602 与 603 共用一条公开资源 `GET /display/v1/policy/governance/results`，按区块分发。本分册只定 **清洗质量** 区块与同资源上的页眉附卡读法；结构化区块归 `POL-L2-PC1-STRUCT-API`。

## 1. 公开资源

前缀 `/display/v1/policy/`。浏览器经网关打 `gkxlumen-display`。不另开页。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 602 | `GET /display/v1/policy/governance/results` | 同步。不返回 501。element 只读第 6 项已有 DWD/ADS 结果 |

查询参数（契约冻结名；本分册用中文语义）：

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 处理状态 | 否 | 质量明细只保留该 `script_state.status`（六值闭包：`done/empty/no_match/degraded/failed/llm_unavailable`）。不选则全部 |
| 政策 id（`policyId`） | 否 | 总控 §1.2：**602 非强制**。库级规则/批次已够核增展示时可不暴露。若实现暴露，仅过滤质量明细；页眉 KPI / 规则 / 批次总览不随此改口径 |

## 2. 内部委托

| 公开资源 | 内部委托 |
|---|---|
| `governance/results` | `gkxlumen-display` 不直连库、不调 Python、不进异步。`gkxlumen-element` 只读 `gkxlumenx_dwd.policy_base_info`、`gkxlumenx_dwd.script_state`，以及同资源上 603 所需 ADS（本分册不展开 603） |

浏览器不改打 `/topic/v1/policy`，不打开算法中台，不打 `/v1/policy/**`。`E-E7-POLICY-M1-L06` 不是本路径。

失败语义：质量区块无行则空，不造 0；不清空同资源已返回的其它区块。

## 3. 602 清洗区块要点

一次 `GET …/governance/results` 返回（成功 HTTP，非 501）：

1. **质量聚合**：按 `script_state.job` × `status` 计数（全库，除非实现约定 job 过滤；默认含清洗相关 job）。无行 → 质量区空。  
2. **质量明细**：`script_state` 行级列表（可分页由契约定）。可被处理状态、`policyId` 过滤。  
3. **页眉附卡「库内政策数」**：读法对齐 `M_POLICY_TOTAL_COUNT`；D4=mock 时对齐前数值仍是 mock；**不受 `policyId` 影响**。  
4. **规则总览 / 批次总览**（若契约保留演示结构）：全库只读呈现；不随 `policyId` 改写。真实作业态以 `script_state` 为准，禁止接口直接返回写死分数。

不建清洗 Job。不重开 GDF。不调用 `polan`。

## 4. 与 603 / 604 / 605

| 资源 | 本分册 |
|---|---|
| 同资源结构化区块 | 归 STRUCT-API；可同一次响应按区块分发 |
| `governance/lineage-index` | 604，本分册不实现 |
| `governance/indicator-library` | 605，本分册不实现 |

## 5. 明确不做

- 不写字段表/DTO/枚举闭包正文（留给 BE-POL-CONTRACT-01）
- 不新造 `metric_id`；不把 `M_POLICY_VALIDITY_RATE` 改挂清洗 KPI
- 不写实现代码；不改 FE（实现段另叶；政策选择接线在实现段）
- 不允许接口函数直接返回 mock 质量分数

## 6. 签收

可实现：element 对 `script_state` / 主表的只读聚合 + 可选 `policyId` 过滤，经 display 原样返回。写成「再建清洗管道」或接口写死分数 → 不可签收。
