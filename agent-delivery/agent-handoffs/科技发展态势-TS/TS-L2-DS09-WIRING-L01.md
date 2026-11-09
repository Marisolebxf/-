# Frontend handoff：TS-L2-DS09-WIRING-L01

- 时间：2026-11-06 · **执行**：agent:zcode 会话代跑 frontend-agent · **监管**：`human:王梓真`（派单：coordinator）
- 仓库：`lumen-ui-science-pc`（分支 dev，**本地 commit 未 push**——派单明令禁止 push；完工即推条款本单按派单覆盖）
- commit：**`d4a5200`** `[agent:frontend-agent] feat(planning): DS-09 后端接线 10 GET+1 PUT、G-B4 哈希兜底移除与 501/导出任务中心（TS-L2-DS09-WIRING-L01）`（3 files，+988/-66）
- 覆盖功能点：DS-09 三页签前端接线（09a 综合 178–184 / 09b 重点领域 185–190 / 09c 研究分析 191–196）
- **图**：`TS-DS09-OV-CALLCHAIN-01`（OV-ARCH 稿 §2）——**接线不改变调用链拓扑，直接引用并声明**：前端 → 网关 `/display/v1/situation/planning/**`（StripPrefix=1）→ PlanningController → PlanningQueryService 只读 ADS（`ts_plan_*` 28 张）/ 订阅面走既有 SubscriptionPushJob + upms Feign；direction-warnings 过模型注册门（未注册 501）。本单仅把前端从「单聚合端点」改为同前缀多端点并发，仍全部经网关单入口（D15），无新增层级/无 demo-* 旁路。
- 输入真源：OV/KEY/RES 三份 API 分册 v2（FE 接线差异清单）+ TS-L2-DS09-IMPL-JAVA-L01（端点实际路径与 DTO 形状，**以 Java 实现为准逐字段核对**）+ TS-L2-DS09-SEED-L01（库内 375 行已就绪）

---

## 1. 范围与实现（对照 DoD 逐条）

