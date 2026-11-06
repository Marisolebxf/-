# M3 类型修复 + M5/M6 真实链路整改 + 三页报告导出（2026-11-03）

> 范围：`lumen-ui-science-pc` 的 `src/views/situation/{tracking,bay-innovation,shenzhen-innovation,global-innovation,shared}`
> 约束：**不改前端既有样式与结构**，只换数据源、补空态、改口径文案、新增报告/导出功能
> 上游依据：久新库实测 + ADS_SCHEMA 6.30.0 + 指标台账（249,482 B / `4850a839` 最新版）+ 算法侧产物

---

## 一、M3（技术发展跟踪）type-check 修复

仓库基线 `pnpm type-check` 原本失败，报错全部来自已提交的 `e5c5085`，与本页业务无关但会阻塞构建。本轮全部修掉，**未改任何行为**。

| # | 位置 | 报错 | 修法 | 依据 |
|---|---|---|---|---|
| 1 | `mock/modules/tracking.ts:1353` | `b.heat/a.heat` 可能为 null | 排序改 `(x.heat ?? -1)`，缺值沉底 | `TrackingHotTopic.heat` 类型本就是 `number \| null`（后端评估表可缺列），原代码当 number 用 |
| 2 | `tracking.ts:1381` | `item.heat` 求和 | mock 聚合 `?? 0` 并注明「仅 mock 种子构造器」 | mock 演示路径，真实数据集走 api 不经过此函数 |
| 3 | `tracking.ts:1403-1405` | heat/potential/maturity 求和 | 同上 `?? 0` | 同上 |
| 4 | `tracking.ts:1420-1422` | heat/scale/investment 运算 | **保留 null**：缺源维度整行留空 | `HeatMatrixRow.attentionValues` 允许 `number \| null`，压 0 会伪造「热度为 0」 |
| 5 | `tracking.ts:1475-1478` | 四个 bubble 维度 | `item.x == null ? null : clamp(...)` | `TrackingBubble` 允许 null，不得凭空生成分值 |
| 6 | `tracking.ts:1484` | `item.maturity` 求和 | `?? 0` | mock 工作流阶段判定 |
| 7 | `types/tracking.ts:488` | `TrackingEvaluationRunParams` 缺 `regionLabel` | 补可选字段 + 注释 | **后端 TrackingController.java:855 确实读取并使用该字段**，是前端类型漏声明 |
| 8 | `types/tracking.ts:545` | `TrackingMetaResult` 缺 `dataSourceNote` | 补可选字段 | **后端 TrackingController.java:1108 / 1972 均下发该字段** |
| 9 | `ResultDashboard.vue:1512` | `TrackingBubble` 不能赋给 `(typeof resultTimelineBubbleRows.value)[number]` | 参数类型改 `TrackingBubble \| null \| undefined` | 与 `BubbleHitTargets` 的 emit 类型对齐 |
| 10 | `ResultDashboard.vue:1835/1838/1839` | `activeResultTrackingDimensionSummary` 可能 undefined | 模板加 `?.` + 兜底文案 | `summaries[dim] ?? summaries.overall` 两者都可能缺 |
| 11 | `tracking/index.vue:954` | `meta.dataSourceNote` 不存在 | 去掉多余的 `as Record<string, unknown>` 断言 | 断言反而屏蔽了字段类型 |

**结果**：`pnpm type-check` 全绿（项目 0 error）。这是本轮唯一改到的非 M5/M6 文件，且全部为类型/空值安全修复。

---

## 二、M5（湾区创新监测）整改

审计结论：**P0 14 处、P1 31 处**。本轮清掉全部 P0。

