# LUMEN-SVC-FE-ENTRY-VISUAL-C1 · 派单厚包

> 监管：`human:侯佳伟` · `coordinator_dispatch` · lock 24h  
> 仓：`lumen-ui-topic` · `origin/dev` · ponytail **full**

## 问题

ENTRY 交付把已评审 Demo 降成「轻量表单+表格」。不符合 `fe-replica-visual-dod.md` 与段 D 总派单「语义+布局」要求。

## DoD

1. 门户五 Tab：结构对齐 `demo-ui-topic` `service-portal/*`；Java 无分段数据时诚实空，但子导航/卡片骨架保留。
2. `/service-center/search`：复用本仓 `SearchHub` / `SearchScaffold` / `RecommendationSection` / `FilterPanel`（对照 `IndustrySearchPage` / 企业查询），**禁止**继续用裸 `a-table` 壳。
3. 保留：mode URL、画像抽屉、对比篮入口、D9 角标、只调 `/svc/topic/v1/**`。
4. handoff：`agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ENTRY-VISUAL-C1.md`，V1–V7 逐条。

## 对照真源

- Demo：`repos/demo-ui-topic/src/app/pages/service-portal/*`、`service-center/ServiceOrgSearchPage.tsx`
- 本仓兄弟：`src/views/industry-center/IndustrySearchPage.vue`、`src/components/search/*`
- 现错页：`src/views/service-center/ServiceOrgSearchPage.vue`、`src/views/service-portal/*`

## 审计锁定 P0（本叶硬验收）

> 真源 = `demo-ui-topic`（**不是** `demo-ui-science`）。

| 面 | 必过 |
|----|------|
| 查询 V2/V3/V6/V7 | SearchHub Hero；推荐/结果**卡**（禁裸 `a-table`）；未搜推荐区；禁叠 `industry-search-result-card` |
| 查询 UX | 三模式 + FilterPanel；最近检索；对比篮/分析集合；结构化画像（禁 JSON `<pre>`）；尽量 `?org=` |
| 门户 | Tab≈`global-workbench-tabs`；Overview 有数则图表；薄 Tab **禁** debug JSON 当产品 UI |

WORKSPACE 深度 / Job 白名单扩容 → `LUMEN-SVC-FE-WORKSPACE-VISUAL-C1` + C 段，本叶不做。
