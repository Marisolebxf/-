# POL-SIM-VIS-FDE-L01 · 233 新出台预测图表化对齐原型（FDE）

- 时间：2026-11-11
- 仓库：`lumen-algo-py` + `lumen-svc-platform` + `lumen-ui-science-pc` + `gkx-orchestration`（用例文档）
- 分支：各仓 `dev`
- 复刻自：`demo-ui-science` `src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx`（只读对照，未 merge）
- 监管：`human:淮政玮`
- 强度：ponytail full；**推送未获当次确认（默认人工确认闸门）**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent`（本会话代跑，CMP-FIX 先例） |
| supervised_by | `human:淮政玮` |
| 说明 | 任务已存在（`task-get` 确认 in_progress），未重复 task-claim；本次回填 evidence/note |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用仓内 `yearPoints`/`namedScorePoints`/`spatialItemsToCities`/`shenzhenDistrictMapOption`/`toShenzhenDistrictName`，只扩格式与补坐标表，未新造组件；YAGNI 未跳过 D9（沿用 D01 真轨先例） |

## 根因

live 模式图表逻辑原本可用，退化为纯文本是**数据格式**问题：`gapfill_policy_sim_forecast` 的 `time_trend_text` / `industry_text` / `space_feature_text` 灌的是整句说明（带「AI推演结果，仅供参考。」），前端解析器 `yearPoints` 等全部匹配失败走文字兜底；且无 `medium_effect_text` / `auto_tags` 列，中期列空、关键词标签缺。

## 修改内容

### lumen-algo-py（数据契约）

- `vendor/entan-py/polan/mockgen/simulation.py`：`_ISSUED_SERIES` 改序列字面量（对齐 demo `policyData.js`：时间趋势 2026-06月45→2027-12月115 六点、产业五档、深圳六区、tags 四枚）；`_ISSUED_TEXT` 与 `_forecast_rows()` 增 `medium_effect_text`（「中期受惠面扩大，申报与兑现形成稳定节奏。」）、`auto_tags`；`self_check_writer()` 断言同步。
- `scripts/seed_gapfill_policy_sim_forecast.py` + `scripts/mysql/gapfill_policy_sim_forecast.sql`：两列进 COLS/DDL/migration/SPECS；`--check` 绿。

### lumen-svc-platform（API）

- `gkxlumen-element/.../PolicySimulationReadController.java`：`FORECAST_COLUMNS` 追加 `medium_effect_text`、`auto_tags`（纯字符串常量，无逻辑改动）。

### lumen-ui-science-pc（前端）

- `simulationLive.mjs`：
  - `yearPoints` 支持「YYYY-MM月数字」月粒度；年/月混排不画（新增守卫）。
  - `namedScorePoints` 月份序列排除同步扩展（`YYYY-MM月` 也算时间序列不算产业柱）。
  - `SPATIAL_CITY_POINT` 补深圳光明/坪山/罗湖/盐田/龙华五区坐标（原仅 4 区，demo 种子六区解析丢 2 个）。
- `EstimateWorkbench.vue` live 233 分支：摘要卡挂 `auto_tags` 标签、中期列读 `medium_effect_text`（替换硬编码空态）、右侧三图改单卡 + computed option（`liveIssuedTrendOption` / `liveIssuedIndustryOption` / `liveIssuedSpaceOption`）；空间图从全国城市柱改深圳区县图（`shenzhenDistrictMapOption`，与 demo 同语义）；解析不出仍文字/空态不编数。
- `simulationLive.test.mjs`：月粒度折线、混排互斥、月份序列非产业柱、深圳六区坐标断言。

### gkx-orchestration（用例）

- `POL-L2-DS12-EST-合规演示用例.md` 233 行（覆盖表 + 主路径）按模板句重冻结：中期效果句、时间趋势/产业影响/空间特征改序列字面量并标注呈现形式（图表呈现/深圳区县图呈现）、关键词标签四枚。

## 自检

| 命令 | 结果 |
|------|------|
| `node src/views/policy/simulation/simulationLive.test.mjs` | ✅ 通过（`simulationLive 条件闭集自检通过`；迭代 4 轮：深圳坐标表、年月混排守卫、测试期望笔误） |
| `python scripts/seed_gapfill_policy_sim_forecast.py --check` | ✅ 绿（上一波次） |
| `pnpm type-check`（`vue-tsc --build`） | ⚠️ **用户裁定忽略本机编译/检查**。实测 exit 2：`EstimateWorkbench.vue(402)` 1 处本叶相关（`rowText` 可能 undefined 传入 `issuedSpatialOption` 参数）、`BenchmarkCompareModal.vue` 2 处非本叶（并行会话未提交文件）。CI 需关注 |
| `mvn` 编译 | ⚠️ 用户裁定跳过（本机 Maven 3.6 过老 + 机器满载）。改动为字符串常量追加 |
| `FE-POL-03A.test.mjs` | 未跑（含并行会话未提交断言改动，机器满载） |

## 测试结果

- 未打线上库：`medium_effect_text` / `auto_tags` 两列需重跑模拟灌数（`seed_gapfill_policy_sim_forecast.py`）后才在 live 生效，DoD §6.5 对照 233 未执行。
- 浏览器点验未做（待 CI 部署后冒烟）。

## 遗留风险

- 233 live 图表卡未挂 🧪 MockBadge（数据源为 gapfill mock 行，D4=mock；沿用 D01 真轨先例，如评审要求补挂为后续小改）。
- vue-tsc 1 处本叶相关类型红未修（用户裁定忽略本机检查）；CI 若红，修法为 `issuedSpatialOption` 参数收窄或调用点判空。
- 前端仓工作区含并行会话未提交文件（`api/policyEvaluationPlan.ts`、`analysis/*`、`panorama/*`），本叶提交已排除，勿一起带上。

## CI/CD（必填）

- 分支：各仓 `dev`
- commit：见下方「涉及文件」对应仓（本地已提交，**push 待监管人确认**）
- pipeline URL / ID：未触发（未 push）
- 部署 namespace / 镜像 tag：未核对
- K8s rollout：未核对
- dev 测试 URL：待 push + CI 后冒烟

## 涉及文件

- `lumen-algo-py`：`vendor/entan-py/polan/mockgen/simulation.py`、`scripts/seed_gapfill_policy_sim_forecast.py`、`scripts/mysql/gapfill_policy_sim_forecast.sql`
- `lumen-svc-platform`：`gkxlumen-element/.../controller/PolicySimulationReadController.java`
- `lumen-ui-science-pc`：`src/views/policy/simulation/simulationLive.mjs`、`simulationLive.test.mjs`、`estimate/EstimateWorkbench.vue`、`FE-POL-03A.test.mjs`
- `gkx-orchestration`：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS12-EST-合规演示用例.md`、本 handoff
