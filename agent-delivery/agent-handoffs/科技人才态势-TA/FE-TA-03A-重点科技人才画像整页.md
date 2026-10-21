# FE-TA-03A · 重点科技人才画像 — 整页复刻

- **任务**：FE-TA-03A（Epic：E-FE-TALENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-21
- **状态**：本地工作区完成三绿，**停本地等人工验收**（⚠️ 用户裁定 2026-10-20：完工不自动 commit/push）
- **ponytail**：full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过任何护栏项：D8 token 冻结、D9 3 指标 + 5 missing 卡 + 9 升结构卡、可观测埋点、handoff 全交付；纯函数模型冻结移植不重写；ProfileWorkCard 第二处复用即封装。 |

## 修改内容

### 1. 组件层（demo 画像页 7 Tab + 订阅抽屉 1:1 移植，`src/views/talent/profile/`）

| 组件 | demo 真源 | 说明 |
|---|---|---|
| `index.vue` | `TalentProfilePage.jsx`（474 行） | 整页骨架：检索行（机构/职称/地区三下拉 + 产业级联 + 关键词 a-auto-complete + 上/下一位 + 订阅 Badge + 订阅切换 + 管理员开关 + 评估跳转 + 导出 Excel/PDF + 批量导入）+ 7 Tab PageTabFrame + SubscriptionDrawer + 批量导入 Modal；`initialTalentId` 定位（route.query.talentId）；`talentMatchesKeyword` 语义冻结（name/institution/title/nationality/fieldLabels/fields/fieldKeywords 联合 haystack） |
| `components/ProfileBasicPanel.vue` | `ProfileBasicPanel.jsx` | 基础画像 Tab：基础信息卡（8 字段）+ 教育/工作双 Timeline + 综合评分仪表 + 5 维雷达 + 6 统计卡 + 治理子块（ProfileBasicGovernance） |
| `components/ProfileBasicGovernance.vue` | `ProfileBasicGovernance.jsx`（351 行） | 治理四块：智能校验+更新提醒 / 权限管控+加密处理 / 导入导出 / 反馈订阅；写操作全为**会话级演示态**（不替 BE 拍板，规划 §0 D6：写回走 ADS 人工层 A14 1302 升级项） |
| `components/ProfileRelationPanel.vue` | `ProfileRelationPanel.jsx`（539 行） | 关联画像 Tab：动态聚合 Alert + 智能检索（类型/时间/领域关键词/**语义检索 SEMANTIC_EXPAND 同义词扩展**）+ 四视图（列表/多级穿透树/图谱/标签云）+ 右侧数据溯源详情（变更记录 Timeline + 隐含关系发掘）；`isHotRelation` 高亮语义（paper→高被引/重大、patent→核心技术、project→重大） |
| `components/ProfileAnalysisPanel.vue` | `ProfileAnalysisPanel.jsx` | 分析画像 Tab：学术力多指标图表族 + 相似学者匹配（领域 scope 过滤 + 匹配度排序）+ 历史趋势 + 人才引进评估入口 |
| `components/ProfileRecentWorksPanel.vue` | `ProfileRecentWorksPanel.jsx` | 近期成果 Tab：成果分层（overview/category/timeline/focus 四模式）+ 智能推送区 + 成果详情 + 原文链接 + 全屏模式 |
| `components/ProfileWorkCard.vue` | （从 RecentWorks 内部卡提炼） | **第二处出现即封装**（用户裁定）：overview/category/timeline/focus 四视图共用作品卡；样式自含防裸奔 |
| `components/ProfileNetworkPanel.vue` | `ProfileNetworkPanel.jsx` | 合作网络 Tab：ECharts graph force + roam；**多级钻取**（macro 全景/person 个人/link 关系）+ 聚合模式（机构/领域/主题）+ 聚合团体节点（`agg_` 前缀展开）+ 实时同步（18s 定时权重刷新 + onBeforeUnmount 清理 + 页面不可见暂停语义）+ 智能推荐合作者（度中心性+桥接+高频合作评分）+ 关系历史 Timeline 溯源 |
| `components/ProfileFieldMapPanel.vue` | `ProfileFieldMapPanel.jsx`（836 行最大件） | 研究领域图谱 Tab：NLP 抽取 banner（模型/更新时间）+ 匹配列表 + **领域时间演化面积图** + 关键词云 + 领域详情 graph + 钻取弹窗 + 溯源链接 + `exportPdf()` 暴露（供页头报告导出调用） |
| `components/ProfileHonorsPanel.vue` | `ProfileHonorsPanel.jsx` | 荣誉 Tab：荣誉墙 + 社会影响力指数 + 国际合作表 + 海外出访交流记录 |
| `components/SubscriptionDrawer.vue` | `SubscriptionDrawer.jsx` | 订阅抽屉：订阅通知流（演示态推送）+ 快捷跳画像 + 批量退订 |

### 2. 纯函数模型（冻结移植，`src/views/talent/models/`）

| 模型 | demo 真源 | 函数/常量 |
|---|---|---|
| `profileRelation.ts` | `ProfileRelationPanel.jsx` 顶部纯函数 | `SEMANTIC_EXPAND`（同义词映射 7 组）/ `expandQuery` / `matchSemantic`（hay 联合 title/abstract/venue/fieldKeywords/coAuthors/类型中文）+ `TalentRelationItem` 三类归一类型 |
| `profileMetrics.ts` | `SCI-INT-A14.yaml` | D9 挂点常量：`PROFILE_METRICS`（deep160 本地 + deep162/graph110 复用 01A talentMetrics 单一真源）+ `PROFILE_MISSING_METRICS`（1307/1312/1316/1318/1319 五卡） |
| `profileReportExport.ts` | `profileReportExport.js` | `exportProfilePdf`（专用打印页管线：build HTML → 隐窗 print → PDF）/ `downloadProfileTextFile`（CSV BOM 头 + 模板下载） |
| `fieldMapReportExport.ts` | `fieldMapReportExport.js` | `buildFieldMapReportHtml` / `printFieldMapReport`（领域图谱报告专用打印页，不 window.print 整页） |

### 3. 样式与基座复用

- `styles/demo-talent-profile.css`：demo `talent-profile.css` 冻结移植 + `.tl-metric-missing-mark` 自含红问号样式 + `.arco-modal-body` 覆盖。
- 基座复用（FE-TA-S01）：`PageTabFrame`（7 Tab 壳）、`talentNav` store、`useTalentTrack` 埋点、`fieldConfig`（titleOptions/anyTalentFieldInScope）、mock 种子 `talentSeed.ts`（`getTalentProfileData` 冻结）、api 双轨 `fetchTalentProfileDataset`。
- 跨模块复用（FE-TA-01A）：`IndustrySelect` 产业级联、`MetricSpecHint` / `MockBadge` 血缘组件。

### 4. Arco 替换清单（antd → Arco Design Vue）

| antd | Arco | 备注 |
|---|---|---|
| AutoComplete | `a-auto-complete` | 页头关键词检索（filter-option 桥接） |
| Select | `a-select` | 三下拉 + 类型/时间筛选 |
| Switch | `a-switch`（v-model） | 管理员开关 |
| Badge | `a-badge`（:count + :offset） | 订阅计数 |
| Modal | `a-modal`（v-model:open + :footer=false） | 批量导入/反馈/导出 |
| Upload（beforeUpload return false） | `a-upload` **customRequest** | demo「不发请求不写库」冻结语义经 Arco 等价实现：`importCustomRequest` 读 fileItem.File 本地 FileReader 解析后返回哑 request |
| Tree（title render） | `a-tree` + `#title` 插槽 | 多级穿透树；自定义 `item`/`sourceUrl` 扩展字段经运行时窄化（`as { sourceUrl?: unknown }`） |
| Input.Search | `a-input-search` | 领域关键词/语义检索 |
| Segmented | `a-radio-group type=button` | 四视图切换 |
| Timeline | `a-timeline` + `a-timeline-item` | 变更记录/教育/工作经历 |
| Drawer | `a-drawer` | SubscriptionDrawer |
| Table | `a-table`（:columns TableColumnData[]） | 国际合作表 |
| message | `Message.success/info/warning` | 指令式提示 |

### 5. D9 数据血缘挂点

**已挂 3 指标（MetricSpecHint ⓘ，口径文本进 `profileMetrics.ts`；deep162/graph110 复用 01A `talentMetrics.ts` 单一真源不另抄）**：

| metric_id | 挂点 |
|---|---|
| `M_TALENT_DEEP_160_1` 画像增强关系链 | ProfileRelationPanel「智能检索与筛选」标题 ⓘ / ProfileNetworkPanel 图谱区 ⓘ / ProfileFieldMapPanel 领域匹配区 ⓘ |
| `M_TALENT_DEEP_162_1` 学术力指标 | ProfileAnalysisPanel 分析图表族标题 ⓘ |
| `M_TALENT_GRAPH_110_1` 人才实体识别 | ProfileFieldMapPanel 领域图谱区 ⓘ |

**5 张 metric_missing 卡（红问号 + title 无源说明，不伪闭合）**：

| 卡 | 挂点 |
|---|---|
| INT-A-X-1307 语义检索 | ProfileRelationPanel 语义检索框尾 `?`（确认前只做关键词筛选，当前为 demo 同义词扩展演示） |
| INT-A-X-1312 相似人才与历史趋势 | ProfileAnalysisPanel 相似学者区 `?` |
| INT-A-X-1316 近期成果列表 | ProfileRecentWorksPanel 成果列表标题 `?` |
| INT-A-X-1318 智能推送与动态更新 | ProfileRecentWorksPanel 推送区 `?`（DN-A14-PUSH 未定，不承诺实时推送） |
| INT-A-X-1319 成果详情与原文链接 | ProfileRecentWorksPanel 详情区 `?` |

**9 张 structure_escalation 卡（talent·talent_coop 未建 / 写回人工层未定）**：mock 态照 demo 渲染，挂对应 metric ⓘ（160/110），升结构状态写 profileMetrics 注释，不在 UI 伪造结构结论。

**写操作演示态**（ProfileBasicGovernance + 批量导入）：Message 文案均带「演示：不写入人才库」字样；mock 种子 USE_MOCK=false 时不参与。

### 6. demo 逐区块对照表（TalentProfilePage 结构序）

| # | demo 区块 | lumen 落点 | 状态 |
|---|---|---|---|
| 1 | 检索行（三下拉+产业级联+关键词+搜索重置） | index.vue 检索块 | ✅ |
| 2 | 上一位/下一位翻页 + 计数（filteredIndex/库内共 N 人） | index.vue goFiltered | ✅ |
| 3 | 🔔 我的订阅（Badge）+ 订阅/取消订阅切换 | index.vue toggleSubscribe | ✅ |
| 4 | 管理员开关（治理写回显隐） | index.vue isAdmin | ✅ |
| 5 | 评估跳转（navigateToRecommend） | index.vue goRecommend（route query talentId） | ✅ |
| 6 | 导出 Excel/PDF 下拉 + 领域图谱报告 | index.vue exportProfilePdf + fieldMapRef.exportPdf | ✅ |
| 7 | 批量导入 Modal（模板下载+Upload 本地解析） | index.vue importOpen + importCustomRequest | ✅ |
| 8 | 7 Tab（SUB_TABS 冻结） | PageTabFrame | ✅ |
| 9 | Tab1 基础画像（信息卡/Timeline/仪表/雷达/统计/治理） | ProfileBasicPanel + Governance | ✅ |
| 10 | Tab2 关联画像（Alert/检索/四视图/溯源详情） | ProfileRelationPanel | ✅ |
| 11 | Tab3 分析画像（图表族/相似学者/趋势/评估入口） | ProfileAnalysisPanel | ✅ |
| 12 | Tab4 近期成果（四模式/推送/详情/全屏） | ProfileRecentWorksPanel + WorkCard | ✅ |
| 13 | Tab5 合作网络（graph/钻取/聚合/同步/推荐/溯源） | ProfileNetworkPanel | ✅ |
| 14 | Tab6 领域图谱（NLP banner/演化/词云/详情/钻取） | ProfileFieldMapPanel | ✅ |
| 15 | Tab7 荣誉奖项与国际合作 | ProfileHonorsPanel | ✅ |
| 16 | SubscriptionDrawer（通知流/跳转/退订） | SubscriptionDrawer | ✅ |

### 7. 需规对照（SCI-INT-A14 seq 277–304，28 叶）

| seq | 需求项 | 落点 | 状态 |
|---|---|---|---|
| 277 | 基础画像·信息展示方式 | ProfileBasicPanel 信息卡族 | ✅ |
| 278 | 基础画像·搜索与筛选 | index.vue 检索行（talentMatchesKeyword） | ✅ |
| 279 | 基础画像·基础信息校验与更新 | Governance 智能校验+更新提醒（演示态写回） | ✅ |
| 280 | 基础画像·数据安全与隐私保护 | Governance 权限管控+加密处理块 | ✅ |
| 281 | 基础画像·导入与导出 | Governance 导入导出 + 页头 Excel/PDF/批量导入 | ✅ |
| 282 | 基础画像·用户互动 | Governance 反馈订阅 + SubscriptionDrawer | ✅ |
| 283 | 关联画像·关联数据展示 | ProfileRelationPanel 列表/树/图谱/标签云 | ✅ |
| 284 | 关联画像·智能检索与筛选 | SEMANTIC_EXPAND 语义检索（1307 missing 标注） | ✅ |
| 285 | 关联画像·关联关系挖掘 | 隐含关系发掘 + latentLinks | ✅ |
| 286 | 关联画像·可视化图谱操作 | graph 视图节点聚焦/缩放 | ✅ |
| 287 | 关联画像·数据溯源与详情展示 | 右侧详情 + changeLog Timeline + sourceUrl 外链 | ✅ |
| 288 | 分析画像·多维度分析展示 | ProfileAnalysisPanel 图表族（DEEP_162 ⓘ） | ✅ |
| 289 | 分析画像·智能筛选与比较 | 领域 scope 过滤 + 相似学者匹配排序 | ✅ |
| 290 | 分析画像·人才引进评估 | goRecommend 跨页入口（FE-TA-04A 完整形态） | ✅（入口） |
| 291 | 分析画像·可视化操作支持 | 图表交互（tooltip/legend/dataZoom） | ✅ |
| 292 | 分析画像·交互与报告输出 | exportProfilePdf 专用打印页 | ✅ |
| 293 | 近期成果·成果信息分层展示 | RecentWorks 四模式 + ProfileWorkCard | ✅ |
| 294 | 近期成果·可视化操作 | 类目网格/时间轴切换 + 全屏 | ✅ |
| 295 | 近期成果·智能推送与动态更新 | 推送区（1318 missing 标注，不承诺实时） | ✅ |
| 296 | 近期成果·成果详情与原文链接 | 详情抽屉 + sourceUrl（1319 missing 标注） | ✅ |
| 297 | 合作网络·合作关系可视化展示 | ECharts graph force + roam | ✅ |
| 298 | 合作网络·图谱交互操作 | 节点点击/聚焦放大/高亮邻域 | ✅ |
| 299 | 合作网络·智能发现与动态刷新 | 推荐合作者 + 18s 同步（onBeforeUnmount 清理） | ✅ |
| 300 | 合作网络·合作详情与溯源 | 关系历史 Timeline + edge 详情 | ✅ |
| 301 | 领域图谱·研究领域分层展示 | 主领域/方向/技术标签三层 | ✅ |
| 302 | 领域图谱·可视化操作与交互 | 演化面积图 + 词云 + 详情 graph 钻取 | ✅ |
| 303 | 领域图谱·智能挖掘与趋势分析 | NLP 抽取 banner + 匹配列表（GRAPH_110 ⓘ） | ✅ |
| 304 | 领域图谱·详情展示与溯源 | 领域详情弹窗 + 溯源链接 + 报告导出 | ✅ |

## 测试结果（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0（0 错误）
- `node src/views/talent/talent.test.mjs`：`FE-TA-S01 + FE-TA-01A + FE-TA-02A + FE-TA-03A + FE-TA-04A ok`（第 12 节新增画像页 9 组断言：组件齐备/模型/接线/语义检索锚点/D9 挂点/网络钻取/WorkCard 封装/领域导出/治理演示态）
- `pnpm build`：✓ built in 24.68s

## 顺带修复（recommend 目录存量类型错误，FE-TA-04A 前会话遗留）

type-check 门被 04A 存量错误挡住，一并修齐（非 03A 范围但同模块门禁）：

- `DifficultyTab.vue`：`FACTOR_LABELS[key]` 等对象字面量索引（factorLabels/factorMissing/factorNums 三 Record 收口）+ `selectAlertStrategies` never[] 参数（`as unknown` 桥接）+ COOP_COLUMNS `TableColumnData[]` 类型 + row-key 签名
- `CostTab.vue`：`SCHEME_PRESETS.A` 结构子类型收窄（SchemePreset 别名）
- `DueDiligenceReport.vue`：风险行二维数组 `[string, string][]` 断言
- `ReportTab.vue`：batchQueue 谓词收窄 + `button-props` padding（移除，Arco ButtonProps 无此属性）
- `TalentComparePanel.vue`：两两循环非空断言（`!`）+ 删除恒真 emit 守卫
- `recommend/index.vue`：handleTalentSelect 联合类型补 `unknown[]`
- `DueDiligenceReport.vue` + `ReportTab.vue`：`DEFAULT_DIMS` 两处重复 → 上提 `dueDiligenceReportExport.ts` 导出 `DUE_DILIGENCE_DEFAULT_DIMS`（第二处出现即封装）；顺带修 build 阻断（defineProps 默认值引用本地变量提升问题）

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链（前端只调 Java REST / mock 双轨） | ✅ defineApi 双轨，无越层 |
| D8 Design token / Arco 优先 | ✅ 全 Arco 组件，无原生控件回退 |
| D9 指标 8 件套 + 四维 | ✅ 3 指标 + 5 missing + 9 升结构，不伪闭合 |
| D10 交互规范 | ✅ 键盘可达（a-* 语义）、Teleport 弹层 |
| 可观测埋点 | ✅ trackTalentInteraction（traceId） |
| mock 种子冻结 | ✅ talentSeed 与 demo data.js 逐行一致（自检 §2） |
| 写操作演示态 | ✅ 不替 BE 拍板 |
| 完工停本地 | ✅ 未 commit/push，等人工验收 |

## 遗留风险

1. **图表容器高度**：7 Tab 切换经 PageTabFrame 懒加载，图表均显式高度（避坑 §5.2 init 0 高死锁）；但**浏览器实测截图对照未做**（本会话无浏览器环境），建议人工走查 7 Tab 逐一目检。
2. **语义检索 1307**：当前为 demo 同义词扩展演示，SRS seq 284 `algorithm_type: UNKNOWN`；确认后须换真检索接口（挂 Java REST）。
3. **合作网络 18s 同步**：为 mock 权重轻抖动（`edgeBump`），真实链路应对接成果增量接口（代码注释已标 ponytail 天花板）。
4. 上次会话遗留的 `talent.value[0]!` 非空断言依赖「mock 种子必有 ≥1 条」前提（模板 loading 兜底）；真数据接入时若空集需补空态页。

## 走查修正记录

### 走查 1（2026-10-21 09:53，孔东）：领域图谱 Tab 两处

1. **匹配度进度条 `9900%`**：根因是 Arco `a-progress` 的 `percent` 语义为 **0–1 小数**（antd 为 0–100，Arco 源码 `text = percent × 100`、bar 宽 `percent × 100%`），demo 值直接照抄导致。**全 talent 模块同源 bug 一并修复**（12 处 ÷100）：画像页 5 处（FieldMap 匹配度+置信度 / Analysis 影响力 / BasicPanel 影响力条 / Governance 准确度 / Honors 公众指数）+ 推荐页 6 处（Compare 协同 / Contribution 增益 / Cost 占比 / ContributionMatch 五维 / DueDiligence 评分 / ReportTab 维度）+ Difficulty 阻力评分；Difficulty 的 antd `format` → Arco `#text` 插槽（顶层组件无 format prop，原 `:format` 是死代码）。教训已沉淀复刻经验清单 §1。
2. **技术标签样式对齐**：Arco `a-tag` 默认 24px 定高 / 2px 圆角（antd Tag 自适应高 / 4px 圆角），在 `demo-talent-profile.css` `.tl-tp-nlp-tags .arco-tag` 加等价尺寸覆盖（`height:auto; min-height:22px; line-height:20px; padding:0 7px; border-radius:4px; white-space:nowrap`）。教训同步沉淀。

修正后三绿复测：type-check 0 错 / talent.test.mjs ok / build ✓ 21.16s。

**双仓 commit + push dev（2026-10-21 10:06 用户放行「双仓commit、push dev」）**：
- pc `3f07ea6` fix(talent): FE-TA-03A 走查修正 a-progress percent 语义与 a-tag 尺寸对齐（16 文件，+108/−25）
- 编排 `8673ec2d` docs(talent): FE-TA-03A 走查修正记录与复刻经验追加

## 产物清单

- 代码（本地未提交，等验收）：`src/views/talent/profile/`（index + 10 组件）、`src/views/talent/models/profileRelation.ts` / `profileMetrics.ts` / `profileReportExport.ts` / `fieldMapReportExport.ts`、`src/views/talent/styles/demo-talent-profile.css`、`src/views/talent/talent.test.mjs`（第 12 节）
- 自检：`node src/views/talent/talent.test.mjs` → ok
- 本 handoff
