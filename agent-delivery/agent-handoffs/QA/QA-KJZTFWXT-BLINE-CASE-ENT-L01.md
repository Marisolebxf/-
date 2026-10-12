# QA-KJZTFWXT-BLINE-CASE-ENT-L01 · 专题系统企业要素 11 入口 B 线用例收口

> **状态**：用例编写完成（执行另起任务）  
> **执行**：agent:qa-agent（主对话编排 + 8 个 subAgent 分入口产出）  
> **监管**：human:黄敬洲  
> **日期**：2026-10-12  
> **方案**：方案甲（用户 2026-10-12 确认）——SEARCH/COMPARE 按既有资产收编不补 A 线矩阵；9 个新入口对齐 v8 功能点全量写用例 + coverage。

---

## 1. 范围与实现

### 1.1 Phase A · 收编（3 入口）

| 入口 | 用例（既有） | coverage 处置 |
|------|--------------|----------------|
| SEARCH 企业查询 | 00001~00014、00030~00045（30 条，v1.2） | 新建 `coverage-fp.md`：**N/A**（数据查询域未进 A 线 v8 拆分），替代基准 = USM 故事矩阵 |
| COMPARE 对比篮 | 00015~00029（15 条） | 新建 `coverage-fp.md`：**N/A**（系统级浮层无 v8 拆分） |
| KEYENT 重点企业类型分析 | 00046~00061（16 条） | 已有 `coverage-fp.md`（T09 46 条），不改动 |

### 1.2 Phase B · 新写（9 入口，subAgent 分工产出）

| 入口 | catalog | A线 | 用例编号 | 条数 | coverage（已覆盖/总） | 产出 subAgent |
|------|---------|-----|----------|------|---------------------|----------------|
| 重点企业领域分析 | ent-key-domain | T10 (20) | 00062~00072 | 11 | 20/20（含开放项口径） | 主对话 |
| 企业技术力评估对比分析 | ent-eval-tech | T11 (42) | 00073~00084 | 12 | 36/42 | EVALTECH 子代理 |
| 企业商业力评估对比分析 | ent-eval-business | T12 (40) | 00085~00096 | 12 | 36/40 | EVALBIZ 子代理 |
| 企业综合竞争力评估 | ent-eval-compete | T18 (36) | 00097~00106 | 10 | 27/36 | EVALCOMP 子代理 |
| 深圳企业现状分析 | ent-sz-status | T13 (37) | 00107~00118 | 12 | 30/37 | SZSTATUS 子代理 |
| 招引企业推荐分析 | ent-attract | T14 (42) | 00119~00130 | 12 | 32/42 | ATTRACT 子代理 |
| 培育企业推荐分析 | ent-cultivate | T15 (41) | 00131~00142 | 12 | 25/41 | CULTIVATE 子代理 |
| 企业供应链关系分析 | ent-supply | T16 (44) | 00143~00154 | 12 | 32/44 | SUPPLY 子代理 |
| 企业发展痛难点分析 | ent-pain | T17 (36) | 00155~00164 | 10 | 31/36 | PAIN 子代理 |

**合计**：新写 103 条用例（00062~00164），9 入口 v8 功能点 338 条全量入矩阵（已覆盖 249 + 部分覆盖/未覆盖 89，后者均为算法黑盒归算法库、失败态需断链构造、空态需后端注入三类，逐条挂开放项不判 Fail）。

### 1.3 现场勘察依据

- 环境 `http://111.198.38.90:50892/`（admin 账号，2026-10-12 全入口勘察）
- 关键 as-built 事实已写入各用例文档 as_built 摘要：六类型发起弹窗、URL `source=compare-basket&analysis_type=*&return_context_id` 流转、Q013/Q015 待甲方确认角标、培育政策导向 #G5 空态不回落、供应链备份方案收敛为提示文案（DEC-RISK-BACKUP-PROMPT-20260720）、评审模式零泄漏等。

## 2. 编号与台账

- `qa/code-registry.yaml` → `KJZTFWXT.FUNC` 已更新：`next_seq = 165`
- 全局查重：164 个唯一用例号（00001~00164）无重复；本次 00062~00164 连续无断号（脚本校验通过）。

## 3. 产物清单

- 新建 9 个用例文档 + 9 个 coverage-fp.md（`qa/test-cases/KJZTFWXT/{KEYDOM,EVALTECH,EVALBIZ,EVALCOMP,SZSTATUS,ATTRACT,CULTIVATE,SUPPLY,PAIN}/`）
- 新建 2 个收编 coverage（`SEARCH/`、`COMPARE/`）
- 更新 `qa/code-registry.yaml`
- 本 handoff

## 4. 偏离说明

- T18 子项拆分：派单简报写 17+19，真源实为 18+18（合计 36 不变），文档头按真源标注。
- CULTIVATE 8 条未覆盖（一企一策全链路）：按 USM C2 与 TRACE `explicit_exclusions`，一企一策载体在模块外，非本模块缺口。
- SUPPLY 4 条未覆盖（备份方案编辑器类）：按 DEC-RISK-BACKUP-PROMPT-20260720 收敛为提示文案，无编辑器可验；如评审要求方案实体载体则升级需求变更。

## 5. 架构合规自检

- [x] D9：结果态 KPI ⓘ / Q013 / Q015 角标均写入用例预期（ⓘ 必有、Mock/待确认角标按现场）
- [x] 评审模式零泄漏：9 入口各有一条专项用例（挂 review 契约）
- [x] 三层 ID 纪律：功能点键（Txx|子项|功能点）/ 用例号（ZNFWJQ-…-FUNC-xxxxx）/ 自动化脚本号（P0-xx，本轮未写脚本）不混用
- [x] 不越界：全部产物在 gkx-orchestration `agent-delivery/qa/` 与 `agent-handoffs/QA/`，未触碰业务仓

## 6. 后续

- 执行轮（另起任务）：按 `_script.md` 为 9 入口写 Playwright 脚本并跑 run（参考 search/key-type 先例）
- ponytail: full（文档产物，无代码；subAgent 提示词已带范围约束）

## 7. cost

- actual_tokens: ~1.1M（主对话 + 8 subAgent）；model_used: glm-5.3 / Cursor agent；actual_cost: ~$6；cost_warn: false
