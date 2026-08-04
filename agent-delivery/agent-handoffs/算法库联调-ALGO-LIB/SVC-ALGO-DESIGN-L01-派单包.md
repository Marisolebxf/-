# 派单包：SVC-ALGO-DESIGN-L01 — 产业服务（服务机构）算法设计

- **任务 ID**：SVC-ALGO-DESIGN-L01
- **派发角色**：coordinator-agent
- **承接角色**：algorithm-agent
- **监管人**：human:唐绍祖
- **仓**：`${GKX_ROOT}/repos/demo-algo-ent-analysis`
- **认领**：`claimed` · `coordinator_dispatch` · lock 至 `2026-08-04T16:00:00+08:00`
- **派发时间**：2026-08-04
- **effort / difficulty**：8 / L · est.tokens 500k
- **cicd**：`skip_design_only`（本阶段仅设计）

---

## 1. 背景

招标 `科技专题服务算法库.md` **§1.1.1.1.1.1.1.9 产业服务深度分析模型构建** 定义 10 类服务机构相关模型。联调台将灰显「产业服务算法库」占位，需先补齐算法设计说明，再进入实现波次。

仓选定：`demo-algo-ent-analysis`（与 entan/polan/chain 同仓扩展；可新建 `svcan/` 或等价包名，设计阶段先定目录与章节即可）。

## 2. 范围（必做 · 设计）

对照招标覆盖以下 **10 模型**（顺序保持招标）：

1. 服务链短板分析模型  
2. 服务关系链模型  
3. 金融服务机构技术力评价模型  
4. 知识产权服务机构技术力评价模型  
5. 人力资源服务机构技术力评价模型  
6. 市场营销服务机构技术力评价模型  
7. 咨询服务机构技术力评价模型  
8. 科技创新服务机构技术力评价模型  
9. 服务机构引入推荐模型  
10. 服务机构培育推荐模型  

每模型章节须含（对齐既有《算法设计说明》体例）：

- 业务语义与适用场景  
- 输入 / 输出契约  
- 指标、权重、阈值草案（待甲方确认标 `pending_client`）  
- 数据依赖（ADS / DWD / Nebula 图谱；标明缺口）  
- API 草图（建议挂 `/internal/*` 或未来 `/v1/svc/*`，**Java 不写算法**）  
- 与联调台「产业服务算法库」子页映射表  
- Mock vs 真实数据策略  

**不做**（本任务）：完整 Python 实现、灌数流水线、联调台页面实现。

## 3. 口径与合规

- 业务口径歧义 → 登记 `客户决策清单跟踪表.md`（🟡），禁止替甲方拍板  
- 算法只在 Python（架构铁律）  
- 图谱引擎 NebulaGraph，禁止 Neo4j 生产路径  

## 4. DoD / 产物

见 registry `SVC-ALGO-DESIGN-L01.definition_of_done`。

建议产物路径：

- `repos/demo-algo-ent-analysis/算法设计说明.md` 新增「产业服务/服务机构」章  
- 或 `docs/产业服务算法设计说明.md` + 主文档交叉引用  

完工 handoff：`agent-handoffs/算法库联调-ALGO-LIB/SVC-ALGO-DESIGN-L01.md`

## 5. /goal 话术

```markdown
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法/数据科学工程师，精通 Python、指标工程、知识图谱与可解释模型；算法只在 Python，权重/阈值进 config，禁止 Java 写算法。
任务 ID：SVC-ALGO-DESIGN-L01
监管人：human:唐绍祖
仓库：${GKX_ROOT}/repos/demo-algo-ent-analysis
必读：
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/SVC-ALGO-DESIGN-L01-派单包.md
  - agent-delivery/bid-reference/科技专题服务算法库.md §1.1.1.1.1.1.1.9
  - repos/demo-algo-ent-analysis/算法设计说明.md（体例）
  - agent-delivery/task-registry.yaml#SVC-ALGO-DESIGN-L01
目标：产出产业服务（服务机构）10 模型算法设计说明；口径歧义登记决策清单；本阶段不强制编码实现。
DoD：见 registry；handoff；status→review；cost 回填。
明确开工后将本任务改为 in_progress。可与 COMP-ALGO-DESIGN-L01 并行（注意同文件 Convoy：先约定章节归属或串行写同一 md）。
不要问我，按派单包执行。
```

## 6. Convoy 提示

与 `COMP-ALGO-DESIGN-L01` 同改 `算法设计说明.md` 时：约定分章互不覆盖，或一人先提交再 rebase；硬冲突则串行。
