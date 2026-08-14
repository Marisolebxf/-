# DEMO-CHAIN-UI-SEED-JOB-MOCK-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01`  
> **派单人 / 监管**：`human:淮政玮`（长任务总控已授权，不必再问）  
> **执行**：`algorithm-agent`（协作 `data-agent`）  
> **仓**：`${GKX_ROOT}/repos/demo-algo-science`（push **`origin/dev`**；禁止 `main` / 禁止 force）  
> **Epic**：`E-CHAIN-PROTOTYPE` · Sprint `2026-W33`  
> **强度**：ponytail **full**  
> **结构歧义升级**：`human:李伟`（禁止自创表 / 改主键）  
> **薄条**：[`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01-派单条.md`](./DEMO-CHAIN-UI-SEED-JOB-MOCK-L01-派单条.md)  
> **前序**：`DEMO-CHAIN-UI-SEED-ODS-L01`（联调闸门已过，不等签收 `done`）

淮政玮 2026-08-14 拍板：**段 A 的 LLM MOCK 必须能撑起后面的用例**。不是把 Job 改成「缺底分也绿」，也不是灌正式四力真源。

---

## 段 E 缺陷包（触发）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | [`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md) |
| 故事 ID | `US-CHAIN-REG-01` / `US-CHAIN-REG-03`（连带周期 `US-CHAIN-DIAG` cycle） |
| 已发布 URL | 专题前端（K8s / 外网映射）区域产业评价 |
| 操作步骤 | 集成电路 `INB1303` × 深圳市 `440300` → 生成区域产业指数 |
| 期望 | freeze 后 `load_base_scores` **succeeded**，Job 能出正式 Result（分数标 mock + GAP） |
| 实际现象 | `CHAIN-20260814-011` 第二步 failed |
| HTTP / 页面态 | 过程节点 failed，无 Result |
| **X-Trace-Id** | 前端轮询 `c82596b544f805be783ce4952892e564`；Python execute `0ba2055ff9b67d8183d173914b7e6839` |
| Tempo | Python OTel 打到不存在的 `gkx-otel-collector`（已知残差）；以 Loki/DB `error_msg` 为准 |
| Loki / DB | `BASE_SCORE_MISSING: no subject has scorable index base scores` |
| 怀疑层 | **数据（段 A LLM MOCK 不完整）**，不是 Java/Python 菜谱 bug |
| 诚实空态？ | **否。** 总控本条是「MOCK 须支撑用例」。缺四力底分导致 Job failed = 期望未发生 |

---

## 0. 根因（已核实，不要再猜）

| 层 | 现状 |
|---|---|
| `ads_v2.recalc_ads` | TRUNCATE 含 `industry_chain_region_scorecard`，**从不回写** |
| `DEMO-CHAIN-PY-METRIC-L01` | scorecard **0 行**（「无模型四力，不造假分」） |
| Job `chain:regional:index` | 读 ADS scorecard；`dimension_json` / 列须能解析出四力；全空 → `BASE_SCORE_MISSING` |
| 周期 `chain:diagnosis:cycle` | 读 `industry_chain_metric_series`（跳过 Q056/QC07）；须 **≥2 年** 且 `min(year) ≤ time_range.start_year`。现网资讯约 2023–2025，默认窗若从 2021 起会 `ADS_SERIES_UNAVAILABLE` |
| 瓶颈 | 时序 `unavailable` 允许继续，**本单不挡** |
| 深圳对比 | 菜谱内有 `SZ_MOCK`，**本单不挡** |
| 关键环节 | E1 已绿，**本单不挡** |

Python 解析四力：`lumen_common/algorithms/chain/regional_common.py` `_row_dim_scores` = 行字段 ∪ `dimension_json`。  
指数键：`score_commerce` / `score_tech` / `score_academic` / `score_support`（及 INDEX_ROW_FIELDS 别名）。  
竞争力键：`score_commerce` / `score_academic` / `score_tech`（及 COMP_ROW_FIELDS 别名）。  
**同一行 `dimension_json` 写全上述键，两键都能打分。**

demo DDL 的 scorecard **可能没有** `score_commerce` 等列（只有 `score_total` + `dimension_json`）。**不要改 DDL / 不要加列**（升级李伟）。只写已有列 + JSON。

---

