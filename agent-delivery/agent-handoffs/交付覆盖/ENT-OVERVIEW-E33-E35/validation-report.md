# ENT-OVERVIEW-E33-E35 validation report

## 当前结论

用户于 2026-07-14 明确指示“跳过任务认领，后续补，先开始编码”。本轮已在 `repos/demo-ui-topic/dev@e287e91` 基线上完成 E-33～35 首轮实现；14 个覆盖项均为 `implemented`。生产构建、设计契约和本批静态契约通过，视觉截图与逐态浏览器复核尚未完成，因此暂不标记 `verified`。

## 基线核对

- 定义仓：`gkx-orchestration/dev@9f4d4e8`，与 `origin/dev` 对齐。
- Demo 仓：`repos/demo-ui-topic/dev@e287e91`，与 `origin/dev` 对齐，工作区干净。
- E-32 已在同一 Demo `dev` 历史中，本批 E-33～35 将在该基线上延续企业总览壳层与视觉规范。
- `gkx-orchestration` 原有两个已修改文档及 `p2a-session/` 不属于本次写集，保持不动。

## 门禁与授权核对

| 项目 | 当前状态 | 结论 |
| --- | --- | --- |
| ENT-MOD-KEYPANO-PACK-L01 | review | 尚未完成门 1 通过登记 |
| ENT-MOD-STAR-PACK-L01 | review | 尚未完成门 1 通过登记 |
| ENT-MOD-SHENZHEN-PACK-L01 | review | 尚未完成门 1 通过登记 |
| ENT-MOD-OVERVIEW-PDR-G1 | blocked | P0 阻塞 Demo 编码 |
| ENT-UE-IA-L04 | blocked / Legacy | 不可作为当前实现认领依据 |

本次编码依据用户显式授权先行，任务认领与门 1 登记作为后补事项，不在本轮伪造或倒填。

## 已落地范围

### E-33

- 支持权威 query `key-enterprises`，并保留兼容 key/legacy 路由。
- 移除企业总览 E-33～35 顶部全局筛选条；共享上下文改为页面内只读摘要或轻量局部切换，并保留当前产业链与数据时间。
- 实现链位选择、右侧最多 3 家代表企业、全部企业 Drawer 与企业画像入口。
- 规模统计统一为外企、国高企、小微、上市及国/省/市三级，并提示多标签不可求和。
- 移除竞争力分，补充论文/专利关键词、映射覆盖率、证据摘要与证据不足态。

### E-34

- 移除明星企业自由选择，改为当前产业固定一家。
- 增加入选理由、标准版本和只读入选标准 Drawer。
- 增加视频、3D 模型、行业案例和操作演示的评审/演示双模式。
- 增加技术原理、科研成果、人才比例、团队成果、生态关系摘要、发展历程和公开口碑。
- 按 `Design.md §1.1` 不展示企业 Logo，仅以企业名称和业务字段识别对象。

### E-35

- 固定深圳地域并以八大未来产业组织全页。
- KPI 补充国有企业数，移除无正式依据的同比百分比。
- 增加八产业数量对比、单产业领域聚焦、映射覆盖和趋势有效点判断。
- 规模分析改为“八产业 × 大型/中型/小型/微型”堆叠结构。
- 移除需求外行政区地图与竞争力分；重点企业改为按产业分组卡片。
- 增加企业性质、统一资质荣誉、CMS 定位/优势/专家观点和缺失空态。

## 样例数据检查

`http://111.198.38.90:50100/#/home` 于 2026-07-14 22:47（Asia/Shanghai）返回 HTTP 200，仅确认应用壳可访问；本轮没有建立可审计的 E-33～35 字段级映射。因此后续采用固定 seed `ENT-OVERVIEW-E33-E35-20260714` 的确定性模拟数据。内部溯源保留 `mock_20260714_e33_e35`，页面仅展示数据时间；评审信息使用 `DEMO / Q047~Q049`。

## 本轮检查

