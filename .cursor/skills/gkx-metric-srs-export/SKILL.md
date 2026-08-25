---
name: gkx-metric-srs-export
description: >
  Regenerates the full 指标需求来源 Excel (registry catalog + SRS book/seq/name/brief
  + 展示系统/专题系统). Use when the user says 导出指标需求来源,
  带有需求来源的完整Excel, 指标需求来源表, 需求来源完整表, 需求来源Excel,
  需求来源没有填全, 来自专题还是展示, 来源系统, or metric-srs-export.
  Calls MCP metric-registry tool metric-srs-export (rebuilds sidecar from A1/A2 first);
  does not write seed/matrix YAML and does not change Feishu progress columns.
  Not for single-metric 8件套 lookup (use gkx-metric-lookup) and not for
  指标进度统计 (use gkx-metric-progress).
---

# 指标需求来源（完整 Excel）

把当前 `metrics/registry/` 全量投影成带 **SRS 需求来源** 的 Excel。与飞书「指标与数据开发进度」**分文件**，禁止往进度表加列。上手：`agent-delivery/metric-mcp-usage-guide.md` §3.5。Codex 指针：`.codex/skills/gkx-metric-srs-export/`。

产物：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`（汇总 / 指标目录 / 需求来源明细）。

| 工作表 | 系统列 | 含义 |
|---|---|---|
| 指标目录 | **来源系统** | 该指标全部需规并集：展示系统 / 专题系统 / 展示+专题 / 算法库 |
| 指标目录 / 明细 | **决策清单中的编号** | `客户决策清单跟踪表.md` 的 Q 号；空=未点名本指标 |
| 需求来源明细 | **系统** | 这一条需规挂在哪套 A2；仅 05、没有页面时为「算法库」 |

Sidecar：`metrics/registry/metric-srs-map.yaml`（需规叶子，**不是** 8 件套；`srs_refs[].systems` 为 `展示` / `专题`）。导出前必须重建，禁止拿旧 map 充「已填全」。

## 何时用

用户说 **导出指标需求来源** / **带有需求来源的完整 Excel** / **指标需求来源表** / **需求来源没有填全** / **来自专题还是展示** / **来源系统** / `metric-srs-export`。

不要用本 skill：查单条 8 件套或单条 SRS → `gkx-metric-lookup`；导出飞书同列进度表 → `gkx-metric-progress`；改 seed/矩阵 → data-agent。

## 怎么跑

1. 调 MCP `metric-registry` → **`metric-srs-export`**（无参数）。它会先跑 `node scripts/build-metric-srs-map.mjs`，再写 xlsx。
2. 面板若仍只有 4 个工具：提示 Reload Window 后再调。MCP 未加载时才用后备：

```powershell
node scripts/build-metric-srs-map.mjs
python agent-delivery/metrics/registry/export/export_metric_srs_board.py --json
```

只跑 Python **不会**重建 map，会把旧 sidecar 再导一遍。

3. 对人只报：`xlsx` 路径、`catalog_rows` / `with_refs` / `without_refs`、`by_book`（02 / 04 / 05）、`by_system`（展示系统 / 专题系统 / 展示+专题 / 算法库）。`by_system` 计的是**明细行**，不是目录行。若 `xlsx_locked=true`：主文件正被 Excel 打开，已写时间戳副本，请关掉后再跑一次以覆盖主文件。
4. **空来源 = 尚未从 A1/A2 对上，不是「无需求」。** 禁止编造 `srs_refs`。`seq` 只在分册内唯一（02 的 97 ≠ 05 的 97）。
5. 回填来源（生成脚本已吃这些，不要手填 YAML）：
   - **05**：A1 表1 正式 `M_*`；`TEMP_ALGO_*` 按赋号约定派生的 `M_{维}_{层}_{seq}_{n}`（若已在注册表）；A2 `A1需规ID` / `05 seq N` / `algo_lib_leaf`。
   - **02 / 04**：A2 正式 `M_*` + 取数依据 `srs/02 seq N`、`04 seq N`、展示/专题页 `SRS seq N`（闭区间跨度 ≤2 才展开；更宽的 `40–58` 不编造单号）。专题页写明「不消费」的 demand 不把展示 `M_*` 挂到 04。
   - T0X 正式号回写 A2 `metric_id: null` 用 `node scripts/apply-t0x-a2-metric-ids.mjs`（不改差集判定，幂等）。**导出不必每次跑**；用户点名「回写 T0X / 整批回写」才跑。
6. 557 条目录**不会**全绿。未回填包括：A2 `n/a_ops` / `other_system` / `missing` 且无正式 ID、矩阵-only、A2 尚未挂 A1 的页 KPI。对人照实报缺口，不要说「已填全」。
7. **禁止**整文件读 `cfg_metric-*-seed.yaml` / `metric-readiness-matrix-*.yaml` / `metric-srs-map.yaml` 来回答单条口径。
8. 未点名 `commit` / `push` 不要提交。xlsx 只覆写 `registry/export/` 主文件；时间戳副本不要进 git。sidecar 由 builder 覆写，不手改。
