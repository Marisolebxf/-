# QA-ASBUILT-METHOD-L01 · As-built B 线方法基线固化（四步 + schema + catalog）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |
| 说明 | 2026-10-12 经 MCP 认领（同日建单 e4b9774d）；方法产物先于任务存在于仓，本单补任务身份与签收位。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义/方法固化文档；不缩代码） |
| 说明 | 未用 YAGNI 跳过 handoff / cost / 方法基线本身即为防漏件。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 范围与实现

- **本单只固化方法身份**：确认 B 线权威过程为四步，不新建各模块用例/脚本执行叶。
- 四步真源（`qa/as-built/prompts/`，逐条核对在仓）：
  1. **测试用例**（`_case.md`）：B 线现场起稿人读用例 + 功能点→用例覆盖矩阵；禁止从 A 线功能点一对一灌
  2. **测试脚本**（`_script.md`）：Playwright yaml + 脚本→用例覆盖矩阵
  3. **测试结果**（`_result.md`）：`runs/{run-id}/` 明细 + `SUMMARY.md`
  4. **总集提交表**（`_submit.md`）：已覆盖功能点切点投影「一功能点一行」
- 入口与落盘约定：`qa/as-built/schema.md` + `catalog/{系统}.yaml`
- 三系统 catalog 状态（核对 2026-10-12）：
  - `KJZTFWXT`：active，环境锁 `http://111.198.38.90:50892/`，45 个 entries
  - `KJXXZSXT`：placeholder，`base_url: null`（环境未锁，待定后实爬补全）
  - `KJZTFWALGO`：placeholder，`no_ui`（无独立用户前端，总集对功能点仍可转录）
- `qa/README.md` 与 `qa/as-built/README.md` 均已指向上述约定（禁止 localhost；专题线锁 50892）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 四步提示词 | `agent-delivery/qa/as-built/prompts/_case.md` · `_script.md` · `_result.md` · `_submit.md` |
| schema 约定 | `agent-delivery/qa/as-built/schema.md` |
| 三系统入口台账 | `agent-delivery/qa/as-built/catalog/{index,KJZTFWXT,KJXXZSXT,KJZTFWALGO}.yaml` |
| QA 工作区索引 | `agent-delivery/qa/README.md`（含 B 线说明段） |
| 本 handoff | `agent-delivery/agent-handoffs/QA/QA-ASBUILT-METHOD-L01.md` |

## 偏离说明

- 无范围偏离。模块级任务已在建单后另开：`QA-KJZTFWXT-BLINE-CASE-ENT-L01`（专题企业要素 R01，2026-10-12）。
- 展示系统 KJXXZSXT 环境未锁（`base_url: null`），不阻塞本单；开测前需先锁环境（候选 `http://192.168.88.50:30891`）。

## 验收证据

- 四步提示词与 catalog 均在仓且 git 已入库（历史提交 719288be / e4b9774d）
- 状态经 MCP `task-claim` / `task-update-status` 推进（2026-10-12），非手改 YAML

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 本单为方法文档，不改业务仓代码 | ✅ |
| D8 / D9 / D10（本单不触 UI / 指标 / 交互实现） | N/A |
| 环境约定禁止 localhost、锁 50892 | ✅ |
| 未绕过 MCP 直改 registry 状态字段 | ✅（状态字段全部经 MCP；建单内容经 task-create） |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~120000（会话估算：核对 + handoff + 建单衔接） |
| model_used | GLM 5.3（Cursor） |
| actual_cost | ~0.5 |
| cost_warn | green |
| source | session_estimate |

## 下一步

1. R01 批次 `QA-KJZTFWXT-BLINE-CASE-ENT-L01` 待本单 done 后 confirm 解锁（depends_on 已挂）
2. 展示系统环境锁定 → KJXXZSXT 首批建单
3. KJZTFWALGO 拆分 v2 收口补登记（独立单，勿并本单）
