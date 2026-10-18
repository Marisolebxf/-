# SCI-INT-B01 handoff：指标分层集成架构 + 通用集成模式（人才 / 技术链 / 科研机构）

- 任务：SCI-INT-B01 · 角色：agent:architect-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：北京久新（51 行交付清单全部「待确认」）
- ponytail: N/A（分析叶）
- 日期：2026-10-18

## 1. 范围与实现

范围是科技信息展示系统三要素的 93 个指标（P00-baseline：人才 32 / 技术链 39 / 科研机构 22），对应 bid-reference/srs/02-科技信息展示系统中的科技发展态势与科技人才态势两章。

产物 `产物/SCI-INT-B01.yaml` 包含以下内容：

1. **layers L0–L4**：分为前端 ⓘ/角标、`/metrics/v1/catalog`、Java 业务门面、Python `/internal`、对端/ADS/Nebula 五层。每层写明责任、现状（仓、模块、有无）和缺口，现状均由本叶只读核查得出。
2. **patterns IP-01…IP-13**：

   | IP | 一句话 |
   |---|---|
   | IP-01 | STAT 自建：GDF 建 ADS，Java 只读 |
   | IP-02 | COMPUTE：在 ADS 上做确定性公式派生，Python 批 Job 写 ADS（93 个指标中暂无此类型，作为预留） |
   | IP-03 | MODEL 同步推理：同时满足 P95≤2s、单对象、无写库、可缓存才走同步 |
   | IP-04 | MODEL/GRAPH 异步 Job：提交后由 worker 计算，结果写快照，前端轮询；单飞、当天复用、可重新分析 |
   | IP-05 | GRAPH 自建：Python 读写 NebulaGraph TRSGraph，结果投影到 ADS；Java 不写 nGQL |
   | IP-06 | 久新交 SQL：经我方评审后纳入 GDF，落 ADS，读链同 IP-01 |
   | IP-07 | 久新交 Python：并入 lumen-algo-py，按 IP-04/05 运行；禁止回落 demo-* |
   | IP-08 | 久新交 API：在 Python 适配层封装鉴权、限流、超时、缓存、熔断、字段映射；Java 只调 Python |
   | IP-09 | 页面派生：读父库叶快照的子字段，不单独向久新再要 |
   | IP-10 | 无来源或无主：显示空态加 ⚠️，禁止伪造数值 |
   | IP-11 | 结果快照与版本（横切） |
   | IP-12 | metric_id 与 8 件套挂接（横切） |
   | IP-13 | Mock 切换开关（横切） |

   每个 IP 都含 id、name、applies_to、responsibility_by_layer、freshness、failure_degrade、observability、test_points、open_items 九个字段。IP-03 另写明了同步与异步的判据。
3. **initial_mapping**：93 行，每行含 metric_id、algorithm_type（MCP）、b_leaf、pattern、jiuxin_row_id、备注。
4. **汇总**：conflicts C1–C9、decision_needed DN-01–DN-09、risks R1–R9。

## 2. 偏离说明

- **card_count**：本叶不出 INT-B-* 卡片，`card_count=93` 指 initial_mapping 的 93 行，与 scope_count 对齐。卡片由 B02–B09 出。
- **IP-02**：93 个指标中没有 COMPUTE 类型，按 DoD 要求仍定义该模式，作为预留。
- **展示 13 行**：13 个展示 third_party 行（DS-03/07/08/09-*）不单独映射 metric_id。按 JIUXIN 约定，它们挂在库叶 SRS-134/135/137/162 上，记在备注和 C7 中。
- **起点与核查**：架构级初稿 §2 是起点，本叶已逐项复核，修正和新增了以下内容：
  - catalog 缺 algorithm_type 和 D1–D4，且 seed 只有 ENT；
  - `/situation/v1` 没有 Java 实现；
  - GraphController 直读 DWM 层；
  - svcan 存在同名路由；
  - 人才页仍是 DevelopingView。

## 3. 产物清单

| 路径（相对 `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/`） | 说明 |
|---|---|
| `产物/SCI-INT-B01.yaml` | 分层、IP、93 行映射、冲突、待决、风险 |
| `产物/_work/B01-check.py` | 对照 P00 的自检脚本 |
| `SCI-INT-B01.md` | 本 handoff |

没有改动任何业务仓、seed 或矩阵，也没有执行 git commit（由 coordinator 统一提交）。

## 4. 验收证据

运行命令：`python 产物/_work/B01-check.py`（exit 0）

