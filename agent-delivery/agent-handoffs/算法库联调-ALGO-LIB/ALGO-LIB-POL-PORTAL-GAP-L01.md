# ALGO-LIB-POL-PORTAL-GAP-L01 · 算法中台补门户政策扶持十条指标缺口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 依赖 `PORTAL-CMS-METRIC-COVER-POL-L01` 已 `done` 后，本单由 `backlog` 升到 `ready` 再认领，锁定 4 小时。监管人按派单包与「以淮政玮认领」。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 十条共用一个纯函数，空结果也算独立行。未用 YAGNI 跳过调用链、handoff。未新编口径，未改种子和矩阵。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未用 Headroom 压缩本单材料。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用 |
| 图 diff | 未改架构图。demo 结果只挂在既有 `GET /v1/policy/indicators?kind=all` |
| 会签态 | 不适用 |
| 说明 | 本叶不改存储流图或时序图。 |

## 问题清单

- QPOL-02 仍是 🟡。本单不拍板。机遇数不顶数量。
- 发布密度没有已登记分母。重点城市名单没有登记。连续性 / 增长率公式仍是 `pending_algorithm`。
- `SYSINT-03-04B` 不读这十条 demo 数。

## 范围与实现

DoD 五条都落在 demo。十条在 `portal_gap_rows` 各有独立结果，政策分析左侧「基础指标」下各有一页。相近指标不填数。密度缺分母、重点城市名单未登记时为空并写明原因。种子、矩阵、`PORTAL-CMS-政策扶持.md`、lumen 与 SYSINT-03-04B 都没改。

## 偏离

展示从基础指标页的一张总表改成十条独立菜单，名称以「政策扶持-」开头。每页只画该条的 `series`。`series` 为空时图上写「没有可画的序列」。结果仍全部为空，原因与派单包一致。

## 产物清单

- `demo-algo-ent-analysis` `5427a65`：十条独立结果与单测
- `demo-ui-system-test` `67ccd78`：十条菜单与页面
- `demo-ui-system-test` `dfe18cb`：菜单名称加上「政策扶持-」
- 本 handoff

## 验收证据

- 单测 `tests/test_policy_portal_gaps.py`：2 passed
- 本地政策分析页十条菜单各打开一次，结果为「空」，原因与算法返回一致
- 上述 commit 已在各自 `origin/dev`。本次未再查 K8s rollout

## 修改内容

计算在 `demo-algo-ent-analysis` 的 `portal_gap_rows`。`nearby_metrics` 只参与拒绝改挂，不写入 `value`。`reject_portal_gap_rehang` 拒绝把 `M_POLICY_INTENSITY_INDEX`、`M_POLICY_INTENSITY_SCORE`、`M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH` 写成 `filled_from` 或 `metric_id`。力度排名仍只认 `M_POLICY_INTENSITY_SCORE`，不在这十条里，也不新造排名 ID。

展示在 `demo-ui-system-test` 政策分析左侧菜单，「基础指标」下面十条各一页。每页只读 `fetchIndicators('all')` 返回的 `portal_gaps` 里同 key 的一行，并画该行的 `series`。`series` 为空时图上写「没有可画的序列」。基础指标页不再放这张总表。调用链仍是页面 → `/api/policy/v1` → 网关 → Python。

