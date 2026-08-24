# ALGO-LIB-T0X-L01 · T0-X 三清单收口（纠偏：先入库再分桶）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义/会议叶 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 禁止 compress 代替精读分析清单与 L02 |

## 偏离说明（主持纠偏 2026-08-24 20:03）

原派单把 T0-X 写成「对 77 条 missing 当场四桶」。主持实际顺序是：

1. **先把分析出来的指标全部写入 `metrics/registry`**  
2. **再在库上逐条核对**（分桶 / 指定 `algorithm_type`）

上次预分桶（①4 / ②0 / ③0 / ④73）**作废**。yaml 处置桶已回滚未分拣。

## 覆盖证据（lib 查询，不整文件读 seed）

`metrics/request/_work/ALGO-LIB-T0X-L01-registry-coverage.json`

| 清单 | 结论 |
|------|------|
| F−L 77 | 5 条已在 seed；**72 条无 `metric_id`**，不能点名核对 |
| F∩L 专题 mapped | unique `M_*` 116：seed 67；**49 未入**（`M_CHAIN_REG_*` / 大量 `M_SVC_*`）；另 53 行无号 |
| F∩L 展示 mapped | unique 78：seed 75；3 未入；另 113 行无号 |
| A1 表2 | 正式 11 入 10（缺 `M_ENT_KEY_TOTAL`）；**90 `TEMP_ALGO_*` 不在 seed** |
| registry | 346 条身份；类型已填仅 10，336 = UNKNOWN |

## 后续拆单

| 叶 | 做什么 | Owner | 状态 |
|--------|--------|-------|------|
| `ALGO-LIB-T0X-REGISTER-L01` | 赋号（无 `M_*` 行）+ 已有号未入 seed 的注册；`D1=draft`，类型 `UNKNOWN` | data-agent；监管淮政玮 | **ready**（2026-08-24 MCP） |
| `ALGO-LIB-T0X-L01` 复会 | 闸门：要核对的行 `metric-get` → `found.seed=true` 后，再逐条分桶/定类型 | 本会原四席 | 仍 `blocked` |

OPEN / GDF 仍会后按桶拆，入库完成前不开。

## 产物清单

- `metrics/request/T0X/ALGO-LIB-T0X-L01-minutes.md`（纠偏稿）
- `metrics/request/T0X/ALGO-LIB-T0X-L01-pre-meeting.yaml`（未分拣 77+22）
- `metrics/request/_work/ALGO-LIB-T0X-L01-registry-coverage.json`
- 本 handoff

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 不写算法 |
| 调用链 | ✅ 不越层 |
| Nebula | ✅ 不引入 Neo4j |
| D9 | ✅ 不把 missing 改绿；本叶不发明 `M_*` 写入 seed |
| D12 | ✅ 不调 demo 服务 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000（按 estimated；含纠偏） |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.40 |
| cost_warn | green |

## 遗留风险

- T0-X DoD「每条落入四桶」在入库完成前无法满足。任务应保持阻塞，直到 REGISTER 叶交稿。
- 72 条无号若强行编 `M_*` 会与「T2 另叶赋号」冲突；必须走赋号 + data-agent 注册，禁止本会话手写 seed。

## CI/CD

- 分支：`dev`（编排仓；未要求 push）
- commit：待监管人确认
- pipeline / K8s：N/A
