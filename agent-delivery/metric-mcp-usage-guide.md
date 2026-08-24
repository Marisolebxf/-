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
- **需求来源**（SRS 哪一条）= `extras.srs_refs`（`book` / `seq` / `name` / `brief`）。**不是** 8 件套。空列表 = 尚未从 A1/A2 回填。`seq` 只在分册内唯一（02 的 97 ≠ 05 的 97）。
- **域** = 顶层 `domain`（中文枚举：企业/产业链/产业服务/政策/综合/创新/技术/机构/人才/通用/科技动态）+ `domain_code`（ENT/CHAIN/…）。**不是** 8 件套。`metric-query` / `metric-summary` 的 `domain` 参数中文或代码均可。
- 只有 seed 或只有矩阵时，`found.seed` / `found.matrix` 会标出来，不要脑补另一侧。

口头仍称「8 件套」，身份证 9 项：`metric_id` / `metric_name_zh` / `definition` / `formula` / `algorithm_type` / `source_tables` / `source_systems` / `update_freq` / `version`。

---

## 二、安装配置

| 文件 | 用途 |
|------|------|
| `.cursor/mcp.json` | 注册 `metric-registry`（相对路径 `scripts/metric-mcp-server.mjs`） |
| `.cursor/mcp.json.example` | 团队模板 |
| `.cursorignore` | 屏蔽 seed / 矩阵 YAML，逼走 MCP |
| `.cursor/skills/gkx-metric-lookup/SKILL.md` | 单条 8 件套 / D1–D4 / 单条 SRS |
| `.cursor/skills/gkx-metric-progress/SKILL.md` | 飞书同列进度 Excel |
| `.cursor/skills/gkx-metric-srs-export/SKILL.md` | 带需求来源的完整 Excel |
| `.codex/skills/gkx-metric-*/SKILL.md` | Codex 同事副本（真源在 `.cursor/skills/`） |

MCP 面板应看到 **`metric-registry`** 五个工具：`metric-get` / `metric-query` / `metric-summary` / `metric-progress-export` / `metric-srs-export`。未出现则重启 Cursor。

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

返回要点：`kit`、`readiness`、`extras.srs_refs`、`found`、`sources.seed_file` / `matrix_file` / `srs_map_file`。找不到时带 `suggestions`。

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

返回 `xlsx` 路径、`rows` / `assessed`、`domain` / `algorithm_type` / `contract_set` / `overall`。表在 `指标名` 后有 **域**（中文枚举，不是 8 件套）；**模块** 列名不改。产物：`metrics/registry/export/指标与数据开发进度.xlsx`。Skill：`gkx-metric-progress`。

### 3.5 metric-srs-export

导出「指标需求来源」完整 Excel：注册表全量一行一条，带 SRS 分册/序号/名称/简述。不调飞书 API，不改 seed/矩阵，不改飞书进度表列。

```
导出带需求来源的完整 Excel
  → metric-srs-export
```

返回 `xlsx` 路径、`catalog_rows` / `with_refs` / `without_refs`、`by_book`。空来源 = 尚未从 A1/A2 回填。产物：`metrics/registry/export/指标需求来源.xlsx`。Skill：`gkx-metric-srs-export`。后备 CLI：

```powershell
python agent-delivery/metrics/registry/export/export_metric_srs_board.py --json
```

---

## 四、禁止

- 直接读/改 `agent-delivery/metrics/registry/cfg_metric-*.yaml`、`metric-readiness-matrix-*.yaml` 或 `metric-srs-map.yaml` 来回答「这条指标是什么 / 接入到哪 / 需求来自哪条 SRS」
- 把 D1/D2/D3/D4、`lifecycle_stage` 或 `srs_refs` 说成 8 件套
- 用本 MCP 改口径、改公式、改绿就绪度（改 YAML 走 data-agent 正式化，见 `metrics/README.md`）
- 未填类型时当成 `STAT` 充数
