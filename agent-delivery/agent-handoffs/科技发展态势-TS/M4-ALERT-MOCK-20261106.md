# M4 全球创新监测 · 预警（alerts）演示数据留痕

> **任务**：M4 `POST /v1/situation/global-innovation/alerts` 数据 mock（建表 + 填数 + 留痕）
> **发起**：`human`（当前会话）2026-11-06
> **仓**：`lumen-svc-platform`（SQL / upms / display）、`lumen-ui-science-pc`（类型 / api / 页面角标）
> **状态**：代码完成，未 commit 未 push（等用户确认）

---

## 1. ⚠️ 一句话结论

**「创新预警」区块当前展示的全部是 mock 演示数据，不是真实数仓预警结果。**
数据落在 upms 主库 `gkxlumenx.sys_innovation_alert_mock`，每行 `is_mock=1`，
接口响应固定带 `mock=true` / `mockVersion` / `mockNote`，
前端「创新预警」标题旁展示 **「演示数据（Mock）」** 角标（`IconExperiment`）。

> 走查 / 验收 / 截图汇报时必须带上这句，**不得把 mock 预警当作真实监测结论**。

---

## 2. 为什么 mock

- 数仓侧**没有预警结果表**（原 `/alerts` 恒返回空列表 + `emptyReason=NO_SOURCE_COLUMN`）；
- 写面端点（`alerts/{id}/read`、`monitor/subscriptions`、`push-records`）按 U5 已 deferred 到二期；
- 「创新预警」区块长期空态，`human` 2026-11-06 要求先用 mock 把区块填起来并留痕。

---

## 3. 建表 + 数据

**迁移文件**：`repos/lumen-svc-platform/db/migration/20261106_m4_alert_mock.sql`

- 表：`gkxlumenx.sys_innovation_alert_mock`
- mock 标记列：`is_mock`（恒 1）、`mock_version`（`M4-ALERT-MOCK-V1`）、`mock_reason`
- 数据：**6 条**，覆盖三类
  | alert_no | level | type | 主题 |
  |---|---|---|---|
  | M4-ALERT-0001 | urgent | threshold | 深圳人工智能专利授权量突破阈值 |
  | M4-ALERT-0002 | important | threshold | 创新价值评估样本量低于阈值 |
  | M4-ALERT-0003 | important | trend | 量子信息创新点发现连续三周上行 |
  | M4-ALERT-0004 | normal | trend | 生物医药创新价值均值短期回落 |
  | M4-ALERT-0005 | normal | relation | 深圳—香港机构合作论文密度上升 |
  | M4-ALERT-0006 | normal | relation | 深圳与班加罗尔城市排名交叉风险 |
- 幂等：`CREATE TABLE IF NOT EXISTS` + `INSERT ... ON DUPLICATE KEY UPDATE`（`alert_no` 唯一）
- **执行状态（2026-11-06 已执行）**：在 dev 库 `10.50.11.76:3306 / gkxlumenx`（MySQL 8.0.39，host `node03`）执行完成，客户端 `mysql --defaults-extra-file`（口令取自本机 `C:\Users\35197\.cache\gkx-lumen\my.cnf`，不在仓库、不进 git）。
  - 回读核对：`COUNT(*)=6`、`SUM(is_mock='1')=6`；6 条中文标题无乱码；`uk_alert_no`（唯一键，cardinality 6）与 `idx_module_time(module_code,del_flag,trigger_time)` 均在。
  - 幂等复跑：再次 `source` 同一脚本，行数仍为 6（`ON DUPLICATE KEY UPDATE` 生效）。
  - ⚠️ 到此为止只证明「表已建、数据已灌」；链路是否读得到还依赖 upms 起来（见 §6）。

---

## 4. 读取链路

```
前端 POST /display/v1/situation/global-innovation/alerts
  → display GlobalInnovationController#alerts()
  → Feign RemoteUserBehaviorService#listMockAlerts("M4")（@NoToken）
  → upms SysUserBehaviorController#listMockAlerts（@Inner /user/behavior/alert/mock-list）
  → SysInnovationAlertMockMapper.selectList（sys_innovation_alert_mock）
```

> display 模块 pom **无 mybatis/jdbc 依赖**，不直连 DB，只能走 upms Feign（与订阅规则同链路）。

**改动清单**

