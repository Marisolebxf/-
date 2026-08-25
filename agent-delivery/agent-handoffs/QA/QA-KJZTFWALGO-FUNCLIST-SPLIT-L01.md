# QA-KJZTFWALGO-FUNCLIST-SPLIT-L01 · 进度保存（暂停）

> 本文件是 **暂停节点**，不是完工 handoff。F–L 指标明确后继续补点，再写正式收口。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |
| agent | `qa-agent` |
| status | `in_progress`（暂停；勿自行 `done`） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 拆点/合表文档，不缩 D8/D9/D10。 |

## 范围与实现

- 输入：功能清单 v1.2 · sheet「深度挖掘算法」· 四级「科技专题服务算法库」· **60 六级**
- 编号：`ZNFWJQ-KJZTFWALGO-v1.0-FUNC-#####`
- 合表 v1：3347 条；A1=`智能服务集群-科技专题服务算法库功能点拆分`
- 拆法：v1.3 → v1.4 加深 → v1.5 口径 B；**不开口径 C**

## 偏离说明

- 总集要求 **3889**，v1 为 **3347**（差额 542）
- 监管人 2026-08-25：不用判定依据（口径 C）灌水；待算法库指标开发识别出 **F–L 指标**后再按点名指标补功能点
- 同 sheet 其余约 52 条六级仍不纳入

## 产物清单

| 产物 | 路径 |
|---|---|
| 合表 Excel v1 | `agent-delivery/qa/total-set/KJZTFWALGO/6.国际科技信息中心项目_科技专题服务算法库_功能点拆分_v1.xlsx` |
| 原则 | `…/科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md` |
| 中间稿 | `fp-split-run/work/` `review/` `prompts/` `00-control.md` `01-task-list.md` |
| 合表/核对脚本 | `agent-delivery/scripts/_merge_kjztfwalgo_fp_split_work.py` · `_check_kjztfwalgo_fp_work.py` · `_gen_kjztfwalgo_fp_split_prompts.py` |
| 本机快照（不入库） | `fp-split-run/snapshots/v1/` |

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python / 不写界面功能点 | ✅ |
| 调用链 / Nebula / 可观测 | N/A（拆点文档） |
| D12 demo 不入库 lumen | ✅ |
| 未读 demo-algo / lumen-algo / 五件套增减点 | ✅ |

## cost（暂停节点）

| 字段 | 值 |
|---|---|
| actual_tokens | 未回填 Console |
| model_used | Cursor Grok 4.6 |
| actual_cost | 未回填 |
| cost_warn | n/a |
| source | session_estimate（暂停，待收口再填） |

## 下一步

1. 等 F–L 指标清单明确
2. 按点名指标补功能点（禁止口径 C、禁止未点名指标）
3. 另存合表 v2（禁止覆盖 v1）
4. 正式 handoff + MCP 推进；仍勿自行 `done`
