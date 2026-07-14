# Handoff · ENT-MOD-SEARCH-V2-S1

> **状态**：待执行（模板已建；依赖 `ENT-MOD-SEARCH-V2-S0` done）  
> **task-id**：`ENT-MOD-SEARCH-V2-S1`  
> **父任务**：`ENT-MOD-SEARCH-V2-DEMO`  
> **监管**：`human:孔东`  
> **派单包**：`agent-delivery/sprints/ENT-MOD-SEARCH-V2-S0S1-派单包.md`

## 1. 范围与实现

- [ ] 1.1 `api/enterprise.ts` 五接口 `defineApi`  
- [ ] 1.2 `mock/enterprise/*`（≥30 条 + schema/parser/aggregates）  
- [ ] 1.3 `stores/compareBasket.ts`  

对照：`lumen-ui-topic-开发任务拆分规划.md` 阶段 1。

## 2. 偏离说明

（无 / 有则写 as-built）

## 3. 产物清单

| 项 | 路径 / 链接 |
|---|---|
| PR | |
| commit SHA | |
| API 清单 | |
| mock 条数与字段覆盖 | |

## 4. 验收证据

- [ ] `VITE_APP_USE_MOCK=true/false` 签名一致  
- [ ] 对比篮超限提示  
- [ ] `npm run build` 绿  

## 5. 架构合规自检

| # | 铁律 | ✅/❌ |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A |
| 2 | 前端 → Java REST（api 层切换） | |
| 3 | NebulaGraph | ✅ N/A |
| 4 | 可观测性 | |
| 5 | CI/CD | |
| 6 | demo 不 merge 进 lumen | |
| 7 | 共享聚合 / 不直连 nGQL | ✅ N/A |
| 8 | Design.md / Arco Vue | |
| 9 | 字段 metricId / pending | |
| 10 | D10 交互 | ✅ N/A（本阶段无 UI 页） |

## 6. cost 回填（完工必填）

```yaml
actual_tokens:
model_used:
actual_cost:
cost_warn: green
```
