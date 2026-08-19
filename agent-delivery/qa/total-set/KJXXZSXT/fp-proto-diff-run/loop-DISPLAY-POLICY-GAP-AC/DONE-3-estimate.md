# DONE · 3-estimate（T43 效果预估）

- 任务：`DISPLAY-POLICY-GAP-AC-L01`
- 仓：`repos/demo-ui-science`
- 强度：ponytail full
- 未 commit / 未 push
- 未改 `policyData.js` / `sharedCharts.jsx` / `fp-split-run/`

## 已改文件

| 文件 | 说明 |
|---|---|
| `repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx` | 档 A #17–#23 + 档 C 8 条闸门 |

## 档 A

| # | 功能点 | 怎么验收 |
|---|---|---|
| 17 | 预测对产业发展的影响 | 政策效果推演 → 效果预估 → **新出台效果预测**：右侧「产业发展影响」接入已有 `IndustryImpactChart`（人工智能等产业分），不只 GDP%。 |
| 18 | 预测对科技创新的影响 | 同 Tab 左侧「短中长期效果（经济 / 创新）」三期卡同时出 `gdp` 与 `estimatedEffects.*.innovation`。 |
| 19 | 选择空间模拟的政策类型 | **区域经济空间模拟**：参数区增加「政策类型」Select；改类型后 KPI 随类型系数变；点「运行空间模拟」地图柱高/文案含类型。 |
| 20–23 | 目标合理 / 组织协调 / 程序公正规范 / 方法科学可行 | **利益攸关方参与**顶部「评估活动识别」四卡（页内 mock）。 |

## 档 C（闸门）

默认完成态。切未就绪：清空 Select / 关 Switch / 清空意见。前提不满足 → 按钮 disabled + Empty，不继续渲染完整 mock。

| 功能点 | 怎么点 |
|---|---|
| 未完成关键参数输入时不可仿真模拟 | **未出台政策仿真**：清空「政策类型」或「实施时间」→ 运行按钮 disabled，结果区 Empty。 |
| 未具备历史数据时不可仿真模拟 | 关 Switch「具备历史数据」→ 同上。 |
| 未完成政策文本解析时不可预测效果 | **新出台**：关「文本解析已完成」→ Empty，不渲染趋势/产业图/三期卡。 |
| 未具备历史相似政策效果数据时不可预测效果 | 关「具备历史相似政策效果」→ 同上。 |
| 未选择特定区域时不可模拟区域经济发展 | **区域**：清空「目标区域」→ 运行 disabled，地图与结果 Empty。 |
| 未选择政策类型时不可模拟区域经济发展 | 清空「政策类型」→ 同上。 |
| 未完成各维度评估时不可展示综合效果 | **多维度效果评估**：关「各维评估已完成」→ 雷达/柱/推演结果 Empty。 |
| 未汇总各方意见时不可纳入效果评估模型 | **利益攸关方**：点「清空意见」→ 「纳入评估模型」Switch disabled，列表 Empty。提交问卷可回到完成态。 |

## 页面路径

政策跟踪 → **政策效果推演** → 效果预估（五子 Tab）。本地 vite 默认 4176。

## 未完成 / 不做

- 档 B 106 条、T124 档 D、`fp-split-run` / `work/Txx.md` 结论列：按规则不做。

## 收口（父会话补）

- 页头「预估综合效果」已跟「各维评估已完成」Switch：关 → Empty，不展示 86.5。
- `IndustryImpactChart` 接收 `items`；新出台 Tab 增加政策 Select，产业分随所选政策缩放。
