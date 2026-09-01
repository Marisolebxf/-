# DATA-SUPPLIER-Q-METHOD-L01 · 三方问题清单 — 指标驱动方法 / 日志模板 / sidecar schema

> 定义·文档叶。把「指标定义/计算 → 三方问题」收成可续写方法。未改 seed、未改 D3 枚举、未跑全量指标、未写业务仓代码、未改政策现稿结构、未改进度导出脚本。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 父会话已认领并开工；本叶不重复认领、不把状态改成 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | N/A（定义·文档类） |
| 说明 | 定义类任务不压文档完整性。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓文档，未走 Headroom。 |

## 范围与实现

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md` §0–§6 与 `/goal`：

1. 方法页落到 `question/README.md`：算法类型问法、现行待回复、按日日志、注册表域目录（综合=`SYNTH`）。
2. 锁定 sidecar schema：`question/source-gap-index.yaml` 字段注释完整；`metrics: {}`。
3. 可复制模板 `_TEMPLATE-SUPPLIER-QUESTIONS.md`（文件名不加日期）。
4. 各域 README 一两行指向方法与模板；不虚构问题清单。
5. 已拍板不复议：STAT+COMPUTE+MODEL+third_party+GRAPH+UNKNOWN；MIXED 后拆；sidecar 优先于 `d3_gap`；按入站 `dwd_*` 表.列一列一题。

## DoD 对照

| 项 | 结果 |
|----|------|
| `question/README.md` 写清方法：算法类型问法、现行待回复+按日日志模板、注册表域目录（综合=SYNTH） | ✅ §2 目录、§3 问法、§4–§5 模板、§7 续写步骤 |
| `source-gap-index.yaml` schema 锁定，metrics 可为 `{}` | ✅ `version` / `updated` / `metrics.{id}`：`as_of` `algorithm_type` `q_id` `summary` `domain` 均有注释；`metrics: {}` |
| STAT/COMPUTE、GRAPH、MODEL、third_party、UNKNOWN 问法写清；MIXED 本波跳过 | ✅ README §3 |
| 可复制模板（无日期文件名）：现行待回复表头 + `## YYYY-MM-DD` | ✅ `_TEMPLATE-SUPPLIER-QUESTIONS.md` |
| 各域 README 指向模板与方法；不虚构清单 | ✅ 11 域 stub；政策仍指向现稿，结构留给 POLICY-L01 |
| 不改 seed、不改 D3 枚举、不跑全量指标分析 | ✅ |
| handoff 含 cost 四字段 | ✅ 见下 |

## 偏离说明

无。未把政策现稿改成按日（那是 POLICY-L01）。未改 `export_feishu_metric_board.py`（PROGRESS-L01）。

## 产物清单

- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- `agent-delivery/data/third-party-source/question/_TEMPLATE-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/{产业链,企业,政策,服务机构,综合,创新,机构,人才,技术,通用,科技动态}维度/README.md`
- 本 handoff

## 验收证据

- README 含类型问法表、现行待回复表头、按日日志骨架、11 域目录（`SYNTH`）、禁问与跳过规则、sidecar 优先说明。
- sidecar 可被 YAML 解析；`metrics` 为空对象；字段注释覆盖派单包 §4。
- 模板无日期文件名；含滚动表头与 `## YYYY-MM-DD`。
- 未触碰 `POLICY-SUPPLIER-QUESTIONS.md`、`export_feishu_metric_board.py`、`metrics/registry` seed/矩阵。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层；未让前端直连算法 |
| 3 图谱 NebulaGraph | ✅ 未引入 Neo4j；GRAPH 问法只问入站码 |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip / 未 push（文档仓） |
| 6 demo2 merge | ✅ 未 merge 进 lumen |
| 7 共享聚合 | ✅ 未改 Java、未直连 nGQL |
| 8 数据策略 | ✅ 只消费入站 `dwd_*` 问法；未伪 full |
| 9 D8 | N/A |
| 10 D9 | ✅ sidecar ≠ 8 件套；D3 ≠ 8 件套；未改 D3 枚举 |
| 11 D10 | N/A |
| 12 D12 | ✅ 未调 demo 服务、未写业务仓 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~90000（估：必读 + 方法正文；非整会话精确计数） |
| model_used | Cursor Grok 4.6 |
| actual_cost | ~0.4 USD（文档叶档粗算；Grok 4.6 未列入 `budget-estimate.md` pricing 表） |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓；本叶按指令 **未 commit / 未 push**）
- commit：无
- pipeline URL / ID：skip（设计/文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- `agent-delivery/data/third-party-source/question/_TEMPLATE-SUPPLIER-QUESTIONS.md`
- 11 个域 `question/*/README.md`
- 本文件

## 遗留风险 / 开放项

- sidecar `metrics` 仍为 `{}`：进度表「源缺口」在 PROGRESS-L01 接线前仍只会回落 `d3_gap`。
- 政策现稿仍是 P0/P1/P2 长文，不是按日结构 → POLICY-L01。
- 各域尚无真实题目 → 后续 `DATA-SUPPLIER-Q-{DOMAIN}-L01`。
- 父会话收口：本叶不 `task-update-status` 到 integration/done。
