# ENT-MOD-EVAL-TEST-TRIAGE-L01 · demo-ui-topic 存量测试失败排查 Handoff

- **任务**：排查并收敛 `tests/enterprise-evaluation-definition.test.mjs` / `tests/enterprise-evaluation-v12-contract.test.mjs` 两项存量失败（与就绪度改造无关，stash 复跑已证实）
- **执行**：agent:frontend-agent（Cursor 会话）
- **监管**：human:淮政玮
- **日期**：2026-08-01
- **状态**：review（等待监管人验收，不自行转 done）

## 1. 根因结论（两测试根因不同，均非页面行为缺陷）

### 根因一：断言对 CRLF 行尾敏感（enterprise-evaluation-definition）

- 失败断言：第 111 行 `enterprise evaluation page title and its trace decoration must be review-only`，正则要求 `<TraceInfoIcon` 到 `</ReviewOnly>` 间隔 ≤ `[\s\S]{0,500}`。
- 证据：逐 commit 测量该窗口字符数（f1fac5d → HEAD 共 13 个采样点），**git 库内 LF 版本全部为 492 字符、正则全部命中**（含 HEAD）；Windows `core.autocrlf=true` 工作区 checkout 为 CRLF（`git ls-files --eol` 显示 `i/lf w/crlf`），窗口内 11 行 × `\r` = **503 字符，超窗 3 字符**。
- 结论：**断言实现不鲁棒（对行尾编码敏感），非断言语义过期、亦非页面缺陷**。页面标题自 `f1fac5d`（引入 `mountId`/`sourceRelation`/完整 bid-reference `sourceLocation`）以来语义始终满足契约：标题整体 `<ReviewOnly>` 包裹 + 内含 `TraceInfoIcon`（D9/D10 合规结构完好）。该测试在 LF checkout（CI/Linux）一直是绿的，只在 CRLF checkout 失败。

### 根因二：编排仓覆盖登记滞后（enterprise-evaluation-v12-contract）

- 失败断言：第 151 行，`交付覆盖/ENT-EVAL/implementation-coverage.yaml` 的 mount_id 集合（18 个）≠ `Wireframe-ENT-EVAL.md` 定义集合（24 个）。
- 证据：编排仓 commit **`f11cdd9`**（2026-07-31，docs(ent): sync product and UX definitions）给 Wireframe 新增恰好 6 个 mount_id（`ENT-EVAL-F02-OBJECT-SNAPSHOT-NOTE` / `ENT-EVAL-F02-RANKING-DISCLOSURE-NOTE` / `ENT-EVAL-F02-RANKING-SNAPSHOT-NOTE` / `ENT-EVAL-F09-QUOTA-TITLE` / `ENT-EVAL-F10-REPORT-TITLE` / `ENT-EVAL-F10-LIMITATIONS-TITLE`），但**未同步更新 implementation-coverage.yaml**（该文件停留在 `4b0d9de` v1.6 包，2026-07-20）。
- 关键事实：6 个挂载点在 demo-ui-topic 源码中**全部已实现**（`EnterpriseEvaluationResultWorkspace.tsx`×3、`EvaluationQuotaExceededModal.tsx`、`EnterpriseEvaluationReportView.tsx`×2，F10 两项另经 `SystemReportReader.tsx` 的 ENT-EXPORT-F02 迁移映射），v12 测试第 156–159 行的"渲染源码必含挂载点"断言本可通过。缺的只是覆盖登记文档。

## 2. 处置方式（二选一收敛：更新断言/登记，未动页面）

| 测试 | 处置 | 依据 |
|---|---|---|
| enterprise-evaluation-definition | 测试读文件处统一 `replace(/\r\n/g,'\n')` 归一化行尾（page + IA/TRACE/USM/Wireframe 四份定义文件） | 断言语义正确、页面合规结构完好，失败纯因 `\r` 计入字符窗口；**未放宽任何 `{0,n}` 窗口、未删改任何 D8/D9/D10 合规断言** |
| enterprise-evaluation-v12-contract | 编排仓补齐 `implementation-coverage.yaml` 6 条 mount 登记（按 Wireframe 定义原样登记：host_label/marker_type/trace_refs/required_payload/source_relation 一致；3 条 F02 note 挂 ENT-EVAL-DEMO-RESULT、F09 挂 ENT-EVAL-DEMO-RESULT（quota_modal）、F10 两条挂 ENT-EVAL-DEMO-REPORT（report_view））；coverage_summary 18→24；updated_at 2026-08-01 | 源码已实现、Wireframe 已定义，属登记文档滞后；不涉及"改绿"任何未实现项 |
| enterprise-evaluation-processing-navigation（同因新发现） | 同因一：读文件处归一化行尾 | 第 18 行截取正则要求 `` `{\n` ``，CRLF 下 `` `{\r\n` `` 导致 resumeEffectBlock 截空；断言本身未改 |

## 3. 同因核查（任务第 3 条）

批量复跑 tests/ 下全部 evaluation 相关非 pointer 测试（model / quota-modal / report×3 / result-model / structured-report / task-store / template-store / ent-export-system-report-contract）：仅 **enterprise-evaluation-processing-navigation** 存在同因（CRLF）失败，已一并修复；其余全绿。范围外known 存量（*-pointer 系列、enterprise-review-mount-contract）未触碰。

## 4. 复跑结果（全绿）

| 测试 | 结果 |
|---|---|
| tests/enterprise-evaluation-definition.test.mjs | ✅ passed |
| tests/enterprise-evaluation-v12-contract.test.mjs | ✅ passed |
| tests/enterprise-eval-readiness.test.mjs（防回归） | ✅ passed |
| tests/enterprise-evaluation-processing-navigation.test.mjs（同因顺带） | ✅ 2/2 passed |

## 5. 产物清单

- **demo-ui-topic**（origin/dev）：commit `1500f8c`
  - `tests/enterprise-evaluation-definition.test.mjs`（读文件行尾归一化）
  - `tests/enterprise-evaluation-processing-navigation.test.mjs`（同上）
- **gkx-orchestration**（origin/dev）：本 handoff 同 commit
  - `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/implementation-coverage.yaml`（补 6 条 mount 登记，18→24）
  - `agent-delivery/agent-handoffs/ENT-MOD-EVAL-TEST-TRIAGE-L01.md`（本文件）
  - `agent-delivery/task-registry.yaml`（状态 review + cost 回填）

## 6. 架构合规自检（宪法 §2 相关条目）

- 未触碰页面/组件代码，无 D8（Arco/token）影响：✅
- D9/D10 合规断言（ReviewOnly 包裹、TraceInfoIcon、mount_id 契约）全部保留原强度，未"为绿而绿"：✅
- 覆盖登记按 Wireframe 真源原样补齐，未伪造实现状态（6 挂载点源码实测存在）：✅
- 未改 `.gitignore`/`package.json`/`vite.config` 等配置；未 force push；commit 带 `[agent:frontend]`：✅

## 7. 遗留与建议（不在本单执行）

- 仓内无 `.gitattributes`，`core.autocrlf=true` 环境下所有"读源码做正则断言"的测试都潜在 CRLF 敏感；建议后续单独建单：加 `* text=auto eol=lf` 或在共享测试工具函数统一归一化（本单只按范围修了 evaluation 相关 3 个）。
- `f11cdd9` 这类"定义文件与覆盖登记不同步"可考虑在定义包发布流程加 checklist。
