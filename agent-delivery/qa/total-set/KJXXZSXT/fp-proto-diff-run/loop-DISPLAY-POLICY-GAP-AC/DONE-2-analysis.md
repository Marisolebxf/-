# DONE · 2-analysis（T41 闸门 + T42 档 A #11–#16）

- 任务：`DISPLAY-POLICY-GAP-AC-L01`
- 簇：`PolicyAnalysis.jsx`（结果解读 + 推荐方案）
- ponytail: full
- 未改 `policyData.js` / `fp-split-run/` / `work/Txx.md`；未 git commit / push

## 已改文件

- `repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx`
- `repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.css`

## 档 A（#11–#16）

| # | 功能点 | 怎么点验收 |
|---|---|---|
| 11 | 按优劣/风险/ROI 过滤方案列表 | 政策分析评价 → Tab「推荐方案」→「选择推荐方案」卡片标题右侧三个 Select；切「相对较优 / 低风险 / ROI ≥ 3x」列表应变 |
| 12 | 模拟区展示已归档模拟记录 | 同 Tab「方案参数自定义模拟」底部「模拟效果归档」；初始 Empty，采纳后列表出现 |
| 13 | 采纳写入归档集合 | 点「采纳方案」不只 toast：归档列表新增一行（参数 + 投入/产出/ROI/创新指数） |
| 14 | 关键节点可改日期 / 简易甘特 | 「实施路径与风险辅助」上方三格甘特条；Timeline 每节点 DatePicker，改日期后甘特日期跟随 |
| 15 | 方案报告政策汇报/报送 | 点「一键导出所有推荐方案报告」→ Modal 底部「政策汇报/报送」→ toast + Tag「汇报状态：已报送（演示）」 |
| 16 | 内部流转（不复用分析报告分享） | 同一 Modal「内部流转」→ 独立 toast「未复用分析报告分享」+ Tag「流转状态」；分析报告 Tab 的「分享报告」仍是另一套 `handleShareReport` |

## 档 C 闸门（默认完成态，关 Switch 切未就绪）

### T41 结果解读 Tab 顶栏 Switch

| 关哪项 | 期望 |
|---|---|
| 评估报告 | Empty「无评估报告，不可识别政策问题」+ 识别按钮 disabled |
| 问题识别 | Empty「未完成问题识别，不可生成问题诊断看板」；可点「识别政策问题（演示）」 |
| 诊断看板 | Empty「未生成…不可定位…」+「诊断详情」disabled |
| 分类展示 | Empty「未完成分类展示，不可点选板块」+ 点选 disabled |
| 已点选板块 | Empty「未点选…不可联动…」 |
| 多媒体素材 | Empty「无多媒体素材，不可提供辅助解读」 |
| 专家视频 | Empty「未嵌入专家视频点评，不可播放」+ 播放 disabled |
| 报告页内容 | Empty「无报告页内容，不可生成…」+ 生成 disabled |
| 摘要已生成 | Empty「未完成生成，不可编辑/推送」+ 编辑/推送 disabled |

### T42 推荐方案 Tab 顶栏 Switch

| 关哪项 | 期望 |
|---|---|
| 评估模型 | Empty「未具备评估模型，不可生成推荐方案」；「生成推荐方案」disabled；路径 Empty；导出 disabled |
| 已生成方案 | 方案列表 Empty；「生成推荐方案（演示）」可点；路径/导出不可用 |
| 方案≥2 | 雷达/KPI 换成 Empty「生成方案不足两个，不可开展并排对比」；列表仅 1 套 |
| 优劣识别 | 三个筛选 Select disabled + Alert「未完成优劣识别，不可筛选」 |
| 已设关键参数 | 实时预测 Empty「未设置关键参数，不可启动方案模拟」；采纳 / 应用模拟 disabled |

## 未完成项

- 档 B 106 条（方案非真评估模型生成、路径非流程图、导出仍 toast 无真文件）不在本簇
- T124 / 档 D 不派
- 子组件 `HotIssueDiagnosisBoard` / `TopicIndicatorInteractive` / `MultimediaAssistPanel` / `IntelligentSummaryPush` 未改文件：闸门在本页包裹（关 Switch 不挂载完整 mock）
- 并排对比雷达仍绑 `schemeComparisonData` 三套，不随左侧筛选重算（属档 B）
- NLP / 评估模型仅为 mock 文案，无真实调用（按规则）
