# DS-ALGO-GAP-L01 · 展示系统 vs 算法库差集

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | A2.1 FANIN 之后开工；DW1–DW16 页面包后 FANIN |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 差集/语义对照，禁止砍 METRIC-OPEN 覆盖或发明口径 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机编排会话以页面 yaml 为中间产物，未走 Headroom 压缩 |

## 范围与实现

对照 `bid-reference/srs/02-科技信息展示系统` + 详设 04～10 + METRIC-OPEN/TRACE/WF 第 6 列，与算法库 `srs/05` 97 叶及 B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`。

粒度：态势 DS-01～09 = 需规五级一页（35）；其余 = 四级或 METRIC-OPEN 产品包（40）；FANIN 另加数据需求 1 行。教育核增 / 政策对比核增 / 抗疫核减 skip。

主产物 = `差集判定=missing` **70 条**（items 内 71，去掉专题已列的 `M_POLICY_INDUSTRY_FIT`）。mapped 204 只保留对应，不重写定义。

## 偏离说明

- A1 双表未交：`A1需规ID` / `A1指标叶ID` 空。
- 多数展示 missing 无正式 `M_*`，FANIN 未补造。
- `CHAIN-PORTAL-OVERVIEW` 情感占比曾误标 missing；父会话改为 mapped（B 轨 `M_CHAIN_NEWS_SENTIMENT_RATIO` + POV-B07）。
- 半成品 xlsx 只读，未覆盖。未改 seed。
- DoD 曾写 `metrics/algo-results/`；8/22 schema 真源为 `metrics/request/展示系统/`（与专题叶同目录约定）。

## 产物清单

- `metrics/request/展示系统/pages/*.yaml`（75 页）
- `metrics/request/展示系统/DS-ALGO-GAP-L01.yaml`
- `metrics/request/展示系统/DS-ALGO-GAP-L01.xlsx`（931 行含表头）
- `metrics/request/展示系统/DS-ALGO-GAP-L01-summary.md`
- 本 handoff

未覆盖半成品 xlsx、未改 seed、未 commit。

## 验收证据

- 75 页 yaml 齐；FANIN 930 行；xlsx `max_row=931`。
- missing 主清单 70 条见 summary。
- B 轨 missing 违规 = 0。
- CI/CD：`skip`（编排仓文档 spike，无业务 Pipeline）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未在 Java 写算法 |
| 2 调用链 | ✅ 差集不改调用链 |
| 3 图谱 Nebula | ✅ 未引入 Neo4j |
| 4 可观测 | N/A 无运行时代码 |
| 5 CI/CD | N/A `cicd: skip` |
| 6 demo2 merge | ✅ 未 merge lumen |
| 7 共享聚合 | ✅ 未让前端直连算法 |
| 8 数据 ADS/Mock | ✅ 未改数仓 |
| 9 D8 Design | N/A |
| 10 D9 血缘 | ✅ 未发明正式 `M_*` 进 seed |
| 11 D10 交互 | N/A |
| 12 D12 demo/lumen | ✅ 只改编排仓 |

## 问题清单

- A1 交卷后回填 70 条 missing 的需规/指标叶 ID。
- 父单 `TOPIC-DS-METRIC-GAP-L01` 仍 backlog，索引已写 `metrics/request/TOPIC-DS-METRIC-GAP-L01.md`，待 coordinator / 淮政玮签收两叶后推进。

## 遗留风险

- 语义欠账 247 条不进主清单，上线前需产品会签。
- 态势多条 missing 无正式 metric_id，后续注册须走 METRIC-OPEN，禁止本叶补造。

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未 commit）
- commit：无
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：本地 yaml 合并 + openpyxl 写 xlsx（`max_row=931`）

## 涉及文件

- `agent-delivery/metrics/request/展示系统/`
- `agent-delivery/metrics/request/_work/_fanin_display.py`
- `agent-delivery/metrics/request/_work/A2-GAP-loop-state.yaml`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/A2.2-GAP-loop-编排.md`
