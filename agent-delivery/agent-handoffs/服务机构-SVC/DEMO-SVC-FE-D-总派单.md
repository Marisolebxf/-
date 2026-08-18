# 段 D · SVC 前端（lumen-ui-topic）总派单

> **监管**：`human:侯佳伟` · 总控已授权  
> **仓**：`lumen-ui-topic` · `origin/dev` · **强度**：ponytail **full**  
> **总控**：[DEMO-SVC-ABCD-长任务总控.md](./DEMO-SVC-ABCD-长任务总控.md)  
> **复刻验收**：[`templates/fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)（手册 §9.0c · 规约 §5.1 / **§9.1**）  
> **2026-08-18 loop**：施工真源 [`DEMO-SVC-CD-细叶拆单.md`](./DEMO-SVC-CD-细叶拆单.md)。ENTRY/WORKSPACE/视觉 C1/C2 **不进下一张队列**。金路径用总控 §4 真实 `US-SVC-*`。旧 E1 不算本轮完成。

## 铁律

- 复刻已评审 `demo-ui-topic` `service-portal` / `service-center`：**布局 + 交互 + 样式 + 评审 + Mock 开关**。  
- **只调 Java**；D12 禁止打 `demo-*`。  
- Vue 3 `<script setup>` + TS；禁止贴 JSX / React props。  
- 评审只走 `@/review`；关评审零泄漏。D9 角标/ⓘ 按 readiness；Q-SVC-010 待核验诚实展示。  
- Mock 只走 `USE_MOCK` + `src/mock/register.ts`。**`USE_MOCK=false` 时禁止硬 mock，禁止 `@/mock/**` 或 Demo fixture 填数。**  
- 地图复用 `UnifiedLeafletMap` / 已有天地图封装；禁止页面再 `new L.map`。  
- 已有 `src/api/svc` 则**不要**再开「API 封装」单。组件抽离发生在第一张用到它的叶。  
- 同仓一次一张 frontend 单。下一叶走联调闸门，**不**等人审截图。  
- 占位路由不算复刻完成。

## 旧叶（废作铺齐，不算复刻完成）

施工真源（2026-08-18）：**一故事一叶**，见 [`DEMO-SVC-CD-细叶拆单.md`](./DEMO-SVC-CD-细叶拆单.md)。下表厚包仅骨架，**不要按此口径开工**。

| ID | 说明 |
|----|------|
| `LUMEN-SVC-FE-ENTRY-L01` | 原「入口壳 + 门户/查询接线」。DoD 过薄，仅骨架 fan-in。 |
| `LUMEN-SVC-FE-WORKSPACE-L01` | 原「分析/生态/招引一张」。仅骨架 fan-in。 |

## 后续建单（建议 · 粒度自选 · registry 另做）

下表是**可选切法**，不是强制一页一叶。也可按能力横切（查询+篮分发、过程壳、地图）或门户+查询一叶，只要 `/goal` 有区块清单。

| 可选范围 | Demo 真源 | 说明 |
|----------|-----------|------|
| 门户 | `service-portal/*` 五 Tab | 可一叶，DoD 必须按五 Tab **区块清单 + 五维**，不能写「入口壳」 |
| 机构查询 + 篮 | `ServiceOrgSearchPage.tsx` | 可与门户合并，或单独 |
| 机构分析三键 | `workspace=field/trend/capability` | 可一叶三键或按键拆；过程壳抽出后复用 |
| 生态 | `ServiceChainEcosystemPage.tsx` | |
| 招引 | `ServiceRecommendPage.tsx` | |
| 维护 | `ServiceMaintenancePage.tsx` | 只复刻壳，写侧不接 |

## `/goal` 头

```
任务：{ID}
仓：lumen-ui-topic · origin/dev
监管：human:侯佳伟 · coordinator_dispatch · lock 24h
强度：ponytail full
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：{本叶路由/键/能力/多页，列出区块}。占位与只改 Hero 不算完成。
禁止：贴 JSX；USE_MOCK=false 时硬 mock 或 Demo fixture 填数；自造 ⓘ；再 new 地图。
必读：总控 · 本总派单 · E7 五件套 · demo-ui-topic service-* · 本仓 AGENTS.md
```
