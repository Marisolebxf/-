# BATCH32 方法论补丁（2026-10-14）

> 背景：铺开至 ~24/34 live 入口后叫停。问题不是吞吐，而是「有脚本 ≠ 可机跑绿」：`allow_skip` 命中约 262 行，环境债被脚本层吞掉。  
> 父单：`QA-ASBUILT-SCRIPT-BATCH32-L01`。本文件生效后，续派 / 回炉必须遵守。

## 1. 双档产物（强制）

| 档 | 内容 | 交卷门槛 |
|----|------|----------|
| **A · smokeable** | `index.yaml` 的 `gold:` + 对应 `cases/{id}.yaml`（建议 3～5 条，不强制 5）；仅**当前环境可机跑绿**主路径 | 父 agent 用 `tools/run-scripts.mjs --only <gold-ids>` **headless 全绿**才算过 |
| **B · coverage** | 其余 `cases/*.yaml` | 允许 `allow_skip` / `manual`，但须挂 **缺陷/环境单号或 GAP 引用**；禁止无编号裸 skip |

禁止再交「条数漂亮、金样也 skip」的包。

### 1.1 布局 cases-v1（一用例一文件 · 2026-10-14 增补）

```text
{功能}/
  index.yaml           # layout: cases-v1；gold: […]；all: […]（可选）
  cases/P0-01.yaml     # 单文件 = 一条脚本对象
  cases/P0-02.yaml
  fixtures/…
  coverage.md
```

| 规则 | 说明 |
|------|------|
| **新写 / 回炉** | 必须 cases-v1；禁止再写大 `scripts.yaml` / `gold.yaml` |
| **存量** | **2026-10-14 已全量拆分**（25 入口 / 577 条；`id→func_id` 对账 DIFF_OK；catalog 24 处改挂 `index.yaml`+`cases/`） |
| **回放 / 改稿** | `--only P0-0x`；改一条只动一个 `cases/*.yaml` |
| **runner** | 仅 cases-v1（旧双文件加载已删） |

## 2. allow_skip 配额

- 金样（A 档）：**禁止** `allow_skip: true`（环境不通 → 模块 `blocked`，不写假金样）。
- 全量（B 档）：`allow_skip` 脚本条数 / 全量条数 **≤ 25%**；超阈 → 交卷失败，标 blocked + 环境/缺陷清单。
- 每条 skip 必须写：`skip_reason` + `ticket`（缺陷 ID / 环境债 ID / `GAP-*` / `Q0xx`）；仅写「数据空」不合格。

## 3. 环境前置闸门（写结果态之前）

下列任一不过，**禁止**写过程态/结果态机检脚本（可只写配置空态/门控 disabled 断言）：

1. 登录 + 深链可达目标路由（`survey-page.mjs` 先 `/login`）。
2. 「开始分析」在合法对象选齐后为 **enabled**（或本页无异步分析）。
3. 评估类：回填对象后无「预检未返回企业明细」阻塞。
4. 诊断/图谱类：所用产业组合不触发 `INPUT_OBJECT_INVALID`（生物等已知坏组合写入 fixtures 黑名单）。
5. 历史结果依赖：至少 1 条**已完成**任务可供「查看结果」（否则结果态整段放入 B 档 skip + ticket，不进金样）。

闸门证据落 `fixtures/scout/env-gate.json`（pass/fail + 截图路径）。

## 4. 探针公约

- **只用**独立无头：`tools/survey-page.mjs`（或同目录一次性 headless）；禁止 IDE/`cursor-ide-browser`/`user-playwright` 共享有头。
- **禁止**对 `disabled` / `not visible` 控件硬点；失败落 `scout-*.json` 后继续，禁止卡死 30s+。
- 对比篮关闭、追溯 popover：可见才点；挡点击先 Esc。
- 二次探测产出一律进本模块 `fixtures/scout/`，禁止污染其他入口。

## 5. catalog 与并行

- 子 agent **不改** `catalog/KJZTFWXT.yaml`；交卷只报路径，由**父 agent 批量挂** `scripts`/`gold`/`full_scripts`。
- 写稿并发 ≤4；**金样机跑串行**（同时只 1 个 `run-scripts`）。
- 同波次目录互斥；半成品目录须在派单包 §进度标明。

## 6. 交卷抽检（父 agent）

1. 文件：`index.yaml` + `cases/*.yaml`（存量过渡期可仍为 gold+scripts）/ `coverage.md` / `fixtures/testdata.yaml` / `fixtures/scout/env-gate.json`
2. expect 双层；金样无 `allow_skip`
3. `node tools/run-scripts.mjs <功能目录> --only <金样ids逗号分隔>` → 全绿
4. B 档 skip 占比与 ticket 齐全
5. coverage 主表含列：**档(A/B)**、**skip ticket**

## 7. 偏差分级（as_built_note）

| 级 | 含义 | 处理 |
|----|------|------|
| D1 文案/结构 as-built | 现场与用例文案不一致但可测 | 脚本跟现场；note 标明 |
| D2 用例过时 | 控件形态变了（chip→下拉） | 脚本跟现场；回开用例修订单 |
| D3 产品缺陷 | 空搜仍检索、预检失败等 | 预期红或 skip+缺陷单；**不进金样** |
| D4 环境债 | 无成功任务、坏产业组合 | skip+环境单；金样绕开 |

## 8. 回炉试点（本轮）

| 域 | entry_id | 目录 | 选型理由 |
|----|----------|------|----------|
| enterprise | `ent-eval-tech` | `enterprise/eval-tech/` | 评估类预检失败 / 结果链 skip 典型 |
| industry-center | `chain-bottleneck` | `industry-center/bottleneck/` | 诊断类过程 UI / 失败单查看结果典型 |
| service | `svc-portal` | `service/portal/` | 门户诚实空 skip 典型；刚交易回炉 |

**试点目标（每个）**：

1. 重写 A 档金样：3～5 条，**零 allow_skip**，父 agent runner 全绿。  
2. 整理 B 档：skip ≤25% 且条条有 ticket；超阈则砍脚本改声明「本轮不自动化」。  
3. 补 `env-gate.json` + coverage 档列。  
4. **不**新开未铺模块；**不**改业务仓；catalog 仍由父挂（路径不变则可不改）。

**试点并发**：3 路可并行写；金样机跑由父串行验收。
