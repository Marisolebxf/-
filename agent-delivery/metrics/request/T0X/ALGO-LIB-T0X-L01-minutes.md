# ALGO-LIB-T0X-L01 · T0-X 会纪要（纠偏）

> 任务：`ALGO-LIB-T0X-L01`  
> 书记：`agent:product-agent` · 主持纠偏：`human:淮政玮`（2026-08-24 20:03）  
> yaml：`ALGO-LIB-T0X-L01-pre-meeting.yaml`（处置桶已回滚 **未分拣**）  
> 覆盖对照：`metrics/request/_work/ALGO-LIB-T0X-L01-registry-coverage.json`（`metric-registry-lib`，未整文件读 seed）

---

## 0. 主持纠偏（本页有效结论）

**正确顺序**：分析清单上的指标先全部进入 `metrics/registry`（seed 身份，`D1=draft`，类型可 `UNKNOWN`）→ **再**在库里逐条核对（分桶 / 指定 `algorithm_type`）。

上次按「无 ID 的 missing 行」直接落四桶，**顺序反了，分桶作废**。yaml 已回滚。四桶整数不再作为决议。

本叶仍不写公式、不把 missing 改 mapped。入库叶已建：`ALGO-LIB-T0X-REGISTER-L01`（`ready` · `data-agent` · 监管 `human:淮政玮` · pull，不代认领）。

---

## 1. 现在库里有什么、分析清单缺什么

registry 现网：seed+矩阵合计 **346** 条身份；`algorithm_type` 已填仅 **10**（SEED-TYPE 的 3 STAT + 7 MODEL），其余 **336 = UNKNOWN**。

| 分析清单 | 有正式 `M_*` | 其中已在 seed | 行上无 `metric_id` | 有号但不在 seed |
|----------|--------------|---------------|--------------------|-----------------|
| F−L 77（本会主清单） | 5 | **5** | **72** | 0 |
| F∩L 专题 mapped 171 | 116 unique | 67 | 53 行 | **49**（多为 `M_CHAIN_REG_*` / `M_SVC_*`） |
| F∩L 展示 mapped 204 | 78 unique | 75 | 113 行 | 3（`M_ENT_STAR_ENTERPRISE_COUNT` / `M_ENT_RESEARCHER_COUNT` / `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`） |
| A1 表2 | 11 正式 + 90 `TEMP_ALGO_*` | 正式 10；`M_ENT_KEY_TOTAL` 未入；TEMP **0** | — | `M_ENT_KEY_TOTAL` + 90 TEMP |

F−L 已在 seed 的 5 条（可待入库完成后一起定类型，本会仍不拍桶）：

- `M_CHAIN_PRODUCT_COUNT` / `M_CHAIN_PATENT_COUNT`
- `M_POLICY_INDUSTRY_FIT`
- `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_COLLAB_OUTPUT_CORR`

F−L **72 条无号**：无法在 registry 里点名核对。展示 missing 70 条全部无号；专题另 2 条无号 = `TOPIC-DIAG-018` 环节健康度、`TOPIC-SZ-016` 全球成功案例匹配。

专题 mapped 未入 seed 的 49 个号，与 REGISTER 已写明的事实一致：B 轨 `M_SVC_*` 未全量灌 SVC seed；一批 `M_CHAIN_*` 区域/深圳对比号不在 CHAIN seed。

---

## 2. 正确工作流（会前必须做完）

```text
分析真源（A1 表2 + A2 L02 items）
    → 无 M_* 的行：赋号（METRIC-ID-ASSIGN 同类，D1=draft）
    → 有 M_* 但不在 seed：注册进 cfg_metric-{域}-seed.yaml + 矩阵
    → TEMP_ALGO_*：先赋正式号再注册，禁止把 TEMP_ 当页面终态
    → 会前闸门：本会要核对的每一行都能 metric-get 到 found.seed=true
    → T0-X：在库里逐条 分桶 + 指定 algorithm_type（STAT/MODEL/GRAPH/…）
```

入库叶（2026-08-24 20:21 MCP 已建）：`ALGO-LIB-T0X-REGISTER-L01`  
执行：`data-agent` · 监管：`human:淮政玮` · 类型仍 `UNKNOWN` 直到本会逐条指定（唐绍祖签公式/类型）。  
派单：`agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-T0X-REGISTER-L01-派单包.md`

入库范围建议（主持可裁）：

1. F−L 72 条无号 → 赋号 + 注册  
2. F∩L 已有号、未入 seed：专题 49 + 展示 3 + `M_ENT_KEY_TOTAL`  
3. 专题 mapped 53 行 / 展示 mapped 113 行无 `metric_id` → 按 A1指标叶ID 赋号或 reuse 后再注册  
4. A1 90 条 `TEMP_ALGO_*` → 赋正式号后注册（与 3 可能重叠，去重）

---

## 3. 本会暂停项

| 项 | 状态 |
|----|------|
| F∩L 171+204 计数 | L02 原文仍有效，不是入库 |
| F−L 四桶 | **未分拣**（作废 ①4/②0/③0/④73） |
| L−F 22 | **未分拣**（入库后与功能清单一起核对；原则 3 仍适用） |
| 桶③ / 郭万迎 ±10% | 无名单；入库完成后再议 |
| SEED-TYPE 10 条 | 与 F−L 77 仍不相交；不能当 72 条无号的替身 |

SEED-TYPE / REGISTER-L01 / OPEN 赋号 **不是**「A2 77 条可以开始映射」的绿灯。

---

## 4. 作废记录（2026-08-24 19:19 预分拣，不执行）

曾误按原则 2 把 4 条写成 ①、其余 73 写成 ④、L−F 22 写成联调台 DEMO。主持指出应先入库。该表作废，不进拆单。

---

## 禁止事项

- [x] 未把 missing 改 mapped  
- [x] 未改 seed / 未发明正式 `M_*`（入库另叶）  
- [x] T0-X 本叶不代认领入库；主持点名后已 MCP `ALGO-LIB-T0X-REGISTER-L01`  
- [x] yaml 处置桶已回滚未分拣  
- [ ] 会前闸门：要核对的行全部 `found.seed=true`（未达到）
