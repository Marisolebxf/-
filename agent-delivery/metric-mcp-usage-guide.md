# Metric Registry MCP 使用说明

> 按 `metric_id` 或中文名查询 **8 件套（身份，v1.5 共 9 项）** 和 **D1–D4 接入状态**，不要让 agent 直接打开 `metrics/registry/*.yaml`。

对照任务 MCP：`task-mcp-usage-guide.md`。seed/矩阵 **只读**（无 claim / 无改口径）。`metric-progress-export` 只覆写离线 Excel，不写 YAML。

---

## 一、两套真源（禁止混说）

| 问 | 真源 | MCP 字段 |
|----|------|----------|
| 这条指标是什么（身份证） | `metrics/registry/cfg_metric-{域}-seed.yaml` | `kit`（9 项） |
| 现在算不算得出（角标） | `metrics/registry/metric-readiness-matrix-{域}.yaml` | `readiness`（D1–D4 + 可选 `lifecycle_stage`） |

- D1–D4 **不是** 8 件套字段；`aligned` + `D4=mock` 合法。
- 未写 `algorithm_type` → `UNKNOWN`（`kit.algorithm_type_inferred=true`）。`UNKNOWN` 禁止派实现单，也禁止把 D1 说成 aligned。
- 未写 `lifecycle_stage` → `unspecified`。该字段同样不进 8 件套。
- 只有 seed 或只有矩阵时，`found.seed` / `found.matrix` 会标出来，不要脑补另一侧。

口头仍称「8 件套」，身份证 9 项：`metric_id` / `metric_name_zh` / `definition` / `formula` / `algorithm_type` / `source_tables` / `source_systems` / `update_freq` / `version`。

---

## 二、安装配置

| 文件 | 用途 |
|------|------|
| `.cursor/mcp.json` | 注册 `metric-registry`（相对路径 `scripts/metric-mcp-server.mjs`） |
| `.cursor/mcp.json.example` | 团队模板 |
| `.cursorignore` | 屏蔽 seed / 矩阵 YAML，逼走 MCP |
| `.cursor/skills/gkx-metric-lookup/SKILL.md` | Cursor skill |
| `.codex/skills/gkx-metric-lookup/SKILL.md` | Codex 同事副本 |

MCP 面板应看到 **`metric-registry`** 四个工具：`metric-get` / `metric-query` / `metric-summary` / `metric-progress-export`。未出现则重启 Cursor。

前置：Node.js 18+，无额外 npm 依赖。自检：

```
node scripts/metric-mcp-selfcheck.mjs
```

---

## 三、工具

### 3.1 metric-get

精确查一条。

```
metric_id 是 M_ENT_TOTAL_COUNT 的 8 件套和接入状态？
  → metric-get  metric_id="M_ENT_TOTAL_COUNT"
```

返回要点：`kit`、`readiness`、`found`、`sources.seed_file` / `matrix_file`。找不到时带 `suggestions`。

### 3.2 metric-query

模糊搜，默认最多 20 条 summary。

```
企业域里名字带「总数」、D4 还是 mock 的指标
  → metric-query  q="总数"  domain="ENT"  d4="mock"  limit=10

CHAIN 里 D1=aligned 的列表
  → metric-query  domain="CHAIN"  d1="aligned"  fields="summary"
```

`fields=full` 才带完整 kit+readiness。不要无过滤倾倒全表。

### 3.3 metric-summary

只给计数。

```
现在 registry 覆盖如何？
  → metric-summary

只看 SVC（有矩阵、可能无 seed）
  → metric-summary  domain="SVC"
```

### 3.4 metric-progress-export

重新执行「指标进度统计」：按飞书「指标与数据开发进度」同列覆写离线 Excel。不调飞书 API，不改 seed/矩阵。

```
重新执行一下「指标进度统计」
  → metric-progress-export
```

返回 `xlsx` 路径、`rows` / `assessed`、`algorithm_type` / `contract_set` / `overall`。产物：`metrics/registry/export/指标与数据开发进度.xlsx`。Skill：`gkx-metric-progress`。

---

## 四、禁止

- 直接读/改 `agent-delivery/metrics/registry/cfg_metric-*.yaml` 或 `metric-readiness-matrix-*.yaml` 来回答「这条指标是什么 / 接入到哪」
- 把 D1/D2/D3/D4 或 `lifecycle_stage` 说成 8 件套
- 用本 MCP 改口径、改公式、改绿就绪度（改 YAML 走 data-agent 正式化，见 `metrics/README.md`）
- 未填类型时当成 `STAT` 充数
