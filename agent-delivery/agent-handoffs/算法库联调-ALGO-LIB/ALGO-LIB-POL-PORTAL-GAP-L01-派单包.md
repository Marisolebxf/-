# 派单包：ALGO-LIB-POL-PORTAL-GAP-L01 — 算法中台补门户政策扶持十条指标缺口

- **任务 ID**：ALGO-LIB-POL-PORTAL-GAP-L01
- **标题**：算法中台补门户政策扶持十条指标缺口
- **派发角色**：coordinator-agent
- **承接角色**：algorithm-agent（协作 frontend-agent）
- **监管人**：human:淮政玮
- **仓**：`${GKX_ROOT}/repos/demo-algo-ent-analysis`（计算）；`${GKX_ROOT}/repos/demo-ui-system-test`（展示）。两仓都 push `origin/dev`
- **登记状态**：`backlog`。**本文件写出时未认领，未改 registry**
- **依赖**：`PORTAL-CMS-METRIC-COVER-POL-L01` 现为 `ready_to_sign`，监管人 `human:淮政玮`。该单 `done` 之前，本单保持 `backlog`，不得 `task-claim`
- **effort / difficulty**：8 / L · est.tokens 120000
- **task_type**：feature
- **强度**：ponytail full
- **派发说明落盘**：2026-10-23

认领窗口（依赖签收、本单升 `ready` 之后才写）：`claimed_by=agent:algorithm-agent`，`supervised_by=human:淮政玮`，`claim_type=pull`，锁定 4 小时。明确开工再改 `in_progress`。

---

## 0. 现在为什么不能开工

建单 note 写明：建单不认领；核对单未 `done` 前本单保持 `backlog`。认领指南只允许认领 `ready`，且 `depends_on` 全部 `done`。

要开工，先由 `human:淮政玮` 签收 `PORTAL-CMS-METRIC-COVER-POL-L01`，再由 coordinator 把本单升到 `ready`，然后才能认领。

---

## 1. 背景

门户政策扶持契约里有十条展示行。`PORTAL-CMS-METRIC-COVER-POL-L01` 的结论是：这十条都没有可以改挂的现成 `metric_id`。相近 ID 种子里有、矩阵未覆盖、D1 为空，对象也对不上招标句。

本单把这十条补进**算法中台 demo**：计算在 `demo-algo-ent-analysis`，展示在 `demo-ui-system-test` 政策分析。demo 数不接进 lumen，也不填 `SYSINT-03-04B` 的门户缺口（那些行继续空态）。

## 2. 十条（独立结果，禁止改挂）

真源：`agent-delivery/agent-handoffs/PORTAL-CMS-METRIC-COVER-POL-L01.md` §十条缺项。下表只列不能拿来填空的 ID。

| # | 展示行 | 不能改挂 |
|---|---|---|
| 1 | 全国相关产业政策数量及连续性 | `M_POLICY_TOTAL_COUNT`、`M_POLICY_TIMESERIES`、`M_POLICY_OPPORTUNITY_COUNT` |
| 2 | 各省政策数量对比及连续性 | `M_POLICY_LEVEL_DIST`、`M_POLICY_TOTAL_COUNT`、`M_POLICY_TIMESERIES` |
| 3 | 重点城市政策数量对比及连续性 | 同上。没有 `M_POLICY_CITY*` |
| 4 | 全国政策发布密度 | `M_POLICY_NATIONAL_DIST`（按省计数和占比，没有分母） |
| 5 | 省发布密度 | 同上，且不是省内密度 |
| 6 | 市发布密度 | 没有市级密度 ID |
| 7 | 产业链各节点政策覆盖 | `M_POLICY_INDUSTRY_COVERAGE`（覆盖率，不是各节点覆盖） |
| 8 | 深圳相关产业政策数量及趋势 | `M_POLICY_SZ_DIST`、`M_POLICY_TIMESERIES`、`M_POLICY_TOTAL_COUNT` |
| 9 | 深圳各区发布情况 | `M_POLICY_SZ_DIST`、`M_CHAIN_SZ_POLICY` |
| 10 | 深圳产业链节点政策覆盖 | `M_POLICY_INDUSTRY_COVERAGE` |

力度排名只认 `M_POLICY_INTENSITY_SCORE`。`M_POLICY_INTENSITY_INDEX` 不替换它。本单不新造排名 ID。

