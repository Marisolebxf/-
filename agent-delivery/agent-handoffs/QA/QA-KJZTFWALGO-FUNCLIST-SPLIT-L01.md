# QA-KJZTFWALGO-FUNCLIST-SPLIT-L01 · v2 进度（未收口）

> 本文件是 **v2 合表节点**，不是完工 handoff。registry 保持 `in_progress`（任务已从 MCP 摘走时仍勿自行 `done`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |
| agent | `qa-agent` |
| status | `in_progress`（v2 已出；勿自行 `done`） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 拆点/合表文档，不缩 D8/D9/D10。 |

## 范围与实现

- 输入：功能清单 v1.2 · sheet「深度挖掘算法」· 四级「科技专题服务算法库」· **60 六级**
- 编号：`ZNFWJQ-KJZTFWALGO-v1.0-FUNC-#####`
- 原则：v1.6（2026-09-03 拍板）
- 合表 v1（冻结）：3347 条；**未覆盖**
- 合表 v2：**3960** 条；A1=`智能服务集群-科技专题服务算法库功能点拆分`
- 拆法：v1.5 口径 B 底稿 + **口径 C** + F−L 可挂/弱挂 + F−L 开 C + T01 B5

## 偏离说明

- 总集要求 **3889**，v2 为 **3960**（超出 71）。原则「数量超出不裁」；未为压条数删点，未用权重三步/笛卡尔补差。
- 不挂 25 条、同簇不计 3 条、已覆盖 2 条（L13 中心度/密度）未写入。
- 弱挂 39 条规则来源 = `验收补充`；可挂 8 条 = `原文隐含`。
- 同 sheet 其余约 52 条六级仍不纳入。
- MCP `task-get QA-KJZTFWALGO-FUNCLIST-SPLIT-L01` 当前查无此 ID。

## 产物清单

| 产物 | 路径 |
|---|---|
| 合表 Excel v1（冻结） | `agent-delivery/qa/total-set/KJZTFWALGO/6.国际科技信息中心项目_科技专题服务算法库_功能点拆分_v1.xlsx` |
| 合表 Excel v2 | `agent-delivery/qa/total-set/KJZTFWALGO/6.国际科技信息中心项目_科技专题服务算法库_功能点拆分_v2.xlsx` |
| 原则 v1.6 | `…/科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md` |
| 中间稿 | `fp-split-run/work/` `review/` `prompts/` `00-control.md` `01-task-list.md` |
| F−L 对照 | `fp-split-run/work/_fl77-to-l60-map.md` |
| apply / 合表 / 核对 | `_apply_kjztfwalgo_fp_v2.py` · `_merge_kjztfwalgo_fp_split_work.py` · `_check_kjztfwalgo_fp_work.py` |
| 本机快照（不入库） | `fp-split-run/snapshots/v1/` |

## 增量（相对 v1）

| 笔 | 条数 |
|---|---|
| 口径 C（v1 点名阈值） | +326 |
| F−L 可挂 + 弱挂（含评估/识别类自带 C） | +283 |
| T01 B5 有效性验证不通过不发布 | +4 |
| **合计** | **+613 → 3960** |

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python / 不写界面功能点 | ✅ |
| 调用链 / Nebula / 可观测 | N/A（拆点文档） |
| D12 demo 不入库 lumen | ✅ |
| 未读 demo-algo / lumen-algo / 五件套增减点 | ✅ |
| 口径 C 不 × 空态/优短 | ✅ |
| 未覆盖 v1 xlsx | ✅ |

## cost（v2 节点）

| 字段 | 值 |
|------|-----|
| actual_tokens | 未回填 Console |
| model_used | Cursor Grok 4.6 |
| actual_cost | 未回填 |
| cost_warn | n/a |
| source | session_estimate（未收口） |

## 下一步

1. 监管人抽检 L31 / L01 / L14 / L13 / L17 / L51
2. 正式签收后再 MCP 推进；仍勿自行 `done`
