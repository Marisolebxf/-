# 派单包：COMP-ALGO-DESIGN-L01 — 产业综合分析算法设计

- **任务 ID**：COMP-ALGO-DESIGN-L01
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

招标 `科技专题服务算法库.md` **§1.1.1.1.1.1.1.10 产业综合分析模型构建** 定义 10 类区域综合/创新要素评价模型。联调台「产业综合分析算法库」灰显占位，需先补设计说明。

仓：`demo-algo-ent-analysis`（可规划 `comp/` 或等价包；设计阶段定目录与章节）。

## 2. 范围（必做 · 设计）

覆盖招标 **10 模型**（顺序保持）：

1. 区域科技创新成果综合评价模型  
2. 区域产业创新成果综合评价模型  
3. 区域产业创新人才综合评价模型  
4. 区域产业创新政策综合评价模型  
5. 区域创新活力综合分析模型  
6. 区域创新要素类型综合评价模型  
7. 区域创新要素层次综合评价模型  
8. 区域创新要素领域综合评价模型  
9. 区域创新要素综合分析模型  
10. 区域创新协同分析模型  

每模型须含：输入输出、指标与权重草案、**对前序要素算法（产业/技术/企业/人才/政策/服务）输出的依赖**、API 草图、联调台子页映射、Mock vs 真实。

**不做**：本阶段强制编码实现 / 联调台页面。

## 3. 口径与合规

- 歧义 → `客户决策清单跟踪表.md`（🟡）  
- 算法只在 Python；NebulaGraph；不替甲方拍板  

## 4. DoD / 产物

见 registry `COMP-ALGO-DESIGN-L01.definition_of_done`。

建议：`算法设计说明.md` 新增「产业综合分析」章，或 `docs/产业综合分析算法设计说明.md` + 交叉引用。

完工 handoff：`agent-handoffs/算法库联调-ALGO-LIB/COMP-ALGO-DESIGN-L01.md`

## 5. /goal 话术

```markdown
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法/数据科学工程师，精通 Python、多源指标融合与可解释综合评价；算法只在 Python，权重进 config。
任务 ID：COMP-ALGO-DESIGN-L01
监管人：human:唐绍祖
仓库：${GKX_ROOT}/repos/demo-algo-ent-analysis
必读：
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/COMP-ALGO-DESIGN-L01-派单包.md
  - agent-delivery/bid-reference/科技专题服务算法库.md §1.1.1.1.1.1.1.10
  - repos/demo-algo-ent-analysis/算法设计说明.md
  - agent-delivery/task-registry.yaml#COMP-ALGO-DESIGN-L01
目标：产出产业综合分析 10 模型算法设计说明；写明对前序模块依赖；口径歧义登记决策清单；本阶段不强制编码。
DoD：见 registry；handoff；status→review；cost 回填。
明确开工后改为 in_progress。与 SVC-ALGO-DESIGN-L01 并行时注意同文件 Convoy。
不要问我，按派单包执行。
```

## 6. Convoy 提示

与 `SVC-ALGO-DESIGN-L01` 同文件时分章互斥提交，或串行。