| 层 | 文件 | 动作 |
|---|---|---|
| SQL | `db/migration/20261106_m4_alert_mock.sql` | 新建：建表 + 6 条 mock |
| upms-api | `.../api/entity/SysInnovationAlertMock.java` | 新建实体（**不加 `@TenantTable`**：全局演示数据） |
| upms-api | `.../api/feign/RemoteUserBehaviorService.java` | 新增 `listMockAlerts` |
| upms-biz | `.../mapper/SysInnovationAlertMockMapper.java` | 新建 Mapper |
| upms-biz | `.../service/SysUserBehaviorService.java` + `impl` | 新增 `listMockAlerts` |
| upms-biz | `.../controller/SysUserBehaviorController.java` | 新增 `@Inner /alert/mock-list` |
| display | `.../controller/GlobalInnovationController.java` | `alerts()` 由「写死空列表」改为读 mock 表，透出 `mock/mockVersion/mockNote` + 逐条 `isMock/mockReason` |
| 前端类型 | `src/types/situation.ts` | `InnovationAlert` 加 `metricId/isMock/mockVersion/mockReason`；dataset 加 `alertsMock/alertsMockNote` |
| 前端 api | `src/api/situation/globalInnovation.ts` | 新增 `/global-innovation/alerts` 调用 + 映射 |
| 前端页面 | `views/situation/global-innovation/tabs/InnovationMonitor.vue` | 「创新预警」标题旁「演示数据（Mock）」角标 + 空态文案改真 |

---

## 5. 清理条件（真实源就绪后）

1. 数仓产出真实预警结果表 / 算法侧上线预警模型 → 后端 `alerts()` 切源，删除 `mock/mockVersion/mockNote` 与逐条 `isMock`；
2. 前端删除「演示数据（Mock）」角标与 `alertsMock*` 字段消费；
3. 手工 DROP `gkxlumenx.sys_innovation_alert_mock`，删除 `db/migration/20261106_m4_alert_mock.sql` 的建表与数据段（保留迁移历史时改为注释下线）；
4. 检索归零：`sys_innovation_alert_mock` / `M4-ALERT-` / `alertsMock`。

---

## 6. 验证状态

- 前端 `type-check`：见本会话运行记录（`$env:npm_config_engine_strict='false'; pnpm run type-check`）。
- 后端编译：`gkxlumen-upms-api` / `upms-biz` / `gkxlumen-display` 均可编译（JDK17）。
- 建表/灌数：**已执行并回读核对**（2026-11-06，dev 库 `gkxlumenx`，6 条、`is_mock` 全 1，幂等复跑通过）——见 §3。
- **未做**：`alerts` 的 HTTP 端到端（本机 upms 未起，Feign 不可达 → display 返回 `DOWNSTREAM_UNREACHABLE` 诚实降级）。页面实跑还需：起 upms → 起 display → 前端 `pnpm dev`。
- 已做：创新价值评估 `POST /v1/situation/global-innovation/innov-value` 的 HTTP 端到端（直探 :7099 与 vite 代理均 `code=0`、`candidates=20`、`supportJudgment=部分支持`）。

---

## 附录 · 算法侧「创新价值评分 / 四维评分」支撑检查（2026-11-06，v2 修正）

> **结论（v2）**：**有真实实现**——`M_INNOV_POINT_VALUE` 在 precompute 批处理层有一份
> **真实算过的三维评分结果**（2026-10-23 产出，非 mock），单指标 compute 接口可直接取到；
> 但算法自评 `support_judgment = 部分支持`（影响潜力维基本缺测）。四维评分（科学/技术/产业/政策）仍无 M4 模型。

### 1. 有真实算法：precompute 批处理产出

`demo-algo-science/data/precompute/M_INNOV_POINT_VALUE.json`（generated_at 2026-10-23 23:57:24）：

- **三维评分公式（真实实现，非占位）**：
  - 新颖性 = `1/(1+T−t0)`（burst/新词强度）
  - 影响潜力 = 关联成果被引合计
  - 成熟度 = 授权专利 / 专利数
  - 同 point_type 内极值归一（0—100），缺测维重归一
- **实际产出规模**：ipc4 33 个候选、keyword_patent 6,498 个、keyword_paper 2 个，均带 value_score；
- `compute_metric` 路由（`metrics.py`）：REAL_CALC_OVERRIDES（该指标未注册）→ **precompute 命中** →
  `POST /v1/innov/metric/M_INNOV_POINT_VALUE/compute` 返回 `data_source=precompute, confidence=high` 的真实结果；
- 同义指标 `M_INNOV_DS_04_MONITOR_002` 也有 precompute 文件。

### 2. 算法自评「部分支持」——数据侧局限（文件内 reasons 如实记录）

