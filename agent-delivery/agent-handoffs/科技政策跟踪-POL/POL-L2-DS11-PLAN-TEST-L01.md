# POL-L2-DS11-PLAN-TEST-L01 · 推荐方案报告交互展示 · 测试用例（阶段一交付）

- 任务：`POL-L2-DS11-PLAN-TEST-L01`
- 日期：2026-11-04
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 强度：ponytail full
- 状态：**阶段一完成**（用例文档+数据准备核实）；阶段二（界面验证+截图）阻塞于 `POL-L2-DS11-PLAN-WIRING-L01`（in_progress）
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH/API/DATA.md`（已签收）、`POL-L2-DS11-PLAN-GAPFILL-L01.md`（commit `423527e`，19 行）

## 范围与实现

按派单两阶段执行。本轮完成第一阶段全部可做项：

1. **用例文档落盘**：`工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS11-PLAN-TEST-L01.md`，覆盖 227 方案对照 / 228 参数模拟 / 229 路径与风险 / 230 互动意见 / 231 方案报告五叶：
   - 第 1 节 合规交付主路径数据准备（DP-01 四种类行集 / DP-02 意见闭集 / DP-231 导出数据面 / DP-05 环境汇总），连库口令来源 `repos/lumen-algo-py/k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_PASSWORD`（只进进程环境变量）
   - 第 2 节 关键路径验证 TC-01~TC-07 共 13 条，每叶正常态（有行）+ 空态（未选方案/参数档对不上/无行）双路径；230/231 按交互壳口径验证"界面行为诚实、不伪造成功记录、库内行数不变"，不验证"库内有新行"
   - 第 3 节 界面操作 S1–S5b（双路径截图清单，截图目录已定为 `agent-handoffs/科技政策跟踪-POL/screenshots/POL-L2-DS11-PLAN-TEST-L01/`）
2. **DP-01 连库核实通过**（临时脚本用后即删，未留仓）：`by_kind` = 方案对照 2 / 参数模拟 5 / 路径与风险 6 / 互动意见 6 = 19 行；`is_mock=1` 全 19 行；路径行 `metric_id='M_POLICY_DS_11_POLICY_EVAL_015'` 恰 6 行；其余种类 `metric_id` 非空计数 0；param_keys 五档与 GAPFILL 单一致；意见分类 评价/评论/建议 各 2。
3. **格式对齐**：`POL-L2-DS11-VIZ-TEST-L01.md` 尚未落盘（2026-11-04 00:53 查无），已对齐同目录 `POL-L2-DS11-READ-TEST-L01.md` 五章结构（接口总览/数据准备/关键路径/界面操作/缺陷与结论）。

## 每叶判定（阶段一）

| 叶 | 数据准备 | 用例成文 | 界面验证+截图 | 判定 |
|---|---|---|---|---|
| 227 方案对照 | ✅ 2 行已核实 | ✅ TC-01a/01b | ⏸ 待 WIRING | 阶段一通过 |
| 228 参数模拟 | ✅ 5 档已核实 | ✅ TC-02a/02b | ⏸ 待 WIRING | 阶段一通过 |
| 229 路径与风险 | ✅ 6 行+metric 命中已核实 | ✅ TC-03a/03b | ⏸ 待 WIRING | 阶段一通过 |
| 230 互动意见 | ✅ 6 行闭集已核实 | ✅ TC-04a/04b（不落库断言） | ⏸ 待 WIRING | 阶段一通过 |
| 231 方案报告 | ✅ 无需新灌（读 227+230 行） | ✅ TC-05a/05b（文件禁区断言） | ⏸ 待 WIRING | 阶段一通过 |

## 偏离说明

- 派单写"截图存 `screenshots\POL-L2-DS11-PLAN-TEST-L01\\`"，实际目录用单反斜杠 `agent-handoffs/科技政策跟踪-POL/screenshots/POL-L2-DS11-PLAN-TEST-L01/`（Windows 路径转义笔误，语义不变）。
- DATA 分册列名与线上真表不一致（见用例文档 RISK-01）：用例以 GAPFILL 单落库的 26 列为准（`scheme_brief`/`pros_cons_text`/`opinion_subject` 等；表无 `sort_no`，读取顺序按 `id` 升序）。未回改 DATA 分册（qa 无改定义稿权限，已登记风险待 coordinator 处置）。

## 阻塞项

- **阶段二阻塞**：`POL-L2-DS11-PLAN-WIRING-L01`（前端接线）2026-11-04 00:14 仍 `in_progress`。按派单"不空转等待"，本轮交付阶段一；待其 integration/done 后补做 S1–S5b 截图与 TC-01~TC-07 联调实测回填。

## 产物清单

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS11-PLAN-TEST-L01.md`（用例文档，13 用例 + 5 DP + 11 截图位）
- 本 handoff
- WBS 行 `WBS-05-23-L2-07F` 状态 ready → **testing**（同 commit）
- registry：认领 commit `b34ed1be7` + merge `ea673564f` 已推 origin/dev

## 验收证据

- 连库 SELECT 输出（2026-11-04，口令经环境变量注入）：`by_kind {互动意见:6, 参数模拟:5, 方案对照:2, 路径与风险:6}`、`is_mock 19`、`path_with_metric 6`、`other_with_metric 0` —— 与 GAPFILL 单验收 JSON 完全一致
- 截图 0 张（阶段二未执行，不伪造）

## 架构合规自检

- ✅ 只读验证：未改 `lumen-ui-science-pc` / `lumen-svc-platform` / `lumen-algo-py` 任何业务代码（临时验证脚本用后即删）
- ✅ 五叶口径与 ARCH/API 分册一致：同步只读、一次一种类、无 501、空态为空、不进异步管道、不调 Python
- ✅ 230/231 交互壳按"演示态不落库、行为诚实"验收，不要求库内有新行
- ✅ D16：测试断言不把 mock 行写成已上线（`is_mock=1` 全行断言）
- ✅ 口令不入库入文档：验证命令口令仅进程环境变量

## 遗留

- 阶段二（WIRING done 后）：playwright 开 K8s dev 前端逐叶操作，正常态+空态双路径截图 ≥11 张，回填用例文档"实际结果"列与本文档每叶终判
- RISK-01 待 coordinator 令 data-agent 在 DATA 分册补 as-built 列名备注
- cost：actual_tokens ≈ 90k；model_used：glm-5.3；actual_cost ≈ $0.6；cost_warn：green
