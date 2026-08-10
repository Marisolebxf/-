# E-ZHIKU-PROTOTYPE-110-S5 · 高端智库原型 S5：智树侧基础研究智能决策（6/6 项，P67-P72）

- **认领人**：human:淮政玮（AI 代为执行）
- **仓库**：`demo-ui-gaoduanzhiku-view`（GitLab `gkx-lumen` 组；registry `repo` 字段历史遗留值待 coordinator 订正，同 S1-S4 已登记问题）
- **分支**：`dev`（待推送）
- **CI**：本机已实测 `vue-tsc --noEmit -p tsconfig.app.json`（全绿）与 `vite build`（成功，`3312 modules transformed`，`built in 27.00s`），非纯静态自检；推送后待淮政玮确认 GitLab Pipeline 最终结果

## 零、五件套先行（延续 S1-S4 流程要求）

按淮政玮指令「S1-S6 前端设计先出五件套，经严谨分析后再实现前端原型代码」「跳过中间评审环节，直接产出结果」，本批次执行顺序：

1. 先补全产品定义五件套，路径：`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`
   - `Wireframe-E-ZHIKU-新型高端智库.md` 由 v0.5（S4 补至 P66）升级至 **v0.6**：新增 P67-P72 共 6 张字段级 wireframe 表（问题清单 / 问题发展趋势 / 竞争格局报告 / 深圳市部署清单 / 组织实施分析 / 成果评估），覆盖拆解表 82-87 全部 6 项
   - 竞争格局报告（84）追加算法诚实性标注，追加关联至已登记的 **Q-ZHIKU-04**（原仅覆盖人才指数/成果评估权重算法，本批次追加区域对比指数）
   - `metricSeed.ts` / `readinessSeed.ts` / `METRIC-OPEN-...核对记录.md` 同步补充 6 个 S5 指标
2. 严谨分析后再落代码：以补全后的 wireframe 字段表为唯一依据实现下述页面组件
3. ⚠️ 五件套仍为 **draft_unsigned**（体验 Owner 高颍 / 语义 Owner 何老师 / 合规 Owner 郭万迎均未会签），仅作团队内部工程推进依据

## 一、范围与实现（对照 DoD）

| DoD | 结果 |
|---|---|
| 覆盖矩阵 S5 负责序号 ✅ 全量 | ✅ 82-87 共 6 项已全部由 🚧 更新为 ✅（含 4 项 ✅⚠️ 演示态标注），`docs/coverage-matrix-110.md` 同步更新，**已落地总数 103→109（110 项功能点全部落地，无 ❌，仅剩 S6 联调整合终验）** |
| 问题清单可检索/订阅；地图可视化清单可渲染；成果评估四维雷达可切换 | ✅ `IssueListPanel.vue` 来源筛选+清单表格+订阅；`BasicResearchDeployHome.vue` 复用 `TalentMapView` 渲染部署清单地图视角；`BasicResearchEvalHome.vue` 成果选择器切换后雷达图/统计卡/报告文案联动更新，实测通过 |
| 统计指标带 ⓘ + 🧪；`vite build` 通过 | ✅ `MetricCard` 统一挂载 D9 五件套角标；本批新增指标：`ZHIKU-S5-ISSUE-TOTAL`/`ZHIKU-S5-ISSUE-HEAT-SCORE`/`ZHIKU-S5-COMPETITION-INDEX`/`ZHIKU-S5-DEPLOY-TOTAL`/`ZHIKU-S5-ORG-CAPABILITY-SCORE`/`ZHIKU-S5-EVAL-SCORE`（后两项 🔴 演示态）共 6 项；`vite build` 本机实测通过（`built in 27.00s`） |
| 不改 package.json 依赖范围外的内容 | ✅ 本批次未修改 `package.json`；复用既有 `leaflet`/`echarts`/`pinia` 依赖，未新增任何 npm 包 |

## 一.1、偏离说明

