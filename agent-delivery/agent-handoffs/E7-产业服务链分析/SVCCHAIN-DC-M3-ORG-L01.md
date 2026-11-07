# SVCCHAIN-DC-M3-ORG-L01 handoff｜产业服务链分析 · 服务机构分析域合规演示用例 + LOOP 计划

> **任务**：`SVCCHAIN-DC-M3-ORG-L01`（总控：`SVCCHAIN-合规演示用例-长任务总控.md` 段 M3a）
> **agent**：doc-agent｜**监管人**：human:徐滕强｜**强度**：ponytail full
> **日期**：2026-11-07
> **依赖**：M1（`SVCCHAIN-需规条目矩阵.md` §2.1）+ M2（`SVC-数据调研-20261107.md`）
> **产物**：
> 1. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md`
> 2. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ORG-LOOP计划.md`

`ponytail:` full——按金样 POL-L2-DS10-QRY 体例最小交付：两份文件零自造脚手架；覆盖表 8 列金样结构；期望值全部来自实查/快照真值，不造数；不建单不跑 LOOP；历史 as-built 文件零改写。

## 1. 范围与实现

- **用例**：ORG 域 6 行（7.1.1–7.3.2）100% 落覆盖表；金样 8 列（需规位置/界面/输入或选择/触发/接口地址/按界面值填好的请求/期望输出/数据情况）；每行期望写具体值（机构名/org_id/depth/stars/分值/rank_no/请求体 JSON）；一条主路径串 6 可演行 + 检索前置步骤串；文头带规程指针/系统/需规序号/日期/调度核对指针 + 历史记录不改写声明。
- **LOOP 计划**：按总控 §4 全要素——建议 ID `SVC-ORG-DEMO-ACCEPT-LOOP`（只写不建）、先决条件、纯后端 token（`~/.gkx/topic-loop-token` + `systemCode: topic`）、一轮四步（探测→只读库+调接口→对照→缺口分类 DATA/QUERY/ALGO/ENV）、缺口分类表 8 条预判、每轮 ≤3 张（`SVC-ORG-DEMO-FIX-R{YYYYMMDD}-*`）、同缺口两轮不进则停、报告 handoff 路径（只追加）、状态行「覆盖已齐，未执行。等人说『按 LOOP 跑』」。
- **接口地址真源**：lumen 调用链 as-built 只读对照——网关 `/topicAsync/**` → `gkxlumen-topic-async-service-biz` `AnalysisTaskController`（`POST /topic/v1/analysis/tasks` / `GET /tasks/{taskId}` / `GET /tasks/{taskId}/result`）→ Feign `/internal/gkx-svc/analysis/tasks/*`（D12 合规，只指 `lumen-algo-py`）；`SvcAnalysisTypes` 白名单 `svc:analysis:org_coverage|org_trend|tech_power`。

## 2. 查库实勘（只读，零写操作）

- 入口连接 `demo-gkxlumenx-ods`（M2 同款绕行连接），跨库限定名查 `demo_gkxlumenx_ads` / `demo_gkxlumenx_dwd` / `gkxlumenx_topic_enterprise`；2026-11-07 17:30–18:10（UTC+8）。
- 关键实值（用例期望的数据底座）：
  - `svc_org_card` 43,343 行；机构集合 5 家真值（东莞双奉 `007050fc…` / 君智容 `004671cd…` / 星诚优威 `007d0adc…` / 优威电气 `2c058eb8…` / 一禾亿株 `539d5a4e…`）；`service_type_candidate='IP' AND city='深圳市'` 64 行（检索前置真值池：深圳航羿 `71fca0ea…`、深圳市中科为 `01aab8a1…`）。
  - `svc_compare_basket_item` 6 行 guest（含 7.3.1 两家：篮 id 60/61）。
  - `svc_tech_power_score` 300 行 = 6 模型×50 机构，CONSULT/HR/INNOV/IP 恒 40.0、FINANCE/MKT 恒 20.0（实测 `MIN=MAX` 六组确认），`weights` 五维各 20、`ext.name` 机构名、批次 `svcmodels_20261107_155402`。
  - `svc_metric_series.M_SVC_ORG_NEW_COUNT` 1978–2026（2022–2026 = 2,779/2,330/1,885/1,251/36）。
  - `svc_chain_gap` 六环节（旁证；中试熟化 0 runtime_flag=blank）。
  - 任务快照（`analysis_task.target_params.result_payload`）：coverage `SVC-20261107-019`（2 家矩阵 depth 91/66）、`SVC-20261102-019`（4 家 12 格 fill 0.75、depth 82/92/100）；trend `SVC-20261106-008`（series 9×17 点 2010=1501 起 + heat INB1309 1 星低迷三行依据原文 + INB2505 5 星高热 + INB1204 insufficient 不评级 + yellow_gaps=GAP-SVC-TREND-FIELD/Q060）；tech_power `SVC-20261107-020`（`cap_w="25,25,20,20,10"`、tech_power.rows score 恒 40、yellow_gaps=Q060）。
- 前端枚举只读对照：`CLUSTER_SEED` 15 集群、`TrendView.tsx` 时间窗 3/5/8、`serviceCenterStore.defaultEvalConfig` 默认权重 25/25/20/20/10、`CAPABILITY_DIM_DEFS` 五维、`CUSTOM_DIM_CANDIDATES` 3 候选、检索页三模式。
- 受阻：无（零 SELECT 失败）。

## 3. 6 行判定汇总

