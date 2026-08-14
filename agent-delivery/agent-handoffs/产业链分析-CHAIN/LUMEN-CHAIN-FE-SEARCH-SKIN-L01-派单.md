# LUMEN-CHAIN-FE-SEARCH-SKIN-L01 · 派单厚包

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（长任务总控已授权，不必再问）  
> **执行**：`frontend-agent`（全栈子代理可诊推荐空态接线；**默认不改 Java/Python**）  
> **仓**：`${GKX_ROOT}/repos/lumen-ui-topic` · push **`origin/dev`**  
> **强度**：ponytail **full**  
> **总控**：[`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md)  
> **D 总派单**：[`DEMO-CHAIN-FE-D-总派单.md`](./DEMO-CHAIN-FE-D-总派单.md)

人审截图：专题「产业查询」灰白裸页 + 白卡片搜框 +「暂无推荐产业」。对照本仓企业查询（蓝 Hero + `#D8E7FC` 页底）未复刻。

---

## 0. 根因（已定位，按此修）

1. `IndustrySearchPage.vue` 页根只有 `industry-search-page`，**没有** `enterprise-search-page`，也没有 `background: var(--sci-bg-page)`。  
2. Hero 写死在 `src/assets/search-workspace.css`：`.enterprise-search-page .search-hub-card` / `.enterprise-search-page .enterprise-search-hero`。产业查询吃不到底图、蓝渐变、白胶囊 Tab、橙色搜索钮。  
3. Demo 用 `ElementSearchWorkbench` + `SearchContentSurface` 挂同一套 Hero；Lumen 对应物是 **页根 class + SearchHub**（企业查询另包 `SearchScaffold`）。产业查询只丢了 SearchHub，没套页壳。  
4. 推荐列表用 `INDUSTRY_SEARCH_RECOMMENDATIONS` 的 fixture `recordId` 去对 catalog；ID 对不上 → `a-empty`「暂无推荐产业」。catalog 有数时应能出卡。

`SearchScaffold` 绑企业 `ElementRecord` 检索状态机。**禁止**为套 Scaffold 重写产业查询。最短路径：页根皮肤 + Hero 选择器覆盖 + 推荐接线。

---

## 1. 必做

| # | 改什么 | 怎么做（最短） |
|---|---|---|
| 1 | 产业查询页根 | 同时带 `enterprise-search-page` **和** `industry-search-page`；`min-height:100%`；`background: var(--sci-bg-page)`。对照 `EnterpriseSearch.vue`。 |
| 2 | Hero CSS | 选择器扩到产业页（例如 `, .industry-search-page .search-hub-card`），或只靠页根双 class。禁止复制第二套 Hero 色值。 |
| 3 | 推荐区 | catalog 非空：用 catalog 记录出推荐卡（fixture 对得上优先，对不上则取目录前 N 条）。无数：诚实空，文案保留。优先复用 `RecommendationSection`；套不上就保留现卡，但放进半透明内容壳（`search-translucent-container` / 与企业推荐区同 token）。 |
| 4 | 总览 + 诊断/区域/深圳/全景页根 | 补 `background: var(--sci-bg-page)`。不重做 G6/工作区。 |
| 5 | 自检 | 产业查询 Hub 计算样式含 `enterprise-search-bg.png` 或等价蓝渐变；页底 `#d8e7fc`。可加最小 self-check，勿上新测试框架。 |

---

## 2. 禁止

- 直连 Python / ES / MySQL / Nebula。  
- 新 npm 依赖。  
- 抄 Demo React 进 Vue。  
- 另起灰白皮肤、第二套 Hero。  
- 为套 `SearchScaffold` 重写三模式/入篮。  
- 无闸门写正式库。  
- 改 Java/Python（推荐空且 catalog API 真 0 行 → handoff 记诚实空，**不要**假装有推荐）。  
- force push。

---

## 3. DoD

- `/industry-center/search` 视觉对齐本仓 `/enterprise/search` 的 Hub Hero + 页底。  
- 推荐：有 catalog 则有卡；无则诚实空。  
- 产业链其它已落地页页根为 `#D8E7FC`。  
- 只调已有 Java；CI lint/type/build 绿（或登记本地命令输出）。  
- push `origin/dev`；commit 含 `[agent:frontend-agent]`。  
- handoff `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-SEARCH-SKIN-L01.md`：ponytail full、cost 四字段、commit SHA、是否需要 E0 再 rollout。

---

## 4. `/goal`

```text
/goal
你是经验丰富的前端工程师（frontend-agent），本单全栈诊接线但默认只改 lumen-ui-topic。
仓库：${GKX_ROOT}/repos/lumen-ui-topic · origin/dev
监管：human:淮政玮
task-id：LUMEN-CHAIN-FE-SEARCH-SKIN-L01
强度：ponytail full。禁止用 YAGNI 跳过 D8 Design 皮肤。
必读：本厚包 · DEMO-CHAIN-FE-D-总派单.md · Design.md §4/§14 · EnterpriseSearch.vue · search-workspace.css · IndustrySearchPage.vue
禁止：直连 Python；另起灰白 UI；重写 SearchScaffold；改 Java/Python；问用户。
先 MCP task-claim（若尚未认领）再改代码。修完 push origin/dev，写 handoff，状态转到 in_progress 完成后由 coordinator 收（你把 evidence 填上即可）。
```

认领：`claimed_by=agent:frontend-agent` · `supervised_by=human:淮政玮` · `claim_type=coordinator_dispatch` · `lock_hours=24`