- 深圳市基础研究部署清单（P70）与组织实施分析（P71）为**深圳本地化特色**条目（拆解表 85/86 明确标注"深圳市"），本批严格按 wireframe 字段表落地为深圳专属数据集（机构/经费/管理机制均标注深圳本地机构名称），未泛化为全国通用清单。
- 基础研究问题清单（P67）"权威来源目录+大数据挖掘构建识别模型"中"智能识别"为前端固定延时（1.2s）+ 预置结果的 Mock 演示，非接入真实文本挖掘/NLP 模型；已在按钮旁的 `Message.success` 反馈文案中明确标注"演示态"。
- 问题发展趋势（P68）"增长速度/研究热度/潜力评估"为前端本地简化打分（`ISSUE_SCORE_BY_ID` 硬编码），非真实"时序+文献引用+科研成果"综合模型；已在面板底部加诚实性提示。
- 竞争格局报告（P69）区域对比指数（`ZHIKU-S5-COMPETITION-INDEX`）是否需独立权重算法待算法 Lead 确认，追加登记至已有 **Q-ZHIKU-04**（原条目已含人才指数/成果评估，本批次追加区域对比指数，三者统一按"暂用等权重占位，不参与真实排名对外展示"处理）。
- 深圳市部署清单（P70）"动态生成更新"为前端 Mock 静态数据集合演示，非接入真实情报数据自动生成流水线；已在页面底部加诚实性提示。
- 组织实施分析（P71）需求预测虚线段沿用 S3/S4 已验证的"实际/预测双线"处理模式（前端演示态推测区间，禁止用于对外决策展示）；资源配置建议为固定文案模板，非真实决策引擎输出；均已标注。
- 基础研究成果评估（P72）四维量化评价算法定义卡未落地（登记 Q-ZHIKU-04），当前为前端等权重求和演示态；已在页面顶部加 `a-alert` 强提示，禁止用于对外决策展示。
- 其余无范围/技术方案偏离。

## 二、产物清单

### 产品定义（五件套，draft_unsigned）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/Wireframe-E-ZHIKU-新型高端智库.md` v0.6（新增 6 张字段表，P67-P72）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md`（新增 6 个 S5 指标核对 + Q-ZHIKU-04 追加竞争格局报告条目）
- USM / TRACE / IA 文档沿用初版（已覆盖 S5 路由的用户故事与 IA 结构，本批未再修改）

### 前端代码（`demo-ui-gaoduanzhiku-view`）
- **基础研究问题清单与趋势**（`BasicResearchIssuesHome.vue` 壳 + 3 个 panel，P67-P69）：
  - `IssueListPanel.vue`：权威来源目录 Tag 筛选 + 问题清单表格（来源/领域/状态）+「智能识别」演示态按钮 + 定向查询与订阅（复用订阅关键词体系）
  - `IssueTrendPanel.vue`：问题选择器 + 发展轨迹折线图 + 增长速度/研究热度/潜力评估统计卡 + 动态监控预警列表 + 智能推荐（相关问题/相关文献）
  - `CompetitionPanel.vue`：国际/国家/深圳市三层次 Tab 切换 + 统计卡组 + 柱状/雷达图切换对比 + 趋势追踪折线图 + 生成报告跳转智能写作
- **深圳市基础研究部署清单**（`BasicResearchDeployHome.vue`，P70，深圳本地化特色）：领域筛选 + 复用 `TalentMapView` 可视化清单（地图视角）+ 部署清单表格（优先级/依托机构/进展状态）+ 趋势分析折线图 + 热点问题识别（关联 P67 问题清单）
- **基础研究组织实施分析**（`BasicResearchOrgHome.vue`，P71，深圳本地化特色）：核心能力雷达图（学科覆盖/人才品质/机构资源/经费投入/管理机制 5 维）+ 深圳现有科研资源清单表格 + 引进/创新资源需求预测折线图（实际/预测双线）+ 资源配置建议列表
- **基础研究成果评估**（`BasicResearchEvalHome.vue`，P72）：成果选择器 + 四维量化雷达图 + 统计卡组 + 可视化评估报告文案 + 趋势分析折线图 + 对比分析柱状图；顶部 `a-alert` 演示态强提示
- **Mock 数据层**：`src/mock/basicResearch.ts`（问题清单/来源/趋势/评分/预警/推荐、竞争格局统计/趋势、部署清单/趋势、组织能力维度/资源清单/预测/建议、成果评估结果/趋势，含 `useBasicResearchStore` Pinia store）
- **指标注册**：`src/mock/metricSeed.ts` 新增 6 条 S5 指标语义卡；`src/mock/readinessSeed.ts` 新增 `s5Readiness` 函数并注册 6 个 S5 指标（`ZHIKU-S5-COMPETITION-INDEX`/`ZHIKU-S5-EVAL-SCORE` 标记 `def.status = missing`，对齐算法定义卡未落地事实）
- **覆盖矩阵**：`docs/coverage-matrix-110.md` 82-87 项更新为 ✅，累计 103→109（110 项全部落地）

