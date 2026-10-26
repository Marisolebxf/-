# 深圳政策现状分析 · 固定指标卡长任务总控

> **日期**：2026-10-24  
> **授权人**：待监管人落款（E7 既有管线监管人为 `human:淮政玮`）。**本文件尚未写入「后续认领不必再问」**。补上该句之前，coordinator 不得无人值守认领。  
> **目标**：`/policy/recommendation` 从「自由勾选二级指标 + 34/33/33」改为三张固定指标卡，结果与 `M_POLICY_SUPPORT_STRENGTH` 口径一致。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。  
> **设计真源**：[`FUNC-DESIGN-E7-政策分析.md`](../产品整体定义/E7-政策分析/FUNC-DESIGN-E7-政策分析.md) §3.6 / §4.3 **v0.7**。实现方案：[`05.6.2-深圳政策现状分析.md`](../产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md)。故事：USM v1.4.9 `US-E7-POL-04`。线框：Wireframe §6 v1.4.6。  
> **派单**：[`LUMEN-POLICY-SZ3D-总派单.md`](./LUMEN-POLICY-SZ3D-总派单.md)  
> **不替代**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) 的时序 / 区域对比 / 门户。本管线只改深圳三维。

| 段 | 仓 | 分支 | task-id | 依赖门 |
|----|-----|------|---------|--------|
| B | `lumen-algo-py` | `origin/dev` | `LUMEN-POLICY-SZ3D-B-JOB-L01` | 无前序任务。设计 v0.5 已落盘 |
| C | `lumen-svc-platform` | `origin/dev` | `LUMEN-POLICY-SZ3D-C-FACADE-L01` | B ≥ `integration` 且 handoff 含结果板字段 |
| D | `lumen-ui-topic` | `origin/dev` | `LUMEN-POLICY-SZ3D-D-FE-L01` | C ≥ `integration` |
| E0 | 发布 | K8s `dev` | `LUMEN-POLICY-SZ3D-E0-DEVOPS-L01` | D ≥ `pending_test` |
| E1 | qa | 已发布前端 | `LUMEN-POLICY-SZ3D-E1-QA-L01` | E0 点名 deploy 绿。禁止逐叶 QA |

锁：`lock_hours=24`（仅在授权句落款之后使用）。升级人：结构歧义 `human:李伟`。`QPOL-02` 不升级、不停工。  
Epic：`E-POLICY-PDR`。Sprint：`2026-W43`。五叶初始状态全部 `backlog`。

---

## 0. 已拍板（执行勿再改回勾选模型）

| # | 决定 |
|---|------|
| 1 | 三维框架保留为三张卡：`M_POLICY_SUPPORT_STRENGTH` / `M_POLICY_INDUSTRY_FIT` / `M_POLICY_IMPLEMENTATION_EFFECT` |
| 2 | 支持力度因子固定为政策条数、政策层级。扶持力度档位置 `null`，不置 0，不用 `dwd_bid_*` 金额 |
| 3 | 内部权重 0.5/0.5 冻结展示，待 `QPOL-02`。页面无 34/33/33 编辑，无二级勾选 |
| 4 | 产业 / 技术锚点只作用于产业适配性。支持力度是城市截面，不按锚点重算 |
| 5 | 落地实效 `computable=false`，不入综合分。`QPOL-02` 会签且实效可算之前**不出综合分** |
| 6 | 结果标明：供给规模与层级合成、条数主导、非资金强度、min-max 不可当趋势。深圳市级为主导致层级分偏低，不写成「政策弱」 |
| 7 | `GET .../indicators?kind=all` 仍是分布接口，不做指标目录 |
| 8 | 调用链不变：前端 → Java → Python `/internal/policy/jobs/execute`。Java 不写算法 |
| 9 | `USE_MOCK=false` 禁止用 Demo `POLICY_SZ_CORE_INDICATORS` 填卡片 |
| 10 | 监管与认领：授权句落款前全部 `backlog`。落款后 `supervised_by` 用落款人，`claim_type=coordinator_dispatch` |
| 11 | 优化建议复用时序解读润色：规则定卡，模型只改 `conclusion`。落地实效与综合分不出建议卡。合同见详设 `05.6.2` §5 |

## 1. 废作（不得当依赖、不得再派成「把勾选接上」）

| 项 | 原因 |
|----|------|
| 配置页 `parseSzPool(indicatorResp.items)` 当核心指标目录 | 分布实包没有 `dimKey=support\|fit\|effect` 的二级行 |
| Demo 二级池：资金规模、创新激励、执行率、受益覆盖、满意度 | 支持力度无金额列；落地实效完全不支持 |
| 空目录时 `indicatorOk=true` 从而绿条「可开始分析」 | 与「目录暂时没到」不是同一件事 |
| 前端按勾选列表本地加权 | 正式分只认 Python 结果板 |

## 2. 段 E 金路径（5 条）

已发布专题前端，`US-E7-POL-04`：

1. 打开 `/policy/recommendation`：三张卡可见；无二级勾选；无一级权重步进器。
2. 未选锚点时开始分析禁用。选中合法产业后可提交。
3. 支持力度结果含深圳条数、层级均值、分数、名次；档位不是 0；文案含非资金强度。
4. 更换产业后，支持力度城市截面分数不变；适配性请求范围变化。
5. 落地实效整卡空；页面无三维综合分。

期望未发生必红。QA 不改代码。

## 3. 认领

补写授权句「后续认领不必再问」并署名 `human:{花名册真名}` 之后，coordinator 才可按 DAG 把满足门禁的叶标 `ready` 并 `coordinator_dispatch`。在此之前本文件只是编排，不是开工令。
