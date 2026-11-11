# TS handoff：TS-TALENT-FLOW-RANGE-L01（人才流动监控白板修复 + range 时间窗全链路）

- 时间：2026-11-11
- 会话：agent:zcode（用户直接派单，registry 无既有任务 ID；跨 frontend/api/data 三角色联合作业，用户单点授权）
- 仓库与分支：
  - `lumen-ui-science-pc` @ `dev`（本地 commit，未 push）
  - `lumen-svc-platform` @ worktree `worktrees/lumen-svc-platform--ts-talent-flow-range`，分支 `feat/ts-talent-flow-range`（自 origin/dev 切出；主检出被并行会话 `feat/xxl-job-admin-deploy` 占用，按 multi-session-protection 规约隔离，未 push）
  - `gkx-orchestration` @ `dev`（本 handoff + OV-API §2.5 契约增补，未 push）

## 背景与根因（用户报障两问题）

1. **顶层「时间维度」切换后科技人才流动监控数据无变化**
   - 前端：`timeRange` 仅被「技术与产业热点动态跟踪」消费（`technologyTrendSeriesByRange[timeRange]`）；人才流动块一次性全量拉取后仅按 flow_type 客户端过滤。
   - 后端：`GET /display/v1/situation/planning/talent-flow` 契约（OV-API §2.5）只有 `flow_type`/`risk_level`，无时间参数；表 `ts_plan_talent_flow` record 行无可切片的日期键。
2. **「人才流动方向」白板（TOPS 表有数据）**
   - 线上 records 聚合出 `学术界→产业界 29` + `产业界→学术界 4` 双向链路 → **ECharts sankey 仅支持 DAG**（`sankeyLayout.js:154` 成环直接 throw）→ 整图不渲染，白框 = 空 `.tzp-talent-od-chart` 容器；TOPS 表走独立 `institution_flows` 块故有数据。

## 范围与实现

### 前端（lumen-ui-science-pc）

| 文件 | 改动 |
|---|---|
| `src/views/situation/tech-development-plan/models/planningFilterLive.ts` | `aggregateTalentFlowLinks` 出口改为：类型对**双向净流对冲**（A→B 与 B→A 合并为净流向单边，净值 0 不出边）+ **剥环守卫**（BFS 可达性检环，删环内最小值边并 `console.warn`，兜底三/四节点环）——从根上保证 DAG，宁缺一条边不白屏 |
| `src/api/situation/techDevelopmentPlan.ts` | 抽出 `mapTalentBlock`（records/TOPS/od_nodes 三片映射，buildRealDataset 与重取数共用，消灭双写）；新增 `fetchTalentFlowBlock(range)`（`GET talent-flow?range=3m/6m/12m`，optionalGet 诚实空块模式） |
| `src/views/situation/tech-development-plan/tabs/OverviewTab.vue` | `watch(timeRange)`（real 轨道）→ 重取 talent 块写入 `talentBlockOverride`（三 computed 回落整页 dataset）；失败 `console.warn` 保留当前数据不白屏；桑基副标题「近12个月」写死 → 动态 `talentRangeLabel`（近3/6/12个月）；人才卡挂 `:loading` |
| `src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs` | 净流对冲 / 完全对冲无边 / 三节点环剥离 三组行为断言 + range 接线源码断言 |

自检：`node --experimental-strip-types techDevelopmentPlan.test.mjs` 全过（剥环断言实测触发）；`vue-tsc --build` 绿；eslint（3 个改动文件）绿。

### 后端（lumen-svc-platform / gkxlumen-display）

| 文件 | 改动 |
|---|---|
| `PlanningController.java` | talent-flow 增 `@RequestParam(defaultValue="12m") range`，复用 `OVERVIEW_RANGES` 校验（出枚举 400，先于 flow_type/risk_level 校验）；Javadoc 补 `@param` |
| `PlanningQueryService.java` | `talentFlow(flowType, riskLevel, range, today)` 4 参（`today` 由 Controller 传 `LocalDate.now()`、测试传固定日期保确定性）；`filterRecordsByRange`：`flow_date ≥ today−N 月`，缺 `flow_date` 回落 `updated_at` 前 10 位，双缺遗留行仅 12m 全窗口可见（不造日期）；**stats 的 record 三数（warning_count/方向计数）改按窗口内记录行现算**；records 输出走窗口行 |
| `PlanningQueryServiceTest.java` | 既有 talentFlow 用例改 4 参（固定 today=2026-11-11）；新增 `talentFlowRangeFiltersRecordRowsAndStats`（3m 窗口行序/回落行/双缺行不可见/stats 随窗口收窄/net_inflow 不收窄 断言） |
| `PlanningControllerTest.java` | `enumValidationOnOtherEndpoints` 增 `range=24m→400`、`3m/12m→200` 断言 |

自检：`mvn -pl gkxlumen-display -am test -Dtest='PlanningQueryServiceTest,PlanningControllerTest'` 全绿（含上游模块编译）。

### 数据侧（lumen-svc-platform / db）

| 文件 | 改动 |
|---|---|
| `db/9x_gkxlumenx_ads_ts_plan_ds09.sql` | CREATE TABLE 增 `flow_date date` 列 + `idx_flow_date`（新库直带）；注释同步（record 9 行 / tf-101..109） |
| `db/9x_gkxlumenx_ads_ts_plan_talent_flow_range_alter.sql`（新增） | 幂等 ALTER（information_schema+PREPARE 惯例）+ `row_kind='record'` 行重灌：9 条分时间粒度种子（窗口基准 2026-11-11；3m 4 条 / 6m +3 条 / 12m +2 条；机构对沿用冻结种子语义 + 深圳 3 对扩展；person_count 沿用线上量级）。**stats / institution_flow 全窗口行不动** |

