# TOPIC-ALGO-GAP-L01 · 专题系统 vs 算法库差集

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 页面包波次 W1–W5 后 FANIN；未开工 DS-ALGO-GAP-L01 直至本叶四件套落盘 |

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

对照 `bid-reference/srs/04-科技专题服务系统` 产品定义叶子 + METRIC-OPEN/TRACE/WF 第 6 列，与算法库 `srs/05` 97 叶及 B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`。粒度 = 四件套/05.x 页，不是 129 叶平铺。

主产物 = `差集判定=missing` **7 条**。mapped 171 只保留对应，不重写定义。

## 偏离说明

- A1 双表未交：`A1需规ID` 空，用 SRS 05 打底。
- 诊断「环节健康度」、深圳「全球成功案例匹配」语义层无正式 `M_*`，仍按页包判定 missing（功能要了、库无专叶），未新造 ID。
- 查询/运营/数据需求不扫 05 八维冒充覆盖。

## 产物清单

- `metrics/request/专题系统/pages/*.yaml`（20 页）
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml`
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.xlsx`
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L01-summary.md`
- 本 handoff

未覆盖半成品 xlsx、未改 seed、未 commit。

## 验收证据

- 20 页 yaml 齐；FANIN 250 行；xlsx `officecli validate` 通过。
- missing 7 条见 summary。
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

- A1 交卷后回填 7 条 missing 的需规/指标叶 ID。
- A2.2 展示叶按五级编排已落盘，待本叶签收后 claim `DS-ALGO-GAP-L01`。

## 遗留风险

- 部分 missing 无正式 metric_id，FANIN 未补造。
- 语义欠账 111 条不进主清单，上线前需产品会签。

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未 commit）
- commit：无
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：本地 yaml 合并 + `officecli validate` 通过

## 涉及文件

- `agent-delivery/metrics/request/专题系统/`
- `agent-delivery/metrics/request/_work/A2-GAP-loop-state.yaml`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/A2-GAP-loop-编排.md`
