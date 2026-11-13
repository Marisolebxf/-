# POL-L2-DS11-REPORT-CARD-DEF-L01 · 分析报告卡口径定义与真轨接线

> [agent:coordinator]（FDE 总控，data/frontend 波次同会话代执行）· 监管 human:淮政玮 · in_progress → ready_to_sign · 2026-11-12
> ponytail: full —— 最小 diff：seed 脚本补一行 + FE 真轨分支换标准得分卡，零新表零新依赖零新文件（除本 handoff）

## 1. FDE 判类与口径定义（波次 A）

监管人原话：「分析报告 报告份数无读面出处 需要产品先定义一下，FDE 完成」。按规程 §4.2.0 判为**需求**（产品定义口径 + 实现），走 FDE。

**决策卡（2026-11-12，AskQuestion 四选一，用户选定「种子实算」）**：

| 选项 | 结论 |
|---|---|
| **✅ 种子实算（选定）** | 口径 = 平台累计生成分析报告份数；sim_score 表补 `M_POLICY_REPORT_COUNT` 行，is_mock=1 + QPOL-02 ⚠️，与其他 5 卡机制统一 |
| 真实读面改义（模板数） | 未选——「模板数」≠「报告份数」，语义不符 |
| 导出事件计数 | 未选——中档工作量（新表需数据 Owner），演示初期恒 0 |
| 维持空态 | 未选 |

需规依据：SRS 1325（政策分析评价该叶）无「报告份数」指标——此卡系 demo 自加元素，口径此前从未定义；本次以 FDE 决策卡补定义，数值挂 QPOL-02 伞待甲方确认。

## 2. 实现（波次 B/D，单会话按依赖顺序）

### data 波次（`lumen-algo-py/scripts/seed_policy_sim_score.py`）

- `compute()` 追加第 6 行：`M_POLICY_REPORT_COUNT`，score_value=128（对齐 Mock 契约种子值，双轨视觉一致），score_text 注明口径来源与「导出事件流未持久化暂取种子值」
- `check()`：行数断言 5→6 + 报告份数 `isinstance(int) and >= 0` 断言
- `apply()` / `verify()`：目标行数 5→6；verify `need` 集合加 `M_POLICY_REPORT_COUNT`
- docstring 口径表补第 6 行

### frontend 波次（`lumen-ui-science-pc/src/views/policy/analysis/index.vue`）

- 真轨分支：恒空态卡（「报告份数无读面出处」）→ 标准 `PolicyStatCard`（`scoreNum('M_POLICY_REPORT_COUNT')` 接线 + `scorePending` ⚠️ 角标，suffix=份，色 #165dff 与 Mock 轨一致）
- 无行兜底空态：文案改「报告份数待发布」（与焦点指数等「得分待发布」同语义族）
- Mock 轨分析报告卡补 `metric-id="M_POLICY_REPORT_COUNT"`（历史遗漏，双轨 6 metric-id 对齐）
- `FE-POL-02A.test.mjs` 断言同步新口径：真轨 6 卡（原 5）、双轨 12 metric-id（原 11）、REPORT_COUNT 接线、旧恒空态文案防回归

## 3. 灌数执行结果（✅ 2026-11-12 19:4x 直连 10.50.11.76）

- `--apply`：6 行 upsert 成功（`M_POLICY_REPORT_COUNT=128.0000`，is_mock=1，QPOL-02）
- `--verify`：独立连接 `ok=true, row_count=6`，六 metric_id 齐

## 4. 验证与产物

| 项 | 结果 |
|---|---|
| seed 编译 / apply / verify | ✅ compile OK / 6 行 / ok=true |
| `pnpm type-check` | ✅ 0 error（两次复跑） |
| `FE-POL-02A.test.mjs` | ✅ 35 组全绿 |
| `POL-L2-DS11-VIZ-WIRING.test.mjs` | ✅ 29 项全绿 |
| commit | `lumen-algo-py@7d722b4`、`lumen-ui-science-pc@51e1f78`（均 origin/dev，例外 C 免确认） |

FE 点亮：刷新政策分析评价页，「分析报告」卡显示 **128 份** + ⚠️ 角标（点 ⓘ/⚠️ 见口径说明与 QPOL-02 引用）。

## 5. 架构合规自检

| 条 | 结论 |
|---|---|
| D1 调用链 | ✅ 未新增链路；FE→Java jobs（kind=页面得分）只读既有读面 |
| D9 8 件套 | ✅ metric_id=新 M_POLICY_REPORT_COUNT 挂 8 件套语义，is_mock=1 + pending_ref=QPOL-02，不伪闭合 |
| D16 | ✅ 只写 gapfill 库，未触碰 ODS/DWD/ADS/供应方库 |
| D18 | ✅ 接口不返回写死 mock——Java 仍只读表，行由 seed 脚本灌入（同既有 5 卡机制） |
| D19 | ✅ 连接 utf8mb4 / utf8mb4_general_ci 沿用 |
| 算法在 Python | ✅ 数值产自 seed 脚本（Python） |
| FDE 用户可见文案 | ✅ 「报告份数待发布」业务话术；gapfill/track 等实现黑话只在注释与 handoff |

## 6. 遗留与后续

- **数值升级路径**：导出事件流持久化立项后（gapfill 导出日志表 + Java 记录 + FE 上报），seed 行由真实计数取代或退役——升级时同步评估 222 操作日志区真轨点亮
- **QPOL-02 伞**：本卡口径与种子值随 QPOL-02 一并待甲方确认；确认后若甲方给正式口径，改 seed 公式重灌即可
- 恒空态时代文案「报告份数无读面出处」已在测试层防回归（不得回潮）

## 7. cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~45000 |
| model_used | glm-5.3-flash |
| actual_cost | $0.04 |
| cost_warn | false |
