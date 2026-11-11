# 政策效果推演页头四卡真轨接口 — 交付报告

> 全栈 agent（api 为主 + 前端接线）· 强度 ponytail full · 2026-11-11
> ⚠️ 状态说明：本任务代码改动在执行期间已被并行会话收编提交（前端 `3922805`、Java `c7b495f`，均为本任务同一工作的产物，内容与本次改动一致）。**本次会话未执行任何 commit / push**，符合任务约束。下文按改动本身描述。

## 一、改动文件清单

### lumen-svc-platform（Java，已进 commit `c7b495f`）
| 文件 | 改动 |
|---|---|
| `gkxlumen-element/.../PolicySimulationReadController.java` | 新增 `SCORE_COLUMNS` / `SCORE_SQL` 常量（与 `STAKEHOLDER_SQL` 同构）：`SELECT ... FROM {gapfill}.gapfill_policy_sim_score WHERE row_kind = ?`，kind=`页面得分` 读 `row_kind='页头卡'` 行，带 `is_mock, metric_id, pending_ref, gap_item, fill_method, gapfill_batch_id, generated_at` 血缘列；表不存在时 `dao.listOrEmpty` 返回空列表（不崩、不编数） |
| `gkxlumen-display/.../PolicySimulationService.java` | `KINDS` 白名单 + `ready()` 加入「页面得分」（无参直通，同利益攸关方） |
| `gkxlumen-element/.../PolicySimulationReadControllerTest.java` | 新增 `scoreKindReadsHeaderRows`：断言 SQL 打 score 表、只读（无 insert/update/delete）、绑定「页头卡」 |
| `gkxlumen-display/.../PolicySimulationServiceTest.java` | 新增 `scoreKindForwardsToElementWithoutParams`：断言 kind 转发 + records 透传 |

编译验证：`D:\maven\apache-maven-3.8.8\bin\mvn.cmd -pl gkxlumen-element,gkxlumen-display -am -DskipTests compile` → **BUILD SUCCESS**（16 modules，注意本机 PATH 默认 mvn 3.6.0 低于插件要求 3.6.3，须用 D 盘 3.8.8）。Feign `RemoteElementClient.policySimulation` 是 kind 透传，无需改。

### lumen-ui-science-pc（前端，已进 commit `3922805`）
| 文件 | 改动 |
|---|---|
| `src/api/policySimulation.ts` | 新增 `PolicySimulationScoreRow` 接口 + `fetchPolicySimulationScore()`（kind=`页面得分`，行含 `metricId/scoreValue/scoreText/isMock/pendingRef`；USE_MOCK=true 经 jobs 返回空） |
| `src/views/policy/simulation/index.vue` | 真轨分支（USE_MOCK=false）：① 前三卡按 `scoreNum(metricId)` 有行出 `PolicyStatCard` 数值、无行空态文案改「**得分待发布（D4 接入中）**」（替换原「没有接口得分」）；② `scorePending()`：`isMock===1 或 pendingRef` 非空时出 ⚠️ 角标（qid 用 pendingRef，无 ref 时占位 `D4-mock`，hint 读镜像 `findPolicyMetric().pendingHint`，不自造文案）；③ 第 4 卡 `stakeholderCount` = `fetchPolicySimulationJob({kind:'利益攸关方'})` 的 records 条数，有数出数、无数空态「暂无意见数据」。Mock 轨种子语义与 `dimsEvalDone` 评审闸门未动 |
| `src/views/policy/simulation/FE-POL-03A.test.mjs` | 新增 3 条断言：得分行渲染（含 API kind / 得分待发布空态 / 禁「没有接口得分」回潮）、is_mock ⚠️ 角标、利益攸关条数；PolicyStatCard 双轨计数改 8 |

## 二、探查结论（Python / 灌数）

- **`gapfill_policy_sim_score` 表不存在**：`lumen-algo-py/scripts/mysql/` 只有 `gapfill_policy_sim_forecast.sql` / `gapfill_policy_sim_result.sql` / `gapfill_policy_demo_extra.sql`（后者建 forecast/result/stakeholder 三表 + 演示行），无 score 表 DDL。
- **无灌数 job**：`lumen-algo-py` 全仓无 `policy_sim_score` 命中；`polan/mockgen/simulation.py` 只灌 forecast/result/stakeholder（232–242 缺项），未产出页头得分。
- **v2 基线已有探测数据**：`vendor/entan-py/data/precompute/M_POLICY_EFFECT_SCORE.json`（v1 三维复现，effect_score=60.3）；镜像 `policyMetricsMirror.gen.ts` 记录 v2 确定性公式「有效率×0.5+力度均值×50」（2026-11-05 淮政玮拍板，QPOL-02 归一中）。**当前线上任何地方都没有 v2 得分落表** → 接口现阶段返回空行，页面显示「得分待发布」是诚实态。