| 需规 | 判定 | 依据摘要 |
|---|---|---|
| 7.1.1 覆盖分析 | **可演** | 任务链 57 条 success 同型 + 机构池真值；⚠️ Q-SVCCHAIN-02（深度 draft）+ Q-SVCCHAIN-09（产业回落默认） |
| 7.1.2 结果呈现（热力/矩阵） | **可演** | 同快照 `matrix` 双图同源；as-built 历史诚实空票已被 11 月灌数消除（原文件不改写） |
| 7.2.1 趋势可视化 | **可演** | 28 条 success + 快照 series/heat 双证 + ADS 序列同值；⚠️ 2026 末端骤降如实写 |
| 7.2.2 市场热度判断 | **可演（演示规则判定 🧪）** | 快照 heat 实值（1 星低迷 + 依据行原文 + insufficient 反例）；⚠️ Q-SVCCHAIN-02 + GAP-SVC-ORG-HEAT |
| 7.3.1 五维评价模型 | **可演（演示态声明）** | 27 条 success + 评分表 300 行实值；恒分 40/20 区分度弱如实写；⚠️ Q-SVCCHAIN-01 + Q060 |
| 7.3.2 自定义对比分析 | **可演（演示态声明）** | 同快照；同分并列/雷达多边形重合=数据实情；⚠️ Q-SVCCHAIN-01 |

**合计：可演 6 / 覆盖不到 0 / 设计无资源 0。** 三条口径行（深度/热度/技术力）按「演示规则判定 / 演示态声明」写，不当正式业务结论。

## 4. 偏离说明

1. **无覆盖不到行**：M2 预判的趋势诚实空（`ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`）与能力域无分（`ENV-SVCCAP-NO-SCORE-RESULT`）经 11-05/06/07 灌批 + 任务快照实勘已消除或降级为「演示态声明」，6 行全部可演；as-built 历史文件按铁律零改写，仅在用例文头作不改写声明。
2. **接口地址按 lumen as-built 写**（`/topicAsync/topic/v1/analysis/*` + svc 白名单），M1 矩阵条件枚举锚点（前端 demo store 本地任务门控）不改写、只作路由参数形态参照——两仓任务键一致（`svc:analysis:*` / `service_org_*` 别名并存于 `SvcAnalysisTypes` 注释），期望按 lumen 白名单写。
3. **技术力默认权重两轨**：前端默认 25/25/20/20/10（`defaultEvalConfig`），库侧模型 `weights` 等权各 20（Q060 临时基线）——用例按前端默认填请求、库侧差值如实注明，LOOP §5 预判 DATA 类登记，不判谁对。
4. **检索历史/收藏不做行**：svc 域两表全实例不存在（M2 §0-3），检索前置只串「查机构+入篮」步骤，不断言历史/收藏（与 POL 金样 201 行性质不同，不硬凑）。

## 5. 验收证据

- 两份产物已写入目标路径（目录内已有 PT 域姊妹产物，体例对齐）。
- 期望值可复核性：每行的机构名/org_id/depth/stars/分值都能用本文「查库」节列出的连接与表名以只读 SELECT 复现；任务快照以 `analysis_task.task_id` 直查。
- LOOP 计划含总控 §4 全要素核对：建议 ID ✅ / 先决条件 ✅ / token+systemCode ✅ / 一轮四步 ✅ / 缺口四分类 ✅ / 每轮≤3 ✅ / 两轮停 ✅ / 报告路径只追加 ✅ / 状态行 ✅。
- 本任务**只产文档**：未建任何 registry 单、未跑 LOOP、未派修数单、未 commit/push（coordinator 统一提交）。

## 6. 6 行覆盖核对（总控门）

- 需规 7.1.1–7.3.2 共 6 行，覆盖表 6 行，零缺行 ✅
- 可演行的请求参数值 = 界面输入真源值（前端枚举/对比篮实值）且引用实查数据 ✅
- `覆盖不到` 0 行，无需引用缺口编号的落行；演示态行引用 Q-SVCCHAIN-01/02/09、Q060、GAP-SVC-ORG-HEAT、GAP-SVC-TREND-FIELD，全部既有编号 ✅
- 主路径只串可演行 ✅

## 7. 架构合规自检

| 铁律 | 自检 |
|---|---|
| D12 不触业务仓 | ✅ demo-ui-topic / lumen-svc-platform 只读对照，零改动 |
| 只读库 | ✅ database-mcp 仅 SELECT/information_schema，零写；失败 0 次 |
| 调用链（铁律 2） | ✅ 接口地址按 前端→Java `/topicAsync/topic/v1/analysis/*`→Python `/internal/gkx-svc/*` 写，无越层 |
| D9 指标口径 | ✅ 只引用注册指标 M_SVC_ORG_COVERAGE_* / M_SVC_ORG_NEW_COUNT / M_SVC_ORG_TECH_SCORE / M_SVC_ORG_MARKET_HEAT（D1 missing 如实），未新造 |
| 不造数 | ✅ 期望全部实查/快照真值；口径未定行按演示态声明，无编造业务结论 |
| 缺口编号 | ✅ 只引用既有 Q-*/GAP-*，未新造 |
| 不建单/不跑 LOOP/不派单 | ✅ 验收单建议 ID 只写进计划 |
| 历史文件不改写 | ✅ as-built 四工作区 cases/coverage.md 零改动 |

## 8. cost

- `actual_tokens`: ~180k（估算）
- `model_used`: glm-5.3-Flash
- `actual_cost`: ~$0.6
- `cost_warn`: false（<$10 阈值）