- `git branch --show-current` / `git rev-parse --short HEAD`：通过。
- `git status --short`：Demo 仓干净；定义仓原有用户改动已隔离。
- 四件套文件存在性与 TRACE/IA/USM/Wireframe 路由、字段、状态、排除项对照：完成。
- `node tests/enterprise-overview-e33-e35.test.mjs`：通过。
- `npm run design:check`：通过。
- `npm run build`：通过；Vite 仅报告既有大 chunk 警告。
- 三个权威 URL 经本地 Vite 服务返回 HTTP 200。
- `node scripts/check-enterprise-ia.mjs`：失败，失败点为既有“产业服务链分析 group 应包含 industry portal source pages”，与 E-33～35 写集无关。
- 浏览器截图与逐态视觉复核：未执行，保留为 manual review。

## 后续验证计划

1. 使用用户选定浏览器对三个权威 query 做逐态视觉复核并留存截图。
2. 修复或确认既有 `check-enterprise-ia.mjs` 产业服务链断言，再运行全量企业 IA 契约。
3. 补任务认领与统一门 1 登记，不倒填时间。

## 2026-07-15 E-33 浏览器评审迭代

- 当前产业链选择扩展为八大未来产业，每次仍只展示一条产业链；切换后重置链位与领域局部选中态。
- 上游/中游/下游调整为左侧竖排，企业列表扩展为右侧 9/12 栅格并增加首屏可见企业数量。
- 规模统计改为增量堆叠：深圳市、广东省其他、全国其他。由于国家/省/市是嵌套集合，不直接堆叠原始总量，避免重复计数。
- `node tests/enterprise-overview-e33-e35.test.mjs` 已新增对应静态契约。

## 2026-07-15 双模式可见性整改

- 归因结论：四件套已明确内部评审模式边界，主要问题为实现与验证遗漏；交付契约未强制记录 `visibility_by_mode`，属于流程放大因素。
- E-33～35 的 `MockBadge`、Q047～Q049、字段/接口依赖与实现口径统一改为仅在 `reviewMode` 下展示；原始 mock 批次从两种页面模式中完全移除。
- 业务态保留获批业务说明与可读数据时间；E-33 的“多标签不可直接相加”属于业务解释，保持常显。
- E-34 非评审媒体使用“示例演示内容”说明，不暴露原始 DEMO/CMS 接入字段；标准版本和关系摘要在业务态去除 DEMO 后缀。
- 契约测试增加双模式代码路径检查，要求评审信息由 `reviewMode` 控制；视觉层仍需分别截取业务态和评审态后才能标记 `verified`。
- 整改后复验：`node tests/enterprise-overview-e33-e35.test.mjs`、`npm run design:check`、`npm run build`、两仓 `git diff --check` 均通过；本地权威 URL 返回 HTTP 200。构建仅保留既有大 chunk 警告。

## 2026-07-15 数据时间语义统一

- E-33～35 四件套统一使用“数据时间 / `data_time`”，删除“数据批次 / `data_batch`”及批次化验收表述。
- 三个页面的业务态和评审态均只显示“数据时间 2026-07-14”；评审态 MockBadge 不再暴露内部 mock 批次。
- 内部 mock 批次仅保留在 `source-manifest.yaml` 的交付溯源数据中，不属于产品字段或页面文案。

## 2026-07-15 普通中文评审说明防泄漏整改

- 根因：上一轮只检查 MockBadge/Q/DEMO/mock 等显式标记，未把普通中文的来源说明、实现解释、口径约束、禁止行为和共享组件装饰纳入逐元素可见性清单。
- 新增共享 `ReviewOnly` 门控；E-33～35 的说明、来源、规则和排除项统一迁入该容器。
- `MetricCard` 在组件内部自动隐藏 MetricSpec、Mock、Pending 和无源标识，避免页面调用方漏传模式状态。
- 契约测试新增逐条 `ReviewOnly` 包裹检查，并覆盖用户标注的 7 类文案；视觉双模式复核完成前仍不标记 `verified`。
- 整改后 `node tests/enterprise-overview-e33-e35.test.mjs`、`npm run design:check`、`npm run build`、Skill `quick_validate.py`、交付 YAML 解析及两仓 `git diff --check` 均通过；三个本地权威 URL 返回 HTTP 200。

## 2026-07-15 企业画像来源面包屑修正

