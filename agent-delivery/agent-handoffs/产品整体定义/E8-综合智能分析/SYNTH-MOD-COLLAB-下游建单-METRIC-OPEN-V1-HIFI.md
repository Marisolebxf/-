# SYNTH-MOD-COLLAB 下游建单记录（METRIC-OPEN + V1-HIFI）

> **时间**：2026-08-10  
> **触发**：`human:淮政玮` 确认 Pack1 会签通过并授权回填 cost  
> **操作**：`agent:product-agent`（经监管确认执行 registry）

## Pack1

| ID | 动作 |
| --- | --- |
| `SYNTH-MOD-COLLAB-PACK-L01` | `blocked` → cost 回填 → `integration` → `ready_to_sign` → **`done`**（actor=`human:淮政玮`） |
| cost | `actual_tokens≈200000` / `model_used=Cursor Grok 4.5` / `actual_cost≈$2.8` / `cost_warn=green` |

## 新建并认领

| ID | status | agent | claimed_by / supervised_by | depends_on | repo |
| --- | --- | --- | --- | --- | --- |
| `SYNTH-MOD-COLLAB-METRIC-OPEN-L01` | claimed | algorithm-agent（协作 data-agent） | **human:王惠** | PACK done | gkx-orchestration |
| `SYNTH-MOD-COLLAB-V1-HIFI` | claimed | ui-agent（协作 frontend-agent） | **human:淮政玮** | PACK done | demo-ui-topic |

## 说明

- METRIC-OPEN：口径主责王惠；算法共签仍按方案 B 挂唐绍祖（DoD 写明）。  
- V1-HIFI：可与 METRIC-OPEN **并行**；消费 Pack1 五件套；禁止「密度×强度」冒充正式公式。  
- 派单包：`SYNTH-MOD-COLLAB-V1-HIFI-派单包.md`（含 §6 粘贴话术）  
- `SYNTH-MOD-COLLAB-PDR-G1` **未建**（仍待 METRIC-OPEN + UX 可评）。