| # | DoD | 实现 |
|---|---|---|
| 1 | `techDevelopmentPlan.ts` real 分支：单端点 → 10 GET + 1 PUT，组装回 dataset 既有键 | `src/api/situation/techDevelopmentPlan.ts` 全量重写 real 分支：`fetchDirectionWarnings()`（501 通道独立）+ `Promise.all` 并发 9 组（hot-technologies ×3 range / metric-system / talent-flow / resource-push / subscriptions GET / key-areas / research-analysis）+ `Promise.allSettled`（tracking / local-advantage，见偏离 1）。映射：OV 9 端点块 + key-areas 平铺 9 块 + research-analysis 12 块 → `TechDevelopmentPlanDataset` 全部既有键（snake_case→demo 键名映射逐条对三份分册 §6/§7 映射表）；R 信封经 `optionalGet`/`unwrap` 解包（code=0 取 data）；路径 `/display/v1/situation/planning/*`（BASE 常量，对齐仓内 real 先例）；`defineApi` id `tsTechDevelopmentPlanDataset` 不变；新增导出 `updatePlanningSubscriptions`（PUT，唯一写面，.vue 冻结期无调用点）。端点未上线（404/405/501）→ 该块诚实空态；其余错误照常抛出（整页错误态=保持单端点期行为）；183 两端点 401/403 → 个人块空态（未登录无个人推送数据，不伪造默认清单） |
| 2 | model 移除哈希造数兜底（G-B4）+ 系数读响应 + od_nodes + 本地优势响应行 | `models/techDevelopmentPlanModel.ts`：① **`getDeterministicOverlap` 整函数删除**；`getPairOverlapCompute` 无真值对返回 `overlap/base=null` + 显空文案 `—（暂无重叠数据）`（新常量 `OVERLAP_EMPTY_TEXT`）；`buildCompanyOverlapSummaries` 均值分母仅含有值对（与后端 `competing_enterprises.avg_overlap` 同口径），空对溯源文案进 tooltip。② 复算系数：`overlapTimeScopeFactor` ← time_scopes（近1年 0.82/近3年 1/近5年 1.12）、规则三档阈值 ← overlap_rules（strict 75/60/59…），api 层从响应块填充 dataset，model 无写死阈值/系数。③ 人才 OD：`buildTalentOdOption` 把桑基链路 target **重锚**到节点表实际标签（节点名由 `od_nodes` 组装 `深圳\|18,932人\|↑21.7%` demo 形态）——写死 18932/12458 的展示值闭合在响应数据侧；mock 轨道种子标签与冻结链路一致 → 行为逐字节不变。④ 本地优势两补充维度：**受契约缺口阻塞**，见偏离 2 |
| 3 | 184 预警 501：空态 + ⚠️ 未注册 + 导出入口禁用 | api `fetchDirectionWarnings`：HTTP 501 → `directionMonitorItems=[]` + `directionMonitorSources=[]`（六源均分条不显伪 0 卡）+ `setDirectionAlertStatus('unregistered')`；200 → 'registered'；404/405 → 'unknown'。model：`buildDirectionMonitorReport` 在未注册态正文头部插入「⚠️ 预警模型未注册：M_INNOV_PLAN_DIRECTION_ALERT 尚未上线（赋号草稿·未签）。预警区暂无数据，报告导出入口已禁用。」；Word 导出对 `content_key=planning-direction-warning` 且未注册时功能性拒绝（Message.warning，任务中心同闸 501 亦拦截）。前端只按 HTTP 状态码判定，不解析 msg 文案（OV-API §3.1） |
| 4 | 195 报告下载改走导出任务中心 | model `downloadHtmlAsWord` 双轨：USE_MOCK=true → demo 逐字 Blob（轨道完全不变）；real → `runPlanningReportExport`：`POST /display/v1/situation/export/jobs` `{format:'doc', content_keys:[key], filter:{title}}` → job_id → 2s×15 轮询 `GET .../jobs/{job_id}` → success 取 `file.url/download_url` 触发浏览器下载，failed/超时诚实提示。**端点 404/405 → 「导出服务未就绪：报告导出任务中心尚未上线」，不回退 FE Blob 旧通道（已废弃）**。content_key 按报告标题解析（184=planning-direction-warning / 195=planning-research-intelligence）。PDF 沿浏览器打印（printHtmlAsPdf 不动） |
| 5 | 🧪 MockBadge 保留 / ⓘ draft 语义卡不动 | 本单零 .vue / 零 mock 模块 / 零 types 改动（git diff 证实仅 2 个接线文件 + 1 个测试文件），角标体系原样 |
| 6 | 自检 | 见 §4 验证证据 |

## 2. 偏离与注记（逐条登记，不改契约）

