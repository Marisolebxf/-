# As-built 测试线（B 线执行仓）

> **过程**（`prompts/_case.md` · `_script.md` · `_result.md` · `_submit.md`）：**测试用例**（人读场景）→ **测试脚本** → **测试结果** → **总集提交表**（已覆盖功能点从场景用例切点投影；未覆盖不在第 4 步）。  
> **A 线**（v8 功能点拆分）不在本目录维护；第 1 步写完用例后做 **功能点→用例** 覆盖矩阵，未覆盖允许登记，禁止按功能点一对一灌用例。  
> **规范**：人读编号遵守 `qa-test-case-spec.md`；脚本 id 为功能内 `P0-xx`。  
> **执行环境（本线锁定）**：<http://111.198.38.90:50892/>（已发布专题前端）。禁止 localhost。

## 三大系统

| 系统码 | 中文 | 本线现状 |
|--------|------|----------|
| `KJZTFWXT` | 科技专题服务系统 | **当前执行对象**（50892） |
| `KJXXZSXT` | 科技信息展示系统 | 台账占位，环境未锁 |
| `KJZTFWALGO` | 科技专题服务算法库 | 无独立用户前端；入口标 `no_ui` |

系统码与总集一致（算法库工作区用 `KJZTFWALGO`，交付转录仍可映射 `SDWJSF/KJZTFWSFK`）。

## 目录

```text
as-built/
  README.md                 本文件
  schema.md                 字段 / 状态 / 落盘约定
  catalog/                  L0 功能入口台账（可增删，不删历史 id）
    index.yaml
    KJZTFWXT.yaml
    KJXXZSXT.yaml
    KJZTFWALGO.yaml
  scripts/{系统}/{模块}/{功能}/   测试脚本（yaml）+ fixtures
  prompts/                  过程提示词（_case / _script / _result / _submit）+ 按功能顺序
  tools/                    辅助 node 脚本 + 业务仓 e2e spec 指针
  runs/{run-id}/            每一次执行的明细 / 汇总 / 中间过程
    scripts/{id}/           该条脚本的结果（result.yaml + steps.md）
```

增减入口：只改 `catalog/{系统}.yaml` 的 `entries[]`（`status` 用 `live|hidden|stub|planned|retired|not_in_env|no_ui`），**不要改 id**。新模块新建 `scripts/...` 子目录即可。

catalog 字段：`scripts` / `gold` / `full_scripts`（指向 yaml 目录与金样/全量文件）。

## 金样

- 功能：`KJZTFWXT / enterprise / search`（企业查询）
- 过程：`scripts/KJZTFWXT/enterprise/search/gold.yaml`
- 提示词：`prompts/KJZTFWXT/enterprise/search/gold.md`
- 首轮执行：`runs/20260826-50892-search-gold/`
- 全量试跑：`runs/20260826-50892-search-full/`（P0 18 pass；P1 20 pass / 4 n/a / **2 fail** 导出无文件）。2026-08-27 已补每条 `scripts/{id}/` 与检索/抽屉 `observed/`；导出加严后 P1-11/P1-22 为 C1。

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
| 测试用例 | `qa/test-cases/KJZTFWXT/KEYENT/FUNC-重点企业类型分析-用例.md`（FUNC-00046～00061）+ `coverage-fp.md`（T09 46 点） |
| 测试脚本 | `scripts/KJZTFWXT/enterprise/key-type/` |
| 测试结果 | `runs/20260828-50892-key-type-full/`（P0 11 pass / P1 5 pass / Fail 0） |
