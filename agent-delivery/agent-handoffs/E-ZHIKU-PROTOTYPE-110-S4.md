# E-ZHIKU-PROTOTYPE-110-S4 · 高端智库原型 S4：智树侧科技人才智慧服务（23/23 项，P56-P66）

- **认领人**：human:淮政玮（AI 代为执行）
- **仓库**：`demo-ui-gaoduanzhiku-view`（GitLab `gkx-lumen` 组；registry `repo` 字段历史遗留值待 coordinator 订正，同 S1-S3 已登记问题）
- **分支**：`dev`（已推送，commit `ca2be9a`）
- **CI**：本批次本机环境补齐 Node.js/pnpm（`C:\Program Files\nodejs` + `C:\Users\hzw\AppData\Local\pnpm\bin`，S0-S3 均因本机无 Node 只能等 CI 反馈），已在本机实测 `vue-tsc --build`（全绿）与 `vite build`（成功，`built in 26.02s`），非纯静态自检；已推送等待 GitLab Pipeline 最终确认

## 零、五件套先行（延续 S1-S3 流程要求）

按淮政玮指令「S1-S6 前端设计先出五件套，经严谨分析后再实现前端原型代码」「跳过中间评审环节，直接产出结果」，本批次执行顺序：

1. 先补全产品定义五件套，路径：`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`
   - `Wireframe-E-ZHIKU-新型高端智库.md` 由 v0.4（S3 补至 P54）升级至 **v0.5**：新增 P56-P66 共 11 张字段级 wireframe 表（人才画像四维 Tab / 领域分类 / TOP100 / 列表筛选 / 人才地图 / 人才指数 / 人才检索 / 人才驾驶舱 / 人才库订阅 / 人才动态 / 信息推送），覆盖拆解表 59-81 全部 23 项
   - 心理信息（62）与语义检索（77）追加合规/诚实性标注，登记 **Q-ZHIKU-05**（心理信息采集边界待合规 Owner 郭万迎确认）
   - `metricSeed.ts` / `readinessSeed.ts` / `METRIC-OPEN-...核对记录.md` 同步补充 7 个 S4 指标
2. 严谨分析后再落代码：以补全后的 wireframe 字段表为唯一依据实现下述页面组件
3. ⚠️ 五件套仍为 **draft_unsigned**（体验 Owner 高颍 / 语义 Owner 何老师 / 合规 Owner 郭万迎均未会签），仅作团队内部工程推进依据

## 一、范围与实现（对照 DoD）

| DoD | 结果 |
|---|---|
| 覆盖矩阵 S4 负责序号 ✅ 全量 | ✅ 59-81 共 23 项已全部由 🚧 更新为 ✅（含 5 项 ✅⚠️ 演示态标注），`docs/coverage-matrix-110.md` 同步更新，已落地总数 81→103 |
| 画像四维 Tab 可切换；地图可渲染热力；驾驶舱可全屏 | ✅ `TalentProfileHome.vue` 四 Tab（基础/关联/行为/心理）切换实测；`MapPanel.vue`/`CockpitPanel.vue` 均基于新增通用 `TalentMapView.vue`（Leaflet + 天地图），热力开关/图层筛选/全屏切换（`requestFullscreen` API）已实现 |
| 统计指标带 ⓘ + 🧪；npm run build 通过 | ✅ `MetricCard` 统一挂载 D9 五件套角标；本批新增指标：`ZHIKU-S4-TALENT-INFLUENCE-SCORE`/`ZHIKU-S4-TALENT-GROWTH-INDEX`/`ZHIKU-S4-TALENT-MAP-DIST-TOTAL`/`ZHIKU-S4-TALENT-INDEX-SCORE`/`ZHIKU-S4-TALENT-COCKPIT-ALERT`（🔴 演示态）等 7 项；`vite build` 本机实测通过（`built in 26.02s`） |
| 不改 package.json 依赖范围外的内容 | ✅ 本批次未修改 `package.json`；`leaflet`/`@types/leaflet`/`echarts`/`@antv/g6`/`pinia` 均为既有依赖；地图底图对齐 `lumen-ui-topic` 参考实现，天地图 Key 复用同项目组已有公开 Key |

## 一.1、偏离说明

