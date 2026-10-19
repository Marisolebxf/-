# QA 工作区索引

> **功能测试命令路由（先读）**：[`func-test-playbook-index.md`](func-test-playbook-index.md) ——「执行{系统}的用例/脚本/执行/交付/记录」对照表 + Kickoff。  
> 正式规范：[`../qa-test-case-spec.md`](../qa-test-case-spec.md)（v1.0）  
> 模板：[`../templates/test-case-template.md`](../templates/test-case-template.md) · [`../templates/test-record-template.md`](../templates/test-record-template.md) · [`../templates/test-retest-template.md`](../templates/test-retest-template.md)（复测）  
> 交付模板真源（客户）：`参考文档/测试模板-v2/`（用例簿 4 类 sheet + 记录簿 4 类 sheet + 5 类报告 + 3 张评估表）

## 已确认规则

- 功能类型码 = **FUNC**
- GKX 扩展列 = **主表右侧**
- 系统码一律取自总集「规则 -0529」：算法库 = **`SDWJSF/KJZTFWSFK`**（编号内 `/`；**目录名**用 `SDWJSF-KJZTFWSFK`，旧 `KJZTFWALGO` 已废弃 2026-10-13，仅任务 ID `QA-KJZTFWALGO-*` 保留历史）

## 目录

| 路径 | 用途 |
|------|------|
| `test-cases/` | 用例 MD：`{系统码}/{模块层-中文}/{模块-中文}/FUNC-{模块}-用例.md`（算法库主册 **`API-*`**，见 `SDWJSF-KJZTFWSFK/README.md`）；**COMP/INT/PERF** 同目录混放；系统级入 `shell-系统壳/` |
| `test-records/` | 执行记录：`{系统码}/{轮次 R0..Rn}/`（2026-10-13 起按轮次；旧模块平铺目录已迁入 R0） |
| `evidence/` | 证据：`{系统码}/{轮次}/`（旧按模块目录已迁入 R0）；文件名 `{用例编号}-{Pass\|Fail}-{序号}.png` |
| `total-set/` | **A 线**功能点拆分工作区（KJXXZSXT / KJZTFWXT / SDWJSF-KJZTFWSFK） |
| `as-built/` | **B 线**现场勘察线（prompts/**runs**/scripts/catalog/tools）；机跑结果**只**落 `as-built/runs/`（ignore）。勿使用已废弃的 `qa/runs/` |
| `coverage/` | 三张评估表 MD 工作稿（按系统码） |
| `reports/` | 5 类测试报告 MD 源稿（按系统码；安全在 `_security/`；与 doc-agent 协作汇编 docx） |
| `delivery/` | **总集交付成品**（按系统码；含交付前 sheet 级清检单，见其 README） |
| `tools/` | 测试工具产物（jmeter/postman，服务报告交付） |
| `bug-registry.yaml` | BUG 编号台账（按日取号，防并行撞号） |
| `code-registry.yaml` | 系统码与用例序号台账 |
| `perf-baseline.md` | **三系统性能测试规约**（SLA 定标 + 判定口径 + 场景基线 + 接口盘点 + 工具脚本 + 执行证据 + 交付映射，单文件统一承载；QA-PERF-SPEC-L01） |

## 用例库

执行仓：**lumen-ui-topic**（`VITE_APP_USE_MOCK=false`，走 Java `/topic/v1`；INTEG：`http://192.168.88.50:30892`；B 线环境：`http://10.50.69.111:30888/`）。

| 模块 | 文件 | 编号 | 状态 | 入口 |
|------|------|------|------|------|
| 企业查询 SEARCH | `test-cases/KJZTFWXT/enterprise-企业分析/SEARCH-企业查询/FUNC-企业查询-用例.md` | 00001–00014, 00030–00045 | **v1.2**（字段/页签勾选）· ENT-MOD-SEARCH-QA-ACCEPT-L01 | `/enterprise/enterprise-search` |
| 对比篮 COMPARE | `test-cases/KJZTFWXT/enterprise-企业分析/COMPARE-对比篮/FUNC-对比篮-用例.md` | 00015–00029 | v1.0 试点 | `/enterprise/enterprise-compare` |
| SEARCH 记录 | `test-records/KJZTFWXT/R0/FUNC-企业查询-记录-待填.md` | — | 待人工填 | — |

## 算法库 QA 路由