发布密度没有已登记分母时，结果为空，并写明缺分母。政策条数不能冒充密度。重点城市名单未登记时，市级对比为空，不自造城市集。

本单不新编正式口径，不改指标种子、就绪度矩阵、`PORTAL-CMS-政策扶持.md`，不拍板 QPOL-02。

## 3. 范围

### 3.1 计算（algorithm-agent）

仓：`demo-algo-ent-analysis`。点名文件：

- `polan/basic/indicators.py`
- `polan/eval/intensity.py`

十条各有自己的结果结构。可以复用已有聚合函数，但返回对象必须对应该行的招标句。对象不同的 ID 保持原语义，不把门户缺口挂到它们上面。

算不出的行返回空，并带原因（缺分母、缺城市名单、连续性公式仍是 `pending_algorithm`、QPOL-02 未闭合）。空也算一条独立结果。

### 3.2 展示（frontend-agent）

仓：`demo-ui-system-test`。点名文件：

- `src/views/policy/components/BasicIndicators.vue`

政策分析页能看见这十行。有数的行显示计算结果；空的行显示原因，不拿相近指标的数填上。调用链仍是页面 → Java → Python，不直连 Python，不把 demo 服务接进 lumen。

### 3.3 明确不做

- 不改 `agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md`
- 不改指标种子、就绪度矩阵
- 不拍板 QPOL-02
- 不让 `SYSINT-03-04B` 改读这十条 demo 数；门户缺口继续空
- 不新造省级排名 ID、城市排名 ID

## 4. DoD

1. 十条在算法中台 demo 各有独立结果：全国/省/市数量及连续性，全国/省/市发布密度，产业链节点覆盖，深圳数量及趋势、各区发布、深圳节点覆盖。展示在 `demo-ui-system-test` 政策分析，计算在 `demo-algo-ent-analysis`。
2. 相近 ID 不顶缺口。`M_POLICY_OPPORTUNITY_COUNT` 不顶数量；`M_POLICY_LEVEL_DIST` 的行政级别不顶省市对比；`M_POLICY_NATIONAL_DIST` 的按省计数与占比不顶发布密度；`M_POLICY_INDUSTRY_COVERAGE` 的覆盖率不顶各节点覆盖；`M_POLICY_INTENSITY_INDEX` 不替换 `M_POLICY_INTENSITY_SCORE`。
3. 发布密度没有已登记分母时结果为空，并写明缺分母。重点城市名单未登记则市级对比为空。
4. 不改契约、种子、矩阵；不拍板 QPOL-02；demo 不进 lumen 调用链；`SYSINT-03-04B` 对这些缺口仍返回空。
5. handoff 逐条写明用了哪段计算、哪行仍空。单测至少一条证明缺口没有被相近 ID 填上，一条证明密度缺分母时为空。
6. handoff 路径：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-POL-PORTAL-GAP-L01.md`。含 `ponytail:` 行与 cost 四字段。

## 5. /goal 话术（依赖签收且本单 `ready` 之后，复制到新会话）

```markdown
/goal algorithm-agent
身份：你是政策分析算法工程师。计算只在 Python。前端只经 Java 网关。不新编正式口径，不改指标种子和就绪度矩阵。
任务 ID：ALGO-LIB-POL-PORTAL-GAP-L01
监管人：human:淮政玮
强度：ponytail full
仓库：
  - ${GKX_ROOT}/repos/demo-algo-ent-analysis（push origin/dev）
  - ${GKX_ROOT}/repos/demo-ui-system-test（push origin/dev，展示协作 frontend-agent）
必读：
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-POL-PORTAL-GAP-L01-派单包.md
  - agent-delivery/agent-handoffs/PORTAL-CMS-METRIC-COVER-POL-L01.md
  - agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md
  - agent-delivery/bid-reference/智慧服务门户系统-要素相关.md
目标：
  1) 十条缺口在 demo 各有独立结果；相近 ID 不改挂
  2) 发布密度无已登记分母则为空并写明原因；重点城市名单未登记则市级对比为空
  3) 政策分析页展示这十行；SYSINT-03-04B 继续对这些缺口返回空
DoD：见派单包 §4。完工 handoff。认领时 status=ready 才 task-claim；开工后改 in_progress。
不要问我，按派单包执行。
```
