# POL-L2-DS11-MOCKAUDIT-L01 · 盘点表

- 日期：2026-11-11（首轮静态盘点 + 代码取证；连库核对见文末）
- 范围：政策分析评价（DS-11）三二级 13 叶 + 分析页三 Tab 块级清单
- 判定口径：**A** 真·读面（ADS/DWD 真表，非缺项表）/ **B** gapfill 缺项表 mock（唯一合规 mock，`is_mock=1`）/ **C** 前端演示态（不落库不进请求）；**违规 = 绕过 gapfill 的数据伪造通道**（接口写死、前端 fixture 直出且无评审标注）
- 代码基线：`lumen-ui-science-pc` dev @ `5447061`（工作区另有 schemeBlockReport 未提交改动，属 231 块式报告演进线，本表按当前工作区实况盘点）
- 证据方法：逐组件读 `defineProps`/`import`/`fetch*` 调用与 `<MockBadge>` 挂点；接口出处对照 VIZ/READ/PLAN 三分册

## 一、逐叶表（219–231）

| 叶 | 判定 | 数据出处（代码实据） | 角标现状 | 缺口/判定说明 |
|---|---|---|---|---|
| 219 多维指标趋势图 | **B 合规** | `TrendMetricsChart.vue` → `fetchPolicyEvalTrend({kind:'趋势'})` → `gapfill_policy_eval_trend`；USE_MOCK 双轨（mock 轨=种子词表，真轨=表内闭集 `trendVocab`） | ✅ 有 | 无行空态不造假曲线；合规 |
| 220 分区/群体对比分析图 | **B 合规** | `RegionGroupCompare.vue` → `fetchPolicyEvalPartition({kind:'分区'})` → `gapfill_policy_eval_partition` | ✅ 有 | subject 三闭集；柱/热力同批行；合规 |
| 221 多维结构关联图 | **合规（诚实空态）** | `StructureLinkPanel.vue`：真轨（USE_MOCK=false）三模式全空态——第 7 项子图无独立消费通道，不用演示矩阵充当 | ✅ 有 | mock 轨保留 demo 冻结视觉（USE_MOCK 双轨契约内） |
| 222 报告模板定制与批量导出 | **B 合规 + C 演示** | `ReportTemplateExport.vue` → `fetchPolicyEvalTemplates({kind:'模板选用'})` → `gapfill_policy_eval_template`；批量导出队列/操作日志为会话演示态（日志仅 USE_MOCK 显示） | ✅ 有（模板/队列/日志三处） | 导出文件=前端拼装当次表单内容（222 契约内交互壳，非数据 mock） |
| 223 热点问题分析看板 | **A 意图 + ⚠️接线断点** | `evaluationWiring.runJob('policy_focus_ads')` → `ads.policy_focus`（真轨 A）；但 `HotIssueDiagnosisBoard.vue` **props 未声明** `focus-ranking/focus-state` 等 → 传入被丢弃，组件仍渲染种子 `hotIssuesData` | ✅ 有 | **违规形态**：页面实际展示=前端 fixture。见 FIX-02 |
| 223 短板条数（页头卡） | **A 合规** | `evaluationWiring.loadCounts()` → `GET evaluation/counts` → `ads.policy_effect` region_gap；无行诚实空 | —（卡挂 QPOL pending 提示） | 唯一真读面统计卡 |
| 224 分主题分指标互动解读 | **⚠️接线断点** | `:server-entries="interpretationEntries"`（真轨 `gapfill_policy_eval_shell` entryKind=解读）已传入，但组件 props 只声明种子默认 → 服务端行被丢弃，展示种子 `interactiveAnalysisData` | ✅ 有 | **违规形态**。见 FIX-02 |
| 225 多媒体辅助解读 | **⚠️接线断点** | 同上：`multimediaEntries`（shell entryKind=多媒体）传入未声明 → 展示种子 `multimediaPlaylist`（含演示视频/动画 timer） | ✅ 有 | **违规形态**。见 FIX-02 |
| 226 智能摘要与结论推送 | **⚠️接线断点** | `summaryLines`（`ads.policy_text_parse.summary`，真轨 A）+ `runSummaryJob` 传入未声明 → 展示种子 `intelligentSummary`；「生成摘要（演示）」toast 已如实声明 | ✅ 有 | **违规形态**。见 FIX-02 |
| 227 多方案对比展示 | **B 合规** | `schemePlanWiring.loadCompare()` → `POST jobs {kind:方案对照}` → `gapfill_policy_eval_scheme`；雷达/KPI 维度=行上 compare_items 并集，行<2 对比空 | ✅ 有 | 经 `schemeRowParse.ts` 归一（WIRING-L01 已验收） |
| 228 方案参数自定义模拟 | **B 合规** | `POST jobs {kind:参数模拟}` 同表；换档=换一次查询，行原样展示不现算 | 块级由 227 闸门行覆盖 | 左栏方案卡同源 227（同块语义） |
| 229 实施路径与风险辅助 | **B 合规** | `POST jobs {kind:路径与风险}` 同表；sort_no=id 升序；风险=带 risk_title 节点行 | 块级由 227 闸门行覆盖 | 行上 metric_id=M_POLICY_DS_11_POLICY_EVAL_015（GAPFILL 单已核） |
| 230 互动意见收集与专家参与 | **B 合规 + C 契约内** | `GET shells {kind:互动意见, scheme_name}` → 同表；分类闭集评价/评论/建议外丢弃；页面新评价只入浏览器会话数组（230 分册「请求不插入」契约内，**不算违规**） | ✅ 有 | 库内 6 行（种子批），每方案 3 条 |
| 231 方案报告导出与归档 | **B 合规 + C 契约内** | `GET shells {kind:方案报告}` → 方案对照行+意见行拼装；块式 HTML 报告+PDF 导出=前端从当次行生成（「不灌文件」契约内） | ✅ 有 | 无方案对照行则报告空 |

