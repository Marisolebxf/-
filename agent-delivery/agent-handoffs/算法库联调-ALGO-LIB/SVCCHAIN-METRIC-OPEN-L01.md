# SVCCHAIN-METRIC-OPEN-L01 · 产业服务链 METRIC-OPEN（LOOP Round 1）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 1。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 1：

- 覆盖四页：`SVCCHAIN-ORG-ANALYSIS` / `ECOSYSTEM` / `RECOMMEND` / `PORTAL`。
- ④ 四页均适用（kit）；页内检索/对比篮/门户导航等 **N/A + 依据**。
- 只消费已有 `M_SVC_*`（B 轨 29 枚全集 mapped）。禁止发明正式 `M_*` 写入 seed。
- 禁止消费展示 DS-30；禁止挂 `ENT-MOD-*` OPEN；禁止把 29 个 `M_SVC_*` 打 missing。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 17）；指针写入 `METRIC-OPEN-LOOP-a2-patch.yaml`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 未改 TRACE 原文 `owner_semantic: pending_assignment(何老师)`；会签栏以本核对记录为准。
- 未新建 `SVC-data-gap-catalog.yaml`：⑤ 已登记 Q-SVCCHAIN-01…06。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/E7-产业服务链分析/METRIC-OPEN-SVCCHAIN-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/SVCCHAIN-METRIC-OPEN-L01.yaml` |
| A2 patch | `metrics/request/_work/METRIC-OPEN-LOOP-a2-patch.yaml`（四页 present） |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/SVCCHAIN-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 4，均 `metric_open_status: present`。
- patch `entries` 含上述四 `page_id`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文。
- 会签通过（口径草稿；公式 pending）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶） |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 → 门 1 仅有条件闭合。
- Q-SVC-010 准入债覆盖全部 SVC 数字。
- Round 17 才把 patch 写回 catalog。

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
| actual_tokens | 95000 |
| model_used | grok-4.6 |
| actual_cost | 0.80 |
| cost_warn | green |

## 下一步

LOOP-state Round 1 → `done`；`current` → `TOPIC-ENT-METRIC-OPEN-L01`。**本会话不开工 Round 2。** 状态留 `in_progress` 等 coordinator AV。
