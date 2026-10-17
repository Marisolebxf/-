# QA-ASBUILT-SCRIPT-BATCH32-L01 · 专题 as-built 脚本批量编写（cases-v1 全量收口）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |
| 说明 | 父单自 2026-10-14 起由黄敬洲监管；本 handoff 为脚本编制阶段收口（2026-10-16）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 写脚本与 coverage；未用 YAGNI 跳过 schema/catalog/规约与独立验收纪律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 范围与实现

- **系统**：`KJZTFWXT` · 环境 `http://111.198.38.90:50892/`（禁止 localhost）。
- **交付形态**：由派单包期的 `gold.yaml`/`scripts.yaml` 大包 **迁移为 `schema.md` cases-v1**——每脚本 `cases/{id}.yaml` + 入口 `index.yaml`（`gold:` / `all:`）+ `coverage.md` + `fixtures/`。
- **覆盖**：`gap-func-vs-scripts.py --system KJZTFWXT` → **FUNC 774 / scripts 774 / gap 0**（2026-10-16）。
- **catalog**：`live` 入口 **34**；挂 `scripts` / `gold` 指针 **28**（其余 6 个 live 入口脚本已在磁盘、待 catalog 字段补全，不阻塞 gap 0）。
- **编排资产（同批 push）**：`script-backfill-playbook.md`、`script-batch-run-playbook.md`、`func-test-playbook-index.md`；工具 `gap-func-vs-scripts.py`、`aggregate-wave-results.py` 等；历史误入库的 `as-built/runs/` 已从 git 移除（本地波次仍 gitignore）。

### 相对 registry DoD 的 as-built 说明

| 原 DoD 表述 | 实际 |
|-------------|------|
| gold.yaml + scripts.yaml | **已废止**；以 `schema.md` §cases-v1 为准 |
| 本阶段禁止 runner | 编制阶段已结束；**S3 已在监管人环境下 smoke/full 机跑**（见下），不将 runs 目录入库 |
| 32 入口补齐 | 含先期 search/key-type，合计 **34 live 入口** 均已落盘 |

## 产物清单

| 产物 | 路径 |
|------|------|
| 脚本工程 | `agent-delivery/qa/as-built/scripts/KJZTFWXT/**` |
| 入口台账 | `agent-delivery/qa/as-built/catalog/KJZTFWXT.yaml` |
| 派单包（历史） | `agent-delivery/agent-handoffs/QA/QA-ASBUILT-SCRIPT-BATCH32-L01-派单包.md` |
| 回炉进度（参考） | `agent-delivery/agent-handoffs/QA/script-quality-rework-KJZTFWXT-progress.md` |
| 本 handoff | `agent-delivery/agent-handoffs/QA/QA-ASBUILT-SCRIPT-BATCH32-L01.md` |

## S3 机跑摘要（证据在本地 runs，不入库）

| 波次 | 行数 | 通过 | 不通过 | 跳过 | 待人工 |
|------|------|------|--------|------|--------|
| `20261015-50892-smoke-r1`（金样） | 167 | 156 | 11 | — | — |
| `20261016-50892-full-r1`（全量） | 774 | 414 | 205 | 137 | 18 |

- 汇总表：`qa/as-built/runs/{波次}/results.xlsx`（`aggregate-wave-results.py` 生成）。
- **不通过 / 待人工** 未在本单内全部回炉；产品缺陷 vs C4 脚本债 vs C6 分诊 **另开 bugfix/S2 子波**，不阻塞「脚本工程落盘」签收。

## 偏离说明

- 无业务仓改动；无 D12 越层。
- 用例册 `test-cases/KJZTFWXT/**` 自动化 ID 回填 **未随本 handoff 提交**（仍本地未 push）；与 S1 签收单独立。
- `task-registry` 在 2026-10-16 rebase 时保留远端版本，**父单 ID 若在看板缺失**需 coordinator 用 MCP 补登或恢复（本 handoff 仍用原 ID）。

## 验收证据

| 项 | 值 |
|----|-----|
| 分支 | `dev` |
| commit A | `51ca61b0` — feat(qa): KJZTFWXT as-built 脚本 cases-v1 全量 |
| commit B | `19c27019` — docs(qa): S2/S3 编排手册与汇总工具，runs 移出版本库 |
| 远程 | `origin/dev`（2026-10-16 push） |
| gap | 774/774/0 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python / 前端只调 Java | ✅（本单仅 QA 资产） |
| 未改 lumen/demo 业务仓 | ✅ |
| D8/D9/D10 实现 | N/A（脚本层；指标 ⓘ 由用例/页面叶负责） |
| 环境 50892、非 localhost | ✅ |
| runs 不入库 | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | （未统计） |
| model_used | Cursor 多会话 + human 监管 |
| actual_cost | — |
| cost_warn | green |
| source | 略 |

## 联调确认

脚本编制与仓内 push 已完成；S3 full-r1 已跑毕。**请监管人黄敬洲核对 handoff 与 commit 后签收**；最终 `done` 按团队闸门由 `human:淮政玮`（tech_task 若豁免则以 registry 为准）。

ponytail: full
