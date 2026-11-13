# FE-TOPIC-SMALL-CHAIN-POL-L01 · 专题小屏·产业链+政策

> 批 1（产业链 6 页）复刻完成 handoff。批 2（政策 5 项）已在同一任务内先行落地基础壳，本次未再扩展。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent`（原 human:曹丽影，2026-11-11 会话裁定主执行转移） |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

用户 2026-11-12 指令：「对比产业链分析 mobile 实现，目前基本处于不可用状态，认真仔细逐条复刻 pc 端功能和接口，目前接口数据已有，可忽略评审模式和数据mock」。
据此把 `lumen-ui-topic-mobile` 产业链 6 页全部对齐 PC 仓真源（`repos/lumen-ui-topic/src/views/industry-center/*`），**全部走真实后端接口**（`VITE_APP_USE_MOCK=false`），评审模式按指令忽略（env 关闭 + 组件门控）。

### 页面清单（对照 PC 真源逐条复刻）

| mobile 页面 | PC 真源 | 复刻要点 |
|------|------|------|
| `IndustryOverviewView` 产业专题全景 | `IndustryOverviewPage` | 3 页签：G6 全景图谱（节点详情抽屉+跳全景）/ 产业资讯（独立 `industryOverviewNews` + 类型筛选 + 外链详情）/ 整体概况（产业介绍、发展历程、`regionPoints` 区域分布、深圳 `4403` 区级分布） |
| `IndustrySearchView` 产业查询 | `IndustrySearchPage` | 真实场景标签 `chainSearchBizScenesList`；搜索历史 `chainSearchBizHistoryList/Save/Clear`；未搜索时目录推荐；结果卡 + 摘要抽屉 + 跳全景 |
| `IndustryPanoramaView` 产业链全景图谱 | `IndustryPanoramaPage` | 快照秒开 `industryPanoramaSnapshot`；`committedKey` 脏检测 → 显式「开始分析」建真任务 `chain:panorama:graph`（asOf 缺省预取最新快照日期）；演进时间轴（播放/单步/下拉）；图/结构列表双形态（>300 节点自动降列表）；节点/边详情抽屉 |
| `IndustryDiagnosisView` 产业诊断 | `IndustryDiagnosisPage` | 3 工作区 + 记录页签。周期：4 参数范围校验 + `time_range` 契约 + ECharts 趋势/拐点/回溯/决策摘要/检索快照；关键环节：5 KPI 卡 + 环节列表 + 详情（代表企业/竞争/技术趋势）；瓶颈：五维确认包 `user_confirmed=true` + 健康度节点（稳健/关注/薄弱/卡脖子）+ 成因建议；记录：任务列表 + 复制配置（`parseChainHistoryDraft` 还原表单）+ 查看结果 |
| `IndustryRegionalView` 区域产业评价 | `IndustryRegionalPage` | 单/多产业模式（1产业×5城市 / 5产业×1城市）；官方/个人模板（`chainRegionalTemplates*` 真接口 + 保存个人模板）；指标勾选/添加/移除 + 一键均分；竞争力三维修可调权重；结果：排名卡/综合指数/四力维度/竞争力条形图/优势短板 |
| `IndustryShenzhenView` 深圳产业分析 | `IndustryShenzhenPage` | 对比：1–5 标杆（就绪校验、未就绪自动剔除并提示）+ 四维只读权重 → 维度对比表/独特优势/差距/劣势/发展阶段；发展：绑定有效**同产业**对比结果（`source_result_id`，跨产业配置期拦截 `SOURCE_INVALID`）+ 政策/技术/人才目标 → 三类建议 + 发展路径；对比完成自动写 sessionStorage 供发展页带入 |

### 基础设施（随本批新建/重写）

- `src/components/visualization/ChainAnalysisShell.vue`：I2-12 完整闸门（切条件不自动 create / 同参在跑接续 / 当天成功直接看结果 + 重新分析）；真任务创建 `buildChainCreateRequest`；轮询 + asset 大结果回退 + 取消；`showExternalResult`（记录页查看结果注入结果态）；`object` prop 支持异步（全景 asOf 预取）
- `src/api/industry/chainUx.ts`：#U5–U9 查询辅助 + #U13–U17 区域模板端点
- `src/config/industryWorkspace.ts`：工作区配置契约（analysisType/阶段文案/周期参数/区域选项/深圳标杆树/权重合并）
- `src/utils/industryChainTask.ts`：结果解析器全集（`parseCycleBoard`/`parseKeyLink*`/`parseBottleneck*`/`parseRegionalBoard`/`parseShenzhen*`）+ 请求构造 + 错误码映射
- `src/utils/industryAnalysisGate.ts`：I2-12 指纹闸门
- `src/utils/industryWorkspaceRuntime.ts`：任务配置清洗/历史草稿还原/关键环节详情/全景 asOf 推导
- `src/stores/industryWorkspaceMeta.ts`：#C1 工作区字典（评价城市/标杆/年窗/权重）
- `src/api/enterprise/analysisTask.ts` 扩展：cancel/events/running/asset JSON

### 评审模式清理（用户 2026-11-12 追加指令）

- `.env.development` / `.env.production` / `.env.example`：`VITE_REVIEW_MODE` → `false`
- `StatCard.vue`：`.stat-card__markers` 包裹层加 `v-if="reviewMode"`（关闭后 DOM 零泄漏）
- `EnterpriseEvaluationView.vue`：直接引用的 `MetricMarker` 加 `v-if="reviewMode"`
- 复刻的 6 页确认未引入任何 ReviewMount/MockBadge/data-frame-id 挂载

## 架构合规

| 铁律 | 状态 |
|------|------|
| D12 不 merge demo / 不调 demo 服务 | ✅ 只读对照 PC 仓后重写 |
| 调用链 前端 → Java REST | ✅ 全部真实端点（chain/topic/v1/*、analysisTask*） |
| Mock 开关 | ✅ `USE_MOCK=false` 真实数据；mock 模块不参与 |
| 评审模式 | ✅ 按用户指令忽略：env 关闭 + 组件双重门控，DOM 零泄漏 |
| I2-12 异步分析工作区 | ✅ Shell 完整闸门（不自动 create/单飞/当天复用/重新分析） |
| D9 ⓘ 角标 | ⚠️ 按用户指令「可忽略评审模式」关闭；组件保留未删，上线清理时统一处理 |

## 测试结果（2026-11-13 本地）

- `pnpm type-check` ✅ exit 0
- `npx eslint src/views/industry/ src/components/StatCard.vue` ✅ 0 error
- `pnpm test` ✅ 42/42 通过
- `pnpm build-only` ✅ 构建成功（ChainPanoramaGraph chunk 1.4MB 警告为 G6 既有情况）
- 顺带修复：overview 页 Vant 4 不存在的 `van-timeline` 组件导致 build 炸点

## 遗留风险

- 门户权限拦截（`?noPerm=1`）：服务端 `get-permission-info` 菜单数据需含对应 nav path，前端拦截逻辑正确——需门户菜单配置侧给账号授权
- 政策批 2 仅基础壳（3 分析叶 + 门户/列表页），深圳权重工作台、报告章节按 §10 红线不进小屏
- 深圳对比标杆树为静态配置（对齐 PC `SHENZHEN_BENCHMARK_TREE`）；meta benchmark items 恒空（Q016 未定）

## CI/CD

- 分支：`dev`
- commit：见下方提交记录（本 handoff 同步提交）
- pipeline：push 后 GitLab CI 自动触发（lumen-ui-topic-mobile）
- dev URL：本地 `pnpm dev`（3101）；线上 `https://edu.itic-sci.com/tts/msvcz/`

## 涉及文件（23 改 + 6 新）

修改：`.env.{development,production,example}`、`auto-imports.d.ts`、`components.d.ts`、`api/enterprise/{analysisTask,types/analysisTask}.ts`、`api/industry/{index,paths,types}.ts`、`components/{StatCard,visualization/ChainAnalysisShell}.vue`、`portal/perms.ts`、`router/index.ts`、`shell/MobileShell.vue`、`views/enterprise/EnterpriseEvaluationView.vue`、`views/industry/Industry{Overview,Search,Panorama,Diagnosis,Regional,Shenzhen}View.vue`、`views/policy/PolicyAnalysisConfigView.vue`

新增：`api/industry/chainUx.ts`、`config/industryWorkspace.ts`、`stores/industryWorkspaceMeta.ts`、`utils/industry{AnalysisGate,ChainTask,WorkspaceRuntime}.ts`
