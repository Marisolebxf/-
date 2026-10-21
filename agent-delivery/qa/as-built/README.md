# As-built 测试线（B 线执行仓）

> **过程**（`prompts/_case.md` · `_script.md` · `_result.md` · `_submit.md`）：**测试用例**（人读场景）→ **测试脚本** → **测试结果** → **总集提交表**（已覆盖功能点从场景用例切点投影；未覆盖不在第 4 步）。  
> **A 线**（v8 功能点拆分）不在本目录维护；第 1 步写完用例后做 **功能点→用例** 覆盖矩阵，未覆盖允许登记，禁止按功能点一对一灌用例。  
> **规范**：人读编号遵守 `qa-test-case-spec.md`；脚本 id 为功能内 `P0-xx`。  
> **执行环境（本线锁定）**：专题 <http://10.50.69.111:30892/> · 算法库联调台 <https://edu.itic-sci.com/dma/algovwz/>（`lumen-ui-algo-apiview`，hash 路由；`111.198.38.90:50897` 已停用）。禁止 localhost。  
> **脚本补齐（FUNC↔scripts 缺口）**：编排真源 [`script-backfill-playbook.md`](script-backfill-playbook.md)；缺口机检 `tools/gap-func-vs-scripts.py` → `script-backfill-gap-{系统}.md`。  
> **脚本批量执行（S3）**：[`script-batch-run-playbook.md`](script-batch-run-playbook.md)（冒烟/全量/回归、波次目录、强制 Excel+总结）；总路由 [`../func-test-playbook-index.md`](../func-test-playbook-index.md)。

## 三大系统

| 系统码 | 中文 | 本线现状 |
|--------|------|----------|
| `KJZTFWXT` | 科技专题服务系统 | **当前执行对象**（30892） |
| `KJXXZSXT` | 科技信息展示系统 | 台账占位，环境未锁 |
| `SDWJSF/KJZTFWSFK` | 科技专题服务算法库 | **algovwz 联调台**（89 页 + 总览/登录）；招标用户端仍无，验收入口见 `catalog/SDWJSF-KJZTFWSFK.yaml` |

系统码与总集一致（算法库工作区用 `SDWJSF/KJZTFWSFK`，交付转录仍可映射 `SDWJSF/KJZTFWSFK`）。

## 目录

```text
as-built/
  README.md                 本文件
  schema.md                 字段 / 状态 / 落盘约定
  catalog/                  L0 功能入口台账（可增删，不删历史 id）
    index.yaml
    KJZTFWXT.yaml
    KJXXZSXT.yaml
    SDWJSF-KJZTFWSFK.yaml
  scripts/{系统}/{模块}/{功能}/   测试脚本（yaml）+ fixtures
  prompts/                  过程提示词（_case / _script / _result / _submit）+ 按功能顺序
  tools/                    辅助 node 脚本 + 业务仓 e2e spec 指针
  runs/{run-id}/            每一次执行的明细 / 汇总 / 中间过程（**唯一**落盘根；见下）
    scripts/{id}/           该条脚本的结果（result.yaml + steps.md）
```

### Runs 落盘根（勿混用）

| 路径 | 状态 |
|------|------|
| **`as-built/runs/{波次}/`** | ✅ **唯一真源**。`run-scripts.mjs` 默认 `runsRoot`、S3 `script-batch-run-playbook.md`、`aggregate-wave-results.py` 均在此；**gitignore，不入库** |
| `qa/runs/`（`as-built` 的兄弟目录） | ❌ **历史误用**（早期手填 `--run-dir` 或旧会话产物）；**禁止新建**；已加入根 `.gitignore` |
| `test-records/{系统}/R{n}/` | 正式交付轮次工作稿（从 as-built 波次摘要拷贝，非 runner 默认输出） |

增减入口：只改 `catalog/{系统}.yaml` 的 `entries[]`（`status` 用 `live|hidden|stub|planned|retired|not_in_env|no_ui`），**不要改 id**。新模块新建 `scripts/...` 子目录即可。

catalog 字段：`scripts` / `gold` / `full_scripts`（指向 yaml 目录与金样/全量文件）。

## 金样

- 功能：`KJZTFWXT / enterprise / search`（企业查询，2026-10-13 v2.0 重写）
- 过程：`scripts/KJZTFWXT/enterprise/search/gold.yaml`
- 提示词：`prompts/KJZTFWXT/enterprise/search/gold.md`
- 当前执行：`runs/20261013-50892-search-r2/`（v2.0 重写后全量重跑：41 脚本，P0 18 全过；合计 35 pass / 3 fail（导出断头 C1）/ 3 n/a）。2026-08 首轮金样与全量两个 run 已随 v2.0 重写删除（历史见 retro/20261013-script-rewrite-pilot.md）。

## 企业查询全量（P0/P1 正向）

金样五条只做冒烟。**写全 / 回归**用：

| 文件 | 用途 |
|------|------|
| `scripts/KJZTFWXT/enterprise/search/scripts.yaml` | P0-06 起 + 全部 P1；`includes` 金样 |
| `scripts/KJZTFWXT/enterprise/search/coverage.md` | **脚本→用例**（旧表曾把 FUNC-000xx 误当功能点，新模块勿效仿） |
| `prompts/KJZTFWXT/enterprise/search/full.md` | 全量执行顺序（先金样再其余） |

P2 / 访客最近检索 / 跨模块对比篮深度：**登记在 coverage 暂缓**。导出文件+字段已进 P1-11/P1-22，不再暂缓。

## 重点企业类型分析（三步试跑 · 2026-08-28）

| 步骤 | 产物 |
|------|------|
| 测试用例 | `qa/test-cases/KJZTFWXT/enterprise-企业分析/KEYENT-重点企业类型分析/FUNC-重点企业类型分析-用例.md`（FUNC-00046～00061）+ `coverage-fp.md`（T09 46 点） |
| 测试脚本 | `scripts/KJZTFWXT/enterprise/key-type/` |
| 测试结果 | `runs/20261014-50892-keytype-r2/`（v2.0 重写后全量重跑：24 脚本全 pass；P0 14 / P1 9 / P2 1）。2026-08-28 旧 run 已随 v2.0 重写删除 |
