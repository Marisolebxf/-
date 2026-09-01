# DATA-POLICY-DEMO-ACCEPT-MATRIX-L01 · Demo 算子级验收对照

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控） |
| 说明 | 用户要能点测验收 demo；算子真实计算；lumen 只参考算子必重写工程；每页可在 apiview 测 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·对照文档；apiview catalog 只补路由对齐） |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无新流图；对照 `POLICY-ETL-DEMO-MOCK` |
| 图 diff | 未改 S1 会签图 |
| 会签态 | `01-data-flow.md` approved |

## 范围与实现

写成 `etl/demo-operator-accept-matrix.md`：35 条对照、两套 UI、手算抽检、lumen 接手边界。  
apiview `policy.json` 补 parse/match/simulate/guide/guard，与 system-test 算子页对齐。

## 偏离

无。写明「真实」= 对 Mock DWD 的确定性算子，不是正式大数据工程。

## 产物清单

- `agent-delivery/data/data-design/storage/POLICY/etl/demo-operator-accept-matrix.md`
- `etl/README.md` 索引行
- `CHANGELOG.md`
- `lumen-ui-algo-apiview/src/catalog/policy.json` + `index.ts` + `scripts/catalog.test.mjs`
- 本 handoff

## 验收证据

- 对照覆盖叶 22 + 组合 4 + 身份 9
- `node --test scripts/catalog.test.mjs` → 20 passed
- 会签通过：定位与 lumen 边界已写死

## 问题清单

- Demo 库需现场灌数后才能按 §3 点绿
- apiview catalog `status` 字段仍为历史 `unavailable` 标签，不影响 `runtime=java_api` 真调

## 修改内容

见产物。

## 测试结果

- catalog 20 测过
- 未改 polan

## 遗留风险

- 旧 Python 无 `analysis/guide` 时对照 §3 #8/#9 会红

## CI/CD

- 未提交
- 测：`lumen-ui-algo-apiview` `node --test scripts/catalog.test.mjs`

## 可观测性

- N/A

## 涉及文件

- 见产物清单

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 对照指向 polan，未把公式搬进 Java |
| 调用链 | ✅ apiview 仍 `/policy/v1/**` 经网关 |
| 图谱仅 Nebula 一张 G | ✅ |
| 可观测 | N/A（文档叶） |
| CI/CD | 未推 |
| demo2 不 merge lumen | ✅ 只补 apiview catalog |
| Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ 对照按 ADS 读面 |
| D8 / D10 | N/A |
| D9 指标 8 件套 | ✅ 35 条按 metric_id |
| D12 | ✅ lumen 只参考算子、工程重写 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 38000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.18 |
| cost_warn | green |
