# FE-TS-05A · 湾区创新监测（M5）— 整页复刻与真实链路整改

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 整页复刻原由 frontend-agent 完成；2026-11-03 真实链路整改轮由本机会话执行（此前本任务 handoff 一直缺失，本轮补齐） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 四 Tab 全量对齐 demo 结构；本轮只换数据源、补空态、改口径，未跳过 D9 缺口标注 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 纯前端取数与文案整改，无存储流图变更 |
| 会签态 | N/A |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| Tab1 湾区创新成果综合展示 | ✅ | `OverviewTab.vue`：城市点位落点 + 城市/类型/领域/时间筛选联动 |
| Tab2 湾区创新能力 | ✅ | `CapacityTab.vue`：城市能力按久新真实计数；四维权重与综合得分无源 → 「—」 |
| Tab3 湾区创新能力分析 | ✅ | `SwotAnalysisTab.vue`：SWOT 四象限由后端下发，无数据整块空态，诊断报告有 guard |
| Tab4 湾区创新指标数据 | ✅ | `IndicatorsTab.vue`：指标清单 + 城市构成；同比/环比无源 → 「—」，预警判定三态 |
| 数据链路 | ✅ | `BayInnovationController` → `RemoteShowPythonClient` → `gkx_show_service` → 久新 Doris（只读） |
| 报告与导出 | ✅ | 页头「生成报告 / 打印另存 PDF / 导出数据」，纯前端产出 HTML + CSV |
| 构建 | ✅ | `pnpm type-check` + `pnpm build-only` 双绿（2026-11-03） |

## 2026-11-03 整改明细（P0 全清，18 项）

| # | 改动 | 文件 |
|---|------|------|
| 1 | 四维权重 30/25/25/20 → 全部「—」 | `components/CalcMethodModal.vue` |
| 2 | 综合得分公式 → 「暂时不能计算 + 原因」 | 同上 |
| 3 | 5 条外部统计来源 → 2 条久新真实表 | 同上 |
| 4 | 更新频率「按季度」→ 「按年度统计口径」 | 同上 |
| 5 | 指标权重恒空集（原来命中 mock 会返回 18/34/48） | `CalcMethodModal.vue`、`IndicatorSpecTrigger.vue` |
| 6 | 「可靠性」不再默认「官方发布口径」 | `IndicatorSpecTrigger.vue` |
| 7 | 同比/环比 NaN 直渲 → `fmtPctOrDash`（6 处） | `tabs/IndicatorsTab.vue` |
| 8 | 「是否预警」→ 三态（是/否/无法判定） | 同上 |
| 9 | 「未发现明显触发项」→ 无规则时「无法判定」 | 同上 |
| 10 | 阈值文案标明「前端本地试算，非服务端预警」 | `IndicatorsTab.vue`、`CapacityTab.vue` |
| 11 | 洞察「同比增速最高城市」改为有值才输出 | `models/bayAreaModel.ts` |
| 12 | 「近五期保持上行」→「较首期累计变化」 | 同上 |
| 13 | 「综合贡献 权重 NaN%」整条不出 | 同上 |
| 14 | 诊断报告加数据 guard + 空态 | `components/DiagnosisReportModal.vue` |
| 15 | 删 1500ms 假生成，无 SWOT 时按钮 disabled | `tabs/SwotAnalysisTab.vue` |
| 16 | 通知记录补空态 | `components/AlertCenterDrawer.vue` |
| 17 | 环形图环心无源「—」，不画 0% 弧 | `tabs/CapacityTab.vue` |
| 18 | 页级取数失败加错误态 + 重试 | `index.vue` |

## 偏离说明

- **四维指数**：demo 的「四维指数 + 2020–2025 趋势 + 城市雷达」不实现。依据 ADS_SCHEMA.md:2962
  「`ads_geo_yearly_index` 在公式批准前保持空表」，实测 0 行，权重与公式均无来源。
- **预警判定**：久新无预警规则表与预警事件表，页面只做本地阈值试算并在文案中标明，不宣称服务端预警。
- **不新增区块**：整改未新增任何区块，仅补空态与文案；报告导出按钮为新增功能。

## 验证

| 项 | 结果 |
|---|---|
| lint（M5 全目录） | 0 error / 0 warning |
| `pnpm type-check` | ✅ 全绿 |
| `pnpm build-only` | ✅ 绿（1m 27s） |
| `Math.random` | 0（2026-10-30 已移除，本轮复查无残留） |

## 遗留与后续

| 项 | 任务 |
|---|---|
| 影响力分展示位置、热点凑数、环形图单卡 undefined、表格/地图空态 | `FE-TS-05B` |
| 领域×国家、领域-国家地图、覆盖率披露 | `FE-TS-04B/04C/04D` |

## 关联文档

- 决策留痕：`agent-handoffs/科技发展态势-TS/M5-M6-REMEDIATION-20261103.md`
- 报告导出工具：`src/views/situation/shared/reportExport.ts`
- 库侧规约：`_local/dw-docs/久新数仓-资料同步与取数规约.md`