- 人才地图/驾驶舱底图选用**天地图**（`t{s}.tianditu.gov.cn` WMTS `vec_w`/`cva_w` 图层）而非通用 OSM，理由：中国范围底图精度/合规性更优，对齐 `lumen-ui-topic` 参考实现的既有约定；未新增 npm 依赖（`leaflet` 已在 S0 阶段声明）。
- 人才指数（P61）权重定制"实时重算"为前端本地加权求和演示，非接入真实产业统计模型；已在面板内以 `a-alert` + 说明文案标注，`ZHIKU-S4-TALENT-INDEX-SCORE` 的展示保持诚实性约束。
- 人才检索（P62）语义检索为前端关键词/同义词字典匹配演示（`SYNONYM_DICT` 硬编码 3 组示例词），非真实 NLP 语义理解模型；已在检索框下方标注"演示态语义匹配"。
- 人才驾驶舱（P63）趋势预测虚线段与 `ZHIKU-S3-TREND-FORECAST` 同类处理，为前端演示态推测区间，已标注禁止用于对外决策展示。
- 人才画像·心理信息（P56 Tab-4，拆解表 62）为高敏感字段，本批仅完成前端 Mock 结构演示（科研诚信记录/意识形态指标/情感聚类词云），已加 `a-alert` 合规提示并登记 **Q-ZHIKU-05**；正式采集范围与展示边界严格按团队公约 §3.8 "业务口径决策只能甲方拍板"，不在本批擅自扩大或收窄。
- 信息推送（P66）"千人千面"为前端按偏好关键词过滤 Mock 数据流演示，非接入真实推荐算法模型；已标注 Python 侧真实推荐排序留待后续算法批次。
- 其余无范围/技术方案偏离。

## 二、产物清单

### 产品定义（五件套，draft_unsigned）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/Wireframe-E-ZHIKU-新型高端智库.md` v0.5（新增 11 张字段表，P56-P66）
- `agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md`（新增 7 个 S4 指标核对 + Q-ZHIKU-05）
- USM / TRACE / IA 文档沿用初版（已覆盖 S4 路由的用户故事与 IA 结构，本批未再修改）

### 前端代码（`demo-ui-gaoduanzhiku-view`）
- **人才画像**（`TalentProfileHome.vue` 壳 + 4 个 panel + 学者搜索切换，P56）：
  - `ProfileBasicPanel.vue`：基本信息卡（头像/职称/机构/方向/荣誉）+ 教育/工作 Timeline + 联系方式编辑弹窗
  - `ProfileRelationPanel.vue`：成果影响力雷达图 + 成果产出河流图（ECharts ThemeRiver）+ `GraphView` 合作团队关系网络（点击节点可切换画像）+ 相似学者推荐卡片
  - `ProfileBehaviorPanel.vue`：学术迁徙路径图（复用 `TalentMapView`）+ 科研成长轨迹折线图 + 成长指数/企业合作倾向指数 + 合作活跃度热力网格
  - `ProfilePsychPanel.vue`：科研诚信记录表 + 意识形态/舆情指标进度条 + 文本情感分析主题词云（复用 `WordCloudTags`）；高敏感字段合规提示
- **人才库**（`TalentPoolHome.vue` 壳 + 3 个 panel，P57-P59）：
  - `DomainClassifyPanel.vue`：九大类节点树（`a-tree`）+ 分类结构饼图 + `GraphView` 知识图谱（人才-学科-机构-项目-成果）+ 智能推荐卡片 + 导出触发
  - `Top100Panel.vue`：关键字检索 + 综合评分/论文数/专利数排序切换 + 「查看画像」跳转 `talent/profile`
  - `ListFilterPanel.vue`：领域/机构双维度筛选 + ECharts 领域分布柱状图 + 多选加入自建人才库 + 人才库列表管理（重命名/删除）
- **人才地图**（`TalentMapHome.vue` 壳 + 5 个 panel，P60-P64）：
  - `MapPanel.vue`：图层开关（专家学者/科研机构/企业/服务机构）+ 热力开关 + 机构人才规模排行表 + 人才流动趋势折线图
  - `IndexPanel.vue`：区域选择器 + 五维统计卡 + 柱线图切换对比 + 雷达图 + 区域×维度热力矩阵 + 权重定制滑块（演示态标注）
  - `SearchPanel.vue`：语义/关键词/全局筛选三模式 Tab + 智能推荐专家卡片 + 检索结果列表 + 人才详情弹层（可跳转完整画像）
  - `CockpitPanel.vue`：全屏大屏（顶部统计卡条 + 热力地图/流向图 + 产业/学科/机构三栏联动 + 综合能力雷达图 + 趋势预测虚线时间轴）
  - `SubscriptionPanel.vue`：全球高端人才资源分类 Tag 筛选 + 检索 + 定制订阅规则表单 + 智能更新推送记录 Timeline
