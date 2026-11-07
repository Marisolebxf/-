# 门户专题服务（SVC-PT）· LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 任务：`SVCCHAIN-DC-M3-PT-L01`（长任务总控 `SVCCHAIN-合规演示用例-长任务总控.md` §4；本计划为 M3d 产物，只写不建单）
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-PT-合规演示用例.md`
- 系统：科技信息展示系统 · 智慧服务门户「专题服务」。不打开页面。
- 监管人：`human:徐滕强`
- 日期：2026-11-07

- 状态：**2026-11-07 第 1 轮已跑：样本未满足；停止=ENV（步①探测 200 正常，步②只读库 `demo-gkxlumenx-ods`→`demo_gkxlumenx_ads` SELECT 连续失败 2 次即停，步③④未执行）；11 行均未判定，双轨核对顺延；读过任务号 SVC-PT-DEMO-ACCEPT-LOOP（claimed，状态未动），本轮 0 张子任务；报告已追加 `agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-PT-DEMO-ACCEPT-LOOP.md`；验收单维持 claimed 等监管人处置（未改 ready/blocked，未签 done）。等连接恢复后重说「按 LOOP 跑」。**

覆盖表 11 行全部「可演」（其中 8 行期望值=前端确定性聚合常量；全球/类型/规模/区域/领域×环节等口径行与库侧 ADS 面、机构卡面存在**两轨差异**，已在用例「数据情况」列如实标注）。覆盖不到的行不存在，但**口径接线核对**在按 LOOP 跑时才逐行做；不派数据单，不派算法单，不打探测。

## 1. 常驻验收单（建议 ID，本计划只写不建）

- 建议 ID：`SVC-PT-DEMO-ACCEPT-LOOP`（§6.5.2；等人说「按 LOOP 跑」后由 coordinator 建，不把这张单签 `done`）
- 建单前置：总控 `SVCCHAIN-合规演示用例-长任务总控.md` 仍在授权期内；M3d 产物已签收
- 建单后必填：`claim_type=coordinator_dispatch`、`supervised_by=human:徐滕强`、`task_type=chore`（跑批性质，豁免签收）

## 2. 先决条件

1. 用例文件（上文路径）已签收且本轮未被改动；查库节时间戳之后 `svc_metric_*` / `svc_region_dist` / `svc_chain_gap` 无重新灌批（`etl_batch_id` 仍为 `svc-fseed-20261020` / `svcmodels_20261107_155402`）。若发生重灌，先重跑一轮探测再对照。
2. 库入口连接可用：database-mcp 组 `gkx-mysql` → `demo-gkxlumenx-ods`（跨库限定名查 `demo_gkxlumenx_ads`）。**严格只读**；SELECT 失败 2 次 → 该步记受阻即停，禁止探活。
3. 前端真源只读对照仓 `repos/demo-ui-topic`（`src/app/pages/service-portal/*`）在本地可用，仅作常量值核对，不改代码。
4. 页面可达性探测属 LOOP 轮次内动作，本计划不预检。

## 3. 纯后端 token 熔断约定

- token 文件：`~/.gkx/topic-loop-token`
- 轮次内所有后端请求头带 `systemCode: topic`
- 每轮开工先校验 token 文件存在且未过期；缺失/过期 → 该轮记 ENV 缺口即停，不重试 token 获取
- token 值不入档、不写进报告（脱敏铁律）

## 4. 一轮四步（每轮）

| 步 | 动作 | 产物 |
|---|---|---|
| ① 探测 | 校验 token + `systemCode: topic` 后端会话可用；只探测本轮清单涉及的门户页面路由（`/service-portal/*`），不打全量 | 轮日志·探测节 |
| ② 只读库+调接口 | 按本轮行清单：SELECT 对应 ADS 面（只读）+ 调页面读数（GET 只读）；对照用例「期望输出」列逐值核 | 轮日志·对照节（逐行 差值/一致） |
| ③ 对照 | 期望值 vs 实测值：页面常量轨 vs 库 ADS 轨两轨差逐一登记（重点=97/98/99 类型规模两轨、33.3 区域两轨、103 十区缩放比） | 差异清单（分缺口类型） |
| ④ 缺口分类 | 每条差值落 DATA / QUERY / ALGO / ENV 四类之一（§5 表），不新造编号，引用 Q-SVCCHAIN-01/06/07/08/09、Q-SVC-010、GAP-SVC-* 既有集合 | 分类结论 → 决定是否开子任务 |

一轮四步走完即收轮；不做步⑤「顺手修」。每轮 ≤3 张子任务（见 §6）。

## 5. 缺口分类表（本轮预判，执行时按实测修正）

| 缺口现象（预期） | 分类 | 既有引用 | 处置 |
|---|---|---|---|
| 97/98/99/33.3 页面常量值与库 ADS 面值不一致（类型全塌企业、规模档距大、区域 12 国 vs 5 国 150 行种子） | **DATA**（ADS 面与前端常量未对齐；全球名录无源） | Q-SVCCHAIN-06、Q-SVCCHAIN-07 | 登记差异清单；不修前端常量、不造国家真值；等甲方口径 |
| 页面统计全部读前端常量、未接 `/metrics/v1/catalog` 或 Java REST | **QUERY**（接线缺口） | Q-SVCCHAIN-06 临时基线（「圈定池确定性聚合写 svc_metric_*」） | 建接线核对子任务（只核对，不改业务仓代码——改码需另派前端任务） |
| `svc_metric_series.M_SVC_PT_SZ_TOTAL` 近年非年增量（2025=423、2026=14）与「本年新增=相邻年差」口径矛盾 | **DATA** | Q-SVCCHAIN-06（本年新增口径已锁） | 登记 series 灌数口径差，不灌数 |
| 102/33.2 领域×环节计数无库源（仅 `svc_chain_gap` 六环节堵点面） | **DATA**（事实表缺） | Q-SVCCHAIN-08 | 诚实空/常量演示维持；不建新表（建表=另行立项，非 LOOP 动作） |
| 33.4 榜单与 `svc_tech_power_score` 300 行恒定分（40/20）无个体区分度 | **ALGO**（评分模型区分度） | Q-SVCCHAIN-01、CT-SVC-PT-03 | 榜单维持分析侧 `computeEvaluation` 复用；模型升级不在 LOOP 内 |
| 页面路由不可达 / token 失效 / 库连接拒 | **ENV** | as-built `ENV-SVC-PORTAL-*` 票 | 记受阻即停轮；不探活、不重试第三轮 |
| 104 扩展档案（领导人/人数/营收）无库源表 | **DATA** | Q-SVCCHAIN-06（重点机构扩展档案） | 卡面 `svc_org_card.employees_number/operating_revenue` 可对标；差异登记，不灌 |

## 6. 子任务规则

- 每轮最多 **3 张**，ID 形如 `SVC-PT-DEMO-FIX-R{YYYYMMDD}-*`（R+轮次日期；`*`=缺口关键词，如 `TYPE-DIST` / `WIRE-TWO-TRACK`）
- 子任务只做核对/登记/报告，**不派修数单、不派前端改码单**（那是 LOOP 之外的正常任务流）
- **同缺口连续两轮不收敛 → 停**：第 3 轮起不再为该缺口开子任务，升级监管人 `human:徐滕强`，该缺口在报告挂「两轮停」标记
- 子任务创建动作（task-create）在建单之后由 coordinator 执行；本轮计划不建任何单

## 7. 库表清单（引用 M2 调研 + M3d 查库节）

| 面 | 表（`demo_gkxlumenx_ads`，跨库限定名） | 用途 |
|---|---|---|
| 全球总量 | `svc_metric_series`（metric_id=`M_SVC_PT_GLOBAL_TOTAL`） | 97 趋势两轨核对 |
| 全球当期 | `svc_metric_fact`（43296 / slice=all） | 97 KPI 对照 |
| 类型/规模分布 | `svc_metric_dist`（`M_SVC_PT_GLOBAL_TYPE_DIST` / `M_SVC_PT_GLOBAL_SCALE_DIST` / `M_SVC_PT_SZ_TYPE_DIST`） | 98/99/101 两轨核对 |
| 区域 | `svc_global_dist`（5 国种子面板）/ `svc_region_dist`（province 3 省 + sz_district 9 区） | 33.3/103 两轨核对 |
| 深圳总量 | `svc_metric_series.M_SVC_PT_SZ_TOTAL` / `svc_metric_fact`（14033 / slice=city） | 100 两轨核对 |
| 环节 | `svc_chain_gap`（六环节堵点面，q061_pending_client=1） | 102/33.2 旁证 |
| 机构卡面 | `svc_org_card`（city=深圳市 14,080 行；`employees_number` / `operating_revenue` / `service_type_candidate`） | 104 对标 |
| 前端常量 | `repos/demo-ui-topic/src/app/pages/service-portal/servicePortalData.ts`（只读） | 页面期望值真源 |

## 8. 报告与状态行

- 报告路径：`agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-PT-DEMO-ACCEPT-LOOP.md`（与验收单同 ID；**只追加**，每轮一节，不回写历史节）
- 报告内容：轮次 / 四步结果 / 差异清单 / 缺口分类 / 子任务 ID 与状态 / 下一轮建议
- 脱敏：token、连接串、口令一律不入报告
- 状态行（本计划）：**覆盖已齐，未执行。等人说「按 LOOP 跑」。**
