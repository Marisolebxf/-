# E8-综合智能分析（专题服务系统 §1.1.1.2.4.2.8）

> **registry（定义轨）**：`SYNTH-MOD-VITALITY-PACK-L01` · `SYNTH-MOD-ELEMENT-PACK-L01` · `SYNTH-MOD-COLLAB-PACK-L01`（2026-08-10 修正拆叶；见总包）  
> **历史任务**：`TOPIC-SYNTH-R3`（单叶捆交付，**产品定义权威已废止**，实现仅参照）  
> **系统方案真源**：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.8  
> **算法库真源**：`bid-reference/科技专题服务算法库.md` §1.1.1.1.1.1.1.10「产业综合分析模型构建」  
> **实现仓（历史/后续 V1）**：`${GKX_ROOT}/repos/demo-ui-topic` `src/app/pages/intelligence/`

## 叶子划分（现行）

按系统方案三个二级功能拆为 **3 个叶子**；共享区域上下文契约 `CT-SYN-CTX`，但验收与算法专章分叶闭合（修正原「单叶 SYNTH-REGION」决策）。

| 叶子 | 代号 | 系统方案 | 算法库 | Pack1 | 目录 |
| --- | --- | --- | --- | --- | --- |
| 区域创新活力分析 | `SYNTH-VITALITY` | §8.1.1–8.1.3 | §10.5（输入参照 §10.1–10.4） | `SYNTH-MOD-VITALITY-PACK-L01` | `SYNTH-VITALITY-区域创新活力分析/` |
| 区域创新要素分析 | `SYNTH-ELEMENT` | §8.2.1–8.2.3 | §10.6–10.9 | `SYNTH-MOD-ELEMENT-PACK-L01` | `SYNTH-ELEMENT-区域创新要素分析/` |
| 区域创新协同分析 | `SYNTH-COLLAB` | §8.3.1–8.3.3 | §10.10 | `SYNTH-MOD-COLLAB-PACK-L01` | `SYNTH-COLLAB-区域创新协同分析/` |

## 派单包

- `TOPIC-SYNTH-R3-修正拆叶-Pack1派单总包.md`
- `SYNTH-MOD-VITALITY-PACK-L01-派单包.md`
- `SYNTH-MOD-ELEMENT-PACK-L01-派单包.md`
- `SYNTH-MOD-COLLAB-PACK-L01-派单包.md`
- `SYNTH-三叶子-PACK-L01-registry-提案.md`

## 指标与开放项前缀

| 叶子 | metric 建议前缀 | 开放项 |
| --- | --- | --- |
| 活力 | `M_SYNTH_VIT_*` / 沿用部分 `M_SYNTH_VITALITY_*` | `Q-SYNTH-01` + `Q-SYNTH-V-*` |
| 要素 | `M_SYNTH_ELEM_*` | `Q-SYNTH-02` + `Q-SYNTH-E-*` |
| 协同 | `M_SYNTH_COLLAB_*` | `Q-SYNTH-03` + `Q-SYNTH-C-*` |

跨模块契约：`CT-SYN-01`（企业画像）、`CT-SYN-02`（机构画像）、`CT-SYN-03`（报告面）、**`CT-SYN-CTX`（区域/对比/时间窗共享）**。

## lumen 实现注意（必读）

- **`SYNTH-系统任务队列-lumen实现注意.md`** — 同条件禁止重复入队、切回菜单维持过程/结果态、fingerprint /「开始分析」决策表、Demo 参照路径与交付检查清单。正式仓（`lumen-ui-topic` 等）接 `SYS-ANALYSIS-JOBS` 前先读此文。

## 历史目录（非权威）

- `SYNTH-REGION-区域创新分析/` — R3 单叶五件套，**仅历史参照**，见目录内废止说明。
