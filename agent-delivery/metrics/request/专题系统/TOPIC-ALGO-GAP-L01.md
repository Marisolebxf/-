# TOPIC-ALGO-GAP-L01 · 专题系统 vs 算法库差集

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。  
> **Round 17**（METRIC-OPEN-LOOP）：只改指针 + 分类文案。旧版不签；库 missing 未改。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | Round 17 指针返工。不标 `done` / `ready_to_sign`。未开工 `DS-ALGO-GAP-L01`。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义类；指针/分类文案，不以缩代码为目标 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机编排会话以 catalog / pages yaml 为中间产物，未走 Headroom 压缩 |

## 相对旧版 diff：指针 / 计数

### 指针（catalog `metric_open_status` missing → present）

| page_id | 旧 | 新 |
|---------|----|----|
| SVCCHAIN-ORG-ANALYSIS / ECOSYSTEM / RECOMMEND / PORTAL | missing / null | present · `METRIC-OPEN-SVCCHAIN-核对记录.md` · `SVCCHAIN-METRIC-OPEN-L01` |
| TOPIC-ENT-05 | missing | present · `METRIC-OPEN-TOPIC-ENT-核对记录.md` · 仅 `TEMP_TOPIC_ENT_*`（禁 `M_ENT_*` / `ENT-MOD-*`） |
| TOPIC-TECH-05 | missing | present · `METRIC-OPEN-TOPIC-TECH-核对记录.md` |
| TOPIC-ORG-05 | missing | present · `METRIC-OPEN-TOPIC-ORG-核对记录.md` |
| TOPIC-TALENT-05 | missing | present · `METRIC-OPEN-TOPIC-TALENT-核对记录.md`（不混 DS-13～16） |
| TOPIC-QUERY | missing | present · `METRIC-OPEN-TOPIC-QUERY-核对记录.md` |
| E7-POLICY | missing +「勿误用」 | present · `METRIC-OPEN-E7-DS10-12-核对记录.md` · `POLICY-METRIC-OPEN-L01`；**已删**「勿误用」 |
| SYNTH-REGION | missing | present（**父索引** `metric_open_role: parent_index`）；三兄弟 OPEN 路径不变；不另建叶 |

CHAIN-TOPIC-* 原已有 CHAIN OPEN，本轮补 `present`，禁止 missing。SYNTH 三兄弟补 `present`。TOPIC-OPS / TOPIC-DATAREQ 保持 n/a_ops / other_system。ZHIKU 专题 catalog n/a，未新增 `TOPIC-ZHIKU`。

### 计数

| 口径 | 旧版 | Round 17 |
|------|------|----------|
| 缺 OPEN 叶 | 11 页 catalog missing | **0** |
| 库 missing（列 11） | **7** | **7（未改 mapped）** |
| mapped / third_party / other_system / n/a_ops | 171 / 10 / 39 / 23 | 同左 |
| 语义欠账条数 | 111 | 111（文案从「缺 OPEN 叶」改为「已挂指针」） |

## 范围与实现

对照 SRS 04 产品定义叶子 + METRIC-OPEN，与算法库 SRS 05 及 B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`。主产物仍是列 11 `missing` **7 条**。本轮不签公式、不升 Q 决策 🟢、不改 `metrics/registry/` seed、不发明正式 `M_*`、不改展示 catalog、不改 LOOP-state。

## 偏离说明

- A1 双表未交：`A1需规ID` 空。
- 库 7 条 missing 保持（含 E7-POLICY 产业适配、SYNTH CONTRIB / OUTPUT_CORR）。
- xlsx 汇总表已加 Round 17 两行计数；清单 250 行未改列 11。yaml 为机器真源。

## 产物清单

- `metrics/request/专题系统/A2-GAP-page-catalog.yaml`
- `metrics/request/专题系统/pages/*.yaml`（语义层指针）
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml` / `-summary.md` / `.xlsx` / 本文件
- `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ALGO-GAP-L01.md`

未覆盖根目录半成品 xlsx、未改 seed、未 commit。

## 验收证据

- 缺 OPEN 叶 11→0；库 missing 仍 7。
- E7-POLICY catalog 已无「勿误用」。
- SYNTH-REGION 父索引 present，三兄弟 path 未改挂。
- 展示 catalog 未动。
- CI/CD：`skip`。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未在 Java 写算法 |
| 2 调用链 | ✅ 差集不改调用链 |
| 3 图谱 Nebula | ✅ 未引入 Neo4j |
| 4 可观测 | N/A 无运行时代码 |
| 5 CI/CD | ✅ `cicd: skip` |
| 6 demo2 merge | ✅ 未 merge lumen |
| 7 共享聚合 | ✅ 未让前端直连算法 |
| 8 数据 ADS/Mock | ✅ 未改数仓 |
| 9 D8 Design | N/A |
| 10 D9 血缘 | ✅ 未发明正式 `M_*` 进 seed |
| 11 D10 交互 | N/A |
| 12 D12 demo/lumen | ✅ 只改编排仓 |

## 问题清单

- 旧版不签；等 `human:淮政玮` 再签。本叶保持 `in_progress`。
- 库 7 条 missing 待 A1 交卷回填需规/指标叶 ID。
- Round 18 `DS-ALGO-GAP-L01` 未开工。

## 遗留风险

- 部分 missing 无正式 metric_id，FANIN 未补造。
- 语义欠账 111 条（口径/公式/分项）不进主清单，上线前需产品会签。
- 公式/`algorithm_type` 仍 `pending_cosign: human:唐绍祖`（8/25 前不派）。

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未 commit）
- commit：无
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- **cicd: skip**
- dev 测试 URL / 命令与结果：catalog/pages 指针自检；列 11 missing 仍 7 行

## Cost（必填四字段）

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 2.8（估） |
| cost_warn | green |

## 涉及文件

- `agent-delivery/metrics/request/专题系统/`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ALGO-GAP-L01.md`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/METRIC-OPEN-LOOP-循环工程.md` §4 Round 17