## 二、块级表（三 Tab 全块，含非序号块）

### 页头（跨 Tab）

| 块 | 判定 | 出处 | 缺口 |
|---|---|---|---|
| 统计卡「分析报告 128 份」 | **违规** | 写死字面量 | 无接口。FIX-01 |
| 统计卡「焦点指数 78 分」 | **违规** | 写死字面量（契约=jobs 异步读 ads.policy_focus，页内 223 板块才接） | FIX-01 |
| 统计卡「效果评分 86.5」 | **违规** | 写死（M_POLICY_EFFECT_SCORE 无读面出处） | FIX-01 |
| 统计卡「短板数」 | **A 合规** | counts 真轨 | 无 |
| 统计卡「布局建议 8 套」 | **违规** | 写死（METRIC 分册明示 227–231 不挂 M_POLICY_LAYOUT_REC_COUNT） | FIX-01 |
| 统计卡「机遇数 156 条」 | **违规** | 写死（READ 分册：机遇条数无本段序号） | FIX-01 |

### Tab1 report（分析报告可视化）

| 块 | 判定 | 出处 | 角标 | 缺口 |
|---|---|---|---|---|
| 分析维度条 DimensionBar | C（筛选器，无数据承诺） | 前端状态 | ✅ | 无 |
| 评估指标体系卡（进度条+雷达） | **违规（前端 fixture）** | 种子 `evaluationMetrics` 直出，无接口 | ❌ **无** | FIX-03 |
| 分享/导出报告按钮（toolbar） | C 演示态 | `analysisExport` 前端拼装 | ❌ 无 | FIX-05（小：补 C 类标注） |
| 219 趋势 | B 合规 | 真轨 | ✅ | 无 |
| 220 区域组对比 | B 合规 | 真轨 | ✅ | 无 |
| 三联画像 PortraitTrio | **违规（前端 fixture）** | 种子 `policyPortraitSummaries` | ✅ 有（但按口径仍违规） | FIX-03 |
| 地理分布图 GeographicMapPanel | **违规（前端 fixture）** | 种子 | ✅ 有 | FIX-03 |
| 分地区落实率 ImplementationByRegion | **违规（前端 fixture）** | 种子 | ✅ 有 | FIX-03 |
| 话题热力图+情感分布 | **违规（前端 fixture）** | 种子 `topicHeatmapData` | ✅ 有 | FIX-03 |
| 产业影响力气泡图 | **违规（前端 fixture）** | 种子 `bubbleChartData` | ✅ 有 | FIX-03 |
| 221 结构关联 | 合规空态 | 真轨无通道→空 | ✅ | 无 |
| 222 模板导出 | B 合规 | 真轨 | ✅ | 无 |

### Tab2 interpret（结果解读）

