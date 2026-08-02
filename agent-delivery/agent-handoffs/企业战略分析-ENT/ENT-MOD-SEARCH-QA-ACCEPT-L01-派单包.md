# 派单包：ENT-MOD-SEARCH-QA-ACCEPT-L01

- **派单方**：coordinator（auto-dispatch 补登 · 2026-08-03）  
  > 门 3 confirm（`approved_by=human:郭万迎` · `trigger=impl-gate3-unlock`）时本应落盘；磁盘缺失，由 qa-agent 按 `dispatch-rules` / `coordinator-dispatch.mjs#generateDispatchPackage` 规范补写。
- **时间**：2026-08-03
- **执行 Agent**：`agent:qa-agent`
- **监管人**：`human:黄敬洲`（更正：原误填 `human:郭万迎`，来自 `dispatch-rules#agent_supervisors` 错误默认；2026-08-03 已改规则为黄敬洲）
- **仓 / 产物落点**：`agent-delivery`（报告与用例）；被测系统 `lumen-ui-topic`（GitLab #231，**不是** `lumen-ui-science-topic`）
- **Sprint**：2026-W32（Theme 试点 SEARCH）
- **上游**：`ENT-MOD-SEARCH-DG-G3` ✅ done（批准附条件）
- **性质**：实现期验收（`delivery_phase: implementation` · `task_type: feature` · 难度 S / 2 点）
- **故事挂载（草案）**：US-E1-SCH-01～08（Theme 验收以 §1 必测为准；06/07 暂缓）

---

## 1. 目标

按 Theme 试点演示脚本，对 **企业查询（SEARCH）** 做 Sprint 验收场景回归，结论可支撑：

1. **S-T1 筛选可用**、**S-T2 初始引导** 是否达到 Theme Done 口径  
2. 人工勾选证据 + qa-agent handoff，供 Review / 门 I 后续签收引用  

**演示脚本真源**：`agent-delivery/sprints/ent-scrum-theme-pilot-SEARCH-KEYENT.md` §2  

**环境**：`http://192.168.88.50:30892`（`repo-registry` · lumen-ui-topic / NodePort 30892）

---

## 2. 人机分工（本任务强制）

| 角色 | 做什么 | 不做什么 |
|------|--------|----------|
| **人工（监管人黄敬洲或指定测试人）** | 在本机浏览器打开环境，按用例逐步点界面、截图、勾选 Pass/Fail/Blocked | 不改业务代码；不替甲方拍板口径 |
| **`qa-agent`** | 维护用例、汇总回传、写正式 handoff、回填 cost、经 MCP 更新任务状态 | **默认不代点** IDE Browser / CDP 登录与操作页（监管明确授权除外） |

用例文件（已交付）：

`agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-人工测试用例.md`

---

## 3. 验收范围

### 3.1 必测（Sprint Goal）

| Theme | 故事 | 用例 |
|-------|------|------|
| **S-T2 初始引导** | US-E1-SCH-03、US-E1-SCH-08 | TC-ST2-01～05 |
| **S-T1 筛选可用** | US-E1-SCH-04（+SCH-05 再筛） | TC-ST1-01～05 |

### 3.2 Stretch（有余力）

| Theme | 故事 | 用例 |
|-------|------|------|
| **S-T3 结果确认硬化** | US-E1-SCH-01、US-E1-SCH-05 | TC-ST3-01～02 |

### 3.3 暂缓（不进本 Goal · 勿判 Fail）

- US-E1-SCH-06 对比篮跨模块接力  
- US-E1-SCH-07 导出完整链路  

裁剪口径：Q033（不做 NL LLM）、Q034（仅横向长卡片）、Q036（高筛不做复杂 AND/OR 嵌套）。

---

## 4. Definition of Done

1. 人工测试用例已交付，且 **S-T1 + S-T2** 已由人工勾选回传（或明确 Blocked + 原因）  
2. 正式 handoff：`agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01.md`  
   - 含范围对照、逐 Theme 结论、截图/证据索引、开放项、架构合规自检、cost 四字段  
3. Theme 进度建议：在 `ent-scrum-theme-pilot-SEARCH-KEYENT.md` §0 进度板标注 S-T1/S-T2 ✅/❌（可附 Review 证据路径；**不**由 qa-agent 擅自改 Theme Done 机器字段）  
4. 关单一句：**所属 Theme 演示路径通/不通 + 依据**  
5. 经 MCP 推进状态（人工回传后 → `review` / 按状态机；**勿自行 `done`**）  

---

## 5. 必读

| 优先级 | 路径 |
|--------|------|
| P0 | `sprints/ent-scrum-theme-pilot-SEARCH-KEYENT.md` §0～§2 |
| P0 | `agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-人工测试用例.md` |
| P0 | `agent-handoffs/产品整体定义/E1-企业查询/USM-E1-ENT-SEARCH-企业查询.md`（验收口径） |
| P0 | `agent-handoffs/产品整体定义/DG-ENT-SEARCH-拍板纪要.md`（附条件未闭合项勿当 Fail） |
| P1 | `产品实现规程.md`、`acceptance-review-workflow.md` |
| P1 | `客户决策清单跟踪表.md` Q033～Q037 |

---

## 6. 不做

- 改 `lumen-ui-topic` / Java / Python 业务代码（缺陷开单回派对应 agent）  
- 用错误仓 `lumen-ui-science-topic` 当验收对象  
- 把 SCH-06/07 或 DG 附条件未闭合项写成「实现缺陷 Fail」而无说明  
- 替甲方闭合业务口径 🟡 项  

---

## 7. 认领话术

```text
/goal qa-agent
任务 ID：ENT-MOD-SEARCH-QA-ACCEPT-L01
监管：human:黄敬洲
认领：先按 gkx-task-claim-supervision 写入 claimed → in_progress
派单包：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-派单包.md
被测：lumen-ui-topic · http://192.168.88.50:30892
真源：sprints/ent-scrum-theme-pilot-SEARCH-KEYENT.md §2
分工：界面操作人工执行；qa-agent 出用例/汇总结论/写 handoff
必测：S-T1、S-T2；stretch：S-T3；暂缓：SCH-06/07
用例：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-人工测试用例.md
产物 handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01.md
禁止：默认 IDE Browser 代点联调页（除非监管授权）
架构铁律：前端→Java→Python；不直连 nGQL；decision 不外包给 AI
```

---

## 8. 回传与关闭路径

1. 人工按用例勾选 → 用用例文末「回传模板」贴回会话或飞书  
2. `qa-agent` 汇编正式 handoff + cost  
3. MCP：`evidence` 指向 handoff；状态进入 `review`（或按 feature 状态机推进）  
4. coordinator / 淮政玮签收 → `done`  

---

**关联**：`pending-dispatch.yaml` · `impl-gate3-unlock-ENT-MOD-SEARCH-DG-G3-ENT-MOD-SEARCH-QA-ACCEPT-L01`  
**维护**：补登后以本文件为派单真源；用例变更同步改 §3 / 人工测试用例文件。
