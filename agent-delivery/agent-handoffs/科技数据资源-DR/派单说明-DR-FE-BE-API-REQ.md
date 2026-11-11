# 派单说明 · 科技数据资源 · 前端视角后台接口需求（两叶）

> 建单日：2026-11-11  
> 监管人：**human:淮政玮**（两叶统一，用户裁定）  
> Epic：`E-FE-DATA-RESOURCES`  
> 父上下文：WBS-05-04 / `SYSINT-05-04-L01`；契约真源 `BE-DR-CONTRACT-01`（done）；Java C1～C4 integration  
> 过程夹索引：可挂 `工程过程/04-系统集成/05-展示系统集成/`（本文件真源在 DR handoff 夹）

---

## 总览

| 顺序 | task-id | 执行 | 状态（建单时） | 一句话 |
|---|---|---|---|---|
| 1 | `FE-DR-BE-API-REQ-L01` | frontend-agent | ready | 依现有前端整理**后台接口需求草稿**（四 GET） |
| 2 | `BE-DR-FE-API-ALIGN-L01` | api-agent | backlog | 对照草稿 ↔ 契约/C1～C4 **出差异表** |

依赖：2 依赖 1 审定（草稿可用）+ `BE-DR-CONTRACT-01` + `DR-RES-C4-L01`。  
分工铁律：**只谈前端消费的后台 HTTP**；不写供方 EXT-B3、不写 gapfill DDL/灌数、不改业务仓代码（除非对齐叶经人批准改契约——默认不改）。

认领：`task-claim` 时 `supervised_by=human:淮政玮`。锁未过期不要重复 claim。  
查询任务只用 MCP；**禁止**读 `task-registry.yaml`。  
MCP 写 registry 后立刻 commit + push `origin/dev`。文档类若主区脏 → worktree。

---

## 叶 1 · FE-DR-BE-API-REQ-L01

```text
/goal frontend-agent
身份：你是展示系统前端工程师。本单是定义任务：只整理「前端要后台提供什么 HTTP」，不写实现代码。
强度：ponytail off（definition）。
任务：FE-DR-BE-API-REQ-L01
标题：科技数据资源：依据现有前端整理后台接口需求草稿（四 GET Dataset）
监管人：human:淮政玮
执行：agent:frontend-agent
状态：ready。认领后 in_progress。勿把本单标 done（definition 走会签/ready_to_sign，操作 done 仅 human:淮政玮）。
仓：gkx-orchestration（只改 agent-delivery 文档）。不改 lumen-ui-science-pc / lumen-svc-platform 代码。
协作：api-agent 只读对照，不在本叶改契约。

目标：在现有草稿上审定/补齐「前端视角后台接口需求」，使 api-agent 可据此做差异核对。
已有草稿（须精读后修订或确认可签）：
- agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md

必读（前端实现真源）：
- lumen-ui-science-pc/src/types/dataResources.ts
- lumen-ui-science-pc/src/api/dataResources.ts（事实：real() 仍回种子、未接网关）
- lumen-ui-science-pc/src/mock/modules/dataResources.ts + dataResourcesSeed.ts
- lumen-ui-science-pc/src/views/data-resources/{overview,access,theme,application}/
对照（勿扩写成供方清单）：
- agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-CONTRACT-01.md
- agent-delivery/工程过程/04-系统集成/05-展示系统集成/方案-科技数据资源-后台接口.md §5

范围（必须写清）：
1. 仅四个无参 GET：/display/v1/data-ops/{overview|access|theme|application}/dataset
2. PigX 信封 code=0 → data；空库仍 0，数组 []、键保留
3. 按四 Dataset 列出前端必有根键 + 页面用途；嵌套以 types/种子为准
4. 写明「前端明确不要求」：筛导出 API、WS 监控、主题卡涨跌字段、Nebula、R-01～R-24 直出
5. 待对齐项交给叶 2（种子多键如 totalCalls、接线状态等）

不做：
- 不改 api/views 接线（属 DR-RES-D1 或后续叶）
- 不写 EXT-B3 / 总集供方 / gapfill 表
- 不替代 BE-DR-CONTRACT-01 冻结正文
- 不自行 task-create 开发叶

DoD：
1. 草稿路径仍为 FE-DR-BE-API-REQ-DRAFT.md（或同夹修订版）；监管人可审
2. 覆盖四视窗四 GET；写明当前未接网关事实
3. 列出待对齐项（给 BE-DR-FE-API-ALIGN-L01）
4. handoff：agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-L01.md；evidence 指草稿+handoff；ponytail: off
5. 状态：evidence 齐后可走 AV → integration/ready_to_sign（definition）；禁止自行 done

认领示例：
task-claim id=FE-DR-BE-API-REQ-L01 claimed_by=agent:frontend-agent supervised_by=human:淮政玮
```

---

## 叶 2 · BE-DR-FE-API-ALIGN-L01

```text
/goal api-agent
身份：你是 Java / 展示 BFF 侧接口工程师。本单只做对照差异，默认不改契约、不改前端、不扩路径。
强度：ponytail off（definition）。
任务：BE-DR-FE-API-ALIGN-L01
标题：科技数据资源：对照 FE 接口需求草稿与契约/C1-C4 出差异表
监管人：human:淮政玮
执行：agent:api-agent
状态：backlog。须 FE-DR-BE-API-REQ-L01 草稿经监管人可用后再认领；依赖 BE-DR-CONTRACT-01、DR-RES-C4-L01。
仓：gkx-orchestration（差异表/handoff）。可读 lumen-svc-platform 已合入的 data-ops 实现，但本叶不强制改码。
协作：frontend-agent。

目标：逐键对照 FE 草稿与 BE-DR-CONTRACT-01 / C1～C4，输出差异表并给处置建议（保持/禁止出站/需人批准变更）。

必读：
- agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md
- agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-CONTRACT-01.md
- agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-C1-L01.md ～ C4（及实现说明）
- lumen-ui-science-pc/src/types/dataResources.ts（键名冲突时类型优先）

范围：
1. 差异表列：路径、根键/嵌套路径、FE 要求、契约、C 实现、判定（一致/多种子键/缺键/多余键）、建议
2. 明确：不扩四个 GET 以外路径
3. 种子多出但类型无的键（如 resourceUsageStats.totalCalls）：是否禁止 HTTP 出站 → 写进结论
4. origin / entityStock / columnCatalog：与契约多出规则是否一致

不做：
- 未经 human:淮政玮 批准不改契约正文、不改前端 types
- 不写供方/DDL
- 不把本叶标 done（仅人签收）

DoD：
1. 差异表落盘 agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-FE-API-ALIGN-L01.md（或同夹差异专表）
2. 结论含「禁止出站键」清单与「需人批准才变更」项
3. evidence + handoff；ponytail: off
4. 状态可至 ready_to_sign；done 仅 human:淮政玮

认领示例：
task-claim id=BE-DR-FE-API-ALIGN-L01 claimed_by=agent:api-agent supervised_by=human:淮政玮
```

---

## 监管人检查清单（human:淮政玮）

- [ ] FE 草稿是否只含四 GET、无供方扩范围  
- [ ] 是否写明前端未接网关事实（避免误以为 D1 已合入）  
- [ ] 对齐叶差异表是否把「类型无、种子有」标成禁止出站  
- [ ] 两叶均未擅自改契约 / 未伪称联调通过  

---

## 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版：两叶合册；监管人统一 human:淮政玮；含可复制 /goal 正文 |
