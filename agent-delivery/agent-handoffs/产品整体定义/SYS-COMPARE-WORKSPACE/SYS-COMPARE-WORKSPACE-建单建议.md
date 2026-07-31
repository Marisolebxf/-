# SYS-COMPARE-WORKSPACE：系统级对比工作台建单建议

> 状态：待 PM 采纳；本文件不是正式任务台账，不产生认领、解锁或飞书状态变更。
>
> 发起：高颖（体验 Owner）；建议 PM：郭万迎；架构会签：徐滕强 / 李伟。

## 1. 立项边界

将现有企业专属 `ENT-COMPARE` 的“对象暂存与分发”模式提升为系统级**统一对象工作台**。首批接入域为：企业分析、产业链分析、政策分析、产业服务链分析、综合智能分析。

系统级工作台只负责：

- 按对象域分别暂存、恢复、去重和管理待比较对象；
- 记录来源页面、筛选/分析上下文、数据批次与最近操作时间；
- 将同域对象交给其所属模块的对比/分析配置与结果页；
- 统一处理容量、对象失效、无权限、跨域不可比和返回上下文状态。

它不负责生成跨域统一评分、雷达图、结论或报告；对比结果、指标、权重和可比规则仍由各业务模块负责。禁止把企业篮的对象键、50 家容量或分析类型硬套到其他域。

## 2. 范围与来源判定

| 首批域 | 可回溯的原始能力 | 判定 |
|---|---|---|
| 企业分析 | 多企业技术力横向对比：`科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.3.3 | `direct_requirement`（企业域对比） |
| 产业链分析 | 深圳产业情况分析对比：§1.1.1.2.4.2.2.6 | `direct_requirement`（产业链域对比） |
| 政策分析 | 多维政策对比：`科技信息展示系统(政策对比功能升级)核增需求.md` §1.1.1.1.4.2.4.3 | `direct_requirement`（政策域对比） |
| 产业服务链分析 | 深圳服务链现状分析的横向对比：`科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.7.8 | `direct_requirement`（服务链域对比） |
| 综合智能分析 | 战略分析模块清单包含“综合智能分析”：§1.1.1.2.4.1（5）；尚未找到其对象与对比机制的细化 Bid 叶子 | 模块存在为 `direct_requirement`；接入对象为 🔴 `source_gap` |

跨模块共用的对象工作台、统一暂存协议和跨页上下文不是上述 Bid 的明确业务叶子，统一列为 `product_enhancement`。正式入库前必须取得 `approved_scope_change_ref`，并补足“综合智能分析”的精确 Bid 锚点或明确其不在首批范围。

## 3. 建议任务链（供 PM 转入 registry-gap-proposals）

| 顺序 | 建议任务 ID | 阶段 / 责任 | 依赖与交付 |
|---|---|---|---|
| 1 | `SYS-COMPARE-WORKSPACE-PACK-L01` | `definition` / product-agent，高颖共创 | IA、TRACE、USM、Wireframe；登记五域接入矩阵、跨域禁止规则、精确 Bid 锚点与增强项 |
| 2a | `SYS-COMPARE-WORKSPACE-METRIC-OPEN-L01` | `definition` / algorithm-agent + data-agent | 对象键、可比性前置、数据批次、指标/来源血缘与未决 Q 项；依赖 PACK |
| 2b | `SYS-COMPARE-WORKSPACE-UX-L01` | `definition` / ux-agent，高颖会签 | 统一入口、域切换、暂存/恢复、空/失效/无权/跨域不可比状态；依赖 PACK |
| 3 | `SYS-COMPARE-WORKSPACE-V1-HIFI-R1` | `definition` / ui-agent | 五域中至少企业、产业链、政策三个真实入口的共用流程验证；依赖 2a、2b |
| 4 | `SYS-COMPARE-WORKSPACE-PDR-G1` | `definition` / product-agent，郭万迎主持 | 四件套、数据/对象契约、V1 反馈、范围增强授权完整闭合；依赖 2a、3、`approved_scope_change_ref` |
| 5 | `SYS-COMPARE-WORKSPACE-V1-FINAL` | `definition` / product-agent + 高颖 | PDR 和 V1 联合修订冻结；依赖 PDR-G1 |
| 6 | `SYS-COMPARE-WORKSPACE-V2-LUMEN` | `implementation` / frontend-agent + api-agent | 共享前端工作台与 `/topic/v1/{element}/*` 聚合契约接线；依赖 V1-FINAL |

所有建议任务初始状态只能为 `backlog`。不得从飞书新增行、拖拽或本草案直接变更正式台账。

## 4. V1 可验收的最小闭环

1. 三个真实入口（企业、产业链、政策）可加入对应域的暂存区并恢复；
2. 同一域内的对象去重、来源和数据批次可追溯；
3. 每个域只展示该域允许的对比/分析动作；跨域混选明确阻止并说明原因；
4. 对象失效、无权限、数据批次不一致和空工作台均有可验证状态；
5. 产业服务链接入以现有原始范围为准；综合智能分析在来源缺口闭合前不进入 V1 验收。

## 5. 采纳前待决事项

- PM / 决策 Owner：为系统级工作台登记 `approved_scope_change_ref`；
- 综合智能分析 Owner：提供精确 Bid 章节、验收单元和对象类型；
- 架构 Owner：确认统一契约挂在 `gkxlumen-topic` 聚合核心，避免各域重复直连算法；
- 数据 / 语义 Owner：确认各域对象主键、可比性条件和数据批次的一致性规则；
- 高颖 / 孔东：确定 Track-MS `medium_1440_1920` 的 V1 交互与可实现性会签。

## 6. 与既有企业对比篮的关系

`ENT-MOD-COMPARE-*` 仍只处理企业域的既有 PDR、V1-FINAL 与 V2 会签，不迁移、不覆盖、不修改其在修订中的四件套。待本系统级 PACK 冻结后，企业篮作为首个适配器接入；其余四域各自按其原始需求与对象契约接入。
