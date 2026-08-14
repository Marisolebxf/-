# LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01 · 派单厚包

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（长任务总控已授权）  
> **执行**：`frontend-agent`  
> **仓**：`${GKX_ROOT}/repos/lumen-ui-topic` · `origin/dev`  
> **强度**：ponytail **full**  
> **复刻验收**：[`templates/fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)

人审：`/industry-center/search`「推荐产业」卡内文字竖排、操作钮漂在空白。Hero/页底已由 SEARCH-SKIN 修好。

---

## 根因（已定位）

`IndustrySearchPage.vue` 推荐 `article`：

```text
class="industry-search-recommendation-card industry-search-result-card"
```

| class | display | 设计给谁 |
|---|---|---|
| `industry-search-recommendation-card` | flex 横排 | 推荐卡：主文 + 操作 |
| `industry-search-result-card` | `grid-template-columns: 24px minmax(0,1fr) auto` | 检索结果：勾选列 + 主文 + 操作 |

后者写在 CSS 后，**grid 覆盖 flex**。推荐卡只有 2 个子节点 → 主文进 **24px 第一列** → 一字一换行；操作进第二列，漂在大片空白。

Demo 真源（不要再猜）：

```text
className="search-content-card industry-search-recommendation-card"
```

**没有** `industry-search-result-card`。

---

## 必做（最短）

1. 推荐 `article` **去掉** `industry-search-result-card`。需要边框/圆角则用 Demo 的 `search-content-card`，或只在 `.industry-search-recommendation-card` 补边框 token（不要复制结果卡网格）。  
2. 保证宽屏 `display:flex; flex-direction:row`；`recommendation-main` `flex:1; min-width:0`；摘要正常横向换行（`white-space: normal`），标题可 ellipsis 但列宽不能是 24px。  
3. 自检：`industrySearchModel.selfcheck.mjs`（或等价）断言推荐模板字符串 **不含** `industry-search-result-card`。  
4. 对照 `fe-replica-visual-dod.md` V1–V7 写进 handoff。

禁止：重写 SearchScaffold；改 Java/Python；为修布局再叠第三套 class。

---

## `/goal`

```text
/goal
你是 frontend-agent。task-id：LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01
仓：${GKX_ROOT}/repos/lumen-ui-topic · origin/dev
监管：human:淮政玮
强度：ponytail full
复刻：语义+布局。必读 templates/fe-replica-visual-dod.md。
禁止：推荐 article 再挂 industry-search-result-card；问用户。
根因：flex 推荐卡被 grid 24px 结果卡覆盖。Demo 只用 search-content-card + industry-search-recommendation-card。
修完 push origin/dev；handoff LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01.md（含 V1–V7）。
```
