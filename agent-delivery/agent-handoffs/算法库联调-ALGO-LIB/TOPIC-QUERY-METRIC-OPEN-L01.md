# TOPIC-QUERY-METRIC-OPEN-L01 · 专题查询 METRIC-OPEN（LOOP Round 6）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 6。名词见 `task-claiming-guide.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；USM/TRACE/A2 pages 按原文精读，不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义精读；本叶不压缩会签原文 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶无拓扑、无调用链改边 |
| 会签态 | N/A |
| 说明 | OPEN 语义卡 + 开放项登记，无 Mermaid 契约图 |

---

## 范围与实现

对照给人说明 **§8.4 甲** + LOOP 协议 Round 6：

- 覆盖一页：`TOPIC-QUERY`（04 十二招标叶子）。
- ④ **混页**：**kit** = seq 6–7 推荐图表 5×正式 `M_*_QUERY`（TEMP 对照）；**N/A+依据** = seq 1–5 / 8–12 / 命中条数 / 八维 / E1。禁止口头 N/A。
- 赋号草稿见 §赋号表。**禁止写入 seed**。禁止 `M_QUERY_*` / `M_SEARCH_*` / `M_HEAT_*` / `M_WORDCLOUD_*`。
- **不对 05 八维打 missing/mapped**；禁止 seq 116 顶替；禁止 reuse 05 模型 ID / `M_CHAIN_HOTSPOT_*` / `M_CHAIN_NEWS_*` / `M_SVC_ORG_CNT`。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 17）；本叶指针写入 `open-loop/TOPIC-QUERY-METRIC-OPEN-L01-a2-patch.yaml`。**未改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml` 与 `LOOP-state.yaml`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。本会话不开工其它 OPEN 叶。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 给人说明「查询走 n/a_ops、不进九新清单」≠ 允许对推荐图表统计口头 N/A；本叶按 §8.4「有统计数字则 ④语义卡」出 TEMP_。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q-TOPIC-QUERY-*`、未改客户决策清单。
- 详细设计 §4 `.2.15` / 图谱API 仅作实现接线提示，不构成本页 05 mapped，也不因此 missing。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-QUERY-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01.yaml` |
| 叶级赋号卡 | `metrics/request/_work/id-assign/TOPIC-QUERY-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-QUERY-METRIC-OPEN-L01-questions.yaml` |
| A2 patch（本叶） | `metrics/request/_work/open-loop/TOPIC-QUERY-METRIC-OPEN-L01-a2-patch.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-QUERY-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 1，`page_id=TOPIC-QUERY`，`metric_open_status: present`，`kit_or_na: kit`。
- `demands` = 5×正式 `M_*` + `temp_id` 对照（赋号 5 / 复用 0）。
- 叶级 `id-assign` 条数 = 5 = 原 TEMP_*；每条有 `algorithm_type_suggested`。
- 未改 `metrics/registry/`；未改展示 catalog / pages；未改共享 QUESTIONS / LOOP-state。
- 赋号草稿；类型未签。不对 05 打 missing。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码；检索标明 etl-es，禁止查询并进 algo-py 冒充 05 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java→ES/ADS |
| 图谱 Nebula | ✅ 未引入 Neo4j；本页图谱=结果浏览，不 mapped seq 116 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；检索壳无口头 N/A |

## 遗留风险

- 公式 / `algorithm_type` 未签 → 门 1 仅有条件闭合；D1 不得标 aligned。
- 正式 ID 若被误写入 seed 即违规；差集仍 other_system，禁止对 05 打 missing。
- 分箱 / 绩效核 / 热度分母 / 类型字典 / 时间桶 = Q-MO-QUERY-01…05（🟡）。

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
| actual_tokens | 92000 |
| model_used | grok-4.6 |
| actual_cost | 0.76 |
| cost_warn | green |

## 下一步

状态留 `in_progress` 等 coordinator AV。**不改** LOOP-state；共享 a2-patch 由 coordinator 合流本叶 `TOPIC-QUERY-METRIC-OPEN-L01-a2-patch.yaml`。本会话不开工其它叶。

---

## 赋号（METRIC-ID-ASSIGN-LOOP · 2026-08-22）

> 协议：`METRIC-ID-ASSIGN-LOOP-循环工程.md`。product-agent 代执行；监管 `human:淮政玮`。**赋号草稿；类型未签。** 不标 done。不写 seed / 展示 catalog / 共享 QUESTIONS。

| 项 | 值 |
|----|----|
| 赋号份数 | 5（= 原 TEMP_* 数） |
| 复用份数 | 0 |
| 新号 | `M_TALENT_STRUCT_QUERY` / `M_ORG_PERF_QUERY` / `M_TECH_HEAT_QUERY` / `M_SVC_TYPE_DIST_QUERY` / `M_COMMON_INFO_TREND_QUERY` |
| Q 份数 | 5（Q-MO-QUERY-01…05，一律 🟡） |
| 建议类型分布 | STAT×5 |
| 05 八维 | 未 mapped、未 missing、未 reuse 模型 ID |
| 防撞 | 只读 query；近义 `M_CHAIN_HOTSPOT_*` / `M_CHAIN_NEWS_*` / `M_SVC_ORG_CNT` 口径不同 |

产物：核对记录 **§赋号表**；机器卡 `demands` 已换 `M_*`（保留 `temp_id`）；`id-assign/TOPIC-QUERY-METRIC-OPEN-L01.yaml` + `-questions.yaml`。

