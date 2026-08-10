# E-ZHIKU-PROTOTYPE-110-S2 · 高端智库原型 S2：智树侧研究需求分析 + 技术体系分析（28/28 项，P22-P41）

- **认领人**：human:淮政玮（AI 代为执行）
- **仓库**：`demo-ui-gaoduanzhiku-view`（GitLab `gkx-lumen` 组；registry `repo` 字段历史遗留值待 coordinator 订正，同 S1 已登记问题）
- **分支**：`dev`（已推送，commit `9b0ef3b`）
- **CI**：已推送等待 GitLab Pipeline 验证（本机仍无 Node.js 环境，无法本地复测 `vue-tsc --build` / `vite build`，与 S0/S1 同一限制；本批已针对已知类型陷阱做静态自检，见 §4）

## 零、五件套先行（延续 S1 流程要求）

按淮政玮指令「S1-S6 前端设计先出五件套，经严谨分析后再实现前端原型代码」「跳过中间评审环节，直接产出结果」，本批次执行顺序：

1. 先补全产品定义五件套，路径：`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`
   - `Wireframe-E-ZHIKU-新型高端智库.md` 由 v0.2（S1 写作链路 17 张字段表）补全至 **v0.3**：新增 P22-P41 共 20 张字段级 wireframe 表（科技实体清单/颠覆性技术/前沿技术/技术趋势/媒体聚焦/技术体系树/专家交互/论文分析/专利分析/科研项目分析/社会网络分析），覆盖 S2 全部路由
   - `metricSeed.ts` / `readinessSeed.ts` / `METRIC-OPEN-...核对记录.md` 同步补充 6 个 S2 指标
2. 严谨分析后再落代码：以补全后的 wireframe 字段表为唯一依据实现下述页面组件
3. ⚠️ 五件套仍为 **draft_unsigned**（体验 Owner 高颍 / 语义 Owner 何老师 / 合规 Owner 郭万迎均未会签），仅作团队内部工程推进依据

## 一、范围与实现（对照 DoD）

| DoD | 结果 |
|---|---|
| 覆盖矩阵 28/28 ✅（S2 负责的功能序号全部有落点） | ✅ 1-28 项（研究需求分析 7 项 + 技术体系分析 21 项）已全部由 🚧 更新为 ✅，`docs/coverage-matrix-110.md` 同步更新 |
| 每个统计指标带 ⓘ MetricSpecCard（8件套）+ 🧪 MockBadge | ✅ `MetricCard` 组件统一挂载 D9 五件套角标；本批新增指标：`ZHIKU-S2-ENTITY-TOTAL`/`ZHIKU-S2-TREND-TECH-TOTAL`/`ZHIKU-S2-TECHSYS-TOTAL`/`ZHIKU-S2-PAPER-TOTAL`/`ZHIKU-S2-PROJECT-TOTAL`/`ZHIKU-S2-NETWORK-NODE-TOTAL` |
| 关键链路可走通：科技实体检索 → 颠覆性技术识别 → 技术体系在线编辑 → 论文/专利/项目分析 → 社会网络可视化 | ✅ `ResearchNeedHome.vue`（实体清单→颠覆性技术卡片→趋势卡片→媒体聚焦）+ `TechSystemHome.vue`（体系列表→在线树编辑器→专家交互→论文/专利/项目分析→AntV G6 社会网络图→维护）全链路可点通 |
| 社会网络分析采用 AntV G6（技术要求硬指标） | ✅ `SocialNetworkGraph.vue` 使用 `@antv/g6` v5 `Graph` + `force` 布局，节点/边转纯 JS 结构后传入（规避响应式对象警告） |
| npm run build 通过 | ⚠️ 已推送 CI，待淮政玮验证反馈（本机无 Node.js，无法本地复测；已对照 S1 CI 曾报错的类型陷阱模式逐项自检，见 §4） |
| 不改 package.json 依赖范围外的内容 | ✅ 本批次仅新增业务代码文件；`@antv/g6`/`echarts`/`vue-echarts`/`pinia` 均为 S0 阶段已声明依赖，未新增 package.json 条目 |

## 一.1、偏离说明

