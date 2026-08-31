# DATA-POLICY-STORAGE-DEMO-METRIC-L01 · 灌数过程覆盖指标映射

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控：后续认领不必再问） |
| 说明 | 用户指令：把灌数过程覆盖的 `M_POLICY_*` 补进 `pipeline-demo-mock.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类，不改代码） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓 Markdown |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-ETL-DEMO-MOCK` §2.1（新增步→叶指标图） |
| 图 diff | 加 A/C1–C6 → 19 条叶指标的 Mermaid；S1 `POLICY-STORAGE-FLOW` **未改** |
| 会签态 | `01-data-flow.md` 仍 `approved`；本文件 `status: as-built` |

## 范围与实现

对照政策域指标注册表（32 条）与 `run_all_policy` as-built：在 `pipeline-demo-mock.md` §2.1 列出哪一步写出哪条 `metric_id`。查询走 MCP `metric-registry`，不读 seed/矩阵 YAML。

## 偏离

无。用户举例把「政策产业覆盖度」误写在 `M_POLICY_NATIONAL_DIST` 上，文档按注册表拆开：覆盖度 = `M_POLICY_INDUSTRY_COVERAGE`（C2），全国分布 = `M_POLICY_NATIONAL_DIST`（A）。

## 产物清单

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-demo-mock.md` §2.1
- `CHANGELOG.md`
- 本 handoff

## 验收证据

- `metric-query domain=政策` → 32 条；叶 19 + 身份 9 + 不覆盖 4 = 32
- 叶指标 `metric_id` 与 `polan/basic/indicators.py`、`eval/{focus,intensity,effect,gap,opportunity,layout}.py` 文头一致
- 会签通过：映射与 as-built 对齐，待 `human:淮政玮` 签收

## 问题清单

- 4 条 DS-07 / DS-11 身份叶本管线不算，需另开展示算法叶
- D1–D3 有表无注册叶 KPI

## 修改内容

- `pipeline-demo-mock.md` 增 §2.1 覆盖表 + 步→指标图；frontmatter `task_id` 改为本叶
- `CHANGELOG` 一行

## 测试结果

- 32 = 19 + 9 + 4 算术闭合
- 未改 `polan`、未改 seed/矩阵

## 遗留风险

- C2 覆盖度分母是本批 `ext5` 去重，不是 `dwd.industry_chain`（已在表内标明）

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（本叶未提交，待用户指示）
- commit：—
- pipeline URL / ID：文档叶，无业务 CI
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`
- `agent-delivery/agent-handoffs/DATA-POLICY-STORAGE-DEMO-METRIC-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 未改代码 |
| 调用链 | ✅ 未改 |
| 图谱仅 Nebula 一张 G | ✅ 关联度标明读 ADS 边、不把 B+ 当写出步 |
| 可观测 | N/A |
| CI/CD | N/A |
| demo2 不 merge lumen | ✅ |
| Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ |
| D8 / D10 | N/A |
| D9 指标 8 件套 | ✅ 只映射、不改口径；D1/D4 抄 MCP |
| D12 | ✅ |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 28000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.12 |
| cost_warn | green |
