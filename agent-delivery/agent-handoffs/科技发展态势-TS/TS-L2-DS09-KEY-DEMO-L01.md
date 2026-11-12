# TS-L2-DS09-KEY-DEMO-L01 · 重点领域规划 demo 库部署版（handoff）

> 完成时间：2026-11-11 ｜ 执行：agent:zcode ｜ 监管：human:淮政玮
> 用户指令：重点领域规划页做成可上线版本，mock 数据库走 demo_gkxlumenx_，丰富前后端调用，代码 review，自己部署供验收。

## 1. 范围与实现（对照需规 seq 185–190）

| 需规叶 | 实现载体 | 本单增量 |
|---|---|---|
| 185 空间布局 / 188 载体分布 | key-areas carriers/carrier_types | demo 库表族 + 载体详情补数列透传（service_capacity/resource_focus） |
| 186 竞争力评估 | competitiveness/dimension/benchmark | district_baselines 附服务端现算 intensity（占最大区比 18-100）/ efficiency（土地行均值，无行 null） |
| 187 土地效益 | land_use | 随表族搬运（无增量，UI 不变） |
| 189 筛选联动 | clusters | **从 FE 本地壳升级为服务端承载**：region/carrier_type/cluster 三 Query（零参调用与 KEY-API §2.9 逐字兼容；出表值域 400） |
| 190 方案模拟 | plans + FE Modal | **新增 GET /key-areas/simulate**（表行静态值线性年化，与 KEY-API delta-3 FE 演示口径同核；基准年读 timeline_meta.current_year 表行；plan_id 不存在 404 / 参数出界 400）。FE 接线，404/失败回落本地公式（旧后端契约行为保留） |

## 2. 数据面（D18 口径）

- `demo_gkxlumenx_ads` 落地 `ts_plan_*` 30 张表：`gkxlumenx_ads`（SEED-L01 实灌库，只读真源）SHOW CREATE TABLE 逐表克隆 + 列交集搬运，逐表行数校验 30/30 OK。
- demo 补数（mock 入库、接口只读表，禁止接口返回写死 mock）：`ts_plan_key_area_carrier` 增列 `service_capacity` / `resource_focus`（仅 demo 库；确定性公式 = 原 FE 演示公式同形，正式态数据侧回填真值即生效）。FE 渲染优先表行值、缺省回落演示公式。
- 脚本：`gkx-orchestration/scripts/ts_plan_seed/seed_demo_warehouse.py`（幂等可重跑；--dry-run / --apply；密码只走环境变量 TS_PLAN_MYSQL_PASSWORD）。

## 3. 后端改动（lumen-svc-platform @ feat/ts09-key-demo-db，3 commits 未 push）

- `PlanningController`：keyAreas 三 Query + simulate 端点（IllegalArgumentException → 400 信封；404 信封）。
- `PlanningQueryService`：keyAreas(region, carrierType, cluster) 过滤（值域以表行真值校验，过滤只作用 carriers 块与 carrier_total，其余块保持全市口径）+ 补数列透传（列缺失键不下发）+ 区县现算指标 + simulatePlan。零参重载保留（ExportJobService 调用点零改动）。
- `JdbcPlanningTableReader`：连接复用（doSelect 串行化 + 共享连接失效重建；跨网段建连 6s×9 表 → 复用后 1.4s/次）。
- 单测：23 个全绿（含新增 keyAreasRejectsUnknownRegion / simulateValidatesAndHandlesMissingPlan）。

## 4. 前端改动（lumen-ui-science-pc @ feat/ts09-key-demo，1 commit 未 push）