## 1. 目标（一句话）

在 **`demo-algo-science` `chainan/llm_ods`** 把 LLM/离线 MOCK 补全到：**灌数一次之后，区域两键 + 周期键在 Demo 库上能跑通**，且分数/序列诚实标 mock。

---

## 2. 架构裁决（冲突时不得自选）

1. **只改 `demo-algo-science`**（测试可改本仓 `tests/test_chain_llm_ods.py`）。禁止改 `lumen-algo-py` / Java / 前端。禁止把 Job 改成缺底分也 succeeded。  
2. **只写 `demo_gkxlumenx_*`**。`assert_demo_mysql_targets`。正式库行数抽查前后不变。  
3. **仍禁止**：Q056 假市场规模、QC07 假投融资、CMS 历程/介绍、把七键 Result 写入 `graph_snapshot`。  
4. **允许**：确定性 MOCK 四力底分、多年度资讯/企业新增序列。须 `data_version` 含 mock、`dimension_json.gap_ref=GAP-CHAIN-REG-METRICS`（或等价 honesty）。Job 读到分后会标 `status=mock`。  
5. **不建新表、不加列、不改主键**。结构不够用 → `blocked` + 李伟。  
6. **灌数入口仍是** `run_all.py --chain --mode replace|append` / `POST /internal/run-chain-pipeline`。两种 mode 都 TRUNCATE ADS 后全量重算，因此 **scorecard 必须在 `ads_v2.recalc_ads` 写出**，不能只手工 INSERT 一次。  
7. **不要跑** `lumen-algo-py` `metric_engine --self-check`（会 DELETE 指标 6 表、把 scorecard 清回 0）。handoff 写 OPEN：若必须重跑 METRIC，等 coordinator 派投影补单。  
8. git：`origin/dev`；commit `[agent:algorithm-agent]`。

---

## 3. 必做（SEED-09）

### 3.1 区域 scorecard（P0，堵住 `CHAIN-20260814-011`）

对每个 L0 产业（`INB1303` 集成电路、`INB1401` 智能机器人）× `ads_v2` 已有 `geo_map` 城市（**必须含** `深圳→440300`）：

- 插入 `industry_chain_region_scorecard`
- `industry_id` = L0 码；`region_code` / `region_name` 与 `region_dist` 一致
- `score_total` = 四力均值（确定性，不要全员同分）
- `dimension_json` **至少**含：

```json
{
  "score_commerce": 0,
  "score_tech": 0,
  "score_academic": 0,
  "score_support": 0,
  "score_industry": 0,
  "score_innovation": 0,
  "industry_force": 0,
  "innovation_force": 0,
  "academic_force": 0,
  "support_force": 0,
  "industry_foundation": 0,
  "academic_ecology": 0,
  "innovation_ecology": 0,
  "gap_ref": "GAP-CHAIN-REG-METRICS",
  "honesty": "mock"
}
```

（数值用种子哈希，区间建议 55–90，城市间有区分。）

- `metric_id=M_CHAIN_REGION_INDEX`；`publish_status=published`；`data_version` 带 `mock`
- **禁止**把 `M_CHAIN_MARKET_SIZE` / INVEST_* 写进 scorecard 当分

验收：`(industry_id=INB1303, region_code=440300)` 至少 1 行；四力键均可被 `_row_dim_scores` 解析为非空。

### 3.2 周期主序列（P0）

- `build_news`（或等价）年份覆盖 **2020–2025**（含），使 DWD 资讯分年 ≥6 档  
- `ads_v2` 对 L0 `INB1303` / `INB1401` 写出 `M_CHAIN_NEWS_COUNT`（或其它 **非 Q056/QC07**）`metric_series`，`object_id=industry_id`，年份覆盖 **2020–2025**  
- 满足 cycle：`len(years)≥2` 且 `min(year)≤2021`（对齐 `tests/test_chain_cycle.py` 默认窗 2021–2029）

### 3.3 回归矩阵（灌数后自检，写进 handoff）

