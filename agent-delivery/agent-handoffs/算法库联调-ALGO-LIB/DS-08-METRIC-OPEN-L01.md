# DS-08-METRIC-OPEN-L01 · 展示科技指数 METRIC-OPEN（LOOP Round 15 / 波 B）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 15 OPEN + Wave B 赋号。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 15 + catalog `ds_id=DS-08`：

- 覆盖 3 页：`DS-08-RANK` / `DS-08-VIZ` / `DS-08-INDICATOR`。
- ④：**2 kit + 1 整页 N/A**（INDICATOR）。本页 A=0；不标 501；差集 other_system / third_party **不改 mapped**。
- 只列 `TEMP_DS08_*`。禁止发明正式 `M_*` / `M_TINDEX_*` 写入 seed。
- **禁止改挂** `M_SYNTH_*` 为本页正式 ID（三兄弟已有 OPEN；可同源说明）。禁止混挂 DS-04/05/06 排名页、专题 QUERY。
- **Q-TINDEX-01 保持待登**，不升 🟢，不新建 `Q0xx`。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针只写分叶 `DS-08-METRIC-OPEN-L01-a2-patch.yaml`。
- **未改**共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q0xx`、未改客户决策清单：⑤ = 核对记录 §4 已有待登项 + A2 `semantic_debt`。赋号歧义仅叶级 `Q-MO-DS08-01…03`。
- 本会话 Cursor MCP 未挂载 `metric-registry`；用编排仓 `scripts/lib/metric-registry-lib.mjs` 等价只读查询（未整文件读 seed YAML 当答案）。TINDEX 域 0 条；SYNTH 形近 ID 一律不消费、不改挂。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-08-科技指数-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-08-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-08-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-08-METRIC-OPEN-L01-questions.yaml` |
| A2 patch（分叶） | `metrics/request/_work/open-loop/DS-08-METRIC-OPEN-L01-a2-patch.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-08-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 3，全部 `metric_open_status: present`。
- kit：RANK / VIZ；N/A：INDICATOR。
- Wave B：`demands` 5 条已换 `M_INNOV_*`（保留 `temp_id`）；INDICATOR `demands: []`。
- `pending_501: false`；Q-TINDEX-01 / 03 保持待登；**零改挂 SYNTH / CHAIN 学术力**。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 LOOP / QUESTIONS / 客户决策清单。
- 会签通过（口径草稿；公式 pending；赋号草稿；类型未签）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端态势 → Java BFF → ADS / 智库封装 |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 赋号草稿未入 seed → 门 1 仅有条件闭合。
- 赋号草稿若被误写入 seed 即违规；Round 18 仍须 `keep_library_missing`（本页 A=0，other_system/third_party 不改 mapped）。
- 若把 Q-TINDEX-01 升 🟢 或改挂 `M_SYNTH_*` / `M_CHAIN_ACADEMIC_POWER` 即违规。
- xlsx 行 92 三页 yaml 曾互指；本叶收口到 VIZ `M_INNOV_SCIINDEX_VALUE`（对照 `TEMP_DS08_TINDEX_VALUE`），Round 18 回写时勿再拆回 INDICATOR 当目录成员。

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
| actual_tokens | 145000 | 72000 | 217000 |
| model_used | grok-4.6 | grok-4.6 | grok-4.6 |
| actual_cost | 1.10 | 0.55 | 1.65 |
| cost_warn | green | green | green |

## 下一步

状态留 `integration`。**本会话不标 done、不改 LOOP-state。** Round 18 才回写 A2 catalog 指针。公式 / 类型仍 `pending_cosign: human:唐绍祖`。

---

## 赋号（本 loop · Wave B · 2026-08-22）

| 项 | 值 |
|----|-----|
| 赋号份数 | **5**（= 机器卡 `demands`：RANK 1 + VIZ 4；注释 `TEMP_RANK_SCORE` / `TEMP_TINDEX_VALUE` 不是额外号） |
| 复用份数 | **0**（近义 `M_SYNTH_VIT_*` / `M_CHAIN_ACADEMIC_POWER` / `M_INNOV_SCHOLAR_INFLUENCE` / `M_TALENT_ACADEMIC_SCORE` 口径不同，不改挂） |
| Q 份数 | **3**（Q-MO-DS08-01…03，🟡）；Q-TINDEX-01 / 03 **保持待登**，不升绿 |
| 建议类型分布 | STAT **3** / third_party **2**（一律 `suggested_unsigned`） |
| ELEMENT | `INNOV` → `M_INNOV_SCIINDEX_*`（指数三兄弟）+ `M_INNOV_EXPERT_*`（H/活跃度） |
| INDICATOR | **整页 N/A，0 号** |
| 501 | `pending_501: false`；预测在 DS-09 |
| 库缺口 | 本页 A=0；other_system / third_party **不改 mapped** |
| 未做 | seed / 展示 catalog / 共享 QUESTIONS / LOOP-state / 客户决策清单 / 标 done |

产物：核对记录 **§赋号表**；机器卡 `demands` 已换 `M_*`（保留 `temp_id`）；`id-assign/DS-08-METRIC-OPEN-L01.yaml` + `-questions.yaml`。

MCP note：**赋号草稿；类型未签**。