| # | 展示行 | 用的计算 | 结果 |
|---|---|---|---|
| 1 | 全国相关产业政策数量及连续性 | `portal_gap_rows`，不读总数 / 时序 / 机遇数 | 空。连续性公式仍是 `pending_algorithm`。相关产业范围未登记。QPOL-02 未闭合，机遇数不顶数量 |
| 2 | 各省政策数量对比及连续性 | 同上，不读行政级别分布 | 空。连续性公式仍是 `pending_algorithm`。行政级别不是各省对比 |
| 3 | 重点城市政策数量对比及连续性 | `key_cities` 缺省为空（配置里没有名单） | 空。重点城市名单未登记 |
| 4 | 全国政策发布密度 | `density_denominator` 缺省为空 | 空。缺已登记分母。按省计数与占比不顶密度 |
| 5 | 省发布密度 | 同上 | 空。缺已登记分母。按省计数不是省内密度 |
| 6 | 市发布密度 | 同上 | 空。缺已登记分母。没有市级密度 |
| 7 | 产业链各节点政策覆盖 | 不读覆盖率 | 空。各节点覆盖没有已登记公式。覆盖率 `pending_algorithm` 不顶各节点 |
| 8 | 深圳相关产业政策数量及趋势 | 不读深圳按区分布 / 全库时序 / 总数 | 空。趋势所用连续性与增长率仍是 `pending_algorithm` |
| 9 | 深圳各区发布情况 | 不读深圳按区存量计数 | 空。发布口径未登记 |
| 10 | 深圳产业链节点政策覆盖 | 不读全库覆盖率 | 空。没有深圳各节点覆盖公式 |

未改 `PORTAL-CMS-政策扶持.md`、指标种子、就绪度矩阵。未改 `lumen-algo-py`。该仓 `vendor` 里的 `/internal/policy/indicators` 没有 `portal_gaps`。

## 测试结果

- `python -m pytest tests/test_policy_portal_gaps.py -q`：2 passed。
- 一条证明十条的 `value` 都不是传入的相近指标标量（含机遇数 7、总数 99、级别分布 40、全国分布 12、覆盖率 80、力度指数 55）。
- 一条证明三条发布密度在分母为空时 `value` 为空且原因含「缺已登记分母」；市级对比在名单为空时原因含「重点城市名单未登记」。
- 本地打开政策分析左侧菜单。十条都在「基础指标」下方，点进各自页面只显示这一条：结果为「空」，图为「没有可画的序列」。市级对比写明重点城市名单未登记，全国密度写明缺已登记分母。基础指标页不再出现这十条总表。页面数据来自本次 `portal_gap_rows`，不是远端已部署服务。

## 遗留风险

- 十条目前都是空结果。分母、重点城市名单、相关产业范围、连续性公式登记之后才能填数。
- 页面要看到这十条，已部署的 demo 政策算法服务须包含 `portal_gaps`。代码已推 `origin/dev`，本次未再查部署是否已滚出。
- 注册表 `model_used` 枚举没有 Grok。价按 `claude-sonnet-4.5` 价表、algorithm 75/25 估算。`source: estimate_no_console`。

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` 与 `demo-ui-system-test` 的 `origin/dev`
- commit：`5427a65`、`67ccd78`、`dfe18cb`
- pipeline URL / ID：未在本次记录
- 部署 namespace / 镜像 tag：未在本次记录
- K8s rollout：未再查
- dev 测试 URL / 命令与结果：单测 2 passed。本地 `#/policy/portal-*` 十条页面已核对

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新加服务
- traceId（dev 抽样）：无
- Tempo / Loki：无新埋点。沿用政策分析页原有请求

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/basic/indicators.py`
- `repos/demo-algo-ent-analysis/polan/eval/intensity.py`
- `repos/demo-algo-ent-analysis/api/policy_routes.py`
- `repos/demo-algo-ent-analysis/tests/test_policy_portal_gaps.py`
- `repos/demo-ui-system-test/src/views/policy/policyMenuConfig.ts`
- `repos/demo-ui-system-test/src/views/policy/pages/PortalGapPage.vue`
- `repos/demo-ui-system-test/src/router/index.ts`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ |
| 前端只经既有网关到 Python | ✅ |
| 未把 demo 接进 lumen | ✅ |
| 未改种子、矩阵、契约 | ✅ |
| 未拍板 QPOL-02 | ✅ |
| 未写 Nebula | ✅ |
| 未新造对象存储桶 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 90000 |
| model_used | 会话为 Grok 4.7；注册表枚举写入 `claude-sonnet-4.5`（价表代理） |
| actual_cost | 0.54 |
| cost_warn | green |

ponytail: full