| # | 决策 | 依据 | 落点 |
|---|---|---|---|
| 1 | 四维权重 `30%/25%/25%/20%` → 全部「—」 | `ads_geo_yearly_index` 按 ADS_SCHEMA.md:2962「公式批准前保持空表」，实测 0 行，无任何权重来源 | `CalcMethodModal.vue` |
| 2 | 综合得分公式 `0.30×…+0.20×…` → 改为「暂时不能计算 + 原因」 | 同上 | `CalcMethodModal.vue` |
| 3 | 数据来源 5 条外部统计（国家统计局/广东省统计局/各市科技局/知识产权局/火炬中心）→ 改为 2 条久新真实表 | 本页一条外部来源都没接，属把 demo 来源当官方口径展示 | `CalcMethodModal.vue` |
| 4 | 更新频率「按季度更新」→「按年度统计口径，与久新同步」 | 久新是按年数仓 | `CalcMethodModal.vue` |
| 5 | 指标权重恒空集 | 原读 mock `getIndicatorWeightRows`，真实 id 未命中仍返回 18%/34%/48% 编造权重 | `CalcMethodModal.vue`、`IndicatorSpecTrigger.vue` |
| 6 | 「可靠性」不再默认「官方发布口径」→ 无源即「—」 | 默认值等于替无源数据背书 | `IndicatorSpecTrigger.vue` |
| 7 | 同比/环比 NaN 直渲 → 统一 `fmtPctOrDash`（6 处） | 后端明确把 yoy/mom 置 NaN（无源列），原页面渲染 `+NaN%` 且着红绿色 | `IndicatorsTab.vue` |
| 8 | 「是否预警」三态化 | `NaN < floor` 恒 false → 一律显示「否」，等于对无源数据宣称正常 | `IndicatorsTab.vue` |
| 9 | 「未发现明显触发项」→ 无规则时「无法判定」 | 同上 | `IndicatorsTab.vue` |
| 10 | 预警阈值文案标明「前端本地试算，非服务端预警」 | 久新无预警规则表 | `IndicatorsTab.vue`、`CapacityTab.vue` |
| 11 | 洞察「同比增速最高城市」改为有值才输出 | 原 `sort((a,b)=>b.yoy-a.yoy)` 在 NaN 下退化为原序 → 随机点名城市 + 渲染 NaN% | `bayAreaModel.ts` |
| 12 | 「近五期保持上行」→ 「较首期累计变化 X%」 | 「五期」写死，且无论涨跌都宣称上行 | `bayAreaModel.ts` |
| 13 | 「综合贡献 权重 NaN%」→ 权重/基准无源则整条不出 | 同上 | `bayAreaModel.ts` |
| 14 | 诊断报告加数据 guard；SWOT 为空时整块空态 | 原无数据也渲染「本报告依据 SWOT 四类因素分析形成…结论」 | `DiagnosisReportModal.vue` |
| 15 | 删 1500ms「模拟生成」；无 SWOT 时按钮 disabled | 假动作 | `SwotAnalysisTab.vue` |
| 16 | 通知记录 Tab 补空态 | 后端 alerts 恒空 → 永远白板 | `AlertCenterDrawer.vue` |
| 17 | 环形图环心无源显示「—」，进度弧不画 0 | `Number(x) \|\| 0` 把无源画成 0%，环心渲染 NaN | `CapacityTab.vue` |
| 18 | 页级取数失败加错误态 + 重试 | 原 catch 只 `console.error`，四 Tab 全空、无提示 | `bay-innovation/index.vue` |

---

## 三、M6（深圳创新监测）整改

审计结论：**P0 12 处、P1 34 处**。本轮清掉全部 P0。

| # | 决策 | 依据 | 落点 |
|---|---|---|---|
| 1 | 载体对比雷达**不再绘制**，出空态说明 | 雷达三项全无源：成果分/潜力分来自 mock 加权编造口径（`patents/500×40 + papers/300×35 + projects/60×25`，函数注释自己写明「真实路径不要当综合指标展示」），创新价值由后端 `noSourceFields` 声明缺失 | `CarrierTab.vue` |
| 2 | 对比摘要改为陈述真实计数 | 原调 mock `buildSzCarrierCompareSummary` 用假分排「A 成果领先/B 价值最高/C 潜力更强」 | `CarrierTab.vue` |
| 3 | 载体卡「创新价值 {{value}}」→ `fmtCarrierNum` | 无源渲染 `NaN` | `CarrierTab.vue` |
| 4 | 排名进度条无源时不画 | `Math.max(8, …)` 会伪装出一根 8% 的假条 | `CarrierTab.vue` |
| 5 | 详情弹窗四项计数与描述统一 `fmtCarrierNum` / `—` | 部分载体缺列 | `CarrierTab.vue` |
| 6 | 订阅 toast「订阅成功」→「已加入本次会话清单（未接订阅接口）」 | 无订阅写接口，原话术会被读成服务端已落库 | `CarrierTab.vue` |
| 7 | 缺口瀑布删除 `0.43/0.34/0.23` 假归因与「产业创新优势 20%」 | 四个系数无任何来源，把一个真实分差拆成四条编造归因 | `CompareTab.vue` |
| 8 | 报告删除「四、历史趋势与未来预测」与写死 `2021-2025` | 久新未下发年份维度与能力分历史，预测是编造 | `CompareTab.vue` |
| 9 | 「全局判断基于全量样本池形成」→「综合得分取自后端城市对标表」 | 原句暗示了不存在的统计推断 | `CompareTab.vue` |
| 10 | 删死码 `showForecastNotice` 提示块 | `v-if` 恒 false，永远不会显示 | `CompareTab.vue` |
| 11 | 领域「优势/潜力/薄弱」改为「按当前排序指标分段，非综合评价」 | 原 `classifySzDomainAdviceRows` 把排序切三段，读起来像综合评价结论 | `DomainTab.vue` |
| 12 | 指标页「生成并导出」改为真实 CSV 导出 | 原只 `showIndicatorDetail = true`，名字叫导出却什么都不下载 | `IndicatorTab.vue` |
| 13 | 「五年累计变化 / 2021-2025」→「按实际数据期次」 | 期次由后端 history 决定，写死年份会把真实值错标 | `IndicatorTab.vue` |
| 14 | 页级取数失败加错误态 + 重试 | 原 catch 只 `console.error`；且 api 层 `block()` 失败只 `console.warn` 回落 `[]`，错误根本冒不到页面 | `shenzhen-innovation/index.vue` |