- 根因：企业画像已收到 `source=/enterprise-center/overview` 与新 `sourceTab`，但来源映射仍停留在旧 `key-objects/key/shenzhen` 规则，其中 `shenzhen` 还错误返回重点对象。
- 补齐 `overall`、`key-enterprises`、`star-enterprises`、`shenzhen` 四个企业总览来源，并同步修正兼容 `key/star` 映射。
- 从 E-33、E-34、E-35 进入企业画像时，第三层面包屑分别返回重点企业概览、明星企业介绍、深圳企业介绍，并保留对应 query Tab。
- 回归契约、设计检查和生产构建通过；构建仅保留既有大 chunk 警告。

## 2026-07-15 E-33 方案 A 定义落地

- 定义基线：E-33 四件套 `v0.2 / 2026-07-15`，采用“顶部当前产业链 + 左侧链路导航 + 右侧同屏联动工作区”。
- 顶部保留当前产业链选择器；八大未来产业链仍可单选切换。
- 左侧纵向展示上游、中游、下游，只保留链位名称、重点企业数和重点领域数，并使用可键盘聚焦的选中控件。
- 右侧企业改为单列列表，使用 Arco `Pagination`，每页 3 家；切换产业链或链位后回到第 1 页，翻页不改变产业链与链位。
- 右侧规模与资质图表继续使用整条当前产业链记录；链位切换只更新企业列表、领域摘要和关键词证据。
- 领域区只呈现当前链位证据，切换链位后默认选中该链位首个证据项。
- 删除旧“查看全部 + Drawer”企业浏览路径，不新增批量、导出、评估、风险或推荐能力。
- 数据策略不变：复用固定 seed 的确定性模拟数据，没有新增字段、指标公式或数据源。

### 本轮机器检查

- `node tests/enterprise-overview-e33-e35.test.mjs`：通过；测试先在旧实现上按预期失败，再由方案 A 实现转绿。
- `node scripts/check-enterprise-overview-chrome.mjs`：通过，3 项。
- `npm run design:check`：通过。
- `npm run build`：通过；仅保留既有大 chunk 警告。
- `http://127.0.0.1:4177/enterprise-center/overview?tab=key-enterprises`：HTTP 200。
- 评审文案审计：`MockBadge / Q047 / 数据时间 / 多标签与增量堆叠说明` 均受 `reviewMode` 或 `ReviewOnly` 门控；“当前链位暂无已发布重点企业”为冻结四件套明确的业务空态。

### 当前门禁

E-33 四项覆盖记录标记为 `manual_review`：当前环境未直接操控用户选定的 in-app browser，因此没有伪造业务态/评审态 DOM 与截图证据。用户在当前本地页面完成视觉复核后再升级为 `verified`。

## 2026-07-15 E-33 整链重点企业资质分布 v0.3 落地

- 定义基线升级为 E-33 四件套 `v0.3`；页面标题统一为“整链重点企业资质分布”。
- 原增量堆叠柱改为横向分组条形图，固定展示外企、国高企、小微、上市四行，以及深圳市、广东省、全国三个完整嵌套系列。
- 三个地域系列使用同一个绝对数量轴，不堆叠、不按行归一化；每根条形末端固定显示精确数量，零值保留为 `0`。
- 图表保持整条当前产业链口径且只读，不响应链位、分页或领域状态，不点击筛选企业列表。
- 两条业务语义提示常显：地域层级数量不可相加；资质为多标签计数、不可相加为企业总数。
- `DEMO / Q047` 仍由既有 `MockBadge` 在评审模式中展示，业务模式不暴露内部编号或替换计划。

### TDD 与机器检查

- RED：修改 `tests/enterprise-overview-e33-e35.test.mjs` 后，旧实现因缺少新标题与横向分组配置按预期失败。
- GREEN：`node tests/enterprise-overview-e33-e35.test.mjs` 通过。
- `node scripts/check-enterprise-overview-chrome.mjs`：通过，3 项。
- `npm run design:check`：通过。
- `npm run build`：通过；仅保留既有大 chunk 警告。
- `http://127.0.0.1:4177/enterprise-center/overview?tab=key-enterprises`：HTTP 200。

### 当前门禁

`E33-SCALE-QUALIFICATION` 保持 `manual_review`：当前环境未直接操控用户选定的 in-app browser，业务态/评审态 DOM 与截图证据尚未补齐；未伪标为 `verified`。

## 2026-07-15 E-33～E-35 页签级需求追溯补齐

