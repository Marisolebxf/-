# TOPIC-TALENT-METRIC-OPEN-L01 · 专题人才 METRIC-OPEN（LOOP Round 5）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 5。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 5：

- 覆盖一页：`TOPIC-TALENT-05`（05.5 十一招标叶子进算法差集者 + `.7.2` 流动统计核）。
- ④ **kit**（非整页 N/A）；筛选壳 / 报告面 / 识别前置 / 图谱无独立核 / 展示 DS-13～16 / 智库 / 综合人才维 **N/A + 依据**。
- 只列 `TEMP_TOPIC_TALENT_*`。禁止发明正式 `M_*` 写入 seed。
- **未混入**展示 DS-13～16；禁止消费展示人才 METRIC-OPEN（本批也没建）。
- 关系链 = A 面 G1（可与 DS-15 同源但不消费展示 OPEN）；引入 / 培育 = G3 Job（可与 DS-16 复用但不消费展示 OPEN）；流动 = 关系+时间，禁止轨迹引擎。
- 实现类草稿 = third_party；禁止伪 COUNT / 伪加权。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 17）；指针写本叶 `TOPIC-TALENT-METRIC-OPEN-L01-a2-patch.yaml`。**未改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml` 与 `LOOP-state.yaml`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。未开工其它 OPEN。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q-TOPIC-TALENT-*`、未改客户决策清单：展示 DS-13～16 不改挂；专题债留 TAL-B03…B12。
- 人才功能实现 Owner 给人说明仍 **待指定**；指标清单+九新对接 = `human:郭万迎`。
- 未改其它 OPEN 叶产物。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-TALENT-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-TALENT-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-TALENT-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/TOPIC-TALENT-METRIC-OPEN-L01-questions.yaml` |
| A2 patch（本叶） | `metrics/request/_work/open-loop/TOPIC-TALENT-METRIC-OPEN-L01-a2-patch.yaml`（本轮未改） |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-TALENT-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 1，`page_id=TOPIC-TALENT-05`，`metric_open_status: present`，`kit_or_na: kit`，`mix_ds13_16: false`。
- `demands` 均为 `TEMP_TOPIC_TALENT_*`（12 条），**零** `M_TALENT_*` / 展示人才 ID。
- 本叶 patch `entries` 含 `TOPIC-TALENT-05` + `keep_library_missing: true` + `mix_ds13_16: false`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改 `LOOP-state.yaml`；未改共享 a2-patch。
- 会签通过（口径草稿；公式 pending）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java→ADS / Job / A 面图 |
| 图谱 Nebula | ✅ 未引入 Neo4j；关系链标 A 面当前图；流动禁止轨迹引擎 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 无正式 `M_*` + 第三方不展开 → 门 1 仅有条件闭合。
- TEMP_ 若被误写入 seed 即违规；Round 17 仍禁止 `M_TALENT_*`、仍禁止混入 DS-13～16。
- 展示人才 OPEN 本批未建；同源 `.7.5`/`.7.9` 与展示分叶并存，禁止混挂。

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
| actual_tokens | 98000 |
| model_used | grok-4.6 |
| actual_cost | 0.82 |
| cost_warn | green |

## 下一步

本叶 **不**改 LOOP-state（coordinator 合流）。状态留 `in_progress` 等 coordinator AV。**不标 done。**

---

## 赋号（METRIC-ID-ASSIGN-LOOP · 2026-08-22）

| 项 | 值 |
|----|-----|
| 赋号份数 | **12**（= 原 TEMP_* 12，含流动 `.7.2`；零废弃） |
| 复用份数 | **0**（TALENT 域 seed/矩阵为空；形近 ENT/CHAIN/SYNTH/SVC 不同口径不复用） |
| Q 份数 | **10**（`Q-MO-TALENT-01`…`10`，仅叶级 yaml；未写共享 QUESTIONS） |
| 建议类型分布 | STAT 3 / MODEL 6 / GRAPH 2 / MIXED 1 |
| 类型状态 | `suggested_unsigned`；公式未签 |
| ELEMENT | `TALENT` |
| 未改 | seed / 展示 catalog / 专题 pages / LOOP-state / 共享 QUESTIONS / DS-13～16 |

正式草稿 ID：`M_TALENT_REGIONAL_DIST` / `ORG_DIST` / `SUPPLY_STRUCT` / `RELATION_NET` / `SZ_STATUS` / `ACADEMIC_SCORE` / `INDUSTRY_SCORE` / `ATTRACT_SCORE` / `CULTIVATE_SCORE` / `UNIV_NEW` / `SZ_SUPPLY_DEMAND` / `FLOW_TRACK`。

MCP note：**赋号草稿；类型未签。** 本叶 **不**改 OPEN 为 done。
