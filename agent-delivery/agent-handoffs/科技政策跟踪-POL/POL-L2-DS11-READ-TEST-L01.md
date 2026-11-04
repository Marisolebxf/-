# POL-L2-DS11-READ-TEST-L01 · 结果解读报告多维展示 · 集成测试

- 任务：`POL-L2-DS11-READ-TEST-L01`（WBS 行 `WBS-05-23-L2-06F`）
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 执行：`agent:qa-agent`
- 强度：ponytail full
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（已签收）、`sdd/l2/POL-L2-DS11-READ-API.md`；被测实现 `POL-L2-DS11-READ-IMPL-JAVA`、`POL-L2-DS11-READ-IMPL-PY`、`POL-L2-DS11-READ-GAPFILL-L01`

## 范围与实现

对 DS11 结果解读报告多维展示（SRS 223–226）三条公开资源做集成测试设计 + 可执行项验证：

1. **测试用例文档**：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS11-READ-TEST-L01.md`
   - §1 合规交付主路径数据准备 DP-01~DP-05（region_gap 行、gapfill 7 行灌数含幂等重跑、两 Job 样本含防破坏断言、环境前置）
   - §2 关键路径用例 TC-01a/01b（counts 有值/空态）、TC-02（shells 渲染）、TC-03a/03b（jobs 白名单 + 两新键豁免）、TC-04a/04b（两 Job 异步轮询完成）、TC-05（X-Trace-Id 贯通）、TC-06（Job 失败不清空只读面）——共 10 条，每条含编号/前置/步骤/预期/实际结果
   - §3 界面操作 S1–S5（打开结果解读 Tab → 短板看板 → 互动解读 → 焦点任务 → 摘要/多媒体结果）
2. **验证执行**：代码走查 + 本地脚本校验 + 既有单测证据核对；前端截图尝试（见偏离）。
3. **发现缺陷 BUG-01（P1）**：见下。

## 测试发现

### BUG-01（P1，阻塞 TC-02）：Java SHELL_SQL 列名与线上表错位

- 位置：`lumen-svc-platform` `gkxlumen-element` `PolicyGapfillController.SHELL_SQL`（当前 origin/dev HEAD `387502a` 仍存在）
- 现象：SQL SELECT 旧列 `topic_or_metric`、`caption`；GAPFILL 单 commit `8c0a59c` 起线上表列名为 `subject_name`、`caption_text`（分册第 5 节口径）
- 后果：MySQL `Unknown column` 被 `ElementDao.listOrEmpty` 的 DataAccessException 捕获吞掉 → `GET /display/v1/policy/evaluation/shells` **恒返回空列表**，224/225 两叶联调态等于无数据，且无任何错误暴露
- 建议：api-agent 一行修复（SHELL_SQL 两列名）+ 单测列名断言，随后复测 TC-02

## 偏离说明

| 偏离 | 说明 |
|---|---|
| 派单背景「shells 5 行（3 解读 + 2 多媒体）」 | 实现真源（GAPFILL handoff + 脚本 `--check` 实跑 + SQL 镜像）为 **7 行 = 4 解读 + 3 多媒体**。测试按 7 行断言，已在用例文档 DP-02 标注 |
| 截图 | **截图待补：环境原因**。本机 `pnpm install` 失败两次：全局 pnpm 10.9.2 报 `packages field missing or empty`（读不懂本仓 `pnpm-workspace.yaml` 的 `allowBuilds` 键），corepack 又因网络取不到 pnpm 发行版失败。按派单要求不伪造截图，用例文档 §3 已保留完整操作步骤与预期截图文件名，环境修复后可补 |
| 联调用例 PENDING | K8s dev 联调（TC-01a/02/04/05 真接口）不在本机完成；对应断言已由既有单测证据覆盖的项在用例「实际结果」列注明单测出处 |
| 未跑 `gap.run` | 按 ARCH 分册，counts GET 与测试都不调用 `gap.run`，region_gap 行依赖既有批次 |

## 产物清单

| 产物 | 路径 |
|---|---|
| 测试用例文档 | `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS11-READ-TEST-L01.md`（10 条用例 + 5 条数据准备 + 5 步界面操作） |
| 本 handoff | `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-TEST-L01.md` |
| 截图 | 待补（环境原因，见偏离说明）；预留目录 `agent-handoffs/科技政策跟踪-POL/assets/POL-L2-DS11-READ-TEST-L01/` |
| 代码改动 | 无（QA 不改代码；BUG-01 转 api-agent） |

## 验收证据

- 既有单测全绿（引自实现单，本次抽查核对存在性与断言点）：
  - Java 23 项：`PolicyAnalysisTypesTest`(4)、`PolicyAnalysisAdapterImplTest`(11)、`PolicyEvaluationServiceTest`(7)、`PolicyGapfillEvaluationTest`(1)、`PolicyGapfillControllerTest`(6)
  - Python 36 项：`lumen-algo-py/tests/test_policy_job.py`（含两新键白名单、`_policy_text_parse_rows` 只 SELECT、`_policy_focus_ads_rows` 先 run 再读）
- 本轮实跑：
  - `python -c ... seed_gapfill_policy_eval_shell.rows()` → total 7 / read 4 / media 3，空值约束与 BANNED 断言通过
  - `git pull --no-rebase` 同步 `lumen-svc-platform` 至 `387502a` 后确认 BUG-01 仍在（`SHELL_SQL` 行 58–60）
- K8s dev 联调证据：PENDING（TC-01a/02/04/05 待环境；BUG-01 修复后复测）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端→Java→Python /internal | ✅ 用例按此断言（TC-05 counts 链无 Python span） |
| 算法只在 Python | ✅ 测试不要求 Java 计算任何指数/摘要 |
| D9 空态不伪闭合 | ✅ TC-01b/TC-02 空态断言不造 0、不 501、不写死 mock |
| D16 gapfill | ✅ DP-02 只灌 `gkxlumenx_gapfill` 一张表，幂等可重跑 |
| D18 不在接口写死 mock | ✅ BUG-01 恰好证明"吞错返回空"会掩盖故障，已按缺陷上报而非绕过 |
| 人工验收闸门 | ✅ 改动全部停本地（仅新增两份文档），未 commit / 未 push |
| PowerShell 规约 | ✅ 全程 `;` 串联，无 `&&`、无 heredoc |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 42000 |
| model_used | glm-5.3 |
| actual_cost | 0.21 |
| cost_warn | green |
| user_story | `US-DS-POL-05` |

ponytail: full —— 测试文档只写会跑的用例（10 条），数据准备全部复用已有脚本与批次，不造第二条灌数路径；截图不伪造。

## 遗留

1. BUG-01 需 api-agent 修复（SHELL_SQL 列名），修复后复测 TC-02 并补联调证据
2. 前端截图待补（pnpm 环境修复后按用例 §3 五步补拍）
3. K8s dev 联调（TC-01a/04a/04b/05）待环境与 BUG-01 修复