- 新增共享 `ReviewTraceHeader / TraceInfoIcon`，组件内部读取全局 `reviewMode`；页面调用方只提供当前模块追溯元数据。
- E-33、E-34、E-35 均在页签内容首部挂载评审标题、来源锚点、源文档位置、原文摘要、当前落位和 TRACE / 开放项状态。
- TDD RED：专项契约首先因缺少 `ReviewTrace.tsx` 失败；GREEN：共享组件和三页挂载完成后通过。
- 双模式 DOM：三个页签评审态均为 `data-review-trace=1`、需求追溯入口 `=1`；业务态两者均为 `0`。
- 浮层复核：三个页签均可读到对应 E 编号、`bid-reference/智慧服务门户系统-要素相关.md` 和“企业总览 / 当前页签标题”落位。
- 截图证据：`/Users/ying/.codex/visualizations/2026/07/15/019f64c5-2efe-77e0-907d-f2c48214bf35/e33-{review,business}.png`、`e34-review-popover.png`、`e34-business.png`、`e35-{review,business}.png`。
- 机器验证：专项契约、`npm run design:check`、`npm run build` 和两仓 `git diff --check` 均通过；构建仅保留既有大 chunk 警告。
- 覆盖项 `E33-E35-REVIEW-TRACE` 具备静态、构建、真实 DOM 和双模式截图证据，状态记为 `verified`。

## 2026-07-15 E-33 评审内容逐元素门控补漏

- 根因：交付覆盖合同曾按“统计图表”和“领域证据”成组分类，没有把组内每段说明文案分别标注可见性，导致图表下方两条统计口径说明和领域证据的生成性摘要作为普通业务 DOM 渲染。
- 按用户浏览器批注新增交付覆盖：两条统计口径说明、`基于公开论文与专利关键词……` 生成性摘要均归为 `review_only`；业务模式保留图表、数值、关键词、覆盖率与关联企业。
- 页面统一通过共享 `ReviewOnly` 门控，不新增页面私有模式判断；契约测试增加三条精确包裹断言。
- TDD RED：新增断言后旧实现首先在“国家、省、市为嵌套统计范围……”处失败；GREEN：完成门控后专项契约通过。
- 本项仍保持 `manual_review`，待用户选定浏览器补修正后的业务态隐藏与评审态可见截图证据。

## 2026-07-15 E-34 多明星企业选择定义落地

- 定义基线升级为 E-34 四件套 `v0.2 / 2026-07-15`：每产业固定运营名单为 `0..N` 家，“固定表”不再解释为固定一家。
- 当前产业 0 家展示业务空态；1 家直接展示且隐藏选择器；2 家及以上使用 Arco `Select` 可搜索选择器并显示“当前产业共 N 家明星企业”。
- Demo 名单条目增加 `sortOrder`、`selectionTag`、`listPublished`、`basicIntroPublished`；只有名单条目和基础介绍均发布的企业进入候选集。
- 当前企业写入 `enterprise_code`；缺失或无效编码回退到当前产业 `sortOrder` 第一家并替换 URL。切换企业后清除媒体、标准和关系局部状态，并滚动回明星企业首屏。
- 选择项展示企业名称和一句公开入选标签；依据 `Design.md §1.1` 的高优先级企业标识约束，不展示企业 Logo。
- 业务态媒体提示移除 CMS 内部发布语言，只保留必要的“当前为示例演示内容”披露；Q048、字段名、接口依赖和排除说明仍由 `reviewMode` / `ReviewOnly` 隔离。
- 参考站 `http://111.198.38.90:50100/#/home` 于 2026-07-15 13:15（Asia/Shanghai）返回 HTTP 200，但仍无 E-34 字段级可靠映射，继续使用固定 seed 的确定性模拟数据。

### TDD 与机器检查

- RED：新增多企业、发布准入、排序、URL、0/1/N 和回首屏断言后，旧 `fixedStarRecord` 实现按预期失败。
- GREEN：`node tests/enterprise-overview-e33-e35.test.mjs` 通过。
- `npm run design:check`：通过。
- `npm run build`：通过；仅保留既有大 chunk 警告。

### 当前门禁

E-34 五项覆盖均标记为 `manual_review`：当前工具集不能直接操控用户正在使用的 in-app browser，尚缺业务态/评审态 DOM 与截图、选择器切换和滚动定位的浏览器证据，因此未标记为 `verified`。