种子窗口预期（供 QA 核对）：3m 学术→产业 24·产业→学术 6·warning 1；6m 32/13/1；12m 41/15/2。

### 契约（gkx-orchestration）

- `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-OV-API.md` §2.5：Query 表增 `range` 行（口径/默认值/400 语义/受影响面逐条写明）。

## 偏离说明

1. **参数命名用 `range` 而非 `period`**：用户原话为「period 参数」；实现取 `range` 对齐同控制器 178 hot-technologies 既有枚举惯例（`range=3m/6m/12m`、默认 12m、出枚举 400，OV-API §2.1），避免同模块两套时间窗命名。如甲方/PM 坚持 `period`，重命名为机械改动（Controller/前端 API/契约三处）。
2. **stats 口径微调**：`warning_count`/方向计数由「全量行现算」改为「窗口内行现算」（随时间维度联动，符合用户预期）；`net_inflow` 维持机构聚合行求和（全窗口冻结行，数据侧未提供分窗机构聚合），已在 Javadoc 与契约行注明。
3. **institution_flows（TOPS 表）/ od_nodes 不随窗口变化**：数据侧为冻结聚合行（U6 机构级 5 行）；用户指令范围为「流动记录」分时间粒度，未扩窗。后续如需 TOPS 分窗，需数据侧加机构×窗口聚合行。
4. **USE_MOCK 轨道不变**：demo 冻结种子无 range 口径，mock 轨道 watch 直接 return（副标题动态跟随，数据冻结——视觉沙箱可接受）。
5. **桑基净流对冲语义**：双向流动展示为净流向单边（差值），非双向双边。demo 写死链路本就无双向形态，real 轨道按「流动方向」语义取净值，孔东口径未见反对记录；如需保双向可改「拆两列节点」方案（改动大，未采用）。

## 验收证据

- 前端：行为断言测试输出 `✅ FE-TS-09A … 全部通过`（含新剥环 warning 日志实测）；type-check/lint 绿。
- 后端：surefire 两测试类全绿（结果见下方「环境插曲」）。
- 种子模拟验证（前端聚合纯函数 × 迁移 SQL 新种子，node strip-types 直跑）：三窗口桑基净值 3m=24 / 6m=28 / 12m=32（互异、全部 DAG 无环）；stats 方向计数 3m 24/6、6m 32/13、12m 41/15（按 flow_type 口径）。
- 线上接口验证（改前）：`curl /tid/api/display/v1/situation/planning/talent-flow` 确认 records 双向链路成环根因。
- 部署后手测路径（QA）：时间维度切 3m/6m/12m → 桑基链路数值变化 + 副标题跟随；人才流动类型筛选不回归。

## 环境插曲（并行会话相关，需 coordinator 知悉）

1. **origin/dev 的 gkxlumen-display 编译不过**：`PolicyPanoramaService` 调 `elementClient.policySupportFactors(id)`，但 `RemoteElementClient`（dev @ a15a0b4）缺该声明。并行会话已建 `fix/display-feign-support-factors`（b7aa052）修复但未合 dev。
   本分支为跑通测试已 `git merge b7aa052`（merge commit 506c48a）——**本分支合入 dev 时会顺带带上该修复**，与修复分支本身合并不冲突（同内容幂等）。
2. **Maven 构建缓存串味**：`~/.m2/build-cache` 把主检出（feat/xxl-job 分支）的陈旧 common jar 恢复进 worktree 导致假编译错；本地跑测试需 `-Dmaven.build.cache.enabled=false`。CI 不受影响。

## 架构合规自检（§2 铁律）

1. 算法只在 Python：✅ 未涉算法（读表聚合在 Java 既有口径内延续）
2. 调用链：✅ 前端 → Java REST（未越层）
3. 图谱：✅ 不涉及
4. 可观测性：✅ 复用既有 defineApi/optionalGet 通道；新增 console.warn 降级路径
5. CI/CD：✅ 本地三检绿；push 后走 Pipeline（待用户确认 push）
6. demo2 只读：✅ 未 merge demo 代码（对照 demo 行为重写）
7. 共享聚合核心：✅ gkxlumen-display 轻 BFF 读 ADS，不直连三方
8. 数据策略：✅ 只动 ADS `ts_plan_` 表（不进 ODS/DWD/供应方库，符合 D18 表形态）
9. D8 前端规范：✅ 无新组件/色值（复用既有 token 与 Arco a-card loading）
10. D9 血缘：✅ metric_id 口径未变；窗口过滤不改指标身份（M_INNOV_PLAN_TALENT_FLOW 8 件套待 data-agent 评审口径行是否需注明 range 维度）
11. D10 交互：✅ loading/空态复用既有模式
12. D12：✅ 走 `/display/v1` 网关语义，无 demo 直连
13-16. ✅ 不涉及（对象存储/缺项/合规算法/签收条件未触及；数据侧为 D18 合规「新表列 + 种子行」通道）

## 待办 / 风险

- ⚠️ **ops 需在 dev 库执行** `db/9x_gkxlumenx_ads_ts_plan_talent_flow_range_alter.sql`（前端 range 切换才有真实分窗数据；未执行前 3m/6m 窗口会因线上旧行无 flow_date 而「只见 12m 全量」，属诚实降级不报错）。
- ⚠️ 三仓 commit 均未 push（工作区铁律：push 前征得用户确认）。
- metric-registry 口径行（M_INNOV_PLAN_TALENT_FLOW）如需补「range 时间窗」维度说明，走 data-agent 正式化流程（本单未动 seed YAML）。
