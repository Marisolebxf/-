# DONE · 5-region（DISPLAY-POLICY-GAP-AC-L01）

- 仓：`repos/demo-ui-science`
- 簇：`analysis/` 分组对比 + 趋势 / 关联 / 导出闸门
- ponytail：full
- **未 git commit / push**；未改 `policyData.js`、`PolicyAnalysis.jsx`、`fp-split-run/`

## 已改文件

| 文件 | 作用 |
|---|---|
| `src/pages/policy-tracking/analysis/DimensionBar.jsx` | 维度条增加「资源投向」Select；导出 `RESOURCE_TARGET_OPTIONS`；`DEFAULT_DIMENSIONS.resourceTarget` |
| `src/pages/policy-tracking/analysis/RegionGroupCompare.jsx` | 卡片内资源投向筛选并过滤柱状/热力；效果数据 Switch → Empty |
| `src/pages/policy-tracking/analysis/TrendMetricsChart.jsx` | 无核心数据 / 未选指标 → Empty，不再回落到前 3 项硬出图 |
| `src/pages/policy-tracking/analysis/StructureLinkPanel.jsx` | 未整合要素不可出关联图；未展示传导路径不可追踪高亮 |
| `src/pages/policy-tracking/analysis/ReportTemplateExport.jsx` | 未自定义模板不可批量；汇报周期/分析维度/图表类型必选 |
| `src/pages/policy-tracking/analysis/analysisGateHints.jsx` | 可复用 `GateEmpty`（本簇已就地引用） |

## 档 A

| # | 功能点 | 怎么验收 |
|---|---|---|
| #10 | 筛选资源投向 | **政策跟踪 → 政策分析评价 → Tab「分析报告可视化」** → 「分组对比」卡片 extra「资源投向」Select。默认「全部投向」出全量柱/热力；改「资金支持 / 人才引进 / 平台载体 / 税收优惠」后类别轴随 mock `resourceTarget` 过滤。页顶「分析维度」条也有同名下拉（选项同源）。 |

## 档 C（T40 · 7 条）

默认均为完成态（有图、已选指标、已自定义模板）。切未就绪：关 Switch / 清空 Select。

| 功能点 | 怎么验收 |
|---|---|
| 未具备政策效能评估核心数据时不可生成趋势分析图 | 「趋势指标」卡片 extra「核心数据」Switch 关掉 → Empty，不渲染折线/柱状 |
| 未选取评估指标时不可查看动态趋势 | 页顶维度条「指标」清空后点「应用」→ 趋势图 Empty「未选取评估指标…」（不再回落前 3 项） |
| 未具备政策效果数据时不可生成对比分析图 | 「分组对比」extra「效果数据」Switch 关掉 → Empty，不渲染柱/热力 |
| 未完成政策要素整合时不可展示关联图 | 「多维结构关联」extra「要素整合」关掉 → 弦线/关系网 Empty |
| 未展示效果传导链路时不可追踪影响路径 | 默认弦线图**不高亮**第一条路径；须先点 Radio「传导路径」再点某条链路，才切回弦线并高亮 |
| 未自定义报表模板时不可批量生成报告 | 「报告模板与导出归档」extra「已自定义模板」关掉 → 「加入批量队列」disabled，队列区 Empty |
| 校验汇报周期、分析维度与图表类型均已选择 | 清空「汇报周期」或「图表类型」或取消全部「分析维度」后点导出 / 入队 → 表单校验拦截，不入队 |

## 簇 2 接线（仅可选）

趋势 / 关联 / 导出闸门已在 `analysis/` 子文件就地完成，**不必**再把 `GateEmpty` 接到 `PolicyAnalysis.jsx`。

父会话已接线：`PolicyAnalysis.jsx` 传入 `resourceTarget={appliedDimensions.resourceTarget}`。页顶维度条改投向后点「应用」驱动分组对比图；卡片内 Select 隐藏。
