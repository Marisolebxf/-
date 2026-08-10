# Handoff：TOPIC-SVCCHAIN-ALIGN-L01

- **时间**：2026-08-10
- **执行**：agent:ui-agent
- **监管**：human:郭万迎
- **认领类型**：coordinator_dispatch
- **仓库**：`${GKX_ROOT}/repos/demo-ui-topic`（分支 `dev`）
- **状态建议**：review（待 coordinator 验收）
- **demo-ui-topic commit**：`afd6583`（pushed `origin/dev`）
- **orchestration commit**：`a761bf2`（registry + handoff）

## Summary

完成产业服务链分析模块三菜单定点更新：

1. 技术力评估页签标题「评价模型配置」→「技术力评价模型」
2. 链路短板全周期图：步骤卡箭头流 → 地铁轨道图，每站清晰展示依赖服务类型（Bid 7.4.1）
3. 招引/培育：去掉自定义权重 UI 与权重合计校验，改用内置固定权重生成名单；保留演示标注与生成/导出

## Touched files（白名单核对）

| 文件 | 是否在 registry 白名单 | 变更摘要 |
|------|------------------------|----------|
| `src/app/pages/service-center/CapabilityView.tsx` | ✅ | 标题更名 |
| `src/app/pages/service-center/ChainLinkView.tsx` | ✅ | 地铁轨道图 |
| `src/app/pages/service-center/serviceCenter.css` | ✅ | `.svc-eco-metro*` + `.svc-fixed-weights`；移除旧 `.svc-eco-chain*` |
| `src/app/pages/service-center/ServiceRecommendPage.tsx` | ✅ | 去 WeightEditor；固定权重展示 |
| `src/app/pages/service-center/serviceRecommendStore.ts` | ✅ | STORE_VERSION=2；移除 weight actions；hydrate 强制默认权重 |
| `docs/符合度评估-产业服务链-三页定点.md` | DoD 文档 | 7.3/7.4/7.6/7.7 + 3 条产品变更对照 |
| `docs/screenshots-TOPIC-SVCCHAIN-ALIGN-L01/*` | DoD 截图 | 三页主路径截图 |

**未触碰（硬边界）**：enterprise/*、research*、industry-center/*、service-portal/*、ServiceOrgSearch*、ServiceMaintenance*、Layout、StageDetailDrawer（下钻服务类型已足够，无需改）、serviceEcosystemModel/Data（映射已满足 7.4.1）、serviceRecommendModel/Data（DEFAULT_* 权重沿用）。

## 验证

- Build：`pnpm run build` ✅
- 截图：`docs/screenshots-TOPIC-SVCCHAIN-ALIGN-L01/`
  - `01-org-capability.png`（含「技术力评价模型」）
  - `02-chain-metro.png`（地铁轨道图 + 依赖服务类型）
  - `03-recommend-attract.png` / `03b-recommend-cultivate.png`（固定权重、无自定义权重编辑）
- 符合度文档：`docs/符合度评估-产业服务链-三页定点.md`

## Design.md §14 自检（摘要）

- 浅蓝白工作台 / Arco / 主色 `#165DFF`：✅ 沿用既有 service-center
- 未引入深色大屏/营销 hero/emoji 状态：✅
- D9：`SvcMetricBadges` / `ServiceReviewMount` 保留：✅
- 右侧分析面板：本三页为工作台式卡片流（既有骨架），未改 Layout：N/A（策略 A 禁止扩面）

## 偏离

1. 招引/培育自定义权重 → 内置固定权重：产品定点要求，相对 R2 可调 UI 有意收敛；相对招标「内置模型」对齐。
2. StageDetailDrawer / ecosystem data 未改：既有服务类型映射已满足展示与下钻。

## 开放项

- Q-SVCCHAIN-03/05 正式模型与专家规则库仍待算法/后端口径
- localStorage key `topic-svc-recommend` 升至 v2，旧自定义权重失效并回默认（预期行为）

## 下一步

coordinator 验收 → registry `review`→`done`；如需 lumen 复刻另开 frontend leaf。