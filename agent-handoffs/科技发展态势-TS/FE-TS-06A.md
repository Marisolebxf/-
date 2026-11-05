# FE-TS-06A · 深圳创新监测（M6）— 整页复刻

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 本机 Cursor 会话实装 M6 整页；完工推 integration 联调 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | demo→lumen 整页复刻；未跳过 D8/D9/D10、ts-sz-innovation-track 可观测、MetricSpecHint 接线 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 纯前端页面复刻，无存储流图变更 |
| 会签态 | N/A |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| Tab1 载体综合 | ✅ | `CarrierTab.vue`：筛选（级联/领域/创新价值 select）、TiandituMap 标记/热力/混合、飞线 SVG、排名/订阅/对比弹窗 |
| Tab2 指标系 | ✅ | `IndicatorTab.vue`：10 系树、四型图、对比/区间、详情弹窗 + MetricSpecHint |
| Tab3 领域分布 | ✅ | `DomainTab.vue`：8 领域图层、地图热力、对比图、报告抽屉 |
| Tab4 城市分析 | ✅ | `CompareTab.vue`：对标矩阵/趋势/瀑布/报告 PDF·Word |
| 数据 | ✅ | `fetchSzInnovationDataset` + `mock/modules/shenzhenInnovation.ts` 冻结种子；`USE_MOCK` 双轨 |
| 路由 | ✅ | `/trend/shenzhen-innovation-monitor`，`menu.ts` + `fullBleed` |
| 构建 | ✅ | 本地 `pnpm type-check`、`pnpm build` 绿（会话末） |

### 本迭代附加（态势共用）

- **`PageTabFrame`**（`src/components/workbench/`）：全球/湾区/深圳顶栏页签统一 Arco `a-tabs`，样式对齐 demo `global-workbench-tabs` 下划线。
- **`PageNoticeAlert`** + **`ExportTaskToast`**（`src/views/situation/components/`）：订阅/导出/口径等提示统一 Arco Alert（标题/图标/可关闭）；湾区指标导出与若干 inline 提示已同栈接入。
- **载体 Tab UX**：筛选栏 36px 对齐、级联单行 max-tag-count=3、地图工具栏 `width: max-content`、地图控件/图例样式对齐 demo。

## 偏离说明

- 创新价值筛选：产品要求由 tag 改为 Arco `a-select`（demo 为 tag 组）；其余交互对齐 demo。
- 页内提示：demo `ExportTaskToast` 绿底浮层 → Arco Alert 固定浮层（监管人 UX 统一要求）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 不调 demo 服务 | ✅ 仅读 demo 代码复写 |
| 前端→Java 网关（目标态） | ✅ API 层 `shenzhenInnovation.ts`；当前 Mock 开关 |
| D9 ⓘ | ✅ 指标 Tab / 对比等点位 MetricSpecHint（评审门控同仓惯例） |
| 可观测 | ✅ `ts-sz-innovation-track` CustomEvent + traceId |
| D8 Arco | ✅ |

## 测试结果

- `pnpm type-check`：通过
- `pnpm build`：通过（会话内）
- 浏览器：四 Tab 结构点测（载体筛选/地图 marker/页签切换）；**联调阶段建议监管人全量点测 DoD + 与 demo 截图比对**

## 遗留风险

- D3/D4 多数指标仍为 Mock（🧪）；后端 `/situation/*` 契约就绪后需切 `USE_MOCK=false` 联调。
- 深圳 CSS 体量大（demo 抽取 + lumen 追加），与湾区/global 共用的 `map-*` 类在 M6 页 scoped 覆盖，后续抽公共样式可减重复。
- `innovation-evaluation` 仓内另有未纳入本 handoff 的本地改动（若存在），未随本任务提交。

## CI/CD（必填）

- 分支：`dev`
- commit：`lumen-ui-science-pc` `b4e1eda`；`gkx-orchestration` `ab567532`（`origin/dev` 已 push）
- pipeline：push 后待 GitLab CI
- K8s dev URL：按仓 CI 部署（路由 `/trend/shenzhen-innovation-monitor`）

## 可观测性

- 事件名：`ts-sz-innovation-track`（`tab-change` 等）
- OTEL：沿用仓内 `observability.ts` / `createTraceId`

## 涉及文件（主路径）

- `src/views/situation/shenzhen-innovation/**`
- `src/api/situation/shenzhenInnovation.ts`
- `src/types/shenzhenInnovation.ts`
- `src/mock/modules/shenzhenInnovation.ts`、`src/mock/register.ts`
- `src/components/workbench/PageTabFrame.vue`、`page-tab-frame.css`、`PageNoticeAlert.vue`
- `src/views/situation/components/ExportTaskToast.vue`
- 连带：`global-innovation/index.vue`、`bay-innovation/*`（PageTabFrame / PageNoticeAlert）

## cost（待回填 registry）

| 字段 | 值 |
|------|-----|
| actual_tokens | （监管人回填） |
| model_used | Composer |
| actual_cost | （监管人回填） |
| cost_warn | false |

## 2026-11-03 整改轮（真实链路收口，P0 全清 14 项）

> 决策留痕：`agent-handoffs/科技发展态势-TS/M5-M6-REMEDIATION-20261103.md`

| # | 改动 | 文件 |
|---|------|------|
| 1 | 载体对比雷达**不再绘制**，出空态说明 | `tabs/CarrierTab.vue` |
| 2 | 对比摘要改为陈述真实计数，不用 mock 加权分排名次 | 同上 |
| 3 | 载体卡「创新价值」→ `fmtCarrierNum`（无源出「—」） | 同上 |
| 4 | 排名进度条无源时不画（原 `Math.max(8,…)` 会伪装出假条） | 同上 |
| 5 | 详情弹窗四项计数与描述统一格式化 | 同上 |
| 6 | 订阅 toast「订阅成功」→「已加入本次会话清单（未接订阅接口）」 | 同上 |
| 7 | 缺口瀑布删除 `0.43/0.34/0.23` 假归因与「产业创新优势 20%」 | `tabs/CompareTab.vue` |
| 8 | 报告删除「历史趋势与未来预测」章节与写死 `2021-2025` | 同上 |
| 9 | 「全局判断基于全量样本池形成」→「综合得分取自后端城市对标表」 | 同上 |
| 10 | 删死码 `showForecastNotice` 提示块 | 同上 |
| 11 | 领域「优势/潜力/薄弱」标注为「按当前排序指标分段，非综合评价」 | `tabs/DomainTab.vue` |
| 12 | 指标页「生成并导出」改为真实 CSV 导出（原只开弹窗） | `tabs/IndicatorTab.vue` |
| 13 | 「五年累计变化 / 2021-2025」→「按实际数据期次」 | 同上 |
| 14 | 页级取数失败补错误态 + 重试 | `index.vue` |

新增：页头「生成报告 / 打印另存 PDF / 导出数据」三个按钮，纯前端产出（久新无 M6 报告端点），
报告章节为 载体 / 指标 / 领域 / 城市对标，不含任何评分、名次或预测结论。

验证：`pnpm type-check` 与 `pnpm build-only` 双绿；M6 全目录 lint 0 error / 0 warning。

遗留 P1（空历史年份渲染、单指标空态、搜索无结果提示、领域表格空态）→ `FE-TS-06B`。