---

## 四、报告与导出（三页统一）

### 4.1 方案选择

M4/M5/M6 后端**均无报告端点** —— 全仓只有技术发展跟踪 `TrackingController` 有 `/reports` 与 `gkx_tech_report_record` 表。因此「参考技术发展追踪」落地为：

- **结构参考 M3**：标题 + 生成时间 + 「数据口径」区块 + 分章节正文 + 页脚声明；
- **实现改为纯前端**：数据 → HTML → Word(.doc) / 打印另存 PDF / CSV，不依赖后端转换服务。

### 4.2 公共工具

新建 `src/views/situation/shared/reportExport.ts`（仓内第 3 处 blob 下载，按「第二处出现即封装」沉淀）：

| 导出 | 用途 |
|---|---|
| `buildReportDocument` | 组装完整 HTML 文档（内联样式，Word 与打印都能正确渲染） |
| `buildAutoTable` | 对象数组 → 表格，只取顶层标量字段，后端加字段自动多一列，减字段不崩 |
| `downloadReportAsWord` / `downloadReportAsHtml` | Blob 下载 |
| `printReportHtml` | 隐藏 iframe 打印（避免 `window.open` 被拦截），打印后移除 |
| `downloadCsv` | CSV 导出，UTF-8 BOM，逗号/引号/换行正确转义 |
| `reportValue` / `escapeReportHtml` | 无源一律「—」，所有文本转义 |

**诚实性约束写进工具注释**：不得补 0、不得外推、不得下结论、每份报告必须带数据口径区块。

### 4.3 三页入口

| 页 | 按钮 | 报告章节 |
|---|---|---|
| M4 全球创新监测 | 生成报告 / 打印另存 PDF / 导出数据 | 成果、实时、载体、城市、监测（预警为空则写明「预期缺口」） |
| M5 湾区创新监测 | 同上 | 成果、能力、指标、SWOT、预警 |
| M6 深圳创新监测 | 同上；指标页另有「生成并导出」 | 载体、指标、领域、城市对标 |

M3 本身的报告链路（后端 PDF + 报告记录）未改动。

---

## 五、验证

| 项 | 结果 |
|---|---|
| `pnpm type-check` | ✅ 全绿（M3 基线错误 + 本轮新增代码，0 error） |
| `pnpm build-only` | ✅ 绿（`✓ built in 1m 27s`） |
| M3/M4/M5/M6 lint | 0 error / 0 warning（逐目录 `read_lints`） |
| 全页 `Math.random` | 0（M5/M6 早在 10-30 已移除） |

---

## 六、未做与去向

| 项 | 原因 | 任务 |
|---|---|---|
| M5 剩余 P1（影响力分展示、热点凑数、环形图单卡 undefined、表格/地图空态） | 体验类问题，不影响可信度 | `FE-TS-05B` |
| M6 剩余 P1（空历史年份渲染、单指标空态、搜索无结果、领域表格空态） | 同上 | `FE-TS-06B` |
| M4 领域×国家 / 领域-国家地图 / 覆盖率披露 | 需前端选中入口与新契约 | `FE-TS-04B/04C/04D` |
| 后端报告端点（PDF 服务端渲染、报告记录表） | 需后端新建，非前端范围 | 待立项 |
| `cityModel.ts` 领域加权 `0.7/0.3`、`0.55/0.45` | 输入是真实计数，改权重会改变排名语义 | 待产品裁定 |

