# DS-ALGO-GAP-L01 · 展示系统 vs 算法库差集

> 格式参考 `templates/handoff-template.md`。定义类；**不写业务代码、不改 seed、不签收、不 commit。**  
> **Round 18**（METRIC-OPEN-LOOP）：只改指针 + 分类文案。旧版不签；库 missing 未改。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | Round 18 指针返工。不标 `done` / `ready_to_sign`。8/25 前不派唐绍祖。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义类；指针/分类文案，不以缩代码为目标 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 指针返工；未压缩会签原文 |

## 相对旧版 diff：指针 / 计数

### 指针（catalog `metric_open_status` missing → present）

| page_id | 旧 | 新 |
|---------|----|-----|
| DS-01 ×4（FACTORS / LAYERS / MAP / EVENTS） | missing | present · `METRIC-OPEN-DS-01-科技全域态势-核对记录.md` · `DS-01-METRIC-OPEN-L01` |
| DS-02 ×5 | missing | present · `METRIC-OPEN-DS-02-科学技术全景-核对记录.md` · `DS-02-METRIC-OPEN-L01` |
| DS-03 ×2 | missing | present · `METRIC-OPEN-DS-03-技术发展跟踪-核对记录.md` · `DS-03-METRIC-OPEN-L01` |
| DS-04 ×6 | missing | present · `METRIC-OPEN-DS-04-全球创新监测-核对记录.md` · `DS-04-METRIC-OPEN-L01` |
| DS-05 ×4 | missing | present · `METRIC-OPEN-DS-05-湾区创新监测-核对记录.md` · `DS-05-METRIC-OPEN-L01` |
| DS-06 ×4 | missing | present · `METRIC-OPEN-DS-06-深圳创新监测-核对记录.md` · `DS-06-METRIC-OPEN-L01` |
| DS-07 ×4 | missing | present · `METRIC-OPEN-DS-07-科技创新评估-核对记录.md` · `DS-07-METRIC-OPEN-L01` |
| DS-08 ×3 | missing | present · `METRIC-OPEN-DS-08-科技指数-核对记录.md` · `DS-08-METRIC-OPEN-L01` |
| DS-09 ×3 | missing | present · `METRIC-OPEN-DS-09-科技发展规划-核对记录.md` · `DS-09-METRIC-OPEN-L01` |
| E-ZHIKU | 有 path、无 status | present · `ZHIKU-METRIC-OPEN-L01`（演示态 🔴 未改 mapped） |
| DS-10 / 11 / 12 | 有 E7-DS10-12 path、无 status | present · `POLICY-METRIC-OPEN-L01`；未重写核对记录 |
| DS-13～16 | missing | **仍 missing**；禁止改挂 `TOPIC-TALENT-METRIC-OPEN-L01` |

成果/服务全景/图谱第二波 / ENT-E33 等未在 16 张 OPEN 内，保持原状。

### 计数

| 口径 | 旧版 | Round 18 |
|------|------|----------|
| 缺 OPEN 叶 DS-01…09 | 35 页 catalog missing | **0** |
| 缺 OPEN 叶 E-ZHIKU | 无 status | **0**（补 present） |
| 缺 OPEN 叶 DS-13～16 | 4 | **4（仍 missing）** |
| 库 missing（列 11） | **70**（items 71） | **70（未改 mapped）** |
| mapped / third_party / other_system / n/a_ops | 204 / 16 / 336 / 303 | 同左 |

## 范围与实现

协议 `METRIC-OPEN-LOOP-循环工程.md` §4 Round 18。指针真源 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`。会签通过**仅指指针返工口径**。旧版不签；库 missing 未改；DS-13～16 仍缺 OPEN。不改专题 catalog、不改 LOOP-state、不改 seed、不发明正式 `M_*`。8/25 前不派唐绍祖。

## 偏离说明

- A1 双表未交：`A1需规ID` 空。
- 库 70 条 missing 保持（含态势无正式 ID 的算法缺口）。专题 7 条不重列（`M_POLICY_INDUSTRY_FIT` 仅 also_in）。
- xlsx 加「封面」计数页；清单 930 行未改列 11。yaml 为机器真源。根目录半成品 xlsx 未覆盖。

## 产物清单

- `metrics/request/展示系统/A2-GAP-page-catalog.yaml` + `pages/DS-0*.yaml` / `E-ZHIKU.yaml`
- `metrics/request/展示系统/DS-ALGO-GAP-L01.yaml` / `-summary.md` / `.xlsx` / 本文件
- `agent-handoffs/算法库联调-ALGO-LIB/DS-ALGO-GAP-L01.md`

未覆盖根目录半成品 xlsx、未改 seed、未 commit。

## 验收证据

- DS-01…09 缺 OPEN 35→0；E-ZHIKU 补 present；DS-13～16 仍 missing。
- 库 missing 仍 70。未改挂 TOPIC-TALENT。专题 catalog 未动。
- **cicd: skip**。不签收。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未在 Java 写算法 |
| 2 调用链 | ✅ 差集不改调用链 |
| 3 图谱 Nebula | ✅ 未引入 Neo4j |
| 4 可观测 | N/A 无运行时代码 |
| 5 CI/CD | N/A `cicd: skip` |
| 6 demo2 merge | ✅ 未 merge lumen |
| 7 共享聚合 | ✅ 未让前端直连算法 |
| 8 数据 ADS/Mock | ✅ 未改数仓 |
| 9 D8 Design | N/A |
| 10 D9 血缘 | ✅ 未发明正式 `M_*` 进 seed |
| 11 D10 交互 | N/A |
| 12 D12 demo/lumen | ✅ 只改编排仓 |

## 问题清单

- 旧版不签；等 `human:淮政玮` 再签。
- DS-13～16 展示人才 OPEN 本批未建。
- A1 交卷后回填 70 条 missing 的需规/指标叶 ID。

## 遗留风险

- 语义欠账 247 条不进主清单，上线前需产品会签。
- 态势多条 missing 无正式 metric_id，后续注册须走已挂 OPEN，禁止本叶补造。

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未 commit）
- commit：无
- pipeline URL / ID：N/A
- **cicd: skip**
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 3.2（估） |
| cost_warn | green |

## 涉及文件

- `agent-delivery/metrics/request/展示系统/`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DS-ALGO-GAP-L01.md`