| 用例 | 最低数据 | 期望 |
|---|---|---|
| 区域指数 `INB1303`×`440300`（可再加北京/上海） | scorecard 四力非空 | `load_base_scores` 不再 `BASE_SCORE_MISSING` |
| 区域竞争力 同上 | 同一 JSON 含三维键 | 同上 |
| 周期 `industry=INB1303`，窗 2021–2025 | 非 Q056 序列覆盖 | 不再 `ADS_SERIES_UNAVAILABLE` |
| 门户 KPI | 已有企业数等 | 不回退；Q056/QC07 仍 null |
| 关键环节 / 深圳负例 | 不依赖本单 | 不破坏 |

能 curl 本机/集群 Python `/internal/v1/chain/jobs/execute` 则实跑区域指数到 `load_base_scores` succeeded（或整 Job succeeded）。不能 curl 则用 **直连 demo ADS 的断言脚本** + 说明环境限制。

---

## 4. 明确不做

- 改 `lumen-algo-py` 菜谱 / METRIC 引擎  
- 假市场、假投融资、假 CMS  
- 写正式 `gkxlumenx_*`  
- 为查询上 ES、改 Nebula 模式  
- 把 MOCK 标成 `live` / 把就绪度改绿  
- system-test 视觉大改（灌数按钮文案可加一行「含区域 MOCK 底分」，非必须）

---

## 5. 必读（禁止用压缩摘要代替精读）

| 序 | 路径 |
|---:|---|
| 1 | 本文件 + 派单条 + 长任务总控 |
| 2 | `repos/demo-algo-science/chainan/llm_ods/ads_v2.py` · `generate.py` · `ddl.py` scorecard |
| 3 | `repos/lumen-algo-py/lumen_common/algorithms/chain/regional_common.py`（只读，对照解析键） |
| 4 | `DESIGN-LANDING-regional_index.v0.md` §8；`USM-CHAIN-TOPIC-REGIONAL.md` |
| 5 | `storage/CHAIN/seeds/README.md` · `etl/pipeline-demo-mock.md` §5 |
| 6 | `DEMO-CHAIN-UI-SEED-ODS-L01.md`（勿回退只写 demo_* / 勿再灌 Q056 市场） |

---

## 6. DoD

- [ ] `ads_v2.recalc_ads` 写出 scorecard（replace/append 都会再有）  
- [ ] `INB1303`+`440300` 四力可解析；至少 2 个区域有分（能排名）  
- [ ] L0 资讯/序列覆盖 2020–2025；cycle 窗 2021 起不因序列失败  
- [ ] Q056 / QC07 ADS 值仍为 NULL  
- [ ] 正式库抽查未变（`gkxlumenx_ods.dwd_org_industry_tags`、`gkxlumenx_dwd.chain`）  
- [ ] `python scripts/run_all.py --self-check` 或本仓 llm_ods 测试绿  
- [ ] Demo 库 **replace 实跑**；handoff 附表行数  
- [ ] 更新 `storage/CHAIN/seeds/README.md` 增 **SEED-09**（区域 MOCK 底分 + 周期序列）  
- [ ] handoff：`agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-UI-SEED-JOB-MOCK-L01.md`（认领 / ponytail full / cost 四字段 / 架构合规 / OPEN：METRIC 重跑会清空 scorecard）

---

## 7. `/goal`

```text
/goal
你是经验丰富、遵循业界最佳实践的算法工程师（algorithm-agent）。
任务：DEMO-CHAIN-UI-SEED-JOB-MOCK-L01 段 A LLM MOCK 补全，支撑区域/周期 Job
仓库：${GKX_ROOT}/repos/demo-algo-science（push origin/dev）
监管：human:淮政玮
强度：ponytail full。禁止用 YAGNI 跳过 scorecard 回写、多年度序列、handoff、只写 demo_*、D9 mock/GAP 标记。
上下文：headroom 推荐。本派单说明 + regional_common 解析键 + DESIGN-LANDING-regional_index 禁止 compress 代替精读。

必读：agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-UI-SEED-JOB-MOCK-L01-派单说明.md
铁律：只改 demo-algo-science；只写 demo_gkxlumenx_*；不改 lumen-algo-py；
不造 Q056/QC07 假市场/投融资；不建表不加列；scorecard 必须在 ads_v2 全量重算写出；
dimension_json 同时服务指数四力与竞争力三维；深圳 440300 必有行。
不要跑 lumen-algo-py metric_engine。
DoD：见本派单说明 §6。
完工写 handoff agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-UI-SEED-JOB-MOCK-L01.md
```