| 块 | 判定 | 出处 | 角标 | 缺口 |
|---|---|---|---|---|
| T41 闸门 Switch 条 | C 演示态 | `t41` 前端状态 | ✅ | 无 |
| 识别/诊断/点选/生成等「（演示）」按钮 | C 演示态 | toast 已声明演示 | —（闸门覆盖） | 无 |
| 223 看板 | ⚠️ 断点（表一已列） | 组件吃种子 | ✅ | FIX-02 |
| 224 互动解读 | ⚠️ 断点 | 组件吃种子 | ✅ | FIX-02 |
| 225 多媒体 | ⚠️ 断点 | 组件吃种子 | ✅ | FIX-02 |
| 226 智能摘要 | ⚠️ 断点 | 组件吃种子 | ✅ | FIX-02 |
| 政策文本辅助解读 PolicyTextAnalysis | **违规（前端 fixture）** | 种子 `policyTextAnalysis` 直出（三个子 Tab） | ❌ **无** | FIX-04 |

### Tab3 recommend（推荐方案）

| 块 | 判定 | 出处 | 角标 | 缺口 |
|---|---|---|---|---|
| T42 闸门条 | C 演示态 | 前端状态 | ✅ | 无 |
| 227–231 五叶 | B 合规 | 全部真轨 gapfill | ✅（227/230/231 独立挂，228/229 由闸门行覆盖） | 228/229 建议补块级角标（FIX-05） |
| 选择推荐方案卡（左栏） | B（227 同源） | 同 227 | —（同块） | 无 |
| 汇报/流转按钮 | C 演示态 | toast「演示，未外发」 | ❌ 无 | FIX-05（小） |

## 三、违规/缺口清单（各挂 FIX 子单，本单只登记不修）

| 单号 | 内容 | 强度 | 优先级 |
|---|---|---|---|
| `POL-L2-DS11-MOCKAUDIT-FIX-01` | 页头 5 张写死统计卡（128/78/86.5/8/156）：接真轨读面（焦点/机遇有分册出处；效果评分/布局建议/分析报告份数无出处→应显 — 或撤卡） | 2 点 | P1 |
| `POL-L2-DS11-MOCKAUDIT-FIX-02` | READ 四组件 props 断点：`HotIssueDiagnosisBoard/TopicIndicatorInteractive/MultimediaAssistPanel/IntelligentSummaryPush` 声明 `focus-ranking/server-entries/server-lines` 等 props，接 `evaluationWiring` 真轨行；种子降级为 USE_MOCK 轨默认 | 3 点 | P1 |
| `POL-L2-DS11-MOCKAUDIT-FIX-03` | Tab1 六个前端 fixture 卡（指标体系/三联画像/地理/落实率/话题热力/气泡）：无分册出处与接口 → 二选一：挂 A 类读面（需先立 DATA 单）或评审模式明确标「前端种子（无后端出处）」+ 上线态撤数据 | 2 点 | P2 |
| `POL-L2-DS11-MOCKAUDIT-FIX-04` | `PolicyTextAnalysis` 种子直出且无角标：补 C 类标注或接 237 文本解析真轨 | 1 点 | P2 |
| `POL-L2-DS11-MOCKAUDIT-FIX-05` | 角标 reason 口径统一 + 小缺口：MockBadge 全部补 reason 文案（`gapfill 缺项表 mock（出处 库.表）` / `前端演示态（不落库）`）；228/229 补块级角标；分享/汇报按钮补 C 标 | 1 点 | P2 |

## 四、结论速览

- **合规主力**：227–231 五叶全部读 `gapfill_policy_eval_scheme`（B），219/220/222 三叶读各自缺项表（B），223 短板数读 ADS（A）——**9/13 叶合规**。
- **221** 诚实空态合规；**230 页内评价、231 前端导出**属契约内 C，不算 mock。
- **不合规集中在**：① READ 四组件接线断点（真轨行已拉到但组件没接，页面实际展示前端种子）；② 页头 5 张写死统计卡；③ Tab1 六张无后端出处的种子直出卡；④ 两处无角标裸奔（PolicyTextAnalysis、评估指标体系卡）。
- **评审模式现状**：MockBadge 挂点较全（页内 ≥20 处），但全部无 reason 文案、且 A/B/C 三层不区分；`?review=1` 的闸门条只覆盖 Tab2/Tab3 流程演示，未做数据来源标注。

## 五、连库核对

本轮未连库（判定基于代码与三分册；gapfill 各表行数以 2026-11-11 凌晨数据修复后的复核为准：scheme 19 行、shell 7 行、trend/partition/template 仅按钮批）。执行 FIX 单时需连库核对各表 `is_mock` 与行集。
