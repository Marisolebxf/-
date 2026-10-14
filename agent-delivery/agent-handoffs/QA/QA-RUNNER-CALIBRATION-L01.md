# QA-RUNNER-CALIBRATION-L01 · 原生 Playwright runner 校准

> **状态**：已收口（2026-10-14）；r9 最终验证跑结果见 §3（runs 落盘为唯一真源）
> **监管**：human:黄敬洲 · **执行**：qa-agent
> **产物根**：`agent-delivery/qa/as-built/`

## 1. 范围与实现

- 落地 `tools/run-scripts.mjs`：原生 Playwright 跑批器（headless、单 context 顺序执行、逐步截图、SUMMARY/COMPARISON 自动落盘、`--check` 编译校验、`--only` 单测模式）。
- `pwExpect` 垫片：轮询式 `toBeVisible/toBeHidden/toBeDisabled/toHaveCount/toHaveAttribute/toHaveText/toContainText/toHaveValue/toHaveURL/toHaveTitle`。
- 词表（`tryHeuristic`）：中文 target 词 → Playwright locator 映射；SEARCH 域 71/71 全覆盖（审计脚本内联于校准过程，建议固化）。
- fixtures 真源：`scripts/KJZTFWXT/enterprise/search/fixtures/selectors.yaml`（四状态 DOM 实勘快照）。

## 2. 校准结果（SEARCH 41 条收敛全程）

| 轮 | 变更 | pass |
|---|---|---|
| r2 | MCP 有头基线 | 35 |
| r3 | runner 首跑 | 5 |
| r5 | 一次实勘 + 批量修 + 前置自足 | 19 |
| r7 | 补词表（应先审计——浪费的一轮） | 19 |
| r8 | 视口外浮动条文本级断言 | 21 |
| r9 | 修 `第[一二]张卡复选框` 正则同映射 bug | runs/20261014-50892-search-r9-runner |

KEYENT 24 条：一次校准通过（MCP/runner verdict 一致）。

## 3. 系统性根因清单（runner 工具层，波及面 > 单条脚本）

1. **R18 正则字符族掩盖多目标**：`第[一二]张卡复选框` 一条正则 return 同一 `.first()` → 两次点击同一行 = 勾选→取消 → 全部勾选族断言假红。修：一词一映射，序数语义目标禁用 `[一二]` 字符族。
2. **R19 视口外 toBeVisible 必假**：底部浮动条（已选 N 家企业）文本在 DOM、视口外。修：runner 新增 `floattext` kind（innerText 文本级断言）。
3. **R20 select_option 限原生 `<select>`**：Arco 下拉族改 click 展开 + click 选项。
4. **R17 词表审计先于重跑**：全量 target → tryHeuristic 正则扫描应为每功能铺开前置步骤，禁止"跑一轮发现一批"。
5. P7/P8（Arco 隐形 input 点容器、步骤前置自足）在 runner 下延续有效。

## 4. 教训与自我检讨

- r6→r7 一轮空跑：猜测驱动（"词表缺"）而非证据驱动（先审计）。正确顺序 = 先全量扫描覆盖率，再决定是否值得跑。
- "操作 ✓ 断言 ✗" 优先怀疑**点击语义错位**（同映射/勾选取消/遮挡），不要先怀疑断言写法——截图目视 diff（`ImageChops` bbox）是定位此类问题的最快手段。

## 5. 产物清单

- `qa/as-built/tools/run-scripts.mjs`（含 floattext kind、词表 +21 条、checkbox nth 修正）
- `qa/as-built/scripts/KJZTFWXT/enterprise/search/{scripts.yaml,gold.yaml,fixtures/selectors.yaml}`
- `qa/as-built/runs/20261014-50892-search-r{3..9}-runner/`（每轮 SUMMARY/COMPARISON/prompts-used）
- retro 增补：`qa/as-built/retro/20261013-script-rewrite-pilot.md` **§4.8**（R17~R22 runner 层教训与铺开闸门）

## 6. 架构合规自检

- 仅触碰 `agent-delivery/qa/as-built/`，未改业务仓 ✅；未越 QA 职责 ✅；50892 为测试环境只读交互 ✅。

## 7. 后续（并入 BATCH32 铺开流程）

1. 词表覆盖审计固化为 `tools/` 常驻脚本（R17 闸门，铺开每功能必跑）。
2. BATCH32 回炉三模块（ent-eval-tech / chain-bottleneck / svc-portal）先过 runner 校准再铺开。
3. retro §4.8 建议随 v1.3 spec 评审一并定稿。
