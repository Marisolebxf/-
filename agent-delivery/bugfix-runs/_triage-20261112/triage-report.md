# 2026-11-12 批量分诊报告：16 个 OPEN 政策域缺陷

> 产物：截图 23 张（本目录 `*.png`）+ 代码定位（explore agent 8cc9859e）。
> 分诊方式：只读 brief + 截图 + 代码定位，**未动工单状态、未认领、未改代码**。
> 工单：GKX 生产 `6a687a81e231818dec771f9a`，全部经办人=淮政玮，报告人=黄敬洲。

## A 组 · 纯前端可修（8 单，建议第一波 subagent 批量修）

| 工单ID | 标题摘要 | 嫌疑文件 | 修复要点 |
|---|---|---|---|
| 7167107397 | 「导出Excel」实际导出 word | `analysis/index.vue` L352-364 `confirmExportReport` | `'excel'` 被三元吞成 `'word'`；修映射分支（需确认导出契约支持 excel） |
| 7167153701 | 「查看关联（演示）」点击无反应 + 文案带（演示） | `analysis/interpret/HotIssueDiagnosisBoard.vue` L261 | 按钮无 `@click`，补接线；去「（演示）」 |
| 7166906229 | 政策舆情评估 Toast/提示框暴露开发任务文案 | `panorama/components/SentimentTab.vue` L280-372 + `sentimentLive.ts` `jobErrMsg` | 任务号/等待秒数/超时内部话术改用户话术 |
| 7166930830 | 政策匹配与推送：开发文案 + code 直出 | `SentimentTab.vue` L556-595 + `sentimentLive.ts` `mapMatchRows` | 删表名话术；主体 code 用已加载 `subjectOptions` 前端反查名称 |
| 7167087763 | 分析报告导出图表无内容 + 「周期」显示 3y | `analysis/ReportTemplateExport.vue` L275-297 + `policyReportExport.ts` | 导出前收集 ECharts 实例转 PNG；period 加 code→标题映射 |
| 7166817412 | 新旧对比导出 pdf/word 图表无数据 + word 图过大 | `panorama/components/VersionCompareModal.vue` L107-135 + `policyReportExport.ts` | 导出前兜底确保 chartOption 就绪；Word 插图按页宽定宽 |
| 7166059325 | 行业领域复选框状态不稳定（上屏不勾选/同级第二个选不中） | `situation/global-innovation/components/IndustrySelect.vue` L55-123 + `lib/industryCluster/resolve.ts` + `search/displayPolicySearchConfig.ts` `asPolicyIndustryValue` | 受控 value 归一化统一；去 DOM 合成 click 改 `@change`；policy 页传参统一树内 code |
| 7167234520（前半） | 弦线图实为关系图 | `analysis/StructureLinkPanel.vue` L111-137 | `type:'graph'` 换 chord/sankey/矩阵（仓内已装 echarts） |

## B 组 · 前端可修一半 + 另一半需数据/产品（4 单，拆开处置）

| 工单ID | 前端半边 | 数据/产品半边 |
|---|---|---|
| 7166979592 | `analysis/schemeBlockReport.ts` L130-179 开发口吻文案改用户话术 | 「报告无数据」上游 eval 任务载荷无行，前端不能造假（D9） |
| 7167287026 | `interpret/TopicIndicatorInteractive.vue` L75-98 表名/行数话术改用户空态 | 无解读行本体等 `gapfill_policy_eval_shell` 灌数（D16） |
| 7167124091 | `analysis/TrendMetricsChart.vue` L111-220 x 轴年/季混排分组修复 | 「组合选取指标」= 需规新交互，**需产品定口径**（登记客户决策清单） |
| 7167233464→7166233464 | `analysis/index.vue` L1306-1322 `openKeyFieldPanorama` 补路由 query→锚点滚动+高亮 | 「定位什么」语义需产品确认（定位到领域筛选 or 具体政策卡） |

## C 组 · 数据/后端依赖，前端空修无意义（3 单，建议转派数据/算法侧）

| 工单ID | 标题 | 根因 |
|---|---|---|
| 7166357090 **P0** | 深度分析报告无内容 | `KeyFieldAnalysisPanel.vue` 骨架在，`深度分析报告` job 载荷无报告行（`trendLive.ts` `trendJobBodyOf` 映射不到字段）→ Python/数据侧补载荷 |
| 7166957136 | 实施效果跟踪缺需规字段（执行情况/受益反馈/社会影响/实时进展/效果指标） | `ImplementationTracker.vue` liveColumns 5 列；需规字段集上游 `ads.policy_effect` 无列 → 数据侧补列/补映射 |
| 7166804371 | 区域差异「实施条件」列恒空 | `sentimentLive.ts` `mapRegionDiff` 载荷无 `condition` 字段 → Python 侧 board 补字段 |

## D 组 · 需契约确认（1 单）

| 工单ID | 标题 | 状况 |
|---|---|---|
| 7166023304 | 政策来源(scope)/适用地区(region) 互覆过滤失效 | 前端确实同发两组参数且语义交叠（`displayPanoramaQuery.ts` L341-391）；前端可先做客户端消歧，**根修需后端确认 scope/region 契约语义** |

## 批量执行建议

1. **第一波（subagent 并行，8 单）**：A 组全部——多为文案脱敏/导出链路/事件接线/受控状态，互相独立可并行；同仓并行用独立 worktree + 按 ship_order 串行合并。
2. **第二波（4 单）**：B 组前端半边随第一波带掉；数据半边与产品决策项另开登记，不阻塞提测。
3. **C 组 3 单**：不在前端 subagent 范围内——按规约转派 Python/数据侧任务（gapfill/ads 补列），前端等载荷就绪后回验。
4. **D 组 1 单**：先向后端确认契约再派单。
5. 口令闸门不变：每单仍需「进入开发」→「提测<编号>」→「验收通过<编号>」，可按波次批量发。

## 附：截图清单（23 张，命名 `<work_item_id>-<序号>.png`）

7166023304-1, 7166059325-1/2, 7166233464-1/2, 7166357090-1, 7166804371-1, 7166817412-1/2, 7166906229-1/2, 7166930830-1, 7166957136-1, 7166979592-1, 7167087763-1/2/3, 7167107397-1, 7167124091-1, 7167153701-1, 7167234520-1/2, 7167287026-1

> 用户存储镜像（Read 可读）：`C:\Users\redfo\AppData\Local\Cursor\AgentStores\cursor_agent_stores\u189766899\files\triage-<id>-<n>.png`