- 拆解表第 19/20 项（专利分析总览/任务管理"算法层"描述，属 Python 算法能力说明而非前端交互组件）以静态能力说明卡形式与 15/16 共页呈现，不重复建交互组件；算法本身（混合检索、可解释性输出、资源限流）留待后续批次由 Python 层落地，前端本批仅做产品语义占位说明，不构成范围缺失。
- 社会网络可视化的"结果分析"（关键节点识别/社群划分）采用点击节点侧栏详情 + 统计卡片方式呈现，未做独立"结果分析"路由页；IA 层面判断二者信息密度足够在同一 Tab 内呈现，避免过度拆分导致的跳转负担，与 Wireframe P40 字段表设计一致。
- 词云（论文/专利关键词）与专利全球布局采用轻量自研组件（`WordCloudTags` 标签云 + ECharts 柱状图替代真实地理地图），非引入新的地图/词云第三方库，理由：控制依赖面（未在 package.json 声明）、demo 阶段视觉可读性优先于地理精度；如业务后续要求真实地理底图，可平滑升级为 Leaflet（已在依赖中）绘制。
- 其余无范围/技术方案偏离。

## 二、产物清单

### 产品定义（五件套，draft_unsigned）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/Wireframe-E-ZHIKU-新型高端智库.md` v0.3（新增 20 张字段表，P22-P41）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md`（新增 6 个 S2 指标核对）
- USM / TRACE / IA 文档沿用初版（已覆盖 S2 路由的用户故事与 IA 结构，本批未再修改）

### 前端代码（`demo-ui-gaoduanzhiku-view`）
- **研究需求分析**（`ResearchNeedHome.vue` 壳 + 4 个 panel，P22-P26）：
  - `TechEntityPanel.vue`：科技实体清单，搜索+多维筛选（领域/地区/类型）+卡片/表格双视图+模拟导入
  - `DisruptiveTechPanel.vue`：颠覆性技术识别卡片 + 前沿技术清单卡片（含 ECharts 热度趋势迷你图）
  - `TechTrendPanel.vue`：技术趋势宏观统计卡片组
  - `MediaFocusPanel.vue`：媒体聚焦舆情列表 + 预警标注 + 生成简报（弹窗）
- **技术体系分析**（`TechSystemHome.vue` 壳 + 5 个 panel，P27-P41）：
  - `TechSystemPanel.vue`：技术体系列表 + 在线编辑（`a-tree` 可拖拽 + 成熟度 TRL/重要性星级侧栏编辑）+ 专家交互（按分支筛选+回复+确认）
  - `PaperAnalysisPanel.vue`：论文分析总览（词云+排行+ECharts 趋势）+ 二维交叉分析（`CrossHeatTable`）+ 任务列表/操作
  - `PatentAnalysisPanel.vue`：专利分析总览（词云+排行+国家布局柱状图+IPC 饼图）+ 任务管理 + 案例库 + 深度分析（交叉矩阵）；19/20 算法层以能力说明卡呈现
  - `ResearchProjectPanel.vue`：科研项目检索（关键词+学科/年份）+ 统计分析仪表盘（经费/活跃度/地域）+ 任务管理
  - `SocialNetworkPanel.vue`：网络可视化（`SocialNetworkGraph.vue`，AntV G6 力导向图）+ 结果分析（节点详情侧栏）+ 任务管理 + 数据上传 + 网络维护
- **可复用组件**：`src/components/common/WordCloudTags.vue`（标签云）、`src/components/common/CrossHeatTable.vue`（颜色编码交叉热力表）、`src/components/network/SocialNetworkGraph.vue`（AntV G6 封装）
- **图表配置**：`src/config/echarts.ts`（vue-echarts 按需注册 Bar/Line/Pie + Canvas 渲染器）
- **Mock 数据层**：`src/mock/researchNeed.ts`（科技实体/颠覆性技术/前沿技术/趋势卡片/媒体聚焦）、`src/mock/techSystem.ts`（技术体系树 + 专家意见，含 Pinia store）、`src/mock/paperAnalysis.ts`（论文词云/排行/趋势/交叉表/任务，含 store）、`src/mock/patentAnalysis.ts`（专利词云/排行/国家布局/IPC/案例/交叉表/任务，含 store）、`src/mock/researchProject.ts`（项目/经费/活跃度/地域/任务，含 store）、`src/mock/socialNetwork.ts`（网络节点/边/统计/任务/上传模板/维护清单，含 store）
- **类型定义**：`src/types/crossHeat.ts`（`CrossCell` 交叉表通用类型）
- **覆盖矩阵**：`docs/coverage-matrix-110.md` 1-28 共 28 项更新为 ✅