- `api/situation/techDevelopmentPlan.ts`：KeyAreasResp 增补数列/现算指标类型；refreshKeyAreaPlanBlock 增 KeyAreaFilterParams（零值字段不下发）；新增 fetchKeyAreaSimulation。
- `views/.../KeyAreaTab.vue`：筛选 watch → 服务端过滤取数（filterFetchSeq 防竞态，失败 Message 告警 + 保留已加载数据）；模拟弹窗打开/目标年切换 → 远端口径（plan_id 对齐消费，null/失败回落本地公式）；USE_MOCK 轨道零改动。
- `models/techDevelopmentPlanModel.ts` + `types`：intensity/efficiency/serviceCapacity/resourceFocus 表行优先、缺省回落原演示公式；展示字段改名 serviceCapacityText/resourceFocusText（与原始值字段分名）。
- type-check（vue-tsc --build）通过。

## 5. 部署与自测证据（本机，验收时仍在运行）

- **后端**：`http://localhost:7099`（jar = worktree `D:/gkx-lumen/wt/ts09-key-demo/gkxlumen-display/target/gkxlumen-display.jar`；ads-url 指向 demo_gkxlumenx_ads；本地验收专用启动参数：nacos 关闭 / redis-listener+tenant 过滤 exclude / ignore-urls=/v1/** / direction-alert.registered=true）。
- **前端**：`http://localhost:3000`（vite dev；`.env.development.local`：VITE_APP_API_URL=http://localhost:7099/ + VITE_ENABLE_MOCK_AUTH=true，登录页默认账号点登录即 mock 会话）。
- 接口自测（python urllib，UTF-8）：
  - key-areas 零参：carrier_total=22 / plans=3（原契约兼容）
  - region=南山区：total=9 全南山 ✓；南山区+lab：3 行（鹏城/深圳湾/人工智能与数字经济实验室）✓；cluster=ai：6 ✓
  - 出域 region/carrier_type/cluster → 400 ✓；simulate 缺参/出界 400、plan_id 不存在 404 ✓；simulate a@2028 → 37.2/46.4 ✓ b@2029 → 68.7/59.4 ✓
- 浏览器端到端（IAB）：登录 → 重点领域 tab 全数据块渲染；方案 A「查看建议」弹窗 2028 → +37.2%/-46.4%（与后端一致）；切 2030 → +74.4%/-92.8%；规划区域=南山区 → 竞争力卡标题变南山区、载体清单 7 行且服务能力来自表行（腾讯云 76%，FE 回落公式会算 85%，证明走库值）。截图存 `C:\Users\EDY\.zcode\cli\artifacts\...\call_22de6763611f44e1a253d14d-tool-result-*.png`。

## 6. 偏离与说明

1. **未 push**：两业务仓 + 编排仓均为本地 commit（feat/ts09-key-demo-db / feat/ts09-key-demo / dev@90ae85db），按铁律待用户确认后推 dev（业务仓 dev 直推策略）。
2. **并行会话冲突处置**：另一 agent 会话在主仓工作区切分支（chore/ci-debug-joblogs），已按宪法 §4.2 冲突例外改用独立 worktree `D:/gkx-lumen/wt/ts09-key-demo`（部署 jar 在用，暂不清理）。
3. **本地验收启动参数不进任何仓**：exclude redis/tenant 自动配置与 /v1/** 匿名仅为本机无 Redis/Nacos 的验收形态；K8s dev 部署走 Nacos 正常配置，无需这些参数。
4. **mock 边界**：demo 补数列仅 demo 库；正式库 gkxlumenx_ads 未动（只读）。D4 就绪度口径不变（表行 source=demo_seed）。
5. **性能**：连接复用后 key-areas 首调 ~8s（含首次建连+30 表共享初始化）、复用 1.4s；K8s pod 内网建连毫秒级，首调即快。

## 7. 架构合规自检（宪法 §2）

- D1 算法只在 Python ✅（Java 只做确定性现算与读表）
- D2 调用链 FE → Java REST ✅（无越层）
- D8 前端规范 ✅（Arco/Vite 栈零新增依赖）
- D18 ADS 表先行 + mock 行入库 + 接口只读表 ✅（无接口写死 mock）
- D12 正式仓隔离 ✅（lumen-* 仓无 demo-* 依赖）
- 人机协作 3/6/7 ✅（commit 标注 / 本 handoff / cost 待回填见下）
