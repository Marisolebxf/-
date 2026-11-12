# handoff · POL-L2-DS12-SIM-237-COVER-FDE-L01

- 时间：2026-11-12
- 监管人：human:淮政玮
- 裁定：卡1=A、卡2=B；样例 `18318861`；批准 UPDATE ADS
- ponytail: full

## 范围与实现

闭合 237 需规分句：关键词 + 核心内容/支持对象/申报条件/支持力度 在 live 可见且可演。真 NLP async 另单 `POL-L2-DS12-SIM-237-ASYNC-L01`（backlog）。

## 产物

| 层 | 产物 |
|---|---|
| 审计/A/B | `sdd/简报/2026-11-12-政策文本智能解析-需规分句闭合.md`、`…-A-product.md`、`…-B-arch.md` |
| C/D/E 简报 | `sdd/简报/2026-11-12-SIM-237-COVER-FDE-CDE.md` |
| 说明书 | #### 237 回写四键 + 样例 UPDATE + ASYNC 边界 |
| ADS | `policy_text_parse` `18318861` 已 UPDATE（summary/tags/四键；保留 clauses） |
| 脚本 | `lumen-algo-py/scripts/patch_policy_text_parse_237_demo.py`（已 push） |
| FE | `InterpretWorkbench` 固定五区 + options 含 18318861；本地 commit `c406b59` **待推** |
| 用例 | `POL-L2-DS12-SIM-合规演示用例.md` 237 可演 + 主路径第 1 步 |

## 验收证据

- 库核：四键 ok、clauses 保留、summary_len>0、auto_tags 三词
- `node simulationLive.test.mjs` 绿
- Java 读列未改；FE 推送后即可在页选 18318861 点解析冒烟

## 架构合规

- 调用链：仍 `jobs`·文本解析 → element 只读 ADS ✅
- 禁 `run()` ✅；不建 gapfill ✅；D12 无 demo 直连 ✅
- 真算另单，本叶不进 async 白名单 ✅

## cost（估）

- model_used: composer
- actual_tokens: ~80000（估）
- actual_cost: —
- cost_warn: green
