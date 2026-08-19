# DONE · 4-interpret（T44 推演）

- 任务：`DISPLAY-POLICY-GAP-AC-L01`
- 簇：InterpretWorkbench
- ponytail: full
- 禁 commit / push；未改 `fp-split-run/`、`work/Txx.md`

## 已改文件

| 文件 | 改什么 |
|---|---|
| `repos/demo-ui-science/src/pages/policy-tracking/simulation/interpret/InterpretWorkbench.jsx` | Select 选文本；重点柱图；覆盖面展示；历史对照先于预测；档 C 18 条 disabled + Empty + Switch |
| `repos/demo-ui-science/src/pages/policy-tracking/policyData.js` | 仅三块：`policyTextAnalysis`（补 `'5'` 核心内容/战略意图）、`policyImpactScopeData`（覆盖面）、`policyPathForecastData`（history + forecast） |
| 未改 | `sharedCharts.jsx`（复用已有 `MultiDimensionBarChart` / `ImpactRegionBarChart`） |

## 档 A

| # | 功能点 | 怎么点 |
|---|---|---|
| 24 | 选择待解析的政策文本 | 解析 Tab 顶部 Select，默认 `'1'`；切 `'5'` 关键词/支持对象/支持力度跟着变 |
| 25 | 以图表展示政策重点 | 重点 Tab 导图下方「政策重点（柱图）」四枝：目标/领域/路径/资金 |
| 26 | 识别政策覆盖面 | 影响范围 Tab「覆盖面」覆盖率/应覆盖/已覆盖 + 分区域覆盖面柱；空间图仍标渗透指数，不冒充 |
| 27 | 汇聚历史数据 | 路径 Tab 先「历史对照（汇聚样本 3 条）」，再「政策实施流程图（预测）」 |

## 档 C（18 条）

默认完成态。切未就绪：清空 Select 或关对应 Switch。

| 功能点 | 操作 | 期望 |
|---|---|---|
| 未选择政策文本时不可解析 | 解析 Tab 清空 Select | 「解析」disabled；Empty「未选择政策文本，不可解析」 |
| 未完成解析时不可查看结构化结果 | 选文本后关「解析完成」 | Empty「未完成解析…」；开 Switch 或点「解析」恢复 |
| 未具备政策重点内容时不可可视化展示 | 重点 Tab 关「具备重点内容」 | Empty；导图/柱图不渲染 |
| 未完成可视化时不可查看详细说明 | 关「可视化完成」 | 图仍在；右侧 Empty「未完成可视化…」 |
| 未具备政策效果推演结果时不可分析影响范围 | 影响范围关「具备推演结果」 | 「分析影响范围」disabled；Empty |
| 未完成影响范围分析时不可查看空间分布 | 开推演、关「分析完成」 | 覆盖面可见；空间图不渲染 |
| 未完成影响范围分析时不可查看时间变化 | 同上 | 时间轴不渲染 |
| 未指定当前政策时不可分析关联 | 解析 Tab 清空 Select 再进关联 | Empty「未指定当前政策…」 |
| 知识图谱不可用时不可分析政策关联 | 关联 Tab 关「图谱可用」 | Empty「知识图谱不可用…」 |
| 未完成关联分析时不可查看关联网络图 | 关「关联完成」 | Empty；网络图不渲染 |
| 未具备政策内容时不可预测实施路径 | 关解析完成再进路径 | Empty「未具备政策内容…」 |
| 历史数据不足时不可预测实施路径 | 路径 Tab 关「历史数据充足」 | Empty「历史数据不足…」 |
| 未完成预测时不可查看实施流程图 | 关「预测完成」 | Empty；流程图不渲染 |
| 未完成预测时不可查看关键节点说明 | 同上 | 节点说明一并隐藏 |
| 未具备政策解析结果时不可生成解读报告 | 报告 Tab 关「具备解析结果」 | 「生成」disabled；Empty |
| 未具备效果推演结果时不可生成解读报告 | 关「具备推演结果」 | Empty「未具备效果推演结果…」 |
| 未生成报告时不可查看 | 关「已生成」 | 预览 Empty「未生成报告，不可查看」 |
| 未生成报告时不可下载 | 同上 | 「下载」disabled |

## 页面入口

本地 `pnpm dev`（vite 约 4176）→ 政策跟踪 → 效果推演 / 科技政策推演 → `InterpretWorkbench` 六子 Tab（解析 / 重点 / 影响范围 / 关联 / 路径 / 报告）。

## 未做（本簇范围外）

- 档 B：影响范围不读 Estimate `simulationResults`；报告正文仍是静态草稿、不从解析/推演组装；路径仍是 Timeline 不是甘特/流程图
- 档 D / T124、T19–T21、`fp-split-run/`、git commit