| 维度 | 状态 | 原因 |
|---|---|---|
| 新颖性 | ✅ 可算 | 但专利基窗 2017—2020 零行，词条「新/突现」只有 2021 基线 |
| 影响潜力 | ⚠️ 基本缺测 | `dwd_patent_cited` 与主表仅 2.28%（467/20,515）可连；论文侧有「年份+被引」的只有 799 篇（0.79%）→ **两源被引都不成立**，结果里 `n_with_influence=0`（ipc4） |
| 成熟度 | ✅ 可算（限专利侧） | 来自 6.80% 主键切片；论文词条无授权概念，恒缺测 |

> 结论：M4 若接这份结果，必须按**「部分支持 / 待核验」**口径展示：标注 `data_source=precompute` +
> `support_judgment`，且影响潜力缺测的词条只展示已算维度，不得补 0 或伪造三维齐全。

### 3. 其余两层（诚实口径）

| 层 | 状态 |
|---|---|
| `spec_specs.py` SPEC 定义 | ⚠️ **兜底占位**：三维 SQL 完全相同（`dwd_patent` 按 `pn` 的 COUNT(*)），等权。因 precompute 优先命中，正常不会走到；仅 precompute 文件缺失/失败时才会降级到它 |
| `batch-compute` 接口 | ⚠️ 计算失败时返回**确定性伪值兜底**（`ok=false`）；接批接口必须校验 `ok`，禁止把伪值当真实分 |
| `calc_logic_ref` 引用的 `metrics/calc-logic/INNOV/M_INNOV_POINT_VALUE.md` | ❌ 文件不存在（目录登记引用了，实际缺失） |
| `catalog.py` 登记 | `mapping_status='⏳'` + `pending_ref='GAP-ALGO-TYPE-UNSIGNED'`（算法类型未签署，与「部分支持」自评一致） |

### 4. 四维评分（科学 / 技术 / 产业 / 政策）—— 无 M4 模型（结论不变）

- 四维是 **M7 评估体系（DS-07）** 的划分，不是 M4 创新点评分；M7 snapshot 明确 **不计算总分**；
- M4 若要有四维条，需产品先定义维度口径/权重/数据源，再让算法侧建模型。

### 5. 待裁决（v2 更新，2026-11-06 当日已裁决）

1. ✅ **M4「创新价值评分」接算法侧 precompute 结果**（human 2026-11-06 当日裁决「接」），
   必须标注「部分支持 / 待核验」+ `data_source=precompute`，缺测维度不补 0 —— **已实现**（见 §6）；
2. 四维条是否保留 —— 当前无模型，建议先不展示或按诚实空态处理（未裁决）；
3. 建议给算法侧提缺口单：①补 calc-logic MD；②`GAP-ALGO-TYPE-UNSIGNED` 签署；③影响潜力维数据血缘（patent_cited 关联率 2.28%）。

### 6. 创新价值评分接线实现（2026-11-06，裁决「接」后同日交付）

**链路**：前端详情抽屉（创新点发现 → 「创新价值评估」）懒加载
`POST /display/v1/situation/global-innovation/innov-value`
→ display `GlobalInnovationController#innovValue`
→ Feign `RemoteAlgoScienceClient#compute`（已有 client，无新增）
→ 算法库 `POST /v1/innov/metric/M_INNOV_POINT_VALUE/compute`（precompute 命中，真实结果）

**诚实性处理**：

- 后端压缩提取（不透传 6,498 条全量 JSON）：三类 `result.*.top` 合并按综合分降序截 Top20，
  附 `typeStats`（n_candidates / n_with_influence / n_with_maturity）与 `reasons`（算法局限原文）；
- 响应带 `honestyNote`（影响潜力维血缘不足说明）+ 逐词条三维分；
- 前端抽屉：「部分支持 · 待核验」橙色角标（`a-tag orangepremium`）+ 来源/产出时间行 +
  当前创新点词条 best-effort 匹配卡（中文关键词包含即命中，IPC4 不参与；无匹配如实不显示）+
  全局 Top10 表格（**缺测维度显示「缺测」，不补 0**）+ 可折叠「模型支撑度说明」（算法 reasons 原文）；
- 算法库不可达 / 无结果时回退占位文案（「不以伪值兜底」），**不回退**到任何伪分。

**改动文件**：

| 层 | 文件 | 动作 |
|---|---|---|
| display | `GlobalInnovationController.java` | 新增 `/innov-value` 端点 + `innovValuePayload` 压缩提取；注入 `RemoteAlgoScienceClient` |
| 前端 api | `src/api/situation/globalInnovation.ts` | 新增 `InnovValueCandidate` / `InnovValueResult` 类型 + `fetchInnovValue()`（失败返回 null） |
| 前端页面 | `tabs/InnovationMonitor.vue` | 抽屉「创新价值评估」区接真实评分（角标 / 匹配卡 / Top10 表 / 缺测不补 0 / 支撑度折叠说明） |
