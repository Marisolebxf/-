# DATA-SUPPLIER-Q-PROGRESS-L01 · 指标进度导出 — 源缺口 sidecar 优先接线

> coding 叶。`export_feishu_metric_board.py`「源缺口」优先读 sidecar；JSON / MCP 回报三类计数。未改 seed、未改 D3 枚举、未改飞书列集合。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户点名认领并执行；跨切叶不套专题维度Owner。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短接线：sidecar 有 `as_of`+`summary` 写 `[{as_of}] {summary}`，否则回落 `d3_gap`。未新依赖、未改飞书列。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓导出脚本，未走 Headroom。 |

## 范围与实现

1. `parse_source_gap_index()` 读 `question/source-gap-index.yaml`；缺键视为无 sidecar。
2. 行字段 `源缺口` + 内部 `source_gap_kind`（`indexed` / `fallback` / `empty`）；xlsx 仍用原列名「源缺口」。
3. `--json` / MCP：`source_gap_indexed` / `source_gap_fallback` / `source_gap_empty` + `source_gap_by_domain` / `source_gap_by_algorithm_type`。
4. 表头批注、`gkx-metric-progress` skill、`metric-mcp-usage-guide` §3.4、MCP 工具描述同步。
5. 自检：POLICY sidecar `M_POLICY_TEXT_PARSE` 单元格以 `[2026-09-01]` 开头；`indexed>=20`；三类之和 = `rows`。

## DoD 对照

| 项 | 结果 |
|----|------|
| 导出读 sidecar；单元格 `[{as_of}] {summary}`；无则回落 `d3_gap` | ✅ 实测 indexed=25 fallback=458 empty=77（合计 560） |
| MCP / `--json` 含三类计数（可按域、algorithm_type） | ✅ |
| skill + usage-guide §3.4 须报源缺口概要；表头批注 sidecar 优先 | ✅ |
| 禁止写 seed/矩阵 YAML；不改飞书列集合 | ✅ |
| handoff + cost；ponytail: full | ✅ |

## 偏离说明

`node scripts/metric-mcp-selfcheck.mjs` 仍有 1 条预存失败：`M_ENT_TOTAL_COUNT definition mentions credit code`（与本叶无关）。本叶新增的 `source_gap_indexed` / kinds sum 两条均 ok。

## 产物清单

- `agent-delivery/metrics/registry/export/export_feishu_metric_board.py`
- `scripts/metric-mcp-server.mjs`（工具描述）
- `scripts/metric-mcp-selfcheck.mjs`（源缺口断言）
- `.cursor/skills/gkx-metric-progress/SKILL.md`
- `.codex/skills/gkx-metric-progress/SKILL.md`
- `agent-delivery/metric-mcp-usage-guide.md` §3.4
- 覆写 `agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`（未要求则不 commit）
- 本 handoff

## 验收证据

```text
python …/export_feishu_metric_board.py --json
source_gap_indexed=25  source_gap_fallback=458  source_gap_empty=77
政策: indexed=25 fallback=10
```

政策 25 条 sidecar 与 `source-gap-index.yaml` 条数一致。`scripts/lib/metric-progress-export.mjs` 原样透传 Python JSON，未改。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写业务算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ 未引入 Neo4j |
| 4 可观测性 | N/A（导出脚本） |
| 5 CI/CD | skip / 编排仓文档+脚本；本叶未 push |
| 6 demo2 merge | ✅ |
| 7 共享聚合 | ✅ |
| 8 数据策略 | ✅ sidecar ≠ D3 真源 |
| 9 D8 | N/A |
| 10 D9 | ✅ 未改 seed/矩阵；sidecar 不是 8 件套 |
| 11 D10 | N/A |
| 12 D12 | ✅ 未调 demo 服务 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~70000（估：接线 + 导出自检；非整会话精确计数） |
| model_used | Cursor Grok 4.6 |
| actual_cost | ~0.35 USD |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓；本叶按惯例 **未 commit / 未 push**，待用户指令）
- commit：无
- pipeline URL / ID：skip
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- 命令：`python agent-delivery/metrics/registry/export/export_feishu_metric_board.py --json`

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- Tempo / Loki：无

## 遗留风险 / 开放项

- 飞书 Bitable 同步脚本未改「源缺口」列逻辑（配额；本叶 DoD 不改飞书列集合）。下次 `sync-feishu-metric-board.mjs` 仍写矩阵 `d3_gap`。
- xlsx 已覆写主文件；是否入库由用户决定。