- **总索引（A 线 F0～F4 + B 线 S1～S5）**：[`algo-lib-playbook-index.md`](algo-lib-playbook-index.md)
- **B 线编排真源（接口入参/出参，50897）**：[`algo-lib-api-case-playbook.md`](algo-lib-api-case-playbook.md)
- **专题/展示 B 线**：[`func-test-playbook-index.md`](func-test-playbook-index.md)（算法库 S1 勿套用其页面场景 Kickoff）

## 总集拆分（A 线）

| 系统 | 任务 | 功能点表 |
|------|------|----------|
| 专题 KJZTFWXT | `QA-KJZTFWXT-FUNCLIST-SPLIT-L01`（done） | `total-set/KJZTFWXT/6.…功能点拆分_v8.xlsx`（1298 条） |
| 展示 KJXXZSXT | `QA-KJXXZSXT-FUNCLIST-SPLIT-L01`（done） | `total-set/KJXXZSXT/fp-split-run/` |
| 算法库 SDWJSF-KJZTFWSFK | 需规 `FUNCLIST-SPLIT-L01`（内部 v2）；**by-api v0.2.1 对外交付**（`FP-BY-API-L01` 待 PM 补建） | `fp-split-run/`（对照）+ `fp-split-by-api-run/`（主）；B 线用例 `test-cases/SDWJSF-KJZTFWSFK/` |

拆分原则：`total-set/{系统码}/科技专题战略分析-最细颗粒度功能点拆分原则-v1.md`（各系统同名变体）；合表脚本 `agent-delivery/scripts/_merge_*_fp_split_work.py`。

## As-built 测试线（B 线，进行中）

过程提示词：`as-built/prompts/_case.md`（用例）· `_script.md`（脚本）· `_result.md`（结果）· `_submit.md`（总集提交表投影）。

- 说明：`as-built/README.md` · 约定：`as-built/schema.md` · 入口台账：`as-built/catalog/`（KJZTFWXT、SDWJSF-KJZTFWSFK **50897** active；KJXXZSXT placeholder）
- 金样脚本：`as-built/scripts/KJZTFWXT/enterprise/search/`（cases-v1；旧 `gold.yaml` 已废弃）
- **脚本补齐编排**（金样收口后把 FUNC 1:1 补齐；可复用）：`as-built/script-backfill-playbook.md` · 缺口快照 `as-built/script-backfill-gap-KJZTFWXT.md`
- **脚本批量执行**（冒烟/全量/回归 + 强制 Excel/总结）：`as-built/script-batch-run-playbook.md` · 命令总路由 `func-test-playbook-index.md` **S3**
- **用例交付合并**（S4 骨架）：`case-delivery-playbook.md` · 总路由同文件 **S4**
- **可交付测试记录**（S5 骨架）：`record-delivery-playbook.md` · 总路由同文件 **S5**

## 新建模块用例

**专题 / 展示**

1. 按 `as-built/prompts/_case.md`：**B 线现场**起稿，不从 v8 功能点一对一拆
2. 落盘 `test-cases/{系统码}/{模块层-中文}/{模块短名-中文}/FUNC-{模块}-用例.md`（目录双语命名），从 `code-registry.yaml` 取号
3. 打开对应 `fp-split-run/work/Txx.md` 做功能点覆盖矩阵（未覆盖允许登记）
4. 脚本/结果见 `_script.md` / `_result.md`；总集「一功能点一行」见 `_submit.md`
5. 失败用例先到 `bug-registry.yaml` 取 BUG 号再回填记录

**算法库 `SDWJSF-KJZTFWSFK`**

1. 按 [`algo-lib-api-case-playbook.md`](algo-lib-api-case-playbook.md) §编写方法论 + §长任务返工。接口文档只读 apiview catalog JSON；不写登录/Token；第一轮 `API-00001`～`00888` 作废
2. 落盘 `test-cases/SDWJSF-KJZTFWSFK/…/API-{页}-用例.md` + `coverage-fp.md`；矩阵对照 `fp-split-by-api-run/work/Lxx.md`
3. 总路由与 Kickoff：[`algo-lib-playbook-index.md`](algo-lib-playbook-index.md) §5～§6

## 待决策清单（PM 级，未处理）

| # | 项 | 影响 | 状态 |
|---|----|------|------|
| H3 | COMP 三屏（移动/电脑/大屏）适配范围 | 兼容用例矩阵设计前提；大屏 Track-L blocked | 🔴 待 PM |
| H4 | 三张评估表责任矩阵（谁填/何时填） | 交付前三表无人认领 | 🔴 待 PM |
| S3 | 安全测试执行主体（我方/三方渗透） | 安全报告 + INT「安全」子集用例归属 | 🔴 待 PM |