### 复用说明（未新增组件/依赖）
- 地图渲染统一复用 S4 已验证的 `TalentMapView.vue` + `mapTypes.ts`（新增 `deployToMapPoints` 转换函数将 `DeployItem[]` 映射为 `MapPoint[]`，未修改组件本身）
- 图表统一复用 `src/config/echarts.ts` 已注册的内置模块（`LineChart`/`BarChart`/`RadarChart`），未新增注册

## 三、架构合规自检（团队公约 §2 十条）

| # | 条款 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 不涉及，本批为纯前端 Mock 交互；竞争格局指数/成果评估四维得分/组织能力得分均为前端演示态，非真实算法产出，已标注诚实性文案 |
| 2 | 前端→Java REST→Python /internal/*（不可越层） | ✅ 未接任何后端，不违反调用链 |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ 不涉及，本批无图谱可视化需求 |
| 4 | 可观测性三件套 | ✅ 沿用 S0 `src/utils/observability.ts` |
| 5 | CI/CD 绿 → K8s dev rollout | ⚠️ 待推送，本机已实测 `vue-tsc --noEmit` 全绿 + `vite build` 成功，待淮政玮确认 GitLab Pipeline 最终结果 |
| 6 | demo2 只读 merge 铁律 | ✅ 不涉及 |
| 7 | 共享聚合核心方案 A | ✅ 不涉及（纯前端阶段未接 Java） |
| 8 | 数据策略：ADS 先行 + Mock 填充 | ✅ 全部 Mock 数据文件化于 `src/mock/`，D4=mock |
| 9 | 前端规范唯一来源 D8 | ✅ 沿用 `design-tokens.css`，Arco 组件为主；地图/图表均复用既有 Design.md §8 规范落地的组件，未新增视觉规范例外 |
| 10 | 数据血缘铁律 D9 | ✅ 每个统计数字均带 ⓘ MetricSpecCard + 对应角标；D1=`ZHIKU-S5-COMPETITION-INDEX`/`ZHIKU-S5-EVAL-SCORE` 为 missing（🔴 演示态，算法未落地），其余 draft；D2=pending、D3=none、D4=mock，`readinessSeed.ts` 已登记 6 个新指标 |

## 四、五件套 → 代码 严谨分析对照 + 本机实测结果

### 4.1 Wireframe → 代码对照

| Wireframe 页面 | 落地组件 | 分析结论 |
|---|---|---|
| P67 问题清单 | `IssueListPanel.vue` | 来源目录 Tag 筛选复用 S4 `CockpitPanel` 已验证的"点击 Tag 切换筛选"交互模式，验证该模式在不同数据域（人才→问题）下仍成立；订阅体系复用 talentMap/talentNews store 已验证的"关键词订阅"设计范式，未重新发明轮子 |
| P68 问题发展趋势 | `IssueTrendPanel.vue` | 问题选择器驱动折线图/统计卡/预警/推荐四区块联动，验证"单选择器多区块联动"设计假设（同 P61 人才指数区域选择器模式）在新数据域下的可复用性 |
| P69 竞争格局报告 | `CompetitionPanel.vue` | Tab 切换三层次 + 柱状/雷达图切换双视图，验证"多层次对比 + 多视图切换"组合模式；生成报告跳转 `writing/create` 复用 S1 已验证的报告生成入口，未重复实现写作链路 |
| P70 深圳市部署清单 | `BasicResearchDeployHome.vue` | 首次将 `TalentMapView` 从"人才场景"迁移到"部署清单场景"（新增 `deployToMapPoints` 纯函数转换，未修改组件本身），验证该地图组件的场景无关性设计假设成立 |
| P71 组织实施分析 | `BasicResearchOrgHome.vue` | 雷达图 + 表格 + 预测折线图 + 建议列表四段式布局，复用 S4/S3 已验证的"能力画像+资源清单+趋势预测+行动建议"叙事结构，验证该结构对"组织级"分析主题同样适用 |
| P72 成果评估 | `BasicResearchEvalHome.vue` | 四维雷达图 + 报告文案生成，复用 P69 生成报告交互；顶部强提示 `a-alert`（区别于其他页面的底部弱提示），因本页算法未落地风险等级更高，验证"诚实性标注强度应与算法成熟度风险分级匹配"的设计原则 |

### 4.2 本机实测结果

本批次沿用 S4 已补齐的本机 Node.js（`v24.19.0`）/pnpm（`11.20.0`）环境，执行以下实测（非静态自检）：

| 检查项 | 命令 | 结果 |
|---|---|---|
| 类型检查 | `vue-tsc --noEmit -p tsconfig.app.json`（`node_modules/.bin`） | ✅ 全绿，0 error |
| 生产构建 | `vite build` | ✅ 成功，`3312 modules transformed`，`built in 27.00s`（`chunkSizeWarningLimit` 提示部分 chunk >500KB，为既有 `echarts` 依赖体积，非本批引入的新问题，不阻断构建） |

实测过程中未发现新增类型错误（S4 已修复的既有 `a-form` 遗留问题本批未再触发）。

> 说明：CI 使用 `npm install`（仓内无 `package-lock.json`），本机使用 `pnpm install`／既有 `node_modules`，两者解析到的依赖版本理论上可能存在细微差异；本机实测结果作为强信号参考，最终仍以 GitLab CI Pipeline 结果为准。

## 五、已知限制（需人工核实）

1. **五件套未会签**：本批 Wireframe v0.6 与此前 USM/TRACE/IA/METRIC-OPEN 均为 draft_unsigned，需高颍（体验）/何老师（语义）/郭万迎（合规）后续会签，当前仅作团队内部工程推进依据。
2. **CI Pipeline 最终结果待确认**：本机实测通过不等同于 CI 环境（`npm install` 解析）100% 一致，若 CI 报错将立即追加修复 commit。
3. **Q-ZHIKU-04 范围扩大**：原仅覆盖人才指数（76）/成果评估（87）权重算法，本批次追加竞争格局报告（84）区域对比指数，三项算法定义卡均未落地，建议算法 Lead（唐绍祖）统一评估优先级。
4. **task-registry `repo` 字段**历史遗留问题同 S1-S4，需 coordinator 订正。
5. **110 项功能点已全部落地**：至此覆盖矩阵 82-87 补齐后，110 行全部为 ✅（无 ❌），S6 批次范围收窄为**纯联调整合 + 最终 100% 合规终验**，不再涉及新页面/新组件开发。
6. **S1-S4 任务状态**：S1 因网关规则滞留 `pending_test`；S2/S3/S4 处于 `integration`，均待 CI 验证与后续测试网关处理；已在对应任务备注中记录，不影响 S5 独立推进（S5 仅依赖 S0）。

## 六、Cost（估算，平台账单为准）

- `model_used`：Sonnet 5（Cursor cloud agent，模型标识以平台账单为准）
- `actual_tokens` / `actual_cost`：本环境无法读取平台计费数据，本批次涉及 5 件套补全（6 张 wireframe 表）+ 4 个页面/6 个组件（3 个 tab 页面 + 3 个直出页面）+ 1 个 mock 数据模块（含 Pinia store）+ 本机实测，规模小于 S4（无新增可复用组件/新技术栈引入），建议 coordinator 从平台账单回填
- `cost_warn`：green（预估未超 $10 阈值）

## 七、下一步

1. **待淮政玮确认 GitLab CI Pipeline 最终结果**（本机实测已通过，作为强信号参考）。
2. S5 验收通过后，按淮政玮指令自动认领并开工 `E-ZHIKU-PROTOTYPE-110-S6`（联调整合 + 覆盖矩阵 110 行终验），该批次不涉及新页面开发，重点为全站可演示性验收与合规三件套（Design.md §14 / D9 血缘 / D10 交互）无阻断项核查。
3. 提请 coordinator 批量订正 S0-S6 各任务 `repo` 字段（历史遗留值与实际执行仓 `demo-ui-gaoduanzhiku-view` 不一致问题，S1-S5 已连续五批登记）。
4. 提请 PM 推进 **Q-ZHIKU-04**（人才指数/竞争格局/成果评估三项权重算法定义卡）与 **Q-ZHIKU-05**（心理信息采集边界）合规/算法确认，登记入 `客户决策清单跟踪表.md`。