```text
scope_count=93 baseline=93 mapped=93
差集 baseline-mapped=[] mapped-baseline=[]
非法IP=[] 类型不一致=[] 叶不一致=[] 非法久新行=[]
patterns: ['IP-01', 'IP-02', 'IP-03', 'IP-04', 'IP-05', 'IP-06', 'IP-07', 'IP-08', 'IP-09', 'IP-10', 'IP-11', 'IP-12', 'IP-13']
按 IP: {'IP-01': 6, 'IP-04': 3, 'IP-05': 4, 'IP-06': 3, 'IP-07': 6, 'IP-08': 29, 'IP-09': 35, 'IP-10': 7}
按类型: {'third_party': 84, 'STAT': 6, 'MODEL': 3}
挂久新行=73 无久新行=20
未被映射引用的久新行: ['DS-03-RESULT-001', 'DS-03-RESULT-002', 'DS-03-RESULT-004', 'DS-03-RESULT-005', 'DS-03-RESULT-006', 'DS-07-INDUSTRY-POTENTIAL-002', 'DS-07-SCI-CREATE-003', 'DS-07-TECH-INNOV-003', 'DS-08-VIZ-001', 'DS-08-VIZ-004', 'DS-09-COMPREHENSIVE-001', 'DS-09-COMPREHENSIVE-002', 'DS-09-COMPREHENSIVE-004']
OK
```

- 范围数 93，已映射 93，两个方向的差集都为 0。
- 久新 37 个库叶行和 1 个无专叶行全部被引用。
- 未被引用的 13 行正好是「与库叶同交」的展示 third_party 行，符合预期。
- algorithm_type 以 MCP `metric-get` / `metric-query` 为准（2026-10-18），与 P00 的 93 行逐条一致。93 个指标 D1 全为 draft、D4 全为 mock。

## 5. 架构合规自检（公约 §2）

| # | 铁律 | 结论 |
|---|---|---|
| 1 | 算法只在 Python | ✅ MODEL/GRAPH/第三方适配都在 lumen-algo-py，Java 只读或只调用 |
| 2 | 调用链 前端→Java→Python /internal | ✅ 写入 call_chain_rule。存量的非 /internal 路由记为风险 R7 |
| 3 | 图谱只用 NebulaGraph TRSGraph | ✅ IP-05/07，禁止 Neo4j，禁止使用 demo space |
| 4 | 可观测（Java Agent / Python instrument / 前端 observability.ts） | ✅ 每个 IP 都有 observability 字段 |
| 5 | CI/CD | N/A（分析叶，cicd skip） |
| 6 | demo 只读、不 merge | ✅ 只读 demo 作参照 |
| 7 | 共享聚合核心方案 A；Java 只读 ADS、不直连 nGQL | ✅ 方案。存量 GraphController 直读 DWM 记为风险 R4 / 冲突 C6 |
| 8 | ADS 先行，Mock 填充 | ✅ IP-01/06/11/13 |
| 9 | D8 前端规范 | ✅ 不涉及视觉；角标与 ⓘ 按 AGENTS.md |
| 10 | D9 8 件套 + D1–D4 | ✅ IP-12；catalog 缺字段记为风险 R3 / 冲突 C5，未伪称已有 |
| 11 | D10 交互规范 | ✅ IP-04 遵循附录 E（不自动起任务、单飞、当天复用、可重新分析） |
| 12 | D12 lumen 不调用 demo-* | ✅ 方案层面合规。M_TECH_DS_07_* 的 algo_server_location 指向 demo-algo-science，记为高风险 R1，要求在 lumen 重写 |

另外三项约束：

- 前端不直连久新：✅ 久新凭据只放在 Python Secret 中（IP-08）。
- 久新 51 行没有任何一行写成「已确认」：✅
- 业务口径没有替甲方拍板：✅ 全部进入 DN 项。

## 6. 开放项与升级

- **structure_escalation: true**，升级给 human:李伟。新结构有两项：IP-11 的结果快照表（候选 `ads_sci_result_snapshot`）和 IP-08 的适配层缓存表；另需确定三要素 Java 门面所在模块（DN-07）。
- **前三项风险或开放项**：
  1. 久新 42 行 API 的接口文档、鉴权和 SLA 全部「待确认」（DN-01 / R2）。
  2. catalog 不含三要素数据，也缺 algorithm_type 和 D1–D4，导致 93 个指标的 ⓘ 全空（R3）。
  3. M_TECH_DS_07 模型指向 demo-algo-science（D12，R1），而且模型 Owner 未定（DN-05）。
- **下游约束**：B02–B09 卡片的 `integration_pattern` 必须引用 IP-01…IP-13。C1（DS-02 图指标）、C3（专题/展示写者）、C9（svcan 同名路由）须在 B06/B07/B09 卡片中落实。

## 7. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈ 520000（估算，in≈470k / out≈50k） |
| model_used | claude-opus |
| actual_cost | ≈ $6.5（估算） |
| cost_warn | yellow（>$5，未达 $10 暂停线） |
