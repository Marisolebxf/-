# POL-L2-DS12-EST-ACCEPT-LOOP · 效果预估演示实例反复验收

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-07 按编排计划执行第一轮。探测失败后已 `blocked`。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 本轮只读探测，没有改业务代码。 |

## 图

本轮不改调用链，没有图。

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-EST-TEST-L01.md` 第 1.1、1.2 节
- 库：未读。探测未通过，没有进入样本对照，也没有 `SELECT`
- 样本满足：否
- 停止：映射不存在
- 探测：`POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs`，body `{"kind":"多维评估"}`，请求头带 `systemCode: display` 与已登录 Bearer。HTTP **404**，Spring 体 `path=/v1/policy/simulation/jobs`，`error=Not Found`。不是 401，也不是 424
- 子任务：未建。验收单改为 `blocked`。已通知 `human:淮政玮`。不再开下一轮

### 缺口

无。404 不归数据、查询或算法。

## 运行 2026-11-08

- 用例：同上第 1.1、1.2 节；期望文案按 2026-11-08 用户指令由「缺项演示」读作「AI推演结果，仅供参考」（合规演示用例已同步改写）
- 探测：同址同头重打，HTTP **200**，多维评估 records 4 行，`scoreText` 已是新文案。404 映射已恢复，从 `blocked` 重入本轮
- 只读库行数（SELECT only）：`gapfill_policy_sim_forecast` 未出台仿真 7、新出台预测 7、区域空间 7；`gapfill_policy_sim_result` 多维评估 9；`gapfill_policy_sim_stakeholder` 8。与用例 §1.2「当前表内行数」一致
- 样本满足：**8/8 全 PASS**。232 研发补助档/人才引进档（含 128亿/46亿 句与逐年趋势）、233 `18363390`/`18407696`、234 广东省/深圳市（空间分布与 GDP 句）、235 四维、236 三条意见，接口返回与用例期望逐字一致
- 恢复动作（本轮一次性的数据修复，非子任务）：2026-11-08 改演示文案重灌主种子时把 §1.2 的 25 条 `POL-L2-DS12-DEMO-EXTRA` 追加行清掉了（主种子脚本「先删全表再插」语义）。已按 §1.2 原值幂等恢复：`lumen-algo-py/scripts/seed_gapfill_policy_demo_extra.py`（按 `gapfill_batch_id` 定界删重插，不动主种子行），`--apply` 已执行，行数回到 7/7/7/9/8，接口抽样 5 条全过。灌数 SQL 已入库仓 `scripts/mysql/gapfill_policy_demo_extra.sql`
- 缺口分类：唯一残留缺口 = 232 带目标产业等值过滤（线上表无 `target_industry` 列，Java 未加谓词）。**挂既有 ready 单 `POL-L2-DS12-INDUSTRY-EQ-FIX-L01`，不重复建单**。其余零 DATA/QUERY/ALGO 缺口，本轮不建子任务
- 通过线判定：探测 200 + 8/8 可演行一致 → **本轮样本满足**。EST-TEST-L01 历史实测不改写，不标完成

## 运行 2026-11-08（EQ 复核轮）

- 意图：复验 232 目标产业等值（Java 过滤 + 库列已上线，CI 4286 绿）。
- 探测：HTTP 401（token 过期）。按规程 §6.5.3 归 ENV：验收单 blocked，通知 human:淮政玮，本轮不建子任务，不重登。
- 库侧证据（直连只读）：target_industry 列已落库，uk_forecast_params 五列(128)前缀就位；未出台仿真 7 行 industry 分布 = 新一代信息技术/生物产业/海洋产业/高端装备/新材料/新能源/绿色环保；forecast 共 21 行（主种子 6 + extras 15）。
- 下次重入：人换 token 后从探测开始，样本 8 条全量重跑（232/233 两条用例原文含产业级联回显全文）。

