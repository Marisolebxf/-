# ZHIKU-METRIC-OPEN-L01 · 高端智库 METRIC-OPEN 补登记（LOOP Round 7）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 7 **补登记**。名词见 `task-claiming-guide.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；USM/核对记录按原文补栏，不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义补登记；本叶不压缩会签原文 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶无拓扑、无调用链改边 |
| 会签态 | N/A |
| 说明 | OPEN 会签栏补登记，无 Mermaid 契约图 |

---

## 范围与实现

对照 LOOP 协议 Round 7 + 已有 `METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md`：

- **只补会签栏**，**未从零重写** §1 ④ / §4 ⑤。
- 覆盖一页：`E-ZHIKU`（10 子叶共用父 OPEN）。④ **kit**；S6 未建页 **N/A**。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- 演示态 🔴 四枚不得转正：`ZHIKU-S3-TREND-FORECAST` / `ZHIKU-S4-TALENT-INDEX-SCORE` / `ZHIKU-S4-TALENT-COCKPIT-ALERT` / `ZHIKU-S5-EVAL-SCORE`。
- `Q-ZHIKU-01`～`05` 保持待登客户决策清单，不升 🟢；本叶不改跟踪表。
- 不另开 `E-ZHIKU-METRIC-OPEN-L01`。不改 seed。
- **未改** `LOOP-state.yaml` 与共享 `METRIC-OPEN-LOOP-a2-patch.yaml`。指针在本叶独立 `{ID}-a2-patch.yaml`。
- 专题 A2.1 catalog = **n/a**（无智库页）。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 原核对记录起草栏「何老师 / 郭万迎未会签」保留，不回溯删除。
- 共享 a2-patch / LOOP-state 由 coordinator 合流；本叶按并行波次红线不写这两文件。
- 未改 `客户决策清单跟踪表.md`。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录（补栏 + §赋号表） | `agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/ZHIKU-METRIC-OPEN-L01.yaml`（demands 仍为 `ZHIKU-S*`，未改挂 `M_*`） |
| 赋号卡 | `metrics/request/_work/id-assign/ZHIKU-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/ZHIKU-METRIC-OPEN-L01-questions.yaml` |
| A2 本叶 patch | `metrics/request/_work/open-loop/ZHIKU-METRIC-OPEN-L01-a2-patch.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/ZHIKU-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed；A2 catalog 正文；`LOOP-state.yaml`；共享 QUESTIONS；`客户决策清单跟踪表.md` |

## 验收证据

- 核对记录新增 §6 会签栏 + §7 签署区；§1 / §4 原文保留。
- 机器卡 `pages[]` 长度 = 1，`page_id=E-ZHIKU`，`metric_open_status: present`，`kit_or_na: kit`。
- `demands` 均为已有 `ZHIKU-S*`（29 枚），**零**新编 `M_*`。
- 本叶 a2-patch：`E-ZHIKU` present + 专题 catalog `n/a`；`keep_library_missing: true`。
- 会签通过（口径草稿；公式 pending）。
- 从零重写④⑤：**否**。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶） |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含语义卡 / 开放项 / 演示态锁定；不跳过 |

## 遗留风险

- 公式未签 + 算法定义卡未落地（Q-ZHIKU-04）→ 门 1 仅有条件闭合。
- PDR-07 未同步客户决策清单。
- 四枚 🔴 若被误转正即违规。
- 共享 patch 尚未合流；Round 18 前 catalog 正文仍靠 pages yaml 已有 present。

## CI/CD（必填）

- 分支：不提交（用户禁止 commit）
- commit：无
- pipeline URL / ID：`cicd: skip`
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A（定义叶）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## Cost（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | grok-4.6 |
| actual_cost | 0.40 |
| cost_warn | green |

## 下一步

状态留 **`integration`**。**不标 done。** LOOP-state / 共享 QUESTIONS / 客户决策清单由 coordinator 合流。不派唐绍祖。

---

## 赋号（METRIC-ID-ASSIGN-LOOP Wave B · 2026-08-22）

| 项 | 值 |
|----|-----|
| 非红条数 | **25**（保持 `ZHIKU-S*` 正式草稿身份；零 `TEMP_*`；零新编 `M_*`） |
| 红锁 | **4**（`TREND-FORECAST` / `TALENT-INDEX-SCORE` / `TALENT-COCKPIT-ALERT` / `EVAL-SCORE`；不得转正） |
| 复用份数 | **0**（形近链热点/企业潜力/专题人才草稿不同口径，不改挂） |
| Q 条数 | **3**（`Q-MO-ZHIKU-01`…`03`，仅叶级 yaml；`Q-ZHIKU-01`～`05` 待登不升 🟢） |
| 建议类型分布 | STAT 19 / COMPUTE 4 / GRAPH 1 / MODEL 1 |
| 类型状态 | `suggested_unsigned`；公式未签 |
| ELEMENT | `COMMON`（只写在卡上说明，不另造 `M_COMMON_*`） |
| 未改 | seed / 展示 catalog / pages / LOOP-state / 共享 QUESTIONS / DS-30 / DS-13～16 |

MCP note：**赋号草稿；类型未签；四枚红不转正。** 本叶 **不**改 OPEN 为 done。