## 三、待办移交清单（data / algorithm agent）

1. **建表 DDL**（在 `gkxlumenx_gapfill` 执行，风格对齐 `gapfill_policy_sim_forecast.sql`，D19：显式 utf8mb4 / utf8mb4_general_ci）：
```sql
CREATE TABLE IF NOT EXISTS `gapfill_policy_sim_score` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `row_kind` varchar(16) NOT NULL COMMENT '行种类；页头卡=页头统计卡',
  `metric_id` varchar(64) NOT NULL COMMENT 'M_POLICY_EFFECT_SCORE / M_POLICY_IMPLEMENTATION_EFFECT / M_POLICY_LAYOUT_REC_COUNT',
  `score_value` decimal(10,4) DEFAULT NULL COMMENT '得分数值；布局建议为条数（可 0）',
  `score_text` varchar(512) DEFAULT NULL COMMENT '一句话说明（可选）',
  `is_mock` tinyint NOT NULL DEFAULT '1' COMMENT 'v2 基线期间恒 1（D4 仍 mock，QPOL-02 归一+QA 后翻转）',
  `pending_ref` varchar(32) DEFAULT 'QPOL-02' COMMENT '口径待确认引用',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_score_metric` (`row_kind`,`metric_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='政策效果推演页头得分（D18 只读 mock 表，不进 ODS/DWD/ADS）';
```
2. **v2 公式灌数 job**（归 algorithm）：按已锁公式「评分=有效率×0.5+力度均值×50」「落地成效=有效政策占比百分数值」「布局建议=对冲计数（诚实可为 0，阈值临时 55.0）」产 3 行 `row_kind='页头卡'`，`is_mock=1`、`pending_ref='QPOL-02'`；幂等 upsert 按 `uk_score_metric`。
3. **QA 核验后 D4 翻转**：甲方归一（QPOL-02）+ 正式灌数 + QA 过 → 行 `is_mock` 置 0、镜像矩阵 d4 翻转，前端 ⚠️ 随 pendingRef 清空自动消失，无需再改前端。

## 四、自检输出尾部

```
FE-POL-03A 自检全绿（49 项：文件清单 / PageTabFrame / 主页面 wiring / Estimate 语义 / Interpret 语义 / 图表族 / 导出 / D9 评审层）
```
（依赖重装后复跑两次均 49/49 绿）

Type-check（vue-tsc --build）：**本任务涉及文件 0 错误**；全仓现剩 2 条错误位于 `src/views/policy/panorama/components/BenchmarkCompareModal.vue`（任务明令禁碰的其他会话在写文件，其收尾提交 6ed642c 尚未覆盖该两处，非本任务引入）。

Java：`mvn -pl gkxlumen-element,gkxlumen-display -am -DskipTests compile` BUILD SUCCESS（用 `D:\maven\apache-maven-3.8.8`；PATH 默认 3.6.0 不满足插件要求）。

## 五、环境修复说明（本次会话副产物，前端仓遗留未提交）

本机 `node_modules` 残缺（约 230 个包目录缺 package.json，pnpm 软链断裂），导致 `pnpm type-check` 一开始 3092 个 TS 错误。已做：
1. `pnpm install --no-frozen-lockfile`（npmmirror 源）全量重装 9m46s 完成——**顺带把另一会话已写进 package.json 的 `html2canvas`/`jspdf` 补进了 `pnpm-lock.yaml`**（lockfile +145 行，安装必需）。
2. `pnpm-workspace.yaml` 被 pnpm 自动补了 `packages: - .`（3 行；缺它 pnpm 所有命令直接报 `packages field missing or empty`）。

前端仓当前未提交遗留：`package.json` / `pnpm-lock.yaml` / `pnpm-workspace.yaml`（环境修复+他会话依赖）+ `src/views/policy/analysis/**`（他会话在写）。均未提交、未 push，请监管人定夺。
