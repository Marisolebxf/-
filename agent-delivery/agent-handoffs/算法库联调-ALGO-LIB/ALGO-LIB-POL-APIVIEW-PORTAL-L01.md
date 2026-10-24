# ALGO-LIB-POL-APIVIEW-PORTAL-L01 · 联调台展示政策扶持十条

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | `ALGO-LIB-POL-PORTAL-LUMEN-L01` 已有 handoff 且为 integration。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用联调台目录和图表。只加十条的切片，没有新请求层。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 名称对齐 demo 菜单原文，未用压缩代替。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用 |
| 图 diff | 未改图。浏览器只调 Java `GET /policy/v1/policy/indicators?kind=all` |
| 会签态 | 未改图 |
| 说明 | 不直连 Python，不调用 demo。 |

## 范围与实现

政策分析新增页面「政策扶持」（`/policy/portal`）。十条名称与 `demo-ui-system-test` 菜单一致，都以「政策扶持-」开头。

每条请求同一个 Java 指标读接口，`kind=all`。展示前只留下该 key 的 `value`、`series`、`reason`。相近指标和其它 key 不进入这一条。

`series` 为空时图表位置显示「没有可画的序列」，并带上 Python 返回的 `reason`。

## 偏离

无。

## 产物清单

- `src/catalog/policy.json`
- `src/catalog/index.ts`
- `src/api/policyPortal.js`
- `src/api/policy.ts`
- `src/components/algo/ApiTestPanel.vue`
- `src/components/algo/ResultVisualization.vue`
- `src/utils/externalLinks.ts`
- `tests/policyPortal.test.mjs`

## 验收证据

`node tests/policyPortal.test.mjs`：`policyPortal ok`。覆盖有序列、空序列保留原因、相近字段不进入结果。

未对运行中的联调台做浏览器点击。代码在本地，随本任务提交。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 只调 Java 已有指标读接口 | ✅ |
| 不直连 Python，不调用 demo-* | ✅ |
| 每条只展示同 key 的 value 和 series | ✅ |
| 空序列有固定文案和返回原因 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |
