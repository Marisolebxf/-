# DS-06-METRIC-OPEN-L01 · 展示深圳创新监测 METRIC-OPEN（LOOP Round 13）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 13 / 波 B。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 13 + catalog `ds_id=DS-06`：

- 覆盖 4 页：`DS-06-CITY` / `DS-06-CARRIER` / `DS-06-INDICATOR` / `DS-06-DOMAIN`。
- ④：**4 kit、0 整页 N/A**。GIS/筛选/订阅/导出/建议文案均 **N/A+依据**。
- 只列 `TEMP_DS06_*`（9 条）。禁止发明正式 `M_*` 写入 seed。
- 禁止改挂 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*`；禁止混挂 DS-04 CITY/CARRIER 正式 ID、DS-05、DS-08、TOPIC-*、POLICY/DS-10-12。
- CITY 已 mapped 186：**不改挂** `M_SYNTH_*`。CARRIER seq 114 **missing 保持**（also_in 全球载体榜，不改挂）。
- 详设 DS-06 未给 501；CITY 趋势 mapped 186 + SZCITY-B04。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针只写分叶 `DS-06-METRIC-OPEN-L01-a2-patch.yaml`。
- **未改**共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。
- ⑤：无新 Q0xx；不改客户决策清单。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- DoD 原文 `owner_semantic: human:淮政瑎` 为错字，本叶按 `human:淮政玮`。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q0xx`、未改客户决策清单：⑤ = 核对记录 §4 + A2 `semantic_debt`。
- metric-registry MCP 本会话未挂载；未整文件读 seed。形近 ID 以 A2 `b_track_lookalikes` / `srs05_do_not_map` 为准，一律不消费。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-06-深圳创新监测-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/DS-06-METRIC-OPEN-L01.yaml`（demands→`M_*`，保留 temp_id_map） |
| A2 patch（分叶） | `metrics/request/_work/open-loop/DS-06-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-06-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-06-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-06-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 4，全部 `metric_open_status: present`。
- kit：CITY / CARRIER / INDICATOR / DOMAIN；无整页 N/A。
- OPEN 阶段 `demands` 曾为 `TEMP_DS06_*`；赋号后换成 `M_INNOV_*_SZ`，保留 `temp_id_map`。**零**写入 seed。
- CARRIER `keep_library_missing: true`（seq 114）；CITY mapped 186 不改挂 SYNTH。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 LOOP 文件 / QUESTIONS。
- 会签通过（口径草稿；公式 pending 唐绍祖）。赋号草稿；类型未签。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端 `/display` → Java BFF → ADS |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 类型未签 → 门 1 仅有条件闭合。正式 `M_*` 只在 §赋号表 / id-assign，**未入 seed**。
- TEMP_ / 赋号卡若被误写入 seed 即违规；Round 18 仍须 `keep_library_missing`（CARRIER seq 114）。
- CARRIER 价值排名若被改 mapped（挂 141/151/182–191/`M_SVC_ORG_TECH_SCORE`/`M_INNOV_CARRIER_*_GLOBAL`）即伪闭合。
- CITY 分项 vs 186 四维（SZCITY-B03 / Q-MO-DS06-01）、趋势预测未冻（SZCITY-B04）待甲方，不发明分项 ID。
- CITY 已 mapped 186 若被改挂 `M_SYNTH_VIT_*` 即违规。

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
| actual_tokens | 145000 |
| model_used | grok-4.6 |
| actual_cost | 1.10 |
| cost_warn | green |

## 下一步

状态留 `integration`。**本会话不标 done、不改 LOOP-state。** Round 18 才回写 A2 catalog 指针。

---

## 赋号追加（METRIC-ID-ASSIGN-LOOP · 2026-08-22）

| 项 | 值 |
|----|-----|
| 执行 | product-agent；监管 `human:淮政玮` |
| 赋号份数 | **9**（= 机器卡 `TEMP_DS06_*`；无废弃） |
| 复用份数 | **0**（CITY/载体 ≠ `M_SYNTH_*` / DS-04 GLOBAL / DS-05 GBA 口径，禁止改挂） |
| Q 份数 | **3**（`Q-MO-DS06-01`…`03`，叶级 yaml；未写共享 QUESTIONS） |
| 建议类型分布 | MIXED 5 / STAT 2 / MODEL 1 / third_party 1 |
| 186 / missing | CITY 对比/排名/指数/竞争力/趋势 **mapped 186 读面保持**，正式号 `M_INNOV_CITY_*_SZ` 不改挂 SYNTH；CARRIER **missing 保持**，also_in 不改挂全球载体号 |
| 未改 | seed / 展示 catalog / `METRIC-SEMANTIC-QUESTIONS.md` / LOOP-state |
| MCP note | 赋号草稿；类型未签 |

产物：核对记录 §赋号表；机器卡 demands→`M_*`；`id-assign/DS-06-METRIC-OPEN-L01.yaml` + `-questions.yaml`。
