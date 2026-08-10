# 派单包：ENT-MOD-OVERVIEW-ARCH-IMPL-L01

> ⚠️ **故事驱动拆单草案加厚包**（coordinator 批量生成 · 2026-08-03）  
> - 提案状态：`story-impl-proposals.yaml` → **proposed / 待审建单**  
> - registry：**尚未 merge**（须飞书「建单已采纳」或 `merge --approved-by`）  
> - **禁止**在 DG-G3 未 done + confirm 前把本 leaf 当 ready 开工编码（SEARCH 等已入库例外按 registry 实态）  
> - 规约：`自动派单与确认规约.md` §4.1 · `task-creation-guide.md` §16

- **派单方**：coordinator-agent（故事库全量强制补缺）
- **时间**：2026-08-03
- **执行 Agent**：`agent:architect-agent`
- **监管人**：`human:徐滕强`
- **仓 / 产物落点**：`agent-delivery`（相对 `${GKX_ROOT}/repos/` 或编排仓）
- **Epic**：E-ENT-SCRUM-PDR
- **模块**：E-31-企业发展（slug=OVERVIEW）
- **难度 / 点数**：M / 3
- **上游门3**：`ENT-MOD-OVERVIEW-DG-G3` · 当前 **MISSING（merge 时 auto-ensure）**
- **故事挂载**：US-E32-01,US-E32-02

---

## 1. 目标

确认实现期架构边界、调用链、契约与仓边界，输出可被 API/DATA/FE 消费的 ARCH-IMPL 纪要。

**标题（registry 草案）**：企业发展总览 — 实现期架构/契约确认（故事驱动草案）

---

## 2. 覆盖用户故事

| 故事 ID | 标题 | 库内 status |
|---------|------|-------------|
| US-E32-01 | 查看总体态势 | defined |
| US-E32-02 | 查看空间分布与科研人力 | defined |

### Theme 切片（Sprint Planning 参考 · 不入库）

| Theme | 故事 |
|-------|------|
| T1 | US-E32-01、US-E32-02 |

---

## 3. 范围（做）

- 对照 USM / Wireframe / TRACE，划定本模块 Java REST ↔ Python `/internal/*` ↔ ADS 边界
- 列出本模块必接端点清单与依赖契约（含枚举/字典）
- 标注 Convoy / 共享仓风险与禁止越层项
- 输出 `ARCH-IMPL-{slug}.md`（或模块等价路径）供下游 leaf 引用

## 4. 不做

- 不写业务功能代码、不改正式仓 main
- 不替甲方闭合业务口径 🟡 项
- 不引入 Neo4j / 前端直连图库或 Python
- 不自动把提案标 `ready`；ready 仍等门3 `*-DG-G3` done + confirm
- 不直接改 `task-registry.yaml`（须 MCP / merge 流程）

---

## 5. Definition of Done

1. ARCH-IMPL 纪要落盘，含调用链与端点表
2. depends_on 中 DG-G3 状态已记录（未 done 则标阻塞条件）
3. handoff + cost 四字段
4. 提案已 merge 进 registry（backlog）后方可认领；本文件可先作审阅说明书

---

## 6. 必读

| 优先级 | 路径 |
|--------|------|
| P0 | `agent-delivery/agent-handoffs/产品整体定义/E-31-企业发展/USM-E-31-企业发展.md` |
| P0 | `agent-delivery/user-story-library.yaml`（本模块故事） |
| P0 | `agent-delivery/story-impl-proposals.yaml` → `sip-ENT-MOD-OVERVIEW-ARCH-IMPL-L01` |
| P0 | `agent-delivery/产品实现规程.md` §2.4 / §8.1 |
| P0 | `agent-delivery/architecture-baseline.md`（D1–D8） |
| P1 | `agent-delivery/Design.md` + `UX-UE 通用交互组件规范.md`（FE/QA） |
| P1 | `agent-delivery/data-lineage-policy.md`（含指标则必读） |
| P1 | `agent-delivery/客户决策清单跟踪表.md`（相关 🟡） |
| P1 | `00-team-constitution` / 团队协作公约 |

---

## 7. 环境与仓

| 项 | 值 |
|----|-----|
| GKX_ROOT | 读 `gkx-orchestration/.env` |
| 业务仓 | `${GKX_ROOT}/repos/（本 leaf 以编排文档为主）` |
| lumen-* 分支 | 默认 push `origin/dev`；禁止 push main |
| demo-ui-* | 仅沙箱；禁止 merge 进 lumen |

---

## 8. 认领 /goal（merge + confirm 后粘贴）

```text
/goal ENT-MOD-OVERVIEW-ARCH-IMPL-L01
监管：human:徐滕强
执行：agent:architect-agent
仓：agent-delivery

先读本派单包：agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-MOD-OVERVIEW-ARCH-IMPL-L01-派单包.md
对照故事：US-E32-01,US-E32-02
上游：ENT-MOD-OVERVIEW-DG-G3（须 done 后才可按 ready 开工）

架构铁律：算法只在 Python；前端→Java→Python/internal；图谱 Nebula；D8 Design.md；D9 血缘；D10 交互规范。
完成须写 handoff + cost 四字段；禁止自行 done。
```

---

## 9. 建单门控（给人）

| 步骤 | 动作 |
|------|------|
| 1 | 审阅本派单包 + proposals 行 |
| 2 | 飞书改「建单已采纳」或 `node scripts/suggest-story-impl-tasks.mjs merge --ids sip-ENT-MOD-OVERVIEW-ARCH-IMPL-L01 --approved-by human:真名` |
| 3 | merge 时缺 `ENT-MOD-OVERVIEW-DG-G3` 会 auto-ensure（ready+待确认，监管淮政玮） |
| 4 | 门3 DG done → scan → confirm → ready → 本包可执行 |