- **人才动态**（`TalentNewsHome.vue` 壳 + 2 个 panel，P65-P66）：
  - `NewsPanel.vue`：资讯聚合列表（5 类）+ 关联学者跳转 + 定向检索 + 分类订阅（同步至 P64）+ 空态覆盖
  - `PushPanel.vue`：热点推送流 + 专属定制推送流（按偏好过滤）+ 推送偏好设置（学者/方向/关键词）+ 未读数角标
- **可复用组件**：`src/components/map/TalentMapView.vue` + `src/components/map/mapTypes.ts`（通用 Leaflet + 天地图地图组件，`MapPoint`/`MapFlowLine` 类型抽象，点位/热力/流向线/工具条/图例齐备，供人才地图与驾驶舱两处不同数据视角复用）
- **地图配置**：`src/config/tianditu.ts`（天地图 WMTS 底图 URL + 子域配置）
- **图表配置**：`src/config/echarts.ts` 新增注册 `RadarChart`/`ThemeRiverChart`/`RadarComponent`/`SingleAxisComponent`/`VisualMapComponent`
- **设计 Token**：`src/styles/design-tokens.css` 新增 `--sci-legend-bg`/`--sci-legend-shadow`（地图图例样式，Design.md §8.1）
- **Mock 数据层**：`src/mock/talentProfile.ts`（学者基础信息/教育工作/影响力/河流图/合作网络/相似学者/迁徙/成长/诚信/意识形态/情感主题，含 store）、`src/mock/talentPool.ts`（领域树/知识图谱/推荐/TOP100/人才列表/自建库，含 store）、`src/mock/talentMap.ts`（地图点位/机构排名/流动趋势/流向线/指数维度/检索/订阅资源/驾驶舱统计/产业联动/预测趋势，含 store）、`src/mock/talentNews.ts`（资讯/推送流/偏好，含 store）
- **覆盖矩阵**：`docs/coverage-matrix-110.md` 59-81 项更新为 ✅，累计 81→103

### 附带修复（既有代码，非本批新增范围，为使 `vue-tsc --build` 全绿一并处理）
- `src/mock/talentPool.ts`：`noUncheckedIndexedAccess` 下数组按下标取值可能为 `undefined`，`Top100Talent.org/field`、`TalentListItem.org/field/region` 补 `?? ''` 兜底
- `src/views/tech-roadmap/panels/DelphiPanel.vue` / `RoadmapPanel.vue`、`src/views/tech-system/panels/SocialNetworkPanel.vue`、`src/views/tech-trend/panels/AlertTrackingPanel.vue`：`a-form` 缺失必填 `model` prop 导致的既有类型错误（S1-S3 遗留，本机首次具备 Node 环境实测才暴露），统一补 `:model="{}"`（表单字段均为独立 `v-model` 绑定，不依赖 `a-form` 的 `model` 聚合对象，补空对象不改变运行时行为）

## 三、架构合规自检（团队公约 §2 十条）