---

## 七、2026-11-06 追加轮：M6 载体榜久新真实链路实测校正（BE-TS-06A）

> 范围：三仓（lumen-topic-py / lumen-svc-platform / lumen-ui-science-pc）。本轮**连久新 Doris 真库实测**，两个探针结论推翻了此前基于文档的判断，全部按实测落地。

### 实测推翻的两项

| # | 此前判断 | 实测结论 | 处置 |
|---|---|---|---|
| 1 | 按 ADS_SCHEMA 6.30 文档接入 20 个「新增扩展列」 | `ads_institution_profile` 实为 **71 列**，17 个文档列在库里**不存在**（citations_count / h_index / patent_grant_* / research_to_patent_* / 合作指数 / 档案完整度等），照文档硬查载体榜**整榜空掉** | 17 列全部撤下进 `noSourceFields`；只装实测存在且深圳填充率 ≥90% 的列 |
| 2 | 「两段式查询规避 JOIN 代价」（11-05 改造） | **LEFT JOIN 27ms vs 两段式 77ms**（min-of-3，64698 行右表主键哈希连接几乎免费） | 回退单条 LEFT JOIN，列分层降级保留 |

### 实测新增的口径事实与标注（全部透传至前端可见）

| 口径事实（实测） | 标注方式 |
|---|---|
| 经费全额 = 真实换算额 + 模拟额，深圳真实覆盖率仅 **1.3%~3.2%** | 详情页「全额（真实额 X，覆盖率 Y%，其余为模拟额）」+ `fundingAmountMixType` 构成标签 |
| 代表性专利转化额为 TOP20 专利**模拟**推算（scope_status 恒 `REPRESENTATIVE_PATENT_TOP20_SIMULATED`，件数 ≤20） | 「模拟推算，非真实成交额」灰字斜体（`szi-detail-caveat`） |
| 专利年度数据覆盖至 **2022**（2023 起全库恒 0，覆盖滞后非产出归零） | `patent_coverage_last_year` 三层透传 + 年度序列「专利覆盖」提示行 |
| 年度表 `project_count` 全库全 NULL（816,120 行非空数=0） | `project_count_available=false`，前端删「项目」列 |
| `city_name='深圳'` 135 行 vs `'深圳市'` 1 行脏数据 | Python 端补归一化（直调端点传「深圳市」不再假空） |

### 技术机制

- Python `_columns_of`：information_schema 被 test2 账号拒（Permission denied）后自动关闭该路径，改走 `SELECT * FROM t LIMIT 1` 取 keys；探测失败不阻断主查询。
- 列分层：核心列 / 实测扩展列 / 技术力三组独立探测，缺列只丢字段不出「—」，降级信号 `unavailable_fields` 三层透传。
- `/carriers/field-coverage` 探针端点留作线上自查基线（深圳 verdict：16 列全可用 / missing=[]）。
- 前端详情抽屉重写为三节：科技实力（0-100 百分位 + 四维 paper/citation/talent/topic）/ 代表性专利转化 / 经费·合作·档案，全部真实列。

### 验证

| 项 | 结果 |
|---|---|
| 真库端点实测（carrier-list / carrier-yearly / city-yearly / field-coverage） | 全部真数据，`unavailable_fields=[]` |
| `python -m py_compile` / `mvn compile` / `vue-tsc --noEmit` | 三绿 |
| 本地三服务起服冒烟（show-py:8082 → display:7099 → vite:3000） | Java→Feign→Python→Doris 全链路通，字段映射/降级信号/口径标记正确 |
| 浏览器视觉验证（Playwright，深圳大学详情抽屉） | 新三节、专利覆盖提示、caveat 样式全部生效；console 仅预期内订阅 401 降级 |

### 提交

| 仓 | commit |
|---|---|
| lumen-topic-py | `de21eee` |
| lumen-svc-platform | `cf64ffc` |
| lumen-ui-science-pc | `5e8f991` |

均已在 `dev` 分支推送（远端新提交经 `rebase --autostash` 合入，其他任务的工作区改动未受影响）。
