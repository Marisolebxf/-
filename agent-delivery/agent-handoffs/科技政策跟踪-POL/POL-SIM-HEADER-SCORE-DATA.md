# POL-SIM-HEADER-SCORE-DATA · 页头得分表建表 + v2 灌数 handoff

> 执行 agent:data-agent · 监管 human:淮政玮（当次会话在场批准）· pull 认领 · 2026-11-11
> 强度：ponytail full —— 未重做已有实现，只做了「核验 + 执行 + 验收」

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `POL-SIM-HEADER-SCORE-DATA` |
| claimed_by | `agent:data-agent`（本会话） |
| supervised_by | `human:淮政玮`（当次会话用户，AskQuestion 明确批准建表灌数与认领） |
| claim_type | `pull` |
| claimed_at / lock | `2026-11-11 21:41 +08:00` / +4h |

## 背景（防双派澄清）

- 真源移交清单：`agent-delivery/agent-handoffs/POL-SIM-HEADER-SCORE-L01.md` §三（上一轮 frontend 会话产出，含 DDL/公式/D4 翻转步骤）。
- 代码实现（DDL + 灌数脚本）由并行 data-agent 于 18:02 commit `e6f1fef` 完成（`lumen-algo-py`），走的是 handoff 文档而**非 registry 单**——建单时（17:26 commit `77ea5692`）该条目被并行提交 `a7de7033` 从旧基线挤掉，导致无人认领。本会话 21:38 基线拉齐后重建（`c9669853`）并认领。
- 本会话**未重做代码**：核验并行会话的实现满足 DoD 后执行验证与线上灌数。

## 范围与实现（本会话实际动作）

1. **核验**：DDL（`scripts/mysql/gapfill_policy_sim_score.sql`）与 Java `PolicySimulationReadController.SCORE_COLUMNS` 逐列对齐；脚本 `--check` 实算绿（20212 政策、入集 17663、在效 17577 → 64.76 / 99.51 / 0）。
2. **口令文件差异修复**：脚本 docstring 写「`LUMEN_ALGO_MYSQL_PASSWORD` 环境变量」，代码实际只读 `%TEMP%\gkx-mysql-pwd.txt`；本会话按仓内既有回退源（`vendor/innov-py/conf/settings.yaml` → `db.mysql_password`）落口令文件（值不经终端回显），**未改脚本代码**（docstring 与实现的差异留给原实现者择机统一）。
3. **建表 + 灌数**（经用户批准）：`10.50.11.76` `gkxlumenx_gapfill.gapfill_policy_sim_score`，幂等 upsert 3 行：
   - `M_POLICY_EFFECT_SCORE` = **64.76**（有效率 99.5131%×0.5 + 力度均值 0.30×50）
   - `M_POLICY_IMPLEMENTATION_EFFECT` = **99.51**（在效 17577/17663）
   - `M_POLICY_LAYOUT_REC_COUNT` = **0**（机遇侧无过线，诚实 0；阈值临时 55.0）
   - `is_mock=1`、`pending_ref='QPOL-02'`、`gapfill_batch_id='POL-SIM-HEADER-SCORE-L01'`
4. **线上链路验证**：`POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs` body `{"kind":"页面得分"}` + `systemCode: display` + `Authorization: Bearer`（令牌读本机令牌文件，不入库入 git）：HTTP 200，`data.records` **3 行**，驼峰字段与前端 `PolicySimulationScoreRow` 契约逐字对上。
5. **前端零改动**：`index.vue` 页头三卡按 `scoreNum(metricId)` 出数（64.8 分 / 99.5 分 / 0 节点），⚠️ 角标因 `is_mock=1` 仍在（D9 诚实性，符合预期）。

## 产物清单

| 产物 | 位置 |
|---|---|
| DDL 脚本 | `lumen-algo-py/scripts/mysql/gapfill_policy_sim_score.sql`（并行会话 commit `e6f1fef`，本单核验） |
| 灌数脚本 | `lumen-algo-py/scripts/seed_policy_sim_score.py`（同上，`--check` / `--apply` 双模式） |
| 线上表 | `10.50.11.76 / gkxlumenx_gapfill.gapfill_policy_sim_score`（3 行，幂等 upsert） |
| 线上验证 | `POST /display/v1/policy/simulation/jobs` HTTP 200，3 行驼峰记录（见验收证据） |
| 前端改动 | 无（页头三卡既有代码直接出数） |

