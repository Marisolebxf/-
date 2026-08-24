---
name: gkx-metric-progress
description: >
  Regenerates the Feishu-format 指标与数据开发进度 Excel from metrics/registry.
  Use when the user says 指标进度统计, 重新执行一下指标进度统计,
  重新执行一下"指标进度统计", 导出指标进度, 同步指标进度表,
  or metric-progress-export. Calls MCP metric-registry tool metric-progress-export;
  does not write seed/matrix YAML. Not for single-metric 8件套 lookup (use gkx-metric-lookup)
  and not for Feishu API sync (quota-bound).
---

# 指标进度统计（离线看板）

把当前 `metrics/registry/` 投影成飞书「指标与数据开发进度」同列 Excel。飞书开放平台配额不够时用这张表。上手：`agent-delivery/metric-mcp-usage-guide.md` §3.4。Codex 指针：`.codex/skills/gkx-metric-progress/`。

## 何时用

用户说 **指标进度统计** / **重新执行一下「指标进度统计」** / 导出指标进度表。

不要用本 skill：查单条 8 件套 → `gkx-metric-lookup`；改 seed/矩阵 → data-agent；推飞书 Bitable → `sync-feishu-metric-board.mjs`（本月配额可能已满）。

## 怎么跑

1. 调 MCP `metric-registry` → **`metric-progress-export`**（无参数）。
2. 面板若仍只有 3 个工具：提示 Reload Window 后再调。MCP 未加载时才用后备：

```powershell
python agent-delivery/metrics/registry/export/export_feishu_metric_board.py --json
```

3. 对人只报：`xlsx` 路径、`rows` / `assessed`、`algorithm_type` / `contract_set` / `overall`。若 `xlsx_locked=true`：主文件正被 Excel 打开，已写时间戳副本，请关掉后再跑一次以覆盖主文件。
4. **禁止**整文件读 `cfg_metric-*-seed.yaml` / `metric-readiness-matrix-*.yaml`。
5. 未点名 `commit` / `push` 不要提交。xlsx 只覆写 `registry/export/`，不回写 YAML。
