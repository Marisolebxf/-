# E8-综合智能分析（专题服务系统 §1.1.1.2.4.2.8）

> **registry**：Epic `E8-综合智能分析` · 任务 `TOPIC-SYNTH-R3`
> **范围真源**：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.8（8.1 区域创新活力分析 / 8.2 区域创新要素分析 / 8.3 区域创新协同分析，共 9 个三级项）
> **实现仓**：`${GKX_ROOT}/repos/demo-ui-topic` `src/app/pages/intelligence/`（push origin/dev）

## 叶子划分

综合智能分析三个二级功能（活力 / 要素 / 协同）共享同一"区域"分析对象与同一"看整体—析要素—促协同"闭环叙事（Bid §2.4.2.8 总述明示），拆开会切断下钻链路的产品语义，故收为 **1 个叶子**：

| 叶子 | 代号 | 覆盖 Bid 条目 | 五件套 |
| --- | --- | --- | --- |
| 区域创新分析 | `SYNTH-REGION` | 8.1.1–8.1.3、8.2.1–8.2.3、8.3.1–8.3.3（9 项全量） | `SYNTH-REGION-区域创新分析/` |

## 指标与开放项前缀

- 指标：`M_SYNTH_*`（只读镜像：demo-ui-topic `src/app/pages/intelligence/intelReadinessSeed.ts`）
- 开放项：`Q-SYNTH-01`（活力指标体系+综合评价模型）、`Q-SYNTH-02`（要素评价模型+贡献度关联算法）、`Q-SYNTH-03`（协同度计算模型+协同-产出相关性口径），已登记 `客户决策清单跟踪表.md`
- 跨模块契约：`CT-SYN-01`（图谱企业节点 → 企业统一画像）、`CT-SYN-02`（图谱服务机构节点 → E7 机构画像）、`CT-SYN-03`（生成分析报告 → 系统报告面）

## 文档清单

- `SYNTH-REGION-区域创新分析/USM-SYNTH-REGION.md`
- `SYNTH-REGION-区域创新分析/IA-SYNTH-REGION.md`
- `SYNTH-REGION-区域创新分析/Wireframe-SYNTH-REGION.md`
- `SYNTH-REGION-区域创新分析/UX-SPEC-SYNTH-REGION.md`
- `SYNTH-REGION-区域创新分析/TRACE-SYNTH-REGION.yaml`
