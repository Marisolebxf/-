# 派单包：ENT-DEEP-GAP-L01 — 企业深度三缺口（历程/招引/培育）

- **任务 ID**：ENT-DEEP-GAP-L01
- **派发角色**：coordinator-agent
- **承接角色**：algorithm-agent
- **监管人**：human:唐绍祖
- **effort / difficulty**：8 / L · est.tokens 300k
- **优先级**：P1（部署 P0 完成后）

---

## 1. 背景

联调台 `/entan` 招标组 9 子页中，3 页 **无后端 REST**：

| UI | 招标 | 现状 |
|----|------|------|
| `/entan/history` 发展历程 | 企业深度 | Empty 占位 |
| `/entan/attract` 招引推荐 | 招引推荐模型 | 无 entan API；`demo-algo-science/innov/analysis/attraction.py` 有 async 能力 |
| `/entan/cultivate` 培育推荐 | 培育推荐模型 | 同上 `cultivation.py` |

属 **bid-reference 未对齐**，非 UI  alone 可闭合。

---

## 2. 范围（方案二选一，handoff 须 as-built）

### 方案 A（推荐 demo 快路径）

1. 在 `demo-algo-ent-analysis` 新增：
   - `GET /v1/history` 或 `/v1/roadmap`（读 ADS 或 mock seed）
   - `POST /v1/recommend/attract`、`POST /v1/recommend/cultivate`（薄封装，可调 innov 算法或内联规则）
2. 前端 `src/api/entan` 接线，Empty → 真实图表/列表
3. 网关 `/entan/**` 已通（依赖 ALGO-GATEWAY-ROUTE-SYNC-L01）

### 方案 B（迁算法）

将 `attraction.py` / `cultivation.py` 迁入 entan-py 模块，统一 `/v1/**`；innov 仅保留创新监测。

---

## 3. 不在范围

- lumen 正式 Java 门面（另开 tech_task）
- 甲方口径：招引/培育评分权重（🟡 待确认则 UI 角标）

---

## 4. DoD

- [ ] 三页 Network 无 404，有 `{code:0}` 或明确业务空态
- [ ] handoff 对照 bid §企业深度分析
- [ ] 架构 D1：算法只在 Python

---

## 5. /goal 话术

```markdown
/goal algorithm-agent
任务 ID：ENT-DEEP-GAP-L01
监管人：human:唐绍祖
必读：ENT-DEEP-GAP-L01-派单包.md、demo-ui-system-test/src/views/entan/entanMenuConfig.ts
目标：历程 + 招引 + 培育 REST 与 UI 闭环。
```