| # | 条款 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 不涉及，本批为纯前端 Mock 交互；人才指数权重重算/语义检索/趋势预测/千人千面推荐均为前端演示态，非真实算法产出，已标注诚实性文案 |
| 2 | 前端→Java REST→Python /internal/*（不可越层） | ✅ 未接任何后端，不违反调用链 |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ 不涉及；知识图谱/合作网络可视化为前端 Mock 图数据 + AntV G6 渲染，非图数据库查询 |
| 4 | 可观测性三件套 | ✅ 沿用 S0 `src/utils/observability.ts` |
| 5 | CI/CD 绿 → K8s dev rollout | ⚠️ 已推送，本机已实测 `vue-tsc --build` 全绿 + `vite build` 成功，待淮政玮确认 GitLab Pipeline 最终结果 |
| 6 | demo2 只读 merge 铁律 | ✅ 不涉及 |
| 7 | 共享聚合核心方案 A | ✅ 不涉及（纯前端阶段未接 Java） |
| 8 | 数据策略：ADS 先行 + Mock 填充 | ✅ 全部 Mock 数据文件化于 `src/mock/`，D4=mock |
| 9 | 前端规范唯一来源 D8 | ✅ 沿用 `design-tokens.css`，Arco 组件为主；地图新增图例 token 对齐 Design.md §8.1；ECharts/AntV G6/Leaflet 均为团队既有技术栈 |
| 10 | 数据血缘铁律 D9 | ✅ 每个统计数字均带 ⓘ MetricSpecCard + 对应角标；D1=draft、D2=`ZHIKU-S4-TALENT-INDEX-SCORE`/`ZHIKU-S4-TALENT-COCKPIT-ALERT` 为 provisional（🔴 演示态，其余 aligned）、D3=none、D4=mock，`readinessSeed.ts` 已登记 7 个新指标 |

## 四、五件套 → 代码 严谨分析对照 + 本机实测结果

### 4.1 Wireframe → 代码对照

| Wireframe 页面 | 落地组件 | 分析结论 |
|---|---|---|
| P56 人才画像 | `TalentProfileHome.vue` + 4 panel | 四维 Tab（基础/关联/行为/心理）分层呈现，符合"标签化画像"设计假设；心理信息 Tab 独立隔离并加合规提示，避免与其他三维混淆敏感度分级 |
| P57 领域分类 | `DomainClassifyPanel.vue` | `a-tree` 承载九大类节点树，`GraphView` 二次跨模块复用（继 S3 语义/合作网络后第三个消费场景），验证组件抽象通用性边界仍成立 |
| P58 TOP100 | `Top100Panel.vue` | 排序切换（评分/论文/专利）+ 跳转画像联动 `talentProfile` store，验证"榜单→详情"跨页面 store 联动设计可行 |
| P59 列表筛选 | `ListFilterPanel.vue` | 双维度筛选 + 多选建库，验证"筛选结果批量归档"最小可行交互 |
| P60 人才地图 | `MapPanel.vue` | 新增通用 `TalentMapView.vue`（首次引入 Leaflet + 天地图，对齐 Design.md §8 地图工作区规范），验证"地图组件跨场景复用"设计假设（P60/P63 共用） |
| P61 人才指数 | `IndexPanel.vue` | 柱线图切换 + 雷达图 + 手写热力矩阵表格（非 ECharts heatmap，因需要精确控制单元格文案与 Design.md 色阶）+ 权重滑块，多视图对同一数据集的呈现验证"一数多面"设计假设 |
| P62 人才检索 | `SearchPanel.vue` | Tab 切换改变检索输入形态，同义词字典模拟语义扩展，验证"演示态语义检索"最小可行方案；详情弹层→跳转画像复用 P58 已验证的联动模式 |
| P63 人才驾驶舱 | `CockpitPanel.vue` | 深色大屏主题（区别于常规浅色界面），复用 `TalentMapView` 验证地图组件在深色背景下的可读性；三栏联动通过 Tag 点击驱动 `computed` 过滤，未引入额外状态管理复杂度 |
| P64 人才库订阅 | `SubscriptionPanel.vue` | 分类 Tag 筛选 + 表单新建规则 + Timeline 展示，复用 talentMap store 的 `subscriptionRules` 状态，验证"资讯订阅"跨页面（P64/P65）数据一致性 |
| P65 人才动态 | `NewsPanel.vue` | 资讯分类筛选 + 关联学者跳转，`EmptyState` 复用覆盖 Wireframe 要求的空态文案 |
| P66 人才信息推送 | `PushPanel.vue` | 热点/专属双列布局直观区分"全网"与"个性化"，偏好增删即时影响下方列表，验证"千人千面"演示态最小实现路径 |

### 4.2 本机实测结果（S0-S3 因无 Node.js 只能静态自检，本批首次具备本机环境）

本批次在本机补齐 Node.js（`v24.19.0`）与 pnpm（`11.20.0`）后，执行了以下实测（非静态自检）：

| 检查项 | 命令 | 结果 |
|---|---|---|
| 类型检查 | `vue-tsc --build`（`node_modules/.bin`） | ✅ 全绿，0 error |
| 生产构建 | `vite build` | ✅ 成功，`3299 modules transformed`，`built in 26.02s`（`chunkSizeWarningLimit` 提示部分 chunk >500KB，为既有 `echarts`/`@antv/g6` 依赖体积，非本批引入的新问题，不阻断构建） |

实测过程中发现并修复的问题：
- `talentPool.ts` 两处 `noUncheckedIndexedAccess` 索引访问类型错误（本批新增代码问题，已修复，见 §二"附带修复"）
- 既有 4 个文件（`DelphiPanel.vue`/`RoadmapPanel.vue`/`SocialNetworkPanel.vue`/`AlertTrackingPanel.vue`）的 `a-form` 缺失 `model` prop 类型错误（S1-S3 遗留，因本机首次具备 Node 环境实测才暴露，本批一并修复，不改变运行时行为）

> 说明：由于 CI 使用 `npm install`（仓内无 `package-lock.json`）而本机使用 `pnpm install`（生成 `pnpm-lock.yaml`，**未纳入本次提交**，因项目历史上未采用 pnpm 工作流），两者解析到的依赖版本理论上可能存在细微差异；本机实测结果作为强信号参考，最终仍以 GitLab CI Pipeline 结果为准。

## 五、已知限制（需人工核实）

1. **五件套未会签**：本批 Wireframe v0.5 与此前 USM/TRACE/IA/METRIC-OPEN 均为 draft_unsigned，需高颍（体验）/何老师（语义）/郭万迎（合规）后续会签，当前仅作团队内部工程推进依据；**心理信息采集边界（Q-ZHIKU-05）为新增高优先级待确认事项**，涉及合规风险，建议 PM 优先推进郭万迎书面确认。
2. **CI Pipeline 最终结果待确认**：本机实测通过不等同于 CI 环境（`npm install` 解析）100% 一致，若 CI 报错将立即追加修复 commit。
3. **地图组件依赖浏览器 Fullscreen API**：`CockpitPanel.vue`/`TalentMapView.vue` 全屏功能依赖 `document.fullscreenElement`，部分嵌入式 iframe 场景可能受限，属浏览器标准行为限制，非代码缺陷。
4. **task-registry `repo` 字段**历史遗留问题同 S1-S3，需 coordinator 订正。
5. **pnpm-lock.yaml 未提交**：本机为实测 `vue-tsc`/`vite build` 临时用 pnpm 安装依赖，未纳入本次提交（仓库历史工作流为 npm，无 `package-lock.json`），如需固化依赖版本建议 PM/架构师后续统一决策采用的包管理器并补充锁文件。
6. **S1 任务状态**因网关规则（`pending_test → testing` 需 `qa-agent` 认领或 `human:黄敬洲` 监管）在纯自主模式下无法自动推进；**S2/S3 任务状态**处于 `integration`，同样待 CI 验证与后续测试网关处理；均已在对应任务备注中记录，不影响 S4 独立推进（S4 仅依赖 S0）。

## 六、Cost（估算，平台账单为准）

- `model_used`：Sonnet 5（Cursor cloud agent，模型标识以平台账单为准）
- `actual_tokens` / `actual_cost`：本环境无法读取平台计费数据，本批次涉及 5 件套补全（11 张 wireframe 表）+ 14 个页面组件 + 1 个可复用地图组件（首次引入 Leaflet + 天地图）+ 4 个 mock 数据模块（均含 Pinia store）+ 本机 Node 环境搭建与实测排障（含既有 4 处遗留类型错误修复），规模略大于 S3，建议 coordinator 从平台账单回填
- `cost_warn`：green（预估未超 $10 阈值）

## 七、下一步

1. **待淮政玮确认 GitLab CI Pipeline 最终结果**（本机实测已通过，作为强信号参考）。
2. S4 验收通过后，按淮政玮指令自动认领并开工 `E-ZHIKU-PROTOTYPE-110-S5`（基础研究智能决策，6 项，P67-P72），同样先出五件套再实现代码。
3. 提请 coordinator 批量订正 S0-S6 各任务 `repo` 字段（历史遗留值与实际执行仓 `demo-ui-gaoduanzhiku-view` 不一致问题，S1-S4 已连续四批登记）。
4. 提请 PM 优先推进 **Q-ZHIKU-05**（心理信息采集边界）合规确认，登记入 `客户决策清单跟踪表.md`。
