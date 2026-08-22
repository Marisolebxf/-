# DS-05-METRIC-OPEN-L01 · 展示湾区创新监测 METRIC-OPEN（LOOP 态势叶）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领且 `in_progress`；本会话 product-agent 代执行 DS-05 一叶。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议态势叶 + SRS `湾区创新监测.md`：

- 覆盖 catalog `ds_id=DS-05` 全部 4 页：`DS-05-GBA-ANALYSIS` / `DS-05-GBA-INDICATOR` / `DS-05-GBA-ACHIEVE` / `DS-05-GBA-CAPACITY`。
- ④ 四页均为 **kit**（非整页 N/A）；图壳 / 导出 / 阈值告警 / 字面对比 / 详情读面 **N/A + 依据**。
- 只列 `TEMP_DS05_GBA_*`。禁止发明正式 `M_GBA_*` 写入 seed。
- 禁止改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_CONTRIB`；禁止 B 轨形近 ID；禁止按号 mapped 05 seq 95/96/97/104/105。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针写入叶级 `open-loop/DS-05-METRIC-OPEN-L01-a2-patch.yaml`。**未改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml` 与 `LOOP-state.yaml`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。库 missing（SWOT 四象限 + 地理热点）保持。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建湾区 `Q0xx`、未改客户决策清单、未新建 `data-gap-catalog`：⑤ = N/A + 依据（清单无 DS-05 口径项；文案真源 A2 `semantic_debt`）。
- 未改共享 LOOP 状态机文件（用户/coordinator 禁写）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录（含 §赋号表） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-05-湾区创新监测-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-05-METRIC-OPEN-L01.yaml` |
| 叶级赋号卡 | `metrics/request/_work/id-assign/DS-05-METRIC-OPEN-L01.yaml` |
| 叶级 Questions | `metrics/request/_work/id-assign/DS-05-METRIC-OPEN-L01-questions.yaml` |
| A2 patch（叶级） | `metrics/request/_work/open-loop/DS-05-METRIC-OPEN-L01-a2-patch.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-05-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 4；`demands` 18 条均为 `metric_id: M_INNOV_GBA_*` + `temp_id` 对照。
- 叶级 `id-assign` items 数 = 18 = 原 TEMP_*；reuse_of 全 null。
- SWOT/热点 `keep_library_missing`；CAPACITY 不 reuse `M_SYNTH_VIT_*`。
- 未改 `metrics/registry/`；未改 A2 catalog / pages 正文；未改共享 QUESTIONS / LOOP-state。
- **赋号草稿；类型未签。** 不标 done。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java→ADS；CAPACITY 186 为展示读面不跑 Job |
| 图谱 Nebula | ✅ 未引入 Neo4j；本页无独立构图核 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式 / 类型未签；`M_INNOV_GBA_*` **未入 seed** → 门 1 仍有条件闭合。
- 误挂 `M_SYNTH_VIT_*` 或把 SWOT/热点 missing 改 mapped 即违规。
- Q-MO-DS05-01…05 待甲方；不升 🟢。

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

| 字段 | OPEN 核对 | 本轮赋号 | 合计（handoff） |
|------|-----------|----------|----------------|
| actual_tokens | 96000 | 52000 | 148000 |
| model_used | grok-4.6 | grok-4.6 | grok-4.6 |
| actual_cost | 0.80 | 0.45 | 1.25 |
| cost_warn | green | green | green |

## 下一步

状态留 `in_progress` 等 coordinator AV。叶级 a2-patch 待合流进共享 `METRIC-OPEN-LOOP-a2-patch.yaml`。**本会话不标 done、不改 LOOP-state。**

---

## 赋号（本 loop · 2026-08-22）

| 项 | 值 |
|----|-----|
| 赋号份数 | **18**（= 机器卡 `TEMP_DS05_GBA_*`） |
| 复用份数 | **0**（近义 `M_SYNTH_VIT_*` / `M_ENT_*` / `M_CHAIN_*` 口径不同，不改挂） |
| Q 份数 | **5**（Q-MO-DS05-01…05，🟡） |
| 建议类型分布 | STAT **7** / MODEL **11**（一律 `suggested_unsigned`） |
| ELEMENT | `INNOV` → `M_INNOV_GBA_*` |
| 库缺口 | SWOT 四象限 + 热点 **missing 保持**；CAPACITY seq 186 **mapped 读面** |
| 未做 | seed / 展示 catalog / 共享 QUESTIONS / LOOP-state / 标 done |

产物：核对记录 **§赋号表**；机器卡 `demands` 已换 `M_*`（保留 `temp_id`）；`id-assign/DS-05-METRIC-OPEN-L01.yaml` + `-questions.yaml`。

MCP note：**赋号草稿；类型未签**。
