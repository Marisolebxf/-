# 前端复刻 · 视觉/布局验收（派单必贴）

> **读者**：coordinator 写 `/goal`、frontend-agent 收单。  
> **触发**：任何「对照已评审 Demo / 本仓兄弟页」的 lumen 前端单（含 demo→lumen、专题直落对照 `demo-ui-topic`）。  
> **挂钩**：手册 **§9.0c** · `.cursor/rules/frontend.mdc` 铁律 11 · 长任务 D 段。

## 一句话

**复刻 = 语义 + 路由 + 状态机 + 页面结构 + 卡片内部布局。**  
只对齐路由/三模式/Hero 色，**不算**复刻完成。禁止用「禁止抄 React」当借口另起一套灰白/挤爆的 DOM。

## `/goal` 必贴（frontend 复刻单，缺则拒派）

```text
复刻：语义+布局。必读 templates/fe-replica-visual-dod.md。
禁止：两套互斥 display 叠同一节点（flex 卡 + grid 结果卡）；正文被挤成竖排字；只改页底/Hero 宣称视觉完成。
对照：本仓已有兄弟页（如企业查询 RecommendationSection）+ Demo 真源 class 清单，不要猜。
```

## 验收清单（handoff 逐条 ✅/❌）

| # | 项 | 不过的典型样子 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | 灰白整页 |
| V2 | 检索 Hub Hero 与本仓企业查询同皮肤 | 白卡片搜框、无底图/橙钮 |
| V3 | **卡片/列表内部**：标题+摘要横向书写；操作在右侧或下行，不断开漂 | 一字一换行（容器被挤到 ~24px） |
| V4 | **一个节点一套 layout**：Demo 用 `recommendation-card` 就不要再叠 `result-card`（后者 `grid-template-columns: 24px 1fr auto` 是给「勾选列」的） | 推荐卡变成三列网格，主文进 24px 列 |
| V5 | `min-width: 0` 只加在 **flex/grid 子项需要截断** 时，不要让唯一内容列宽度塌成 0 | 标题 `ellipsis` 只剩 1～2 字 |
| V6 | 推荐/结果空态：无数诚实空；有数则卡结构与 Demo/`RecommendationSection` 同行（`xl:flex-row`） | 有数据却 `a-empty`，或有卡但结构错 |
| V7 | 自检：推荐 `article` class **不得**同时含 `industry-search-result-card`（除非子节点数=网格列数，且第一列真是 checkbox） | 本清单 V3 复现 |

## 施工顺序（防 ponytail 偷工）

1. 打开 Demo 真源页，**抄 class 清单**（不要凭记忆叠「看起来像结果卡」的 class）。  
2. 打开本仓兄弟页（企业查询）对照 Hero / 推荐行。  
3. 改完用宽屏（>1490px）看推荐卡：必须是 **一行：左文右钮**。  
4. handoff 写 V1–V7，缺条 `needs-revision`。