## 偏离说明

无实质偏离，两点执行方式备注：

1. **claim_type=pull + 复用并行实现**：DDL 与灌数脚本由并行 data-agent commit `e6f1fef` 先行落地（当时未走 registry，建单条目被并发提交挤掉），本单以 pull 认领后只做核验、执行与线上验收，未重写代码——目的是把已有产出纳回派单体系可追溯。
2. **口令获取路径**：脚本 docstring 声称环境变量 `LUMEN_ALGO_MYSQL_PASSWORD`，实现实际读 `%TEMP%\gkx-mysql-pwd.txt`；本会话按仓内既有回退源（`vendor/innov-py/conf/settings.yaml`）落口令文件（值不经终端回显），未改他人已提交代码，docstring 与实现的差异列入遗留移交（P3）。

## 验收证据

- `--check`：`{"ok": true, "valid_rate": 99.5131, "avg_factor": 0.3}`，断言全过（含「对冲计数必须诚实 0」）
- `--apply`：`{"connected": true, "rows": [["页头卡","M_POLICY_EFFECT_SCORE","64.7600",1], ["页头卡","M_POLICY_IMPLEMENTATION_EFFECT","99.5100",1], ["页头卡","M_POLICY_LAYOUT_REC_COUNT","0.0000",1]]}`
- 线上 jobs：HTTP 200，`n_records: 3`，`metricId/scoreValue/isMock/pendingRef` 齐全
- 前端影响：刷新政策推演页即出三卡数值；第 4 卡（利益攸关反馈）不受本单影响

## 架构合规自检

| 条 | 结论 |
|---|---|
| D1 调用链 | ✅ 前端 → Java jobs → gapfill 表，未越层、未直连 Python |
| D8 前端规范 | ✅ 前端零改动，页头卡沿用既有 Arco 组件与 token |
| D9 指标 8 件套 | ✅ 三行均带 `metric_id`；`is_mock=1` + `pending_ref='QPOL-02'`，ⓘ/⚠️ 追溯入口保留 |
| D12 demo/lumen 隔离 | ✅ 全链路只涉 lumen 仓与 lumen 库（`gkxlumenx_gapfill`），无 demo 依赖 |
| D16 缺项只进 gapfill_ | ✅ `gkxlumenx_gapfill.gapfill_policy_sim_score`，未触碰 ODS/DWD/ADS/供应方库 |
| D18 接口不返回写死 mock | ✅ 接口只读表；表由真实工具链实算灌入（polan.eval.effect 同源） |
| D19 字符集 | ✅ 显式 utf8mb4 / utf8mb4_general_ci |
| 算法在 Python | ✅ v2 公式实算在 `seed_policy_sim_score.py`（Python），Java 只读表转驼峰 |
| 可观测性 | ✅ 走 jobs 既有链路（平台统一埋点），无新增旁路 |
| D4 翻转路径 | `is_mock` 恒 1，待 QPOL-02 甲方归一 + QA 核验后另行置 0（脚本不碰，前端角标届时自动消失） |

## 遗留 / 移交

- **脚本口令回退源统一**（P3，原实现者择机）：`seed_policy_sim_score.py` docstring 说环境变量、代码读 Temp 口令文件；仓内标准是 `LUMEN_ALGO_MYSQL_PASSWORD` 或 settings.yaml 回退。本会话不动他人已提交代码。
- **QA 核验后 D4 翻转**：正式链路走 QA → `is_mock=0` → 镜像矩阵 D4 翻绿 → 前端 ⚠️ 自动消失。
- **前端验收**：监管人刷新政策效果推演页确认三卡出数即可；无需发版（jobs 接口已在线）。

## cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~45000 |
| model_used | glm-5.3-flash |
| actual_cost | $0.04 |
| cost_warn | false |