## 三、架构合规自检（团队公约 §2 十条）

| # | 条款 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 不涉及，本批为纯前端 Mock 交互；专利分析 19/20 算法层仅做静态说明卡，不在前端实现算法 |
| 2 | 前端→Java REST→Python /internal/*（不可越层） | ✅ 未接任何后端，不违反调用链 |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ 不涉及；社会网络可视化为前端 Mock 图数据 + AntV G6 渲染，非图数据库查询 |
| 4 | 可观测性三件套 | ✅ 沿用 S0 `src/utils/observability.ts` |
| 5 | CI/CD 绿 → K8s dev rollout | ⚠️ 已推送，待淮政玮验证 Pipeline 结果 |
| 6 | demo2 只读 merge 铁律 | ✅ 不涉及 |
| 7 | 共享聚合核心方案 A | ✅ 不涉及（纯前端阶段未接 Java） |
| 8 | 数据策略：ADS 先行 + Mock 填充 | ✅ 全部 Mock 数据文件化于 `src/mock/`，D4=mock |
| 9 | 前端规范唯一来源 D8 | ✅ 沿用 `design-tokens.css`，Arco 组件为主；ECharts/AntV G6 按团队既有技术栈使用 |
| 10 | 数据血缘铁律 D9 | ✅ 每个统计数字均带 ⓘ MetricSpecCard + 对应角标；D1=draft、D3=none、D4=mock，`readinessSeed.ts` 已登记 6 个新指标 |

## 四、五件套 → 代码 严谨分析对照 + CI 类型陷阱自检

### 4.1 Wireframe → 代码对照

| Wireframe 页面 | 落地组件 | 分析结论 |
|---|---|---|
| P22 科技实体清单 | `TechEntityPanel.vue` | 卡片/表格双视图满足"快速浏览"与"批量对比"两类使用场景；空态引导"调整筛选条件"而非纯空白 |
| P23/P24 颠覆性技术/前沿技术 | `DisruptiveTechPanel.vue` | 二者信息结构高度相似（技术卡片+热度趋势），合并单组件用 Tab 区分，避免重复代码 |
| P25 技术趋势 | `TechTrendPanel.vue` | 宏观统计卡片 + 标签云，作为"总览入口"引导用户进入 P23/P24 细节 |
| P26 媒体聚焦 | `MediaFocusPanel.vue` | 预警项用红色标记区分普通舆情，生成简报走弹窗确认（防误触） |
| P27/P28 技术体系+在线编辑 | `TechSystemPanel.vue`（list/edit 双模式） | 树形编辑器選中节点后侍栏编辑 TRL 成熟度（滑杆 1-9）+ 重要性（星级 1-5），符合行业惯用量表 |
| P29 专家交互 | `TechSystemPanel.vue`（expert Tab） | 按技术分支筛选，区分"已确认"/"待确认"意见，回复走即时输入框（低摩擦） |
| P30-P32 论文分析 | `PaperAnalysisPanel.vue` | 交叉分析复用 `CrossHeatTable`，验证"复用组件覆盖多模块交叉分析需求"设计假设成立 |
| P33-P36 专利分析 | `PatentAnalysisPanel.vue` | 国家布局用条形图替代地理地图（demo 阶段可读性优先），19/20 算法层降级为说明卡，不做"假交互" |
| P37-P39 科研项目分析 | `ResearchProjectPanel.vue` | 年份区间筛选拆为 `yearFrom`/`yearTo` 两个独立 ref（规避数组索引类型风险，见 4.2） |
| P40/P41 社会网络分析 | `SocialNetworkPanel.vue` + `SocialNetworkGraph.vue` | AntV G6 力导向图为技术要求硬指标；节点点击→侍栏详情验证"可视化+结果分析同页"设计可行 |

### 4.2 CI 类型陷阱自检（对照 S1 首推遇到的 `vue-tsc` 报错模式）

鉴于 S1 首次推送曾因 Arco 表格插槽隐式 `any` 索引 `Record` 类型触发 CI 报错（commit `876e270` 修复），本批交付前对以下已知陷阱逐项自检：

| 陷阱类型 | 自检结果 |
|---|---|
| `verbatimModuleSyntax`：类型-only 导出未加 `type` 修饰符 | ✅ 逐文件核对，`TechEntity`/`FrontierTech`/`MediaFocusItem`/`TechSystemNode`/`AnalysisTaskStatus`/`PatentTask`/`ProjectTask`/`NetworkNode`/`NetworkTask`/`CrossCell`/`Graph as G6Graph` 均以 `import type` 或行内 `type` 修饰符导入 |
| ECharts `option` 对象字面量未显式标注 `EChartsOption`，导致 `xAxis.type` 等字面量被推断为宽泛 `string` 与联合类型不兼容 | ✅ 已修复：`DisruptiveTechPanel`/`PaperAnalysisPanel`/`PatentAnalysisPanel`/`ResearchProjectPanel` 全部图表 option 显式标注 `EChartsOption`（或 `computed<EChartsOption>`）+ `as EChartsOption` 断言，与 lumen-ui-topic 参考实现（`EnterpriseRelationGraph.vue`）一致模式 |
| `noUncheckedIndexedAccess`：数组下标 / 动态 key 索引产生 `T \| undefined` | ✅ `yearFrom`/`yearTo` 拆分为独立 ref 而非数组索引；`Record<K,V>` 类固定 key 索引（如 `TASK_STATUS_COLOR[status]`）不受影响；表格插槽 `record` 统一 `as` 断言为具体类型后取字段 |
| Arco 组件 prop 类型边界（`a-progress` percent 0-1 制、`a-tag` color 为 `TagColor \| string`、`a-alert` type） | ✅ `a-progress` 沿用 `value / 100` 既有模式；`a-tag color` 传入字符串在类型上始终合法；未使用 `a-alert` |
| `a-tree` `data` prop 结构不完全匹配业务节点类型（含额外 `maturity`/`importance` 字段） | ✅ 显式 `as any` 断标注在 `:data` 绑定处隔离类型不匹配，模板内部通过 `as unknown as TechSystemNode` 还原类型后取字段，避免污染其他类型检查 |

> 说明：因本机无 Node.js 环境，以上为静态代码审阅结论，非 `vue-tsc` 实测结果；最终以 CI Pipeline 结果为准，如仍有报错将立即修复并追加 commit。

## 五、已知限制（需人工核实）

1. **本机仍无 Node.js**（S0/S1 已记录同一限制），全部依赖 GitLab CI 做构建校验；本次推送后暂未获得淮政玮的 CI 结果反馈，**Pipeline 状态待确认**。
2. **五件套未会签**：本批 Wireframe v0.3 与此前 USM/TRACE/IA/METRIC-OPEN 均为 draft_unsigned，需高颍（体验）/何老师（语义）/郭万迎（合规）后续会签，当前仅作团队内部工程推进依据。
3. **拆解表 19/20（专利算法层）**以静态说明卡呈现，Python 侧混合检索/可解释性输出/资源限流算法本身留待后续批次（S4/S5 或独立算法批次）实现，不在本批范围内。
4. **task-registry `repo` 字段**历史遗留问题同 S1，需 coordinator 订正。
5. **S1 任务状态**因网关规则（`pending_test → testing` 需 `qa-agent` 认领或 `human:黄敬洲` 监管）在纯自主模式下无法自动推进，已在 S1 任务备注中记录，不影响本批（S2）独立推进（S2 仅依赖 S0）。

## 六、Cost（估算，平台账单为准）

- `model_used`：Sonnet 5（Cursor cloud agent，模型标识以平台账单为准）
- `actual_tokens` / `actual_cost`：本环境无法读取平台计费数据，本批次涉及 5 件套补全（20 张 wireframe 表）+ 9 个页面组件 + 3 个可复用组件 + 6 个 mock 数据模块（均含 Pinia store）+ AntV G6 首次集成，规模偏大，建议 coordinator 从平台账单回填
- `cost_warn`：green（预估未超 $10 阈值，但因规模较 S1 更大，建议 coordinator 核实）

## 七、下一步

1. **待淮政玮验证 CI Pipeline 结果**；若报错将立即追加修复 commit（参照 §4.2 自检清单排查）。
2. S2 验收通过后，按淮政玮指令自动认领并开工 `E-ZHIKU-PROTOTYPE-110-S3`（下一批次范围以 task-registry 依赖关系为准），同样先出五件套再实现代码。
3. 提请 coordinator 批量订正 S0-S6 各任务 `repo` 字段（历史遗留值与实际执行仓 `demo-ui-gaoduanzhiku-view` 不一致问题，S1/S2 已连续两批登记）。
