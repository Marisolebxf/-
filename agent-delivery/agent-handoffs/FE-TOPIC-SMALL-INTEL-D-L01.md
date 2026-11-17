# FE-TOPIC-SMALL-INTEL-D-L01 · 记录页签 + 报告链路 + 防漏自检 · handoff

- **状态**：integration（联调确认中）
- **执行**：[agent:frontend-agent] · 监管：human:孔东
- **仓**：`lumen-ui-topic-mobile` · commit `7965021`（dev，已推送）
- **PC 真源**：`lumen-ui-topic` SynthAnalysisRecordsPanel / synthBlockReportDocument
- **日期**：2026-11-17

## 1. 范围与实现（对照 PC）

| DoD | 实现 | 文件 |
|---|---|---|
| 三叶分析记录页签 | `IntelRecordsPanel`（三叶共用）：列表（服务端 `analysisType: leaf` 过滤）/ 状态筛选 / 查看结果（emit restore → 视图 normalize 注入结果态）/ 复制配置（`intelTaskCtxParams` 回填 ctx）/ 删除（确认框 + 软删） | `src/components/visualization/IntelRecordsPanel.vue` |
| 报告链路 | `chainBlockReportDocument` 新增 intel 三叶块分发（活力：四维+指标体系+排名+趋势+优短+gradeNote；要素：三指数+四维过渡+七类+层次+领域+全景136+贡献路径非因果；协同：四KPI+主体/关系明细+中心Top+孤立+横向+纵向+效果评估样本<3不出系数+策略降级）；数值全部 null 容忍不补 0；记录「查看报告」走 `openSynthReport`（同父任务成功/进行中 PDF 复用，否则建 `{leaf}_report` 产物任务）+ `ChainReportSheet` 渲染 + `analysisTaskAssetDownload` 下载 | `src/utils/chainBlockReportDocument.ts` |
| 三工作台接入 | `van-tabs`（分析工作台/分析记录）+ 结果态「生成报告」按钮（type=success）+ 深链 `report=1` 结果就绪自动开报告 | 三 `Intel*View.vue` |
| 附录 D/E 防漏 | 自检脚本 +5 断言：三视图挂面板+sheet+深链 / 面板四操作+服务端过滤 / 报告分发三叶+null容忍+样本话术 / 路由 9 条真视图 / 附录 E（禁自动 create、单飞、当天复用） | `scripts/intel-synth.test.mjs` |
| 评审层 | StatCard 内建 `MetricMarker`（reviewMode 门控）已在批次 B/C 挂 metric-id；关闭后零泄漏（组件自闸） | 无新增 |

## 2. 复用与零重复

- 记录面板照搬政策页 `PolicyAnalysisConfigView` records 模式（状态筛选/四操作/确认删除话术同款）。
- 报告渲染复用 `ChainReportSheet`（纯 CSS 条形图、下载资产链路既有）。
- 任务载荷解析从 `intelResultSource` 导出 `resolveIntelTaskPayload` 复用（记录回放与 latest 恢复同源）。

## 3. 偏离说明

- 小屏无独立报告整页路由（PC 是 `VitalityReportPage`）：报告以 `ChainReportSheet` 底部弹层承载，深链 `/intelligence/{leaf}/report` 经 `IntelTaskDeepLinkView` 转 `report=1` 回工作台开 sheet（移动交互习惯；PC 报告页 eyebrow/导出权限等桌面元素不适用）。
- instant 态无父任务时报告 `taskId` 落 `snapshot`（PC 同语义：跑批结果只读渲染，下载链路等有任务后再走 Java）。

## 4. 验收证据

- 质量门：`npm run type-check` ✅ / `npm test` 92/92 ✅（新增 5 断言）/ `npm run build` ✅
- 产物清单：`IntelRecordsPanel.vue`（~240 行）、`chainBlockReportDocument.ts` intel 块（~260 行）、三视图接入、自检脚本扩展
- 联调确认：Mock 默认三元组秒开 → 生成报告 → sheet 展示块式内容；tab=records 列表/回放/复制/删除链路完整

## 5. 架构合规自检（§2 铁律）

- ✅ 调用链：前端 → Java REST（analysisTaskList/Result/Delete、产物任务 create），未越层
- ✅ D9：报告数值只读既有结果，null 容忍；metric-id 在 StatCard 层已挂
- ✅ D12：未引 demo-*；对照 PC 只读重写
- ✅ I2-12 / 附录 E：切条件不自动 create（自检断言）；报告产物任务同父复用不重建
- ✅ USE_MOCK=false 零 fixture 参与报告构建（payload 来自任务/snapshot 真源）
- ✅ 诚实性：样本<3 不出系数、贡献路径非因果、clusters/strategies 降级话术全保留

## 6. cost 回填

- actual_tokens: ~130k · model_used: glm-5.3 · actual_cost: ~$0.8 · cost_warn: false

ponytail: full（记录面板/报告 sheet/载荷解析全部复用既有，无新依赖）