1. **tracking / local-advantage 取回不映射**：当前 .vue 冻结范围无 timeline/spatial/维度级渲染点（OverviewTab 未移植 demo 研判演进时间轴/空间点位区；`TechDevelopmentPlanDataset` 无对应槽位）。两端点已请求（tracking 裸调默认参数、local-advantage 全量），结果占位不映射、失败经 `allSettled` 吞掉不拖垮已消费块；.vue 解冻补渲染时在 `buildRealDataset` 挂映射。
2. **本地优势三图 + 热度口径三卡保持 demo 冻结种子**（派单项「两补充维度由响应行提供」**受阻**）：local-advantage 响应为维度级标量（`dimensions[].items[]` 子项序列属 OV-API §7-5 批 4 建议未冻结；IMPL-JAVA §4-6 明确「不擅自加块，FE 三块图表保持 mock 种子的会签点沿袭」）；热度口径三要素无 DTO 字段（§7-7）。种子经 `@/mock/modules` import + 显式 TODO 标注（OV-API §6「显式 TODO 二步接线」原文授权）；批 4 冻结后替换。
3. **趋势三窗序列改由 hot-technologies ×3 range 组装**（超出 OV-API §6 行的字面「保持冻结种子」）：该行依据「heat_series 是按技术年度序列」已陈旧——S-1 会签后序列表按 range_key 分区（128 行=8 技术×3 窗），后端已实现 range Query。以真端点供数比保留种子更诚实（种子序列与库内序列同源，视觉零漂移）。
4. **501 的 ⚠️ 角标与导出入口「禁用」落点受限**（.vue 零改动约束）：预警卡片区无数据槽位（六源条/预警行均为空态），⚠️ 文案落在报告 Modal 正文（生成报告仍可打开，内容诚实）；导出禁用 = Word 通道功能性拒绝 + 诚实提示，按钮视觉 disabled 态需 .vue 解冻（孔东锁至 2026-11-12）。.vue 的 `Message.success('Word 报告已开始下载')` 在导出未就绪时会先于降级提示出现（冻结无法移除，降级 Message 紧随其后）——解冻项。
5. **companies 展示位 id 重排 shim**：ResearchTab 冻结硬编码 `selectedCompanyIds=['1','2']`，real 的 `company_id`（C-01…）不匹配 → api 层按响应序（sort_no ASC）给 compare 行赋 '1'..'N'（名称为业务键，mock 种子序一致=华为+腾讯入象限语义保持）。target 行不入 companies（对齐 demo 种子形态，其在 graph 节点/报告目标位承载）。
6. **模块态注入 shim**：`setDirectionAlertStatus` / `setResearchGraphCategoryLabels` 为模块态（.vue 冻结期页面无数据槽位/参数透传通道），api real 分支注入、mock 轨道不经过 → 默认值= demo 行为不变；解冻后改参数传入。图谱图例 real 轨道对齐响应 categories（企业/机构/技术领域/文献/**专利**，专家→专利勘误，RES-API §6-5），mock 轨道保持 demo 冻结五类（轨道不变）。
7. **195 导出 filter 参数面最小实现**：任务中心后端未实现（IMPL §6-1 已知缺口），filter 仅 `{title}`；job 轮询 file 字段按 M1 §3.8（`file.url/download_url`）防御式读取。后端落地联调时如参数面调整，仅改 `createPlanningExportJob`。
8. **测试文件更新**（超出「两文件+新增测试」字面）：既有 `techDevelopmentPlan.test.mjs` 断言「模型应保留确定性兜底函数」与 G-B4 DoD 直接冲突、且 `mockSource` 既有未使用 lint 报错——最小翻新（哈希断言反转 + G-B4/接线/轨道不变新断言 + mockSource 用于种子保持断言），否则自检必红。

## 3. 产物清单（commit d4a5200）

- `src/api/situation/techDevelopmentPlan.ts`：real 分支全量重写（10 GET + 1 PUT 组装 + 501 通道 + 401 个人块空态 + 响应形状接口与块映射）
- `src/views/situation/tech-development-plan/models/techDevelopmentPlanModel.ts`：G-B4（哈希兜底删除/均值仅有值对）、OD 重锚、图例注入、501 注册态 + 报告 ⚠️、Word 导出双轨改任务中心
- `src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs`：陈旧断言翻新 + 新增接线断言
- **零改动**：全部 .vue / `src/mock/**` / `src/types/**`（类型未扩展，dataset 既有键完全复用）

## 4. 验证证据

- `vue-tsc --build` → **EXIT=0**（pnpm type-check 绿）
- `node --experimental-strip-types src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs` → **全绿**（种子一致性 + 接线 + 视图结构 + G-B4 + 导出任务中心 + 轨道不变性）
- 仓内相关 .test.mjs 复跑不红：innovationEvaluation（42 项）/ maintain / techIndex（55 项）/ FE-POL-SENT-LIVE（honestEmpty 引用方）
- eslint 三文件 → **LINT_OK**（含顺手修复的既有 mockSource 未使用报错）
- 未跑：CI / K8s dev（commit 未 push，按派单禁 push；后端 lumen-svc-platform 亦未部署——real 轨道上线前各块诚实空态，联调待两端合流）

## 5. 架构合规自检（§2 铁律逐条）

| # | 项 | 结论 |
|---|---|---|
| 1 | 调用链（TS-DS09-OV-CALLCHAIN-01 拓扑不变） | ✅ 全部经网关 `/display/v1/situation/planning/**` 单入口（D15/铁律 9 拼接）；不直调 Python、不碰 demo-*（D12）；无越层 |
| 2 | D18 无 FE 造数 | ✅ G-B4 哈希兜底移除（无真值对显空）；reason/match/evidenceSource/name/avatar 等无契约来源字段置空不造数；空态诚实（空数组，未登录个人块空态） |
| 3 | 501 语义 | ✅ 仅 184；只按 HTTP 状态码判定不解析 msg；501=通道态非覆盖证明；导出同闸（未注册功能性禁用 + 任务中心 501 拦截） |
| 4 | 195 导出 | ✅ 走 M1 §3.8 任务中心（建任务→job_id→轮询）；FE Blob 旧通道 real 轨道废弃不回退；任务中心未上线诚实降级 |
| 5 | D9 | ✅ 🧪 MockBadge / ⓘ draft 语义卡零改动（D4 仍 mock，角标保留至翻转） |
| 6 | USE_MOCK 轨道 | ✅ 完全不变（Blob/冻结图例/种子/mock 注册原样；模块态默认值= demo 行为，测试断言覆盖） |
| 7 | 可观测性 | ✅ index.vue 既有 traceId/埋点零改动；降级路径 console.warn 留排障依据 |
| 8 | 交付边界 | ✅ 未 push（派单禁令）；未改 task-registry；未动 .gitignore/package.json；仅 2 接线文件 + 1 测试文件 |

## 6. 待下游 / 解冻项

1. **M1 §3.8 导出任务中心后端实现**（IMPL §6-1 阻塞延续）：落地后 FE 零改动即通（或按实际参数面微调 `createPlanningExportJob`）。
2. **批 4 冻结**：§7-5 `dimensions[].items[]`（本地优势三图换真源）、§7-7 热度口径三卡、§7-6 records[].reason——冻结后替掉对应 TODO 种子保留。
3. **.vue 解冻（2026-11-12 后）**：预警卡 ⚠️ 角标与导出按钮视觉禁用；推送设置 Modal 接 `updatePlanningSubscriptions`；`talentFlowData` 个人卡降级形态（孔东会签点）；tracking/local-advantage 渲染；companies id shim 与模块态注入改参数化；移除导出前的假成功 Message。
4. **网关 501 透传核验**（OV-API §9-6 遗留）：部署联调时确认（当前 FE 只按状态码判定，若网关改写 501→500 会落入整页错误态而非预警空态——上线前必须核）。

## 7. cost 估算与 ponytail 自检

- **cost 估算**：actual_tokens ≈ 620K（含三份分册/两份 handoff/后端 Java 实现全量精读），model=GLM-5.3-Highspeed，actual_cost ≈ $3.5，cost_warn=**green**（<$10）。cost 字段回填留 coordinator（派单纪律）。
- **ponytail 自检行**：产物=3 文件单 commit（d4a5200）+ 本 handoff；无仓外散落；.vue/mock/types 零改动（git diff 证实）；USE_MOCK 轨道逐字节不变（测试断言）；无第二套统计口径（均值/系数/阈值全读响应或后端）；偏离 8 条逐条登记如上；未 push（本地 dev）。

---

## 8. 解冻项完成记录（2026-11-06 · 孔东 2026-11-09 放行 .vue，经监管人 human:王梓真 转达）

- **commit**：`6c09d5c` `[agent:frontend-agent] feat(planning): DS-09 六项 .vue 解冻收尾——501 角标/导出禁用、PUT 写面、shim 转正（TS-L2-DS09-WIRING-L01）`（6 files，+222/-75，本地未 push）
- **改动面**：`src/types/techDevelopmentPlan.ts`（3 个 lumen 补充可选槽位）/ `src/api/situation/techDevelopmentPlan.ts` / `models/techDevelopmentPlanModel.ts` / `tabs/OverviewTab.vue` / `tabs/ResearchTab.vue` / `techDevelopmentPlan.test.mjs`；**零改动**：`src/mock/**`、`styles/**`、`tabs/KeyAreaTab.vue`、`index.vue`（USE_MOCK 轨道种子逐字节不变）

### 8.1 六项逐项落点

| # | 解冻项 | 落点 | 状态 |
|---|---|---|---|
| 1 | 预警卡 ⚠️ 角标与导出按钮视觉禁用 | OverviewTab：预警卡 title ⚠️ 角标（a-tooltip+tzp-card-info-icon 先例形态，aria-label 无障碍）+ 报告 Modal 正文顶部 ⚠️ 行 + footer「下载 Word」视觉 disabled（span 包 native title；PDF 沿浏览器打印不受模型闸门约束）；「生成报告」仍可打开（内容诚实，沿偏离 4 决策）。注册态消费 `dataset.directionAlertStatus ?? 'unknown'` | ✅ |
| 2 | 移除导出前假成功 Message | OverviewTab/ResearchTab 两处 `Message.success('Word 报告已开始下载')` 改 `if (USE_MOCK)` 分支保留（demo 冻结 Blob 同步下载的既有提示，轨道不变）；real 轨道无抢跑——任务中心流程自带 info/success/error 提示 | ✅ |
| 3 | 推送设置 Modal 接 updatePlanningSubscriptions | OverviewTab `handleSavePushSettings` 双轨：USE_MOCK=true 保持 demo 本地提示（轨道不变）；real 乐观更新（表单值即目标态 + 保存按钮 loading）→ PUT `{resource_types, fields, frequency}` 全量小对象（resource_types 为 GET 原值，经 `defaultPushSettings.resourceTypes` 新槽位回传，防全量提交清空）→ 失败回滚打开 Modal 时的表单快照（`pushSettingsSnapshot`，watch showPushModal 拍照）+ `Message.error` 诚实提示 + console.warn 留排障 + Modal 不关 | ✅ |
| 4 | talentFlowData 个人卡降级「机构对」 | **判定为 FE-TS-09A 复刻缺口关联项，不在本单新建 UI**（见 8.2 判定 A）。数据侧机构对形态已在 d4a5200 闭合（api 映射 name/avatar 置空不造数 + from/to 机构对 + 类型/领域/风险位全真值）；孔东放行即认可此形态，api 注释已收口 | ✅（判定登记） |
| 5 | tracking / local-advantage 渲染 | **tracking 判定为 FE-TS-09A 复刻缺口**（见 8.2 判定 B），不新建 UI，api 占位 allSettled 维持；**local-advantage 三图槽位存在**（本地优势卡 localAdvantageOption），但响应为维度级标量、`dimensions[].items[]` 批 4 未冻结（偏离 2 会签点沿袭）→ **维持 demo 冻结种子**，api 注释更新判定结论 | ✅（判定登记） |
| 6 | shim 转正 | ① companies id 重排 shim 删除：api 用响应真值 `row.company_id`；ResearchTab 冻结硬编码 `['1','2']` 改 `computed(() => companies.slice(0, 2).map(id))`（本 Tab 无选中态修改 UI，纯派生；mock 种子序=华为+腾讯 → ['1','2'] 行为不变，real 响应序 sort_no ASC 同语义）。② 模块态注入删除：`setDirectionAlertStatus`/`getDirectionAlertStatus`/`setResearchGraphCategoryLabels` 全删，注册态与图例经 dataset 正规通道（`directionAlertStatus`/`researchGraphCategoryLabels` 可选槽位），`buildDirectionMonitorReport(…, alertStatus)` / `buildResearchGraphOption(nodes, categoryLabels)` / `downloadHtmlAsWord(…, options)` 参数消费；顺手转正 model 注释承诺的「调用方显式传 content_key」（`ReportExportOptions`，文件名解析降级为缺省兜底） | ✅ |

### 8.2 复刻缺口判定链（第 4/5 项，留孔东决策）

- **判定 A（talentFlowData 个人卡）**：demo 源码核实（demo-ui-science/src/TechDevelopmentPlan.tsx）——`talentFlowData` 的全部消费链 = `selectedTalentFlowId` state（L1070）→ `selectedTalentFlow`（L1671）→ `buildOverviewExportPayload`（L1708-1714），而 `handleGenerateOverviewExport`（L1719）**在 demo 全文无 UI 调用点（死代码）**；`avatar` 字段仅存在于类型（L94）与种子（L569-575），无渲染点；机构 TOPS 行点击（L2897）只 setSelectedTalentFlowId，lumen 复刻时该点击只做 track 埋点。⇒「个人卡」在 demo 与 lumen **均无 UI 渲染槽位**，按派单纪律（不新建 UI）登记缺口：若后续要落「机构对」明细展示，需孔东确认形态后补 FE-TS-09A 复刻（数据面已就绪）。
- **判定 B（tracking）**：demo 全文 grep「时间轴/演进/点位」零命中——demo 本就没有研判演进时间轴/空间点位区，180 tracking 端点为 lumen 后端新增（数据已就绪、FE 无槽位）。⇒ 登记为 FE-TS-09A 复刻缺口（严格说是 demo 无此区块的**新增 UI 待定义**，非复刻遗漏；留孔东定义形态）。api 层占位请求保持 `allSettled` 不拖垮页面（偏离 1 沿袭）。

### 8.3 验证证据

- `vue-tsc --build` → **EXIT=0**
- `node --experimental-strip-types src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs` → **全绿**（种子一致性 + 接线 + 视图结构 + 新增解冻收尾断言组：模块态 shim 删除断言反转 / dataset 正规通道 / ⚠️ 角标与 Word 禁用 / 假成功 Message 仅 USE_MOCK 分支 / PUT+快照回滚 / 复刻缺口登记 / id 真值 + 前两家派生；轨道不变性断言全部保持）
- eslint 6 个改动文件 → **LINT_OK**（顺手清除 ResearchTab 既有未使用 import `cascadeDisplayLabel`——.vue 冻结期未跑过 eslint 的存量问题）
- 仓内相关 .test.mjs 复跑不红：innovationEvaluation（42 项）/ maintain / techIndex（55 项）/ FE-POL-SENT-LIVE
- USE_MOCK=true 轨道不变性论证：mock 模块/样式/KeyAreaTab/index.vue 零改动；model mock 分支（Blob/冻结图例五类）逐字未动；OverviewTab 角标/禁用/⚠️ 行均 `v-if` 未注册态（mock 种子无 `directionAlertStatus` → unknown → 全不渲染）；Word/推送假成功提示保留在 USE_MOCK 分支；`selectedCompanyIds` 派生值在 mock 种子下等价 `['1','2']`
- 未跑：CI / K8s dev（本地 commit 未 push，按派单 push 由 coordinator 统一执行；后端 lumen-svc-platform 未部署——real 轨道上线前各块诚实空态）

### 8.4 cost 增量（解冻段，累计至全单）

- 解冻段 actual_tokens ≈ 350K（含 handoff/规约/全部源文件/demo 源码对照精读 + 6 文件编辑 + 三绿验证），model=GLM-5.3-Highspeed，actual_cost ≈ $2.0，cost_warn=**green**
- 全单累计（d4a5200 + 6c09d5c）：actual_tokens ≈ 970K，actual_cost ≈ $5.5，cost_warn=**green**（<$10）。cost 字段回填仍留 coordinator（派单纪律）
