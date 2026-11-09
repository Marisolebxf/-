# 落地实效 · 宏观/行业结果面代理长任务总控

> **日期**：2026-11-09  
> **授权**：`human:淮政玮`（当次会话要求「按建议落地，编排长任务」）。授权句：**后续认领不必再问**。  
> **目标**：用三方**宏观行业要素库**（主）+ **行业分析要素库**（辅）重做城市级「落地实效」可算路径；同步算法、算法中台与 lumen 专题应用；正本三维缺口诚实保留。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。  
> **依据**：`加工/GKX数据源表及行数报告-20261109-1026.MD` 宏观/行业分析两库；`M_POLICY_IMPLEMENTATION_EFFECT.md` 正本三维仍为「完全不支持」；建议取舍见 2026-11-09 会话分析。  
> **派单**：[`POL-EFFECT-MACRO-总派单.md`](./POL-EFFECT-MACRO-总派单.md)  
> **不替代**：[`LUMEN-POLICY-SZ3D-长任务总控.md`](./LUMEN-POLICY-SZ3D-长任务总控.md)（深圳 UI/需规 114–116）；本管线只改实效**算法与取数**，配置区 10 项清单不变。

| 段 | 仓 | 分支 | task-id | 依赖门 |
|----|-----|------|---------|--------|
| A0 | `gkx-orchestration` | `origin/dev` | `POL-EFFECT-MACRO-CALIBER-L01` | 无。口径 + calc-logic + 详设 §3 增补 |
| A1 | `gkx-orchestration` + 只读 `gkx` | `origin/dev` | `POL-EFFECT-MACRO-DATA-L01` | A0 ≥ `integration`（会签中可并行草稿，门禁以联调闸门为准） |
| B | `demo-algo-ent-analysis` + `lumen-algo-py` | `origin/dev` | `POL-EFFECT-MACRO-ALGO-L01` | A0 口径稿落盘；A1 指标白名单与区划键就绪 |
| B2 | `demo-ui-system-test` | `origin/dev` | `POL-EFFECT-MACRO-MID-L01` | B ≥ `integration` |
| C | `lumen-svc-platform` | `origin/dev` | `POL-EFFECT-MACRO-JAVA-L01` | B ≥ `integration` |
| D | `lumen-ui-topic` | `origin/dev` | `POL-EFFECT-MACRO-FE-TOPIC-L01` | C ≥ `integration` |
| E0 | 发布 | K8s `dev` | `POL-EFFECT-MACRO-E0-DEVOPS-L01` | D ≥ `pending_test` |
| E1 | qa | 已发布前端 | `POL-EFFECT-MACRO-E1-QA-L01` | E0 点名 deploy 绿 |

锁：`lock_hours=24`。升级人：结构歧义 `human:李伟`；口径争议挂 `QPOL-02` / 新项，**不停工**（临时默认见 §0）。  
Epic：`E-POLICY-PDR`。`claim_type=coordinator_dispatch`，`supervised_by=human:淮政玮`。

---

## 0. 已拍板

| # | 决定 |
|---|------|
| 1 | **正本三维**（启动日 / 支持对象 / 反馈调查）不因本管线宣告「已支持」；缺维仍诚实，禁止把空写成 0 |
| 2 | **城市卡落地实效现行可算路径**改为**宏观结果面代理**（P0）：`gkx.dwd_macro_index_data` + `dwd_dim_index_attribute` + `dwd_dim_admin_area`；窗口与指标白名单由 A0/A1 冻结 |
| 3 | **行业分析**（P1）只作辅维/叙述：`dwd_industry_analysis_documents` + topics/content_types/industries；`companies`（102 行）**禁止**当受益企业名单 |
| 4 | **metric_id 策略（临时默认，挂 QPOL-02）**：深圳结果板 `cards.effect` 继续挂 `M_POLICY_IMPLEMENTATION_EFFECT`，但 `ext.caliber=macro_outcome_proxy` + UI ⚠️「待甲方确认」；正本三维公式保留在 calc-logic 并标明「正本·当前不可算」；甲方归一前 **不出综合分** |
| 5 | **D17**：若与唐绍祖锁定合规闭包冲突，合理探索落副本包/路由，中台展示名成对「落地实效性-合规 / -合理」；无冲突则单名 + 角标 |
| 6 | 调用链不变：前端 → Java → Python `/internal/*`；Java 不写算法、不直连三方 `gkx` |
| 7 | 三方库只读；落库只允许 Demo ADS / 既有 ADS 契约表（或 A1 指定的只读汇聚面）；禁止写供应方库 / 正式 ODS；缺项补齐仍只进 `gapfill_` |
| 8 | 算法双仓同文：`demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py` |
| 9 | 前端推送默认人工确认（`fe-manual-confirm-push`）；总控未写「完工即推」则 FE 停本地等确认 |
| 10 | 废作：用宏观值冒充启动率；用研报条数冒充满意度；用 `companies` 冒充覆盖种类；旁路按钮绕开算法库 Mock 写 gapfill（gapfill 演示路径仍有效，与本结果面代理并存） |

## 1. 废作

| 项 | 原因 |
|----|------|
| 宣称两库「直接支持」正本三维 | 无 `policy_id` / 实施日 / 问卷 |
| `dwd_industry_analysis_companies` 当覆盖维 | 仅 102 行 |
| 静默覆盖王惠正本三维公式且不标临时默认 | 违反口径诚实与 QPOL-02 |
| 接口硬编码 mock 分进 `cards.effect` | D18 / 禁止写死 |

## 2. 依赖（联调闸门）

```text
A0 口径 ──┬──> A1 白名单/区划
          └──> B 算法（可与 A1 末段并行，但白名单未冻不得标 integration）
B ──> B2 算法中台
B ──> C Java
C ──> D FE 专题
D ──> E0 ──> E1
```

前序 `POL-IMPL-EFFECT-MOCK-VIA-UI-L01`（gapfill 双入口）= **done**，本管线**不回退**；结果面代理与 gapfill 三维补空**并存**（代理服务城市卡；gapfill 服务正本维可读时的补齐）。

## 3. 金路径（E1）

| # | 故事 | 已发布路由 | 期望（未发生=红） | 允许空态 |
|---|------|------------|-------------------|----------|
| 1 | US-E7-POL-04 | `/policy/recommendation` 结果板 | `cards.effect.computable=true` 且非 0；`ext` 含 `macro_outcome_proxy`（或会签后的正式键）；有 ⚠️/待确认语义 | 宏观源不可达时 `computable=false` 且**不写 0** |
| 2 | 同上 | 切换对比城市（若页支持） | 分数随城市宏观截面变化，非常量 | 无第二城市数据则该城空态 |
| 3 | 算法中台 | `demo-ui-system-test` 政策算法相关页 | 可见新口径说明 + 试算/结果非写死 | — |
| 4 | 回归 | 深圳页支持力度/适配性 | 两卡行为与 SZ3D 金路径一致，本管线未改坏 | — |

## 4. 认领

授权句已由 `human:淮政玮` 于 2026-11-09 落款：**后续认领不必再问**。coordinator 按 DAG `ready` → `coordinator_dispatch`。
